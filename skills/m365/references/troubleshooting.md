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

## Authentication

Run:

```bash
m365 status
m365 connection list
m365 cli doctor
```

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
m365 version
m365 <command> --help response
```

Prefer explicit `--query` projections and pin CLI versions in CI when output shape matters.
