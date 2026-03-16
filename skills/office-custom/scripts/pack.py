#!/usr/bin/env python3
"""
pack.py — Repack an edited OOXML directory back into a .docx / .pptx / .xlsx.

Takes a directory previously unpacked by unpack.py, validates and auto-repairs
common XML issues, condenses the pretty-printed XML back to compact form, and
zips everything into a valid Office Open XML file.

Auto-repair fixes:
  • durableId values >= 0x7FFFFFFF — regenerates a valid 31-bit integer.
  • Missing xml:space="preserve" on <w:t> elements that contain leading or
    trailing whitespace (Word will silently strip the spaces otherwise).

Usage:
    python office-custom/scripts/pack.py unpacked/ output.docx --original document.docx
    python office-custom/scripts/pack.py unpacked/ output.pptx --original presentation.pptx
    python office-custom/scripts/pack.py unpacked/ output.xlsx --original spreadsheet.xlsx

Options:
    --original PATH   Path to the original file.  Required so that the correct
                      ZIP comment and Content_Types are preserved.
    --validate        Run validate.py after packing (default: true).
    --no-validate     Skip validation.
"""

import argparse
import random
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------------------
# Auto-repair helpers
# ---------------------------------------------------------------------------

# Maximum allowed durableId (Word rejects values >= 0x7FFFFFFF).
_DURABLE_ID_MAX = 0x7FFFFFFF


def fix_durable_ids(text: str) -> tuple[str, int]:
    """Replace out-of-range w:durableId values with valid random IDs.

    Word uses 31-bit unsigned integers for durableId.  Values >= 0x7FFFFFFF
    (2147483648) are invalid and cause Word to fail on open.

    Args:
        text: XML content as a string.

    Returns:
        Tuple of (fixed_text, number_of_replacements).
    """
    count = 0

    def replacer(match: re.Match) -> str:
        nonlocal count
        val = int(match.group(1))
        if val >= _DURABLE_ID_MAX:
            new_val = random.randint(1, _DURABLE_ID_MAX - 1)
            count += 1
            return f'w:durableId="{new_val}"'
        return match.group(0)

    fixed = re.sub(r'w:durableId="(\d+)"', replacer, text)
    return fixed, count


def fix_xml_space_preserve(text: str) -> tuple[str, int]:
    """Add xml:space="preserve" to <w:t> elements missing it when needed.

    Word silently strips leading/trailing whitespace from <w:t> elements
    unless xml:space="preserve" is present.  This is required whenever the
    text content starts or ends with a space character.

    Args:
        text: XML content as a string.

    Returns:
        Tuple of (fixed_text, number_of_replacements).
    """
    count = 0

    def replacer(match: re.Match) -> str:
        nonlocal count
        tag_open = match.group(1)  # e.g. '<w:t>' or '<w:t foo="bar">'
        content = match.group(2)

        # Only add if content has leading/trailing whitespace.
        if content and (content[0] == " " or content[-1] == " "):
            if 'xml:space' not in tag_open:
                count += 1
                # Insert attribute before the closing >.
                tag_open = tag_open.rstrip(">") + ' xml:space="preserve">'
        return f"{tag_open}{content}</w:t>"

    fixed = re.sub(r"(<w:t(?:\s[^>]*)?>)(.*?)</w:t>", replacer, text, flags=re.DOTALL)
    return fixed, count


# ---------------------------------------------------------------------------
# XML condensing
# ---------------------------------------------------------------------------

