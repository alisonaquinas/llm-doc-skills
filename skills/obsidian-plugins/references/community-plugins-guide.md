# Community Plugins Guide

Community plugins are third-party extensions installable from the Obsidian plugin directory.

## Enabling community plugins

Community plugins are disabled by default under Restricted Mode.
To enable them: Settings → Community Plugins → turn off Restricted Mode → confirm.

After disabling Restricted Mode, a Browse button appears to open the plugin directory.

## Installing a plugin

1. Settings → Community Plugins → Browse
2. Search by name or keyword
3. Click Install on the plugin page
4. Click Enable after installation completes
5. Open the plugin's settings page to configure it

Plugins are stored in `.obsidian/plugins/<plugin-id>/`.

## Popular community plugins

| Plugin | Purpose |
| --- | --- |
| Dataview | SQL-like queries to build tables and lists from note metadata |
| Templater | Advanced template engine with JavaScript scripting |
| Calendar | Calendar view linked to daily notes |
| Tasks | Task management with due dates, recurrence, and filters |
| Obsidian Git | Automated Git commit, push, and pull on a schedule |
| Advanced Tables | Spreadsheet-like table editor for Markdown tables |
| Excalidraw | Hand-drawn diagram embedding inside notes |
| Kanban | Kanban board view for task tracking |
| Style Settings | UI for configuring theme variables |
| BRAT | Install and update beta and pre-release plugins |
| Linter | Lint and auto-format note content and frontmatter |
| Periodic Notes | Extended daily, weekly, and monthly note management |

## Updating plugins

Settings → Community Plugins → installed plugins list → Check for updates → Update All.
Obsidian does not auto-update plugins; check for updates regularly.

## Disabling and removing plugins

Toggle off a plugin from the installed plugins list to disable it without deleting data.
To fully remove: disable, then click the delete icon, or delete the folder from `.obsidian/plugins/<id>/`.
Plugin data (settings) lives in `.obsidian/plugins/<id>/data.json` and persists after reinstall.
