# OOXML Specification Reference

> **Cross-references:** [Overview](./01-overview.md) | [Package Structure](./03-package-structure.md) | [XML Namespaces](./04-xml-namespaces.md)

---

## 1. Specification Editions

### ECMA-376 Editions

| Edition | Year | ISO/IEC Equivalent | Notes |
| --- | --- | --- | --- |
| 1st | Dec 2006 | — | Initial submission; basis for ISO fast-track |
| 2nd | Dec 2008 | ISO/IEC 29500:2008 | First ISO version |
| 3rd | Jun 2011 | ISO/IEC 29500:2011 | Corrections and clarifications |
| 4th | Dec 2012 | ISO/IEC 29500:2012 | Further corrections |
| **5th** | **Dec 2015** | **ISO/IEC 29500:2016** | **Current version** |

The 5th edition of ECMA-376 is available for free download:

- <https://ecma-international.org/publications-and-standards/standards/ecma-376/>

---

## 2. Standard Parts

### Part 1 — Fundamentals and Markup Language Reference

The core document. Contains:

- Fundamental concepts (document properties, content types)
- **WordprocessingML** — complete word processing markup
- **SpreadsheetML** — complete spreadsheet markup
- **PresentationML** — complete presentation markup
- **DrawingML** — shared drawing/graphics markup
- VML (Vector Markup Language) — transitional shapes
- Complete element and attribute reference (thousands of pages)

Download: <https://ecma-international.org/wp-content/uploads/ECMA-376-1_5th_edition_december_2015.zip>

### Part 2 — Open Packaging Conventions (OPC)

Specifies the ZIP-based packaging format:

- Package structure (parts and relationships)
- Content types
- Relationship types
- Core properties
- Digital signatures in packages

Download: <https://ecma-international.org/wp-content/uploads/ECMA-376-2_5th_edition_december_2015.zip>

### Part 3 — Markup Compatibility and Extensibility (MCE)

Specifies how OOXML markup can be extended while maintaining backward/forward compatibility:

- `mc:AlternateContent` element
- `mc:Choice` and `mc:Fallback` elements
- Ignorable and ProcessContent attributes
- Compatibility rules

Download: <https://ecma-international.org/wp-content/uploads/ECMA-376-3_5th_edition_december_2015.zip>

### Part 4 — Transitional Migration Features

Documents deprecated "legacy" elements for backward compatibility:

- Legacy drawing elements (VML)
- Old compatibility settings
- Elements from binary format era

Download: <https://ecma-international.org/wp-content/uploads/ECMA-376-4_5th_edition_december_2015.zip>

---

## 3. XML Schemas

OOXML uses **W3C XML Schema Definition (XSD)** files (not RELAX NG like ODF).

### Schema Packages

The ECMA-376 5th edition includes schema ZIP packages for each part:

| Schema Package | Content |
| --- | --- |
| `ECMA-376 Part 1 Schemas.zip` | wml.xsd, sml.xsd, pml.xsd, dml-*.xsd, etc. |
| `ECMA-376 Part 2 Schemas.zip` | opc-*.xsd |
| `ECMA-376 Part 3 Schemas.zip` | mce.xsd |

### Key Schema Files

| File | Covers |
| --- | --- |
| `wml.xsd` | WordprocessingML |
| `sml.xsd` | SpreadsheetML |
| `pml.xsd` | PresentationML |
| `dml-main.xsd` | DrawingML main |
| `dml-chart.xsd` | DrawingML charts |
| `dml-chartDrawing.xsd` | Charts in DrawingML |
| `dml-diagram.xsd` | SmartArt/diagrams |
| `dml-spreadsheetDrawing.xsd` | Drawings in spreadsheets |
| `dml-wordprocessingDrawing.xsd` | Drawings in documents |
| `dml-picture.xsd` | Picture markup |
| `shared-*.xsd` | Shared types (math, bibliography, etc.) |

---

## 4. Conformance Classes

### Strict Documents

- Only use elements/attributes defined in ISO/IEC 29500-1
- No Transitional elements
- No VML shapes
- Cleaner specification compliance

