# 🏪 Soe-Skills

Repotenciando agentes IA para marketing digital.

Skills personalizadas de Soe para sus agentes Hermes (Ghost/IAm IA).

## Skills incluidas

| Skill | Descripción | Estado |
|-------|-------------|--------|
| **soe-hermes-setup** | Configuración y mantenimiento de Hermes en VPS Hostinger | ✅ |
| **soe-marketing-agent** | Estratega de marketing para Le Cliníq | ✅ |
| **hermes-gateway-setup** | Configuración del gateway Telegram | ✅ |
| **local-llm-integration** | Conexión Ollama + Hermes | ✅ |
| **hermes-migration-and-archiving** | Migración y backup de Hermes | 📝 Pendiente |
| **hermes-windows-troubleshooting** | Solución de problemas en Windows | 📝 Pendiente |

## Uso

Cada skill está en `skills/<nombre>/SKILL.md` con formato estándar de Hermes (frontmatter YAML + markdown). Las skills se cargan desde aquí mediante symlink o copia a `~/.hermes/skills/`.

## Estructura

```
Soe-skills/
├── README.md
└── skills/
    ├── soe-hermes-setup/
    │   └── SKILL.md
    ├── soe-marketing-agent/
    │   ├── SKILL.md
    │   └── references/
    ├── hermes-gateway-setup/
    │   ├── SKILL.md
    │   └── references/
    ├── local-llm-integration/
    │   ├── SKILL.md
    │   ├── references/
    │   └── templates/
    ├── hermes-migration-and-archiving/
    └── hermes-windows-troubleshooting/
```