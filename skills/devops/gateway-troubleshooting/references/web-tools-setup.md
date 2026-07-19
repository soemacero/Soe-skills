# Web Tools Backend Reference

## Firecrawl Cloud

| Property | Value |
|----------|-------|
| Website | https://www.firecrawl.dev/ |
| Free tier | 500 pages/month |
| API key prefix | `fc-` |
| Env var | `FIRECRAWL_API_KEY` |
| Config yaml | `web.backend: firecrawl` + `web.use_gateway: false` |

**Pricing (as of 2025):** Free tier includes 500 credits. Paid from $19/mo for 5K credits.

## Firecrawl Self-Hosted

| Property | Value |
|----------|-------|
| Repo | https://github.com/nicholasgriffintn/firecrawl-selfhost |
| Env var URL | `FIRECRAWL_API_URL` |
| Env var key | `FIRECRAWL_API_KEY` |
| Config yaml | `web.backend: firecrawl` + `web.use_gateway: false` |

Requires Docker or Railway to deploy the self-hosted instance.

## Tavily

| Property | Value |
|----------|-------|
| Website | https://tavily.com/ |
| Free tier | 1000 searches/month |
| API key prefix | `tvly-` |
| Env var | `TAVILY_API_KEY` |
| Config yaml | `web.backend: tavily` + `web.use_gateway: false` |

**Pricing (as of 2025):** Free tier includes 1000 credits. Paid from $49/mo for 10K credits.
Tavily is **search-only** — it doesn't have an extract/scrape mode like Firecrawl.
