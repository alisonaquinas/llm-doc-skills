#!/usr/bin/env python3
"""
check_fragility.py — Detect fragility signals in a .pptx package.

PowerPoint Online has a stricter OOXML validator than PowerPoint Desktop,
LibreOffice, or python-pptx. Decks emitted by third-party exporters (the
canonical example is "Walnut Exporter", but the same pattern appears in
Aspose-style and screenshot-to-deck tools) often parse fine in lenient
readers but fail in PowerPoint Online — and a python-pptx re-save normalizes
just enough XML serialization details to push an already-fragile file past
that threshold.

This script inspects a .pptx without modifying it and reports the fragility
signals observed in real Walnut-style failures:

    1. Exporter fingerprint     — docProps/app.xml Application value
    2. Image duplication ratio  — ppt/media/* files vs unique content hashes
    3. Inline xmlns redundancy  — xmlns:* attribute count vs irreducible minimum
    4. Content_Types defaults   — Default Extension="xml" pointing at
                                  core-properties (wrong; must be Override)
    5. Slide layout numbering   — slideLayout1.xml missing
    6. Theme misplacement       — themeN.xml under notesMasters/
    7. Relationship-ID style    — random hex IDs vs canonical rIdN
    8. Empty xfrm shells        — <a:xfrm/> self-closing instead of full
                                  <a:off/><a:ext/> children
    9. App-properties sanity    — Slides=0 or Notes=0 in a non-empty deck

Exits 0 when no fragility signals are found, 1 when any signal is found.
Use --json for machine-readable output.

Usage:
    python pptx-custom/scripts/check_fragility.py deck.pptx
    python pptx-custom/scripts/check_fragility.py deck.pptx --json

Recommended remediation flows are documented in
`pptx-custom/recovering-fragile-decks.md`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

# Exporter Application strings that are known to emit fragile OOXML.
# Match is case-insensitive substring against docProps/app.xml <ap:Application>.
_FRAGILE_EXPORTERS = (
    "walnut exporter",
    "aspose",
    "openxml sdk",  # Common in pipelines that hand-assemble parts.
    "syncfusion",
    "spire",
    "gembox",
    "docx4j",  # Mostly Word, but the symptom set overlaps.
)

# Rel IDs that look like rId<digits>; the random-hex style is the smell.
_REL_ID_CANONICAL = re.compile(r"^rId\d+$")
_REL_ID_RANDOM_HEX = re.compile(r"^R[0-9a-fA-F]{12,}$")


@dataclass
class Finding:
    """A single fragility signal observed in the package."""

    code: str
    severity: str  # "info", "warn", or "fail"
    message: str
    details: dict = field(default_factory=dict)


@dataclass
class Report:
    path: str
    findings: list[Finding] = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    @property
    def worst(self) -> str:
        order = {"fail": 3, "warn": 2, "info": 1}
        return max(
            (f.severity for f in self.findings),
            default="info",
            key=lambda s: order.get(s, 0),
        )

    def add(self, **kwargs) -> None:
        self.findings.append(Finding(**kwargs))


def _read_text(zf: zipfile.ZipFile, name: str) -> str | None:
    """Read *name* as UTF-8 text. Return None if missing or unreadable."""
    try:
        return zf.read(name).decode("utf-8", errors="replace")
    except KeyError:
        return None


def _check_core_creator(
    zf: zipfile.ZipFile,
    report: Report,
    application_lower: str,
) -> None:
    """Inspect docProps/core.xml for a fragile-producer creator signature.

    Only emits a finding when core.xml names a known-fragile producer AND
    app.xml's Application field does NOT — i.e. when the creator signature
    is the only evidence left. If app.xml already flagged the same producer
    we'd double-report, which adds noise without information.
    """
    text = _read_text(zf, "docProps/core.xml")
    if not text:
        return

    match = re.search(r"<dc:creator>([^<]*)</dc:creator>", text)
    creator = match.group(1).strip() if match else ""
    if not creator:
        return

    report.summary["creator"] = creator
    creator_lower = creator.lower()
    if not any(needle in creator_lower for needle in _FRAGILE_EXPORTERS):
        return

    # Skip if app.xml already named the same fragile producer.
    if any(needle in application_lower for needle in _FRAGILE_EXPORTERS):
        return

    report.add(
        code="creator-fragile",
        severity="fail",
        message=(
            f"docProps/core.xml dc:creator = {creator!r} names a known-fragile "
            "producer even though docProps/app.xml does not. PowerPoint's "
            "repair rewrites app.xml but leaves core.xml alone, so this is "
            "often the only surviving signature on a laundered deck."
        ),
        details={"creator": creator},
    )


def _check_exporter(zf: zipfile.ZipFile, report: Report) -> None:
    text = _read_text(zf, "docProps/app.xml")
    if not text:
        report.add(
            code="app-missing",
            severity="warn",
            message="docProps/app.xml is missing; cannot identify producing tool.",
        )
        # core.xml may still carry a creator signature even without app.xml.
        _check_core_creator(zf, report, application_lower="")
        return

    # The extended-properties schema declares the default namespace at the
    # root, so the Application/Slides/Notes elements appear unprefixed in
    # real Office output. Aspose and some pipelines emit the `ap:` prefix
    # explicitly. Match either form.
    app_match = re.search(r"<(?:ap:)?Application>([^<]+)</(?:ap:)?Application>", text)
    application = app_match.group(1).strip() if app_match else ""

    slides_match = re.search(r"<(?:ap:)?Slides>(\d+)</(?:ap:)?Slides>", text)
    notes_match = re.search(r"<(?:ap:)?Notes>(\d+)</(?:ap:)?Notes>", text)
    decl_slides = int(slides_match.group(1)) if slides_match else None
    decl_notes = int(notes_match.group(1)) if notes_match else None

    report.summary["application"] = application
    report.summary["declared_slides"] = decl_slides
    report.summary["declared_notes"] = decl_notes

    lower = application.lower()
    if any(needle in lower for needle in _FRAGILE_EXPORTERS):
        report.add(
            code="exporter-fragile",
            severity="fail",
            message=(
                f"docProps/app.xml Application = {application!r}. This producer "
                "is known to emit OOXML that PowerPoint Online rejects."
            ),
            details={"application": application},
        )
    elif application and "microsoft" not in lower and "libreoffice" not in lower:
        report.add(
            code="exporter-unknown",
            severity="warn",
            message=(
                f"docProps/app.xml Application = {application!r}. Producer is "
                "not a known Office-family app; treat the file as potentially fragile."
            ),
            details={"application": application},
        )

    # Slide / notes count sanity vs actual slides on disk uses the same
    # prefix-agnostic regex match resolved above.

    # PowerPoint Desktop's repair rewrites docProps/app.xml but does NOT
    # touch docProps/core.xml. A fragile producer's signature can survive
    # there even after an Office re-save laundered the Application field —
    # so check core.xml's <dc:creator> independently.
    _check_core_creator(zf, report, application_lower=lower)

    # Slide / notes count sanity vs actual slides on disk.
    actual_slides = sum(
        1 for n in zf.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)
    )
    actual_notes = sum(
        1
        for n in zf.namelist()
        if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n)
    )
    report.summary["actual_slides"] = actual_slides
    report.summary["actual_notes"] = actual_notes

    if decl_slides is not None and decl_slides != actual_slides:
        report.add(
            code="app-slide-mismatch",
            severity="warn",
            message=(
                f"docProps/app.xml declares {decl_slides} slides but the package "
                f"contains {actual_slides}. A real Office app would not write this."
            ),
        )
    if decl_notes is not None and decl_notes != actual_notes and actual_notes:
        report.add(
            code="app-notes-mismatch",
            severity="warn",
            message=(
                f"docProps/app.xml declares {decl_notes} notes but the package "
                f"contains {actual_notes}."
            ),
        )


def _check_image_dedup(zf: zipfile.ZipFile, report: Report) -> None:
    media = [n for n in zf.namelist() if n.startswith("ppt/media/")]
    if not media:
        return

    hashes: Counter[str] = Counter()
    sizes: dict[str, int] = {}
    for name in media:
        data = zf.read(name)
        digest = hashlib.sha256(data).hexdigest()
        hashes[digest] += 1
        sizes[digest] = len(data)

    duplicate_blobs = {h: c for h, c in hashes.items() if c > 1}
    wasted_bytes = sum(sizes[h] * (c - 1) for h, c in duplicate_blobs.items())
    report.summary["media_files"] = len(media)
    report.summary["unique_media_blobs"] = len(hashes)
    report.summary["duplicate_media_wasted_bytes"] = wasted_bytes

    if duplicate_blobs:
        worst = max(duplicate_blobs.values())
        severity = "fail" if worst >= 5 or wasted_bytes >= 200_000 else "warn"
        report.add(
            code="image-duplication",
            severity=severity,
            message=(
                f"{len(media)} files in ppt/media/ but only {len(hashes)} unique "
                f"blobs by SHA-256 — {worst}× max copy count, "
                f"{wasted_bytes:,} bytes of duplicated image data. "
                "Exporters that re-emit the same image per shape produce this; "
                "PowerPoint Desktop's repair collapses it."
            ),
            details={
                "media_files": len(media),
                "unique_blobs": len(hashes),
                "max_copies": worst,
                "wasted_bytes": wasted_bytes,
            },
        )


def _check_inline_xmlns(zf: zipfile.ZipFile, report: Report) -> None:
    """Flag slides whose child elements re-declare xmlns instead of inheriting."""
    slide_names = sorted(
        n for n in zf.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)
    )
    if not slide_names:
        return

    inline_counts: dict[str, int] = {}
    for name in slide_names:
        text = _read_text(zf, name) or ""
        # Count xmlns:* declarations on non-root elements by subtracting the
        # root namespace declarations from the total.
        total = len(re.findall(r"\bxmlns:[a-zA-Z0-9]+=", text))
        # The well-formed minimum is 1 declaration per foreign namespace at root.
        # Anything north of ~5x that ratio means inline re-declaration spam.
        inline_counts[name] = total

    high = {n: c for n, c in inline_counts.items() if c > 60}
    report.summary["inline_xmlns_per_slide"] = inline_counts

    if high:
        worst_name, worst_count = max(high.items(), key=lambda kv: kv[1])
        report.add(
            code="inline-xmlns-spam",
            severity="fail" if worst_count > 150 else "warn",
            message=(
                f"{len(high)} slide(s) carry redundant inline xmlns declarations "
                f"(worst: {worst_name} with {worst_count} xmlns: attributes). "
                "PowerPoint Online's validator is stricter about this pattern "
                "than Desktop is."
            ),
            details={"max": worst_count, "max_slide": worst_name},
        )


def _check_content_types_defaults(zf: zipfile.ZipFile, report: Report) -> None:
    text = _read_text(zf, "[Content_Types].xml")
    if not text:
        report.add(
            code="content-types-missing",
            severity="fail",
            message="[Content_Types].xml is missing; the package is structurally invalid.",
        )
        return

    # Look for the specific bug: Default Extension="xml"
    # ContentType="application/vnd.openxmlformats-package.core-properties+xml"
    bad_default = re.search(
        r'<Default\s+Extension="xml"\s+ContentType="([^"]*core-properties[^"]*)"',
        text,
    )
    if bad_default:
        report.add(
            code="content-types-default-xml",
            severity="fail",
            message=(
                "[Content_Types].xml uses Default Extension=\"xml\" with the "
                "core-properties ContentType. Core properties must be declared "
                "via an Override entry, not a Default."
            ),
            details={"content_type": bad_default.group(1)},
        )


def _check_slide_layout_numbering(zf: zipfile.ZipFile, report: Report) -> None:
    layouts = sorted(
        int(m.group(1))
        for n in zf.namelist()
        if (m := re.fullmatch(r"ppt/slideLayouts/slideLayout(\d+)\.xml", n))
    )
    if not layouts:
        return
    if 1 not in layouts:
        report.add(
            code="slideLayout1-missing",
            severity="warn",
            message=(
                f"slideLayout1.xml is missing (found layouts: {layouts}). "
                "Office layouts are 1-indexed; some readers treat the gap as a smell."
            ),
        )


def _check_theme_location(zf: zipfile.ZipFile, report: Report) -> None:
    misplaced = [
        n
        for n in zf.namelist()
        if re.fullmatch(r"ppt/notesMasters/theme/theme\d+\.xml", n)
        or re.fullmatch(r"ppt/slideMasters/theme/theme\d+\.xml", n)
    ]
    if misplaced:
        report.add(
            code="theme-misplaced",
            severity="warn",
            message=(
                f"Theme file(s) located under a master subtree instead of "
                f"ppt/theme/: {misplaced}. PowerPoint moves these during repair."
            ),
            details={"paths": misplaced},
        )


def _check_rel_id_style(zf: zipfile.ZipFile, report: Report) -> None:
    random_hex = 0
    canonical = 0
    sampled_files = [n for n in zf.namelist() if n.endswith(".rels")]
    for name in sampled_files:
        text = _read_text(zf, name) or ""
        for match in re.finditer(r'Id="([^"]+)"', text):
            rid = match.group(1)
            if _REL_ID_CANONICAL.fullmatch(rid):
                canonical += 1
            elif _REL_ID_RANDOM_HEX.fullmatch(rid):
                random_hex += 1

    report.summary["rel_ids_canonical"] = canonical
    report.summary["rel_ids_random_hex"] = random_hex

    if random_hex and random_hex > canonical:
        report.add(
            code="rel-id-random-hex",
            severity="warn",
            message=(
                f"{random_hex} relationship IDs use the random-hex style "
                f"(R<12+ hex chars>) versus {canonical} canonical rId<N>. "
                "Both are syntactically legal, but the random-hex style is a "
                "third-party-tool tell."
            ),
        )


def _check_empty_xfrm(zf: zipfile.ZipFile, report: Report) -> None:
    """Count self-closing <a:xfrm/> elements across slide XML."""
    slide_names = [n for n in zf.namelist() if n.startswith("ppt/slides/slide")]
    empty = 0
    for name in slide_names:
        text = _read_text(zf, name) or ""
        empty += len(re.findall(r"<a:xfrm\s*/>", text))

    if empty:
        report.add(
            code="empty-xfrm",
            severity="warn",
            message=(
                f"{empty} self-closing <a:xfrm/> element(s) found across slide "
                "XML. PowerPoint reads but never writes this shape; repair fills "
                "in explicit <a:off/> and <a:ext/> children."
            ),
            details={"count": empty},
        )


def check(path: Path) -> Report:
    report = Report(path=str(path))
    try:
        zf = zipfile.ZipFile(path, "r")
    except zipfile.BadZipFile as exc:
        report.add(
            code="bad-zip",
            severity="fail",
            message=f"Not a valid ZIP/OOXML file: {exc}",
        )
        return report

    with zf:
        _check_exporter(zf, report)
        _check_image_dedup(zf, report)
        _check_inline_xmlns(zf, report)
        _check_content_types_defaults(zf, report)
        _check_slide_layout_numbering(zf, report)
        _check_theme_location(zf, report)
        _check_rel_id_style(zf, report)
        _check_empty_xfrm(zf, report)

    return report


def _format_text(report: Report) -> str:
    if not report.findings:
        return f"OK   {report.path}  (no fragility signals)"

    lines = [f"{report.worst.upper():<4} {report.path}"]
    if app := report.summary.get("application"):
        lines.append(f"     application: {app}")
    for f in report.findings:
        lines.append(f"     [{f.severity}] {f.code}: {f.message}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("files", nargs="+", help=".pptx files to inspect")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON report instead of a human-readable summary.",
    )
    args = parser.parse_args()

    reports = [check(Path(p)) for p in args.files]

    if args.json:
        json.dump(
            [
                {
                    "path": r.path,
                    "worst": r.worst,
                    "summary": r.summary,
                    "findings": [asdict(f) for f in r.findings],
                }
                for r in reports
            ],
            sys.stdout,
            indent=2,
        )
        sys.stdout.write("\n")
    else:
        for r in reports:
            print(_format_text(r))

    sys.exit(0 if all(not r.findings for r in reports) else 1)


if __name__ == "__main__":
    main()
