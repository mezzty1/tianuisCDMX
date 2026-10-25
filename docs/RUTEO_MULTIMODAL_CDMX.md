# Ruteo Multimodal para Transporte Público y Peatonal en la CDMX
## Arquitectura Técnica, Algoritmos y Prototipo de Ruteo (Chilangatón 2026)

---

## 1. Resumen Ejecutivo

El objetivo de esta investigación es diseñar e implementar una solución de **cálculo de rutas multimodal de punto a punto (origen a destino)** para la Ciudad de México y su Zona Metropolitana (ZMVM), conectando a la ciudadanía desde cualquier coordenada o punto de referencia hacia los **329 Mercados Públicos** y **1,367 Tianguis y Mercados sobre Ruedas** catalogados en el proyecto.

La solución integra:
1. **Primera y última milla a pie**: Caminata con velocidades y distancias de acceso realistas ($1.25\text{ m/s} = 4.5\text{ km/h}$, radio máximo de caminata de abordaje $1.2\text{ km}$).
2. **Red de Transporte Masivo y de Superficie**: Metro CDMX (12 líneas), Metrobús (7 líneas), Trolebús (incluyendo Trolebús Elevado Línea 10), Cablebús (Líneas 1, 2 y 3), Tren Ligero, Ferrocarril Suburbano, Red de Transporte de Pasajeros (RTP), Corredores Concesionados y Pumabús.
3. **Reglas Tarifarias Oficiales**: Matriz de tarifas de la Tarjeta de Movilidad Integrada (MI), contemplando transbordos gratuitos intramodales (Metro a Metro, Metrobús a Metrobús).
4. **Métricas de Impacto Social y Ambiental**: Tiempo de traslado, número de transbordos, costo en pesos mexicanos y kilogramos de $\text{CO}_2$ evitados frente al uso de automóvil particular.

