# Cierres Viales Dinámicos por Tianguis en la Ciudad de México
## Análisis Espacial, Modelado de Red Vial y Afectación a la Movilidad (Chilangatón 2026)

---

## 1. Resumen Ejecutivo

En la Ciudad de México operan formalmente **1,367 tianguis y mercados sobre ruedas**, los cuales se instalan en días fijos de la semana sobre arroyos vehiculares, camellones y plazas públicas de las 16 alcaldías. Este sistema de abasto popular genera **más de 330 kilómetros lineales de calles ocupadas semanalmente**, movilizando a más de **239,000 oferentes** y abasteciendo a millones de capitalinos.

No obstante su relevancia económica y comunitaria, la instalación de los tianguis impone desafíos severos a la movilidad urbana:
- **Cierre total de calles secundarias y colectoras**: El 78% de las operaciones bloquea el flujo vehicular de acera a acera.
- **Reducción de carriles en vías primarias y avenidas**: El 17% de los tianguis ocupa laterales o carriles de extrema derecha en calzadas, ejes viales y bulevares.
- **Interferencia con transporte de superficie**: Afectación directa a rutas de RTP, corredores concesionados y trolebuses.

El presente módulo técnico (Módulo 4) implementa un **motor espacial y analítico reproducible** para la detección, delimitación geométrica y predicción de cortes viales en tiempo real. La solución integra un parser de direcciones urbanas, un modelo de dimensionamiento físico basado en puestos de venta, un indexador de acimut vial conectado a la red de transporte integrada y la generación de geometrías vectoriales (`LineString` y `Polygon`).

El código fuente principal se encuentra disponible en [`scripts/process_street_closures.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/process_street_closures.py), con datasets procesados listos para consumo en [`data/processed/cierres_viales_tianguis.geojson`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/cierres_viales_tianguis.geojson) y [`data/processed/cierres_viales_por_dia.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/processed/cierres_viales_por_dia.json).

---

## 2. Marco Normativo y Tipología de Espacios en CDMX

El funcionamiento de los tianguis se rige por el *Lineamiento para la Operación y Funcionamiento de los Tianguis en la Ciudad de México* (Gaceta Oficial de la CDMX) y la supervisión de la Secretaría de Desarrollo Económico (SEDECO) en coordinación con las 16 alcaldías.

### 2.1 Tipología de Afectación Vial
A partir del análisis de las 1,367 ubicaciones auditadas, se establecieron tres regímenes de ocupación vial:

1. **Cierre Total de Calle (78.2% de los casos)**:
   - Se presenta en calles residenciales, cerradas, callejones y vías terciarias.
   - El arroyo vehicular queda completamente clausurado al tránsito particular y de transporte público.
   - Requiere desvíos vehiculares perimetrales hacia calles paralelas adyacentes.

2. **Reducción de Carriles (17.1% de los casos)**:
   - Se ubica en avenidas principales, calzadas, ejes viales o laterales de vías rápidas (ej. Eje 5 Sur, Calzada Ermita Iztapalapa, Av. Texcoco, Av. Guelatao).
   - Ocupa de 1 a 2 carriles (generalmente el carril de extrema derecha o estacionamiento en cordón).
   - Provoca estrangulamientos viales ("cuellos de botella") y fricción vehicular severa.

3. **Ocupación de Camellón / Banqueta / Plaza (4.7% de los casos)**:
   - Se ubica sobre áreas peatonales, camellones centrales arbolados, bajopuentes o explanadas de deportivos y mercados (ej. Jardín del Arte en Sullivan, camellón de Av. 10 en Santa Cruz Meyehualco).
   - El arroyo vehicular permanece abierto pero con alta demanda peatonal y cruce constante de transeúntes, requiriendo pacificación del tránsito (velocidad máxima preventiva de 20 km/h).

---

## 3. Metodología de Análisis Espacial y Modelado Geométrico

