"""Tests for office-custom/scripts/pack.py serialization fidelity.

Regression coverage for the OPC package-part namespace bug: re-serializing
``.rels`` and ``[Content_Types].xml`` through ElementTree must NOT rewrite their
default (prefix-less) namespace as ``ns0:``.  A package whose relationship or
content-type roots are prefixed is well-formed XML — so validate.py passes it —
yet Word flags it for recovery and LibreOffice may refuse to open it.

The fix lives in pack.py; this test locks it in via a full unpack -> pack
round-trip on a synthetic DOCX.
"""

import importlib.util
import shutil
import sys
import tempfile
import unittest
import zipfile
from contextlib import contextmanager
from pathlib import Path
from xml.etree import ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tests._fixtures import make_minimal_docx  # noqa: E402

SCRIPTS_DIR = REPO_ROOT / "skills" / "office-custom" / "scripts"

# Package parts whose roots must keep the default (prefix-less) namespace.
_PACKAGE_PARTS = [
    "[Content_Types].xml",
    "_rels/.rels",
    "word/_rels/document.xml.rels",
    "word/_rels/footer1.xml.rels",
]


def _load_module(name: str):
    """Load a script from office-custom/scripts as a module."""
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@contextmanager
def _temp_dir(prefix: str):
    path = Path(tempfile.mkdtemp(prefix=prefix))
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


class TestPackPreservesPackageNamespaces(unittest.TestCase):
    """pack.py must not introduce ns0: prefixes on OPC package parts."""

    def _round_trip(self, tmp: Path) -> Path:
        """Build -> unpack -> pack and return the repacked file path."""
        unpack = _load_module("unpack")
        pack = _load_module("pack")

        original = tmp / "original.docx"
        make_minimal_docx(original)

        unpacked = tmp / "unpacked"
        unpack.unpack(original, unpacked, merge_runs=False)

        output = tmp / "repacked.docx"
        pack.pack(unpacked, output, original=original, validate=False)
        return output

    def test_package_parts_keep_default_namespace(self):
        with _temp_dir("pack-ns-") as tmp:
            output = self._round_trip(tmp)
            with zipfile.ZipFile(output, "r") as zf:
                names = set(zf.namelist())
                for part in _PACKAGE_PARTS:
                    self.assertIn(part, names, f"missing package part: {part}")
                    raw = zf.read(part).decode("utf-8", errors="replace")
                    self.assertNotIn(
                        "ns0:", raw,
                        f"{part} was re-serialized with a non-default namespace "
                        f"prefix (ns0:); Word will flag the file for recovery.",
                    )

    def test_relationship_roots_are_prefixless(self):
        with _temp_dir("pack-rels-") as tmp:
            output = self._round_trip(tmp)
            with zipfile.ZipFile(output, "r") as zf:
                rels = zf.read("_rels/.rels").decode("utf-8")
            self.assertIn("<Relationships", rels)
            self.assertIn("<Relationship ", rels)

    def test_content_types_root_is_prefixless(self):
        with _temp_dir("pack-ct-") as tmp:
            output = self._round_trip(tmp)
            with zipfile.ZipFile(output, "r") as zf:
                ct = zf.read("[Content_Types].xml").decode("utf-8")
            self.assertIn("<Types", ct)
            self.assertNotIn("<ns0:Types", ct)

    def test_document_body_keeps_w_prefix(self):
        """Sanity check: the fix must not disturb the main document namespace."""
        with _temp_dir("pack-w-") as tmp:
            output = self._round_trip(tmp)
            with zipfile.ZipFile(output, "r") as zf:
                doc = zf.read("word/document.xml").decode("utf-8")
            self.assertIn("<w:document", doc)
            self.assertNotIn("ns0:", doc)

    def test_mc_ignorable_prefixes_stay_declared_after_round_trip(self):
        """Round-tripping must not leave mc:Ignorable prefixes undeclared."""
        unpack = _load_module("unpack")
        pack = _load_module("pack")

        document_xml = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document mc:Ignorable="w14 w15 wp14"
            xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
            xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
            xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"
            xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing">
  <w:body>
    <w:p><w:r><w:t>Text</w:t></w:r></w:p>
    <w:sectPr/>
  </w:body>
</w:document>
"""

        with _temp_dir("pack-mc-") as tmp:
            original = tmp / "original.docx"
            make_minimal_docx(original, document_xml=document_xml)
            unpacked = tmp / "unpacked"
            unpack.unpack(original, unpacked, merge_runs=True)
            output = tmp / "repacked.docx"
            pack.pack(unpacked, output, original=original, validate=False)

            with zipfile.ZipFile(output, "r") as zf:
                doc = zf.read("word/document.xml").decode("utf-8")

            self.assertIn('mc:Ignorable="w14 w15 wp14"', doc)
            self.assertIn('xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"', doc)
            self.assertIn('xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"', doc)
            self.assertIn(
                'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"',
                doc,
            )

    def test_mc_ignorable_repair_handles_self_closing_root(self):
        """Namespace repair must keep self-closing roots well-formed."""
        pack = _load_module("pack")
        xml = (
            '<w:fonts xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
            'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'mc:Ignorable="w14 w15" />'
        )
        output = pack.condense_xml(xml).decode("utf-8")
        ET.fromstring(output.encode("utf-8"))
        self.assertIn('xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"', output)
        self.assertIn('xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"', output)


if __name__ == "__main__":
    unittest.main()
