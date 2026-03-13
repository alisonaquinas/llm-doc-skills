# PDF Form Filling

Use this guide when the task involves existing PDF form fields rather than
freeform document generation.

## Choose the right approach

- Use `pypdf` for standard AcroForm text fields, checkboxes, and simple
  dropdowns.
- Use `pdf-lib` if a JavaScript runtime is available and you need better
  appearance handling or richer field helpers.
- Do not promise support for XFA-only forms. Those are not handled reliably by
  the libraries documented in this repo.

## Inspect the form first

Before writing values, confirm the PDF actually exposes fields:

```python
from pypdf import PdfReader

reader = PdfReader("form.pdf")
fields = reader.get_fields() or {}

for name, field in fields.items():
    print(name, field.get("/FT"), field.get("/V"))
```

If `get_fields()` returns `None`, the file may be flattened, image-based, or an
XFA form.

## Fill AcroForm fields with `pypdf`

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("form.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

writer.update_page_form_field_values(
    writer.pages[0],
    {
        "FullName": "Jane Example",
        "Email": "jane@example.com",
        "AgreeToTerms": "/Yes",
    },
)

with open("filled-form.pdf", "wb") as handle:
    writer.write(handle)
```

## Checkbox and radio values

- Checkboxes usually expect an export value such as `/Yes`, not `True`.
- Radio buttons also expect the widget's export value.
- If a box stays visually unchecked, inspect the field dictionary to confirm
  the allowed appearance states.

## Preserve appearances

Some viewers show updated values only after the file is reopened or printed.
When that happens:

1. Write the file with `pypdf`.
2. Re-open it in a PDF viewer to confirm the appearance stream updates.
3. If the target workflow needs a flattened output, create a rendered copy
   after the values are confirmed.

## JavaScript option with `pdf-lib`

```python
import fs from "node:fs";
import { PDFDocument } from "pdf-lib";

const bytes = fs.readFileSync("form.pdf");
const pdf = await PDFDocument.load(bytes);
const form = pdf.getForm();

form.getTextField("FullName").setText("Jane Example");
form.getTextField("Email").setText("jane@example.com");
form.getCheckBox("AgreeToTerms").check();

fs.writeFileSync("filled-form.pdf", await pdf.save());
```

## Common failure modes

- Missing fields: confirm the PDF contains AcroForm fields, not only visible
  text.
- Blank output values: verify the field names exactly as returned by
  `get_fields()`.
- Checkbox state ignored: inspect the export values instead of sending `True`.
- Broken viewer appearance: reopen in Acrobat/Preview/Chrome and verify the
  saved file, then flatten only after the value layer looks correct.

## Related docs

- See [REFERENCE.md](REFERENCE.md) for tool-selection and troubleshooting notes.
- See [SKILL.md](SKILL.md) for the broader PDF workflow guide.
