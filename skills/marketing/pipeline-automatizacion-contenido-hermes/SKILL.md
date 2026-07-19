---
name: pipeline-automatizacion-contenido-hermes
description: "Pipeline completo para campañas de fotos y video de producto/moda con IA orquestado desde Hermes. Hermes genera prompts y gestiona referencias; Claude Code ejecuta Higgsfield CLI. Con feedback loop de mejora continua vía Google Sheets."
version: 1.0.0
author: Soe Macero + Hermes
tags: [higgsfield, cli, automatizacion, contenido, producto, seedance, feedback-loop, pipeline, hermes-orquestador]
---

# Pipeline de Automatización de Contenido desde Hermes

## Diferencia Clave con Versión Claude Code
Este skill reemplaza a Claude Code como ORQUESTADOR. Hermes (yo) genero los prompts, gestiono los UUIDs, trackeo el feedback, y orquesto todo. Claude Code solo se usa en tu PC para ejecutar la Higgsfield CLI (subir imágenes, correr batches). Yo hago el resto.

## Stack
| Componente | Rol | Dónde |
|---|---|---|
| **Hermes (yo)** | Orquestador, generación prompts, tracking | VPS |
| **Claude Code** | Brazo ejecutor de Higgsfield CLI | Tu PC |
| **Higgsfield CLI** | Motor de generación (Nano Banana Pro + Seedance 2.0) | Tu PC local |
| **Google Sheets** | Feedback tracker + loop de mejora continua | Cloud |
| **WhisperFlow** (opcional) | Dictado rápido de prompts | Tu PC |

## Estructura de Carpetas (en tu PC)
```
Claude x GenHQ automation/
├── environment-references/   # Imágenes de entornos + .md descriptor con UUIDs
├── model-references/         # Character sheets + outfits + UUIDs
├── product-references/       # Fotos del producto todos los ángulos + material descriptors
├── outputs/                  # Lo generado
├── prompt-log.md             # Historial completo de prompts por batch
├── reference-ids.md          # UUID ↔ nombre de archivo
├── seedance-prompt-failure-log.md  # Fallos y lecciones aprendidas
├── seedance-prompt-foundations.md  # Framework de prompting (2+ años de experiencia)
└── handoff.md                # Overview + cuentas + reglas + UUIDs maestros
```

## Flujo de Trabajo

### Fase 1: Setup Inicial (1 vez, en tu PC con Claude Code)
1. Instalar Higgsfield CLI: `npm install -g @higgsfield/cli`
2. Iniciar sesión: `higgsfield auth login` → "device authorized"
3. Instalar los 4 skills de Higgsfield
4. Crear carpeta plantilla y dársela a Claude

### Fase 2: Preparar Referencias
1. Subir entornos (~18 imágenes) → Claude extrae UUIDs y crea .md descriptor
2. Subir character sheets de modelo(s) → extraer UUIDs
3. Subir product sheets (todos los ángulos) → extraer UUIDs
4. Incluir descriptores de material en product sheets (ej: "obsidiana, brillante, refracta luz")
5. Escribir reglas: "solo usar character sheet + product sheet, NUNCA fotos editoriales como referencia"

### Fase 3: Generar Contenido
Yo (Hermes) genero el prompt exacto. Tú lo pegas en Claude Code para que ejecute el batch.

**Prompt para batch de video:**
> "I would like you to create [N] videos with Seedance 2.0, of [modelo(s)], all inside environment [X]. Dynamic camera motions and controls, unique camera angles. Duration: [X] seconds. Aspect ratio: [16:9/9:16]."

**Prompt para batch de imágenes:**
> "Use environment [X] and generate [N] images where [X] are [estilo] and [Y] are [otro estilo]. Unique camera angles, play with depth/blur. [Modelo(s)]. Aspect ratio: [16:9/9:16]."

**Prompt para product shots:**
> "White background, create a product sheet that covers all angles of this product. Six separate images all inside of one photo."

### Fase 4: Feedback Loop (la clave del sistema)
1. Revisas resultados en Google Sheets
2. Marcas status: ✅ Approved / ❌ Rejected / 🟡 Pending
3. En rechazados: nota específica y accionable (ej: "proporciones del producto muy grandes vs modelo")
4. Me dices los resultados
5. Yo ajusto los prompts futuros basado en el feedback

### Fase 5: Escalar
- **Routines**: generación automática programada (ej: "6am genera X videos e imágenes")
- **Auto-logging**: cada batch actualiza prompt-log.md y reference-ids.md
- **Auto-feedback**: basado en reglas de calidad
- **Outreach**: conectar Gmail para enviar contenido aprobado

## Reglas Críticas
1. ⚠️ NUNCA usar fotos editoriales/detail como referencia de personaje o producto
2. ✅ Siempre usar character sheet + product sheet (trainer sheet)
3. 📝 Incluir descriptores de material en product sheets
4. 🔗 Si múltiples personajes → reglas de asociación personaje↔producto
5. 📊 Batch máximo: 6 jobs de Seedance concurrentes (límite plan Creator)
6. 🎯 End screens: mejor subir PNG transparente del logo
7. 🧠 El sistema aprende con cada ronda de feedback — volumen + criterio = mejora

## Errores Comunes
| Síntoma | Causa | Solución |
|---|---|---|
| Job falla sin error | Límite 8 concurrentes | Batch de 6 en 6 |
| Video rechazado por guidelines | Palabra disparó moderación | Registrar en failure log |
| Producto desproporcionado | Falta guía de escala | Marcar Rejected + nota |
| End screen alucina | Prompt vago | Usar PNG del logo |
| Seedance copia foto literal | Usaste detail image como ref | Reforzar regla |
