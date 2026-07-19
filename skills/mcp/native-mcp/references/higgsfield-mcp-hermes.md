# Higgsfield MCP + Hermes

Connecting Higgsfield's MCP server to Hermes Agent for AI video/image generation.

## Higgsfield MCP Server

- URL: `https://mcp.higgsfield.ai/mcp`
- Transport: Streamable HTTP
- Auth: OAuth (via browser) or Bearer token (via API key from cloud.higgsfield.ai/api-keys)
- Models: 30+ including Sora, Kling 3.0, Veo 3.1, Seedance, etc.

## Hermes Config (with API key)

```yaml
mcp_servers:
  higgsfield:
    url: "https://mcp.higgsfield.ai/mcp"
    headers:
      Authorization: "Bearer YOUR_API_KEY"
    timeout: 180
```

## Getting an API key

1. Go to https://cloud.higgsfield.ai/api-keys
2. Sign in / create account
3. Generate a new API key
4. Use it as Bearer token in config above

## OAuth limitation

The MCP server's native auth is browser-based OAuth. When running Hermes on a headless server (no browser), you MUST use an API key from cloud.higgsfield.ai/api-keys instead. The MCP endpoint returns `401 Unauthorized` with `WWW-Authenticate: Bearer resource_metadata="..."` when no token is provided.

## Verified tools (from MCP discovery)

After connecting, tools appear as `mcp_higgsfield_*` in the Hermes tool registry. Common tools include:
- `mcp_higgsfield_generate_video`
- `mcp_higgsfield_generate_image`
- `mcp_higgsfield_list_models`

## Alternative: Open-Higgsfield-AI (local fork)

Community open-source clone: https://github.com/Mr-Moon121/open-higgsfield-ai
- 200+ models, local inference
- Uses Muapi backend
- Runs on GPU (ComfyUI-compatible)
- No filters, no subscriptions
