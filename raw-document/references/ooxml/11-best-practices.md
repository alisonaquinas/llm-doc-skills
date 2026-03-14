# OOXML Best Practices

> **Cross-references:** [Overview](./01-overview.md) | [Specification](./02-specification.md) | [Package Structure](./03-package-structure.md) | [Tooling](./12-tooling.md) | [Interoperability](../interop/01-comparison.md)

---

## 1. Conformance and Compliance

### Prefer Strict Conformance for New Documents

Strict conformance (ISO/IEC 29500 Part 1) is the cleanest, most interoperable form. Use it when:

- Creating new documents programmatically
- Building document generation pipelines
- The target applications support Strict (Office 2013+, LibreOffice 3.5+)

To produce a Strict `.docx`, set the content type without `/transitional`:

```xml
<Override PartName="/word/document.xml"
          ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
```

Avoid VML shapes (Transitional-only):

```xml
<!-- Bad (Transitional only): -->
<v:rect xmlns:v="urn:schemas-microsoft-com:vml" style="width:100pt;height:50pt"/>

<!-- Good (Strict, DrawingML): -->
<a:sp><a:spPr><a:prstGeom prst="rect">...</a:prstGeom></a:spPr></a:sp>
```

### Validate Your Output

Use the Open XML SDK Validator:

```csharp
using DocumentFormat.OpenXml.Validation;

var validator = new OpenXmlValidator(FileFormatVersions.Microsoft365);
var errors = validator.Validate(document);
foreach (var error in errors)
{
    Console.WriteLine($"{error.ErrorType}: {error.Description}");
    Console.WriteLine($"  Path: {error.Path?.XPath}");
}
```

Or use the online validator at: <https://ooxmlvalidator.azurewebsites.net/>

---

## 2. Package Construction

### Always Keep `[Content_Types].xml` Complete

Every part in the ZIP must appear in `[Content_Types].xml` either through a `<Default>` (by extension) or an `<Override>` (specific path). Missing entries cause parsing failures.

### Relationship IDs Must Be Unique Per Part

`rId` values must be unique within a single `.rels` file, but may repeat across different `.rels` files.

```xml
<!-- word/_rels/document.xml.rels -->
<Relationship Id="rId1" .../>  <!-- OK: rId1 in document.xml.rels -->

<!-- ppt/slides/_rels/slide1.xml.rels -->
<Relationship Id="rId1" .../>  <!-- OK: rId1 in slide1.xml.rels is independent -->
```

### Use Valid Part URIs

Part names must:

- Start with `/`
- Not end with `/`
- Not contain consecutive `/`
- Be URI-encoded (spaces → `%20`)
- Be case-sensitive

---

## 3. Styles and Formatting

### Always Use Named Styles

Named styles (defined in `styles.xml`) are far more interoperable than direct formatting. Direct formatting accumulates and creates large, fragile documents.

```xml
<!-- Good: named style -->
<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>

<!-- Avoid: pure direct formatting -->
<w:pPr>
  <w:jc w:val="left"/>
  <w:outlineLvl w:val="0"/>
  <!-- ... 20 more properties ... -->
</w:pPr>
<w:rPr>
  <w:b/><w:sz w:val="32"/><w:color w:val="2E74B5"/>
</w:rPr>
```

### Standard Style IDs

Use the canonical `styleId` values (`Normal`, `Heading1`, `DefaultParagraphFont`) for maximum compatibility. Custom style IDs should be unique and descriptive.

### Theme Colors

Reference theme colors rather than hard-coded hex values so that documents update correctly when the theme changes:

```xml
<!-- Good: theme color reference -->
<w:color w:val="2E74B5" w:themeColor="accent1" w:themeTint="BF"/>

<!-- Avoid: hard-coded only (won't update with theme changes) -->
<w:color w:val="2E74B5"/>
```

---

## 4. Images and Media

### Use EMU for All Measurements in DrawingML

All DrawingML coordinates use English Metric Units (EMU). Conversions:

- 1 inch = 914,400 EMU
- 1 cm = 360,000 EMU
- 1 pt = 12,700 EMU

```csharp
// Helper conversions
long InchesToEmu(double inches) => (long)(inches * 914400);
long CentimetersToEmu(double cm) => (long)(cm * 360000);
long PointsToEmu(double pts) => (long)(pts * 12700);
```

### Image Compression and Format

| Format | Recommended Use | Not Recommended For |
| --- | --- | --- |
| PNG | Screenshots, diagrams, graphics with text | Photos |
| JPEG | Photographs | Graphics with text, transparency |
| GIF | Animated images only | High-quality images |
| SVG | Vector graphics (Office 2016+) | Legacy compatibility |
| EMF | Windows vector graphics (legacy) | Cross-platform |
| TIFF | High-quality archival | Web/email |

### Always Set Alt Text

```csharp
// Open XML SDK
nvPicPr.NonVisualDrawingProperties.Description = "Descriptive alt text";

// Or in XML:
<pic:cNvPr id="1" name="Image 1" descr="Descriptive alt text"/>
```

