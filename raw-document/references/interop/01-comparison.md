# ODF vs OOXML — Comprehensive Comparison

> **Cross-references:** [ODF Overview](../odf/01-overview.md) | [OOXML Overview](../ooxml/01-overview.md) | [Conversion](./02-conversion.md) | [Feature Mapping](./03-feature-mapping.md)

---

## 1. Standards Governance

| Aspect | ODF | OOXML |
| --- | --- | --- |
| **Primary standard** | ISO/IEC 26300 | ISO/IEC 29500 / ECMA-376 |
| **Development body** | OASIS TC (vendor-neutral) | ECMA TC45 (Microsoft-led, then ISO) |
| **ISO version** | ISO/IEC 26300:2015 (v1.2), DIS v1.3 | ISO/IEC 29500:2016 |
| **Governance** | Open, multi-vendor consensus | Initially Microsoft-driven |
| **Versions** | ODF 1.0 – 1.4 (2005–2024) | ECMA-376 1st–5th ed. (2006–2015) |
| **Primary software** | LibreOffice, Apache OpenOffice | Microsoft Office |
| **Free download** | Yes (OASIS and ITTF) | Yes (ECMA and ITTF) |

---

## 2. Design Philosophy

### ODF Design Goals

- **Interoperability first** — designed for exchange between different applications
- **Vendor independence** — no single vendor controls the format
- **Simplicity where possible** — lean XML that's amenable to XSLT processing
- **Separation of concerns** — content, styles, metadata in distinct files
- **Long-term archival** — ISO adoption aimed at preservation use cases

### OOXML Design Goals

- **Backward compatibility** — faithfully represent existing Microsoft Office binary format features
- **Feature completeness** — preserve every capability of Word, Excel, PowerPoint
- **Microsoft ecosystem** — seamless with Windows, .NET, SharePoint, OneDrive
- **Extensibility** — MCE mechanism for forward/backward compat of extensions

---

## 3. Package Format Comparison

| Aspect | ODF | OOXML |
| --- | --- | --- |
| Container | ZIP (ODF Package) | ZIP (Open Packaging Conventions) |
| Package manifest | `META-INF/manifest.xml` | `[Content_Types].xml` |
| Relationships | Via `manifest.xml` | Separate `.rels` files |
| Content discovery | Manifest lists all files | Content types + relationships graph |
| `mimetype` file | Required, first, uncompressed | No equivalent |
| Single-file format | Flat ODF (`.fodt`, `.fods`, `.fodp`) | None standard |
| Part naming | Free paths within ZIP | `/word/`, `/xl/`, `/ppt/` conventions |

---

## 4. XML Characteristics

| Aspect | ODF | OOXML |
| --- | --- | --- |
| Schema language | RELAX NG (ISO/IEC 19757-2) | W3C XSD (XML Schema) |
| Namespaces | ~20 OASIS URNs + externals | ~15 OOXML URIs + Microsoft extensions |
| Root elements | `office:document-*` | `w:document`, `workbook`, `p:presentation` |
| Measurements | CSS/XSL-FO units (cm, pt, %) | Twips (word), EMU (DrawingML), custom units |
| Style references | `*:style-name` attribute | `*:val` with style ID |
| Formulas | OpenFormula (`of:` prefix) | Excel formula syntax |
| Color values | CSS hex `#RRGGBB` | Hex without `#`: `RRGGBB` |

---

## 5. Style System Comparison

| Aspect | ODF | OOXML |
| --- | --- | --- |
| Style types | Named + automatic styles | Named styles + direct formatting |
| Style inheritance | `style:parent-style-name` | `w:basedOn` |
| Default styles | `style:default-style` | `w:docDefaults` |
| Theme system | None (planned for 1.4) | Full theme XML with colors, fonts, effects |
| Style families | 16 families (paragraph, text, table, etc.) | 4 types (paragraph, character, table, numbering) |
| Table conditional | Via named style families | Extensive `w:tblStylePr` with 12 regions |
| Page layouts | `style:page-layout` + master page | `w:sectPr` per section |

---

## 6. Feature Coverage Comparison

### Text / Word Processing

| Feature | ODF | OOXML | Notes |
| --- | --- | --- | --- |
| Paragraphs | `text:p` | `w:p` | Equivalent |
| Headings | `text:h` + `outline-level` | `w:pStyle` + `w:outlineLvl` | Equivalent |
| Character styles | `text:span` | `w:r` with `w:rStyle` | Equivalent |
| Tables | `table:table` | `w:tbl` | Equivalent, different cell spanning syntax |
| Lists | `text:list` with list-style | `w:numPr` → `numbering.xml` | Both powerful, different model |
| Footnotes/endnotes | `text:footnote`, `text:endnote` | `footnotes.xml`, `endnotes.xml` | Equivalent |
| Comments | `office:annotation` | `comments.xml` | Equivalent |
| Track changes | `text:tracked-changes` | `w:ins`, `w:del`, `w:rPrChange` | Similar |
| Sections | `text:section` | `w:sectPr` | Different model |
| Fields | Rich field elements | SDTs, simple fields | Both powerful |
| Content controls | Limited | `w:sdt` (SDT) | OOXML more powerful |
| Change tracking | ODF 1.3 improvements | Mature | Both mature |

