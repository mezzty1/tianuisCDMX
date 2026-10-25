# Datasets Procesados y Normalizados del Comercio Popular y Barrial de la CDMX

Este directorio contiene los datasets limpios, estandarizados y estructurados listos para ser consumidos por la aplicación web, motores de búsqueda espacial, mapas interactivos y modelos de analítica territorial y logística urbana.

---

## 1. Resumen de Archivos Generados

| Archivo Base | Formatos | Registros | Coordenadas Válidas | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| **`directorio_comercio_popular`** | `.json` / `.csv` | **1,971** | **1,914 (97.1%)** | **Catálogo unificado maestro** de abasto popular: mercados públicos, tianguis, mercados sobre ruedas y concentraciones, con clasificación tipológica (`FIJO` vs. `MOVIL`), horarios numéricos, 7 banderas por día, **categorías, subgiros, Canasta Básica y Mercomuna**. |
| **`vocabulario_compras`** | `.json` / `.csv` | **460** | N/A (Vocabulario) | **Índice de Compras Populares (Nivel Micro)**: catálogo exhaustivo de más de 460 términos de consumo barrial en tianguis y mercados (frutas, carnicería, mariscos, barbacoa, paca, herramientas, chácharas) mapeados a 67 subgiros y 9 macrocategorías. |
| **`tianguis_reviews`** | `.json` / `.csv` | **1,367** | **1,365 (99.8%)** | **Dataset de Reseñas y Fotografías de Google Maps (Tarea 5.5 - Fase 1)**: calificaciones promedio, número total de opiniones, reseñas de compradores, citas destacadas, temas frecuentes y enlaces directos a fotos reales de puestos (`lh3.googleusercontent.com`). |
| **`tianguis_especialidades_nlp`** | `.json` / `.csv` | **1,367** | **1,365 (99.8%)** | **Minería de Texto y Vocaciones Comunitarias NLP (Tarea 5.5 - Fase 2)**: clasificación en las 4 macrovocaciones (Abasto Fresco, Antojitos, Ropa de Paca, Herramientas), redacción fluida de especialidad comunitaria y ranking de los 3 a 6 artículos más elogiados. |
| **`tianguis_map_data`** | `.json` / `.js` | **1,367** | **1,365 (99.8%)** | **Bundle Especializado para Mapa Minimalista (Tareas 5.5 y 7.7)**: los 1,367 tianguis semanales enriquecidos con estatus en vivo, nombres populares, vocación, especialidad comunitaria NLP, top artículos más elogiados, fotografías de Google Maps, estación de Metro/Metrobús más cercana a pie y cartografía CDMX/ZMVM. |
| **`dashboard_analytics_data`** | `.json` / `.js` | **1,367 / 4 Ejes** | N/A (Analítico) | **Dataset Analítico del Tablero de Inteligencia Estratégica (Tarea 7.9)**: ranking de los tianguis más visitados con afluencia estimada y validaciones territoriales (Proof of Location), 6 macrocategorías de consumo popular con tickets y medios de pago, curva semanal y horaria de interacciones (06-20h), y matriz demográfica de 10 deciles por edad (D1-D10). |
| **`msr_rutas_itinerantes`** | `.json` / `.csv` | **13** | N/A (Agrupado) | **Trazabilidad de Rutas de Mercados Sobre Ruedas (MSR)**: itinerarios semanales ordenados de Lunes a Domingo, colonias, alcaldías y oferentes. |
| **`msr_rutas_paradas_itinerantes`**| `.json` / `.csv` | **51** | **51 (100.0%)** | Paradas semanales de MSR en formato tabular plano GIS-ready con secuencia temporal, alcaldía, coordenadas y oferentes. |
| **`centros_abasto_mayoristas`** | `.json` / `.csv` | **8** | **8 (100.0%)** | **Catálogo de Nodos de Abasto Mayoristas y Semimayoristas**: CEDA Iztapalapa, La Merced (Nave Mayor y Menor), Sonora, Jamaica, La Nueva Viga, La Viga y San Juan Pugibet. |
| **`tianguis_limpio`** | `.json` / `.csv` | 1,367 | 1,365 (99.8%) | Tianguis semanales autorizados por SEDECO con días, horarios numéricos, oferentes estimados y coordenadas. |
| **`mercados_publicos_limpio`** | `.json` / `.csv` | 329 | 329 (100.0%) | Mercados públicos tradicionales y especializados con número oficial, locales, año y superficie. |
| **`mercados_sobre_ruedas_limpio`** | `.json` / `.csv` | 51 | 51 (100.0%) | Registros individuales de MSR con ruta, día de operación, oferentes y ubicación. |
| **`concentraciones_comerciantes_limpio`** | `.json` / `.csv` | 224 | 169 (75.4%) | Concentraciones de comerciantes en vía pública, con proyección UTM 14N convertida a WGS84. |
| **`mercomuna_comercios_limpio`** | `.json` / `.csv` | 250 | N/A (Padrón) | Muestra de tienditas y comercios barriales (abarrotes, carnicerías, papelerías) afiliados a MERCOMUNA. |
| **`apoyos_emergentes_limpio`** | `.json` / `.csv` | 2,673 | N/A (Padrón) | Padrón de microcomerciantes beneficiarios de apoyos emergentes CDMX, con status de dispersión, edad y género. |
| **`cierres_viales_tianguis`** | `.geojson` | 1,367 | 1,365 (99.8%) | **Capa Vectorial de Afectación Vial**: tramos de calle cerrados (`LineString`) por tianguis con entrecalles, longitud, ancho, tipo de afectación y desvíos sugeridos. |
| **`cierres_viales_por_dia`** | `.json` | 7 días | N/A (Consolidado) | **Índice de Cierres Viales por Día de la Semana**: consolidación de LUNES a DOMINGO con 330 km de vialidades afectadas y desglose por alcaldía para el frontend. |
| **`desiertos_abasto_cdmx`** | `.json` / `.csv` | **1,543** | **1,543 (100.0%)** | **Detección de Desiertos de Abasto Popular por Colonia (Tarea 6.3)**: análisis isócrono peatonal (500m/1km) de todas las colonias de la CDMX, distancias mínimas y diarias (Lunes a Domingo), tiempo de caminata, tianguis más cercano, día crítico e índice de vulnerabilidad de abasto. |
| **`cobertura_tianguis_alcaldias`** | `.json` / `.csv` | **16** | **16 (100.0%)** | **Matriz Consolidada de Cobertura y Desiertos por Alcaldía (Tarea 6.3)**: superficie total, cobertura de buffers a 500m y 1,000m, porcentaje de desierto territorial, número de tianguis y oferentes, cobertura diaria (L-D), día crítico, ISDAP (0-100) y Top 5 colonias prioritarias. |
| **`normalize_all.py`** | `.py` | Script | N/A | Pipeline automatizado y reproducible que genera todos los archivos procesados desde `data/raw/`. |

