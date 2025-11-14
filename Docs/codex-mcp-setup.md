# Configuring Codex for MCP Servers

Use this guide to wire the Google Analytics MCP server (or any other MCP service) into Codex. Codex expects MCP servers to be declared in a top-level `[mcp_servers]` table inside your Codex configuration file—usually `~/.config/codex/settings.toml` or the platform equivalent.

## Basic STDIO Configuration
Most local MCP servers, including this Google Analytics project, run via STDIO.

```toml
# The top-level table name must be `mcp_servers`.
[mcp_servers.analytics_ga]
command = "docker"
args = [
  "run",
  "--rm",
  "-i",
  "-e", "GOOGLE_APPLICATION_CREDENTIALS=/creds.json",
  "-v", "/Users/<user>/keys/analytics.json:/creds.json:ro",
  "analytics-mcp:latest"
]
```

Add additional `-e` / `-v` arguments to match your credential and configuration
needs. Build the `analytics-mcp:latest` image with `make docker-build` (run by
default within `make launch`).

Reference whitelist: https://github.com/openai/codex/blob/main/codex-rs/rmcp-client/src/utils.rs#L82

### Optional timeouts and tool filters

```toml
[mcp_servers.analytics_ga]
startup_timeout_sec = 20      # default is 10s
tool_timeout_sec = 60         # default is 60s
enabled = true                # set to false to disable without removing
enabled_tools = ["run_report", "get_property_details"]
disabled_tools = ["get_property_annotations"]
```

Codex first enforces `enabled_tools` (allow-list) and then applies `disabled_tools` (deny-list).

## Streamable HTTP Servers
If your MCP server is accessible via HTTP, configure it like this:

```toml
[mcp_servers.analytics_http]
url = "https://analytics.example.com/mcp"
bearer_token_env_var = "GA_MCP_TOKEN"     # optional
http_headers = { "X-Tenant" = "clientA" } # optional static headers
env_http_headers = { "X-Auth" = "GA_AUTH_TOKEN" } # optional env-driven headers
```

HTTP servers use the experimental Rust MCP client; enable it in your config:

```toml
experimental_use_rmcp_client = true
```

After enabling the flag, you can complete OAuth flows when supported:

```sh
codex mcp login analytics_http
```

## MCP CLI Commands

```
codex mcp --help                      # list commands
codex mcp add ga -- docker run --rm -i analytics-mcp:latest
codex mcp list                        # list servers (table)
codex mcp list --json                 # list servers (JSON)
codex mcp get ga                      # describe one server (table)
codex mcp get ga --json               # describe one server (JSON)
codex mcp remove ga                   # delete a server
codex mcp login analytics_http        # OAuth login for HTTP server
codex mcp logout analytics_http       # revoke OAuth session
```

`make launch` in the repository automatically builds the Docker image, registers
the `docker run --rm -i ... analytics-mcp:latest` command with Codex (if the
`codex` CLI is installed), and then starts the container. Override the `CODEX`,
`MCP_SERVER_NAME`, or `DOCKER_RUN_FLAGS` variables to tailor the registration.

## Tips
- Keep credentials scoped to read-only access when possible.  
- If you disabled ADC by default in the server (`ANALYTICS_MCP_ALLOW_ADC` unset), ensure each request provides explicit credentials or set the env var when launching via Codex.  
- Use separate `mcp_servers` entries if you need different env vars per tenant.  
- Re-run `codex mcp list` after editing the TOML to confirm Codex picked up the new configuration.
