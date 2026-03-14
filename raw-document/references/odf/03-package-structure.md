# ODF Package Structure

> **Cross-references:** [Overview](./01-overview.md) | [Specification](./02-specification.md) | [XML Namespaces](./04-xml-namespaces.md) | [Metadata](./10-metadata.md)

---

## 1. Package Format Overview

An ODF file is a **ZIP archive** containing a collection of XML files and associated resources. This design is called an **ODF Package** and is specified in:

- ODF 1.2 Part 3: Packages
- ODF 1.3 Part 2: Packages

The ZIP format used is ZIP 2.0, allowing both deflate compression and store (no compression) methods.

---

## 2. Complete Package Contents

### Typical `.odt` (Text Document) Package

```text
myDocument.odt (ZIP archive)
├── mimetype                    ← MUST be first, uncompressed
├── META-INF/
│   ├── manifest.xml            ← Package manifest (REQUIRED)
│   └── manifest.rdf            ← RDF manifest (optional, ODF 1.2+)
├── content.xml                 ← Document content (REQUIRED)
├── styles.xml                  ← Styles definitions (REQUIRED)
├── meta.xml                    ← Document metadata (recommended)
├── settings.xml                ← Application settings (recommended)
├── Thumbnails/
│   └── thumbnail.png           ← Thumbnail image (optional)
├── Pictures/
│   ├── image1.png              ← Embedded images
│   └── image2.jpg
├── Object1/                    ← Embedded ODF objects
│   ├── content.xml
│   └── styles.xml
└── Configurations2/            ← UI configuration (LibreOffice extension)
    └── ...
```

### Typical `.ods` (Spreadsheet) Package

```text
mySpreadsheet.ods (ZIP archive)
├── mimetype
├── META-INF/
│   └── manifest.xml
├── content.xml
├── styles.xml
├── meta.xml
├── settings.xml
└── Charts/
    └── Chart1/
        ├── content.xml
        └── styles.xml
```

---

## 3. Core Files Description

### `mimetype` (REQUIRED)

- **Position**: MUST be the FIRST file in the ZIP archive
- **Compression**: MUST NOT be compressed (stored as-is)
- **Content**: Single line with the MIME type of the primary document, no trailing newline

```text
application/vnd.oasis.opendocument.text
```

This allows identification of the document type without parsing XML.

### `META-INF/manifest.xml` (REQUIRED)

The manifest is the "table of contents" for the package. It lists every file in the package with its media type and any encryption information.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest
    xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
    manifest:version="1.3">

  <manifest:file-entry
      manifest:full-path="/"
      manifest:version="1.3"
      manifest:media-type="application/vnd.oasis.opendocument.text"/>

  <manifest:file-entry
      manifest:full-path="content.xml"
      manifest:media-type="text/xml"/>

  <manifest:file-entry
      manifest:full-path="styles.xml"
      manifest:media-type="text/xml"/>

  <manifest:file-entry
      manifest:full-path="meta.xml"
      manifest:media-type="text/xml"/>

  <manifest:file-entry
      manifest:full-path="settings.xml"
      manifest:media-type="text/xml"/>

  <manifest:file-entry
      manifest:full-path="Pictures/image1.png"
      manifest:media-type="image/png"/>

</manifest:manifest>
```

### `content.xml` (REQUIRED)

Contains all document content. Root element: `<office:document-content>`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    ...
    office:version="1.3">

  <office:automatic-styles>
    <!-- Automatic (unnamed) styles referenced by content -->
  </office:automatic-styles>

  <office:body>
    <office:text>
      <!-- Actual document text content -->
    </office:text>
  </office:body>

</office:document-content>
```

### `styles.xml` (REQUIRED)

Contains named styles, page layouts, and master pages.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    ...
    office:version="1.3">

  <office:font-face-decls>
    <!-- Font declarations -->
  </office:font-face-decls>

  <office:styles>
    <!-- Named (user-visible) styles -->
  </office:styles>

  <office:automatic-styles>
    <!-- Automatic styles used by page layouts -->
  </office:automatic-styles>

  <office:master-styles>
    <!-- Master pages -->
  </office:master-styles>

</office:document-styles>
```

### `meta.xml` (Recommended)

Contains document metadata (Dublin Core + ODF-specific).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    office:version="1.3">

  <office:meta>
    <dc:title>Document Title</dc:title>
    <dc:creator>Author Name</dc:creator>
    <dc:description>Document description</dc:description>
    <dc:subject>Subject</dc:subject>
    <meta:creation-date>2024-01-15T10:30:00</meta:creation-date>
    <dc:date>2024-03-01T14:20:00</dc:date>
    <meta:editing-cycles>5</meta:editing-cycles>
    <meta:editing-duration>PT2H30M</meta:editing-duration>
    <meta:generator>LibreOffice/7.6.0</meta:generator>
    <meta:document-statistic meta:word-count="1250"
                              meta:paragraph-count="45"
                              meta:character-count="7800"/>
    <meta:keyword>keyword1</meta:keyword>
    <meta:keyword>keyword2</meta:keyword>
  </office:meta>

</office:document-meta>
```

