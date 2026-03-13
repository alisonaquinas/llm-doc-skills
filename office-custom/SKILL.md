---
name: office-custom
description: Common utilities for unpacking, editing, repacking, and validating Office Open XML files (.docx, .pptx, .xlsx)
---

# Office Open XML Utilities

This skill provides the shared scripts used by the `docx-custom`, `pptx-custom`,
and `xlsx-custom` skills to work with **Office Open XML (OOXML)** files — the ZIP-based
XML format that underlies all modern Microsoft Office documents.

## Intent Router

No separate reference files. All workflows are documented inline below:

- Unpack/repack an OOXML file → `## Scripts` section (`unpack.py`, `pack.py`)
- Validate OOXML structure → `## Scripts` section (`validate.py`)
- Convert to PDF via LibreOffice → `## Scripts` section (`soffice.py`)

## What Is OOXML?

A `.docx`, `.pptx`, or `.xlsx` file is a **ZIP archive** containing XML files:

```text
document.docx (ZIP)
├── [Content_Types].xml       ← declares every part's MIME type
├── _rels/.rels               ← top-level relationships
└── word/
    ├── document.xml          ← main body content
    ├── styles.xml            ← style definitions
    ├── settings.xml          ← document settings
    ├── _rels/document.xml.rels
    └── media/                ← embedded images, etc.
```

Editing an OOXML file means: **unpack → edit XML → repack**.

---

## Scripts

All scripts live in `office-custom/scripts/` and are runnable from the repo root.

### `unpack.py` — Extract an OOXML file for editing

```bash
python office-custom/scripts/unpack.py <source> <dest_dir>
python office-custom/scripts/unpack.py document.docx unpacked/
python office-custom/scripts/unpack.py presentation.pptx unpacked/ --merge-runs false
```

**What it does:**
- Extracts the ZIP to a working directory
- Pretty-prints every `.xml` / `.rels` file (2-space indent, Unix line endings)
- Escapes smart-quote characters (`"` `"` `'` `'` `–` `—`) to XML entities so
  tools that rewrite encoding don't corrupt them
- For `.docx` files (optional, default on): merges adjacent `<w:r>` runs that
  share identical formatting — makes find-and-replace reliable across run boundaries

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--merge-runs true\|false` | `true` | Merge adjacent same-format runs in `.docx` |

---

### `pack.py` — Repack an edited directory back into an OOXML file

```bash
python office-custom/scripts/pack.py <unpacked_dir> <output_file> [--original <original>]
python office-custom/scripts/pack.py unpacked/ output.docx --original document.docx
python office-custom/scripts/pack.py unpacked/ output.pptx --original presentation.pptx
```

**What it does:**
- Walks the unpacked directory and writes every file into a new ZIP
- Writes `[Content_Types].xml` first (OOXML spec requirement)
- Applies two **auto-repair** passes to every XML file:
  1. **durableId fix** — regenerates `w:durableId` values ≥ `0x7FFFFFFF`
     (Word rejects these; they appear when content is copy-pasted from other documents)
  2. **`xml:space="preserve"` fix** — adds the attribute to `<w:t>` elements
     whose text has leading/trailing spaces (Word strips the spaces without it)
- Condenses pretty-printed XML back to compact form before writing
- Runs `validate.py` on the output (can be suppressed with `--validate false`)

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--original PATH` | — | Copy ZIP metadata/comment from the original file |
| `--validate true\|false` | `true` | Run validate.py after packing |

---

### `validate.py` — Validate an OOXML file

```bash
python office-custom/scripts/validate.py document.docx
python office-custom/scripts/validate.py presentation.pptx spreadsheet.xlsx
python office-custom/scripts/validate.py *.docx --quiet
```

**What it does — three checks in order:**
1. **ZIP integrity** — can the file be opened as a valid ZIP archive?
2. **Required parts** — are `[Content_Types].xml` and `_rels/.rels` present?
3. **XML well-formedness** — does every `.xml` / `.rels` member parse without error?

**Output:**

```text
OK    document.docx  (14 XML members validated)
FAIL  broken.docx
      ERROR: XML parse error in word/document.xml: ...
```

**Exit codes:** `0` = all passed, `1` = any failure.

**Options:**

| Option | Description |
|--------|-------------|
| `--quiet` | Suppress per-file output; only print summary |

---

### `soffice.py` — LibreOffice CLI wrapper

```bash
# Used programmatically by other scripts; can also be run directly:
python office-custom/scripts/soffice.py --headless --convert-to pdf document.docx
python office-custom/scripts/soffice.py --headless --convert-to docx document.doc
python office-custom/scripts/soffice.py --headless --convert-to pdf output.pptx
```

**What it does:**
- Locates the `soffice` binary across macOS, Linux, and sandboxed environments:
  - macOS app bundle: `/Applications/LibreOffice.app/Contents/MacOS/soffice`
  - Linux packages: `/usr/bin/soffice`, `/usr/bin/libreoffice`
  - Snap: `/snap/bin/libreoffice`
  - PATH fallback
- Creates an isolated temporary user-profile directory so LibreOffice doesn't
  need write access to `~/.config/libreoffice` (critical in CI / sandboxes)
- Drop-in pass-through: any arguments after the script name are forwarded
  verbatim to the `soffice` binary

**Dependency:** LibreOffice must be installed separately.
- macOS: `brew install --cask libreoffice`
- Ubuntu: `apt install libreoffice`

---

## Standard Edit Workflow

