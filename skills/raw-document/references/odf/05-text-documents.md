# ODF Text Documents (ODT)

> **Cross-references:** [Namespaces](./04-xml-namespaces.md) | [Styles & Formatting](./09-styles-formatting.md) | [Metadata](./10-metadata.md) | [OOXML WordprocessingML](../ooxml/05-wordprocessingml.md)

---

## 1. Overview

OpenDocument Text (`.odt`) is the ODF format for word processing documents. Text documents are defined in the `office:text` body element within `content.xml`.

The key XML files in an `.odt` package:

- `content.xml` — body text, embedded images, tables
- `styles.xml` — paragraph styles, character styles, page layouts
- `meta.xml` — author, creation date, word count
- `settings.xml` — print settings, view settings

---

## 2. Document Structure

```xml
<office:document-content ...>
  <office:automatic-styles>
    <!-- paragraph/character styles generated for this content -->
  </office:automatic-styles>

  <office:body>
    <office:text>

      <!-- Sequence numbers and variable declarations -->
      <text:sequence-decls>...</text:sequence-decls>

      <!-- User-defined field declarations -->
      <text:user-field-decls>...</text:user-field-decls>

      <!-- Text sections, headings, paragraphs, tables -->
      <text:h text:style-name="Heading_20_1" text:outline-level="1">
        Chapter One
      </text:h>

      <text:p text:style-name="Text_20_Body">
        This is body text with <text:span text:style-name="Bold">bold</text:span>
        and <text:a xlink:type="simple"
                    xlink:href="https://example.com">a link</text:a>.
      </text:p>

    </office:text>
  </office:body>
</office:document-content>
```

---

## 3. Paragraphs and Headings

### `text:p` — Paragraph

The basic unit of text content. Every block of text resides in a `<text:p>` element.

```xml
<text:p text:style-name="Text_20_Body">
  Simple paragraph text.
</text:p>

<text:p text:style-name="Text_20_Body">
  Paragraph with <text:span text:style-name="Emphasis">italic</text:span> text
  and a <text:line-break/> forced line break.
</text:p>
```

Key attributes:

- `text:style-name` — references a named paragraph style
- `text:cond-style-name` — conditional style name (for e.g., first paragraph)
- `xml:id` — unique identifier for cross-referencing

### `text:h` — Heading

```xml
<text:h text:style-name="Heading_20_1"
        text:outline-level="1">
  Main Chapter Title
</text:h>

<text:h text:style-name="Heading_20_2"
        text:outline-level="2"
        text:is-list-header="false">
  Section Title
</text:h>
```

Key attributes:

- `text:outline-level` — heading level 1–10
- `text:style-name` — references a heading style
- `text:restart-numbering` — restart outline numbering

---

## 4. Character-Level Content

### `text:span` — Inline Style Span

```xml
<text:span text:style-name="Bold">bold text</text:span>
<text:span text:style-name="Italic">italic text</text:span>
<text:span text:style-name="Code">code text</text:span>
```

### `text:a` — Hyperlink

```xml
<text:a xlink:type="simple"
        xlink:href="https://example.com"
        xlink:show="new"
        office:name="Link Name">
  Link text
</text:a>
```

Internal anchor link:

```xml
<text:a xlink:type="simple" xlink:href="#section1">Go to Section 1</text:a>
```

### Special Characters

```xml
<text:s/>              <!-- single space (multiple: text:s text:c="3") -->
<text:tab/>            <!-- tab character -->
<text:line-break/>     <!-- soft line break within paragraph -->
<text:soft-page-break/> <!-- soft page break hint -->
```

---

## 5. Lists

### Basic List Structure

```xml
<text:list text:style-name="List_20_Bullet">
  <text:list-item>
    <text:p text:style-name="List_20_Bullet">First item</text:p>
  </text:list-item>
  <text:list-item>
    <text:p text:style-name="List_20_Bullet">Second item</text:p>
    <!-- Nested list -->
    <text:list>
      <text:list-item>
        <text:p text:style-name="List_20_Bullet_20_2">Nested item</text:p>
      </text:list-item>
    </text:list>
  </text:list-item>
</text:list>
```

### Numbered List

```xml
<text:list text:style-name="List_20_Number">
  <text:list-item>
    <text:p text:style-name="List_20_Number">Step one</text:p>
  </text:list-item>
  <text:list-item>
    <text:p text:style-name="List_20_Number">Step two</text:p>
  </text:list-item>
</text:list>
```

To continue numbering from a previous list:

```xml
<text:list text:continue-numbering="true" text:style-name="List_20_Number">
```

---

## 6. Tables in Text Documents

```xml
<table:table table:name="Table1" table:style-name="Table1">

  <!-- Column definitions -->
  <table:table-column table:style-name="Table1.A"
                      table:number-columns-repeated="3"/>

  <!-- Header row -->
  <table:table-header-rows>
    <table:table-row table:style-name="Table1.Header">
      <table:table-cell table:style-name="Table1.A1"
                        office:value-type="string">
        <text:p text:style-name="Table_20_Heading">Column A</text:p>
      </table:table-cell>
      <table:table-cell table:style-name="Table1.A1"
                        office:value-type="string">
        <text:p text:style-name="Table_20_Heading">Column B</text:p>
      </table:table-cell>
    </table:table-row>
  </table:table-header-rows>

  <!-- Data rows -->
  <table:table-row>
    <table:table-cell office:value-type="string">
      <text:p>Value 1</text:p>
    </table:table-cell>
    <table:table-cell office:value-type="float" office:value="42">
      <text:p>42</text:p>
    </table:table-cell>
  </table:table-row>

  <!-- Cell spanning: number-columns-spanned -->
  <table:table-row>
    <table:table-cell table:number-columns-spanned="2"
                      office:value-type="string">
      <text:p>Merged cell spanning 2 columns</text:p>
    </table:table-cell>
    <table:covered-table-cell/>  <!-- placeholder for covered cell -->
  </table:table-row>

</table:table>
```

