# Plugin Data and BRAT

## Plugin directory structure

Each installed community plugin occupies a folder under `.obsidian/plugins/`:

```text
.obsidian/plugins/
  dataview/
    main.js           # Compiled plugin code
    manifest.json     # Plugin metadata (id, version, minAppVersion)
    styles.css        # Optional styles
    data.json         # Plugin settings/data (written by the plugin)
  templater-obsidian/
    main.js
    manifest.json
    data.json
```

## manifest.json

```json
{
  "id": "dataview",
  "name": "Dataview",
  "version": "0.5.67",
  "minAppVersion": "0.15.0",
  "description": "Complex data views for the Obsidian knowledge base.",
  "author": "Michael Brenan",
  "authorUrl": "https://github.com/blacksmithgu",
  "isDesktopOnly": false
}
```

## data.json

`data.json` stores all plugin-specific settings.
It is written and managed by the plugin at runtime.
Back up `data.json` files alongside the vault to preserve plugin configuration.

When migrating a vault, copy the entire `.obsidian/plugins/<id>/` folder to the new vault location.
Re-enable the plugin in Settings → Community Plugins after moving.

## community-plugins.json

`.obsidian/community-plugins.json` lists the IDs of all enabled plugins:

```json
["dataview", "templater-obsidian", "obsidian-git", "calendar"]
```

This file does not install plugins — it only marks which installed plugins are enabled.
On a new machine, install each plugin from the directory first, then enable them.

## BRAT (Beta Reviewers Auto-update Tool)

BRAT installs plugins directly from GitHub repositories, bypassing the community directory.
Use it for beta plugins, forks, or plugins under active development.

Installing a plugin with BRAT:

1. Install and enable BRAT from the community plugin directory.
2. Open Settings → BRAT → Add Beta Plugin.
3. Enter the GitHub repository URL (e.g., `https://github.com/author/plugin-repo`).
4. Optionally pin to a specific release tag for stability.
5. BRAT installs the plugin and adds it to the standard plugins list.

BRAT also provides a command to check for beta plugin updates.

## Git considerations

Exclude built plugin files from version control if tracking vault config:

```gitignore
.obsidian/plugins/*/main.js
.obsidian/plugins/*/styles.css
```

Commit `manifest.json` and `data.json` to preserve versions and settings.
The community plugin manifests serve as a lockfile for plugin versions.
