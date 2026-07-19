# Hostinger VPS Setup & Maintenance

This reference covers the specific environment of Soe's Hostinger VPS (179.197.66.231).

## Environment Profile

- **Host:** Hostinger managed VPS
- **OS:** Linux (6.8.0-134-generic)
- **Init:** `/sbin/init` (bare metal, NOT Docker)
- **Hermes install:** `uv tool install hermes-agent` → binary at `/root/.local/share/uv/tools/hermes-agent/bin/hermes`
- **Hermes binary path:** `/root/.local/share/uv/tools/hermes-agent/bin/python -m hermes_cli.main gateway run`
- **Config:** `/data/config.yaml`
- **Secrets:** `/data/.env`
- **Hermes supervision:** systemd service (`/etc/systemd/system/hermes-gateway.service`) — active and running
- **Python toolchain:** `python3=3.12.3`, `uv=installed`, `pip=missing` (use `uv pip install`), PEP 668 active (use venv)

## Data Verified (July 2026)

```
Hermes PID 69790 — running under systemd since Jul 19, 2026
Model: deepseek-chat (provider: deepseek)
MCP servers configured: higgsfield (higgsfield MCP)
Gateway: connected to Telegram
Systemd: ✅ service created, enabled, active
```

## Systemd Service Setup

Service file at `/etc/systemd/system/hermes-gateway.service`:
```ini
[Unit]
Description=Hermes Agent Gateway
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
EnvironmentFile=/etc/default/hermes_gateway
ExecStart=/root/.local/share/uv/tools/hermes-agent/bin/python -m hermes_cli.main gateway run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Environment file at `/etc/default/hermes_gateway`:
```
HERMES_HOME=/data
TELEGRAM_BOT_TOKEN=8930865229:AAE3t...ATao
```

**⚠️ ⚠️ CRITICAL: .env vs EnvironmentFile (July 2026)**

This VPS had a working gateway for weeks under bare-process mode, reading `/data/.env`. After moving to systemd with `EnvironmentFile=/etc/default/hermes_gateway`, Telegram stopped working with "token rejected" — even though the token was valid (verified via `curl https://api.telegram.org/bot<token>/getMe` returned `200`).

**Root cause:** systemd only passes vars from the `EnvironmentFile` to the process. `/data/.env` is NOT sourced. The gateway couldn't see `TELEGRAM_BOT_TOKEN`.

**Fix:** When creating the systemd service, always include **all** critical platform tokens in the EnvironmentFile, not just `HERMES_HOME`:

```bash
echo "TELEGRAM_BOT_TOKEN=8930865229:AAE3t...ATao" >> /etc/default/hermes_gateway
systemctl restart hermes-gateway
```

**Verification:** Check if the running process actually has the token:
```bash
cat /proc/$(pgrep -f 'gateway run' | head -1)/environ 2>/dev/null | tr '\0' '\n' | grep TELEGRAM
```

**⚠️ Pitfall:** If the user pastes heredoc commands via Hostinger Web Terminal and it doesn't create the file, the issue is usually multi-line paste handling. Write a script file instead and execute it (see `templates/web-terminal-heredoc-fix.md` in the skill).

## Gateway Restart Procedure

With systemd installed:
```bash
systemctl restart hermes-gateway
```

**⚠️ Cannot restart from inside the agent session:** The agent is a child of the gateway process. Running `systemctl restart` from the agent's terminal kills the agent mid-execution. The user **must** run the restart from the Hostinger Web Terminal or an external SSH session.

**To restart from the agent's terminal session (non-destructive alternative):**
```bash
# Just tell the user what to paste in their web terminal:
# systemctl restart hermes-gateway
```

## Telegram Token Troubleshooting

When the gateway log shows:
```
ERROR [Telegram] No se pudo conectar a Telegram: El token '8930865229:***' fue rechazado
```

**Step 0 — Check if a stale TELEGRAM_PROXY placeholder is blocking the connection first:**

Look at the gateway log:
```bash
sudo journalctl -u hermes-gateway.service --no-pager | grep -E 'puerto|Proxy detected' | tail -5
```
If you see `Invalid port: 'puerto'` or `socks5://tu_proxy_aqui:puerto`, the real problem is a stale proxy config, not the token. Remove it:
```bash
sed -i '/TELEGRAM_PROXY/d' /root/.hermes/.env
sed -i '/TELEGRAM_PROXY/d' /data/.env
```
The proxy line is a common leftover from initial setup where the user never filled in real proxy details. The gateway treats any non-empty TELEGRAM_PROXY as an active proxy config, so "socks5://tu_proxy_aqui:puerto" causes an invalid port error that masquerades as a token rejection.

**Step 0 — Check if the token exists in the process environment:**
```bash
cat /proc/$(pgrep -f 'gateway run' | head -1)/environ 2>/dev/null | tr '\0' '\n' | grep TELEGRAM_BOT
```
If empty, the token is not reaching the gateway process — it is an EnvironmentFile issue (see systemd section above), not a bad token.

**Step 1 — Verify the token is correct by calling Telegram API directly:**
```bash
curl -s "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
```
If this returns `{"ok": true, ...}`, the token is valid and the problem is in the deployment (EnvironmentFile vs .env mismatch).

**Fix procedure:**
1. Write the correct token to `/data/.env`: `sed -i 's|TELEGRAM_BOT_TOKEN=.*|TELEGRAM_BOT_TOKEN=<real-token>|' /data/.env`
2. **Also** add to EnvironmentFile (if using systemd): `echo "TELEGRAM_BOT_TOKEN=<token>" >> /etc/default/hermes_gateway`
3. Verify length: 46 chars for standard bot tokens
4. Restart gateway from the VPS terminal (not from inside the agent)

## DeepSeek Usage Monitoring

Soe tracks DeepSeek spend via CSV exports from the platform. Report format:
- Model: deepseek-v4-flash
- Period: typically monthly
- Cache hit rate is excellent (~95%)
- Two API keys in use: "AGENTE IA 1" (primary, ~827 requests) and "Agente IA" (secondary, ~5 requests)
- Monthly cost is very low (~$0.76/month on recent data)
- Balance: $9.23 USD remaining (as of July 19, 2026)

## Verification Commands

```bash
# Check Hermes is running
systemctl status hermes-gateway --no-pager

# Check config.yaml has mcp_servers
grep -A6 'mcp_servers:' /data/config.yaml

# Check Telegram token length
grep TELEGRAM_BOT_TOKEN /data/.env | python3 -c "import sys; line=sys.stdin.read().strip(); print('len=', len(line.split('=',1)[1]))"
```
