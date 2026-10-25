# Catálogo Exhaustivo de APIs, Geodatos y Servicios Urbanos de la CDMX
**Proyecto:** Chilangatón 2026 — Reto de Comercio Popular y Barrial  
**Fecha de validación en vivo:** Octubre 2026  
**Documento:** `data/docs/apis_cdmx.md`  

---

## 1. Resumen Ejecutivo y Hallazgos Clave

Este catálogo documenta las interfaces de programación (APIs), servicios de mapas estándar (WFS/WMS/GeoJSON) y fuentes de datos abiertos en tiempo real y geoespaciales disponibles para la **Ciudad de México (CDMX)**. Todas las fuentes listadas a continuación fueron verificadas mediante pruebas automatizadas de conectividad, latencia, esquema de respuesta y autenticación.

### Principales conclusiones técnicas:
1. **Portal de Datos Abiertos CDMX (CKAN API v3 / Datastore):**  
   - 100% abierto, sin API key ni tokens requeridos.
   - Cuenta con soporte directo para consultas SQL dinámicas (`datastore_search_sql`) y paginación rápida por filtros (`datastore_search`), lo que permite realizar cruces analíticos en milisegundos directamente en el servidor sin descargar gigabytes de datos.
   - Alberga datos canónicos de: Tianguis (1,367 registros), Mercados Públicos (329 mercados), PILARES (300 centros), Comedores Comunitarios (483 puntos), Reportes de Agua SACMEX (313k+ registros), Emergencias Urbanas RUSE (31k+ registros) e Incidentes Viales C5 (590k+ registros).
2. **Movilidad en Tiempo Real (Ecobici GBFS):**  
   - El feed GBFS v2.3 oficial de Ecobici CDMX (`https://gbfs.mex.lyftbikes.com/gbfs/...`) opera con actualización en tiempo real cada 60 segundos, cubriendo 677 estaciones con disponibilidad exacta de bicis mecánicas, bicis eléctricas y anclajes libres.
3. **Geoportal Oficial SIG CDMX (GeoServer GeoNode WFS):**  
   - Se descubrió el endpoint activo de GeoServer WFS de la ADIP / SIG CDMX (`catalogov2.sig.cdmx.gob.mx/geoserver/geonode/ows`), el cual entrega capas vectoriales completas en formato nativo **GeoJSON** (`outputFormat=application/json`) sin requerir token.
   - Entrega capas vectoriales críticas: Atlas de Riesgo por Inundación, Atlas de Granizo, CETRAMs, Paradas y Líneas de Metrobús, Metro, Trolebús STE, Rutas Concesionadas (microbuses), Rutas RTP, Ciclovías, Áreas Verdes y Centros LUNAS de atención a mujeres.
4. **Meteorología y Clima Hiperlocal en Tiempo Real:**  
   - El portal web de SEDEMA/SIMAT se encuentra frecuentemente en migración/mantenimiento, pero la integración con la API abierta Open-Meteo para las coordenadas exactas de la CDMX (`19.4326, -99.1332`) y tianguis específicos proporciona probabilidad de lluvia horaria, radiación UV, temperatura y viento sin costo ni límites restrictivos.
5. **Ruteo Peatonal y Ciclista (OSRM):**  
   - El motor OSRM público (`router.project-osrm.org`) resuelve en menos de 1 segundo rutas caminables paso a paso con coordenadas GeoJSON precisas para conectar paradas de transporte público con tianguis y mercados.

---

## 2. Matriz Comparativa de APIs Disponibles

