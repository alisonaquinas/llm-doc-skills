"""Tests for office-custom/scripts/lint_docx.py — pre-delivery corruption lint."""

import importlib.util
import io
import sys
import unittest
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tests._fixtures import make_docx_bytes  # noqa: E402

SCRIPTS_DIR = REPO_ROOT / "skills" / "office-custom" / "scripts"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lint_docx = _load("lint_docx")


def _docx_with(extra: dict, tmp_path: Path, name: str = "d.docx") -> Path:
    data = make_docx_bytes(extra_members={k: v.encode() if isinstance(v, str) else v
                                          for k, v in extra.items()})
    out = tmp_path / name
    out.write_bytes(data)
    return out


class TestLintDocx(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = Path(tempfile.mkdtemp(prefix="lint-"))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write(self, members: dict) -> Path:
        buf = io.BytesIO(make_docx_bytes())
        # Rebuild zip overriding members.
        base = {}
        with zipfile.ZipFile(buf, "r") as zf:
            for n in zf.namelist():
                base[n] = zf.read(n)
        base.update({k: (v.encode() if isinstance(v, str) else v) for k, v in members.items()})
        out = self.tmp / "d.docx"
        with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for n, d in base.items():
                zf.writestr(n, d)
        return out

    # A content-type-complete CT declaring the fixture's png/jpeg media, so a
    # genuinely clean package passes (the minimal fixture omits image types).
    _COMPLETE_CT = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Default Extension="jpeg" ContentType="image/jpeg"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
        '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
        '<Override PartName="/word/footer2.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
        '</Types>'
    )

    def test_clean_docx_passes(self):
        out = self._write({"[Content_Types].xml": self._COMPLETE_CT})
        self.assertTrue(lint_docx.lint(out, quiet=True))

    def test_prefixed_rels_fails(self):
        bad_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<ns0:Relationships xmlns:ns0="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<ns0:Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="word/document.xml"/></ns0:Relationships>'
        )
        out = self._write({"_rels/.rels": bad_rels})
        self.assertFalse(lint_docx.lint(out, quiet=True))

    def test_prefixed_content_types_fails(self):
        bad_ct = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<ns0:Types xmlns:ns0="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<ns0:Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<ns0:Default Extension="xml" ContentType="application/xml"/>'
            '<ns0:Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '</ns0:Types>'
        )
        out = self._write({"[Content_Types].xml": bad_ct})
        self.assertFalse(lint_docx.lint(out, quiet=True))

    def test_numbering_missing_durable_id_warns_but_passes(self):
        numbering = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid">'
            '<w:abstractNum w:abstractNumId="0"/>'
            '<w:num w:numId="1" w16cid:durableId="111111"/>'
            '<w:num w:numId="2"/>'  # missing durableId — the injected one
            '</w:numbering>'
        )
        ct = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Default Extension="png" ContentType="image/png"/>'
            '<Default Extension="jpeg" ContentType="image/jpeg"/>'
            '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
            '</Types>'
        )
        out = self._write({"word/numbering.xml": numbering, "[Content_Types].xml": ct})
        # Warning only — still returns True (deliverable, but flagged).
        self.assertTrue(lint_docx.lint(out, quiet=True))

    def test_missing_content_type_override_fails(self):
        # Add an .xyz part with no Default/Override.
        out = self._write({"word/custom.xyz": b"data"})
        self.assertFalse(lint_docx.lint(out, quiet=True))


if __name__ == "__main__":
    unittest.main()
