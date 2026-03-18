# OOXML Relationships and Content Types

> **Cross-references:** [Package Structure](./03-package-structure.md) | [XML Namespaces](./04-xml-namespaces.md) | [Specification Part 2](./02-specification.md)

---

## 1. Open Packaging Conventions Model

The Open Packaging Conventions (OPC) model centers on two concepts:

1. **Parts** — files within the ZIP package
2. **Relationships** — typed, directed connections between parts

Together these form a directed graph describing the document's structure.

---

## 2. Content Types (`[Content_Types].xml`)

Every OOXML package MUST have `[Content_Types].xml` at the root. It maps file paths and extensions to MIME-type-like content type strings.

```xml
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">

  <!-- Defaults apply to all files with matching extension -->
  <Default Extension="rels"
           ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"   ContentType="application/xml"/>
  <Default Extension="png"   ContentType="image/png"/>
  <Default Extension="jpeg"  ContentType="image/jpeg"/>
  <Default Extension="jpg"   ContentType="image/jpeg"/>
  <Default Extension="gif"   ContentType="image/gif"/>
  <Default Extension="bmp"   ContentType="image/bmp"/>
  <Default Extension="svg"   ContentType="image/svg+xml"/>
  <Default Extension="emf"   ContentType="image/x-emf"/>
  <Default Extension="wmf"   ContentType="image/x-wmf"/>
  <Default Extension="tiff"  ContentType="image/tiff"/>

  <!-- Overrides apply to specific part URIs -->
  <!-- Override takes precedence over Default -->

</Types>
```

### Complete Content Type Reference

#### Word Processing (`.docx`)

| Part | Content Type |
| --- | --- |
| `word/document.xml` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml` |
| `word/document.xml` (strict) | `application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml` |
| `word/styles.xml` | `application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml` |
| `word/settings.xml` | `application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml` |
| `word/numbering.xml` | `application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml` |
| `word/footnotes.xml` | `application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml` |
| `word/endnotes.xml` | `application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml` |
| `word/comments.xml` | `application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml` |
| `word/header*.xml` | `application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml` |
| `word/footer*.xml` | `application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml` |
| `word/fontTable.xml` | `application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml` |
| `word/webSettings.xml` | `application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml` |
| `word/theme/theme1.xml` | `application/vnd.openxmlformats-officedocument.theme+xml` |
| `docProps/core.xml` | `application/vnd.openxmlformats-package.core-properties+xml` |
| `docProps/app.xml` | `application/vnd.openxmlformats-officedocument.extended-properties+xml` |

#### Spreadsheet (`.xlsx`)

| Part | Content Type |
| --- | --- |
| `xl/workbook.xml` | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml` |
| `xl/worksheets/sheet*.xml` | `application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml` |
| `xl/styles.xml` | `application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml` |
| `xl/sharedStrings.xml` | `application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml` |
| `xl/calcChain.xml` | `application/vnd.openxmlformats-officedocument.spreadsheetml.calcChain+xml` |
| `xl/charts/chart*.xml` | `application/vnd.openxmlformats-officedocument.drawingml.chart+xml` |
| `xl/drawings/drawing*.xml` | `application/vnd.openxmlformats-officedocument.drawing+xml` |
| `xl/tables/table*.xml` | `application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml` |
| `xl/pivotTables/pivotTable*.xml` | `application/vnd.openxmlformats-officedocument.spreadsheetml.pivotTable+xml` |
| `xl/theme/theme1.xml` | `application/vnd.openxmlformats-officedocument.theme+xml` |

#### Presentation (`.pptx`)

| Part | Content Type |
| --- | --- |
| `ppt/presentation.xml` | `application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml` |
| `ppt/slides/slide*.xml` | `application/vnd.openxmlformats-officedocument.presentationml.slide+xml` |
| `ppt/slideLayouts/slideLayout*.xml` | `application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml` |
| `ppt/slideMasters/slideMaster*.xml` | `application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml` |
| `ppt/notesSlides/notesSlide*.xml` | `application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml` |
| `ppt/notesMasters/notesMaster*.xml` | `application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml` |
| `ppt/presProps.xml` | `application/vnd.openxmlformats-officedocument.presentationml.presProps+xml` |
| `ppt/viewProps.xml` | `application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml` |
| `ppt/tableStyles.xml` | `application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml` |
| `ppt/theme/theme1.xml` | `application/vnd.openxmlformats-officedocument.theme+xml` |
| `ppt/charts/chart*.xml` | `application/vnd.openxmlformats-officedocument.drawingml.chart+xml` |
| `ppt/diagrams/data*.xml` | `application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml` |
| `ppt/diagrams/layout*.xml` | `application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml` |

