# Themes and CSS Snippets

Obsidian supports community themes and per-vault CSS snippet overrides for visual customization.

## Community themes

Browse and install themes via Settings → Appearance → Themes → Manage.
Themes are stored in `.obsidian/themes/<theme-name>/` and consist of a `theme.css` file and `manifest.json`.

Popular themes include Minimal, Things, AnuPpuccin, Blue Topaz, and Sanctum.
Each theme may expose style settings via the Style Settings community plugin.

To switch themes: Settings → Appearance → Themes → select from dropdown.
To remove a theme: delete its folder from `.obsidian/themes/` and reset the theme to Default.

## CSS snippets

Snippets are individual CSS files in `.obsidian/snippets/`.
They load on top of the active theme and can be toggled independently.

To add a snippet:

1. Create a `.css` file in `.obsidian/snippets/` — for example, `custom-font.css`.
2. Open Settings → Appearance → CSS snippets → click the reload button.
3. Toggle the snippet on.

Example snippet — monospace font in the editor:

```css
.cm-s-obsidian {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}
```

Example snippet — wider readable line width:

```css
.markdown-preview-view,
.cm-s-obsidian .cm-content {
  max-width: 900px;
}
```

## Per-note CSS classes

Add a `cssclass` property in a note's frontmatter to apply a CSS class only to that note:

```yaml
---
cssclass: wide-table
---
```

Then target it in a snippet:

```css
.wide-table table {
  width: 100%;
}
```

## Debugging styles

Use the developer console (Ctrl+Shift+I / Cmd+Option+I) to inspect rendered elements and identify which CSS rules apply.
The console also shows JavaScript errors from plugins.
