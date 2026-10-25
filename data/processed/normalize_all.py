#!/usr/bin/env python3
"""
normalize_all.py
----------------
Script de limpieza, estandarización y normalización de datasets del comercio popular y barrial
de la Ciudad de México (SEDECO, MERCOMUNA, Apoyos de Emergencia).

Genera datasets procesados en formato JSON y CSV, así como el catálogo unificado
'directorio_comercio_popular'.
"""

import os
import re
import math
import json
import unicodedata
import pandas as pd
from typing import Tuple, Optional, List, Dict, Any

RAW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../raw'))
PROCESSED_DIR = os.path.abspath(os.path.dirname(__file__))

# Bounding box oficial aproximado de la Ciudad de México (WGS84)
CDMX_LAT_MIN, CDMX_LAT_MAX = 19.04, 19.59
CDMX_LNG_MIN, CDMX_LNG_MAX = -99.37, -98.94

# 16 Alcaldías Oficiales Canónicas
CANONICAL_ALCALDIAS = [
    'ALVARO OBREGON',
    'AZCAPOTZALCO',
    'BENITO JUAREZ',
    'COYOACAN',
    'CUAJIMALPA DE MORELOS',
    'CUAUHTEMOC',
    'GUSTAVO A. MADERO',
    'IZTACALCO',
    'IZTAPALAPA',
    'LA MAGDALENA CONTRERAS',
    'MIGUEL HIDALGO',
    'MILPA ALTA',
    'TLAHUAC',
    'TLALPAN',
    'VENUSTIANO CARRANZA',
    'XOCHIMILCO'
]

ALCALDIA_MAPPING = {
    'ALVARO OBREGON': 'ALVARO OBREGON',
    'AZCAPOTZALCO': 'AZCAPOTZALCO',
    'BENITO JUAREZ': 'BENITO JUAREZ',
    'COYOACAN': 'COYOACAN',
    'CUAJIMALPA': 'CUAJIMALPA DE MORELOS',
    'CUAJIMALPA DE MORELOS': 'CUAJIMALPA DE MORELOS',
    'CUAUHTEMOC': 'CUAUHTEMOC',
    'G.A. MADERO': 'GUSTAVO A. MADERO',
    'G. A. MADERO': 'GUSTAVO A. MADERO',
    'GUSTAVO A MADERO': 'GUSTAVO A. MADERO',
    'GUSTAVO A. MADERO': 'GUSTAVO A. MADERO',
    'IZTACALCO': 'IZTACALCO',
    'IZTAPALAPA': 'IZTAPALAPA',
    'M.CONTRERAS': 'LA MAGDALENA CONTRERAS',
    'M. CONTRERAS': 'LA MAGDALENA CONTRERAS',
    'MAGDALENA CONTRERAS': 'LA MAGDALENA CONTRERAS',
    'LA MAGDALENA CONTRERAS': 'LA MAGDALENA CONTRERAS',
    'MIGUEL HIDALGO': 'MIGUEL HIDALGO',
    'MILPA ALTA': 'MILPA ALTA',
    'TLAHUAC': 'TLAHUAC',
    'TLALPAN': 'TLALPAN',
    'VENUSTIANO CARRANZA': 'VENUSTIANO CARRANZA',
    'XOCHIMILCO': 'XOCHIMILCO',
}

DIAS_SEMANA_ORDEN = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']


def clean_text(text: Any) -> str:
    """Limpia espacios en blanco redundantes y artefactos de codificación/mojibake."""
    if text is None or pd.isna(text):
        return ''
    s = str(text)
    # Correcciones de mojibake conocidas (Windows-1252 / ISO-8859-1 decodificados como UTF-8 o viceversa)
    mojibake_fixes = {
        'Ã‘': 'Ñ', 'Ã±': 'ñ',
        'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
        'Ã ': 'Á', 'Ã‰': 'É', 'Ã ': 'Í', 'Ã“': 'Ó', 'Ãš': 'Ú',
        'Â': '', 'â€œ': '"', 'â€': '"', 'â€™': "'",
        '\xa0': ' ', '\t': ' ', '\r': ' ', '\n': ' '
    }
    for bad, good in mojibake_fixes.items():
        s = s.replace(bad, good)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def normalize_alcaldia(val: Any) -> str:
    """Estandariza el nombre de la alcaldía al formato canónico en mayúsculas sin acentos."""
    if val is None or pd.isna(val):
        return 'NO ESPECIFICADA'
    s = clean_text(val).upper()
    # Eliminar acentos para mapeo
    s_no_acc = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s_clean = re.sub(r'^(?:DEL\.|DELEGACI[OÓ]N)\s*', '', s_no_acc).strip()
    s_clean = re.sub(r'\s+', ' ', s_clean)
    
    canonical = ALCALDIA_MAPPING.get(s_clean)
    if not canonical:
        # Búsqueda difusa/parcial si no hubo coincidencia directa
        for key, target in ALCALDIA_MAPPING.items():
            if key in s_clean or s_clean in key:
                canonical = target
                break
    return canonical if canonical else s_clean


def utm_14n_to_wgs84(easting: float, northing: float) -> Tuple[Optional[float], Optional[float]]:
    """
    Convierte coordenadas UTM Zona 14N (elipsoide WGS84) a grados decimales (latitud, longitud).
    Retorna (None, None) si las coordenadas son 0 o inválidas.
    """
    if easting == 0 or northing == 0 or pd.isna(easting) or pd.isna(northing):
        return None, None
    if easting < 400000 or easting > 600000 or northing < 2000000 or northing > 2300000:
        return None, None

    a = 6378137.0
    f = 1 / 298.257223563
    b = a * (1 - f)
    e = math.sqrt(1 - (b / a) ** 2)
    e_prime_sq = (e ** 2) / (1 - (e ** 2))

    k0 = 0.9996
    lon0 = math.radians(-99.0)  # Meridiano central de la Zona 14N

    x = easting - 500000.0
    y = northing

    M = y / k0
    mu = M / (a * (1 - e ** 2 / 4 - 3 * e ** 4 / 64 - 5 * e ** 6 / 256))
    e1 = (1 - math.sqrt(1 - e ** 2)) / (1 + math.sqrt(1 - e ** 2))

    phi1 = mu + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * math.sin(2 * mu) + \
           (21 * e1 ** 2 / 16 - 55 * e1 ** 4 / 32) * math.sin(4 * mu) + \
           (151 * e1 ** 3 / 96) * math.sin(6 * mu) + \
           (1097 * e1 ** 4 / 512) * math.sin(8 * mu)

    sin_phi1 = math.sin(phi1)
    cos_phi1 = math.cos(phi1)
    tan_phi1 = math.tan(phi1)

    N1 = a / math.sqrt(1 - e ** 2 * sin_phi1 ** 2)
    T1 = tan_phi1 ** 2
    C1 = e_prime_sq * cos_phi1 ** 2
    R1 = a * (1 - e ** 2) / ((1 - e ** 2 * sin_phi1 ** 2) ** 1.5)
    D = x / (N1 * k0)

    lat = phi1 - (N1 * tan_phi1 / R1) * (
            D ** 2 / 2 - (5 + 3 * T1 + 10 * C1 - 4 * C1 ** 2 - 9 * e_prime_sq) * D ** 4 / 24 +
            (61 + 90 * T1 + 298 * C1 + 45 * T1 ** 2 - 252 * e_prime_sq - 3 * C1 ** 2) * D ** 6 / 720
    )
    lon = lon0 + (
            D - (1 + 2 * T1 + C1) * D ** 3 / 6 +
            (5 - 2 * C1 + 28 * T1 - 3 * C1 ** 2 + 8 * e_prime_sq + 24 * T1 ** 2) * D ** 5 / 120
    ) / cos_phi1

    lat_deg = math.degrees(lat)
    lon_deg = math.degrees(lon)
    return round(lat_deg, 6), round(lon_deg, 6)


