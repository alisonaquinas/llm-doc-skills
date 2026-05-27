---
name: m365
description: >
  Use when working with CLI for Microsoft 365 (`m365`) for document libraries,
  SharePoint pages and files, SPFx assets, Microsoft 365 tenant inspection,
  command help lookup, installation, authentication, CI/CD automation, MCP server
  setup, or troubleshooting. Triggers include "install m365", "use CLI for
  Microsoft 365", "automate SharePoint documents", "check m365 permissions",
  and "configure m365 MCP".
---

# CLI for Microsoft 365

Use CLI for Microsoft 365 to inspect and automate Microsoft 365 document, SharePoint, SPFx, and tenant workflows.

## Intent Router

- Install, runtime setup, or safe local verification -> `references/install-and-setup.md`
- Login, auth mode selection, tenant permissions, or credential safety -> `references/authentication-and-permissions.md`
- Command discovery, help output, command groups, `--query`, or `request` -> `references/command-surface.md`
- SharePoint document libraries, pages, files, app catalog, or SPFx assets -> `references/document-workflows.md`
- CI/CD, GitHub Actions, Azure-hosted automation, or persistent runners -> `references/ci-cd-automation.md`
- MCP server setup or agent-tool integration -> `references/mcp-server.md`
- Errors, access denied, install failures, or output parsing breakage -> `references/troubleshooting.md`
- CLI upgrades, pinned versions, or regenerated help snapshots -> `references/versioning-and-upgrades.md`

## Quick Start

Safe verification commands:

```bash
node --version
npm --version
m365 version --output text
m365 status --output text
m365 --help
m365 docs --output text
```

Install the stable CLI:

```bash
npm install -g @pnp/cli-microsoft365
```

Inspect a command before use:

```bash
m365 spo file list --help
m365 spo file list --help permissions
m365 spo file list --help examples
```

## Safety Rules

1. Verify the command with local help before running tenant-affecting operations.
2. Inspect `--help permissions` before designing authenticated workflows.
3. Require explicit tenant, site, library, environment, or app targets for write operations.
4. Prefer read/list/get commands before add/set/remove/delete/deploy/publish commands.
5. Avoid `secret` auth for SharePoint command workflows.
6. Treat tokens, certificates, passwords, connection files, and access-token output as secrets.
7. Run `m365 logout` during teardown on shared, persistent, or disposable automation hosts.

## Common Workflows

### Local Setup

```bash
npm install -g @pnp/cli-microsoft365
m365 version --output text
m365 status --output text
m365 docs --output text
```

Load `references/install-and-setup.md` for runtime and setup details. Run `m365 cli doctor` only after login, because
it can fail on a logged-out workstation.

### Human Operator Login

```bash
m365 login --authType browser --tenant contoso.onmicrosoft.com --connectionName admin-workstation
m365 status --output text
```

Load `references/authentication-and-permissions.md` before selecting unattended auth.

### SharePoint Document Library Inspection

```bash
m365 spo set --url "https://contoso.sharepoint.com"
m365 spo list list --webUrl "https://contoso.sharepoint.com/sites/docs" --output json
```

Load `references/document-workflows.md` before upload, overwrite, publish, app catalog, or SPFx operations; confirm the
target and backup or rollback path first.

### Automation Output

```bash
m365 tenant info get --output json
m365 tenant serviceannouncement message list --output json --query "[].{title:title,id:id}"
```

Use JSON output and explicit JMESPath projections for scripts.

### MCP Server

```bash
npm install -g @pnp/cli-microsoft365-mcp-server@latest
m365 cli config set --key prompt --value false
m365 cli config set --key helpMode --value full
```

Load `references/mcp-server.md` before connecting authenticated tenant access to agent tooling.

## Windows Notes

- Prefer `pwsh -NoProfile -File skills/m365/scripts/verify-m365-install.ps1` and
  `pwsh -NoProfile -File skills/m365/scripts/collect-m365-help.ps1` to avoid user-profile noise during verification.
- If non-interactive runs print update-check warnings, set `NO_UPDATE_NOTIFIER=1` for that shell session before running
  `m365`.
- Use `--output text` for scalar checks such as `version`, `status`, and `docs` to avoid quoted JSON-string output in
  scripts.

## Resource Index

| Reference | Load when |
| --- | --- |
| `references/install-and-setup.md` | Installing, verifying, or configuring local runtime |
| `references/authentication-and-permissions.md` | Logging in, choosing auth, or planning permissions |
| `references/command-surface.md` | Discovering commands, help sections, or output options |
| `references/document-workflows.md` | Working with SharePoint files, pages, libraries, SPFx, or app catalogs |
| `references/ci-cd-automation.md` | Running m365 in pipelines or unattended jobs |
| `references/mcp-server.md` | Configuring the m365 MCP server |
| `references/troubleshooting.md` | Diagnosing install, auth, access, or output issues |
| `references/versioning-and-upgrades.md` | Pinning, upgrading, or refreshing command snapshots |
