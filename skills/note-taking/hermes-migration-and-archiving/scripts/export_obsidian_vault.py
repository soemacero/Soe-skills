import os
import sqlite3
import re
import shutil
import zipfile
from datetime import datetime
import json

# Define paths
DB_PATH = "/data/state.db"
VAULT_DIR = "/data/obsidian_vault"
CONVERSATIONS_DIR = os.path.join(VAULT_DIR, "01_Conversaciones")
MEMORIES_DIR = os.path.join(VAULT_DIR, "02_Memorias")
SKILLS_DIR = os.path.join(VAULT_DIR, "03_Skills")
BACKUP_ZIP_PATH = "/data/backups/hermes_obsidian_vault.zip"

def sanitize_filename(name):
    # Remove restricted characters for filesystems
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    # Trim and limit length to avoid OS limits
    return name.strip()[:100]

def format_timestamp(ts):
    if not ts:
        return "N/A"
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "N/A"

def clean_thought_content(content):
    if not content:
        return ""
    # Prefix every line with '> ' for markdown callout indentation
    return "\n".join(f"> {line}" for line in content.strip().split("\n"))

def export_sessions():
    os.makedirs(CONVERSATIONS_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all sessions
    cursor.execute("""
        SELECT id, title, started_at, ended_at, message_count, tool_call_count, 
               model, input_tokens, output_tokens, estimated_cost_usd, source 
        FROM sessions 
        ORDER BY started_at ASC
    """)
    sessions = cursor.fetchall()
    
    print(f"Exportando {len(sessions)} sesiones...")
    
    for session in sessions:
        s_id, title, started_at, ended_at, msg_count, tool_count, model, in_tok, out_tok, cost, source = session
        
        # We only care about sessions that have messages (or are the current one)
        # Skip cron logs if they have only 1 message and it's the automated ones, but let's export everything just in case
        if not msg_count and not title:
            # Let's check if there are actual messages in this session
            cursor.execute("SELECT COUNT(*) FROM messages WHERE session_id = ?", (s_id,))
            real_count = cursor.fetchone()[0]
            if real_count == 0:
                continue # Skip completely empty sessions

        start_date_str = datetime.fromtimestamp(started_at).strftime("%Y-%m-%d")
        session_title = title if title else f"Sesión {s_id[:8]}"
        filename = f"{start_date_str} - {sanitize_filename(session_title)}.md"
        file_path = os.path.join(CONVERSATIONS_DIR, filename)
        
        # Handle duplicate filenames by appending session ID suffix
        counter = 1
        while os.path.exists(file_path):
            filename = f"{start_date_str} - {sanitize_filename(session_title)} ({counter}).md"
            file_path = os.path.join(CONVERSATIONS_DIR, filename)
            counter += 1
            
        # Fetch messages for this session
        cursor.execute("""
            SELECT role, content, tool_calls, tool_name, reasoning_content, timestamp, tool_call_id
            FROM messages 
            WHERE session_id = ? AND active = 1
            ORDER BY id ASC
        """, (s_id,))
        messages = cursor.fetchall()
        
        # Write markdown content
        with open(file_path, "w", encoding="utf-8") as f:
            # Frontmatter
            f.write("---\n")
            f.write(f"id: \"{s_id}\"\n")
            f.write(f"fecha: {format_timestamp(started_at)}\n")
            if ended_at:
                f.write(f"fin: {format_timestamp(ended_at)}\n")
            f.write(f"modelo: \"{model or 'Desconocido'}\"\n")
            f.write(f"origen: \"{source or 'Desconocido'}\"\n")
            f.write(f"mensajes: {len(messages)}\n")
            f.write(f"herramientas_usadas: {tool_count or 0}\n")
            f.write(f"tokens: {in_tok or 0} in / {out_tok or 0} out\n")
            if cost is not None:
                f.write(f"costo_usd: {cost:.6f}\n")
            f.write("tags:\n")
            f.write("  - hermes-chat\n")
            f.write("---\n\n")
            
            f.write(f"# 💬 {session_title}\n\n")
            f.write(f"**ID de Sesión:** `{s_id}` | **Modelo:** `{model}` | **Origen:** `{source}`\n\n")
            f.write("---\n\n")
            
            for msg in messages:
                role, content, tool_calls, tool_name, reasoning_content, timestamp, tool_call_id = msg
                time_str = format_timestamp(timestamp)
                
                if role == "user":
                    f.write(f"### 👤 Soe (Usuario)\n")
                    f.write(f"*{time_str}*\n\n")
                    f.write(f"{content or ''}\n\n")
                    f.write("---\n\n")
                    
                elif role == "assistant":
                    f.write(f"### 🤖 Hermes (Asistente)\n")
                    f.write(f"*{time_str}*\n\n")
                    
                    # Add reasoning if present
                    if reasoning_content:
                        f.write("> [!thought] Pensamiento de Hermes\n")
                        f.write(clean_thought_content(reasoning_content))
                        f.write("\n\n")
                    
                    # Add tool calls if present
                    if tool_calls:
                        try:
                            tc_parsed = json.loads(tool_calls)
                            f.write("> [!info]- 🛠️ Llamadas a Herramientas\n")
                            f.write("> ```json\n")
                            formatted_tc = json.dumps(tc_parsed, indent=2, ensure_ascii=False)
                            for line in formatted_tc.split("\n"):
                                f.write(f"> {line}\n")
                            f.write("> ```\n\n")
                        except Exception:
                            f.write("> [!info]- 🛠️ Llamadas a Herramientas (Crudo)\n")
                            f.write(f"> `{tool_calls}`\n\n")
                    
                    if content:
                        f.write(f"{content}\n\n")
                    f.write("---\n\n")
                    
                elif role == "tool":
                    f.write(f"> [!example]- 🔧 Herramienta Ejecutada: `{tool_name}`\n")
                    f.write(f"> **ID de Llamada:** `{tool_call_id}`\n")
                    f.write(f"> **Timestamp:** *{time_str}*\n")
                    f.write("> \n")
                    f.write("> ```\n")
                    # Safely escape backticks inside code blocks to avoid rendering breakages
                    safe_content = (content or "").replace("```", "'''")
                    for line in safe_content.split("\n"):
                        f.write(f"> {line}\n")
                    f.write("> ```\n\n")
                    f.write("---\n\n")
                    
    conn.close()

def copy_memories():
    os.makedirs(MEMORIES_DIR, exist_ok=True)
    src_dir = "/data/memories"
    if os.path.exists(src_dir):
        for f in os.listdir(src_dir):
            if f.endswith(".md"):
                shutil.copy(os.path.join(src_dir, f), os.path.join(MEMORIES_DIR, f))
        print("Memorias copiadas.")
    else:
        print("Directorio de memorias no encontrado.")

def copy_skills():
    os.makedirs(SKILLS_DIR, exist_ok=True)
    src_dir = "/data/skills"
    if os.path.exists(src_dir):
        for root, dirs, files in os.walk(src_dir):
            # Skip hidden folders/files
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for file in files:
                if file.startswith("."):
                    continue
                src_file_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_file_path, src_dir)
                dest_file_path = os.path.join(SKILLS_DIR, rel_path)
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                shutil.copy(src_file_path, dest_file_path)
        print("Skills copiadas.")
    else:
        print("Directorio de skills no encontrado.")

def create_zip():
    print("Creando archivo zip...")
    os.makedirs(os.path.dirname(BACKUP_ZIP_PATH), exist_ok=True)
    with zipfile.ZipFile(BACKUP_ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(VAULT_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, VAULT_DIR)
                zipf.write(file_path, os.path.join("Hermes_Obsidian_Vault", rel_path))
    print(f"Zip creado con éxito en: {BACKUP_ZIP_PATH}")

def main():
    if os.path.exists(VAULT_DIR):
        shutil.rmtree(VAULT_DIR)
    os.makedirs(VAULT_DIR, exist_ok=True)
    
    export_sessions()
    copy_memories()
    copy_skills()
    create_zip()
    
    # Cleanup temporary vault directory to save disk space
    shutil.rmtree(VAULT_DIR)
    print("Exportación completa y directorio temporal limpiado.")

if __name__ == "__main__":
    main()