| Nombre del Servicio | Dependencia / Fuente | Tipo de API / Protocolo | Estado en Vivo | Latencia Media | Autenticación | Formato de Salida | Cobertura / Actualización |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CKAN Datastore CDMX** | ADIP CDMX | REST JSON (CKAN API v3) | **Activo (200)** | ~250 ms | Pública (Ninguna) | JSON / Tabular | CDMX (300k - 600k registros) |
| **CKAN Datastore SQL** | ADIP CDMX | SQL sobre HTTP POST/GET | **Activo (200)** | ~300 ms | Pública (Ninguna) | JSON (filas SQL) | CDMX (Consultas relacionales) |
| **Ecobici GBFS Info** | SEMOVI / Lyft Bikes | REST GBFS v2.3 | **Activo (200)** | ~550 ms | Pública (Ninguna) | JSON | 677 estaciones CDMX |
| **Ecobici GBFS Status** | SEMOVI / Lyft Bikes | REST GBFS v2.3 | **Activo (200)** | ~520 ms | Pública (Ninguna) | JSON | En vivo (cada 60 segundos) |
| **GeoServer WFS SIG CDMX** | ADIP / SIG CDMX | OGC WFS 1.0.0 / 1.1.0 | **Activo (200)** | ~400 ms | Pública (Ninguna) | GeoJSON (`application/json`) | 44 capas vectoriales oficiales |
| **Atlas de Riesgo WFS** | SGIRPC / ADIP | OGC WFS 1.0.0 | **Activo (200)** | ~450 ms | Pública (Ninguna) | GeoJSON (Polígonos riesgo) | Inundaciones, Granizo, Sismo |
| **Red de Transporte WFS** | SEMOVI / ADIP | OGC WFS 1.0.0 | **Activo (200)** | ~350 ms | Pública (Ninguna) | GeoJSON (Puntos y Líneas) | Metro, Metrobús, Trolebús, RTP |
| **Open-Meteo Clima & UV** | Open-Meteo / DWD | REST JSON | **Activo (200)** | ~180 ms | Pública (Ninguna) | JSON | Tiempo real + Pronóstico 7 días |
| **OSM Nominatim CDMX** | OpenStreetMap | REST JSON | **Activo (200)** | ~500 ms | Pública (User-Agent) | JSON | Geocodificación directa/inversa |
| **OSRM Ruteo Caminable** | Project OSRM / OSM | REST JSON | **Activo (200)** | ~400 ms | Pública (Ninguna) | GeoJSON con pasos de ruta | Ruteo peatonal y ciclista |

---

## 3. Fichas Técnicas Detalladas de Endpoints

### 3.1 Portal de Datos Abiertos CDMX (CKAN v3)

- **Base URL:** `https://datos.cdmx.gob.mx/api/3/action/`
- **Autenticación:** Ninguna.
- **Formato:** JSON estándar CKAN (`{"help": "...", "success": true, "result": {...}}`).

#### Endpoints Principales:
1. **Búsqueda de Catálogos:** `GET /package_search?q={query}&rows={n}`
2. **Metadatos de Dataset:** `GET /package_show?id={slug_o_id}`
3. **Consulta de Registros:** `GET /datastore_search?resource_id={resource_id}&limit={n}&q={filtro}`
4. **Consulta SQL Directa:** `GET o POST /datastore_search_sql?sql={SELECT ... FROM "resource_id" WHERE ...}`

#### Recursos Verificados con Datastore Activo:

##### A) Tianguis de la Ciudad de México
- **Resource ID:** `c16cc0f7-8307-4a5f-a2d4-25e83b71faae`
- **Total Registros:** 1,367 tianguis
- **Campos:** `_id`, `alcaldia`, `colonia`, `ubicacion`, `giro`, `dia`, `horario`, `latitud`, `longitud`
- **Ejemplo de Consulta SQL (Tianguis del Miércoles en Iztapalapa):**
```sql
SELECT _id, ubicacion, colonia, horario, latitud, longitud 
FROM "c16cc0f7-8307-4a5f-a2d4-25e83b71faae" 
WHERE "alcaldia" = 'IZTAPALAPA' AND "dia" = 'MIERCOLES'
```

##### B) Mercados Públicos Tradicionales
- **Resource ID:** `c27dbd03-6083-40d5-a5cc-9e8c429779bc`
- **Total Registros:** 329 mercados
- **Campos:** `_id`, `mercado`, `numero`, `locales`, `direccion`, `colonia_mercado`, `alcaldia_mercado`, `tipo`, `superficie_m2`, `anio_inauguracion`, `longitud`, `latitud`
- **Ejemplo de Consulta:**
```http
GET https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=c27dbd03-6083-40d5-a5cc-9e8c429779bc&limit=5
```

