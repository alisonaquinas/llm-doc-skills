# Command Surface

Use this reference for command discovery, help navigation, and broad command-family routing.

## Core Commands

The installed v11.8.0 help surface includes:

```text
docs, login, logout, request, search, setup, status, version
```

Use `m365 docs --output text` to get the docs URL and `m365 <command> --help` for local help.

## Command Groups

Raw help from v11.8.0 lists these top-level groups:

| Area | Groups |
| --- | --- |
| CLI/session | `cli`, `connection`, `context`, `util` |
| Identity/tenant | `app`, `entra`, `exo`, `tenant` |
| Search/files/API | `search`, `graph`, `external`, `file` |
| Collaboration | `booking`, `onedrive`, `onenote`, `outlook`, `planner`, `teams`, `todo`, `viva` |
| Power/compliance | `flow`, `pa`, `pp`, `purview` |
| SharePoint/dev | `adaptivecard`, `spe`, `spfx`, `spo`, `spp` |

`spo` is the largest family and should be handled with extra care because SharePoint operations often touch tenant,
site, list, page, file, permission, hub, app catalog, and SPFx deployment state.

## Standard Options

Most command pages expose:

```bash
m365 <command> --help
m365 <command> --help examples
m365 <command> --help permissions
m365 <command> --help response
m365 <command> --output json
m365 <command> --query "<JMESPath>"
m365 <command> --verbose
m365 <command> --debug
```

Prefer JSON output for automation and add `--query` only after confirming the response shape.

## Escape Hatches

Use `m365 request` when no dedicated command exists:

```bash
m365 request --method GET --url "https://graph.microsoft.com/v1.0/sites/root" --output json
```

Use `m365 util accesstoken get` for scripts that need a token for a specific resource. Treat tokens as secrets and avoid
printing them into logs.
