# ODF Best Practices

> **Cross-references:** [Overview](./01-overview.md) | [Specification](./02-specification.md) | [Styles](./09-styles-formatting.md) | [Tooling](./13-tooling.md) | [Interoperability](../interop/01-comparison.md)

---

## 1. Document Authoring Best Practices

### Use Named Styles, Not Direct Formatting

**Do this:**

```xml
<text:h text:style-name="Heading_20_1" text:outline-level="1">Title</text:h>
<text:p text:style-name="Text_20_Body">Content</text:p>
```

**Not this (direct/automatic formatting):**

```xml
<text:p text:style-name="P1">  <!-- P1 is an auto-generated style -->
  <text:span text:style-name="T1">Big bold text</text:span>
</text:p>
```

Reasons:

- Named styles survive round-trips through different ODF applications
- Named styles enable consistent global reformatting
- Automatic styles accumulate and bloat documents
- Interoperability is much higher with standard named styles

### Standard Style Name Conventions

ODF applications use underscores followed by hex codes for spaces in internal names. The display name uses actual spaces:

| Display Name | Internal XML Name |
| --- | --- |
| `Heading 1` | `Heading_20_1` |
| `Text Body` | `Text_20_Body` |
| `Default Paragraph Style` | `Default_20_Paragraph_20_Style` |
| `List Bullet` | `List_20_Bullet` |

---

## 2. Namespace and Schema Compliance

### Always Declare All Namespaces on Root Element

Declare all namespaces used in the document on the root element to ensure valid XML:

```xml
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    ... (all used namespaces)
    office:version="1.3">
```

### Always Set `office:version`

```xml
office:version="1.3"    <!-- Use the highest version your content requires -->
```

### Validate Against RELAX NG Schema

```bash
# Install jing (Java-based RELAX NG validator)
java -jar jing.jar OpenDocument-v1.3-schema.rng myDocument.fodt

# Or using xmllint
xmllint --relaxng OpenDocument-v1.3-schema.rng myDocument.fodt
```