##### C) PILARES (Puntos de Innovación, Libertad, Arte, Educación y Saberes)
- **Resource ID:** `8a6d280d-3ac4-4341-aad4-8ab1b66f1efb`
- **Total Registros:** 300 centros
- **Campos:** `_id`, `CLAVE_ID`, `NOMBRE_PILARES*`, `ESTATUS`, `REGION`, `ALCALDIA`, `LATITUD`, `LONGITUD`
- **Utilidad:** Puntos de conexión digital, asesoría de cooperativas y talleres para comerciantes populares.

##### D) Comedores Comunitarios (SIBISO / Participación Ciudadana)
- **Resource ID:** `5e91cdbf-0ac3-44de-b60f-9402dba8b893`
- **Total Registros:** 483 comedores populares
- **Campos:** `_id`, `folio`, `tipo_comedor`, `denominacion_o_razon_social`, `alcaldia`, `calle`, `colonia`, `codigo_postal`, `latitud`, `longitud`
- **Utilidad:** Nodos de seguridad alimentaria y precios accesibles articulados con mercados.

##### E) Incidentes Viales reportados por C5
- **Resource ID:** `20e3f3a2-c53d-4ead-bb50-95fd4923dbe4`
- **Total Registros:** 590,636 incidentes georreferenciados
- **Campos:** `folio`, `fecha_creacion`, `hora_creacion`, `tipo_incidente_c4`, `incidente_c4`, `alcaldia_inicio`, `colonia_catalogo`, `longitud`, `latitud`
- **Utilidad:** Identificar puntos ciegos, atropellamientos o conflictos de tránsito alrededor de zonas de carga y descarga de tianguis.

##### F) Reportes de Agua SACMEX (Fugas, Falta de Agua, Encharcamientos)
- **Resource ID:** `a8069e94-c7cb-45d7-8166-561e80884422`
- **Total Registros:** 313,756 reportes (2022 - 2024)
- **Campos:** `folio_incidente`, `clasificacion`, `reporte`, `alcaldia_catalogo`, `colonia_catalogo`, `latitud`, `longitud`

##### G) Registro Único de Situaciones de Emergencia (RUSE - Protección Civil)
- **Resource ID:** `803cb0b9-43af-4073-bbfd-0b542c5fd337`
- **Total Registros:** 31,589 emergencias
- **Campos:** `fenomeno`, `taxonomia`, `incidente`, `causas`, `calle_y_nu`, `colonia`, `alcaldia`, `latitud`, `longitud`

---

### 3.2 Movilidad en Tiempo Real: Ecobici GBFS

Ecobici publica sus datos bajo el estándar internacional **GBFS v2.3 (General Bikeshare Feed Specification)**. Es el único sistema de transporte de la CDMX con API abierta de streaming en tiempo real sin token.

- **Auto-Discovery URL (Master):** `https://gbfs.mex.lyftbikes.com/gbfs/gbfs.json`
- **Frecuencia de refresco:** 60 segundos (campo `ttl: 60`).

#### Endpoints Específicos:
1. **Información de Estaciones (Estática):**
   - **URL:** `https://gbfs.mex.lyftbikes.com/gbfs/es/station_information.json`
   - **Payload de salida:**
     ```json
     {
       "station_id": "1",
       "name": "CE-710 Molino del Rey - Glorieta de la Lealtad",
       "short_name": "710",
       "lat": 19.416795,
       "lon": -99.192508,
       "capacity": 39,
       "rental_methods": ["CREDITCARD", "KEY"],
       "has_kiosk": true
     }
     ```
2. **Estado Dinámico de Estaciones (Tiempo Real):**
   - **URL:** `https://gbfs.mex.lyftbikes.com/gbfs/es/station_status.json`
   - **Payload de salida:**
     ```json
     {
       "station_id": "1",
       "num_bikes_available": 9,
       "num_bikes_disabled": 0,
       "num_docks_available": 30,
       "num_docks_disabled": 0,
       "is_renting": 1,
       "is_returning": 1,
       "last_reported": 1792946736
     }
     ```
3. **Información del Sistema:**
   - **URL:** `https://gbfs.mex.lyftbikes.com/gbfs/es/system_information.json`

---

### 3.3 Geoportal ADIP / SIG CDMX (GeoServer WFS / WMS)

El servidor GeoServer de la ADIP alberga 44 capas oficiales de cartografía vectorial urbana. El protocolo WFS 1.0.0 permite solicitar directamente features en formato **GeoJSON** estándar para integrarlos en Leaflet, Mapbox GL o Turf.js.

