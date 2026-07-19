# Guía de Solución de Problemas y Despliegue en Windows (PC ANGEL)

Esta referencia recopila los aprendizajes y resoluciones de errores técnicos críticos ocurridos durante la configuración de Hermes Agent y Ollama de forma local en entornos Windows (específicamente en la PC con usuario `ANGEL` y terminal `PowerShell`).

---

## 🚨 1. El Bug de la "Ruta Fantasma" (AppData vs. .hermes)

*   **Síntoma:** Editas el archivo de configuración en `C:\Users\ANGEL\.hermes\config.yaml` pero el agente Hermes ignora por completo tus cambios, sigue leyendo variables viejas o arrojando errores del token antiguo.
*   **Causa:** En instalaciones de Windows, Hermes posee una ruta de configuración en la carpeta de la aplicación local que tiene prioridad absoluta sobre la carpeta del usuario:
    `C:\Users\ANGEL\AppData\Local\hermes\config.yaml`
*   **Solución:** Los scripts y comandos de edición manual de PowerShell deben escribir y sobreescribir la configuración directamente en la ruta oculta de AppData:
    ```powershell
    $SystemPath = "C:\Users\ANGEL\AppData\Local\hermes\config.yaml"
    # Escribir o abrir este archivo directamente
    notepad "C:\Users\ANGEL\AppData\Local\hermes\config.yaml"
    ```

---

## 🚨 2. El Conflicto de Expansión del Símbolo `$` en Windows

*   **Síntoma:** Al arrancar el gateway (`hermes gateway run`), el servidor se cae inmediatamente con el error:
    `Failed to connect to Telegram: The token '$TELEGRAM_BOT_TOKEN' was rejected by the server.`
*   **Causa:** A diferencia de Linux/Unix, PowerShell y el parser de Windows no expanden automáticamente el símbolo `$` (variables de entorno como `$TELEGRAM_BOT_TOKEN` especificadas en el `.env`) dentro del archivo `config.yaml`. El sistema lee la cadena literalmente como si ese fuera tu token real de Telegram.
*   **Solución:** Escribir el token de Telegram directamente como un texto (string) duro entre comillas dentro del archivo `config.yaml` en la sección correspondiente:
    ```yaml
    telegram:
      bot_token: "8501390565:AAE..."
      enabled: true
    ```

---

## 🚨 3. Error de Librería de Logs y Pip Desaparecido en el Venv

*   **Síntoma:** Al inicializar Hermes por primera vez, el sistema colapsa con el error:
    `Failed to initialize agent: No module named 'concurrent_log_handler'`
    Al intentar instalarlo con `python -m pip install concurrent-log-handler`, la terminal devuelve:
    `No module named pip`
