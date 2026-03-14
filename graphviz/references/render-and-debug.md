# Render and Debug

Graphviz debugging is usually a matter of separating structural problems from styling problems.

## Render strategy

- start with `dot` unless the graph topology clearly suggests another engine
- render SVG first for crisp labels and easy inspection
- switch to PNG only when the destination requires a raster image
- treat PDF as a delivery format rather than the first debug target

## Debug flow

1. render the graph with minimal attributes
2. confirm node and edge structure
3. choose the most appropriate engine
4. add styling and spacing hints only after structure is stable

## Common failure modes

- the chosen engine does not match the graph topology
- labels are too dense for the graph size
- clusters or rank hints fight the engine
- styling changes hide that the graph itself needs simplification