def validate_coordinates(lat: Any, lng: Any) -> Tuple[Optional[float], Optional[float], bool]:
    """
    Valida si lat/lng son válidos y caen dentro del polígono delimitador de la CDMX.
    Retorna (lat_limpia, lng_limpia, es_valida).
    """
    try:
        if lat is None or lng is None or pd.isna(lat) or pd.isna(lng):
            return None, None, False
        f_lat = float(lat)
        f_lng = float(lng)
        if CDMX_LAT_MIN <= f_lat <= CDMX_LAT_MAX and CDMX_LNG_MIN <= f_lng <= CDMX_LNG_MAX:
            return round(f_lat, 6), round(f_lng, 6), True
        return None, None, False
    except (ValueError, TypeError):
        return None, None, False


def parse_days_of_operation(text: Any) -> Tuple[List[str], str, Dict[str, bool]]:
    """
    Analiza un texto de días y extrae una lista ordenada de días, una cadena formateada
    y un diccionario con banderas booleanas para cada día de la semana.
    """
    if text is None or pd.isna(text) or str(text).strip() == '':
        return [], 'NO ESPECIFICADO', {d.lower(): False for d in DIAS_SEMANA_ORDEN}

    s = clean_text(text).upper()
    s_norm = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    found = set()
    for d in DIAS_SEMANA_ORDEN:
        if d in s_norm:
            found.add(d)

    # Si dice 'LUNES A DOMINGO' o 'TODOS LOS DIAS'
    if 'LUNES A DOMINGO' in s_norm or 'DIARIO' in s_norm or 'TODA LA SEMANA' in s_norm:
        found = set(DIAS_SEMANA_ORDEN)

    ordered_days = [d for d in DIAS_SEMANA_ORDEN if d in found]
    bool_flags = {d.lower(): (d in found) for d in DIAS_SEMANA_ORDEN}

    if len(ordered_days) == 7:
        formatted_str = 'LUNES A DOMINGO'
    elif len(ordered_days) > 0:
        formatted_str = ', '.join(ordered_days)
    else:
        formatted_str = s

    return ordered_days, formatted_str, bool_flags


def extract_colonia_from_address(addr: str, fallback: str = '') -> str:
    """Extrae el nombre de la colonia si viene dentro del campo de dirección."""
    if not addr:
        return clean_text(fallback)
    m = re.search(r'(?:col\.?|colonia)\s+([^,]+)', addr, flags=re.IGNORECASE)
    if m:
        c = m.group(1).strip()
        c = re.split(r'\s+(?:esq|esquina|entre|no\.|núm|#)\b', c, flags=re.IGNORECASE)[0].strip()
        return clean_text(c).upper()
    return clean_text(fallback).upper()


def parse_horario(text: Any) -> Tuple[float, float, bool]:
    """
    Parsea un rango de horario en texto (ej. '8:00 A 17:00 HORAS', '07:00 A 19:00 HRS', '24 HORAS')
    y retorna una tupla (hora_apertura: float, hora_cierre: float, horario_estimado: bool).
    
    Si no se encuentra un rango válido o el campo es nulo, asigna un default estándar comercial
    (08:00 a 18:00) y marca horario_estimado=True.
    """
    if text is None or pd.isna(text) or str(text).strip() == '':
        return 8.0, 18.0, True

    s = clean_text(text).upper()

    # Caso 24 horas continuo
    if '24 HORAS' in s or '24 HRS' in s or 'CONTINU' in s:
        return 0.0, 24.0, False

    # Expresión regular para horas con o sin minutos: H:MM o HH:MM
    m = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(?:A|A LAS|-|HASTA)\s*(\d{1,2})(?::(\d{2}))?', s)
    if m:
        h1 = float(m.group(1)) + (float(m.group(2)) / 60.0 if m.group(2) else 0.0)
        h2 = float(m.group(3)) + (float(m.group(4)) / 60.0 if m.group(4) else 0.0)
        return round(h1, 2), round(h2, 2), False

    return 8.0, 18.0, True


def esta_abierto(record: Dict[str, Any], dia_o_fecha: Any = None, hora: Optional[float] = None) -> bool:
    """
    Determina si un comercio o tianguis está abierto en un día y hora dados.
    
    Args:
        record: Diccionario del registro de comercio (del directorio unificado).
        dia_o_fecha: Nombre del día en español (ej. 'LUNES', 'martes', 'miércoles')
                     o un objeto datetime / date. Si es None, utiliza el día actual del sistema.
        hora: Hora decimal (ej. 14.5 para 14:30). Si es None y se pasó datetime, se infiere
              del datetime; de lo contrario se asume la hora actual del sistema.
              
    Returns:
        bool: True si el comercio opera en ese día y dentro del rango horario [hora_apertura, hora_cierre].
    """
    from datetime import datetime

    if dia_o_fecha is None:
        now = datetime.now()
        dia_str = DIAS_SEMANA_ORDEN[now.weekday()]
        if hora is None:
            hora = now.hour + (now.minute / 60.0)
    elif hasattr(dia_o_fecha, 'weekday'):  # datetime o date
        dia_str = DIAS_SEMANA_ORDEN[dia_o_fecha.weekday()]
        if hora is None and hasattr(dia_o_fecha, 'hour'):
            hora = dia_o_fecha.hour + (dia_o_fecha.minute / 60.0)
    else:
        # String
        dia_norm = ''.join(c for c in unicodedata.normalize('NFD', str(dia_o_fecha).upper()) if unicodedata.category(c) != 'Mn')
        dia_str = dia_norm

    flag_key = dia_str.lower()
    opera_dia = False
    if flag_key in record:
        opera_dia = bool(record[flag_key])
    elif 'dias_operacion_lista' in record and isinstance(record['dias_operacion_lista'], list):
        opera_dia = dia_str in record['dias_operacion_lista']

    if not opera_dia:
        return False

    if hora is None:
        return True

    h_apertura = record.get('hora_apertura', 8.0)
    h_cierre = record.get('hora_cierre', 18.0)
    if h_apertura is None or pd.isna(h_apertura):
        h_apertura = 8.0
    if h_cierre is None or pd.isna(h_cierre):
        h_cierre = 18.0

    return h_apertura <= hora <= h_cierre


