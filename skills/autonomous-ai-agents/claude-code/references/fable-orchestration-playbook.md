# Playbook de Orquestación con Fable 5 (Diego Cardoso Style)

Este documento detalla el patrón de diseño agéntico para ejecutar **Claude Fable 5** como orquestador principal (Director de Orquesta) sobre subagentes más económicos en Claude Code (como Opus y Sonnet), permitiendo optimizar el consumo de tokens y presupuesto hasta un 90% sin perder calidad.

## 🎼 Arquitectura de la Orquesta
1. **Fable 5 (Max Reasoning) - Orquestador:** Planifica, descompone la tarea, supervisa la calidad y sintetiza la solución final.
2. **deep-reasoner (Claude 3 Opus) - Razonador Profundo:** Se invoca para tareas complejas de arquitectura, depuración de algoritmos y análisis conceptual pesado.
3. **fast-worker (Claude 3.5 Sonnet) - Trabajador Rápido:** Ejecuta tareas mecánicas, generación de boilerplate, formateo de código, pruebas unitarias y ediciones sencillas de forma rápida y barata.
4. **Codex (Peer Engineer) - Perspectiva Paralela:** Un desarrollador senior alternativo (vía OpenAI Codex CLI) que aporta un enfoque independiente y complementario en paralelo con el razonador profundo.

## 🛠️ Configuración en Claude Code

### 1. Establecer el Orquestador y Esfuerzo Máximo
En tu terminal interactiva de Claude Code local, configura el modelo principal:
```bash
/model Fable 5
/effort max
```

### 2. Crear los Subagentes Especializados
Ejecuta el asistente `/agents` y crea estos dos agentes permanentes con sus prompts correspondientes:

- **deep-reasoner** (pinned to `opus`):
  > "Use for reasoning-heavy phases, architecture, debugging complex issues, algorithm design. Think thoroughly, return a concise conclusion the orchestrator can act on."

- **fast-worker** (pinned to `sonnet`):
  > "Use for mechanical tasks, boilerplate, tests, formatting, simple edits. Execute efficiently."

### 3. Integración de Codex (Opcional)
Si tienes el Codex CLI en tu sistema, añade su plugin a Claude Code:
```bash
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/codex:setup
```

### 4. Plantilla de Configuración para `CLAUDE.md`
Agrega la siguiente sección a tu archivo `CLAUDE.md` o `.claude/rules/orchestration.md` para indicarle a Fable cómo liderar:

```markdown
## Orchestration workflow  
You (Fable) are the orchestrator. Plan, decompose, synthesize.  
Reasoning-heavy phases → deep-reasoner  
Mechanical work → fast-worker  
Codex (/codex:rescue --background) is a cracked engineer on par with deep-reasoner, from a different perspective. Treat as a peer, not a reviewer.  
High-stakes decisions: task Opus + Codex on the same problem in parallel, synthesize the best of both, without showing either the other's answer. Keep your own context lean.   
```

## 🎯 Ejemplo de Prompt para Ejecución (Como Tech Lead)
Pídele a Claude Code tus objetivos usando esta estructura directiva:
```text
Objetivo: [Tu meta, ej: Integrar n8n con la API de Meta Ads]
Contexto: [Estructura del proyecto, limitaciones, credenciales .env]
Tú eres el Director de Orquesta. Planifica la tarea, delega el diseño de arquitectura a deep-reasoner, el código repetitivo a fast-worker, y pídele una opinión de revisión a Codex. Muéstrame tu plan de delegación primero y luego ejecútalo de forma secuencial.
```
