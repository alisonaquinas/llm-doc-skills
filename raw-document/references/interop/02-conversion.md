# ODF ↔ OOXML Conversion

> **Cross-references:** [Comparison](./01-comparison.md) | [Feature Mapping](./03-feature-mapping.md) | [ODF Best Practices](../odf/12-best-practices.md) | [OOXML Best Practices](../ooxml/11-best-practices.md)

---

## 1. Overview

Converting between ODF and OOXML is inherently lossy at the edges because the two formats have different models for several features. ISO/IEC TR 29166:2011 formally documents the challenges.

Key principle: **No conversion tool achieves 100% fidelity across all features.** Plan for review after any automated conversion.

---

## 2. Conversion Tools

### LibreOffice (Best Open-Source Option)

LibreOffice provides the highest-quality open-source ODF↔OOXML conversion.

**Command-line conversion:**

```bash
# OOXML → ODF
libreoffice --headless --convert-to odt --outdir /output/ document.docx
libreoffice --headless --convert-to ods --outdir /output/ spreadsheet.xlsx
libreoffice --headless --convert-to odp --outdir /output/ presentation.pptx

# ODF → OOXML
libreoffice --headless --convert-to docx --outdir /output/ document.odt
libreoffice --headless --convert-to xlsx --outdir /output/ spreadsheet.ods
libreoffice --headless --convert-to pptx --outdir /output/ presentation.odp

# Batch conversion
libreoffice --headless --convert-to docx --outdir /output/ *.odt

# Convert to PDF
libreoffice --headless --convert-to pdf document.odt
```

**Python wrapper:**

```python
import subprocess
from pathlib import Path

def convert_document(input_path: str, output_format: str, output_dir: str) -> str:
    """
    Convert using LibreOffice headless.
    output_format: 'odt', 'docx', 'ods', 'xlsx', 'odp', 'pptx', 'pdf'
    """
    result = subprocess.run([
        "libreoffice",
        "--headless",
        "--norestore",
        "--convert-to", output_format,
        "--outdir", output_dir,
        input_path
    ], capture_output=True, text=True, timeout=60)

    if result.returncode != 0:
        raise RuntimeError(f"Conversion failed: {result.stderr}")

    input_stem = Path(input_path).stem
    return str(Path(output_dir) / f"{input_stem}.{output_format}")
```

**Python with PyUNO (more control):**

```python
import subprocess
import os

def libreoffice_convert(input_path, output_format, output_dir):
    """Requires LibreOffice installed."""
    cmd = [
        "soffice",
        "--headless",
        "--invisible",
        "--nofirststartwizard",
        "--convert-to", output_format,
        "--outdir", output_dir,
        input_path
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode == 0
```

### Pandoc

Pandoc converts via its internal AST (abstract syntax tree). Good for text-heavy documents.

```bash
# DOCX → ODT
pandoc -f docx -t odt -o output.odt input.docx

# ODT → DOCX
pandoc -f odt -t docx -o output.docx input.odt

# With reference document (use a template for formatting)
pandoc -f odt -t docx --reference-doc=template.docx -o output.docx input.odt

# ODT → Markdown (useful for content extraction)
pandoc -f odt -t markdown -o output.md input.odt

# DOCX → HTML
pandoc -f docx -t html -o output.html input.docx
```

Pandoc limitations:

- Complex table layouts may degrade
- Custom styles are mapped to best-effort equivalents
- Charts and drawings are not converted (images extracted as-is)

### Microsoft Office (Best Fidelity for OOXML)

Microsoft Office provides the highest fidelity for OOXML → ODF and ODF → OOXML, especially for Word/Excel features:

- **Office 2010+**: File > Save As > ODF
- **Office 2013+**: Better ODF 1.1/1.2 support
- **Office 365**: ODF 1.1 and early ODF 1.4 support

Via COM Automation (Windows only):

```python
import win32com.client as win32

def word_convert_to_odt(input_docx, output_odt):
    word = win32.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(input_docx)
        # WdSaveFormat: wdFormatOpenDocumentText = 23
        doc.SaveAs2(output_odt, FileFormat=23)
        doc.Close()
    finally:
        word.Quit()
```

### ONLYOFFICE Document Server

ONLYOFFICE provides API-based conversion:

