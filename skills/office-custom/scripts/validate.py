#!/usr/bin/env python3
"""
validate.py — Validate an Office Open XML file (.docx / .pptx / .xlsx).

Performs three checks:
  1. ZIP integrity  — the file can be opened as a valid ZIP archive.
  2. XML well-formedness — every .xml and .rels member parses without error.
  3. Required parts   — the mandatory [Content_Types].xml and _rels/.rels
                        entries are present.

Exits with code 0 if all checks pass, non-zero otherwise.

Usage:
    python office-custom/scripts/validate.py document.docx
    python office-custom/scripts/validate.py presentation.pptx
    python office-custom/scripts/validate.py spreadsheet.xlsx

Options:
    --quiet   Suppress per-file output; only print summary.
"""

import argparse
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

# Parts that MUST be present in any valid OOXML package.
_REQUIRED_PARTS = ["[Content_Types].xml", "_rels/.rels"]


def validate(source: Path, quiet: bool = False) -> bool:
    """Validate *source* and return True if it passes all checks.

    Args:
        source: Path to a .docx / .pptx / .xlsx file.
        quiet:  If True, suppress per-member output.

    Returns:
        True if the file is valid, False otherwise.
    """
    source = Path(source)
    if not source.exists():
        print(f"ERROR: File not found: {source}")
        return False

    errors: list[str] = []
    warnings: list[str] = []

    # ------------------------------------------------------------------
    # Check 1: ZIP integrity
    # ------------------------------------------------------------------
    try:
        zf = zipfile.ZipFile(source, "r")
    except zipfile.BadZipFile as exc:
        print(f"ERROR: Not a valid ZIP/OOXML file: {exc}")
        return False

    with zf:
        member_names = zf.namelist()

        # ------------------------------------------------------------------
        # Check 2: Required parts
        # ------------------------------------------------------------------
        for part in _REQUIRED_PARTS:
            if part not in member_names:
                errors.append(f"Missing required part: {part}")

        # ------------------------------------------------------------------
        # Check 3: XML well-formedness
        # ------------------------------------------------------------------
        xml_ok = 0
        xml_bad = 0
        for name in member_names:
            if not (name.endswith(".xml") or name.endswith(".rels")):
                continue
            try:
                raw = zf.read(name)
                ET.fromstring(raw)
                xml_ok += 1
                if not quiet:
                    pass  # Don't print every OK file — too noisy.
            except ET.ParseError as exc:
                xml_bad += 1
                errors.append(f"XML parse error in {name}: {exc}")

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------
    label = source.name
    if errors:
        print(f"FAIL  {label}")
        for err in errors:
            print(f"      ERROR: {err}")
        return False

    if warnings:
        print(f"WARN  {label}")
        for warn in warnings:
            print(f"      WARN: {warn}")
        return True

    if not quiet:
        print(f"OK    {label}  ({xml_ok} XML members validated)")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("files", nargs="+", help="Files to validate")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-file output")
    args = parser.parse_args()

    all_passed = True
    for path_str in args.files:
        passed = validate(Path(path_str), quiet=args.quiet)
        if not passed:
            all_passed = False

    if len(args.files) > 1:
        status = "All passed" if all_passed else "Some checks FAILED"
        print(f"\n{status} ({len(args.files)} files checked)")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
