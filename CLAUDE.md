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
| `pandoc` | Cross-format conversion, metadata-driven publishing, templates, and citations |
| `latex` | LaTeX authoring, engine selection, compile loops, and TeX toolchain troubleshooting |
| `typst` | Typst-native authoring, layout control, and export workflows |
| `markdown` | CommonMark and GFM authoring plus lightweight rendering and export |
| `github-flavored-markdown` | GitHub-targeted Markdown authoring, rendering, and portability review |
| `gitlab-flavored-markdown` | GitLab-targeted Markdown authoring, rendering, and portability review |
| `mermaid` | Mermaid diagram authoring, embedding, and CLI export |
| `plantuml` | PlantUML authoring, includes, themes, and UML-oriented rendering |
| `graphviz` | DOT authoring, layout engine selection, and Graphviz export |
| `asciidoc` | AsciiDoc authoring, attributes, includes, and Asciidoctor backends |
| `obsidian-docs` | Obsidian vault documentation, MOC design, note organization, and graph navigation |
| `obsidian-config` | Obsidian `.obsidian/` settings, themes, CSS snippets, and vault sync |
| `obsidian-flavored-markdown` | OFM syntax: wikilinks, embeds, callouts, properties, and tags |
| `obsidian-plugins` | Obsidian core and community plugin management, BRAT, and plugin data |
| `obsidian-templates` | Obsidian core templates, Templater plugin, and frontmatter injection |
| `obsidian-canvas` | Obsidian Canvas `.canvas` JSON authoring and visual knowledge maps |

## Core Workflows

### OOXML editing

Use the shared Office helpers for existing `.docx`, `.pptx`, and `.xlsx`
packages:

```bash
python skills/office-custom/scripts/unpack.py file.docx unpacked/
# edit files inside unpacked/
python skills/office-custom/scripts/pack.py unpacked/ output.docx --original file.docx
python skills/office-custom/scripts/validate.py output.docx
```

### Spreadsheet recalculation

When `openpyxl` or XML edits touch formulas, recalculate before handing the
file to another system:

```bash
python skills/xlsx-custom/scripts/recalc.py model.xlsx
```

### Presentation QA

Generated or edited decks must be rendered and reviewed visually:

```bash
python skills/pptx-custom/scripts/thumbnail.py deck.pptx
```

For deeper guidance:

- use [skills/pptx-custom/editing.md](skills/pptx-custom/editing.md) for XML-based edits
- use [skills/pptx-custom/pptxgenjs.md](skills/pptx-custom/pptxgenjs.md) for generated decks

### PDF workflows

Read [skills/pdf-custom/SKILL.md](skills/pdf-custom/SKILL.md) first, then branch to:

- [skills/pdf-custom/FORMS.md](skills/pdf-custom/FORMS.md) for AcroForms
- [skills/pdf-custom/REFERENCE.md](skills/pdf-custom/REFERENCE.md) for advanced operations

### Text-first publishing workflows

Use the text-first skills when the task is centered on authoring or publishing
from plain-text sources rather than OOXML packages.

- use [skills/pandoc/SKILL.md](skills/pandoc/SKILL.md) for cross-format conversion and publishing
- use [skills/latex/SKILL.md](skills/latex/SKILL.md) for LaTeX authoring and build orchestration
- use [skills/typst/SKILL.md](skills/typst/SKILL.md) for Typst-native layout and export
- use [skills/markdown/SKILL.md](skills/markdown/SKILL.md) for CommonMark and baseline GFM docs work
- use [skills/github-flavored-markdown/SKILL.md](skills/github-flavored-markdown/SKILL.md) for GitHub-specific Markdown surfaces
- use [skills/gitlab-flavored-markdown/SKILL.md](skills/gitlab-flavored-markdown/SKILL.md) for GitLab-specific Markdown surfaces
- use [skills/mermaid/SKILL.md](skills/mermaid/SKILL.md) for Mermaid diagrams in docs workflows
- use [skills/plantuml/SKILL.md](skills/plantuml/SKILL.md) for UML-style text diagrams
- use [skills/graphviz/SKILL.md](skills/graphviz/SKILL.md) for DOT and layout-engine-driven graph diagrams
- use [skills/asciidoc/SKILL.md](skills/asciidoc/SKILL.md) for Asciidoctor publishing flows

### Obsidian vault workflows

Use the Obsidian skills when working inside a local Obsidian vault.

- use [skills/obsidian-docs/SKILL.md](skills/obsidian-docs/SKILL.md) for vault structure, MOCs, and knowledge-base patterns
- use [skills/obsidian-config/SKILL.md](skills/obsidian-config/SKILL.md) for `.obsidian/` settings, themes, and sync
- use [skills/obsidian-flavored-markdown/SKILL.md](skills/obsidian-flavored-markdown/SKILL.md) for OFM syntax including wikilinks, callouts, and properties
- use [skills/obsidian-plugins/SKILL.md](skills/obsidian-plugins/SKILL.md) for plugin management and BRAT
- use [skills/obsidian-templates/SKILL.md](skills/obsidian-templates/SKILL.md) for Core Templates and Templater authoring
- use [skills/obsidian-canvas/SKILL.md](skills/obsidian-canvas/SKILL.md) for `.canvas` JSON authoring and visual maps

## Important Implementation Notes

- Word tables need explicit widths at both the table and cell level.
- Spreadsheet outputs should preserve formulas instead of hardcoding totals.
- Presentation work should avoid text-only slides and always go through QA.
- ReportLab PDFs should use `<sub>` and `<super>` markup instead of Unicode
  subscript and superscript characters.
- Text-first and diagram wrapper scripts should keep command construction testable without
  requiring the external binary in unit tests.
- External publishing tools such as Pandoc, latexmk, Typst, `cmark-gfm`, Mermaid CLI,
  PlantUML, Java, Graphviz, and Asciidoctor are optional system prerequisites rather than vendored repo dependencies.

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