- **WFS Base URL:** `https://catalogov2.sig.cdmx.gob.mx/geoserver/geonode/ows`
- **Parámetros estándar:**
  - `service=WFS`
  - `version=1.0.0`
  - `request=GetFeature`
  - `typeName=geonode:{nombre_capa}`
  - `outputFormat=application/json`
  - `maxFeatures={n}` *(opcional)*
  - `bbox={minx,miny,maxx,maxy}` *(opcional, para recortar geográficamente)*

#### Capas Más Valiosas Verificadas:

| Capa (`typeName`) | Geometría | Descripción y Aplicación |
| :--- | :--- | :--- |
| `geonode:atlas_de_riesgo_inundaciones` | MultiPolygon | Zonas y polígonos de susceptibilidad a inundación y encharcamiento severo con periodo de retorno. |
| `geonode:atlas_de_riesgo_granizo` | MultiPolygon | Historial y susceptibilidad de tormentas de granizo (crítico para techumbres de lonas de tianguis). |
| `geonode:cetram` | Point | Centros de Transferencia Modal (Paraderos Pantitlán, Indios Verdes, Chapultepec, etc.). |
| `geonode:metrobus_estaciones` | Point | Estaciones de las 7 líneas de Metrobús con nombre, línea y alcaldía. |
| `geonode:metrobus_lineas` | MultiLineString | Trazado de los corredores BRT de Metrobús. |
| `geonode:stc_metro_estaciones` | Point | 195 estaciones del Sistema de Transporte Colectivo Metro. |
| `geonode:stc_metro_lineas` | MultiLineString | Red de 12 líneas de Metro. |
| `geonode:ste_trolebus_paradas` | Point | Paradas de trolebús (Servicio de Transportes Eléctricos). |
| `geonode:cablebus_estaciones_...` | Point | Estaciones de Línea 1, 2 y 3 de Cablebús. |
| `geonode:cconcesionado_rutas` | MultiLineString | Rutas de transporte concesionado (microbuses y vagonetas que conectan barrios periféricos). |
| `geonode:rutas_rtp` | MultiLineString | Red de Transporte de Pasajeros de la CDMX (RTP). |
| `geonode:infr_vial_ciclista` | MultiLineString | Red de ciclovías, ciclocarriles y sendas compartidas. |
| `geonode:cdmx_areas_verdes_2017` | MultiPolygon | Parques y camellones arbolados (análisis de sombra e islas de calor). |
| `geonode:lunas` | Point | Unidades de atención a mujeres de la Secretaría de las Mujeres (puntos seguros). |
| `geonode:biciestacionamientos` | Point | Biciestacionamientos masivos y semimasivos en nodos de transporte. |

---

### 3.4 Meteorología y Clima Hiperlocal (Open-Meteo CDMX)

Dado que los puestos de comercio popular en tianguis operan al aire libre bajo carpas y lonas, el factor meteorológico es crítico para la seguridad y las ventas.

- **URL:** `https://api.open-meteo.com/v1/forecast`
- **Método:** `GET` (0 API Keys, 100% abierto)
- **Parámetros:**
  - `latitude=19.4326&longitude=-99.1332`
  - `current=temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,wind_speed_10m`
  - `hourly=precipitation_probability,uv_index,temperature_2m`
  - `timezone=America/Mexico_City`
  - `forecast_days=1`
- **Ejemplo de Respuesta:**
  ```json
  {
    "current": {
      "temperature_2m": 17.6,
      "relative_humidity_2m": 52,
      "precipitation": 0.0,
      "weather_code": 3,
      "wind_speed_10m": 2.3
    },
    "hourly": {
      "precipitation_probability": [0, 5, 10, 45, 60, ...],
      "uv_index": [0.0, 1.2, 4.6, 7.8, 8.5, 3.2, ...]
    }
  }
  ```

---

### 3.5 Geocodificación y Enrutamiento Ligero (OSM & OSRM)

#### A) Geocodificación acotada a CDMX (Nominatim)
- **URL:** `https://nominatim.openstreetmap.org/search`
- **Parámetros:**
  - `q=Mercado+de+Jamaica+CDMX`
  - `format=json`
  - `countrycodes=mx`
  - `viewbox=-99.36,19.59,-98.94,19.12` *(Bounding Box CDMX)*
  - `bounded=1`
  - `limit=1`
