# Document Workflows

Use this reference when Microsoft 365 document libraries, SharePoint pages, files, or SPFx assets are involved.

## SharePoint Document Libraries

Common read-first pattern:

```bash
m365 spo set --url "https://contoso.sharepoint.com"
m365 spo list list --webUrl "https://contoso.sharepoint.com/sites/docs" --output json
m365 spo file list --webUrl "https://contoso.sharepoint.com/sites/docs" --folderUrl "Shared Documents" --output json
```

Before uploads, moves, deletes, app deployments, or permission changes, inspect command help and permissions. Confirm the
site URL, library or folder target, and overwrite behavior explicitly.

## File Operations

Use `spo file` commands for SharePoint-specific file operations and `file` commands for Microsoft Graph file workflows.
Do not assume the two families accept the same identifiers or permissions.

Safe upload planning checklist:

- Verify authentication status.
- Verify target site and library.
- Inspect `--help permissions`.
- Confirm overwrite policy.
- Keep a local copy of the input document.
- Prefer a test site before tenant-wide rollout.

## Pages and Publishing

SharePoint page commands can change visible intranet content. Use read/list/get commands before `set`, `add`, `remove`,
or `publish` commands. For generated HTML or Markdown-to-page workflows, preserve a source copy outside the tenant.

## SPFx and App Catalog

CLI for Microsoft 365 supports SPFx diagnostics, upgrades, package inspection, and workflow scaffolding. Validate the
local Node/SPFx version combination before applying generated upgrade guidance. For app catalog operations, use a custom
app registration with only the required permissions.

## Relationship to OOXML Skills

Use `docx-custom`, `pptx-custom`, `xlsx-custom`, and `office-custom` for local document file construction or inspection.
Use `m365` for tenant-side discovery, upload, download, publishing, app catalog, and SharePoint/Graph operations.
