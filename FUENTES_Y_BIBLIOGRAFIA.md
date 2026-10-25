# Compendio Exhaustivo de Fuentes, Datasets, APIs y Bibliografía
**Proyecto:** Comercio Popular, Barrial y Movilidad Integrada en la CDMX  
**Marco:** Chilangatón 2026 — Reto 1: Comercio Popular y Barrial (SEDECO / SECTEI / SAF)  
**Ubicación:** `FUENTES_Y_BIBLIOGRAFIA.md`  
**Última actualización:** 25 de octubre de 2026  

---

## Índice General

1. [Páginas Web y Portales Consultados Directamente (Webliografía Oficial y Enlaces en Vivo)](#1-páginas-web-y-portales-consultados-directamente)
2. [Inventario de Datasets Descargados y Procesados Localmente](#2-inventario-de-datasets-descargados-y-procesados-localmente)
3. [APIs, Servicios Web y Geoportales en Vivo](#3-apis-servicios-web-y-geoportales-en-vivo)
4. [Bibliografía Académica y Estudios Socioterritoriales](#4-bibliografía-académica-y-estudios-socioterritoriales)
5. [Crítica al Solucionismo y Principios de Gobernanza de Datos](#5-crítica-al-solucionismo-y-gobernanza-de-datos)
6. [Marco Normativo, Gacetas y Políticas Públicas](#6-marco-normativo-gacetas-y-políticas-públicas)
7. [Investigación Periodística y Reportes Gremiales](#7-investigación-periodística-y-reportes-gremiales)
8. [Trazabilidad de Scripts y Entregables del Repositorio](#8-trazabilidad-de-entregables-del-repositorio)

---

## 1. Páginas Web y Portales Consultados Directamente

Relación detallada de todas las URLs, plataformas web, repositorios de datos abiertos y endpoints que fueron consultados, sondeados o descargados durante el desarrollo de este proyecto:

### 1.1 Portal de Datos Abiertos de la Ciudad de México (`datos.cdmx.gob.mx`)
* **Portal Principal:** [`https://datos.cdmx.gob.mx/`](https://datos.cdmx.gob.mx/)
* **Motor de Búsqueda CKAN API v3:** [`https://datos.cdmx.gob.mx/api/3/action/package_search`](https://datos.cdmx.gob.mx/api/3/action/package_search)
* **Datasets consultados y descargados:**
  1. *Tianguis de la Ciudad de México:*
     - Página del dataset: [`https://datos.cdmx.gob.mx/dataset/tianguis-de-la-ciudad-de-mexico`](https://datos.cdmx.gob.mx/dataset/tianguis-de-la-ciudad-de-mexico)
     - Descarga directa CSV: [`https://datos.cdmx.gob.mx/dataset/64aa33ed-e3f4-4949-aab5-4fcca129eecd/resource/c16cc0f7-8307-4a5f-a2d4-25e83b71faae/download/c16cc0f7-8307-4a5f-a2d4-25e83b71faae.csv`](https://datos.cdmx.gob.mx/dataset/64aa33ed-e3f4-4949-aab5-4fcca129eecd/resource/c16cc0f7-8307-4a5f-a2d4-25e83b71faae/download/c16cc0f7-8307-4a5f-a2d4-25e83b71faae.csv)
     - Descarga directa GeoJSON: [`https://datos.cdmx.gob.mx/dataset/64aa33ed-e3f4-4949-aab5-4fcca129eecd/resource/c9360f3f-ce49-4b4f-a3c9-f221a97f870e/download/c9360f3f-ce49-4b4f-a3c9-f221a97f870e.json`](https://datos.cdmx.gob.mx/dataset/64aa33ed-e3f4-4949-aab5-4fcca129eecd/resource/c9360f3f-ce49-4b4f-a3c9-f221a97f870e/download/c9360f3f-ce49-4b4f-a3c9-f221a97f870e.json)
  2. *Mercados Públicos de la Ciudad de México:*
     - Página del dataset: [`https://datos.cdmx.gob.mx/dataset/mercados-publicos`](https://datos.cdmx.gob.mx/dataset/mercados-publicos)
     - Descarga directa CSV: [`https://datos.cdmx.gob.mx/dataset/6e008c6b-197c-49f2-899f-47b9a406596c/resource/c27dbd03-6083-40d5-a5cc-9e8c429779bc/download/c27dbd03-6083-40d5-a5cc-9e8c429779bc.csv`](https://datos.cdmx.gob.mx/dataset/6e008c6b-197c-49f2-899f-47b9a406596c/resource/c27dbd03-6083-40d5-a5cc-9e8c429779bc/download/c27dbd03-6083-40d5-a5cc-9e8c429779bc.csv)
     - Descarga directa GeoJSON: [`https://datos.cdmx.gob.mx/dataset/6e008c6b-197c-49f2-899f-47b9a406596c/resource/39a74f11-55c5-4abf-aaf2-3558a9a281f7/download/39a74f11-55c5-4abf-aaf2-3558a9a281f7.json`](https://datos.cdmx.gob.mx/dataset/6e008c6b-197c-49f2-899f-47b9a406596c/resource/39a74f11-55c5-4abf-aaf2-3558a9a281f7/download/39a74f11-55c5-4abf-aaf2-3558a9a281f7.json)
  3. *Mercados Sobre Ruedas de la Ciudad de México:*
     - Página del dataset: [`https://datos.cdmx.gob.mx/dataset/mercados-sobre-ruedas`](https://datos.cdmx.gob.mx/dataset/mercados-sobre-ruedas)
     - Descarga directa CSV: [`https://datos.cdmx.gob.mx/dataset/07c86bbd-6795-4d13-aaca-42427e24e895/resource/90edcf0d-f603-4720-b386-e1d381260e8a/download/90edcf0d-f603-4720-b386-e1d381260e8a.csv`](https://datos.cdmx.gob.mx/dataset/07c86bbd-6795-4d13-aaca-42427e24e895/resource/90edcf0d-f603-4720-b386-e1d381260e8a/download/90edcf0d-f603-4720-b386-e1d381260e8a.csv)
     - Descarga directa GeoJSON: [`https://datos.cdmx.gob.mx/dataset/07c86bbd-6795-4d13-aaca-42427e24e895/resource/4814c177-b5c5-47f0-b5c5-9997be87a711/download/4814c177-b5c5-47f0-b5c5-9997be87a711.json`](https://datos.cdmx.gob.mx/dataset/07c86bbd-6795-4d13-aaca-42427e24e895/resource/4814c177-b5c5-47f0-b5c5-9997be87a711/download/4814c177-b5c5-47f0-b5c5-9997be87a711.json)
  4. *Concentraciones de Comerciantes:*
     - Página del dataset: [`https://datos.cdmx.gob.mx/dataset/concentraciones-de-comerciantes`](https://datos.cdmx.gob.mx/dataset/concentraciones-de-comerciantes)
     - Descarga directa CSV: [`https://datos.cdmx.gob.mx/dataset/a9fe73b0-7f67-45e9-91dd-85cca91d45ca/resource/1949ed54-f009-4dfe-a466-fd2620a9c2b5/download/1949ed54-f009-4dfe-a466-fd2620a9c2b5.csv`](https://datos.cdmx.gob.mx/dataset/a9fe73b0-7f67-45e9-91dd-85cca91d45ca/resource/1949ed54-f009-4dfe-a466-fd2620a9c2b5/download/1949ed54-f009-4dfe-a466-fd2620a9c2b5.csv)
     - Descarga directa GeoJSON: [`https://datos.cdmx.gob.mx/dataset/a9fe73b0-7f67-45e9-91dd-85cca91d45ca/resource/6ddb338e-3d03-4a79-b5e7-b0478608c2f0/download/6ddb338e-3d03-4a79-b5e7-b0478608c2f0.json`](https://datos.cdmx.gob.mx/dataset/a9fe73b0-7f67-45e9-91dd-85cca91d45ca/resource/6ddb338e-3d03-4a79-b5e7-b0478608c2f0/download/6ddb338e-3d03-4a79-b5e7-b0478608c2f0.json)
  5. *Solicitudes de Financiamiento para Microempresas FONDESO:*
     - Descarga directa XLSX: [`https://datos.cdmx.gob.mx/dataset/6ab620e0-a11b-4a60-a5b1-cbfff4ddc207/resource/67df5e9f-8b3a-4b1b-9786-30354f63338c/download/67df5e9f-8b3a-4b1b-9786-30354f63338c.xlsx`](https://datos.cdmx.gob.mx/dataset/6ab620e0-a11b-4a60-a5b1-cbfff4ddc207/resource/67df5e9f-8b3a-4b1b-9786-30354f63338c/download/67df5e9f-8b3a-4b1b-9786-30354f63338c.xlsx)
  6. *Apoyos Emergentes a Comercio en Vía Pública (Alimentos):*
     - Descarga directa CSV: [`https://datos.cdmx.gob.mx/dataset/e5404c70-dda3-4a84-87fe-e7dabd4296fe/resource/b900d083-43bc-49e3-ae25-422d14803a92/download/b900d083-43bc-49e3-ae25-422d14803a92.csv`](https://datos.cdmx.gob.mx/dataset/e5404c70-dda3-4a84-87fe-e7dabd4296fe/resource/b900d083-43bc-49e3-ae25-422d14803a92/download/b900d083-43bc-49e3-ae25-422d14803a92.csv)
  7. *Líneas y Estaciones de Movilidad Integrada (Metro, Metrobús, Trolebús, Cablebús, RTP, Tren Ligero):*
     - Dataset SEMOVI: [`https://datos.cdmx.gob.mx/dataset/lineas-y-estaciones-del-metro-metrobus-rtp-trolebus-tren-ligero-y-cablebus`](https://datos.cdmx.gob.mx/dataset/lineas-y-estaciones-del-metro-metrobus-rtp-trolebus-tren-ligero-y-cablebus)

---

### 1.2 Padrón Oficial de Comercios Mercomuna
* **Portal Oficial del Programa:** [`https://comercios-mercomuna.cdmx.gob.mx/`](https://comercios-mercomuna.cdmx.gob.mx/)
* **Script de Búsqueda:** [`https://comercios-mercomuna.cdmx.gob.mx/assets/reporteador2.js`](https://comercios-mercomuna.cdmx.gob.mx/assets/reporteador2.js)
* **Endpoint de Paginación y Consulta AJAX en vivo:** `https://comercios-mercomuna.cdmx.gob.mx/?page={num_pagina}` *(probado con cabecera `X-Requested-With: XMLHttpRequest` para extracción de 250 comercios muestra de las 905 páginas existentes).*

---

### 1.3 Sistema Nacional de Información e Integración de Mercados (SNIIM)
* **Portal de la Secretaría de Economía:** [`http://www.economia-sniim.gob.mx/nuevo/`](http://www.economia-sniim.gob.mx/nuevo/)
* **Módulo de Consulta Agrícola (Frutas y Hortalizas):** [`http://www.economia-sniim.gob.mx/nuevo/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ConsultaFrutasYHortalizas.aspx`](http://www.economia-sniim.gob.mx/nuevo/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ConsultaFrutasYHortalizas.aspx)
* **Resultados de Precios Mayoreo en Central de Abasto CDMX:** [`http://www.economia-sniim.gob.mx/nuevo/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ResultadosConsultaFechaFrutasYHortalizas.aspx`](http://www.economia-sniim.gob.mx/nuevo/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ResultadosConsultaFechaFrutasYHortalizas.aspx) *(Parámetro validado: Destino ID 100: DF Central de Abasto de Iztapalapa).*

---

### 1.4 Geoportal Oficial SIG CDMX / GeoServer GeoNode (ADIP)
* **Endpoint WFS Oficial en Vivo:** [`https://catalogov2.sig.cdmx.gob.mx/geoserver/geonode/ows`](https://catalogov2.sig.cdmx.gob.mx/geoserver/geonode/ows)
* **Petición GetCapabilities:** `https://catalogov2.sig.cdmx.gob.mx/geoserver/geonode/ows?service=wfs&version=1.1.0&request=GetCapabilities`
* **Peticiones GetFeature probadas con salida GeoJSON (`outputFormat=application/json`):**
  - Atlas de Riesgo por Inundación: `...&request=GetFeature&typeName=geonode:atlas_de_riesgo_inundaciones&outputFormat=application/json`
  - Atlas de Riesgo por Granizo: `...&request=GetFeature&typeName=geonode:atlas_de_riesgo_granizo&outputFormat=application/json`
  - Centros de Transferencia Modal (CETRAM): `...&request=GetFeature&typeName=geonode:cetram&outputFormat=application/json`
  - Transporte Concesionado (Rutas de Microbuses): `...&request=GetFeature&typeName=geonode:cconcesionado_rutas&outputFormat=application/json`
  - Rutas de la Red de Transporte de Pasajeros (RTP): `...&request=GetFeature&typeName=geonode:rutas_rtp&outputFormat=application/json`
  - Estaciones y Líneas de Metrobús: `...&request=GetFeature&typeName=geonode:metrobus_estaciones&outputFormat=application/json`
  - Estaciones y Líneas del STC Metro: `...&request=GetFeature&typeName=geonode:stc_metro_estaciones&outputFormat=application/json`
  - Áreas Verdes de la CDMX (Sombra y confort peatonal): `...&request=GetFeature&typeName=geonode:cdmx_areas_verdes_2017&outputFormat=application/json`
  - Módulos LUNAS (Espacios seguros de atención a mujeres): `...&request=GetFeature&typeName=geonode:lunas&outputFormat=application/json`

---

### 1.5 Ecobici CDMX (API GBFS en Tiempo Real)
* **Página Oficial de Datos Abiertos de Ecobici:** [`https://ecobici.cdmx.gob.mx/datos-abiertos/`](https://ecobici.cdmx.gob.mx/datos-abiertos/)
* **Información Fija de Cicloestaciones (GBFS v2.3):** [`https://gbfs.mex.lyftbikes.com/gbfs/es/station_information.json`](https://gbfs.mex.lyftbikes.com/gbfs/es/station_information.json)
* **Estado en Tiempo Real (Bicicletas y Anclajes Disponibles cada 60 s):** [`https://gbfs.mex.lyftbikes.com/gbfs/es/station_status.json`](https://gbfs.mex.lyftbikes.com/gbfs/es/station_status.json)

---

### 1.6 PROFECO (Procuraduría Federal del Consumidor)
* **Portal de Datos Abiertos PROFECO:** [`https://datos.profeco.gob.mx/`](https://datos.profeco.gob.mx/) *(Monitoreado en vivo; en mantenimiento).*
* **Programa Quién es Quién en los Precios (QQP):** [`https://www.gob.mx/profeco/acciones-y-programas/quien-es-quien-en-los-precios`](https://www.gob.mx/profeco/acciones-y-programas/quien-es-quien-en-los-precios)

---

### 1.7 Instituto Nacional de Estadística y Geografía (INEGI)
* **Censos Económicos 2024 (Resultados Oportunos CDMX):** [`https://www.inegi.org.mx/programas/ce/2024/`](https://www.inegi.org.mx/programas/ce/2024/)
* **Marco Geoestadístico Nacional (Polígonos de Alcaldías y Municipios Conurbados):** [`https://www.inegi.org.mx/temas/mg/`](https://www.inegi.org.mx/temas/mg/)
* **Directorio Estadístico Nacional de Unidades Económicas (DENUE - SCIAN 46):** [`https://www.inegi.org.mx/app/mapa/denue/`](https://www.inegi.org.mx/app/mapa/denue/)
* **Encuesta Nacional de Ocupación y Empleo (ENOE - Informalidad Laboral):** [`https://www.inegi.org.mx/programas/enoe/15ymas/`](https://www.inegi.org.mx/programas/enoe/15ymas/)
* **Encuesta Nacional de Inclusión Financiera (ENIF 2024 - Medios de Pago y Efectivo):** [`https://www.inegi.org.mx/programas/enif/2024/`](https://www.inegi.org.mx/programas/enif/2024/)

---

### 1.8 Servicios Cartográficos, Meteorológicos y de Ruteo Abiertos
* **Project OSRM (Ruteo Peatonal y Ciclista Ligero para CDMX):** [`https://router.project-osrm.org/route/v1/walking/`](https://router.project-osrm.org/route/v1/walking/)
* **OpenStreetMap Nominatim (Geocodificación Directa e Inversa de Colonias y Calles):** [`https://nominatim.openstreetmap.org/search`](https://nominatim.openstreetmap.org/search)
* **Open-Meteo API (Meteorología y Clima Hiperlocal en Tiempo Real):** [`https://api.open-meteo.com/v1/forecast`](https://api.open-meteo.com/v1/forecast)

---

### 1.9 Google Maps Places, Reseñas Ciudadanas y Galerías de Fotografías
* **Google Maps Places Web Platform:** [`https://maps.google.com/`](https://maps.google.com/)
* **Consultas directas por Feature ID y Place ID WGS84:** `https://maps.google.com/maps?q=place_id:{place_id}&hl=es&dg=es5`
* **Endpoint de Previsualización y Metadatos de Fichas:** `https://www.google.com/maps/preview/place?authuser=0&hl=es&gl=mx&pb=...`
* **Servidor de Fotografías de Alta Calidad de Usuarios:** `https://lh3.googleusercontent.com/` (enlaces públicos directos optimizados a resolución `=w800-h600-k-no`).
* **Extracción:** 512 `place_id` únicos auditados para los 1,367 tianguis de la CDMX, obteniendo ratings, conteos de opiniones, comentarios de compradores, temas frecuentes ("ropa de paca", "carnitas", "barbacoa", "chácharas", "precios") y fotografías reales sin almacenamiento de datos personales.

---

## 2. Inventario de Datasets Descargados y Procesados Localmente

Todos los datasets base han sido descargados en `data/raw/` y normalizados bajo el estándar WGS84 en `data/processed/`.

### 2.1 Comercio Popular y Barrial

| Nombre del Dataset | Dependencia / Fuente | Formatos | Registros | Cobertura / Contenido | Ubicación Local |
|---|---|:---:|:---:|---|---|
| **Tianguis de la Ciudad de México** | SEDECO CDMX (Portal Datos Abiertos) | CSV, GeoJSON | 1,367 tianguis | Alcaldía, colonia, tramo de calle (`ubicacion`), días de instalación (lunes a domingo), horarios y coordenadas WGS84. | [`data/raw/tianguis.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/tianguis.csv)<br>[`data/processed/tianguis_limpio.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/tianguis_limpio.json) |
| **Mercados Públicos de la CDMX** | SEDECO CDMX (Portal Datos Abiertos) | CSV, GeoJSON | 329 mercados | Nombre oficial, número de mercado, total de locales, superficie en m², año de inauguración, estatus de inmueble protegido y coordenadas. | [`data/raw/mercados_publicos.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/mercados_publicos.csv)<br>[`data/processed/mercados_publicos_limpio.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/mercados_publicos_limpio.json) |
| **Mercados Sobre Ruedas (MSR)** | SEDECO CDMX (Portal Datos Abiertos) | CSV, GeoJSON | 51 paradas (13 rutas) | Código de ruta (`RUTA 1` a `10`, `6-A/B`, `8-A/B`, `MINI RUTA`), día de operación semanal, número de oferentes, dirección y coordenadas. | [`data/raw/mercados_sobre_ruedas.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/mercados_sobre_ruedas.csv)<br>[`data/processed/msr_rutas_itinerantes.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/msr_rutas_itinerantes.json) |
| **Concentraciones de Comerciantes** | SEDECO CDMX (Portal Datos Abiertos) | CSV, GeoJSON | 224 concentraciones | Puntos fijos semifijos en vía pública con registro SEDECO. Coordenadas UTM proyectadas convertidas a WGS84 decimal. | [`data/raw/concentraciones_comerciantes.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/concentraciones_comerciantes.csv)<br>[`data/processed/concentraciones_comerciantes_limpio.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/concentraciones_comerciantes_limpio.json) |
| **Padrón Mercomuna CDMX (Muestra Activa)** | Secretaría de Bienestar / SAPCI | Web Scraped (AJAX) | 250 comercios muestra | Nombre del establecimiento, dirección, colonia, alcaldía y giro comercial registrado para recepción de vales Mercomuna. | [`data/raw/mercomuna_comercios_muestra.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/mercomuna_comercios_muestra.csv)<br>[`data/processed/mercomuna_comercios_limpio.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/mercomuna_comercios_limpio.json) |
| **Apoyos Emergentes a Comercio en Vía Pública** | Secretaría de Gobierno / SEDECO CDMX | CSV | 2,673 beneficiarios | Estatus de dispersión económica a comerciantes de alimentos preparados y comercio ambulante en las 16 alcaldías. | [`data/raw/apoyos_emergentes_comercio.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/apoyos_emergentes_comercio.csv)<br>[`data/processed/apoyos_emergentes_limpio.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/apoyos_emergentes_limpio.json) |
| **Programa de Microcréditos FONDESO** | Fondo para el Desarrollo Social (FONDESO) | Excel (XLSX) | 86,402 solicitudes | Folio, alcaldía, colonia, giro textual detallado, fecha de solicitud y estatus de aprobación/rechazo. | [`data/raw/fondeso_solicitudes.xlsx`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/fondeso_solicitudes.xlsx) |
| **Directorio Maestro Unificado de Comercio Popular** | Compilación propia normalizada | JSON, CSV | 1,971 establecimientos | Esquema homogéneo de 26 campos enriquecido con categorías, subgiros, Canasta Básica Oficial y Mercomuna. | [`data/processed/directorio_comercio_popular.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/directorio_comercio_popular.json)<br>[`data/processed/directorio_comercio_popular.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/directorio_comercio_popular.csv) |
| **Vocabulario Jerárquico de Compras Populares** | Compilación taxonómica Chilangatón 2026 | JSON, CSV | 159 términos | Vocabulario de productos de consumo popular (Nivel Micro) con mapeo directo a los 67 subgiros, 9 macrocategorías y sinónimos barriales. | [`data/catalog/vocabulario_compras.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/vocabulario_compras.json)<br>[`data/processed/vocabulario_compras.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/vocabulario_compras.csv) |
| **Centros de Abasto Mayoristas CDMX** | Compilación estratégica | JSON, CSV | 8 nodos clave | CEDA Iztapalapa, Merced Nave Mayor/Menor, Sonora, Jamaica, La Nueva Viga, La Viga y San Juan Pugibet con coordenadas y giros. | [`data/processed/centros_abasto_mayoristas.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/centros_abasto_mayoristas.json)<br>[`data/processed/centros_abasto_mayoristas.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/centros_abasto_mayoristas.csv) |
| **Reseñas y Fotografías de Tianguis en Google Maps** | Web Crawling y Places API (Chilangatón 2026 - Tarea 5.5) | JSON, CSV | 1,367 tianguis (512 fichas auditadas) | Ratings promedio, opiniones de compradores, citas destacadas, temas frecuentes y URLs directas de fotografías reales de tianguis. | [`data/processed/tianguis_reviews.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/tianguis_reviews.json)<br>[`data/processed/tianguis_reviews.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/tianguis_reviews.csv) |
| **Especialidades y Vocaciones Comunitarias NLP** | Minería de Texto NLP & Vocabulario Barrial (Tarea 5.5) | JSON, CSV | 1,367 tianguis clasificados | Vocación comercial (Abasto Fresco, Antojitos, Ropa de Paca, Herramientas), redacción descriptiva humana, top 3-6 productos elogiados y fotos. | [`data/processed/tianguis_especialidades_nlp.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/tianguis_especialidades_nlp.json)<br>[`data/processed/tianguis_especialidades_nlp.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/tianguis_especialidades_nlp.csv) |

---

### 2.2 Cartografía y División Territorial

| Nombre | Fuente | Formato | Registros | Descripción | Ubicación Local |
|---|---|:---:|:---:|---|---|
| **Alcaldías de la CDMX** | Marco Geoestadístico INEGI / ADIP | GeoJSON | 16 polígonos | Polígonos oficiales de las 16 demarcaciones territoriales con claves INEGI (`CVEGEO`). | [`data/raw/cartografia/alcaldias.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/cartografia/alcaldias.geojson) |
| **Colonias de la CDMX** | IECM / ADIP | GeoJSON | 1,814 polígonos | Delimitación oficial de colonias, pueblos y barrios originarios para agregación barrial. | [`data/raw/cartografia/colonias.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/cartografia/colonias.geojson) |
| **Municipios Conurbados (ZMVM)** | Marco Geoestadístico INEGI | GeoJSON | 60 municipios | 59 municipios del Estado de México y 1 de Hidalgo conurbados con la capital para análisis de flujos metropolitanos. | [`data/raw/cartografia/zmvm_edomex.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw/cartografia/zmvm_edomex.geojson) |

---

### 2.3 Movilidad Integrada (Red MI) y Transporte Concesionado

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

## 3. APIs, Servicios Web y Geoportales en Vivo

Catálogo técnico detallado disponible en: [`data/docs/apis_cdmx.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/docs/apis_cdmx.md).

### 3.1 Portal de Datos Abiertos CDMX (CKAN API v3)
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

### 3.2 GeoServer WFS Oficial SIG CDMX (ADIP)
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

### 3.3 Movilidad en Tiempo Real: Ecobici GBFS v2.3
- **Base URL:** `https://gbfs.mex.lyftbikes.com/gbfs/es/`
- **Refresco:** Cada 60 segundos (en vivo).
- **Endpoints:**
  - `GET /station_information.json` $\rightarrow$ Metadatos fijos de 677 estaciones (nombre, capacidad y coordenadas).
  - `GET /station_status.json` $\rightarrow$ Disponibilidad en tiempo real: `num_bikes_available`, `num_ebikes_available`, `num_docks_available`, `is_renting`.

### 3.4 Meteorología y Resiliencia Climática Hiperlocal (Open-Meteo)
- **Endpoint:** `https://api.open-meteo.com/v1/forecast`
- **Parámetros:** `latitude=19.4326&longitude=-99.1332&hourly=temperature_2m,precipitation_probability,precipitation,wind_gusts_10m,uv_index&timezone=America%2FMexico_City`
- **Utilidad:** Detección predictiva de lluvia torrencial o viento para alerta temprana en tianguis semanales.

### 3.5 Ruteo Peatonal y Multimodal (OSRM & OpenStreetMap)
- **OSRM Router:** `https://router.project-osrm.org/route/v1/walking/{lng1},{lat1};{lng2},{lat2}?overview=full&geometries=geojson`
- **Nominatim Geocoding:** `https://nominatim.openstreetmap.org/search?q={direccion},+CDMX&format=json`

---

## 4. Bibliografía Académica y Estudios Socioterritoriales

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

## 5. Crítica al Solucionismo y Principios de Gobernanza de Datos

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

## 6. Marco Normativo, Gacetas y Políticas Públicas

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
7. **Gaceta Oficial de la Ciudad de México — Tarifas de Transporte Concesionado (SEMOVI):**
   - Publicación del esquema tarifario oficial por distancia en microbuses y vagonetas ($6.00 hasta 5 km, $6.50 de 5 a 12 km, $7.50 más de 12 km; corredores $8.00 - $8.50) y recargo nocturno oficial de +20% (23:00 a 06:00 hrs).
8. **Gaceta del Gobierno del Estado de México — Tarifas del Servicio Público Concesionado (Secretaría de Movilidad GEM):**
   - Ajuste tarifario oficial para el transporte colectivo mexiquense (combis y microbuses): tarifa mínima de $14.00 MXN para los primeros 5 kilómetros y $0.25 MXN por cada kilómetro adicional, con impacto directo en rutas conurbadas hacia CETRAMs de la CDMX.
9. **Tarifas Oficiales Red de Movilidad Integrada (MI) CDMX:**
   - SEMOVI CDMX: Metro ($5.00), Metrobús ($6.00), Cablebús ($7.00), Trolebús ($4.00 general / $7.00 Elevado), Tren Ligero ($3.00), RTP ($2.00 ordinario / $4.00 expreso / $5.00 Ecobús / $7.00 Nochebús). Gratuidad social universal para personas mayores de 60 años con INAPAM y personas con discapacidad.
10. **Secretaría de Infraestructura, Comunicaciones y Transportes (SICT) & Ferrocarriles Suburbanos:**
    - Esquema tarifario oficial del Ferrocarril Suburbano de la ZMVM: Viaje corto (0 a 12.89 km) en $10.50 MXN; Viaje largo (12.90 a 25.59 km) en $24.50 MXN. Costo plástico de tarjeta inteligente recargable: $16.00 MXN.

---

## 7. Investigación Periodística y Reportes Gremiales

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

## 8. Metodología de Desiertos de Alimentos, Seguridad Alimentaria y Geografía Urbana

1. **CONEVAL (Consejo Nacional de Evaluación de la Política de Desarrollo Social, 2022-2024):**
   - *«Medición multidimensional de la pobreza y acceso a la alimentación nutritiva y de calidad en México»*: Criterios metodológicos para evaluar la carencia por acceso a la alimentación en zonas urbanas y periurbanas. Enlace: [https://www.coneval.org.mx/](https://www.coneval.org.mx/)
2. **USDA Economic Research Service (ERS, 2012-2023):**
   - *«Food Access Research Atlas & Mapping Food Deserts in the United States»*: Definición estandarizada de buffers de caminabilidad (500m y 1,000m) e isócronas peatonales aplicadas al acceso a alimentos frescos. Enlace: [https://www.ers.usda.gov/data-products/food-access-research-atlas/](https://www.ers.usda.gov/data-products/food-access-research-atlas/)
3. **FAO (Organización de las Naciones Unidas para la Alimentación y la Agricultura, 2021):**
   - *«Sistemas alimentarios urbanos y comercio tradicional en América Latina»*: Documentación del rol de los tianguis, ferias libres y mercados municipales como amortiguadores inflacionarios y garantes de la diversidad dietética barrial frente a cadenas de autoservicio corporativo.
4. **INSP (Instituto Nacional de Salud Pública, 2022-2024):**
   - *«Encuesta Nacional de Salud y Nutrición (ENSANUT) - Resultados CDMX»*: Análisis de prevalencia de obesidad, hipertensión y diabetes tipo 2 cruzado con la proximidad a tiendas de conveniencia y entornos alimentarios no saludables (*food swamps*). Enlace: [https://ensanut.insp.mx/](https://ensanut.insp.mx/)
5. **Bitler, M. & Haider, S. (2011):**
   - *«An Economic View of Food Deserts in the United States»*, Journal of Policy Analysis and Management: Análisis de elasticidad de precios, costos de transporte y fricción espacial en la elección alimentaria de hogares vulnerables.
6. **Widener, M. J., Farber, S., Neutens, T., & Horner, M. W. (2013):**
   - *«Spatiotemporal accessibility to supermarkets using public transit, an interaction potential approach in space-time»*: Fundamento para modelar la accesibilidad alimentaria no como un fenómeno estático, sino dinámico según el día de la semana y el horario de operación de los mercados móviles.

---

## 9. Trazabilidad de Scripts y Entregables del Repositorio

| Directorio / Archivo | Tipo | Descripción y Componentes |
|---|:---:|---|
| [`data/raw/`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/raw) | Datasets Crudos | Archivos CSV, JSON, GeoJSON y Excel descargados directamente de portales abiertos gubernamentales. |
| [`data/processed/`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed) | Datasets Limpios | Datos estandarizados WGS84, horarios decimales, alcaldías canónicas y catálogo unificado (`directorio_comercio_popular.json`). |
| [`data/processed/desiertos_abasto_cdmx.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/desiertos_abasto_cdmx.json) / [`.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/desiertos_abasto_cdmx.csv) | Datasets Derivados | Análisis micro-territorial de las 1,543 colonias de la CDMX: distancias a tianguis, tiempo de caminata, día crítico, distancias diarias y clasificación de abasto. |
| [`data/processed/cobertura_tianguis_alcaldias.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/cobertura_tianguis_alcaldias.json) / [`.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/cobertura_tianguis_alcaldias.csv) | Datasets Derivados | Matriz consolidada de las 16 alcaldías con porcentajes de cobertura a 500m y 1,000m, ISDAP (0-100), densidad de oferentes y Top 5 colonias prioritarias. |
| [`data/catalog/`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog) | Taxonomía y Tarifas | 9 Macro-Categorías, 67 Subgiros normalizados, `giro_classifier.py`, `vocabulario_compras.json` y catálogo maestro de tarifas y horarios (`tarifas_horarios_transporte.json` / `.csv`). |
| [`data/docs/apis_cdmx.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/docs/apis_cdmx.md) | Catálogo de APIs | Guía técnica y pruebas de conectividad en vivo de CKAN Datastore, GeoServer WFS SIG CDMX, Ecobici GBFS y OSRM. |
| [`docs/TARIFAS_Y_HORARIOS_TRANSPORTE.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/docs/TARIFAS_Y_HORARIOS_TRANSPORTE.md) | Documentación Tarifaria | Estudio exhaustivo de la asimetría metropolitana CDMX vs Edomex, fórmulas de cobro por distancia, recargos nocturnos e impacto en comerciantes madrugadores. |
| [`docs/RUTEO_MULTIMODAL_CDMX.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/docs/RUTEO_MULTIMODAL_CDMX.md) | Documentación Técnica | Especificación del motor de ruteo multimodal (Metro + Metrobús + Trolebús + RTP + caminata hacia tianguis). |
| [`docs/CIERRES_VIALES_TIANGUIS.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/docs/CIERRES_VIALES_TIANGUIS.md) | Documentación Espacial | Modelado geométrico de cortes viales dinámicos, afectación a transporte público e indexador acimutal de calles ocupadas. |
| [`docs/DESIERTOS_ABASTO_CDMX.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/docs/DESIERTOS_ABASTO_CDMX.md) | Política Pública | Reporte de política pública para SEDECO y SECTEI sobre equidad alimentaria barrial, penetración de cadenas privadas (Oxxo) y 4 propuestas estratégicas. |
| [`scripts/schedule_pricing_engine.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/schedule_pricing_engine.py) | Motor de Horarios y Precios | Motor CLI y API Python para consulta dinámica de transporte abierto/cerrado por hora y cotización exacta tramo por tramo. |
| [`scripts/analyze_food_deserts.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/analyze_food_deserts.py) | Motor de Desiertos de Abasto | Script espacial reproducible para buffers peatonales (500m/1km), cruce dinámico por día de la semana, cálculo de ISDAP y exportación dual (JSON/CSV). |
| [`scripts/governance_engine.js`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/governance_engine.js) | Motor de Gobernanza y Auditoría Barrial | Módulo JavaScript modular (UMD) para votación local-first (Principios CARE), Proof of Location (≤300m = +3 pts), cooldown anti-spam (24h) y estados epistémicos (CONFIRMADO, PROPUESTO, EN_DISPUTA). |
| [`scripts/integrate_governance.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/integrate_governance.py) | Compilador de Gobernanza en Visor | Script automatizado para integrar estilos, componentes UI, marcadores y handlers del motor de gobernanza en `scripts/build_revamped_map.py`. |
| [`scripts/generate_admin_dashboard_data.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/generate_admin_dashboard_data.py) | Generador de Analítica de Gobernanza | Script reproducible para modelado y agregación de los 4 ejes: ranking de afluencia, categorías de consumo, volumen horario/semanal y 10 deciles generacionales. |
| [`data/processed/dashboard_analytics_data.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/dashboard_analytics_data.json) / [`.js`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/dashboard_analytics_data.js) | Datasets Analíticos | Bundle consolidado en formato dual (JSON y JavaScript directo libre de CORS) con matrices de los 4 ejes analíticos y KPIs ejecutivos. |
| [`dashboard_gobernanza_cdmx.html`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/dashboard_gobernanza_cdmx.html) | Tablero de Inteligencia Estratégica | Interfaz ejecutiva interactiva para tomadores de decisiones (SEDECO/SECTEI/SAF) con Chart.js, ranking filtrable, 4 ejes analíticos y enlace al visor. |
| [`TODO_PROYECTO.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/TODO_PROYECTO.md) | Backlog del Proyecto | Lista estructurada de 8 módulos de trabajo con dependencias, dificultad y estatus de ejecución en tiempo real. |
| [`TODO_PROYECTO.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/TODO_PROYECTO.md) | Backlog del Proyecto | Lista estructurada de 8 módulos de trabajo con dependencias, dificultad y estatus de ejecución en tiempo real. |
| [`mapa_comercio_movilidad_cdmx.html`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/mapa_comercio_movilidad_cdmx.html) | Visor Web Integrado | Prototipo cartográfico interactivo que combina la capa de comercio popular con la Red de Movilidad Integrada. |
| [`scripts/`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts) | Pipelines ETL y Build | Scripts en Python para descarga, compilación del grafo de ruteo, normalización de datos y generación del visor web. |
