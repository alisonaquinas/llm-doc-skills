# ODF Tooling and Libraries

> **Cross-references:** [Best Practices](./12-best-practices.md) | [Specification](./02-specification.md) | [OOXML Tooling](../ooxml/12-tooling.md)

---

## 1. Python Libraries

### odfpy

**Purpose**: Create and manipulate ODF 1.2 documents
**Status**: Stable, actively maintained
**Install**: `pip install odfpy`
**Source**: <https://github.com/eea/odfpy>

```python
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import P, H, Span

doc = OpenDocumentText()

# Define a style
style = Style(name="MyBold", family="text")
style.addElement(TextProperties(fontweight="bold"))
doc.styles.addElement(style)

# Add content
h = H(outlinelevel=1, text="Main Heading")
doc.text.addElement(h)

p = P(text="This is ")
s = Span(stylename=style, text="bold")
p.addElement(s)
p.addText(" text.")
doc.text.addElement(p)

doc.save("output.odt")
```

**Capabilities:**

- Create `.odt`, `.ods`, `.odp`, `.odg`, `.odc`, `.odf`, `.odb`
- Add styles, content, images, tables
- Read/parse existing ODF documents
- Schema validation on element insertion

---

### odfdo

**Purpose**: Modern Python ODF library with high-level API
**Status**: Actively maintained
**Install**: `pip install odfdo`
**Source**: <https://github.com/jdum/odfdo>
**Docs**: <https://jdum.github.io/odfdo/>

```python
from odfdo import Document, Paragraph, Header, Span, Table, Row, Cell

# Create text document
doc = Document("odt")
body = doc.body

# Add heading
body.append(Header(1, "My Document Title"))

# Add paragraph with mixed content
para = Paragraph()
para.append("Normal text, then ")
span = Span(style="Strong Emphasis", text="strong text")
para.append(span)
para.append(", then normal again.")
body.append(para)

# Add a table
table = Table("MyTable")
row = Row()
row.append(Cell("Header 1"))
row.append(Cell("Header 2"))
table.append(row)
row2 = Row()
row2.append(Cell("Value 1"))
row2.append(Cell(42))
table.append(row2)
body.append(table)

doc.save("output.odt")

# Read and modify existing document
doc2 = Document("existing.odt")
print(doc2.meta.title)
print(doc2.meta.creator)
paragraphs = doc2.body.paragraphs
for p in paragraphs:
    print(p.text_content)
```

**Capabilities:**

- High-level document creation API
- Read/modify metadata
- Table, list, heading, paragraph creation
- Image insertion
- Spreadsheet cell manipulation
- Presentation slide creation
- Section and header/footer management
- Command-line utilities included

---

### python-odf (alternatives summary)

| Library | API Level | ODF Version | Activity |
| --- | --- | --- | --- |
| `odfpy` | Low-level XML | 1.2 | Active |
| `odfdo` | High-level | 1.2/1.3 | Active |
| `relatorio` | Template-based | 1.2 | Maintenance |

---

## 2. Java Libraries

### ODF Toolkit (odftoolkit)

**Purpose**: Comprehensive Java ODF library with low and high-level APIs
**Status**: Apache Software Foundation project
**Website**: <https://odftoolkit.org/>
**Maven**:

```xml
<dependency>
    <groupId>org.odftoolkit</groupId>
    <artifactId>odfdom-java</artifactId>
    <version>0.12.0</version>
</dependency>
```

**Modules:**

- `odfdom` — Low-level DOM access to ODF elements
- `simple-odf` — High-level document creation API
- `taglets` — Documentation tools
- `xslt-runner` — XSLT processing for ODF

**Example (odfdom):**

```java
import org.odftoolkit.odfdom.doc.OdfTextDocument;
import org.odftoolkit.odfdom.dom.element.text.TextPElement;
import org.odftoolkit.odfdom.dom.element.text.TextHElement;

OdfTextDocument doc = OdfTextDocument.newTextDocument();
OdfContentDom contentDom = doc.getContentDom();

// Add heading
TextHElement heading = contentDom.newOdfElement(TextHElement.class);
heading.setTextOutlineLevelAttribute(1);
heading.setTextContent("My Heading");
doc.getText().appendChild(heading);

// Add paragraph
TextPElement para = contentDom.newOdfElement(TextPElement.class);
para.setTextContent("Paragraph text here.");
doc.getText().appendChild(para);

doc.save("output.odt");
```

**Example (simple-odf):**

```java
import org.odftoolkit.simple.TextDocument;
import org.odftoolkit.simple.text.Paragraph;
import org.odftoolkit.simple.table.Table;

TextDocument doc = TextDocument.newTextDocument();

// Add heading
Paragraph h = doc.addParagraph("Chapter One");
h.applyHeading(true, 1);

// Add paragraph
doc.addParagraph("Content text here.");

// Add table
Table table = doc.addTable(3, 4);  // 3 rows, 4 columns
table.getCellByPosition(0, 0).setStringValue("Cell A1");

doc.save("output.odt");
```

