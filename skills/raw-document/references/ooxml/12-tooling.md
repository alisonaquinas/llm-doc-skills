# OOXML Tooling and Libraries

> **Cross-references:** [Best Practices](./11-best-practices.md) | [Specification](./02-specification.md) | [ODF Tooling](../odf/13-tooling.md)

---

## 1. .NET / C# Libraries

### Open XML SDK (Microsoft)

**Purpose**: Official Microsoft SDK for OOXML manipulation
**Status**: Open source, actively maintained
**Package**: `DocumentFormat.OpenXml` (NuGet)
**Source**: <https://github.com/dotnet/Open-XML-SDK>
**Docs**: <https://learn.microsoft.com/en-us/office/open-xml/open-xml-sdk>

```bash
# Install via NuGet
dotnet add package DocumentFormat.OpenXml
```

#### Creating a DOCX

```csharp
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;

using (WordprocessingDocument doc =
    WordprocessingDocument.Create("output.docx", WordprocessingDocumentType.Document))
{
    // Add main document part
    MainDocumentPart mainPart = doc.AddMainDocumentPart();
    mainPart.Document = new Document();
    Body body = mainPart.Document.AppendChild(new Body());

    // Add a paragraph
    Paragraph para = body.AppendChild(new Paragraph());
    Run run = para.AppendChild(new Run());
    run.AppendChild(new Text("Hello, World!"));

    // Add heading
    Paragraph heading = new Paragraph(
        new ParagraphProperties(
            new ParagraphStyleId() { Val = "Heading1" }),
        new Run(new Text("Document Title")));
    body.PrependChild(heading);
}
```

#### Reading a DOCX

```csharp
using (WordprocessingDocument doc =
    WordprocessingDocument.Open("input.docx", false))
{
    MainDocumentPart mainPart = doc.MainDocumentPart;
    string text = mainPart.Document.Body.InnerText;

    // Get all paragraphs
    var paragraphs = mainPart.Document.Body
        .Descendants<Paragraph>();

    foreach (var para in paragraphs)
    {
        string styleId = para.ParagraphProperties?
            .ParagraphStyleId?.Val?.Value ?? "Normal";
        Console.WriteLine($"[{styleId}] {para.InnerText}");
    }
}
```

#### Creating an XLSX

```csharp
using DocumentFormat.OpenXml.Spreadsheet;

using (SpreadsheetDocument doc =
    SpreadsheetDocument.Create("output.xlsx", SpreadsheetDocumentType.Workbook))
{
    WorkbookPart workbookPart = doc.AddWorkbookPart();
    workbookPart.Workbook = new Workbook();

    WorksheetPart worksheetPart = workbookPart.AddNewPart<WorksheetPart>();
    worksheetPart.Worksheet = new Worksheet(new SheetData());

    Sheets sheets = workbookPart.Workbook.AppendChild(new Sheets());
    sheets.AppendChild(new Sheet()
    {
        Id = workbookPart.GetIdOfPart(worksheetPart),
        SheetId = 1,
        Name = "Sheet1"
    });

    // Add data
    SheetData sheetData = worksheetPart.Worksheet.GetFirstChild<SheetData>();
    Row row = new Row() { RowIndex = 1 };
    row.Append(new Cell()
    {
        CellReference = "A1",
        DataType = CellValues.String,
        CellValue = new CellValue("Hello XLSX")
    });
    sheetData.AppendChild(row);
}
```

### Open Xml PowerTools

**Purpose**: High-level operations on top of Open XML SDK
**Source**: <https://github.com/OfficeDev/Open-Xml-PowerTools>
**Capabilities**:

- Document assembly from templates
- Content comparison and diff
- Document splitting and merging
- WmlToHtmlConverter (DOCX → HTML)
- PresentationBuilder

```csharp
// Split a document at heading breaks
using (WordprocessingDocument source = WordprocessingDocument.Open("input.docx", false))
{
    var docs = DocumentBuilder.BuildDocument(new List<Source>
    {
        new Source(new WmlDocument("input.docx"), true)
    });
}
```

---

## 2. Python Libraries

### python-docx

**Purpose**: Create and modify `.docx` files
**Install**: `pip install python-docx`
**Source**: <https://github.com/python-openxml/python-docx>
**Docs**: <https://python-docx.readthedocs.io/>

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Create document
doc = Document()

# Add heading
doc.add_heading("My Document", level=1)

# Add paragraph with formatting
para = doc.add_paragraph()
run = para.add_run("Bold and colored text")
run.bold = True
run.font.color.rgb = RGBColor(0x2E, 0x74, 0xB5)
run.font.size = Pt(12)

