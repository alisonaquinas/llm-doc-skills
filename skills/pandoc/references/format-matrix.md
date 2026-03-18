# Pandoc Format Matrix

Authoritative sources:
- Pandoc User's Guide: <https://pandoc.org/MANUAL.html>
- Pandoc Getting Started: <https://pandoc.org/getting-started.html>

## Core formats to route through this skill

- Markdown families: CommonMark, GFM, Pandoc Markdown
- HTML and HTML fragment output
- DOCX input and output
- EPUB export
- PDF export through a chosen PDF engine
- Slide decks such as reveal.js and slidy

## Preferred usage patterns

- Normalize heterogeneous authoring inputs into a single publishing target.
- Use metadata blocks and `--metadata` flags for title, author, date, and custom fields.
- Use templates when output structure matters more than one-off formatting edits.
- Use DOCX export for downstream review workflows.
- Use standalone HTML or EPUB when a self-contained deliverable is required.

## Common conversion examples

```bash
pandoc report.md --to html --standalone --output report.html
pandoc brief.docx --to gfm --output brief.md
pandoc paper.md --to docx --output paper.docx
pandoc slides.md --to revealjs --standalone --output slides.html
```

## Routing notes

- Prefer this skill when the task centers on transformation between formats.
- Prefer `markdown`, `latex`, `typst`, or `asciidoc` when the task centers on authoring idioms in that source language.
- Keep PDF-engine choice explicit when output fidelity matters.
