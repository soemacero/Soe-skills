---
name: soe-hermes-setup
description: "Configuración y mantenimiento del agente Hermes de Soe en VPS Hostinger — reglas críticas, playbooks, historial de errores y notas de respaldo"
version: 1.0.0
author: Soe Macero + Ghost
platforms: [linux, windows, vps]
metadata:
  hermes:
    tags: [hermes, gateway, deepseek, vps, hostinger, telegram, maintenance]
    related_skills: [hermes-agent, hermes-gateway-setup, soe-marketing-agent]
---

# 🏗 Soe's Hermes Agent — Setup & Training Reference

> **Purpose:** This is the canonical reference for Soe's Hermes Agent.
> It combines fixes from TWO independent troubleshooting sessions (Claude Code + Hermes Agent) so no single point of failure is missed.

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

---

## 🚨 CRITICAL RULES (Never Break These)

### Rule 1: DeepSeek is ALWAYS the default provider
- **NEVER** change `model.provider` away from `deepseek`
- **NEVER** change `model.default` away from `deepseek/deepseek-v4-flash`
- If you see Anthropic → **restore immediately**:
  ```bash
  hermes config set model.provider deepseek
  hermes config set model.default deepseek/deepseek-v4-flash
  ```

### Rule 2: Gateway restart from INSIDE is blocked
- From within a gateway session (Telegram), these are BLOCKED:
  - `hermes gateway restart`
  - `systemctl --user restart hermes-gateway`
- These WORK from inside:
  - `systemctl --user reload hermes-gateway` ✅ (SIGUSR1)
  - `systemctl --user daemon-reload` ✅
  - `hermes config migrate` ✅
- For full restart: run from Hostinger Web Terminal:
  ```bash
  systemctl --user restart hermes-gateway
  ```

### Rule 3: Only ONE gateway service (user-level)
- No system-level gateway (`/etc/systemd/system/hermes-gateway.service`)
- If found: `sudo $(which hermes) gateway uninstall --system`
- Verify: `ps aux | grep "gateway run" | grep -v grep` → exactly 1 process

### Rule 4: Always run `hermes doctor` first
Before any maintenance: `hermes doctor`. Fix these if found:
- `Config version outdated` → `hermes config migrate`
- `Both user and system gateway services` → remove system service
- `Installed gateway service definition is outdated` → `systemctl --user daemon-reload && reload`

### Rule 5: Language = Spanish
All responses in Spanish unless Soe explicitly asks for English.

### Rule 6: `/etc/default/hermes_gateway` must exist
This file is required for systemd to pass env vars.
```bash
# Content:
TELEGRAM_BOT_TOKEN=<token>
```

---

## 🔧 Maintenance Playbooks

### Full Gateway Recovery
1. `hermes doctor` — assess damage
2. Check `/etc/default/hermes_gateway` exists
3. Remove system-level gateway if dual services
4. `hermes config migrate` (safe from inside)
5. `systemctl --user daemon-reload`
6. `systemctl --user reload hermes-gateway` (or restart from web terminal)
7. Verify DeepSeek is provider
8. Check logs: `journalctl --user -u hermes-gateway -n 20 --no-pager | grep -i error`

### Telegram Connection Issues
1. **Is Soe talking to you on Telegram?** → Then it works. Ignore logs.
2. **Test the token directly:**
   ```bash
   curl -s "https://api.telegram.org/bot<TOKEN>/getMe"
   ```
3. **Check both env locations:**
   ```bash
   grep TELEGRAM_BOT ~/.hermes/.env
   cat /etc/default/hermes_gateway
   ```

---

## 📖 Complete Error History

### Round 1 — Claude Code (earlier session)
| Problem | Fix |
|---------|-----|
| Gateway crashing | Created missing `/etc/default/hermes_gateway` with env vars |
| Telegram token bad | Was actually invalid; disabled Telegram temporarily |
| Duplicate processes | Killed ghost process, clean restart |
| Higgsfield not loaded | Gateway restart activated video/image tools |
| Model on Anthropic (no credits) | Switched to DeepSeek v4-flash |
| Web extract missing | Registered Tavily account |

### Round 2 — Hermes Agent (this session)
| Problem | Fix |
|---------|-----|
| Dual gateways (system + user) | Removed system-level service |
| Config outdated (v27 → v33) | `hermes config migrate` |
| Gateway unit outdated | `systemctl --user daemon-reload && reload` |
| Zombie process (`still -0 74438`) | Cleaned up with system service removal |
| Toolsets as YAML string | Fixed to proper YAML list |
| Provider changed to Anthropic | Restored DeepSeek, saved to memory |
| Skills missing new pitfalls | Added 4 pitfalls to gateway-troubleshooting skill |

---

## 🤖 Training Notes for Backup Agents

**When to take over:**
- Primary Hermes agent is unresponsive or crashing
- Soe asks you to help with maintenance
- Gateway needs restart from external shell

**How to interact with Soe:**
- Telegram DM — speak **Spanish**
- She's technical and can run commands
- She values **permanent fixes** — document in skills
- She runs TWO agents (Hermes + you). You are her safety net.

**The #1 mistake to avoid:** Changing the provider to Anthropic.
**When in doubt:** `hermes doctor` first. Always.