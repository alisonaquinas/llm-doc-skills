# Open Office Document Formats — Research Library

A comprehensive reference collection covering both major open office document format standards:

- **ODF** — OpenDocument Format (ISO/IEC 26300, OASIS)
- **OOXML** — Office Open XML (ISO/IEC 29500, ECMA-376)

---

## Quick Navigation

| What You Need | Go To |
| --- | --- |
| I'm new to ODF | [ODF Overview](./odf/01-overview.md) |
| I'm new to OOXML | [OOXML Overview](./ooxml/01-overview.md) |
| Compare ODF and OOXML | [Comparison](./interop/01-comparison.md) |
| Convert between formats | [Conversion Guide](./interop/02-conversion.md) |
| XML element/namespace reference | [ODF Namespaces](./odf/04-xml-namespaces.md) · [OOXML Namespaces](./ooxml/04-xml-namespaces.md) |
| Word processing (ODT/DOCX) | [ODF Text Docs](./odf/05-text-documents.md) · [OOXML WordprocessingML](./ooxml/05-wordprocessingml.md) |
| Spreadsheets (ODS/XLSX) | [ODF Spreadsheets](./odf/06-spreadsheets.md) · [OOXML SpreadsheetML](./ooxml/06-spreadsheetml.md) |
| Presentations (ODP/PPTX) | [ODF Presentations](./odf/07-presentations.md) · [OOXML PresentationML](./ooxml/07-presentationml.md) |
| Graphics and shapes | [ODF Drawing](./odf/08-drawing-graphics.md) · [OOXML DrawingML](./ooxml/08-drawingml.md) |
| Styles and formatting | [ODF Styles](./odf/09-styles-formatting.md) · [OOXML Styles & Themes](./ooxml/09-styles-themes.md) |
| Programming libraries | [ODF Tooling](./odf/13-tooling.md) · [OOXML Tooling](./ooxml/12-tooling.md) |
| Best practices | [ODF Best Practices](./odf/12-best-practices.md) · [OOXML Best Practices](./ooxml/11-best-practices.md) |
| Security and signatures | [ODF Security](./odf/11-security-signatures.md) |
| Feature mapping tables | [Feature Mapping](./interop/03-feature-mapping.md) |

---

## ODF Section

**Standard**: ISO/IEC 26300 / OASIS OpenDocument Format
**Current versions**: ODF 1.3 (OASIS Standard), ODF 1.4 (OASIS 2024)
**File extensions**: `.odt`, `.ods`, `.odp`, `.odg`, `.odc`, `.odf`, `.odb`

| # | File | Description |
| --- | --- | --- |
| 1 | [01-overview.md](./odf/01-overview.md) | What is ODF, history, standardization timeline, file types, key adopters |
| 2 | [02-specification.md](./odf/02-specification.md) | Spec documents (OASIS 1.2/1.3/1.4), RELAX NG schemas, conformance classes, normative references |
| 3 | [03-package-structure.md](./odf/03-package-structure.md) | ZIP package layout, `content.xml`, `styles.xml`, `meta.xml`, `manifest.xml`, encryption, digital signatures in packages |
| 4 | [04-xml-namespaces.md](./odf/04-xml-namespaces.md) | Complete namespace reference: `office:`, `text:`, `table:`, `draw:`, `style:`, `fo:`, `svg:`, external namespaces |
| 5 | [05-text-documents.md](./odf/05-text-documents.md) | `text:p`, `text:h`, `text:span`, `text:a`, lists, tables, frames, fields, bookmarks, footnotes, change tracking |
| 6 | [06-spreadsheets.md](./odf/06-spreadsheets.md) | `table:table`, cell types, OpenFormula syntax, merged cells, named ranges, pivot tables, data validation |
| 7 | [07-presentations.md](./odf/07-presentations.md) | `draw:page`, presentation classes, master pages, slide size, transitions (SMIL), animations, speaker notes |
| 8 | [08-drawing-graphics.md](./odf/08-drawing-graphics.md) | `draw:frame`, shapes (`draw:rect`, `draw:circle`, `draw:path`), connectors, groups, fills, strokes, layers, charts |
| 9 | [09-styles-formatting.md](./odf/09-styles-formatting.md) | Named vs automatic styles, style families, paragraph/text properties (`fo:` attributes), page layouts, list styles, data styles, inheritance |
| 10 | [10-metadata.md](./odf/10-metadata.md) | `meta.xml` elements, Dublin Core, ODF-specific metadata, RDF metadata (ODF 1.2+), user-defined fields |
| 11 | [11-security-signatures.md](./odf/11-security-signatures.md) | Password encryption (AES-256/PBKDF2), OpenPGP (ODF 1.3), protection locks, digital signatures, XAdES |
| 12 | [12-best-practices.md](./odf/12-best-practices.md) | Named styles, package requirements, interoperability testing, accessibility, long-term preservation |
| 13 | [13-tooling.md](./odf/13-tooling.md) | odfpy, odfdo, ODF Toolkit (Java), LibreOffice headless, XSLT processing, validation tools |

