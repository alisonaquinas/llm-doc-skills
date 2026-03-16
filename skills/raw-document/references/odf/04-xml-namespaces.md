# ODF XML Namespaces

> **Cross-references:** [Package Structure](./03-package-structure.md) | [Text Documents](./05-text-documents.md) | [Styles](./09-styles-formatting.md) | [Spec §3](https://docs.oasis-open.org/office/OpenDocument/v1.3/os/part3-schema/)

---

## 1. Overview

ODF documents use a large number of XML namespaces, all anchored under the OASIS base URI:

```text
urn:oasis:names:tc:opendocument:xmlns:<name>:1.0
```

These namespaces separate different functional areas of the document model, making it easier to parse and extend ODF documents.

---

## 2. Core ODF Namespaces (Complete Reference)

### Primary Document Namespaces

| Prefix | Namespace URI | Purpose |
| --- | --- | --- |
| `office` | `urn:oasis:names:tc:opendocument:xmlns:office:1.0` | Root elements, document-level constructs |
| `text` | `urn:oasis:names:tc:opendocument:xmlns:text:1.0` | Text content (paragraphs, headings, lists, fields) |
| `table` | `urn:oasis:names:tc:opendocument:xmlns:table:1.0` | Tables (rows, cells, columns) |
| `draw` | `urn:oasis:names:tc:opendocument:xmlns:drawing:1.0` | Drawing shapes, frames, images |
| `presentation` | `urn:oasis:names:tc:opendocument:xmlns:presentation:1.0` | Presentation-specific elements |
| `chart` | `urn:oasis:names:tc:opendocument:xmlns:chart:1.0` | Charts |
| `form` | `urn:oasis:names:tc:opendocument:xmlns:form:1.0` | Form controls |
| `db` | `urn:oasis:names:tc:opendocument:xmlns:database:1.0` | Database front-end |
| `dr3d` | `urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0` | 3D drawing shapes |
| `anim` | `urn:oasis:names:tc:opendocument:xmlns:animation:1.0` | Animations |
| `script` | `urn:oasis:names:tc:opendocument:xmlns:script:1.0` | Scripts/macros |
| `config` | `urn:oasis:names:tc:opendocument:xmlns:config:1.0` | Application configuration |
| `meta` | `urn:oasis:names:tc:opendocument:xmlns:meta:1.0` | Document metadata |

### Style Namespaces

| Prefix | Namespace URI | Purpose |
| --- | --- | --- |
| `style` | `urn:oasis:names:tc:opendocument:xmlns:style:1.0` | Style definitions |
| `number` | `urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0` | Number/date/time format styles |

### Package and Manifest Namespaces

| Prefix | Namespace URI | Purpose |
| --- | --- | --- |
| `manifest` | `urn:oasis:names:tc:opendocument:xmlns:manifest:1.0` | Package manifest |

### Compatibility Namespaces (W3C/SVG/SMIL)

| Prefix | Namespace URI | Purpose |
| --- | --- | --- |
| `fo` | `urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0` | CSS/XSL-FO style properties |
| `svg` | `urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0` | SVG-compatible attributes |
| `smil` | `urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0` | SMIL animation attributes |

---

## 3. External Namespaces Used in ODF Documents

ODF documents also incorporate several external (non-OASIS) namespaces:

| Prefix | Namespace URI | Purpose |
| --- | --- | --- |
| `dc` | `http://purl.org/dc/elements/1.1/` | Dublin Core metadata |
| `xlink` | `http://www.w3.org/1999/xlink` | XLink for hyperlinks |
| `xml` | `http://www.w3.org/XML/1998/namespace` | Base XML attributes (`xml:id`, `xml:lang`, `xml:space`) |
| `rdf` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | RDF metadata (ODF 1.2+) |
| `rdfa` | `http://docs.oasis-open.org/ns/office/1.2/meta/rdfa#` | RDFa metadata (ODF 1.2+) |
| `grddl` | `http://www.w3.org/2003/g/data-view#` | GRDDL profile |
| `math` | `http://www.w3.org/1998/Math/MathML` | MathML for formulas |
| `xhtml` | `http://www.w3.org/1999/xhtml` | XHTML in annotations |

---

## 4. Namespace Declarations in Documents

In practice, all namespaces are declared on the root element:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
    xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"
    xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0"
    xmlns:math="http://www.w3.org/1998/Math/MathML"
    xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"
    xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"
    xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0"
    xmlns:anim="urn:oasis:names:tc:opendocument:xmlns:animation:1.0"
    xmlns:smil="urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0"
    office:version="1.3">
```

---

## 5. Namespace Usage by Element Category

### `office:` — Document Root and Body Elements

```xml
<office:document-content>    <!-- root of content.xml -->
<office:document-styles>     <!-- root of styles.xml -->
<office:document-meta>       <!-- root of meta.xml -->
<office:document-settings>   <!-- root of settings.xml -->
<office:document>            <!-- root of flat ODF single-file format -->

<office:body>                <!-- document body container -->
<office:text>                <!-- text document body -->
<office:spreadsheet>         <!-- spreadsheet body -->
<office:presentation>        <!-- presentation body -->
<office:drawing>             <!-- drawing body -->
<office:chart>               <!-- chart body -->

<office:automatic-styles>    <!-- automatically generated styles -->
<office:styles>              <!-- named (user-visible) styles -->
<office:master-styles>       <!-- master pages -->
<office:meta>                <!-- metadata container -->
<office:settings>            <!-- settings container -->
<office:scripts>             <!-- scripts container -->
<office:font-face-decls>     <!-- font declarations -->
```

### `text:` — Text Content Elements

```xml
<text:p>                     <!-- paragraph -->
<text:h>                     <!-- heading (with text:outline-level) -->
<text:span>                  <!-- inline text span (for character styles) -->
<text:a>                     <!-- hyperlink -->
<text:list>                  <!-- list container -->
<text:list-item>             <!-- list item -->
<text:line-break>            <!-- forced line break -->
<text:tab>                   <!-- tab character -->
<text:s>                     <!-- space (with text:c count attribute) -->
<text:soft-page-break>       <!-- soft page break hint -->
<text:page-break>            <!-- hard page break -->

<!-- Text fields -->
<text:date>                  <!-- date field -->
<text:time>                  <!-- time field -->
<text:page-number>           <!-- page number field -->
<text:page-count>            <!-- page count field -->
<text:author-name>           <!-- author field -->
<text:chapter>               <!-- chapter title/number field -->
<text:sequence>              <!-- sequence number field -->
<text:variable-set>          <!-- user variable -->
<text:variable-get>          <!-- retrieve variable -->

<!-- Sections and anchoring -->
<text:section>               <!-- named section -->
<text:bookmark>              <!-- named bookmark -->
<text:bookmark-start>        <!-- bookmark start point -->
<text:bookmark-end>          <!-- bookmark end point -->

<!-- Tables of contents -->
<text:table-of-content>      <!-- auto-generated TOC -->
<text:index-body>            <!-- index body content -->
<text:index-entry-chapter>   <!-- chapter entry in index -->
```

### `table:` — Spreadsheet and Table Elements

```xml
<table:table>                <!-- table or spreadsheet -->
<table:table-row>            <!-- table row -->
<table:table-cell>           <!-- table cell -->
<table:covered-table-cell>   <!-- spanned/covered cell -->
<table:table-column>         <!-- column properties -->
<table:table-header-rows>    <!-- repeated header rows -->
<table:table-header-columns> <!-- repeated header columns -->
<table:named-range>          <!-- named range in spreadsheet -->
<table:data-pilot-table>     <!-- pivot table -->
<table:database-range>       <!-- database import range -->
```

### `draw:` — Drawing and Frame Elements

```xml
<draw:frame>                 <!-- frame container (for images, objects, etc.) -->
<draw:image>                 <!-- image inside a frame -->
<draw:object>                <!-- embedded ODF object -->
<draw:object-ole>            <!-- OLE object -->
<draw:text-box>              <!-- text box inside a frame -->
<draw:rect>                  <!-- rectangle shape -->
<draw:circle>                <!-- circle/ellipse shape -->
<draw:line>                  <!-- line shape -->
<draw:polyline>              <!-- polyline -->
<draw:polygon>               <!-- polygon -->
<draw:path>                  <!-- SVG-like path shape -->
<draw:connector>             <!-- connector between shapes -->
<draw:caption>               <!-- caption shape -->
<draw:g>                     <!-- shape group -->
<draw:page>                  <!-- drawing page / slide -->
<draw:page-thumbnail>        <!-- slide thumbnail -->
<draw:layer-set>             <!-- layer definitions -->
<draw:layer>                 <!-- individual layer -->
<draw:glue-point>            <!-- connection point -->
<draw:plugin>                <!-- plugin object -->
```

### `style:` — Style Definition Elements

```xml
<style:style>                <!-- named or automatic style -->
<style:default-style>        <!-- default style for family -->
<style:page-layout>          <!-- page dimensions and margins -->
<style:master-page>          <!-- master page (slide master) -->
<style:font-face>            <!-- font face declaration -->
<style:header>               <!-- page header -->
<style:footer>               <!-- page footer -->
<style:header-left>          <!-- left-page header -->
<style:footer-left>          <!-- left-page footer -->
<style:columns>              <!-- multi-column layout -->
<style:column>               <!-- single column definition -->
<style:drop-cap>             <!-- drop cap configuration -->
<style:list-level-properties> <!-- list level formatting -->
<style:graphic-properties>  <!-- frame/drawing formatting -->
<style:chart-properties>    <!-- chart formatting -->
<style:drawing-page-properties> <!-- slide/page background -->
<style:paragraph-properties> <!-- paragraph formatting -->
<style:text-properties>     <!-- character formatting -->
<style:table-properties>    <!-- table formatting -->
<style:table-cell-properties> <!-- cell formatting -->
<style:section-properties>  <!-- section formatting -->
```

### `fo:` — XSL-FO Compatible Properties (used as attributes)

These are used as **attributes** within `<style:*-properties>` elements:

```text
fo:font-family        fo:font-size          fo:font-style
fo:font-weight        fo:color              fo:background-color
fo:text-align         fo:text-indent        fo:margin-left
fo:margin-right       fo:margin-top         fo:margin-bottom
fo:padding            fo:padding-left       fo:padding-right
fo:padding-top        fo:padding-bottom     fo:border
fo:border-left        fo:border-right       fo:border-top
fo:border-bottom      fo:line-height        fo:keep-together
fo:keep-with-next     fo:break-before       fo:break-after
fo:widows             fo:orphans            fo:language
fo:country            fo:letter-spacing     fo:word-spacing
fo:text-decoration    fo:text-shadow        fo:wrap-option
fo:column-count       fo:column-gap
```

### `svg:` — SVG-Compatible Attributes

Used in shape and image positioning:

```text
svg:x         svg:y          svg:width       svg:height
svg:rx        svg:ry         svg:cx          svg:cy
svg:r         svg:d          svg:points      svg:viewBox
svg:x1        svg:y1         svg:x2          svg:y2
svg:fill      svg:stroke     svg:stroke-width
```

---

## 6. Foreign Namespace Extensions

ODF allows application-specific extensions using foreign namespaces. The ODF specification requires conformant processors to **preserve** (not discard) foreign namespace content they don't understand.

Example (LibreOffice-specific extension):

```xml
xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0"
```

---

## 7. Namespace Version Notes

All core ODF namespaces carry version `1.0` in their URI (e.g., `xmlns:office:1.0`), regardless of whether the document conforms to ODF 1.0, 1.1, 1.2, or 1.3. The actual ODF version is declared through:

```xml
office:version="1.3"
```

---

*Previous: [Package Structure ←](./03-package-structure.md) | Next: [Text Documents →](./05-text-documents.md)*
