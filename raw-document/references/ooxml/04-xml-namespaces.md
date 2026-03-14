# OOXML XML Namespaces

> **Cross-references:** [Package Structure](./03-package-structure.md) | [WordprocessingML](./05-wordprocessingml.md) | [SpreadsheetML](./06-spreadsheetml.md) | [PresentationML](./07-presentationml.md) | [DrawingML](./08-drawingml.md)

---

## 1. Overview

OOXML documents use a set of fixed namespaces based on the pattern:

```text
http://schemas.openxmlformats.org/<category>/2006/<type>
```

Each markup language (WordprocessingML, SpreadsheetML, etc.) has its own primary namespace, with DrawingML providing shared graphic functionality across all document types.

---

## 2. Primary Markup Language Namespaces

### WordprocessingML

| Prefix | Namespace URI | Description |
| --- | --- | --- |
| `w` | `http://schemas.openxmlformats.org/wordprocessingml/2006/main` | Main WordprocessingML namespace |
| `w14` | `http://schemas.microsoft.com/office/word/2010/wordml` | Word 2010 extensions |
| `w15` | `http://schemas.microsoft.com/office/word/2012/wordml` | Word 2013 extensions |
| `w16` | `http://schemas.microsoft.com/office/word/2018/wordml` | Word 2019 extensions |
| `w16cid` | `http://schemas.microsoft.com/office/word/2016/wordml/cid` | Content ID extensions |
| `wpc` | `http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas` | Drawing canvas |
| `wps` | `http://schemas.microsoft.com/office/word/2010/wordprocessingShape` | Word shapes |
| `wpg` | `http://schemas.microsoft.com/office/word/2010/wordprocessingGroup` | Word groups |

### SpreadsheetML

| Prefix | Namespace URI | Description |
| --- | --- | --- |
| `x` | `http://schemas.openxmlformats.org/spreadsheetml/2006/main` | Main SpreadsheetML namespace |
| `x14` | `http://schemas.microsoft.com/office/spreadsheetml/2009/9/main` | Excel 2010 extensions |
| `x15` | `http://schemas.microsoft.com/office/spreadsheetml/2010/11/main` | Excel 2013 extensions |
| `xr` | `http://schemas.microsoft.com/office/spreadsheetml/2014/revision` | Revision tracking |

### PresentationML

| Prefix | Namespace URI | Description |
| --- | --- | --- |
| `p` | `http://schemas.openxmlformats.org/presentationml/2006/main` | Main PresentationML namespace |
| `p14` | `http://schemas.microsoft.com/office/powerpoint/2010/main` | PowerPoint 2010 extensions |
| `p15` | `http://schemas.microsoft.com/office/powerpoint/2012/main` | PowerPoint 2013 extensions |

---

## 3. DrawingML Namespaces

DrawingML is the shared graphics language used across all OOXML document types:

| Prefix | Namespace URI | Description |
| --- | --- | --- |
| `a` | `http://schemas.openxmlformats.org/drawingml/2006/main` | DrawingML main (shapes, colors, fonts) |
| `c` | `http://schemas.openxmlformats.org/drawingml/2006/chart` | Charts |
| `dgm` | `http://schemas.openxmlformats.org/drawingml/2006/diagram` | SmartArt/diagrams |
| `pic` | `http://schemas.openxmlformats.org/drawingml/2006/picture` | Pictures |
| `wp` | `http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing` | Drawings in documents |
| `xdr` | `http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing` | Drawings in spreadsheets |
| `cdr` | `http://schemas.openxmlformats.org/drawingml/2006/chartDrawing` | Drawings in charts |
| `a14` | `http://schemas.microsoft.com/office/drawing/2010/main` | Drawing 2010 extensions |
| `a16` | `http://schemas.microsoft.com/office/drawing/2014/main` | Drawing 2016 extensions |

---

## 4. Packaging and Relationship Namespaces

| Prefix | Namespace URI | Description |
| --- | --- | --- |
| `r` | `http://schemas.openxmlformats.org/officeDocument/2006/relationships` | Relationship references |
| `cp` | `http://schemas.openxmlformats.org/package/2006/metadata/core-properties` | OPC core properties |
| `mc` | `http://schemas.openxmlformats.org/markup-compatibility/2006` | Markup Compatibility and Extensibility |

