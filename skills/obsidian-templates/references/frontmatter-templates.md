# Frontmatter Templates

Frontmatter templates pre-populate YAML properties when a new note is created from a template.
Consistent frontmatter across a note type enables reliable Dataview queries and the Properties panel.

## Basic frontmatter template pattern

```yaml
---
title: <% tp.file.title %>
date: <% tp.date.now("YYYY-MM-DD") %>
created: <% tp.file.creation_date("YYYY-MM-DD") %>
modified: <% tp.date.now("YYYY-MM-DD") %>
tags: []
status: draft
---
```

## Project note template

```yaml
---
title: <% tp.file.title %>
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [project]
status: active
due:
related: []
---
```

## Daily note template

A daily note template that pre-links to yesterday and tomorrow:

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
week: <% tp.date.now("W") %>
tags: [daily]
---

# <% tp.date.now("dddd, MMMM D, YYYY") %>

← [[<% tp.date.yesterday("YYYY-MM-DD") %>]] | [[<% tp.date.tomorrow("YYYY-MM-DD") %>]] →

## Tasks

## Notes

## Review
```

## MOC template

```markdown
---
title: <% tp.file.title %>
created: <% tp.date.now("YYYY-MM-DD") %>
tags: [moc]
---

# <% tp.file.title %>

## Overview

## Notes

## Related MOCs
```

## Template inheritance

Obsidian does not support template inheritance natively.
Simulate it by creating a base template with shared frontmatter and inserting it first, then inserting a specialized template that adds type-specific sections.
The Templater plugin's `tp.file.include()` can compose template fragments:

```javascript
<% await tp.file.include("[[_base-frontmatter]]") %>
```

This inserts the content of `_base-frontmatter.md` inline, enabling shared property definitions.

## Folder templates

Templater supports auto-triggering a specific template when a new note is created inside a particular folder:
Settings → Templater → Folder Templates → add a folder-to-template mapping.
This enforces consistent note structure by note type without manual template selection.
