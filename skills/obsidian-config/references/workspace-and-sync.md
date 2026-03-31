# Workspace and Sync

## Workspace layout

`workspace.json` stores the current pane layout, sidebar state, and last-opened file.
It updates on every Obsidian session close and should not be committed to Git in shared vaults since it causes frequent merge conflicts.

To restore a workspace layout across machines, use the Workspaces core plugin:
Settings → Core Plugins → Workspaces.
Save a named workspace snapshot; it persists in `.obsidian/` as part of `workspace.json` under a `workspaces` key.

## Obsidian Sync

Obsidian Sync is the official paid sync service.
It encrypts vault contents end-to-end and syncs across desktop and mobile.

Configuration: Settings → Sync → log in with Obsidian account → select or create a remote vault.

Sync selective folders by toggling them in Settings → Sync → Selective sync.
Plugin configs and community plugins sync by default; toggle off if managing plugins per device.

## Git-based backup

A Git repository in the vault root provides version history and device sync when combined with a remote like GitHub or Gitea.

Recommended `.gitignore` for an Obsidian vault:

```gitignore
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.trash/
.DS_Store
```

The Obsidian Git community plugin automates commits and push/pull on a schedule.
Configure it via Settings → Community Plugins → Obsidian Git → Options.

## Mobile sync

Obsidian mobile uses the same vault format.
Options for mobile sync:

- **Obsidian Sync** — simplest, official, paid
- **iCloud Drive / iCloud** — on iOS, place vault inside iCloud Drive folder
- **Working Copy + Obsidian Git** — Git-based sync on iOS using Working Copy app
- **Syncthing** — open-source peer-to-peer sync on Android and desktop
