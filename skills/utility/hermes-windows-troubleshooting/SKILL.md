---
name: hermes-windows-troubleshooting
description: "Troubleshooting and configuring Hermes Agent natively on Windows (PowerShell, CMD, paths, Python dependencies, and Ollama)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [windows, powershell, local-ai, troubleshooting, ollama, path-mismatch, python]
    related_skills: [hermes-agent, hermes-gateway-setup]
---

# Troubleshooting and Configuring Hermes Agent on Windows

Running Hermes Agent natively on Windows (via PowerShell or CMD) presents unique challenges compared to POSIX systems. This guide lists the most common Windows-specific bugs, environment quirks, and exact PowerShell diagnostics to fix them.

---

## 🔍 Path Mismatch: `.hermes` vs `AppData\Local`

### Symptoms
Changes made to `$HOME\.hermes\config.yaml` or `$HOME\.hermes\.env` are completely ignored by the CLI or gateway.

### Root Cause
Depending on how Hermes was installed and the execution context on Windows, it may read and write configurations from `C:\Users\<User>\AppData\Local\hermes\` instead of the standard `$HOME\.hermes\`.

### Diagnostic Commands (PowerShell)
Find out exactly where Hermes is looking for files:
```powershell
hermes config path
hermes config env-path
```

### Solution
Always inspect the paths returned by the diagnostic commands and write configurations directly to those paths. For example, to programmatically rewrite the config in the active path without Notepad-BOM issues:
```powershell
$ActivePath = (hermes config path)
$YamlClean = @"
model:
  default: ollama/llama3.1:8b
  provider: ollama
  base_url: http://localhost:11434

telegram:
  bot_token: "YOUR_BOT_TOKEN"
  enabled: true
"@
[System.IO.File]::WriteAllText($ActivePath, $YamlClean, [System.Text.Encoding]::UTF8)
```

---

## 🐍 Missing Python Dependencies (e.g. `concurrent_log_handler`)

### Symptoms
Startup crashes with:
`Failed to initialize agent: No module named 'concurrent_log_handler'`

### Root Cause
Windows Python environments may fail to install optional dependencies during the initial global installation script or due to sandbox/antivirus locks.

### Solution
Install the missing module manually into the active Python environment:
```powershell
python -m pip install concurrent-log-handler
```
*(If running under a virtual environment, ensure you activate it first or use the venv's specific python binary).*

---

## ⚙️ Environment Variables and `$` Expansion

### Symptoms
Connection failures like:
`Failed to connect to Telegram: The token '$TELEGRAM_BOT_TOKEN' was rejected by the server.`

### Root Cause
Unlike Linux/macOS, Windows terminals (CMD, PowerShell) do not automatically expand env variables starting with `$` inside configuration YAMLs. Hermes literally attempts to connect using the string `"$TELEGRAM_BOT_TOKEN"`.

### Solution
Avoid using environmental placeholders inside `config.yaml` on native Windows. Put the raw, quoted values directly inside `config.yaml`:
```yaml
telegram:
  bot_token: "8501390565:AAE..."
  enabled: true
```

---

## ⚡ Port & PID Conflicts (`Another gateway instance is already running`)

### Symptoms
`X Another gateway instance is already running (PID <PID>).`

### Root Cause
Windows does not release background daemon processes as gracefully as POSIX on exit, or a zombie terminal process keeps holding the gateway file lock.

### Solution
1. **Kill all active Hermes processes:**
   ```powershell
   Stop-Process -Name "hermes" -Force -ErrorAction SilentlyContinue
   ```
2. **Force startup with the replace flag:**
   ```powershell
   hermes gateway run --replace
   ```

---

## 📝 Notepad Encoding and the invisible UTF-8 "BOM"

### Symptoms
HTTP 400 "No models provided" or YAML parsing exceptions after editing files manually in Windows Notepad.

### Root Cause
By default, Windows Notepad saves files with **UTF-8 BOM (Byte Order Mark)**. Hermes's YAML parser fails on the hidden leading bytes.

### Solution
* Use a safe editor like VS Code.
* Programmatically write the files using PowerShell (which writes pure UTF-8 without BOM):
  ```powershell
  [System.IO.File]::WriteAllText($FilePath, $Content, [System.Text.Encoding]::UTF8)
  ```
