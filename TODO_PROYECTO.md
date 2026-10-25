# Backlog y To-Do List del Proyecto: Comercio Popular y Movilidad CDMX
> **Chilangotón 2026 — Reto 1: Comercio Popular y Barrial**  
> *Enfoque: Resiliencia económica barrial, accesibilidad ciudadana, logística popular y movilidad urbana.*

---

## 🧭 Visión General de la Integración

El reto se centra en el **comercio popular y barrial** (1,367 tianguis, 329 mercados públicos, 51 rutas de mercados sobre ruedas y 224 concentraciones comerciales). Integrar la capa de **Transporte, Movilidad y Cartografía de la CDMX** permite:
1. **Para la ciudadanía / compradores:** 
   - Saber qué tianguis o mercado está activo hoy cerca de su ubicación o trabajo sobre un mapa interactivo de la ciudad.
   - Cómo llegar de la forma más económica y rápida (Movilidad Integrada vs. transporte secundario).
   - Seguir a sus tianguis móviles y puesteros favoritos a lo largo de su ruta semanal.
   - Evitar embotellamientos sabiendo qué calles están cerradas por instalación de tianguis.
2. **Para las y los comerciantes:** 
   - Rutas óptimas de abasto desde centros mayoristas (CEDA, La Merced) hasta sus puntos de venta.
   - Un canal directo y sin intermediarios para mantener viva y actualizada su información (días festivos, cambios de sede, medios de pago).
3. **Para la movilidad y la política pública:** 
   - Prever afectaciones viales temporales (cierres de calles programados de lunes a domingo).
   - Detectar "desiertos de movilidad" y "desiertos de abasto fresco" en colonias periféricas.
   - Contrastar los mercados populares contra las unidades económicas formales (DENUE INEGI).

---

## 🗂️ Arquitectura Modular del Proyecto

Para permitir trabajar en paralelo sin bloqueos, el proyecto se divide en 8 áreas independientes:

```mermaid
graph TD
    M0[Módulo 0: Cartografía Base CDMX & Límites] --> F[Integración Espacial & Analítica]
    A[Módulo 1: Datos de Comercio Barrial & Rutas] --> F
    B[Módulo 2: Movilidad Integrada - MI] --> F
    C[Módulo 3: Transporte Secundario Concesionado] --> F
    D[Módulo 4: Afectación y Cierres Viales] --> F
    E[Módulo 5: Sistema Vivo & Crowdsourcing] --> G[Prototipo / App Web]
    F --> G
    H[Módulo 7: Pitch & Narrativa Hackatón] --> G
```

---

## 📋 To-Do List Modular (Backlog "Rascable")

> Cada tarea indica su **Nivel de Dependencia** (`[100% Independiente]` o `[Depende de...]`) y su **Dificultad** (`Baja`, `Media`, `Alta`). Puedes tomar cualquier tarea independiente en el orden que prefieras.

---

### MÓDULO 0: Infraestructura Cartográfica Base de la CDMX (Lienzo Geográfico)

> Descarga y estandarización de las capas vectoriales sobre las que se montarán todos los datos (alcaldías, colonias, malla vial y unidades económicas).

- [x] **0.1 Descargar polígonos de límites de la CDMX y las 16 Alcaldías** `[Hecho]`
  - Obtenido GeoJSON oficial de las 16 alcaldías en `data/raw/cartografia/alcaldias.geojson`.
- [ ] **0.2 Descargar polígonos de Colonias de la CDMX** `[100% Independiente] [Dificultad: Baja]`
  - Fuente: Catálogo oficial IECM / ADIP (~1,814 colonias con claves oficiales).
  - Permite vincular la columna `colonia` de tianguis y mercados con su polígono real para agregaciones y mapas de calor.
- [ ] **0.3 Descargar Red Vial de la CDMX (Malla de Calles y Avenidas)** `[100% Independiente] [Dificultad: Media]`
  - Fuente: OpenStreetMap (extracto CDMX vía Geofabrik / Overpass) o Red Vial Oficial SEMOVI.
  - Extraer ejes viales, vías primarias, secundarias y locales. Crucial para proyectar sobre qué tramo de calle exacto se monta cada tianguis.
