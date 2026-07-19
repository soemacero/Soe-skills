---
name: anuncios-cinematicos-le-cliniq
description: "Pipeline completo para generar anuncios cinemáticos con IA: Claude Code + Higgsfield (GPT Image 2 + Seedance 2.0) + ElevenLabs + FFmpeg. De una foto a un comercial completo en 5-10 min."
version: 1.0.0
author: Soe Macero + Hermes
tags: [higgsfield, elevenlabs, video, ads, marketing, le-cliniq, cinematic, hermes-orquestador]
---

# Anuncios Cinemáticos con IA — Pipeline Completo

## ⚠️ QUIÉN ES QUIÉN EN EL EQUIPO
- **Hermes (DeepSeek)**: el cerebro, el orquestador, el que diseña y dirige. Genera guiones JSON ligeros, estructura prompts, coordina. Consume tokens LIMITADOS — no derrochar aquí.
- **Claude Code (Fable 5)**: el brazo ejecutor. Recibe instrucciones precisas de Hermes y LAS EJECUTA. Consume tokens ILIMITADOS — aquí va el trabajo pesado.
- **Soe**: la visionaria. Aporta el criterio creativo, las notas de pantalla, la dirección. Su ventaja competitiva es el criterio, no la ejecución técnica.

**Hermes no es "una tool más". Hermes es el líder. Claude Code es una tool de ejecución.**

## Stack
| Herramienta | Rol |
|---|---|
| **Claude Code** | Orquestador — dirige todo el proceso |
| **Higgsfield MCP** | Imágenes (GPT Image 2) + Video (Seedance 2.0) |
| **ElevenLabs** | Voz en off + Música cinemática |
| **FFmpeg** | Ensamblaje final (vía script Python) |
| **Airtable** (opcional) | Base visual de proyectos y assets |

## Costos Reales
- **8 escenas, 1080p, Seedance 2.0**: ~$24
- **8 escenas, 720p, Seedance 2.0**: ~$10-12
- **Reducir costos**: Kling 3.0 en vez de Seedance, menos escenas, 720p para pruebas

## Flujo de Trabajo

### 1. Prompt Inicial para Claude Code
```
Vamos a crear un sistema donde yo te voy a ir pasando distintas fotos de 
productos y tú vas a idear y producir anuncios cinemáticos completos. 
El stack: Higgsfield para imágenes (GPT Image 2) y animar con Seedance 2.0; 
Eleven Labs para voz y música; FFmpeg para ensamblar. Yo te doy una foto 
y tú empiezas por dirección creativa: historia, concepto, storyboard, escenas. 
Una buena dirección creativa tiene historia clara, ilustra bien el punto y 
pregunta qué destacar, qué referencia visual tengo y qué estilo busco.
```

### 2. Activar Modo Automático
Configuración → omitir permisos → permitir siempre en esta sesión

### 3. Conectar ElevenLabs
- API Key en `.env`: `ELEVENLABS_API_KEY=...`
- Nunca pegar la key en el chat

### 4. Conectar Higgsfield MCP
- Desde higgsfield.ai → MCP → copiar URL
- En Claude Code: Configuración → Conectores → Agregar conector personalizado
- O directamente: pedirle a Claude que se conecte

### 5. Conectar Airtable (opcional)
- Token con permisos: data.records:read/write, schema.bases:read/write
- Guardar en `.env`: `AIRTABLE_TOKEN=...`

## Proceso Creativo

### Antes de generar — definir:
1. **Historia** — no "un anuncio de X", sino la historia específica
2. **Atributo a exagerar** — el beneficio central amplificado al máximo
3. **Estilo visual** — cinemático, UGC, emocional, minimalista

### Concept Board (opcional)
- Generar 3-4 imágenes de referencia del mood visual
- El Money Shot: la imagen principal del producto en contexto

### Storyboard Prompt
```
Aquí tienes la foto desde distintos ángulos. Vamos a crear un anuncio de 
[N] escenas. La historia: [descripción detallada escena por escena]. 
El tagline final: "[tagline]". La voz: [tono/estilo]. Música: [estilo]. 
Seedance 2.0 para los videos.
```

## Aplicación para Le Cliníq

### Anuncio Microblading 9D
**Historia**: Clienta se mira al espejo todas las mañanas — siente que algo falta. Procedimiento. Al día siguiente despierta, se mira al espejo — la sensación desapareció.
**Tagline**: *"Despierta lista."*

### Variaciones por Audiencia
- **Mujeres jóvenes ejecutivas**: tiempo escaso, verse bien sin esfuerzo diario
- **Transformación personal**: recuperar cómo se sienten consigo mismas

### Temporada
- Día de la Madre, Navidad, vuelta al trabajo — misma clínica, historia distinta

## Criterios de Calidad
- La diferencia entre un buen anuncio y AI slop es el **criterio creativo** de quien lo dirige
- Ajustes quirúrgicos: pedir regenerar escena específica, no todo
- Probar en 720p primero, subir a 1080p solo la versión final

## Checklist de Proyecto
- [ ] Higgsfield activo con créditos
- [ ] ElevenLabs API Key en .env
- [ ] Higgsfield MCP conectado
- [ ] Fotos del producto (2-3 ángulos)
- [ ] Historia clara definida
- [ ] Atributo a exagerar definido
- [ ] Estilo visual/musical definido
