# Typst Export and CLI Patterns

Authoritative source:
- Typst docs and CLI reference: <https://typst.app/docs/reference/>

## Common exports

- PDF for final distribution
- PNG for raster page previews
- SVG for vector page output

```bash
typst compile report.typ report.pdf
typst compile slides.typ slides.png --pages 1-3 --ppi 144
```

## Operational guidance

- Set `--root` for projects with includes or asset directories.
- Keep output filenames explicit in scripted workflows.
- Use page selection for preview or targeted export loops.
- Re-run on a narrow sample when a large document fails.
