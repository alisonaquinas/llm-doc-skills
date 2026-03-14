# OOXML Styles and Themes

> **Cross-references:** [WordprocessingML](./05-wordprocessingml.md) | [SpreadsheetML](./06-spreadsheetml.md) | [DrawingML](./08-drawingml.md) | [ODF Styles](../odf/09-styles-formatting.md)

---

## 1. OOXML Theme System

OOXML uses a **theme** system that provides coordinated colors, fonts, and effects for a document. Themes are stored in `theme/theme1.xml` for all document types.

### Theme Structure (`ppt/theme/theme1.xml` or `word/theme/theme1.xml`)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
         name="Office Theme">

  <a:themeElements>

    <!-- Color scheme -->
    <a:clrScheme name="Office">
      <a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>     <!-- Dark 1 -->
      <a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>          <!-- Light 1 -->
      <a:dk2><a:srgbClr val="44546A"/></a:dk2>                          <!-- Dark 2 -->
      <a:lt2><a:srgbClr val="E7E6E6"/></a:lt2>                          <!-- Light 2 -->
      <a:accent1><a:srgbClr val="4472C4"/></a:accent1>                  <!-- Accent 1 -->
      <a:accent2><a:srgbClr val="ED7D31"/></a:accent2>                  <!-- Accent 2 -->
      <a:accent3><a:srgbClr val="A9D18E"/></a:accent3>                  <!-- Accent 3 -->
      <a:accent4><a:srgbClr val="FFC000"/></a:accent4>                  <!-- Accent 4 -->
      <a:accent5><a:srgbClr val="5B9BD5"/></a:accent5>                  <!-- Accent 5 -->
      <a:accent6><a:srgbClr val="70AD47"/></a:accent6>                  <!-- Accent 6 -->
      <a:hlink><a:srgbClr val="0563C1"/></a:hlink>                      <!-- Hyperlink -->
      <a:folHlink><a:srgbClr val="954F72"/></a:folHlink>                 <!-- Followed Hyperlink -->
    </a:clrScheme>

    <!-- Font scheme -->
    <a:fontScheme name="Office">
      <a:majorFont>                  <!-- Headings font -->
        <a:latin typeface="Calibri Light" panose="020F0302020204030204"/>
        <a:ea typeface=""/>
        <a:cs typeface=""/>
        <!-- Script-specific fonts -->
        <a:font script="Jpan" typeface="游ゴシック Light"/>
        <a:font script="Arab" typeface="Times New Roman"/>
      </a:majorFont>
      <a:minorFont>                  <!-- Body font -->
        <a:latin typeface="Calibri" panose="020F0502020204030204"/>
        <a:ea typeface=""/>
        <a:cs typeface=""/>
      </a:minorFont>
    </a:fontScheme>

    <!-- Format scheme (fills, lines, effects) -->
    <a:fmtScheme name="Office">
      <a:fillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:gradFill rotWithShape="1">
          <a:gsLst>
            <a:gs pos="0"><a:schemeClr val="phClr"><a:lumMod val="110000"/>
              <a:satMod val="105000"/></a:schemeClr></a:gs>
            <a:gs pos="100000"><a:schemeClr val="phClr">
              <a:lumMod val="65000"/><a:satMod val="103000"/>
              <a:lumOff val="35000"/></a:schemeClr></a:gs>
          </a:gsLst>
          <a:lin ang="16200000" scaled="0"/>
        </a:gradFill>
        <a:gradFill rotWithShape="1">
          <!-- ... -->
        </a:gradFill>
      </a:fillStyleLst>

      <a:lnStyleLst>
        <a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
              <a:prstDash val="solid"/><a:miter lim="800000"/></a:ln>
        <a:ln w="12700"><!-- medium weight --></a:ln>
        <a:ln w="19050"><!-- heavy weight --></a:ln>
      </a:lnStyleLst>

      <a:effectStyleLst>
        <a:effectStyle><!-- subtle --><a:effectLst/></a:effectStyle>
        <a:effectStyle><!-- moderate --><a:effectLst>
          <a:outerShdw blurRad="40000" dist="23000" dir="5400000" rotWithShape="0">
            <a:srgbClr val="000000"><a:alpha val="35000"/></a:srgbClr>
          </a:outerShdw>
        </a:effectLst></a:effectStyle>
        <a:effectStyle><!-- intense --></a:effectStyle>
      </a:effectStyleLst>

      <a:bgFillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"><a:tint val="95000"/>
          <a:satMod val="170000"/></a:schemeClr></a:solidFill>
        <a:gradFill rotWithShape="1"><!-- ... --></a:gradFill>
      </a:bgFillStyleLst>

    </a:fmtScheme>

  </a:themeElements>

