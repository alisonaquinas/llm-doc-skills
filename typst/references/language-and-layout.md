# Typst Language and Layout Reference

Authoritative sources:
- Typst documentation: <https://typst.app/docs/>
- Typst reference: <https://typst.app/docs/reference/>

## Core ideas

Typst uses concise markup plus programmable layout primitives.
Common areas to route here:
- headings and document structure
- math and equations
- figures, tables, and references
- page setup and layout

## Typical patterns

- `#set page(...)` for global page layout
- `#show` rules for presentation overrides
- semantic heading and list markup for source structure
- native math blocks instead of TeX passthrough where possible

```typst
#set page(margin: 1in)
#set text(font: "Libertinus Serif")

= Report Title

This paragraph introduces the document.
```
