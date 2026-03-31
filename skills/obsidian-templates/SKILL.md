---
name: obsidian-templates
description: Use when a task involves Obsidian template authoring, configuring
  the core Templates plugin or Templater plugin, building daily note templates,
  injecting frontmatter properties dynamically, or using variables and script
  blocks in Obsidian template files.
---

# Obsidian Templates

## Intent Router

Load sections based on the task:

- Core Templates plugin configuration and built-in variables → `references/core-templates-reference.md`
- Templater plugin syntax, tp.* functions, and script blocks → `references/templater-syntax.md`
- Frontmatter injection, daily note templates, and template inheritance → `references/frontmatter-templates.md`

## Overview

This skill covers template authoring inside Obsidian vaults.
Two template systems are available: the Core Templates plugin (built-in, simple variable substitution) and the Templater community plugin (full scripting, dynamic execution, file and system access).

Use it when creating daily note templates, note scaffolds, frontmatter schemas, or reusable content blocks that auto-populate on note creation.

## Quick Start

```markdown
<!-- Core Templates: variables available anywhere in a template file -->
---
date: {{date}}
time: {{time}}
title: {{title}}
---

# {{title}}

Created: {{date:YYYY-MM-DD}}
```

```javascript
<%* /* Templater: dynamic frontmatter with scripting */ %>
---
date: <% tp.date.now("YYYY-MM-DD") %>
title: <% tp.file.title %>
week: <% tp.date.now("W") %>
tags: [daily]
---

# <% tp.file.title %>

## Tasks

## Notes

## Links
```

## Preferred Workflow

1. Start with the Core Templates plugin for simple note scaffolds that only need `{{title}}`, `{{date}}`, and `{{time}}` substitution.
2. Switch to Templater when templates require dynamic logic, user prompts, file operations, or external data.
3. Store all templates in a dedicated folder (e.g., `Templates/`) and configure the plugin to point there.
4. Name templates descriptively so the quick switcher or template picker can find them by keyword.
5. Test templates by creating a scratch note and inserting the template before deploying it vault-wide.

## Authoring Guidance

This skill is the right fit for:

- creating daily note, weekly review, or meeting note templates
- building project templates with pre-filled frontmatter
- authoring MOC or index note scaffolds
- injecting dynamic values such as today's date, current time, or note title at creation time
- using Templater's `tp.system.prompt()` to gather input when creating a note

## Template Organization

Keep templates in a flat Templates folder rather than nested subfolders.
Name templates with a consistent prefix or suffix (e.g., `TPL - Daily Note`, `TPL - Project`) to group them in the file picker.
Archive outdated templates by moving them to a `Templates/Archive/` subfolder rather than deleting them.

## Official References

Primary sources:

- Obsidian Core Templates: <https://help.obsidian.md/Plugins/Templates>
- Templater documentation: <https://silentvoid13.github.io/Templater/>

Deep-dive references for this skill:

- `references/core-templates-reference.md`
- `references/templater-syntax.md`
- `references/frontmatter-templates.md`
