# Compendio Exhaustivo de Fuentes, Datasets, APIs y Bibliografía
**Proyecto:** Comercio Popular, Barrial y Movilidad Integrada en la CDMX  
**Marco:** Chilangatón 2026 — Reto 1: Comercio Popular y Barrial (SEDECO / SECTEI / SAF)  
**Ubicación:** `FUENTES_Y_BIBLIOGRAFIA.md`  
**Última actualización:** 25 de octubre de 2026  

---

## Índice General

1. [Conjuntos de Datos Oficiales (Descargados y Procesados)](#1-conjuntos-de-datos-oficiales)
2. [APIs, Servicios Web y Geoportales en Vivo](#2-apis-servicios-web-y-geoportales-en-vivo)
3. [Bibliografía Académica y Estudios Socioterritoriales](#3-bibliografía-académica-y-estudios-socioterritoriales)
4. [Crítica al Solucionismo y Principios de Gobernanza de Datos](#4-crítica-al-solucionismo-y-gobernanza-de-datos)
5. [Marco Normativo, Gacetas y Políticas Públicas](#5-marco-normativo-gacetas-y-políticas-públicas)
6. [Investigación Periodística y Reportes Gremiales](#6-investigación-periodística-y-reportes-gremiales)
7. [Trazabilidad de Scripts y Entregables del Repositorio](#7-trazabilidad-de-entregables-del-repositorio)

---

## 1. Conjuntos de Datos Oficiales

Todos los datasets base han sido descargados en `data/raw/` y normalizados bajo el estándar WGS84 en `data/processed/`.

### 1.1 Comercio Popular y Barrial

| Nombre del Dataset | Dependencia / Fuente | Formatos | Registros | Cobertura / Contenido | Ubicación Local |
|---|---|:---:|:---:|---|---|
| **Tianguis de la Ciudad de México** | SEDECO CDMX (Portal Datos Abiertos) | CSV, GeoJSON | 1,367 tianguis | Alcaldía, colonia, tramo de calle (`ubicacion`), días de instalación (lunes a domingo), horarios y coordenadas WGS84. | [`data/raw/tianguis.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/tianguis.csv)<br>[`data/processed/tianguis_limpio.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/tianguis_limpio.json) |
| **Mercados Públicos de la CDMX** | SEDECO CDMX (Portal Datos Abiertos) | CSV, GeoJSON | 329 mercados | Nombre oficial, número de mercado, total de locales, superficie en m², año de inauguración, estatus de inmueble protegido y coordenadas. | [`data/raw/mercados_publicos.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/mercados_publicos.csv)<br>[`data/processed/mercados_publicos_limpio.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/mercados_publicos_limpio.json) |
| **Mercados Sobre Ruedas (MSR)** | SEDECO CDMX (Portal Datos Abiertos) | CSV, GeoJSON | 51 paradas (13 rutas) | Código de ruta (`RUTA 1` a `10`, `6-A/B`, `8-A/B`, `MINI RUTA`), día de operación semanal, número de oferentes, dirección y coordenadas. | [`data/raw/mercados_sobre_ruedas.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/mercados_sobre_ruedas.csv)<br>[`data/processed/msr_rutas_itinerantes.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/msr_rutas_itinerantes.json) |
| **Concentraciones de Comerciantes** | SEDECO CDMX (Portal Datos Abiertos) | CSV, GeoJSON | 224 concentraciones | Puntos fijos semifijos en vía pública con registro SEDECO. Coordenadas UTM proyectadas convertidas a WGS84 decimal. | [`data/raw/concentraciones_comerciantes.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/concentraciones_comerciantes.csv)<br>[`data/processed/concentraciones_comerciantes_limpio.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/concentraciones_comerciantes_limpio.json) |
| **Padrón Mercomuna CDMX (Muestra Activa)** | Secretaría de Bienestar / SAPCI | Web Scraped (AJAX) | 250 comercios muestra | Nombre del establecimiento, dirección, colonia, alcaldía y giro comercial registrado para recepción de vales Mercomuna. | [`data/raw/mercomuna_comercios_muestra.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/mercomuna_comercios_muestra.csv)<br>[`data/processed/mercomuna_comercios_limpio.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/mercomuna_comercios_limpio.json) |
| **Apoyos Emergentes a Comercio en Vía Pública** | Secretaría de Gobierno / SEDECO CDMX | CSV | 2,673 beneficiarios | Estatus de dispersión económica a comerciantes de alimentos preparados y comercio ambulante en las 16 alcaldías. | [`data/raw/apoyos_emergentes_comercio.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/apoyos_emergentes_comercio.csv)<br>[`data/processed/apoyos_emergentes_limpio.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/apoyos_emergentes_limpio.json) |
| **Programa de Microcréditos FONDESO** | Fondo para el Desarrollo Social (FONDESO) | Excel (XLSX) | 86,402 solicitudes | Folio, alcaldía, colonia, giro textual detallado, fecha de solicitud y estatus de aprobación/rechazo. | [`data/raw/fondeso_solicitudes.xlsx`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/fondeso_solicitudes.xlsx) |
| **Directorio Maestro Unificado de Comercio Popular** | Compilación propia normalizada | JSON, CSV | 1,971 establecimientos | Esquema homogéneo de 26 campos: ID, nombre, tipo_espacio (`FIJO`/`MOVIL`), horarios decimales, 7 banderas de días y coordenadas WGS84. | [`data/processed/directorio_comercio_popular.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/directorio_comercio_popular.json)<br>[`data/processed/directorio_comercio_popular.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/directorio_comercio_popular.csv) |
| **Centros de Abasto Mayoristas CDMX** | Compilación estratégica | JSON, CSV | 8 nodos clave | CEDA Iztapalapa, Merced Nave Mayor/Menor, Sonora, Jamaica, La Nueva Viga, La Viga y San Juan Pugibet con coordenadas y giros. | [`data/processed/centros_abasto_mayoristas.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/centros_abasto_mayoristas.json)<br>[`data/processed/centros_abasto_mayoristas.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/centros_abasto_mayoristas.csv) |

---

### 1.2 Cartografía y División Territorial

| Nombre | Fuente | Formato | Registros | Descripción | Ubicación Local |
|---|---|:---:|:---:|---|---|
| **Alcaldías de la CDMX** | Marco Geoestadístico INEGI / ADIP | GeoJSON | 16 polígonos | Polígonos oficiales de las 16 demarcaciones territoriales con claves INEGI (`CVEGEO`). | [`data/raw/cartografia/alcaldias.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/cartografia/alcaldias.geojson) |
| **Colonias de la CDMX** | IECM / ADIP | GeoJSON | 1,814 polígonos | Delimitación oficial de colonias, pueblos y barrios originarios para agregación barrial. | [`data/raw/cartografia/colonias.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/cartografia/colonias.geojson) |
| **Municipios Conurbados (ZMVM)** | Marco Geoestadístico INEGI | GeoJSON | 60 municipios | 59 municipios del Estado de México y 1 de Hidalgo conurbados con la capital para análisis de flujos metropolitanos. | [`data/raw/cartografia/zmvm_edomex.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/cartografia/zmvm_edomex.geojson) |

---

### 1.3 Movilidad Integrada (Red MI) y Transporte Concesionado

| Subsistema de Transporte | Fuente | Formato | Contenido | Ubicación Local |
|---|---|:---:|---|---|
| **Metro (STC)** | SEMOVI CDMX | GeoJSON | Líneas 1 a 12 y 195 estaciones georreferenciadas. | [`data/raw/transporte/metro_lineas.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/metro_lineas.geojson)<br>[`data/raw/transporte/metro_estaciones.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/metro_estaciones.geojson) |
| **Metrobús** | SEMOVI CDMX | GeoJSON | Líneas 1 a 7 y ~290 estaciones con conexiones. | [`data/raw/transporte/metrobus_lineas.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/metrobus_lineas.geojson)<br>[`data/raw/transporte/metrobus_estaciones.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/metrobus_estaciones.geojson) |
| **Cablebús** | SEMOVI CDMX | GeoJSON | Líneas 1, 2 y 3 con estaciones elevadas. | [`data/raw/transporte/cablebus_lineas.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/cablebus_lineas.geojson)<br>[`data/raw/transporte/cablebus_estaciones.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/cablebus_estaciones.geojson) |
| **Trolebús (STE)** | SEMOVI CDMX | GeoJSON | Líneas 1 a 12 (incluyendo Trolebús Elevado y Aztecas) y paradas. | [`data/raw/transporte/trolebus_lineas.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/trolebus_lineas.geojson)<br>[`data/raw/transporte/trolebus_paradas.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/trolebus_paradas.geojson) |
| **Tren Ligero (STE)** | SEMOVI CDMX | GeoJSON | Línea única Tasqueña - Xochimilco y 18 estaciones. | [`data/raw/transporte/tren_ligero_linea.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/tren_ligero_linea.geojson)<br>[`data/raw/transporte/tren_ligero_estaciones.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/tren_ligero_estaciones.geojson) |
| **RTP (Red de Transporte de Pasajeros)** | SEMOVI CDMX | GeoJSON | Rutas ordinarias, expresas, nochebús y ecobús con paradas. | [`data/raw/transporte/rtp_lineas.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/rtp_lineas.geojson)<br>[`data/raw/transporte/rtp_paradas.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/rtp_paradas.geojson) |
| **Transporte Concesionado (Microbuses)** | SEMOVI CDMX | Shapefile / ZIP | Rutas y ramales concesionados tradicionales hacia colonias periféricas. | [`data/raw/transporte/concesionado.zip`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/concesionado.zip) |
| **Paquete GTFS Estático Oficial CDMX** | SEMOVI CDMX | GTFS (ZIP) | `stops.txt`, `routes.txt`, `trips.txt`, `shapes.txt` de toda la Red MI. | [`data/raw/transporte/gtfs_cdmx.zip`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/transporte/gtfs_cdmx.zip) |

---

## 2. APIs, Servicios Web y Geoportales en Vivo

Catálogo técnico detallado disponible en: [`data/docs/apis_cdmx.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/docs/apis_cdmx.md).

### 2.1 Portal de Datos Abiertos CDMX (CKAN API v3)
- **Base URL:** `https://datos.cdmx.gob.mx/api/3/action/`
- **Autenticación:** Abierta (sin tokens ni restricciones de cuota rígidas).
- **Formatos:** JSON estándar CKAN con soporte de consultas relacionales SQL.
- **Endpoints verificados:**
  - `GET /package_search?q={termino}&rows={limite}`
  - `GET /datastore_search?resource_id={id}&limit={n}&q={filtro}`
  - `GET /datastore_search_sql?sql={SELECT ... FROM "resource_id" WHERE ...}`
- **Recursos estratégicos probados con Datastore activo:**
  - `c16cc0f7-8307-4a5f-a2d4-25e83b71faae` $\rightarrow$ Padrón de Tianguis de la CDMX (1,367 registros).
  - `c27dbd03-6083-40d5-a5cc-9e8c429779bc` $\rightarrow$ Padrón de Mercados Públicos (329 registros).
  - `8a6d280d-3ac4-4341-aad4-8ab1b66f1efb` $\rightarrow$ Infraestructura Comunitaria PILARES (300 centros activos).
  - `5e91cdbf-0ac3-44de-b60f-9402dba8b893` $\rightarrow$ Comedores Comunitarios SIBISO (483 comedores a $11 MXN).
  - `20e3f3a2-c53d-4ead-bb50-95fd4923dbe4` $\rightarrow$ Incidentes Viales reportados al C5 (590k+ registros).
  - `a8069e94-c7cb-45d7-8166-561e80884422` $\rightarrow$ Reportes de Agua y Fugas SACMEX (313k+ registros).

### 2.2 GeoServer WFS Oficial SIG CDMX (ADIP)
- **Endpoint WFS:** `https://catalogov2.sig.cdmx.gob.mx/geoserver/geonode/ows`
- **Protocolo:** OGC WFS 1.0.0 / 1.1.0 con salida nativa GeoJSON (`outputFormat=application/json`).
- **Autenticación:** Pública (sin token).
- **Capas vectoriales en vivo:**
  - `geonode:atlas_de_riesgo_inundaciones` $\rightarrow$ Polígonos de zonas inundables.
  - `geonode:atlas_de_riesgo_granizo` $\rightarrow$ Polígonos de vulnerabilidad por granizo (riesgo en lonas y techumbres de tianguis).
  - `geonode:cetram` $\rightarrow$ Centros de Transferencia Modal de la CDMX.
  - `geonode:metrobus_estaciones` y `geonode:metrobus_lineas` $\rightarrow$ Red Metrobús.
  - `geonode:stc_metro_estaciones` y `geonode:stc_metro_lineas` $\rightarrow$ Red Metro.
  - `geonode:cconcesionado_rutas` $\rightarrow$ Rutas de microbuses hacia colonias altas y periferias.
  - `geonode:rutas_rtp` $\rightarrow$ Red de Transporte de Pasajeros.
  - `geonode:cdmx_areas_verdes_2017` $\rightarrow$ Parques y arbolado para cálculo de sombra peatonal.
  - `geonode:lunas` $\rightarrow$ Unidades territoriales de atención y protección a mujeres.

### 2.3 Movilidad en Tiempo Real: Ecobici GBFS v2.3
- **Base URL:** `https://gbfs.mex.lyftbikes.com/gbfs/es/`
- **Refresco:** Cada 60 segundos (en vivo).
- **Endpoints:**
  - `GET /station_information.json` $\rightarrow$ Metadatos fijos de 677 estaciones (nombre, capacidad y coordenadas).
  - `GET /station_status.json` $\rightarrow$ Disponibilidad en tiempo real: `num_bikes_available`, `num_ebikes_available`, `num_docks_available`, `is_renting`.

### 2.4 Meteorología y Resiliencia Climática Hiperlocal (Open-Meteo)
- **Endpoint:** `https://api.open-meteo.com/v1/forecast`
- **Parámetros:** `latitude=19.4326&longitude=-99.1332&hourly=temperature_2m,precipitation_probability,precipitation,wind_gusts_10m,uv_index&timezone=America%2FMexico_City`
- **Utilidad:** Detección predictiva de lluvia torrencial o viento para alerta temprana en tianguis semanales.

### 2.5 Ruteo Peatonal y Multimodal (OSRM & OpenStreetMap)
- **OSRM Router:** `https://router.project-osrm.org/route/v1/walking/{lng1},{lat1};{lng2},{lat2}?overview=full&geometries=geojson`
- **Nominatim Geocoding:** `https://nominatim.openstreetmap.org/search?q={direccion},+CDMX&format=json`

---

## 3. Bibliografía Académica y Estudios Socioterritoriales

Investigaciones académicas documentadas en el dossier de investigación del Chilangatón 2026 sobre mercados, tianguis y gobernanza popular:

1. **Giglia, Angela (2018).** *Comercio, consumo y cultura en los mercados públicos de la Ciudad de México.* Universidad Autónoma Metropolitana, Unidad Iztapalapa (UAM-I). Incluye el levantamiento de la encuesta ECOMP a más de 18,000 locatarios en coordinación con SEDECO y el Consejo Económico y Social de la CDMX.  
   *Aporte al proyecto:* Demuestra que la política para mercados debe partir de la diversidad socioterritorial de cada barrio y no de recetas uniformes de modernización forzada.

2. **Delgadillo Polanco, Víctor Manuel (2016).** *«La disputa por los mercados de La Merced»*, Revista *Alteridades*, 26(51), pp. 55-69, UAM-Iztapalapa.  
   *Aporte al proyecto:* Análisis crítico sobre los proyectos gubernamentales de "rescate" que bajo un discurso de supuesta obsolescencia buscan mercantilizar y desplazar a los comerciantes tradicionales.

3. **Rosales, R., Hayden, T. y Crossa, M. (2023).** *«Heterogeneity among merchants in Mexico City's municipal markets»*, *Estudios Demográficos y Urbanos*, 38(2), El Colegio de México (Colmex). DOI: `10.24201/edu.v38i2.2148`.  
   *Aporte al proyecto:* Evidencia cuantitativa y cualitativa sobre cómo las intervenciones físicas y de digitalización vertical aumentan la vulnerabilidad laboral de los locatarios de mayor edad.

4. **Gayosso Ramírez, José Luis (2009).** *«Los tianguistas de la Ciudad de México: de informales a trabajadores atípicos»*, *Iztapalapa: Revista de Ciencias Sociales y Humanidades*, 30(66), pp. 119-140, UAM-I.  
   *Aporte al proyecto:* Documentación etnográfica y organizativa del tianguis de San Felipe de Jesús (GAM), demostrando la existencia de estructuras de gobernanza colectiva y defensa gremial histórica.

5. **Castillo Berthier, Héctor (1983).** *«El mercado de La Merced antes del cambio»*, *Revista Mexicana de Sociología*, 45(3), pp. 917-943, Instituto de Investigaciones Sociales, UNAM.  
   *Aporte al proyecto:* Estudio clásico sobre los mecanismos de abasto, relaciones de poder e intermediación mayorista en el centro de la Ciudad de México antes del traslado a la CEDA.

6. **Villegas, Pascale (2010).** *«Del tianguis prehispánico al tianguis colonial: pervivencia y transformación del mercado indígena en el centro de México»*, *Estudios Mesoamericanos*, Nueva Época, 8, pp. 43-52, UNAM.  
   *Aporte al proyecto:* Documenta la raíz mesoamericana de los tianguis (con juzgados propios de plaza en Tlatelolco para dirimir disputas), fundamentando por qué la tecnología moderna debe respetar la auto-organización comunitaria.

7. **Batista da Costa, F. y Alvarado Sizzo, I. (2023).** *Mercados y tianguis como patrimonio territorial latinoamericano.* Colección Geografía Urbana y Cultura, Universidad de La Rioja / UNAM.  
   *Aporte al proyecto:* Fundamenta el valor del mercado barrial como infraestructura social indispensable frente al modelo extractivo de los hipermercados.

---

## 4. Crítica al Solucionismo y Gobernanza de Datos

Marco teórico para blindar el prototipo frente al extractivismo de datos y la digitalización tecnocrática:

1. **Morozov, Evgeny (2013).** *To Save Everything, Click Here: The Folly of Technological Solutionism.* PublicAffairs, Nueva York.  
   *Premisa:* El solucionismo tecnológico reduce injusticias estructurales y conflictos de poder a problemas de "ineficiencia de datos", ofreciendo apps donde se requieren políticas públicas integrales.

2. **Couldry, Nick y Mejias, Ulises A. (2019).** *The Costs of Connection: How Data Is Colonizing Human Life and Appropriating It for Capitalism.* Stanford University Press.  
   *Premisa:* Colonialismo de datos: la extracción forzada de transacciones barriales para generar perfiles de riesgo y scores crediticios al servicio de corporaciones financieras y bancos.

3. **Costanza-Chock, Sasha (2020).** *Design Justice: Community-Led Practices to Build the Worlds We Need.* The MIT Press, Cambridge, MA.  
   *Premisa:* El codiseño de soluciones tecnológicas debe estar liderado por las comunidades tradicionalmente excluidas, garantizando que el valor generado se quede en el territorio.

4. **Scholz, Trebor (2016).** *Platform Cooperativism: Challenging the Corporate Sharing Economy.* Rosa Luxemburg Stiftung, Nueva York.  
   *Premisa:* Frente al extractivismo de plataformas tipo Uber/Rappi, la tecnología cívica debe operar bajo esquemas de cooperativismo, propiedad colectiva de datos y código abierto.

5. **GIDA (Global Indigenous Data Alliance) & Carroll et al. (2020).** *The CARE Principles for Indigenous Data Governance.* *Data Science Journal*, 19(1), p. 43.  
   *Principios adoptados por el proyecto:*
   - **C**ollective Benefit (Beneficio colectivo para los comerciantes).
   - **A**uthority to Control (Autoridad de la asamblea y del puestero sobre sus datos).
   - **R**esponsibility (Responsabilidad y rendición de cuentas del desarrollador).
   - **E**thics (Ética estricta: prohibición de capturar datos sensibles de cobro de piso, extorsión o fiscalización tributaria individual).

---

## 5. Marco Normativo, Gacetas y Políticas Públicas

1. **Reglamento de Mercados para el Distrito Federal (Vigente):** Marco legal que regula la administración compartida entre SEDECO (emisión de cédulas de empadronamiento) y las 16 Alcaldías (operación diaria, mantenimiento menor y Ventanilla Única).
2. **Lineamientos SITRAMERP / "Mercados Digitales CDMX" (Gaceta Oficial CDMX, 9 de enero y 27 de febrero de 2025):** Política de digitalización obligatoria suspendida y posteriormente derogada tras movilizaciones de más de 2,000 comerciantes que temían despojo de sus cédulas y locales.
3. **Programa de Rehabilitación de Mercados Públicos 2025–2026 (Gobierno CDMX):**
   - 2025: Inversión de 240 mdp para 81 mercados (prioridad en Gustavo A. Madero, Venustiano Carranza y Cuauhtémoc).
   - 2026: Presupuesto asignado de 234 mdp para 189 mercados públicos (1 millón de pesos por mercado, administrado por dos comisiones electas en asamblea: administración y vigilancia).
4. **Reglas de Operación del Programa Mercomuna (2020–2026):**
   - Secretaría de Bienestar e Igualdad Social (SIBISO) / SAPCI.
   - Presupuesto 2026: 1,600 millones de pesos, con 635,000 familias beneficiarias y 27,500 pequeños comercios afiliados.
   - Vales físicos en papel canjeables exclusivamente en comercio barrial sin comisiones bancarias.
5. **Banco de México — Circular 9/2026:**
   - Estandarización de los flujos de cobro interoperables mediante CoDi (código QR) y DiMo (transferencia por número de teléfono) sobre la infraestructura SPEI, obligando a las instituciones bancarias a unificar interfaces antes de diciembre de 2026.
6. **Censos Económicos 2024 (Resultados Oportunos CDMX, INEGI 2025):**
   - 453,823 unidades económicas en la CDMX; 93.5% son microempresas que concentran apenas el 11.8% de los ingresos totales.
   - 87.8% de los negocios cobra exclusivamente en efectivo; solo 6.7% vendió por internet en 2023.

---

## 6. Investigación Periodística y Reportes Gremiales

1. **Alianza Nacional de Pequeños Comerciantes (ANPEC, 2025):**  
   - Encuesta *«Pulso de la Tienda de Barrio 2025»*: El 53.86% de las tienditas otorga fiado; 4 de cada 10 reporta solicitudes crecientes por inflación; 77.5% teme cierres permanentes ante la expansión de cadenas de conveniencia y tiendas de descuento duro (Tiendas 3B, OXXO).
2. **Expansión Política (Febrero de 2025):**  
   - Reportaje especial sobre los 339 mercados públicos: 7 millones de consumidores atendidos semanalmente, 285,000 empleos directos y 2% de contribución al PIB local. Documentación de las 14 acciones prioritarias del Gobierno de la Ciudad.
3. **24 Horas y Eje Central (2026):**  
   - Cobertura sobre el subejercicio en la rehabilitación de mercados: a finales de junio de 2026 se había ejercido menos del 6% de los fondos programados para las comisiones de locatarios, evidenciando trabas burocráticas entre SEDECO y las alcaldías.
4. **El Universal (Marzo de 2025):**  
   - Cobertura de las protestas de locatarios contra la digitalización forzada y declaraciones de autoridades respecto a la corrupción en ventanillas de trámites (cobros indebidos de $5,000 a $50,000 por regularización de cédulas).
5. **Chilango y Posta (Octubre de 2025):**  
   - Reseña del mapa interactivo de tianguis desarrollado por el arquitecto Jerónimo Monroy a partir del padrón de SEDECO, señalando omisiones territoriales severas en alcaldías como Milpa Alta y Tláhuac.
6. **El CEO (2025):**  
   - Análisis económico sobre la pérdida del 42.8% en la facturación promedio de las tiendas de abarrotes frente al avance de más de 24,000 tiendas OXXO y 3,100 tiendas 3B a nivel nacional.

---

## 7. Trazabilidad de Entregables del Repositorio

| Directorio / Archivo | Tipo | Descripción y Componentes |
|---|:---:|---|
| [`data/raw/`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw) | Datasets Crudos | Archivos CSV, JSON, GeoJSON y Excel descargados directamente de portales abiertos gubernamentales. |
| [`data/processed/`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed) | Datasets Limpios | Datos estandarizados WGS84, horarios decimales, alcaldías canónicas y catálogo unificado (`directorio_comercio_popular.json`). |
| [`data/catalog/`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog) | Taxonomía de Giros | 9 Macro-Categorías, 67 Subgiros normalizados, `giro_classifier.py` con motor regex multi-etiqueta y atributos Mercomuna. |
| [`data/docs/apis_cdmx.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/docs/apis_cdmx.md) | Catálogo de APIs | Guía técnica y pruebas de conectividad en vivo de CKAN Datastore, GeoServer WFS SIG CDMX, Ecobici GBFS y OSRM. |
| [`docs/RUTEO_MULTIMODAL_CDMX.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/docs/RUTEO_MULTIMODAL_CDMX.md) | Documentación Técnica | Especificación del motor de ruteo multimodal (Metro + Metrobús + Trolebús + RTP + caminata hacia tianguis). |
| [`TODO_PROYECTO.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/TODO_PROYECTO.md) | Backlog del Proyecto | Lista estructurada de 8 módulos de trabajo con dependencias, dificultad y estatus de ejecución en tiempo real. |
| [`mapa_comercio_movilidad_cdmx.html`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/mapa_comercio_movilidad_cdmx.html) | Visor Web Integrado | Prototipo cartográfico interactivo que combina la capa de comercio popular con la Red de Movilidad Integrada. |
| [`scripts/`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts) | Pipelines ETL y Build | Scripts en Python para descarga, compilación del grafo de ruteo, normalización de datos y generación del visor web. |
