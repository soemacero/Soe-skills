# Copy-Paste Prompts for Claude Code (Fable 5)

Estos son los prompts exactos. Hermes prepara la materia prima, Soe pega prompt + contenido en Claude Code con Fable 5.

## ⚠️ Regla de recursos

- **DeepSeek (Hermes/yo)**: prepara materia prima, estructura ligera. NO procesar contenido pesado aquí.
- **Claude Code (Fable 5)**: recibe materia prima + prompt, genera SKILL COMPLETO. Tokens ilimitados.
- **NUNCA** gastar tokens de DeepSeek para lo que Claude puede hacer.

## Después de que Claude devuelva el skill

1. Leer el skill que devolvió Claude
2. Pasármelo a mí (Hermes) para integrarlo en la biblioteca de skills
3. Lo guardo con `skill_manage(action='create')` y queda disponible para siempre

---

## 🚀 PROMPT #1 — YouTube/curso → Skill

```
Voy a darte el contenido completo de un video que vi. Las pepitas de oro están en PANTALLA (diagramas, configuraciones, códigos), no solo en el audio. Trabajas con Fable 5, úsalo al máximo.

Tu tarea ÚNICA: convertir TODO este contenido en un SKILL para Hermes Agent con esta estructura exacta:

---
name: [nombre-del-skill]
description: "[descripción en una línea]"
version: 1.0.0
author: Soe Macero + Claude
tags: [tags, relevantes, separados, por, comas]
---

# [Nombre del Skill]

## OBJETIVO
Qué problema resuelve, para quién, qué se logra al final.

## PRERREQUISITOS
Herramientas exactas, cuentas, API keys, instalaciones.

## CONCEPTOS CLAVE
Glosario de términos. Una línea cada uno.

## PASO A PASO
Cada paso: verbo de acción + comando/código EXACTO + cómo validar que funcionó.

## EJEMPLOS PRÁCTICOS
Mínimo 2 ejemplos completos con inputs y outputs.

## TRUCOS DEL INSTRUCTOR
Lo que dice en off, los tips que no están en slides.

## ERRORES COMUNES
Cada error: síntoma → causa → solución exacta.

## CHECKLIST
Lista ordenada para implementar sin saltarse nada.

---

REGLAS ESTRICTAS:
1. Marca CLARAMENTE:
   - [AUDIO] = lo que dice el instructor
   - [PANTALLA] = ⭐ lo que se ve (configuraciones, prompts, diagramas)
   - [NOTA] = mis observaciones
2. Si algo solo está en pantalla, transfórmalo a texto COMPLETO en el skill
3. Identifica los momentos "esto es lo que importa" y ponlos como citas textuales
4. El skill debe ser ejecutable por alguien que NUNCA vio el video
5. Mínimo 3 escenas de ejemplo si aplica, con prompts detallados

AQUÍ ESTÁ EL CONTENIDO:
[pégalo aquí]
```

---

## 🚀 PROMPT #2 — Libro/PDF → Skill

```
Convierto este libro/material en un skill para Hermes Agent. Trabajas con Fable 5.

Estructura obligatoria:

---
name: [nombre]
description: [descripción]
version: 1.0.0
author: Soe Macero + Claude
tags: []
---

# [Nombre]

## PRINCIPIOS FUNDACIONALES
Las 3-5 ideas fuerza del libro que lo sostienen todo.

## EL SISTEMA
El método o framework que propone el autor, descrito como pasos secuenciales.

## HERRAMIENTAS MENTALES
Conceptos, marcos de decisión, preguntas que enseña.

## ACCIONES CONCRETAS
Qué hacer MAÑANA con esto. Implementación inmediata, no teoría.

## LO QUE NO HACER (Antipatrones)
Lo que el libro dice explícitamente que evites.

## MÉTRICAS DE ÉXITO
Cómo saber si lo estás aplicando bien. Qué medir y cada cuánto.

## CITAS CLAVE
Las 3-5 frases textuales del autor que resumen el libro.

---

REGLAS:
- Traduce ideas abstractas a instrucciones accionables
- El skill debe servir para que alguien APLIQUE el libro sin haberlo leído
- Nada de descripción genérica. Cada línea debe poder ejecutarse

CONTENIDO:
[pégalo aquí]
```

---

## 🚀 PROMPT #3 — Manual práctico → Skill

```
Convierto este manual práctico paso a paso en un skill para Hermes Agent. Trabajas con Fable 5.

Estructura obligatoria:

---
name: [nombre]
description: [descripción]
version: 1.0.0
author: Soe Macero + Claude
tags: []
---

# [Nombre]

## QUÉ VAS A LOGRAR
El resultado final del manual en una frase.

## STACK
Herramientas exactas con versiones.

## CONFIGURACIÓN INICIAL (1 vez)
API keys, cuentas, instalaciones, variables de entorno. Nada se asume.

## DIAGRAMA DE FLUJO
Input → Paso 1 → Paso 2 → ... → Output (usa flechas, no párrafos)

## PASOS DETALLADOS
- Cada paso empieza con VERBO DE ACCIÓN
- Incluye el COMANDO EXACTO (no "instala X", sino "pip install Y")
- Incluye el CÓDIGO COMPLETO, no fragmentos
- Incluye los JSON de ejemplo COMPLETOS
- Incluye cómo validar cada paso (código HTTP, mensaje esperado)

## PLANTILLAS
Scripts y configuraciones completas para copiar y pegar.

## ERRORES FRECUENTES
Cada error: síntoma → causa → solución.

## CHECKLIST
Ordenado. Para tachar al completar cada paso.

---

REGLAS:
- NO generalices. "Configura la API" → muestra la línea exacta
- NO asumas contexto. Cada paso ejecutable por un principiante
- Si hay opciones, marca cuál es la RECOMENDADA
- Scripts COMPLETOS, no referencias externas

CONTENIDO:
[pégalo aquí]
```

---

## 🚀 PROMPT #4 — Canvas Higgsfield Execution

```
Tienes Fable 5. Eres el brazo ejecutor de Hermes Agent (Soe Macero). Tu misión es ejecutar este pipeline:

1. Toma esta historia/idea: [descripción del anuncio]
2. Genera un JSON de guion estructurado con 5-8 escenas
3. Cada escena: prompt en inglés (40+ palabras), movimiento de cámara variado, duración 3-6s
4. Incluye Soul ID si aplica: [soul_id o "ninguno"]
5. Formato: [9:16 o 16:9], resolución: 1080p
6. Guarda el JSON como guion.json
7. Ejecuta el script Python canvas_automation.py con ese JSON
8. Espera a que termine y dime la URL del video final

Devuelve SOLO: el JSON del guion + la URL del video.
```
