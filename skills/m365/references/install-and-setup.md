# Install and Setup

Use this reference for local installation, setup, verification, and runtime selection for CLI for Microsoft 365.

## Install Paths

Stable global npm install:

```bash
npm install -g @pnp/cli-microsoft365
```

Beta channel:

```bash
npm install -g @pnp/cli-microsoft365@next
```

The upstream docs currently require a modern Node.js runtime. Verify the current upstream install page before stating a
hard minimum; prefer current Node LTS for new setups.

## Safe Verification

These checks do not call tenant APIs:

```bash
node --version
npm --version
m365 version --output text
m365 status --output text
m365 --help
m365 docs --output text
```

Expected unauthenticated status is `Logged out`.

On Windows, prefer `pwsh -NoProfile -File` when running the bundled PowerShell helper scripts so a user profile does not
add unrelated output to the verification step. If sandboxed or shared environments print update-check warnings, set
`NO_UPDATE_NOTIFIER=1` before running `m365`.

## Setup Wizard

`m365 setup` can configure defaults and create or reuse an Entra application. Treat it as an onboarding wizard, not a
production permission design. For production use, prefer a custom Entra application with only the permissions needed for
the selected command families.

Useful configuration checks:

```bash
m365 cli config list
```

`m365 cli doctor` is useful after login or when diagnosing an authenticated environment. It is not a reliable
pre-login verification step because it can fail while logged out.

## Runtime Options

Use global npm install for developer workstations and stable build agents. Use the project Docker image when isolation is
more important than host integration. In CI, install the CLI inside the job or use a pinned runner image, then run
`m365 logout` during teardown when a persistent runner is used.