---

## 2. Reglas de Limpieza y Estandarización Aplicadas

### 2.1 Clasificación Tipológica (Fijo vs. Móvil)
Se incorporó el atributo estándar `tipo_comercio` para distinguir de forma binaria la naturaleza física del comercio:
- **`FIJO` (553 espacios)**: 
  - `Mercado Público` (329 inmuebles permanentes catalogados por SEDECO).
  - `Concentración` (224 concentraciones comerciales semifijas en vía pública).
- **`MOVIL` (1,418 espacios)**: 
  - `Tianguis` (1,367 tianguis de periodicidad semanal).
  - `Mercado Sobre Ruedas` (51 paradas itinerantes con vehículos y estructuras desmontables).

### 2.2 Normalización de Horarios y Filtros Temporales ("Abierto Ahora")
- **Extracción Numérica**: A partir de cadenas de texto (ej. `"8:00 A 17:00 HORAS"`, `"07:00 A 19:00 HORAS"`, `"24 HORAS"`), se extrajeron:
  - `hora_apertura` (`float`): Hora en formato decimal (ej. `8.0` para las 8:00 hrs, `7.0` para las 7:00 hrs, `0.0` para 24 hrs).
  - `hora_cierre` (`float`): Hora en formato decimal (ej. `17.0` para las 17:00 hrs, `19.0` para las 19:00 hrs, `24.0` para 24 hrs).
  - `horario_estimado` (`boolean`): Bandera que indica si el horario proviene explícitamente de la fuente oficial (`false`) o si fue asignado por default estándar comercial (`true`).
- **Banderas Booleanas por Día**: Se integraron 7 columnas/campos booleanos (`lunes`, `martes`, `miercoles`, `jueves`, `viernes`, `sabado`, `domingo`) en el directorio maestro.
- **Función de Consulta Dinámica (`esta_abierto`)**:
  Permite validar en tiempo real si un espacio comercial está en operación:
  ```python
  from normalize_all import esta_abierto

  # Consulta con día y hora explícitos
  abierto = esta_abierto(registro, dia='LUNES', hora=11.5)  # 11:30 hrs

  # Consulta automática con la fecha/hora actual del sistema
  abierto_ahora = esta_abierto(registro)
  ```

