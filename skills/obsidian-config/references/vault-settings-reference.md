# Vault Settings Reference

The `.obsidian/` folder at the vault root stores all per-vault configuration.
It is created automatically when Obsidian first opens a folder as a vault.

## Key files

| File | Purpose |
| --- | --- |
| `app.json` | Core editor and UI settings (line width, spellcheck, vim mode, etc.) |
| `appearance.json` | Theme name, font choices, dark/light mode, font size |
| `hotkeys.json` | Custom key bindings for commands |
| `workspace.json` | Open panes, sidebar state, last-opened file |
| `community-plugins.json` | List of installed community plugin IDs |
| `core-plugins.json` | Which core plugins are enabled |
| `plugins/<id>/` | Plugin installation folder with `main.js`, `manifest.json`, `data.json` |
| `themes/<name>/` | Installed community theme files |
| `snippets/` | Custom CSS snippet files |

## app.json common keys

```json
{
  "spellcheck": true,
  "spellcheckLanguages": ["en"],
  "vimMode": false,
  "readableLineLength": true,
  "showLineNumber": false,
  "livePreview": true
}
```

## appearance.json common keys

```json
{
  "theme": "Minimal",
  "cssTheme": "Minimal",
  "interfaceFontFamily": "",
  "textFontFamily": "",
  "monospaceFontFamily": "",
  "baseFontSize": 16,
  "translucency": false
}
```

## Editing settings files directly

Close Obsidian before editing JSON files to avoid overwrite conflicts.
Validate JSON with `python -c "import json; json.load(open('.obsidian/app.json'))"` before reopening.
Settings take effect on next Obsidian launch or on Settings reload.

## Git considerations

Commit `.obsidian/` to share settings between machines.
Exclude `workspace.json` since it changes on every session:

```gitignore
.obsidian/workspace.json
.obsidian/workspace-mobile.json
```
