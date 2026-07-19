# Exporting Hermes State & Conversations to Obsidian

This guide documents how to export Hermes sessions (chat history), memories, and skills directly into an Obsidian-compatible Markdown vault structure.

## Vault Layout

The exported Obsidian Vault is structured as follows:
* **`01_Conversaciones/`**: Chat history files formatted in Markdown. Filenames are structured as `YYYY-MM-DD - [Session Title].md`. Includes full YAML frontmatter, collapsing blocks for raw tool executions (`[!example]-`), and clear thought blocks (`[!thought]`).
* **`02_Memorias/`**: Copy of your `/data/memories/` files (`MEMORY.md` and `USER.md`).
* **`03_Skills/`**: Replicated tree of your `/data/skills/` folder, skipping internal dotfiles.

## Executing the Exporter

To run the session exporter, you can execute the Python template script included with this skill. It has no external dependencies and runs on any standard Python 3 installation:

```bash
python3 /data/skills/note-taking/obsidian/templates/export_obsidian_vault.py
```

This will:
1. Create a temporary folder structure.
2. Read the SQLite `state.db` conversation database.
3. Clean and parse all active messages, format tool calls into collapsed Obsidian callouts, and write Markdown files for each session.
4. Replicate and copy the memories and skills directories.
5. Compress the entire structured vault into a single distributable zip file: `/data/backups/hermes_obsidian_vault.zip`.

## Opening in Obsidian

1. Download the generated `/data/backups/hermes_obsidian_vault.zip` archive.
2. Extract it anywhere on your local computer.
3. Open **Obsidian**.
4. Choose **Open folder as vault** (Abrir carpeta como bóveda) and select the extracted `Hermes_Obsidian_Vault` folder.
