# Typst Templates, Show Rules, and Reuse

Authoritative source:
- Typst reference: <https://typst.app/docs/reference/>

## Reuse patterns

Typst supports composition through functions, modules, and show rules.
Use these tools when a task needs repeatable layout or house style.

## High-value techniques

- encapsulate repeated page or section shells in functions
- centralize styling with `set` and `show` rules
- separate content from presentation when a document family shares one theme

```typst
#show heading.where(level: 1): set text(fill: rgb("2f4f6a"))
```

## Escalation rule

If a task is really about template architecture rather than one document, route here before editing the main source body.
