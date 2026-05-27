# Troubleshooting

Use this reference for common CLI for Microsoft 365 failure modes.

## Install and Path

If `m365` is not found:

```bash
node --version
npm --version
npm list -g @pnp/cli-microsoft365 --depth=0
```

Reinstall with `npm install -g @pnp/cli-microsoft365` if the package is absent.

On Windows, also verify that the global npm bin directory is on `PATH`. Running `npm bin -g` shows the directory that
should contain `m365.cmd`.

## Authentication

Run:

```bash
m365 status --output text
m365 connection list
```

`m365 connection list` can return `[]` while logged out, which is expected. Run `m365 cli doctor` only after login or
when validating an authenticated workstation, because it can fail with `Log in to Microsoft 365 first` on a logged-out
session.

If certificate auth fails, verify tenant, app ID, thumbprint, certificate format, and whether the Entra app is configured
for certificate credentials.

If a SharePoint command fails under secret auth, change auth mode. SharePoint command workflows require delegated,
certificate, or managed identity patterns rather than client secret auth.

## Permissions

For `403` or access-denied errors:

```bash
m365 <command> --help permissions
```

Check both app permissions and the delegated user's actual access. SharePoint app-only workflows may need both Graph
permissions for discovery and SharePoint permissions for the target operation.

## Output and Parsing

If a script breaks after an upgrade, compare:

```bash
m365 version --output text
m365 <command> --help response
```

Prefer explicit `--query` projections and pin CLI versions in CI when output shape matters.

If non-interactive or sandboxed runs print repeated update-check warnings, set `NO_UPDATE_NOTIFIER=1` for the shell
session before running `m365`.
