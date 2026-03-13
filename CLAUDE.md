# CLAUDE.md

This file provides Claude Code-specific guidance for working in
`llm-doc-skills`. The repository is packaged for both Claude and OpenAI agent
ecosystems, but this file focuses on local Claude Code workflows.

## Repository Overview

Each skill directory is self-contained and ships its own `SKILL.md`, agent
manifests, assets, and helper scripts as needed.

| Skill | Purpose |
| --- | --- |
| `office-custom` | Shared OOXML utilities for unpacking, packing, validation, and LibreOffice conversion |
| `docx-custom` | Word document creation, XML editing, comments, and tracked changes |
| `pdf-custom` | PDF extraction, OCR, forms, and generation |
| `pptx-custom` | Presentation generation, editing, and visual QA |
| `xlsx-custom` | Spreadsheet modeling, formulas, and recalculation |

## Core Workflows

### OOXML editing

Use the shared Office helpers for existing `.docx`, `.pptx`, and `.xlsx`
packages:

```bash
python office-custom/scripts/unpack.py file.docx unpacked/
# edit files inside unpacked/
python office-custom/scripts/pack.py unpacked/ output.docx --original file.docx
python office-custom/scripts/validate.py output.docx
```

### Spreadsheet recalculation

When `openpyxl` or XML edits touch formulas, recalculate before handing the
file to another system:

```bash
python xlsx-custom/scripts/recalc.py model.xlsx
```

### Presentation QA

Generated or edited decks must be rendered and reviewed visually:

```bash
python pptx-custom/scripts/thumbnail.py deck.pptx
```

For deeper guidance:

- use [pptx-custom/editing.md](pptx-custom/editing.md) for XML-based edits
- use [pptx-custom/pptxgenjs.md](pptx-custom/pptxgenjs.md) for generated decks

### PDF workflows

Read [pdf-custom/SKILL.md](pdf-custom/SKILL.md) first, then branch to:

- [pdf-custom/FORMS.md](pdf-custom/FORMS.md) for AcroForms
- [pdf-custom/REFERENCE.md](pdf-custom/REFERENCE.md) for advanced operations

## Important Implementation Notes

- Word tables need explicit widths at both the table and cell level.
- Spreadsheet outputs should preserve formulas instead of hardcoding totals.
- Presentation work should avoid text-only slides and always go through QA.
- ReportLab PDFs should use `<sub>` and `<super>` markup instead of Unicode
  subscript and superscript characters.

## Packaging and Verification

The build system packages each skill directory into `built/*-skill.zip`.
Rebuilt archives use the current repository name, `llm-doc-skills`, as the ZIP
root.

```bash
make clean
make build
make verify
```

The repo also includes a local `.markdownlint-cli2.jsonc` so Markdown cleanup
is consistent when a markdownlint runner is available.