def process_tianguis() -> List[Dict[str, Any]]:
    """Procesa el catálogo de tianguis en la CDMX."""
    csv_path = os.path.join(RAW_DIR, 'tianguis.csv')
    json_path = os.path.join(RAW_DIR, 'tianguis.json')
    
    df = pd.read_csv(csv_path)
    
    # Cargar json para extraer NUM_OFER_1 (oferentes/puestos estimados)
    oferentes_map = {}
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            t_json = json.load(f)
            for i, feat in enumerate(t_json.get('features', [])):
                props = feat.get('properties', {})
                num_of = props.get('NUM_OFER_1')
                oferentes_map[i] = int(num_of) if num_of is not None and not pd.isna(num_of) else None

    processed = []
    for idx, row in df.iterrows():
        t_id = f"TIANG-{idx + 1:04d}"
        alcaldia = normalize_alcaldia(row.get('alcaldia'))
        colonia = clean_text(row.get('colonia')).upper()
        ubicacion = clean_text(row.get('ubicacion'))
        
        # Validar coordenadas
        raw_lat = row.get('latitud')
        raw_lng = row.get('longitud')
        lat, lng, valid_coords = validate_coordinates(raw_lat, raw_lng)
        
        # Parsear días
        raw_dia = row.get('dia')
        days_list, days_str, day_flags = parse_days_of_operation(raw_dia)
        
        # Horario
        horario = clean_text(row.get('horario'))
        if not horario:
            horario = '08:00 A 17:00 HORAS'
        h_apertura, h_cierre, h_est = parse_horario(horario)
            
        # Giro
        raw_giro = clean_text(row.get('giro'))
        if not raw_giro or raw_giro == '0' or raw_giro.upper() == 'NAN':
            giro = 'MIXTO'
        else:
            giro = raw_giro.upper()
            
        # Nombre representativo
        nombre = f"TIANGUIS {colonia}"
        if raw_dia and len(days_list) == 1:
            nombre += f" ({days_list[0]})"
            
        num_oferentes = oferentes_map.get(idx)

        record = {
            'id': t_id,
            'nombre': nombre,
            'tipo_espacio': 'Tianguis',
            'tipo_comercio': 'MOVIL',
            'alcaldia': alcaldia,
            'colonia': colonia,
            'direccion': ubicacion,
            'dia': clean_text(raw_dia).upper(),
            'dias_operacion': days_str,
            'dias_operacion_lista': days_list,
            'horario': horario,
            'hora_apertura': h_apertura,
            'hora_cierre': h_cierre,
            'horario_estimado': h_est,
            'lat': lat,
            'lng': lng,
            'coordenadas_validas': valid_coords,
            'num_oferentes': num_oferentes,
            'giro': giro,
            'fuente_original': 'SEDECO - Tianguis',
            **day_flags
        }
        processed.append(record)
    return processed


def process_mercados_publicos() -> List[Dict[str, Any]]:
    """Procesa el catálogo de mercados públicos de la CDMX."""
    csv_path = os.path.join(RAW_DIR, 'mercados_publicos.csv')
    df = pd.read_csv(csv_path)

    processed = []
    all_week_days = DIAS_SEMANA_ORDEN
    all_week_flags = {d.lower(): True for d in DIAS_SEMANA_ORDEN}

    for idx, row in df.iterrows():
        m_id = f"MERC-{idx + 1:04d}"
        mercado_nombre_raw = clean_text(row.get('mercado')).upper()
        if not mercado_nombre_raw.startswith('MERCADO'):
            nombre = f"MERCADO {mercado_nombre_raw}"
        else:
            nombre = mercado_nombre_raw

        alcaldia = normalize_alcaldia(row.get('alcaldia_mercado'))
        colonia = clean_text(row.get('colonia_mercado')).upper()
        direccion = clean_text(row.get('direccion'))

        lat, lng, valid_coords = validate_coordinates(row.get('latitud'), row.get('longitud'))

        locales = int(row.get('locales')) if not pd.isna(row.get('locales')) else None
        num_oficial = int(row.get('numero')) if not pd.isna(row.get('numero')) else None
        superficie_m2 = int(row.get('superficie_m2')) if not pd.isna(row.get('superficie_m2')) else None

        raw_inaug = clean_text(row.get('anio_inauguracion'))
        anio_inaug = None
        if raw_inaug:
            m_year = re.search(r'\b(19\d\d|20\d\d)\b', raw_inaug)
            if m_year:
                anio_inaug = int(m_year.group(1))

        tipo = clean_text(row.get('tipo')).upper()
        raw_giro = clean_text(row.get('giro'))
        if not raw_giro or raw_giro.upper() == 'NAN':
            giro = 'ABASTO TRADICIONAL Y MIXTO'
        else:
            giro = raw_giro.upper()

        horario = '07:00 A 19:00 HORAS'
        h_apertura, h_cierre, h_est = parse_horario(horario)

        record = {
            'id': m_id,
            'nombre': nombre,
            'tipo_espacio': 'Mercado Público',
            'tipo_comercio': 'FIJO',
            'alcaldia': alcaldia,
            'colonia': colonia,
            'direccion': direccion,
            'numero_oficial': num_oficial,
            'locales': locales,
            'tipo': tipo if tipo else 'TRADICIONAL',
            'superficie_m2': superficie_m2,
            'anio_inauguracion': anio_inaug,
            'giro': giro,
            'detalle': clean_text(row.get('detalle')).upper(),
            'forma': clean_text(row.get('forma')).upper(),
            'niveles': clean_text(row.get('niveles')).upper(),
            'tamano': clean_text(row.get('tamaño')).upper(),
            'protegido': clean_text(row.get('protegido')).upper(),
            'dias_operacion': 'LUNES A DOMINGO',
            'dias_operacion_lista': all_week_days,
            'horario': horario,
            'hora_apertura': h_apertura,
            'hora_cierre': h_cierre,
            'horario_estimado': h_est,
            'lat': lat,
            'lng': lng,
            'coordenadas_validas': valid_coords,
            'fuente_original': 'SEDECO - Mercados Públicos',
            **all_week_flags
        }
        processed.append(record)
    return processed