### Transitional Documents

- Use elements from both Part 1 and Part 4
- May include legacy VML shapes
- Allow old compatibility settings (`w:compat`)
- The vast majority of real-world Office documents

### Key Differences: Strict vs Transitional

| Feature | Strict | Transitional |
| --- | --- | --- |
| VML shapes | Not allowed | Allowed |
| DrawingML only | Yes | Both DrawingML and VML |
| Compatibility settings | None | `w:compat` element |
| Legacy list numbering | Not allowed | Allowed |
| `r:id` relationships | Strict form | Legacy form |
| Content type suffix | No suffix | `/transitional` suffix option |

---

## 5. Markup Compatibility and Extensibility (MCE)

MCE enables forward/backward compatibility for OOXML extensions:

```xml
<!-- Part of the document using MCE -->
<mc:AlternateContent
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">

  <!-- Preferred content (for apps that understand "newFeature") -->
  <mc:Choice Requires="newFeature">
    <newFeature:specialElement xmlns:newFeature="http://example.com/newfeature">
      New feature content
    </newFeature:specialElement>
  </mc:Choice>

  <!-- Fallback for apps that don't understand "newFeature" -->
  <mc:Fallback>
    <w:p>
      <w:r><w:t>Equivalent text representation</w:t></w:r>
    </w:p>
  </mc:Fallback>

</mc:AlternateContent>
```

MCE attributes:

- `mc:Ignorable` — list of namespaces that can be ignored
- `mc:ProcessContent` — namespaces whose content should be processed even if the containing element is ignored
- `mc:MustUnderstand` — namespaces that MUST be understood (else error)

---

## 6. Part 1 Chapter Map (Key Sections)

| Section | Content |
| --- | --- |
| §1 | Scope |
| §2 | Normative References |
| §3 | Terms and Definitions |
| §4 | Conformance |
| §5 | Packages |
| §6 | Word Processing Documents (WordprocessingML) |
| §7 | Spreadsheet Documents (SpreadsheetML) |
| §8 | Presentation Documents (PresentationML) |
| §9 | Shared MLs (DrawingML base, Math, Bibliography) |
| §14 | DrawingML |
| §15 | VML (Transitional) |
| §16 | Custom XML Data Storage |
| §17 | Shared String Tables |
| §18 | Styles |
| §19 | Themes |
| §20 | DrawingML (extended) |
| §22 | SpreadsheetML Data |

---

## 7. Microsoft Implementation Notes

Microsoft publishes `[MS-OE376]` documenting where their Office implementations deviate from or extend the ECMA-376 standard:

- **URL**: <https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oe376/>
- Documents: Office 2007, 2010, 2013, 2016, 2019 deviations
- Covers intentional extensions and known bugs

Key deviation categories:

- Elements/attributes Microsoft ignores
- Elements/attributes Microsoft adds beyond spec
- Behavioral differences
- Default value differences

---

## 8. Normative References in ECMA-376

| Standard | Purpose |
| --- | --- |
| W3C XML 1.0 | Base XML |
| W3C XML Schema 1.0 | Schema language (XSD) |
| W3C XML Namespaces | Namespace handling |
| ZIP specification | Package format |
| RFC 3986 | URI syntax |
| W3C XML Signature | Package digital signatures |
| ISO 8601 | Date/time format |
| Unicode | Character encoding |
| CSS2 | Style property values |
| OOXML Part 2 (OPC) | Packaging (self-referential) |
| OOXML Part 3 (MCE) | Compatibility (self-referential) |

---

## 9. Free Access to Specifications

| Source | URL |
| --- | --- |
| ECMA-376 (all editions) | <https://ecma-international.org/publications-and-standards/standards/ecma-376/> |
| ISO/IEC 29500 (ITTF free) | <https://standards.iso.org/ittf/PubliclyAvailableStandards/> |
| ooxml.info (formatted reference) | <https://ooxml.info/docs/> |

---

*Previous: [Overview ←](./01-overview.md) | Next: [Package Structure →](./03-package-structure.md)*
