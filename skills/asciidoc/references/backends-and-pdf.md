# Asciidoctor Backends and PDF Publishing

Authoritative sources:
- Asciidoctor documentation: <https://docs.asciidoctor.org/>
- AsciiDoc language docs: <https://docs.asciidoctor.org/asciidoc/latest/>

## Common targets

- HTML5 through `asciidoctor`
- PDF through `asciidoctor-pdf`
- DocBook through the DocBook backend

```bash
asciidoctor guide.adoc
asciidoctor-pdf book.adoc
asciidoctor --backend docbook guide.adoc
```

## Practical guidance

- Use HTML for iterative preview and review.
- Use PDF for distribution-ready styled output.
- Use DocBook when a downstream XML-based publishing flow requires it.
