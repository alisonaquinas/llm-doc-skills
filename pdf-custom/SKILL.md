---
name: pdf-custom
description: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
---

# PDF Processing Guide

## Intent Router

Load sections based on the task:
- **Extract text** → "Quick Start" + "pdfplumber - Text and Table Extraction" for layout-aware extraction
- **Merge/split/rotate PDFs** → "Command-Line Tools" for qpdf or "Python Libraries" for pypdf
- **Create PDF from scratch** → "reportlab - Create PDFs" section with canvas or Platypus examples
- **Fill PDF forms** → Read [FORMS.md](FORMS.md) for detailed form-filling patterns
- **Scanned PDF / OCR** → "Extract Text from Scanned PDFs" for pytesseract workflow
- **Advanced operations** → "Command-Line Tools" for qpdf, pdftk, or "Python Libraries" for pypdfium2

## Overview

This guide covers essential PDF processing operations using Python libraries and
command-line tools. For advanced features, JavaScript libraries, and detailed
examples, see [REFERENCE.md](REFERENCE.md). If you need to fill out a PDF form,
read [FORMS.md](FORMS.md) and follow its instructions.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF

```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata

```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages

```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables

```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction

```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

#### Subscripts and Superscripts

**IMPORTANT**: Never use Unicode subscript/superscript characters (₀₁₂₃₄₅₆₇₈₉, ⁰¹²³⁴⁵⁶⁷⁸⁹) in ReportLab PDFs. The built-in fonts do not include these glyphs, causing them to render as solid black boxes.

Instead, use ReportLab's XML markup tags in Paragraph objects:

```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# Subscripts: use <sub> tag
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])

# Superscripts: use <super> tag
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

For canvas-drawn text (not Paragraph objects), manually adjust font the size and position rather than using Unicode subscripts/superscripts.

## Command-Line Tools

### pdftotext (poppler-utils)

```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf

```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (if available)

```text
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

## Common Tasks

### Extract Text from Scanned PDFs

```text
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Add Watermark

```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images

```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf (see [FORMS.md](FORMS.md)) | See [FORMS.md](FORMS.md) |

## Next Steps

- For advanced pypdfium2 usage, see [REFERENCE.md](REFERENCE.md)
- For JavaScript libraries such as `pdf-lib`, see [REFERENCE.md](REFERENCE.md)
- If you need to fill out a PDF form, follow [FORMS.md](FORMS.md)
- For troubleshooting guides, see [REFERENCE.md](REFERENCE.md)

---

## API Reference

