#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Etiquetado y Clasificación de Giros Comerciales para la CDMX
Chilangotón 2026 - Reto 1: Comercio Popular y Barrial

Permite clasificar texto libre, cédulas, notas de mercado y solicitudes de microcrédito
en una taxonomía jerárquica modular, detectando giros múltiples, canasta básica y Mercomuna.
"""

import os
import json
import re
import unicodedata
import pandas as pd
from typing import Dict, List, Any, Optional, Union

# Cargar catálogo base
CATALOG_PATH = os.path.join(os.path.dirname(__file__), "giros_catalogo.json")

def load_catalog(path: str = CATALOG_PATH) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

_CATALOG_DATA = load_catalog()
CATEGORIAS_MAP = {c["id"]: c for c in _CATALOG_DATA["categorias"]}
SUBGIROS_MAP = {sg["id"]: sg for sg in _CATALOG_DATA["subgiros"]}

# Precompilar expresiones regulares para rendimiento
COMPILED_RULES = []
for sg in _CATALOG_DATA["subgiros"]:
    regex_list = [re.compile(p, re.IGNORECASE) for p in sg.get("keywords_regex", [])]
    COMPILED_RULES.append((sg, regex_list))

# Patrón para términos genéricos de comercio ambulante o venta general
GENERIC_COMMERCE_PATTERN = re.compile(
    r"^\s*(COMERCIO|COMERCIAL|VENTAS?|COMERCIANTES?|PUESTO(\s+AMBULANTE)?|AMBULANTE|TIANGUIS|SERVICIOS?|ACCESORIOS|VENTA\s+DE\s+PRODUCTOS|TALLER)\s*$",
    re.IGNORECASE
)

def normalize_text(text: Any) -> str:
    """
    Normaliza texto libre eliminando acentos, estandarizando mayúsculas,
    y corrigiendo errores frecuentes de codificación (mojibake) en datasets de CDMX.
    """
    if text is None or pd.isna(text):
        return ""
    s = str(text).strip()
    try:
        s = s.encode('latin1').decode('utf-8')
    except Exception:
        pass
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^A-Z0-9\s]', ' ', s.upper())
    s = re.sub(r'\bUA\s*AS\b', 'UNAS', s)
    s = re.sub(r'\bALBAA\s*ILERIA\b', 'ALBANILERIA', s)
    s = re.sub(r'\bPIN\s*ATAS\b', 'PINATAS', s)
    return re.sub(r'\s+', ' ', s).strip()

def tag_giro(text: Any, return_full: bool = False) -> Dict[str, Any]:
    """
    Clasifica un texto de giro comercial en uno o múltiples subgiros del catálogo.

    Parámetros:
    - text: Texto crudo del giro (ej. 'Tacos de guisado y jugos', 'Tienda de Abarrotes', 'NA').
    - return_full: Si es True, incluye la metadata completa de cada subgiro detectado.

    Retorna:
    - Diccionario estructurado con status, giros asignados, giro principal, categorías,
      compatibilidad con canasta básica, Mercomuna y tipo de mercado CDMX.
    """
    norm_txt = normalize_text(text)
    
    # Manejo de registros vacíos, '0', o no especificados
    if not norm_txt or norm_txt in {'0', 'NA', 'N A', 'NULL', 'NINGUNO', 'NO APLICA', 'S N'}:
        return {
            "texto_original": text,
            "texto_normalizado": norm_txt,
            "status": "sin_informacion",
            "giros": [],
            "giro_principal": None,
            "categorias": [],
            "es_canasta_basica": False,
            "apto_mercomuna": False,
            "perecedero": False,
            "es_servicio": False,
            "tipo_mercado_cdmx": []
        }
    
    matched_scores = []
    # Evaluamos primero los giros específicos (todos excepto comercio_mixto_general)
    for sg, patterns in COMPILED_RULES:
        if sg["id"] == "comercio_mixto_general":
            continue
        score = sum(1 for pat in patterns if pat.search(norm_txt))
        if score > 0:
            matched_scores.append((sg, score))
            
    # Si no hubo match específico, probamos comercio_mixto_general o patrón genérico
    if not matched_scores:
        mixto_sg = SUBGIROS_MAP.get("comercio_mixto_general")
        if mixto_sg:
            mixto_pats = [p for s, p in COMPILED_RULES if s["id"] == "comercio_mixto_general"][0]
            score = sum(1 for pat in mixto_pats if pat.search(norm_txt))
            if score > 0 or GENERIC_COMMERCE_PATTERN.match(norm_txt):
                matched_scores.append((mixto_sg, max(score, 1)))

    if not matched_scores:
        return {
            "texto_original": text,
            "texto_normalizado": norm_txt,
            "status": "no_clasificado",
            "giros": [],
            "giro_principal": None,
            "categorias": [],
            "es_canasta_basica": False,
            "apto_mercomuna": False,
            "perecedero": False,
            "es_servicio": False,
            "tipo_mercado_cdmx": []
        }
        
    # Ordenar por especificidad / número de coincidencias
    matched_scores.sort(key=lambda x: x[1], reverse=True)
    matched_subgiros = [m[0] for m in matched_scores]
    
    primary = matched_subgiros[0]
    cat_ids = list(dict.fromkeys(s["categoria_id"] for s in matched_subgiros))
    
    result = {
        "texto_original": text,
        "texto_normalizado": norm_txt,
        "status": "clasificado",
        "giros": [s["id"] for s in matched_subgiros],
        "giro_principal": {
            "id": primary["id"],
            "nombre": primary["nombre"],
            "categoria_id": primary["categoria_id"],
            "categoria_nombre": CATEGORIAS_MAP.get(primary["categoria_id"], {}).get("nombre", "")
        },
        "categorias": cat_ids,
        "es_canasta_basica": any(s["canasta_basica"] for s in matched_subgiros),
        "apto_mercomuna": any(s["mercomuna"] for s in matched_subgiros),
        "perecedero": any(s["perecedero"] for s in matched_subgiros),
        "es_servicio": any(s["es_servicio"] for s in matched_subgiros),
        "tipo_mercado_cdmx": sorted(list(set(s["tipo_mercado_cdmx"] for s in matched_subgiros)))
    }
    
    if return_full:
        result["detalles_giros"] = matched_subgiros
        
    return result

def add_giro(comercio: Dict[str, Any], giro_id: str) -> Dict[str, Any]:
    """
    Agrega de forma modular un subgiro a la ficha de un comercio y recalcula
    automáticamente sus categorías y banderas de canasta básica y Mercomuna.
    """
    if giro_id not in SUBGIROS_MAP:
        raise ValueError(f"El giro_id '{giro_id}' no existe en el catálogo.")
    
    current_giros = list(comercio.get("giros", []))
    if giro_id not in current_giros:
        current_giros.append(giro_id)
        
    active_subgiros = [SUBGIROS_MAP[gid] for gid in current_giros if gid in SUBGIROS_MAP]
    cat_ids = list(dict.fromkeys(s["categoria_id"] for s in active_subgiros))
    
    updated = dict(comercio)
    updated["giros"] = current_giros
    updated["categorias"] = cat_ids
    updated["es_canasta_basica"] = any(s["canasta_basica"] for s in active_subgiros)
    updated["apto_mercomuna"] = any(s["mercomuna"] for s in active_subgiros)
    updated["perecedero"] = any(s["perecedero"] for s in active_subgiros)
    updated["es_servicio"] = any(s["es_servicio"] for s in active_subgiros)
    updated["tipo_mercado_cdmx"] = sorted(list(set(s["tipo_mercado_cdmx"] for s in active_subgiros)))
    
    if current_giros and ("giro_principal" not in updated or not updated["giro_principal"]):
        primary = SUBGIROS_MAP[current_giros[0]]
        updated["giro_principal"] = {
            "id": primary["id"],
            "nombre": primary["nombre"],
            "categoria_id": primary["categoria_id"],
            "categoria_nombre": CATEGORIAS_MAP.get(primary["categoria_id"], {}).get("nombre", "")
        }
    return updated

def remove_giro(comercio: Dict[str, Any], giro_id: str) -> Dict[str, Any]:
    """
    Elimina un subgiro de la ficha de un comercio y actualiza sus atributos.
    """
    current_giros = [g for g in comercio.get("giros", []) if g != giro_id]
    active_subgiros = [SUBGIROS_MAP[gid] for gid in current_giros if gid in SUBGIROS_MAP]
    cat_ids = list(dict.fromkeys(s["categoria_id"] for s in active_subgiros))
    
    updated = dict(comercio)
    updated["giros"] = current_giros
    updated["categorias"] = cat_ids
    updated["es_canasta_basica"] = any(s["canasta_basica"] for s in active_subgiros)
    updated["apto_mercomuna"] = any(s["mercomuna"] for s in active_subgiros)
    updated["perecedero"] = any(s["perecedero"] for s in active_subgiros)
    updated["es_servicio"] = any(s["es_servicio"] for s in active_subgiros)
    updated["tipo_mercado_cdmx"] = sorted(list(set(s["tipo_mercado_cdmx"] for s in active_subgiros)))
    
    if current_giros:
        primary = SUBGIROS_MAP[current_giros[0]]
        updated["giro_principal"] = {
            "id": primary["id"],
            "nombre": primary["nombre"],
            "categoria_id": primary["categoria_id"],
            "categoria_nombre": CATEGORIAS_MAP.get(primary["categoria_id"], {}).get("nombre", "")
        }
    else:
        updated["giro_principal"] = None
        
    return updated

def tag_dataframe(df: pd.DataFrame, text_column: str, prefix: str = "giro_") -> pd.DataFrame:
    """
    Aplica el motor de clasificación a una columna de un DataFrame de pandas.
    """
    results = df[text_column].apply(tag_giro)
    df_out = df.copy()
    df_out[f"{prefix}status"] = results.apply(lambda r: r["status"])
    df_out[f"{prefix}principal_id"] = results.apply(lambda r: r["giro_principal"]["id"] if r["giro_principal"] else None)
    df_out[f"{prefix}principal_nombre"] = results.apply(lambda r: r["giro_principal"]["nombre"] if r["giro_principal"] else None)
    df_out[f"{prefix}todos_ids"] = results.apply(lambda r: ",".join(r["giros"]) if r["giros"] else "")
    df_out[f"{prefix}categorias"] = results.apply(lambda r: ",".join(r["categorias"]) if r["categorias"] else "")
    df_out[f"{prefix}canasta_basica"] = results.apply(lambda r: r["es_canasta_basica"])
    df_out[f"{prefix}mercomuna"] = results.apply(lambda r: r["apto_mercomuna"])
    return df_out

if __name__ == "__main__":
    import sys
    test_str = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Tacos de guisado, carnitas y refrescos"
    res = tag_giro(test_str)
    print(f"=== CLASIFICACIÓN DE PRUEBA: '{test_str}' ===")
    print(json.dumps(res, ensure_ascii=False, indent=2))