def process_mercados_sobre_ruedas() -> List[Dict[str, Any]]:
    """Procesa el catálogo de Mercados Sobre Ruedas (MSR)."""
    csv_path = os.path.join(RAW_DIR, 'mercados_sobre_ruedas.csv')
    df = pd.read_csv(csv_path)

    processed = []
    for idx, row in df.iterrows():
        msr_id = f"MSR-{idx + 1:04d}"
        ruta = clean_text(row.get('Ruta')).upper()
        colonia = clean_text(row.get('Colonia')).upper()
        direccion = clean_text(row.get('Dirección'))
        alcaldia = normalize_alcaldia(row.get('Alcaldía'))

        raw_dia = clean_text(row.get('Día_Oper'))
        days_list, days_str, day_flags = parse_days_of_operation(raw_dia)

        num_oferentes = int(row.get('Num_Oferen')) if not pd.isna(row.get('Num_Oferen')) else None

        lat, lng, valid_coords = validate_coordinates(row.get('Coor_GeogY'), row.get('Coor_GeogX'))

        nombre = f"MERCADO SOBRE RUEDAS {ruta}"
        if colonia:
            nombre += f" - {colonia}"

        horario = '08:00 A 18:00 HORAS'
        h_apertura, h_cierre, h_est = parse_horario(horario)

        record = {
            'id': msr_id,
            'nombre': nombre,
            'tipo_espacio': 'Mercado Sobre Ruedas',
            'tipo_comercio': 'MOVIL',
            'alcaldia': alcaldia,
            'colonia': colonia,
            'direccion': direccion,
            'ruta': ruta,
            'dia': clean_text(raw_dia).upper(),
            'dias_operacion': days_str,
            'dias_operacion_lista': days_list,
            'horario': horario,
            'hora_apertura': h_apertura,
            'hora_cierre': h_cierre,
            'horario_estimado': h_est,
            'num_oferentes': num_oferentes,
            'giro': 'ABASTO POPULAR Y CANASTA BÁSICA',
            'lat': lat,
            'lng': lng,
            'coordenadas_validas': valid_coords,
            'fuente_original': 'SEDECO - Mercados Sobre Ruedas',
            **day_flags
        }
        processed.append(record)
    return processed


def process_concentraciones() -> List[Dict[str, Any]]:
    """Procesa el catálogo de concentraciones de comerciantes (tianguis fijos y concentraciones)."""
    csv_path = os.path.join(RAW_DIR, 'concentraciones_comerciantes.csv')
    df = pd.read_csv(csv_path)

    processed = []
    all_week_days = DIAS_SEMANA_ORDEN
    all_week_flags = {d.lower(): True for d in DIAS_SEMANA_ORDEN}

    for idx, row in df.iterrows():
        c_id = f"CONC-{idx + 1:04d}"
        mercado_raw = clean_text(row.get('MERCADO'))
        if not mercado_raw.upper().startswith('CONCENTRACI'):
            nombre = f"CONCENTRACIÓN {mercado_raw.upper()}"
        else:
            nombre = mercado_raw.upper()

        alcaldia = normalize_alcaldia(row.get('ALCALDÍA'))
        direccion = clean_text(row.get('DIRECCION'))
        colonia = extract_colonia_from_address(direccion, fallback=mercado_raw)

        # Conversión de UTM Zona 14N a WGS84
        easting = float(row.get('COORD_X')) if not pd.isna(row.get('COORD_X')) else 0.0
        northing = float(row.get('COORD_Y')) if not pd.isna(row.get('COORD_Y')) else 0.0

        lat_conv, lng_conv = utm_14n_to_wgs84(easting, northing)
        lat, lng, valid_coords = validate_coordinates(lat_conv, lng_conv)

        num_oficial = int(row.get('NUM_OF')) if not pd.isna(row.get('NUM_OF')) else None
        observaciones = clean_text(row.get('OBSERVACI'))

        horario = '08:00 A 18:00 HORAS'
        h_apertura, h_cierre, h_est = parse_horario(horario)

        record = {
            'id': c_id,
            'nombre': nombre,
            'tipo_espacio': 'Concentración',
            'tipo_comercio': 'FIJO',
            'alcaldia': alcaldia,
            'colonia': colonia,
            'direccion': direccion,
            'numero_oficial': num_oficial,
            'coord_utm_x': easting if easting > 0 else None,
            'coord_utm_y': northing if northing > 0 else None,
            'lat': lat,
            'lng': lng,
            'coordenadas_validas': valid_coords,
            'dias_operacion': 'LUNES A DOMINGO',
            'dias_operacion_lista': all_week_days,
            'horario': horario,
            'hora_apertura': h_apertura,
            'hora_cierre': h_cierre,
            'horario_estimado': h_est,
            'giro': 'COMERCIO Y SERVICIOS EN VÍA PÚBLICA',
            'observaciones': observaciones if observaciones else None,
            'fuente_original': 'SEDECO - Concentraciones de Comerciantes',
            **all_week_flags
        }
        processed.append(record)
    return processed


def process_mercomuna() -> List[Dict[str, Any]]:
    """Procesa la muestra de comercios de barrio afiliados a MERCOMUNA."""
    csv_path = os.path.join(RAW_DIR, 'mercomuna_comercios_muestra.csv')
    df = pd.read_csv(csv_path)

    processed = []
    for idx, row in df.iterrows():
        mercom_id = f"MERCOM-{idx + 1:04d}"
        comercio = clean_text(row.get('comercio')).upper()
        direccion = clean_text(row.get('direccion'))
        colonia = clean_text(row.get('colonia')).upper()
        alcaldia = normalize_alcaldia(row.get('alcaldia'))
        giro = clean_text(row.get('giro')).upper()

        record = {
            'id': mercom_id,
            'nombre': comercio,
            'tipo_espacio': 'Comercio Barrial Mercomuna',
            'alcaldia': alcaldia,
            'colonia': colonia,
            'direccion': direccion,
            'giro': giro if giro else 'ABARROTES',
            'fuente_original': 'SEDECO / Alcaldía - Muestra Mercomuna'
        }
        processed.append(record)
    return processed


