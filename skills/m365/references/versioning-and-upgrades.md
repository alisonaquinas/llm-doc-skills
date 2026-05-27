# Versioning and Upgrades

Use this reference before changing installed CLI versions or updating generated command references.

## Version Check

```bash
m365 version
npm list -g @pnp/cli-microsoft365 --depth=0
```

Record the CLI version when capturing command help snapshots.

## Upgrade Rules

- Pin versions in CI when command output shape matters.
- Review upstream upgrade guides before major upgrades.
- Re-run safe verification commands after upgrade.
- Refresh command-surface references from `m365 --help` and group help.
- Re-check commands that use `--query` because response shapes can change.

## Documentation Drift

The CLI has a fast release cadence. Treat public docs as the current authority for install requirements, command
permissions, auth caveats, and upgrade notes. When docs conflict with older local research, prefer current upstream docs
and note the difference explicitly.
