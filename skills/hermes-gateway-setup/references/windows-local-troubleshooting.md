# Windows Local Gateway Setup & Troubleshooting

When setting up or debugging Hermes Agent locally on a Windows host (e.g. ASUS TUF Laptop), several OS-specific quirks can arise. Use this reference to diagnose and resolve them.

## 1. Configuration Path Resolution

Depending on the installation method, Hermes local on Windows may read from user profile settings instead of the standard `$HOME\.hermes`.
*   **Default User Directory:** `C:\Users\<user>\.hermes\`
*   **Hidden AppData Directory:** `C:\Users\<user>\AppData\Local\hermes\`

### Exact Path Discovery
Do not guess which file Hermes is loading. Always run the following commands in PowerShell:
```powershell
hermes config path       # Prints the active config.yaml path
hermes config env-path   # Prints the active .env path
```

If you modify `$HOME\.hermes\config.yaml` but changes do not take effect, check if the active path points to `AppData\Local\hermes\config.yaml` and apply edits there.

---

## 2. Python Virtual Environment (`venv`) Pitfalls

On Windows, Hermes may run in an isolated virtual environment. If a dependency is missing, you may see:
> `Failed to initialize agent: No module named 'concurrent_log_handler'`

### Broken or Missing `pip` (`No module named pip`)
If you try to install the missing package using standard Python commands and get:
> `...venv\Scripts\python.exe: No module named pip`

This means the virtual environment's `pip` bundle is corrupt or missing. Bootstrap `pip` in the virtualenv using Python's built-in `ensurepip` module:

```powershell
# 1. Bootstrap pip directly into the Hermes virtual environment
C:\Users\<user>\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m ensurepip --default-pip

# 2. Install the missing concurrent-log-handler module using the bootstrapped pip
C:\Users\<user>\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m pip install concurrent-log-handler
```

Once installed, restart Hermes using the standard `hermes` command.

---

## 3. PowerShell Shell Redirection Bug (`>`)

When copy-pasting code blocks from Markdown, users may accidentally copy the leading `>` (used for block quotes). 

### Error:
> `El término '>' no se reconoce como nombre de un cmdlet, función, archivo de script o programa ejecutable...`

### Solution:
Clean the terminal using `Clear-Host` and ensure commands are typed or pasted *without* any leading `>` symbol, as Windows PowerShell interprets `>` as a file output redirector.

---

## 4. Port / PID Lockout Conflict

When launching a local Telegram gateway instance, you may encounter:
> `X Another gateway instance is already running (PID 1234).`

This occurs when an older gateway process did not close cleanly and is still holding the Telegram listener socket. 

### Solution:
Forcefully replace the running instance and release the port lock:
```powershell
hermes gateway run --replace
```
This automatically stops the conflicting process and mounts the new session.
