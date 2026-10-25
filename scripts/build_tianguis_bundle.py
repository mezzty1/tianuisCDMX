#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compilador de Datos Especializados para el Mapa Minimalista de Tianguis CDMX + ZMVM
Chilangatón 2026 - Reto 1: Comercio Popular y Barrial (Tarea 7.7)

Genera:
- 1,367 tianguis semanales de la CDMX enriquecidos con:
  * Estatus operativo según día y hora
  * Escala comercial: Megatianguis (>300), Mediano (100-300), Barrial (<100)
  * Nombres populares emblemáticos identificados (El Salado, San Felipe / La Bola, Chopo, Sullivan, Apatlaco, etc.)
  * Estación de Metro o Metrobús más cercana a pie (distancia y minutos caminando calculados)
  * Vocación y etiquetas de productos clave
- Cartografía contextual ligera:
  * 16 Alcaldías de la CDMX
  * 60 Municipios conurbados de la ZMVM
- Vocabulario y catálogo de productos (+460 artículos) para Omnibox predictivo
"""

import os
import json
import math
import re
import unicodedata
from typing import Dict, List, Any

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula distancia en metros entre dos puntos geográficos WGS84."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2.0) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def clean_popular_name(nom: str, dir_str: str, col: str) -> str:
    """Extrae o normaliza un nombre popular limpio y humano para el tianguis."""
    # 1. Buscar apodo entrecomillado en dirección (ej. “Tianguis Serapio”, “Tianguis Lagunilla”)
    m = re.search(r'[\"“](Tianguis[^\"”]+)[\"”]', dir_str or '', re.IGNORECASE)
    if m:
        return m.group(1).strip()
    
    # 2. Identificar tianguis emblemáticos por ubicación
    u_dir = (dir_str or '').upper()
    u_col = (col or '').upper()
    u_nom = (nom or '').upper()

    if 'ERMITA ZARAGOZA' in u_col and ('TEXCOCO' in u_dir or 'SENTIMIENTOS' in u_dir):
        return "Tianguis El Salado (Ermita Zaragoza)"
    if 'SANTA MARTHA ACATITLA' in u_col and ('REPUBLICA FEDERAL' in u_dir or 'EXPLORADORES' in u_dir):
        return "Tianguis El Salado / Acatitla"
    if 'SAN FELIPE DE JESUS' in u_col or 'SAN FELIPE' in u_nom:
        return "Tianguis San Felipe de Jesús / La Bola"
    if 'SULLIVAN' in u_dir:
        return "Tianguis Sullivan / Jardín del Arte"
    if 'CHOPO' in u_dir or 'SAN SIMON' in u_dir:
        return "Tianguis Cultural del Chopo"
    if 'COMONFORT' in u_dir or 'MATAMOROS' in u_dir:
        return "Tianguis Lagunilla / Antigüedades"
    if 'SANTA CRUZ MEYEHUALCO' in u_col:
        return "Tianguis Santa Cruz Meyehualco"
    if 'APATLACO' in u_nom or 'APATLACO' in u_col:
        return "Tianguis Apatlaco"
    if 'HIPODROMO CONDESA' in u_col or 'CONDESA' in u_nom:
        return "Tianguis Condesa"
    if 'DOCTORES' in u_col:
        return "Tianguis Doctores"
    if 'PORTALES' in u_nom or 'PORTALES' in u_col:
        return "Tianguis Portales"

    # 3. Limpieza estándar
    s = re.sub(r'^TIANGUIS\s+', '', nom or '', flags=re.IGNORECASE)
    s = re.sub(r'\s*\((LUNES|MARTES|MIERCOLES|MIÉRCOLES|JUEVES|VIERNES|SABADO|SÁBADO|DOMINGO)\)', '', s, flags=re.IGNORECASE)
    s = re.sub(r'\s*\((U HAB|AMPL|PBLO|BARR|SECC|SEC)\)', r' \1', s, flags=re.IGNORECASE)
    s = s.title().strip()
    if not s.lower().startswith('tianguis'):
        s = 'Tianguis ' + s
    return s

def classify_scale(oferentes: int) -> Dict[str, str]:
    """Clasifica la escala del tianguis por volumen de oferentes."""
    if oferentes >= 300:
        return {"id": "mega", "nombre": "Megatianguis", "badge_class": "badge-mega", "icono": "🎪"}
    elif oferentes >= 100:
        return {"id": "mediano", "nombre": "Tianguis Mediano", "badge_class": "badge-mediano", "icono": "🏪"}
    else:
        return {"id": "barrial", "nombre": "Tianguis Barrial", "badge_class": "badge-barrial", "icono": "🧺"}

def assign_vocation(pname: str, oferentes: int, giro: str, col: str) -> Dict[str, Any]:
    """Determina la especialidad y vocación comercial del tianguis."""
    p_up = pname.upper()
    if 'CHOPO' in p_up:
        return {
            "nombre": "Contracultura, Música y Coleccionismo",
            "descripcion": "Especializado en discos de vinilo, rock, playeras de bandas, ropa alternativa y arte.",
            "tags": ["rock", "musica", "vinilos", "discos", "ropa negra", "coleccionismo", "botas"]
        }
    if 'SALADO' in p_up:
        return {
            "nombre": "Ropa de Paca, Herramientas y Chácharas",
            "descripcion": "Megatianguis de fin de semana con miles de puestos de ropa de segunda mano, herramientas usadas, refacciones y antojitos.",
            "tags": ["paca", "ropa de paca", "herramientas", "chacharas", "tenis", "barbacoa", "antojitos"]
        }
    if 'SAN FELIPE' in p_up or 'BOLA' in p_up:
        return {
            "nombre": "Megatianguis Mixto Metropolitano",
            "descripcion": "El tianguis más extenso de la CDMX y ZMVM: abasto completo de alimentos, ropa de paca, tenis, calzado, autopartes y gastronomía.",
            "tags": ["megatianguis", "paca", "tenis", "autopartes", "comida", "frutas", "verduras", "carniceria"]
        }
    if 'SULLIVAN' in p_up:
        return {
            "nombre": "Arte al Aire Libre y Antigüedades",
            "descripcion": "Corredor cultural y dominical de pinturas, esculturas, marcos, artesanías y gastronomía.",
            "tags": ["arte", "pinturas", "marcos", "antiguedades", "artesanias", "comida"]
        }
    if 'LAGUNILLA' in p_up:
        return {
            "nombre": "Antigüedades, Muebles y Ropa Vintage",
            "descripcion": "Tradicional tianguis dominical de piezas históricas, ropa retro, antigüedades y coctelería barrial.",
            "tags": ["antiguedades", "vintage", "ropa", "muebles", "coleccionismo", "chacharas"]
        }
    if 'MEYEHUALCO' in p_up:
        return {
            "nombre": "Ropa, Calzado y Abasto Mixto",
            "descripcion": "Gran corredor de ropa de paca, tenis, artículos del hogar, abarrotes y comida.",
            "tags": ["ropa", "tenis", "calzado", "paca", "abarrotes", "antojitos"]
        }

    # Tianguis general barrial
    if oferentes >= 300:
        return {
            "nombre": "Abasto Popular y Comercio Mixto Completo",
            "descripcion": "Gran tianguis barrial con amplia oferta de canasta básica fresca, comida preparada, ropa de paca y ferretería.",
            "tags": ["frutas", "verduras", "carniceria", "pollo", "pescado", "cremeria", "barbacoa", "carnitas", "ropa", "tenis", "chacharas", "ferreteria"]
        }
    else:
        return {
            "nombre": "Canasta Básica y Abasto Barrial",
            "descripcion": "Puntos de abasto local con alimentos frescos, frutas, verduras, carnes, huevo y antojitos del día.",
            "tags": ["frutas", "verduras", "jitomate", "aguacate", "carniceria", "polleria", "huevo", "cremeria", "tortillas", "antojitos", "chacharas"]
        }

def round_coords(geom, precision=4):
    """Reduce precisión de coordenadas GeoJSON para aligerar la transferencia."""
    if isinstance(geom, list):
        if len(geom) == 2 and isinstance(geom[0], (int, float)) and isinstance(geom[1], (int, float)):
            return [round(geom[0], precision), round(geom[1], precision)]
        return [round_coords(item, precision) for item in geom]
    elif isinstance(geom, dict):
        return {k: round_coords(v, precision) for k, v in geom.items()}
    return geom

def run():
    print("Iniciando compilación de bundle especializado de Tianguis CDMX + ZMVM...")

    # 1. Cargar Estaciones de Metro y Metrobús para calcular transporte a pie
    print("• Cargando estaciones de transporte oficial...")
    stations = []
    if os.path.exists('data/raw/transporte/metro_estaciones.geojson'):
        with open('data/raw/transporte/metro_estaciones.geojson', 'r', encoding='utf-8') as f:
            m_data = json.load(f)
            for feat in m_data['features']:
                c = feat['geometry']['coordinates']
                p = feat['properties']
                stations.append({
                    'tipo': 'Metro',
                    'nombre': p.get('NOMBRE', ''),
                    'linea': f"L{p.get('LINEA', '')}",
                    'lat': c[1],
                    'lng': c[0]
                })

    if os.path.exists('data/raw/transporte/metrobus_estaciones.geojson'):
        with open('data/raw/transporte/metrobus_estaciones.geojson', 'r', encoding='utf-8') as f:
            mb_data = json.load(f)
            for feat in mb_data['features']:
                c = feat['geometry']['coordinates']
                p = feat['properties']
                stations.append({
                    'tipo': 'Metrobús',
                    'nombre': p.get('NOMBRE', ''),
                    'linea': f"L{p.get('LINEA', '')}",
                    'lat': c[1],
                    'lng': c[0]
                })

    print(f"  ✓ {len(stations)} estaciones cargadas para cálculo caminable.")

    # 2. Cargar Tianguis Limpio (1,367 registros) y Enriquecimiento NLP (Tarea 5.5)
    print("• Procesando los 1,367 tianguis semanales...")
    nlp_dict = {}
    if os.path.exists('data/processed/tianguis_especialidades_nlp.json'):
        with open('data/processed/tianguis_especialidades_nlp.json', 'r', encoding='utf-8') as f:
            for item in json.load(f):
                idx_val = item['idx']
                nlp_dict[idx_val] = item
                try:
                    nlp_dict[f"TIANG-{int(idx_val)+1:04d}"] = item
                except Exception:
                    pass
        print(f"  ✓ Especialidades y fotografías NLP cargadas.")

    # Cargar citas textuales de reseñas de Google Maps de tianguis_reviews.json
    reviews_dict = {}
    if os.path.exists('data/processed/tianguis_reviews.json'):
        with open('data/processed/tianguis_reviews.json', 'r', encoding='utf-8') as f:
            for item in json.load(f):
                idx_val = item.get('idx')
                citas = []
                # Intentar parsear snippets_json
                raw_snippets = item.get('snippets_json')
                if raw_snippets:
                    try:
                        if isinstance(raw_snippets, str):
                            snips = json.loads(raw_snippets)
                        else:
                            snips = raw_snippets
                        for s in snips:
                            s_clean = str(s).strip()
                            if s_clean and len(s_clean) > 8 and not s_clean.startswith('['):
                                citas.append(s_clean)
                    except Exception:
                        pass
                # Si no hay snippets, buscar en resenas_texto_corpus
                if not citas and item.get('resenas_texto_corpus'):
                    parts = str(item['resenas_texto_corpus']).split('|')
                    for p in parts:
                        p_clean = p.strip()
                        if p_clean and len(p_clean) > 15 and not p_clean.startswith('['):
                            citas.append(p_clean)
                reviews_dict[idx_val] = citas[:4]
                try:
                    reviews_dict[f"TIANG-{int(idx_val)+1:04d}"] = citas[:4]
                except Exception:
                    pass
        print(f"  ✓ Citas textuales de reseñas ciudadanas cargadas ({len([k for k,v in reviews_dict.items() if v])} tianguis con opiniones).")

    with open('data/processed/tianguis_limpio.json', 'r', encoding='utf-8') as f:
        tianguis_raw = json.load(f)

    tianguis_processed = []
    dias_semana_canonicos = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']

    for t in tianguis_raw:
        lat = t.get('lat')
        lng = t.get('lng')
        coords_valid = True if (lat is not None and lng is not None and isinstance(lat, (int, float)) and isinstance(lng, (int, float)) and lat > 0) else False

        oferentes = int(t.get('num_oferentes') or 0)
        pname = clean_popular_name(t['nombre'], t.get('direccion', ''), t.get('colonia', ''))
        scale = classify_scale(oferentes)
        vocation = assign_vocation(pname, oferentes, t.get('giro', ''), t.get('colonia', ''))

        # Enriquecimiento NLP de Tarea 5.5
        nlp_info = nlp_dict.get(t['id'], {})
        voc_nombre = nlp_info.get('vocacion_nombre') or vocation['nombre']
        voc_desc = nlp_info.get('especialidad_comunitaria') or vocation['descripcion']
        voc_icono = nlp_info.get('vocacion_icono') or '🧺'
        top_art = nlp_info.get('top_articulos_mencionados') or vocation['tags'][:6]
        fotos = nlp_info.get('fotos') or []
        rating = nlp_info.get('rating_google')
        total_rev = nlp_info.get('total_resenas', 0)
        foto_main = nlp_info.get('foto_principal') or (fotos[0] if fotos else '')

        # Citas textuales de reseñas de compradores
        citas_list = reviews_dict.get(t['id']) or reviews_dict.get(nlp_info.get('idx')) or []

        # Calcular estación más cercana si tiene coordenadas válidas
        transporte_info = {}
        if coords_valid:
            closest_station = None
            min_dist = float('inf')
            for s in stations:
                d = haversine(lat, lng, s['lat'], s['lng'])
                if d < min_dist:
                    min_dist = d
                    closest_station = s

            if closest_station:
                walk_min = max(1, round(min_dist / 80))  # ~80m/min caminando
                if min_dist <= 2500:
                    texto_transporte = f"🚶 A {walk_min} min a pie de {closest_station['tipo']} {closest_station['nombre']} ({closest_station['linea']}) · {int(min_dist)} m"
                else:
                    texto_transporte = f"🚌 A {(min_dist/1000):.1f} km de {closest_station['tipo']} {closest_station['nombre']} ({closest_station['linea']})"

                transporte_info = {
                    'tipo': closest_station['tipo'],
                    'nombre': closest_station['nombre'],
                    'linea': closest_station['linea'],
                    'distancia_m': int(min_dist),
                    'tiempo_min': walk_min,
                    'texto': texto_transporte
                }
        else:
            transporte_info = {
                'tipo': '',
                'nombre': '',
                'linea': '',
                'distancia_m': 0,
                'tiempo_min': 0,
                'texto': '📍 Coordenadas en proceso de auditoría territorial'
            }

        # Días de operación normalizados en lista
        dias_op = []
        if t.get('lunes'): dias_op.append('LUNES')
        if t.get('martes'): dias_op.append('MARTES')
        if t.get('miercoles'): dias_op.append('MIERCOLES')
        if t.get('jueves'): dias_op.append('JUEVES')
        if t.get('viernes'): dias_op.append('VIERNES')
        if t.get('sabado'): dias_op.append('SABADO')
        if t.get('domingo'): dias_op.append('DOMINGO')
        if not dias_op:
            dias_op = [d.strip().upper() for d in t.get('dia', '').split(',') if d.strip()]

        tianguis_item = {
            'id': t['id'],
            'nombre_oficial': t['nombre'],
            'nombre_popular': pname,
            'alcaldia': t.get('alcaldia', '').upper(),
            'colonia': t.get('colonia', '').title(),
            'direccion': t.get('direccion', ''),
            'dias': dias_op,
            'dia_principal': t.get('dia', ''),
            'hora_apertura': float(t.get('hora_apertura') or 8.0),
            'hora_cierre': float(t.get('hora_cierre') or 17.0),
            'lat': round(lat, 6) if coords_valid else None,
            'lng': round(lng, 6) if coords_valid else None,
            'coordenadas_validas': coords_valid,
            'oferentes': oferentes,
            'escala_id': scale['id'],
            'escala_nombre': scale['nombre'],
            'escala_badge': scale['badge_class'],
            'escala_icono': scale['icono'],
            'vocacion_nombre': voc_nombre,
            'vocacion_desc': voc_desc,
            'vocacion_icono': voc_icono,
            'especialidad_comunitaria': voc_desc,
            'top_articulos_mencionados': top_art,
            'tags': list(set(vocation['tags'] + [a.lower() for a in top_art])),
            'fotos': fotos,
            'foto_principal': foto_main,
            'rating_google': rating,
            'total_resenas': total_rev,
            'citas_resenas': citas_list,
            'transporte': transporte_info
        }
        tianguis_processed.append(tianguis_item)

    print(f"  ✓ {len(tianguis_processed)} tianguis enriquecidos.")

    # 3. Cargar Cartografía Base Ligera (Alcaldías CDMX + ZMVM Edomex)
    print("• Optimizando cartografía de 16 alcaldías y 60 municipios conurbados...")
    alcaldias_features = []
    if os.path.exists('data/raw/cartografia/alcaldias.geojson'):
        with open('data/raw/cartografia/alcaldias.geojson', 'r', encoding='utf-8') as f:
            alc_raw = json.load(f)
            for feat in alc_raw['features']:
                geom = round_coords(feat['geometry'], precision=4)
                props = feat['properties']
                nom = props.get('nomgeo') or props.get('NOMGEO') or props.get('nombre') or ''
                alcaldias_features.append({
                    'type': 'Feature',
                    'properties': {
                        'nombre': nom.upper(),
                        'tipo': 'Alcaldía CDMX'
                    },
                    'geometry': geom
                })

    zmvm_features = []
    zmvm_path = 'data/raw/cartografia/zmvm_edomex_opt.geojson'
    if not os.path.exists(zmvm_path):
        zmvm_path = 'data/raw/cartografia/zmvm_edomex.geojson'
    if os.path.exists(zmvm_path):
        with open(zmvm_path, 'r', encoding='utf-8') as f:
            zmvm_raw = json.load(f)
            for feat in zmvm_raw['features']:
                geom = round_coords(feat['geometry'], precision=4)
                props = feat['properties']
                nom = props.get('NOMGEO') or props.get('nomgeo') or ''
                zmvm_features.append({
                    'type': 'Feature',
                    'properties': {
                        'nombre': nom,
                        'tipo': 'Municipio Conurbado ZMVM'
                    },
                    'geometry': geom
                })

    cartografia = {
        'alcaldias': {'type': 'FeatureCollection', 'features': alcaldias_features},
        'zmvm': {'type': 'FeatureCollection', 'features': zmvm_features}
    }
    print(f"  ✓ {len(alcaldias_features)} alcaldías y {len(zmvm_features)} municipios listos.")

    # 4. Cargar Vocabulario de Compras (+460 productos)
    print("• Cargando catálogo ampliado de compras populares...")
    vocabulario = []
    if os.path.exists('data/catalog/vocabulario_compras.json'):
        with open('data/catalog/vocabulario_compras.json', 'r', encoding='utf-8') as f:
            vocabulario = json.load(f)
    print(f"  ✓ {len(vocabulario)} términos de consumo para el omnibox.")

    # 5. Compilar bundle final
    bundle = {
        'version': 'Chilangatón 2026 - Tarea 7.7 Minimalista',
        'total_tianguis': len(tianguis_processed),
        'tianguis': tianguis_processed,
        'cartografia': cartografia,
        'vocabulario': vocabulario,
        'alcaldias_lista': sorted(list(set(t['alcaldia'] for t in tianguis_processed if t['alcaldia'])))
    }

    # Guardar JSON
    json_path = 'data/processed/tianguis_map_data.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(bundle, f, ensure_ascii=False)
    print(f"✓ Guardado: {json_path} (Tamaño: {os.path.getsize(json_path) / 1024:.1f} KB)")

    # Guardar JS (para compatibilidad total file:// y sin CORS)
    js_path = 'data/processed/tianguis_map_data.js'
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write("window.TIANGUIS_DATA = ")
        json.dump(bundle, f, ensure_ascii=False)
        f.write(";\n")
    print(f"✓ Guardado: {js_path} (Tamaño: {os.path.getsize(js_path) / 1024:.1f} KB)")

    print("=" * 70)
    print("BUNDLE DE TIANGUIS MINIMALISTA COMPILADO CON ÉXITO")
    print("=" * 70)

if __name__ == '__main__':
    run()
