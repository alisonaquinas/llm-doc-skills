#!/usr/bin/env python3
"""Validate raw OOXML or ODF XML parts against bundled schemas.

This helper exists because the canonical OOXML XSD assets are stored in a
reference-friendly directory layout, not in the flat sibling layout expected by
many XML validators. The script stages the needed XSD dependency closure into a
throwaway directory, patches a small number of XML namespace/schema-location
quirks, and then validates the target XML with lxml.

Examples
--------
Validate a DOCX main document part:
    python raw-document/scripts/validate_xml.py \
        --family ooxml --schema wml --package sample.docx --part word/document.xml

Validate an extracted ODF content part with auto-detected office:version:
    python raw-document/scripts/validate_xml.py \
        --family odf --xml content.xml
"""

from __future__ import annotations

import argparse
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable

try:
    from lxml import etree
except ImportError:  # pragma: no cover - exercised manually, not in unit tests
    etree = None

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
OOXML_SCHEMA_ROOT = SKILL_DIR / "assets" / "schemas" / "ooxml"
ODF_SCHEMA_ROOT = SKILL_DIR / "assets" / "schemas" / "odf"
XSD_NS = "http://www.w3.org/2001/XMLSchema"
ODF_OFFICE_NS = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"

OOXML_SCHEMA_MAP = {
    ("wml", False): OOXML_SCHEMA_ROOT / "wml" / "wml.xsd",
    ("sml", False): OOXML_SCHEMA_ROOT / "sml" / "sml.xsd",
    ("pml", False): OOXML_SCHEMA_ROOT / "pml" / "pml.xsd",
    ("dml-main", False): OOXML_SCHEMA_ROOT / "dml" / "dml-main.xsd",
    ("opc-contenttypes", False): OOXML_SCHEMA_ROOT / "opc" / "opc-contentTypes.xsd",
    ("opc-coreproperties", False): OOXML_SCHEMA_ROOT / "opc" / "opc-coreProperties.xsd",
    ("opc-digsig", False): OOXML_SCHEMA_ROOT / "opc" / "opc-digSig.xsd",
    ("opc-relationships", False): OOXML_SCHEMA_ROOT / "opc" / "opc-relationships.xsd",
    ("wml", True): OOXML_SCHEMA_ROOT / "strict" / "wml.xsd",
    ("sml", True): OOXML_SCHEMA_ROOT / "strict" / "sml.xsd",
    ("pml", True): OOXML_SCHEMA_ROOT / "strict" / "pml.xsd",
    ("dml-main", True): OOXML_SCHEMA_ROOT / "strict" / "dml-main.xsd",
}


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def schema_display_path(path: Path) -> str:
    return path.relative_to(SKILL_DIR).as_posix()


