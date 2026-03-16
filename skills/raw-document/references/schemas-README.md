# Canonical Schema Collection

This directory contains canonical schemas for the two major office document format standards:
**ODF (OpenDocument Format)** and **OOXML (Office Open XML / ECMA-376 / ISO/IEC 29500)**.

All files are sourced directly from the official standards bodies (OASIS and Ecma International).

---

## ODF — OpenDocument Format

Source: [OASIS OpenDocument TC](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=office)

### `odf/v1.3-os/` — ODF 1.3 OASIS Standard (2021)

Official schema index: <https://docs.oasis-open.org/office/OpenDocument/v1.3/os/schemas/>

| File | Description |
| --- | --- |
| `OpenDocument-v1.3-schema.rng` | Main document schema (RELAX NG) — all document content |
| `OpenDocument-v1.3-manifest-schema.rng` | Package manifest schema (RELAX NG) |
| `OpenDocument-v1.3-dsig-schema.rng` | Digital signature schema (RELAX NG) |

### `odf/v1.4-os/` — ODF 1.4 OASIS Standard (2025-12-03)

Official schema index: <https://docs.oasis-open.org/office/OpenDocument/v1.4/os/schemas/>

| File | Description |
| --- | --- |
| `OpenDocument-v1.4-schema.rng` | Main document schema (RELAX NG) — all document content |
| `OpenDocument-v1.4-manifest-schema.rng` | Package manifest schema (RELAX NG) |
| `OpenDocument-v1.4-dsig-schema.rng` | Digital signature schema (RELAX NG) |

---

## OOXML — Office Open XML (ECMA-376 5th Edition, 2015–2021)

Source: [Ecma International ECMA-376](https://ecma-international.org/publications-and-standards/standards/ecma-376/)

The ECMA-376 5th edition is aligned with ISO/IEC 29500:2016.
Each part provides schemas in both **XSD** (XML Schema Definition) and **RELAX NG Compact** (`.rnc`) forms.
The XSD is normative in ISO/IEC 29500; RELAX NG is normative in ECMA-376.

### XSD Schemas — Transitional Conformance Class (Part 4, 2016)

These are the schemas for documents using the **Transitional** conformance class, which is what
the vast majority of real-world `.docx`, `.xlsx`, and `.pptx` files use.
Includes all Strict schemas plus VML (legacy vector graphics).

| Directory | Files | Description |
| --- | --- | --- |
| `ooxml/dml/` | 8 XSD + 2 XML | DrawingML: charts, diagrams, drawing surfaces, pictures; preset geometry definitions |
| `ooxml/pml/` | 1 XSD | PresentationML: `pml.xsd` (full presentation model) |
| `ooxml/sml/` | 1 XSD | SpreadsheetML: `sml.xsd` (full workbook/worksheet model) |
| `ooxml/wml/` | 1 XSD | WordprocessingML: `wml.xsd` (full document model) |
| `ooxml/shared/` | 11 XSD | Shared types, properties, math, bibliography; `xml.xsd` (W3C) |
| `ooxml/vml/` | 5 XSD | VML (Vector Markup Language) — legacy drawing format, Transitional only |
| `ooxml/opc/` | 4 XSD | OPC (Open Packaging Conventions, Part 2, 2021): content types, relationships, core properties, digital signatures |

### XSD Schemas — Strict Conformance Class (Part 1, 2016)

The **Strict** conformance class removes legacy compatibility elements (no VML, no deprecated attributes).
Strict is a subset of Transitional — 21 XSDs covering the same modules except VML.

| Directory | Files | Description |
| --- | --- | --- |
| `ooxml/strict/` | 21 XSD | All modules (DML, PML, SML, WML, Shared) in Strict form |

### RELAX NG Compact Schemas (`.rnc`)

Normative per ECMA-376. More granular than XSD — each document part has its own `.rnc` file.

| Directory | Files | Description |
| --- | --- | --- |
| `ooxml/relaxng/strict/` | 86 RNC | Part 1 — Strict conformance class |
| `ooxml/relaxng/transitional/` | 92 RNC | Part 4 — Transitional conformance class (adds VML) |
| `ooxml/relaxng/opc/` | 5 RNC | Part 2 — OPC schemas |

---

## Known Gaps

| Schema | Reason not included |
| --- | --- |
| `mc.xsd` (MCE, ECMA-376 Part 3) | Ecma does not distribute Part 3 as a standalone XSD; the schema is defined normatively only in the Part 3 prose/PDF. The MCE namespace is `http://schemas.openxmlformats.org/markup-compatibility/2006`. |
| ODF 1.2 schemas | ODF 1.3 is the current OASIS Standard superseding 1.2; 1.3 schemas are included instead. |

---

## File Counts

```text
schemas/
├── odf/
│   ├── v1.3-os/    3 RNG files
│   └── v1.4-os/    3 RNG files
└── ooxml/
    ├── dml/        8 XSD + 2 XML (preset geometry data)
    ├── opc/        4 XSD
    ├── pml/        1 XSD
    ├── shared/     11 XSD
    ├── sml/        1 XSD
    ├── strict/     21 XSD
    ├── vml/        5 XSD
    ├── wml/        1 XSD
    └── relaxng/
        ├── strict/        86 RNC
        ├── transitional/  92 RNC
        └── opc/            5 RNC
```
