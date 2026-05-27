# CI/CD Automation

Use this reference for pipelines and unattended Microsoft 365 automation.

## Preferred Auth by Runtime

| Runtime | Preferred auth | Notes |
| --- | --- | --- |
| GitHub Actions | `federatedIdentity` when available | Avoids long-lived secrets |
| Azure-hosted jobs | `identity` when available | Managed identity reduces secret handling |
| Generic CI | `certificate` | Use protected variables and short-lived runners |
| Legacy CI | `password` only when unavoidable | MFA and security defaults can block it |

Do not use secret auth for SharePoint command workflows.

## Pipeline Pattern

```bash
npm install -g @pnp/cli-microsoft365
export NO_UPDATE_NOTIFIER=1
m365 version --output text
m365 login --authType certificate --appId "$ENTRA_APP_ID" --tenant "$TENANT_ID" --certificateFile "$CERT_FILE" --thumbprint "$THUMBPRINT"
m365 status --output text
# run read or deployment commands
m365 logout
```

For persistent runners, ensure teardown runs even on failure.

For PowerShell-based pipelines, set `$env:NO_UPDATE_NOTIFIER='1'` instead of the shell-style assignment shown above.

## Output Standards

Use `--output json` for machine parsing and `--query` for controlled projection. Keep `--debug` output out of normal CI
logs because it can expose request details that are inappropriate for broad log retention.

## Context Files

`.m365rc.json` can store non-secret defaults such as site URLs, environment names, or list names. Do not put secrets,
tokens, certificates, passwords, or tenant-private values in committed context files.
