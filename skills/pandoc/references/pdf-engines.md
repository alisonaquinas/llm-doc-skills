# Pandoc PDF Engines

Authoritative source:
- Pandoc User's Guide PDF section: <https://pandoc.org/MANUAL.html>

## Engine selection

Pandoc delegates PDF rendering to external engines. Common choices include:
- `pdflatex`
- `xelatex`
- `lualatex`
- `wkhtmltopdf`
- `weasyprint`
- `prince`

## Practical guidance

- Prefer `xelatex` or `lualatex` for modern font and Unicode coverage.
- Prefer HTML/CSS PDF engines when the source is effectively a styled web document.
- Keep engine selection explicit in automation so output stays reproducible.

```bash
pandoc handbook.md --to pdf --pdf-engine xelatex --output handbook.pdf
pandoc site.md --to pdf --pdf-engine weasyprint --output site.pdf
```

## Failure patterns

- Missing binary on PATH
- Fonts not installed for the selected engine
- Template variables incompatible with the chosen engine
- LaTeX package errors bubbling up through Pandoc

When PDF generation fails, first verify the engine directly, then narrow the failing input to a minimal example.
