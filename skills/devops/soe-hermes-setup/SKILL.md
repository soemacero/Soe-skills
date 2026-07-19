---
name: soe-hermes-setup
description: "Complete reference for Soe's Hermes Agent setup on Hostinger VPS. Use this to train backup agents (Claude Code, local LLM) and for all maintenance tasks."
version: 3.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [soe, hermes, setup, vps, hostinger, deepseek, gateway, backup-agent, higgsfield]
    related_skills: [gateway-troubleshooting, hermes-gateway-setup]
---

# 🏗 Soe's Hermes Agent — Setup & Training Reference

> **Purpose:** This is the canonical reference for Soe's Hermes Agent.
> It combines fixes from TWO independent troubleshooting sessions (Claude Code + Hermes Agent) so no single point of failure is missed.
> **Read this entirely before making any changes.**

---

## 📋 Environment Overview

| Property | Value |
|---|---|
| **Host** | Hostinger VPS "srv1815278" (Linux 6.8.0) |
| **Python** | 3.12.3 (PEP 668 — use `uv`, no system pip) |
| **Hermes** | Installed via `uv tool install hermes-agent` |
| **Hermes binary** | `~/.local/share/uv/tools/hermes-agent/bin/hermes` |
| **Config** | `~/.hermes/config.yaml` |
| **Secrets** | `~/.hermes/.env` |
| **Systemd EnvironmentFile** | `/etc/default/hermes_gateway` |
| **Skills** | `~/.hermes/skills/` (symlinked to `/data/skills/`) |
| **Gateway** | `systemd --user` service (`hermes-gateway.service`) ✅ User-level ONLY |
| **Provider** | **DeepSeek** (`deepseek/deepseek-v4-flash`) |
| **API Keys present** | DeepSeek, Anthropic (fallback only), Telegram Bot |
| **Platform** | Telegram DM (Soe Macero) |
| **Toolsets** | `hermes-cli`, `vision` |
| **Web backend** | `firecrawl` via `use_gateway: true` (Tavily registered as backup) |
| **Notion** | API key and token configured |
| **GitHub repo** | `https://github.com/soemacero/Soe-skills` |
| **Higgsfield MCP** | Configured in `mcp_servers` — needs full gateway restart to activate |

---

## 🚨 CRITICAL RULES (Never Break These)

### Rule 1: DeepSeek is ALWAYS the default provider
Never change `model.provider` away from `deepseek` or `model.default` from `deepseek/deepseek-v4-flash`.

### Rule 2: Gateway restart from INSIDE is blocked
Use `systemctl --user reload` from inside. Restart only from Hostinger Web Terminal.

### Rule 3: Only ONE gateway service (user-level)
No system-level gateway. `sudo $(which hermes) gateway uninstall --system` if found.

### Rule 4: Always run `hermes doctor` first

### Rule 5: Language = Spanish

### Rule 6: `/etc/default/hermes_gateway` must exist

### ⭐ Rule 7: ALWAYS specify WHERE to run bash commands
When giving Soe any terminal command, you MUST explicitly say which terminal:
- **Hostinger Web Terminal** → for VPS Linux commands (systemctl, hermes config, git)
- **PC local (Windows ASUS)** → for PowerShell commands, Claude Code, npm install
- **Telegram CLI** → for commands you run yourself as the agent (safe operations)
Never assume the user knows where to run a command. If the command is for an external shell (restart, install), tell them clearly.

---

## 🔧 Maintenance Playbooks

### GitHub Skills Backup (Playbook F)
Skills repo: `https://github.com/soemacero/Soe-skills`

To sync skills to GitHub after a session:
```bash
cd /root/Soe-skills
git add -A skills/devops/ skills/marketing/ skills/diseno/ skills/soe-marketing-agent/
git commit -m "Sync skills - DATE"
git push origin main
# If push fails → generate a Classic PAT (ghp_...), not fine-grained
# Classic PAT: https://github.com/settings/tokens → "Generate classic" → check "repo"
```
See `references/github-token-setup.md` for token setup details.

The repo tracks: `skills/devops/`, `skills/marketing/`, `skills/diseno/`, `skills/soe-marketing-agent/`, `skills/local-llm-integration/`, `skills/youtube-to-skill/`, `skills/yuanbao/`.

---

## 📖 Complete Error History (v3)

### Round 3 — Hermes Agent (this session, continued)
| Problem | Fix |
|---------|-----|
| Higgsfield MCP lost after config migrate | Restored `mcp_servers` section to `~/.hermes/config.yaml` |
| Fine-grained PAT couldn't git push | Need Classic PAT (`ghp_...`) for git operations |
| Vision analyze not available | No vision provider configured |
| User asked to always clarify terminal | Added Rule 7 |

---

## 🤖 Training Notes for Backup Agents

**How to interact with Soe:**
- Telegram DM — speak **Spanish**
- She's technical and can run commands when guided
- She values **permanent fixes** — document everything in skills
- She runs TWO agents (Hermes + you). You are her safety net.
- **ALWAYS say which terminal** when giving bash commands

**The #1 mistake to avoid:** Changing the provider to Anthropic.
**When in doubt:** `hermes doctor` first. Always.
