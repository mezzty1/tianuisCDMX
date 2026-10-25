#!/usr/bin/env python3
"""
Route Calculator Multimodal CDMX (Chilangatón 2026)
===================================================
Motor de ruteo multimodal de código abierto para la Ciudad de México y ZMVM.
Calcula rutas óptimas punto A a punto B integrando:
- Caminata peatonal (primera y última milla)
- Red de Transporte Masivo: Metro CDMX, Metrobús, Cablebús, Tren Ligero, Tren Suburbano
- Red de Superficie: Trolebús (incluyendo Trolebús Elevado), RTP y Corredores Concesionados
- Destinos de Comercio Popular: 329 Mercados Públicos y 1,367 Tianguis y Mercados sobre Ruedas

Implementa:
- Grafo de estados consciente de línea (Line-Aware State Graph)
- Penalización realista de transbordos y tiempos de espera
- Integración de tarifas oficiales del Sistema de Movilidad Integrada (MI)
- Cálculo de huella de carbono y emisiones evitadas de CO2
"""

import os
import sys
import math
import time
import json
import pickle
import argparse
import re
import unicodedata
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

import pandas as pd
import numpy as np
import networkx as nx
from scipy.spatial import cKDTree

# Constantes de Ruteo
EARTH_RADIUS_METERS = 6371000.0
DEFAULT_WALK_SPEED_MS = 1.25  # 4.5 km/h
DEFAULT_MAX_WALK_METERS = 1200.0  # 1.2 km radio máximo de caminata para abordar
TRANSFER_BASE_PENALTY_MIN = 3.0   # Espera promedio de tren/autobús en transbordo
CAR_CO2_GRAMS_PER_KM = 143.0      # Emisión promedio auto particular CDMX
TRANSIT_CO2_GRAMS_PER_KM = 28.0   # Emisión promedio por pasajero-km en red eléctrica/híbrida CDMX

# Tarifas Oficiales Sistema Movilidad Integrada (MI) CDMX
FARES_MXN = {
    'METRO': 5.00,        # STC Metro (tarifa plana, transbordos libres internos)
    'MB': 6.00,           # Metrobús (tarifa plana, transbordo libre dentro de 2h)
    'TROLE': 4.00,        # Trolebús habitual
    'TROLE_ELEVADO': 7.00,# Trolebús Línea 10 (Elevado)
    'TL': 3.00,           # Tren Ligero (STE)
    'CBB': 7.00,          # Cablebús (STE)
    'RTP': 2.00,          # RTP Servicio Ordinario/Atenea ($4.00 Expreso, $5.00 Ecobús)
    'CC': 8.00,           # Corredores Concesionados (tarifa base $8.00 - $9.00)
    'SUB': 10.50,         # Tren Suburbano viaje corto ($24.50 viaje largo)
    'PUMABUS': 0.00,      # Gratuito UNAM
    'INTERURBANO': 15.00, # Tren El Insurgente (tramo base)
}

# Colores Oficiales de Líneas CDMX
METRO_COLORS = {
    '1': '#F04E98', '01': '#F04E98',
    '2': '#0057B8', '02': '#0057B8',
    '3': '#808200', '03': '#808200',
    '4': '#6EC4E8', '04': '#6EC4E8',
    '5': '#FCD116', '05': '#FCD116',
    '6': '#E53935', '06': '#E53935',
    '7': '#E67300', '07': '#E67300',
    '8': '#00824B', '08': '#00824B',
    '9': '#592C1D', '09': '#592C1D',
    'A': '#8B2464', 'LA': '#8B2464',
    'B': '#B5BD00', 'LB': '#B5BD00',
    '12': '#C19D53', 'L12': '#C19D53',
}

AGENCY_COLORS = {
    'METRO': '#E53935',
    'MB': '#CC0000',
    'TROLE': '#004899',
    'TL': '#007AC9',
    'CBB': '#009B77',
    'RTP': '#008B45',
    'CC': '#9B26B6',
    'SUB': '#E65100',
    'PUMABUS': '#002B49',
    'INTERURBANO': '#83332E',
    'SEMOVI': '#2E7D32',
}

# Lugares emblemáticos de referencia rápida
LANDMARKS = {
    'zocalo': (19.432608, -99.133208, 'Zócalo / Plaza de la Constitución'),
    'bellas artes': (19.4352, -99.1412, 'Palacio de Bellas Artes'),
    'pino suarez': (19.4258, -99.1330, 'Metro Pino Suárez'),
    'chabacano': (19.4084, -99.1358, 'Metro Chabacano'),
    'pantitlan': (19.4165, -99.0722, 'Metro Pantitlán'),
    'indios verdes': (19.4953, -99.1194, 'Indios Verdes'),
    'taxquena': (19.3458, -99.1408, 'Tasqueña'),
    'tasquena': (19.3458, -99.1408, 'Tasqueña'),
    'observatorio': (19.3982, -99.2004, 'Metro Observatorio'),
    'cu': (19.3317, -99.1867, 'Ciudad Universitaria (UNAM)'),
    'coyoacan': (19.3498, -99.1622, 'Centro de Coyoacán'),
    'polanco': (19.4337, -99.1913, 'Polanco'),
    'santa fe': (19.3598, -99.2600, 'Santa Fe'),
    'central de abasto': (19.3712, -99.0913, 'Central de Abasto (Iztapalapa)'),
    'mercado jamaica': (19.408584, -99.122788, 'Mercado Jamaica'),
    'mercado merced': (19.4262, -99.1250, 'Mercado de la Merced'),
    'mercado san juan': (19.4299, -99.1425, 'Mercado de San Juan'),
    'mercado sonora': (19.4231, -99.1267, 'Mercado de Sonora'),
    'tianguis meyehualco': (19.345737, -99.042582, 'Tianguis Santa Cruz Meyehualco (Iztapalapa)'),
    'tianguis salado': (19.369935, -99.049703, 'Tianguis El Salado / Renovación (Iztapalapa)'),
    'tianguis san felipe': (19.4930, -99.0710, 'Tianguis San Felipe de Jesús (GAM)')
}