> Sources: [pypdf docs](https://pypdf.readthedocs.io/en/stable/), [pdfplumber GitHub](https://github.com/jsvine/pdfplumber), [ReportLab docs](https://docs.reportlab.com/)

### pypdf (version 6.x)

#### PdfReader

```python
from pypdf import PdfReader

reader = PdfReader("file.pdf")
reader = PdfReader("file.pdf", password="secret")  # Encrypted PDF
```

| Property / Method | Type / Returns | Notes |
|-------------------|---------------|-------|
| `.pages` | `list[PageObject]` | All pages |
| `.metadata` | `DocumentInformation` | Title, Author, Subject, Creator, etc. |
| `.outline` | `list` | Bookmarks/outline tree |
| `.named_destinations` | `dict` | Named navigation targets |
| `.get_num_pages()` | `int` | Total page count |
| `.get_page(page_number)` | `PageObject` | 0-indexed |
| `.get_fields()` | `dict \| None` | Form fields |
| `.is_encrypted` | `bool` | |
| `.decrypt(password)` | `int` | Returns 0 (fail), 1 (user), 2 (owner) |

#### PageObject

```text
page = reader.pages[0]
text = page.extract_text()
text = page.extract_text(extraction_mode="layout")  # Preserve layout
```

| Method | Parameters | Returns |
|--------|-----------|---------|
| `extract_text()` | `extraction_mode: str = "plain"`, `orientations: tuple = (0,90,180,270)` | `str` |
| `extract_xform_text()` | — | `str` |
| `merge_page(page2)` | `page2: PageObject` | `None` (modifies in-place) |
| `merge_transformed_page(page2, ctm)` | Transformation matrix | `None` |
| `rotate(angle)` | `angle: int` (90, 180, 270) | `PageObject` |
| `scale(sx, sy)` | `sx, sy: float` | `None` |
| `scale_by(factor)` | `factor: float` | `None` |
| `scale_to(width, height)` | pixels | `None` |
| `compress_content_streams()` | — | `None` |
| `transfer_rotation_to_content()` | — | `None` |

**Properties:** `.mediabox`, `.cropbox`, `.bleedbox`, `.trimbox`, `.artbox`, `.rotation`, `.images`, `.annotations`

#### PdfWriter

```python
from pypdf import PdfWriter

writer = PdfWriter()
writer.add_page(reader.pages[0])
writer.clone_reader_document_root(reader)   # Clone entire document

with open("output.pdf", "wb") as f:
    writer.write(f)
```

| Method | Parameters | Notes |
|--------|-----------|-------|
| `add_page(page)` | `PageObject` | Appends page |
| `insert_page(page, index)` | `PageObject`, `int` | Insert at position |
| `remove_page(page_index)` | `int` | |
| `add_blank_page(width, height)` | pts | |
| `clone_reader_document_root(reader)` | `PdfReader` | Full document clone |
| `append(fileobj, pages, import_outline)` | Path / Reader | Merge files |
| `encrypt(user_password, owner_password, use_128bit)` | `str`, `str`, `bool=True` | |
| `decrypt(password)` | `str` | |
| `add_bookmark(title, pagenum, parent)` | | Add outline entry |
| `add_annotation(page_number, annotation)` | | |
| `set_page_layout(layout)` | `"/SinglePage"` etc. | |
| `set_page_mode(mode)` | `"/UseOutlines"` etc. | |
| `add_metadata(infos)` | `dict` | Update metadata |
| `compress_identical_objects(remove_identicals, remove_orphans)` | `bool` | Reduce file size |

#### Transformation

```python
from pypdf import Transformation

op = Transformation().rotate(90).translate(tx=50, ty=100).scale(sx=0.5, sy=0.5)
page.add_transformation(op)
```

---

### pdfplumber

#### Opening and navigating

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    page = pdf.pages[0]
    text = page.extract_text()
```

`pdfplumber.open(path, password=None, laparams=None, unicode_norm=None, strict_metadata=False)`

#### PDF properties

| Property | Type | Notes |
|----------|------|-------|
| `.metadata` | `dict` | CreationDate, Producer, Title, Author, … |
| `.pages` | `list[Page]` | All pages |

#### Page properties

| Property | Type | Notes |
|----------|------|-------|
| `.page_number` | `int` | 1-based |
| `.width`, `.height` | `float` | Points |
| `.chars` | `list[dict]` | Character objects |
| `.lines` | `list[dict]` | Line objects |
| `.rects` | `list[dict]` | Rectangle objects |
| `.curves` | `list[dict]` | Curve objects |
| `.images` | `list[dict]` | Image objects |
| `.annots` | `list[dict]` | Annotations |
| `.hyperlinks` | `list[dict]` | Hyperlink annotations |
| `.edges` | `list[dict]` | All edges (from rects, curves, lines) |

#### Page methods

| Method | Parameters | Returns |
|--------|-----------|---------|
| `extract_text()` | `x_tolerance=3`, `y_tolerance=3`, `layout=False`, `x_density=7.25`, `y_density=13` | `str` |
| `extract_words()` | `x_tolerance=3`, `y_tolerance=3`, `keep_blank_chars=False`, `use_text_flow=False` | `list[dict]` |
| `extract_tables()` | `table_settings={}` | `list[list[list[str]]]` |
| `extract_table()` | `table_settings={}` | `list[list[str]]` (first table only) |
| `find_tables()` | `table_settings={}` | `list[Table]` |
| `crop(bbox)` | `(x0,top,x1,bottom)` | `Page` |
| `within_bbox(bbox)` | `(x0,top,x1,bottom)` | `Page` |
| `outside_bbox(bbox)` | `(x0,top,x1,bottom)` | `Page` |
| `filter(test_function)` | `callable` | `Page` |
| `to_image(resolution=72)` | `int` | `PageImage` |
| `close()` | — | Flush cache |

#### Character object fields

`text`, `fontname`, `size`, `x0`, `x1`, `y0`, `y1`, `top`, `bottom`, `width`, `height`, `upright`, `stroking_color`, `non_stroking_color`, `matrix`

#### Table settings (key options)

```text
table_settings = {
    "vertical_strategy": "lines",     # "lines", "lines_strict", "text", "explicit"
    "horizontal_strategy": "lines",   # same options
    "explicit_vertical_lines": [],    # x-coordinates
    "explicit_horizontal_lines": [],  # y-coordinates
    "snap_tolerance": 3,
    "join_tolerance": 3,
    "edge_min_length": 3,
    "min_words_vertical": 3,
    "min_words_horizontal": 1,
    "intersection_tolerance": 3,
    "text_tolerance": 3,
    "text_x_tolerance": 3,
    "text_y_tolerance": 3,
}
```

---

### ReportLab

#### Canvas (low-level drawing)

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm, mm

c = canvas.Canvas("output.pdf", pagesize=letter)
width, height = letter   # 612, 792 pts

# Coordinates: origin bottom-left, y increases upward
c.drawString(1*inch, 10*inch, "Hello")
c.drawRightString(7.5*inch, 10*inch, "Right-aligned")
c.drawCentredString(4.25*inch, 10*inch, "Centered")
c.showPage()   # Start new page
c.save()
```

| Canvas Method | Parameters | Notes |
|---------------|-----------|-------|
| `drawString(x,y,text)` | pts | Bottom-left origin |
| `drawRightString(x,y,text)` | pts | Right-aligned at x |
| `drawCentredString(x,y,text)` | pts | Centered at x |
| `setFont(name, size)` | `str`, `float` | e.g., `"Helvetica"`, `12` |
| `setFillColor(color)` | `Color` | `colors.red`, `HexColor("#FF0000")` |
| `setStrokeColor(color)` | `Color` | |
| `setLineWidth(width)` | `float` | pts |
| `line(x1,y1,x2,y2)` | pts | Draw line |
| `rect(x,y,width,height,fill,stroke)` | pts | `fill=0\|1`, `stroke=0\|1` |
| `circle(cx,cy,r)` | pts | |
| `ellipse(x1,y1,x2,y2)` | bounding box | |
| `drawImage(path,x,y,width,height)` | pts | |
| `beginPath()` / `moveTo()` / `lineTo()` / `curveTo()` / `closePath()` | | Path drawing |
| `translate(x,y)` | pts | Transform origin |
| `rotate(angle)` | degrees | |
| `saveState()` / `restoreState()` | | Push/pop graphics state |
| `showPage()` | | Finalize page |
| `save()` | | Write file |

**Built-in fonts:** Helvetica, Helvetica-Bold, Helvetica-Oblique, Helvetica-BoldOblique, Times-Roman, Times-Bold, Times-Italic, Times-BoldItalic, Courier, Courier-Bold, Courier-Oblique, Courier-BoldOblique, Symbol, ZapfDingbats

#### Platypus (high-level layout)

```python
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether,
    Table, TableStyle, Image, HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

doc = SimpleDocTemplate("report.pdf", pagesize=letter,
                         leftMargin=inch, rightMargin=inch,
                         topMargin=inch, bottomMargin=inch)
styles = getSampleStyleSheet()
story = []
story.append(Paragraph("Title", styles["Title"]))
story.append(Spacer(1, 0.2*inch))
story.append(PageBreak())
doc.build(story)
```

**Built-in styles:** `Normal`, `Title`, `Heading1`–`Heading6`, `BodyText`, `Italic`, `Bold`, `BulletList`, `Definition`, `Code`

#### ParagraphStyle options

```text
ParagraphStyle(
    name="MyStyle",
    fontName="Helvetica",
    fontSize=12,
    leading=14,           # Line height
    spaceBefore=6,        # pts before paragraph
    spaceAfter=6,
    leftIndent=0,
    rightIndent=0,
    firstLineIndent=0,
    alignment=TA_LEFT,
    textColor=colors.black,
    backColor=None,
    borderWidth=0,
    borderColor=None,
    borderPadding=0,
    borderRadius=None,
)
```

#### Platypus Table

```text
data = [["Header 1", "Header 2"], ["Row 1 Col 1", "Row 1 Col 2"]]
t = Table(data, colWidths=[3*inch, 3*inch], rowHeights=None)
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.grey),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 10),
    ("ALIGN",      (0,0), (-1,-1), "CENTER"),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.black),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.lightgrey]),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
```

TableStyle commands use `(col, row)` tuples; `-1` means last.

#### XML markup in Paragraphs

```python
# Bold, italic, color, links, sub/superscript
Paragraph("<b>Bold</b> and <i>italic</i>", styles["Normal"])
Paragraph('<font color="red" size="14">Red text</font>', styles["Normal"])
Paragraph('x<super>2</super> + H<sub>2</sub>O', styles["Normal"])
Paragraph('<a href="https://example.com">Link</a>', styles["Normal"])
```

---

### Command-Line Tools (qpdf, pdftk, pdftotext)

#### qpdf (recommended for merge/split/rotate)

```bash
# Merge multiple PDFs
qpdf --empty --pages file1.pdf file2.pdf file3.pdf -- merged.pdf

# Extract page range
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf

# Rotate specific pages (+90, +180, +270, -90, or absolute 0,90,180,270)
qpdf input.pdf output.pdf --rotate=+90:1          # Page 1 only
qpdf input.pdf output.pdf --rotate=90             # All pages

# Decrypt
qpdf --password=secret --decrypt encrypted.pdf out.pdf

# Linearize (optimize for web streaming)
qpdf --linearize input.pdf output.pdf

# Inspect PDF structure
qpdf --check input.pdf
qpdf --json input.pdf | jq .

# Split each page to separate file
qpdf --split-pages input.pdf page-%d.pdf
```

#### pdftk

```text
pdftk A=file1.pdf B=file2.pdf cat A B output merged.pdf
pdftk input.pdf burst output page_%04d.pdf
pdftk input.pdf rotate 1-endeast output rotated.pdf    # east=90°, west=270°, south=180°
pdftk input.pdf dump_data > metadata.txt
pdftk input.pdf update_info metadata.txt output updated.pdf
```

#### pdftotext (poppler)

```bash
pdftotext input.pdf                      # output to input.txt
pdftotext -layout input.pdf output.txt   # Preserve layout spacing
pdftotext -f 1 -l 5 input.pdf out.txt   # Pages 1-5 only
pdftotext -nopgbrk input.pdf out.txt    # No page break characters
pdftotext -enc UTF-8 input.pdf out.txt  # Force encoding
```

#### pdfimages (poppler)

```bash
pdfimages -j input.pdf prefix            # Extract as JPEG
pdfimages -png input.pdf prefix          # Extract as PNG
pdfimages -f 2 -l 4 input.pdf prefix    # Pages 2-4 only
pdfimages -list input.pdf               # List images without extracting
```

#### Page size reference

| Size | Width (pts) | Height (pts) |
|------|------------|-------------|
| US Letter | 612 | 792 |
| US Legal | 612 | 1008 |
| A4 | 595 | 842 |
| A3 | 842 | 1191 |
| Tabloid | 792 | 1224 |
