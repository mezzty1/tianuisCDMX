import os
import sys
import json
import re
import unicodedata
import shapefile
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.build_compras_catalog import classify_space, build_search_vocabulary

def clean_name(s):
    s = s.lower().strip()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s

def run():
    print("Compilando bundle enriquecido con estaciones oficiales, iconografía e inventario secundario...")
    os.makedirs('data/processed', exist_ok=True)
    
    # 1. Cargar Alcaldías CDMX y ZMVM
    with open('data/raw/cartografia/alcaldias.geojson', 'r', encoding='utf-8') as f:
        alcaldias_geo = json.load(f)
    
    zmvm_geo = None
    if os.path.exists('data/raw/cartografia/zmvm_edomex_opt.geojson'):
        with open('data/raw/cartografia/zmvm_edomex_opt.geojson', 'r', encoding='utf-8') as f:
            zmvm_geo = json.load(f)

    # 2. Cargar GTFS Base
    routes_df = pd.read_csv('data/raw/transporte/gtfs/routes.txt')
    trips_df = pd.read_csv('data/raw/transporte/gtfs/trips.txt')
    shapes_df = pd.read_csv('data/raw/transporte/gtfs/shapes.txt')
    
    metro_colors = {
        '1': '#F04E98', '01': '#F04E98',
        '2': '#0057B8', '02': '#0057B8',
        '3': '#808200', '03': '#808200',
        '4': '#6EC4E8', '04': '#6EC4E8',
        '5': '#FCD116', '05': '#FCD116',
        '6': '#D62828', '06': '#D62828',
        '7': '#FF7F32', '07': '#FF7F32',
        '8': '#009A44', '08': '#009A44',
        '9': '#6C3B14', '09': '#6C3B14',
        'A': '#8F1A95', '0A': '#8F1A95',
        'B': '#007A3D', '0B': '#007A3D',
        '12': '#B59A57',
    }

    transport_layers = {
        'METRO': {'name': 'Metro (STC)', 'color': '#E53935', 'features': []},
        'MB': {'name': 'Metrobús', 'color': '#D81B60', 'features': []},
        'CBB': {'name': 'Cablebús', 'color': '#00A3E0', 'features': []},
        'TROLE': {'name': 'Trolebús (STE)', 'color': '#00897B', 'features': []},
        'TL': {'name': 'Tren Ligero (STE)', 'color': '#1E88E5', 'features': []},
        'RTP': {'name': 'RTP (Red Pasajeros)', 'color': '#2E7D32', 'features': []},
        'CC': {'name': 'Corredores Concesionados', 'color': '#8E24AA', 'features': []}
    }

    trip_route_map = trips_df[['trip_id', 'route_id', 'shape_id', 'trip_headsign']].drop_duplicates(subset=['shape_id'])
    merged_routes = trip_route_map.merge(routes_df, on='route_id', how='inner')
    shapes_grouped = shapes_df.sort_values(['shape_id', 'shape_pt_sequence']).groupby('shape_id')
    
    rtp_count = 0
    for shape_id, group in shapes_grouped:
        r_info = merged_routes[merged_routes['shape_id'] == shape_id]
        if r_info.empty:
            continue
        row = r_info.iloc[0]
        agency = row['agency_id']
        if agency not in transport_layers or agency == 'CC':
            continue
        
        if agency == 'RTP':
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

        # Tarifas e información de Red Primaria (Movilidad Integrada)
        tarifa_map = {
            'METRO': ('$5.00 MXN', 'Tarjeta Movilidad Integrada (MI)', 'Tren de rodadura neumática / férrea'),
            'MB': ('$6.00 MXN', 'Tarjeta Movilidad Integrada (MI)', 'Autobús articulado / biarticulado BRT'),
            'TROLE': ('$4.00 MXN (Elevado: $7.00)', 'Tarjeta Movilidad Integrada (MI)', 'Trolebús 100% eléctrico'),
            'CBB': ('$7.00 MXN', 'Tarjeta Movilidad Integrada (MI)', 'Teleférico urbano'),
            'TL': ('$3.00 MXN', 'Tarjeta Movilidad Integrada (MI)', 'Tren ligero superficial'),
            'RTP': ('$2.00 - $4.00 MXN', 'Tarjeta MI o Efectivo exacto', 'Autobús urbano de pasajeros')
        }
        tarifa_info, pago_info, unidad_info = tarifa_map.get(agency, ('$5.00 MXN', 'Tarjeta MI', 'Transporte Masivo'))

        transport_layers[agency]['features'].append({
            'type': 'Feature',
            'properties': {
                'agency': agency,
                'agency_name': transport_layers[agency]['name'],
                'red_tipo': 'PRIMARIA',
                'red_nombre': 'Red Primaria (Movilidad Integrada - MI)',
                'tarifa': tarifa_info,
                'forma_pago': pago_info,
                'tipo_unidad': unidad_info,
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
        })

    # 3. Incorporar Rutas Secundarias del Shapefile Concesionado Oficial (331 rutas)
    print("Cargando rutas secundarias concesionadas desde SHP...")
    sf_concesionado = shapefile.Reader('data/raw/transporte/concesionado_shp/concesionado_shp/concesionado_rutas.shp')
    cc_count = 0

    import math
    def calc_dist_km(pts):
        total = 0.0
        for i in range(len(pts) - 1):
            p1, p2 = pts[i], pts[i+1]
            lat1, lon1 = p1[1], p1[0]
            lat2, lon2 = p2[1], p2[0]
            phi1, phi2 = lat1 * math.pi / 180, lat2 * math.pi / 180
            dphi = (lat2 - lat1) * math.pi / 180
            dlam = (lon2 - lon1) * math.pi / 180
            a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            total += 6371.0 * c
        return round(total, 1)

    for shape_rec in sf_concesionado.shapeRecords():
        rec = shape_rec.record
        shp = shape_rec.shape
        if not shp.points:
            continue
        
        # Muestra representativa balanceada de 70 rutas secundarias concesionadas
        cc_count += 1
        if cc_count > 70:
            continue

        orig_dest = rec['ORIG_DEST'] or 'Ruta Concesionada'
        corredor = rec['CORREDOR'] or 'Zonal'
        empresa = rec['EMPRESA'] or 'Concesionario'
        nomencl = rec['NOMENCL'] or ''

        # Convertir puntos a coordenadas [lon, lat]
        pts = shp.points
        dist_km = calc_dist_km(pts)
        if len(pts) > 150:
            pts = pts[::2]
        coords = [[round(p[0], 5), round(p[1], 5)] for p in pts]

        # Esquema tarifario oficial SEMOVI para transporte concesionado
        if dist_km <= 5.0:
            tarifa_sec = f"$6.00 MXN (~{dist_km} km)"
            tramo_desc = "Tramo corto (hasta 5 km)"
        elif dist_km <= 12.0:
            tarifa_sec = f"$6.50 MXN (~{dist_km} km)"
            tramo_desc = "Tramo medio (5 a 12 km)"
        else:
            tarifa_sec = f"$7.50 MXN (~{dist_km} km)"
            tramo_desc = "Tramo largo (más de 12 km)"

        if 'corredor' in str(corredor).lower() or 'sausa' in str(empresa).lower() or 'coavensa' in str(empresa).lower():
            tarifa_sec = f"$8.00 MXN (~{dist_km} km)"
            tramo_desc = "Autobús de Corredor Concesionado"

        transport_layers['CC']['features'].append({
            'type': 'Feature',
            'properties': {
                'agency': 'CC',
                'agency_name': f'Ruta Concesionada · {corredor}',
                'red_tipo': 'SECUNDARIA',
                'red_nombre': 'Red Secundaria (Transporte Concesionado / Alimentadora)',
                'tarifa': tarifa_sec,
                'tramo_descripcion': tramo_desc,
                'distancia_km': dist_km,
                'forma_pago': 'Efectivo exacto al operador (monedas)',
                'tipo_unidad': 'Microbús colectivo / Vagoneta (combi)',
                'route_id': nomencl,
                'route_short': nomencl,
                'route_long': orig_dest,
                'headsign': f'Operado por: {empresa}',
                'color': '#8E24AA',
                'weight': 2.5,
                'opacity': 0.8
            },
            'geometry': {
                'type': 'LineString',
                'coordinates': coords
            }
        })
    print(f"Rutas secundarias añadidas al visor: {len(transport_layers['CC']['features'])} trazados")

    # 4. Procesar Estaciones del Metro con Iconografía oficial
    print("Cargando estaciones del Metro y mapeando iconografía...")
    with open('data/raw/transporte/metro_estaciones.geojson', 'r', encoding='utf-8') as f:
        metro_st_geo = json.load(f)

    with open('assets/css/ui-transport-mx.css') as f:
        css_text = f.read()
    icon_classes = set(re.findall(r'\.estacion-([a-z0-9\-]+):before', css_text))

    metro_stations_list = []
    for st in metro_st_geo['features']:
        props = st['properties']
        coords = st['geometry']['coordinates']
        nom = props.get('NOMBRE', 'Estación')
        linea = str(props.get('LINEA', '01'))
        
        c_nom = clean_name(nom)
        icon_class = 'estacion-metro'
        if c_nom in icon_classes:
            icon_class = f'estacion-{c_nom}'
        else:
            for ic in icon_classes:
                if ic in c_nom or c_nom in ic:
                    icon_class = f'estacion-{ic}'
                    break
        
        l_color = metro_colors.get(linea, '#E53935')
        if not l_color.startswith('#'):
            l_color = metro_colors.get(linea.zfill(2), '#E53935')

        metro_stations_list.append({
            'nombre': nom,
            'linea': linea,
            'color': l_color,
            'icon_class': icon_class,
            'tipo': props.get('TIPO', 'Paso'),
            'alcaldia': props.get('ALCALDIAS', 'CDMX'),
            'lon': coords[0],
            'lat': coords[1]
        })
    print(f"Estaciones de Metro listas con icono: {len(metro_stations_list)}")

    # 5. Procesar Estaciones de Metrobús
    print("Cargando estaciones de Metrobús...")
    with open('data/raw/transporte/metrobus_estaciones.geojson', 'r', encoding='utf-8') as f:
        mb_st_geo = json.load(f)
    
    mb_stations_list = []
    for st in mb_st_geo['features']:
        props = st['properties']
        coords = st['geometry']['coordinates']
        nom = props.get('NOMBRE', 'Estación Metrobús')
        linea = str(props.get('LINEA', '01'))
        mb_stations_list.append({
            'nombre': nom,
            'linea': f'Línea {linea}',
            'alcaldia': props.get('ALCALDIAS', 'CDMX'),
            'lon': coords[0],
            'lat': coords[1]
        })
    print(f"Estaciones de Metrobús listas: {len(mb_stations_list)}")

    # 6. Mercados Públicos
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
                radio = 15
            elif locales >= 250:
                cat_tamano = 'Grande (250-499 locales)'
                radio = 11
            elif locales >= 100:
                cat_tamano = 'Mediano (100-249 locales)'
                radio = 8
            else:
                cat_tamano = 'Barrial (<100 locales)'
                radio = 6

            nom_merc = str(row['mercado'])
            giro_merc = str(row['giro']) if pd.notnull(row['giro']) else 'Mixto'
            cls = classify_space('Mercado Público', giro_merc, nom_merc)

            mercados_list.append({
                'nombre': nom_merc,
                'numero': str(row['numero']),
                'alcaldia': str(row['alcaldia_mercado']),
                'colonia': str(row['colonia_mercado']),
                'locales': locales,
                'superficie_m2': sup,
                'categoria': cat_tamano,
                'radio': radio,
                'giro': giro_merc,
                'cats': cls['categorias'],
                'subgiros': cls['subgiros'],
                'canasta_basica': cls['canasta_basica'],
                'mercomuna': cls['mercomuna'],
                'tags': cls['popular_tags'],
                'lat': float(row['latitud']),
                'lon': float(row['longitud'])
            })
        except Exception:
            continue

    # 7. Mercados Sobre Ruedas (MSR enriquecido)
    msr_list = []
    if os.path.exists('data/processed/mercados_sobre_ruedas_limpio.json'):
        with open('data/processed/mercados_sobre_ruedas_limpio.json', 'r', encoding='utf-8') as f:
            msr_raw = json.load(f)
        for row in msr_raw:
            if not row.get('coordenadas_validas') or not row.get('lat') or not row.get('lng'):
                continue
            try:
                ruta_nom = row.get('ruta', row.get('nombre', 'MSR'))
                cls = classify_space('Mercado Sobre Ruedas', 'ABASTO POPULAR CANASTA BASICA', ruta_nom)
                msr_list.append({
                    'id': row.get('id', 'MSR-0000'),
                    'nombre': row.get('nombre', ruta_nom),
                    'ruta': ruta_nom,
                    'tipo_espacio': 'Mercado Sobre Ruedas',
                    'dia': str(row.get('dia', '')).strip().upper(),
                    'dias_operacion': str(row.get('dias_operacion', row.get('dia', ''))).strip().upper(),
                    'dias_operacion_lista': row.get('dias_operacion_lista', [str(row.get('dia', '')).strip().upper()]),
                    'oferentes': int(row.get('num_oferentes', 100)),
                    'direccion': str(row.get('direccion', '')),
                    'alcaldia': str(row.get('alcaldia', '')),
                    'colonia': str(row.get('colonia', '')),
                    'horario': str(row.get('horario', '08:00 A 18:00 HORAS')),
                    'hora_apertura': float(row.get('hora_apertura', 8.0)),
                    'hora_cierre': float(row.get('hora_cierre', 18.0)),
                    'giro': str(row.get('giro', 'ABASTO POPULAR Y CANASTA BÁSICA')),
                    'cats': cls['categorias'],
                    'subgiros': cls['subgiros'],
                    'canasta_basica': cls['canasta_basica'],
                    'mercomuna': cls['mercomuna'],
                    'tags': cls['popular_tags'],
                    'lat': float(row['lat']),
                    'lon': float(row['lng']),
                    'radio': 9
                })
            except Exception:
                continue
    print(f"Mercados Sobre Ruedas procesados: {len(msr_list)}")

    # 8. Tianguis (Enriquecido con padrón auditado Google Maps y oferentes)
    tianguis_list = []
    if os.path.exists('data/processed/tianguis_limpio.json'):
        with open('data/processed/tianguis_limpio.json', 'r', encoding='utf-8') as f:
            t_raw = json.load(f)
        df_audit = None
        if os.path.exists('data/processed/padron_tianguis_auditado_maps.csv'):
            df_audit = pd.read_csv('data/processed/padron_tianguis_auditado_maps.csv')

        for idx, row in enumerate(t_raw):
            if not row.get('coordenadas_validas') or not row.get('lat') or not row.get('lng'):
                continue
            try:
                col_tian = str(row.get('colonia', '')).strip()
                p_name = ''
                if df_audit is not None and idx < len(df_audit):
                    val = df_audit.iloc[idx].get('place_name')
                    if pd.notnull(val):
                        p_name = str(val).strip()

                nombre_oficial = str(row.get('nombre', 'TIANGUIS')).strip()
                if p_name and not p_name.lower().startswith('mercado público') and not p_name.lower().startswith('mercado'):
                    nombre_popular = p_name
                else:
                    nombre_popular = f"Tianguis {col_tian.title()}" if col_tian else "Tianguis Popular"

                cls = classify_space('Tianguis', 'ABASTO POPULAR MIXTO', col_tian + ' ' + nombre_popular)
                tianguis_list.append({
                    'id': str(row.get('id', f'TIANG-{idx+1:04d}')),
                    'nombre': nombre_oficial,
                    'nombre_popular': nombre_popular,
                    'tipo_espacio': 'Tianguis',
                    'alcaldia': str(row.get('alcaldia', '')),
                    'colonia': col_tian,
                    'ubicacion': str(row.get('direccion', '')),
                    'dia': str(row.get('dia', 'DESCONOCIDO')).strip().upper(),
                    'dias_operacion': str(row.get('dias_operacion', row.get('dia', ''))).strip().upper(),
                    'dias_operacion_lista': row.get('dias_operacion_lista', [str(row.get('dia', '')).strip().upper()]),
                    'horario': str(row.get('horario', '8:00 A 17:00 HORAS')),
                    'hora_apertura': float(row.get('hora_apertura', 8.0)),
                    'hora_cierre': float(row.get('hora_cierre', 17.0)),
                    'oferentes': int(row.get('num_oferentes', 120)),
                    'giro': str(row.get('giro', 'MIXTO / ABASTO POPULAR')),
                    'cats': cls['categorias'],
                    'subgiros': cls['subgiros'],
                    'canasta_basica': cls['canasta_basica'],
                    'mercomuna': cls['mercomuna'],
                    'tags': cls['popular_tags'],
                    'lat': float(row['lat']),
                    'lon': float(row['lng'])
                })
            except Exception:
                continue
    print(f"Tianguis procesados y enriquecidos: {len(tianguis_list)}")

    # 9. Concentraciones de Comerciantes (SEDECO)
    concentraciones_list = []
    if os.path.exists('data/processed/concentraciones_comerciantes_limpio.json'):
        with open('data/processed/concentraciones_comerciantes_limpio.json', 'r', encoding='utf-8') as f:
            conc_raw = json.load(f)
        for row in conc_raw:
            if not row.get('coordenadas_validas') or not row.get('lat') or not row.get('lng'):
                continue
            try:
                nom = str(row.get('nombre', 'CONCENTRACIÓN')).strip()
                col = str(row.get('colonia', '')).strip()
                alc = str(row.get('alcaldia', '')).strip()
                giro = str(row.get('giro', 'COMERCIO Y SERVICIOS EN VÍA PÚBLICA')).strip()
                cls = classify_space('Concentración', giro, nom + ' ' + col)
                concentraciones_list.append({
                    'id': str(row.get('id', 'CONC-0000')),
                    'nombre': nom,
                    'nombre_popular': nom.title(),
                    'tipo_espacio': 'Concentración',
                    'tipo_comercio': str(row.get('tipo_comercio', 'FIJO')),
                    'alcaldia': alc,
                    'colonia': col,
                    'ubicacion': str(row.get('direccion', '')),
                    'dias_operacion': str(row.get('dias_operacion', 'LUNES A DOMINGO')),
                    'dias_operacion_lista': row.get('dias_operacion_lista', ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']),
                    'horario': str(row.get('horario', '08:00 A 18:00 HORAS')),
                    'hora_apertura': float(row.get('hora_apertura', 8.0)),
                    'hora_cierre': float(row.get('hora_cierre', 18.0)),
                    'oferentes': int(row.get('numero_oficial', 50)) if row.get('numero_oficial') else 50,
                    'giro': giro,
                    'cats': cls['categorias'],
                    'subgiros': cls['subgiros'],
                    'canasta_basica': cls['canasta_basica'],
                    'mercomuna': cls['mercomuna'],
                    'tags': cls['popular_tags'],
                    'lat': float(row['lat']),
                    'lon': float(row['lng'])
                })
            except Exception:
                continue
    print(f"Concentraciones georreferenciadas procesadas: {len(concentraciones_list)}")

    # 10. Estadísticas de Cierres Viales y Afectaciones por Día
    compact_cierres = {'resumen_semanal': {}, 'dias': {}}
    if os.path.exists('data/processed/cierres_viales_por_dia.json'):
        with open('data/processed/cierres_viales_por_dia.json', 'r', encoding='utf-8') as f:
            cv_raw = json.load(f)
            compact_cierres['resumen_semanal'] = cv_raw.get('resumen_semanal', {})
            for d, d_info in cv_raw.get('dias', {}).items():
                compact_cierres['dias'][d] = {
                    'total_tianguis': d_info.get('total_tianguis', 0),
                    'tianguis_activos': d_info.get('tianguis_activos', 0),
                    'km_lineales_ocupados': d_info.get('km_lineales_ocupados', 0.0),
                    'superficie_m2_ocupada': d_info.get('superficie_m2_ocupada', 0.0),
                    'oferentes_totales': d_info.get('oferentes_totales', 0),
                    'distribucion_afectacion': d_info.get('distribucion_afectacion', {}),
                    'top_corredores': d_info.get('top_corredores_dia', [])[:10],
                    'alcaldias': d_info.get('alcaldias', {})
                }
    print("Estadísticas de cierres viales compactadas para frontend.")

    # Cargar metadatos de categorías y subgiros para el frontend
    with open('data/catalog/giros_catalogo.json', 'r', encoding='utf-8') as f:
        catalog_raw = json.load(f)

    vocab_compras = build_search_vocabulary()

    # Guardar en JSON y JS bundle
    output_bundle = {
        'alcaldias': alcaldias_geo,
        'zmvm': zmvm_geo,
        'transport': transport_layers,
        'metro_stations': metro_stations_list,
        'metrobus_stations': mb_stations_list,
        'mercados': mercados_list,
        'msr': msr_list,
        'tianguis': tianguis_list,
        'concentraciones': concentraciones_list,
        'cierres_viales': compact_cierres,
        'catalog_categorias': catalog_raw['categorias'],
        'catalog_subgiros': [{
            'id': sg['id'],
            'categoria_id': sg['categoria_id'],
            'nombre': sg['nombre'],
            'canasta_basica': sg.get('canasta_basica', False),
            'mercomuna': sg.get('mercomuna', False)
        } for sg in catalog_raw['subgiros']],
        'vocabulario_compras': vocab_compras
    }
    
    with open('data/processed/map_bundle.json', 'w', encoding='utf-8') as f:
        json.dump(output_bundle, f, ensure_ascii=False)

    with open('data/processed/map_bundle.js', 'w', encoding='utf-8') as f:
        f.write("window.MAP_DATA = ")
        json.dump(output_bundle, f, ensure_ascii=False)
        f.write(";\n")

    print(f"Bundle enriquecido generado exitosamente: {len(mercados_list)} mercados, {len(tianguis_list)} tianguis, {len(msr_list)} MSR, {len(vocab_compras)} términos de compras.")

if __name__ == '__main__':
    run()
