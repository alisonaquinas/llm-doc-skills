# llm-doc-skills

`llm-doc-skills` is a repository of packaged skills for working with common
document formats and publishing toolchains. The repo is designed to ship cleanly
for both Claude and OpenAI agent runtimes and includes shared helper scripts for
OOXML workflows plus wrappers for text-first publishing tools.

## Included Skills

| Skill | Formats | Use When |
| --- | --- | --- |
| [office-custom](office-custom/SKILL.md) | `.docx`, `.pptx`, `.xlsx` | Unpack, repack, validate, or convert OOXML files |
| [docx-custom](docx-custom/SKILL.md) | `.docx` | Create or edit Word documents, tracked changes, tables, and comments |
| [pdf-custom](pdf-custom/SKILL.md) | `.pdf` | Merge, split, extract, OCR, form filling, and PDF generation |
| [pptx-custom](pptx-custom/SKILL.md) | `.pptx` | Build or edit presentations with visual QA |
| [xlsx-custom](xlsx-custom/SKILL.md) | `.xlsx`, `.csv`, `.tsv` | Create spreadsheet models, formulas, and formatted outputs |
| [pandoc](pandoc/SKILL.md) | `.md`, `.html`, `.docx`, `.epub`, `.pdf` | Convert and publish documents across formats with Pandoc |
| [latex](latex/SKILL.md) | `.tex`, `.bib`, `.pdf` | Author, build, and debug LaTeX documents and toolchains |
| [typst](typst/SKILL.md) | `.typ`, `.pdf`, `.png`, `.svg` | Write and export Typst documents with native layout control |
| [markdown](markdown/SKILL.md) | `.md`, docs text | Author and render CommonMark and GFM documents |
| [asciidoc](asciidoc/SKILL.md) | `.adoc`, `.asciidoc`, `.pdf`, `.html` | Publish AsciiDoc with Asciidoctor backends |

## Cross-Agent Packaging

Each packaged skill is expected to ship:

- `agents/claude.yaml`
- `agents/openai.yaml`
- `SKILL.md`
- any required `assets/`, `scripts/`, or companion docs

The build output lives in `built/` and is generated from the current
repository name, so rebuilt packages use `llm-doc-skills/` as their archive
root.

## Quick Start

Read the skill that matches the task, then follow its companion docs when the
workflow branches into a deeper topic.

```bash
cat docx-custom/SKILL.md
cat pdf-custom/SKILL.md
cat pptx-custom/SKILL.md
cat xlsx-custom/SKILL.md
cat pandoc/SKILL.md
cat latex/SKILL.md
cat typst/SKILL.md
cat markdown/SKILL.md
cat asciidoc/SKILL.md
```

## Companion Guides

These reference files are bundled and linked from the skills:

- [pdf-custom/FORMS.md](pdf-custom/FORMS.md) for AcroForm workflows
- [pdf-custom/REFERENCE.md](pdf-custom/REFERENCE.md) for advanced PDF patterns
- [pptx-custom/editing.md](pptx-custom/editing.md) for unpack/edit/repack flows
- [pptx-custom/pptxgenjs.md](pptx-custom/pptxgenjs.md) for generated decks
- [pandoc/references/format-matrix.md](pandoc/references/format-matrix.md) for conversion targeting
- [latex/references/engines-and-toolchain.md](latex/references/engines-and-toolchain.md) for build orchestration
- [typst/references/export-and-cli.md](typst/references/export-and-cli.md) for CLI export patterns
- [markdown/references/commonmark-vs-gfm.md](markdown/references/commonmark-vs-gfm.md) for dialect boundaries
- [asciidoc/references/backends-and-pdf.md](asciidoc/references/backends-and-pdf.md) for backend selection

## Core Validation Rules

- Recalculate spreadsheet formulas after edits:
  `python xlsx-custom/scripts/recalc.py workbook.xlsx`
- Validate edited OOXML packages:
  `python office-custom/scripts/validate.py document.docx`
- QA presentations visually after any meaningful change:
  `python pptx-custom/scripts/thumbnail.py presentation.pptx`
- Keep text-first publishing wrappers testable without their external binaries:
  validate command builders and missing-tool messages with stdlib-only unit tests

## Build, Test, and Verify

```bash
make clean
make build
make verify

# Run the full repo test gate (unit tests, stdlib only)
make test
```

## Project Structure

```text
llm-doc-skills/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── VALIDATION_REPORT.md
├── Makefile
├── built/
├── office-custom/
├── docx-custom/
├── pdf-custom/
├── pptx-custom/
├── xlsx-custom/
├── pandoc/
├── latex/
├── typst/
├── markdown/
└── asciidoc/
```

## Related Repo Docs

- [AGENTS.md](AGENTS.md) for agent-usage guidance in this repo
- [CLAUDE.md](CLAUDE.md) for Claude Code-specific workflows
- [VALIDATION_REPORT.md](VALIDATION_REPORT.md) for the current repo status
