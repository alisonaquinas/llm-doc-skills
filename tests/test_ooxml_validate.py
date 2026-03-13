"""Tests for office-custom/scripts/validate.py — generic OOXML validation."""

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

# Ensure repo root is importable
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tests._fixtures import make_minimal_docx  # noqa: E402


class TestOoxmlValidate(unittest.TestCase):
    """Tests for the generic OOXML structural validator."""

    def _validate(self, path: Path, quiet: bool = True) -> bool:
        # Import lazily so path manipulation is already done
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "validate",
            REPO_ROOT / "office-custom" / "scripts" / "validate.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.validate(path, quiet=quiet)

    def test_valid_minimal_docx_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_minimal_docx(Path(tmp) / "ok.docx")
            self.assertTrue(self._validate(path))

    def test_missing_content_types_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.docx"
            # Write a ZIP without [Content_Types].xml
            with zipfile.ZipFile(path, "w") as zf:
                zf.writestr("_rels/.rels", "<Relationships/>")
                zf.writestr("word/document.xml", "<doc/>")
            self.assertFalse(self._validate(path))

    def test_missing_root_rels_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.docx"
            with zipfile.ZipFile(path, "w") as zf:
                zf.writestr("[Content_Types].xml", '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
                # _rels/.rels intentionally omitted
                zf.writestr("word/document.xml", "<doc/>")
            self.assertFalse(self._validate(path))

    def test_malformed_xml_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.docx"
            with zipfile.ZipFile(path, "w") as zf:
                zf.writestr("[Content_Types].xml", '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
                zf.writestr("_rels/.rels", "<Relationships/>")
                zf.writestr("word/document.xml", "<unclosed>")  # malformed
            self.assertFalse(self._validate(path))

    def test_not_a_zip_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "notzip.docx"
            path.write_bytes(b"This is not a ZIP file at all.")
            self.assertFalse(self._validate(path))

    def test_nonexistent_file_fails(self):
        path = Path("/tmp/does_not_exist_ever_12345.docx")
        self.assertFalse(self._validate(path))


if __name__ == "__main__":
    unittest.main()