def process_apoyos_emergentes() -> List[Dict[str, Any]]:
    """Procesa el padrón de beneficiarios de apoyos emergentes al comercio."""
    csv_path = os.path.join(RAW_DIR, 'apoyos_emergentes_comercio.csv')
    df = pd.read_csv(csv_path)

    processed = []
    for idx, row in df.iterrows():
        apoyo_id = f"APOYO-{idx + 1:04d}"
        orig_id = int(row.get('id'))
        status = clean_text(row.get('status')).upper()
        paterno = clean_text(row.get('apellido_paterno')).upper()
        materno = clean_text(row.get('apellido_materno')).upper()
        nombre_ind = clean_text(row.get('nombre')).upper()
        nombre_completo = f"{nombre_ind} {paterno} {materno}".strip()

        sexo = clean_text(row.get('sexo')).upper()
        edad = int(row.get('edad')) if not pd.isna(row.get('edad')) else None
        giro = clean_text(row.get('giro')).upper()
        colonia = clean_text(row.get('colonia')).upper()
        alcaldia = normalize_alcaldia(row.get('alcaldia'))

        record = {
            'id': apoyo_id,
            'id_original': orig_id,
            'status': status,
            'nombre_completo': nombre_completo,
            'nombre': nombre_ind,
            'apellido_paterno': paterno,
            'apellido_materno': materno,
            'sexo': sexo,
            'edad': edad,
            'giro': giro,
            'colonia': colonia,
            'alcaldia': alcaldia,
            'fuente_original': 'Gobierno CDMX - Apoyos Emergentes al Comercio'
        }
        processed.append(record)
    return processed


