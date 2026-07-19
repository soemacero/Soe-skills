---
name: youtube-to-skill
description: "Pipeline para convertir cualquier video de YouTube en un skill de Hermes. yt-dlp descarga audio + Whisper transcribe + Hermes estructura ligera + Claude Code (Fable 5) convierte a skill final. Regla clave: el valor está en PANTALLA, no solo en audio."
version: 1.1.0
author: Soe Macero + Hermes
tags: [youtube, whisper, transcripcion, skills, automatizacion, pipeline, claude-code, fable-5, pantalla, token-optimization]
---
# YouTube → Skill Pipeline

## ⚠️ REGLA CRÍTICA: Asignación de recursos (tokens)

**Soe tiene tokens ILIMITADOS en Claude (Fable 5) pero LIMITADOS en DeepSeek (API activa de Hermes).**

| Recurso | Para qué usarlo | No usarlo para |
|---|---|---|
| **DeepSeek (Hermes/yo)** | Descargar audio, transcribir gratis (Whisper local), estructurar texto BASE ligero | Procesar contenido pesado, análisis profundos, convertir skills |
| **Claude Code (Fable 5)** | Procesar, analizar y CONVERTIR en skill final | (ilimitados, usar sin miedo) |

- **NUNCA** gastar tokens de DeepSeek procesando contenido pesado que pueda hacer Claude.
- Hermes prepara la materia prima (estructura ligera), Claude la transforma en skill.

## ⚠️ PEPITA DE ORO: El valor en PANTALLA > audio

Los cursos/tutoriales (Canvas, diseño, edición, Higgsfield) muestran configuraciones, parámetros, diagramas y workflows **en pantalla** que el audio nunca menciona. La transcripción sola captura ~50% del valor.

**Flujo correcto para que Soe no desperdicie tiempo ni tokens:**

1. **Hermes** descarga y transcribe (gratis, Whisper local en VPS) o usa `youtube-transcript-api` si hay subtítulos
2. **Soe ve el video en su PC** y toma notas de lo que aparece en pantalla (diagramas, prompts, configuraciones, códigos)
3. **Hermes** combina transcripción + notas → estructura ligera: temas, comandos, parámetros, qué se ve vs qué se dice
4. **Soe pega estructura + notas + prompt en Claude Code (Fable 5)** → Claude devuelve el skill completo
5. **Soe me pasa el skill** y lo integro en Hermes

**Cuando el VPS no puede autenticarse en YouTube** (yt-dlp falla con "Sign in"):
- Usar `youtube-transcript-api` si el video tiene subtítulos públicos
- Si no: Soe ve el video directo en su PC (sin depender del VPS) y toma notas manuales

## Stack

- **yt-dlp**: descarga audio del video
- **ffmpeg**: extrae y corta audio
- **openai-whisper**: transcripción local (CPU, modelo tiny)
- **Hermes (DeepSeek)**: estructura ligera, orquestación
- **Claude Code (Fable 5)**: conversión final a skill

## Instalación

```bash
pip install yt-dlp openai-whisper
apt-get install ffmpeg
```

## Pipeline Manual

### 1. Descargar audio

```bash
yt-dlp --extract-audio --audio-format mp3 -o "video.mp3" "URL_DEL_VIDEO"
```

### 2. Transcribir

```bash
whisper video.mp3 --model tiny --language es --output_dir ./
```

Genera: `video.txt`, `video.vtt`, `video.srt`, `video.tsv`

### 3. Estructurar con Hermes (ligero, pocos tokens)

Pasar transcripción con:

> "Toma esta transcripción y dame una estructura ligera con: temas principales, momentos clave, comandos exactos que menciona, y qué partes probablemente están en PANTALLA y no en audio. Sé conciso, no gastes muchos tokens."

### 4. Convertir a skill con Claude Code

Pasar estructura ligera + notas visuales a Claude con el prompt de skill completo.

### 5. Sincronizar con Hermes

Cuando Soe tenga el skill final, me lo pasa y lo integro con `skill_manage(action='create')`.

## Notas Técnicas

- **CPU mode**: Whisper en CPU es lento (~15s por 30s de audio con modelo tiny)
- **Idioma**: `--language es` para español, `en` para inglés
- **Modelos Whisper**: tiny (rápido), base, small, medium, large (preciso pero lento sin GPU)
- **Videos 3h+**: procesar en segundo plano con `terminal(background=true)`

## Next Level (cuando haya GPU en el VPS)

- `faster-whisper` (4x más rápido)
- Pipeline completo: link de YouTube → skill final sin intervención manual