- [ ] **0.4 Descargar Unidades Económicas de Comercio al por Menor (DENUE INEGI)** `[100% Independiente] [Dificultad: Media]`
  - Descargar registros de CDMX del DENUE (código SCIAN 46: Comercio al por menor: abarrotes, fruterías, carnicerías, pollerías, minisúpers, tiendas de autoservicio).
  - Permite comparar la presencia del comercio popular vs. tiendas de autoservicio/conveniencia por colonia.
- [x] **0.6 Descargar y mapear municipios conurbados de la Zona Metropolitana (ZMVM)** `[Hecho]`
  - Obtenidos los 60 municipios metropolitanos del Estado de México e Hidalgo (Naucalpan, Tlalnepantla, Ecatepec, Nezahualcóyotl, Chimalhuacán, Huixquilucan, Chalco, etc.) en `data/raw/cartografia/zmvm_edomex.geojson` para dar contexto geográfico continuo a todo el Valle de México.
- [x] **0.7 Exploración y catálogo de APIs de consultas de mapas y servicios geoespaciales de la CDMX** `[Hecho]`
  - Investigadas y probadas con éxito las APIs de CDMX: CKAN API v3 (Datastore & SQL en vivo), Ecobici GBFS v2.3 en tiempo real, GeoServer WFS SIG CDMX (GeoJSON directo de 44 capas oficiales incluyendo Atlas de Riesgo por Inundación, CETRAM, transporte concesionado, Metrobús y Metro), Open-Meteo CDMX y OSRM ruteo caminable.
  - Generado catálogo exhaustivo con matriz comparativa, fichas técnicas, payloads reales y 6 ideas de alto impacto para el Hackatón en `data/docs/apis_cdmx.md`.

---

### MÓDULO 1: Datos de Comercio Popular, Tipología (Fijo vs. Móvil) y Rutas

- [x] **1.1 Inventario de bases de datos existentes** `[Hecho]`
  - Tianguis (1,367), Mercados Públicos (329), Mercados sobre Ruedas (51), Concentraciones (224), Solicitudes FONDESO, Muestra Mercomuna.
- [x] **1.2 Clasificación tipológica formal: Fijos vs. Móviles (Itinerantes)** `[Hecho]`
  - Etiqueta canónica `tipo_comercio` integrada en `directorio_comercio_popular` (.json/.csv) y en cada dataset base:
    - `FIJO` (553 espacios): Mercados Públicos (329 inmuebles con cédula SEDECO) y Concentraciones comerciales (224 en vía pública).
    - `MOVIL` (1,418 espacios): Tianguis semanales (1,367) y paradas de Mercados Sobre Ruedas (51).
- [x] **1.3 Normalización de horarios y días de instalación** `[Hecho]`
  - Horarios parseados con precisión decimal (`hora_apertura`, `hora_cierre`, `horario_estimado`):
    - Cobertura al 100% (1,971 registros sin nulos; apertura entre 6.0 y 9.0 hrs, cierre entre 16.0 y 19.0 hrs).
    - Matriz de 7 banderas booleanas por día (`lunes` a `domingo`) en el directorio unificado.
    - Función reproducible `esta_abierto(record, dia, hora)` para responder en vivo *"¿Qué comercio está abierto ahora?"*.
- [x] **1.4 Trazabilidad y seguimiento de Rutas de Mercados Sobre Ruedas (MSR)** `[Hecho]`
  - Generados `data/processed/msr_rutas_itinerantes.json` y `.csv`:
    - 13 rutas gremiales agrupadas (RUTA 1 a RUTA 10, variantes A/B y MINI RUTA).
    - Paradas ordenadas cronológicamente de lunes a domingo con secuencia semanal, georreferenciación WGS84, alcaldía, colonia y oferentes.
    - Generado dataset complementario GIS-ready `data/processed/msr_rutas_paradas_itinerantes.csv` (51 paradas geolocalizadas) para mapeo directo.