### `settings.xml` (Recommended)

Contains application-specific settings (view, print, etc.).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<office:document-settings
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0"
    office:version="1.3">

  <office:settings>
    <config:config-item-set config:name="ooo:view-settings">
      <config:config-item config:name="ViewAreaTop"
                          config:type="int">0</config:config-item>
      <!-- ... more view settings ... -->
    </config:config-item-set>
  </office:settings>

</office:document-settings>
```

---

## 4. Single-Document XML Format ("Flat ODF")

ODF also supports a **single flat XML file** format (not zipped), used for simpler exchange or XSLT processing. These files use the extension `.fodt`, `.fods`, `.fodp`, `.fodg` and the root element `<office:document>`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<office:document
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    ...
    office:mimetype="application/vnd.oasis.opendocument.text"
    office:version="1.3">

  <office:meta>...</office:meta>
  <office:settings>...</office:settings>
  <office:scripts>...</office:scripts>
  <office:font-face-decls>...</office:font-face-decls>
  <office:styles>...</office:styles>
  <office:automatic-styles>...</office:automatic-styles>
  <office:master-styles>...</office:master-styles>
  <office:body>...</office:body>

</office:document>
```

---

## 5. Encryption in ODF Packages

ODF supports encrypting package content (ODF 1.2+). Encrypted files have encryption info in `manifest.xml`:

```xml
<manifest:file-entry manifest:full-path="content.xml"
                     manifest:media-type="text/xml">
  <manifest:encryption-data
      manifest:checksum-type="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0#sha256-1k"
      manifest:checksum="BASE64_CHECKSUM">
    <manifest:algorithm
        manifest:algorithm-name="http://www.w3.org/2001/04/xmlenc#aes256-cbc"
        manifest:initialisation-vector="BASE64_IV"/>
    <manifest:start-key-generation
        manifest:start-key-generation-name="http://www.w3.org/2000/09/xmldsig#sha256"
        manifest:key-size="32"/>
    <manifest:key-derivation
        manifest:key-derivation-name="PBKDF2"
        manifest:key-size="32"
        manifest:iteration-count="100000"
        manifest:salt="BASE64_SALT"/>
  </manifest:encryption-data>
</manifest:file-entry>
```

**ODF 1.3 adds OpenPGP encryption** as an alternative to password-based encryption:

```xml
<manifest:file-entry ...>
  <manifest:encryption-data>
    <manifest:encrypted-key>
      <!-- OpenPGP key data -->
    </manifest:encrypted-key>
  </manifest:encryption-data>
</manifest:file-entry>
```

**Important**: `META-INF/manifest.xml` itself MUST NOT be encrypted (it must be readable to discover the rest of the package).

---

## 6. Digital Signatures

ODF 1.2+ supports digital signatures stored in the package. Signature files are listed in `manifest.xml` and reside under `META-INF/`:

```text
META-INF/
├── manifest.xml
├── documentsignatures.xml    ← Document content signatures
└── macrosignatures.xml       ← Macro signatures
```

Signature format uses W3C XML Signature with optional XAdES extensions (ODF 1.3+). See [Security & Signatures](./11-security-signatures.md).

---

## 7. RDF Metadata (ODF 1.2+)

ODF 1.2 added support for RDF-based metadata using named graphs. The `manifest.rdf` file references additional `.rdf` files:

```xml
<!-- META-INF/manifest.rdf -->
<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="">
    <rdf:type rdf:resource="http://docs.oasis-open.org/ns/office/1.2/meta/odf#ContentFile"/>
  </rdf:Description>
  <rdf:Description rdf:about="content.xml">
    <rdf:type rdf:resource="http://docs.oasis-open.org/ns/office/1.2/meta/odf#ContentFile"/>
  </rdf:Description>
</rdf:RDF>
```

---

## 8. Embedded Objects

ODF supports embedding other ODF documents as objects within a document. Embedded objects reside in subdirectories:

```text
Object1/
├── content.xml     ← Embedded ODF content
├── styles.xml
└── meta.xml
```

In `content.xml`, an embedded object is referenced:

```xml
<draw:object draw:notify-on-update-of-ranges="" xlink:href="./Object1"
             xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
```

---

## 9. Package Requirements Summary

| Requirement | Mandatory |
| --- | --- |
| ZIP 2.0 compatible | MUST |
| `mimetype` as first uncompressed entry | MUST |
| `META-INF/manifest.xml` present | MUST |
| Manifest lists all files | MUST |
| `META-INF/manifest.xml` not encrypted | MUST |
| `content.xml` present | MUST (for document packages) |
| `styles.xml` present | SHOULD |
| `office:version` attribute | SHOULD (for version identification) |

---

*Previous: [Specification ←](./02-specification.md) | Next: [XML Namespaces →](./04-xml-namespaces.md)*