Use the **ODF Validator** (<https://odfvalidator.org/>) for ZIP-based packages.

---

## 3. Package Structure Best Practices

### `mimetype` File Rules

```text
✓ Must be the first file in the ZIP archive
✓ Must NOT be compressed (stored only)
✓ Must contain exactly the MIME type string, no trailing newline
✓ No BOM (Byte Order Mark)
```

Creating a compliant ODF package in Python:

```python
import zipfile

with zipfile.ZipFile("output.odt", "w") as zf:
    # 1. mimetype FIRST, uncompressed
    zf.writestr(
        zipfile.ZipInfo("mimetype"),   # default compression = ZIP_STORED
        "application/vnd.oasis.opendocument.text"
    )
    # 2. All other files (can use deflate compression)
    zf.write("META-INF/manifest.xml", compress_type=zipfile.ZIP_DEFLATED)
    zf.write("content.xml", compress_type=zipfile.ZIP_DEFLATED)
    # ...
```

### Manifest Completeness

Every file in the ZIP MUST be listed in `META-INF/manifest.xml`. Missing entries cause validation failures.

---

## 4. Interoperability Best Practices

### Cross-Application Testing

Test documents in the major ODF implementations before distributing:

- **LibreOffice** (reference implementation, <https://www.libreoffice.org>)
- **Apache OpenOffice** (<https://www.openoffice.org>)
- **Microsoft Office 365** (limited ODF support, varies by version)
- **ONLYOFFICE** (<https://www.onlyoffice.com>)

### Round-Trip Testing

```text
1. Create document in Application A
2. Open in Application B
3. Save in Application B
4. Re-open in Application A
5. Compare: layout, styles, content, formulas, images
```

### Avoid Application-Specific Extensions

Use only standard ODF namespaces. If you must use extensions, use the foreign namespace mechanism:

```xml
xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0"
```

Note: Other applications will silently ignore these extensions. Never rely on extension-only features for core document functionality.

### Avoid Relative Positioning for Critical Layout

For documents that must render identically across applications, avoid relying on:

- Exact frame anchoring positions
- Complex multi-column layouts with mixed anchoring
- Features only supported by one ODF implementation

---

## 5. Spreadsheet-Specific Best Practices

### Always Include Cached Values

Cell formulas MUST include a cached value for applications that cannot compute formulas:

```xml
<!-- Good: includes cached value -->
<table:table-cell table:formula="of:=SUM([.B2:.B10])"
                  office:value-type="float"
                  office:value="450">
  <text:p>450</text:p>        <!-- display value -->
</table:table-cell>

<!-- Bad: no cached value -->
<table:table-cell table:formula="of:=SUM([.B2:.B10])"/>
```

### Use `of:` Formula Prefix

Always prefix OpenFormula expressions with `of:`:

```xml
table:formula="of:=VLOOKUP([.A2],[$Sheet2.$A$1:$B$100],2,0)"
```

This explicitly identifies the formula language as OpenFormula.

### Efficient Empty Cell Representation

Use `table:number-columns-repeated` to avoid bloat:

```xml
<!-- Good: efficient -->
<table:table-cell table:number-columns-repeated="1000"/>

<!-- Bad: 1000 individual empty cell elements -->
```

---

## 6. Presentation Best Practices

### Define All Layout on Master Pages

Put shared layout elements on master pages rather than individual slides. This reduces file size and ensures consistency.

### Use Presentation Classes for Placeholders

```xml
<draw:frame presentation:class="title" ...>  <!-- Not just draw:name="title" -->
```

Presentation class attributes enable applications to correctly identify and map content during theme changes.

### Include Slide Notes for Accessibility

```xml
<presentation:notes draw:style-name="dp-notes">
  <draw:frame presentation:class="notes" ...>
    <draw:text-box>
      <text:p>Speaker notes and screen reader content here.</text:p>
    </draw:text-box>
  </draw:frame>
</presentation:notes>
```

---

## 7. Accessibility Best Practices

ODF accessibility follows the W3C WCAG 2.1 guidelines and the OASIS ODF Accessibility Guidelines.

### Image Alt Text

Always provide SVG title and description for images:

```xml
<draw:frame ...>
  <draw:image xlink:href="Pictures/chart.png" .../>
  <svg:title>Quarterly Sales Chart</svg:title>
  <svg:desc>Bar chart showing Q1-Q4 sales by region. Q3 was the highest at $2.4M.</svg:desc>
</draw:frame>
```

### Heading Structure

Use proper heading hierarchy; do not skip levels:

```xml
<text:h text:outline-level="1">Chapter One</text:h>
  <text:h text:outline-level="2">Section 1.1</text:h>
    <text:h text:outline-level="3">Subsection 1.1.1</text:h>
  <text:h text:outline-level="2">Section 1.2</text:h>
```

### Table Headers

Always define header rows in tables:

```xml
<table:table-header-rows>
  <table:table-row>
    <table:table-cell office:value-type="string">
      <text:p text:style-name="Table_20_Heading">Product Name</text:p>
    </table:table-cell>
  </table:table-row>
</table:table-header-rows>
```

### Language Attributes

Set document language in metadata and override where text changes language:

```xml
<!-- In meta.xml -->
<dc:language>en-US</dc:language>

<!-- For sections in another language -->
<text:span text:style-name="French_20_Text">
  <!-- text:style-name should have fo:language="fr" fo:country="FR" -->
  Bonjour le monde
</text:span>
```

### Form Controls

Always provide labels for form controls:

```xml
<form:label for="ctrl1" value="First Name:"/>
<form:text-field id="ctrl1" form:name="firstName"/>
```

---

## 8. Long-Term Preservation

ODF is an excellent choice for long-term document preservation due to its ISO standard status and open specification.

### Preservation Recommendations

1. **Use ODF 1.2 or 1.3** — most widely supported ISO versions
2. **Store as ZIP package** — not flat ODF (better tooling support)
3. **Embed all fonts** — or use common open fonts (Liberation, Noto)
4. **Include metadata** — creation date, creator, subject, keywords
5. **Use UTF-8 encoding** — for all XML files in the package
6. **Avoid macros** — for archival copies (macros reduce longevity)
7. **Test opening** — verify with multiple tools before archiving
8. **Digital signatures** — use for legal/regulatory archival with XAdES timestamps
9. **Validate** — run ODF Validator before archiving

### UK Government ODF Policy

The UK Government mandates ODF for editable documents shared across government. Their guidance is available at: <https://www.gov.uk/guidance/using-open-document-formats-odf-in-your-organisation>

---

## 9. Performance Considerations

### Large Spreadsheets

- Use `table:number-rows-repeated` and `table:number-columns-repeated` for empty runs
- Store images with appropriate compression in the ZIP
- Avoid excessive number of distinct automatic styles

### Large Text Documents

- Break documents into sections or use master documents for very large content
- Compress images before embedding (target ≤300 DPI for print, ≤150 DPI for screen)
- Use embedded objects sparingly; external links are lighter

### Document Comparison Diff

For tracking changes programmatically, use the flat ODF format (`.fodt`, `.fods`) with diff tools:

```bash
diff -u original.fodt modified.fodt
```

---

*Previous: [Security & Signatures ←](./11-security-signatures.md) | Next: [Tooling & Libraries →](./13-tooling.md)*
