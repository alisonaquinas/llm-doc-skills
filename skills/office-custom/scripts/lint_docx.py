#!/usr/bin/env python3
"""
lint_docx.py — Pre-delivery lint for silent .docx corruption.

validate.py checks ZIP integrity, XML well-formedness, and required parts.
Those are necessary but NOT sufficient: a file can pass them, render fine in
LibreOffice, and still make Word display "Word found unreadable content" and
rebuild the document on open.  This linter flags the two most common silent
corruptions behind that behaviour:

  1. Package parts (*.rels, [Content_Types].xml) whose root element carries a
     namespace PREFIX instead of the default (prefix-less) namespace — e.g.
     <ns0:Relationships> / <ns0:Types>.  These are well-formed XML but trip
     strict OPC readers (Word recovery; LibreOffice may refuse to open).

  2. Numbering definitions in word/numbering.xml that are missing the metadata
     Word-authored definitions carry:
       • <w:num> without w16cid:durableId
       • <w:abstractNum> without w15:restartNumberingAfterBreak
     A hand-injected list definition that omits these (while siblings have
     them) is the classic trigger for Word rebuilding numbering.xml.

It also checks content-type completeness: every part should have a matching
<Override> or a <Default> for its extension.

Exits 0 if clean, 1 if any issue is found.

Usage:
    python office-custom/scripts/lint_docx.py document.docx
    python office-custom/scripts/lint_docx.py document.docx --quiet
"""

import argparse
import posixpath
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

# OPC content-types namespace (on [Content_Types].xml as the default ns).
_PKG_CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

_W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
_W16CID_NS = "http://schemas.microsoft.com/office/word/2016/wordml/cid"
_W15_NS = "http://schemas.microsoft.com/office/word/2012/wordml"


def _root_has_prefix(raw: bytes) -> bool:
    """Return True if the serialized root element uses a namespace prefix.

    We look at the raw bytes rather than the parsed tree because ElementTree
    discards prefixes on parse; the on-disk prefix is what readers see.
    """
    text = raw.decode("utf-8", errors="replace")
    # Find the first element tag (skip the XML declaration / PIs / comments).
    i = 0
    while i < len(text):
        lt = text.find("<", i)
        if lt == -1:
            return False
        nxt = text[lt + 1 : lt + 2]
        if nxt in ("?", "!"):  # declaration, comment, doctype
            i = lt + 1
            continue
        # Read the tag name up to whitespace or '>'.
        j = lt + 1
        while j < len(text) and text[j] not in " \t\r\n>/":
            j += 1
        name = text[lt + 1 : j]
        return ":" in name
    return False


def _check_package_prefixes(zf: zipfile.ZipFile, errors: list[str]) -> None:
    for name in zf.namelist():
        if name.endswith(".rels") or name == "[Content_Types].xml":
            if _root_has_prefix(zf.read(name)):
                errors.append(
                    f"{name}: package part root has a namespace prefix "
                    f"(e.g. <ns0:...>); use the default prefix-less namespace "
                    f"or Word will flag the file for recovery."
                )


def _check_numbering(zf: zipfile.ZipFile, warnings: list[str]) -> None:
    if "word/numbering.xml" not in zf.namelist():
        return
    try:
        root = ET.fromstring(zf.read("word/numbering.xml"))
    except ET.ParseError as exc:
        warnings.append(f"word/numbering.xml: could not parse ({exc})")
        return

    nums = root.findall(f"{{{_W_NS}}}num")
    missing_durable = [
        n.get(f"{{{_W_NS}}}numId", "?")
        for n in nums
        if n.get(f"{{{_W16CID_NS}}}durableId") is None
    ]
    if missing_durable and len(missing_durable) != len(nums):
        warnings.append(
            f"word/numbering.xml: <w:num> entries {missing_durable} lack "
            f"w16cid:durableId while siblings have it — Word may rebuild "
            f"numbering.xml on open."
        )
    elif missing_durable:
        warnings.append(
            "word/numbering.xml: all <w:num> entries lack w16cid:durableId; "
            "Word-authored definitions carry a unique one."
        )

    abstracts = root.findall(f"{{{_W_NS}}}abstractNum")
    missing_restart = [
        a.get(f"{{{_W_NS}}}abstractNumId", "?")
        for a in abstracts
        if a.find(f"{{{_W15_NS}}}restartNumberingAfterBreak") is None
    ]
    if missing_restart and len(missing_restart) != len(abstracts):
        warnings.append(
            f"word/numbering.xml: <w:abstractNum> {missing_restart} lack "
            f"w15:restartNumberingAfterBreak while siblings have it."
        )


def _check_content_types(zf: zipfile.ZipFile, errors: list[str]) -> None:
    if "[Content_Types].xml" not in zf.namelist():
        return
    try:
        root = ET.fromstring(zf.read("[Content_Types].xml"))
    except ET.ParseError:
        return  # well-formedness is validate.py's job

    defaults = {
        d.get("Extension", "").lower()
        for d in root.findall(f"{{{_PKG_CT_NS}}}Default")
    }
    overrides = {
        o.get("PartName", "")
        for o in root.findall(f"{{{_PKG_CT_NS}}}Override")
    }
    for name in zf.namelist():
        if name.endswith("/") or name == "[Content_Types].xml":
            continue
        if name.startswith("_rels/") or "/_rels/" in name:
            continue  # covered by the 'rels' Default
        ext = posixpath.splitext(name)[1].lstrip(".").lower()
        part = "/" + name
        if part in overrides or ext in defaults:
            continue
        errors.append(
            f"{name}: no <Override> and no <Default> for extension "
            f"'.{ext}' in [Content_Types].xml (the part is unreachable)."
        )


def lint(source: Path, quiet: bool = False) -> bool:
    """Lint *source* and return True if no issues are found."""
    source = Path(source)
    if not source.exists():
        print(f"ERROR: File not found: {source}")
        return False
    try:
        zf = zipfile.ZipFile(source, "r")
    except zipfile.BadZipFile as exc:
        print(f"ERROR: Not a valid ZIP/OOXML file: {exc}")
        return False

    errors: list[str] = []
    warnings: list[str] = []
    with zf:
        _check_package_prefixes(zf, errors)
        _check_content_types(zf, errors)
        _check_numbering(zf, warnings)

    label = source.name
    if errors:
        print(f"FAIL  {label}")
        for err in errors:
            print(f"      ERROR: {err}")
        for warn in warnings:
            print(f"      WARN:  {warn}")
        return False
    if warnings:
        print(f"WARN  {label}")
        for warn in warnings:
            print(f"      WARN:  {warn}")
        return True
    if not quiet:
        print(f"OK    {label}  (no silent-corruption signatures)")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("files", nargs="+", help="Files to lint")
    parser.add_argument("--quiet", action="store_true", help="Suppress OK output")
    args = parser.parse_args()

    all_clean = True
    for path_str in args.files:
        if not lint(Path(path_str), quiet=args.quiet):
            all_clean = False

    sys.exit(0 if all_clean else 1)


if __name__ == "__main__":
    main()