---

## OOXML Section

**Standard**: ISO/IEC 29500 / ECMA-376
**Current version**: ECMA-376 5th Edition / ISO/IEC 29500:2016
**File extensions**: `.docx`, `.xlsx`, `.pptx` (and macro/template variants)

| # | File | Description |
| --- | --- | --- |
| 1 | [01-overview.md](./ooxml/01-overview.md) | What is OOXML, history, editions, Strict vs Transitional, file types, implementations |
| 2 | [02-specification.md](./ooxml/02-specification.md) | ECMA-376 editions, ISO/IEC 29500 parts, XSD schemas, conformance, MCE, normative references |
| 3 | [03-package-structure.md](./ooxml/03-package-structure.md) | ZIP/OPC structure for `.docx`, `.xlsx`, `.pptx`; `[Content_Types].xml`, `.rels` files, core/app properties |
| 4 | [04-xml-namespaces.md](./ooxml/04-xml-namespaces.md) | WordprocessingML (`w:`), SpreadsheetML (`x:`), PresentationML (`p:`), DrawingML (`a:`, `c:`, `pic:`), packaging namespaces, relationship type URIs |
| 5 | [05-wordprocessingml.md](./ooxml/05-wordprocessingml.md) | `w:document`, `w:p`, `w:r`, `w:t`, `w:pPr`, `w:rPr`, tables, sections, page layout, numbering, hyperlinks, comments, track changes, SDTs |
| 6 | [06-spreadsheetml.md](./ooxml/06-spreadsheetml.md) | `workbook.xml`, worksheet structure, cell types, shared strings, styles, formulas, merged cells, tables, pivot tables |
| 7 | [07-presentationml.md](./ooxml/07-presentationml.md) | `presentation.xml`, `p:sld`, placeholders, slide masters, layouts, slide transitions (all types), animations, speaker notes |
| 8 | [08-drawingml.md](./ooxml/08-drawingml.md) | Shapes and preset geometries, `a:spPr`, color models, text in shapes, pictures (`pic:pic`), charts, SmartArt, inline vs floating in Word |
| 9 | [09-styles-themes.md](./ooxml/09-styles-themes.md) | Theme XML (color scheme, fonts, effects), `styles.xml` structure, paragraph/character/table styles, built-in style IDs, SpreadsheetML number formats |
| 10 | [10-relationships-content-types.md](./ooxml/10-relationships-content-types.md) | OPC model, complete content type tables (docx/xlsx/pptx), relationship type URI reference, `.rels` file format, external relationships |
| 11 | [11-best-practices.md](./ooxml/11-best-practices.md) | Strict vs Transitional, validation, named styles, MCE usage, EMU measurements, image handling, accessibility, performance |
| 12 | [12-tooling.md](./ooxml/12-tooling.md) | Open XML SDK (.NET/C#), python-docx, openpyxl, python-pptx, Apache POI (Java), Node.js libraries (docx, xlsx/SheetJS, PptxGenJS), debugging tools |

---

## Interoperability Section

| # | File | Description |
| --- | --- | --- |
| 1 | [01-comparison.md](./interop/01-comparison.md) | Side-by-side comparison: governance, design philosophy, package format, XML characteristics, styles, features by category, security, government policy |
| 2 | [02-conversion.md](./interop/02-conversion.md) | Conversion tools (LibreOffice, Pandoc, MS Office, ONLYOFFICE), quality matrix by feature, ISO TR 29166, batch strategies, round-trip testing |
| 3 | [03-feature-mapping.md](./interop/03-feature-mapping.md) | Element-by-element mapping tables: text docs, tables, spreadsheets, presentations, styles, metadata, drawing, units, unavoidable losses |

---

## Key External References

### ODF Specifications

| Resource | URL |
| --- | --- |
| OASIS ODF 1.3 | <https://docs.oasis-open.org/office/OpenDocument/v1.3/> |
| OASIS ODF 1.2 | <https://docs.oasis-open.org/office/v1.2/> |
| OASIS ODF 1.4 (draft) | <https://oasis-tcs.github.io/odf-tc/odf1.4/> |
| ISO/IEC 26300 (free) | <https://standards.iso.org/ittf/PubliclyAvailableStandards/> |
| OASIS ODF TC | <https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=office> |
| ODF Validator | <https://odfvalidator.org/> |

### OOXML Specifications

| Resource | URL |
| --- | --- |
| ECMA-376 5th Edition | <https://ecma-international.org/publications-and-standards/standards/ecma-376/> |
| ISO/IEC 29500 (free) | <https://standards.iso.org/ittf/PubliclyAvailableStandards/> |
| officeopenxml.com | <http://officeopenxml.com/> |
| ooxml.info | <https://ooxml.info/docs/> |
| Microsoft Open XML SDK | <https://learn.microsoft.com/en-us/office/open-xml/open-xml-sdk> |
| MS-OE376 (deviations) | <https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oe376/> |

### Interoperability

| Resource | URL |
| --- | --- |
| ISO/IEC TR 29166 | <https://www.iso.org/standard/45245.html> |
| Library of Congress FDD (ODF) | <https://www.loc.gov/preservation/digital/formats/fdd/fdd000247.shtml> |
| Library of Congress FDD (OOXML) | <https://www.loc.gov/preservation/digital/formats/fdd/fdd000395.shtml> |
| UK Gov ODF guidance | <https://www.gov.uk/guidance/using-open-document-formats-odf-in-your-organisation> |

### Tools and Libraries

| Tool | Language | Format | URL |
| --- | --- | --- | --- |
| odfpy | Python | ODF | <https://github.com/eea/odfpy> |
| odfdo | Python | ODF | <https://github.com/jdum/odfdo> |
| ODF Toolkit | Java | ODF | <https://odftoolkit.org/> |
| python-docx | Python | OOXML (docx) | <https://python-docx.readthedocs.io/> |
| openpyxl | Python | OOXML (xlsx) | <https://openpyxl.readthedocs.io/> |
| python-pptx | Python | OOXML (pptx) | <https://python-pptx.readthedocs.io/> |
| Open XML SDK | .NET/C# | OOXML | <https://github.com/dotnet/Open-XML-SDK> |
| Apache POI | Java | ODF + OOXML | <https://poi.apache.org/> |
| LibreOffice | Headless | Both | <https://www.libreoffice.org> |
| Pandoc | CLI | Both (via AST) | <https://pandoc.org> |

---

## Directory Structure

```text
research/
├── README.md                    ← This file
├── odf/
│   ├── 01-overview.md
│   ├── 02-specification.md
│   ├── 03-package-structure.md
│   ├── 04-xml-namespaces.md
│   ├── 05-text-documents.md
│   ├── 06-spreadsheets.md
│   ├── 07-presentations.md
│   ├── 08-drawing-graphics.md
│   ├── 09-styles-formatting.md
│   ├── 10-metadata.md
│   ├── 11-security-signatures.md
│   ├── 12-best-practices.md
│   └── 13-tooling.md
├── ooxml/
│   ├── 01-overview.md
│   ├── 02-specification.md
│   ├── 03-package-structure.md
│   ├── 04-xml-namespaces.md
│   ├── 05-wordprocessingml.md
│   ├── 06-spreadsheetml.md
│   ├── 07-presentationml.md
│   ├── 08-drawingml.md
│   ├── 09-styles-themes.md
│   ├── 10-relationships-content-types.md
│   ├── 11-best-practices.md
│   └── 12-tooling.md
└── interop/
    ├── 01-comparison.md
    ├── 02-conversion.md
    └── 03-feature-mapping.md
```

---

*Total: 28 markdown files covering ODF and OOXML comprehensively.*
*Research based on: OASIS ODF 1.3 specification, ECMA-376 5th edition, ISO/IEC 26300:2015, ISO/IEC 29500:2016, ISO/IEC TR 29166:2011, and official SDK documentation.*
