# MCP Server

Use this reference when connecting agent tooling to CLI for Microsoft 365 through the MCP server.

## Role

The MCP server is adjacent tooling for agent access to the CLI. It is not the same thing as the `m365` binary, and it
inherits the risk profile of the authenticated CLI session beneath it.

## Install

```bash
npm install -g @pnp/cli-microsoft365-mcp-server@latest
```

Upstream docs also show stdio use with:

```bash
npx -y @pnp/cli-microsoft365-mcp-server@latest
```

## Recommended CLI Config

Current upstream docs recommend:

```bash
m365 cli config set --key prompt --value false
m365 cli config set --key output --value text
m365 cli config set --key helpMode --value full
```

Apply these settings only when they fit the local workflow. For scripted command execution outside MCP, JSON output is
usually better than text output.

## Safety

- Configure MCP only after deciding which tenant and identity it may control.
- Prefer least-privilege app registrations.
- Avoid authenticated MCP sessions on shared machines.
- Keep destructive operations behind explicit operator approval.