El pipeline implementado en [`scripts/process_street_closures.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/process_street_closures.py) opera en cuatro fases secuenciales:

```
┌─────────────────────────────────┐
│ Padrón Oficial SEDECO / Maps    │
│ (1,367 Tianguis con Coordenadas)│
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ 1. Parser Lingüístico Vial      │ ──► Calle Principal, Entrecalles 1 y 2,
│    y Clasificador de Tipología  │     Tipo Afectación, Corredor Homologado
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ 2. Modelo Físico Dimensional    │ ──► Longitud L = f(oferentes) [100m - 4500m]
│    (Capacidad, Oferentes, Sup.) │     Ancho W (8m, 10m, 18m) -> Superficie m²
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ 3. Motor Geodésico y de Acimut  │ ◄── Red Vial Integrada (RTP, Concesionados,
│    (KDTree + Malla Vial CDMX)   │     Metrobús, Trolebús - 107,008 segmentos)
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ 4. Generador Vectorial          │ ──► cierres_viales_tianguis.geojson
│    (LineString + Buffer Polygon)│ ──► cierres_viales_por_dia.json
└─────────────────────────────────┘
```

### 3.1 Parser Lingüístico de Direcciones Urbanas
Las direcciones catastrales y del padrón popular en México contienen sintaxis no estandarizada. El parser utiliza expresiones regulares robustas para descomponer cadenas complejas:

- **Patrón `ENTRE ... Y ...`**: `"ADOLFO DE LA HUERTA ENTRE RUIZ CORTINEZ Y BENITO JUAREZ"` $\rightarrow$ Vía Principal: `ADOLFO DE LA HUERTA`, Entrecalle 1: `RUIZ CORTINEZ`, Entrecalle 2: `BENITO JUAREZ`.
- **Patrón `ESQUINA / ESQ. CON`**: `"RIO BRAVO ESQ. RIO MIXCOAC"` $\rightarrow$ Vía Principal: `RIO BRAVO`, Cruce: `RIO MIXCOAC`.
- **Patrón de Intervalo Tramo `DE ... A ...`**: `"AV. 4 DE CALLE C55 A 31"` $\rightarrow$ Vía Principal: `AV. 4`, Límite 1: `CALLE C55`, Límite 2: `CALLE 31`.
- **Limpieza de alias comerciales**: Extracción de sufijos como `“Tianguis El Salado”` o anotaciones administrativas `(PBLO)`, `(U HAB)`.

### 3.2 Modelo Dimensional de Afectación Física
La longitud de calle ocupada guarda una correlación directa con el número de oferentes (puestos comerciales):
- En tianguis sobre arroyo vehicular, los puestos se instalan enfrentados a ambos lados de la calle (doble fila).
- Cada puesto tiene un frente estándar promedio de $2.5\text{ metros}$. Con dos filas paralelas:
  $$\text{Longitud Lineal} \approx \frac{\text{oferentes}}{2} \times 2.5\text{ m} = 1.25 \times \text{num\_oferentes}$$
- Para salvaguardar la coherencia urbana:
  - **Límite inferior**: $100\text{ metros}$ (longitud típica de 1 manzana urbana en CDMX).
  - **Valor por omisión**: $150\text{ metros}$ para tianguis con puestos no censados.
  - **Límite superior**: $4,500\text{ metros}$ para mega-concentraciones lineales (ej. San Felipe de Jesús o El Salado).

### 3.3 Motor de Acimut Vial (Bearing) con Red de Transporte
Para proyectar el tramo de calle en el plano geográfico con su orientación real:
1. Se unificaron y segmentaron más de **107,000 tramos vectoriales** procedentes de:
   - Red de Transporte de Pasajeros (RTP)
   - Rutas Secundarias Concesionadas (Microbuses y Corredores)
   - Red de Trolebús y Metrobús
2. Se construyó un árbol espacial $k\text{-d}$ (`scipy.spatial.cKDTree`) sobre los centros de segmento.
3. Para cada tianguis a una distancia $\le 250\text{ m}$ de una línea de transporte, se hereda la tangente angular exacta del segmento vial.
4. Para vías sin cobertura inmediata de transporte masivo, se aplican las reglas del damero capitalino:
   - Ejes Sur/Norte y Calles Oriente/Poniente: orientadas a $90^\circ$ (Este-Oeste).
   - Ejes Oriente/Poniente, Eje Central y Calles Norte/Sur: orientadas a $0^\circ$ (Norte-Sur).
   - Traza central histórica de Tenochtitlan / Virreinal: acimut primario de $15^\circ$ NNE-SSW.

### 3.4 Geometría Geodésica
A partir de la coordenada auditada $(lng_0, lat_0)$, la longitud calculada $L$ y el acimut $\theta$:
$$\Delta x = \frac{L}{2} \sin(\theta), \quad \Delta y = \frac{L}{2} \cos(\theta)$$
$$\Delta lng = \frac{\Delta x}{111320 \times \cos(lat_0)}, \quad \Delta lat = \frac{\Delta y}{110574}$$

Se computan las coordenadas del extremo inicial, punto medio y extremo final, conformando un `LineString` vectorial de alta precisión y un polígono envolvente de ancho $W$ (8 m a 18 m).

---

## 4. Métricas de Impacto Vial en la CDMX

### 4.1 Distribución Semanal de Cierres y Kilómetros Ocupados
Los 1,367 tianguis se distribuyen de manera escalonada a lo largo de los siete días de la semana, sumando **1,396 eventos operativos semanales**:

| Día de la Semana | Tianguis Activos | Longitud Ocupada (km) | Cierres Totales | Reducción Carril | Ocupación Camellón | Oferentes Totales |
|:-----------------|:----------------:|:---------------------:|:---------------:|:----------------:|:------------------:|:-----------------:|
| **LUNES**        | 194              | 42.15 km              | 157             | 32               | 5                  | 29,070            |
| **MARTES**       | 199              | 48.68 km              | 154             | 37               | 8                  | 38,177            |
| **MIÉRCOLES**    | 177              | 41.45 km              | 138             | 23               | 16                 | 29,039            |
| **JUEVES**       | 194              | 44.79 km              | 157             | 25               | 12                 | 31,923            |
| **VIERNES**      | 163              | 34.87 km              | 123             | 33               | 6                  | 24,219            |
| **SÁBADO**       | 202              | 52.90 km              | 155             | 35               | 12                 | 40,058            |
| **DOMINGO**      | **267**          | **65.16 km**          | **199**         | **53**           | **15**             | **47,142**        |
| **TOTAL SEMANAL**| **1,396**        | **330.00 km**         | **1,083**       | **238**          | **74**             | **239,628**       |

> [!IMPORTANT]
> **El pico máximo de afectación vial ocurre el DOMINGO**, con **267 tianguis** que cierran o restringen **65.16 kilómetros** de calles y avenidas simultáneamente. El segundo día de mayor impacto es el **SÁBADO** (52.90 km), seguido por el **MARTES** (48.68 km, impulsado por macrotianguis en Iztapalapa).

---

### 4.2 Matriz Completa de Afectación por Alcaldía y Día (km lineales)

La siguiente matriz documenta los kilómetros de vías públicas ocupadas cada día por tianguis en cada una de las 16 alcaldías de la CDMX:

| Alcaldía | Lunes | Martes | Miércoles | Jueves | Viernes | Sábado | Domingo | Total Semanal (km) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **IZTAPALAPA** | 12.94 | **22.34** | 10.26 | 17.46 | 12.19 | **28.01** | 15.89 | **119.09 km** |
| **GUSTAVO A. MADERO** | 8.12 | 5.73 | 12.26 | 6.85 | 4.99 | 7.51 | **15.91** | **61.37 km** |
| **COYOACÁN** | 3.99 | 4.55 | 2.67 | 4.37 | 3.08 | 0.77 | 6.18 | **25.61 km** |
| **ÁLVARO OBREGÓN** | 2.88 | 2.40 | 2.03 | 3.30 | 1.82 | 3.41 | 7.12 | **22.96 km** |
| **TLALPAN** | 2.50 | 2.90 | 4.49 | 1.87 | 2.27 | 2.91 | 3.35 | **20.29 km** |
| **CUAUHTÉMOC** | 1.63 | 1.55 | 2.12 | 1.20 | 1.67 | 3.64 | 6.48 | **18.29 km** |
| **IZTACALCO** | 2.12 | 1.95 | 1.24 | 1.72 | 1.42 | 1.12 | 1.07 | **10.64 km** |
| **VENUSTIANO CARRANZA**| 1.99 | 2.38 | 1.65 | 0.59 | 0.94 | 0.69 | 1.35 | **9.59 km** |
| **BENITO JUÁREZ** | 1.01 | 1.37 | 1.06 | 1.55 | 1.05 | 0.91 | 1.35 | **8.30 km** |
| **AZCAPOTZALCO** | 0.72 | 0.50 | 0.92 | 1.94 | 1.60 | 1.15 | 1.24 | **8.07 km** |
| **TLÁHUAC** | 0.85 | 0.73 | 1.06 | 1.81 | 1.73 | 0.77 | 0.36 | **7.31 km** |
| **XOCHIMILCO** | 0.66 | 0.60 | 0.68 | 0.78 | 0.60 | 0.66 | 2.02 | **6.00 km** |
| **MIGUEL HIDALGO** | 1.56 | 0.85 | 0.40 | 0.25 | 0.69 | 0.69 | 0.88 | **5.32 km** |
| **LA MAGDALENA CONTRERAS**| 0.41 | 0.53 | 0.29 | 0.45 | 0.20 | 0.55 | 1.06 | **3.49 km** |
| **CUAJIMALPA DE MORELOS**| 0.78 | 0.10 | 0.21 | 0.35 | 0.39 | 0.10 | 0.20 | **2.13 km** |
| **MILPA ALTA** | 0.00 | 0.20 | 0.10 | 0.31 | 0.23 | 0.00 | 0.72 | **1.56 km** |
| **TOTAL CDMX POR DÍA** | **42.15** | **48.68** | **41.45** | **44.79** | **34.87** | **52.90** | **65.16** | **330.00 km** |

---

### 4.3 Top 10 Corredores Viales con Mayor Impacto en Movilidad (CDMX)

Al clasificar por volumen de puestos concentrados y longitud lineal acumulada a lo largo de la semana, destacan diez corredores emblemáticos:

| No. | Corredor Vial Homologado | Longitud Ocupada | Puestos Acumulados | Régimen de Afectación | Alcaldías Afectadas |
|:---:|:---|:---:|:---:|:---|:---|
| **1** | **CALLE CANDELABROS** | 13.23 km | 13,776 | Cierre total de calle | Iztapalapa (San Lorenzo Tezonco) |
| **2** | **AV. 10** | 4.50 km | 7,500 | Ocupación de camellón/banqueta | Iztapalapa (Santa Cruz Meyehualco) |
| **3** | **AV. VILLA DE AYALA** | 6.78 km | 5,066 | Cierre total de calle | Gustavo A. Madero, Iztapalapa |
| **4** | **AV. TEXCOCO** | 5.77 km | 4,893 | Reducción de carriles | Iztacalco, Iztapalapa |
| **5** | **AV. REPÚBLICA FEDERAL** | 4.55 km | 3,640 | Cierre total de calle | Iztapalapa (El Salado) |
| **6** | **AV. AZCÁRRAGA VIDAURRETA** | 4.53 km | 3,500 | Reducción de carriles | Iztapalapa (Cabeza de Juárez) |
| **7** | **AV. GUELATAO** | 4.08 km | 3,172 | Reducción de carriles | Iztapalapa |
| **8** | **EXPLORADORES DE EJÉRCITO DE ORIENTE** | 3.85 km | 3,035 | Cierre total de calle | Iztapalapa |
| **9** | **PLAYA ENCANTADA** | 3.54 km | 2,830 | Cierre total de calle | Iztacalco, Iztapalapa |
| **10**| **CALLE 7** | 3.63 km | 2,829 | Cierre total de calle | Coyoacán, Iztacalco, Iztapalapa |

---

### 4.4 Análisis Focalizado por Alcaldías Críticas

#### A. Iztapalapa (Capital del Comercio Popular)
Concentra el **36.1% de todos los kilómetros cerrados en la capital** (119.09 km semanales).
- **Martes y Sábados críticos**: El martes registra 22.34 km y el sábado alcanza 28.01 km.
- **Tianguis El Salado (Miércoles / Sábado)**: En Av. República Federal e Ignacio López Tarso, ocupa más de 3.5 km lineales con afectación directa al distribuidor vial de Calzada Ignacio Zaragoza y la estación del Metro Santa Martha (Línea A).
- **San Lorenzo Tezonco (Calle Candelabros)**: Bloquea el eje conector entre Av. Tláhuac y Periférico Oriente durante cuatro días a la semana.

#### B. Gustavo A. Madero (Eje Norte y Conurbación ZMVM)
Segunda alcaldía con mayor afectación vial con **61.37 km semanales**.
- **Tianguis de San Felipe de Jesús (Domingo)**: Es el tianguis más grande de América Latina. Se extiende a lo largo de **Emiliano Zapata y Av. Villa de Ayala**, cruzando colonias enteras hasta el límite con Nezahualcóyotl y Ecatepec, bloqueando más de 5.4 km lineales en un solo día con más de 1,800 oferentes censados y miles más intermitentes.
- **Nueva Atzacoalco (Miércoles)**: Ocupa Calle 308 (2.52 km lineales), generando cierres en la cuadrícula de acceso a Eduardo Molina.

#### C. Cuauhtémoc (Zona Central de Alta Densidad Vehicular)
Aunque en kilómetros absolutos suma 18.29 km, el impacto vial por metro cuadrado es el más severo de la metrópoli por tratarse del nodo emisor/receptor de viajes más congestionado del país:
- **Jardín del Arte / Sullivan (Sábado y Domingo)**: Bloqueo perimetral en Calle James Sullivan entre Manuel M. Contreras y Rosas Moreno, estrangulando el acceso entre Insurgentes Centro y Circuito Interior.
- **La Lagunilla (Domingo)**: Bloqueo de Calle Comonfort, Jaime Nunó y reducción de laterales en Paseo de la Reforma, entre Eje 1 Norte e Hidalgo.
- **Corredor Roma-Condesa**: Bazares en Plaza de la Cibeles (Calle El Oro), Parque Pushkin y Plaza del Lanzador en Orizaba.

---

## 5. Guía de Uso para Movilidad Urbana y Ciudadanía

### 5.1 Para Automovilistas y Motociclistas
1. **Verificación Previa por Día de la Semana**:
   - Antes de iniciar un trayecto barrial, consulte el mapa dinámico con filtro del día correspondiente. Los tianguis operan habitualmente entre las **07:00 y las 19:00 horas**.
2. **Protocolo ante Cierre Total**:
   - Al encontrar una señal de tianguis en vías secundarias, no intente forzar el paso. Las cuerdas de lonas y estructuras tubulares invaden el ancho total de banqueta a banqueta.
   - Gire a la derecha o izquierda en el cruce previo y use vías colectoras primarias (Ejes Viales o Avenidas Maestras).
3. **Precaución en Avenidas con Reducción de Carriles**:
   - En avenidas como Texcoco, Guelatao o Ermita Iztapalapa, los carriles derechos son ocupados por camionetas de carga y puestos. Cambie con anticipación a los carriles centrales o izquierdos para evitar frenados intempestivos.

### 5.2 Para Peatones, Ciclistas y Usuarios de Transporte Público
1. **Peatones**:
   - Los tianguis funcionan como corredores peatonales vivos y seguros durante el día; no obstante, mantenga atención en los cruces de calles transversales donde el flujo vehicular intersecta el tianguis.
2. **Ciclistas**:
   - Se recomienda **desmontar de la bicicleta** al transitar por el interior de tianguis con alta aglomeración (>100 oferentes) debido a cables tensores, cajas y pasillos estrechos ($<1.5\text{ m}$).
3. **Transporte Público de Superficie (RTP y Microbuses)**:
   - En días de tianguis, decenas de rutas modifican su derrotero habitual virando 1 o 2 cuadras antes de la calle de costumbre. Tome en cuenta un incremento de 10 a 15 minutos en sus tiempos de traslado en colonias populares de Iztapalapa y GAM.

### 5.3 Para Planeadores Urbanos, SEMOVI y Protección Civil
- **Corredores de Evacuación y Ambulancias**: Los datos generados en GeoJSON permiten a los Centros de Comando C5 y ambulancias del ERUM/Cruz Roja calcular rutas de emergencia que eviten calles bloqueadas por tianguis según el día y la hora.
- **Logística Urbana y Abasto**: Los municipios conurbados del Estado de México (Nezahualcóyotl, Ecatepec, Tlalnepantla) pueden sincronizar sus límites de cuadrante vial con el atlas de cierres de la CDMX.

---

## 6. Especificación Técnica de los Archivos de Datos

### 6.1 `data/processed/cierres_viales_tianguis.geojson`
FeatureCollection estándar EPSG:4326 con **1,367 geometrías vectoriales**:
- **Geometría**: `LineString` con coordenadas `[[lng_inicio, lat_inicio], [lng_medio, lat_medio], [lng_fin, lat_fin]]`.
- **Propiedades Clave**:
  ```json
  {
    "id": "TIANG-0001",
    "nombre": "TIANGUIS PILOTO (ADOLFO LOPEZ MATEOS) (AMPL) (LUNES)",
    "alcaldia": "ALVARO OBREGON",
    "colonia": "PILOTO (ADOLFO LOPEZ MATEOS) (AMPL)",
    "calle_principal": "ADOLFO DE LA HUERTA",
    "entre_calle1": "RUIZ CORTINEZ",
    "entre_calle2": "BENITO JUAREZ",
    "tipo_afectacion": "Cierre total de calle",
    "nivel_impacto": "ALTO",
    "longitud_metros": 328.8,
    "ancho_estimado_metros": 10.0,
    "superficie_afectada_m2": 3288.0,
    "orientacion_grados": 35.4,
    "orientacion_cardinal": "NE-SW",
    "desvio_recomendado": "Cierre total de circulación en ADOLFO DE LA HUERTA entre RUIZ CORTINEZ y BENITO JUAREZ...",
    "poligono_buffer": [[[lng1, lat1], [lng2, lat2], [lng3, lat3], [lng4, lat4], [lng1, lat1]]],
    "bbox": [-99.222778, 19.374583, -99.220518, 19.376641]
  }
  ```

### 6.2 `data/processed/cierres_viales_por_dia.json`
Estructura JSON optimizada para indexación inmediata en cliente web/móvil:
- **`metadata`**: Datos del proyecto y total de tianguis.
- **`resumen_semanal`**:
  - `top_10_corredores_cdmx`
  - `matriz_alcaldia_dia_km`
- **`dias`**: Diccionario indexado por `LUNES`, `MARTES`, `MIERCOLES`, `JUEVES`, `VIERNES`, `SABADO`, `DOMINGO`. Cada día contiene:
  - Métricas agregadas (`km_lineales_ocupados`, `distribucion_afectacion`, `oferentes_totales`).
  - Desglose por alcaldía.
  - Top corredores afectados del día.
  - Lista de cierres con coordenadas de línea y buffer poligonal listos para capas de Leaflet / MapLibre.

---

## 7. Reproducibilidad

El script se ejecuta de forma determinista y sin dependencias pesadas (usa Python estándar, NumPy, SciPy, Pandas y PyShp):

```bash
# Ejecutar pipeline completo de cierres viales
python3 scripts/process_street_closures.py

# Parámetros avanzados
python3 scripts/process_street_closures.py \
  --input-csv data/processed/tianguis_limpio.csv \
  --transporte-dir data/raw/transporte \
  --output-geojson data/processed/cierres_viales_tianguis.geojson \
  --output-json data/processed/cierres_viales_por_dia.json
```
