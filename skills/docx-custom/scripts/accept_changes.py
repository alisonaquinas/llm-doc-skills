#!/usr/bin/env python3
"""
accept_changes.py — Accept all tracked changes in a Word document (.docx).

Tracked changes in OOXML are represented as revision-markup elements:
  - <w:ins>  — inserted text (accept = keep the run, drop the w:ins wrapper)
  - <w:del>  — deleted text (accept = remove the run entirely)

After acceptance the document no longer contains any revision markup and can
be saved as a clean, review-free copy.

Usage:
    python docx-custom/scripts/accept_changes.py input.docx output.docx

Options:
    --in-place   Overwrite the input file (no output path required).
    --dry-run    Report how many insertions / deletions would be accepted,
                 then exit without writing any file.

Exit codes:
    0  — Success (or dry-run completed).
    1  — Input file not found or not a valid .docx.
    2  — XML processing error.
"""

import argparse
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------------------
# OOXML namespace URIs used by tracked-change elements
# ---------------------------------------------------------------------------

# The "w:" prefix maps to the main WordprocessingML namespace.
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# Convenience helpers so we can write _w("ins") instead of the full Clark name.
def _w(local: str) -> str:
    """Return the Clark-notation tag name for a WordprocessingML element."""
    return f"{{{W_NS}}}{local}"


# Tags we need to recognise during traversal.
TAG_INS   = _w("ins")    # <w:ins>  — tracked insertion wrapper
TAG_DEL   = _w("del")    # <w:del>  — tracked deletion wrapper
TAG_DTEXT = _w("delText") # <w:delText> inside a <w:del> run

# Elements that may directly contain <w:ins> or <w:del> as children.
# We only process these containers to avoid touching nested structures we
# don't understand (e.g. change-tracking in table properties).
CONTAINER_TAGS = {
    _w("p"),    # paragraph
    _w("tr"),   # table row
    _w("tc"),   # table cell
}


# ---------------------------------------------------------------------------
# Core acceptance logic
# ---------------------------------------------------------------------------

def _accept_in_element(parent: ET.Element) -> tuple[int, int]:
    """
    Recursively accept tracked changes inside *parent*.

    For each child of *parent*:
      - <w:ins>  → unwrap: replace the <w:ins> with its children in-place.
      - <w:del>  → remove: delete the element entirely.

    Returns:
        (insertions_accepted, deletions_accepted)
    """
    ins_count = 0
    del_count = 0

    # We iterate over a snapshot of the current child list because we modify
    # *parent* in the loop.
    i = 0
    while i < len(parent):
        child = parent[i]

        if child.tag == TAG_INS:
            # Accept insertion: lift the children of <w:ins> into *parent*
            # at the same position, then remove the wrapper element.
            ins_children = list(child)
            # Insert the children right before position i.
            for j, ins_child in enumerate(ins_children):
                parent.insert(i + j, ins_child)
            parent.remove(child)
            ins_count += 1
            # Advance past the newly inserted children.
            i += len(ins_children)
            continue

        elif child.tag == TAG_DEL:
            # Accept deletion: remove the entire <w:del> element (the deleted
            # text was already gone from the reader's perspective).
            parent.remove(child)
            del_count += 1
            # Don't advance i — the next child has shifted into position i.
            continue

        else:
            # Recurse into non-tracked-change elements to handle nested markup.
            sub_ins, sub_del = _accept_in_element(child)
            ins_count += sub_ins
            del_count += sub_del

        i += 1

    return ins_count, del_count


def accept_tracked_changes_xml(xml_bytes: bytes) -> tuple[bytes, int, int]:
    """
    Accept all tracked changes in the XML content of a single OOXML part.

    Args:
        xml_bytes: Raw bytes of the XML member (e.g. ``word/document.xml``).

    Returns:
        (modified_xml_bytes, insertions_accepted, deletions_accepted)

    Raises:
        ET.ParseError: If *xml_bytes* is not well-formed XML.
    """
    # Register all known namespaces so ElementTree doesn't rewrite them as
    # ns0:, ns1:, etc., which would corrupt references elsewhere in the package.
    _register_namespaces()

    root = ET.fromstring(xml_bytes)
    ins_total, del_total = _accept_in_element(root)

    # Re-serialise back to bytes, preserving the original XML declaration if
    # present (ET.tostring omits it, so we re-add it manually).
    modified = ET.tostring(root, encoding="unicode", xml_declaration=False)
    modified_bytes = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n{modified}'.encode()

    return modified_bytes, ins_total, del_total


# ---------------------------------------------------------------------------
# Namespace registration
# ---------------------------------------------------------------------------

