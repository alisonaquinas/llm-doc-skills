# ODF Specification Reference

> **Cross-references:** [Overview](./01-overview.md) | [Package Structure](./03-package-structure.md) | [XML Namespaces](./04-xml-namespaces.md) | [Schemas](https://docs.oasis-open.org/office/OpenDocument/v1.3/)

---

## 1. Specification Documents

### OASIS ODF 1.3 (Current OASIS Standard, 2021)

The ODF 1.3 specification consists of multiple parts:

| Part | Document | URL |
| --- | --- | --- |
| **Part 1** | Introduction and General Principles | <https://docs.oasis-open.org/office/OpenDocument/v1.3/os/part1-introduction/> |
| **Part 2** | Packages | <https://docs.oasis-open.org/office/OpenDocument/v1.3/os/part2-packages/> |
| **Part 3** | OpenDocument Schema | <https://docs.oasis-open.org/office/OpenDocument/v1.3/os/part3-schema/> |
| **Part 4** | Recalculated Formula (OpenFormula) Format | <https://docs.oasis-open.org/office/OpenDocument/v1.3/os/part4-formula/> |

### OASIS ODF 1.2 (ISO/IEC 26300:2015)

| Part | Document | URL |
| --- | --- | --- |
| **Part 1** | OpenDocument Schema | <https://docs.oasis-open.org/office/v1.2/os/OpenDocument-v1.2-os-part1.html> |
| **Part 2** | OpenFormula Format | <https://docs.oasis-open.org/office/v1.2/os/OpenDocument-v1.2-os-part2.html> |
| **Part 3** | Packages | <https://docs.oasis-open.org/office/v1.2/cs01/OpenDocument-v1.2-cs01-part3.html> |

---

## 2. RELAX NG Schemas

ODF uses **RELAX NG** (ISO/IEC 19757-2) to define its XML schemas, rather than W3C XML Schema (XSD). RELAX NG is more expressive and easier to read for complex document schemas.

### Schema Files for ODF 1.3

| Schema | File | Purpose |
| --- | --- | --- |
| Main document schema | `OpenDocument-v1.3-schema.rng` | All document elements and attributes |
| Strict schema | `OpenDocument-v1.3-strict-schema.rng` | Conformant (no foreign elements) |
| Digital signatures schema | `OpenDocument-v1.3-dsig-schema.rng` | Digital signature structure |
| Manifest schema | `OpenDocument-v1.3-manifest-schema.rng` | Package manifest |

### Schema Download Locations

- **OASIS ODF 1.3 schemas**: <https://docs.oasis-open.org/office/OpenDocument/v1.3/os/schemas/>
- **Digital Signatures RNG (HTML)**: <https://docs.oasis-open.org/office/OpenDocument/v1.3/csd03/schemas/OpenDocument-v1.3-dsig-schema-rng.html>
- **ODF 1.2 schemas**: <https://docs.oasis-open.org/office/v1.2/os/>

### Schema Validation Example

```bash
# Using jing (RELAX NG validator)
jing OpenDocument-v1.3-schema.rng myDocument.xml

# Using xmllint with RELAX NG
xmllint --relaxng OpenDocument-v1.3-schema.rng myDocument.xml
```

---

## 3. Conformance Classes

ODF defines two conformance classes for documents and applications:

### Conformant Document

A conformant ODF document:

1. Is a valid ZIP package (or single XML file for "flat ODF")
2. Contains a `META-INF/manifest.xml` that accurately lists package contents
3. Uses elements and attributes only from ODF namespaces (or foreign namespaces clearly declared)
4. Satisfies all MUST/SHALL constraints in the specification

### Extended Conformant Document

Allows use of foreign namespace extensions while still being conformant at the core.

### Application Conformance

Applications claiming ODF conformance must:

- Read all mandatory ODF elements
- Not produce invalid ODF content
- Preserve (not remove) content they do not understand
- Support the digital signatures mechanism (ODF 1.2+)

---

## 4. Specification Structure (ODF 1.3 Part 3 — Schema)

The main schema specification (Part 3) covers the following major areas:

### Chapter Map

| Chapter | Topic |
| --- | --- |
| 2 | Document Structure |
| 3 | Metadata |
| 4 | Text Content |
| 5 | Paragraph-Level Text Elements |
| 6 | Text Fields |
| 7 | Text Indexes |
| 8 | Tables |
| 9 | Graphic Content |
| 10 | Chart Content |
| 11 | Form Content |
| 12 | Database Front-End |
| 13 | Presentations |
| 14 | Drawing Shapes |
| 15 | 3D Shapes |
| 16 | Animations |
| 17 | Style Information |
| 18 | Data Styles (Number Formatting) |
| 19 | Page Styles |
| 20 | List Styles |
| 21 | Outline Numbering |
| 22 | Table of Contents and Indexes |
| 23 | Bibliographies |
| 24 | Change Tracking |
| 25 | Script Events |
| 26–33 | Attribute Definitions |

---

## 5. OpenFormula (ODF Part 2 / Part 4)

OpenFormula defines the formula language used in ODF spreadsheets (`.ods`). It standardizes the syntax used in cell formula expressions.

### Key OpenFormula Features

- Defined as ODF Part 2 (1.2) and Part 4 (1.3)
- Based on function libraries used in OpenOffice.org Calc and LibreOffice Calc
- Covers 300+ mathematical, statistical, logical, text, and date/time functions
- Defines operator precedence and expression syntax
- Specifies cell reference syntax (e.g., `[.A1]`, `[$Sheet1.$A$1]`)

### Formula Syntax

```text
= [formula-expression]
```

Example in XML:

```xml
<table:table-cell table:formula="of:=SUM([.B2:.B10])"
                  office:value-type="float"
                  office:value="450">
  <text:p>450</text:p>
</table:table-cell>
```

---

## 6. Package Specification (ODF Part 2/3)

See [Package Structure](./03-package-structure.md) for full details.

Key package requirements from the spec:

- Packages MUST use ZIP 2.0 compression or store
- The `META-INF/manifest.xml` file MUST be present and MUST be unencrypted
- `mimetype` file MUST be the first entry in the ZIP and MUST NOT be compressed
- The `mimetype` file declares the primary document type

---

## 7. Normative References in ODF 1.3

| Standard | Purpose |
| --- | --- |
| ISO/IEC 19757-2 (RELAX NG) | XML schema language used for ODF schemas |
| W3C XML 1.0 | Base XML specification |
| W3C XML Namespaces | Namespace handling |
| W3C XLink 1.1 | Linking mechanism |
| W3C XPath 1.0 | Used in formula and field expressions |
| W3C CSS2 | Property values for style attributes |
| RFC 3986 | URI syntax |
| RFC 2045/2046 | MIME types |
| ISO 8601 | Date and time format |
| Unicode | Character encoding |
| ZIP specification | Package container format |
| W3C XML Signature | Digital signatures |
| XAdES | Extended digital signatures |
| OpenPGP (RFC 4880) | Encryption (ODF 1.3) |
| Dublin Core | Metadata elements |
| RDF | Metadata graphs (ODF 1.2+) |

---

## 8. Key Specification Differences by Version

| Feature | ODF 1.0 | ODF 1.1 | ODF 1.2 | ODF 1.3 |
| --- | --- | --- | --- | --- |
| RELAX NG schemas | ✓ | ✓ | ✓ | ✓ |
| OpenFormula | — | — | ✓ (Part 2) | ✓ (Part 4) |
| RDF metadata | — | — | ✓ | ✓ |
| Digital signatures | — | — | ✓ | ✓ (enhanced) |
| OpenPGP encryption | — | — | — | ✓ |
| Change tracking | Partial | Partial | ✓ | ✓ (improved) |
| XAdES signatures | — | — | — | ✓ |
| Accessibility (ARIA) | — | ✓ (guidelines) | ✓ | ✓ (improved) |

---

## 9. Freely Available Specification Downloads

All ODF specifications are freely available:

| Source | URL |
| --- | --- |
| OASIS ODF 1.3 | <https://docs.oasis-open.org/office/OpenDocument/v1.3/> |
| OASIS ODF 1.2 | <https://docs.oasis-open.org/office/v1.2/> |
| ISO/IEC 26300 (ITTF) | <https://standards.iso.org/ittf/PubliclyAvailableStandards/> |
| ODF 1.4 (draft) | <https://oasis-tcs.github.io/odf-tc/odf1.4/> |

---

*Previous: [Overview ←](./01-overview.md) | Next: [Package Structure →](./03-package-structure.md)*
