---
name: hermes-migration-and-archiving
description: Migrate Hermes Agent state between servers and export full conversation history, memories, and skills into a beautifully formatted Obsidian Vault.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  tags: [migration, backup, obsidian, vault, archive, sqlite]
---

# Hermes Migration and Obsidian Archiving

This skill provides a class-level playbook for backing up, migrating, and archiving a Hermes Agent instance. It covers raw state migration between host servers (such as a managed Hostinger instance or a custom VPS) and the structured extraction of SQLite conversation history into an Obsidian-compatible Markdown vault.

## When to Use

Use this skill when:
- Moving Hermes from one hosting provider or VPS to another.
- Creating a full backup of the agent's "soul" (configurations, custom skills, memories, and database).
- Generating a local Markdown-based archive of all chat sessions for personal note-taking in Obsidian, preserving internal thoughts and tool-execution logs.

## 1. Raw State Migration (Server-to-Server)

Hermes provides built-in CLI commands to handle raw backups of configuration, memories, and database state.

### Creating a Backup
Run the backup command on the source system to generate a compressed `.zip` archive of the home directory:
```bash
/opt/venv/bin/hermes backup -o /data/backups/hermes_app_state_backup.zip
```
*Note: Use the `--quick` flag if only critical files (config, database, environment, and credentials) are needed.*

### Restoring a Backup
Upload the zip archive to the target system and import it:
```bash
/opt/venv/bin/hermes import /path/to/hermes_app_state_backup.zip --force
```
This restores all configurations, custom skills, memories, and the SQLite session database (`state.db`) instantly.

---

## 2. Archiving Sessions to an Obsidian Vault

The conversation logs are stored in a SQLite database (`state.db`). To read and browse these chats comfortably inside Obsidian, they should be formatted as rich Markdown files using Obsidian's native callouts.

### Exporter Layout
A well-structured archive consists of:
- **`01_Conversaciones/`**: Raw chats formatted as `.md` files.
- **`02_Memorias/`**: Copy of raw `MEMORY.md` and `USER.md` files.
- **`03_Skills/`**: Directory structure of custom and system skills.

### Markdown Formatting Conventions

#### YAML Frontmatter
Each session file must begin with descriptive frontmatter to enable Dataview querying in Obsidian:
```markdown
---
id: "session_uuid"
fecha: 2026-07-08 20:29:56
modelo: "gemini-3.5-flash"
origen: "telegram"
mensajes: 15
herramientas_usadas: 32
tokens: 4500 in / 1200 out
costo_usd: 0.005321
tags:
  - hermes-chat
---
```

#### Message Roles
Format distinct chat participants for visual clarity:
- **User (Soe):** Format with a clean user icon and timestamp:
  ```markdown
  ### 👤 Soe (Usuario)
  *2026-07-08 20:30:15*
  
  [Message content here]
  ```
- **Assistant (Hermes):** Format thoughts and tool invocations as custom callouts before outputting text:
  - **Thoughts/Reasoning:** Wrap in a `> [!thought] Pensamiento` block.
  - **Tool Calls:** Wrap in a collapsed `> [!info]- 🛠️ Llamadas a Herramientas` block.
  ```markdown
  ### 🤖 Hermes (Asistente)
  *2026-07-08 20:30:20*
  
  > [!thought] Pensamiento de Hermes
  > [Internal thought logic lines]
  
  [Response content here]
  ```
- **Tool Outputs:** Since raw tool outputs (e.g., terminal output or JSON dumps) can be massive, wrap them in collapsed execution callouts to avoid cluttering the Obsidian reading view:
  ```markdown
  > [!example]- 🔧 Herramienta Ejecutada: `tool_name`
  > **ID de Llamada:** `call_id`
  > 
  > ```
  > [Raw content lines]
  > ```
  ```

---

## Common Pitfalls & Solutions

### 1. Provider Leakage and Unexpected Billing
Scheduled cron jobs and background/auxiliary tasks (e.g. context compression, vision analysis, summarization) resolve to the primary provider and model defined in `config.yaml` (`model.provider` and `model.default`) unless overridden. When migrating or switching providers to save costs (e.g., from Gemini to OpenRouter or DeepSeek), users may experience "unexpected loops" or depleted credits on the old API key if this configuration is not fully audited.
- **Diagnostic:** Run `hermes logs` to confirm which models are being called during scheduled intervals or side tasks. The scheduler (`scheduler.py`) and auxiliary clients (`auxiliary_client.py`) do *not* have hardcoded model providers; they dynamically inherit your settings.
- **Solution:** 
  1. Audit your `config.yaml` model section to ensure the primary default provider is updated.
  2. For specific scheduled jobs, pin the desired model and provider explicitly in the job configuration (`cron/jobs.json`) to decouple them from system default changes.
  3. Override auxiliary task slots in `config.yaml` under the `auxiliary:` section (e.g., `auxiliary.compression.provider: openrouter`, `auxiliary.vision.model: deepseek/deepseek-chat`) to route background processes to cheap, reliable endpoints.

### 2. Restricted Characters in Filenames
Operating systems restrict character usage in file names (e.g., `\ / : * ? " < > |`). When using session titles as filenames:
- **Solution:** Clean the titles in Python before saving:
  ```python
  import re
  clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
  ```

### 2. Duplicate Filenames
Sessions on the same day can have identical titles or no titles (defaulting to the same name).
- **Solution:** Implement a counter suffix check:
  ```python
  counter = 1
  while os.path.exists(file_path):
      file_path = f"{base_path} ({counter}).md"
      counter += 1
  ```

### 3. Extremely Large Tool Outputs
Long execution logs can make scrolling impossible in Obsidian.
- **Solution:** Always use collapsed callouts (`> [!example]-` or `> [!info]-`) so the user can optionally expand them.

---

## Verification Checklist
- [ ] Export script executes with exit code `0`.
- [ ] Output zip file contains all three subdirectories (`01_Conversaciones`, `02_Memorias`, `03_Skills`).
- [ ] Session files open cleanly in Obsidian with syntax highlighting working on codeblocks.
- [ ] Custom system memories (`USER.md` and `MEMORY.md`) are placed in the root of the memories folder.
