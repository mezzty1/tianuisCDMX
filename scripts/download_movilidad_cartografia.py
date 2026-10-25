#!/usr/bin/env python3
"""
Descarga y procesamiento de datasets de Movilidad Integrada (MI) y Cartografía Base CDMX.
Fuente: Portal de Datos Abiertos de la Ciudad de México (datos.cdmx.gob.mx)
"""

import os
import io
import json
import shutil
import tempfile
import urllib.request
import zipfile
import geopandas as gpd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CARTOGRAFIA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'cartografia')
TRANSPORTE_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'transporte')
GTFS_DIR = os.path.join(TRANSPORTE_DIR, 'gtfs')

os.makedirs(CARTOGRAFIA_DIR, exist_ok=True)
os.makedirs(TRANSPORTE_DIR, exist_ok=True)
os.makedirs(GTFS_DIR, exist_ok=True)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

def download_file(url, dest_path):
    print(f"Descargando {url} -> {dest_path}...")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as response, open(dest_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    print(f"  -> Guardado: {os.path.getsize(dest_path)} bytes")

def convert_shp_to_geojson(shp_path, geojson_path):
    print(f"Leyendo SHP: {shp_path}...")
    gdf = gpd.read_file(shp_path)
    if gdf.crs is None:
        # Asumir UTM 14N si tiene coordenadas > 1000
        sample_geom = gdf.geometry.dropna().iloc[0] if len(gdf) > 0 else None
        if sample_geom and (sample_geom.bounds[0] > 180 or sample_geom.bounds[0] < -180):
            gdf = gdf.set_crs(epsg=32614)
    if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
        print(f"  Reproyectando de {gdf.crs} a EPSG:4326...")
        gdf = gdf.to_crs(epsg=4326)
    gdf.to_file(geojson_path, driver='GeoJSON')
    print(f"  -> Guardado {geojson_path}: {len(gdf)} features")
    return len(gdf)

def process_datasets():
    stats = {}

    # 1. Alcaldías de la CDMX
    alcaldias_url = "https://datos.cdmx.gob.mx/dataset/bae265a8-d1f6-4614-b399-4184bc93e027/resource/deb5c583-84e2-4e07-a706-1b3a0dbc99b0/download/deb5c583-84e2-4e07-a706-1b3a0dbc99b0.json"
    alcaldias_geojson = os.path.join(CARTOGRAFIA_DIR, "alcaldias.geojson")
    download_file(alcaldias_url, alcaldias_geojson)
    gdf_alc = gpd.read_file(alcaldias_geojson)
    stats['cartografia/alcaldias.geojson'] = {
        'nombre': 'Límites de las 16 Alcaldías de la CDMX',
        'features': len(gdf_alc),
        'tipo': gdf_alc.geom_type.iloc[0] if len(gdf_alc) > 0 else 'Unknown',
        'origen': 'CKAN: alcaldias'
    }

    # 2. Catálogo de Colonias CDMX
    colonias_url = "https://datos.cdmx.gob.mx/dataset/02c6ce99-dbd8-47d8-aee1-ae885a12bb2f/resource/026b42d3-a609-44c7-a83d-22b2150caffc/download/026b42d3-a609-44c7-a83d-22b2150caffc.json"
    colonias_geojson = os.path.join(CARTOGRAFIA_DIR, "colonias.geojson")
    download_file(colonias_url, colonias_geojson)
    gdf_col = gpd.read_file(colonias_geojson)
    stats['cartografia/colonias.geojson'] = {
        'nombre': 'Catálogo de Colonias de la CDMX',
        'features': len(gdf_col),
        'tipo': gdf_col.geom_type.iloc[0] if len(gdf_col) > 0 else 'Unknown',
        'origen': 'CKAN: catalogo-de-colonias-datos-abiertos'
    }

    # 3. Metro CDMX
    metro_url = "https://datos.cdmx.gob.mx/dataset/1b014317-ddb1-46c7-ac79-7330c652abe3/resource/288b10dd-4f21-4338-b1ed-239487820512/download/288b10dd-4f21-4338-b1ed-239487820512.zip"
    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = os.path.join(tmp_dir, "metro.zip")
        download_file(metro_url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(tmp_dir)
        
        # Buscar shapefiles
        for root, dirs, files in os.walk(tmp_dir):
            for f in files:
                if f.endswith('.shp'):
                    full_p = os.path.join(root, f)
                    if 'estaciones' in f.lower():
                        dst = os.path.join(TRANSPORTE_DIR, "metro_estaciones.geojson")
                        n = convert_shp_to_geojson(full_p, dst)
                        stats['transporte/metro_estaciones.geojson'] = {
                            'nombre': 'Estaciones del STC Metro CDMX',
                            'features': n,
                            'tipo': 'Point',
                            'origen': 'CKAN: lineas-y-estaciones-del-metro'
                        }
                    elif 'lineas' in f.lower():
                        dst = os.path.join(TRANSPORTE_DIR, "metro_lineas.geojson")
                        n = convert_shp_to_geojson(full_p, dst)
                        stats['transporte/metro_lineas.geojson'] = {
                            'nombre': 'Líneas del STC Metro CDMX',
                            'features': n,
                            'tipo': 'LineString/MultiLineString',
                            'origen': 'CKAN: lineas-y-estaciones-del-metro'
                        }

    # 4. Metrobús CDMX
    metrobus_url = "https://datos.cdmx.gob.mx/dataset/63a08f93-e959-430f-8dc4-bf07182401e6/resource/66cd5773-d83f-4a80-8c15-8ab34851e046/download/66cd5773-d83f-4a80-8c15-8ab34851e046.zip"
    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = os.path.join(tmp_dir, "metrobus.zip")
        download_file(metrobus_url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(tmp_dir)
        
        for root, dirs, files in os.walk(tmp_dir):
            for f in files:
                if f.endswith('.shp'):
                    full_p = os.path.join(root, f)
                    if 'estaciones' in f.lower():
                        dst = os.path.join(TRANSPORTE_DIR, "metrobus_estaciones.geojson")
                        n = convert_shp_to_geojson(full_p, dst)
                        stats['transporte/metrobus_estaciones.geojson'] = {
                            'nombre': 'Estaciones del Metrobús CDMX',
                            'features': n,
                            'tipo': 'Point',
                            'origen': 'CKAN: geolocalizacion-metrobus'
                        }
                    elif 'lineas' in f.lower():
                        dst = os.path.join(TRANSPORTE_DIR, "metrobus_lineas.geojson")
                        n = convert_shp_to_geojson(full_p, dst)
                        stats['transporte/metrobus_lineas.geojson'] = {
                            'nombre': 'Líneas del Metrobús CDMX',
                            'features': n,
                            'tipo': 'LineString/MultiLineString',
                            'origen': 'CKAN: geolocalizacion-metrobus'
                        }

    # 5. STE (Cablebús, Tren Ligero, Trolebús)
    ste_url = "https://datos.cdmx.gob.mx/dataset/6a3bc652-a775-41a0-aeb6-05d31ee40b59/resource/c7a1b906-92ff-4525-9b0c-f166ea731f95/download/c7a1b906-92ff-4525-9b0c-f166ea731f95.zip"
    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = os.path.join(tmp_dir, "ste.zip")
        download_file(ste_url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(tmp_dir)
        
        # Descomprimir sub-zips
        for root, dirs, files in os.walk(tmp_dir):
            for f in files:
                if f.endswith('.zip'):
                    subz_path = os.path.join(root, f)
                    sub_extract = os.path.join(root, f.replace('.zip', ''))
                    with zipfile.ZipFile(subz_path, 'r') as sz:
                        sz.extractall(sub_extract)

        # Buscar shapefiles de STE
        for root, dirs, files in os.walk(tmp_dir):
            for f in files:
                if not f.endswith('.shp'):
                    continue
                full_p = os.path.join(root, f)
                fn_lower = f.lower()

                # Cablebús
                if 'cablebus' in fn_lower and 'estaciones' in fn_lower:
                    dst = os.path.join(TRANSPORTE_DIR, "cablebus_estaciones.geojson")
                    n = convert_shp_to_geojson(full_p, dst)
                    stats['transporte/cablebus_estaciones.geojson'] = {
                        'nombre': 'Estaciones del Cablebús CDMX',
                        'features': n,
                        'tipo': 'Point',
                        'origen': 'CKAN: geolocalizacion-de-lineas-y-estaciones-paradas-del-servicio-de-transportes-electricos'
                    }
                elif 'cablebus' in fn_lower and 'lineas' in fn_lower:
                    dst = os.path.join(TRANSPORTE_DIR, "cablebus_lineas.geojson")
                    n = convert_shp_to_geojson(full_p, dst)
                    stats['transporte/cablebus_lineas.geojson'] = {
                        'nombre': 'Líneas del Cablebús CDMX',
                        'features': n,
                        'tipo': 'LineString/MultiLineString',
                        'origen': 'CKAN: STE'
                    }

                # Tren Ligero
                elif 'trenligero' in fn_lower and 'estaciones' in fn_lower:
                    dst = os.path.join(TRANSPORTE_DIR, "tren_ligero_estaciones.geojson")
                    n = convert_shp_to_geojson(full_p, dst)
                    stats['transporte/tren_ligero_estaciones.geojson'] = {
                        'nombre': 'Estaciones del Tren Ligero CDMX',
                        'features': n,
                        'tipo': 'Point',
                        'origen': 'CKAN: STE'
                    }
                elif 'trenligero' in fn_lower and 'linea' in fn_lower:
                    dst = os.path.join(TRANSPORTE_DIR, "tren_ligero_linea.geojson")
                    n = convert_shp_to_geojson(full_p, dst)
                    stats['transporte/tren_ligero_linea.geojson'] = {
                        'nombre': 'Línea del Tren Ligero CDMX',
                        'features': n,
                        'tipo': 'LineString/MultiLineString',
                        'origen': 'CKAN: STE'
                    }

                # Trolebús
                elif 'trolebus' in fn_lower and 'paradas' in fn_lower:
                    dst = os.path.join(TRANSPORTE_DIR, "trolebus_paradas.geojson")
                    n = convert_shp_to_geojson(full_p, dst)
                    stats['transporte/trolebus_paradas.geojson'] = {
                        'nombre': 'Paradas del Trolebús CDMX',
                        'features': n,
                        'tipo': 'Point',
                        'origen': 'CKAN: STE'
                    }
                elif 'trolebus' in fn_lower and 'lineas' in fn_lower:
                    dst = os.path.join(TRANSPORTE_DIR, "trolebus_lineas.geojson")
                    n = convert_shp_to_geojson(full_p, dst)
                    stats['transporte/trolebus_lineas.geojson'] = {
                        'nombre': 'Líneas del Trolebús CDMX',
                        'features': n,
                        'tipo': 'LineString/MultiLineString',
                        'origen': 'CKAN: STE'
                    }

    # 6. RTP (Red de Transporte de Pasajeros)
    rtp_url = "https://datos.cdmx.gob.mx/dataset/e5e67126-8964-4457-a88b-ed0194bb5eb5/resource/391b1ea2-d5e6-4a60-a1fe-114ccb99ee82/download/391b1ea2-d5e6-4a60-a1fe-114ccb99ee82.zip"
    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = os.path.join(tmp_dir, "rtp.zip")
        download_file(rtp_url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(tmp_dir)
        
        for root, dirs, files in os.walk(tmp_dir):
            for f in files:
                if f.endswith('.shp'):
                    full_p = os.path.join(root, f)
                    if 'paradas' in f.lower():
                        dst = os.path.join(TRANSPORTE_DIR, "rtp_paradas.geojson")
                        n = convert_shp_to_geojson(full_p, dst)
                        stats['transporte/rtp_paradas.geojson'] = {
                            'nombre': 'Paradas de la Red de Transporte de Pasajeros (RTP)',
                            'features': n,
                            'tipo': 'Point',
                            'origen': 'CKAN: rutas-de-rtp'
                        }
                    elif 'lineas' in f.lower():
                        dst = os.path.join(TRANSPORTE_DIR, "rtp_lineas.geojson")
                        n = convert_shp_to_geojson(full_p, dst)
                        stats['transporte/rtp_lineas.geojson'] = {
                            'nombre': 'Rutas y Líneas de RTP',
                            'features': n,
                            'tipo': 'LineString/MultiLineString',
                            'origen': 'CKAN: rutas-de-rtp'
                        }

    # 7. GTFS estático oficial CDMX
    gtfs_url = "https://datos.cdmx.gob.mx/dataset/75538d96-3ade-4bc5-ae7d-d85595e4522d/resource/32ed1b6b-41cd-49b3-b7f0-b57acb0eb819/download/32ed1b6b-41cd-49b3-b7f0-b57acb0eb819.zip"
    gtfs_zip = os.path.join(TRANSPORTE_DIR, "gtfs_cdmx.zip")
    download_file(gtfs_url, gtfs_zip)
    with zipfile.ZipFile(gtfs_zip, 'r') as z:
        z.extractall(GTFS_DIR)
    
    # Contar registros en GTFS
    gtfs_files = [f for f in os.listdir(GTFS_DIR) if f.endswith('.txt')]
    gtfs_info = {}
    for gf in gtfs_files:
        with open(os.path.join(GTFS_DIR, gf), 'r', encoding='utf-8', errors='ignore') as f:
            lines = sum(1 for _ in f) - 1
            gtfs_info[gf] = lines

    stats['transporte/gtfs/'] = {
        'nombre': 'GTFS Oficial Estático de la CDMX (Movilidad Integrada)',
        'features': f"{gtfs_info.get('routes.txt', 0)} rutas, {gtfs_info.get('stops.txt', 0)} paradas, {gtfs_info.get('shapes.txt', 0)} puntos de forma",
        'tipo': 'GTFS Relational Tables (CSV/TXT)',
        'origen': 'CKAN: gtfs'
    }

    # 8. Generar README.md en data/raw/transporte/
    readme_path = os.path.join(TRANSPORTE_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# Datasets Oficiales de Transporte y Movilidad Integrada (CDMX)\n\n")
        f.write("Datasets espaciales y tabulares descargados y normalizados desde el Portal de Datos Abiertos de la Ciudad de México (`datos.cdmx.gob.mx`).\n\n")
        f.write("Todos los archivos GeoJSON fueron proyectados al estándar geográfico global **WGS84 (EPSG:4326)**.\n\n")
        f.write("## Inventario de Capas de Transporte\n\n")
        f.write("| Archivo | Subsistema / Capa | Geometría | Registros / Features | Paquete Origen en CKAN |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for k, v in stats.items():
            f.write(f"| `{k}` | {v['nombre']} | {v['tipo']} | **{v['features']}** | `{v['origen']}` |\n")

        f.write("\n## Detalle de Archivos GTFS (`data/raw/transporte/gtfs/`)\n\n")
        f.write("| Archivo GTFS | Registros |\n")
        f.write("| :--- | :--- |\n")
        for gf, cnt in sorted(gtfs_info.items()):
            f.write(f"| `{gf}` | {cnt:,} |\n")

        f.write("\n## Notas de Integración\n")
        f.write("- **Metro**: Incluye estaciones (puntos) y trazado de líneas (líneas) con atributos de línea y correspondencias.\n")
        f.write("- **Metrobús**: Incluye estaciones y líneas de los corredores 1 al 7.\n")
        f.write("- **Servicio de Transportes Eléctricos (STE)**: Cobertura completa de Cablebús (Líneas 1 y 2), Tren Ligero (Taxqueña-Xochimilco) y Red de Trolebús (líneas y paradas).\n")
        f.write("- **RTP**: Paradas y trazado de rutas de autobuses ordinarios y expresos.\n")
        f.write("- **GTFS**: Especificación estándar que unifica todos los modos de transporte de la CDMX.\n")

    print(f"\nResumen generado exitosamente en {readme_path}")
    return stats

if __name__ == '__main__':
    res = process_datasets()
    print("PROCESO COMPLETADO:")
    print(json.dumps(res, indent=2))
