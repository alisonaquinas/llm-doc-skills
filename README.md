# llm-doc-skills

`llm-doc-skills` is a repository of packaged skills for working with common
document formats and publishing toolchains. The repo is designed to ship cleanly
for both Claude and OpenAI agent runtimes and includes shared helper scripts for
OOXML workflows plus wrappers for text-first publishing tools.

## Included Skills

| Skill | Formats | Use When |
| --- | --- | --- |
| [office-custom](skills/office-custom/SKILL.md) | `.docx`, `.pptx`, `.xlsx` | Unpack, repack, validate, or convert OOXML files |
| [docx-custom](skills/docx-custom/SKILL.md) | `.docx` | Create or edit Word documents, tracked changes, tables, and comments |
| [pdf-custom](skills/pdf-custom/SKILL.md) | `.pdf` | Merge, split, extract, OCR, form filling, and PDF generation |
| [pptx-custom](skills/pptx-custom/SKILL.md) | `.pptx` | Build or edit presentations with visual QA |
| [xlsx-custom](skills/xlsx-custom/SKILL.md) | `.xlsx`, `.csv`, `.tsv` | Create spreadsheet models, formulas, and formatted outputs |
| [pandoc](skills/pandoc/SKILL.md) | `.md`, `.html`, `.docx`, `.epub`, `.pdf` | Convert and publish documents across formats with Pandoc |
| [latex](skills/latex/SKILL.md) | `.tex`, `.bib`, `.pdf` | Author, build, and debug LaTeX documents and toolchains |
| [typst](skills/typst/SKILL.md) | `.typ`, `.pdf`, `.png`, `.svg` | Write and export Typst documents with native layout control |
| [markdown](skills/markdown/SKILL.md) | `.md`, docs text | Author and render CommonMark and GFM documents |
| [github-flavored-markdown](skills/github-flavored-markdown/SKILL.md) | `.md`, GitHub docs | Author and render GitHub-targeted Markdown |
| [gitlab-flavored-markdown](skills/gitlab-flavored-markdown/SKILL.md) | `.md`, GitLab docs | Author and render GitLab-targeted Markdown |
| [mermaid](skills/mermaid/SKILL.md) | `.mmd`, `.svg`, `.png`, `.pdf` | Author and render Mermaid diagrams for docs |
| [plantuml](skills/plantuml/SKILL.md) | `.puml`, `.plantuml`, `.svg`, `.png` | Author and render UML-style PlantUML diagrams |
| [graphviz](skills/graphviz/SKILL.md) | `.dot`, `.svg`, `.png`, `.pdf` | Author and render Graphviz DOT diagrams |
| [asciidoc](skills/asciidoc/SKILL.md) | `.adoc`, `.asciidoc`, `.pdf`, `.html` | Publish AsciiDoc with Asciidoctor backends |
| [raw-document](skills/raw-document/SKILL.md) | Any binary or text document | Inspect, extract, and repair documents at the raw byte or XML level |

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
cat skills/docx-custom/SKILL.md
cat skills/pdf-custom/SKILL.md
cat skills/pptx-custom/SKILL.md
cat skills/xlsx-custom/SKILL.md
cat skills/pandoc/SKILL.md
cat skills/latex/SKILL.md
cat skills/typst/SKILL.md
cat skills/markdown/SKILL.md
cat skills/github-flavored-markdown/SKILL.md
cat skills/gitlab-flavored-markdown/SKILL.md
cat skills/mermaid/SKILL.md
cat skills/plantuml/SKILL.md
cat skills/graphviz/SKILL.md
cat skills/asciidoc/SKILL.md
```

## Companion Guides

These reference files are bundled and linked from the skills:

- [pdf-custom/FORMS.md](skills/pdf-custom/FORMS.md) for AcroForm workflows
- [pdf-custom/REFERENCE.md](skills/pdf-custom/REFERENCE.md) for advanced PDF patterns
- [pptx-custom/editing.md](skills/pptx-custom/editing.md) for unpack/edit/repack flows
- [pptx-custom/pptxgenjs.md](skills/pptx-custom/pptxgenjs.md) for generated decks
- [pandoc/references/format-matrix.md](skills/pandoc/references/format-matrix.md) for conversion targeting
- [latex/references/engines-and-toolchain.md](skills/latex/references/engines-and-toolchain.md) for build orchestration
- [typst/references/export-and-cli.md](skills/typst/references/export-and-cli.md) for CLI export patterns
- [markdown/references/commonmark-vs-gfm.md](skills/markdown/references/commonmark-vs-gfm.md) for dialect boundaries
- [github-flavored-markdown/references/gfm-syntax-matrix.md](skills/github-flavored-markdown/references/gfm-syntax-matrix.md) for GitHub-specific syntax and portability
- [gitlab-flavored-markdown/references/glfm-syntax-matrix.md](skills/gitlab-flavored-markdown/references/glfm-syntax-matrix.md) for GitLab-specific syntax and portability
- [mermaid/references/diagram-types.md](skills/mermaid/references/diagram-types.md) for Mermaid diagram selection
- [plantuml/references/diagram-families.md](skills/plantuml/references/diagram-families.md) for UML-oriented diagram patterns
- [graphviz/references/layout-engines.md](skills/graphviz/references/layout-engines.md) for engine selection
- [asciidoc/references/backends-and-pdf.md](skills/asciidoc/references/backends-and-pdf.md) for backend selection

## Core Validation Rules

- Recalculate spreadsheet formulas after edits:
  `python skills/xlsx-custom/scripts/recalc.py workbook.xlsx`
- Validate edited OOXML packages:
  `python skills/office-custom/scripts/validate.py document.docx`
- QA presentations visually after any meaningful change:
  `python skills/pptx-custom/scripts/thumbnail.py presentation.pptx`
- Keep text-first publishing and diagram wrappers testable without their external binaries:
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
├── github-flavored-markdown/
├── gitlab-flavored-markdown/
├── mermaid/
├── plantuml/
├── graphviz/
└── asciidoc/
```

## Related Repo Docs

- [AGENTS.md](AGENTS.md) for agent-usage guidance in this repo
- [CLAUDE.md](CLAUDE.md) for Claude Code-specific workflows
- [VALIDATION_REPORT.md](VALIDATION_REPORT.md) for the current repo status
