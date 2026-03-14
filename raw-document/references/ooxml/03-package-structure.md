# OOXML Package Structure (Open Packaging Conventions)

> **Cross-references:** [Overview](./01-overview.md) | [Specification Part 2](./02-specification.md) | [XML Namespaces](./04-xml-namespaces.md) | [Relationships & Content Types](./10-relationships-content-types.md)

---

## 1. Open Packaging Conventions (OPC)

OOXML files are **ZIP archives** structured according to **Open Packaging Conventions (OPC)**, defined in ISO/IEC 29500-2 (ECMA-376 Part 2). OPC provides:

- A **Part** model (files within the ZIP)
- A **Relationship** model (typed connections between parts)
- A **Content Types** manifest
- **Core Properties** for document metadata
- Support for **digital signatures**

---

## 2. `.docx` Package Structure

```text
myDocument.docx (ZIP archive)
├── [Content_Types].xml            ← Content type registry (REQUIRED)
├── _rels/
│   └── .rels                      ← Root relationships (REQUIRED)
├── docProps/
│   ├── core.xml                   ← Core properties (Dublin Core metadata)
│   └── app.xml                    ← Application properties
├── word/
│   ├── document.xml               ← Main document body (REQUIRED)
│   ├── styles.xml                 ← Style definitions
│   ├── settings.xml               ← Document settings
│   ├── numbering.xml              ← List/numbering definitions
│   ├── comments.xml               ← Comments/annotations
│   ├── endnotes.xml               ← Endnotes
│   ├── footnotes.xml              ← Footnotes
│   ├── header1.xml                ← Header part
│   ├── footer1.xml                ← Footer part
│   ├── theme/
│   │   └── theme1.xml             ← Office Theme
│   ├── fontTable.xml              ← Font table
│   ├── webSettings.xml            ← Web settings
│   ├── _rels/
│   │   └── document.xml.rels      ← document.xml relationships
│   └── media/
│       ├── image1.png             ← Embedded images
│       └── image2.jpg
└── customXml/                     ← Custom XML data parts
    ├── item1.xml
    └── itemProps1.xml
```

---

## 3. `.xlsx` Package Structure

```text
myWorkbook.xlsx (ZIP archive)
├── [Content_Types].xml
├── _rels/
│   └── .rels
├── docProps/
│   ├── core.xml
│   └── app.xml
└── xl/
    ├── workbook.xml               ← Workbook structure
    ├── styles.xml                 ← Cell styles
    ├── sharedStrings.xml          ← Shared string table
    ├── calcChain.xml              ← Formula calculation order
    ├── _rels/
    │   └── workbook.xml.rels      ← Workbook relationships
    ├── worksheets/
    │   ├── sheet1.xml             ← Sheet 1 data
    │   ├── sheet2.xml             ← Sheet 2 data
    │   └── _rels/
    │       └── sheet1.xml.rels
    ├── charts/
    │   ├── chart1.xml             ← Chart definitions
    │   └── _rels/
    ├── drawings/
    │   ├── drawing1.xml           ← Drawing layer
    │   └── _rels/
    ├── tables/
    │   └── table1.xml             ← Table definitions
    ├── pivotTables/
    │   └── pivotTable1.xml        ← Pivot table
    ├── theme/
    │   └── theme1.xml
    └── media/
        └── image1.png
```

---

## 4. `.pptx` Package Structure

```text
myPresentation.pptx (ZIP archive)
├── [Content_Types].xml
├── _rels/
│   └── .rels
├── docProps/
│   ├── core.xml
│   └── app.xml
├── ppt/
│   ├── presentation.xml           ← Presentation structure
│   ├── presProps.xml              ← Presentation properties
│   ├── viewProps.xml              ← View properties
│   ├── tableStyles.xml            ← Table styles
│   ├── _rels/
│   │   └── presentation.xml.rels
│   ├── slides/
│   │   ├── slide1.xml             ← Individual slides
│   │   ├── slide2.xml
│   │   └── _rels/
│   │       └── slide1.xml.rels
│   ├── slideLayouts/
│   │   ├── slideLayout1.xml       ← Layout templates
│   │   └── _rels/
│   ├── slideMasters/
│   │   ├── slideMaster1.xml       ← Master slides
│   │   └── _rels/
│   ├── notesMasters/
│   │   └── notesMaster1.xml
│   ├── handoutMasters/
│   │   └── handoutMaster1.xml
│   ├── theme/
│   │   └── theme1.xml
│   └── media/
│       └── image1.png
```

---

## 5. `[Content_Types].xml`

