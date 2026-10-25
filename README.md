# Plataforma de Comercio Popular, Barrial y Movilidad Integrada (CDMX)
> **Chilangatón 2026 — Reto 1: Comercio Popular y Barrial**  
> *SEDECO · SECTEI · SAF · Gobierno de la Ciudad de México*  
> *Enfoque: Soberanía de datos barrial, accesibilidad ciudadana, logística popular y movilidad urbana sustentable.*

---

## 📌 Visión del Proyecto

El comercio popular y barrial de la Ciudad de México (329 mercados públicos, 1,367 tianguis semanales, 51 rutas de mercados sobre ruedas y más de 86,000 pequeños comercios) es la columna vertebral del abasto alimentario y del empleo de cientos de miles de familias.

Este proyecto articula una **plataforma cívica, cartográfica y de soberanía de datos** que conecta:
1. **A la ciudadanía y compradores:** Saber qué tianguis o mercado está abierto hoy cerca de su casa o trabajo, qué productos frescos ofrece, y cómo llegar de la forma más rápida y económica mediante la **Red de Movilidad Integrada (Metro, Metrobús, Trolebús, Cablebús, RTP y Ecobici)**.
2. **A los comerciantes y locatarios:** Herramientas ligeras, offline-first y sin comisiones bancarias abusivas (facilitando cobros DiMo/SPEI y vales Mercomuna), respetando la autonomía de sus asambleas y evitando el extractivismo de datos.
3. **A la movilidad y resiliencia urbana:** Mapeo de afectaciones viales temporales (cierres de calles programados por tianguis) y alertas de resiliencia climática (lluvias e inundaciones).

---

## 🗂️ Documentación y Enlaces Clave

* 📚 **[Compendio de Fuentes, Datasets, APIs y Bibliografía](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/FUENTES_Y_BIBLIOGRAFIA.md)**: Inventario exhaustivo de datos abiertos, geoportales WFS, bibliografía académica (Giglia, Delgadillo, Colmex, etc.), marco normativo y reportes periodísticos.
* 📋 **[Backlog y To-Do List del Proyecto](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/TODO_PROYECTO.md)**: Roadmap modular de 8 módulos con seguimiento de tareas independientes y dependencias.
* 🌐 **[Catálogo de APIs y Servicios Geoespaciales en Vivo](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/docs/apis_cdmx.md)**: Pruebas de conectividad y endpoints de CKAN Datastore SQL, GeoServer WFS SIG CDMX, Ecobici GBFS y OSRM.
* 🥦 **[Catálogo Modular de Giros Comerciales](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/README.md)**: 9 macro-categorías, 67 subgiros estandarizados, motor en Python (`giro_classifier.py`) y reglas de canasta básica y Mercomuna.
* 🗺️ **[Visor Cartográfico Interactivo](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/mapa_comercio_movilidad_cdmx.html)**: Prototipo funcional que renderiza el comercio popular superpuesto a la Red de Movilidad Integrada.
* 🚶 **[Especificación de Ruteo Multimodal](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/docs/RUTEO_MULTIMODAL_CDMX.md)**: Algoritmo de conexión a pie y transporte masivo hacia puntos de venta barrial.

---

## 📂 Estructura del Repositorio

```text
├── FUENTES_Y_BIBLIOGRAFIA.md    # Compendio maestro de fuentes, citas, datasets y APIs
├── TODO_PROYECTO.md             # Backlog y seguimiento del plan de trabajo
├── README.md                    # Documento principal del repositorio
├── mapa_comercio_movilidad_cdmx.html # Visor cartográfico web integrado
├── data/
│   ├── raw/                     # Datasets originales (SEDECO, INEGI, SEMOVI, etc.)
│   ├── processed/               # Datasets limpios WGS84, horarios y catálogo unificado
│   ├── catalog/                 # Taxonomía de 67 giros y motor de clasificación
│   └── docs/                    # Catálogo de APIs y servicios geoespaciales
├── docs/                        # Especificaciones de algoritmos y ruteo
├── scripts/                     # Pipelines ETL, constructores de grafos y visualizadores
└── Referencias/                 # Material gráfico y capturas de campo
```

---

## 🚀 Inicio Rápido

Para explorar el prototipo cartográfico interactivo, abre el archivo [`mapa_comercio_movilidad_cdmx.html`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/mapa_comercio_movilidad_cdmx.html) en tu navegador web.
Para reproducir la normalización de datos o ejecutar el clasificador de giros:

```bash
# Ejecutar pipeline de normalización de datos
python3 data/processed/normalize_all.py

# Probar clasificador de giros comerciales
python3 data/catalog/giro_classifier.py "Tienda de abarrotes y cremería"
```
