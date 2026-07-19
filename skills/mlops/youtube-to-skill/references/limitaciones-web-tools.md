# Limitaciones de Web Tools en este VPS

## Estado actual
- **web_search**: ✅ Funciona con DuckDuckGo (ddgs). Sin API key, sin límites.
- **web_extract**: ❌ NO funciona con ddgs. ddgs es search-only.
- **Backends que sí soportan extract**: firecrawl, tavily, exa, parallel.
- **yt-dlp**: ⚠️ Funciona solo para videos SIN restricción de auth. Fallará con "Sign in to confirm you're not a bot" si el video requiere cookies.
- **youtube-transcript-api**: ✅ Funciona sin auth para videos CON subtítulos públicos.

## Por qué falló la extracción del video
- yt-dlp requiere autenticación de YouTube (cookies de navegador)
- Sin cookies, el VPS no puede descargar videos de YouTube
- youtube-transcript-api requiere que el video tenga subtítulos públicos

## Soluciones para cuando el VPS no puede acceder a un recurso
1. **YouTube sin subtítulos**: pedir al usuario que vea el video en su PC y tome notas visuales
2. **YouTube con subtítulos**: youtube-transcript-api funciona sin auth
3. **Páginas web sin extract**: usar `execute_code` + `requests` para scraping manual
4. **Contenido detrás de auth**: el usuario debe proporcionar el contenido directamente

## Nota para YouTube + Soe
Soe tiene acceso directo a YouTube desde su PC personal. Cuando el VPS no pueda descargar:
1. Ella ve el video en su PC
2. Toma notas de lo que ve en PANTALLA (configuraciones, diagramas, prompts)
3. Me pasa las notas + transcripción si existe
4. Yo preparo estructura ligera, ella completa con Claude Code (F5)

## Próximo paso cuando se configure web extract
- Instalar firecrawl API key o tavily
- Cambiar `web.extract_backend` en config.yaml
- Probar con `web_extract(urls=[...])`