---

## 7. Frames, Images, and Embedded Objects

### Image in a Frame

```xml
<draw:frame draw:style-name="Graphics1"
            draw:name="Picture1"
            text:anchor-type="paragraph"
            svg:x="2.5cm" svg:y="1.0cm"
            svg:width="8cm" svg:height="6cm"
            draw:z-index="0">

  <draw:image xlink:href="Pictures/image1.png"
              xlink:type="simple"
              xlink:show="embed"
              xlink:actuate="onLoad"/>

  <!-- Optional image alt text -->
  <svg:title>Image description</svg:title>
  <svg:desc>Longer image description for accessibility</svg:desc>
</draw:frame>
```

Anchor types:

- `text:anchor-type="page"` — anchored to the page
- `text:anchor-type="paragraph"` — anchored to a paragraph
- `text:anchor-type="char"` — anchored to a character
- `text:anchor-type="as-char"` — inline (as character)
- `text:anchor-type="frame"` — anchored to an enclosing frame

### Text Box

```xml
<draw:frame text:anchor-type="paragraph"
            svg:width="8cm" svg:height="4cm"
            draw:style-name="TextBox1">
  <draw:text-box>
    <text:p text:style-name="TextContents">Text inside the box.</text:p>
  </draw:text-box>
</draw:frame>
```

---

## 8. Sections

Sections allow dividing text into named areas with distinct properties (columns, backgrounds, protection):

```xml
<text:section text:style-name="Sect1" text:name="Introduction">
  <text:p text:style-name="Text_20_Body">Section content here.</text:p>
</text:section>
```

Section with two-column layout (via style):

```xml
<style:style style:name="Sect1" style:family="section">
  <style:section-properties>
    <style:columns fo:column-count="2" fo:column-gap="0.5cm"/>
  </style:section-properties>
</style:style>
```

---

## 9. Fields and Dynamic Content

ODF text documents support a rich set of field elements for dynamic content:

| Element | Description |
| --- | --- |
| `<text:date>` | Current date |
| `<text:time>` | Current time |
| `<text:page-number>` | Current page number |
| `<text:page-count>` | Total page count |
| `<text:author-name>` | Document author |
| `<text:author-initials>` | Author initials |
| `<text:chapter>` | Chapter name/number |
| `<text:file-name>` | File name |
| `<text:sheet-name>` | Sheet name (spreadsheet context) |
| `<text:subject>` | Document subject metadata field |
| `<text:title>` | Document title metadata field |
| `<text:description>` | Document description metadata field |
| `<text:keywords>` | Document keywords |
| `<text:variable-set>` | User variable assignment |
| `<text:variable-get>` | Retrieve user variable value |
| `<text:sequence>` | Auto-incrementing sequence (for figure numbers) |
| `<text:conditional-text>` | Conditional display text |

Example:

```xml
<text:p text:style-name="Footer">
  Page <text:page-number text:select-page="current">1</text:page-number>
  of <text:page-count>1</text:page-count>
</text:p>
```

---

## 10. Bookmarks and Cross-References

```xml
<!-- Define bookmark -->
<text:bookmark-start text:name="ref-section1"/>
<text:h text:outline-level="1">Section One</text:h>
<text:bookmark-end text:name="ref-section1"/>

<!-- Reference to bookmark -->
<text:a xlink:type="simple" xlink:href="#ref-section1">See Section One</text:a>

<!-- Cross-reference field -->
<text:bookmark-ref text:reference-format="chapter"
                   text:ref-name="ref-section1">1</text:bookmark-ref>
```

---

## 11. Change Tracking

ODF 1.2+ supports tracked changes (redlines):

```xml
<text:tracked-changes>
  <text:changed-region text:id="ct1">
    <text:insertion>
      <office:change-info>
        <dc:creator>Author Name</dc:creator>
        <dc:date>2024-03-01T10:00:00</dc:date>
      </office:change-info>
    </text:insertion>
  </text:changed-region>
</text:tracked-changes>

<!-- In content, changes are marked: -->
<text:change-start text:change-id="ct1"/>
  Inserted text
<text:change-end text:change-id="ct1"/>
```

---

## 12. Footnotes and Endnotes

```xml
<!-- Footnote -->
<text:footnote text:id="ftn1">
  <text:footnote-citation>1</text:footnote-citation>
  <text:footnote-body>
    <text:p text:style-name="Footnote">Footnote text here.</text:p>
  </text:footnote-body>
</text:footnote>

<!-- Endnote -->
<text:endnote text:id="en1">
  <text:endnote-citation>i</text:endnote-citation>
  <text:endnote-body>
    <text:p text:style-name="Endnote">Endnote text here.</text:p>
  </text:endnote-body>
</text:endnote>
```

---

## 13. Notes and Annotations

```xml
<office:annotation office:display="true"
                   svg:x="10cm" svg:y="2cm">
  <dc:creator>Reviewer Name</dc:creator>
  <dc:date>2024-03-01T10:00:00</dc:date>
  <text:p text:style-name="Annotation">Comment text here.</text:p>
</office:annotation>
```

---

*Previous: [XML Namespaces ←](./04-xml-namespaces.md) | Next: [Spreadsheets →](./06-spreadsheets.md)*
