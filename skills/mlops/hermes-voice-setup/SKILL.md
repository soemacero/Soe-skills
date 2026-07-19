---
name: hermes-voice-setup
description: "Voice configuration for Hermes Agent with ElevenLabs (primary) and Edge TTS (fallback). STT with Whisper local. Speed, voice selection, API key setup, and auto-TTS activation. Configured for Soe's 'soe premium' voice at speed 1.2."
version: 1.0.0
author: Soe Macero + Hermes
tags: [voice, tts, stt, elevenlabs, whisper, edge-tts, configuracion]
---

# Hermes Voice Setup

## Stack
| Componente | Herramienta | Estado |
|---|---|---|
| **TTS (hablar)** | ElevenLabs (primario) | ✅ Configurado |
| **TTS fallback** | Edge TTS (Mexicana Dalia) | ✅ Configurado |
| **STT (escuchar)** | Whisper local (modelo base) | ✅ Configurado |
| **auto_tts** | Respuesta automática por voz | ✅ Activado |

## Configuración Actual (Soe)

### TTS Principal — ElevenLabs
- **Provider**: `elevenlabs`
- **Voz**: `soe premium` (ID: `UT6BK299jzZuhXKDXGoK`)
- **Modelo**: `eleven_multilingual_v2`
- **Velocidad**: `1.2` (configurado como predeterminada — decisión final de Soe)
- **Stability**: `0.5`
- **Similarity Boost**: `0.75`
- **API Key**: guardada en `/data/.env` como `ELEVENLABS_API_KEY`
- **Gateway**: `false` (usa API key directa, no portal)

### TTS Fallback — Edge TTS
- **Provider**: `edge`
- **Voz**: `es-MX-DaliaNeural` (voz mexicana femenina)
- **No requiere API key**
- Se activa si ElevenLabs falla

### STT — Whisper Local
- **Provider**: `local`
- **Modelo**: `base`
- **Idioma**: `''` (auto-detect)
- **Record key**: `ctrl+b`
- **Max grabación**: 120s

## Configuración Rápida

### 1. Instalar dependencias
```bash
# Edge TTS (viene con Hermes, solo verificar)
pip install edge-tts

# Whisper (para STT local)
pip install openai-whisper

# Voices de Edge
edge-tts --list-voices | grep -i es
```

### 2. Configurar ElevenLabs
```bash
# Provider
hermes config set tts.provider elevenlabs
hermes config set tts.use_gateway false

# Voz y modelo
hermes config set tts.elevenlabs.voice_id UT6BK299jzZuhXKDXGoK
hermes config set tts.elevenlabs.model_id eleven_multilingual_v2

# Velocidad y calidad (editar config.yaml directamente o con sed)
sed -i 's/voice_id: UT6BK299jzZuhXKDXGoK/voice_id: UT6BK299jzZuhXKDXGoK\\n    stability: 0.5\\n    similarity_boost: 0.75\\n    speed: 1.2/' /data/config.yaml

# API key
echo 'ELEVENLABS_API_KEY=sk-...' >> /data/.env
```

### 3. Configurar Edge (fallback)
```bash
# Edge como fallback
hermes config set tts.edge.voice es-MX-DaliaNeural
```

### 4. Activar auto-tts
```bash
hermes config set voice.auto_tts true
```

### 5. Verificar STT local
Ya configurado en `stt.provider: local` con modelo `base`.

## Verificar que funciona
Usar el tool `text_to_speech` — debe responder con audio:
```python
# Internamente Hermes llama a ElevenLabs con la configuración guardada
```

## Pitfalls
- **El tool `text_to_speech` no expone parámetros de velocidad/stability**. Se configuran directamente en el YAML bajo `tts.elevenlabs`.
- **`hermes config set` no soporta setting anidados profundos**. Para `stability`, `similarity_boost`, `speed` hay que editar el YAML con `sed` y aprobar manualmente.
- **Edge TTS suena más robótico que ElevenLabs**. Usar Edge solo como fallback.
- **Whisper en CPU es lento** (~15s por 30s de audio con modelo tiny). Para uso frecuente, considerar faster-whisper si hay disponibilidad.
- **El audio se guarda en `/data/cache/audio/`** con formato `.ogg` (Edge) o `.mp3` (ElevenLabs directo vía script).
- **El tool nativo `text_to_speech` de Hermes NO respeta `speed` ni `voice_settings` del config.yaml.** Aunque se configure speed=1.15 en el YAML, el tool interno de Hermes llama a ElevenLabs sin pasar esos parámetros. El audio generado por el tool suena a velocidad 1.0 (original). Para que el usuario escuche la velocidad correcta, hay que:
  1. Usar el script directo `/data/scripts/hermes_tts.py` que sí pasa speed.
  2. O generar el audio manualmente con `execute_code` contra la API directa.
- **Al probar velocidades, SIEMPRE comparar audios generados con el mismo método.** El tool nativo vs script directo producen diferencias auditivas que confunden al usuario.
- **El usuario puede pedir escuchar diferentes velocidades.** Tener preparadas variantes: 1.0, 1.1, 1.15, 1.2, 1.25. Soe probó varias y decidió: **"soe premium" a speed 1.2**. Nota importante: cuando probó 1.15 con el tool nativo sonaba más lento, y cuando se generó con el script directo a 1.15 sonaba más rápido. La confusión fue porque el tool nativo ignora el speed. **Decisión final tras comparar audios del script directo**: speed 1.2 con voz "soe premium".

### Flujo para probar voces/velocidades
1. Preguntar qué velocidad prefiere antes de cambiar config
2. Generar con `execute_code` usando API directa (NO tool nativo) para que speed se respete
3. Poner archivos en `/tmp/tts_{label}.mp3`
4. Dejar que compare audios lado a lado
5. Cuando confirme velocidad y voz, actualizar `config.yaml` con sed

## Script Directo (para control fino)
```python
import requests
API_KEY = "sk_..."
VOICE_ID = "UT6BK299jzZuhXKDXGoK"
SPEED = 1.2

headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
payload = {
    "text": text,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.75,
        "speed": SPEED
    }
}
r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}", json=payload, headers=headers, timeout=30)
# r.content is the MP3 audio
```

## Voz Actual por Defecto
- **Nombre**: soe premium
- **ID**: `UT6BK299jzZuhXKDXGoK`
- **Idioma**: Español (latino)
- **Velocidad**: 1.2x (rápida, natural)
  
## Next Level
- **GPT-Live full-duplex** (OpenAI, lanzado jul 2026): cuando llegue a la API, integrar para conversación simultánea hablar+escuchar. Ver `references/gpt-live-research.md`.
- **Clonación de voz más precisa**: entrenar modelo personalizado en ElevenLabs con más muestras.