def require_lxml() -> None:
    if etree is None:
        raise SystemExit(
            "ERROR: lxml is required for schema validation. Install it with "
            "'python -m pip install lxml'."
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--family",
        required=True,
        choices=["ooxml", "odf"],
        help="Document family to validate.",
    )
    parser.add_argument(
        "--schema",
        help=(
            "OOXML schema key: wml, sml, pml, dml-main, opc-contenttypes, "
            "opc-coreproperties, opc-digsig, or opc-relationships."
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Use the OOXML Strict schema variants when available.",
    )
    parser.add_argument(
        "--package",
        type=Path,
        help="Package file (.docx/.xlsx/.pptx/.odt/.ods/.odp) to extract XML from.",
    )
    parser.add_argument(
        "--part",
        help="Package member path to validate when --package is used.",
    )
    parser.add_argument(
        "--xml",
        type=Path,
        help="Path to an extracted XML file to validate directly.",
    )
    parser.add_argument(
        "--odf-version",
        choices=["1.3", "1.4"],
        help="Override the detected office:version for ODF validation.",
    )
    return parser.parse_args(argv)


def build_xsd_index() -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in OOXML_SCHEMA_ROOT.rglob("*.xsd"):
        index.setdefault(path.name, []).append(path)
    return index


def resolve_ooxml_dependency(
    referrer: Path,
    location: str | None,
    namespace: str | None,
    index: dict[str, list[Path]],
) -> Path:
    if location:
        relative = referrer.parent / location
        if relative.exists():
            return relative
        candidates = index.get(Path(location).name, [])
        if candidates:
            if len(candidates) == 1:
                return candidates[0]
            if "strict" in referrer.parts:
                strict = [path for path in candidates if "strict" in path.parts]
                if strict:
                    return strict[0]
            non_strict = [path for path in candidates if "strict" not in path.parts]
            if non_strict:
                return non_strict[0]
            return candidates[0]

    if namespace == XML_NS:
        xml_candidates = index.get("xml.xsd", [])
        if "strict" in referrer.parts:
            strict = [path for path in xml_candidates if "strict" in path.parts]
            if strict:
                return strict[0]
        non_strict = [path for path in xml_candidates if "strict" not in path.parts]
        if non_strict:
            return non_strict[0]
        if xml_candidates:
            return xml_candidates[0]

    raise FileNotFoundError(
        f"Could not resolve imported schema from {referrer.name}: "
        f"schemaLocation={location!r}, namespace={namespace!r}"
    )


def patch_strict_onoff_defaults(tree: etree._ElementTree) -> None:
    for attr in tree.findall(f".//{{{XSD_NS}}}attribute"):
        attr_type = attr.get("type", "")
        default = attr.get("default")
        if attr_type.endswith("ST_OnOff") and default in {"on", "off"}:
            attr.set("default", "true" if default == "on" else "false")


class OoxmlSchemaStager:
    def __init__(self) -> None:
        self.index = build_xsd_index()

    def stage(self, entry_schema: Path, dest_dir: Path) -> Path:
        staged: set[str] = set()
        in_progress: set[Path] = set()

        def _stage_one(path: Path) -> None:
            if path.name in staged or path in in_progress:
                return
            in_progress.add(path)
            tree = etree.parse(str(path))
            elements: Iterable[etree._Element] = (
                list(tree.findall(f".//{{{XSD_NS}}}import"))
                + list(tree.findall(f".//{{{XSD_NS}}}include"))
            )
            for elem in elements:
                target = resolve_ooxml_dependency(
                    path,
                    elem.get("schemaLocation"),
                    elem.get("namespace"),
                    self.index,
                )
                elem.set("schemaLocation", target.name)
                _stage_one(target)
            if "strict" in path.parts:
                patch_strict_onoff_defaults(tree)
            tree.write(
                str(dest_dir / path.name),
                encoding="utf-8",
                xml_declaration=True,
            )
            staged.add(path.name)
            in_progress.remove(path)

        _stage_one(entry_schema)
        return dest_dir / entry_schema.name


def extract_xml_source(args: argparse.Namespace) -> bytes:
    if args.xml and args.package:
        raise SystemExit("ERROR: provide either --xml or --package/--part, not both.")
    if args.xml:
        return args.xml.read_bytes()
    if args.package:
        if not args.part:
            raise SystemExit("ERROR: --part is required when --package is used.")
        with zipfile.ZipFile(args.package) as archive:
            try:
                return archive.read(args.part)
            except KeyError as exc:
                raise SystemExit(f"ERROR: package member not found: {args.part}") from exc
    raise SystemExit("ERROR: provide --xml or --package/--part.")


def infer_odf_version(xml_bytes: bytes) -> str:
    root = etree.fromstring(xml_bytes)
    version = root.get(f"{{{ODF_OFFICE_NS}}}version")
    if not version:
        raise SystemExit(
            "ERROR: could not detect ODF office:version. Pass --odf-version 1.3 or 1.4 explicitly."
        )
    if version not in {"1.3", "1.4"}:
        raise SystemExit(
            "ERROR: detected ODF office:version="
            f"{version}, but this skill currently bundles only ODF 1.3 and 1.4 schemas."
        )
    return version


def validate_odf(args: argparse.Namespace) -> int:
    xml_bytes = extract_xml_source(args)
    version = args.odf_version or infer_odf_version(xml_bytes)
    schema_path = ODF_SCHEMA_ROOT / f"v{version}-os" / f"OpenDocument-v{version}-schema.rng"
    if not schema_path.exists():
        raise SystemExit(f"ERROR: bundled ODF schema not found: {schema_path}")
    try:
        relaxng = etree.RelaxNG(etree.parse(str(schema_path)))
        doc = etree.fromstring(xml_bytes)
    except etree.XMLSyntaxError as exc:
        eprint(f"FAIL: could not parse ODF XML: {exc}")
        return 1
    if relaxng.validate(doc):
        print(f"PASS: ODF XML validates against {schema_display_path(schema_path)}")
        return 0
    eprint(f"FAIL: ODF XML does not validate against {schema_display_path(schema_path)}")
    for entry in relaxng.error_log:
        eprint(f"  line {entry.line}: {entry.message}")
    return 1


def validate_ooxml(args: argparse.Namespace) -> int:
    if not args.schema:
        raise SystemExit("ERROR: --schema is required for OOXML validation.")
    key = (args.schema.lower(), bool(args.strict))
    schema_path = OOXML_SCHEMA_MAP.get(key)
    if not schema_path:
        raise SystemExit(
            "ERROR: unsupported OOXML schema key. Use one of: "
            "wml, sml, pml, dml-main, opc-contenttypes, opc-coreproperties, "
            "opc-digsig, opc-relationships."
        )
    xml_bytes = extract_xml_source(args)
    with tempfile.TemporaryDirectory() as tmpdir:
        staged_entry = OoxmlSchemaStager().stage(schema_path, Path(tmpdir))
        try:
            schema = etree.XMLSchema(etree.parse(str(staged_entry)))
            doc = etree.fromstring(xml_bytes)
        except etree.XMLSyntaxError as exc:
            eprint(f"FAIL: could not parse OOXML XML: {exc}")
            return 1
        if schema.validate(doc):
            print(
                "PASS: OOXML XML validates against "
                f"{schema_display_path(schema_path)}"
            )
            return 0
        eprint(
            "FAIL: OOXML XML does not validate against "
            f"{schema_display_path(schema_path)}"
        )
        for entry in schema.error_log:
            eprint(f"  line {entry.line}: {entry.message}")
        return 1


def main(argv: list[str] | None = None) -> int:
    require_lxml()
    args = parse_args(argv)
    if args.family == "odf":
        return validate_odf(args)
    return validate_ooxml(args)


if __name__ == "__main__":
    raise SystemExit(main())