*   **Causa:** El entorno virtual (venv) de Hermes en Windows (`C:\Users\ANGEL\AppData\Local\hermes\hermes-agent\venv\`) se instaló de forma corrupta, tiene el ejecutable de Python pero no incluye el gestor de paquetes `pip` ni la librería de control de logs.
*   **Solución:** Reconstruir e inyectar `pip` dentro del entorno virtual de Hermes usando el módulo integrado de restauración de Python (`ensurepip`), e instalar la librería faltante apuntando directamente al ejecutable del venv:
    ```powershell
    # 1. Reconstruir e inyectar pip en el venv
    C:\Users\ANGEL\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m ensurepip --default-pip

    # 2. Instalar la librería de control de logs desde el venv reparado
    C:\Users\ANGEL\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m pip install concurrent-log-handler
    ```

---

## 🚨 4. Conflicto de Puertos y Procesos Gateway Fantasma (PID Conflict)

*   **Síntoma:** Al encender Hermes por consola, el sistema devuelve un error indicando que ya hay otra instancia corriendo:
    `X Another gateway instance is already running (PID 2636).`
*   **Causa:** Un proceso anterior del servidor de Telegram quedó colgado y ejecutándose en segundo plano en Windows, bloqueando el puerto de escucha y el archivo de bloqueo de Hermes.
*   **Solución:** Forzar el reemplazo del proceso usando el parámetro `--replace` o matando todos los procesos de Hermes desde PowerShell antes de volver a encenderlo:
    ```powershell
    # Opción A: Reemplazar el gateway en caliente (Recomendado)
    hermes gateway run --replace

    # Opción B: Matar todos los procesos "hermes" colgados en Windows
    Stop-Process -Name "hermes" -Force -ErrorAction SilentlyContinue
    ```

---

## 🚨 5. El error del Formato BOM en Notepad de Windows

*   **Síntoma:** Tras editar el archivo `config.yaml` de forma manual usando el Bloc de Notas (Notepad) de Windows, Hermes lanza errores extraños de formato o ignora los parámetros nuevos por completo.
*   **Causa:** Notepad de Windows tiene la mala práctica de guardar archivos de texto codificados con **BOM (Byte Order Mark)** invisibles al inicio. Esto "rompe" la lectura del parser de YAML de Hermes, que no reconoce los caracteres invisibles iniciales.
*   **Solución:** 
    *   Re-guardar el archivo como "UTF-8 sin BOM" (usando un editor como VS Code o Notepad++).
    *   O bien, forzar la escritura limpia en UTF-8 puro utilizando código de PowerShell de forma directa para puentear el Bloc de Notas:
        ```powershell
        $YamlClean = @"
        model:
          default: ollama/llama3.1:8b
          provider: ollama
          base_url: http://localhost:11434

        telegram:
          bot_token: "TU_TOKEN_REAL"
          enabled: true
        "@
        [System.IO.File]::WriteAllText("C:\Users\ANGEL\AppData\Local\hermes\config.yaml", $YamlClean, [System.Text.Encoding]::UTF8)
        ```

---

## 🚨 6. Upgrade Estratégico a Gemini 3.5 Flash en la Nube

*   **Síntoma:** El bot de Telegram principal en Hostinger consume demasiados tokens bajo el proveedor "nous" o se cae por parpadeos de red al procesar contextos de conversación muy extensos.
*   **Causa:** El uso de modelos grandes o el canal de Nous con re-lecturas completas de historial infla el consumo. Google Gemini 1.5/2.5 tiene capacidades limitadas en comparación al potencial autónomo y ágil.
*   **Solución:** Migrar el cerebro en la nube en tu Hostinger al modelo de última generación **`google/gemini-3.5-flash`** (con la Google API Key del usuario). Proporciona capacidades agénticas de nivel Pro a costo de centavos o gratuito en la consola de Google.
    *   Comando para fijar el modelo en Hostinger:
        ```bash
        /opt/venv/bin/hermes config set model.default google/gemini-3.5-flash
        ```

---

## 🚨 7. Error HTTP 404 con Proveedor "custom" en Ollama Local

*   **Síntoma:** Al arrancar Hermes, la terminal entra en un bucle de intentos de conexión fallidos y lanza el error:
    `Error: HTTP 404: 404 page not found` apuntando a `http://localhost:11434`.
*   **Causa:** El archivo `config.yaml` o la selección de modelo se configuró con el proveedor genérico `custom` apuntando al endpoint base `http://localhost:11434`. Al usar `custom`, Hermes asume que el servidor cumple con el estándar de OpenAI en la ruta raíz y concatena `/chat/completions`. Ollama no soporta esa ruta en su raíz; necesita el prefijo `/v1` o el formateador nativo de Ollama.
*   **Solución:** 
    *   Cambiar el proveedor a `ollama` de forma nativa (la opción correcta que maneja los endpoints específicos de Ollama de forma automática).
    *   O bien, forzar la ruta OpenAI-compatible en el `base_url` agregando el sufijo `/v1` manualmente en tu `config.yaml`:
        ```yaml
        model:
          provider: custom
          base_url: http://localhost:11434/v1
        ```

---

## 🚨 8. Selección Incorrecta de "Ollama Cloud" (Opción 20) vs. Ollama Local

*   **Síntoma:** Al correr `hermes model` para configurar tu Ollama de casa, el instalador te detiene pidiendo obligatoriamente una clave de API:
    `No Ollama Cloud API key configured. OLLAMA_API_KEY (or Enter to cancel):`
*   **Causa:** Se seleccionó por error la opción `20. Ollama Cloud`. Esta opción es para el servicio de pago en la nube alojado en internet por los creadores de Ollama. No es tu motor local gratuito que corre en la tarjeta de video de tu laptop.
*   **Solución:**
    1.  Presiona **Enter** sin escribir nada para cancelar y salir de la solicitud.
    2.  Ejecuta nuevamente `hermes model`.
    3.  Sube en la lista de opciones (usualmente entre las opciones del 1 al 10) y busca la opción simple que dice **`Ollama`** o **`Ollama (local)`**.
    4.  Esta opción no te pedirá ninguna clave (API key) y auto-detectará los modelos descargados en tu disco local (`llama3.1:8b`, `qwen2.5:14b`, etc.) de forma 100% gratuita.
