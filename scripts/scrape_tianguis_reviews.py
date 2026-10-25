#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper de Reseñas, Calificaciones y Fotografías de Tianguis en Google Maps
Chilangatón 2026 - Reto 1: Comercio Popular y Barrial (Tarea 5.5 - Fase 1)

Extrae para cada tianguis de la CDMX con ficha verificada:
- Rating promedio y total de opiniones ciudadanas
- Textos de reseñas recientes de visitantes y compradores
- Citas / snippets destacados de experiencia barrial
- Temas frecuentes mencionados (ej. paca, comida, precios, carnitas)
- URLs directas de fotografías reales de puestos y ambiente

Cuenta con:
- Caché local en disco (data/raw/scraping/cache/{place_id}.json) para reanudación instantánea
- Rate-limiting ético y rotación de User-Agents
- Concurrencia controlada mediante ThreadPoolExecutor
- Exportación dual en JSON y CSV
"""

import os
import re
import time
import json
import random
import logging
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

CACHE_DIR = 'data/raw/scraping/cache'
os.makedirs(CACHE_DIR, exist_ok=True)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.3; rv:122.0) Gecko/20100101 Firefox/122.0'
]

def get_random_headers() -> Dict[str, str]:
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.google.com/maps',
        'DNT': '1'
    }

def fetch_place_data(place_id: str, max_retries: int = 3) -> Dict[str, Any]:
    """Consulta los datos del place_id en Google Maps o recupera de la caché."""
    cache_path = os.path.join(CACHE_DIR, f"{place_id}.json")
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Error leyendo caché de {place_id}: {e}")

    result = {
        'place_id': place_id,
        'status': 'error',
        'nombre_maps': '',
        'rating': None,
        'total_reviews': 0,
        'reviews': [],
        'snippets': [],
        'temas_frecuentes': [],
        'fotos': []
    }

    url1 = f"https://maps.google.com/maps?q=place_id:{place_id}&hl=es&dg=es5"
    session = requests.Session()

    for attempt in range(max_retries):
        try:
            time.sleep(random.uniform(0.1, 0.4))  # Rate limiting cortés
            headers = get_random_headers()
            r1 = session.get(url1, headers=headers, timeout=12)
            if r1.status_code != 200:
                time.sleep(1.0 * (attempt + 1))
                continue

            m = re.search(r'href="(/maps/preview/place\?[^"]+)"', r1.text)
            if not m:
                # Puede no tener preview o haber cambiado la plantilla
                result['status'] = 'sin_preview'
                break

            preview_path = m.group(1).replace('&amp;', '&')
            preview_url = "https://www.google.com" + preview_path

            time.sleep(random.uniform(0.1, 0.3))
            r2 = session.get(preview_url, headers=headers, timeout=12)
            if r2.status_code == 200 and r2.text.startswith(")]}'"):
                clean_json = r2.text[4:].strip()
                data = json.loads(clean_json)
                if len(data) > 6 and data[6]:
                    d6 = data[6]

                    # 1. Nombre y Calificación
                    result['nombre_maps'] = d6[11] if len(d6) > 11 and d6[11] else ''
                    if len(d6) > 4 and d6[4]:
                        result['rating'] = float(d6[4][7]) if len(d6[4]) > 7 and d6[4][7] is not None else None
                        result['total_reviews'] = int(d6[4][8]) if len(d6[4]) > 8 and d6[4][8] is not None else 0

                    # 2. Reseñas completas
                    reviews = []
                    try:
                        if len(d6) > 175 and d6[175] and len(d6[175]) > 9 and d6[175][9]:
                            rev_nodes = d6[175][9][0][0]
                            for node in rev_nodes:
                                try:
                                    sub = node[0][2]
                                    stars = sub[0][0] if len(sub) > 0 and isinstance(sub[0], list) and len(sub[0]) > 0 else None
                                    texto = sub[15][0][0] if len(sub) > 15 and sub[15] and len(sub[15]) > 0 and sub[15][0] else ''
                                    
                                    # Fecha relativa
                                    fecha = ''
                                    def find_date(obj):
                                        nonlocal fecha
                                        if isinstance(obj, list):
                                            for x in obj:
                                                find_date(x)
                                        elif isinstance(obj, str):
                                            if any(k in obj.lower() for k in ['hace ', 'ayer', 'meses', 'año', 'semana', 'días']) and not fecha:
                                                fecha = obj
                                    find_date(sub)

                                    if texto:
                                        reviews.append({
                                            'stars': stars,
                                            'fecha': fecha,
                                            'texto': texto.strip()
                                        })
                                except Exception:
                                    pass
                    except Exception as e:
                        logger.debug(f"Error extrayendo reseñas de {place_id}: {e}")
                    result['reviews'] = reviews

                    # 3. Snippets de citas
                    snippets = []
                    try:
                        if len(d6) > 31 and d6[31] and len(d6[31]) > 1 and d6[31][1]:
                            for snip in d6[31][1]:
                                if len(snip) > 1 and snip[1]:
                                    snippets.append(snip[1].strip('"'))
                    except Exception:
                        pass
                    result['snippets'] = snippets

                    # 4. Temas frecuentes
                    temas = []
                    try:
                        if len(d6) > 153 and d6[153]:
                            for item in d6[153]:
                                try:
                                    t_nombre = item[1]
                                    menciones = item[3][4] if len(item) > 3 and item[3] and len(item[3]) > 4 else 1
                                    temas.append({'tema': str(t_nombre), 'menciones': int(menciones)})
                                except Exception:
                                    pass
                    except Exception:
                        pass
                    result['temas_frecuentes'] = temas

                    # 5. Fotografías
                    fotos = []
                    try:
                        photo_source = d6[72] if len(d6) > 72 and d6[72] else (d6[51] if len(d6) > 51 and d6[51] else [])
                        for p in photo_source:
                            try:
                                url = p[0][6][0]
                                if 'googleusercontent.com' in url:
                                    base_url = url.split('=')[0]
                                    clean_url = f"{base_url}=w800-h600-k-no"
                                    if clean_url not in fotos:
                                        fotos.append(clean_url)
                            except Exception:
                                pass
                    except Exception:
                        pass
                    result['fotos'] = fotos[:6]  # Top 6 fotos representativas
                    result['status'] = 'ok'
                    break
        except Exception as e:
            logger.debug(f"Intento {attempt+1} falló para {place_id}: {e}")
            time.sleep(1.0 * (attempt + 1))

    # Guardar en caché si se obtuvo respuesta o sin_preview
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result

def run():
    print("=" * 70)
    print("CHILANGATÓN 2026 - TAREA 5.5: SCRAPING DE RESEÑAS Y FOTOS GOOGLE MAPS")
    print("=" * 70)

    padron_path = 'data/processed/padron_tianguis_auditado_maps.csv'
    if not os.path.exists(padron_path):
        print(f"ERROR: Archivo no encontrado: {padron_path}")
        return

    df = pd.read_csv(padron_path)
    print(f"• Registros totales en padrón auditado: {len(df):,}")

    # Filtrar place_ids válidos
    valid_pids = [pid for pid in df['place_id'].dropna().unique() if pid and pid.startswith('ChIJ')]
    print(f"• Place IDs únicos a procesar: {len(valid_pids)}")

    # Revisar estado de caché
    cached_pids = set()
    for f in os.listdir(CACHE_DIR):
        if f.endswith('.json'):
            cached_pids.add(f[:-5])

    pending_pids = [pid for pid in valid_pids if pid not in cached_pids]
    print(f"  ✓ {len(cached_pids)} ya en caché local.")
    print(f"  • {len(pending_pids)} pendientes de consultar...")

    # Ejecución concurrente controlada (5 workers)
    max_workers = 5
    results_by_pid = {}

    # Cargar los que ya están en caché
    for pid in cached_pids:
        c_path = os.path.join(CACHE_DIR, f"{pid}.json")
        try:
            with open(c_path, 'r', encoding='utf-8') as f:
                results_by_pid[pid] = json.load(f)
        except Exception:
            pass

    if pending_pids:
        print(f"• Iniciando crawler concurrente con {max_workers} hilos...")
        count = 0
        total_pending = len(pending_pids)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_pid = {executor.submit(fetch_place_data, pid): pid for pid in pending_pids}
            for future in as_completed(future_to_pid):
                pid = future_to_pid[future]
                count += 1
                try:
                    data = future.result()
                    results_by_pid[pid] = data
                    if count % 20 == 0 or count == total_pending:
                        print(f"  [{count}/{total_pending}] Procesados ({count/total_pending*100:.1f}%) - Último: {data.get('nombre_maps') or pid}")
                except Exception as e:
                    logger.error(f"Error en futuro para {pid}: {e}")

    # Consolidar con el padrón completo
    print("\n• Consolidando dataset enriquecido de reseñas y fotos...")
    consolidated_rows = []
    total_reviews_collected = 0
    total_photos_collected = 0

    for _, row in df.iterrows():
        pid = row.get('place_id')
        place_data = results_by_pid.get(pid, {}) if pd.notna(pid) else {}

        reviews_list = place_data.get('reviews', [])
        snippets_list = place_data.get('snippets', [])
        temas_list = place_data.get('temas_frecuentes', [])
        fotos_list = place_data.get('fotos', [])

        total_reviews_collected += len(reviews_list)
        total_photos_collected += len(fotos_list)

        # Concatenar todos los textos para minería NLP
        all_texts = []
        for r in reviews_list:
            if r.get('texto'):
                all_texts.append(r['texto'])
        all_texts.extend(snippets_list)
        for t in temas_list:
            if isinstance(t, dict) and t.get('tema'):
                all_texts.append(t['tema'])

        corpus_reseñas = " | ".join(all_texts)

        consolidated_rows.append({
            'idx': row.get('idx'),
            'alcaldia': row.get('alcaldia'),
            'colonia': row.get('colonia'),
            'ubicacion': row.get('ubicacion'),
            'dia': row.get('dia'),
            'horario': row.get('horario'),
            'latitud': row.get('latitud'),
            'longitud': row.get('longitud'),
            'place_id': pid,
            'place_name_oficial': row.get('place_name'),
            'place_name_maps': place_data.get('nombre_maps', ''),
            'rating_google': place_data.get('rating'),
            'num_resenas_google': place_data.get('total_reviews', 0),
            'num_resenas_extraidas': len(reviews_list),
            'num_fotos_extraidas': len(fotos_list),
            'foto_principal': fotos_list[0] if fotos_list else '',
            'fotos_json': json.dumps(fotos_list, ensure_ascii=False),
            'temas_frecuentes_json': json.dumps([t['tema'] for t in temas_list if isinstance(t, dict)], ensure_ascii=False),
            'snippets_json': json.dumps(snippets_list, ensure_ascii=False),
            'resenas_texto_corpus': corpus_reseñas,
            'veredicto': row.get('veredicto')
        })

    df_out = pd.DataFrame(consolidated_rows)

    # 1. Exportar CSV
    csv_path = 'data/processed/tianguis_reviews.csv'
    df_out.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"✓ CSV guardado: {csv_path} ({os.path.getsize(csv_path) / 1024:.1f} KB)")

    # 2. Exportar JSON
    json_path = 'data/processed/tianguis_reviews.json'
    json_data = df_out.to_dict(orient='records')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON guardado: {json_path} ({os.path.getsize(json_path) / 1024:.1f} KB)")

    print("\n" + "=" * 70)
    print("MÉTRICAS DE EXTRACCIÓN (FASE 1 COMPLETADA):")
    print(f"• Total tianguis en padrón: {len(df_out):,}")
    tianguis_con_rating = df_out['rating_google'].notna().sum()
    print(f"• Tianguis con rating Google: {tianguis_con_rating:,} ({tianguis_con_rating/len(df_out)*100:.1f}%)")
    tianguis_con_fotos = (df_out['num_fotos_extraidas'] > 0).sum()
    print(f"• Tianguis con fotografías reales: {tianguis_con_fotos:,} ({tianguis_con_fotos/len(df_out)*100:.1f}%)")
    tianguis_con_corpus = (df_out['resenas_texto_corpus'].str.len() > 0).sum()
    print(f"• Tianguis con corpus de texto para NLP: {tianguis_con_corpus:,} ({tianguis_con_corpus/len(df_out)*100:.1f}%)")
    print("=" * 70)

if __name__ == '__main__':
    run()
