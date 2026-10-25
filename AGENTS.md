# Guía Operativa y Reglas de Trabajo para Agentes (AGENTS.md)
**Proyecto:** Comercio Popular, Barrial y Movilidad Integrada en la CDMX  
**Marco:** Chilangatón 2026 — Reto 1: Comercio Popular y Barrial (SEDECO / SECTEI / SAF)  
**Ubicación:** `AGENTS.md`  

Este documento define las directrices obligatorias, protocolos de sincronización, estándares técnicos y principios éticos que **todos los agentes de IA y desarrolladores** deben acatar al trabajar en este repositorio.

---

## 🚨 1. Regla de Oro: Ciclo Obligatorio de Git (Commit & Push Continuo)

Para mantener la sincronización continua entre agentes concurrentes y el equipo de desarrollo:

1. **Commit y Push tras cada cambio o tarea:**
   * Cada vez que se complete una tarea del backlog, se normalice un dataset, se actualice la documentación o se modifique el código/interfaz, el agente **DEBE hacer `git add`, `git commit` y `git push origin main` inmediatamente**.
   * **Prohibido terminar el turno dejando cambios locales sin commitear y pushear.**
2. **Formato de Commits:**
   * Usar prefijos claros bajo la convención *Conventional Commits*:
     - `feat:` Nuevas funcionalidades, capas en el mapa o módulos de software.
     - `data:` Procesamiento, normalización o descarga de datasets.
     - `docs:` Actualizaciones a `TODO_PROYECTO.md`, `FUENTES_Y_BIBLIOGRAFIA.md`, READMEs o guías.
     - `fix:` Corrección de errores en scripts, geometrías, coordenadas o estilos.
     - `refactor:` Optimización de código o reorganización de carpetas sin alterar la funcionalidad.
   * Mensajes concisos y descriptivos en español o inglés técnico (ej. `data: normalizar horarios y clasificacion fija/movil en directorio unificado`).
3. **Manejo de Cambios Concurrentes:**
   * Como hay múltiples agentes operando en simultáneo, antes de realizar cambios o push, verificar el estado remoto con `git pull --rebase` para evitar colisiones.
4. **Higiene del Repositorio:**
   * Respetar rigurosamente el `.gitignore`. **Nunca commitear:**
     - Archivos temporales del sistema (`.DS_Store`, `Thumbs.db`).
     - Cachés de Python (`__pycache__/`, `*.pyc`).
     - Archivos binarios pesados o volcados temporales innecesarios.

---

## 🛡️ 2. Principios Éticos y Soberanía de Datos (Comercio Popular)

El reto 1 trata sobre la economía popular, tianguistas, locatarios de mercados públicos y tienditas de barrio. Cualquier desarrollo debe alinearse con la investigación de campo del dossier:

1. **No al Extractivismo de Datos (Principios CARE):**
   * La tecnología debe entregar valor inmediato al comerciante (ahorro de tiempo, visibilidad, cobro sin comisiones abusivas) antes de solicitar datos.
   * **Estrictamente prohibido:** Diseñar modelos de negocio extractivos, scores crediticios abusivos o monetización de datos de personas comerciantes para intermediarios corporativos.
2. **Protección de Datos Sensibles:**
   * **Bajo ninguna circunstancia** se recolectarán, procesarán ni registrarán datos relacionados con extorsión, cobro de piso, situaciones fiscales individuales punitivas o condición migratoria.
3. **Filosofía Offline-First / Local-First:**
   * El 87.8% del comercio popular opera en efectivo y la conectividad en tianguis y naves de mercado suele ser deficiente.
   * Todo componente orientado al comerciante debe funcionar sin conexión a internet (IndexedDB / localStorage / PWA ligera) y sincronizarse solo cuando el usuario lo decida.
