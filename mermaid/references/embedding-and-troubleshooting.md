# Embedding and Troubleshooting

Mermaid diagrams often live inside Markdown, docs portals, or exported design notes.
That makes embedding rules just as important as source syntax.

## Embedding patterns

- keep raw `.mmd` source in version control for reviewability
- render SVG when the host cannot execute Mermaid directly
- use PNG only when SVG support is not practical
- document any required host-side Mermaid integration in adjacent docs

## Troubleshooting flow

1. render the source locally with the CLI
2. shrink the file to a minimal diagram if parsing fails
3. check theme or config overrides
4. export to SVG first before debugging raster output

## Common failure modes

- diagram header does not match the body syntax
- unsupported features for the installed Mermaid version
- Markdown host does not execute Mermaid blocks
- exported output looks cramped because labels or branches are too dense