# Add paragraph with alignment
para2 = doc.add_paragraph("Centered paragraph")
para2.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Add a table
table = doc.add_table(rows=3, cols=3)
table.style = 'Table Grid'
cell = table.rows[0].cells[0]
cell.text = 'Header A'

# Add image
doc.add_picture("image.png", width=Inches(4))

# Access custom XML (low-level)
doc.element  # returns lxml element

doc.save("output.docx")

# Read existing document
doc2 = Document("existing.docx")
for para in doc2.paragraphs:
    print(para.style.name, para.text)
```

### openpyxl

**Purpose**: Create, read, and modify `.xlsx` files
**Install**: `pip install openpyxl`
**Source**: <https://github.com/theorchard/openpyxl>
**Docs**: <https://openpyxl.readthedocs.io/>

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

# Create workbook
wb = Workbook()
ws = wb.active
ws.title = "Sales Data"

# Write headers with styling
headers = ["Product", "Q1", "Q2", "Q3", "Q4"]
for col, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill(fill_type="solid", fgColor="2E74B5")
    cell.alignment = Alignment(horizontal="center")

# Write data
data = [
    ["Widget A", 100, 120, 115, 130],
    ["Widget B", 80, 95, 110, 125],
]
for row_idx, row_data in enumerate(data, 2):
    for col_idx, value in enumerate(row_data, 1):
        ws.cell(row=row_idx, column=col_idx, value=value)

# Set column widths
ws.column_dimensions["A"].width = 20
for col in range(2, 6):
    ws.column_dimensions[get_column_letter(col)].width = 12

# Add formula
ws["F1"] = "Total"
ws["F2"] = "=SUM(B2:E2)"
ws["F3"] = "=SUM(B3:E3)"

# Add chart
chart = BarChart()
chart.title = "Quarterly Sales"
chart.type = "col"
data_ref = Reference(ws, min_col=2, max_col=5, min_row=1, max_row=3)
chart.add_data(data_ref, titles_from_data=True)
cats = Reference(ws, min_col=1, min_row=2, max_row=3)
chart.set_categories(cats)
ws.add_chart(chart, "H1")

wb.save("output.xlsx")

# Read existing file
wb2 = load_workbook("input.xlsx", data_only=True)  # data_only=True reads cached values
ws2 = wb2.active
for row in ws2.iter_rows(min_row=2, values_only=True):
    print(row)
```

### python-pptx

**Purpose**: Create and modify `.pptx` files
**Install**: `pip install python-pptx`
**Source**: <https://github.com/python-openxml/python-pptx>
**Docs**: <https://python-pptx.readthedocs.io/>

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Create presentation
prs = Presentation()

# Use built-in slide layout 1 (Title and Content)
slide_layout = prs.slide_layouts[1]
slide = prs.slides.add_slide(slide_layout)

# Set title and content
title = slide.shapes.title
title.text = "Slide Title"

body = slide.placeholders[1]
tf = body.text_frame
tf.text = "First bullet point"
tf.add_paragraph().text = "Second bullet point"

# Add a slide with custom shapes
blank_layout = prs.slide_layouts[6]  # blank
slide2 = prs.slides.add_slide(blank_layout)

# Add shape
from pptx.enum.shapes import MSO_SHAPE_TYPE
txBox = slide2.shapes.add_textbox(Inches(1), Inches(1), Inches(4), Inches(2))
tf = txBox.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "Text box content"
run.font.size = Pt(24)
run.font.bold = True
run.font.color.rgb = RGBColor(0x2E, 0x74, 0xB5)

# Add image
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
pic = slide3.shapes.add_picture("photo.jpg", Inches(1), Inches(1),
                                 width=Inches(4))

# Add table
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
table = slide4.shapes.add_table(3, 4, Inches(1), Inches(1),
                                  Inches(8), Inches(3)).table
table.cell(0, 0).text = "Header"

# Set slide size (16:9)
prs.slide_width = Emu(9144000)
prs.slide_height = Emu(5143500)

prs.save("output.pptx")
```

---

## 3. JavaScript / Node.js Libraries

### docx (npm)

**Purpose**: Create `.docx` files in Node.js and browser
**Install**: `npm install docx`
**Source**: <https://github.com/dolanmiu/docx>

```javascript
const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require("docx");
const fs = require("fs");

