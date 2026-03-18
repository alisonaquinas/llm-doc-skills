# DOT Syntax and Attributes

DOT describes graphs as structured text.
Use the language to make graph relationships explicit before reaching for styling.

## Core building blocks

- `graph` for undirected graphs
- `digraph` for directed graphs
- nodes and edges with stable identifiers
- subgraphs and clusters for grouping
- graph, node, and edge attributes for styling and layout hints

## Working guidance

Define the graph type first, then add nodes and edges with the smallest useful attribute set.
Prefer consistent attribute blocks over repeated inline overrides.
Use labels to clarify intent, but avoid turning the graph into long-form prose.

## Review checklist

- confirm graph versus digraph matches the relationship model
- confirm edge direction is meaningful and not decorative
- confirm clusters improve structure rather than hiding it
- confirm labels remain readable at the target output size
