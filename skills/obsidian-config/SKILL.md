---
name: obsidian-config
description: Use when a task involves configuring an Obsidian vault, editing .obsidian/
  settings files, managing workspace layout, hotkeys, appearance, themes, CSS snippets,
  or setting up vault sync and backup.
---

# Obsidian Config

## Intent Router

Load sections based on the task:

- `.obsidian/` file layout and core settings → `references/vault-settings-reference.md`
- Community themes, CSS snippets, and appearance → `references/themes-and-snippets.md`
- Workspace layout, Obsidian Sync, Git backup, and mobile → `references/workspace-and-sync.md`

## Overview

This skill covers Obsidian vault configuration: the `.obsidian/` settings folder, workspace layout files, hotkey assignment, appearance and theming, CSS snippet authoring, and vault sync and backup strategies.

Use it when setting up a new vault, migrating settings between vaults, debugging broken configuration, or applying appearance customizations that go beyond built-in theme options.

## Quick Start

```bash
# View the .obsidian/ folder in a file manager or terminal
ls -la /path/to/vault/.obsidian/
# Key files: app.json, appearance.json, hotkeys.json, workspace.json, plugins/
```

```bash
# Apply a CSS snippet: create the file, then enable it in Obsidian
mkdir -p /path/to/vault/.obsidian/snippets/
echo ".cm-s-obsidian { font-family: 'JetBrains Mono', monospace; }" > /path/to/vault/.obsidian/snippets/custom-font.css
# Then: Settings → Appearance → CSS snippets → toggle on custom-font
```

## Preferred Workflow

1. Open Settings (Ctrl+, / Cmd+,) to change most configuration through the UI before editing JSON directly.
2. Edit `.obsidian/app.json` or `appearance.json` directly only for bulk migrations or scripted vault setup.
3. Place CSS snippet files in `.obsidian/snippets/` and toggle them per-vault in Settings → Appearance.
4. Export and import hotkeys by copying `.obsidian/hotkeys.json` between vaults.
5. Commit `.obsidian/` to Git (excluding `workspace.json`) to share settings across machines.

## Authoring Guidance

This skill is the right fit for:

- setting up a fresh vault with consistent settings
- copying configuration between vaults
- authoring and debugging CSS snippets for visual customization
- configuring hotkeys for custom commands or plugin actions
- choosing and applying a community theme
- setting up a Git-based backup or Obsidian Sync for a vault

## Appearance and Theming

Community themes install via Settings → Appearance → Themes → Manage.
Themes are stored in `.obsidian/themes/<theme-name>/`.
CSS snippets in `.obsidian/snippets/` override theme styles and can be toggled independently.
The `cssclass` frontmatter property applies per-note CSS classes for note-specific styling.

## Official References

Primary sources:

- Obsidian help: <https://help.obsidian.md>
- Obsidian CSS snippets: <https://help.obsidian.md/Extending+Obsidian/CSS+snippets>

Deep-dive references for this skill:

- `references/vault-settings-reference.md`
- `references/themes-and-snippets.md`
- `references/workspace-and-sync.md`