### Spreadsheets

| Feature | ODF | OOXML | Notes |
| --- | --- | --- | --- |
| Formula language | OpenFormula (standardized) | Excel formula (de facto standard) | OOXML more widely known |
| Cell types | `office:value-type` attribute | `c` element `t` attribute | Different but equivalent |
| Shared strings | Content embedded in cells | Separate `sharedStrings.xml` | OOXML more efficient for repetition |
| Conditional format | `table:conditional-formats` | `conditionalFormatting` | Equivalent |
| Pivot tables | `table:data-pilot-table` | `pivotTableDefinition` | Both supported |
| Data validation | `table:content-validations` | `dataValidations` | Equivalent |
| Charts | Separate ODF objects | DrawingML chart parts | OOXML more tightly integrated |
| Named ranges | `table:named-range` | `definedNames` | Equivalent |
| Tables (as objects) | `table:table` (all tables) | Separate `table` parts | OOXML distinguishes worksheet grids vs named tables |

### Presentations

| Feature | ODF | OOXML | Notes |
| --- | --- | --- | --- |
| Slides | `draw:page` | `p:sld` | Equivalent |
| Masters | `style:master-page` | `p:sldMaster` | Equivalent |
| Layouts | (limited) | `p:sldLayout` | OOXML has explicit layouts |
| Transitions | SMIL-based | PresentationML transitions | Both supported |
| Animations | SMIL-based | SMIL-like PML timing | Both powerful |
| Shapes | `draw:` elements | `p:sp` + DrawingML | Different but equivalent |
| Charts | Embedded ODF | DrawingML chart | Equivalent |
| SmartArt | Limited drawing support | Full `dgm:` namespace | OOXML significantly richer |
| Slide notes | `presentation:notes` | `p:notes` separate part | Equivalent |

---

## 7. Drawing and Graphics

| Feature | ODF | OOXML |
| --- | --- | --- |
| Shape library | SVG-like `draw:` elements | DrawingML preset geometries (200+) |
| Custom geometry | SVG path syntax | Custom path (similar to SVG) |
| Image embedding | Via `draw:frame` + `draw:image` | Via relationships to image parts |
| Image effects | Limited | Rich: shadows, reflections, glow, blur, 3D |
| Fill types | solid, gradient, bitmap, hatch | solid, gradient, pattern, picture/blip, group |
| Themes | None (ODF) | Full DrawingML theme system |
| SmartArt | Minimal | Full SmartArt system |
| VML (legacy) | Not applicable | Transitional VML support |

---

## 8. Metadata

| Feature | ODF | OOXML |
| --- | --- | --- |
| Basic metadata | Dublin Core in `meta.xml` | Dublin Core in `docProps/core.xml` |
| App-specific metadata | ODF-specific elements | `docProps/app.xml` |
| Custom metadata | `meta:user-defined` | Custom XML data parts |
| RDF metadata | Full RDF in ODF 1.2+ | Not standardized |
| Statistics | `meta:document-statistic` | In `app.xml` |

---

## 9. Security

| Feature | ODF | OOXML |
| --- | --- | --- |
| Password encryption | AES-256-CBC + PBKDF2 | AES-128 or AES-256 |
| OpenPGP encryption | Yes (ODF 1.3+) | No |
| Digital signatures | XML Signature + XAdES (1.3) | XML Signature via OPC |
| Protection locks | Section, sheet, cell protection | Document, section, sheet protection |
| IRM/DRM | Not in spec | Via MSOFFCRYPTO-TOOL / Information Rights Management |

---

## 10. Interoperability Assessment

### ODF Advantages

- Cleaner, smaller XML (better XSLT processing)
- Flat format option for VCS-friendly diffs
- Better for long-term archival and preservation
- Government mandate in many jurisdictions (UK, EU, India, etc.)
- Truly vendor-neutral governance
- OpenPGP encryption (1.3)

### OOXML Advantages

- Default format of Microsoft Office (most popular office suite)
- Richer theme system and visual effects
- More mature chart and SmartArt support
- More library support in the developer ecosystem
- Better backward compatibility with billions of existing documents
- Explicit slide layouts provide more structured template system

---

## 11. Government and Policy

| Jurisdiction | Policy |
| --- | --- |
| **UK Government** | ODF mandated for editable documents shared across government |
| **European Parliament** | ODF preferred for internal documents |
| **India** | ODF mandated for government documents |
| **Brazil** | ODF mandated for government |
| **Germany** | ODF preferred in government |
| **France** | ODF strongly recommended |
| **Netherlands** | ODF on "comply or explain" list |
| **United States** | No single mandate; ODF listed as acceptable |

---

*Next: [Conversion Guide →](./02-conversion.md)*
