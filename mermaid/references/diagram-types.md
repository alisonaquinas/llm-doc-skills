# Mermaid Diagram Types

Mermaid supports several diagram families suited to documentation-first workflows.
Pick the type that matches the question the diagram needs to answer.

## Common diagram families

- flowchart for process or decision flow
- sequenceDiagram for actor and system interactions over time
- classDiagram for type relationships
- stateDiagram-v2 for lifecycle modeling
- erDiagram for entities and cardinality
- journey, gantt, timeline, mindmap, and quadrant charts where those views fit the story

## Working guidance

Use the narrowest diagram type that communicates the model.
Avoid forcing architecture, state, and sequence content into one diagram when separate diagrams read better.
Keep labels short and move long explanation into surrounding prose.

## Review checklist

- confirm the chosen diagram family matches the problem
- confirm labels fit within exported bounds
- confirm directional flow is obvious without color alone
- confirm Markdown embedding context can display the chosen output format
