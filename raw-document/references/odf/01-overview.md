# ODF Overview — OpenDocument Format

> **Cross-references:** [ODF Specification](./02-specification.md) | [Package Structure](./03-package-structure.md) | [XML Namespaces](./04-xml-namespaces.md) | [vs OOXML](../interop/01-comparison.md)

---

## 1. What is OpenDocument Format (ODF)?

OpenDocument Format (ODF), formally **Open Document Format for Office Applications**, is an open, XML-based file format standard for office productivity documents. It covers:

- **Word processing** documents (`.odt`, `.ott`)
- **Spreadsheets** (`.ods`, `.ots`)
- **Presentations** (`.odp`, `.otp`)
- **Drawings and graphics** (`.odg`, `.otg`)
- **Charts** (`.odc`)
- **Formulas** (`.odf`)
- **Database** front-ends (`.odb`)
- **Master documents** (`.odm`)

ODF files are ZIP-compressed archives containing a set of XML files and associated resources (images, embedded objects, etc.), governed by a manifest (`META-INF/manifest.xml`).

---

## 2. Design Philosophy

ODF was designed from the ground up with the following goals:

| Goal | Description |
| --- | --- |
| **Vendor neutrality** | Not controlled by any single software vendor |
| **Interoperability** | Any conforming application can read/write valid ODF |
| **Open governance** | Developed and maintained by OASIS TC, published as ISO/IEC standard |
| **Separation of concerns** | Content, styles, metadata, and settings in distinct XML files |
| **Extensibility** | Foreign namespace elements allowed for application extensions |
| **Accessibility** | ARIA roles, tagged PDF export, accessibility guidelines |
| **Long-term preservation** | ISO adoption ensures suitability for archival |

---

## 3. History and Standardization Timeline

| Year | Event |
| --- | --- |
| 2000–2002 | Sun Microsystems develops XML-based format for StarOffice/OpenOffice.org |
| 2002 | OASIS Open Document Format for Office Applications Technical Committee formed |
| 2005-05-01 | **ODF 1.0** approved as OASIS Standard |
| 2006 | **ODF 1.0** published as **ISO/IEC 26300:2006** |
| 2007-02-07 | **ODF 1.1** approved as OASIS Standard |
| 2012 | ODF 1.1 published as **ISO/IEC 26300:2006/Amd 1:2012** |
| 2011-09-29 | **ODF 1.2** approved as OASIS Standard (three-part structure) |
| 2015 | ODF 1.2 published as **ISO/IEC 26300-1/2/3:2015** |
| 2021-04-27 | **ODF 1.3** approved as OASIS Standard |
| 2024 (in progress) | ODF 1.3 undergoing ISO/IEC DIS process |
| 2024-03 | **ODF 1.4** approved as OASIS Standard |
| 2024 | Microsoft 365 announces early support for ODF 1.4 |

---

## 4. ISO/IEC 26300 Version Overview

### ODF 1.0 — ISO/IEC 26300:2006

The baseline standard establishing the ODF XML schema. Single-part document covering all document types.

### ODF 1.1 — ISO/IEC 26300:2006/Amd 1:2012

Added accessibility improvements, better support for text boxes and frames.

### ODF 1.2 — ISO/IEC 26300-1/2/3:2015

The most widely implemented version. Split into three parts:

- **Part 1**: OpenDocument Schema
- **Part 2**: Recalculated Formula (OpenFormula) Format
- **Part 3**: Packages

Key new features:

- RDF-based metadata with named graphs
- OpenFormula spreadsheet formula language
- Digital signatures for package components
- Improved accessibility support

### ODF 1.3 — OASIS Standard (2021), ISO in progress

- OpenPGP-based encryption of XML documents
- Digital signature improvements (XAdES extensions)
- Enhanced change-tracking
- Improved inter-operability features
- Better support for first pages and section descriptions

### ODF 1.4 — OASIS Standard (2024)

- Currently the latest OASIS version
- Microsoft 365 announced early support (version 2404+)

---

## 5. File Format Summary

| Extension | MIME Type | Description |
| --- | --- | --- |
| `.odt` | `application/vnd.oasis.opendocument.text` | Text document |
| `.ott` | `application/vnd.oasis.opendocument.text-template` | Text template |
| `.ods` | `application/vnd.oasis.opendocument.spreadsheet` | Spreadsheet |
| `.ots` | `application/vnd.oasis.opendocument.spreadsheet-template` | Spreadsheet template |
| `.odp` | `application/vnd.oasis.opendocument.presentation` | Presentation |
| `.otp` | `application/vnd.oasis.opendocument.presentation-template` | Presentation template |
| `.odg` | `application/vnd.oasis.opendocument.graphics` | Drawing |
| `.otg` | `application/vnd.oasis.opendocument.graphics-template` | Drawing template |
| `.odc` | `application/vnd.oasis.opendocument.chart` | Chart |
| `.odf` | `application/vnd.oasis.opendocument.formula` | Formula/math |
| `.odb` | `application/vnd.oasis.opendocument.database` | Database |
| `.odm` | `application/vnd.oasis.opendocument.text-master` | Master document |
| `.oth` | `application/vnd.oasis.opendocument.text-web` | HTML document template |

---

## 6. Key Adopters and Implementations

| Application | Type | ODF Support Level |
| --- | --- | --- |
| **LibreOffice** | Desktop suite | Full, primary format |
| **Apache OpenOffice** | Desktop suite | Full, primary format |
| **Microsoft Office 2007+** | Desktop suite | Read/write (via plugin or built-in) |
| **Microsoft 365** | Cloud/desktop | ODF 1.1+ support, ODF 1.4 early support |
| **Google Docs/Drive** | Cloud | Import/export |
| **ONLYOFFICE** | Cloud/desktop | Full |
| **Calligra Suite** | Desktop | Full |
| **NeoOffice** | macOS | Full |
| **AbiWord** | Desktop | Partial |
| **KOffice/Calligra** | Desktop | Full |

---

## 7. Standards Body and Governance

- **OASIS**: Organization for the Advancement of Structured Information Standards — primary development body
  - TC home: <https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=office>
- **ISO/IEC JTC 1/SC 34**: Standardizes ODF under ISO/IEC 26300
- **ITTF**: ISO publishes ODF as a freely available standard
  - Free access: <https://standards.iso.org/ittf/PubliclyAvailableStandards/>

---

## 8. Key Resources

| Resource | URL |
| --- | --- |
| OASIS ODF TC | <https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=office> |
| ODF 1.3 Specification | <https://docs.oasis-open.org/office/OpenDocument/v1.3/> |
| ODF 1.2 Specification | <https://docs.oasis-open.org/office/v1.2/> |
| ISO/IEC 26300 (free) | <https://standards.iso.org/ittf/PubliclyAvailableStandards/> |
| ODF Guidance (UK Gov) | <https://www.gov.uk/guidance/using-open-document-formats-odf-in-your-organisation> |
| Library of Congress FDD | <https://www.loc.gov/preservation/digital/formats/fdd/fdd000247.shtml> |
| opendocumentformat.org | <https://opendocumentformat.org/> |

---

*Next: [ODF Specification Details →](./02-specification.md)*
