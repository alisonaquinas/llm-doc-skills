# Templater Syntax

Templater is a community plugin that extends Obsidian templates with a full scripting environment.
Templates run JavaScript-like expressions inside `<% %>` tags when a template is inserted or triggered.

## Tag types

| Tag | Purpose |
| --- | --- |
| `<% expression %>` | Evaluate and output the result |
| `<%* statement %>` | Execute JavaScript without output (side effects only) |
| `<%= expression %>` | Explicitly output the expression value (same as `<% %>`) |
| `<%- expression %>` | HTML-escaped output |

## tp.date functions

```javascript
<% tp.date.now() %>                         // Today in default format
<% tp.date.now("YYYY-MM-DD") %>             // Today as ISO date
<% tp.date.now("dddd, MMMM D") %>          // Today as "Wednesday, January 15"
<% tp.date.tomorrow("YYYY-MM-DD") %>        // Tomorrow
<% tp.date.yesterday("YYYY-MM-DD") %>       // Yesterday
<% tp.date.now("YYYY-MM-DD", 7) %>          // 7 days from today
<% tp.date.now("YYYY-MM-DD", -7) %>         // 7 days ago
```

## tp.file functions

```javascript
<% tp.file.title %>                         // Current file title (without extension)
<% tp.file.folder() %>                      // Folder containing the current file
<% tp.file.path() %>                        // Full vault path to the file
<% tp.file.creation_date("YYYY-MM-DD") %>   // File creation date
<% tp.file.last_modified_date() %>          // Last modified date
<% tp.file.cursor() %>                      // Place cursor here after insertion
<% tp.file.cursor(1) %>                     // Named cursor position 1
```

## tp.frontmatter

```javascript
<% tp.frontmatter.tags %>                   // Read the tags property
<% tp.frontmatter["custom-key"] %>          // Read any frontmatter key
```

## tp.system functions

```javascript
<% await tp.system.prompt("Enter title:") %>          // Show an input dialog
<% await tp.system.suggester(["A","B"], ["a","b"]) %> // Show a picker dialog
<% tp.system.clipboard() %>                            // Read clipboard contents
```

## Script blocks

Use `<%* ... %>` for logic that runs without producing output:

```javascript
<%*
const noteTitle = tp.file.title;
const isDaily = noteTitle.match(/^\d{4}-\d{2}-\d{2}$/);
if (isDaily) {
  tR += "## Daily Entry\n";
} else {
  tR += "## Note\n";
}
-%>
```

## Startup templates

Configure a template to run automatically when Obsidian starts:
Settings → Templater → Startup Templates → add template file path.
Startup templates run once per session and are useful for opening a daily note automatically.