El script funcional se encuentra implementado en [`scripts/route_calculator.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/route_calculator.py).

---

## 2. Estado del Arte en Algoritmos de Ruteo de Tránsito Público

A diferencia del ruteo vehicular en grafos viales tradicionales (donde las aristas siempre están disponibles y el costo es una función de la longitud y velocidad máxima), el **ruteo en transporte público presenta desafíos teóricos únicos**:
- **Dependencia temporal y de frecuencias**: Un tramo de autobús o metro solo está disponible en momentos determinados (horarios fijos o intervalos de frecuencia/headways).
- **Multimodalidad y transbordos**: Caminar de una plataforma a otra implica distancias a pie y tiempos de espera para el siguiente tren/autobús.
- **Optimización multicriterio (Frontera de Pareto)**: El usuario no busca únicamente el viaje más corto en minutos si este requiere cuatro transbordos agotadores; busca el mejor balance entre **tiempo de llegada**, **número de transbordos**, **distancia a pie** y **costo económico**.

### 2.1 Algoritmo RAPTOR (Round-Based Public Transit Routing)
*Paper de Referencia:* **Delling, D., Pajor, T., & Werneck, R. F. (2012 / 2014)**. *"Round-Based Public Transit Routing"*, Microsoft Research / Transportation Science.

#### Principio de Funcionamiento:
RAPTOR no construye un grafo expandido por tiempo ni utiliza colas de prioridad con montículos de Fibonacci o Dijkstra. En su lugar, opera directamente sobre las tablas de rutas y viajes del estándar GTFS organizando el cálculo en **rondas discretas**:
- **Ronda 1**: Determina todas las paradas alcanzables tomando exactamente **1 vehículo** (0 transbordos) a partir de las estaciones alcanzables a pie desde el origen.
- **Ronda 2**: Determina todas las paradas alcanzables tomando **2 vehículos** (1 transbordo intermedio).
- **Ronda $k$**: Determina las paradas alcanzables con $k$ etapas de tránsito ($k-1$ transbordos).

```
         [Origen]
            │ (Caminata acceso)
            ▼
        [Parada A] ──────── Ronda 1 (Ruta Metro L2) ────────► [Parada B]
                                                                  │
                                                        (Transbordo a pie)
                                                                  ▼
                                                              [Parada C] ─── Ronda 2 (Línea 9) ───► [Parada D]
                                                                                                        │
                                                                                                (Caminata egreso)
                                                                                                        ▼
                                                                                                    [Destino]
```

#### Ventajas Clave de RAPTOR:
1. **Frontera de Pareto Exacta**: Al finalizar cada ronda $k$, se obtiene la mejor llegada posible usando a lo sumo $k$ vehículos, permitiendo al usuario elegir entre el viaje más rápido o el que requiere menos transbordos.
2. **Exploración por Rutas (Route Scanning)**: En cada ronda, solo se procesan las rutas que tocan paradas mejoradas en la ronda previa. En lugar de explorar nodo por nodo, recorre secuencias completas de paradas en una sola pasada de memoria lineal contigua (extremadamente eficiente en caché de CPU).
3. **Sin necesidad de preprocesamiento costoso**: A diferencia de las Contraction Hierarchies (CH), RAPTOR no requiere horas de preprocesamiento del grafo; puede arrancar inmediatamente con los archivos GTFS crudos.
4. **Variantes Avanzadas**:
   - **McRAPTOR (Multi-criteria RAPTOR)**: Agrega dimensiones adicionales como tarifa monetaria o fiabilidad.
   - **rRAPTOR (Range RAPTOR)**: Calcula las mejores opciones en una ventana de salida de 1 a 2 horas (muy útil para transporte con frecuencias variables).

---

### 2.2 Connection Scan Algorithm (CSA)
*Paper de Referencia:* **Dibbelt, J., Pajor, T., Strasser, B., & Wagner, D. (2013)**. *"Intriguingly Simple and Fast Transit Routing"*.

- **Principio**: Ordena todas las conexiones elementales (salida de parada $A$ a las $t_1$, llegada a parada $B$ a las $t_2$) en un único arreglo plano cronológico.
- **Mecánica**: Realiza un escaneo lineal simple de una sola pasada sobre este arreglo.
- **Ventaja**: Implementación extraordinariamente sencilla y óptima para arquitecturas de hardware modernas.
- **Limitación en CDMX**: Los feeds GTFS de la SEMOVI CDMX utilizan en su mayoría esquemas basados en frecuencias (`frequencies.txt` con intervalos de paso de 3 a 10 minutos) en lugar de horarios exactos de llegada por segundo para las 42,789 paradas.

---

### 2.3 Grafos de Estados Conscientes de Línea (Line-Aware State Graphs)
Para sistemas urbanos densos basados en intervalos regulares de alta frecuencia (como Metro y Metrobús en CDMX, con trenes cada 2 a 5 minutos), el enfoque de **Grafo de Estados con Dijkstra / A*** ofrece un rendimiento sobresaliente cuando se estructura correctamente:

1. **Estado en el Grafo**: Cada nodo representa el par $(\text{parada\_id}, \text{ruta\_id})$.
2. **Aristas en Vehículo**: Conectan $(\text{parada}_i, R)$ con $(\text{parada}_{i+1}, R)$ con peso igual al tiempo de tránsito entre estaciones (sin penalización adicional).
3. **Aristas de Transbordo Interno**: Conectan $(\text{parada}_i, R_1)$ con $(\text{parada}_i, R_2)$ con una penalización de 2.5 a 4.0 minutos (tiempo de espera de la siguiente unidad).
4. **Aristas de Correspondencia Peatonal**: Conectan estaciones físicas a menos de 180 metros (o del mismo complejo de correspondencia oficial) con el tiempo de caminata más la penalización de espera.
5. **Primera y Última Milla**: Nodos temporales `ORIGIN` y `DEST` conectados mediante indexación espacial multivariada (cKDTree en coordenadas 3D geocéntricas).

**Resultado Obtenido en CDMX**: Tiempos de respuesta de **6 a 55 milisegundos**, sin requerir servidores externos ni servicios en la nube.

---

## 3. Comparativa de Motores de Ruteo Open Source

| Motor | Lenguaje | Algoritmo Central | Soporte GTFS | Soporte Peatonal / Bici | Consumo de RAM (CDMX) | Despliegue y Facilidad |
|---|---|---|---|---|---|---|
| **OpenTripPlanner 2 (OTP2)** | Java 17+ | RAPTOR + A* sobre OSM | **Excelente** (Nativo) | Excelente (OpenStreetMap) | Alto (4 - 8 GB RAM) | Docker / Jar oficial. Requiere OSM PBF + GTFS. |
| **Valhalla** | C++17 | Time-Distance Dynamic Tile Routing | Bueno (`valhalla_build_transit`) | Excelente (OpenStreetMap) | Medio (1.5 - 3 GB RAM) | Requiere compilación C++ o contenedor Docker oficial. |
| **OSRM** | C++ | Contraction Hierarchies (CH) / MLD | **No** (Sin soporte de horarios GTFS) | Sobresaliente para autos/bicis | Bajo (500 MB - 1 GB) | Excelente para autos/peatones, no apto para transporte público. |
| **GraphHopper** | Java | Pt Reader + Multi-criteria Dijkstra | Bueno (Módulo Pt) | Excelente (OpenStreetMap) | Medio (2 - 4 GB RAM) | Requiere OSM PBF + GTFS. Buena API REST. |
| **Motor Embebido en Python (Este Proyecto)** | Python (NetworkX + SciPy + cKDTree) | Line-Aware State Graph + RAPTOR Footpaths | **Nativo directo** sobre CSVs locales | Sí (Haversine + Geocéntrico 3D) | Muy Bajo (~180 MB RAM) | **Inmediato**: 0 dependencias externas pesadas, corre en cualquier entorno. |

---

## 4. Librerías Open Source en Python

### 4.1 `r5py` (Conveyal R5 para Python)
- **Descripción**: Wrapper oficial de Python para R5 (*Rapid Realistic Routing on Real-world and Reimagined Realities*), desarrollado por Conveyal.
- **Cómo funciona**: Combina un archivo OpenStreetMap (`.pbf`) y uno o varios archivos GTFS (`.zip`). Ejecuta RAPTOR compilado en Java de alto rendimiento con acceso desde DataFrames de Pandas/GeoPandas.
- **Casos de uso ideales**: Estudios masivos de accesibilidad urbana (matrices origen-destino de millones de puntos).
- **Requisitos**: Java Runtime Environment (JRE 11+) instalado en el sistema operativo anfitrión.

### 4.2 `pytransit`
- **Descripción**: Implementación en Python puro de los algoritmos RAPTOR y Connection Scan Algorithm (CSA).
- **Cómo funciona**: Lee directamente archivos GTFS en memoria y calcula las fronteras de Pareto entre paradas.
- **Ventaja**: Código abierto educativo y flexible para experimentar con variantes de transbordos.

### 4.3 `peartree`
- **Descripción**: Biblioteca desarrollada para convertir tablas GTFS en grafos dirigidos de `networkx`.
- **Cómo funciona**: Interpola frecuencias de viaje para asignar pesos en minutos a las aristas y genera aristas de transbordo entre paradas adyacentes.

### 4.4 `networkx` + `scipy.spatial.cKDTree`
- **Descripción**: Arquitectura elegida para el motor [`scripts/route_calculator.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/scripts/route_calculator.py).
- **Ventajas**:
  - No requiere máquinas virtuales de Java ni dependencias binarias complejas.
  - La indexación espacial 3D con `cKDTree` sobre el radio terrestre resuelve los vecinos más cercanos de 11,363 paradas en microsegundos.
  - Serialización con `pickle` que permite cargar el grafo completo en memoria en solo 0.2 segundos.