---

## 5. Shared/Cross-Type Namespaces

| Prefix | Namespace URI | Description |
| --- | --- | --- |
| `m` | `http://schemas.openxmlformats.org/officeDocument/2006/math` | Office Math Markup Language (OMML) |
| `sl` | `http://schemas.openxmlformats.org/schemaLibrary/2006/main` | Schema library |
| `vt` | `http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes` | Document property value types |
| `o` | `urn:schemas-microsoft-com:office:office` | Office extensions |
| `v` | `urn:schemas-microsoft-com:vml` | Vector Markup Language (VML, transitional) |
| `wne` | `http://schemas.microsoft.com/office/word/2006/wordml/extension` | WNE extensions |

---

## 6. Microsoft Extension Namespaces

| Prefix | Namespace URI | Description |
| --- | --- | --- |
| `mo` | `http://schemas.microsoft.com/office/mac/office/2008/main` | Mac Office extensions |
| `o14` | `http://schemas.microsoft.com/office/2009/07/customui` | Office 2010 UI extensions |
| `ms` | `urn:schemas-microsoft-com:office:spreadsheet` | Legacy Excel XML |
| `x14ac` | `http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac` | Excel AC extensions |

---

## 7. External Namespaces Used in OOXML

| Prefix | Namespace URI | Purpose |
| --- | --- | --- |
| `dc` | `http://purl.org/dc/elements/1.1/` | Dublin Core (core properties) |
| `dcterms` | `http://purl.org/dc/terms/` | Dublin Core Terms (core properties) |
| `xml` | `http://www.w3.org/XML/1998/namespace` | Base XML attributes |
| `xsi` | `http://www.w3.org/2001/XMLSchema-instance` | XML Schema instance |
| `xsd` | `http://www.w3.org/2001/XMLSchema` | XML Schema types |

---

## 8. Namespace Declarations by Part

### `word/document.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document
    xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
    xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    xmlns:aink="http://schemas.microsoft.com/office/drawing/2016/ink"
    xmlns:am3d="http://schemas.microsoft.com/office/drawing/2017/model3d"
    xmlns:o="urn:schemas-microsoft-com:office:office"
    xmlns:oel="http://schemas.microsoft.com/office/2019/extlst"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
    xmlns:v="urn:schemas-microsoft-com:vml"
    xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
    xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
    xmlns:w10="urn:schemas-microsoft-com:office:word"
    xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
    xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"
    xmlns:w16cex="http://schemas.microsoft.com/office/word/2018/wordml/cex"
    xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid"
    xmlns:w16="http://schemas.microsoft.com/office/word/2018/wordml"
    xmlns:w16sdtdh="http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash"
    xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
    xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
    xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml/extension"
    xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
    mc:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh wp14">
```

### `xl/workbook.xml`

```xml
<workbook
    xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    xmlns:x15="http://schemas.microsoft.com/office/spreadsheetml/2010/11/main"
    mc:Ignorable="x15">
```

### `ppt/presentation.xml`

```xml
<p:presentation
    xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
    xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main"
    mc:Ignorable="p14">
```

---

## 9. Relationship Type URIs

These appear in `.rels` files as the `Type` attribute:

| Relationship Type | URI |
| --- | --- |
| Office document (main part) | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument` |
| Styles | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles` |
| Settings | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings` |
| Theme | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme` |
| Image | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/image` |
| Hyperlink | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink` |
| Footnotes | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes` |
| Endnotes | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/endnotes` |
| Comments | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments` |
| Numbering | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering` |
| Font table | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable` |
| Worksheet | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet` |
| Shared strings | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings` |
| Calc chain | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/calcChain` |
| Slide | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide` |
| Slide layout | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout` |
| Slide master | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster` |
| Chart | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart` |
| Drawing | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing` |
| Diagram | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramLayout` |
| Core properties | `http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties` |
| Extended properties | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties` |

---

*Previous: [Package Structure ←](./03-package-structure.md) | Next: [WordprocessingML →](./05-wordprocessingml.md)*