### 2.3 Estandarización Canónica de Alcaldías
Se uniformaron todas las variantes de nombres (con acentos, sin acentos, abreviaturas tipo `M.Contreras`, `G.A. Madero`, `Del. Cuauhtémoc`) a las **16 alcaldías oficiales** de la Ciudad de México en mayúsculas sin acentos:
`ALVARO OBREGON`, `AZCAPOTZALCO`, `BENITO JUAREZ`, `COYOACAN`, `CUAJIMALPA DE MORELOS`, `CUAUHTEMOC`, `GUSTAVO A. MADERO`, `IZTACALCO`, `IZTAPALAPA`, `LA MAGDALENA CONTRERAS`, `MIGUEL HIDALGO`, `MILPA ALTA`, `TLAHUAC`, `TLALPAN`, `VENUSTIANO CARRANZA`, `XOCHIMILCO`.

### 2.4 Validación y Proyección de Coordenadas Geográficas
- **Delimitación WGS84 CDMX**: Se aplicó un polígono delimitador geográfico para la CDMX ($19.04^\circ \text{N} \le \text{Lat} \le 19.59^\circ \text{N}$, $-99.37^\circ \text{W} \le \text{Lng} \le -98.94^\circ \text{W}$).
- **Conversión UTM Zona 14N**: El dataset original de `concentraciones_comerciantes` venía en coordenadas proyectadas métricas UTM Zona 14N (`COORD_X` $\approx 480,000$, `COORD_Y` $\approx 2,140,000$). Se implementó la transformación matemática geodésica exacta basada en el elipsoide WGS84 para proyectarlas a grados decimales WGS84 (latitud y longitud).
- **Manejo de Coordenadas Nulas / Outliers**:
  - 55 registros en concentraciones que tenían `(0.0, 0.0)` en UTM fueron identificados y mapeados a `lat: null`, `lng: null`, con `coordenadas_validas: false`.
  - 2 registros en tianguis con coordenadas corruptas (`lat=4.42` correspondiente a Colombia y `lat=0.0` con estatus "NO SE INSTALA") fueron corregidos a `null` con `coordenadas_validas: false`.

### 2.5 Asignación de Identificadores Únicos Prefijados
Cada registro posee un ID legible y único para claves primarias en bases de datos relacionales o NoSQL:
- Tianguis: `TIANG-0001` a `TIANG-1367`
- Mercados Públicos: `MERC-0001` a `MERC-0329`
- Mercados Sobre Ruedas: `MSR-0001` a `MSR-0051`
- Concentraciones: `CONC-0001` a `CONC-0224`
- Mercomuna: `MERCOM-0001` a `MERCOM-0250`
- Apoyos Emergentes: `APOYO-0001` a `APOYO-2673`
- Rutas MSR: `RUTA-MSR-01` a `RUTA-MSR-10`, `RUTA-MSR-06A/B`, `RUTA-MSR-08A/B`, `RUTA-MSR-MINI`
- Centros Mayoristas: `ABASTO-CEDA`, `ABASTO-MERCED-MAYOR`, `ABASTO-MERCED-MENOR`, `ABASTO-SONORA`, `ABASTO-JAMAICA`, `ABASTO-NUEVA-VIGA`, `ABASTO-LA-VIGA`, `ABASTO-SAN-JUAN-PUGIBET`

