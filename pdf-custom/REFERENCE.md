# PDF Reference

This reference collects the advanced PDF patterns that sit behind the quick
guide in [SKILL.md](SKILL.md).

## Tool selection

| Task | Best starting point | Why |
| --- | --- | --- |
| Merge, split, rotate, encrypt | `pypdf` or `qpdf` | Stable and predictable for document-level changes |
| Text and table extraction | `pdfplumber` | Layout-aware extraction |
| Render pages to images | Poppler tools | Good for QA and OCR staging |
| Create new PDFs | `reportlab` | Reliable programmatic generation |
| Fill AcroForms | `pypdf` or `pdf-lib` | Works with common field-based forms |
| OCR scanned PDFs | `ocrmypdf` or `pytesseract` pipeline | Needed when no text layer exists |

## High-value command patterns

```bash
# Merge files
qpdf --empty --pages part1.pdf part2.pdf -- merged.pdf

# Decrypt a file when you have the password
qpdf --password='secret' --decrypt locked.pdf unlocked.pdf

# Inspect metadata quickly
pdfinfo document.pdf

# Render pages for QA
pdftoppm -jpeg -r 150 document.pdf page
```

## Advanced `pypdf` notes

- Use `PdfReader` and `PdfWriter` for most structural changes.
- Prefer page-level operations when reordering or watermarking files.
- Always write to a new output file first, then replace the original only after
  verification.

Example watermark flow:

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("document.pdf")
watermark = PdfReader("watermark.pdf").pages[0]
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as handle:
    writer.write(handle)
```

## Extraction tips

- Use `pdftotext -layout` or `pdfplumber` when line position matters.
- Use `pdfimages -j` when you need embedded raster assets without screen-grab
  quality loss.
- Expect tables to need cleanup. PDFs preserve appearance, not semantic table
  structure.

## OCR guidance

- If a PDF is scan-only, prefer `ocrmypdf` for a searchable text layer while
  preserving the visual pages.
- Use a `pdf2image` plus `pytesseract` workflow when you need custom OCR
  post-processing in Python.
- Verify OCR output on a few pages before processing a large batch.

## Troubleshooting

| Symptom | Likely cause | First check |
| --- | --- | --- |
| Text extraction is scrambled | Multi-column or positioned text | Try `pdfplumber` or `pdftotext -layout` |
| Merged file opens but pages are blank | Source pages use unsupported features | Re-test with `qpdf` merge path |
| Form values do not display | Appearance stream issue | Reopen in a viewer and verify field states |
| OCR result is poor | Low-resolution scans | Re-render at higher DPI before OCR |

## Related docs

- See [FORMS.md](FORMS.md) for PDF form-filling workflows.
- See [SKILL.md](SKILL.md) for the primary PDF processing guide.