</a:theme>
```

---

## 2. Styles in WordprocessingML

Stored in `word/styles.xml`:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
          xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
          w:docDefaults>

  <!-- Document defaults -->
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia"
                  w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi"/>
        <w:sz w:val="22"/>        <!-- 11pt -->
        <w:szCs w:val="22"/>
        <w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="160" w:line="259" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>

  <!-- Named styles -->

  <!-- Heading 1 -->
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:link w:val="Heading1Char"/>   <!-- linked character style -->
    <w:uiPriority w:val="9"/>
    <w:qFormat/>                     <!-- quick-access style -->
    <w:pPr>
      <w:keepNext/>
      <w:keepLines/>
      <w:spacing w:before="240" w:after="0"/>
      <w:outlineLvl w:val="0"/>      <!-- outline level: 0=H1, 1=H2, etc. -->
    </w:pPr>
    <w:rPr>
      <w:rFonts w:asciiTheme="majorHAnsi" w:eastAsiaTheme="majorEastAsia"
                w:hAnsiTheme="majorHAnsi" w:cstheme="majorBidi"/>
      <w:color w:val="2E74B5" w:themeColor="accent1" w:themeTint="BF"/>
      <w:sz w:val="32"/>             <!-- 16pt -->
      <w:szCs w:val="32"/>
    </w:rPr>
  </w:style>

  <!-- Normal paragraph -->
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
  </w:style>

  <!-- Table style -->
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:basedOn w:val="TableNormal"/>
    <w:tblPr>
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      </w:tblBorders>
    </w:tblPr>
  </w:style>

  <!-- Character style -->
  <w:style w:type="character" w:styleId="Hyperlink">
    <w:name w:val="Hyperlink"/>
    <w:rPr>
      <w:color w:val="0563C1" w:themeColor="hyperlink"/>
      <w:u w:val="single"/>
    </w:rPr>
  </w:style>

</w:styles>
```

### Style Types

| `w:type` | Description |
| --- | --- |
| `paragraph` | Applied via `w:pStyle` in `w:pPr` |
| `character` | Applied via `w:rStyle` in `w:rPr` |
| `table` | Applied via `w:tblStyle` in `w:tblPr` |
| `numbering` | Applied via abstract numbering in `numbering.xml` |

### Built-in Style IDs (partial)

| StyleId | Name |
| --- | --- |
| `Normal` | Normal paragraph |
| `Heading1`–`Heading9` | Heading levels |
| `DefaultParagraphFont` | Default character font |
| `Hyperlink` | Hyperlink character style |
| `TableNormal` | Default table style |
| `ListParagraph` | List paragraph style |
| `PlaceholderText` | Placeholder content |
| `FootnoteText` | Footnote text |
| `EndnoteText` | Endnote text |
| `FootnoteReference` | Footnote reference mark |
| `EndnoteReference` | Endnote reference mark |
| `CommentReference` | Comment reference mark |
| `Strong` | Bold character style |
| `Emphasis` | Italic character style |
| `Code` | Code character style |
| `Title` | Document title |
| `Subtitle` | Document subtitle |
| `Quote` | Block quote |
| `IntenseQuote` | Intense quote |

---

## 3. Table Styles (Conditional Formatting)

Table styles support conditional formatting for different table regions:

```xml
<w:style w:type="table" w:styleId="MyTableStyle">
  <w:tblPr>...</w:tblPr>

  <!-- Whole table properties -->
  <w:tblStylePr w:type="wholeTable">
    <w:tblPr><w:tblBorders>...</w:tblBorders></w:tblPr>
  </w:tblStylePr>

  <!-- First row (header) -->
  <w:tblStylePr w:type="firstRow">
    <w:tblPr>
      <w:tblCellSpacing w:w="0" w:type="dxa"/>
    </w:tblPr>
    <w:trPr><w:cnfStyle w:val="100000000000"/></w:trPr>
    <w:tcPr>
      <w:shd w:val="clear" w:fill="2E74B5"/>
    </w:tcPr>
    <w:rPr><w:b/><w:color w:val="FFFFFF"/></w:rPr>
  </w:tblStylePr>

  <!-- Last row -->
  <w:tblStylePr w:type="lastRow">...</w:tblStylePr>

  <!-- First column -->
  <w:tblStylePr w:type="firstCol">...</w:tblStylePr>

  <!-- Last column -->
  <w:tblStylePr w:type="lastCol">...</w:tblStylePr>

  <!-- Odd rows band -->
  <w:tblStylePr w:type="band1Horz">
    <w:tcPr><w:shd w:val="clear" w:fill="D6E4F7"/></w:tcPr>
  </w:tblStylePr>

  <!-- Even rows band -->
  <w:tblStylePr w:type="band2Horz">...</w:tblStylePr>

  <!-- NW corner -->
  <w:tblStylePr w:type="nwCell">...</w:tblStylePr>

  <!-- Other types: neCell | swCell | seCell | band1Vert | band2Vert -->
</w:style>
```

---

## 4. SpreadsheetML Built-in Number Formats

| ID | Format | ID | Format |
| --- | --- | --- | --- |
| 0 | `General` | 14 | `m/d/yyyy` |
| 1 | `0` | 15 | `d-mmm-yy` |
| 2 | `0.00` | 16 | `d-mmm` |
| 3 | `#,##0` | 17 | `mmm-yy` |
| 4 | `#,##0.00` | 18 | `h:mm AM/PM` |
| 9 | `0%` | 19 | `h:mm:ss AM/PM` |
| 10 | `0.00%` | 20 | `h:mm` |
| 11 | `0.00E+00` | 21 | `h:mm:ss` |
| 12 | `# ?/?` | 22 | `m/d/yyyy h:mm` |
| 13 | `# ??/??` | 37–44 | Accounting formats |
| — | — | 45 | `mm:ss` |
| — | — | 46 | `[h]:mm:ss` |
| — | — | 47 | `mmss.0` |
| — | — | 48 | `##0.0E+0` |
| — | — | 49 | `@` (text) |

Custom number formats use IDs 164+.

---

*Previous: [DrawingML ←](./08-drawingml.md) | Next: [Relationships & Content Types →](./10-relationships-content-types.md)*
