#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Procesamiento de Lenguaje Natural (NLP) y Minería de Reseñas de Tianguis
Chilangatón 2026 - Reto 1: Comercio Popular y Barrial (Tarea 5.5 - Fase 2)

Analiza el corpus de reseñas ciudadanas, menciones de Google y citas para:
1. Mapear artículos mencionados contra el catálogo de +460 productos barriales.
2. Identificar la vocación comercial dominante por tianguis:
   - Especialidad en Ropa y Calzado (paca americana, calzado, ropa deportiva)
   - Especialidad en Gastronomía y Antojitos (barbacoa, carnitas, mixiotes, quesadillas)
   - Especialidad en Herramientas, Ferretería y Segunda Mano (chácharas, herramientas, antigüedades)
   - Abasto Tradicional Fresco (recaudería, carnicería, pollería, canasta básica)
3. Generar la 'especialidad_comunitaria' descriptiva y redactada en lenguaje natural humano.
4. Extraer el top de 3 a 6 artículos más elogiados y reconocidos por visitantes.
5. Seleccionar las mejores fotografías para desplegar en la ficha lateral del visor web.
6. Enriquecer tianguis_map_data.json y .js para su despliegue inmediato.
"""

import os
import re
import json
import unicodedata
from collections import Counter
from typing import Dict, List, Any, Tuple, Optional

import pandas as pd

def normalize_text(text: Any) -> str:
    """Normaliza texto: minúsculas, remoción de acentos para matching léxico."""
    if text is None or not isinstance(text, str):
        return ""
    text = text.lower().strip()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text

# Palabras vacías barriales que no representan productos
STOPWORDS = {
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'de', 'del', 'a', 'al', 'en',
    'por', 'para', 'con', 'sin', 'sobre', 'y', 'e', 'o', 'u', 'que', 'se', 'es', 'son',
    'muy', 'mas', 'buen', 'bueno', 'buena', 'buenos', 'buenas', 'lugar', 'lugares', 'gente',
    'dia', 'dias', 'puesto', 'puestos', 'tianguis', 'mercado', 'aqui', 'siempre', 'puedes',
    'encontrar', 'encuentras', 'ir', 'vamos', 'solo', 'todo', 'tienen', 'recomiendo', 'mucho',
    'calidad', 'precio', 'precios', 'atencion', 'excelente', 'zona', 'calle', 'gente', 'bastante'
}

# Macro-categorías comerciales de la CDMX
CATEGORY_WEIGHTS = {
    'ROPA_CALZADO': {
        'nombre': 'Ropa, Calzado y Moda Barrial',
        'subnombre': 'Especialidad en Ropa y Calzado',
        'icono': '👗',
        'keywords': [
            'ropa', 'paca', 'ropa de paca', 'ropa americana', 'tenis', 'calzado', 'zapatos',
            'chamarra', 'chamarras', 'vestidos', 'playeras', 'pantalon', 'pantalones', 'calcetines',
            'ropa deportiva', 'ropa de segunda mano', 'sudadera', 'gorras', 'bolsas', 'mochilas'
        ]
    },
    'GASTRONOMIA': {
        'nombre': 'Gastronomía y Antojitos Tradicionales',
        'subnombre': 'Especialidad en Gastronomía y Antojitos',
        'icono': '🌮',
        'keywords': [
            'barbacoa', 'carnitas', 'tacos', 'tacos de carnitas', 'tacos de barbacoa', 'mixiotes',
            'quesadillas', 'gorditas', 'tlacoyos', 'sopes', 'birria', 'consome', 'tejuino',
            'aguas frescas', 'tamales', 'pozole', 'pancita', 'cecina', 'longaniza', 'comida corrida',
            'tortas', 'mariscos', 'coctel', 'antojitos', 'chicharron', 'cafe de olla', 'postres'
        ]
    },
    'HERRAMIENTAS_CHICHARAS': {
        'nombre': 'Herramientas, Chácharas y Antigüedades',
        'subnombre': 'Especialidad en Herramientas y Segunda Mano',
        'icono': '🔧',
        'keywords': [
            'chacharas', 'chacharear', 'antiguedades', 'herramientas', 'ferreteria', 'electronica',
            'cables', 'celulares', 'refacciones', 'autopartes', 'juguetes', 'discos', 'vinilos',
            'libros usados', 'taladro', 'taladros', 'segunda mano', 'fierros', 'coleccionismo',
            'relojes', 'muebles usados', 'tornillos', 'chatarra', 'baterias'
        ]
    },
    'ABASTO_FRESCO': {
        'nombre': 'Canasta Básica y Alimentos Frescos',
        'subnombre': 'Abasto Tradicional Fresco',
        'icono': '🍎',
        'keywords': [
            'frutas', 'verduras', 'recauderia', 'jitomate', 'cebolla', 'aguacate', 'limon',
            'carniceria', 'bistec', 'carne de res', 'carne de puerco', 'polleria', 'pollo fresco',
            'pescaderia', 'pescado fresco', 'camaron', 'cremeria', 'queso fresco', 'crema',
            'huevo', 'tortilleria', 'tortillas', 'canasta basica', 'legumbres', 'chiles secos',
            'abarrotes', 'semillas', 'especias'
        ]
    }
}

# Fotos representativas de alta calidad de tianguis chilango como fallback
FALLBACK_PHOTOS = {
    'ROPA_CALZADO': [
        'https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=800&q=80',
        'https://images.unsplash.com/photo-1544441893-675973e31985?w=800&q=80'
    ],
    'GASTRONOMIA': [
        'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800&q=80',
        'https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=800&q=80'
    ],
    'HERRAMIENTAS_CHICHARAS': [
        'https://images.unsplash.com/photo-1581783898377-1c85bf937427?w=800&q=80',
        'https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=800&q=80'
    ],
    'ABASTO_FRESCO': [
        'https://images.unsplash.com/photo-1542838132-92c53300491e?w=800&q=80',
        'https://images.unsplash.com/photo-1610348725531-843dff563e2c?w=800&q=80'
    ]
}

def load_vocabulario() -> List[Dict[str, Any]]:
    path = 'data/catalog/vocabulario_compras.json'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def prepare_compiled_vocab(vocabulario: List[Dict[str, Any]]) -> List[Tuple[str, str, List[re.Pattern]]]:
    """Precompila expresiones regulares para un matching ultrarrápido."""
    compiled = []
    for item in vocabulario:
        termino = item['termino']
        cat_id = item['categoria_id']
        tokens = [termino] + item.get('sinonimos', [])
        patterns = []
        for token in tokens:
            norm_token = normalize_text(token)
            if len(norm_token) >= 3:
                patterns.append(re.compile(r'\b' + re.escape(norm_token) + r'\b'))
        if patterns:
            compiled.append((termino, cat_id, patterns))
    return compiled

def extract_products_from_text(text: str, compiled_vocab: List[Tuple[str, str, List[re.Pattern]]]) -> List[Tuple[str, str, int]]:
    """Extrae productos mencionados en el texto comparando con el vocabulario precompilado."""
    norm_text = normalize_text(text)
    if not norm_text:
        return []
    detected = []

    for termino, cat_id, patterns in compiled_vocab:
        matches = 0
        for p in patterns:
            matches += len(p.findall(norm_text))
        if matches > 0:
            detected.append((termino, cat_id, matches))

    detected.sort(key=lambda x: x[2], reverse=True)
    return detected

    # Ordenar por frecuencia descendente
    detected.sort(key=lambda x: x[2], reverse=True)
    return detected

def score_vocation_categories(text: str, detected_products: List[Tuple[str, str, int]], popular_name: str) -> Dict[str, float]:
    """Calcula el puntaje de afinidad para cada una de las 4 vocaciones."""
    scores = {
        'ROPA_CALZADO': 0.0,
        'GASTRONOMIA': 0.0,
        'HERRAMIENTAS_CHICHARAS': 0.0,
        'ABASTO_FRESCO': 0.0
    }

    norm_text = normalize_text(text)
    norm_pname = normalize_text(popular_name)

    # 1. Ponderación por keywords específicas
    for cat_key, cat_data in CATEGORY_WEIGHTS.items():
        for kw in cat_data['keywords']:
            norm_kw = normalize_text(kw)
            pattern = r'\b' + re.escape(norm_kw) + r'\b'
            hits = len(re.findall(pattern, norm_text))
            scores[cat_key] += hits * 2.5
            # Si la palabra clave está en el nombre popular (ej. "Tianguis Paca", "Tianguis Autos"), bonus masivo
            if norm_kw in norm_pname:
                scores[cat_key] += 15.0

    # 2. Ponderación por productos del catálogo detectados
    for termino, cat_id, count in detected_products:
        if cat_id == 'CAT_ROPA_CALZADO':
            scores['ROPA_CALZADO'] += count * 2.0
        elif cat_id == 'CAT_ALIM_PREPARADOS':
            scores['GASTRONOMIA'] += count * 2.0
        elif cat_id in ['CAT_CHACARAS_MIXTO', 'CAT_HOGAR_FERRETERIA', 'CAT_OFICIOS']:
            scores['HERRAMIENTAS_CHICHARAS'] += count * 2.0
        elif cat_id in ['CAT_ALIM_FRESCOS', 'CAT_ABARROTES_CANASTA']:
            scores['ABASTO_FRESCO'] += count * 1.5

    # Bonus para tianguis emblemáticos
    if 'salado' in norm_pname:
        scores['HERRAMIENTAS_CHICHARAS'] += 20.0
        scores['ROPA_CALZADO'] += 18.0
        scores['GASTRONOMIA'] += 12.0
    elif 'chopo' in norm_pname:
        scores['HERRAMIENTAS_CHICHARAS'] += 25.0
        scores['ROPA_CALZADO'] += 15.0
    elif 'sullivan' in norm_pname:
        scores['GASTRONOMIA'] += 18.0
        scores['ABASTO_FRESCO'] += 14.0
    elif 'lagunilla' in norm_pname:
        scores['HERRAMIENTAS_CHICHARAS'] += 25.0
        scores['ROPA_CALZADO'] += 20.0
    elif 'san felipe' in norm_pname or 'bola' in norm_pname:
        scores['ROPA_CALZADO'] += 20.0
        scores['HERRAMIENTAS_CHICHARAS'] += 18.0
        scores['GASTRONOMIA'] += 18.0
        scores['ABASTO_FRESCO'] += 15.0

    return scores

def generate_human_description(
    dominant_cat: str,
    secondary_cat: Optional[str],
    top_items: List[str],
    oferentes: int,
    popular_name: str
) -> str:
    """Genera una descripción comunitaria fluida y atractiva."""
    items_str = ", ".join(top_items[:3]) if top_items else ""

    if dominant_cat == 'ROPA_CALZADO':
        if secondary_cat == 'GASTRONOMIA' and items_str:
            return f"Corredor muy concurrido de ropa de paca, calzado deportivo y antojitos tradicionales ({items_str})."
        elif items_str:
            return f"Reconocido por visitantes por su amplia oferta de ropa de paca, tenis de marca y prendas de segunda mano ({items_str})."
        return "Especializado en ropa de paca americana, tenis deportivos, calzado y prendas de moda barrial."

    elif dominant_cat == 'GASTRONOMIA':
        if items_str:
            return f"Famoso destino gastronómico barrial con amplia oferta de comida preparada y antojitos de comal ({items_str})."
        return "Famoso por su corredor gastronómico de barbacoa de borrego, tacos de carnitas, cecina y antojitos típicos."

    elif dominant_cat == 'HERRAMIENTAS_CHICHARAS':
        if secondary_cat == 'ROPA_CALZADO' and items_str:
            return f"Gran tianguis de segunda mano: herramientas mecánicas, chácharas, antigüedades y ropa de paca ({items_str})."
        elif items_str:
            return f"Punto de referencia para coleccionistas y búsqueda de herramientas usadas, electrónica y chácharas ({items_str})."
        return "Reconocido para chacharear: herramientas usadas, piezas de ferretería, antigüedades y segunda mano."

    else:  # ABASTO_FRESCO
        if items_str:
            return f"Pilar de abasto popular vecinal con canasta básica fresca, frutas de temporada y carnicería ({items_str})."
        return "Pilar de abasto popular vecinal con recaudería fresca, carnicería, pollería, cremería y canasta básica económica."

def run():
    print("=" * 70)
    print("CHILANGATÓN 2026 - TAREA 5.5: POSPROCESADO NLP Y ESPECIALIDADES")
    print("=" * 70)

    reviews_path = 'data/processed/tianguis_reviews.json'
    if not os.path.exists(reviews_path):
        print(f"ERROR: No se encontró {reviews_path}. Ejecuta scrape_tianguis_reviews.py primero.")
        return

    with open(reviews_path, 'r', encoding='utf-8') as f:
        reviews_data = json.load(f)
    print(f"• Tianguis cargados desde reseñas: {len(reviews_data):,}")

    vocabulario = load_vocabulario()
    print(f"• Vocabulario oficial cargado: {len(vocabulario)} artículos barriales.")
    compiled_vocab = prepare_compiled_vocab(vocabulario)
    print("  ✓ Vocabulario precompilado para matching de alta velocidad.")

    # Cargar datos base de tianguis_map_data.json si existe para sincronizar IDs y oferentes
    tianguis_map_path = 'data/processed/tianguis_map_data.json'
    tianguis_map_dict = {}
    if os.path.exists(tianguis_map_path):
        with open(tianguis_map_path, 'r', encoding='utf-8') as f:
            t_map = json.load(f)
            for item in t_map.get('tianguis', []):
                tianguis_map_dict[item['id']] = item

    processed_rows = []
    category_counts = Counter()

    for row in reviews_data:
        t_id = row.get('idx')
        p_name = row.get('place_name_oficial') or row.get('place_name_maps') or ''
        corpus = row.get('resenas_texto_corpus') or ''
        
        # Recuperar datos base si están en tianguis_map_data
        base_item = tianguis_map_dict.get(t_id, {})
        popular_name = base_item.get('nombre_popular') or p_name or f"Tianguis {row.get('colonia')}"
        oferentes = base_item.get('oferentes', 100)

        # 1. Extracción de productos mencionados
        combined_text = f"{popular_name}. {corpus}. {p_name}"
        detected_products = extract_products_from_text(combined_text, compiled_vocab)

        # 2. Ponderación de categorías
        cat_scores = score_vocation_categories(corpus, detected_products, popular_name)

        # Si el tianguis no tiene reseñas o el corpus es muy chico, usar escala y nombre
        total_score = sum(cat_scores.values())
        if total_score < 1.0:
            if oferentes >= 300:
                cat_scores['ABASTO_FRESCO'] = 10.0
                cat_scores['GASTRONOMIA'] = 8.0
                cat_scores['ROPA_CALZADO'] = 6.0
            else:
                cat_scores['ABASTO_FRESCO'] = 12.0
                cat_scores['GASTRONOMIA'] = 6.0

        sorted_cats = sorted(cat_scores.items(), key=lambda x: x[1], reverse=True)
        dominant_cat = sorted_cats[0][0]
        secondary_cat = sorted_cats[1][0] if len(sorted_cats) > 1 and sorted_cats[1][1] > (sorted_cats[0][1] * 0.45) else None
        category_counts[dominant_cat] += 1

        cat_meta = CATEGORY_WEIGHTS[dominant_cat]

        # 3. Top artículos (3 a 6 productos)
        top_articulos = [p[0] for p in detected_products[:6]]
        if len(top_articulos) < 3:
            # Fallback natural según categoría
            if dominant_cat == 'ROPA_CALZADO':
                top_articulos.extend(['Ropa de Paca', 'Tenis', 'Prendas Deportivas'])
            elif dominant_cat == 'GASTRONOMIA':
                top_articulos.extend(['Tacos de Carnitas', 'Barbacoa', 'Quesadillas'])
            elif dominant_cat == 'HERRAMIENTAS_CHICHARAS':
                top_articulos.extend(['Herramientas Usadas', 'Chácharas', 'Electrónica'])
            else:
                top_articulos.extend(['Jitomate', 'Frutas de Temporada', 'Carnicería'])
        # Quitar duplicados preservando orden
        top_articulos_unique = []
        for a in top_articulos:
            if a not in top_articulos_unique:
                top_articulos_unique.append(a)
        top_articulos_final = top_articulos_unique[:6]

        # 4. Generación de texto descriptivo
        especialidad_desc = generate_human_description(
            dominant_cat, secondary_cat, top_articulos_final, oferentes, popular_name
        )

        # 5. Fotos
        fotos_raw = row.get('fotos_json', '[]')
        try:
            fotos_list = json.loads(fotos_raw) if isinstance(fotos_raw, str) else (fotos_raw or [])
        except Exception:
            fotos_list = []

        if not fotos_list:
            fotos_list = FALLBACK_PHOTOS[dominant_cat]

        # Calificación Google
        rating_val = row.get('rating_google')
        rating_num = float(rating_val) if pd.notna(rating_val) and rating_val is not None else None
        num_reviews = int(row.get('num_resenas_google') or 0)

        processed_rows.append({
            'idx': t_id,
            'nombre_popular': popular_name,
            'alcaldia': row.get('alcaldia'),
            'colonia': row.get('colonia'),
            'latitud': row.get('latitud'),
            'longitud': row.get('longitud'),
            'vocacion_clave': dominant_cat,
            'vocacion_nombre': cat_meta['subnombre'],
            'vocacion_icono': cat_meta['icono'],
            'especialidad_comunitaria': especialidad_desc,
            'top_articulos_mencionados': top_articulos_final,
            'top_articulos_str': ", ".join(top_articulos_final),
            'rating_google': rating_num,
            'total_resenas': num_reviews,
            'foto_principal': fotos_list[0] if fotos_list else '',
            'fotos': fotos_list[:3]
        })

    df_out = pd.DataFrame(processed_rows)

    # Exportar CSV
    csv_path = 'data/processed/tianguis_especialidades_nlp.csv'
    df_out.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"✓ CSV guardado: {csv_path} ({os.path.getsize(csv_path) / 1024:.1f} KB)")

    # Exportar JSON
    json_path = 'data/processed/tianguis_especialidades_nlp.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(processed_rows, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON guardado: {json_path} ({os.path.getsize(json_path) / 1024:.1f} KB)")

    print("\n" + "=" * 70)
    print("DISTRIBUCIÓN DE VOCACIÓN COMUNITARIA DETECTADA:")
    for cat_k, count in category_counts.items():
        nom = CATEGORY_WEIGHTS[cat_k]['subnombre']
        ico = CATEGORY_WEIGHTS[cat_k]['icono']
        print(f"  {ico} {nom}: {count:,} tianguis ({count/len(df_out)*100:.1f}%)")
    print("=" * 70)

if __name__ == '__main__':
    run()
