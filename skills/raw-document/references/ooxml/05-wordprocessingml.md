# OOXML WordprocessingML (DOCX)

> **Cross-references:** [Namespaces](./04-xml-namespaces.md) | [Styles & Themes](./09-styles-themes.md) | [DrawingML](./08-drawingml.md) | [ODF Text Documents](../odf/05-text-documents.md)

---

## 1. Overview

WordprocessingML (WML) is the XML vocabulary for word processing documents in OOXML. It is defined in `wml.xsd` and uses the namespace:

```text
http://schemas.openxmlformats.org/wordprocessingml/2006/main
```

Prefix: `w:`

---

## 2. Document Root Structure

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document
    xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    mc:Ignorable="w14 w15">

  <w:body>
    <!-- Document content: paragraphs, tables, structured document tags -->

    <!-- Final section properties (REQUIRED) -->
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>   <!-- letter: 8.5"×11" in twentieths-of-a-point -->
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"
               w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>

  </w:body>
</w:document>
```

---

## 3. Measurement Units in WordprocessingML

| Unit | Size | Common Usage |
| --- | --- | --- |
| **Twip** (twentieth of a point) | 1/1440 inch | Page size, margins, paragraph spacing |
| **EMU** (English Metric Unit) | 1/914400 inch | DrawingML image/shape positioning |
| **Half-point** | 1/144 inch | Font sizes (`w:sz`: 24 = 12pt) |
| **Hundredths of a percent** | 1/100% | Widths as percentages |
| **Eighth-point** | 1/576 inch | Border widths |

---

## 4. Paragraphs (`w:p`)

The `w:p` element is the fundamental block-level container:

```xml
<w:p>
  <!-- Optional paragraph mark properties -->
  <w:pPr>
    <w:pStyle w:val="Heading1"/>        <!-- Named paragraph style -->
    <w:jc w:val="both"/>               <!-- Justification: left | center | right | both | distribute -->
    <w:ind w:left="720" w:right="0" w:firstLine="720"/>  <!-- Indentation in twips -->
    <w:spacing w:before="240" w:after="120" w:line="240" w:lineRule="auto"/>
    <w:outlineLvl w:val="0"/>           <!-- Outline level 0–8 -->
    <w:keepNext/>                       <!-- Keep with next paragraph -->
    <w:keepLines/>                      <!-- Keep lines together -->
    <w:pageBreakBefore/>               <!-- Page break before -->
    <w:numPr>                           <!-- List number properties -->
      <w:ilvl w:val="0"/>              <!-- Indent level 0–8 -->
      <w:numId w:val="1"/>             <!-- References numbering.xml -->
    </w:numPr>
    <w:rPr>                             <!-- Run properties for paragraph mark -->
      <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
      <w:sz w:val="24"/>               <!-- 12pt -->
    </w:rPr>
  </w:pPr>

  <!-- Runs (inline content) -->
  <w:r>
    <w:rPr>
      <w:b/>                            <!-- Bold -->
      <w:i/>                            <!-- Italic -->
      <w:color w:val="FF0000"/>        <!-- Red text -->
    </w:rPr>
    <w:t>Bold italic red text</w:t>
  </w:r>

  <w:r>
    <w:t xml:space="preserve"> and normal text.</w:t>
  </w:r>