def build_unified_directory(
        tianguis: List[Dict[str, Any]],
        mercados: List[Dict[str, Any]],
        msr: List[Dict[str, Any]],
        concentraciones: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Construye el Directorio Unificado de Comercio Popular y Barrial con un esquema estándar,
    incorporando la clasificación tipológica (Fijo vs. Móvil), normalización de horarios
    y banderas booleanas de días de operación.
    """
    unified = []

    def build_entry(item: Dict[str, Any], tipo_espacio: str, tipo_comercio: str):
        num_loc = item.get('locales') if 'locales' in item else item.get('num_oferentes', None)
        return {
            'id': item['id'],
            'nombre': item['nombre'],
            'tipo_espacio': tipo_espacio,
            'tipo_comercio': tipo_comercio,
            'alcaldia': item['alcaldia'],
            'colonia': item['colonia'],
            'direccion': item['direccion'],
            'dias_operacion': item['dias_operacion'],
            'dias_operacion_lista': item['dias_operacion_lista'],
            'horario': item['horario'],
            'hora_apertura': item['hora_apertura'],
            'hora_cierre': item['hora_cierre'],
            'horario_estimado': item['horario_estimado'],
            'lat': item['lat'],
            'lng': item['lng'],
            'coordenadas_validas': item['coordenadas_validas'],
            'num_locales_oferentes': num_loc,
            'giro': item['giro'],
            'fuente_original': item['fuente_original'],
            'lunes': item.get('lunes', False),
            'martes': item.get('martes', False),
            'miercoles': item.get('miercoles', False),
            'jueves': item.get('jueves', False),
            'viernes': item.get('viernes', False),
            'sabado': item.get('sabado', False),
            'domingo': item.get('domingo', False)
        }

    # 1. Mercados Públicos (Fijo)
    for m in mercados:
        unified.append(build_entry(m, 'Mercado Público', 'FIJO'))

    # 2. Tianguis (Móvil)
    for t in tianguis:
        unified.append(build_entry(t, 'Tianguis', 'MOVIL'))

    # 3. Mercados Sobre Ruedas (Móvil)
    for r in msr:
        unified.append(build_entry(r, 'Mercado Sobre Ruedas', 'MOVIL'))

    # 4. Concentraciones (Fijo)
    for c in concentraciones:
        unified.append(build_entry(c, 'Concentración', 'FIJO'))

    return unified


def process_msr_rutas_itinerantes(msr_records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Agrupa los registros de Mercados Sobre Ruedas por ruta y ordena cronológicamente
    las paradas por día de la semana (Lunes a Domingo).
    
    Retorna:
        (rutas_agrupadas, paradas_planas)
    """
    day_order = {'LUNES': 1, 'MARTES': 2, 'MIERCOLES': 3, 'JUEVES': 4, 'VIERNES': 5, 'SABADO': 6, 'DOMINGO': 7}

    def get_ruta_id(r_name: str) -> str:
        clean_r = r_name.strip().upper()
        if 'MINI' in clean_r:
            return 'RUTA-MSR-MINI'
        m = re.search(r'(\d+)(?:-([A-Z]))?', clean_r)
        if m:
            num = int(m.group(1))
            suffix = m.group(2) if m.group(2) else ''
            return f"RUTA-MSR-{num:02d}{suffix}"
        return f"RUTA-MSR-{clean_r.replace(' ', '-')}"

    routes_map: Dict[str, List[Dict[str, Any]]] = {}
    for item in msr_records:
        r = item['ruta']
        routes_map.setdefault(r, []).append(item)

    def route_sort_key(r_name: str):
        m = re.search(r'(\d+)(?:-([A-Z]))?', r_name)
        if m:
            num = int(m.group(1))
            sub = m.group(2) or ''
            return (1, num, sub)
        return (2, 999, r_name)

    sorted_route_names = sorted(routes_map.keys(), key=route_sort_key)

    rutas_agrupadas = []
    paradas_planas = []

    for r_name in sorted_route_names:
        stops = routes_map[r_name]
        stops_sorted = sorted(stops, key=lambda s: day_order.get(s['dias_operacion'], 99))
        
        r_id = get_ruta_id(r_name)
        r_nombre = f"Mercado Sobre Ruedas {r_name}"

        paradas_detalle = []
        itinerario_text_parts = []
        oferentes_list = []

        for idx, s in enumerate(stops_sorted, start=1):
            dia_str = s['dias_operacion']
            ofer = s.get('num_oferentes')
            if ofer is not None:
                oferentes_list.append(ofer)

            parada_obj = {
                'id_parada': s['id'],
                'orden_parada_semana': idx,
                'dia': dia_str,
                'orden_dia': day_order.get(dia_str, 99),
                'alcaldia': s['alcaldia'],
                'colonia': s['colonia'],
                'direccion': s['direccion'],
                'lat': s['lat'],
                'lng': s['lng'],
                'coordenadas_validas': s['coordenadas_validas'],
                'num_oferentes': ofer,
                'horario': s.get('horario', '08:00 A 18:00 HORAS'),
                'hora_apertura': s.get('hora_apertura', 8.0),
                'hora_cierre': s.get('hora_cierre', 18.0)
            }
            paradas_detalle.append(parada_obj)
            itinerario_text_parts.append(f"{dia_str}: {s['colonia']} ({s['alcaldia']})")

            paradas_planas.append({
                'id_ruta': r_id,
                'ruta': r_name,
                'nombre_ruta': r_nombre,
                'id_parada': s['id'],
                'orden_parada_semana': idx,
                'dia': dia_str,
                'orden_dia': day_order.get(dia_str, 99),
                'alcaldia': s['alcaldia'],
                'colonia': s['colonia'],
                'direccion': s['direccion'],
                'lat': s['lat'],
                'lng': s['lng'],
                'coordenadas_validas': s['coordenadas_validas'],
                'num_oferentes': ofer,
                'horario': s.get('horario', '08:00 A 18:00 HORAS'),
                'hora_apertura': s.get('hora_apertura', 8.0),
                'hora_cierre': s.get('hora_cierre', 18.0)
            })

        alcaldias_set = []
        for p in paradas_detalle:
            if p['alcaldia'] not in alcaldias_set:
                alcaldias_set.append(p['alcaldia'])

        ruta_obj = {
            'id': r_id,
            'ruta': r_name,
            'nombre': r_nombre,
            'tipo_espacio': 'Mercado Sobre Ruedas',
            'tipo_comercio': 'MOVIL',
            'total_ubicaciones_semana': len(paradas_detalle),
            'dias_activos': [p['dia'] for p in paradas_detalle],
            'dias_resumen': ', '.join(p['dia'] for p in paradas_detalle),
            'itinerario_semanal': ' | '.join(itinerario_text_parts),
            'alcaldias_cubiertas': alcaldias_set,
            'colonias_cubiertas': [p['colonia'] for p in paradas_detalle],
            'num_oferentes_estimados': max(oferentes_list) if oferentes_list else None,
            'paradas': paradas_detalle
        }
        rutas_agrupadas.append(ruta_obj)

    return rutas_agrupadas, paradas_planas


def build_centros_abasto_mayoristas() -> List[Dict[str, Any]]:
    """Genera el catálogo georreferenciado de nodos de abasto mayoristas de la CDMX."""
    centros = [
        {
            'id': 'ABASTO-CEDA',
            'nombre': 'Central de Abasto de la Ciudad de México (CEDA)',
            'clave_nodo': 'CEDA-IZTAPALAPA',
            'tipo_espacio': 'Central Mayorista',
            'tipo_comercio': 'FIJO',
            'tipo_abasto': 'Mayorista',
            'alcaldia': 'IZTAPALAPA',
            'colonia': 'CENTRAL DE ABASTO',
            'direccion': 'Av. Canal de Río Churubusco s/n esq. Eje 5 y Eje 6 Sur, C.P. 09040',
            'lat': 19.371450,
            'lng': -99.091200,
            'coordenadas_validas': True,
            'giros_principales': 'FRUTAS, LEGUMBRES, HORTALIZAS, ABARROTES, VÍVERES, CÁRNICOS, AVES, FLORES Y FOLLAJE',
            'dias_operacion': 'LUNES A DOMINGO',
            'dias_operacion_lista': ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO'],
            'horario_operacion': '24 HORAS (DESCARGA NOCTURNA 22:00 A 06:00, MAYOREO 04:00 A 18:00)',
            'hora_apertura': 0.0,
            'hora_cierre': 24.0,
            'horario_estimado': False,
            'relevancia_logistica': 'Principal nodo mayorista del país y el más grande del mundo (327 ha). Abastece al 80% del consumo de la ZMVM y surte a los 329 mercados públicos y más de 1,300 tianguis de la CDMX.',
            'conectividad_transporte': 'Metro Aculco y Apatlaco (Línea 8); Metrobús Río Mayo y Río Tecolutla (Línea 2); Eje 5 Sur, Eje 6 Sur, Canal de Río Churubusco',
            'fuente_original': 'FICEDA / SEDECO CDMX'
        },
        {
            'id': 'ABASTO-MERCED-MAYOR',
            'nombre': 'Mercado de La Merced - Nave Mayor',
            'clave_nodo': 'MERCED-NAVE-MAYOR',
            'tipo_espacio': 'Mercado Público Mayorista',
            'tipo_comercio': 'FIJO',
            'tipo_abasto': 'Mayorista y Semimayorista',
            'alcaldia': 'VENUSTIANO CARRANZA',
            'colonia': 'CENTRO II',
            'direccion': 'Circunvalación y Carretones s/n, Col. Centro, C.P. 15100',
            'lat': 19.426186,
            'lng': -99.123813,
            'coordenadas_validas': True,
            'giros_principales': 'HORTALIZAS, LEGUMBRES, FRUTAS, VÍVERES, CHILES SECOS, ESPECIAS, CANASTA BÁSICA',
            'dias_operacion': 'LUNES A DOMINGO',
            'dias_operacion_lista': ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO'],
            'horario_operacion': '05:00 A 19:00 HORAS',
            'hora_apertura': 5.0,
            'hora_cierre': 19.0,
            'horario_estimado': False,
            'relevancia_logistica': 'Histórico corazón comercial de la CDMX. Polo central de abasto y semimayoreo para el oriente y centro de la capital y oferentes de tianguis.',
            'conectividad_transporte': 'Metro Merced (Línea 1 con acceso directo subterráneo); Metrobús La Merced (Línea 4); Anillo de Circunvalación',
            'fuente_original': 'SEDECO - Mercados Públicos (MERC-0287)'
        },
        {
            'id': 'ABASTO-MERCED-MENOR',
            'nombre': 'Mercado de La Merced - Nave Menor',
            'clave_nodo': 'MERCED-NAVE-MENOR',
            'tipo_espacio': 'Mercado Público Mayorista',
            'tipo_comercio': 'FIJO',
            'tipo_abasto': 'Mayorista y Semimayorista',
            'alcaldia': 'VENUSTIANO CARRANZA',
            'colonia': 'CENTRO II',
            'direccion': 'Rosario y General Anaya s/n, Col. Centro, C.P. 15100',
            'lat': 19.425488,
            'lng': -99.122676,
            'coordenadas_validas': True,
            'giros_principales': 'CÁRNICOS, EMBUTIDOS, CHICHARRÓN, LÁCTEOS, CREMERÍA, MANTECAS Y ABARROTES AL POR MAYOR',
            'dias_operacion': 'LUNES A DOMINGO',
            'dias_operacion_lista': ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO'],
            'horario_operacion': '06:00 A 18:00 HORAS',
            'hora_apertura': 6.0,
            'hora_cierre': 18.0,
            'horario_estimado': False,
            'relevancia_logistica': 'Centro neurálgico de abasto cárnico y de derivados lácteos al mayoreo y semimayoreo para taquerías, fondas y puestos de tianguis.',
            'conectividad_transporte': 'Metro Merced (Línea 1); Metrobús La Merced (Línea 4); Eje 1 Oriente Circunvalación',
            'fuente_original': 'SEDECO - Mercados Públicos (MERC-0286)'
        },
        {
            'id': 'ABASTO-SONORA',
            'nombre': 'Mercado de Sonora',
            'clave_nodo': 'MERCADO-SONORA',
            'tipo_espacio': 'Mercado Público Especializado',
            'tipo_comercio': 'FIJO',
            'tipo_abasto': 'Semimayorista y Especializado',
            'alcaldia': 'VENUSTIANO CARRANZA',
            'colonia': 'MERCED BALBUENA',
            'direccion': 'Fray Servando Teresa de Mier 419, Col. Merced Balbuena, C.P. 15810',
            'lat': 19.422257,
            'lng': -99.124636,
            'coordenadas_validas': True,
            'giros_principales': 'HERBOLARIA TRADICIONAL, MEDICINA NATURAL, PLANTAS VIVAS, ARTESANÍAS, CERÁMICA, ARTÍCULOS DE TEMPORADA',
            'dias_operacion': 'LUNES A DOMINGO',
            'dias_operacion_lista': ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO'],
            'horario_operacion': '07:00 A 19:00 HORAS',
            'hora_apertura': 7.0,
            'hora_cierre': 19.0,
            'horario_estimado': False,
            'relevancia_logistica': 'Epicentro nacional de distribución de plantas medicinales, herbolaria curativa y alfarería. Suministra a hierberos y curanderos de tianguis metropolitanos.',
            'conectividad_transporte': 'Metro Fray Servando (Línea 4) y Metro Candelaria / Merced; Eje 1 Sur Fray Servando',
            'fuente_original': 'SEDECO - Mercados Públicos (MERC-0291)'
        },
        {
            'id': 'ABASTO-JAMAICA',
            'nombre': 'Mercado de Jamaica (Zona y Flores)',
            'clave_nodo': 'MERCADO-JAMAICA',
            'tipo_espacio': 'Mercado Público Mayorista',
            'tipo_comercio': 'FIJO',
            'tipo_abasto': 'Mayorista y Semimayorista',
            'alcaldia': 'VENUSTIANO CARRANZA',
            'colonia': 'JAMAICA',
            'direccion': 'Guillermo Prieto 45, Col. Jamaica, C.P. 15800',
            'lat': 19.408584,
            'lng': -99.122788,
            'coordenadas_validas': True,
            'giros_principales': 'FLORICULTURA, FLORES DE CORTE, ARREGLOS FLORALES, FOLLAJE, PLANTAS DE ORNATO, FRUTAS Y HORTALIZAS',
            'dias_operacion': 'LUNES A DOMINGO',
            'dias_operacion_lista': ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO'],
            'horario_operacion': '24 HORAS (OPERACIÓN CONTINUA / DESCARGA Y VENTA NOCTURNA Y MATUTINA DE FLOR)',
            'hora_apertura': 0.0,
            'hora_cierre': 24.0,
            'horario_estimado': False,
            'relevancia_logistica': 'Principal centro de distribución mayorista de floricultura y follaje en el Valle de México. Abastece a florerías de colonias, puestos de tianguis y eventos.',
            'conectividad_transporte': 'Metro Jamaica (Correspondencia Líneas 4 y 9); Eje 3 Sur Morelos y Av. Congreso de la Unión',
            'fuente_original': 'SEDECO - Mercados Públicos (MERC-0279)'
        },
        {
            'id': 'ABASTO-NUEVA-VIGA',
            'nombre': 'Mercado de La Nueva Viga',
            'clave_nodo': 'NUEVA-VIGA-MARISCOS',
            'tipo_espacio': 'Central Especializada Mayorista',
            'tipo_comercio': 'FIJO',
            'tipo_abasto': 'Mayorista y Semimayorista',
            'alcaldia': 'IZTAPALAPA',
            'colonia': 'SAN JOSÉ ACULCO',
            'direccion': 'Prolongación Eje 6 Sur (Trabajadores Sociales) 560, Col. San José Aculco, C.P. 09410',
            'lat': 19.369720,
            'lng': -99.097580,
            'coordenadas_validas': True,
            'giros_principales': 'PESCADOS Y MARISCOS FRESCOS Y CONGELADOS, CRUSTÁCEOS, MOLUSCOS, PRODUCTOS DEL MAR Y AGUA DULCE',
            'dias_operacion': 'LUNES A DOMINGO',
            'dias_operacion_lista': ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO'],
            'horario_operacion': '03:00 A 18:00 HORAS (DESCARGA Y MAYOREO 03:00 A 11:00, VENTA AL PÚBLICO 07:00 A 18:00)',
            'hora_apertura': 3.0,
            'hora_cierre': 18.0,
            'horario_estimado': False,
            'relevancia_logistica': 'Segundo mercado mayorista de mariscos y pescados más grande del mundo (comercializa cerca del 65% del volumen nacional). Suministra a pescaderías de mercados y tianguis de la ciudad.',
            'conectividad_transporte': 'Metro Aculco (Línea 8); Eje 6 Sur Trabajadores Sociales y Canal de Río Churubusco',
            'fuente_original': 'Sociedad Nacional de Comercializadores de Productos Pesqueros'
        },
        {
            'id': 'ABASTO-LA-VIGA',
            'nombre': 'Mercado de La Viga (Histórico Tradicional)',
            'clave_nodo': 'VIGA-HISTORICA',
            'tipo_espacio': 'Mercado Público Especializado',
            'tipo_comercio': 'FIJO',
            'tipo_abasto': 'Semimayorista',
            'alcaldia': 'CUAUHTEMOC',
            'colonia': 'TRANSITO',
            'direccion': 'Calzada de la Viga y Lorenzo Boturini s/n, Col. Tránsito, C.P. 06820',
            'lat': 19.418650,
            'lng': -99.128420,
            'coordenadas_validas': True,
            'giros_principales': 'PESCADOS Y MARISCOS CRUDOS Y PREPARADOS AL POR MENOR Y MEDIO MAYOREO',
            'dias_operacion': 'LUNES A DOMINGO',
            'dias_operacion_lista': ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO'],
            'horario_operacion': '06:00 A 18:00 HORAS',
            'hora_apertura': 6.0,
            'hora_cierre': 18.0,
            'horario_estimado': False,
            'relevancia_logistica': 'Mercado histórico de mariscos de la CDMX previo al traslado mayorista a Iztapalapa. Mantiene abasto semimayorista y tradicional para el centro-sur de la ciudad.',
            'conectividad_transporte': 'Metro La Viga (Línea 8) y Metro Chabacano (Líneas 2, 8 y 9); Calzada de la Viga y Lorenzo Boturini',
            'fuente_original': 'SEDECO CDMX'
        },
        {
            'id': 'ABASTO-SAN-JUAN-PUGIBET',
            'nombre': 'Mercado de San Juan Pugibet',
            'clave_nodo': 'SAN-JUAN-PUGIBET',
            'tipo_espacio': 'Mercado Público Especializado',
            'tipo_comercio': 'FIJO',
            'tipo_abasto': 'Semimayorista y Especializado',
            'alcaldia': 'CUAUHTEMOC',
            'colonia': 'CENTRO VIII',
            'direccion': 'Ernesto Pugibet 21, Col. Centro, C.P. 06000',
            'lat': 19.430036,
            'lng': -99.144608,
            'coordenadas_validas': True,
            'giros_principales': 'ALIMENTOS GOURMET, CÁRNICOS EXÓTICOS, PESCADOS Y MARISCOS FINOS, QUESOS EUROPEOS, EMBUTIDOS Y VEGETALES ASIÁTICOS',
            'dias_operacion': 'LUNES A DOMINGO',
            'dias_operacion_lista': ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO'],
            'horario_operacion': '07:00 A 17:00 HORAS',
            'hora_apertura': 7.0,
            'hora_cierre': 17.0,
            'horario_estimado': False,
            'relevancia_logistica': 'Polo de referencia gastronómica y abasto especializado gourmet de la CDMX. Provee a chefs, restaurantes de alta cocina y puesteros especializados.',
            'conectividad_transporte': 'Metro Salto del Agua (Líneas 1 y 8); Metrobús San Juan Pugibet / El Salvador (Línea 4); Eje Central Lázaro Cárdenas',
            'fuente_original': 'SEDECO - Mercados Públicos (MERC-0248)'
        }
    ]
    return centros


def save_dataset(records: List[Dict[str, Any]], base_filename: str):
    """Guarda un dataset tanto en formato JSON como CSV."""
    json_path = os.path.join(PROCESSED_DIR, f"{base_filename}.json")
    csv_path = os.path.join(PROCESSED_DIR, f"{base_filename}.csv")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    # Para CSV, las columnas de listas se convierten a string delimitado por punto y coma o JSON
    csv_records = []
    for r in records:
        r_copy = dict(r)
        for k, v in r_copy.items():
            if isinstance(v, list):
                if len(v) > 0 and isinstance(v[0], dict):
                    r_copy[k] = json.dumps(v, ensure_ascii=False)
                else:
                    r_copy[k] = '; '.join(str(item) for item in v)
        csv_records.append(r_copy)

    df = pd.DataFrame(csv_records)
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"✓ Guardado: {base_filename}.json ({len(records)} registros) y {base_filename}.csv")


