# Layout Engines

Graphviz includes multiple layout engines.
Choosing the right one usually matters more than fine-grained styling at the start.

## Common engines

- `dot` for hierarchical and dependency-style graphs
- `neato` for spring-model layouts
- `fdp` for undirected force-directed layouts
- `sfdp` for large force-directed graphs
- `twopi` for radial layouts
- `circo` for circular structures

## Working guidance

Start with the engine that matches the graph's topology.
If the graph still fights the layout, simplify edge density before adding positional hints.
Keep engine selection explicit in docs and scripts so output stays reproducible.

## Common cautions

- an engine that works for a small sample may not scale cleanly
- hard positional constraints can make maintenance harder than changing engines
- switching engines can require revisiting rank, cluster, and spacing assumptions
