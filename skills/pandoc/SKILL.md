---
name: pandoc
description: Use when a task involves Pandoc-based document conversion, publishing pipelines, metadata-driven exports, templates, filters, citations, or cross-format delivery across Markdown, HTML, DOCX, EPUB, slide decks, and PDF.
---

# Pandoc Publishing and Conversion

## Intent Router

Load sections based on the task:
- Format conversion or publishing pipeline -> `references/format-matrix.md`
- Templates, filters, or citations -> `references/templates-filters-citations.md`
- PDF engines or export troubleshooting -> `references/pdf-engines.md`

## Overview

This skill covers Pandoc-centered document transformation and publishing.
Use it when the core problem is converting, normalizing, or publishing content across multiple document formats.

The guidance in this skill follows the official Pandoc User's Guide and Getting Started documentation.
Prefer the official CLI and keep the command explicit so output stays reproducible.

## Quick Start

```bash
python pandoc/scripts/convert.py notes.md --to html --output notes.html --standalone
```

```bash
python pandoc/scripts/convert.py paper.md --to docx --output paper.docx --citeproc --metadata title="Research Brief"
```

## Preferred Workflow

1. Identify the source format and the delivery format.
2. Decide whether source parsing must be explicit with `--from`.
3. Decide whether the output needs a standalone shell, metadata, citations, or a custom PDF engine.
4. Build the simplest command that preserves the required structure.
5. Re-run the same command after narrowing input if an engine or template fails.

## Tool Selection Guidance

Prefer Pandoc when the task calls for:
- format-to-format conversion
- one source rendered to several targets
- metadata-driven publishing
- bibliography and citation processing
- templated export
- slide generation from text sources

Prefer other skills when the task is mainly about source-language authoring:
- `markdown` for CommonMark and GFM writing conventions
- `latex` for TeX-native layout and compile loops
- `typst` for Typst-native writing and layout control
- `asciidoc` for AsciiDoc and Asciidoctor publishing flows

## Conversion and Export

Common targets:
- HTML and standalone HTML
- DOCX for review or editing handoff
- EPUB for ebook output
- PDF via an explicit engine
- reveal.js or slidy for slides

```bash
pandoc handbook.md --to epub --output handbook.epub
pandoc slides.md --to revealjs --standalone --output slides.html
```

## Metadata, Templates, and Citations

Pandoc's power comes from metadata and transformation hooks.
Reach for metadata flags, templates, and citeproc before manual post-processing.

```bash
pandoc chapter.md --to html --template page.html --metadata title="Chapter 1" --output chapter.html
```

```bash
pandoc paper.md --citeproc --bibliography refs.bib --csl apa.csl --output paper.pdf
```

## Troubleshooting

Common failure modes:
- source format guessed incorrectly
- external PDF engine missing
- template variables missing or misnamed
- citation files not resolvable from the working directory
- slide output requiring a standalone shell or asset path review

Start with a minimal conversion that drops optional flags.
Then add back template, metadata, bibliography, and engine options one step at a time.

## Official References

Primary sources:
- Pandoc User's Guide: <https://pandoc.org/MANUAL.html>
- Pandoc Getting Started: <https://pandoc.org/getting-started.html>

Deep-dive references for this skill:
- `references/format-matrix.md`
- `references/templates-filters-citations.md`
- `references/pdf-engines.md`
