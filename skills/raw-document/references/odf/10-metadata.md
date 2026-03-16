# ODF Metadata

> **Cross-references:** [Package Structure](./03-package-structure.md) | [Namespaces](./04-xml-namespaces.md) | [Security & Signatures](./11-security-signatures.md) | [Specification §3](./02-specification.md)

---

## 1. Overview

ODF documents support two metadata systems:

1. **Simple XML metadata** — Dublin Core + ODF-specific elements in `meta.xml`
2. **RDF-based metadata** — Named graphs via `manifest.rdf` and linked `.rdf` files (ODF 1.2+)

Metadata is stored primarily in `meta.xml` with the root element `<office:document-meta>`.

---

## 2. `meta.xml` Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    office:version="1.3">

  <office:meta>

    <!-- Dublin Core elements -->
    <dc:title>Research Report 2024</dc:title>
    <dc:description>Annual research summary document</dc:description>
    <dc:subject>Research, Science, Technology</dc:subject>
    <dc:creator>Jane Smith</dc:creator>
    <dc:language>en-US</dc:language>
    <dc:date>2024-03-15T14:30:00</dc:date>   <!-- last modification date -->

    <!-- ODF-specific metadata -->
    <meta:initial-creator>John Doe</meta:initial-creator>
    <meta:creation-date>2024-01-10T09:00:00</meta:creation-date>
    <meta:editing-cycles>12</meta:editing-cycles>
    <meta:editing-duration>PT5H23M</meta:editing-duration>  <!-- ISO 8601 duration -->
    <meta:print-date>2024-03-20T08:00:00</meta:print-date>
    <meta:printed-by>Jane Smith</meta:printed-by>
    <meta:generator>LibreOffice/7.6.4.1</meta:generator>
    <meta:template xlink:type="simple"
                   xlink:actuate="onRequest"
                   xlink:title="My Template"
                   xlink:href="../templates/mytemplate.ott"
                   meta:date="2024-01-05T12:00:00"/>

    <!-- Keywords -->
    <meta:keyword>research</meta:keyword>
    <meta:keyword>annual report</meta:keyword>
    <meta:keyword>science</meta:keyword>

    <!-- Document statistics -->
    <meta:document-statistic
        meta:table-count="3"
        meta:image-count="5"
        meta:object-count="2"
        meta:page-count="24"
        meta:paragraph-count="187"
        meta:word-count="4521"
        meta:character-count="28150"
        meta:row-count="0"
        meta:frame-count="7"
        meta:sentence-count="312"
        meta:syllable-count="9043"/>

    <!-- Custom metadata fields -->
    <meta:user-defined meta:name="ReviewStatus">Approved</meta:user-defined>
    <meta:user-defined meta:name="Department">R&amp;D</meta:user-defined>
    <meta:user-defined meta:name="ProjectCode">PRJ-2024-001</meta:user-defined>
    <meta:user-defined meta:name="ReviewDate"
                        meta:value-type="date">2024-03-10</meta:user-defined>
    <meta:user-defined meta:name="EstimatedHours"
                        meta:value-type="float">40</meta:user-defined>
    <meta:user-defined meta:name="Approved"
                        meta:value-type="boolean">true</meta:user-defined>

    <!-- Hyperlink base -->
    <meta:hyperlink-behaviour meta:server-map="false"
                               meta:target-frame-name="_blank"/>
    <meta:auto-reload/>

  </office:meta>

