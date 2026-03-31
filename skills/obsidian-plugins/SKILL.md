---
name: obsidian-plugins
description: Use when a task involves managing Obsidian plugins, enabling or
  configuring community or core plugins, installing beta plugins via BRAT,
  or working with plugin data files inside a vault.
---

# Obsidian Plugins

## Intent Router

Load sections based on the task:

- Core (built-in) plugin list and configuration → `references/core-plugins-reference.md`
- Community plugin installation, safe mode, and popular plugins → `references/community-plugins-guide.md`
- Plugin data files, `.obsidian/plugins/` structure, and BRAT → `references/plugin-data-and-brat.md`

## Overview

This skill covers Obsidian plugin management: enabling and configuring core (built-in) plugins, installing and updating community plugins, managing plugin data files inside the vault, and installing pre-release plugins via BRAT.

Use it when setting up a plugin-heavy vault, auditing which plugins are active, debugging plugin conflicts, or automating vault configuration that includes plugin state.

## Quick Start

```bash
# List installed community plugins in a vault
ls /path/to/vault/.obsidian/plugins/

# Inspect a plugin's stored data
cat /path/to/vault/.obsidian/plugins/dataview/data.json
```

```bash
# Validate plugin manifest JSON
python -c "import json; json.load(open('/path/to/vault/.obsidian/plugins/templater-obsidian/manifest.json'))"

# Check which community plugins are enabled
cat /path/to/vault/.obsidian/community-plugins.json
```

## Preferred Workflow

1. Enable community plugins first: Settings → Community Plugins → toggle off Restricted Mode.
2. Browse and install via Settings → Community Plugins → Browse — search by name or keyword.
3. After installing, open each plugin's settings page to configure it before use.
4. Audit `.obsidian/community-plugins.json` when migrating a vault to another machine — installed plugins need reinstalling on the new machine.
5. Use BRAT only for plugins not yet published to the community directory; pin to a specific release tag for stability.

## Authoring Guidance

This skill is the right fit for:

- enabling or disabling core and community plugins
- configuring plugin behavior through settings
- installing beta or pre-release plugins via BRAT
- scripting vault setup that includes plugin state
- debugging plugin conflicts or broken plugin data files
- auditing plugin permissions and data storage

## Plugin Conflicts

Plugins occasionally conflict when two plugins bind the same hotkey or patch the same editor behavior.
Disable plugins one at a time to isolate a conflict.
The developer console (Ctrl+Shift+I / Cmd+Option+I) shows JavaScript errors from failing plugins.

## Official References

Primary sources:

- Obsidian community plugins: <https://obsidian.md/plugins>
- Obsidian help — plugins: <https://help.obsidian.md/Extending+Obsidian/Community+plugins>

Deep-dive references for this skill:

- `references/core-plugins-reference.md`
- `references/community-plugins-guide.md`
- `references/plugin-data-and-brat.md`
