# OOXML Overview — Office Open XML

> **Cross-references:** [OOXML Specification](./02-specification.md) | [Package Structure](./03-package-structure.md) | [XML Namespaces](./04-xml-namespaces.md) | [vs ODF](../interop/01-comparison.md)

---

## 1. What is Office Open XML (OOXML)?

Office Open XML (OOXML), also written as Open XML, is a zipped, XML-based file format standard for office productivity documents developed by Microsoft. It covers:

- **Word processing** documents (`.docx`, `.dotx`, `.docm`, `.dotm`)
- **Spreadsheets** (`.xlsx`, `.xltx`, `.xlsm`, `.xltm`, `.xlam`)
- **Presentations** (`.pptx`, `.potx`, `.pptm`, `.potm`, `.ppam`, `.ppsx`, `.ppsm`)

OOXML files are ZIP archives (Open Packaging Convention — OPC) containing XML files, binary resources (images, fonts), and relationship files.

---

## 2. Design Philosophy

OOXML was designed primarily to:

| Goal | Description |
| --- | --- |
| **Backward compatibility** | Faithfully represent existing Microsoft Office binary formats (`.doc`, `.xls`, `.ppt`) |
| **Rich features** | Support the full feature set of Microsoft Office applications |
| **Interoperability** | Enable third-party applications to read/write Office documents |
| **Open standard** | Published as ECMA-376 and ISO/IEC 29500 for international standardization |
| **Extensibility** | Markup Compatibility and Extensibility (MCE) for forward/backward compat |
| **Roundtrip fidelity** | Preserve all document features when round-tripping through different apps |

---

## 3. History and Standardization Timeline

| Year | Event |
| --- | --- |
| 2005 | Microsoft submits OOXML to Ecma International TC45 |
| 2006-12 | **ECMA-376 1st Edition** published (Office Open XML File Formats) |
| 2007 | OOXML submitted to ISO/IEC JTC 1 as fast-track DIS 29500 |
| 2008-04 | **ISO/IEC 29500:2008** approved (contentious process) |
| 2008-11 | ISO/IEC 29500:2008 officially published |
| 2008-12 | **ECMA-376 2nd Edition** (technically equivalent to ISO/IEC 29500:2008) |
| 2011 | **ISO/IEC 29500:2011** and **ECMA-376 3rd Edition** |
| 2012 | **ISO/IEC 29500:2012** and **ECMA-376 4th Edition** |
| 2015 | **ISO/IEC 29500-1:2016** (dated 2016 but published 2015) |
| 2016 | **ECMA-376 5th Edition** (current) |
| 2007+ | Microsoft Office 2007 introduces OOXML as default format |
| 2013+ | Microsoft Office 2013 adds ISO Strict support |

---

## 4. Standard Structure: Two Conformance Classes

ISO/IEC 29500 defines two conformance classes:

### Transitional Conformance

- Intended for backward compatibility with existing Office documents
- Includes "compatibility" elements that emulate old binary format behaviors
- Most real-world `.docx`/`.xlsx`/`.pptx` files use this conformance
- File type identifiers use `/transitional` in content type strings

### Strict Conformance

- Eliminates deprecated "compatibility" elements
- Cleaner, more interoperable subset
- ISO/IEC 29500-1 (Strict) is the recommended long-term target
- Less widely implemented but gaining traction
- File type identifiers use `/strict` in content type strings

---

## 5. Standard Parts

OOXML is organized into four ISO/IEC 29500 parts:

| Part | Title | Content |
| --- | --- | --- |
| **Part 1** | Fundamentals and Markup Language Reference | Core markup: WordprocessingML, SpreadsheetML, PresentationML, DrawingML |
| **Part 2** | Open Packaging Conventions (OPC) | ZIP packaging, content types, relationships |
| **Part 3** | Markup Compatibility and Extensibility (MCE) | Forward/backward compatibility mechanisms |
| **Part 4** | Transitional Migration Features | Deprecated elements for backward compat |

ECMA-376 uses the same four-part structure.

---

## 6. File Format Summary

### Word Processing

| Extension | Description | Content Type |
| --- | --- | --- |
| `.docx` | Document | `application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml` |
| `.dotx` | Template | `application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml` |
| `.docm` | Macro-enabled document | `application/vnd.ms-word.document.macroEnabled.main+xml` |
| `.dotm` | Macro-enabled template | `application/vnd.ms-word.template.macroEnabledTemplate.main+xml` |

### Spreadsheet

| Extension | Description |
| --- | --- |
| `.xlsx` | Workbook |
| `.xltx` | Template |
| `.xlsm` | Macro-enabled workbook |
| `.xltm` | Macro-enabled template |
| `.xlam` | Add-in |

### Presentation

| Extension | Description |
| --- | --- |
| `.pptx` | Presentation |
| `.potx` | Template |
| `.pptm` | Macro-enabled presentation |
| `.ppsx` | Slide show |
| `.ppsm` | Macro-enabled slide show |
| `.potm` | Macro-enabled template |
| `.ppam` | Add-in |

---

## 7. Microsoft Office Compliance Levels

| Office Version | ECMA-376 | ISO 29500 Transitional | ISO 29500 Strict |
| --- | --- | --- | --- |
| Office 2007 | Read/Write | — | — |
| Office 2010 | Read | Read/Write | Read |
| Office 2013+ | — | Read/Write (default) | Read/Write |
| Office 365/2019+ | — | Read/Write (default) | Read/Write |

---

## 8. Key Implementations

| Application | Type | OOXML Support |
| --- | --- | --- |
| **Microsoft Office 2007+** | Desktop | Full (primary format) |
| **Microsoft 365** | Cloud/desktop | Full |
| **LibreOffice 3.0+** | Desktop | Read/write (high fidelity) |
| **Apache OpenOffice 3.0+** | Desktop | Read/write |
| **ONLYOFFICE** | Cloud/desktop | High fidelity |
| **Google Docs/Drive** | Cloud | Import/export |
| **Apple Pages/Numbers/Keynote** | Desktop/mobile | Read/write |
| **WPS Office** | Desktop/mobile | High fidelity |
| **SoftMaker Office** | Desktop | High fidelity |

---

## 9. Key Resources

| Resource | URL |
| --- | --- |
| ECMA-376 (latest, 5th ed.) | <https://ecma-international.org/publications-and-standards/standards/ecma-376/> |
| ISO/IEC 29500 (free) | <https://standards.iso.org/ittf/PubliclyAvailableStandards/> |
| Microsoft Open XML SDK | <https://learn.microsoft.com/en-us/office/open-xml/open-xml-sdk> |
| officeopenxml.com (reference) | <http://officeopenxml.com/> |
| ooxml.info | <https://ooxml.info/docs/> |
| Microsoft MS-OE376 (deviations) | <https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oe376/> |
| Library of Congress FDD | <https://www.loc.gov/preservation/digital/formats/fdd/fdd000395.shtml> |

---

*Next: [OOXML Specification →](./02-specification.md)*