- [x] **1.5 Catálogo de Centros de Abasto Mayoristas** `[Hecho]`
  - Creados `data/processed/centros_abasto_mayoristas.json` y `.csv` con 8 nodos estratégicos de suministro georreferenciados:
    - Central de Abasto de Iztapalapa (CEDA - 327 ha, mayor central mayorista del mundo)
    - Mercado de La Merced - Nave Mayor (hortalizas, legumbres, víveres y canasta básica)
    - Mercado de La Merced - Nave Menor (cárnicos, embutidos y derivados lácteos)
    - Mercado de Sonora (herbolaria tradicional, plantas medicinales y alfarería)
    - Mercado de Jamaica (gran centro de distribución florícola 24 horas)
    - Mercado de La Nueva Viga (segundo mercado mayorista de mariscos del mundo)
    - Mercado de La Viga (polo semimayorista histórico de pescados y mariscos)
    - Mercado de San Juan Pugibet (abasto semimayorista gourmet y carnes selectas)
    - Cada nodo incluye: ID, nombre, clave_nodo, alcaldía, colonia, dirección, lat, lng, giros, tipo_abasto, horario, relevancia logística y conectividad con la Red MI.
- [x] **1.6 Enriquecimiento de Padrón Comercial con Taxonomía de Giros y Productos** `[Hecho]`
  - Cruzado el padrón unificado (`directorio_comercio_popular`), `tianguis`, `mercados_publicos`, `concentraciones` y muestras de padrón detallado (FONDESO 86k registros, apoyos emergentes, Mercomuna) con el motor [`giro_classifier.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/giro_classifier.py) y [`giros_catalogo.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/giros_catalogo.json).
  - Asignadas a cada espacio comercial sus **Macro-Categorías** (1 a 9), **Subgiros específicos** (de los 67 del catálogo) y **Banderas de Canasta Básica / Mercomuna**.
  - Generado el vocabulario maestro y mapeo inverso de productos de consumo popular (159 términos en [`data/catalog/vocabulario_compras.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/vocabulario_compras.json) y `.csv`, replicado en `data/processed/`) desde términos desagregados: "aguacate", "huevo", "tacos", "pescado", "zapatos", "tornillos" hacia subgiros y macrocategorías.
  - Integradas estas estructuras jerárquicas en [`scripts/compile_advanced_bundle.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/compile_advanced_bundle.py) y en el bundle del visor web ([`data/processed/map_bundle.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/map_bundle.json) y `map_bundle.js`).

---

### MÓDULO 2: Movilidad Integrada (MI) — PRIORIDAD 1

> Fuentes clave: Portal de Datos Abiertos CDMX (`datos.cdmx.gob.mx`), GTFS oficial de SEMOVI, ADIP.

- [x] **2.1 Descargar y estructurar catálogos geográficos de la Red MI** `[Hecho]`
  - Descargado paquete GTFS estático oficial de SEMOVI CDMX con Metro, Metrobús, Cablebús, Trolebús, Tren Ligero y Corredores Concesionados (`data/raw/transporte/gtfs/`).
- [x] **2.2 Crear matriz de Costos, Tarifas y Políticas de Transbordo** `[Hecho]`
  - Implementado catálogo unificado en [`data/catalog/tarifas_horarios_transporte.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/tarifas_horarios_transporte.json) y [`data/catalog/tarifas_horarios_transporte.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/tarifas_horarios_transporte.csv).
  - Incluye los 15 subsistemas de la ZMVM: Metro ($5), Metrobús ($6), Cablebús ($7), Trolebús ($4/$7), Tren Ligero ($3), RTP ($2/$4/$5/$7 Nochebús), Mexibús ($9), Mexicable ($9) y Tren Suburbano ($10.50-$24.50).
  - Políticas de gratuidad (+60 INAPAM, discapacidad, menores de 5 años) y ventanas de transbordo (2 horas en Metrobús, transbordos ilimitados en Metro).
- [x] **2.3 Crear catálogo de Horarios Oficiales de Operación** `[Hecho]`
  - Documentados horarios decimales y cadenas de apertura/cierre para: Lunes-Viernes, Sábados, Domingos y Días Festivos.
  - Modeladas ventanas de servicio nocturno (Nochebús 00:00 - 05:00 hrs) y desfases de cierre de madrugada (Suburbano hasta 00:30 hrs).
  - Motor funcional [`scripts/schedule_pricing_engine.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/schedule_pricing_engine.py) con función `consultar_transporte_por_hora(dia, hora)`.
- [x] **2.4 Procesar GTFS de Movilidad Integrada CDMX** `[Hecho]`
  - Script `scripts/build_demo_data.py` extractor de shapes y routes compilado en `data/processed/map_bundle.json`.
- [ ] **2.5 Catálogo de CETRAMs (Centros de Transferencia Modal)** `[100% Independiente] [Dificultad: Baja]`
  - Georreferenciar los 40+ CETRAMs (Indios Verdes, Pantitlán, Tacubaya, Constitución de 1917, Taxqueña, etc.) como nodos de conexión masiva.

---

### MÓDULO 3: Transporte Secundario y Concesionado — PRIORIDAD 2

> Transporte de última milla y alimentadoras que penetran en colonias donde no llega el metro.

- [ ] **3.1 Mapeo de Rutas de Microbuses y Vagonetas (Combis)** `[100% Independiente] [Dificultad: Media-Alta]`
  - Buscar datos en SEMOVI / OpenStreetMap (Overpass API) / Datos Abiertos:
    - Rutas concesionadas tradicionales (Rutas 1 a 110).
    - Corredores viales concesionados nuevos (SAUSA, COAVENSA, ATROLSA, etc.).
    - Ramales, orígenes y destinos (ej. "Metro Tacubaya - Santa Fe").
- [x] **3.2 Estructura Tarifaria de Transporte Concesionado y Frontera Metropolitana** `[Hecho]`
  - Documentado esquema oficial por distancia en CDMX (Microbús: $6.00 hasta 5 km, $6.50 de 5 a 12 km, $7.50 más de 12 km; Corredor: $8.00 - $8.50).
  - Documentada tarifa conurbada del Estado de México (Combi: $14.00 base primeros 5 km + $0.25/km adicional) y reciprocidad en cruces hacia CETRAMs de CDMX.
  - Recargo nocturno formal (+20% de 23:00 a 06:00 hrs) y motor dinámico `calcular_costo_tramo(sistema_id, distancia_km, hora, origen_edomex)`.
  - Documentación técnica exhaustiva en [`docs/TARIFAS_Y_HORARIOS_TRANSPORTE.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/docs/TARIFAS_Y_HORARIOS_TRANSPORTE.md).
- [ ] **3.3 Padrón de Bases de Taxis y Taxis de Sitio** `[100% Independiente] [Dificultad: Media]`
  - Ubicación de bases autorizadas cercanas a mercados públicos y CETRAMs.
  - Tarifas: Banderazo taxi libre, sitio, radio-taxi, recargo nocturno (23:00 a 06:00).
- [ ] **3.4 Mapeo referencial de Transporte Comunitario (Bicitaxis / Mototaxis)** `[100% Independiente] [Dificultad: Media]`
  - Zonas de alta afluencia (Tláhuac, Iztapalapa, Xochimilco, Venustiano Carranza) donde los mototaxis/bicitaxis son el transporte principal para llevar el mandado a casa.

---

### MÓDULO 4: Afectación Vial y Avisos de Calles Cerradas por Tianguis

> Como los tianguis se instalan sobre el arroyo vehicular, reducen la movilidad y alteran el tráfico local.

- [x] **4.1 Extracción y estructuración de tramos de calle afectados** `[Hecho]`
  - Script [`scripts/process_street_closures.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/process_street_closures.py) con parser regex vial y modelo dimensional físico (~1.5 m por oferente y ancho de 6 a 12 m).
  - Georreferenciación completa en WGS84 para los 1,367 tianguis (1,396 operaciones semanales).
  - Generado [`data/processed/cierres_viales_tianguis.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/cierres_viales_tianguis.geojson) con geometrías `LineString` y polígonos envolventes (`poligono_buffer`).
- [x] **4.2 Calendario de Cierres Viales Programados (Por día y hora)** `[Hecho]`
  - Generado índice optimizado [`data/processed/cierres_viales_por_dia.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/cierres_viales_por_dia.json) organizado de `DOMINGO` a `SÁBADO`.
  - Métrica capitalina: **330.00 km lineales de calles cerradas/ocupadas cada semana en la CDMX**.
  - Domingo es el día pico de afectación vial: 267 tianguis, 65.16 km lineales clausurados y 47,142 oferentes activos.
- [x] **4.3 Impacto en el Transporte Público Secundario (Desvíos)** `[Hecho]`
  - Indexador espacial con KDTree cruzando 107,008 segmentos de transporte público (RTP, microbuses concesionados, Trolebús y Metrobús).
  - Tipificación de afectación: 1,083 cierres totales de calle (77.6%), 238 reducciones de carril (17.0%) y 74 ocupaciones de camellón (5.3%).
  - Generación automatizada de sugerencias de desvío vehicular y rutas alternas en cada tramo.
- [x] **4.4 Feed / API de Alertas Viales Barriales y Documentación** `[Hecho]`
  - Archivos GeoJSON y JSON listos para integración directa en el visor web y sistemas de alerta ciudadana.
  - Documentación exhaustiva en [`docs/CIERRES_VIALES_TIANGUIS.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/docs/CIERRES_VIALES_TIANGUIS.md) con matriz por alcaldía, top 10 corredores viales críticos y directrices operativas.

---

### MÓDULO 5: Accesibilidad Viva y Sinergia Comunitaria (Cero Fricción)

> Principio rector: Entre menos fricción para el usuario, mayor adopción. No exigir reportes pesados ni formularios complejos; en su lugar, habilitar consultas de un solo clic y fuentes directas oficiales.

- [x] **5.1 Depuración de ruido visual en el visor** `[Hecho]`
  - Omitida la sinergia externa con RTPonky en el visor web para mantener la interfaz limpia, profesional y libre de ruido visual.
  - La tarjeta de detalle de cada mercado y tianguis cuenta con un botón único y directo: `[ 🎯 Planificar Ruta hacia aquí ]`.
- [x] **5.2 Conexión con paradas y rutas de RTP oficiales** `[Hecho]`
  - 30 rutas clave y cálculo de distancia a paradas de RTP cercanas a centros de abasto.
- [x] **5.3 Indicador ligero de estatus de tianguis (Sin fricción)** `[Hecho]`
  - Cálculo automático basado en reloj/horario oficial (ej. `🟢 Abierto hoy · Horario de venta activo`, `🟡 En instalación y montaje (06:00 a 08:00 hrs)`, `🟡 En desmontaje y aseo vial (17:00 a 19:00 hrs)`, `🔴 No opera hoy`) sin depender de reportes manuales obligatorios.
  - Integrado de forma reactiva en la ficha lateral de cada tianguis, MSR y concentración en [`mapa_comercio_movilidad_cdmx.html`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/mapa_comercio_movilidad_cdmx.html).
- [ ] **5.4 Sistema de Ponderación Ciudadana y Crowdsourcing Barrial ("¿Qué se vende aquí?")** `[100% Independiente] [Dificultad: Media]`
  - Mecanismo ligero y local-first donde la ciudadanía compradora y los comerciantes pueden votar o confirmar qué productos y especialidades sí se encuentran disponibles en cada tianguis individual (ej. "Ropa de paca", "Barbacoa", "Herramientas usadas", "Pescado fresco").
  - Sistema de reputación por upvotes/downvotes comunitarios almacenado localmente (localStorage/IndexedDB) con sincronización opcional, evitando formularios burocráticos y respetando la soberanía de datos del comerciante.
- [ ] **5.5 Pipeline de Enriquecimiento de Especialidades de Tianguis (Google Maps & Reseñas)** `[En Progreso]`
  - **Fase 1 (Scraping):** Extracción automatizada de reseñas ciudadanas, calificaciones y galerías de fotos para los 1,366 tianguis con `place_id` en Google Maps Places (`scripts/scrape_tianguis_reviews.py`).
  - **Fase 2 (Posprocesado NLP & Especialidades):** Procesamiento de texto de reseñas con extracción de n-gramas, análisis de sentimiento y cruce con el catálogo de 460 artículos para derivar la vocación comercial exacta de cada tianguis ("Ropa de paca", "Barbacoa/Antojitos", "Herramientas usadas", "Abasto fresco").
  - Integración de fotos y especialidades comunitarias en la ficha lateral de [`mapa_comercio_movilidad_cdmx.html`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/mapa_comercio_movilidad_cdmx.html).

---

### MÓDULO 6: Análisis Espacial, Ruteo y Accesibilidad Multimodal

- [x] **6.1 Motor de Cálculo de Rutas Punto A -> Punto B (Ruteo Multimodal CDMX)** `[Prototipo Funcional Hecho]`
  - Implementado script [`scripts/route_calculator.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/route_calculator.py) basado en grafos de estado y GTFS oficial con tiempos de respuesta de 6 a 50 ms.
  - Generado documento técnico [`docs/RUTEO_MULTIMODAL_CDMX.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/docs/RUTEO_MULTIMODAL_CDMX.md) analizando RAPTOR, OTP2, Valhalla, OSRM y APIs públicas.
  - Soporte de consulta por nombres (ej. `Zócalo` a `Mercado Jamaica`), desglose tramo por tramo, costo oficial en pesos ($5.00 - $12.00) y exportación JSON para API/Web.
- [ ] **6.2 Cálculo de buffers de caminabilidad (Isócronas a pie)** `[Depende de 1.1 y 2.1] [Dificultad: Media]`
  - Determinar qué tianguis y mercados tienen una estación de Metro, Metrobús, Trolebús o Cablebús a menos de 5, 10 y 15 minutos caminando (400m, 800m, 1200m).
- [ ] **6.3 Detección de "Desiertos de Movilidad" y "Desiertos de Abasto"** `[En Progreso]`
  - Análisis espacial georreferenciado (buffers isócronos de caminabilidad a 500m, 800m y 1,200m) sobre los 1,367 tianguis de la CDMX y la ZMVM cruzados por día de la semana (lunes a domingo).
  - Tipificación de colonias y zonas barriales en: *Abasto Pleno* (<500 m), *Abasto Moderado* (500-1,000 m) y *Desierto de Abasto Fresco Popular* (>1,000 m sin tianguis caminable).
  - Generación de datasets duales (`data/processed/desiertos_abasto_cdmx.json` y `.csv`) con métricas por alcaldía.
  - Reporte de política pública para el jurado SEDECO/SECTEI en [`docs/DESIERTOS_ABASTO_CDMX.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/docs/DESIERTOS_ABASTO_CDMX.md) con recomendaciones para la asignación de nuevas rutas de abasto popular.
- [ ] **6.4 Densidad de Unidades Económicas (Comercio Popular vs. Cadenas Privadas)** `[Depende de 0.4 y 1.1] [Dificultad: Media]`
  - Contrastar la huella del comercio tradicional (tianguis y mercados) contra la penetración de supermercados y tiendas de conveniencia (Oxxo, Bodega Aurrera Express) por alcaldía.
- [ ] **6.5 Calculadora de Costo Total de Traslado para el Mandado** `[Depende de 2.2 y 3.2] [Dificultad: Baja]`
  - Estimar cuánto gasta una persona en transporte público de ida y vuelta para hacer sus compras en el tianguis vs. supermercado.

---

### MÓDULO 7: Prototipo, Visor Web y Presentación Hackatón

- [ ] **7.1 Arquitectura de almacenamiento portable** `[100% Independiente] [Dificultad: Baja]`
  - Estructurar datos limpios en SQLite / SpatiaLite o GeoJSONs estáticos organizados en `data/processed/` o `data/cartography/`.
- [x] **7.2 Visor Geoespacial Integrado (Frontend Web & UX/UI Renovado)** `[Prototipo v2.1 Frontend Completo]`
  - Archivo interactivo [`mapa_comercio_movilidad_cdmx.html`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/mapa_comercio_movilidad_cdmx.html) con diseño de escritorio inspirado en la App CDMX oficial (`#0f5953`), sin barra inferior estorbosa.
  - **Clustering Inteligente con Leaflet.markercluster:** Agrupación visual optimizada de 1,367 tianguis, 329 mercados y 519 estaciones (Metro y Metrobús) con badges y colores temáticos por subsistema, reduciendo la saturación en zoom bajo y desplegando marcadores individuales a nivel barrial (`zoom >= 14`).
  - **Eliminación Total de `window.alert(...)`:** Reemplazo integral por modal flotante interactivo con 4 pestañas temáticas ("🚧 Cierres Viales", "⏰ Horarios Semanales", "💳 Tarifas MI", "📅 Aviso Hoy") y sistema de notificaciones toast no invasivas.
  - **Buscador Unificado Predictivo:** Autocompletado flotante en tiempo real con ponderación de relevancia para Mercados, Tianguis, Rutas MSR y Estaciones MI con navegación por teclado y centrado suave (`flyTo`).
  - **Ficha Lateral (Sidebar) Rediseñada:** Tarjeta de detalle sin popups redundantes, con badge dinámico de estado (`🟢 Abierto hoy hasta las 18:00 hrs` / `🔴 Cerrado`), cálculo en tiempo real de estación más cercana con distancia en metros y tiempo a pie, alerta de calle ocupada y botón para copiar coordenadas GPS WGS84 al portapapeles.
  - **Carga Asíncrona & Skeleton Loader:** Reducción de 93% en peso de HTML (de 3.6 MB a 254 KB) mediante desacoplamiento a `data/processed/map_bundle.js` / `map_bundle.json` con loader visual animado de CDMX.
  - **Modo Ruta Limpia (Focus Mode):** Al calcular una ruta o pulsar "🎯 Ir hacia aquí", se ocultan automáticamente todas las líneas, tianguis y mercados ruidosos de fondo, dejando únicamente el trayecto activo: Pin Origen (A), tramo de caminata inicial (azul punteado), estación de abordaje con ícono oficial, línea de metro correspondiente, transbordos si aplican, estación de descenso, caminata final (verde punteado) y Pin Destino (B). Incluye banner flotante superior para restaurar el mapa completo.
- [ ] **7.3 Modo Offline / Descargable por Alcaldía** `[100% Independiente] [Dificultad: Baja]`
  - Siguiendo la premisa del dossier (herramientas locales y ligeras): generación de fichas descargables o modo cacheado para consultar sin internet.
- [ ] **7.4 Pitch Deck y Narrativa de Impacto Social** `[100% Independiente] [Dificultad: Baja]`
  - Demostrar que el proyecto no es "otro marketplace", sino una plataforma cívica de infraestructura viva que fortalece la soberanía alimentaria barrial y la movilidad sustentable.
- [x] **7.5 Filtro y Buscador Jerárquico de Compras en el Visor Web (De lo micro a lo macro)** `[Hecho]`
  - Implementado en la interfaz de usuario de [`mapa_comercio_movilidad_cdmx.html`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/mapa_comercio_movilidad_cdmx.html) y compilador [`scripts/build_revamped_map.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/build_revamped_map.py) un sistema de filtros multinivel para compras:
    - **Nivel Macro (Categorías agregadas):** Barra interactiva de chips con íconos temáticos (🥦 Alimentos Frescos, 🥫 Abarrotes y Canasta, 🌮 Comida Preparada, 👕 Ropa y Calzado, 🔨 Hogar y Ferretería, ✂️ Salud y Belleza, ✏️ Papelería y Tecnología, 🪛 Oficios y Reparaciones, 📦 Bazar y Chácharas).
    - **Nivel Meso (Subgiros / Giros específicos):** Menú cascada dinámico con los 67 subgiros estructurados agrupados por categoría (`<optgroup>`), sincronizado automáticamente con la macro-categoría activa.
    - **Nivel Micro (Búsqueda predictiva de productos concretos):** Entrada interactiva *"¿Qué quieres comprar hoy? (ej. jitomate, barbacoa, tenis, clavos, útiles...)"* con autocompletado predictivo en tiempo real sobre 159 términos populares y resolución de sinónimos hacia subgiros y macrocategorías.
    - **Filtros rápidos de política social:** Conmutadores para *"Canasta Básica SEDECO"* y *"Acepta Vales Mercomuna"*.
    - **Reactividad geoespacial:** Actualización instantánea de clusters y marcadores de Leaflet (mercados, tianguis, MSR), panel lateral detallado con oferta de giros por espacio, insignias oficiales y contadores dinámicos de oferta disponible con gestión de píldoras activas y botón de reseteo.
- [x] **7.6 Pivote Estratégico a Comercio Popular y Barrial Itinerante (Tianguis, MSR y Concentraciones)** `[Hecho]`
- [x] **7.7 Mapa Minimalista 100% Centrado en Tianguis (CDMX + ZMVM)** `[Hecho]`
  - **Foco Exclusivo en Tianguis (Cero Ruido):** Eliminación total de mercados públicos, líneas de transporte sobrecargadas y capas de cierres viales. Lienzo CartoDB Positron ultra limpio centrado exclusivamente en los 1,367 tianguis semanales autorizados de la CDMX.
  - **Lienzo Base Limpio Metropolitano:** Incorporación de polígonos vectoriales sutiles de las 16 Alcaldías oficiales de la CDMX y 60 municipios conurbados de la ZMVM (Edomex).
  - **Inicio Dinámico en `[ HOY ]` con Evaluación de Hora Actual:** Detección automática del día de la semana y cálculo de estatus en vivo (🟢 *Abierto hoy hasta las 17:00 hrs*, 🟡 *En montaje / desmontaje*, 🔴 *No opera hoy*) con selector semanal `[ 🧺 HOY ]` `[ LUN ]` `[ MAR ]` `[ MIÉ ]` `[ JUE ]` `[ VIE ]` `[ SÁB ]` `[ DOM ]` `[ TODOS ]` y contadores en tiempo real.
  - **ÚNICO Buscador Omnibox Inteligente y Humano:** Sustitución de cajas duplicadas por una sola barra de búsqueda predictiva con sugerencias categorizadas:
    * 🎪 **Tianguis por Nombre Popular u Oficial:** "El Salado", "San Felipe / La Bola", "Cultural del Chopo", "Sullivan", "Apatlaco", "Condesa", "Doctores", etc.
    * 📍 **Alcaldías y Colonias:** Enfoque espacial automático con auto-encuadre `fitBounds`.
    * 🏷️ **Catálogo Extendido de +460 Productos Barriales:** Frutas, legumbres, carnes, mariscos, barbacoa, birria, carnitas, antojitos, ropa de paca, calzado, tenis, herramientas usadas, chácharas, tecnología, hierbas medicinales, etc.
  - **Ficha Lateral (Sidebar) Sobria:**
    * Nombre popular destacado y cédula oficial SEDECO.
    * Badge de estatus en vivo con pulso de color y detalle horario.
    * Escala comercial: *Megatianguis (300+ puestos)*, *Tianguis Mediano (100–300)* o *Tianguis Barrial (<100)* con número estimado de oferentes.
    * Especialidad y vocación barrial con nube de etiquetas.
    * Referencia caminable calculada por distancia geodésica a transporte masivo: `🚶 A X min a pie de Metro [Nombre] (Línea Y) · Z metros` (sin dibujar líneas en el mapa).
    * Acciones: enlace directo a Google Maps y botón de copiado de coordenadas GPS WGS84 al portapapeles.
  - **Entrega Técnica:** Generación de `scripts/build_compras_catalog.py` (+460 items), `scripts/build_tianguis_bundle.py` (bundle unificado de 3.3 MB), `scripts/build_revamped_map.py` y `mapa_comercio_movilidad_cdmx.html` (interfaz ultraligera de 61 KB).
