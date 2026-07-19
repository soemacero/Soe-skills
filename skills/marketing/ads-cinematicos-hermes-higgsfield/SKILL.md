---
name: ads-cinematicos-hermes-higgsfield
description: "Pipeline para crear anuncios cinemáticos directo desde Hermes usando el MCP de Higgsfield. Sin Claude Code — todo desde aquí."
version: 1.0.0
author: Soe Macero + Hermes
tags: [higgsfield, mcp, video, ads, pipeline, hermetico]
---

# Ads Cinemáticos desde Hermes con Higgsfield MCP

## Prerequisitos
- Higgsfield MCP conectado en `mcp_servers` del config.yaml
- API Key de Higgsfield válida y con créditos
- ElevenLabs API Key (para voz y música)
- FFmpeg instalado en el sistema

## Tools Disponibles (vía MCP)
Una vez conectado, estos tools aparecen con prefijo `mcp_higgsfield_`:
- `models_explore` — explorar/recomendar modelos
- `generate_image` — generar imágenes con GPT Image 2 y otros
- `generate_video` — animar imágenes con Seedance 2.0, Kling 3.0, etc.
- `generate_audio` — voz y música
- `show_characters` — entrenar Soul ID (identidad reusable)
- `media_import_url` — importar media desde URL
- `media_upload` / `media_confirm` — subir archivos

## Flujo Rápido

### 1. Recomendar Modelo
```
models_explore(action='recommend', query='beauty clinic before after video', type='video')
```

### 2. Generar Imagen Base
```
generate_image(params={
  model: 'gpt_image_2',
  prompt: 'mujer mirándose al espejo, luz natural, tono cálido, estilo cinematográfico',
  aspect_ratio: '16:9',
  count: 1
})
```

### 3. Animar a Video
```
generate_video(params={
  model: 'seedance_2.0',
  prompt: 'cámara lenta, ella se toca las cejas, sonríe, transición suave',
  medias: [{value: MEDIA_ID, role: 'image'}],
  duration: 5
})
```

### 4. Generar Audio (voz + música)
```
generate_audio(params={
  model: 'elevenlabs_multilingual_v2',
  prompt: 'voz femenina cálida, tono reflexivo, español neutro',
  text: 'Cada mañana, un nuevo comienzo...',
  duration: 15
})
```

### 5. Ensamblar con FFmpeg
Usar terminal para concatenar clips, superponer audio, añadir tagline.

## Costos Referencia
- Seedance 2.0 1080p 10s: 90 créditos
- Seedance 2.0 720p 10s: 45 créditos
- GPT Image 2: ~5 créditos por imagen
- ElevenLabs: depende del plan
