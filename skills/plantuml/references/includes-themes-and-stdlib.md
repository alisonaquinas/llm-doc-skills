# Includes, Themes, and Stdlib

PlantUML becomes more maintainable when shared elements are factored into includes and theme choices are explicit.
That keeps rendering reproducible across repositories and documentation pipelines.

## Includes

Use includes for shared participants, style conventions, or repeated legend material.
Keep include paths stable and checked into version control when possible.
If a diagram depends on the PlantUML standard library, note that dependency next to the source.

## Themes and styling

Prefer documented theme or skinparam choices over ad hoc SVG edits.
Theme decisions should improve readability, not only appearance.
When a theme changes contrast or spacing materially, render a representative sample before rolling it out widely.

## Common cautions

- unresolved includes often fail only at render time
- theme changes can disrupt layout and note wrapping
- remote includes add availability risk to otherwise simple docs builds