def condense_xml(text: str) -> bytes:
    """Remove pretty-print indentation to produce compact XML bytes.

    Re-parses the XML and re-serialises without extra whitespace.  Preserves
    the xml:space="preserve" attribute semantics because ElementTree honours
    them during serialisation.

    Args:
        text: Pretty-printed XML string.

    Returns:
        Compact XML as UTF-8 bytes, with an XML declaration.
    """
    # Register all known OOXML namespaces to avoid ns0: prefixes.
    _NAMESPACES = {
        "wpc":  "http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas",
        "cx":   "http://schemas.microsoft.com/office/drawing/2014/chartex",
        "mc":   "http://schemas.openxmlformats.org/markup-compatibility/2006",
        "aink": "http://schemas.microsoft.com/office/drawing/2016/ink",
        "am3d": "http://schemas.microsoft.com/office/drawing/2017/model3d",
        "o":    "urn:schemas-microsoft-com:office:office",
        "r":    "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "m":    "http://schemas.openxmlformats.org/officeDocument/2006/math",
        "v":    "urn:schemas-microsoft-com:vml",
        "wp14": "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
        "wp":   "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
        "w10":  "urn:schemas-microsoft-com:office:word",
        "w":    "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "w14":  "http://schemas.microsoft.com/office/word/2010/wordml",
        "w15":  "http://schemas.microsoft.com/office/word/2012/wordml",
        "w16cid": "http://schemas.microsoft.com/office/word/2016/wordml/cid",
        "w16se": "http://schemas.microsoft.com/office/word/2015/wordml/symex",
        "wpg":  "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",
        "wpi":  "http://schemas.microsoft.com/office/word/2010/wordprocessingInk",
        "wne":  "http://schemas.microsoft.com/office/word/2006/wordml",
        "wps":  "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
        "a":    "http://schemas.openxmlformats.org/drawingml/2006/main",
        "p":    "http://schemas.openxmlformats.org/presentationml/2006/main",
        "xdr":  "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
        "x":    "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    }
    for prefix, uri in _NAMESPACES.items():
        ET.register_namespace(prefix, uri)

    try:
        root = ET.fromstring(text.encode("utf-8"))
        return ET.tostring(root, encoding="utf-8", xml_declaration=True)
    except ET.ParseError:
        # If the XML can't be re-parsed, fall back to raw bytes.
        return text.encode("utf-8")


# ---------------------------------------------------------------------------
# Main packing logic
# ---------------------------------------------------------------------------

def pack(
    unpacked_dir: Path,
    output: Path,
    original: Path | None = None,
    validate: bool = True,
) -> None:
    """Repack *unpacked_dir* into *output*.

    Args:
        unpacked_dir: Directory produced by unpack.py.
        output:       Destination .docx / .pptx / .xlsx path.
        original:     Original source file (used to copy ZIP metadata/comment).
        validate:     If True, run validate.py after packing.
    """
    unpacked_dir = Path(unpacked_dir)
    output = Path(output)

    if not unpacked_dir.exists():
        raise FileNotFoundError(f"Unpacked directory not found: {unpacked_dir}")

    output.parent.mkdir(parents=True, exist_ok=True)

    # Collect all files in the unpacked directory.
    all_files = sorted(
        p for p in unpacked_dir.rglob("*") if p.is_file()
    )

    repair_stats = {"durable_ids": 0, "xml_space": 0}
    print(f"Packing {unpacked_dir}/ → {output}")

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # [Content_Types].xml must be the first entry in an OOXML ZIP.
        content_types = unpacked_dir / "[Content_Types].xml"
        if content_types.exists():
            _write_member(zf, content_types, unpacked_dir, repair_stats)

        for member in all_files:
            if member == content_types:
                continue  # Already written first.
            _write_member(zf, member, unpacked_dir, repair_stats)

    if repair_stats["durable_ids"]:
        print(f"  Auto-repaired {repair_stats['durable_ids']} out-of-range durableId(s).")
    if repair_stats["xml_space"]:
        print(f"  Auto-added xml:space=\"preserve\" to {repair_stats['xml_space']} <w:t> element(s).")

    print(f"  Written {output.stat().st_size:,} bytes.")

    if validate:
        _run_validate(output)


def _write_member(
    zf: zipfile.ZipFile,
    member: Path,
    base: Path,
    repair_stats: dict,
) -> None:
    """Write a single file into the ZIP, applying auto-repair if XML."""
    arc_name = member.relative_to(base).as_posix()

    if member.suffix in (".xml", ".rels"):
        text = member.read_text(encoding="utf-8", errors="replace")

        # Auto-repair pass 1: fix out-of-range durableId values.
        text, n = fix_durable_ids(text)
        repair_stats["durable_ids"] += n

        # Auto-repair pass 2: add missing xml:space="preserve".
        text, n = fix_xml_space_preserve(text)
        repair_stats["xml_space"] += n

        data = condense_xml(text)
    else:
        data = member.read_bytes()

    zf.writestr(arc_name, data)


def _run_validate(output: Path) -> None:
    """Run validate.py on the packed file (best-effort; errors are reported)."""
    import subprocess
    import sys
    validate_script = Path(__file__).parent / "validate.py"
    if validate_script.exists():
        result = subprocess.run(
            [sys.executable, str(validate_script), str(output)],
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print(result.stdout.rstrip())
        if result.returncode != 0 and result.stderr:
            print(result.stderr.rstrip())


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("unpacked_dir", help="Directory produced by unpack.py")
    parser.add_argument("output", help="Output .docx / .pptx / .xlsx path")
    parser.add_argument(
        "--original",
        help="Path to the original file (optional; used for metadata)",
    )
    parser.add_argument(
        "--validate",
        default="true",
        choices=["true", "false"],
        help="Run validate.py after packing (default: true)",
    )
    args = parser.parse_args()

    pack(
        unpacked_dir=Path(args.unpacked_dir),
        output=Path(args.output),
        original=Path(args.original) if args.original else None,
        validate=(args.validate == "true"),
    )


if __name__ == "__main__":
    main()
