---
name: raw-document
description: "Last-resort skill for working directly with raw OOXML (Office Open XML) or ODF (OpenDocument Format) document structure. Use ONLY when the higher-level skills ($docx-custom, $pptx-custom, $xlsx-custom, $office-custom) have failed, are not applicable, or when the task explicitly requires schema-level, package-level, or cross-format work: validating against XSD/RELAX NG schemas, recovering malformed archives, researching the format specification, mapping elements between OOXML and ODF, or authoring tooling that operates below the library API layer. Do NOT use for ordinary document creation, editing, or extraction — prefer $docx-custom, $pptx-custom, or $xlsx-custom first."
---

# Raw Document Structure

> **Last resort.** Before loading this skill, confirm that none of these cover the task:
>
> - Ordinary `.docx` work → `$docx-custom`
> - Ordinary `.pptx` work → `$pptx-custom`
> - Ordinary `.xlsx` work → `$xlsx-custom`
> - Unpack / repack / validate OOXML → `$office-custom`

Load this skill when the task requires direct work at the package or XML level
that the higher-level skills cannot reach: schema validation, format recovery,
specification research, cross-format element mapping, or building tools that
parse raw parts.

## Intent Router

| Task | Load |
|------|------|
| Understand OOXML package / ZIP layout | `references/ooxml/03-package-structure.md` |
| Understand ODF package / ZIP layout | `references/odf/03-package-structure.md` |
| Look up OOXML XML namespaces | `references/ooxml/04-xml-namespaces.md` |
| Look up ODF XML namespaces | `references/odf/04-xml-namespaces.md` |
| WordprocessingML element reference | `references/ooxml/05-wordprocessingml.md` |
| SpreadsheetML element reference | `references/ooxml/06-spreadsheetml.md` |
| PresentationML element reference | `references/ooxml/07-presentationml.md` |
| DrawingML shapes / charts / images | `references/ooxml/08-drawingml.md` |
| OOXML styles and themes | `references/ooxml/09-styles-themes.md` |
| OPC content types and relationships | `references/ooxml/10-relationships-content-types.md` |
| ODF text document elements | `references/odf/05-text-documents.md` |
| ODF spreadsheet elements | `references/odf/06-spreadsheets.md` |
| ODF presentation elements | `references/odf/07-presentations.md` |
| ODF drawing and graphics | `references/odf/08-drawing-graphics.md` |
| ODF styles and formatting | `references/odf/09-styles-formatting.md` |
| ODF metadata | `references/odf/10-metadata.md` |
| ODF security and digital signatures | `references/odf/11-security-signatures.md` |
| Compare OOXML vs ODF side-by-side | `references/interop/01-comparison.md` |
| Convert between OOXML and ODF | `references/interop/02-conversion.md` |
| Map elements OOXML ↔ ODF | `references/interop/03-feature-mapping.md` |
| OOXML tooling (python-docx, openpyxl, etc.) | `references/ooxml/12-tooling.md` |
| ODF tooling (odfpy, odfdo, etc.) | `references/odf/13-tooling.md` |
| Schema file locations | `references/schemas-README.md` |

---

## When to Use This Skill

### Appropriate uses

- **Schema validation** — validating a document part against XSD or RELAX NG
  schemas in `assets/schemas/`
- **Format recovery** — fixing a malformed or truncated archive where a library
  cannot open the file at all
- **Specification research** — answering questions about the ECMA-376 / ISO 29500
  or OASIS ODF specification at element or attribute level
- **Interoperability work** — mapping features across OOXML and ODF, diagnosing
  round-trip conversion losses
- **Tooling development** — writing parsers, validators, or transformers that
  operate on raw ZIP parts rather than through a document library
- **Edge-case debugging** — when a library produces structurally valid but
  semantically wrong output and the cause must be traced in raw XML

### Inappropriate uses (use the other skills instead)

| Task | Use instead |
|------|------------|
| Create or edit a Word document | `$docx-custom` |
| Create or edit a PowerPoint deck | `$pptx-custom` |
| Create or edit an Excel workbook | `$xlsx-custom` |
| Unpack / repack / validate OOXML via scripts | `$office-custom` |