### 2.6 Modelo de Detección de Desiertos de Abasto Popular y Fresco (Tarea 6.3)
Generado por [`scripts/analyze_food_deserts.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/analyze_food_deserts.py) con proyección cartográfica métrica en **UTM Zona 14N (EPSG:32614)**:
- **Buffers Isócronos Peatonales**:
  * `500 metros` ($\le 6.7$ min de caminata): *Abasto Pleno* (1,033 colonias, 66.9%).
  * `1,000 metros` ($6.7 - 13.3$ min de caminata): *Abasto Moderado* (406 colonias, 26.3%).
  * `> 1,000 metros` ($> 13.3$ min de caminata): *Desierto de Abasto Popular Fresco* (104 colonias, 6.7%).
- **Dinámica Temporal Diaria (Lunes a Domingo)**: Detección del día crítico semanal (el viernes es el día con mayor déficit, alcanzando el 51.6% de colonias sin abasto cercano).
- **Índice de Severidad de Desierto de Abasto Popular (ISDAP, 0 a 100)**: Combina cobertura territorial desértica, porcentaje de colonias desérticas, déficit temporal promedio y penalización por baja densidad de oferentes. Permite priorizar la asignación de nuevas paradas de Mercados Sobre Ruedas en alcaldías críticas como Milpa Alta (72.0), Cuajimalpa (61.8), Xochimilco (54.3) y Tlalpan (53.7).

---

## 3. Esquema del Catálogo Unificado (`directorio_comercio_popular`)

El archivo `directorio_comercio_popular.json` (y su versión `.csv`) unifica todos los espacios de comercio popular en una sola estructura homogénea de 26 atributos:

```json
{
  "id": "MERC-0001",
  "nombre": "MERCADO AZCAPOTZALCO",
  "tipo_espacio": "Mercado Público",
  "tipo_comercio": "FIJO",
  "alcaldia": "AZCAPOTZALCO",
  "colonia": "CENTRO DE AZCAPOTZALCO",
  "direccion": "AV. AZCAPOTZALCO ENTRE ESPERANZA Y RAYON",
  "dias_operacion": "LUNES A DOMINGO",
  "dias_operacion_lista": ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"],
  "horario": "07:00 A 19:00 HORAS",
  "hora_apertura": 7.0,
  "hora_cierre": 19.0,
  "horario_estimado": false,
  "lat": 19.482872,
  "lng": -99.185439,
  "coordenadas_validas": true,
  "num_locales_oferentes": 546,
  "giro": "ABASTO TRADICIONAL Y MIXTO",
  "fuente_original": "SEDECO - Mercados Públicos",
  "lunes": true,
  "martes": true,
  "miercoles": true,
  "jueves": true,
  "viernes": true,
  "sabado": true,
  "domingo": true
}
```

---

## 4. Trazabilidad de Rutas de Mercados Sobre Ruedas (`msr_rutas_itinerantes`)

El dataset `msr_rutas_itinerantes.json` / `.csv` agrupa y ordena cronológicamente el circuito semanal de las 13 rutas de Mercados Sobre Ruedas de la capital:

| ID Ruta | Nombre Ruta | Paradas Semanales | Días Activos | Alcaldías Recorridas |
| :--- | :--- | :---: | :--- | :--- |
| `RUTA-MSR-01` | RUTA 1 | 6 | LUN, MAR, MIE, VIE, SAB, DOM | Álvaro Obregón, Coyoacán, GAM, Iztacalco, Miguel Hidalgo |
| `RUTA-MSR-02` | RUTA 2 | 3 | JUE, SAB, DOM | Álvaro Obregón, Azcapotzalco, Miguel Hidalgo |
| `RUTA-MSR-03` | RUTA 3 | 5 | MAR, MIE, JUE, VIE, DOM | Benito Juárez, Cuauhtémoc, GAM, Tlalpan |
| `RUTA-MSR-04` | RUTA 4 | 6 | LUN, MAR, MIE, JUE, VIE, DOM | Álvaro Obregón, Azcapotzalco, Benito Juárez, Tlalpan |
| `RUTA-MSR-05` | RUTA 5 | 6 | MAR, MIE, JUE, VIE, SAB, DOM | Álvaro Obregón, GAM, Iztapalapa, Miguel Hidalgo, Tláhuac |
| `RUTA-MSR-06A` | RUTA 6-A | 6 | LUN, MAR, JUE, VIE, SAB, DOM | Álvaro Obregón, Coyoacán, GAM, Iztacalco, Miguel Hidalgo |
| `RUTA-MSR-06B` | RUTA 6-B | 1 | DOM | Cuauhtémoc (Doctores) |
| `RUTA-MSR-07` | RUTA 7 | 6 | MAR, MIE, JUE, VIE, SAB, DOM | Álvaro Obregón, GAM, Iztacalco, Iztapalapa, La Magdalena Contreras |
| `RUTA-MSR-08A` | RUTA 8-A | 6 | LUN, MAR, MIE, JUE, SAB, DOM | Álvaro Obregón, Benito Juárez, Coyoacán, Cuauhtémoc, Iztapalapa, Venustiano Carranza |
| `RUTA-MSR-08B` | RUTA 8-B | 1 | DOM | Cuauhtémoc (San Rafael) |
| `RUTA-MSR-09` | RUTA 9 | 3 | LUN, VIE, SAB | Gustavo A. Madero, Iztapalapa |
| `RUTA-MSR-10` | RUTA 10 | 1 | MIE | Azcapotzalco (El Rosario) |
| `RUTA-MSR-MINI`| MINI RUTA | 1 | MIE | Cuauhtémoc (Roma) |

Para cada ruta, el JSON incluye la lista estructurada `paradas` con `orden_parada_semana`, `dia`, `orden_dia` (1=LUN a 7=DOM), coordenadas WGS84 exactas, oferentes y horario.

---

## 5. Nodos de Abasto Mayoristas (`centros_abasto_mayoristas`)

El dataset `centros_abasto_mayoristas.json` / `.csv` cataloga los 8 polos clave de distribución mayorista y semimayorista que surten a los tianguis y mercados públicos de la ZMVM:

1. **Central de Abasto de la CDMX (CEDA)** (`ABASTO-CEDA`): 327 hectáreas en Iztapalapa; principal polo de frutas, legumbres, hortalizas, víveres y canasta básica. Operación 24 hrs.
2. **Mercado de La Merced - Nave Mayor** (`ABASTO-MERCED-MAYOR`): Histórico corazón comercial mayorista de hortalizas, frutas y chiles secos (Venustiano Carranza).
3. **Mercado de La Merced - Nave Menor** (`ABASTO-MERCED-MENOR`): Polo mayorista de cárnicos, embutidos y derivados lácteos (Venustiano Carranza).
4. **Mercado de Sonora** (`ABASTO-SONORA`): Epicentro de herbolaria, medicina tradicional, plantas vivas y alfarería artesanal (Venustiano Carranza).
5. **Mercado de Jamaica** (`ABASTO-JAMAICA`): Gran centro de distribución mayorista de floricultura, follaje y plantas de ornato, con operación continua 24 hrs (Venustiano Carranza).
6. **Mercado de La Nueva Viga** (`ABASTO-NUEVA-VIGA`): Segundo mercado de pescados y mariscos más grande del mundo (Iztapalapa, colindante con CEDA).
7. **Mercado de La Viga (Histórico)** (`ABASTO-LA-VIGA`): Tradicional polo semimayorista y minorista de productos del mar (Cuauhtémoc).
8. **Mercado de San Juan Pugibet** (`ABASTO-SAN-JUAN-PUGIBET`): Distribuidor semimayorista de alimentos gourmet, cárnicos exóticos y productos importados (Cuauhtémoc).

Cada registro incorpora sus coordenadas WGS84 validadas, horario de operación, descripción logística y conectividad con la red de transporte (Metro, Metrobús y ejes viales).

---

## 6. Distribución Territorial en el Directorio Unificado

Distribución de los 1,971 espacios de abasto popular por Alcaldía y Tipología:

| Alcaldía | Mercados Públicos (Fijo) | Concentraciones (Fijo) | Tianguis (Móvil) | MSR (Móvil) | Total Fijo | Total Móvil | Total General |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **IZTAPALAPA** | 20 | 45 | 442 | 4 | 65 | 446 | **511** |
| **GUSTAVO A. MADERO** | 51 | 49 | 185 | 1 | 100 | 186 | **286** |
| **COYOACAN** | 22 | 8 | 141 | 3 | 30 | 144 | **174** |
| **TLALPAN** | 20 | 14 | 129 | 10 | 34 | 139 | **173** |
| **ALVARO OBREGON** | 16 | 12 | 134 | 2 | 28 | 136 | **164** |
| **CUAUHTEMOC** | 39 | 0 | 70 | 0 | 39 | 70 | **109** |
| **VENUSTIANO CARRANZA** | 42 | 6 | 34 | 0 | 48 | 34 | **82** |
| **BENITO JUAREZ** | 16 | 0 | 60 | 2 | 16 | 62 | **78** |
| **IZTACALCO** | 16 | 5 | 45 | 4 | 21 | 49 | **70** |
| **XOCHIMILCO** | 11 | 34 | 24 | 0 | 45 | 24 | **69** |
| **TLAHUAC** | 19 | 9 | 36 | 2 | 28 | 38 | **66** |
| **AZCAPOTZALCO** | 19 | 13 | 24 | 5 | 32 | 29 | **61** |
| **MIGUEL HIDALGO** | 18 | 0 | 32 | 7 | 18 | 39 | **57** |
| **LA MAGDALENA CONTRERAS** | 5 | 4 | 19 | 2 | 9 | 21 | **30** |
| **CUAJIMALPA DE MORELOS** | 5 | 6 | 10 | 0 | 11 | 10 | **21** |
| **MILPA ALTA** | 10 | 4 | 6 | 0 | 14 | 6 | **20** |
| **TOTAL** | **329** | **224** | **1,367** | **51** | **553** | **1,418** | **1,971** |

---

## 7. Reproducibilidad y Ejecución

Para regenerar todos los archivos procesados desde las fuentes crudas en `data/raw/`:

```bash
cd "data/processed"
python3 normalize_all.py
```

El script verificará las fuentes, calculará las conversiones geodésicas, validará las coordenadas, parseará los horarios numéricos, generará los catálogos de rutas MSR y centros mayoristas, y consolidará el directorio maestro en formatos JSON y CSV.
