# Knowledge Base Patterns

Several established patterns apply well to Obsidian vaults.
Choose the one that matches the retrieval habits for the work at hand.

## Zettelkasten

Originating with Niklas Luhmann, Zettelkasten treats each note as a self-contained atomic idea.
Notes link to each other through explicit wikilinks rather than folder hierarchy.

Core practices:
- each note covers exactly one idea
- every note links to at least one other note
- use an index or MOC to anchor entry points
- avoid generic titles; prefer specific, claim-like note names

Obsidian fit: wikilinks and the graph view make Zettelkasten natural. Tag `#permanent` for stable notes and `#fleeting` for quick captures.

## PARA method

Projects, Areas, Resources, Archives — a folder-based system by Tiago Forte.

- **Projects**: active work with a deadline or goal
- **Areas**: ongoing responsibilities with no end date (health, finances, team)
- **Resources**: reference material organized by topic
- **Archives**: completed projects and inactive areas

PARA is retrieval-oriented: material goes where it will next be needed, not where it logically belongs.

## Evergreen notes

Popularized by Andy Matuschak, evergreen notes are permanent, concept-oriented notes written to develop and refine over time.

Properties:
- titles are full sentences or strong noun phrases, not topics
- notes are revised and linked as understanding grows
- atomic and concept-focused rather than project-scoped

## Daily notes as index

Enable the Daily Notes core plugin to auto-create a dated note each day.
Use the daily note as a lightweight inbox: capture links, ideas, and tasks throughout the day.
At end of day or week, review and move content into permanent notes.

A minimal daily note template:

```markdown
---
date: {{date}}
tags: [daily]
---

## Captures

## Links added today
```