def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula distancia ortodrómica en metros entre dos puntos geográficos."""
    r_lat1, r_lon1 = math.radians(lat1), math.radians(lon1)
    r_lat2, r_lon2 = math.radians(lat2), math.radians(lon2)
    dlat = r_lat2 - r_lat1
    dlon = r_lon2 - r_lon1
    a = math.sin(dlat / 2.0)**2 + math.cos(r_lat1) * math.cos(r_lat2) * math.sin(dlon / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS_METERS * c


def strip_accents(text: Any) -> str:
    """Elimina acentos y diacríticos de un texto."""
    s = str(text or '')
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower().strip()


def clean_name(text: Any) -> str:
    """Normaliza nombres de estaciones eliminando prefijos de modo y puntuación."""
    s = strip_accents(text)
    s = re.sub(r'^(metro|estación|estacion|parada|terminal)\s+', '', s)
    s = re.sub(r'[^a-z0-9]', '', s)
    return s


class CDMXMultimodalRouter:
    """Motor de cálculo de rutas multimodal para CDMX."""

    def __init__(self, gtfs_dir: str = 'data/raw/transporte/gtfs', 
                 cache_path: str = 'data/processed/routing_graph.pickle',
                 rebuild_cache: bool = False):
        self.gtfs_dir = gtfs_dir
        self.cache_path = cache_path
        self.graph = None
        self.stops_df = None
        self.routes_df = None
        self.agencies_df = None
        self.stop_to_nodes = {}
        self.tree = None
        self.stop_ids = []
        self.xyz = None
        self.mercados = []
        self.tianguis = []

        self._load_poi_data()

        if not rebuild_cache and os.path.exists(self.cache_path):
            self._load_from_cache()
        else:
            self._build_and_cache_graph()

    def _load_poi_data(self):
        """Carga catálogo de mercados públicos y tianguis para búsqueda semántica."""
        m_path = 'data/processed/mercados_publicos_limpio.json'
        t_path = 'data/processed/tianguis_limpio.json'
        if os.path.exists(m_path):
            try:
                with open(m_path, 'r', encoding='utf-8') as f:
                    self.mercados = json.load(f)
            except Exception:
                self.mercados = []
        if os.path.exists(t_path):
            try:
                with open(t_path, 'r', encoding='utf-8') as f:
                    self.tianguis = json.load(f)
            except Exception:
                self.tianguis = []

    def _load_from_cache(self):
        """Carga el grafo precalculado desde archivo pickle."""
        try:
            t0 = time.time()
            with open(self.cache_path, 'rb') as f:
                data = pickle.load(f)
            self.graph = data['graph']
            self.stops_df = data['stops_df']
            self.routes_df = data['routes_df']
            self.agencies_df = data['agencies_df']
            self.stop_to_nodes = data['stop_to_nodes']
            self.tree = data['tree']
            self.stop_ids = data['stop_ids']
            self.xyz = data['xyz']
            # print(f"[Router] Grafo cargado desde caché en {time.time() - t0:.2f}s ({self.graph.number_of_nodes()} nodos, {self.graph.number_of_edges()} aristas)")
        except Exception as e:
            # print(f"[Router] Fallo al cargar caché ({e}). Reconstruyendo grafo...")
            self._build_and_cache_graph()

    def _build_and_cache_graph(self):
        """Construye el grafo multimodal de transporte a partir de GTFS y genera la caché."""
        t0 = time.time()
        # print("[Router] Procesando archivos GTFS de CDMX...")

        stops_path = os.path.join(self.gtfs_dir, 'stops.txt')
        routes_path = os.path.join(self.gtfs_dir, 'routes.txt')
        trips_path = os.path.join(self.gtfs_dir, 'trips.txt')
        stop_times_path = os.path.join(self.gtfs_dir, 'stop_times.txt')
        agency_path = os.path.join(self.gtfs_dir, 'agency.txt')

        self.stops_df = pd.read_csv(stops_path).set_index('stop_id')
        self.routes_df = pd.read_csv(routes_path).set_index('route_id')
        trips_df = pd.read_csv(trips_path).set_index('trip_id')
        st_df = pd.read_csv(stop_times_path)
        self.agencies_df = pd.read_csv(agency_path).set_index('agency_id')

        # Asociar ruta a cada trip
        st_df['route_id'] = st_df['trip_id'].map(trips_df['route_id'])

        def parse_time_sec(s):
            if pd.isna(s):
                return 0
            p = str(s).strip().split(':')
            return int(p[0]) * 3600 + int(p[1]) * 60 + int(p[2])

        st_df['dep_s'] = st_df['departure_time'].apply(parse_time_sec)
        st_df['arr_s'] = st_df['arrival_time'].apply(parse_time_sec)
        st_df = st_df.sort_values(['trip_id', 'stop_sequence'])
        st_df['next_stop_id'] = st_df.groupby('trip_id')['stop_id'].shift(-1)
        st_df['next_arr_s'] = st_df.groupby('trip_id')['arr_s'].shift(-1)
        st_df['hop_sec'] = st_df['next_arr_s'] - st_df['dep_s']

        valid_hops = st_df.dropna(subset=['next_stop_id']).copy()
        # Asignar tiempo de viaje promedio de 90 segundos si falta información
        valid_hops.loc[valid_hops['hop_sec'] <= 0, 'hop_sec'] = 90.0

        # Consolidar tiempos medianos entre paradas consecutivas por ruta
        transit_edges = valid_hops.groupby(['stop_id', 'next_stop_id', 'route_id'])['hop_sec'].median().reset_index()

        self.graph = nx.DiGraph()
        self.stop_to_nodes = {}

        # 1. Agregar aristas en vehículo (tránsito regular)
        for _, row in transit_edges.iterrows():
            u_stop, v_stop, r_id, sec = row['stop_id'], row['next_stop_id'], row['route_id'], row['hop_sec']
            u_node = f"{u_stop}::{r_id}"
            v_node = f"{v_stop}::{r_id}"

            r_info = self.routes_df.loc[r_id] if r_id in self.routes_df.index else None
            agency = r_info['agency_id'] if r_info is not None else 'UNKNOWN'
            r_name = str(r_info['route_short_name']) if r_info is not None else ''
            r_long = str(r_info['route_long_name']) if r_info is not None else ''

            # Distancia aproximada entre paradas
            if u_stop in self.stops_df.index and v_stop in self.stops_df.index:
                u_lat, u_lon = self.stops_df.loc[u_stop, ['stop_lat', 'stop_lon']]
                v_lat, v_lon = self.stops_df.loc[v_stop, ['stop_lat', 'stop_lon']]
                hop_dist = haversine_distance_meters(u_lat, u_lon, v_lat, v_lon)
            else:
                hop_dist = (sec / 3600.0) * 25000.0  # estimación a 25 km/h

            self.graph.add_edge(
                u_node, v_node,
                weight=sec / 60.0,
                mode='transit',
                route_id=r_id,
                agency=agency,
                route_name=r_name,
                route_long_name=r_long,
                dist_m=hop_dist,
                stop_from=u_stop,
                stop_to=v_stop
            )

            self.stop_to_nodes.setdefault(u_stop, []).append((u_node, r_id, agency))
            self.stop_to_nodes.setdefault(v_stop, []).append((v_node, r_id, agency))

        # Deduplicar stop_to_nodes
        for s in self.stop_to_nodes:
            self.stop_to_nodes[s] = list(set(self.stop_to_nodes[s]))

        # 2. Agregar aristas de transbordo entre líneas en la misma estación
        for s_id, node_list in self.stop_to_nodes.items():
            if len(node_list) > 1:
                for n1, r1, a1 in node_list:
                    for n2, r2, a2 in node_list:
                        if r1 != r2:
                            # Si es cambio dentro del mismo sistema (ej. Metro a Metro) penalidad 2.5 min
                            # Si es cambio intermodal (ej. Metro a RTP en calle) 4.0 min
                            penalty = 2.5 if a1 == a2 else 4.0
                            self.graph.add_edge(
                                n1, n2,
                                weight=penalty,
                                mode='transfer',
                                dist_m=30.0,
                                stop_from=s_id,
                                stop_to=s_id,
                                agency_from=a1,
                                agency_to=a2
                            )

        # 3. Índice espacial para transbordos a pie entre estaciones cercanas (ej. pasillos del Metro y transbordos Metro-MB)
        active_stops = self.stops_df.loc[list(self.stop_to_nodes.keys())].dropna(subset=['stop_lat', 'stop_lon']).copy()
        lat_rad = np.radians(active_stops['stop_lat'].values)
        lon_rad = np.radians(active_stops['stop_lon'].values)
        x = EARTH_RADIUS_METERS * np.cos(lat_rad) * np.cos(lon_rad)
        y = EARTH_RADIUS_METERS * np.cos(lat_rad) * np.sin(lon_rad)
        z = EARTH_RADIUS_METERS * np.sin(lat_rad)
        self.xyz = np.column_stack([x, y, z])
        self.tree = cKDTree(self.xyz)
        self.stop_ids = active_stops.index.tolist()

        # Conectar estaciones a menos de 180 metros (pasillos de correspondencia)
        pairs = self.tree.query_pairs(r=180.0)
        for i, j in pairs:
            s1, s2 = self.stop_ids[i], self.stop_ids[j]
            if s1 != s2:
                d = np.linalg.norm(self.xyz[i] - self.xyz[j])
                walk_min = (d / DEFAULT_WALK_SPEED_MS) / 60.0 + TRANSFER_BASE_PENALTY_MIN
                for n1, r1, a1 in self.stop_to_nodes[s1]:
                    for n2, r2, a2 in self.stop_to_nodes[s2]:
                        self.graph.add_edge(n1, n2, weight=walk_min, mode='transfer', dist_m=d, stop_from=s1, stop_to=s2, agency_from=a1, agency_to=a2)
                        self.graph.add_edge(n2, n1, weight=walk_min, mode='transfer', dist_m=d, stop_from=s2, stop_to=s1, agency_from=a2, agency_to=a1)

        # 4. Conectar correspondencias oficiales del Metro que comparten nombre base aunque su distancia sea hasta 350m
        metro_stops = active_stops[active_stops.index.str.contains(r'^B_0200', regex=True)].copy()
        metro_stops['cname'] = metro_stops['stop_name'].apply(clean_name)
        grouped_metro = metro_stops.groupby('cname')
        for cname, grp in grouped_metro:
            if len(grp) > 1:
                st_list = grp.index.tolist()
                for i1 in range(len(st_list)):
                    for i2 in range(i1 + 1, len(st_list)):
                        ms1, ms2 = st_list[i1], st_list[i2]
                        if ms1 in self.stop_to_nodes and ms2 in self.stop_to_nodes:
                            lat1, lon1 = active_stops.loc[ms1, ['stop_lat', 'stop_lon']]
                            lat2, lon2 = active_stops.loc[ms2, ['stop_lat', 'stop_lon']]
                            d = haversine_distance_meters(lat1, lon1, lat2, lon2)
                            if d <= 350.0:
                                t_walk = (d / DEFAULT_WALK_SPEED_MS) / 60.0 + 1.5
                                for n1, r1, a1 in self.stop_to_nodes[ms1]:
                                    for n2, r2, a2 in self.stop_to_nodes[ms2]:
                                        self.graph.add_edge(n1, n2, weight=t_walk, mode='transfer', dist_m=d, stop_from=ms1, stop_to=ms2, agency_from=a1, agency_to=a2)
                                        self.graph.add_edge(n2, n1, weight=t_walk, mode='transfer', dist_m=d, stop_from=ms2, stop_to=ms1, agency_from=a2, agency_to=a1)

        # Guardar en caché
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, 'wb') as f:
            pickle.dump({
                'graph': self.graph,
                'stops_df': self.stops_df,
                'routes_df': self.routes_df,
                'agencies_df': self.agencies_df,
                'stop_to_nodes': self.stop_to_nodes,
                'tree': self.tree,
                'stop_ids': self.stop_ids,
                'xyz': self.xyz
            }, f)
        # print(f"[Router] Grafo construido y guardado en {time.time() - t0:.2f}s ({self.graph.number_of_nodes()} nodos, {self.graph.number_of_edges()} aristas)")

    def _get_xyz(self, lat: float, lon: float) -> np.ndarray:
        la, lo = math.radians(lat), math.radians(lon)
        return np.array([
            EARTH_RADIUS_METERS * math.cos(la) * math.cos(lo),
            EARTH_RADIUS_METERS * math.cos(la) * math.sin(lo),
            EARTH_RADIUS_METERS * math.sin(la)
        ])

    def find_poi(self, query: str) -> Optional[Tuple[float, float, str]]:
        """Busca un punto de interés por nombre en landmarks, mercados y tianguis."""
        q = strip_accents(query)
        if q in LANDMARKS:
            return LANDMARKS[q]
        for k, v in LANDMARKS.items():
            k_clean = strip_accents(k)
            if q in k_clean or k_clean in q:
                return v

        # Mercados públicos
        for m in self.mercados:
            m_nom = strip_accents(m.get('nombre', ''))
            if q in m_nom:
                lat = float(m['lat'])
                lng = float(m['lng'])
                return (lat, lng, f"{m.get('nombre')} ({m.get('alcaldia', 'CDMX')})")

        # Tianguis
        for t in self.tianguis:
            t_nom = strip_accents(t.get('nombre', ''))
            if q in t_nom and t.get('lat') and t.get('lng'):
                lat = float(t['lat'])
                lng = float(t['lng'])
                return (lat, lng, f"{t.get('nombre')} ({t.get('alcaldia', 'CDMX')})")

        return None

    def calculate_route(self, orig_lat: float, orig_lon: float,
                        dest_lat: float, dest_lon: float,
                        orig_label: str = "Origen",
                        dest_label: str = "Destino",
                        max_walk_meters: float = DEFAULT_MAX_WALK_METERS,
                        walk_speed_ms: float = DEFAULT_WALK_SPEED_MS) -> Dict[str, Any]:
        """Calcula la ruta multimodal recomendada entre dos coordenadas."""
        t_start = time.time()

        direct_dist = haversine_distance_meters(orig_lat, orig_lon, dest_lat, dest_lon)
        orig_xyz = self._get_xyz(orig_lat, orig_lon)
        dest_xyz = self._get_xyz(dest_lat, dest_lon)

        # Si están a menos de 600m o el usuario está extremadamente cerca, ruta 100% peatonal
        if direct_dist <= 600.0:
            walk_min = (direct_dist / walk_speed_ms) / 60.0
            return {
                'status': 'OK',
                'summary': {
                    'origin': {'name': orig_label, 'lat': orig_lat, 'lon': orig_lon},
                    'destination': {'name': dest_label, 'lat': dest_lat, 'lon': dest_lon},
                    'total_duration_minutes': round(walk_min, 1),
                    'total_walk_meters': round(direct_dist),
                    'total_walk_minutes': round(walk_min, 1),
                    'total_transit_minutes': 0.0,
                    'num_transfers': 0,
                    'total_cost_mxn': 0.0,
                    'co2_saved_kg': round((direct_dist / 1000.0) * CAR_CO2_GRAMS_PER_KM / 1000.0, 3),
                    'mode': 'WALK_ONLY'
                },
                'legs': [{
                    'leg_number': 1,
                    'type': 'walk',
                    'instruction': f"Caminar directamente hacia {dest_label}",
                    'from': orig_label,
                    'to': dest_label,
                    'distance_m': round(direct_dist),
                    'duration_min': round(walk_min, 1),
                    'cost_mxn': 0.0
                }],
                'fare_breakdown': []
            }

        # Conectar origen y destino temporalmente al grafo
        orig_dists, orig_idxs = self.tree.query(orig_xyz, k=25, distance_upper_bound=max_walk_meters)
        dest_dists, dest_idxs = self.tree.query(dest_xyz, k=25, distance_upper_bound=max_walk_meters)

        orig_edges_to_remove = []
        dest_edges_to_remove = []

        self.graph.add_node('ORIGIN')
        self.graph.add_node('DEST')

        # Conexiones de primera milla (Origen -> Estaciones abordables)
        has_orig_conn = False
        for d, idx in zip(orig_dists, orig_idxs):
            if d < max_walk_meters and idx < len(self.stop_ids):
                s_id = self.stop_ids[idx]
                walk_min = (d / walk_speed_ms) / 60.0 + 3.0  # Caminata + tiempo promedio de llegada del tren/camión
                for n, _, agency in self.stop_to_nodes.get(s_id, []):
                    self.graph.add_edge('ORIGIN', n, weight=walk_min, mode='access_walk', dist_m=d, stop_to=s_id, agency=agency)
                    orig_edges_to_remove.append(('ORIGIN', n))
                    has_orig_conn = True

        # Conexiones de última milla (Estaciones finales -> Destino)
        has_dest_conn = False
        for d, idx in zip(dest_dists, dest_idxs):
            if d < max_walk_meters and idx < len(self.stop_ids):
                s_id = self.stop_ids[idx]
                walk_min = (d / walk_speed_ms) / 60.0
                for n, _, agency in self.stop_to_nodes.get(s_id, []):
                    self.graph.add_edge(n, 'DEST', weight=walk_min, mode='egress_walk', dist_m=d, stop_from=s_id, agency=agency)
                    dest_edges_to_remove.append((n, 'DEST'))
                    has_dest_conn = True

        # Conexión directa a pie como fallback competitivo si distancia es caminable (< 2.5 km)
        if direct_dist <= 2500.0:
            direct_walk_min = (direct_dist / walk_speed_ms) / 60.0
            self.graph.add_edge('ORIGIN', 'DEST', weight=direct_walk_min, mode='direct_walk', dist_m=direct_dist)
            orig_edges_to_remove.append(('ORIGIN', 'DEST'))

        # Si no hubo estaciones cercanas en radio estándar, expandir búsqueda
        if not (has_orig_conn and has_dest_conn):
            # Limpiar nodos antes de retornar o reportar
            for u, v in orig_edges_to_remove + dest_edges_to_remove:
                if self.graph.has_edge(u, v):
                    self.graph.remove_edge(u, v)
            if self.graph.has_node('ORIGIN'): self.graph.remove_node('ORIGIN')
            if self.graph.has_node('DEST'): self.graph.remove_node('DEST')
            return {
                'status': 'NO_TRANSIT_STOPS_NEARBY',
                'message': f"No se encontraron estaciones en un radio de {max_walk_meters}m de origen o destino.",
                'direct_distance_m': round(direct_dist)
            }

        try:
            raw_path = nx.shortest_path(self.graph, 'ORIGIN', 'DEST', weight='weight')
            raw_time = nx.shortest_path_length(self.graph, 'ORIGIN', 'DEST', weight='weight')
        except nx.NetworkXNoPath:
            # Limpiar
            for u, v in orig_edges_to_remove + dest_edges_to_remove:
                if self.graph.has_edge(u, v): self.graph.remove_edge(u, v)
            if self.graph.has_node('ORIGIN'): self.graph.remove_node('ORIGIN')
            if self.graph.has_node('DEST'): self.graph.remove_node('DEST')
            return {
                'status': 'NO_PATH',
                'message': "No fue posible encontrar una combinación de transporte viable.",
                'direct_distance_m': round(direct_dist)
            }

        # Extraer detalles de cada paso
        step_edges = []
        for i in range(len(raw_path) - 1):
            u, v = raw_path[i], raw_path[i+1]
            e = self.graph[u][v].copy()
            e['u'] = u
            e['v'] = v
            step_edges.append(e)

        # Limpiar nodos temporales del grafo
        for u, v in orig_edges_to_remove + dest_edges_to_remove:
            if self.graph.has_edge(u, v):
                self.graph.remove_edge(u, v)
        if self.graph.has_node('ORIGIN'): self.graph.remove_node('ORIGIN')
        if self.graph.has_node('DEST'): self.graph.remove_node('DEST')

        # Procesar y consolidar tramos (Legs) para el usuario
        consolidated_legs = self._consolidate_legs(step_edges, orig_label, dest_label)

        # Calcular tarifas y huella de carbono
        fare_summary = self._calculate_fares(consolidated_legs)
        co2_summary = self._calculate_emissions(consolidated_legs, direct_dist)

        total_walk_m = sum(l['distance_m'] for l in consolidated_legs if l['type'] in ('walk', 'transfer'))
        total_walk_time = sum(l['duration_min'] for l in consolidated_legs if l['type'] in ('walk', 'transfer'))
        total_transit_time = sum(l['duration_min'] for l in consolidated_legs if l['type'] == 'transit')
        num_transfers = sum(1 for l in consolidated_legs if l['type'] == 'transfer')

        return {
            'status': 'OK',
            'summary': {
                'origin': {'name': orig_label, 'lat': orig_lat, 'lon': orig_lon},
                'destination': {'name': dest_label, 'lat': dest_lat, 'lon': dest_lon},
                'total_duration_minutes': round(raw_time, 1),
                'total_walk_meters': round(total_walk_m),
                'total_walk_minutes': round(total_walk_time, 1),
                'total_transit_minutes': round(total_transit_time, 1),
                'num_transfers': num_transfers,
                'total_cost_mxn': fare_summary['total_cost_mxn'],
                'co2_saved_kg': co2_summary['co2_saved_kg'],
                'compute_time_sec': round(time.time() - t_start, 4)
            },
            'legs': consolidated_legs,
            'fare_breakdown': fare_summary['breakdown']
        }

    def _consolidate_legs(self, step_edges: List[Dict[str, Any]], orig_label: str, dest_label: str) -> List[Dict[str, Any]]:
        """Agrupa secuencias de paradas del mismo vehículo en tramos coherentes."""
        legs = []
        leg_num = 1
        i = 0
        n = len(step_edges)

        while i < n:
            e = step_edges[i]
            mode = e.get('mode')

            if mode == 'direct_walk':
                dist = e.get('dist_m', 0)
                dur = e.get('weight', 0)
                legs.append({
                    'leg_number': leg_num,
                    'type': 'walk',
                    'instruction': f"Caminar directamente hacia {dest_label}",
                    'from': orig_label,
                    'to': dest_label,
                    'distance_m': round(dist),
                    'duration_min': round(dur, 1),
                    'cost_mxn': 0.0
                })
                leg_num += 1
                i += 1

            elif mode == 'access_walk':
                dist = e.get('dist_m', 0)
                dur = e.get('weight', 0)
                to_stop = e.get('stop_to', '')
                to_stop_name = self.stops_df.loc[to_stop, 'stop_name'] if to_stop in self.stops_df.index else to_stop
                agency = e.get('agency', 'transporte')
                legs.append({
                    'leg_number': leg_num,
                    'type': 'walk',
                    'subtype': 'first_mile',
                    'instruction': f"Caminar hacia la estación {to_stop_name}",
                    'from': orig_label,
                    'to': to_stop_name,
                    'to_stop_id': to_stop,
                    'distance_m': round(dist),
                    'duration_min': round(dur, 1),
                    'cost_mxn': 0.0
                })
                leg_num += 1
                i += 1

            elif mode == 'egress_walk':
                dist = e.get('dist_m', 0)
                dur = e.get('weight', 0)
                from_stop = e.get('stop_from', '')
                from_stop_name = self.stops_df.loc[from_stop, 'stop_name'] if from_stop in self.stops_df.index else from_stop
                legs.append({
                    'leg_number': leg_num,
                    'type': 'walk',
                    'subtype': 'last_mile',
                    'instruction': f"Caminar desde {from_stop_name} hacia {dest_label}",
                    'from': from_stop_name,
                    'to': dest_label,
                    'distance_m': round(dist),
                    'duration_min': round(dur, 1),
                    'cost_mxn': 0.0
                })
                leg_num += 1
                i += 1

            elif mode == 'transfer':
                dist = e.get('dist_m', 0)
                dur = e.get('weight', 0)
                s_from = e.get('stop_from', '')
                s_to = e.get('stop_to', '')
                nom_from = self.stops_df.loc[s_from, 'stop_name'] if s_from in self.stops_df.index else s_from
                nom_to = self.stops_df.loc[s_to, 'stop_name'] if s_to in self.stops_df.index else s_to
                a_from = e.get('agency_from', '')
                a_to = e.get('agency_to', '')

                instr = f"Transbordo a pie en {nom_from}" if nom_from == nom_to else f"Transbordo a pie de {nom_from} a {nom_to}"
                legs.append({
                    'leg_number': leg_num,
                    'type': 'transfer',
                    'instruction': instr,
                    'from': nom_from,
                    'to': nom_to,
                    'distance_m': round(dist),
                    'duration_min': round(dur, 1),
                    'agency_from': a_from,
                    'agency_to': a_to,
                    'cost_mxn': 0.0
                })
                leg_num += 1
                i += 1

            elif mode == 'transit':
                # Agrupar todos los pasos transit consecutivos en la misma ruta
                curr_route = e.get('route_id')
                agency = e.get('agency', 'METRO')
                r_name = e.get('route_name', '')
                r_long = e.get('route_long_name', '')

                # Color
                color = AGENCY_COLORS.get(agency, '#0057B8')
                if agency == 'METRO':
                    for k, c in METRO_COLORS.items():
                        if k.lower() == str(r_name).lower():
                            color = c
                            break

                s_start = e.get('stop_from')
                start_name = self.stops_df.loc[s_start, 'stop_name'] if s_start in self.stops_df.index else s_start

                total_leg_dur = 0.0
                total_leg_dist = 0.0
                intermediate_stops = []

                while i < n and step_edges[i].get('mode') == 'transit' and step_edges[i].get('route_id') == curr_route:
                    cur_e = step_edges[i]
                    total_leg_dur += cur_e.get('weight', 0)
                    total_leg_dist += cur_e.get('dist_m', 0)
                    s_cur_to = cur_e.get('stop_to')
                    cur_to_name = self.stops_df.loc[s_cur_to, 'stop_name'] if s_cur_to in self.stops_df.index else s_cur_to
                    intermediate_stops.append(cur_to_name)
                    i += 1

                end_name = intermediate_stops[-1] if intermediate_stops else start_name

                # Nombre formal de la agencia
                agency_title = self.agencies_df.loc[agency, 'agency_name'] if agency in self.agencies_df.index else agency
                instr = f"Abordar {agency_title} (Línea {r_name}) en {start_name} hacia {end_name}"

                legs.append({
                    'leg_number': leg_num,
                    'type': 'transit',
                    'agency': agency,
                    'agency_name': agency_title,
                    'route_id': curr_route,
                    'route_short_name': r_name,
                    'route_long_name': r_long,
                    'color': color,
                    'instruction': instr,
                    'from': start_name,
                    'to': end_name,
                    'num_stops': len(intermediate_stops),
                    'intermediate_stops': intermediate_stops,
                    'distance_m': round(total_leg_dist),
                    'duration_min': round(total_leg_dur, 1)
                })
                leg_num += 1

            else:
                i += 1

        return legs

    def _calculate_fares(self, legs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcula el costo total considerando reglas tarifarias de CDMX."""
        total_cost = 0.0
        breakdown = []
        boarded_agencies = []

        for leg in legs:
            if leg['type'] == 'transit':
                agency = leg['agency']
                r_name = str(leg.get('route_short_name', ''))

                # Reglas de transbordo gratuito en Metro y Metrobús
                if agency == 'METRO':
                    if 'METRO' not in boarded_agencies:
                        cost = FARES_MXN['METRO']
                        total_cost += cost
                        breakdown.append({'concept': 'STC Metro (Tarifa Integrada)', 'cost_mxn': cost})
                        boarded_agencies.append('METRO')
                    else:
                        breakdown.append({'concept': f"Transbordo gratuito STC Metro (Línea {r_name})", 'cost_mxn': 0.0})

                elif agency == 'MB':
                    if 'MB' not in boarded_agencies:
                        cost = FARES_MXN['MB']
                        total_cost += cost
                        breakdown.append({'concept': 'Metrobús CDMX', 'cost_mxn': cost})
                        boarded_agencies.append('MB')
                    else:
                        breakdown.append({'concept': f"Transbordo gratuito Metrobús (Línea {r_name})", 'cost_mxn': 0.0})

                elif agency == 'TROLE':
                    # Línea 10 Trolebús Elevado tiene tarifa de $7.00
                    if r_name in ('10', 'L10', '12'):
                        cost = FARES_MXN['TROLE_ELEVADO']
                        desc = f"Trolebús Elevado Línea {r_name}"
                    else:
                        cost = FARES_MXN['TROLE']
                        desc = f"Trolebús Línea {r_name}"
                    total_cost += cost
                    breakdown.append({'concept': desc, 'cost_mxn': cost})
                    boarded_agencies.append('TROLE')

                elif agency in FARES_MXN:
                    cost = FARES_MXN[agency]
                    agency_name = leg.get('agency_name', agency)
                    total_cost += cost
                    breakdown.append({'concept': f"{agency_name} (Línea {r_name})", 'cost_mxn': cost})
                    boarded_agencies.append(agency)
                else:
                    cost = 5.00
                    total_cost += cost
                    breakdown.append({'concept': f"Transporte Público ({agency})", 'cost_mxn': cost})
                    boarded_agencies.append(agency)

        return {'total_cost_mxn': round(total_cost, 2), 'breakdown': breakdown}

    def _calculate_emissions(self, legs: List[Dict[str, Any]], direct_dist_m: float) -> Dict[str, Any]:
        """Calcula emisiones evitadas de CO2 en comparación con viaje en automóvil privado."""
        transit_distance_km = sum(l['distance_m'] for l in legs if l['type'] == 'transit') / 1000.0
        car_distance_km = max(transit_distance_km, direct_dist_m / 1000.0)

        car_emissions_kg = (car_distance_km * CAR_CO2_GRAMS_PER_KM) / 1000.0
        transit_emissions_kg = (transit_distance_km * TRANSIT_CO2_GRAMS_PER_KM) / 1000.0
        co2_saved_kg = max(0.0, car_emissions_kg - transit_emissions_kg)

        return {
            'car_emissions_kg': round(car_emissions_kg, 3),
            'transit_emissions_kg': round(transit_emissions_kg, 3),
            'co2_saved_kg': round(co2_saved_kg, 3)
        }

    def format_cli_output(self, result: Dict[str, Any]) -> str:
        """Formatea los resultados en un reporte de consola visual y estructurado."""
        if result.get('status') != 'OK':
            return f"\n[!] Error en el ruteo: {result.get('message', 'Ruta no encontrada')}\n"

        s = result['summary']
        lines = []
        lines.append("\n" + "="*72)
        lines.append("  🗺️   CALCULADORA DE RUTAS MULTIMODAL CDMX - CHILANGATÓN 2026")
        lines.append("="*72)
        lines.append(f"  📍 Origen:      {s['origin']['name']} ({s['origin']['lat']:.4f}, {s['origin']['lon']:.4f})")
        lines.append(f"  🎯 Destino:     {s['destination']['name']} ({s['destination']['lat']:.4f}, {s['destination']['lon']:.4f})")
        lines.append("-" * 72)
        lines.append(f"  ⏱️  Tiempo Total:     {s['total_duration_minutes']} minutos")
        lines.append(f"  🚶 Caminata:         {s['total_walk_minutes']} min ({s['total_walk_meters']} metros)")
        lines.append(f"  🚇 En Tránsito:      {s['total_transit_minutes']} min ({s['num_transfers']} transbordos)")
        lines.append(f"  💵 Costo Total:      ${s['total_cost_mxn']:.2f} MXN")
        lines.append(f"  🌱 CO₂ Ahorrado:     {s['co2_saved_kg']} kg (vs automóvil privado)")
        lines.append("-" * 72)
        lines.append("  ITINERARIO PASO A PASO:")
        lines.append("-" * 72)

        for leg in result['legs']:
            l_num = leg['leg_number']
            l_type = leg['type']
            dur = leg['duration_min']
            dist = leg.get('distance_m', 0)

            if l_type == 'walk':
                subtype = leg.get('subtype', '')
                tag = "🚶 [Caminata Inicial]" if subtype == 'first_mile' else ("🚶 [Caminata Final]" if subtype == 'last_mile' else "🚶 [Caminata]")
                lines.append(f"  {l_num}. {tag} - {dur} min ({dist} m)")
                lines.append(f"     De: {leg['from']}")
                lines.append(f"     A:  {leg['to']}")
                lines.append(f"     👉 {leg['instruction']}")

            elif l_type == 'transfer':
                lines.append(f"  {l_num}. 🔄 [Transbordo a Pie] - {dur} min ({dist} m)")
                lines.append(f"     👉 {leg['instruction']}")

            elif l_type == 'transit':
                agency = leg['agency']
                r_name = leg['route_short_name']
                a_name = leg.get('agency_name', agency)
                icon = "🚇" if agency == 'METRO' else ("🚍" if agency in ('MB', 'TROLE') else "🚡")
                lines.append(f"  {l_num}. {icon} [{a_name} - Línea {r_name}] - {dur} min ({dist} m)")
                lines.append(f"     Subir en: {leg['from']}")
                lines.append(f"     Bajar en: {leg['to']} ({leg['num_stops']} estaciones)")
                if leg.get('intermediate_stops') and len(leg['intermediate_stops']) > 1:
                    stops_str = " ➔ ".join(leg['intermediate_stops'][:4])
                    if len(leg['intermediate_stops']) > 4:
                        stops_str += f" ➔ ... ({len(leg['intermediate_stops'])} en total)"
                    lines.append(f"     Estaciones: {stops_str}")

            lines.append("")

        lines.append("-" * 72)
        lines.append("  💳 DESGLOSE DE TARIFA (Movilidad Integrada CDMX):")
        for item in result['fare_breakdown']:
            cost_str = f"${item['cost_mxn']:.2f} MXN" if item['cost_mxn'] > 0 else "GRATUITO (Transbordo)"
            lines.append(f"     • {item['concept']:<45} {cost_str:>20}")
        lines.append("="*72 + "\n")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Calculadora de Rutas Multimodal CDMX (Chilangatón 2026)")
    parser.add_argument('--origin', help="Coordenadas de origen: lat,lon (ej. 19.4326,-99.1332)")
    parser.add_argument('--dest', help="Coordenadas de destino: lat,lon (ej. 19.4086,-99.1228)")
    parser.add_argument('--from', dest='from_place', help="Nombre del lugar de origen (ej. 'Zócalo', 'Bellas Artes')")
    parser.add_argument('--to', dest='to_place', help="Nombre del lugar de destino (ej. 'Mercado Jamaica', 'Tianguis Meyehualco')")
    parser.add_argument('--rebuild-cache', action='store_true', help="Reconstruir caché de grafo desde los archivos GTFS")
    parser.add_argument('--json', action='store_true', help="Emitir resultado en formato JSON puro")
    parser.add_argument('--bench', action='store_true', help="Ejecutar suite de pruebas de ruteo en CDMX")

    args = parser.parse_args()

    router = CDMXMultimodalRouter(rebuild_cache=args.rebuild_cache)

    if args.bench:
        test_cases = [
            ("Zócalo", "Mercado Jamaica"),
            ("Bellas Artes", "Tianguis Santa Cruz Meyehualco"),
            ("Zócalo", "Central de Abasto"),
            ("Coyoacán Centro", "Mercado de la Merced"),
            ("Indios Verdes", "Mercado Jamaica")
        ]
        print("\n=== SUITE DE PRUEBAS DE RUTEO CDMX ===")
        for o_name, d_name in test_cases:
            o_poi = router.find_poi(o_name)
            d_poi = router.find_poi(d_name)
            if o_poi and d_poi:
                t0 = time.time()
                res = router.calculate_route(o_poi[0], o_poi[1], d_poi[0], d_poi[1], o_poi[2], d_poi[2])
                dur = res['summary']['total_duration_minutes']
                cost = res['summary']['total_cost_mxn']
                walk_m = res['summary']['total_walk_meters']
                print(f"✓ {o_name} ➔ {d_name}: {dur} min | ${cost:.2f} MXN | {walk_m}m caminata | calculada en {time.time()-t0:.3f}s")
        print("======================================\n")
        return

    orig_lat, orig_lon, orig_label = None, None, "Origen"
    dest_lat, dest_lon, dest_label = None, None, "Destino"

    if args.from_place:
        poi = router.find_poi(args.from_place)
        if poi:
            orig_lat, orig_lon, orig_label = poi
        else:
            print(f"[!] No se encontró el lugar de origen '{args.from_place}'. Usando búsqueda directa.")
            sys.exit(1)
    elif args.origin:
        parts = args.origin.split(',')
        orig_lat, orig_lon = float(parts[0]), float(parts[1])
        orig_label = f"Coord ({orig_lat:.4f}, {orig_lon:.4f})"

    if args.to_place:
        poi = router.find_poi(args.to_place)
        if poi:
            dest_lat, dest_lon, dest_label = poi
        else:
            print(f"[!] No se encontró el lugar de destino '{args.to_place}'.")
            sys.exit(1)
    elif args.dest:
        parts = args.dest.split(',')
        dest_lat, dest_lon = float(parts[0]), float(parts[1])
        dest_label = f"Coord ({dest_lat:.4f}, {dest_lon:.4f})"

    # Valores por defecto para prueba si no se especificaron argumentos
    if orig_lat is None or dest_lat is None:
        # Default: Zócalo a Mercado Jamaica
        poi_orig = router.find_poi('zocalo')
        poi_dest = router.find_poi('mercado jamaica')
        orig_lat, orig_lon, orig_label = poi_orig
        dest_lat, dest_lon, dest_label = poi_dest

    result = router.calculate_route(orig_lat, orig_lon, dest_lat, dest_lon, orig_label, dest_label)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(router.format_cli_output(result))


if __name__ == '__main__':
    main()
