---
name: hermes-web-tools-setup
description: "Diagnose, configure, and swap Hermes web search/extract backends. Covers DuckDuckGo (free), Firecrawl, Tavily, Brave, and others — no API key required options, plugin discovery, and troubleshooting."
version: 1.0.0
author: Hermes Agent
tags: [hermes, web, search, firecrawl, tavily, ddgs, brave, configuration, troubleshooting]
trigger: user reports web_search or web_extract failing, or you see 'FIRECRAWL_API_KEY' / 'Web tools are not configured' errors
---

# Hermes Web Tools Setup

Web search (`web_search`) and web extraction (`web_extract`) need a configured backend. Hermes ships with several plugin backends. When the default (`firecrawl`) lacks credentials, swap to a free alternative like DuckDuckGo (ddgs) — no API key, zero config.

## Quick fix: DuckDuckGo (free, no API key)

```bash
# 1. Install the Python package
uv pip install ddgs

# 2. Switch backend via hermes config
hermes config set web.backend ddgs
hermes config set web.search_backend ddgs
hermes config set web.extract_backend ddgs
hermes config set web.use_gateway false
```

**Limitation:** ddgs is search-only. `web_extract` will not work with ddgs as the extract backend. If you need extraction too, use Firecrawl or Tavily.

## Available backends

List plugin-provided web backends:

```bash
find /root/.local/share/uv/tools/hermes-agent/lib/python3.12/site-packages/plugins/web/ -maxdepth 2 -name "plugin.yaml" -exec grep -l "provides_web_providers" {} \;
```

Common ones bundled with Hermes:

| Plugin | Package to install | API key? | Supports |
|--------|-------------------|----------|----------|
| `ddgs` | `uv pip install ddgs` | ❌ No | search only |
| `brave-free` | `uv pip install brave-search` | ✅ `BRAVE_SEARCH_API_KEY` (free tier: 2k/mo) | search |
| `searxng` | None (self-hosted) | ❌ No (needs SearXNG instance) | search + extract |
| `xai` | None (uses xAI/Grok) | ✅ `XAI_API_KEY` | search |
| `firecrawl` | Bundled | ✅ `FIRECRAWL_API_KEY` or `use_gateway: true` (Nous Portal) | search + extract |
| `tavily` | Bundled | ✅ `TAVILY_API_KEY` | search + extract |

## Jina AI Reader (free, no API key — web extraction fallback)

[Jina Reader](https://r.jina.ai) is a free web extraction service that needs no API key and no registration. It works as a simple HTTP proxy: `https://r.jina.ai/<URL>` returns clean markdown.

**Limitation:** Hermes' native `web_extract` tool does NOT support Jina as a configurable backend. To use Jina, call it directly:

```python
# In execute_code
import requests
r = requests.get(f"https://r.jina.ai/{target_url}", timeout=30,
                 headers={"User-Agent": "Mozilla/5.0"})
print(r.text[:15000])
```

Or via curl:
```bash
curl -s "https://r.jina.ai/https://example.com"
```

If you set `extract_backend: jina` in `/data/config.yaml`, it will NOT make the `web_extract` tool use Jina — it's not a valid backend option. A **gateway restart is still required** after any config change for the backend to take effect (see pitfalls below).

## Diagnosis workflow

When web tools fail:

1. **Check the error** — the tool output tells you which env var is missing:
   ```
   Error searching web: Web tools are not configured. Set FIRECRAWL_API_KEY...
   ```

2. **Check current config:**
   ```bash
   hermes config get web.backend
   hermes config get web.use_gateway
   ```

3. **Check .env for the required key:**
   ```bash
   grep FIRECRAWL /data/.env 2>/dev/null || echo "Not set"
   ```

4. **Check plugin registration** in agent.log:
   ```bash
   grep "registered web provider" /data/logs/agent.log | tail -5
   ```

5. **Check if the package is installed:**
   ```bash
   uv pip list 2>/dev/null | grep -iE "ddgs|tavily|firecrawl|brave"
   ```

6. **Pick the cheapest option** — prefer ddgs (free, no signup) for search. For extraction, fall back to Firecrawl with your own key or Tavily.

## Firecrawl (API key) setup

```bash
# Add to /data/.env
echo 'FIRECRAWL_API_KEY=your-key-here' >> /data/.env

# Or use Nous Portal OAuth (use_gateway: true) — runs `hermes model` to auth
```

Free tier: 500 pages/month at firecrawl.dev.

## Tavily setup

```bash
uv pip install tavily-python
hermes config set web.backend tavily
hermes config set web.search_backend tavily
hermes config set web.extract_backend tavily
hermes config set web.use_gateway false
echo 'TAVILY_API_KEY=your-key-here' >> /data/.env
```

Free tier: 1,000 searches/month at tavily.com.

## Pitfalls

- **ddgs is search-only.** `web_extract` returns `"DuckDuckGo (ddgs) is a search-only backend and cannot extract URL content. Set web.extract_backend to firecrawl, tavily, exa, or parallel."` if extract_backend is ddgs. Use a different backend for extraction or fall back to `execute_code` with `requests` for scraping individual URLs (works for simple cases):
  ```python
  import requests
  r = requests.get("https://example.com", timeout=15, headers={"User-Agent": "Mozilla/5.0"})
  print(r.text[:10000])
  ```
- **Config changes require a gateway restart** — unlike some tool configs, `web.backend` / `web.extract_backend` are loaded at gateway startup. The old backend's error will persist until the gateway is restarted. Systemd: `systemctl restart hermes-gateway`. Bare process: `kill -TERM <pid> && ...`.
- **`use_gateway: true`** expects OAuth through Nous Portal. If you don't have portal auth, set it to `false` and configure a direct API key.
- **Some plugins auto-install** their dependencies on first use; ddgs, tavily, and brave-free do NOT — you must `uv pip install` them explicitly.
- **After changing backends**, the agent logs show a line like `Plugin 'web-ddgs' registered web provider: ddgs` — verify it appears.
