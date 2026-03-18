"""Tests for raw-document/scripts/validate_xml.py."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import tempfile
import unittest
import zipfile
from pathlib import Path

from tests._fixtures import make_minimal_docx

try:
    from lxml import etree as _etree  # noqa: F401
except Exception:  # pragma: no cover - environment-specific
    _HAS_LXML = False
else:
    _HAS_LXML = True

try:
    from odf import text
    from odf.opendocument import OpenDocumentText
except Exception:  # pragma: no cover - environment-specific
    _HAS_ODFPY = False
else:
    _HAS_ODFPY = True

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "skills" / "raw-document" / "scripts" / "validate_xml.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("raw_document_validate_xml", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _make_valid_wml_document(path: Path, strict: bool = False) -> Path:
    ns = (
        "http://purl.oclc.org/ooxml/wordprocessingml/main"
        if strict
        else "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    )
    path.write_text(
        """<?xml version='1.0' encoding='UTF-8'?>
<w:document xmlns:w='{ns}'>
  <w:body>
    <w:p><w:r><w:t>Hello schema-valid WML</w:t></w:r></w:p>
    <w:sectPr>
      <w:pgSz w:w='12240' w:h='15840'/>
      <w:pgMar w:top='1440' w:right='720' w:bottom='1440' w:left='1440' w:header='708' w:footer='708' w:gutter='0'/>
    </w:sectPr>
  </w:body>
</w:document>
""".replace("{ns}", ns),
        encoding="utf-8",
    )
    return path


def _make_minimal_odf_content(path: Path, version: str = "1.3") -> Path:
    path.write_text(
        """<?xml version='1.0' encoding='UTF-8'?>
<office:document-content xmlns:office='urn:oasis:names:tc:opendocument:xmlns:office:1.0'
 xmlns:text='urn:oasis:names:tc:opendocument:xmlns:text:1.0'
 office:version='{version}'>
 <office:automatic-styles/>
 <office:body><office:text><text:p>Hello {version}</text:p></office:text></office:body>
</office:document-content>
""".replace("{version}", version),
        encoding="utf-8",
    )
    return path


@unittest.skipUnless(_HAS_LXML, "lxml is required for raw-document validation tests")
class TestRawDocumentValidateXml(unittest.TestCase):
    def setUp(self):
        self.mod = _load_module()

    def _run(self, *argv: str) -> tuple[int | None, str, str, str | None]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        exit_message = None
        code = None
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                code = self.mod.main(list(argv))
            except SystemExit as exc:
                code = exc.code if isinstance(exc.code, int) else None
                exit_message = exc.code if isinstance(exc.code, str) else None
        return code, stdout.getvalue(), stderr.getvalue(), exit_message

    def test_ooxml_package_validation_passes_for_schema_valid_docx(self):
        with tempfile.TemporaryDirectory() as tmp:
            document_xml = _make_valid_wml_document(Path(tmp) / "document.xml").read_text(encoding="utf-8")
            package = make_minimal_docx(Path(tmp) / "sample.docx", document_xml=document_xml)
            code, stdout, stderr, exit_message = self._run(
                "--family", "ooxml",
                "--schema", "wml",
                "--package", str(package),
                "--part", "word/document.xml",
            )
            self.assertEqual(0, code, exit_message or stderr)
            self.assertIn("PASS: OOXML XML validates", stdout)

    def test_ooxml_strict_validation_passes_for_minimal_strict_wml(self):
        with tempfile.TemporaryDirectory() as tmp:
            strict_xml = _make_valid_wml_document(Path(tmp) / "strict.xml", strict=True)
            code, stdout, stderr, exit_message = self._run(
                "--family", "ooxml",
                "--schema", "wml",
                "--strict",
                "--xml", str(strict_xml),
            )
            self.assertEqual(0, code, exit_message or stderr)
            self.assertIn("strict/wml.xsd", stdout)

    def test_ooxml_invalid_part_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad_xml = Path(tmp) / "bad.xml"
            bad_xml.write_text(
                "<w:document xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main'>",
                encoding="utf-8",
            )
            code, stdout, stderr, exit_message = self._run(
                "--family", "ooxml",
                "--schema", "wml",
                "--xml", str(bad_xml),
            )
            self.assertEqual(1, code, exit_message or stdout)
            self.assertIn("FAIL: could not parse OOXML XML", stderr)

    def test_odf_direct_validation_passes_for_minimal_1_3_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            content_xml = _make_minimal_odf_content(Path(tmp) / "content.xml", version="1.3")
            code, stdout, stderr, exit_message = self._run(
                "--family", "odf",
                "--xml", str(content_xml),
            )
            self.assertEqual(0, code, exit_message or stderr)
            self.assertIn("PASS: ODF XML validates", stdout)

    @unittest.skipUnless(_HAS_ODFPY, "odfpy is required for ODF 1.2 fixture generation")
    def test_odf_version_detection_rejects_1_2_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / "sample-1.2.odt"
            doc = OpenDocumentText()
            doc.text.addElement(text.P(text="Hello 1.2"))
            doc.save(str(package))
            with zipfile.ZipFile(package) as archive:
                content_xml = Path(tmp) / "content-1.2.xml"
                content_xml.write_bytes(archive.read("content.xml"))
            code, stdout, stderr, exit_message = self._run(
                "--family", "odf",
                "--xml", str(content_xml),
            )
            self.assertIsNone(code)
            self.assertIn("bundles only ODF 1.3 and 1.4 schemas", exit_message or "")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