---

## OOXML Quick Reference

### Package Structure (`.docx` / `.xlsx` / `.pptx`)

All OOXML files are ZIP archives (OPC packages).

```text
document.docx
├── [Content_Types].xml          ← MIME type for every part
├── _rels/.rels                  ← top-level relationships
├── word/
│   ├── document.xml             ← main body (w: namespace)
│   ├── styles.xml
│   ├── settings.xml
│   ├── numbering.xml
│   ├── theme/theme1.xml
│   ├── media/                   ← embedded images
│   └── _rels/document.xml.rels  ← part relationships
└── docProps/
    ├── app.xml
    └── core.xml
```

Full layout reference → `references/ooxml/03-package-structure.md`

### Key OOXML Namespaces

| Prefix | URI | Used for |
|--------|-----|----------|
| `w:` | `http://schemas.openxmlformats.org/wordprocessingml/2006/main` | Word parts |
| `x:` (or `s:`) | `http://schemas.openxmlformats.org/spreadsheetml/2006/main` | Excel parts |
| `p:` | `http://schemas.openxmlformats.org/presentationml/2006/main` | PowerPoint parts |
| `a:` | `http://schemas.openxmlformats.org/drawingml/2006/main` | DrawingML |
| `r:` | `http://schemas.openxmlformats.org/officeDocument/2006/relationships` | Relationship references |
| `mc:` | `http://schemas.openxmlformats.org/markup-compatibility/2006` | Markup Compatibility |

Full namespace reference → `references/ooxml/04-xml-namespaces.md`

### Conformance: Strict vs Transitional

| Aspect | Transitional | Strict |
|--------|-------------|--------|
| Real-world files | Near-universal | Rare |
| VML support | Yes | No |
| Deprecated attributes | Allowed | Disallowed |
| Schema location | `assets/schemas/ooxml/` (XSD), `assets/schemas/ooxml/relaxng/transitional/` (RNC) | `assets/schemas/ooxml/strict/`, `assets/schemas/ooxml/relaxng/strict/` |

---

## ODF Quick Reference

### Package Structure (`.odt` / `.ods` / `.odp`)

```text
document.odt
├── mimetype                     ← first file; uncompressed; signals ODF type
├── META-INF/manifest.xml        ← lists every file in package
├── content.xml                  ← document content (text:, table:, draw:)
├── styles.xml                   ← named styles and page layouts
├── meta.xml                     ← document metadata (dc:, meta:)
├── settings.xml                 ← application-specific settings
└── Pictures/                    ← embedded images
```

Full layout reference → `references/odf/03-package-structure.md`

### Key ODF Namespaces

| Prefix | URI | Used for |
|--------|-----|----------|
| `office:` | `urn:oasis:names:tc:opendocument:xmlns:office:1.0` | Root elements |
| `text:` | `urn:oasis:names:tc:opendocument:xmlns:text:1.0` | Text content |
| `table:` | `urn:oasis:names:tc:opendocument:xmlns:table:1.0` | Tables / spreadsheets |
| `draw:` | `urn:oasis:names:tc:opendocument:xmlns:drawing:1.0` | Shapes / graphics |
| `style:` | `urn:oasis:names:tc:opendocument:xmlns:style:1.0` | Style definitions |
| `fo:` | `urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0` | Formatting properties |
| `svg:` | `urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0` | SVG geometry |

Full namespace reference → `references/odf/04-xml-namespaces.md`

---

## Schema Assets

All schemas are in `assets/schemas/`. Do not fetch them from the network —
load from the local copies.

### ODF Schemas (RELAX NG)