```text
┌─────────────┐   unpack.py   ┌───────────────┐   edit XML   ┌────────────────┐
│  input.docx │ ──────────── ▶│  unpacked/    │ ──────────── ▶│  unpacked/     │
│  (ZIP)      │               │  word/        │               │  word/         │
└─────────────┘               │  document.xml │               │  document.xml  │
                              │  styles.xml   │               │  (modified)    │
                              └───────────────┘               └────────┬───────┘
                                                                        │
                              ┌───────────────┐   pack.py              │
                              │  output.docx  │ ◀──────────────────────┘
                              │  (ZIP, clean) │   (auto-repair + validate)
                              └───────────────┘
```

### Step-by-step

```bash
# 1. Unpack
python office-custom/scripts/unpack.py document.docx unpacked/

# 2. Edit XML directly — use the Edit tool on files inside unpacked/
#    e.g. unpacked/word/document.xml, unpacked/word/styles.xml

# 3. Repack
python office-custom/scripts/pack.py unpacked/ output.docx --original document.docx

# Optional: validate manually
python office-custom/scripts/validate.py output.docx
```

---

## OOXML Structure Reference

### Required parts (all formats)

| Path | Purpose |
|------|---------|
| `[Content_Types].xml` | Maps ZIP entry paths to MIME content types |
| `_rels/.rels` | Top-level package relationships (points to main document part) |

### Word document (`.docx`)

| Path | Purpose |
|------|---------|
| `word/document.xml` | Main body — paragraphs, tables, runs |
| `word/styles.xml` | Named styles (Normal, Heading 1, etc.) |
| `word/settings.xml` | Document-level settings (compatibility, rsid tracking) |
| `word/numbering.xml` | List/bullet numbering definitions |
| `word/fontTable.xml` | Font declarations |
| `word/comments.xml` | Comment bodies (created by `docx-custom/scripts/comment.py`) |
| `word/theme/theme1.xml` | Colour and font theme |
| `word/media/` | Embedded images and other binary assets |
| `word/_rels/document.xml.rels` | Relationships for document.xml |

### PowerPoint presentation (`.pptx`)

| Path | Purpose |
|------|---------|
| `ppt/presentation.xml` | Presentation-level metadata and slide list |
| `ppt/slides/slide1.xml` | Individual slide content |
| `ppt/slideLayouts/slideLayout1.xml` | Layout templates |
| `ppt/slideMasters/slideMaster1.xml` | Master slide |
| `ppt/theme/theme1.xml` | Colour and font theme |
| `ppt/media/` | Embedded images |

### Excel workbook (`.xlsx`)

| Path | Purpose |
|------|---------|
| `xl/workbook.xml` | Sheet list and workbook metadata |
| `xl/worksheets/sheet1.xml` | Individual sheet data and formulas |
| `xl/styles.xml` | Cell formatting |
| `xl/sharedStrings.xml` | String table (shared across all cells) |
| `xl/calcChain.xml` | Formula calculation order |
| `xl/theme/theme1.xml` | Colour and font theme |

---

## Common XML Namespaces

| Prefix | URI | Used in |
|--------|-----|---------|
| `w:` | `http://schemas.openxmlformats.org/wordprocessingml/2006/main` | `.docx` content |
| `a:` | `http://schemas.openxmlformats.org/drawingml/2006/main` | Drawing (all formats) |
| `r:` | `http://schemas.openxmlformats.org/officeDocument/2006/relationships` | Relationships |
| `p:` | `http://schemas.openxmlformats.org/presentationml/2006/main` | `.pptx` content |
| `x:` | `http://schemas.openxmlformats.org/spreadsheetml/2006/main` | `.xlsx` content |
| `mc:` | `http://schemas.openxmlformats.org/markup-compatibility/2006` | Markup compatibility |
| `w14:` | `http://schemas.microsoft.com/office/word/2010/wordml` | Word 2010+ extensions |

---

## Auto-repair Details

`pack.py` repairs two common issues automatically:

### 1. Out-of-range `w:durableId`

Word assigns `durableId` values (persistent run identifiers) as 31-bit integers.
Values ≥ `0x7FFFFFFF` (2,147,483,648) are invalid and cause Word 2016+ to refuse
to open the file. These appear when content is copy-pasted from malformed documents.

**Fix:** Replace any out-of-range value with a random valid integer in `[1, 0x7FFFFFFE]`.

### 2. Missing `xml:space="preserve"` on `<w:t>`

The XML spec says parsers may strip leading/trailing whitespace from text nodes
unless `xml:space="preserve"` is present. Word relies on this for spaces between
runs (e.g. `"Hello " + "world"`).

**Fix:** Add `xml:space="preserve"` to any `<w:t>` whose text starts or ends with a space.

---

## Smart Quote Entities

When editing XML directly, use these XML entities instead of Unicode characters
to prevent encoding corruption:

| Character | Entity | Description |
|-----------|--------|-------------|
| `"` | `&#x201C;` | Left double quotation mark |
| `"` | `&#x201D;` | Right double quotation mark |
| `'` | `&#x2018;` | Left single quotation mark |
| `'` | `&#x2019;` | Right single quotation mark / apostrophe |
| `–` | `&#x2013;` | En dash |
| `—` | `&#x2014;` | Em dash |
| ` ` | `&#xA0;`   | Non-breaking space |

`unpack.py` converts these automatically on extraction; `pack.py` preserves them.

---

## Dependencies

| Tool | Install | Used by |
|------|---------|---------|
| LibreOffice | `brew install --cask libreoffice` / `apt install libreoffice` | `soffice.py` |
| Python stdlib | (built-in) | `unpack.py`, `pack.py`, `validate.py` |

No third-party Python packages are required for the office utilities themselves.
