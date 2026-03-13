#!/usr/bin/env python3
"""
unpack.py — Unpack an Office Open XML file (.docx / .pptx / .xlsx) for editing.

An OOXML file is a ZIP archive of XML files.  This script:
  1. Extracts the ZIP to a working directory.
  2. Pretty-prints every XML file so diffs are readable and edits are easy.
  3. (docx only, optional) Merges adjacent text runs with identical formatting
     so find-and-replace works across run boundaries.
  4. Converts smart-quote characters to XML entities so they survive round-
     trips through tools that don't handle UTF-8 gracefully.

After editing the unpacked directory, repack with:
    python office-custom/scripts/pack.py <unpacked_dir> <output_file> --original <original>

Usage:
    python office-custom/scripts/unpack.py document.docx unpacked/
    python office-custom/scripts/unpack.py presentation.pptx unpacked/ --merge-runs false
    python office-custom/scripts/unpack.py spreadsheet.xlsx unpacked/
"""

import argparse
import shutil
import zipfile
from pathlib import Path
from xml.dom import minidom
from xml.etree import ElementTree as ET

# Smart-quote characters and their XML entity equivalents.
# These are applied to all XML text content after pretty-printing so that
# editors that strip non-ASCII don't corrupt the document.
_SMART_QUOTE_MAP = {
    "\u2018": "&#x2018;",  # ' LEFT SINGLE QUOTATION MARK
    "\u2019": "&#x2019;",  # ' RIGHT SINGLE QUOTATION MARK / APOSTROPHE
    "\u201C": "&#x201C;",  # " LEFT DOUBLE QUOTATION MARK
    "\u201D": "&#x201D;",  # " RIGHT DOUBLE QUOTATION MARK
    "\u2013": "&#x2013;",  # – EN DASH
    "\u2014": "&#x2014;",  # — EM DASH
    "\u00A0": "&#xA0;",    # non-breaking space
}

