# Datasets para Reto 1: Comercio Popular y Barrial (Chilangotón 2026)

Este directorio contiene los conjuntos de datos abiertos descargados y procesados para el desarrollo del prototipo.

## Inventario de Datos (`data/raw/`)

| Archivo | Tamaño | Registros | Fuente | Descripción |
|---|---|---|---|---|
| [`tianguis.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/tianguis.csv) | ~206 KB | 1,367 | SEDECO CDMX | Padrón completo de tianguis en las 16 alcaldías con días de operación, horarios, colonias y coordenadas geográficas. |
| [`tianguis.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/tianguis.json) | ~637 KB | 1,367 features | SEDECO CDMX | Capa GeoJSON lista para visualización en mapas (Leaflet / Mapbox / OpenLayers). |
| [`mercados_publicos.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/mercados_publicos.csv) | ~64 KB | 329 | SEDECO CDMX | Padrón de mercados públicos con número de locales, m² de superficie, año de inauguración, estatus de protección y coordenadas. |
| [`mercados_publicos.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/mercados_publicos.json) | ~223 KB | 329 features | SEDECO CDMX | Capa GeoJSON de mercados públicos. |
| [`mercados_sobre_ruedas.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/mercados_sobre_ruedas.csv) | ~10 KB | 51 | SEDECO CDMX | Rutas oficiales de mercados sobre ruedas, día de operación, número de oferentes y coordenadas. |
| [`mercados_sobre_ruedas.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/mercados_sobre_ruedas.json) | ~23 KB | 51 features | SEDECO CDMX | GeoJSON de mercados sobre ruedas. |
| [`concentraciones_comerciantes.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/concentraciones_comerciantes.csv) | ~36 KB | 224 | SEDECO CDMX | Concentraciones de comerciantes en vía pública registradas ante SEDECO. |
| [`concentraciones_comerciantes.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/concentraciones_comerciantes.json) | ~103 KB | 224 features | SEDECO CDMX | GeoJSON de concentraciones de comerciantes. |
| [`mercomuna_comercios_muestra.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/mercomuna_comercios_muestra.csv) | ~26 KB | 250 | Mercomuna CDMX (en vivo) | Muestra de comercios de barrio afiliados que aceptan vales Mercomuna (nombre, giro, dirección, colonia, alcaldía). |
| [`apoyos_emergentes_comercio.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/apoyos_emergentes_comercio.csv) | ~279 KB | 2,673 | Gobierno CDMX | Registro de dispersión de apoyos a personas que ejercen el comercio en vía pública (alimentos). |
| [`fondeso_solicitudes.xlsx`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/fondeso_solicitudes.xlsx) | ~7.7 MB | ~80,000 | FONDESO CDMX | Historial de solicitudes de crédito microempresarial con estatus de aprobación/rechazo y giros. |

---

## Campos Principales

### 1. `tianguis.csv`
- `alcaldia`: Alcaldía donde se instala.
- `colonia`: Colonia sede.
- `ubicacion`: Calle o cruce de calles.
- `dia`: Día de instalación (LUNES, MARTES, MIERCOLES, JUEVES, VIERNES, SABADO, DOMINGO).
- `horario`: Rango de operación (ej. "8:00 A 17:00 HORAS").
- `latitud`, `longitud`: Coordenadas WGS84.

### 2. `mercados_publicos.csv`
- `mercado`: Nombre común (ej. "MERCADO AZCAPOTZALCO", "SAN JUAN", "JAMAICA").
- `numero`: Identificador oficial SEDECO.
- `locales`: Cantidad de locales empadronados.
- `direccion`, `colonia_mercado`, `alcaldia_mercado`.
- `superficie_m2`, `anio_inauguracion`, `giro`, `latitud`, `longitud`.
