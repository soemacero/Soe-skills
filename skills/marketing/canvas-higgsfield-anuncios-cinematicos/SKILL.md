---
name: canvas-higgsfield-anuncios-cinematicos
description: "Manual completo: de una foto a un comercial cinemático con IA en un solo prompt. Stack: Claude Code + Higgsfield (GPT Image 2 + Seedance 2.0) + ElevenLabs + FFmpeg. Basado en el sistema del instructor del video 'Cómo crear anuncios cinemáticos con IA'."
version: 1.0.0
author: Soe Macero + Hermes
tags: [higgsfield, elevenlabs, anuncios, cinematicos, video, ffmpeg, claude-code, seedance, canvas]
---

# Canvas: Anuncios Cinemáticos con IA

## El Sistema
De una foto → a un comercial completo en 5-10 minutos. Sin Premiere, sin animación manual, sin saltar entre plataformas.

## Stack
| Herramienta | Rol |
|---|---|
| **Claude Code** | Orquestador — dirige todo |
| **Higgsfield MCP** | Imágenes (GPT Image 2) + Video (Seedance 2.0) |
| **ElevenLabs** | Voz en off + Música cinemática |
| **FFmpeg** | Ensamblaje final (script Python) |
| **Airtable** (opcional) | Base visual de proyectos y assets |

## Configuración Inicial (1 vez)

### Paso 1: Prompt de Rol para Claude Code
> "Vamos a crear un sistema donde yo te voy a ir pasando distintas fotos de productos y tú vas a idear y producir anuncios cinemáticos completos. El stack que vamos a usar es: Higgsfield para las imágenes (GPT Image 2) y para animar esas imágenes con Cedance 2.0; Eleven Labs para la voz y la música; y FFmpeg para ensamblar todo. Yo te voy a dar una foto y tú vas a empezar por la dirección creativa: historia, concepto, storyboard, escenas. Una buena dirección creativa tiene que tener una historia clara, tiene que ilustrar bien el punto y tiene que preguntarme qué quiero destacar, qué referencia visual tengo y qué estilo busco. Luego concatenas todo y me produces el mejor ad cinemático posible."

### Paso 2: Activar Modo Automático
Configuración → omitir permisos → permitir siempre en esta sesión

### Paso 3: Conectar ElevenLabs
- Obtener API Key en elevenlabs.io → Developers → API Keys
- Guardar en `.env`: `ELEVENLABS_API_KEY=...` (NUNCA en el chat)
- Luego decir: "Ya la puse. Continuemos con el onboarding."

### Paso 4: Conectar Higgsfield MCP
- Entrar a higgsfield.ai → sección MCP → copiar URL
- Claude Code: Configuración → Conectores → Agregar conector personalizado
- O pedirle que se conecte directamente

### Paso 5: Conectar Airtable (opcional)
- Token con permisos: data.records:read/write, schema.bases:read/write
- Guardar en `.env`: `AIRTABLE_TOKEN=...`

### Paso 6: Skill de Buenas Prácticas
- Importar el skill de dirección creativa (archivo .md)
- Contiene: parámetros de duración de clips, principios creativos, guías de voz y música, criterios de calidad

## Proceso Creativo

### Las 3 preguntas antes de generar
1. **¿Qué historia quiero contar?** — No "un anuncio de X", sino la historia específica
2. **¿Qué atributo quiero exagerar?** — El beneficio central amplificado al máximo
3. **¿Qué estilo visual busco?** — Cinemático, emocional, UGC, minimalista

### Concept Board (opcional)
- 3-4 imágenes de referencia del mood visual
- Money Shot: la imagen principal del producto en contexto

### Storyboard Prompt
> "Aquí tienes la foto desde distintos ángulos. Vamos a crear un anuncio de [N] escenas. La historia: [descripción detallada escena por escena]. El tagline final: '[tagline]'. La voz: [tono/estilo]. Música: [estilo musical]. Seedance 2.0 para los videos."

## Pipeline de Generación (automático)

1. **Generar imágenes** — GPT Image 2 vía Higgsfield MCP (con consistencia de personaje)
2. **Animar a video** — Seedance 2.0 (3, 5, 8 o 10s por clip según la escena)
3. **Crear voz en off** — ElevenLabs con el script basado en el concepto
4. **Generar música** — ElevenLabs (cinemática, según el estilo definido)
5. **Ensamblar** — FFmpeg: clips + voz + música sincronizados
6. **Registrar** — Airtable: cada escena, imagen, video, audio, output final

**Tiempo total: 5-10 minutos para 8 escenas**

## Costos

| Configuración | Costo |
|---|---|
| 8 escenas, 1080p, Seedance 2.0 | ~$24 |
| 8 escenas, 720p, Seedance 2.0 | ~$10-12 |
| Reducción: Kling 3.0, menos escenas, 720p para pruebas | Varía |

## Refinamiento
Ajustes quirúrgicos — NO regenerar todo:
- "Pon más pausa entre frases en la voz."
- "Regenera la escena 4, la transición no quedó natural."
- "Cambia el tagline final."
- "Quiero versión corta (15s) y larga (30s)."

## Aplicación Le Cliníq

### Anuncio Microblading 9D
**Historia**: Clienta se mira al espejo todas las mañanas — siente que algo falta. Procedimiento. Al día siguiente despierta, se mira — la sensación desapareció.
**Tagline**: "Despierta lista."

### Variaciones por Audiencia
- **Ejecutivas jóvenes**: tiempo escaso, verse bien sin esfuerzo
- **Transformación personal**: recuperar cómo se sienten consigo mismas
- **Temporada**: Día de la Madre, Navidad, vuelta al trabajo

## Checklist de Proyecto
- [ ] Higgsfield con créditos
- [ ] ElevenLabs API Key en .env
- [ ] Higgsfield MCP conectado
- [ ] Fotos del producto (2-3 ángulos)
- [ ] Historia clara
- [ ] Atributo a exagerar
- [ ] Estilo visual/musical
- [ ] Prompt de rol inicial dado
- [ ] Modo automático activado
- [ ] Storyboard aprobado
- [ ] Resultado revisado

## Glosario
- **Seedance 2.0**: Mejor modelo de video, anima imágenes fijas
- **GPT Image 2**: Generación de imágenes vía Higgsfield MCP
- **FFmpeg**: Edición de video open source (ensamblaje final)
- **Concept Board**: Imágenes de referencia del mood visual
- **Money Shot**: Plano estrella del producto
- **AI Slop**: Contenido IA genérico sin criterio creativo
- **MCP**: Protocolo que conecta Claude Code con herramientas externas

*Manual basado en el video "Cómo crear anuncios cinemáticos con IA en un solo prompt" (33:30). Parafraseado y estructurado para referencia personal.*