def main():
    print("=" * 70)
    print("INICIANDO PROCESO DE NORMALIZACIÓN Y LIMPIEZA DE DATOS")
    print("=" * 70)

    # 1. Tianguis
    print("\n[1/8] Procesando Tianguis...")
    tianguis = process_tianguis()
    save_dataset(tianguis, 'tianguis_limpio')

    # 2. Mercados Públicos
    print("\n[2/8] Procesando Mercados Públicos...")
    mercados = process_mercados_publicos()
    save_dataset(mercados, 'mercados_publicos_limpio')

    # 3. Mercados Sobre Ruedas
    print("\n[3/8] Procesando Mercados Sobre Ruedas...")
    msr = process_mercados_sobre_ruedas()
    save_dataset(msr, 'mercados_sobre_ruedas_limpio')

    # 4. Concentraciones de Comerciantes
    print("\n[4/8] Procesando Concentraciones de Comerciantes...")
    concentraciones = process_concentraciones()
    save_dataset(concentraciones, 'concentraciones_comerciantes_limpio')

    # 5. Muestra Mercomuna
    print("\n[5/8] Procesando Comercios Barriales Mercomuna...")
    mercomuna = process_mercomuna()
    save_dataset(mercomuna, 'mercomuna_comercios_limpio')

    # 6. Apoyos Emergentes
    print("\n[6/8] Procesando Padrón de Apoyos Emergentes...")
    apoyos = process_apoyos_emergentes()
    save_dataset(apoyos, 'apoyos_emergentes_limpio')

    # 7. Rutas Itinerantes de Mercados Sobre Ruedas (MSR)
    print("\n[7/8] Procesando Trazabilidad y Rutas Itinerantes de MSR...")
    rutas_msr, paradas_msr = process_msr_rutas_itinerantes(msr)
    save_dataset(rutas_msr, 'msr_rutas_itinerantes')
    save_dataset(paradas_msr, 'msr_rutas_paradas_itinerantes')

    # 8. Catálogo de Nodos de Abasto Mayoristas
    print("\n[8/8] Generando Catálogo de Nodos de Abasto Mayoristas...")
    centros_abasto = build_centros_abasto_mayoristas()
    save_dataset(centros_abasto, 'centros_abasto_mayoristas')

    # 9. Catálogo Unificado
    print("\n[*] Construyendo Directorio Unificado de Comercio Popular...")
    directorio_unificado = build_unified_directory(tianguis, mercados, msr, concentraciones)
    save_dataset(directorio_unificado, 'directorio_comercio_popular')

    print("\n" + "=" * 70)
    print("RESUMEN GENERAL DE PROCESAMIENTO:")
    print("=" * 70)
    print(f"• Mercados Públicos:       {len(mercados):>5} registros (FIJO)")
    print(f"• Tianguis:                 {len(tianguis):>5} registros (MOVIL)")
    print(f"• Mercados Sobre Ruedas:    {len(msr):>5} registros en {len(rutas_msr)} rutas (MOVIL)")
    print(f"• Concentraciones:          {len(concentraciones):>5} registros (FIJO)")
    print(f"--------------------------------------------------")
    print(f"TOTAL DIRECTORIO POPULAR:   {len(directorio_unificado):>5} espacios de abasto popular")
    print(f"--------------------------------------------------")
    print(f"• Rutas Itinerantes MSR:    {len(rutas_msr):>5} rutas ({len(paradas_msr)} paradas semanales)")
    print(f"• Centros Abasto Mayoristas:{len(centros_abasto):>5} nodos clave de suministro")
    print(f"• Muestra Mercomuna:        {len(mercomuna):>5} tiendas y comercios barriales")
    print(f"• Apoyos Emergentes:        {len(apoyos):>5} comerciantes beneficiarios")
    print("=" * 70)


if __name__ == '__main__':
    main()
