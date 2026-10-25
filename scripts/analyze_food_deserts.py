#!/usr/bin/env python3
"""
analyze_food_deserts.py
-----------------------
Chilangatón 2026 — Reto 1: Comercio Popular y Barrial (SEDECO / SECTEI / SAF)
Tarea 6.3: Detección y Análisis Espacial de "Desiertos de Abasto Popular y Fresco"
en la Ciudad de México y ZMVM.

Metodología:
- Proyección cartográfica a UTM Zona 14N (EPSG:32614) para cálculo métrico de distancias y áreas.
- Buffers isócronos de caminabilidad:
  * 500 m (~6-7 min a pie): Abasto Pleno.
  * 1,000 m (~12-15 min a pie): Abasto Moderado.
  * > 1,000 m: Desierto de Abasto Popular y Fresco.
- Análisis dinámico temporal: Cobertura por día de la semana (Lunes a Domingo) y detección de Días Críticos.
- Cálculo de métricas agregadas por Alcaldía:
  * Área cubierta territorial a 500m y 1,000m.
  * Cobertura de colonias urbanas habitadas.
  * Índice de Severidad de Desierto de Abasto Popular (ISDAP, 0 a 100).
  * Top 5 colonias prioritarias por alcaldía con necesidad urgente de tianguis/rutas móviles.
- Generación de datasets duales (JSON y CSV) en data/processed/.
"""

import os
import sys
import json
import csv
import time
import unicodedata
import warnings
from collections import defaultdict

import pyproj
from shapely.geometry import shape, Point
from shapely.ops import unary_union, transform

warnings.filterwarnings("ignore")

# Rutas de entrada y salida
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIANGUIS_PATH = os.path.join(BASE_DIR, "data", "processed", "tianguis_limpio.json")
ALCALDIAS_GEO_PATH = os.path.join(BASE_DIR, "data", "raw", "cartografia", "alcaldias.geojson")
COLONIAS_GEO_PATH = os.path.join(BASE_DIR, "data", "raw", "cartografia", "colonias.geojson")

OUTPUT_DESIERTOS_JSON = os.path.join(BASE_DIR, "data", "processed", "desiertos_abasto_cdmx.json")
OUTPUT_DESIERTOS_CSV = os.path.join(BASE_DIR, "data", "processed", "desiertos_abasto_cdmx.csv")
OUTPUT_COBERTURA_JSON = os.path.join(BASE_DIR, "data", "processed", "cobertura_tianguis_alcaldias.json")
OUTPUT_COBERTURA_CSV = os.path.join(BASE_DIR, "data", "processed", "cobertura_tianguis_alcaldias.csv")

DAYS = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"]


def clean_canonical_name(s: str) -> str:
    """Normaliza texto eliminando acentos y mayúsculas para nombres canónicos."""
    if not s:
        return ""
    norm = unicodedata.normalize("NFD", s)
    res = "".join(c for c in norm if unicodedata.category(c) != "Mn")
    return res.strip().upper()


