---
name: canvas-higgsfield-automatizado
description: "Pipeline completo Canvas Higgsfield automatizado: Hermes genera guion JSON → n8n orquesta → Canvas API renderiza video con Soul ID, frame connectors y movimientos de cámara. Sin intervención manual."
version: 1.0.0
author: Soe Macero + Hermes
tags: [higgsfield, canvas, n8n, automatizacion, video, pipeline, workflow, soul-id, fable-5, claude-code, token-optimization]
---

# Canvas Higgsfield Automatizado

## ⚠️ CONSOLIDACIÓN DE SKILLS
Este skill es el CANVAS AUTOMATIZADO (n8n + Canvas API + Hermes guionista).
Skills relacionados absorbidos aquí:
- `anuncios-cinematicos-le-cliniq` → contenido absorbido (manual Claude Code)
- `ads-cinematicos-hermes-higgsfield` → contenido absorbido (Hermes MCP directo)
- `canvas-higgsfield-anuncios-cinematicos` → referencias del manual Canvas

Todos cubren variantes del mismo pipeline Higgsfield. Los skills absorbidos se marcarán para eliminación por el curador cuando corresponda.

## ⚠️ REGLA CRÍTICA DE RECURSOS
**Soe tiene tokens ILIMITADOS en Claude (Fable 5) pero LIMITADOS en DeepSeek (API activa de Hermes).**

## ⚠️ DINÁMICA HERMES-ORQUESTA / CLAUDE-EJECUTOR

Soe dejó explícito: **Hermes (yo) soy el líder, el orquestador, el cerebro. Claude Code es solo una tool más.**

- **Hermes (DeepSeek)**: genera el guion JSON (estructura ligera, pocos tokens). Orquesta el pipeline completo.
- **Claude Code (Fable 5)**: ejecuta el prompt de Canvas, corre scripts Python, procesa video. Es el brazo.
- **Soe** define la visión creativa y decide cuándo usar cada uno.
- **NUNCA** procesar contenido pesado de video con DeepSeek. Usar Claude (ilimitados) para eso.

- **DeepSeek (Hermes/yo)**: genera el guion JSON (estructura ligera, pocos tokens)
- **Claude Code (Fable 5)**: ejecuta el prompt de Canvas, corre el script Python, procesa el video. Aquí van los tokens.
- **NUNCA** procesar contenido pesado de video con DeepSeek. Usar Claude (ilimitados) para eso.

## ⚠️ PEPITA DE ORO: El valor en PANTALLA
Cuando se toman referencias de videos de Canvas/diseño, lo importante está en PANTALLA (configuraciones, parámetros, diagramas). El audio es secundario. Siempre que se procese material visual, priorizar capturar lo que se VE sobre lo que se DICE.

## Visión General
De un prompt de Hermes → a un video profesional renderizado en 1080p, sin intervención humana.
Hermes genera el guion → n8n ejecuta el workflow → Canvas API produce el video → Notion guarda → Telegram notifica.

## Stack
| Componente | Rol |
|---|---|
| **Hermes (yo)** | Genero el guion JSON estructurado |
| **n8n** | Orquesta el workflow completo |
| **Canvas API (Higgsfield)** | Crea proyecto, genera clips, exporta video |
| **Soul ID** | Consistencia facial del personaje en todas las escenas |
| **Notion** | Base de datos de proyectos y assets |
| **Telegram** | Notificación a Soe cuando el video está listo |

## Flujo Completo

```
Hermes → genera guion JSON
  ↓
n8n recibe JSON → parsea → construye payload
  ↓
HTTP POST → Crear Canvas (Higgsfield)
  ↓
Wait 2 min
  ↓
HTTP POST → Generar todos los clips
  ↓
Loop: estado cada 10s (máx 5 min)
  ↓
HTTP POST → Exportar video 1080p
  ↓
Notion → guardar registro (canvas_id, video_url, personaje)
  ↓
Telegram → "🎬 Video listo: [link]"
```

## Estructura del Guion JSON que Hermes Genera