---

### lpod-java

**Purpose**: Lightweight Java ODF library
**Note**: Less actively maintained; prefer odftoolkit for new projects

---

## 3. JavaScript/Node.js Libraries

### odfkit (various npm packages)

Several npm packages handle ODF documents with varying levels of support:

```bash
npm install odfkit         # ODF document creation
npm install odt2html       # ODT to HTML conversion
```

**Note**: The JavaScript ODF ecosystem is less mature than Python or Java. For production use, consider server-side LibreOffice conversion (see below).

---

## 4. Perl Libraries

### ODF::lpOD

**Purpose**: Full-featured Perl ODF library
**Install**: `cpan ODF::lpOD`
**Docs**: <https://metacpan.org/pod/ODF::lpOD>

```perl
use ODF::lpOD;

my $doc = odf_new_document('text');
my $body = $doc->get_body;

# Add heading
my $h = odf_create_heading(level => 1, text => "Title");
$body->append_element($h);

# Add paragraph
my $p = odf_create_paragraph(
    text  => "Some content",
    style => "Text_Body"
);
$body->append_element($p);

$doc->save("output.odt");
```

---

## 5. Server-Side Conversion with LibreOffice

LibreOffice can run in headless mode to convert documents and generate ODF from templates:

### Document Conversion

```bash
# Convert OOXML to ODF
libreoffice --headless --convert-to odt --outdir /output/ input.docx

# Convert ODF to PDF
libreoffice --headless --convert-to pdf --outdir /output/ input.odt

# Convert multiple files
libreoffice --headless --convert-to ods --outdir /output/ *.xlsx
```

### Using LibreOffice via Python (subprocess)

```python
import subprocess
import os

def convert_to_odt(input_path: str, output_dir: str) -> str:
    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "odt",
        "--outdir", output_dir,
        input_path
    ], check=True, capture_output=True)

    base = os.path.splitext(os.path.basename(input_path))[0]
    return os.path.join(output_dir, base + ".odt")
```

### LibreOffice Macro API (UNO)

For complex programmatic document manipulation, use the LibreOffice UNO API:

```python
# Using python-uno bridge
import uno
from com.sun.star.beans import PropertyValue

def create_connection():
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", localContext)
    ctx = resolver.resolve(
        "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    return ctx
```

Start LibreOffice with UNO server:

```bash
libreoffice --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
```

---

## 6. Validation Tools

### ODF Validator (Online)

- **URL**: <https://odfvalidator.org/>
- Validates against ODF 1.0–1.3 schemas
- Can validate entire ZIP packages
- Provides detailed error messages with element paths

### Command-Line Validation

```bash
# Using jing (RELAX NG validator)
java -jar jing.jar \
  OpenDocument-v1.3-schema.rng \
  MyDocument.fodt

# Using xmllint (libxml2)
xmllint --relaxng OpenDocument-v1.3-schema.rng \
        --noout MyDocument.fodt
```

### odfpy Validation

odfpy validates as you build the document, raising exceptions for invalid elements.

---

## 7. XSLT and XML Processing

ODF's flat XML format (`.fodt`, `.fods`) is ideal for XSLT processing:

```xml
<!-- Extract all headings from an ODF document -->
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">

  <xsl:template match="text:h">
    <heading level="{@text:outline-level}">
      <xsl:value-of select="."/>
    </heading>
  </xsl:template>

</xsl:stylesheet>
```

Apply:

```bash
xsltproc extract-headings.xsl MyDocument.fodt > headings.xml
```

---

## 8. IDE and Editor Support

| Tool | ODF Support |
| --- | --- |
| LibreOffice | Native editor (primary reference implementation) |
| Apache OpenOffice | Native editor |
| ONLYOFFICE Desktop | Native editor |
| VS Code (extensions) | XML editing for flat ODF; zip viewer extensions |
| odfvalidator.org | Web-based validation |
| Oxygen XML Editor | Full XML editing with schema validation |

---

## 9. Key Resources

| Resource | URL |
| --- | --- |
| ODF Toolkit (Java) | <https://odftoolkit.org/> |
| odfpy (Python) | <https://github.com/eea/odfpy> |
| odfdo (Python) | <https://github.com/jdum/odfdo> |
| ODF Validator | <https://odfvalidator.org/> |
| LibreOffice SDK | <https://api.libreoffice.org/> |
| OASIS ODF TC | <https://www.oasis-open.org/committees/office> |
| Document Foundation Wiki | <https://wiki.documentfoundation.org/> |
| ODF generation tools list | <https://wiki.documentfoundation.org/Documentation/ODF_documents_generation_tools/en> |

---

*Previous: [Best Practices ←](./12-best-practices.md) | [Back to ODF Index →](../README.md#odf)*