</office:document-meta>
```

---

## 3. Dublin Core Elements in ODF

ODF uses the Dublin Core Metadata Element Set (<http://purl.org/dc/elements/1.1/>):

| Element | `meta:` mapping | Description |
| --- | --- | --- |
| `dc:title` | Document title | Maps to "Title" in file properties |
| `dc:description` | Document description | Maps to "Comments" |
| `dc:subject` | Subject | Maps to "Subject" |
| `dc:creator` | Last modifier | Person who last modified the document |
| `dc:language` | Language | BCP 47 language tag (e.g., `en-US`) |
| `dc:date` | Last modification date | ISO 8601 datetime |
| `dc:type` | (not commonly used) | Document type |
| `dc:format` | (not commonly used) | MIME type |
| `dc:identifier` | (not commonly used) | Document identifier |
| `dc:source` | (not commonly used) | Source reference |
| `dc:publisher` | (not commonly used) | Publisher |
| `dc:contributor` | (not commonly used) | Additional contributors |
| `dc:rights` | (not commonly used) | Rights statement |

---

## 4. ODF-Specific Metadata Elements

| Element | Description | Format |
| --- | --- | --- |
| `meta:initial-creator` | Original document creator | String |
| `meta:creation-date` | Document creation date | ISO 8601 datetime |
| `meta:editing-cycles` | Number of save cycles | Integer |
| `meta:editing-duration` | Total editing time | ISO 8601 duration (PT...) |
| `meta:print-date` | Last print date/time | ISO 8601 datetime |
| `meta:printed-by` | Name of person who printed | String |
| `meta:generator` | Application that created/saved | String |
| `meta:template` | Template the document is based on | `xlink:href` attribute |
| `meta:auto-reload` | Auto-reload settings | `xlink:href`, `meta:delay` |
| `meta:hyperlink-behaviour` | Hyperlink target behaviour | `meta:target-frame-name` |
| `meta:keyword` | Keyword tags | String (multiple allowed) |
| `meta:document-statistic` | Statistics attributes | See attributes below |
| `meta:user-defined` | Custom key/value properties | `meta:name`, `meta:value-type` |

### `meta:document-statistic` Attributes

| Attribute | Description |
| --- | --- |
| `meta:page-count` | Number of pages |
| `meta:paragraph-count` | Number of paragraphs |
| `meta:word-count` | Number of words |
| `meta:character-count` | Number of characters |
| `meta:table-count` | Number of tables |
| `meta:image-count` | Number of images |
| `meta:object-count` | Number of embedded objects |
| `meta:frame-count` | Number of frames |
| `meta:sentence-count` | Number of sentences |
| `meta:syllable-count` | Number of syllables |
| `meta:row-count` | Number of rows (spreadsheets) |

### `meta:user-defined` Value Types

| `meta:value-type` | Description |
| --- | --- |
| `string` (default) | Text string |
| `float` | Decimal number |
| `date` | ISO 8601 date |
| `time` | ISO 8601 time/duration |
| `boolean` | `true` or `false` |

---

## 5. RDF Metadata (ODF 1.2+)

ODF 1.2 introduced support for arbitrary RDF metadata using named graphs. This allows embedding structured metadata about document parts (paragraphs, sections, cells) beyond what the Dublin Core elements support.

### `META-INF/manifest.rdf`

The RDF manifest declares the document type and lists RDF files:

```xml
<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:odf="http://docs.oasis-open.org/ns/office/1.2/meta/odf#"
    xmlns:pkg="http://docs.oasis-open.org/ns/office/1.2/meta/pkg#">

  <!-- Declare the document itself -->
  <rdf:Description rdf:about="">
    <rdf:type rdf:resource="http://docs.oasis-open.org/ns/office/1.2/meta/odf#TextDocument"/>
  </rdf:Description>

  <!-- Reference to an additional RDF file -->
  <rdf:Description rdf:about="metadata/book-info.rdf">
    <rdf:type rdf:resource="http://docs.oasis-open.org/ns/office/1.2/meta/pkg#MetadataFile"/>
  </rdf:Description>

</rdf:RDF>
```

### Example Custom RDF File

```xml
<!-- metadata/book-info.rdf -->
<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:dc="http://purl.org/dc/elements/1.1/"
         xmlns:dcterms="http://purl.org/dc/terms/"
         xmlns:schema="http://schema.org/">

  <rdf:Description rdf:about="">
    <dc:title>My Document Title</dc:title>
    <dcterms:created rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">
      2024-01-10T09:00:00
    </dcterms:created>
    <dcterms:license rdf:resource="https://creativecommons.org/licenses/by/4.0/"/>
    <schema:author rdf:resource="https://example.com/person/jane-smith"/>
  </rdf:Description>

</rdf:RDF>
```

### In-Document RDF Annotations

ODF 1.2+ also supports inline RDF annotations on document elements using `xml:id` attributes:

```xml
<!-- content.xml -->
<text:p xml:id="para-intro" text:style-name="Text_20_Body">
  Introduction paragraph with semantic metadata.
</text:p>
```

The element `xml:id="para-intro"` allows external RDF to reference it:

```xml
<!-- In an .rdf file -->
<rdf:Description rdf:about="#para-intro">
  <dc:description>The introductory paragraph</dc:description>
</rdf:Description>
```

---

## 6. Reading Metadata Programmatically

### Python (odfpy)

```python
from odf.opendocument import load
from odf.namespaces import OFFICENS, DCNS, METANS

doc = load("document.odt")

# Access Dublin Core metadata
title = doc.meta.getElementsByType(
    type(None)  # use OdfElement
)

# Simpler approach via meta object
meta = doc.meta
for child in meta.childNodes:
    print(child.tagName, child.firstChild.data if child.firstChild else "")
```

### Python (odfdo)

```python
from odfdo import Document

doc = Document("document.odt")

# Access metadata
print(doc.meta.title)
print(doc.meta.creator)
print(doc.meta.creation_date)
print(doc.meta.keywords)
print(doc.meta.statistics)

# Modify metadata
doc.meta.title = "New Title"
doc.meta.keywords = ["keyword1", "keyword2"]
doc.save("modified.odt")
```

---

## 7. Metadata in Different File Types

| File Type | Metadata Location | Additional Notes |
| --- | --- | --- |
| `.odt`, `.odp`, `.ods` | `meta.xml` | Full metadata support |
| `.odg` | `meta.xml` | Drawing metadata |
| `.odf` | `meta.xml` | Formula metadata |
| `.odb` | `meta.xml` | Database metadata |
| Flat ODF (`.fodt`) | `<office:meta>` in single file | Same elements |

---

*Previous: [Styles & Formatting ←](./09-styles-formatting.md) | Next: [Security & Signatures →](./11-security-signatures.md)*
