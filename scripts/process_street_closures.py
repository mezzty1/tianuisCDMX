#!/usr/bin/env python3
"""
Módulo 4: Cierres de Vías Dinámico por Tianguis en la CDMX
===========================================================
Chilangatón 2026 - Comercio Popular y Barrial CDMX

Procesador espacial y generador de cierres viales dinámicos:
1. Extrae y estructura componentes viales de direcciones (calle principal, entrecalles).
2. Clasifica el tipo de afectación vial:
   - 'Cierre total de calle'
   - 'Reducción de carriles'
   - 'Ocupación de camellón/banqueta'
3. Modela dimensiones físicas (longitud lineal en metros según oferentes, ancho de vía y superficie m2).
4. Asocia la orientación espacial y bearing de la red vial integrada (RTP, Concesionados, Metrobús, Trolebús).
5. Genera geometrías geodésicas de tramos viales (LineString) y polígonos de afectación (Polygon Buffer).
6. Exporta:
   - data/processed/cierres_viales_tianguis.geojson (GeoJSON completo con 1,367 tianguis)
   - data/processed/cierres_viales_por_dia.json (Estructura agrupada por día para frontend y ruteo)
"""

import os
import sys
import math
import json
import re
import argparse
from typing import Dict, List, Tuple, Any, Optional

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
import shapefile

# Constantes geodésicas (CDMX ~19.4° N)
LAT_CDMX_REF = 19.4326
METERS_PER_DEG_LAT = 110574.0
METERS_PER_DEG_LNG = 111320.0 * math.cos(math.radians(LAT_CDMX_REF))  # ~104,980 m/deg
GRID_AZIMUTH_PRIMARY = 15.0    # Orientación histórica del damero central CDMX (NNE-SSW)
GRID_AZIMUTH_SECONDARY = 105.0  # Orientación transversal (ENE-WSW)

# Coordenadas de respaldo para casos específicos
FALLBACK_COORDS = {
    'TIANG-1366': (19.319433, -99.108767), # Carmen Serdán, Coyoacán
    'TIANG-1367': (19.349000, -99.162000), # Inactivo / Coyoacán centro
}