4. **Respeto a la Gobernanza Comunitaria Existente:**
   * Mercados y tianguis cuentan con mesas directivas, comisiones electas en asamblea y dinámicas barriales históricas. Las soluciones digitales deben respaldar estos acuerdos colectivos, no imponer burocracias verticales desde arriba (lección del fracaso y derogación de las cédulas digitales de SEDECO en 2025).

---

## 📐 3. Estándares Técnicos y Calidad de Datos

1. **Georreferenciación Obligatoria WGS84:**
   * Todas las coordenadas geográficas deben validarse en grados decimales estándar WGS84 (`lat`, `lng`).
   * Si un dataset fuente contiene proyecciones métricas (UTM Zona 14N) o coordenadas en `0.0`, el script ETL debe transformarlas matemáticamente o aislar los registros no georreferenciados con una bandera `coordenadas_validas: false`.
2. **Nombres Canónicos de Alcaldías:**
   * Usar estrictamente las **16 alcaldías oficiales de la CDMX en mayúsculas sin acentos**:
     `ALVARO OBREGON`, `AZCAPOTZALCO`, `BENITO JUAREZ`, `COYOACAN`, `CUAJIMALPA DE MORELOS`, `CUAUHTEMOC`, `GUSTAVO A. MADERO`, `IZTACALCO`, `IZTAPALAPA`, `LA MAGDALENA CONTRERAS`, `MIGUEL HIDALGO`, `MILPA ALTA`, `TLAHUAC`, `TLALPAN`, `VENUSTIANO CARRANZA`, `XOCHIMILCO`.
3. **Formatos Duales (JSON y CSV):**
   * Todo dataset procesado debe exportarse en formato `.json` (optimizado para consumo web / Leaflet / APIs) y en formato `.csv` (para pandas, hojas de cálculo y auditoría rápida).
4. **Reproducibilidad y Código Probado:**
   * Las transformaciones no se hacen de forma manual. Deben residir en scripts reproducibles en `data/processed/` o `scripts/`.
   * Todo script debe probarse y verificar que termine con código de retorno `0` antes de dar la tarea por concluida.

---

## 📝 4. Protocolo de Documentación Continua

Para evitar que la documentación se desactualice:

1. **Actualización de Backlog (`TODO_PROYECTO.md`):**
   * Cada vez que se complete una tarea, actualizar su casilla a `[x]` e incluir un breve resumen técnico en el backlog.
   * Si se descubre una nueva necesidad técnica o integración, agregarla como una subtarea con su respectivo identificador.
2. **Actualización de Fuentes (`FUENTES_Y_BIBLIOGRAFIA.md`):**
   * **Obligatorio:** Cada vez que se consulte, sondee o descargue una nueva página web, portal de datos, API, servicio WFS o referencia periodística/académica, se debe incorporar de inmediato a la sección correspondiente de `FUENTES_Y_BIBLIOGRAFIA.md` con su enlace URL completo y descripción del uso.
3. **Documentación de Carpetas (`README.md` locales):**
   * Las subcarpetas clave (`data/`, `data/processed/`, `data/catalog/`, `data/docs/`, `scripts/`) deben mantener actualizado su `README.md` con el inventario de archivos que contienen.

---

## 🤝 5. Coordinación Multiagente

1. **Trabajo Modular sin Pisarse Archivos:**
   * Antes de modificar un archivo grande o script central, revisar si otro agente está operando sobre él.
   * Mantener los módulos desacoplados: datos de comercio (`data/processed/`), capas de transporte (`data/raw/transporte/`), clasificadores (`data/catalog/`) y visualizadores web (`scripts/` y `.html`).
2. **Uso Eficiente de Subagentes:**
   * Delegar tareas complejas, exploratorias o de cómputo intensivo a subagentes dedicados con roles específicos (`Especialista en Datos`, `Investigador de APIs`, `Desarrollador Frontend`).
3. **Respuestas Ejecutivas:**
   * Al interactuar con el usuario, ser conciso, estructurado y presentar siempre los links clickeables a los archivos modificados o creados con el esquema `file:///`.
