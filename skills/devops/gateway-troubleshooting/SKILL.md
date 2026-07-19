---
name: gateway-troubleshooting
description: "Troubleshoot, configure, and maintain Hermes messaging gateways (Telegram, Discord) and API keys."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gateway, telegram, env, credentials, troubleshooting, docker, api-keys]
---

# Gateway & Credential Troubleshooting

This skill covers how to diagnose, configure, and restore Hermes messaging gateways (Telegram, Discord, Slack, etc.) and verify API connectivity and credentials.

---

## Trigger Conditions

Use this skill when:
- Configuring messaging credentials (bot tokens, user IDs) on a remote host (e.g., Hostinger VPS).
- The messaging gateway is active but the bot is silent or failing to respond.
- API connectivity errors occur.
- Modifying configurations (`.env`, `config.yaml`) or restarting gateway processes.

---

## Standard Procedures

### Verification of Active Environment & Paths
Always verify where the active `.env` and `config.yaml` files live:
```bash
hermes doctor
hermes config show
```

### Testing API Credentials & Balance Probes
Test API keys directly:
```bash
# DeepSeek
curl -s https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}'
```

### Managing the Gateway
```bash
systemctl --user status hermes-gateway      # check status
systemctl --user reload hermes-gateway       # graceful reload (works from inside)
systemctl --user restart hermes-gateway      # full restart (external shell only)
journalctl --user -u hermes-gateway -n 30    # check logs
```

---

## Major Pitfalls

### ⚠️ Pitfall 1: The Masking Trap (Writing `***` or `...` into files)
**Problem:** Terminal output masks secrets (e.g., `8930865229:***`). Never copy masked strings back into `.env`.
**Mitigation:** Always use the original raw token, not the masked output.

### ⚠️ Pitfall 2: Context-Overflow Failures
**Symptom:** RuntimeError after long conversations. Gateway logs show timeout.
**Fix:** User sends `/new` or `/reset` in Telegram to clear session.

### ⚠️ Pitfall 3: Cumulative Token Scale Cost
**Mitigation:** Advise `/new` frequently.

### ⚠️ Pitfall 4: RuntimeError: No LLM Provider Configured
**Cause:** `model.provider` points to a provider without API key configured.
**Fix:** Switch to a configured provider.

### ⚠️ Pitfall 5: Low-Balance Provider Outage
**Symptom:** HTTP 400 `"Your credit balance is too low"`.
**Fix:** Switch to a provider with active balance.

### ⚠️ Pitfall 6: False-Positive Telegram Token Errors
**Rule:** If the user is talking to you on Telegram, the token works. Ignore log complaints about "token rejected".

### ⚠️ Pitfall 7: Dual Gateway Services Conflict (System + User)
**Symptom:** "Telegram polling conflict — previous session still held open". `hermes doctor` warns about both user+system services.
**Fix:** `sudo $(which hermes) gateway uninstall --system`

### ⚠️ Pitfall 8: Provider Changed Accidentally During Debugging
**Symptom:** Model suddenly changes from DeepSeek to Anthropic without user request.
**Fix:** `hermes config set model.provider deepseek && hermes config set model.default deepseek/deepseek-v4-flash`
**Prevention:** Soe's default is ALWAYS DeepSeek. Never change unless she explicitly asks.

### ⚠️ Pitfall 9: Gateway Cannot Restart From Inside Itself
**What's blocked:** `hermes gateway restart`, `systemctl --user restart hermes-gateway`
**What works:** `systemctl --user reload hermes-gateway` (SIGUSR1), `systemctl --user daemon-reload`, `hermes config migrate`
**Full restart:** Run from **Hostinger Web Terminal**: `systemctl --user restart hermes-gateway`

### ⚠️ Pitfall 10: Config Version Outdated Causes Hidden Issues
**Symptom:** `hermes doctor` shows `Config version outdated (vXX → vYY)`. Sleep commands lag, gateway unstable.
**Fix:** `hermes config migrate` (safe from inside). Then restart from web terminal.

### ⚠️ Pitfall 11: `hermes config migrate` Drops Custom Sections (mcp_servers)
**Symptom:** After running `hermes config migrate`, MCP server connections (Higgsfield, custom tools) stop working.
**Root cause:** `hermes config migrate` rewrites config from system schema — `mcp_servers` section is silently dropped.
**Fix:** Restore from backup or re-add:
```bash
# Hostinger Web Terminal
python3 -c "
import yaml
with open('/root/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
cfg['mcp_servers'] = {
    'higgsfield': {
        'url': 'https://mcp.higgsfield.ai/mcp',
        'headers': {'Authorization': 'Bearer <KEY>'},
        'timeout': 300
    }
}
with open('/root/.hermes/config.yaml', 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)
"
```
**Prevention:** Back up config before migration. After migration, check `grep -A5 'mcp_servers:' ~/.hermes/config.yaml`. After restoring, full restart needed (reload not enough).