- **Encabezado Obligatorio:** `User-Agent: MiAppChilangaton/1.0`

#### B) Ruteo Caminable y Ciclista (Project OSRM)
- **Ruta Peatonal:** `https://router.project-osrm.org/route/v1/walking/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson&steps=true`
- **Ruta Ciclista:** `https://router.project-osrm.org/route/v1/bicycle/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson`
- **Respuesta:** Objeto GeoJSON listo para dibujar en Leaflet (`route.geometry.coordinates`) con distancia en metros, duración estimada en segundos y pasos de giro calle por calle.

---

## 4. Ideas de Valor Agregado para el Hackatón (Chilangatón 2026)

Integrando estas APIs con los 1,367 tianguis y 329 mercados, se pueden implementar **6 innovaciones de alto impacto** para el reto de Comercio Popular y Barrial:

### Idea 1: *Ruta Peatonal Protegida y con Sombra hacia el Tianguis*
- **APIs combinadas:** OSRM (Ruteo a pie) + GeoServer WFS (`cdmx_areas_verdes_2017`) + C5 WiFi/Postes.
- **Caso de uso:** Las marchantas y personas mayores caminan cargando bolsas pesadas bajo el sol del mediodía. El sistema genera una ruta peatonal inteligente desde la estación de Metro/Metrobús más cercana al tianguis, priorizando calles arboladas (con sombra natural) y calles con postes C5 iluminados y vigilados.
- **Innovación en el prototipo:** Un switch interactivo en el mapa: `[Modo Marchante: Ruta con Sombra y Seguridad]`.

### Idea 2: *Radar de Resiliencia Climática para Comerciantes al Aire Libre*
- **APIs combinadas:** Open-Meteo (probabilidad de lluvia y ráfagas de viento) + GeoServer WFS (`atlas_de_riesgo_inundaciones` y `atlas_de_riesgo_granizo`) + SACMEX Datastore (`reportes-de-agua`).
- **Caso de uso:** Una lona desgarrada por vientos de 40 km/h o una inundación repentina puede arruinar miles de pesos en mercancía de ropa o electrónicos de un tianguista. El sistema emite una alerta preventiva horaria ("Alerta Amarilla: Lluvia moderada a las 16:00 hrs en el Tianguis El Salado; riesgo alto de encharcamiento en esquina Av. Texcoco").
- **Innovación en el prototipo:** Tarjeta informativa de *Semáforo Climático Barrial* para el día del tianguis.

### Idea 3: *Hub Digital de Cobro Barrial (Wi-Fi C5 + PILARES + DiMo / CoDi)*
- **APIs combinadas:** CKAN Datastore (`puntos-de-acceso-wifi-en-la-cdmx` / `ubicacion-y-estado-pilares`) + Datasets de Mercados y Tianguis.
- **Caso de uso:** Uno de los grandes cuellos de botella del comercio popular es la falta de datos móviles de marchantes y comerciantes para concretar cobros con tarjeta o transferencias DiMo/SPEI. Al calcular un buffer de 50 metros alrededor de cada poste C5 con Wi-Fi gratuito o PILARES, el mapa identifica las "Zonas de Inclusión Digital de Cobro" dentro del tianguis donde es 100% viable cobrar sin saldo móvil.
- **Innovación en el prototipo:** Filtro visual: *"Ver puestos y pasillos con Wi-Fi CDMX para cobro digital"*.

### Idea 4: *Conexión Intermodal de Marchantes y Mercancías*
- **APIs combinadas:** Ecobici GBFS en vivo + GeoServer WFS (`cetram`, `rutas_rtp`, `cconcesionado_rutas`).
- **Caso de uso:** Muchos comerciantes o ayudantes se mueven en bicicleta o transporte concesionado para trasladar canastos o insumos desde CETRAMs periféricos (ej. Central de Abasto, San Lázaro, Tacubaya). El mapa muestra en tiempo real la disponibilidad de anclajes Ecobici cercanos y las rutas directas de microbuses/RTP que conectan mercados zonales con colonias populares.
- **Innovación en el prototipo:** Módulo *"¿Cómo llegar en transporte público o bici de carga?"* en la ficha de cada mercado.