def clean_text(s: Any) -> str:
    """Limpia cadenas de texto y elimina espacios redundantes y comillas."""
    if not isinstance(s, str):
        return ''
    s = re.sub(r'[\"“”]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def parse_street_address(raw_addr: str) -> Tuple[str, str, str, str, str]:
    """
    Analiza una dirección de tianguis y extrae:
    (calle_principal, entre_calle1, entre_calle2, tipo_afectacion, corredor_normalizado)
    """
    if not isinstance(raw_addr, str) or not raw_addr.strip():
        return '', '', '', 'Cierre total de calle', ''

    clean = raw_addr.strip()
    
    # Caso especial: Inactivo
    if 'ACTUALMENTE NO SE INSTALA' in clean.upper():
        return 'SIN OPERACIÓN', '', '', 'Inactivo - No se instala', 'INACTIVO'

    # Eliminar nombres de tianguis en comillas al final: e.g. “Tianguis ...”
    clean = re.sub(r'[\"“][^\"“”]+[\"”]\s*$', '', clean).strip()

    # Normalizar patrones redundantes como "EN EXPL. DEL MERCADO DE ... ENTRE"
    clean = re.sub(r'\s+EN\s+EXPL\.?\s+DEL\s+MERCADO\s+DE\s+[^\s]+\s+', ' ', clean, flags=re.IGNORECASE)

    cp, e1, e2 = '', '', ''

    # 1. Patrón ENTRE / ENT.
    m_entre = re.search(r'^(.*?)\s+(?:ENTRE|ENT\.?|ENT)\s+(.*)$', clean, re.IGNORECASE)
    if m_entre:
        cp = m_entre.group(1).strip(' ,.;:-')
        rest = m_entre.group(2).strip(' ,.;:-')
        m_split = re.split(r'\s+(?:Y|E|HASTA\s+LA|HASTA)\s+|,\s*', rest, maxsplit=1, flags=re.IGNORECASE)
        e1 = m_split[0].strip(' ,.;:-')
        e2 = m_split[1].strip(' ,.;:-') if len(m_split) > 1 else ''
    # 2. Patrón ESQ. / ESQUINA / ESQ CON
    elif re.search(r'^(.*?)\s+(?:ESQ\.?|ESQUINA|ESQ\b)\s*(?:CON\s+)?(.*)$', clean, re.IGNORECASE):
        m_esq = re.search(r'^(.*?)\s+(?:ESQ\.?|ESQUINA|ESQ\b)\s*(?:CON\s+)?(.*)$', clean, re.IGNORECASE)
        cp = m_esq.group(1).strip(' ,.;:-')
        e1 = m_esq.group(2).strip(' ,.;:-')
    # 3. Patrón DE ... A ...
    elif re.search(r'^(.*?)\s+DE\s+(.*?)\s+A\s+(.*)$', clean, re.IGNORECASE):
        m_de_a = re.search(r'^(.*?)\s+DE\s+(.*?)\s+A\s+(.*)$', clean, re.IGNORECASE)
        cp = m_de_a.group(1).strip(' ,.;:-')
        e1 = m_de_a.group(2).strip(' ,.;:-')
        e2 = m_de_a.group(3).strip(' ,.;:-')
    # 4. Patrón Y / E
    elif re.search(r'^(.*?)\s+(?:Y|E)\s+(.*)$', clean, re.IGNORECASE):
        m_y = re.search(r'^(.*?)\s+(?:Y|E)\s+(.*)$', clean, re.IGNORECASE)
        cp = m_y.group(1).strip(' ,.;:-')
        e1 = m_y.group(2).strip(' ,.;:-')
    # 5. Separado por comas
    elif ',' in clean:
        parts = [p.strip(' ,.;:-') for p in clean.split(',') if p.strip(' ,.;:-')]
        cp = parts[0]
        e1 = parts[1] if len(parts) > 1 else ''
        e2 = parts[2] if len(parts) > 2 else ''
    else:
        cp = clean

    cp = clean_text(cp)
    e1 = clean_text(e1)
    e2 = clean_text(e2)

    # Clasificación de tipo_afectacion
    upper_full = clean.upper()
    upper_cp = cp.upper()

    is_camellon = bool(re.search(r'\b(CAMELL[OÓ]N|BANQUETA|PLAZA|PARQUE|ESTACIONAMIENTO|DEPORTIVO|JARD[IÍ]N|CANCHAS?|BAJO\s*PUENTES?|EXPLANADA|VIVEROS)\b', upper_full))
    is_avenida = bool(re.search(r'\b(AV\.?|AVENIDA|CALZ\.?|CALZADA|EJE\b|EJE\s+\d+|CIRCUITO|PERIF[EÉ]RICO|BOULEVARD|BLVD\.?|CARRETERA|VIADUCTO)\b', upper_cp)) or bool(re.search(r'\b(AMBOS\s+ARROYOS|LATERAL|UN\s+CARRIL)\b', upper_full))

    if is_camellon:
        tipo = 'Ocupación de camellón/banqueta'
    elif is_avenida and not any(k in upper_cp for k in ['CDA.', 'CERRADA', 'CALLEJON', 'CALLEJÓN', 'PRIVADA', 'ANDADOR', 'PASAJE']):
        tipo = 'Reducción de carriles'
    else:
        tipo = 'Cierre total de calle'

    # Normalización del corredor para agregación y rankings
    corredor = upper_cp
    # Homogeneizar prefijos
    corredor = re.sub(r'^AVENIDA\s+', 'AV. ', corredor)
    corredor = re.sub(r'^CALZADA\s+', 'CALZ. ', corredor)
    corredor = re.sub(r'^CERRADA\s+', 'CDA. ', corredor)
    corredor = re.sub(r'\s+NO\.?\s*\d+.*$', '', corredor)

    # Homogeneizar corredores icónicos de alto impacto
    if 'CANDELABROS' in corredor:
        corredor = 'CALLE CANDELABROS'
    elif 'SAN FELIPE DE JESUS' in corredor:
        corredor = 'CALLE SAN FELIPE DE JESÚS'
    elif 'VILLA DE AYALA' in corredor or corredor.startswith('VILLA'):
        corredor = 'AV. VILLA DE AYALA'
    elif 'TEXCOCO' in corredor:
        corredor = 'AV. TEXCOCO'
    elif 'REPUBLICA FEDERAL' in corredor:
        corredor = 'AV. REPÚBLICA FEDERAL'
    elif 'AZACARRGA' in corredor or 'AZCARRAGA' in corredor:
        corredor = 'AV. AZCÁRRAGA VIDAURRETA'
    elif 'GUELATAO' in corredor:
        corredor = 'AV. GUELATAO'
    elif 'EXPLORADORES' in corredor:
        corredor = 'EXPLORADORES DE EJÉRCITO DE ORIENTE'
    elif 'PLAYA ENCANTADA' in corredor:
        corredor = 'PLAYA ENCANTADA'
    elif 'EJE 5 SUR' in corredor:
        corredor = 'EJE 5 SUR'
    elif 'JOSE CLEMENTE OROZCO' in corredor:
        corredor = 'AV. JOSÉ CLEMENTE OROZCO'
    elif 'ROSARIO CASTELLANOS' in corredor:
        corredor = 'ROSARIO CASTELLANOS'
    elif 'COMONFORT' in corredor:
        corredor = 'CALLE COMONFORT (LAGUNILLA)'
    elif 'SULLIVAN' in corredor:
        corredor = 'CALLE JAMES SULLIVAN'
    elif 'ORO' in corredor and 'MONTERREY' in upper_full:
        corredor = 'CALLE EL ORO (CIBELES)'
    elif 'MANUEL ZEPEDA' in corredor or 'MANUEL CEPEDA' in corredor:
        corredor = 'MANUEL ZEPEDA PERAZA'
    elif 'SAN RAFAEL ATLIXCO' in corredor:
        corredor = 'AV. SAN RAFAEL ATLIXCO'
    elif 'HACIENDA SANTO DOMINGO' in corredor:
        corredor = 'HACIENDA SANTO DOMINGO'

    return cp, e1, e2, tipo, corredor


class RoadNetworkBearingEngine:
    """
    Motor espacial que indexa la red vial y de transporte público de la CDMX
    para determinar el acimut (bearing) exacto de la calle donde opera el tianguis.
    """
    def __init__(self, raw_transporte_dir: str):
        self.segments: List[Tuple[float, float, float]] = [] # (mid_x, mid_y, bearing_deg)
        self.tree: Optional[cKDTree] = None
        self._load_network(raw_transporte_dir)

    def _add_linestrings(self, coords_list: List[List[List[float]]]):
        for coords in coords_list:
            for i in range(len(coords) - 1):
                x1, y1 = coords[i][0], coords[i][1]
                x2, y2 = coords[i+1][0], coords[i+1][1]
                mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
                dx = (x2 - x1) * METERS_PER_DEG_LNG
                dy = (y2 - y1) * METERS_PER_DEG_LAT
                dist = math.hypot(dx, dy)
                if dist >= 4.0: # Segmentos con al menos 4 metros
                    # Calcular bearing en grados (0° = Norte, 90° = Este) normalizado a 0-180°
                    bearing = math.degrees(math.atan2(dx, dy)) % 180.0
                    self.segments.append((mx, my, bearing))

    def _load_network(self, base_dir: str):
        # 1. Cargar RTP
        rtp_path = os.path.join(base_dir, 'rtp_lineas.geojson')
        if os.path.exists(rtp_path):
            try:
                with open(rtp_path, 'r', encoding='utf-8') as f:
                    rtp = json.load(f)
                for feat in rtp.get('features', []):
                    geom = feat.get('geometry', {})
                    if geom.get('type') == 'LineString':
                        self._add_linestrings([geom['coordinates']])
                    elif geom.get('type') == 'MultiLineString':
                        self._add_linestrings(geom['coordinates'])
            except Exception as e:
                print(f"Aviso al cargar RTP: {e}")

        # 2. Cargar Concesionados (Shapefile)
        conc_path = os.path.join(base_dir, 'concesionado_shp', 'concesionado_shp', 'concesionado_rutas.shp')
        if os.path.exists(conc_path):
            try:
                sf = shapefile.Reader(conc_path)
                for shp in sf.shapes():
                    parts = list(shp.parts) + [len(shp.points)]
                    for p_idx in range(len(shp.parts)):
                        pts = shp.points[parts[p_idx]:parts[p_idx+1]]
                        self._add_linestrings([pts])
            except Exception as e:
                print(f"Aviso al cargar Concesionados: {e}")

        # 3. Cargar Trolebús
        trole_path = os.path.join(base_dir, 'trolebus_lineas.geojson')
        if os.path.exists(trole_path):
            try:
                with open(trole_path, 'r', encoding='utf-8') as f:
                    trole = json.load(f)
                for feat in trole.get('features', []):
                    geom = feat.get('geometry', {})
                    if geom.get('type') == 'LineString':
                        self._add_linestrings([geom['coordinates']])
                    elif geom.get('type') == 'MultiLineString':
                        self._add_linestrings(geom['coordinates'])
            except Exception as e:
                print(f"Aviso al cargar Trolebús: {e}")

        # 4. Cargar Metrobús
        mb_path = os.path.join(base_dir, 'metrobus_lineas.geojson')
        if os.path.exists(mb_path):
            try:
                with open(mb_path, 'r', encoding='utf-8') as f:
                    mb = json.load(f)
                for feat in mb.get('features', []):
                    geom = feat.get('geometry', {})
                    if geom.get('type') == 'LineString':
                        self._add_linestrings([geom['coordinates']])
                    elif geom.get('type') == 'MultiLineString':
                        self._add_linestrings(geom['coordinates'])
            except Exception as e:
                print(f"Aviso al cargar Metrobús: {e}")

        if self.segments:
            pts = np.array([[s[0], s[1]] for s in self.segments])
            self.tree = cKDTree(pts)
            print(f"-> Red vial indexada para orientación espacial: {len(self.segments):,} segmentos.")

    def get_bearing(self, lng: float, lat: float, street_name: str) -> Tuple[float, str]:
        """
        Calcula el acimut (0°-180°) de la calle. Si hay un tramo de la red a <=250m,
        usa su tangente exacta; de lo contrario infiere de la nomenclatura o cuadrícula CDMX.
        """
        # Heurística de nomenclatura urbana
        s_upper = street_name.upper()
        if re.search(r'\b(EJE\s+\d+\s+SUR|EJE\s+\d+\s+NORTE|PONIENTE\s+\d+|ORIENTE\s+\d+)\b', s_upper):
            return 90.0, 'E-W'
        if re.search(r'\b(EJE\s+\d+\s+ORIENTE|EJE\s+\d+\s+PONIENTE|EJE\s+CENTRAL|NORTE\s+\d+|SUR\s+\d+)\b', s_upper):
            return 0.0, 'N-S'
        if 'INSURGENTES' in s_upper or 'TLALPAN' in s_upper:
            return 15.0, 'N-S'
        if 'REFORMA' in s_upper:
            return 65.0, 'NE-SW'

        if self.tree is not None:
            dist_deg, idx = self.tree.query([lng, lat])
            dist_m = dist_deg * 111000.0
            if dist_m <= 250.0:
                bearing = self.segments[idx][2]
                cardinal = self._bearing_to_cardinal(bearing)
                return round(bearing, 1), cardinal

        # Cuadrícula base CDMX
        h = hash(street_name) % 2
        bearing = GRID_AZIMUTH_PRIMARY if h == 0 else GRID_AZIMUTH_SECONDARY
        cardinal = self._bearing_to_cardinal(bearing)
        return bearing, cardinal

    @staticmethod
    def _bearing_to_cardinal(bearing: float) -> str:
        b = bearing % 180.0
        if 0.0 <= b < 22.5 or 157.5 <= b <= 180.0:
            return 'N-S'
        elif 22.5 <= b < 67.5:
            return 'NE-SW'
        elif 67.5 <= b < 112.5:
            return 'E-W'
        else:
            return 'NW-SE'


def estimate_dimensions(num_oferentes: Any, tipo_afectacion: str) -> Tuple[float, float, float]:
    """
    Modela dimensiones físicas de afectación:
    - Longitud en metros (L)
    - Ancho en metros (W)
    - Superficie en metros cuadrados (S = L * W)
    """
    try:
        oferentes = float(num_oferentes)
        if math.isnan(oferentes) or oferentes <= 0:
            oferentes = 0.0
    except (ValueError, TypeError):
        oferentes = 0.0

    # Modelo de longitud:
    # En calles con puestos a ambos lados: ~2.5m de puesto / 2 filas = ~1.25m por oferente.
    # Longitud mínima de 1 manzana (~100m). Mega-tianguis limitados a 4,500m.
    if oferentes > 0:
        longitud_m = float(np.clip(oferentes * 1.25, 100.0, 4500.0))
    else:
        longitud_m = 150.0  # Manzana estándar promedio en CDMX

    # Modelo de ancho según tipo de afectación
    if tipo_afectacion == 'Cierre total de calle':
        ancho_m = 10.0  # Arroyo vehicular completo + banquetas
    elif tipo_afectacion == 'Reducción de carriles':
        ancho_m = 18.0  # Avenida/calzada principal (afectación de 1 a 2 carriles ~6 a 8m)
    else: # Ocupación de camellón/banqueta
        ancho_m = 8.0   # Franja central o peatonal

    superficie_m2 = round(longitud_m * ancho_m, 1)
    return round(longitud_m, 1), ancho_m, superficie_m2


def calculate_geometries(lng: float, lat: float, length_m: float, width_m: float, bearing_deg: float) -> Tuple[List[List[float]], List[List[List[float]]], List[float]]:
    """
    Calcula:
    1. LineString coords: [[lng_start, lat_start], [lng_mid, lat_mid], [lng_end, lat_end]]
    2. Polygon buffer coords: [[c1, c2, c3, c4, c1]]
    3. Bounding Box: [min_lng, min_lat, max_lng, max_lat]
    """
    rad = math.radians(bearing_deg)
    # Vector unitario a lo largo de la calle (0° = Norte, 90° = Este)
    # dx = sin(rad), dy = cos(rad)
    half_l = length_m / 2.0
    dx_m = half_l * math.sin(rad)
    dy_m = half_l * math.cos(rad)

    d_lng = dx_m / METERS_PER_DEG_LNG
    d_lat = dy_m / METERS_PER_DEG_LAT

    p_start = [round(lng - d_lng, 6), round(lat - d_lat, 6)]
    p_mid = [round(lng, 6), round(lat, 6)]
    p_end = [round(lng + d_lng, 6), round(lat + d_lat, 6)]
    linestring = [p_start, p_mid, p_end]

    # Vector perpendicular para el polígono corredor (offset de medio ancho)
    half_w = width_m / 2.0
    # Vector perpendicular (girado 90° en sentido horario: dx_perp = cos(rad), dy_perp = -sin(rad))
    px_m = half_w * math.cos(rad)
    py_m = -half_w * math.sin(rad)

    p_lng = px_m / METERS_PER_DEG_LNG
    p_lat = py_m / METERS_PER_DEG_LAT

    c1 = [round(p_start[0] + p_lng, 6), round(p_start[1] + p_lat, 6)]
    c2 = [round(p_end[0] + p_lng, 6), round(p_end[1] + p_lat, 6)]
    c3 = [round(p_end[0] - p_lng, 6), round(p_end[1] - p_lat, 6)]
    c4 = [round(p_start[0] - p_lng, 6), round(p_start[1] - p_lat, 6)]
    polygon = [[c1, c2, c3, c4, c1]]

    all_lngs = [c[0] for c in [c1, c2, c3, c4]]
    all_lats = [c[1] for c in [c1, c2, c3, c4]]
    bbox = [min(all_lngs), min(all_lats), max(all_lngs), max(all_lats)]

    return linestring, polygon, bbox


def determine_impact_level(tipo_afectacion: str, num_oferentes: float) -> str:
    """Clasifica severidad de impacto: 'ALTO', 'MEDIO', 'BAJO'."""
    if tipo_afectacion == 'Ocupación de camellón/banqueta':
        return 'BAJO' if num_oferentes < 300 else 'MEDIO'
    if tipo_afectacion == 'Cierre total de calle':
        if num_oferentes >= 200:
            return 'ALTO'
        elif num_oferentes >= 50:
            return 'MEDIO'
        else:
            return 'BAJO'
    else: # Reducción de carriles
        if num_oferentes >= 150:
            return 'ALTO'
        elif num_oferentes >= 40:
            return 'MEDIO'
        else:
            return 'BAJO'


def generate_detour_advice(calle_principal: str, e1: str, e2: str, tipo_afectacion: str, cardinal: str) -> str:
    """Genera recomendación de desvío vehicular estilo Waze / Google Maps."""
    if tipo_afectacion == 'Inactivo - No se instala':
        return 'Sin afectación vial: tianguis inactivo o no instalado actualmente.'
    if tipo_afectacion == 'Ocupación de camellón/banqueta':
        return f"Vía transitable con precaución: Ocupación sobre camellón o banqueta en {calle_principal}. Alta afluencia peatonal y cruces de compradores; reduzca velocidad a 20 km/h."
    
    tramo_str = f"entre {e1} y {e2}" if e1 and e2 else (f"cruce con {e1}" if e1 else "")
    
    if tipo_afectacion == 'Reducción de carriles':
        return f"Precaución por reducción de carriles sobre {calle_principal} {tramo_str}. Tránsito lento; anticipar incorporaciones a carriles centrales o vías paralelas."
    else: # Cierre total
        eje_paralelo = "ejes en sentido norte-sur" if cardinal == 'N-S' else ("ejes en sentido oriente-poniente" if cardinal == 'E-W' else "vías paralelas inmediatas")
        return f"Cierre total de circulación en {calle_principal} {tramo_str}. Desvío sugerido: Tomar {eje_paralelo} para rodear el cuadrante comercial."


def process_street_closures(
    csv_path: str,
    raw_transporte_dir: str,
    output_geojson_path: str,
    output_json_path: str,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Función principal de procesamiento para los 1,367 tianguis.
    """
    print(f"\n========================================================")
    print(f" PROCESADOR DE CIERRES VIALES DINÁMICOS POR TIANGUIS")
    print(f" Chilangatón 2026 - Módulo 4: Análisis Espacial CDMX")
    print(f"========================================================")
    print(f"Leyendo dataset maestro: {csv_path}...")
    df = pd.read_csv(csv_path)
    total_tianguis = len(df)
    print(f"-> Registros leídos: {total_tianguis:,}")

    # Inicializar motor de bearing vial
    print(f"Inicializando motor geodésico y de acimut vial...")
    bearing_engine = RoadNetworkBearingEngine(raw_transporte_dir)

    features = []
    closures_by_day: Dict[str, List[Dict[str, Any]]] = {
        'LUNES': [],
        'MARTES': [],
        'MIERCOLES': [],
        'JUEVES': [],
        'VIERNES': [],
        'SABADO': [],
        'DOMINGO': []
    }

    processed_records = []

    for idx, row in df.iterrows():
        t_id = str(row['id'])
        nombre = clean_text(row['nombre'])
        alcaldia = clean_text(row['alcaldia'])
        colonia = clean_text(row['colonia'])
        direccion_raw = clean_text(row['direccion'])
        dia_semana = clean_text(row['dia'])
        horario = clean_text(row['horario'])
        h_apertura = float(row['hora_apertura']) if pd.notna(row['hora_apertura']) else 8.0
        h_cierre = float(row['hora_cierre']) if pd.notna(row['hora_cierre']) else 18.0
        num_oferentes = float(row['num_oferentes']) if pd.notna(row['num_oferentes']) else 0.0
        giro = clean_text(row['giro'])

        # Coordenadas
        lat = row['lat']
        lng = row['lng']

        if pd.isna(lat) or pd.isna(lng) or lat < 18.0 or lat > 20.5:
            if t_id in FALLBACK_COORDS:
                lat, lng = FALLBACK_COORDS[t_id]
            else:
                lat, lng = (19.4326, -99.1332)

        lat = float(lat)
        lng = float(lng)

        # 1. Parsear dirección
        cp, e1, e2, tipo_afectacion, corredor = parse_street_address(direccion_raw)

        # 2. Inactivo check
        activo = True
        if tipo_afectacion == 'Inactivo - No se instala' or 'ACTUALMENTE NO SE INSTALA' in direccion_raw.upper():
            activo = False
            tipo_afectacion = 'Inactivo - No se instala'

        # 3. Dimensiones
        if activo:
            longitud_m, ancho_m, sup_m2 = estimate_dimensions(num_oferentes, tipo_afectacion)
            bearing_deg, cardinal = bearing_engine.get_bearing(lng, lat, cp)
            nivel_impacto = determine_impact_level(tipo_afectacion, num_oferentes)
        else:
            longitud_m, ancho_m, sup_m2 = 0.0, 0.0, 0.0
            bearing_deg, cardinal = 0.0, 'N-S'
            nivel_impacto = 'BAJO'

        # 4. Geometría
        linestring_coords, polygon_coords, bbox = calculate_geometries(lng, lat, longitud_m, ancho_m, bearing_deg)
        desvio = generate_detour_advice(cp, e1, e2, tipo_afectacion, cardinal)

        # Propiedades completas
        props = {
            'id': t_id,
            'nombre': nombre,
            'alcaldia': alcaldia,
            'colonia': colonia,
            'direccion_original': direccion_raw,
            'calle_principal': cp,
            'entre_calle1': e1,
            'entre_calle2': e2,
            'corredor_normalizado': corredor,
            'tipo_afectacion': tipo_afectacion,
            'nivel_impacto': nivel_impacto,
            'activo': activo,
            'dia_principal': dia_semana,
            'dias_operacion': clean_text(row.get('dias_operacion_lista', row.get('dias_operacion', dia_semana))),
            'horario': horario,
            'hora_apertura': h_apertura,
            'hora_cierre': h_cierre,
            'num_oferentes': int(num_oferentes),
            'giro': giro,
            'longitud_metros': longitud_m,
            'ancho_estimado_metros': ancho_m,
            'superficie_afectada_m2': sup_m2,
            'orientacion_grados': bearing_deg,
            'orientacion_cardinal': cardinal,
            'desvio_recomendado': desvio,
            'coordenadas_centro': [round(lng, 6), round(lat, 6)],
            'poligono_buffer': polygon_coords,
            'bbox': bbox,
            'lunes': bool(row.get('lunes', False)),
            'martes': bool(row.get('martes', False)),
            'miercoles': bool(row.get('miercoles', False)),
            'jueves': bool(row.get('jueves', False)),
            'viernes': bool(row.get('viernes', False)),
            'sabado': bool(row.get('sabado', False)),
            'domingo': bool(row.get('domingo', False)),
        }

        # Feature GeoJSON (LineString para trazado vectorial directo de la calle cerrada)
        feature = {
            'type': 'Feature',
            'id': t_id,
            'geometry': {
                'type': 'LineString',
                'coordinates': linestring_coords
            },
            'properties': props
        }
        features.append(feature)

        record_data = {**props, 'line_coords': linestring_coords}
        processed_records.append(record_data)

        # Indexar por días de la semana activos
        day_mapping = [
            ('lunes', 'LUNES'),
            ('martes', 'MARTES'),
            ('miercoles', 'MIERCOLES'),
            ('jueves', 'JUEVES'),
            ('viernes', 'VIERNES'),
            ('sabado', 'SABADO'),
            ('domingo', 'DOMINGO'),
        ]

        assigned_any = False
        for col_name, day_key in day_mapping:
            if bool(row.get(col_name, False)):
                closures_by_day[day_key].append(record_data)
                assigned_any = True

        if not assigned_any and dia_semana:
            # Fallback a dia_principal si las columnas booleanas fallaran
            d_norm = dia_semana.upper()
            for col_name, day_key in day_mapping:
                if day_key in d_norm or (day_key == 'MIERCOLES' and 'MIÉRCOLES' in d_norm) or (day_key == 'SABADO' and 'SÁBADO' in d_norm):
                    closures_by_day[day_key].append(record_data)
                    assigned_any = True

    # Estructurar GeoJSON
    geojson_data = {
        'type': 'FeatureCollection',
        'metadata': {
            'proyecto': 'Comercio Popular y Barrial CDMX (Chilangatón 2026)',
            'modulo': 'Módulo 4: Cierres de Vías Dinámico por Tianguis',
            'version': '1.0.0',
            'total_tianguis': len(features),
            'crs': 'EPSG:4326 (WGS84)',
            'descripcion': 'Geometrías de tramos viales y atributos operacionales de afectación vehicular por tianguis'
        },
        'features': features
    }

    # Guardar GeoJSON
    os.makedirs(os.path.dirname(output_geojson_path), exist_ok=True)
    with open(output_geojson_path, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)
    print(f"-> GeoJSON generado con éxito: {output_geojson_path} ({os.path.getsize(output_geojson_path):,} bytes)")

    # Calcular estadísticas y métricas agregadas por día
    df_proc = pd.DataFrame(processed_records)
    
    cierres_por_dia_json: Dict[str, Any] = {
        'metadata': {
            'proyecto': 'Comercio Popular y Barrial CDMX (Chilangatón 2026)',
            'modulo': 'Módulo 4: Cierres de Vías Dinámico por Tianguis',
            'descripcion': 'Cierres viales indexados por día de la semana con métricas de movilidad y desvíos para frontend',
            'total_tianguis_padron': total_tianguis,
            'dias_disponibles': list(closures_by_day.keys())
        },
        'resumen_semanal': {},
        'dias': {}
    }

    total_km_semanal = 0.0
    total_oferentes_semanal = 0

    for day_key, day_records in closures_by_day.items():
        if not day_records:
            continue
        df_d = pd.DataFrame(day_records)
        df_d_activos = df_d[df_d['activo'] == True]

        km_lineales = round(df_d_activos['longitud_metros'].sum() / 1000.0, 2)
        sup_m2 = round(df_d_activos['superficie_afectada_m2'].sum(), 1)
        tot_oferentes = int(df_d_activos['num_oferentes'].sum())
        total_km_semanal += km_lineales
        total_oferentes_semanal += tot_oferentes

        # Desglose por tipo de afectación
        tipo_counts = df_d_activos['tipo_afectacion'].value_counts().to_dict()
        impacto_counts = df_d_activos['nivel_impacto'].value_counts().to_dict()

        # Desglose por alcaldía
        alcaldias_res = {}
        for alc, group in df_d_activos.groupby('alcaldia'):
            alcaldias_res[alc] = {
                'tianguis': len(group),
                'km_lineales': round(group['longitud_metros'].sum() / 1000.0, 2),
                'superficie_m2': round(group['superficie_afectada_m2'].sum(), 1),
                'oferentes': int(group['num_oferentes'].sum()),
                'cierres_totales': int((group['tipo_afectacion'] == 'Cierre total de calle').sum()),
                'reducciones_carril': int((group['tipo_afectacion'] == 'Reducción de carriles').sum()),
                'ocupacion_camellon': int((group['tipo_afectacion'] == 'Ocupación de camellón/banqueta').sum()),
            }

        # Top 5 corredores viales afectados del día
        top_vias_dia = []
        for via, group in df_d_activos.groupby('corredor_normalizado'):
            if via in ['INACTIVO', 'SIN OPERACIÓN', '']:
                continue
            top_vias_dia.append({
                'corredor': via,
                'tianguis': len(group),
                'km_lineales': round(group['longitud_metros'].sum() / 1000.0, 2),
                'oferentes': int(group['num_oferentes'].sum()),
                'alcaldias': list(group['alcaldia'].unique()),
                'tipo_afectacion': group['tipo_afectacion'].mode().iloc[0] if len(group) > 0 else 'Cierre total de calle'
            })
        top_vias_dia = sorted(top_vias_dia, key=lambda x: (x['km_lineales'], x['oferentes']), reverse=True)[:5]

        # Lista compacta de cierres del día para el frontend
        cierres_frontend = []
        for r in day_records:
            cierres_frontend.append({
                'id': r['id'],
                'nombre': r['nombre'],
                'alcaldia': r['alcaldia'],
                'colonia': r['colonia'],
                'calle_principal': r['calle_principal'],
                'entre_calle1': r['entre_calle1'],
                'entre_calle2': r['entre_calle2'],
                'tipo_afectacion': r['tipo_afectacion'],
                'nivel_impacto': r['nivel_impacto'],
                'horario': r['horario'],
                'hora_apertura': r['hora_apertura'],
                'hora_cierre': r['hora_cierre'],
                'num_oferentes': r['num_oferentes'],
                'longitud_m': r['longitud_metros'],
                'ancho_m': r['ancho_estimado_metros'],
                'orientacion_cardinal': r['orientacion_cardinal'],
                'lat': r['coordenadas_centro'][1],
                'lng': r['coordenadas_centro'][0],
                'desvio_recomendado': r['desvio_recomendado'],
                'line_coords': r['line_coords'],
                'poligono_buffer': r['poligono_buffer']
            })

        cierres_por_dia_json['dias'][day_key] = {
            'dia': day_key,
            'total_tianguis': len(day_records),
            'tianguis_activos': len(df_d_activos),
            'km_lineales_ocupados': km_lineales,
            'superficie_m2_ocupada': sup_m2,
            'oferentes_totales': tot_oferentes,
            'distribucion_afectacion': {
                'cierres_totales': tipo_counts.get('Cierre total de calle', 0),
                'reducciones_carriles': tipo_counts.get('Reducción de carriles', 0),
                'ocupacion_camellon_banqueta': tipo_counts.get('Ocupación de camellón/banqueta', 0),
            },
            'distribucion_impacto': impacto_counts,
            'alcaldias': alcaldias_res,
            'top_corredores_dia': top_vias_dia,
            'cierres': cierres_frontend
        }

    # Resumen Semanal Consolidado
    df_activos_total = df_proc[df_proc['activo'] == True]
    
    top_10_cdmx = []
    for via, group in df_activos_total.groupby('corredor_normalizado'):
        if via in ['INACTIVO', 'SIN OPERACIÓN', '']:
            continue
        top_10_cdmx.append({
            'corredor': via,
            'tianguis_instalaciones_semana': len(group),
            'oferentes_totales': int(group['num_oferentes'].sum()),
            'km_ocupados_semana': round(group['longitud_metros'].sum() / 1000.0, 2),
            'alcaldias': sorted(list(group['alcaldia'].unique())),
            'tipo_predominante': group['tipo_afectacion'].mode().iloc[0] if len(group) > 0 else 'Cierre total de calle'
        })
    top_10_cdmx = sorted(top_10_cdmx, key=lambda x: (x['oferentes_totales'], x['km_ocupados_semana']), reverse=True)[:10]

    # Matriz alcaldía vs día (km)
    alcaldia_matriz = {}
    for alc in sorted(df_activos_total['alcaldia'].unique()):
        alcaldia_matriz[alc] = {}
        for day_key in ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']:
            d_recs = closures_by_day.get(day_key, [])
            km = sum(r['longitud_metros'] for r in d_recs if r['alcaldia'] == alc and r['activo']) / 1000.0
            alcaldia_matriz[alc][day_key] = round(km, 2)
        alcaldia_matriz[alc]['TOTAL_KM_SEMANA'] = round(sum(alcaldia_matriz[alc].values()), 2)

    cierres_por_dia_json['resumen_semanal'] = {
        'total_tianguis_catalogo': total_tianguis,
        'tianguis_activos_unicos': len(df_activos_total['id'].unique()),
        'total_instalaciones_semanales': sum(len(d) for d in closures_by_day.values()),
        'km_lineales_acumulados_semana': round(total_km_semanal, 2),
        'oferentes_acumulados_semana': total_oferentes_semanal,
        'top_10_corredores_cdmx': top_10_cdmx,
        'matriz_alcaldia_dia_km': alcaldia_matriz
    }

    # Guardar JSON por día
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(cierres_por_dia_json, f, ensure_ascii=False, indent=2)
    print(f"-> JSON por día generado con éxito: {output_json_path} ({os.path.getsize(output_json_path):,} bytes)")

    # Reporte en Consola
    if verbose:
        print("\n========================================================")
        print(" RESUMEN DE IMPACTO VIAL POR DÍA DE LA SEMANA (CDMX)")
        print("========================================================")
        print(f"{'DÍA':<10} | {'TIANGUIS':<8} | {'KM OCUPADOS':<12} | {'CIERRES':<8} | {'REDUCC':<8} | {'CAMELLÓN':<9} | {'OFERENTES':<10}")
        print("-" * 75)
        for d_k in ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']:
            d_info = cierres_por_dia_json['dias'].get(d_k, {})
            af = d_info.get('distribucion_afectacion', {})
            print(f"{d_k:<10} | {d_info.get('total_tianguis', 0):<8} | {d_info.get('km_lineales_ocupados', 0.0):<6.2f} km   | {af.get('cierres_totales', 0):<8} | {af.get('reducciones_carriles', 0):<8} | {af.get('ocupacion_camellon_banqueta', 0):<9} | {d_info.get('oferentes_totales', 0):<10,}")
        print("-" * 75)
        print(f"{'TOTAL':<10} | {sum(d['total_tianguis'] for d in cierres_por_dia_json['dias'].values()):<8} | {total_km_semanal:<6.2f} km   | -        | -        | -         | {total_oferentes_semanal:<10,}")

        print("\n========================================================")
        print(" TOP 10 CORREDORES VIALES CON MAYOR IMPACTO EN CDMX")
        print("========================================================")
        for i, item in enumerate(top_10_cdmx, 1):
            alcs = ", ".join(item['alcaldias'])
            print(f"{i:2d}. {item['corredor']:<35} | {item['km_ocupados_semana']:>6.2f} km | {item['oferentes_totales']:>6,d} puestos | {item['tipo_predominante']:<22} | {alcs}")

    return cierres_por_dia_json


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Procesador Espacial de Cierres Viales por Tianguis CDMX')
    parser.add_argument('--input-csv', default='data/processed/tianguis_limpio.csv', help='Ruta a tianguis_limpio.csv')
    parser.add_argument('--transporte-dir', default='data/raw/transporte', help='Directorio con cartografía de transporte')
    parser.add_argument('--output-geojson', default='data/processed/cierres_viales_tianguis.geojson', help='Ruta de salida GeoJSON')
    parser.add_argument('--output-json', default='data/processed/cierres_viales_por_dia.json', help='Ruta de salida JSON por día')
    parser.add_argument('--quiet', action='store_true', help='Desactivar salida detallada en consola')

    args = parser.parse_args()

    process_street_closures(
        csv_path=args.input_csv,
        raw_transporte_dir=args.transporte_dir,
        output_geojson_path=args.output_geojson,
        output_json_path=args.output_json,
        verbose=not args.quiet
    )
