# Método LLM Wiki (Karpathy) — Memoria Persistente para Agentes

Sistema de Andrej Karpathy para construir "memoria infinita" para agentes de IA usando Obsidian.

## El problema que resuelve

RAG clásico: subes PDF, modelo busca fragmento relevante, responde, y en nueva sesión todo se pierde. No hay acumulación real de conocimiento entre sesiones ni entre agentes.

LLM Wiki: en vez de buscar documentos crudos cada vez, el modelo construye y mantiene una wiki tipo Wikipedia — archivos Markdown interconectados — que le permite navegar relaciones en vez de buscar a ciegas.

## Arquitectura de 3 capas

1. **Fuentes crudas (raw/)**: archivos originales sin clasificar (transcripciones, PDFs, artículos)
2. **La wiki (wiki/)**: archivos Markdown interconectados generados a partir de raw. Incluye páginas de conceptos, entidades, síntesis. Cada nuevo contenido se procesa, etiqueta y relaciona con existentes.
3. **El esquema (AGENTS.md / CLAUDE.md / SOUL.md)**: system prompt que indica al modelo cómo comportarse sobre la wiki.

El **índice** es la pieza central: primera página que el agente consulta. Cada pregunta navega desde el índice hacia nodos relevantes — reduce drásticamente el espacio de búsqueda (ejemplo real: de 88 archivos a solo 7 relevantes).

## Por qué funciona mejor que RAG (para ~90% de casos pyme)

| Aspecto | RAG tradicional | LLM Wiki |
|---|---|---|
| Método | Vectoriza y trocea, busca por similaridad semántica | Navega relaciones directas entre archivos Markdown vía índice |
| Costo | Requiere vector database, costo recurrente | Archivos de texto plano, sin costo |
| Precisión | Puede traer contenido "parecido" pero no exacto | Sigue camino determinado y explícito, menos alucinaciones |
| Portabilidad | Atado a infraestructura de vectores | Solo una carpeta — portable entre Claude Code, Hermes, Codex, OpenClaw |
| Ahorro tokens | Variable | Reportado: 95% de ahorro por consulta con 383 archivos comprimidos |

**Cuándo sí conviene RAG**: escala enterprise con cientos de miles de documentos.

## Las 4 operaciones básicas

1. **Ingest** — contenido nuevo se interpreta, clasifica, etiqueta, se le crea página propia y se actualizan temas relacionados
2. **Query** — consulta directa sobre la wiki
3. **Lint** — detecta archivos huérfanos sin conexiones y los integra a la red
4. **Bulk ingest** — procesa muchos archivos de una sola vez (para poblar la wiki inicial)

## Cómo armarlo

1. Crear Vault en Obsidian con nombre descriptivo
2. Abrir esa misma carpeta con un agente (Claude Code, Hermes, etc.)
3. Usar el repo público llm-wiki de Karpathy en GitHub como referencia
4. Pedir al agente: "Crea un agente que mantenga [contenido] organizado. Crea AGENTS.md, índice, log, carpetas raw/ y wiki/"
5. Poblar la wiki: pedir al agente que extraiga info de fuentes e ingiera. Usar Obsidian Clipper para contenido puntual
6. Ejecutar Lint para conectar archivos huérfanos
7. A partir de ahí, cualquier pregunta navega el índice y las relaciones

## Aplicación directa a Soe

Este método puede estructurar todo el conocimiento de Le CliniQ (guiones, casos de clientas, método S.M.A.R.T. Brows™) como una wiki en Obsidian conectada a Hermes como base de conocimiento externa, portable entre agentes.