---

## 5. APIs Públicas y de Gratuidad (Cobertura CDMX)

| API | Cobertura CDMX | Modo Tránsito Público | Nivel de Gratuidad | Observaciones para el Proyecto |
|---|---|---|---|---|
| **Motor Embebido Local (`route_calculator.py`)** | **100% CDMX y ZMVM** | **Metro, MB, Trolebús, RTP, Cablebús, CC, Trenes** | **100% Libre y Gratuito** (Sin límites) | **Recomendada para el hackathon**: Sin costos, sin latencia de red, offline. |
| **OpenRouteService (ORS)** | Global | No (Solo peatonal, ciclista, auto) | 2,000 req/día gratuitas con API Key | Excelente para obtener geometrías exactas calle a calle de los tramos peatonales. |
| **Transitland API (MobilityData)** | CDMX incluida (Feeds SEMOVI) | Consulta de feeds y rutas | Nivel gratuito comunitario con API Key | Ideal para consultar si hay cambios recientes o cierres en los feeds oficiales de SEMOVI. |
| **Google Maps Directions API** | CDMX completa | Sí (Metro, Metrobús, RTP) | Crédito mensual de $200 USD (~40,000 req/mes) | Comercial, requiere tarjeta de crédito para activar cuenta de Google Cloud. |
| **Stadia Maps (Valhalla)** | Global | Sí (donde haya GTFS activo) | Nivel gratuito de 2,500 req/día | Requiere registrarse y configurar API Key. |

---

## 6. Estructura Tarifaria Oficial (Movilidad Integrada CDMX)

El motor calcula el costo exacto del viaje aplicando las reglas del Sistema de Movilidad Integrada (MI):