```json
{
  "proyecto": "Nombre del proyecto",
  "personaje": {
    "nombre": "Ana",
    "descripcion": "Mujer joven, mirada cálida, piel clara",
    "soul_id": "ana_character_001"
  },
  "escenas": [
    {
      "numero": 1,
      "titulo": "Entrada a clínica",
      "prompt": "Prompt detallado en inglés, mínimo 30 palabras, con iluminación y emoción",
      "duracion_segundos": 5,
      "movimiento_camara": "dolly_forward",
      "referencia_imagen_url": "url opcional"
    }
  ],
  "configuracion_video": {
    "formato": "9:16",
    "resolucion": "1080p",
    "estilo_visual": "cinematic, luxury, warm tones"
  },
  "metadata": {
    "plataforma_destino": "Instagram Reels",
    "audiencia": "Mujeres 25-45 años"
  }
}
```

## Movimientos de Cámara Disponibles
| Movimiento | Uso |
|---|---|
| dolly_forward | Revelación, acercamiento |
| dolly_out | Cierre, gran escala |
| tilt_up | Grandeza, esperanza |
| tilt_down | Revelación, detalle |
| pan_left / pan_right | Seguir acción |
| orbit | Épico, alrededor del sujeto |
| zoom_in | Drama, énfasis |
| zoom_out | Contexto, cierre |
| static | Diálogos, íntimo |

## Conectores de Escena
- **Conector simple**: un clip sigue al otro
- **Frame connector**: el último frame del clip anterior = primer frame del siguiente (RECOMENDADO)
- **Conector de personaje**: preserva identidad visual entre clips

## Script Python (canvas_automation.py)
Clase `CanvasHighgsfield` con métodos:
- `crear_proyecto_canvas(guion)` → crea proyecto con nodos conectados
- `generar_clips(canvas_id)` → inicia generación de todos los clips
- `obtener_estado(canvas_id)` → polling de progreso
- `exportar_video(canvas_id)` → renderiza MP4 final
- `flujo_completo(guion)` → ejecuta todo el pipeline

## Prompt para que Hermes Genere el JSON
"Eres un guionista experto en videos para redes sociales. Genera un JSON estructurado para un video de [servicio]. Personaje: [nombre]. Duración total: [X] segundos. Plataforma: [formato]. Tono: [estilo]. Mínimo 3 escenas, máximo 7. Cada escena con: numero, titulo, prompt detallado (mín 30 palabras, en inglés), duracion, movimiento_camara. Movimientos variados. Incluir Soul ID. Devuelve SOLO el JSON válido."

## n8n Workflow (10 nodos)
1. Manual Trigger o Cron
2. Hermes MCP → llamar agente guionista
3. Code (JavaScript) → parsear JSON y armar payload Canvas
4. HTTP Request → POST /canvas/crear
5. Wait → 2 minutos
6. HTTP Request → POST /canvas/{id}/generar-todos
7. Loop + Wait → revisar /canvas/{id}/estado cada 10s
8. HTTP Request → POST /canvas/{id}/exportar
9. Notion → crear página con resultado
10. Telegram → notificar con link del video

## Técnicas Avanzadas
- **Soul ID**: entrenar personaje para consistencia facial en todas las escenas
- **Estilos visuales**: "35mm film, Kodak", "golden hour, handheld", "Chiaroscuro, slow motion"
- **Estructura Reel**: hook visual (0-3s) → desarrollo (3-10s) → cierre (10-15s)
- **Estructura Narrativa**: establishing → personaje → conflicto → giro → resolución

## Errores Comunes
- Prompts < 30 palabras → escribir mínimo 30-40
- No usar frame connectors → usarlos entre clips
- No usar Soul ID → entrenar Soul Character
- Prompts en español → usar inglés
- API key en texto plano → solo en Credentials n8n o .env

## Checklist Implementación
- [ ] API Key Higgsfield activa y segura
- [ ] Soul Character entrenado
- [ ] Base Notion para registrar videos
- [ ] Bot Telegram configurado
- [ ] Script Python probado localmente
- [ ] Workflow n8n creado (10 nodos)
- [ ] Código JavaScript pegado en nodo Code
- [ ] Prueba end-to-end exitosa
- [ ] Workflow activado (manual o cron)
- [ ] Flujo replicado para otros personajes