This file maps URI extensions and specific paths to MIME content types. It MUST be present at the root of every OOXML package.

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">

  <!-- Default content types by extension -->
  <Default Extension="rels"
           ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"
           ContentType="application/xml"/>
  <Default Extension="png"
           ContentType="image/png"/>
  <Default Extension="jpeg"
           ContentType="image/jpeg"/>
  <Default Extension="jpg"
           ContentType="image/jpeg"/>

  <!-- Overrides for specific parts -->
  <Override PartName="/word/document.xml"
            ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml"
            ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml"
            ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/word/numbering.xml"
            ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
  <Override PartName="/word/fontTable.xml"
            ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>
  <Override PartName="/word/theme/theme1.xml"
            ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  <Override PartName="/docProps/core.xml"
            ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml"
            ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>

</Types>
```

---

## 6. Relationship Files (`.rels`)

Every OOXML package has a root relationship file at `_rels/.rels`, and each XML part may have an associated `.rels` file in a `_rels/` sibling directory.

### Root Relationships (`_rels/.rels`)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships
    xmlns="http://schemas.openxmlformats.org/package/2006/relationships">

  <!-- Points to the main document part -->
  <Relationship
      Id="rId1"
      Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
      Target="word/document.xml"/>

  <!-- Core properties -->
  <Relationship
      Id="rId2"
      Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties"
      Target="docProps/core.xml"/>

  <!-- Application properties -->
  <Relationship
      Id="rId3"
      Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties"
      Target="docProps/app.xml"/>

</Relationships>
```

### Document Part Relationships (`word/_rels/document.xml.rels`)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships
    xmlns="http://schemas.openxmlformats.org/package/2006/relationships">

  <Relationship Id="rId1"
      Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"
      Target="styles.xml"/>
  <Relationship Id="rId2"
      Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings"
      Target="settings.xml"/>
  <Relationship Id="rId3"
      Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering"
      Target="numbering.xml"/>
  <Relationship Id="rId4"
      Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable"
      Target="fontTable.xml"/>
  <Relationship Id="rId5"
      Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme"
      Target="theme/theme1.xml"/>
  <Relationship Id="rId6"
      Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
      Target="media/image1.png"/>
  <Relationship Id="rId7"
      Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
      Target="https://example.com"
      TargetMode="External"/>

</Relationships>
```

---

## 7. Core Properties (`docProps/core.xml`)

The OPC core properties part uses Dublin Core and OPC namespaces:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties
    xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

  <dc:title>Document Title</dc:title>
  <dc:subject>Document Subject</dc:subject>
  <dc:creator>Jane Smith</dc:creator>
  <cp:keywords>keyword1, keyword2, keyword3</cp:keywords>
  <dc:description>Document description here.</dc:description>
  <cp:lastModifiedBy>John Doe</cp:lastModifiedBy>
  <cp:revision>8</cp:revision>
  <dcterms:created xsi:type="dcterms:W3CDTF">2024-01-10T09:00:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2024-03-15T14:30:00Z</dcterms:modified>
  <cp:category>Reports</cp:category>
  <cp:contentStatus>Final</cp:contentStatus>
  <cp:version>2.0</cp:version>

</cp:coreProperties>
```

---

## 8. Application Properties (`docProps/app.xml`)

Application-specific properties:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties
    xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
    xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">

  <Application>Microsoft Office Word</Application>
  <DocSecurity>0</DocSecurity>
  <Lines>42</Lines>
  <Pages>3</Pages>
  <Paragraphs>45</Paragraphs>
  <Words>1250</Words>
  <Characters>7800</Characters>
  <CharactersWithSpaces>9000</CharactersWithSpaces>
  <ScaleCrop>false</ScaleCrop>
  <Company>Example Corp</Company>
  <LinksUpToDate>false</LinksUpToDate>
  <SharedDoc>false</SharedDoc>
  <HyperlinksChanged>false</HyperlinksChanged>
  <AppVersion>16.0000</AppVersion>

  <!-- Heading pairs (for navigation) -->
  <HeadingPairs>
    <vt:vector size="2" baseType="variant">
      <vt:variant><vt:lpstr>Title</vt:lpstr></vt:variant>
      <vt:variant><vt:i4>1</vt:i4></vt:variant>
    </vt:vector>
  </HeadingPairs>

</Properties>
```

---

## 9. Part Naming Conventions

| Document Type | Part Root | Main Part |
| --- | --- | --- |
| `.docx` | `/word/` | `/word/document.xml` |
| `.xlsx` | `/xl/` | `/xl/workbook.xml` |
| `.pptx` | `/ppt/` | `/ppt/presentation.xml` |
| Core properties | `/docProps/` | `/docProps/core.xml` |
| App properties | `/docProps/` | `/docProps/app.xml` |

---

## 10. Digital Signatures in OPC

OPC supports digital signatures stored as parts:

```text
/_xmlsignatures/sig1.xml
```

Listed in content types:

```xml
<Override PartName="/_xmlsignatures/sig1.xml"
          ContentType="application/vnd.openxmlformats-package.digital-signature-xmlsignature+xml"/>
```

---

*Previous: [Specification ←](./02-specification.md) | Next: [XML Namespaces →](./04-xml-namespaces.md)*