```bash
# Via ONLYOFFICE Conversion API (self-hosted or cloud)
curl -X POST "https://your-server/converter" \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://example.com/document.docx",
       "outputtype": "odt",
       "filetype": "docx"
     }'
```

---

## 3. Conversion Quality by Feature

### Text Documents (DOCX ↔ ODT)

| Feature | LibreOffice | Pandoc | MS Office | Notes |
| --- | --- | --- | --- | --- |
| Plain text | ✅ Excellent | ✅ Excellent | ✅ Excellent | |
| Headings | ✅ Excellent | ✅ Good | ✅ Excellent | |
| Character styles | ✅ Good | ⚠️ Partial | ✅ Good | |
| Paragraph styles | ✅ Good | ⚠️ Partial | ✅ Good | |
| Tables | ✅ Good | ⚠️ Partial | ✅ Excellent | |
| Numbered lists | ✅ Good | ✅ Good | ✅ Good | |
| Bullet lists | ✅ Good | ✅ Good | ✅ Good | |
| Images (embedded) | ✅ Excellent | ✅ Good | ✅ Excellent | |
| Footnotes/endnotes | ✅ Excellent | ✅ Good | ✅ Excellent | |
| Comments | ✅ Good | ⚠️ Partial | ✅ Good | |
| Track changes | ⚠️ Partial | ❌ Lost | ✅ Good | |
| Headers/footers | ✅ Good | ⚠️ Partial | ✅ Good | |
| Page breaks/sections | ⚠️ Partial | ⚠️ Partial | ✅ Good | |
| Fields/dynamic | ⚠️ Partial | ❌ Flattened | ✅ Good | |
| Content controls (SDTs) | ❌ Lost | ❌ Lost | ⚠️ Partial | |
| Complex page layout | ⚠️ Partial | ❌ Lost | ✅ Good | |
| Embedded objects | ⚠️ Partial | ❌ Lost | ⚠️ Partial | |
| Macros | ❌ Lost | ❌ Lost | ❌ Lost | |

### Spreadsheets (XLSX ↔ ODS)

| Feature | LibreOffice | Notes |
| --- | --- | --- |
| Cell values | ✅ Excellent | |
| Basic formulas | ✅ Excellent | |
| Complex formulas | ✅ Good | Minor syntax differences |
| Cell formatting | ✅ Good | |
| Named ranges | ✅ Good | |
| Charts | ✅ Good | Some chart types may change |
| Pivot tables | ⚠️ Partial | Model differences |
| Data validation | ✅ Good | |
| Conditional formatting | ⚠️ Partial | Some rules may not map |
| Macros (VBA/Basic) | ❌ Lost | Completely different languages |
| Tables (named) | ⚠️ Partial | ODS doesn't have same concept |
| Custom number formats | ✅ Good | |
| Array formulas | ✅ Good | |

### Presentations (PPTX ↔ ODP)

| Feature | LibreOffice | Notes |
| --- | --- | --- |
| Slide content | ✅ Good | |
| Text formatting | ✅ Good | |
| Backgrounds | ✅ Good | |
| Images | ✅ Excellent | |
| Shapes | ✅ Good | Some preset shapes may differ |
| Transitions | ⚠️ Partial | Many transitions map, some don't |
| Animations | ⚠️ Partial | Complex animations may simplify |
| Charts | ✅ Good | |
| SmartArt | ❌ Becomes image | ODP has no SmartArt equivalent |
| Slide masters | ⚠️ Partial | Layout details may change |
| Speaker notes | ✅ Good | |
| Embedded videos | ⚠️ Partial | Format and codec dependency |
| Theme colors | ⚠️ Partial | ODF lacks full theme system |

---

## 4. ISO/IEC TR 29166 — Translation Guidelines

ISO/IEC TR 29166:2011 is the international technical report on ODF ↔ OOXML translation. It defines a three-level translatability rating:

| Level | Meaning |
| --- | --- |
| **High** | Feature maps reliably; conversion is lossless or near-lossless |
| **Medium** | Feature maps with some information loss or structural change |
| **Low** | Feature has no direct counterpart; significant loss expected |

Key low-translatability areas identified by TR 29166:

- ODF change tracking ↔ OOXML revision marks
- ODF RDF metadata ↔ OOXML custom XML
- ODF text sections with complex column layouts ↔ OOXML sections
- OOXML table conditional formatting ↔ ODF table styles
- OOXML SmartArt ↔ ODF drawing objects
- OOXML content controls (SDT) ↔ ODF user fields