# XML namespaces used in OOXML — needed to parse namespace-prefixed tags.
_NS = {
    "w":   "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r":   "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp":  "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a":   "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p":   "http://schemas.openxmlformats.org/presentationml/2006/main",
    "mc":  "http://schemas.openxmlformats.org/markup-compatibility/2006",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def pretty_print_xml(xml_bytes: bytes) -> str:
    """Return a human-readable, consistently indented XML string.

    Uses minidom to reformat.  Strips the XML declaration added by minidom
    (the original declaration, if any, is preserved when repacking).

    Args:
        xml_bytes: Raw XML bytes from the ZIP archive.

    Returns:
        A UTF-8 string with 2-space indentation and Unix line endings.
    """
    try:
        dom = minidom.parseString(xml_bytes)
        pretty = dom.toprettyxml(indent="  ", encoding=None)
        # minidom adds <?xml version="1.0" ?> — strip it; pack.py re-adds it.
        lines = pretty.splitlines()
        if lines and lines[0].startswith("<?xml"):
            lines = lines[1:]
        return "\n".join(line for line in lines if line.strip()) + "\n"
    except Exception:
        # If XML is malformed, return as-is (UTF-8 decoded).
        return xml_bytes.decode("utf-8", errors="replace")


def escape_smart_quotes(text: str) -> str:
    """Replace Unicode typographic characters with XML numeric entities.

    This prevents corruption when XML files are later opened by tools (or
    text editors) that rewrite the encoding or strip high-codepoint chars.

    Args:
        text: XML content as a string.

    Returns:
        The same string with smart quotes replaced by XML entities.
    """
    for char, entity in _SMART_QUOTE_MAP.items():
        text = text.replace(char, entity)
    return text


def merge_adjacent_runs(xml_text: str) -> str:
    """Merge consecutive <w:r> elements that share identical <w:rPr> formatting.

    Word stores text in 'runs' (<w:r>).  When a document has been edited,
    identical formatting can be split across many runs, making find-and-replace
    unreliable (e.g. "hel" in one run and "lo" in the next).

    This function re-parses the XML, merges adjacent runs with matching
    formatting, and re-serialises.  Only plain text runs are merged;
    runs containing field codes, bookmarks, or special elements are left alone.

    Args:
        xml_text: The content of word/document.xml as a string.

    Returns:
        XML string with adjacent same-format runs merged.
    """
    try:
        # Register namespaces to avoid ns0: prefixes in the output.
        for prefix, uri in _NS.items():
            ET.register_namespace(prefix, uri)

        root = ET.fromstring(xml_text.encode("utf-8"))
        W = _NS["w"]

        def rpr_key(run: ET.Element) -> str:
            """Serialise a run's <w:rPr> to a string for comparison."""
            rpr = run.find(f"{{{W}}}rPr")
            if rpr is None:
                return ""
            return ET.tostring(rpr, encoding="unicode")

        def can_merge(run: ET.Element) -> bool:
            """Return True if this run contains only <w:rPr> and <w:t>."""
            allowed = {f"{{{W}}}rPr", f"{{{W}}}t"}
            return all(child.tag in allowed for child in run)

        # Walk every paragraph and merge runs within it.
        for para in root.iter(f"{{{W}}}p"):
            children = list(para)
            i = 0
            while i < len(children) - 1:
                curr = children[i]
                nxt = children[i + 1]
                if (
                    curr.tag == f"{{{W}}}r"
                    and nxt.tag == f"{{{W}}}r"
                    and can_merge(curr)
                    and can_merge(nxt)
                    and rpr_key(curr) == rpr_key(nxt)
                ):
                    # Append next run's text to current run's <w:t>.
                    curr_t = curr.find(f"{{{W}}}t")
                    nxt_t = nxt.find(f"{{{W}}}t")
                    if curr_t is not None and nxt_t is not None:
                        curr_text = curr_t.text or ""
                        nxt_text = nxt_t.text or ""
                        merged = curr_text + nxt_text
                        curr_t.text = merged
                        # Preserve xml:space="preserve" if either run had spaces.
                        if merged != merged.strip():
                            curr_t.set(
                                "{http://www.w3.org/XML/1998/namespace}space",
                                "preserve",
                            )
                        # Remove the next run from the paragraph.
                        para.remove(nxt)
                        children.pop(i + 1)
                        continue  # Re-check the merged run against the new next.
                i += 1

        return ET.tostring(root, encoding="unicode", xml_declaration=False)
    except Exception:
        # If anything goes wrong, return unchanged.
        return xml_text


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def unpack(
    source: Path,
    dest: Path,
    merge_runs: bool = True,
) -> None:
    """Unpack an OOXML file to *dest* for editing.

    Args:
        source:      Path to the .docx / .pptx / .xlsx file.
        dest:        Directory to extract into (created if absent, cleared if
                     present).
        merge_runs:  If True (default) and source is a .docx, merge adjacent
                     same-format text runs in word/document.xml.
    """
    source = Path(source)
    dest = Path(dest)

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    # Start fresh: remove any existing unpacked directory.
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    suffix = source.suffix.lower()

    print(f"Unpacking {source} → {dest}/")

    with zipfile.ZipFile(source, "r") as zf:
        for name in zf.namelist():
            member_path = dest / name

            if name.endswith("/"):
                # Directory entry — create it.
                member_path.mkdir(parents=True, exist_ok=True)
                continue

            member_path.parent.mkdir(parents=True, exist_ok=True)

            raw = zf.read(name)

            if name.endswith(".xml") or name.endswith(".rels"):
                # Pretty-print XML and escape smart quotes.
                text = pretty_print_xml(raw)
                text = escape_smart_quotes(text)

                # Optionally merge adjacent runs in the main document body.
                if (
                    merge_runs
                    and suffix == ".docx"
                    and name == "word/document.xml"
                ):
                    text = merge_adjacent_runs(text)
                    # Re-escape after merge (ET unescapes entities).
                    text = escape_smart_quotes(text)

                member_path.write_text(text, encoding="utf-8")
            else:
                # Binary file (images, fonts, etc.) — copy as-is.
                member_path.write_bytes(raw)

    print(f"  Extracted {len(list(dest.rglob('*')))} files.")
    if merge_runs and suffix == ".docx":
        print("  Merged adjacent text runs in word/document.xml.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("source", help="Path to the .docx / .pptx / .xlsx file")
    parser.add_argument("dest", help="Destination directory for unpacked files")
    parser.add_argument(
        "--merge-runs",
        default="true",
        choices=["true", "false"],
        help="Merge adjacent same-format runs in docx (default: true)",
    )
    args = parser.parse_args()

    unpack(
        source=Path(args.source),
        dest=Path(args.dest),
        merge_runs=(args.merge_runs == "true"),
    )


if __name__ == "__main__":
    main()
