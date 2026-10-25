# Datasets Oficiales de Transporte y Movilidad Integrada (CDMX)

Datasets espaciales y tabulares descargados y normalizados desde el Portal de Datos Abiertos de la Ciudad de México (`datos.cdmx.gob.mx`).

Todos los archivos GeoJSON fueron proyectados al estándar geográfico global **WGS84 (EPSG:4326)**.

## Inventario de Capas de Transporte

| Archivo | Subsistema / Capa | Geometría | Registros / Features | Paquete Origen en CKAN |
| :--- | :--- | :--- | :--- | :--- |
| `cartografia/alcaldias.geojson` | Límites de las 16 Alcaldías de la CDMX | Polygon | **16** | `CKAN: alcaldias` |
| `cartografia/colonias.geojson` | Catálogo de Colonias de la CDMX | Polygon | **1543** | `CKAN: catalogo-de-colonias-datos-abiertos` |
| `transporte/metro_estaciones.geojson` | Estaciones del STC Metro CDMX | Point | **195** | `CKAN: lineas-y-estaciones-del-metro` |
| `transporte/metro_lineas.geojson` | Líneas del STC Metro CDMX | LineString/MultiLineString | **12** | `CKAN: lineas-y-estaciones-del-metro` |
| `transporte/metrobus_estaciones.geojson` | Estaciones del Metrobús CDMX | Point | **324** | `CKAN: geolocalizacion-metrobus` |
| `transporte/metrobus_lineas.geojson` | Líneas del Metrobús CDMX | LineString/MultiLineString | **64** | `CKAN: geolocalizacion-metrobus` |
| `transporte/trolebus_lineas.geojson` | Líneas del Trolebús CDMX | LineString/MultiLineString | **14** | `CKAN: STE` |
| `transporte/trolebus_paradas.geojson` | Paradas del Trolebús CDMX | Point | **805** | `CKAN: STE` |
| `transporte/cablebus_estaciones.geojson` | Estaciones del Cablebús CDMX | Point | **19** | `CKAN: geolocalizacion-de-lineas-y-estaciones-paradas-del-servicio-de-transportes-electricos` |
| `transporte/cablebus_lineas.geojson` | Líneas del Cablebús CDMX | LineString/MultiLineString | **4** | `CKAN: STE` |
| `transporte/tren_ligero_linea.geojson` | Línea del Tren Ligero CDMX | LineString/MultiLineString | **1** | `CKAN: STE` |
| `transporte/tren_ligero_estaciones.geojson` | Estaciones del Tren Ligero CDMX | Point | **18** | `CKAN: STE` |
| `transporte/rtp_lineas.geojson` | Rutas y Líneas de RTP | LineString/MultiLineString | **200** | `CKAN: rutas-de-rtp` |
| `transporte/rtp_paradas.geojson` | Paradas de la Red de Transporte de Pasajeros (RTP) | Point | **8132** | `CKAN: rutas-de-rtp` |
| `transporte/gtfs/` | GTFS Oficial Estático de la CDMX (Movilidad Integrada) | GTFS Relational Tables (CSV/TXT) | **301 rutas, 11362 paradas, 127135 puntos de forma** | `CKAN: gtfs` |

## Detalle de Archivos GTFS (`data/raw/transporte/gtfs/`)

| Archivo GTFS | Registros |
| :--- | :--- |
| `agency.txt` | 10 |
| `calendar.txt` | 13 |
| `frequencies.txt` | 1,584 |
| `routes.txt` | 301 |
| `shapes.txt` | 127,135 |
| `stop_times.txt` | 42,789 |
| `stops.txt` | 11,362 |
| `trips.txt` | 1,205 |

## Notas de Integración
- **Metro**: Incluye estaciones (puntos) y trazado de líneas (líneas) con atributos de línea y correspondencias.
- **Metrobús**: Incluye estaciones y líneas de los corredores 1 al 7.
- **Servicio de Transportes Eléctricos (STE)**: Cobertura completa de Cablebús (Líneas 1 y 2), Tren Ligero (Taxqueña-Xochimilco) y Red de Trolebús (líneas y paradas).
- **RTP**: Paradas y trazado de rutas de autobuses ordinarios y expresos.
- **GTFS**: Especificación estándar que unifica todos los modos de transporte de la CDMX.
