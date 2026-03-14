# ODF ↔ OOXML Feature Mapping Reference

> **Cross-references:** [Comparison](./01-comparison.md) | [Conversion](./02-conversion.md) | [ODF Text Documents](../odf/05-text-documents.md) | [OOXML WordprocessingML](../ooxml/05-wordprocessingml.md)

---

## 1. Text Document Element Mapping

### Structural Elements

| ODF Element | OOXML Element | Fidelity | Notes |
| --- | --- | --- | --- |
| `<office:text>` | `<w:body>` | High | Body container |
| `<text:p>` | `<w:p>` | High | Paragraph |
| `<text:h>` | `<w:p>` + `<w:pStyle w:val="Heading*"/>` | High | Heading (ODF has explicit outline-level) |
| `<text:span>` | `<w:r>` with `<w:rStyle>` | High | Inline span |
| `<text:a>` | `<w:hyperlink>` | High | Hyperlink |
| `<text:line-break>` | `<w:br>` | High | Line break in paragraph |
| `<text:tab>` | `<w:tab>` | High | Tab character |
| `<text:s text:c="N">` | `<w:r><w:t> …N spaces…</w:t></w:r>` | Medium | Space runs |
| `<text:list>` + `<text:list-item>` | `<w:p>` + `<w:numPr>` | Medium | Different model: ODF uses containers, OOXML uses paragraph references |
| `<text:section>` | `<w:sectPr>` (section break) | Low | Different section model |
| `<text:bookmark>` | `<w:bookmarkStart>/<w:bookmarkEnd>` | High | Named bookmark |
| `<text:footnote>` | `<w:footnote>` in footnotes.xml | High | Footnote |
| `<text:endnote>` | `<w:endnote>` in endnotes.xml | High | Endnote |
| `<office:annotation>` | `<w:comment>` in comments.xml | High | Comment/annotation |

### Character Properties