| Subsistema de Transporte | Tarifa Oficial | Reglas de Transbordo |
|---|---|---|
| **STC Metro** | $5.00 MXN | **Transbordo gratuito ilimitado** entre las 12 líneas dentro de la red subterránea/superficial. |
| **Metrobús (L1 a L7)** | $6.00 MXN | **Transbordo gratuito** entre líneas de Metrobús dentro de un lapso de 2 horas (excepto terminal de L4 al AICM). |
| **Trolebús (Líneas 1 a 9, 12)** | $4.00 MXN | Pago por abordaje con tarjeta MI o moneda. |
| **Trolebús Elevado (Línea 10)** | $7.00 MXN | Tarifa especial del viaducto elevado de Ermita Iztapalapa. |
| **Cablebús (L1, L2, L3)** | $7.00 MXN | Tarifa por viaje en teleférico. |
| **Tren Ligero (Tasqueña - Xochimilco)** | $3.00 MXN | Tarifa integrada STE. |
| **RTP (Red de Transporte de Pasajeros)** | $2.00 MXN (Ordinario/Atenea)<br>$4.00 MXN (Expreso)<br>$5.00 MXN (Ecobús) | Tarifa social subsidiada más económica de la capital. |
| **Corredores Concesionados (CC)** | $8.00 MXN a $9.00 MXN | Autobuses morados/verdes zonales. |
| **Ferrocarril Suburbano** | $10.50 MXN (0 - 12.89 km)<br>$24.50 MXN (12.9 - 25.6 km) | Viaje interurbano Buenavista - Cuautitlán. |
| **Pumabús (UNAM)** | $0.00 MXN | Servicio gratuito dentro del campus de Ciudad Universitaria. |
| **Caminata Peatonal** | $0.00 MXN | Tramos a pie de primera y última milla. |

---

## 7. Guía de Uso del Prototipo (`scripts/route_calculator.py`)

### 7.1 Ejecución por Nombres de Lugares / Mercados / Tianguis
El script incluye resolución semántica automática para los nombres populares de mercados y tianguis:

```bash
# De Zócalo a Mercado Jamaica
python3 scripts/route_calculator.py --from "Zócalo" --to "Mercado Jamaica"

# De Bellas Artes a Tianguis Santa Cruz Meyehualco (Iztapalapa)
python3 scripts/route_calculator.py --from "Bellas Artes" --to "Tianguis Santa Cruz Meyehualco"

# De Indios Verdes a Mercado Jamaica
python3 scripts/route_calculator.py --from "Indios Verdes" --to "Mercado Jamaica"
```

### 7.2 Ejecución por Coordenadas Arbitrarias
```bash
python3 scripts/route_calculator.py --origin 19.4326,-99.1332 --dest 19.4086,-99.1228
```

### 7.3 Emisión en Formato JSON para APIs o Interfaces Web
```bash
python3 scripts/route_calculator.py --from "Zócalo" --to "Mercado Jamaica" --json
```

### 7.4 Ejecutar Suite de Rendimiento (Benchmark)
```bash
python3 scripts/route_calculator.py --bench
```

---

## 8. Resultados de las Pruebas de Rendimiento

Las pruebas realizadas arrojaron los siguientes resultados en la máquina local:

```
=== SUITE DE PRUEBAS DE RUTEO CDMX ===
✓ Zócalo ➔ Mercado Jamaica:
  - Tiempo estimado: 16.4 min
  - Costo: $5.00 MXN (Metro L2 ➔ Chabacano ➔ Metro L9)
  - Caminata: 362 m (9.3 min)
  - Tiempo de cálculo: 0.006 segundos (6 ms)

✓ Bellas Artes ➔ Tianguis Santa Cruz Meyehualco (Iztapalapa):
  - Tiempo estimado: 50.6 min
  - Costo: $12.00 MXN (Metro L2 ➔ Chabacano ➔ Metro L8 ➔ Constitución de 1917 ➔ Trolebús Elevado L10 ➔ Meyehualco)
  - Caminata: 577 m
  - Tiempo de cálculo: 0.047 segundos (47 ms)

✓ Zócalo ➔ Central de Abasto:
  - Tiempo estimado: 54.7 min
  - Costo: $13.00 MXN
  - Caminata: 880 m
  - Tiempo de cálculo: 0.054 segundos (54 ms)

✓ Indios Verdes ➔ Mercado Jamaica:
  - Tiempo estimado: 33.4 min
  - Costo: $5.00 MXN (Metro L3 ➔ Centro Médico ➔ Metro L9)
  - Caminata: 245 m
  - Tiempo de cálculo: 0.014 segundos (14 ms)
======================================
```

---

## 9. Próximos Pasos e Integración en la Plataforma Web

1. **Endpoint REST / FastAPI**:
   - Exponer `CDMXMultimodalRouter.calculate_route()` a través de un endpoint ligero `GET /api/v1/route?orig_lat=...&orig_lon=...&dest_lat=...&dest_lon=...`.
2. **Visualización en el Mapa Interactivo**:
   - Trazar la polilínea del itinerario en Leaflet/MapLibre usando las geometrías de `shapes.txt` de los tramos de metro/autobús y líneas punteadas para los tramos peatonales.
3. **Cálculo de Rutas Accesibles**:
   - Aprovechar el atributo `wheelchair_boarding` presente en `stops.txt` para ofrecer una opción de "Ruta Accesible" (estaciones con elevador y rampas de acceso para personas con movilidad reducida).
