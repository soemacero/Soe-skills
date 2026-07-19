# GPT-Live: Full-Duplex Voice — Research Notes

> OpenAI, lanzado 8 de julio 2026. Reemplaza Advanced Voice Mode en ChatGPT.

## Qué es
Arquitectura **full-duplex**: habla y escucha al mismo tiempo. No es turn-based como antes. Puede:
- Decir "mhmm" mientras tú hablas
- Interrumpir naturalmente
- Quedarse en silencio cuando piensas
- Retomar la conversación sin perder el hilo

## Arquitectura interna (2 capas)
1. **Modelo ligero y rápido**: mantiene el flujo continuo de voz
2. **Delegación silenciosa**: pasa tareas complejas (búsqueda, razonamiento profundo) a GPT-5.5 en background y teje la respuesta en la conversación viva

## Estado de API
| Fecha | Estado |
|---|---|
| Jul 2026 | ❌ Solo en ChatGPT apps (iOS, Android, web) |
| Jul 2026 | 🎯 OpenAI aceptando **design partners** |
| Jul 2026 | 📝 Formulario de notificación abierto para developers |
| ¿Próximo? | API pública `gpt-live-1` y `gpt-live-1-mini` |

## Lo que existe en la API hoy
- **Realtime API**: `gpt-realtime-2.1`, `gpt-realtime-2.1-mini`, `gpt-realtime-translate`, `gpt-realtime-whisper`
- Es **turn-based avanzado**, NO full-duplex
- No es lo mismo que GPT-Live

## Qué nos falta vs GPT-Live

| Capacidad | GPT-Live | Hermes hoy |
|---|---|---|
| Full-duplex | ✅ | ❌ (turn-based) |
| Interrupciones naturales | ✅ | ❌ |
| Backchannel ("mhmm") | ✅ | ❌ |
| Voz humana real | ✅ GPT-Live-1 | ✅ ElevenLabs "soe premium" |
| Velocidad ajustable | ✅ | ✅ 1.2 fijo |
| Razonamiento delegado | ✅ GPT-5.5 | ✅ DeepSeek + Claude |
| STT local | ❌ (cloud) | ✅ Whisper local |
| Sin conexión | ❌ | ✅ Posible |
| Tools / MCP | ❌ Solo voz | ✅ Higgsfield, web, skills |
| Skills guardados | ❌ | ✅ Biblioteca de skills |

## Plan de integración futura
Cuando OpenAI publique la API:

1. Hermes detecta que quieres hablar por voz
2. Abre un stream full-duplex con GPT-Live-1
3. Tú hablas, Hermes escucha y procesa en tiempo real
4. Si necesita algo complejo → delega a DeepSeek o Claude en background
5. Responde con voz natural (ElevenLabs o GPT-Live), sin pausas, sin turnos
6. Si necesita ejecutar una tool (generar video, buscar web) → la ejecuta mientras conversa

## Links relevantes
- https://openai.com/index/introducing-gpt-live/
- https://x.com/OpenAIDevs/status/2074915334377844896 (anuncio de API futura)