---

## 5. Batch Conversion Strategies

### Quality-First Approach (Recommended)

```python
import subprocess
import os
from pathlib import Path
from typing import Optional

def convert_directory(
    input_dir: str,
    output_dir: str,
    input_ext: str,
    output_format: str
) -> dict:
    """
    Batch convert all files with input_ext in input_dir.
    Returns dict of {filename: 'success'|'error'}.
    """
    results = {}
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    files = list(input_path.glob(f"*.{input_ext}"))
    print(f"Converting {len(files)} files...")

    for file in files:
        try:
            result = subprocess.run([
                "libreoffice",
                "--headless",
                "--norestore",
                "--convert-to", output_format,
                "--outdir", str(output_path),
                str(file)
            ], capture_output=True, text=True, timeout=120)

            if result.returncode == 0:
                results[file.name] = "success"
            else:
                results[file.name] = f"error: {result.stderr}"

        except subprocess.TimeoutExpired:
            results[file.name] = "error: timeout"
        except Exception as e:
            results[file.name] = f"error: {e}"

    return results
```

### Round-Trip Validation

For critical conversions, validate the round-trip:

```python
from pathlib import Path
import hashlib

def round_trip_test(original_odt: str, work_dir: str) -> dict:
    """
    Convert ODT → DOCX → ODT and compare.
    Returns comparison metrics.
    """
    import subprocess

    work = Path(work_dir)
    orig = Path(original_odt)

    # Step 1: ODT → DOCX
    subprocess.run(["libreoffice", "--headless", "--convert-to", "docx",
                    "--outdir", str(work), str(orig)], check=True)

    docx_path = work / (orig.stem + ".docx")

    # Step 2: DOCX → ODT
    subprocess.run(["libreoffice", "--headless", "--convert-to", "odt",
                    "--outdir", str(work), str(docx_path)], check=True)

    round_trip_path = work / (orig.stem + ".odt")

    # Compare file sizes (rough proxy for content preservation)
    orig_size = orig.stat().st_size
    rt_size = round_trip_path.stat().st_size

    return {
        "original_size": orig_size,
        "round_trip_size": rt_size,
        "size_ratio": rt_size / orig_size,
        "intermediate": str(docx_path),
        "round_trip": str(round_trip_path)
    }
```

---

## 6. Known Conversion Problem Areas

### Style Name Mapping

ODF and OOXML use different style naming conventions. LibreOffice maintains a mapping table:

| ODF Style | OOXML Style |
| --- | --- |
| `Heading 1` | `heading 1` (styleId: `Heading1`) |
| `Default Paragraph Style` | `Normal` |
| `Text Body` | `Body Text` |
| `List Number` | `List Number` |
| `List Bullet` | `List Bullet` |
| `Caption` | `Caption` |
| `Footnote Text` | `footnote text` |

### Measurement Conversion

ODF → OOXML requires converting units:

```python
# ODF uses CSS units (mm, cm, in, pt)
# OOXML uses twips (word) or EMU (DrawingML)

def cm_to_twips(cm: float) -> int:
    return round(cm * 567)       # 1 cm = 567.0 twips

def pt_to_twips(pt: float) -> int:
    return round(pt * 20)        # 1 pt = 20 twips

def cm_to_emu(cm: float) -> int:
    return round(cm * 360000)    # 1 cm = 360,000 EMU

def in_to_emu(inches: float) -> int:
    return round(inches * 914400) # 1 inch = 914,400 EMU
```

---

## 7. PDF Export (Common Neutral Format)

For situations where cross-format fidelity is critical, exporting to PDF via LibreOffice ensures consistent rendering regardless of the receiving application:

```bash
# High-quality PDF export
libreoffice --headless --convert-to pdf:writer_pdf_Export \
  --infilter='writer_pdf_Export:{"ReduceImageResolution":{"type":"boolean","value":"false"}}' \
  document.odt

# Tagged PDF (for accessibility)
libreoffice --headless \
  --convert-to "pdf:writer_pdf_Export:EmbedStandardFonts=true;UseTaggedPDF=true" \
  document.odt
```

---

*Previous: [Comparison ←](./01-comparison.md) | Next: [Feature Mapping →](./03-feature-mapping.md)*
