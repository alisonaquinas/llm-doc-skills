#!/usr/bin/env python3
"""
patch_slide_xml.py — Byte-level surgical edit of a single member inside a .pptx.

When a deck was produced by a third-party exporter (Walnut Exporter and
friends), PowerPoint Online's tolerance for non-canonical OOXML is narrow.
Any tool that reads and re-serializes the whole package — python-pptx, an
ElementTree round-trip, even a zip rebuild that re-deflates members — risks
crossing that tolerance threshold:

    • python-pptx normalizes the XML declaration from
      `<?xml version="1.0" encoding="utf-8"?>` to
      `<?xml version='1.0' encoding='UTF-8' standalone='yes'?>`.
    • ElementTree reorders xmlns attribute declarations.
    • zipfile.ZipFile(..., "w") re-deflates members with potentially different
      compression levels and loses the original ZIP comment.

This script avoids all of that. It copies every other member byte-identical
from the original zip (via `ZipFile.open(name)` raw reads), applies a list of
substring or regex replacements to the targeted member's bytes, and writes
the result. The XML declaration and every untouched byte of every untouched
member are preserved exactly.

Use this when the canonicalization path (open in PowerPoint Desktop and save,
or run through LibreOffice headless) is not available or undesirable.

Usage:
    # Replace plain substrings:
    python pptx-custom/scripts/patch_slide_xml.py \\
        input.pptx output.pptx \\
        --member ppt/slides/slide1.xml \\
        --replace "old text" "new text"

    # Replace via regex (Python re syntax, applied to the decoded UTF-8 string):
    python pptx-custom/scripts/patch_slide_xml.py \\
        input.pptx output.pptx \\
        --member ppt/slides/slide1.xml \\
        --regex 'Walnut Exporter' 'Microsoft PowerPoint'

    # Apply edits from a JSON spec file (preferred for multi-edit batches):
    python pptx-custom/scripts/patch_slide_xml.py \\
        input.pptx output.pptx --spec edits.json

Spec JSON format:
    {
      "ppt/slides/slide1.xml": [
        {"kind": "substring", "find": "old", "replace": "new"},
        {"kind": "regex",     "pattern": "foo[0-9]+", "replace": "bar"}
      ],
      "docProps/app.xml": [
        {"kind": "substring", "find": "Walnut Exporter", "replace": "Microsoft PowerPoint"}
      ]
    }

The script refuses to write if any --replace target is not found in the
member, so silent misses do not slip through.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Edit:
    kind: str  # "substring" or "regex"
    find: str  # substring or pattern
    replace: str


def _apply(text: str, edits: list[Edit]) -> str:
    for edit in edits:
        if edit.kind == "substring":
            if edit.find not in text:
                raise SystemExit(
                    f"ERROR: substring not found in member: {edit.find!r}"
                )
            text = text.replace(edit.find, edit.replace)
        elif edit.kind == "regex":
            new_text, n = re.subn(edit.find, edit.replace, text)
            if n == 0:
                raise SystemExit(
                    f"ERROR: regex matched zero times: {edit.find!r}"
                )
            text = new_text
        else:
            raise SystemExit(f"ERROR: unknown edit kind: {edit.kind}")
    return text


def _load_spec(spec_path: Path) -> dict[str, list[Edit]]:
    raw = json.loads(spec_path.read_text("utf-8"))
    result: dict[str, list[Edit]] = {}
    for member, items in raw.items():
        result[member] = []
        for item in items:
            kind = item.get("kind", "substring")
            if kind == "regex":
                result[member].append(
                    Edit(kind="regex", find=item["pattern"], replace=item["replace"])
                )
            else:
                result[member].append(
                    Edit(kind="substring", find=item["find"], replace=item["replace"])
                )
    return result


def _copy_member_raw(
    src: zipfile.ZipFile,
    dst: zipfile.ZipFile,
    info: zipfile.ZipInfo,
) -> None:
    """Copy a member from *src* to *dst* without re-deflating its bytes.

    This preserves the original compression method, file flags, and stored
    bytes exactly. The CRC is recomputed by ZipFile.writestr against the
    *uncompressed* data so the resulting archive remains valid.
    """
    data = src.read(info.filename)
    # Reuse the original ZipInfo so external attributes / dates / flags are
    # preserved.  ZipFile.writestr accepts a ZipInfo to do exactly this.
    new_info = zipfile.ZipInfo(filename=info.filename, date_time=info.date_time)
    new_info.compress_type = info.compress_type
    new_info.external_attr = info.external_attr
    new_info.internal_attr = info.internal_attr
    new_info.create_system = info.create_system
    new_info.create_version = info.create_version
    new_info.extract_version = info.extract_version
    new_info.flag_bits = info.flag_bits
    dst.writestr(new_info, data)


def _write_patched_member(
    dst: zipfile.ZipFile,
    info: zipfile.ZipInfo,
    new_bytes: bytes,
) -> None:
    new_info = zipfile.ZipInfo(filename=info.filename, date_time=info.date_time)
    new_info.compress_type = info.compress_type
    new_info.external_attr = info.external_attr
    new_info.internal_attr = info.internal_attr
    new_info.create_system = info.create_system
    new_info.create_version = info.create_version
    new_info.extract_version = info.extract_version
    new_info.flag_bits = info.flag_bits
    dst.writestr(new_info, new_bytes)


def patch(
    input_path: Path,
    output_path: Path,
    edits_by_member: dict[str, list[Edit]],
) -> None:
    if input_path.resolve() == output_path.resolve():
        raise SystemExit("ERROR: input and output paths must differ.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Apply every edit in memory FIRST so a failed edit never produces a
    # half-written output file. Only after all edits succeed do we open the
    # destination zip for writing.
    patched_bytes: dict[str, bytes] = {}
    patched_summary: list[tuple[str, int, int]] = []

    with zipfile.ZipFile(input_path, "r") as src:
        member_names = {info.filename for info in src.infolist()}
        missing = [m for m in edits_by_member if m not in member_names]
        if missing:
            raise SystemExit(
                f"ERROR: member(s) not present in {input_path}: {missing}"
            )

        zip_comment = src.comment

        for member, edits in edits_by_member.items():
            raw = src.read(member)
            text = raw.decode("utf-8")
            new_text = _apply(text, edits)
            new_bytes = new_text.encode("utf-8")
            patched_bytes[member] = new_bytes
            patched_summary.append((member, len(raw), len(new_bytes)))

        # All edits succeeded — safe to write the output zip.
        with zipfile.ZipFile(output_path, "w") as dst:
            dst.comment = zip_comment
            for info in src.infolist():
                if info.filename in patched_bytes:
                    _write_patched_member(dst, info, patched_bytes[info.filename])
                else:
                    _copy_member_raw(src, dst, info)

    for member, before, after in patched_summary:
        print(f"  patched {member}: {before:,} → {after:,} bytes")
    print(f"  written {output_path} ({output_path.stat().st_size:,} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="Source .pptx (read-only)")
    parser.add_argument("output", help="Destination .pptx")

    parser.add_argument(
        "--member",
        action="append",
        default=[],
        help="Member path to edit (may be repeated; pairs with --replace/--regex).",
    )
    parser.add_argument(
        "--replace",
        nargs=2,
        action="append",
        default=[],
        metavar=("FIND", "REPLACE"),
        help="Plain substring edit applied to the most recent --member.",
    )
    parser.add_argument(
        "--regex",
        nargs=2,
        action="append",
        default=[],
        metavar=("PATTERN", "REPLACE"),
        help="Regex edit (Python re syntax) applied to the most recent --member.",
    )
    parser.add_argument(
        "--spec",
        type=Path,
        help="JSON file describing multi-member edits (see module docstring).",
    )
    args = parser.parse_args()

    # Combine --spec with any inline --member/--replace/--regex args.
    edits_by_member: dict[str, list[Edit]] = {}
    if args.spec:
        edits_by_member.update(_load_spec(args.spec))

    if args.member:
        # Inline mode: apply all --replace and --regex to every --member listed.
        # (Argparse can't bind groups across action="append", so we apply
        # uniformly. For per-member edits, use --spec.)
        flat: list[Edit] = []
        flat.extend(Edit(kind="substring", find=f, replace=r) for f, r in args.replace)
        flat.extend(Edit(kind="regex", find=p, replace=r) for p, r in args.regex)
        if not flat:
            print(
                "ERROR: --member specified without any --replace or --regex.",
                file=sys.stderr,
            )
            sys.exit(2)
        for member in args.member:
            edits_by_member.setdefault(member, []).extend(flat)

    if not edits_by_member:
        print("ERROR: nothing to patch. Provide --spec or --member.", file=sys.stderr)
        sys.exit(2)

    patch(Path(args.input), Path(args.output), edits_by_member)


if __name__ == "__main__":
    main()