### Idea 5: *Corredor Seguro de Género para Comerciantes Mujeres*
- **APIs combinadas:** GeoServer WFS (`geonode:lunas`) + CKAN Datastore (`ubicacion_c5_c2` / `incidentes-viales-c5`).
- **Caso de uso:** Más del 50% de las comerciantes en vía pública y marchantas son mujeres. Al identificar la red de centros LUNAS y postes C5 con botón de auxilio violeta adyacentes a tianguis, el sistema traza corredores seguros para la apertura (5:00 AM) y desmantelamiento (7:00 PM) de puestos.
- **Innovación en el prototipo:** Capa de *"Puntos de Auxilio y LUNAS Cercanos"*.

### Idea 6: *Circuito de Canasta Básica y Soberanía Alimentaria*
- **APIs combinadas:** CKAN Datastore (`comedores-cdmx` / `5e91cdbf-0ac3-44de-b60f-9402dba8b893`) + Mercados Públicos.
- **Caso de uso:** Articular la política social de comedores comunitarios ($11 pesos la comida) con el abastecimiento local en mercados públicos y tianguis del mismo barrio, promoviendo el consumo local y apoyando a familias en vulnerabilidad alimentaria.
- **Innovación en el prototipo:** Indicador de proximidad Comedor-Mercado para economías circulares barriales.

---

## 5. Guía de Integración Rápida con Código

### Consulta en JavaScript (Fetch directo desde el Frontend del Mapa):

```javascript
// 1. Obtener Tianguis del día en una alcaldía específica vía SQL CKAN
async function getTianguisPorDia(alcaldia, dia) {
  const resourceId = "c16cc0f7-8307-4a5f-a2d4-25e83b71faae";
  const sql = `SELECT _id, ubicacion, colonia, horario, latitud, longitud 
               FROM "${resourceId}" 
               WHERE "alcaldia" = '${alcaldia}' AND "dia" = '${dia}'`;
  const url = `https://datos.cdmx.gob.mx/api/3/action/datastore_search_sql?sql=${encodeURIComponent(sql)}`;
  
  const response = await fetch(url);
  const data = await response.json();
  return data.result.records;
}

// 2. Cargar Capa GeoJSON del Atlas de Riesgo por Inundación desde GeoServer SIG CDMX
async function getPoligonosInundacion() {
  const url = "https://catalogov2.sig.cdmx.gob.mx/geoserver/geonode/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=geonode:atlas_de_riesgo_inundaciones&outputFormat=application%2Fjson";
  const response = await fetch(url);
  return await response.json(); // Retorna FeatureCollection GeoJSON directo para L.geoJSON(data).addTo(map)
}

// 3. Consultar disponibilidad en tiempo real de Ecobici
async function getEcobiciEnVivo() {
  const [infoRes, statusRes] = await Promise.all([
    fetch("https://gbfs.mex.lyftbikes.com/gbfs/es/station_information.json"),
    fetch("https://gbfs.mex.lyftbikes.com/gbfs/es/station_status.json")
  ]);
  const info = (await infoRes.json()).data.stations;
  const status = (await statusRes.json()).data.stations;
  
  const statusMap = new Map(status.map(s => [s.station_id, s]));
  return info.map(station => ({
    ...station,
    status: statusMap.get(station.station_id) || {}
  }));
}
```

### Consulta en Python (Backend o Scripts de Enriquecimiento):

```python
import requests

def obtener_clima_tianguis(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,precipitation,wind_speed_10m&hourly=precipitation_probability,uv_index&timezone=America%2FMexico_City&forecast_days=1"
    res = requests.get(url, timeout=5)
    return res.json()

def rutar_a_pie(origen_lon, origen_lat, destino_lon, destino_lat):
    url = f"https://router.project-osrm.org/route/v1/walking/{origen_lon},{origen_lat};{destino_lon},{destino_lat}?overview=full&geometries=geojson"
    res = requests.get(url, timeout=5)
    data = res.json()
    if data.get("code") == "Ok":
        ruta = data["routes"][0]
        return {
            "distancia_metros": ruta["distance"],
            "tiempo_minutos": round(ruta["duration"] / 60, 1),
            "geojson": ruta["geometry"]
        }
    return None
```