# Map of prefix → URI for all namespaces commonly found in .docx files.
# Without registering these, ElementTree serialises xmlns attributes using
# generated ns0/ns1/... prefixes, which breaks inter-part relationships.
_OOXML_NAMESPACES: dict[str, str] = {
    "wpc":   "http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas",
    "cx":    "http://schemas.microsoft.com/office/drawing/2014/chartex",
    "cx1":   "http://schemas.microsoft.com/office/drawing/2015/9/8/chartex",
    "cx2":   "http://schemas.microsoft.com/office/drawing/2015/10/21/chartex",
    "cx3":   "http://schemas.microsoft.com/office/drawing/2016/5/9/chartex",
    "cx4":   "http://schemas.microsoft.com/office/drawing/2016/5/10/chartex",
    "cx5":   "http://schemas.microsoft.com/office/drawing/2016/5/11/chartex",
    "cx6":   "http://schemas.microsoft.com/office/drawing/2016/5/12/chartex",
    "cx7":   "http://schemas.microsoft.com/office/drawing/2016/5/13/chartex",
    "cx8":   "http://schemas.microsoft.com/office/drawing/2016/5/14/chartex",
    "mc":    "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "aink":  "http://schemas.microsoft.com/office/drawing/2016/ink",
    "am3d":  "http://schemas.microsoft.com/office/drawing/2017/model3d",
    "o":     "urn:schemas-microsoft-com:office:office",
    "oel":   "http://schemas.microsoft.com/office/2019/extlst",
    "r":     "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "m":     "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "v":     "urn:schemas-microsoft-com:vml",
    "wp14":  "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
    "wp":    "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "w10":   "urn:schemas-microsoft-com:office:word",
    "w":     W_NS,
    "w14":   "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15":   "http://schemas.microsoft.com/office/word/2012/wordml",
    "w16cex":"http://schemas.microsoft.com/office/word/2018/wordml/cex",
    "w16cid":"http://schemas.microsoft.com/office/word/2016/wordml/cid",
    "w16":   "http://schemas.microsoft.com/office/word/2018/wordml",
    "w16sdtdh": "http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash",
    "w16se": "http://schemas.microsoft.com/office/word/2015/wordml/symex",
    "wpg":   "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",
    "wpi":   "http://schemas.microsoft.com/office/word/2010/wordprocessingInk",
    "wne":   "http://schemas.microsoft.com/office/word/2006/wordml",
    "wps":   "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
}


def _register_namespaces() -> None:
    """Register all OOXML namespace prefixes with ElementTree once."""
    for prefix, uri in _OOXML_NAMESPACES.items():
        ET.register_namespace(prefix, uri)


# ---------------------------------------------------------------------------
# File-level entry point
# ---------------------------------------------------------------------------

def accept_changes(
    source: Path,
    dest: Path,
    dry_run: bool = False,
) -> tuple[int, int]:
    """
    Accept all tracked changes in *source* and write the result to *dest*.

    The function only modifies ``word/document.xml``.  Other XML parts (styles,
    comments, footnotes, …) are copied verbatim.

    Args:
        source:  Path to the input ``.docx`` file.
        dest:    Path where the cleaned ``.docx`` will be written.
                 Ignored when *dry_run* is True.
        dry_run: If True, parse and count changes but do not write any file.

    Returns:
        (insertions_accepted, deletions_accepted)

    Raises:
        SystemExit: On file-not-found or ZIP errors (prints message first).
    """
    source = Path(source)
    dest   = Path(dest)

    if not source.exists():
        print(f"ERROR: File not found: {source}", file=sys.stderr)
        sys.exit(1)

    try:
        src_zip = zipfile.ZipFile(source, "r")
    except zipfile.BadZipFile as exc:
        print(f"ERROR: Not a valid ZIP/OOXML file: {exc}", file=sys.stderr)
        sys.exit(1)

    ins_total = 0
    del_total = 0

    with src_zip:
        names = src_zip.namelist()

        if dry_run:
            # Only read and count; do not write anything.
            for name in names:
                if name == "word/document.xml":
                    raw = src_zip.read(name)
                    try:
                        _, ins, dels = accept_tracked_changes_xml(raw)
                        ins_total += ins
                        del_total += dels
                    except ET.ParseError as exc:
                        print(f"ERROR: XML parse error in {name}: {exc}", file=sys.stderr)
                        sys.exit(2)
            return ins_total, del_total

        # Write the cleaned archive.
        with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as dst_zip:
            for name in names:
                raw = src_zip.read(name)

                if name == "word/document.xml":
                    try:
                        raw, ins, dels = accept_tracked_changes_xml(raw)
                        ins_total += ins
                        del_total += dels
                    except ET.ParseError as exc:
                        print(f"ERROR: XML parse error in {name}: {exc}", file=sys.stderr)
                        sys.exit(2)

                dst_zip.writestr(name, raw)

    return ins_total, del_total


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input",  help="Input .docx file with tracked changes")
    parser.add_argument("output", nargs="?", help="Output .docx file (clean copy)")
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite the input file instead of writing a new one",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Count changes and report without writing any file",
    )
    args = parser.parse_args()

    source = Path(args.input)

    if args.dry_run:
        ins, dels = accept_changes(source, source, dry_run=True)
        print(f"DRY RUN  {source.name}")
        print(f"         Insertions to accept : {ins}")
        print(f"         Deletions  to accept : {dels}")
        print(f"         Total tracked changes: {ins + dels}")
        sys.exit(0)

    if args.in_place:
        dest = source
    elif args.output:
        dest = Path(args.output)
    else:
        parser.error("Provide an output path or use --in-place.")

    ins, dels = accept_changes(source, dest)

    print(f"OK  {dest.name}")
    print(f"    Accepted {ins} insertion(s) and {dels} deletion(s).")


if __name__ == "__main__":
    main()
