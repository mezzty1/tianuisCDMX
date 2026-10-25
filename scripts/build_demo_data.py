import os
import json
import pandas as pd

def run():
    print("Iniciando procesamiento de datos enriquecido (Metrópoli + RTP + MI)...")
    os.makedirs('data/processed', exist_ok=True)
    
    # 1. Cargar alcaldias CDMX
    alcaldias_path = 'data/raw/cartografia/alcaldias.geojson'
    with open(alcaldias_path, 'r', encoding='utf-8') as f:
        alcaldias_geojson = json.load(f)
    print(f"Alcaldías CDMX cargadas: {len(alcaldias_geojson['features'])} features")

    # 2. Cargar Municipios Conurbados del Área Metropolitana (Edomex e Hidalgo)
    zmvm_path = 'data/raw/cartografia/zmvm_edomex_opt.geojson'
    zmvm_geojson = None
    if os.path.exists(zmvm_path):
        with open(zmvm_path, 'r', encoding='utf-8') as f:
            zmvm_geojson = json.load(f)
        print(f"Municipios conurbados ZMVM cargados: {len(zmvm_geojson['features'])} features")

    # 3. Cargar GTFS
    print("Cargando GTFS...")
    routes_df = pd.read_csv('data/raw/transporte/gtfs/routes.txt')
    trips_df = pd.read_csv('data/raw/transporte/gtfs/trips.txt')
    shapes_df = pd.read_csv('data/raw/transporte/gtfs/shapes.txt')
    
    # Asignar colores oficiales del Metro
    metro_colors = {
        '1': '#F04E98', 'Línea 1': '#F04E98',
        '2': '#0057B8', 'Línea 2': '#0057B8',
        '3': '#808200', 'Línea 3': '#808200',
        '4': '#6EC4E8', 'Línea 4': '#6EC4E8',
        '5': '#FCD116', 'Línea 5': '#FCD116',
        '6': '#D62828', 'Línea 6': '#D62828',
        '7': '#FF7F32', 'Línea 7': '#FF7F32',
        '8': '#009A44', 'Línea 8': '#009A44',
        '9': '#6C3B14', 'Línea 9': '#6C3B14',
        'A': '#8F1A95', 'Línea A': '#8F1A95',
        'B': '#007A3D', 'Línea B': '#007A3D',
        '12': '#B59A57', 'Línea 12': '#B59A57',
    }

    # Capas de transporte
    transport_layers = {
        'METRO': {'name': 'Metro (STC)', 'color': '#E53935', 'features': []},
        'MB': {'name': 'Metrobús', 'color': '#D81B60', 'features': []},
        'CBB': {'name': 'Cablebús', 'color': '#00A3E0', 'features': []},
        'TROLE': {'name': 'Trolebús (STE)', 'color': '#00897B', 'features': []},
        'TL': {'name': 'Tren Ligero (STE)', 'color': '#1E88E5', 'features': []},
        'RTP': {'name': 'RTP (Red Pasajeros - Sinergia RTPonky)', 'color': '#2E7D32', 'features': []},
        'CC': {'name': 'Corredores Concesionados (Secundario)', 'color': '#8E24AA', 'features': []}
    }

    trip_route_map = trips_df[['trip_id', 'route_id', 'shape_id', 'trip_headsign']].drop_duplicates(subset=['shape_id'])
    merged_routes = trip_route_map.merge(routes_df, on='route_id', how='inner')
    shapes_grouped = shapes_df.sort_values(['shape_id', 'shape_pt_sequence']).groupby('shape_id')
    
    cc_count = 0
    rtp_count = 0
    
    for shape_id, group in shapes_grouped:
        r_info = merged_routes[merged_routes['shape_id'] == shape_id]
        if r_info.empty:
            continue
        row = r_info.iloc[0]
        agency = row['agency_id']
        if agency not in transport_layers:
            continue
        
        # Muestra balanceada de CC y RTP para fluidez del mapa
        if agency == 'CC':
            if cc_count >= 25:
                continue
            cc_count += 1
        elif agency == 'RTP':
            if rtp_count >= 30:
                continue
            rtp_count += 1
            
        r_short = str(row['route_short_name']) if pd.notnull(row['route_short_name']) else ''
        r_long = str(row['route_long_name']) if pd.notnull(row['route_long_name']) else ''
        headsign = str(row['trip_headsign']) if pd.notnull(row['trip_headsign']) else ''
        
        line_color = transport_layers[agency]['color']
        if agency == 'METRO':
            for k, c in metro_colors.items():
                if k.lower() in r_short.lower() or k.lower() in r_long.lower():
                    line_color = c
                    break

        coords = group[['shape_pt_lon', 'shape_pt_lat']].values.tolist()
        if len(coords) > 200:
            coords = coords[::2]

        feature = {
            'type': 'Feature',
            'properties': {
                'agency': agency,
                'agency_name': transport_layers[agency]['name'],
                'route_id': str(row['route_id']),
                'route_short': r_short,
                'route_long': r_long,
                'headsign': headsign,
                'color': line_color,
                'weight': 4 if agency in ['METRO', 'MB', 'CBB'] else 2.5,
                'opacity': 0.85
            },
            'geometry': {
                'type': 'LineString',
                'coordinates': coords
            }
        }
        transport_layers[agency]['features'].append(feature)

    print("Resumen de transporte:")
    for k, v in transport_layers.items():
        print(f"  - {v['name']}: {len(v['features'])} trazados")

    # 4. Mercados Públicos
    mercados_df = pd.read_csv('data/raw/mercados_publicos.csv')
    mercados_list = []
    for _, row in mercados_df.iterrows():
        if pd.isnull(row['latitud']) or pd.isnull(row['longitud']):
            continue
        try:
            locales = int(row['locales']) if pd.notnull(row['locales']) else 0
            sup = float(row['superficie_m2']) if pd.notnull(row['superficie_m2']) else 0
            
            if locales >= 500:
                cat_tamano = 'Macro (500+ locales)'
                radio = 16
            elif locales >= 250:
                cat_tamano = 'Grande (250-499 locales)'
                radio = 12
            elif locales >= 100:
                cat_tamano = 'Mediano (100-249 locales)'
                radio = 8
            else:
                cat_tamano = 'Barrial (<100 locales)'
                radio = 6

            mercados_list.append({
                'nombre': str(row['mercado']),
                'numero': str(row['numero']),
                'alcaldia': str(row['alcaldia_mercado']),
                'colonia': str(row['colonia_mercado']),
                'locales': locales,
                'superficie_m2': sup,
                'categoria': cat_tamano,
                'radio': radio,
                'anio': str(row['anio_inauguracion']) if pd.notnull(row['anio_inauguracion']) else 'N/D',
                'giro': str(row['giro']) if pd.notnull(row['giro']) else 'Mixto',
                'lat': float(row['latitud']),
                'lon': float(row['longitud'])
            })
        except Exception:
            continue

    # 5. Mercados Sobre Ruedas
    msr_df = pd.read_csv('data/raw/mercados_sobre_ruedas.csv')
    msr_list = []
    for _, row in msr_df.iterrows():
        if pd.isnull(row['Coor_GeogY']) or pd.isnull(row['Coor_GeogX']):
            continue
        try:
            oferentes = int(row['Num_Oferen']) if pd.notnull(row['Num_Oferen']) else 0
            msr_list.append({
                'ruta': str(row['Ruta']),
                'dia': str(row['Día_Oper']).strip(),
                'oferentes': oferentes,
                'direccion': str(row['Dirección']),
                'alcaldia': str(row['Alcaldía']),
                'colonia': str(row['Colonia']),
                'lat': float(row['Coor_GeogY']),
                'lon': float(row['Coor_GeogX']),
                'radio': 10 if oferentes > 150 else 7
            })
        except Exception:
            continue

    # 6. Tianguis
    tianguis_df = pd.read_csv('data/raw/tianguis.csv')
    tianguis_list = []
    for _, row in tianguis_df.iterrows():
        if pd.isnull(row['latitud']) or pd.isnull(row['longitud']):
            continue
        try:
            tianguis_list.append({
                'alcaldia': str(row['alcaldia']) if pd.notnull(row['alcaldia']) else '',
                'colonia': str(row['colonia']) if pd.notnull(row['colonia']) else '',
                'ubicacion': str(row['ubicacion']) if pd.notnull(row['ubicacion']) else '',
                'dia': str(row['dia']).strip().upper() if pd.notnull(row['dia']) else 'DESCONOCIDO',
                'horario': str(row['horario']) if pd.notnull(row['horario']) else '8:00 A 17:00',
                'lat': float(row['latitud']),
                'lon': float(row['longitud'])
            })
        except Exception:
            continue

    output_bundle = {
        'alcaldias': alcaldias_geojson,
        'zmvm': zmvm_geojson,
        'transport': transport_layers,
        'mercados': mercados_list,
        'msr': msr_list,
        'tianguis': tianguis_list
    }
    
    bundle_path = 'data/processed/map_bundle.json'
    with open(bundle_path, 'w', encoding='utf-8') as f:
        json.dump(output_bundle, f, ensure_ascii=False)
    
    print(f"Bundle generado con éxito: {bundle_path} ({os.path.getsize(bundle_path)} bytes)")

if __name__ == '__main__':
    run()