const doc = new Document({
  sections: [{
    children: [
      new Paragraph({
        text: "My Document Title",
        heading: HeadingLevel.HEADING_1,
      }),
      new Paragraph({
        children: [
          new TextRun("Normal text with "),
          new TextRun({
            text: "bold text",
            bold: true,
          }),
        ],
      }),
    ],
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync("output.docx", buffer);
});
```

### xlsx (SheetJS)

**Purpose**: Parse and write Excel files in JavaScript
**Install**: `npm install xlsx`
**Source**: <https://github.com/SheetJS/sheetjs>
**Docs**: <https://docs.sheetjs.com/>

```javascript
const XLSX = require("xlsx");

// Read
const wb = XLSX.readFile("input.xlsx");
const ws = wb.Sheets[wb.SheetNames[0]];
const data = XLSX.utils.sheet_to_json(ws);

// Write
const newWb = XLSX.utils.book_new();
const newWs = XLSX.utils.json_to_sheet([
  { Name: "Alice", Score: 95 },
  { Name: "Bob", Score: 87 },
]);
XLSX.utils.book_append_sheet(newWb, newWs, "Results");
XLSX.writeFile(newWb, "output.xlsx");
```

### PptxGenJS

**Purpose**: Create `.pptx` files in Node.js and browser
**Install**: `npm install pptxgenjs`
**Source**: <https://github.com/gitbrent/PptxGenJS>

```javascript
const PptxGenJS = require("pptxgenjs");

const pres = new PptxGenJS();
const slide = pres.addSlide();

slide.addText("Hello World!", {
  x: 1, y: 1, w: 8, h: 1.5,
  fontSize: 36,
  bold: true,
  color: "363636",
});

slide.addImage({ path: "photo.png", x: 1, y: 2, w: 4, h: 3 });

pres.writeFile({ fileName: "output.pptx" });
```

---

## 4. Java Libraries

### Apache POI

**Purpose**: Full Java OOXML/ODF implementation
**Status**: Apache Software Foundation, widely used
**Maven**:

```xml
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi-ooxml</artifactId>
    <version>5.2.5</version>
</dependency>
```

```java
import org.apache.poi.xwpf.usermodel.*;
import org.apache.poi.xssf.usermodel.*;
import org.apache.poi.xslf.usermodel.*;

// Create DOCX
XWPFDocument doc = new XWPFDocument();
XWPFParagraph para = doc.createParagraph();
XWPFRun run = para.createRun();
run.setText("Hello from Apache POI!");
run.setBold(true);
run.setFontSize(12);

try (FileOutputStream out = new FileOutputStream("output.docx")) {
    doc.write(out);
}

// Create XLSX
XSSFWorkbook wb = new XSSFWorkbook();
XSSFSheet sheet = wb.createSheet("Sheet1");
XSSFRow row = sheet.createRow(0);
XSSFCell cell = row.createCell(0);
cell.setCellValue("Hello Excel");

XSSFCellStyle style = wb.createCellStyle();
XSSFFont font = wb.createFont();
font.setBold(true);
style.setFont(font);
cell.setCellStyle(style);

try (FileOutputStream out = new FileOutputStream("output.xlsx")) {
    wb.write(out);
}
```

---

## 5. Inspection and Debugging Tools

### OOXML Viewer (VS Code Extension)

- **Install**: Search "OOXML Viewer" in VS Code Extensions
- Opens OOXML packages as expandable tree
- View and edit XML parts directly
- See raw relationship graphs

### DocxToSource (OfficeDev)

Replacement for the OpenXML SDK Productivity Tool:

- **URL**: <https://github.com/OfficeDev/Open-Xml-PowerTools/tree/vNext/DocxToSource>
- Generates Open XML SDK C# code from a document
- Useful for reverse-engineering existing documents

### Unzip and Inspect

```bash
# Quick inspection on command line
unzip -p document.docx word/document.xml | xmllint --format -

# Extract all files
mkdir extracted && cp document.docx extracted/document.zip
cd extracted && unzip document.zip

# Pretty-print any XML part
cat word/styles.xml | python3 -m json.tool --no-ensure-ascii  # if JSON
xmllint --format word/styles.xml
```

---

## 6. Key Resources

| Resource | URL |
| --- | --- |
| Open XML SDK (GitHub) | <https://github.com/dotnet/Open-XML-SDK> |
| Open XML SDK Docs | <https://learn.microsoft.com/en-us/office/open-xml/> |
| python-docx | <https://python-docx.readthedocs.io/> |
| openpyxl | <https://openpyxl.readthedocs.io/> |
| python-pptx | <https://python-pptx.readthedocs.io/> |
| Apache POI | <https://poi.apache.org/> |
| officeopenxml.com (reference) | <http://officeopenxml.com/> |
| ECMA-376 (5th ed.) | <https://ecma-international.org/publications-and-standards/standards/ecma-376/> |
| ooxml.info | <https://ooxml.info/docs/> |

---

*Previous: [Best Practices ←](./11-best-practices.md) | [Back to OOXML Index →](../README.md#ooxml)*
