#!/usr/bin/env python3
"""
comment.py — Add a comment (annotation) to a paragraph in a Word document.

Word comments live in two places inside a .docx ZIP:
  1. ``word/comments.xml``  — stores the comment body text and metadata
                              (author, date, comment ID).
  2. ``word/document.xml``  — stores the anchor markers that link a range of
                              text to its comment:
                                <w:commentRangeStart w:id="N"/>
                                ...text being commented on...
                                <w:commentRangeEnd   w:id="N"/>
                                <w:r><w:commentReference w:id="N"/></w:r>

This script appends a new comment to an existing document without disturbing
any existing comments or document content.

Usage:
    python docx-custom/scripts/comment.py UNPACKED_DIR PARAGRAPH_INDEX "Comment text"

    UNPACKED_DIR     Directory produced by ``office-custom/scripts/unpack.py``.
    PARAGRAPH_INDEX  0-based index of the paragraph to annotate.
    "Comment text"   The body of the new comment.

Options:
    --author NAME   Comment author (default: "Assistant").
    --date   DATE   ISO-8601 date string (default: today, e.g. 2026-03-13T00:00:00Z).

Exit codes:
    0  — Comment added successfully.
    1  — Bad arguments or file-not-found.
    2  — XML processing error.

Typical workflow:
    python office-custom/scripts/unpack.py document.docx unpacked/
    python docx-custom/scripts/comment.py unpacked/ 3 "Please clarify this paragraph."
    python office-custom/scripts/pack.py unpacked/ output.docx --original document.docx
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------------------
# Namespace constants
# ---------------------------------------------------------------------------

W_NS  = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W_PFX = "{" + W_NS + "}"

def _w(tag: str) -> str:
    """Return Clark-notation tag for a w: namespace element."""
    return f"{W_PFX}{tag}"


# All OOXML namespace prefixes that commonly appear in .docx XML parts.
# ElementTree must know these before serialising or it replaces them with
# auto-generated ns0:/ns1: prefixes that corrupt cross-part references.
_OOXML_NAMESPACES: dict[str, str] = {
    "wpc":   "http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas",
    "cx":    "http://schemas.microsoft.com/office/drawing/2014/chartex",
    "mc":    "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "o":     "urn:schemas-microsoft-com:office:office",
    "r":     "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "m":     "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "v":     "urn:schemas-microsoft-com:vml",
    "wp":    "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "w10":   "urn:schemas-microsoft-com:office:word",
    "w":     W_NS,
    "w14":   "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15":   "http://schemas.microsoft.com/office/word/2012/wordml",
    "w16":   "http://schemas.microsoft.com/office/word/2018/wordml",
    "w16cid":"http://schemas.microsoft.com/office/word/2016/wordml/cid",
    "w16se": "http://schemas.microsoft.com/office/word/2015/wordml/symex",
    "wpg":   "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",
    "wpi":   "http://schemas.microsoft.com/office/word/2010/wordprocessingInk",
    "wne":   "http://schemas.microsoft.com/office/word/2006/wordml",
    "wps":   "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
}


def _register_namespaces() -> None:
    for prefix, uri in _OOXML_NAMESPACES.items():
        ET.register_namespace(prefix, uri)


# ---------------------------------------------------------------------------
# ID management
# ---------------------------------------------------------------------------

def _max_comment_id(comments_root: ET.Element) -> int:
    """Return the highest existing w:id value in comments.xml (or -1 if empty)."""
    max_id = -1
    for comment in comments_root.findall(_w("comment")):
        raw = comment.get(_w("id"), "-1")
        try:
            max_id = max(max_id, int(raw))
        except ValueError:
            pass
    return max_id


# ---------------------------------------------------------------------------
# XML serialisation helpers
# ---------------------------------------------------------------------------

def _serialise(root: ET.Element) -> str:
    """Serialise an ElementTree root to a UTF-8 string with XML declaration."""
    _register_namespaces()
    body = ET.tostring(root, encoding="unicode", xml_declaration=False)
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n{body}'


# ---------------------------------------------------------------------------
# comments.xml helpers
# ---------------------------------------------------------------------------

_COMMENTS_SKELETON = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:comments xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"'
    ' xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"'
    ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    ' xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'
    ' xmlns:o="urn:schemas-microsoft-com:office:office"'
    ' xmlns:v="urn:schemas-microsoft-com:vml"'
    ' xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"'
    ' xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    ' xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"'
    ' xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"'
    ' xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"/>'
)


def _load_or_create_comments(comments_path: Path) -> ET.Element:
    """
    Read word/comments.xml if it exists, otherwise return a bare <w:comments> root.

    Args:
        comments_path: Filesystem path to ``word/comments.xml`` inside the
                       unpacked directory.

    Returns:
        Parsed ElementTree root element.
    """
    if comments_path.exists():
        return ET.parse(str(comments_path)).getroot()
    return ET.fromstring(_COMMENTS_SKELETON)


def _build_comment_element(
    comment_id: int,
    author: str,
    date: str,
    text: str,
) -> ET.Element:
    """
    Build a ``<w:comment>`` element with the given attributes and body text.

    Structure:
        <w:comment w:id="N" w:author="..." w:date="..." w:initials="...">
          <w:p>
            <w:pPr><w:pStyle w:val="CommentText"/></w:pPr>
            <w:r>
              <w:rPr><w:rStyle w:val="CommentReference"/></w:rPr>
              <w:annotationRef/>
            </w:r>
            <w:r><w:t>{text}</w:t></w:r>
          </w:p>
        </w:comment>

    Args:
        comment_id: Unique integer identifier for this comment.
        author:     Display name of the comment author.
        date:       ISO-8601 datetime string.
        text:       Plain-text body of the comment.

    Returns:
        The ``<w:comment>`` Element.
    """
    initials = "".join(word[0].upper() for word in author.split() if word)[:2] or "??"

    comment = ET.Element(_w("comment"))
    comment.set(_w("id"),       str(comment_id))
    comment.set(_w("author"),   author)
    comment.set(_w("date"),     date)
    comment.set(_w("initials"), initials)

    para = ET.SubElement(comment, _w("p"))

    # Paragraph properties: apply the built-in "CommentText" style.
    p_pr = ET.SubElement(para, _w("pPr"))
    p_style = ET.SubElement(p_pr, _w("pStyle"))
    p_style.set(_w("val"), "CommentText")

    # First run: annotation reference marker (shown as superscript comment number).
    ref_run = ET.SubElement(para, _w("r"))
    ref_rpr = ET.SubElement(ref_run, _w("rPr"))
    ref_style = ET.SubElement(ref_rpr, _w("rStyle"))
    ref_style.set(_w("val"), "CommentReference")
    ET.SubElement(ref_run, _w("annotationRef"))

    # Second run: the actual comment text.
    text_run = ET.SubElement(para, _w("r"))
    t_elem = ET.SubElement(text_run, _w("t"))
    t_elem.text = text
    # Preserve leading/trailing whitespace in the comment body.
    if text != text.strip():
        t_elem.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")

    return comment


# ---------------------------------------------------------------------------
# document.xml helpers
# ---------------------------------------------------------------------------

def _find_paragraphs(doc_root: ET.Element) -> list[ET.Element]:
    """
    Return all <w:p> elements in document order from the document body.

    Args:
        doc_root: Root element of ``word/document.xml``.

    Returns:
        List of paragraph elements.
    """
    body = doc_root.find(_w("body"))
    if body is None:
        return []
    # Use XPath-style .// to catch paragraphs nested in tables, text boxes, etc.
    return body.findall(".//" + _w("p"))


def _inject_comment_markers(
    paragraph: ET.Element,
    comment_id: int,
) -> None:
    """
    Insert comment anchor markers into *paragraph* so Word links the comment
    to the entire paragraph text.

    The inserted elements are:
      - ``<w:commentRangeStart w:id="N"/>``  — before the first run
      - ``<w:commentRangeEnd   w:id="N"/>``  — after the last run
      - ``<w:r><w:commentReference w:id="N"/></w:r>``  — after the range end

    Args:
        paragraph:  The <w:p> element to annotate.
        comment_id: The integer ID of the comment to attach.
    """
    children = list(paragraph)

    # Locate the first and last <w:r> (run) child indices.
    run_indices = [i for i, c in enumerate(children) if c.tag == _w("r")]

    if run_indices:
        first_run = run_indices[0]
        last_run  = run_indices[-1]
    else:
        # No runs: insert at end of paragraph (before any trailing pPr).
        first_run = len(children)
        last_run  = first_run - 1  # will cause insertion at end

    # --- commentRangeStart: insert before the first run ---
    start_el = ET.Element(_w("commentRangeStart"))
    start_el.set(_w("id"), str(comment_id))
    paragraph.insert(first_run, start_el)

    # After insertion the indices shifted by 1.
    adjusted_last = last_run + 1  # original last_run position, shifted

    # --- commentRangeEnd: insert after the last run ---
    end_el = ET.Element(_w("commentRangeEnd"))
    end_el.set(_w("id"), str(comment_id))
    paragraph.insert(adjusted_last + 1, end_el)

    # --- commentReference run: insert immediately after the end marker ---
    ref_run = ET.Element(_w("r"))
    ref_rpr = ET.SubElement(ref_run, _w("rPr"))
    ref_style = ET.SubElement(ref_rpr, _w("rStyle"))
    ref_style.set(_w("val"), "CommentReference")
    ref_elem = ET.SubElement(ref_run, _w("commentReference"))
    ref_elem.set(_w("id"), str(comment_id))
    paragraph.insert(adjusted_last + 2, ref_run)


# ---------------------------------------------------------------------------
# Content-types helper
# ---------------------------------------------------------------------------

_CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

def _ensure_comments_content_type(content_types_path: Path) -> None:
    """
    Add a Comments Override entry to ``[Content_Types].xml`` if missing.

    Word requires the comments part to be declared before it will load it.

    Args:
        content_types_path: Path to ``[Content_Types].xml`` in the unpacked dir.
    """
    ET.register_namespace("", _CT_NS)
    tree = ET.parse(str(content_types_path))
    root = tree.getroot()

    target = "/word/comments.xml"
    ct_tag = f"{{{_CT_NS}}}Override"

    # Check whether the Override already exists.
    for override in root.findall(ct_tag):
        if override.get("PartName") == target:
            return  # already present

    override_el = ET.Element(ct_tag)
    override_el.set("PartName", target)
    override_el.set(
        "ContentType",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml",
    )
    root.append(override_el)

    body = ET.tostring(root, encoding="unicode", xml_declaration=False)
    content_types_path.write_text(
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n{body}',
        encoding="utf-8",
    )


def _ensure_comments_relationship(rels_path: Path) -> None:
    """
    Add the comments relationship to ``word/_rels/document.xml.rels`` if missing.

    Without this entry Word silently ignores the comments part.

    Args:
        rels_path: Path to ``word/_rels/document.xml.rels``.
    """
    PKG_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
    COMMENTS_TYPE = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments"
    )

    ET.register_namespace("", PKG_NS)
    tree = ET.parse(str(rels_path))
    root = tree.getroot()

    rel_tag = f"{{{PKG_NS}}}Relationship"

    # Check if comments relationship already exists.
    for rel in root.findall(rel_tag):
        if rel.get("Type") == COMMENTS_TYPE:
            return  # already present

    # Generate a new relationship ID (rId<N+1>).
    existing_ids = [rel.get("Id", "") for rel in root.findall(rel_tag)]
    new_id = f"rId{len(existing_ids) + 1}"

    rel_el = ET.Element(rel_tag)
    rel_el.set("Id",     new_id)
    rel_el.set("Type",   COMMENTS_TYPE)
    rel_el.set("Target", "comments.xml")
    root.append(rel_el)

    body = ET.tostring(root, encoding="unicode", xml_declaration=False)
    rels_path.write_text(
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n{body}',
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Main add_comment function
# ---------------------------------------------------------------------------

def add_comment(
    unpacked_dir: Path,
    paragraph_index: int,
    text: str,
    author: str = "Assistant",
    date: str | None = None,
) -> int:
    """
    Add a comment to the paragraph at *paragraph_index* in an unpacked .docx.

    Args:
        unpacked_dir:     Directory containing the unpacked OOXML files
                          (output of ``office-custom/scripts/unpack.py``).
        paragraph_index:  0-based index into all ``<w:p>`` elements in
                          ``word/document.xml``.
        text:             Plain-text body of the comment.
        author:           Display name for the comment author.
        date:             ISO-8601 timestamp string.  Defaults to UTC now.

    Returns:
        The integer ID assigned to the new comment.

    Raises:
        SystemExit: On any file/XML error.
    """
    _register_namespaces()

    unpacked_dir = Path(unpacked_dir)
    if not unpacked_dir.is_dir():
        print(f"ERROR: Not a directory: {unpacked_dir}", file=sys.stderr)
        sys.exit(1)

    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    word_dir          = unpacked_dir / "word"
    document_path     = word_dir / "document.xml"
    comments_path     = word_dir / "comments.xml"
    rels_path         = word_dir / "_rels" / "document.xml.rels"
    content_types_path = unpacked_dir / "[Content_Types].xml"

    # ---- Validate required files -------------------------------------------
    for required in (document_path, rels_path, content_types_path):
        if not required.exists():
            print(f"ERROR: Required file missing: {required}", file=sys.stderr)
            sys.exit(1)

    # ---- Parse document.xml ------------------------------------------------
    try:
        doc_tree = ET.parse(str(document_path))
    except ET.ParseError as exc:
        print(f"ERROR: Cannot parse document.xml: {exc}", file=sys.stderr)
        sys.exit(2)

    doc_root   = doc_tree.getroot()
    paragraphs = _find_paragraphs(doc_root)

    if not 0 <= paragraph_index < len(paragraphs):
        print(
            f"ERROR: paragraph_index {paragraph_index} out of range "
            f"(document has {len(paragraphs)} paragraphs, indices 0–{len(paragraphs)-1}).",
            file=sys.stderr,
        )
        sys.exit(1)

    # ---- Load or create comments.xml ---------------------------------------
    comments_root = _load_or_create_comments(comments_path)
    comment_id    = _max_comment_id(comments_root) + 1

    # ---- Build and append the new <w:comment> element ---------------------
    comment_el = _build_comment_element(comment_id, author, date, text)
    comments_root.append(comment_el)

    # ---- Inject markers into the target paragraph -------------------------
    _inject_comment_markers(paragraphs[paragraph_index], comment_id)

    # ---- Ensure the package declares and links the comments part ----------
    _ensure_comments_content_type(content_types_path)
    _ensure_comments_relationship(rels_path)

    # ---- Persist changes ---------------------------------------------------
    comments_path.write_text(_serialise(comments_root), encoding="utf-8")
    document_path.write_text(_serialise(doc_root),      encoding="utf-8")

    return comment_id


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "unpacked_dir",
        help="Unpacked .docx directory (output of office-custom/scripts/unpack.py)",
    )
    parser.add_argument(
        "paragraph_index",
        type=int,
        help="0-based paragraph index to annotate",
    )
    parser.add_argument(
        "comment_text",
        help="Text body of the comment",
    )
    parser.add_argument(
        "--author",
        default="Assistant",
        help="Comment author name (default: Assistant)",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="ISO-8601 datetime, e.g. 2026-03-13T10:00:00Z (default: now)",
    )
    args = parser.parse_args()

    comment_id = add_comment(
        unpacked_dir     = Path(args.unpacked_dir),
        paragraph_index  = args.paragraph_index,
        text             = args.comment_text,
        author           = args.author,
        date             = args.date,
    )
    print(f"OK  Added comment ID={comment_id} to paragraph {args.paragraph_index}.")


if __name__ == "__main__":
    main()
