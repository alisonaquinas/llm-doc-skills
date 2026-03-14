# Pandoc Templates, Filters, and Citations

Authoritative sources:
- Pandoc User's Guide sections on templates, variables, and citeproc: <https://pandoc.org/MANUAL.html>

## Templates and variables

Use templates when a stable output shell is required across many documents.
Template variables can be injected from metadata blocks, YAML metadata files, or repeated `--metadata` flags.

```bash
pandoc input.md --template template.html --metadata title="Quarterly Review" --output review.html
```

## Filters and Lua filters

Pandoc supports filters for structural rewrites that are awkward in source markup alone.
For repeatable document-programming tasks, prefer Lua filters because they ship naturally with Pandoc.

Use filters for:
- metadata normalization
- AST-based heading or block rewrites
- custom callout or shortcode expansion
- citation or cross-reference post-processing

## Citations and bibliographies

Pandoc's citeproc flow supports common scholarly publishing patterns.
Typical ingredients:
- bibliography file such as `.bib`
- citation style file such as `.csl`
- `--citeproc`

```bash
pandoc paper.md --citeproc --bibliography refs.bib --csl apa.csl --output paper.docx
```

## Escalation guidance

If the task depends on AST transformation, a custom template, or citation formatting policy, route directly into this reference before drafting the command.
