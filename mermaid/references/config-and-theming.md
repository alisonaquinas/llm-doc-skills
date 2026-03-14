# Mermaid Config and Theming

Mermaid supports configuration through frontmatter, directives, and CLI config files.
Use those inputs to control theme, spacing, security settings, and rendering behavior.

## Practical controls

- theme selection for visual consistency
- background color for exported PNG or PDF assets
- config files for shared render defaults
- frontmatter or init blocks when the host supports them

## Working guidance

Prefer checked-in config files over one-off post-processing.
Keep theme choices legible in both light and dark documentation environments.
If a docs host applies its own Mermaid integration, verify which config fields it honors.

## Common cautions

- init directives can differ by host integration
- theme assumptions may not carry from local CLI output to live docs rendering
- exported raster images can clip labels if the diagram is overly dense