---

## 5. Spreadsheet Best Practices

### Include Cached Values

Always include cached values in formula cells. Applications that can't recalculate will display the cached value:

```xml
<c r="B10">
  <f>SUM(B2:B9)</f>
  <v>450</v>        <!-- REQUIRED: cached value -->
</c>
```

### Use Shared Strings for Repeated Text

Place repeated string values in `sharedStrings.xml` to reduce file size:

```xml
<!-- In sharedStrings.xml: -->
<si><t>Product Name</t></si>   <!-- index 0 -->

<!-- In worksheet: -->
<c r="A1" t="s"><v>0</v></c>   <!-- reference index 0 -->
```

**Note**: Do NOT put strings in the shared string table if they appear only once — use inline strings (`t="inlineStr"`) instead.

### Explicit Cell Styles

Assign explicit style indices for cells that need formatting. Don't rely on default style unless you explicitly want default:

```xml
<c r="A1" s="3" t="s">    <!-- s="3" = style index 3 from styles.xml -->
  <v>0</v>
</c>
```

---

## 6. Presentation Best Practices

### Inherit from Layouts and Masters

Override only what needs to be different on individual slides. Let layouts inherit from masters, and slides inherit from layouts:

```text
Theme → Master → Layout → Slide
```

For maximum flexibility:

- Keep theme colors in the theme
- Keep shared text styles in the master
- Keep layout-specific positions in layouts
- Put unique content on slides only

### Use `ph:idx` for Consistent Placeholder Mapping

When creating slides that reference a layout, use the same `idx` values:

```xml
<!-- In slideLayout: -->
<p:ph idx="1"/>     <!-- content placeholder -->

<!-- In slide (must match idx=1 to inherit layout's position/style) -->
<p:ph idx="1"/>
```

### Explicit Slide IDs Must Be Unique

Each `<p:sldId>` in `presentation.xml` must have a unique `id` attribute (typically 256+):

```xml
<p:sldIdLst>
  <p:sldId id="256" r:id="rId2"/>
  <p:sldId id="257" r:id="rId3"/>
  <!-- id values must be unique across the presentation -->
</p:sldIdLst>
```

---

## 7. Markup Compatibility (MCE)

Use MCE to provide fallbacks when using extension features:

```xml
<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
  <mc:Choice Requires="w14">           <!-- requires Word 2010 extension namespace -->
    <w14:shadow .../>                  <!-- enhanced shadow effect -->
  </mc:Choice>
  <mc:Fallback>
    <w:pPr><w:shd w:fill="CCCCCC"/></w:pPr>  <!-- fallback: gray background -->
  </mc:Fallback>
</mc:AlternateContent>
```

Always declare extension namespaces in `mc:Ignorable` on the root element:

```xml
<w:document ... mc:Ignorable="w14 w15 w16">
```

---

## 8. Performance and File Size

### Minimize Unused Styles

Remove unused styles from `styles.xml`. Accumulated unused styles from template inheritance significantly bloat file size.

### Shared Strings Threshold

Only add a string to the shared string table if it's likely to appear multiple times. Unique strings are more efficient as inline values (`t="s"` with `<v>` vs `t="inlineStr"` with `<is><t>...</t></is>`).

### Image Compression

Use appropriate compression levels:

```python
# python-docx / Pillow
from PIL import Image
import io

def compress_image(image_path, quality=85, max_size=(1200, 1200)):
    img = Image.open(image_path)
    img.thumbnail(max_size, Image.LANCZOS)
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    return output.getvalue()
```

### Avoid Excessive Undo History

In programmatically generated documents, omit revision/change tracking data (`w:rsid*` attributes) to reduce file size:

```xml
<!-- Can be removed from programmatically generated documents: -->
<w:p w:rsidR="00A87B2A" w:rsidRPr="00B4221F">
```

---

## 9. Accessibility

### Document Structure

- Use heading styles (`Heading1`–`Heading9`) rather than large bold text
- Define document language: `<w:lang w:val="en-US"/>` in `rPrDefault`
- Use built-in list styles rather than indented paragraphs with manual bullets

### Tables

- Mark header rows with `w:tblHeader` in `w:trPr`
- Use table styles rather than direct cell formatting
- Provide a table caption via a preceding paragraph with the `Caption` style

### Images

- Always set `descr` (alt text) on `cNvPr` elements
- Use `<pic:cNvPr descr="..."/>` for pictures
- Use `<wp:docPr descr="..."/>` for drawing frames

### Reading Order

For right-to-left content, set:

```xml
<w:bidi/>                   <!-- in w:pPr for paragraph direction -->
<w:rPr><w:rtl/></w:rPr>    <!-- in run properties -->
```

---

*Previous: [Relationships & Content Types ←](./10-relationships-content-types.md) | Next: [Tooling & Libraries →](./12-tooling.md)*