---

## 3. Relationship Naming Convention

For every part `path/to/part.xml`, its relationships file is at:

```text
path/to/_rels/part.xml.rels
```

The root package relationships file is:

```text
_rels/.rels
```

---

## 4. Complete Relationship Types Reference

All standard OOXML relationship type URIs use the prefix:
`http://schemas.openxmlformats.org/officeDocument/2006/relationships/`

| Relationship Name | Full URI Suffix |
| --- | --- |
| `officeDocument` | officeDocument (root → main part) |
| `styles` | styles |
| `settings` | settings |
| `theme` | theme |
| `image` | image |
| `hyperlink` | hyperlink |
| `fontTable` | fontTable |
| `numbering` | numbering |
| `footnotes` | footnotes |
| `endnotes` | endnotes |
| `comments` | comments |
| `header` | header |
| `footer` | footer |
| `webSettings` | webSettings |
| `glossaryDocument` | glossaryDocument |
| `customXml` | customXml |
| `worksheet` | worksheet |
| `sharedStrings` | sharedStrings |
| `calcChain` | calcChain |
| `externalLink` | externalLink |
| `queryTable` | queryTable |
| `connections` | connections |
| `table` | table |
| `pivotTable` | pivotTable |
| `pivotCacheDefinition` | pivotCacheDefinition |
| `drawing` | drawing |
| `chart` | chart |
| `chartSheet` | chartSheet |
| `dialogSheet` | dialogSheet |
| `macroSheet` | macroSheet |
| `slide` | slide |
| `slideLayout` | slideLayout |
| `slideMaster` | slideMaster |
| `notesSlide` | notesSlide |
| `notesMaster` | notesMaster |
| `handoutMaster` | handoutMaster |
| `presProps` | presProps |
| `viewProps` | viewProps |
| `tableStyles` | tableStyles |
| `diagramData` | diagramData |
| `diagramLayout` | diagramLayout |
| `diagramQuickStyle` | diagramQuickStyle |
| `diagramColors` | diagramColors |
| `vbaProject` | vbaProject |

### OPC Package-Level Relationships

Prefix: `http://schemas.openxmlformats.org/package/2006/relationships/`

| Relationship | URI Suffix |
| --- | --- |
| Core properties | `metadata/core-properties` |
| Digital signature | `digital-signature/origin` |
| Thumbnail | `metadata/thumbnail` |

---

## 5. Using `r:id` References

Parts reference each other using the `r:id` attribute, which matches an `Id` in the corresponding `.rels` file:

```xml
<!-- In word/document.xml — referring to an image -->
<w:drawing>
  <wp:inline>
    <a:graphic>
      <a:graphicData uri="...picture">
        <pic:pic>
          <pic:blipFill>
            <a:blip r:embed="rId6"/>   <!-- r:embed references a relationship -->
          </pic:blipFill>
        </pic:pic>
      </a:graphicData>
    </a:graphic>
  </wp:inline>
</w:drawing>

<!-- In word/_rels/document.xml.rels -->
<Relationship Id="rId6"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
    Target="media/image1.png"/>
```

---

## 6. External Relationships

External resources (hyperlinks, external data) use `TargetMode="External"`:

```xml
<!-- In _rels file -->
<Relationship Id="rId10"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
    Target="https://example.com"
    TargetMode="External"/>
```

Internal relationships (default) use `TargetMode="Internal"` (or omit the attribute).

---

## 7. Digital Signatures

Signatures reference the origin via the root `.rels`:

```xml
<!-- In _rels/.rels -->
<Relationship Id="rId99"
    Type="http://schemas.openxmlformats.org/package/2006/relationships/digital-signature/origin"
    Target="/_xmlsignatures/origin.sigs"/>
```

The signature parts are stored in `/_xmlsignatures/sig1.xml`, etc.

---

## 8. Programmatic Access with Open XML SDK

```csharp
using DocumentFormat.OpenXml.Packaging;

// Access relationships
using (WordprocessingDocument doc = WordprocessingDocument.Open("file.docx", false))
{
    MainDocumentPart mainPart = doc.MainDocumentPart;

    // Enumerate all image relationships
    foreach (ImagePart imgPart in mainPart.ImageParts)
    {
        Console.WriteLine($"Image: {imgPart.Uri}");
        Console.WriteLine($"ContentType: {imgPart.ContentType}");
    }

    // Get a specific relationship by ID
    var rel = mainPart.GetRelationshipById("rId6");
    Console.WriteLine($"Target: {rel.TargetUri}");
    Console.WriteLine($"Mode: {rel.TargetMode}");
}
```

---

*Previous: [Styles & Themes ←](./09-styles-themes.md) | Next: [Best Practices →](./11-best-practices.md)*
