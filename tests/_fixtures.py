"""Synthetic OOXML fixture builders for unit tests.

These helpers create minimal but structurally correct OOXML packages in
temporary directories using only the Python standard library.  No customer
files are committed; fixtures are generated fresh for each test run.
"""

from __future__ import annotations

import io
import zipfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Minimal OOXML content templates
# ---------------------------------------------------------------------------

CONTENT_TYPES_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml"
    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml"
    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/header1.xml"
    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
  <Override PartName="/word/footer1.xml"
    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
  <Override PartName="/word/footer2.xml"
    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
</Types>
"""

ROOT_RELS_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
    Target="word/document.xml"/>
</Relationships>
"""

DOCUMENT_RELS_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header"
    Target="header1.xml"/>
  <Relationship Id="rId2"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer"
    Target="footer1.xml"/>
  <Relationship Id="rId3"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer"
    Target="footer2.xml"/>
</Relationships>
"""

HEADER1_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:p><w:r><w:t>Orthomerica header</w:t></w:r></w:p>
</w:hdr>
"""

FOOTER1_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p><w:r><w:t>Confidential Material</w:t></w:r></w:p>
  <w:p><w:r><w:t>Do not distribute without authorization.</w:t></w:r></w:p>
</w:ftr>
"""

# footer2.xml includes the brand footer art markers expected by fidelity checks.
FOOTER2_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
       xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main">
  <w:p>
    <w:r>
      <w:drawing>
        <a:blip r:embed="rId1" cstate="print">
          <a:extLst>
            <a:ext uri="{{C557B03A-5A71-11CF-8700-00AA0060263B}}">
              <a14:useLocalDpi val="0"/>
            </a:ext>
          </a:extLst>
        </a:blip>
        <a:solidFill>
          <a:srgbClr val="4472C4">
            <a:alphaModFix amt="5000"/>
          </a:srgbClr>
        </a:solidFill>
      </w:drawing>
    </w:r>
  </w:p>
</w:ftr>
"""

FOOTER2_XML_BROKEN = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
       xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:p>
    <w:r>
      <w:drawing>
        <a:blip r:embed="rId1">
          <!-- cstate and useLocalDpi stripped — simulates naive round-trip -->
        </a:blip>
      </w:drawing>
    </w:r>
  </w:p>
</w:ftr>
"""

FOOTER1_RELS_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
    Target="../media/image1.png"/>
</Relationships>
"""

FOOTER2_RELS_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
    Target="../media/image2.jpeg"/>
</Relationships>
"""

HEADER1_RELS_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>
"""

# Minimal 1×1 transparent PNG bytes (not a real logo, just a valid PNG header)
PNG_BYTES = bytes([
    0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # PNG signature
    0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,  # IHDR chunk length+type
    0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,  # 1x1
    0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53,  # 8-bit RGB
    0xDE, 0x00, 0x00, 0x00, 0x0C, 0x49, 0x44, 0x41,  # IDAT chunk
    0x54, 0x08, 0xD7, 0x63, 0xF8, 0xCF, 0xC0, 0x00,
    0x00, 0x00, 0x02, 0x00, 0x01, 0xE2, 0x21, 0xBC,
    0x33, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E,  # IEND chunk
    0x44, 0xAE, 0x42, 0x60, 0x82,
])

# Minimal valid JPEG bytes (SOI + EOI markers)
JPEG_BYTES = bytes([0xFF, 0xD8, 0xFF, 0xD9])


def _make_document_xml(
    paragraphs: list[str] | None = None,
    page_width: int = 12240,
    left_margin: int = 1440,
    right_margin: int = 720,
) -> str:
    """Build a minimal word/document.xml with the given paragraph texts."""
    if paragraphs is None:
        paragraphs = ["Sample body text."]

    para_xml = "\n".join(
        f'    <w:p><w:pPr><w:pStyle w:val="p1"/></w:pPr>'
        f'<w:r><w:t xml:space="preserve">{p}</w:t></w:r></w:p>'
        for p in paragraphs
    )

    return f"""\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{para_xml}
    <w:sectPr>
      <w:headerReference w:type="default" r:id="rId1"/>
      <w:footerReference w:type="default" r:id="rId2"/>
      <w:footerReference w:type="first" r:id="rId3"/>
      <w:pgSz w:w="{page_width}" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="{right_margin}" w:bottom="1440" w:left="{left_margin}"/>
    </w:sectPr>
  </w:body>
</w:document>
"""


def make_minimal_docx(
    path: Path,
    *,
    footer2_xml: str = FOOTER2_XML,
    extra_members: dict[str, bytes] | None = None,
    document_xml: str | None = None,
    paragraphs: list[str] | None = None,
) -> Path:
    """Write a minimal valid DOCX to *path* and return it.

    Parameters
    ----------
    path:
        Output file path.
    footer2_xml:
        Content for word/footer2.xml (default includes all fidelity markers).
    extra_members:
        Additional ZIP members to include or override.
    document_xml:
        Override for word/document.xml.
    paragraphs:
        Paragraph texts to include in the default document.xml.
    """
    members: dict[str, bytes] = {
        "[Content_Types].xml": CONTENT_TYPES_XML.encode(),
        "_rels/.rels": ROOT_RELS_XML.encode(),
        "word/_rels/document.xml.rels": DOCUMENT_RELS_XML.encode(),
        "word/document.xml": (document_xml or _make_document_xml(paragraphs)).encode(),
        "word/header1.xml": HEADER1_XML.encode(),
        "word/_rels/header1.xml.rels": HEADER1_RELS_XML.encode(),
        "word/footer1.xml": FOOTER1_XML.encode(),
        "word/_rels/footer1.xml.rels": FOOTER1_RELS_XML.encode(),
        "word/footer2.xml": footer2_xml.encode(),
        "word/_rels/footer2.xml.rels": FOOTER2_RELS_XML.encode(),
        "word/media/image1.png": PNG_BYTES,
        "word/media/image2.jpeg": JPEG_BYTES,
    }
    if extra_members:
        members.update(extra_members)

    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, data in members.items():
            zf.writestr(name, data)
    return path


def make_docx_bytes(
    *,
    footer2_xml: str = FOOTER2_XML,
    extra_members: dict[str, bytes] | None = None,
    document_xml: str | None = None,
    paragraphs: list[str] | None = None,
) -> bytes:
    """Return a minimal DOCX as bytes (no file I/O)."""
    buf = io.BytesIO()
    members: dict[str, bytes] = {
        "[Content_Types].xml": CONTENT_TYPES_XML.encode(),
        "_rels/.rels": ROOT_RELS_XML.encode(),
        "word/_rels/document.xml.rels": DOCUMENT_RELS_XML.encode(),
        "word/document.xml": (document_xml or _make_document_xml(paragraphs)).encode(),
        "word/header1.xml": HEADER1_XML.encode(),
        "word/_rels/header1.xml.rels": HEADER1_RELS_XML.encode(),
        "word/footer1.xml": FOOTER1_XML.encode(),
        "word/_rels/footer1.xml.rels": FOOTER1_RELS_XML.encode(),
        "word/footer2.xml": footer2_xml.encode(),
        "word/_rels/footer2.xml.rels": FOOTER2_RELS_XML.encode(),
        "word/media/image1.png": PNG_BYTES,
        "word/media/image2.jpeg": JPEG_BYTES,
    }
    if extra_members:
        members.update(extra_members)
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, data in members.items():
            zf.writestr(name, data)
    return buf.getvalue()
