# Hermes Docker Security Audit — June 2026

Findings from first security audit of a fresh Hermes deployment (2 days old) on Hostinger VPS.

## Environment

- Host: Hostinger VPS, Linux 6.12.88+deb13-amd64
- Container user: `u4s` (uid=337, non-root ✅)
- RAM: 503 GB total, 309 GB available (very large VPS)
- Disk: 4.4 TB, 13% used
- Hermes version: ~2 days old at time of audit

## Tools available inside container

| Tool | Available? | Alternative |
|------|-----------|-------------|
| `ss` | ❌ | `/proc/net/tcp` (raw hex, needs decoding) |
| `netstat` | ❌ | `/proc/net/tcp` |
| `ufw` | ❌ | N/A — firewall is on the host, not container |
| `iptables` | ❌ | N/A |
| `sshd_config` | ❌ | SSH is on host VPS, not in container |
| `ps aux` | ✅ | — |
| `free -h` | ✅ | — |
| `df -h` | ✅ | — |
| `chmod/chown` | ✅ | — |

## Findings

### CRITICAL: .env permissions were 644
`/data/.env` had world-readable permissions (644). This file contains:
- `ANTHROPIC_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_ALLOWED_USERS`
- `NOTION_API_KEY` / `NOTION_API_TOKEN`

**Fix applied:** `chmod 600 /data/.env` → now `-rw------- 1 u4s u4s`

### INFO: No firewall inside container (expected)
Firewall (UFW/iptables) runs on the host VPS level, not inside Docker. The container is isolated by Docker networking. Ports visible in `/proc/net/tcp` are internal container ports, not exposed to the internet directly.

### INFO: No SSH inside container (expected)
SSH daemon is on the host VPS. Security of SSH (port, key-only auth, no root login) must be managed via the Hostinger control panel or direct VPS SSH session — not from within the container.

### INFO: No git repos (no .env leak risk via git)
`find /data -name ".git"` returned nothing. No risk of `.env` being committed to a repository.

### INFO: Process list clean
Running processes: only `tini`, `u4s-hermes-agent`, hermes gateway. No unexpected processes.

## Actions taken

1. ✅ `chmod 600 /data/.env`
2. ✅ Created `/data/scripts/backup_hermes.sh` — daily backup of memories, skills, config
3. ✅ Created `/data/.hermes/scripts/health_check.sh` — hourly health check, alerts to Telegram
4. ✅ Cron job: backup daily at 03:00 UTC
5. ✅ Cron job: health check every hour (no_agent=true, silent on OK, alerts on issues)
6. ✅ First backup: `hermes_20260618_201826.tar.gz` (2.1 MB)

## Pending (requires host VPS access)

These cannot be done from inside the container:
1. Verify/configure firewall on Hostinger panel
2. Change SSH port from default 22
3. Disable SSH password auth (key-only)
4. Rotate Telegram bot token via @BotFather

## Model recommendation for Ollama

Given 309 GB RAM available:
- Recommended: `llama3.1:70b` or `qwen2.5:72b`
- These are the most capable open models available locally
- No resource constraints at this scale
