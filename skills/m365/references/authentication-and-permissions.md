# Authentication and Permissions

Use this reference before any authenticated `m365` workflow.

## Authentication Types

`m365 login` supports these auth types:

- `deviceCode` - default delegated sign-in; useful when browser launch is unavailable.
- `browser` - delegated interactive sign-in; preferred for human operators when available.
- `password` - delegated username/password; avoid unless a legacy constraint requires it.
- `certificate` - app-only automation with a certificate.
- `secret` - app-only automation with a client secret.
- `identity` - managed identity for Azure-hosted runtimes.
- `federatedIdentity` - workload identity, documented for GitHub Actions.

Example delegated login:

```bash
m365 login --authType browser --tenant contoso.onmicrosoft.com --connectionName admin-workstation
```

Example certificate login pattern:

```bash
m365 login --authType certificate --appId "$ENTRA_APP_ID" --tenant "$TENANT_ID" --certificateFile ./cert.pem --thumbprint "$THUMBPRINT"
```

## Permission Rules

Always inspect command permissions before designing a tenant change:

```bash
m365 spo site list --help permissions
m365 entra app add --help permissions
```

Delegated flows require both app consent and user access. App-only flows require application permissions and do not behave
the same as delegated flows. Some commands do not support app-only execution.

Important limitation: do not use `secret` auth for SharePoint command workflows. Use certificate auth, managed identity,
or delegated auth instead.

## Configuration Precedence

For `appId` and `tenant`, the CLI resolves explicit login options first, then CLI config, then environment variables such
as `CLIMICROSOFT365_ENTRAAPPID` and `CLIMICROSOFT365_TENANT`.

## Security Guardrails

- Prefer custom Entra app registrations with narrow permissions for production.
- Treat persisted connection files as sensitive; upstream docs describe them as JSON and not encrypted.
- Use trusted workstations, hardened build agents, or ephemeral runners.
- Call `m365 logout` during teardown on shared or persistent hosts.
- Do not commit app IDs, tenant IDs, secrets, certificates, tokens, or exported connection state.