</w:p>
```

---

## 5. Runs (`w:r`) and Run Properties (`w:rPr`)

A run is a contiguous region of text sharing the same character formatting:

```xml
<w:r>
  <w:rPr>
    <w:rStyle w:val="StrongEmphasis"/>  <!-- Named character style -->
    <w:rFonts w:ascii="Calibri"
              w:hAnsi="Calibri"
              w:cs="Arial"/>            <!-- Complex script font -->
    <w:b/>                              <!-- Bold (empty element = true) -->
    <w:bCs/>                            <!-- Bold complex script -->
    <w:i/>                              <!-- Italic -->
    <w:iCs/>                            <!-- Italic complex script -->
    <w:u w:val="single"/>              <!-- Underline: single | double | dotted | wave | none -->
    <w:strike/>                         <!-- Strikethrough -->
    <w:dstrike/>                        <!-- Double strikethrough -->
    <w:color w:val="FF0000"/>          <!-- Hex color (no #) -->
    <w:highlight w:val="yellow"/>       <!-- Highlight: yellow | cyan | magenta | darkBlue... -->
    <w:sz w:val="24"/>                  <!-- Font size in half-points (24 = 12pt) -->
    <w:szCs w:val="24"/>               <!-- Complex script size -->
    <w:kern w:val="16"/>               <!-- Kerning threshold in half-points -->
    <w:spacing w:val="20"/>            <!-- Character spacing in twentieths of a point -->
    <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="ar-SA"/>
    <w:vertAlign w:val="superscript"/> <!-- superscript | subscript -->
    <w:caps/>                           <!-- All caps -->
    <w:smallCaps/>                      <!-- Small caps -->
    <w:vanish/>                         <!-- Hidden text -->
    <w:shd w:val="clear" w:fill="FFFF00"/>  <!-- Shading/background -->
    <w:border w:val="single" w:sz="4" w:color="000000"/>  <!-- Character border -->
  </w:rPr>
  <w:t>Formatted text content</w:t>
</w:r>
```

### Whitespace in `w:t`

Use `xml:space="preserve"` when the text starts or ends with spaces:

```xml
<w:t xml:space="preserve"> leading or trailing space </w:t>
```

---

## 6. Paragraph Properties (`w:pPr`) Reference

| Element | Attribute | Description |
| --- | --- | --- |
| `w:pStyle` | `w:val` | Named paragraph style |
| `w:jc` | `w:val` | Alignment: `left`, `right`, `center`, `both`, `distribute` |
| `w:ind` | `w:left`, `w:right`, `w:firstLine`, `w:hanging` | Indentation (twips) |
| `w:spacing` | `w:before`, `w:after`, `w:line`, `w:lineRule` | Spacing (twips); lineRule: `auto`, `exact`, `atLeast` |
| `w:outlineLvl` | `w:val` | Outline level (0=Heading1) |
| `w:numPr` | — | List properties container |
| `w:keepNext` | — | Keep with next paragraph |
| `w:keepLines` | — | Keep lines together |
| `w:pageBreakBefore` | — | Page break before |
| `w:suppressLineNumbers` | — | No line numbers |
| `w:framePr` | — | Paragraph frame (legacy) |
| `w:widowControl` | `w:val` | Widow/orphan control |
| `w:tabs` | — | Tab stop definitions |
| `w:shd` | `w:fill`, `w:val` | Paragraph background shading |
| `w:pBdr` | — | Paragraph borders |
| `w:textDirection` | `w:val` | Text direction |
| `w:contextualSpacing` | — | No space between same-style paragraphs |
| `w:sectPr` | — | Section break (for all but last section) |

---

## 7. Tables (`w:tbl`)

```xml
<w:tbl>
  <!-- Table properties -->
  <w:tblPr>
    <w:tblStyle w:val="TableGrid"/>
    <w:tblW w:w="9360" w:type="dxa"/>  <!-- Table width in twips -->
    <w:tblBorders>
      <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
    </w:tblBorders>
    <w:tblLayout w:type="fixed"/>
    <w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0"
               w:firstColumn="1" w:lastColumn="0"
               w:noHBand="0" w:noVBand="1"/>
  </w:tblPr>

  <!-- Column widths -->
  <w:tblGrid>
    <w:gridCol w:w="3120"/>
    <w:gridCol w:w="3120"/>
    <w:gridCol w:w="3120"/>
  </w:tblGrid>

  <!-- Header row -->
  <w:tr>
    <w:trPr>
      <w:tblHeader/>               <!-- This row is a header -->
    </w:trPr>
    <w:tc>
      <w:tcPr>
        <w:tcW w:w="3120" w:type="dxa"/>
        <w:shd w:fill="2E74B5" w:val="clear"/>
      </w:tcPr>
      <w:p><w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/></w:rPr>
        <w:t>Column A</w:t></w:r></w:p>
    </w:tc>
    <!-- ... more cells ... -->
  </w:tr>

  <!-- Data row -->
  <w:tr>
    <w:tc>
      <w:tcPr>
        <w:tcW w:w="3120" w:type="dxa"/>
        <!-- Cell spanning: -->
        <!-- <w:gridSpan w:val="2"/> for column span -->
        <!-- <w:vMerge w:val="restart"/> for vertical merge start -->
        <!-- <w:vMerge/> for vertical merge continuation -->
      </w:tcPr>
      <w:p><w:r><w:t>Cell content</w:t></w:r></w:p>
    </w:tc>
  </w:tr>

</w:tbl>
```

---

## 8. Sections and Page Layout

Each section defines its own page size, margins, orientation, and columns. The last section's properties are in `w:body/w:sectPr`; earlier sections have `w:sectPr` at the end of the last paragraph in the section.

```xml
<w:sectPr>
  <w:headerReference w:type="default" r:id="rId4"/>  <!-- header part -->
  <w:footerReference w:type="default" r:id="rId5"/>  <!-- footer part -->
  <w:pgSz w:w="12240" w:h="15840" w:orient="portrait"/>  <!-- letter portrait -->
  <w:pgMar w:top="1440" w:right="1440" w:bottom="1440"
           w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
  <w:pgNumType w:fmt="decimal" w:start="1"/>
  <w:formProt w:val="false"/>
  <w:titlePg/>                    <!-- distinct first page header/footer -->
  <w:evenAndOddHeaders/>          <!-- distinct even/odd page headers -->
  <w:cols w:num="2" w:space="720"/>  <!-- 2-column layout -->
  <w:type w:val="continuous"/>    <!-- section type: nextPage | continuous | evenPage | oddPage | nextColumn -->
  <w:docGrid w:type="lines" w:linePitch="240"/>
</w:sectPr>
```

Page size values (in twips, 1/1440 inch):

| Paper | Width | Height |
| --- | --- | --- |
| Letter | 12240 | 15840 |
| A4 | 11906 | 16838 |
| Legal | 12240 | 20160 |
| A3 | 16838 | 23811 |

---

## 9. Lists and Numbering

Lists in WordprocessingML are defined in `word/numbering.xml` and referenced via `w:numPr` in paragraphs.

### `word/numbering.xml` Structure

```xml
<w:numbering xmlns:w="...">

  <!-- Abstract numbering definition -->
  <w:abstractNum w:abstractNumId="0">
    <w:multiLevelType w:val="hybridMultilevel"/>

    <!-- Level 0 (top level): 1. 2. 3. ... -->
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/>
      <w:numFmt w:val="decimal"/>         <!-- decimal | lowerRoman | upperRoman | lowerLetter | upperLetter | bullet | none -->
      <w:lvlText w:val="%1."/>            <!-- %1 = level 0 number -->
      <w:lvlJc w:val="left"/>
      <w:pPr>
        <w:ind w:left="720" w:hanging="360"/>
      </w:pPr>
    </w:lvl>

    <!-- Level 1: a. b. c. ... -->
    <w:lvl w:ilvl="1">
      <w:start w:val="1"/>
      <w:numFmt w:val="lowerLetter"/>
      <w:lvlText w:val="%2."/>
      <w:pPr><w:ind w:left="1440" w:hanging="360"/></w:pPr>
    </w:lvl>

  </w:abstractNum>

  <!-- Concrete numbering instance (references abstract) -->
  <w:num w:numId="1">
    <w:abstractNumId w:val="0"/>
    <!-- Optional level overrides -->
  </w:num>

</w:numbering>
```

### Paragraph Reference to List

```xml
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListParagraph"/>
    <w:numPr>
      <w:ilvl w:val="0"/>     <!-- Level (0-based) -->
      <w:numId w:val="1"/>    <!-- References w:num in numbering.xml -->
    </w:numPr>
  </w:pPr>
  <w:r><w:t>First list item</w:t></w:r>
</w:p>
```

---

## 10. Hyperlinks

```xml
<!-- External hyperlink (requires relationship) -->
<w:hyperlink r:id="rId10" w:history="1">
  <w:r>
    <w:rPr>
      <w:rStyle w:val="Hyperlink"/>
    </w:rPr>
    <w:t>Click here</w:t>
  </w:r>
</w:hyperlink>

<!-- Internal anchor hyperlink -->
<w:hyperlink w:anchor="BookmarkName">
  <w:r>
    <w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr>
    <w:t>Jump to section</w:t>
  </w:r>
</w:hyperlink>
```

In `word/_rels/document.xml.rels`:

```xml
<Relationship Id="rId10"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
    Target="https://example.com"
    TargetMode="External"/>
```

---

## 11. Bookmarks

```xml
<w:bookmarkStart w:id="0" w:name="IntroSection"/>
<w:p>
  <w:r><w:t>Bookmarked content</w:t></w:r>
</w:p>
<w:bookmarkEnd w:id="0"/>
```

---

## 12. Comments, Footnotes, and Endnotes

### Comments

Comments are stored in `word/comments.xml` and referenced in the document:

```xml
<!-- In document.xml -->
<w:commentRangeStart w:id="1"/>
<w:r><w:t>Commented text</w:t></w:r>
<w:commentRangeEnd w:id="1"/>
<w:r><w:commentReference w:id="1"/></w:r>

<!-- In comments.xml -->
<w:comment w:id="1" w:author="Jane Smith" w:date="2024-03-15T10:00:00Z"
           w:initials="JS">
  <w:p><w:r><w:t>Comment text here.</w:t></w:r></w:p>
</w:comment>
```

### Footnotes

Stored in `word/footnotes.xml`:

```xml
<!-- Reference in document.xml -->
<w:r>
  <w:footnoteReference w:id="1"/>
</w:r>

<!-- In footnotes.xml -->
<w:footnote w:type="normal" w:id="1">
  <w:p>
    <w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr>
    <w:r>
      <w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr>
      <w:footnoteRef/>
    </w:r>
    <w:r><w:t xml:space="preserve"> Footnote content here.</w:t></w:r>
  </w:p>
</w:footnote>
```

---

## 13. Track Changes (Revision Marks)

```xml
<!-- Inserted text -->
<w:ins w:id="5" w:author="Jane Smith" w:date="2024-03-15T10:00:00Z">
  <w:r><w:t>Inserted text</w:t></w:r>
</w:ins>

<!-- Deleted text -->
<w:del w:id="6" w:author="John Doe" w:date="2024-03-16T09:00:00Z">
  <w:r><w:delText>Deleted text</w:delText></w:r>
</w:del>

<!-- Format change -->
<w:pPrChange w:id="7" w:author="Jane Smith" w:date="2024-03-15T10:00:00Z">
  <w:pPr><!-- Original paragraph properties --></w:pPr>
</w:pPrChange>
```

---

## 14. Structured Document Tags (SDTs)

SDTs provide content controls for forms and templated content:

```xml
<w:sdt>
  <w:sdtPr>
    <w:alias w:val="First Name"/>
    <w:tag w:val="firstName"/>
    <w:showingPlcHdr/>
    <w:text/>     <!-- plain text content control -->
    <!-- Other types: w:date, w:comboBox, w:dropDownList, w:richText, w:checkbox, w:picture -->
  </w:sdtPr>
  <w:sdtContent>
    <w:p>
      <w:r>
        <w:rPr><w:rStyle w:val="PlaceholderText"/></w:rPr>
        <w:t>Click here to enter text.</w:t>
      </w:r>
    </w:p>
  </w:sdtContent>
</w:sdt>
```

---

*Previous: [XML Namespaces ←](./04-xml-namespaces.md) | Next: [SpreadsheetML →](./06-spreadsheetml.md)*
