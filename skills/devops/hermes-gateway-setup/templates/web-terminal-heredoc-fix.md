# Hostinger Web Terminal: Heredoc & Command Execution Patterns

The Hostinger Web Terminal is a browser-based SSH terminal. It has quirks that differ from a real terminal.

## 🔴 The Heredoc Problem

When you ask the user to paste:
```bash
cat > /etc/systemd/system/hermes-gateway.service << 'EOF'
[Unit]
...
EOF
```

The web terminal often:
- Pastes all lines as LITERAL TEXT into the terminal buffer without executing them
- The `EOF` terminator is pasted as text, not interpreted as end-of-input
- User sees the entire heredoc body printed on screen, file is never created
- **No error message** — the user thinks it worked

## ✅ Fix: Write files via write_file, execute via single-line command

Instead of having the user paste a heredoc, create the script file from Hermes:
```python
write_file(path="/tmp/setup-service.sh", content="""#!/bin/bash
cat > /etc/systemd/system/hermes-gateway.service << 'SERVICEEOF'
[Unit]
Description=Hermes Agent Gateway
...
SERVICEEOF

systemctl daemon-reload
systemctl enable hermes-gateway
""")
```

Then tell the user:
> "Pega esto en el terminal y presiona Enter:
> `bash /tmp/setup-service.sh`"

## 🔵 Single-line commands work fine

Single commands like these paste and execute without issues:
```bash
systemctl daemon-reload
systemctl status hermes-gateway --no-pager
kill -TERM 11799
```

## 🟢 Verification pattern

After asking the user to run a command, **verify from the agent's terminal** before proceeding:
```bash
cat /etc/systemd/system/hermes-gateway.service 2>/dev/null && echo "✅" || echo "❌ File not created"
```

This catches failed heredocs immediately instead of discovering them 3 steps later.

## 📝 The "backseat driver" pattern

When the user is actively running commands on the web terminal and you are giving them:
1. Give ONE command at a time — not a block
2. Wait for them to confirm the output before giving the next
3. If they paste a block and it fails, verify with a simple `ls`/`cat` command
4. If they get frustrated, switch to: "write_file in Hermes → tell user to run one simple command"