| Path | Version | Description |
|------|---------|-------------|
| `assets/schemas/odf/v1.3-os/OpenDocument-v1.3-schema.rng` | ODF 1.3 | Main document schema |
| `assets/schemas/odf/v1.3-os/OpenDocument-v1.3-manifest-schema.rng` | ODF 1.3 | Package manifest |
| `assets/schemas/odf/v1.3-os/OpenDocument-v1.3-dsig-schema.rng` | ODF 1.3 | Digital signatures |
| `assets/schemas/odf/v1.4-os/OpenDocument-v1.4-schema.rng` | ODF 1.4 | Main document schema |
| `assets/schemas/odf/v1.4-os/OpenDocument-v1.4-manifest-schema.rng` | ODF 1.4 | Package manifest |
| `assets/schemas/odf/v1.4-os/OpenDocument-v1.4-dsig-schema.rng` | ODF 1.4 | Digital signatures |

### OOXML XSD Schemas (Transitional, normative per ISO/IEC 29500)

| Path | Description |
|------|-------------|
| `assets/schemas/ooxml/wml/wml.xsd` | WordprocessingML |
| `assets/schemas/ooxml/sml/sml.xsd` | SpreadsheetML |
| `assets/schemas/ooxml/pml/pml.xsd` | PresentationML |
| `assets/schemas/ooxml/dml/dml-main.xsd` | DrawingML core |
| `assets/schemas/ooxml/dml/dml-chart.xsd` | Charts |
| `assets/schemas/ooxml/shared/` | Shared types, math, bibliography, properties |
| `assets/schemas/ooxml/opc/` | Open Packaging Conventions |
| `assets/schemas/ooxml/vml/` | VML (Transitional only) |
| `assets/schemas/ooxml/strict/` | Strict conformance class XSDs |

### OOXML RELAX NG Schemas (normative per ECMA-376)

| Path | Description |
|------|-------------|
| `assets/schemas/ooxml/relaxng/transitional/` | 92 `.rnc` files — Transitional |
| `assets/schemas/ooxml/relaxng/strict/` | 86 `.rnc` files — Strict |
| `assets/schemas/ooxml/relaxng/opc/` | 5 `.rnc` files — OPC |

Full schema inventory → `references/schemas-README.md`

---

## Common Raw Operations

### Inspect a document's XML parts

```bash
# List all parts
unzip -l document.docx

# Inspect a specific part
unzip -p document.docx word/document.xml | xmllint --format -

# Inspect content types
unzip -p document.docx "[Content_Types].xml" | xmllint --format -
```

### Validate against XSD

```bash
# Validate WordprocessingML document part
xmllint --schema assets/schemas/ooxml/wml/wml.xsd word/document.xml --noout

# Validate ODF content
xmllint --schema assets/schemas/odf/v1.3-os/OpenDocument-v1.3-schema.rng \
  content.xml --noout --relaxng
```

### Validate with Python (xmlschema)

```python
import xmlschema
import zipfile

schema = xmlschema.XMLSchema("assets/schemas/ooxml/wml/wml.xsd")

with zipfile.ZipFile("document.docx") as z:
    with z.open("word/document.xml") as f:
        errors = list(schema.iter_errors(f))
        for err in errors:
            print(err)
```

### Unpack and repack manually

```bash
# Unpack (use office-custom scripts if available)
mkdir unpacked && cd unpacked && unzip ../document.docx

# Repack preserving OOXML requirements (mimetype must be first and uncompressed for ODF)
cd unpacked
zip -r ../output.docx . -x "*.DS_Store"

# For ODF: mimetype must be first and stored (not compressed)
zip -r0 ../output.odt mimetype
zip -r ../output.odt . -x mimetype -x "*.DS_Store"
```

---

## Relationship to Other Skills

- **`$office-custom`** — provides `unpack.py`, `pack.py`, `validate.py`, and `soffice.py` scripts that handle the raw ZIP round-trip workflow for OOXML. Start there for OOXML unpack/repack tasks.
- **`$docx-custom`** — XML editing patterns, tracked changes, comments, and images in Word documents. Use raw-document only when docx-custom's XML Reference section is insufficient.
- **`$pptx-custom`** — presentation structure. Refer to `references/ooxml/07-presentationml.md` here for element-level detail not in the pptx-custom skill.
- **`$xlsx-custom`** — workbook structure. Refer to `references/ooxml/06-spreadsheetml.md` here for element-level detail not in the xlsx-custom skill.