| ODF Property | OOXML Property | Notes |
| --- | --- | --- |
| `fo:font-family` | `w:rFonts/@w:ascii` | Font family |
| `fo:font-size` | `w:sz` (half-points) | Unit conversion needed |
| `fo:font-weight="bold"` | `<w:b/>` | Bold |
| `fo:font-style="italic"` | `<w:i/>` | Italic |
| `style:text-underline-style="solid"` | `<w:u w:val="single"/>` | Underline |
| `style:text-line-through-style="solid"` | `<w:strike/>` | Strikethrough |
| `fo:color` | `<w:color w:val="RRGGBB"/>` | Text color (no # in OOXML) |
| `fo:background-color` | `<w:highlight w:val="…"/>` or `<w:shd/>` | Background |
| `style:text-position="super 58%"` | `<w:vertAlign w:val="superscript"/>` | Superscript |
| `style:text-position="sub 58%"` | `<w:vertAlign w:val="subscript"/>` | Subscript |
| `fo:language` | `<w:lang w:val="…"/>` | Language |
| `fo:letter-spacing` | `<w:spacing w:val="…"/>` | Character spacing |
| `fo:font-variant="small-caps"` | `<w:smallCaps/>` | Small caps |
| `fo:text-decoration="underline"` | `<w:u/>` | |

### Paragraph Properties

| ODF Property | OOXML Property | Notes |
| --- | --- | --- |
| `fo:text-align` | `<w:jc w:val="…"/>` | Alignment (values map: `justify` → `both`) |
| `fo:text-indent` | `<w:ind w:firstLine="…"/>` | First-line indent (unit conversion) |
| `fo:margin-left` | `<w:ind w:left="…"/>` | Left indent |
| `fo:margin-right` | `<w:ind w:right="…"/>` | Right indent |
| `fo:margin-top` | `<w:spacing w:before="…"/>` | Space before paragraph |
| `fo:margin-bottom` | `<w:spacing w:after="…"/>` | Space after paragraph |
| `fo:line-height` | `<w:spacing w:line="…" w:lineRule="…"/>` | Line spacing |
| `fo:keep-together="always"` | `<w:keepLines/>` | Keep lines together |
| `fo:keep-with-next="always"` | `<w:keepNext/>` | Keep with next |
| `fo:break-before="page"` | `<w:pageBreakBefore/>` | Page break before |
| `style:writing-mode` | `<w:textDirection w:val="…"/>` | Writing mode/direction |
| `text:number-lines` | `<w:suppressLineNumbers/>` | Line numbering |

---

## 2. Table Element Mapping

| ODF Element | OOXML Element | Fidelity | Notes |
| --- | --- | --- | --- |
| `<table:table>` | `<w:tbl>` | High | Table container |
| `<table:table-row>` | `<w:tr>` | High | Row |
| `<table:table-cell>` | `<w:tc>` | High | Cell |
| `<table:covered-table-cell>` | *(implicit in col/row span)* | Medium | OOXML uses `vMerge` and `gridSpan` |
| `<table:table-column>` | `<w:tblGrid>` + `<w:gridCol>` | High | Column definitions |
| `<table:table-header-rows>` | `<w:trPr><w:tblHeader/>` | High | Header rows |
| `table:number-columns-spanned` | `<w:tcPr><w:gridSpan w:val="N"/>` | High | Column span |
| `table:number-rows-spanned` | `<w:vMerge w:val="restart"/>` | High | Row span start |
| `<table:covered-table-cell>` (row span) | `<w:vMerge/>` | High | Row span continuation |

---

## 3. Spreadsheet Element Mapping

| ODF Element/Attribute | OOXML Element | Fidelity | Notes |
| --- | --- | --- | --- |
| `<table:table>` | `<worksheet>` | High | Sheet |
| `<table:table-row>` | `<row>` | High | Row |
| `<table:table-cell>` | `<c>` | High | Cell |
| `office:value-type="float"` + `office:value` | `<v>` (no `t` attribute) | High | Numeric cell |
| `office:value-type="string"` | `<c t="s"><v>index</v>` | High | String → shared string index |
| `office:value-type="date"` | `<c t="d">` or date-formatted number | Medium | Date handling differs |
| `office:value-type="boolean"` | `<c t="b">` | High | Boolean |
| `table:formula="of:=..."` | `<f>...</f>` | High | Formula (syntax differences) |
| `table:number-columns-repeated` | *(use multiple `<c>` or column ranges)* | High | Efficiency optimization |
| `table:number-rows-repeated` | *(must expand rows)* | High | Must expand to individual rows |
| `<table:named-range>` | `<definedName>` | High | Named range |
| `<table:data-pilot-table>` | `<pivotTableDefinition>` | Medium | Pivot table model differs |
| `<table:content-validation>` | `<dataValidation>` | High | Data validation |
| `<table:conditional-format>` | `<conditionalFormatting>` | Medium | Some rule types don't map |

### Formula Syntax Differences

| Operation | ODF (OpenFormula) | OOXML (Excel) |
| --- | --- | --- |
| Cell reference (relative) | `[.A1]` | `A1` |
| Cell reference (absolute) | `[$A$1]` | `$A$1` |
| Sheet reference | `[$Sheet1.$A$1]` | `Sheet1!$A$1` |
| Range | `[.A1:.D10]` | `A1:D10` |
| Formula prefix | `of:=` | `=` (no prefix) |
| Logical AND | `AND(a;b)` | `AND(a,b)` |
| Argument separator | `;` (locale) | `,` |

---

## 4. Presentation Element Mapping

| ODF Element | OOXML Element | Fidelity | Notes |
| --- | --- | --- | --- |
| `<draw:page>` | `<p:sld>` | High | Slide |
| `<style:master-page>` | `<p:sldMaster>` | Medium | Masters map; layout hierarchy differs |
| `<draw:frame presentation:class="title">` | `<p:sp><p:ph type="title"/>` | High | Title placeholder |
| `<draw:frame presentation:class="body">` | `<p:sp><p:ph type="body"/>` | High | Content placeholder |
| `<draw:image>` | `<pic:pic>` in `<p:pic>` | High | Image |
| `<draw:rect>`, `<draw:circle>` | `<p:sp>` + `<a:prstGeom>` | High | Basic shapes |
| `<draw:g>` | `<p:grpSp>` | High | Group shape |
| `<draw:connector>` | `<p:cxnSp>` | High | Connector |
| `<presentation:transition>` | `<p:transition>` | Medium | Many transitions map |
| `<anim:par>` | `<p:timing>` | Low | Animation model differs significantly |
| `<draw:object>` (chart) | `<p:graphicFrame>` + chart part | Medium | Chart formats differ |
| `draw:frame` (draw:object=SmartArt) | No equivalent | Low | ODF has no SmartArt |
| `<presentation:notes>` | `<p:notes>` separate part | High | |

---

## 5. Style Mapping

| ODF Style Family | OOXML Style Type | Mapping |
| --- | --- | --- |
| `style:family="paragraph"` | `w:type="paragraph"` | Direct |
| `style:family="text"` | `w:type="character"` | Direct |
| `style:family="table"` | `w:type="table"` | Direct |
| `style:family="graphic"` | Draw styles (no direct OOXML equivalent) | Medium |
| `style:family="page-layout"` | `w:sectPr` per section | Low |
| `style:family="drawing-page"` | Slide background in masters | Medium |
| `style:family="presentation"` | PML placeholder text styles | Medium |

### Style Inheritance

```text
ODF:  style:parent-style-name="ParentStyle"
OOXML: w:basedOn w:val="ParentStyle"
```

Both support deep inheritance chains. The root style:

- ODF: `Default Paragraph Style` (family: paragraph)
- OOXML: `Normal` (type: paragraph)

---

## 6. Metadata Mapping

| ODF Element | OOXML Element | Notes |
| --- | --- | --- |
| `<dc:title>` | `<dc:title>` in core.xml | Direct |
| `<dc:description>` | `<dc:description>` in core.xml | Direct |
| `<dc:subject>` | `<dc:subject>` in core.xml | Direct |
| `<dc:creator>` (last modified by) | `<cp:lastModifiedBy>` | Semantic differs slightly |
| `<meta:initial-creator>` | `<dc:creator>` | First author |
| `<meta:creation-date>` | `<dcterms:created>` | ISO 8601 |
| `<dc:date>` (modification) | `<dcterms:modified>` | ISO 8601 |
| `<meta:editing-cycles>` | `<cp:revision>` | Similar |
| `<meta:keyword>` | `<cp:keywords>` (comma-separated) | ODF: multiple elements; OOXML: one string |
| `<meta:generator>` | `<Application>` in app.xml | Application name |
| `<meta:user-defined>` | Custom XML data parts | Different model |
| `<meta:document-statistic>` | Word/page counts in app.xml | Similar |

---

## 7. Drawing and Graphics Mapping

| ODF Property/Element | DrawingML Equivalent | Notes |
| --- | --- | --- |
| `svg:x`, `svg:y` | `<a:off x="…" y="…"/>` (EMU) | Unit conversion required |
| `svg:width`, `svg:height` | `<a:ext cx="…" cy="…"/>` (EMU) | |
| `draw:fill="solid"` + `draw:fill-color` | `<a:solidFill><a:srgbClr val="…"/>` | |
| `draw:fill="gradient"` | `<a:gradFill>` | |
| `draw:fill="bitmap"` | `<a:blipFill>` | |
| `draw:fill="none"` | `<a:noFill/>` | |
| `draw:stroke="solid"` | `<a:ln><a:solidFill>…</a:solidFill>` | |
| `svg:stroke-width` | `<a:ln w="…"/>` (EMU) | |
| `draw:corner-radius` on `draw:rect` | `<a:prstGeom prst="roundRect"><a:avLst><a:gd…/>` | |
| `draw:shadow="visible"` | `<a:outerShdw>` | |
| ODF gradient | DrawingML gradient | Different model; most gradients convert |

---

## 8. Unit Conversion Reference

| Unit | ODF Usage | OOXML Equivalent | Conversion |
| --- | --- | --- | --- |
| cm | `svg:x`, margins, sizes | EMU | × 360,000 |
| mm | page sizes | EMU | × 36,000 |
| in | page sizes | EMU | × 914,400 |
| pt | font size | half-points (w:sz) | × 2 |
| pt | spacing | twips | × 20 |
| px | screen sizes | EMU (at 96 DPI) | × 9,525 |
| % | relative widths | varies | context-dependent |

---

## 9. Feature Loss Summary (Unavoidable)

### ODF → OOXML (features lost)

| Feature | Reason for Loss |
| --- | --- |
| RDF metadata | No OOXML equivalent for arbitrary RDF |
| Text section complex layouts | OOXML section model is page-level |
| OpenPGP encryption | OOXML has no OpenPGP support |
| Flat ODF format | No single-file OOXML equivalent |
| Some accessibility attributes | Different accessibility model |
| ODF database front-end | No equivalent in OOXML |

### OOXML → ODF (features lost)

| Feature | Reason for Loss |
| --- | --- |
| SmartArt | ODF has no SmartArt system |
| Content controls (SDTs) | ODF user fields are not equivalent |
| Complex table conditional formatting | ODF table style regions are limited |
| Full DrawingML effects (3D, glow, reflection) | ODF effects are more limited |
| Themes | ODF 1.3 lacks a theme system |
| VML shapes (Transitional) | ODF uses SVG-like geometry; VML doesn't map cleanly |
| Macros (VBA) | ODF uses StarBasic; completely different |
| Document Information Panel | No ODF equivalent |

---

*Previous: [Conversion ←](./02-conversion.md) | [Back to Main Index →](../README.md)*