def main():
    start_time = time.time()
    print("================================================================================")
    print(" CHILANGATÓN 2026 — DETECCIÓN Y ANÁLISIS DE DESIERTOS DE ABASTO POPULAR Y FRESCO")
    print("================================================================================\n")

    # 1. Configurar transformadores de coordenadas
    wgs84 = pyproj.CRS("EPSG:4326")
    utm14n = pyproj.CRS("EPSG:32614")
    t_to_utm = pyproj.Transformer.from_crs(wgs84, utm14n, always_xy=True).transform

    # 2. Cargar Tianguis georreferenciados
    print(f"[*] Cargando catálogo de tianguis desde: {TIANGUIS_PATH}")
    with open(TIANGUIS_PATH, "r", encoding="utf-8") as f:
        tianguis_raw = json.load(f)

    tianguis_valid = []
    day_tianguis_pts = {d: [] for d in DAYS}
    all_tianguis_pts = []
    tianguis_records = []

    oferentes_per_alc = defaultdict(int)
    tianguis_per_alc = defaultdict(int)

    for item in tianguis_raw:
        if item.get("coordenadas_validas") and item.get("lng") and item.get("lat"):
            x_utm, y_utm = t_to_utm(item["lng"], item["lat"])
            pt = Point(x_utm, y_utm)
            tianguis_valid.append(item)
            all_tianguis_pts.append(pt)
            tianguis_records.append((item, pt))

            alc_norm = clean_canonical_name(item.get("alcaldia", ""))
            oferentes_per_alc[alc_norm] += (item.get("num_oferentes") or 0)
            tianguis_per_alc[alc_norm] += 1

            for d in DAYS:
                if item.get(d.lower()):
                    day_tianguis_pts[d].append(pt)

    print(f"    - Tianguis cargados: {len(tianguis_raw):,}")
    print(f"    - Tianguis válidos georreferenciados: {len(tianguis_valid):,}")
    for d in DAYS:
        print(f"      * {d.capitalize():9s}: {len(day_tianguis_pts[d]):3d} tianguis activos")

    # 3. Generar Buffers Isócronos de Caminabilidad (500m y 1,000m)
    print("\n[*] Generando buffers de caminabilidad (500 m y 1,000 m) y uniones espaciales...")
    t_buf0 = time.time()
    union_500m = unary_union([p.buffer(500) for p in all_tianguis_pts])
    union_1000m = unary_union([p.buffer(1000) for p in all_tianguis_pts])
    day_unions_1000m = {d: unary_union([p.buffer(1000) for p in day_tianguis_pts[d]]) for d in DAYS}
    print(f"    - Buffers calculados en {time.time() - t_buf0:.2f} s")
    print(f"    - Cobertura global de buffers a 500m: {union_500m.area / 1e6:.2f} km²")
    print(f"    - Cobertura global de buffers a 1,000m: {union_1000m.area / 1e6:.2f} km²")

    # 4. Cargar cartografía de Alcaldías
    print(f"\n[*] Cargando polígonos de las 16 Alcaldías desde: {ALCALDIAS_GEO_PATH}")
    with open(ALCALDIAS_GEO_PATH, "r", encoding="utf-8") as f:
        alcaldias_geo = json.load(f)

    # 5. Cargar cartografía de Colonias
    print(f"[*] Cargando polígonos de colonias desde: {COLONIAS_GEO_PATH}")
    with open(COLONIAS_GEO_PATH, "r", encoding="utf-8") as f:
        colonias_geo = json.load(f)

    print(f"    - Total colonias registradas: {len(colonias_geo['features']):,}")

    # 6. Procesar Análisis de Colonias (Desiertos de Abasto a nivel micro-territorial)
    print("\n[*] Procesando métricas de distancia, caminabilidad y clasificación por colonia...")
    colonias_analysis = []
    colonias_by_alc = defaultdict(list)

    for feat in colonias_geo["features"]:
        props = feat["properties"]
        geom_wgs = shape(feat["geometry"])
        geom_utm = transform(t_to_utm, geom_wgs)
        cp_utm = geom_utm.centroid
        cp_wgs = cp_utm

        alc_clean = clean_canonical_name(props.get("alc", ""))
        cve_col = props.get("cve_col", "")
        nombre_col = props.get("colonia", "")
        clasif = props.get("clasif", "Colonia")

        # Distancia mínima global y tianguis más cercano
        min_dist_m = float("inf")
        nearest_tianguis = None
        for item, pt in tianguis_records:
            d = cp_utm.distance(pt)
            if d < min_dist_m:
                min_dist_m = d
                nearest_tianguis = item

        # Distancias diarias por día de la semana
        daily_dists = {}
        covered_days = 0
        for d in DAYS:
            pts = day_tianguis_pts[d]
            if pts:
                min_d_day = min(cp_utm.distance(p) for p in pts)
            else:
                min_d_day = 99999.0
            daily_dists[d] = min_d_day
            if min_d_day <= 1000.0:
                covered_days += 1

        # Día crítico (el día donde el tianguis activo más cercano está a mayor distancia)
        crit_day, crit_dist = max(daily_dists.items(), key=lambda x: x[1])

        # Clasificación de abasto
        if min_dist_m <= 500.0:
            clasif_abasto = "ABASTO_PLENO"
        elif min_dist_m <= 1000.0:
            clasif_abasto = "ABASTO_MODERADO"
        else:
            clasif_abasto = "DESIERTO_ABASTO"

        # Tiempo de caminata estimado a 4.5 km/h (75 m/min)
        tiempo_caminata_min = round(min_dist_m / 75.0, 1)

        # Índice de vulnerabilidad de abasto de la colonia (0 a 100)
        # Factor distancia mínima (hasta 80 pts) + Factor déficit de días a la semana (hasta 20 pts)
        if min_dist_m <= 500.0:
            base_score = (min_dist_m / 500.0) * 20.0
        elif min_dist_m <= 1000.0:
            base_score = 20.0 + ((min_dist_m - 500.0) / 500.0) * 30.0
        else:
            base_score = 50.0 + min(30.0, ((min_dist_m - 1000.0) / 1000.0) * 30.0)

        temporal_penalty = ((7 - covered_days) / 7.0) * 20.0
        vuln_score = round(min(100.0, base_score + temporal_penalty), 1)

        if vuln_score >= 60.0:
            prioridad = "ALTA"
        elif vuln_score >= 35.0:
            prioridad = "MEDIA"
        else:
            prioridad = "BAJA"

        # Obtener lat/lng del centroide
        centroid_lon, centroid_lat = pyproj.Transformer.from_crs(utm14n, wgs84, always_xy=True).transform(cp_utm.x, cp_utm.y)

        col_record = {
            "cve_col": cve_col,
            "colonia": nombre_col,
            "cve_alc": props.get("cve_alc", ""),
            "alcaldia": alc_clean,
            "clasif": clasif,
            "lat_centroide": round(centroid_lat, 6),
            "lng_centroide": round(centroid_lon, 6),
            "distancia_minima_m": round(min_dist_m, 1),
            "tiempo_caminata_min": tiempo_caminata_min,
            "clasificacion_abasto": clasif_abasto,
            "tianguis_mas_cercano_id": nearest_tianguis["id"] if nearest_tianguis else "",
            "tianguis_mas_cercano_nombre": nearest_tianguis["nombre"] if nearest_tianguis else "",
            "tianguis_mas_cercano_dia": nearest_tianguis["dia"] if nearest_tianguis else "",
            "dias_cobertura_semanal": covered_days,
            "dia_critico": crit_day,
            "distancia_dia_critico_m": round(crit_dist, 1),
            "dist_lunes_m": round(daily_dists["LUNES"], 1),
            "dist_martes_m": round(daily_dists["MARTES"], 1),
            "dist_miercoles_m": round(daily_dists["MIERCOLES"], 1),
            "dist_jueves_m": round(daily_dists["JUEVES"], 1),
            "dist_viernes_m": round(daily_dists["VIERNES"], 1),
            "dist_sabado_m": round(daily_dists["SABADO"], 1),
            "dist_domingo_m": round(daily_dists["DOMINGO"], 1),
            "indice_vulnerabilidad_abasto": vuln_score,
            "prioridad_intervencion": prioridad
        }

        colonias_analysis.append(col_record)
        colonias_by_alc[alc_clean].append(col_record)

    # 7. Procesar Análisis por Alcaldía
    print("\n[*] Procesando cobertura territorial, densidades e ISDAP por alcaldía...")
    alcaldias_analysis = []

    for feat in alcaldias_geo["features"]:
        props = feat["properties"]
        alc_clean = clean_canonical_name(props.get("NOMGEO", ""))
        geom_wgs = shape(feat["geometry"])
        geom_utm = transform(t_to_utm, geom_wgs)
        tot_area_m2 = geom_utm.area
        tot_area_km2 = tot_area_m2 / 1e6

        # Cobertura global de buffers
        cov_500_m2 = geom_utm.intersection(union_500m).area
        cov_1000_m2 = geom_utm.intersection(union_1000m).area
        cov_500_km2 = cov_500_m2 / 1e6
        cov_1000_km2 = cov_1000_m2 / 1e6
        pct_cov_500 = (cov_500_m2 / tot_area_m2) * 100.0
        pct_cov_1000 = (cov_1000_m2 / tot_area_m2) * 100.0
        desierto_area_km2 = tot_area_km2 - cov_1000_km2
        pct_desierto_area = 100.0 - pct_cov_1000

        # Cobertura diaria
        daily_cov_pcts = {}
        daily_tianguis_count = {d: 0 for d in DAYS}
        for d in DAYS:
            daily_union = day_unions_1000m[d]
            cov_d_m2 = geom_utm.intersection(daily_union).area
            daily_cov_pcts[d] = (cov_d_m2 / tot_area_m2) * 100.0

        # Contar tianguis de esta alcaldía activos por día
        for item, _ in tianguis_records:
            if clean_canonical_name(item.get("alcaldia", "")) == alc_clean:
                for d in DAYS:
                    if item.get(d.lower()):
                        daily_tianguis_count[d] += 1

        crit_day_alc, crit_cov_pct = min(daily_cov_pcts.items(), key=lambda x: x[1])
        avg_daily_cov = sum(daily_cov_pcts.values()) / 7.0

        # Métricas de colonias en la alcaldía
        cols = colonias_by_alc.get(alc_clean, [])
        tot_cols = len(cols)
        cols_pleno = sum(1 for c in cols if c["clasificacion_abasto"] == "ABASTO_PLENO")
        cols_mod = sum(1 for c in cols if c["clasificacion_abasto"] == "ABASTO_MODERADO")
        cols_des = sum(1 for c in cols if c["clasificacion_abasto"] == "DESIERTO_ABASTO")

        pct_cols_pleno = (cols_pleno / tot_cols * 100.0) if tot_cols else 0.0
        pct_cols_mod = (cols_mod / tot_cols * 100.0) if tot_cols else 0.0
        pct_cols_des = (cols_des / tot_cols * 100.0) if tot_cols else 0.0

        avg_dist_col = (sum(c["distancia_minima_m"] for c in cols) / tot_cols) if tot_cols else 0.0
        max_dist_col = max((c["distancia_minima_m"] for c in cols), default=0.0)

        # Oferentes y densidad
        num_t = tianguis_per_alc.get(alc_clean, 0)
        num_of = oferentes_per_alc.get(alc_clean, 0)
        dens_t = num_t / tot_area_km2
        dens_of = num_of / tot_area_km2

        # Cálculo de Índice de Severidad de Desierto de Abasto Popular (ISDAP)
        # Ponderación rigurosa:
        # - 35% % de área en desierto (>1,000 m)
        # - 35% % de colonias habitadas en desierto (>1,000 m)
        # - 20% Déficit temporal promedio diario (100 - avg_daily_cov)
        # - 10% Penalización por baja densidad de oferentes (menor a 500 oferentes/km2)
        dens_penalty = max(0.0, min(100.0, (1.0 - (dens_of / 500.0)) * 100.0))
        isdap = (0.35 * pct_desierto_area) + (0.35 * pct_cols_des) + (0.20 * (100.0 - avg_daily_cov)) + (0.10 * dens_penalty)
        isdap = round(min(100.0, max(0.0, isdap)), 1)

        # Top 5 colonias prioritarias
        # Ordenadas por mayor distancia mínima y menor número de días cubiertos
        sorted_cols = sorted(cols, key=lambda x: (x["distancia_minima_m"], 7 - x["dias_cobertura_semanal"]), reverse=True)
        top5_cols = []
        for c in sorted_cols[:5]:
            top5_cols.append({
                "colonia": c["colonia"],
                "cve_col": c["cve_col"],
                "distancia_minima_m": c["distancia_minima_m"],
                "tiempo_caminata_min": c["tiempo_caminata_min"],
                "dias_cobertura_semanal": c["dias_cobertura_semanal"],
                "dia_critico": c["dia_critico"],
                "distancia_dia_critico_m": c["distancia_dia_critico_m"],
                "tianguis_mas_cercano": c["tianguis_mas_cercano_nombre"]
            })

        top5_str = "; ".join([f"{i+1}. {c['colonia']} ({c['distancia_minima_m']}m, {c['dias_cobertura_semanal']}d/sem, Peor:{c['dia_critico']})" for i, c in enumerate(top5_cols)])

        alc_record = {
            "alcaldia": alc_clean,
            "cve_alc": props.get("CVE_MUN", props.get("CVEGEO", "")),
            "superficie_km2": round(tot_area_km2, 2),
            "num_tianguis": num_t,
            "densidad_tianguis_km2": round(dens_t, 2),
            "num_oferentes_estimado": num_of,
            "densidad_oferentes_km2": round(dens_of, 1),
            "cobertura_area_500m_km2": round(cov_500_km2, 2),
            "pct_cobertura_500m": round(pct_cov_500, 1),
            "cobertura_area_1000m_km2": round(cov_1000_km2, 2),
            "pct_cobertura_1000m": round(pct_cov_1000, 1),
            "area_desierto_km2": round(desierto_area_km2, 2),
            "pct_area_desierto": round(pct_desierto_area, 1),
            "total_colonias": tot_cols,
            "colonias_abasto_pleno": cols_pleno,
            "pct_colonias_abasto_pleno": round(pct_cols_pleno, 1),
            "colonias_abasto_moderado": cols_mod,
            "pct_colonias_abasto_moderado": round(pct_cols_mod, 1),
            "colonias_desierto": cols_des,
            "pct_colonias_desierto": round(pct_cols_des, 1),
            "distancia_promedio_colonia_m": round(avg_dist_col, 1),
            "distancia_maxima_colonia_m": round(max_dist_col, 1),
            "cobertura_pct_lunes": round(daily_cov_pcts["LUNES"], 1),
            "cobertura_pct_martes": round(daily_cov_pcts["MARTES"], 1),
            "cobertura_pct_miercoles": round(daily_cov_pcts["MIERCOLES"], 1),
            "cobertura_pct_jueves": round(daily_cov_pcts["JUEVES"], 1),
            "cobertura_pct_viernes": round(daily_cov_pcts["VIERNES"], 1),
            "cobertura_pct_sabado": round(daily_cov_pcts["SABADO"], 1),
            "cobertura_pct_domingo": round(daily_cov_pcts["DOMINGO"], 1),
            "dia_critico_alcaldia": crit_day_alc,
            "cobertura_pct_dia_critico": round(crit_cov_pct, 1),
            "tianguis_dia_critico": daily_tianguis_count[crit_day_alc],
            "indice_severidad_desierto": isdap,
            "top5_colonias_prioritarias": top5_cols,
            "top5_colonias_str": top5_str
        }
        alcaldias_analysis.append(alc_record)

    # Ordenar alcaldías por ISDAP de mayor severidad a menor
    alcaldias_analysis.sort(key=lambda x: x["indice_severidad_desierto"], reverse=True)

    # 8. Guardar Datasets Derivados Duales (JSON y CSV)
    print("\n[*] Exportando datasets procesados...")

    # A) Colonias (Desiertos de Abasto)
    with open(OUTPUT_DESIERTOS_JSON, "w", encoding="utf-8") as f:
        json.dump(colonias_analysis, f, ensure_ascii=False, indent=2)
    print(f"    [+] JSON Colonias generado: {OUTPUT_DESIERTOS_JSON} ({len(colonias_analysis)} registros)")

    colonias_csv_headers = list(colonias_analysis[0].keys())
    with open(OUTPUT_DESIERTOS_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=colonias_csv_headers)
        writer.writeheader()
        writer.writerows(colonias_analysis)
    print(f"    [+] CSV Colonias generado: {OUTPUT_DESIERTOS_CSV}")

    # B) Alcaldías (Cobertura Consolidada)
    # Para el JSON incluimos top5_colonias_prioritarias estructurado
    with open(OUTPUT_COBERTURA_JSON, "w", encoding="utf-8") as f:
        json.dump(alcaldias_analysis, f, ensure_ascii=False, indent=2)
    print(f"    [+] JSON Alcaldías generado: {OUTPUT_COBERTURA_JSON} ({len(alcaldias_analysis)} alcaldías)")

    # Para el CSV excluimos la lista anidada y dejamos top5_colonias_str renombrado a top5_colonias_prioritarias
    alcaldias_csv_rows = []
    for alc in alcaldias_analysis:
        row = dict(alc)
        row["top5_colonias_prioritarias"] = row.pop("top5_colonias_str")
        alcaldias_csv_rows.append(row)

    alcaldias_csv_headers = list(alcaldias_csv_rows[0].keys())
    with open(OUTPUT_COBERTURA_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=alcaldias_csv_headers)
        writer.writeheader()
        writer.writerows(alcaldias_csv_rows)
    print(f"    [+] CSV Alcaldías generado: {OUTPUT_COBERTURA_CSV}")

    # 9. Resumen Ejecutivo en Terminal
    header_str = f"{'RANK':4s} | {'ALCALDIA':22s} | {'ISDAP':5s} | {'% DESIERTO':11s} | {'% COL DES':9s} | {'COV 1KM':7s} | {'PEOR DIA (COV %)':18s} | {'DENS TIANG/km²':14s}"
    print("\n" + "="*len(header_str))
    print(header_str)
    print("="*len(header_str))
    for idx, r in enumerate(alcaldias_analysis, 1):
        crit_info = f"{r['dia_critico_alcaldia']} ({r['cobertura_pct_dia_critico']:4.1f}%)"
        print(f"{idx:4d} | {r['alcaldia']:22s} | {r['indice_severidad_desierto']:5.1f} | {r['pct_area_desierto']:10.1f}% | {r['pct_colonias_desierto']:8.1f}% | {r['pct_cobertura_1000m']:6.1f}% | {crit_info:18s} | {r['densidad_tianguis_km2']:14.2f}")
    print("="*len(header_str))

    tot_des_cols = sum(1 for c in colonias_analysis if c["clasificacion_abasto"] == "DESIERTO_ABASTO")
    pct_tot_des = (tot_des_cols / len(colonias_analysis)) * 100.0
    print(f"\nResumen Global CDMX:")
    print(f"  - Total Colonias Evaluadas: {len(colonias_analysis):,}")
    print(f"  - Colonias en Abasto Pleno (<500m): {sum(1 for c in colonias_analysis if c['clasificacion_abasto'] == 'ABASTO_PLENO'):,} ({sum(1 for c in colonias_analysis if c['clasificacion_abasto'] == 'ABASTO_PLENO')/len(colonias_analysis)*100:.1f}%)")
    print(f"  - Colonias en Abasto Moderado (500-1000m): {sum(1 for c in colonias_analysis if c['clasificacion_abasto'] == 'ABASTO_MODERADO'):,} ({sum(1 for c in colonias_analysis if c['clasificacion_abasto'] == 'ABASTO_MODERADO')/len(colonias_analysis)*100:.1f}%)")
    print(f"  - Colonias en Desierto de Abasto (>1000m): {tot_des_cols:,} ({pct_tot_des:.1f}%)")
    print(f"  - Tiempo total de ejecución: {time.time() - start_time:.2f} segundos.")
    print("Proceso completado con éxito (código de salida 0).\n")


if __name__ == "__main__":
    main()
