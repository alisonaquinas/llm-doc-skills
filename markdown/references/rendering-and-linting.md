# Markdown Rendering and Linting Matrix

Credible references:
- CommonMark: <https://spec.commonmark.org/current/>
- GFM: <https://github.github.com/gfm/>
- Pandoc docs: <https://pandoc.org/MANUAL.html>

## Preferred renderer choices

- `cmark-gfm` for fast HTML rendering of CommonMark and GFM content
- `pandoc` for PDF or DOCX export, or when a broader document pipeline is required

```bash
cmark-gfm README.md > README.html
pandoc guide.md --to pdf --output guide.pdf
pandoc guide.md --to docx --output guide.docx
```

## Linting guidance

Markdown linting is policy-specific rather than part of the syntax spec.
Keep renderer choice separate from lint policy.
Use repository-local markdownlint rules when available.
