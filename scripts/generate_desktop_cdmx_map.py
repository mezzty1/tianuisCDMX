import json
import base64
import re
import os

def generate():
    print("Compilando versión con Planificador de Rutas A->B y Marcador GPS Azul...")
    with open('data/processed/map_bundle.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open('assets/fonts/estaciones.woff', 'rb') as f:
        woff_b64 = base64.b64encode(f.read()).decode('utf-8')

    with open('assets/css/ui-transport-mx.css', 'r', encoding='utf-8') as f:
        raw_css = f.read()

    icon_rules = re.findall(r'(\.estacion-[a-z0-9\-]+:before\s*\{[^\}]+\})', raw_css)
    icon_rules_css = '\n    '.join(icon_rules)
    available_icons = set(re.findall(r'\.estacion-([a-z0-9\-]+):before', raw_css))

    for st in data['metro_stations']:
        c = st['icon_class'].replace('estacion-', '')
        if c in available_icons:
            st['has_glyph'] = True
        else:
            st['has_glyph'] = False
            words = st['nombre'].split()
            if len(words) >= 2:
                st['fallback_text'] = (words[0][0] + words[1][0]).upper()
            else:
                st['fallback_text'] = st['nombre'][:2].upper()

    data_json_str = json.dumps(data, ensure_ascii=False)

    html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Movilidad y Comercio CDMX · Portal de Datos</title>
  
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <!-- Google Fonts: Montserrat -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet">

  <style>
    @font-face {{
      font-family: 'estaciones';
      src: url('data:font/woff;base64,{woff_b64}') format('woff');
      font-weight: normal;
      font-style: normal;
    }}

    em[class^="estacion-"], em[class*=" estacion-"] {{
      color: #ffffff !important;
      font-size: 13px;
      font-family: 'estaciones' !important;
      font-style: normal;
      font-weight: normal;
      line-height: 1;
      display: inline-block;
      speak: none;
      -webkit-font-smoothing: antialiased;
    }}

    {icon_rules_css}

    :root {{
      --cdmx-green-dark: #0f5953;
      --cdmx-green-primary: #116962;
      --cdmx-green-light: #eef7f6;
      --cdmx-green-chip: #d5ece9;
      --cdmx-bg: #f8fafc;
      --cdmx-text-dark: #092c29;
      --cdmx-text-muted: #527370;
      --cdmx-border: #d4e7e5;
      --shadow-sidebar: 4px 0 24px rgba(15, 89, 83, 0.12);
      --shadow-fab: 0 4px 14px rgba(0, 0, 0, 0.14);
      --font-main: 'Montserrat', sans-serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-main);
      background: #eef2f6;
      color: var(--cdmx-text-dark);
      height: 100vh;
      width: 100vw;
      overflow: hidden;
      display: flex;
    }}

    /* Sidebar de Escritorio */
    #sidebar {{
      width: 420px;
      height: 100vh;
      background: #ffffff;
      border-right: 1px solid var(--cdmx-border);
      box-shadow: var(--shadow-sidebar);
      display: flex;
      flex-direction: column;
      z-index: 1001;
      transition: margin-left 0.3s ease;
      flex-shrink: 0;
    }}

    #sidebar.collapsed {{
      margin-left: -420px;
    }}

    .sidebar-header {{
      background: var(--cdmx-green-dark);
      color: #ffffff;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .sidebar-brand-title {{
      font-size: 1.05rem;
      font-weight: 800;
      letter-spacing: -0.01em;
    }}

    .sidebar-brand-sub {{
      font-size: 0.72rem;
      color: #bbf7d0;
      font-weight: 500;
    }}

    .btn-toggle-sidebar {{
      background: rgba(255, 255, 255, 0.15);
      border: none;
      color: #fff;
      width: 32px;
      height: 32px;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s;
    }}

    .btn-toggle-sidebar:hover {{
      background: rgba(255, 255, 255, 0.28);
    }}

    #btn-open-sidebar {{
      position: absolute;
      top: 18px;
      left: 18px;
      z-index: 1000;
      display: none;
      background: var(--cdmx-green-dark);
      color: #fff;
      border: none;
      border-radius: 10px;
      padding: 10px 14px;
      box-shadow: var(--shadow-fab);
      cursor: pointer;
      font-weight: 700;
      font-size: 0.82rem;
      align-items: center;
      gap: 6px;
    }}

    .sidebar-scroll {{
      flex: 1;
      overflow-y: auto;
      padding: 16px 18px 24px 18px;
    }}

    .section-block {{
      margin-bottom: 18px;
    }}

    .section-heading {{
      font-size: 0.8rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--cdmx-text-dark);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    /* Planificador de Rutas A -> B */
    .route-planner-card {{
      background: #f0fdf4;
      border: 1.5px solid #22c55e;
      border-radius: 12px;
      padding: 14px;
      margin-bottom: 16px;
    }}

    .route-planner-title {{
      font-size: 0.86rem;
      font-weight: 800;
      color: #15803d;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .route-input-group {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-bottom: 10px;
    }}

    .route-input-row {{
      position: relative;
    }}

    .route-input-row input, .route-input-row select {{
      width: 100%;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      padding: 7px 10px 7px 28px;
      border-radius: 8px;
      font-size: 0.78rem;
      font-family: inherit;
      color: #1e293b;
    }}

    .route-dot-indicator {{
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }}

    .btn-calc-route {{
      width: 100%;
      background: var(--cdmx-green-dark);
      color: #ffffff;
      border: none;
      padding: 9px;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: background 0.2s;
    }}

    .btn-calc-route:hover {{
      background: var(--cdmx-green-primary);
    }}

    #route-result-box {{
      display: none;
      margin-top: 10px;
      background: #ffffff;
      border: 1px solid #86efac;
      padding: 10px;
      border-radius: 8px;
      font-size: 0.76rem;
    }}

    /* Buscador */
    .search-input-box {{
      position: relative;
    }}

    .search-input-box input {{
      width: 100%;
      background: #f1f5f9;
      border: 1px solid var(--cdmx-border);
      padding: 8px 12px 8px 32px;
      border-radius: 8px;
      font-size: 0.8rem;
      font-family: inherit;
      color: var(--cdmx-text-dark);
    }}

    .search-icon-svg {{
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      fill: var(--cdmx-text-muted);
      width: 15px;
      height: 15px;
    }}

    /* Chips */
    .chips-flow {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}

    .chip-btn {{
      background: #ffffff;
      border: 1px solid #cbdad7;
      color: var(--cdmx-text-dark);
      padding: 5px 10px;
      border-radius: 8px;
      font-size: 0.74rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .chip-btn:hover {{
      border-color: var(--cdmx-green-dark);
    }}

    .chip-btn.active {{
      background: var(--cdmx-green-light);
      border-color: var(--cdmx-green-dark);
      color: var(--cdmx-green-dark);
    }}

    .btn-dropdown-main {{
      background: var(--cdmx-green-dark);
      color: #ffffff;
      border: none;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 5px;
      cursor: pointer;
    }}

    #transport-dropdown-menu {{
      background: #ffffff;
      border: 1px solid var(--cdmx-border);
      border-radius: 10px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.12);
      padding: 6px;
      display: none;
      position: absolute;
      z-index: 1050;
      width: 220px;
    }}

    .t-opt {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 6px 8px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.78rem;
      font-weight: 600;
      transition: background 0.15s;
    }}

    .t-opt:hover {{
      background: var(--cdmx-green-light);
    }}

    .t-badge {{
      width: 22px;
      height: 22px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-size: 0.68rem;
      font-weight: 800;
    }}

    /* Ficha de Detalle */
    #detail-card {{
      display: none;
      background: var(--cdmx-green-light);
      border: 1.5px solid var(--cdmx-green-dark);
      border-radius: 12px;
      padding: 12px;
      margin-bottom: 14px;
    }}

    .detail-tag {{
      display: inline-block;
      font-size: 0.62rem;
      font-weight: 800;
      text-transform: uppercase;
      padding: 2px 6px;
      border-radius: 4px;
      color: #fff;
    }}

    .detail-name {{
      font-size: 1.05rem;
      font-weight: 800;
      color: var(--cdmx-green-dark);
      margin: 3px 0 1px 0;
    }}

    .detail-loc {{
      font-size: 0.74rem;
      color: var(--cdmx-text-muted);
      margin-bottom: 8px;
    }}

    .stats-2col {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
      margin-bottom: 8px;
    }}

    .stat-pill {{
      background: #ffffff;
      padding: 6px 8px;
      border-radius: 6px;
      border: 1px solid #dbeae8;
    }}

    .stat-pill-val {{
      font-size: 0.9rem;
      font-weight: 800;
      color: var(--cdmx-green-dark);
    }}

    .stat-pill-lbl {{
      font-size: 0.6rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--cdmx-text-muted);
    }}

    /* Accesos Rápidos */
    .goto-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      text-align: center;
    }}

    .goto-btn {{
      display: flex;
      flex-direction: column;
      align-items: center;
      cursor: pointer;
      text-decoration: none;
    }}

    .goto-btn-circle {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: var(--cdmx-green-dark);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 4px;
      box-shadow: 0 2px 6px rgba(15, 89, 83, 0.2);
      transition: transform 0.2s;
    }}

    .goto-btn:hover .goto-btn-circle {{
      transform: translateY(-2px);
      background: var(--cdmx-green-primary);
    }}

    .goto-btn-circle svg {{
      width: 20px;
      height: 20px;
      fill: #ffffff;
    }}

    .goto-btn-lbl {{
      font-size: 0.65rem;
      font-weight: 700;
      color: var(--cdmx-text-dark);
      line-height: 1.1;
    }}

    /* Mapa y Flotantes */
    #map-wrapper {{
      flex: 1;
      height: 100vh;
      position: relative;
    }}

    #map {{
      width: 100%;
      height: 100%;
    }}

    .map-floating-actions {{
      position: absolute;
      right: 20px;
      bottom: 24px;
      z-index: 1000;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .map-fab {{
      width: 44px;
      height: 44px;
      background: #ffffff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--shadow-fab);
      border: 1px solid rgba(0,0,0,0.06);
      cursor: pointer;
      transition: all 0.2s;
    }}

    .map-fab:hover {{
      transform: scale(1.06);
    }}

    .map-fab svg {{
      width: 22px;
      height: 22px;
    }}

    /* Marcador GPS Azul con Halo Pulsante (Estilo Google Maps / iOS) */
    .user-gps-pulse-halo {{
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: rgba(37, 99, 235, 0.25);
      border: 2px solid #2563eb;
      animation: pulseGps 1.8s infinite ease-out;
      position: absolute;
      top: -4px;
      left: -4px;
    }}

    .user-gps-blue-dot {{
      width: 16px;
      height: 16px;
      background: #2563eb;
      border: 3px solid #ffffff;
      border-radius: 50%;
      box-shadow: 0 0 8px rgba(37, 99, 235, 0.6);
      position: relative;
    }}

    @keyframes pulseGps {{
      0% {{ transform: scale(0.8); opacity: 0.8; }}
      70% {{ transform: scale(2.2); opacity: 0; }}
      100% {{ transform: scale(2.4); opacity: 0; }}
    }}

    /* Badges de Estaciones */
    .metro-station-badge {{
      width: 22px;
      height: 22px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
      border: 1px solid #ffffff;
      cursor: pointer;
      transition: transform 0.15s ease;
      color: #ffffff;
      font-size: 9px;
      font-weight: 800;
    }}

    .metro-station-badge:hover {{
      transform: scale(1.4);
      z-index: 9999 !important;
    }}

    .mb-station-badge {{
      width: 20px;
      height: 20px;
      background: #d81b60;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-size: 9px;
      font-weight: 800;
      box-shadow: 0 2px 5px rgba(0,0,0,0.25);
      border: 1px solid #ffffff;
      cursor: pointer;
      transition: transform 0.15s ease;
    }}

    /* Banner Flotante de Modo Ruta Limpia */
    .route-focus-banner {{
      position: absolute;
      top: 18px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1200;
      background: #ffffff;
      border-radius: 36px;
      box-shadow: 0 8px 30px rgba(15, 23, 42, 0.22);
      border: 1px solid #cbd5e1;
      padding: 7px 18px;
      display: none;
      align-items: center;
      gap: 16px;
      animation: slideDownFocus 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    @keyframes slideDownFocus {{
      from {{ opacity: 0; transform: translate(-50%, -18px); }}
      to {{ opacity: 1; transform: translate(-50%, 0); }}
    }}

    .focus-pulse-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
      animation: pulseGreenDot 1.6s infinite ease-out;
    }}

    @keyframes pulseGreenDot {{
      0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
      70% {{ box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }}
      100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
    }}

    .btn-exit-focus {{
      background: #fee2e2;
      color: #991b1b;
      border: 1px solid #fecaca;
      border-radius: 20px;
      padding: 5px 12px;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s ease;
    }}

    .btn-exit-focus:hover {{
      background: #ef4444;
      color: #ffffff;
      border-color: #ef4444;
    }}

    .btn-clear-route-box {{
      margin-top: 10px;
      width: 100%;
      background: #f8fafc;
      color: #475569;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 8px 10px;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}

    .btn-clear-route-box:hover {{
      background: #e2e8f0;
      color: #0f172a;
    }}

    /* Estilos para los marcadores de la ruta limpia */
    .route-pin-badge {{
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 4px 8px;
      border-radius: 20px;
      font-weight: 800;
      font-size: 11px;
      color: #ffffff;
      box-shadow: 0 3px 12px rgba(0,0,0,0.3);
      border: 2px solid #ffffff;
      white-space: nowrap;
    }}

    .route-pin-badge-a {{
      background: #2563eb;
    }}

    .route-pin-badge-b {{
      background: #ef4444;
    }}

    .route-intermediate-station {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #ffffff;
      border: 2px solid #000000;
      box-shadow: 0 1px 4px rgba(0,0,0,0.4);
    }}
  </style>
</head>
<body>

  <button id="btn-open-sidebar" onclick="toggleSidebar()">
    <span>☰</span>
    <span>Abrir Menú</span>
  </button>

  <aside id="sidebar">
    <div class="sidebar-header">
      <div>
        <div class="sidebar-brand-title">Movilidad y Comercio CDMX</div>
        <div class="sidebar-brand-sub">Chilangotón 2026 · Reto 1</div>
      </div>
      <button class="btn-toggle-sidebar" onclick="toggleSidebar()" title="Colapsar panel lateral">◀</button>
    </div>

    <div class="sidebar-scroll">

      <!-- Planificador de Rutas Interactivo (A -> B) -->
      <div class="route-planner-card">
        <div class="route-planner-title">
          <span>🧭 Planificar Ruta (Punto A ➔ B)</span>
          <span style="font-size:0.65rem; background:#bbf7d0; color:#166534; padding:2px 6px; border-radius:4px;">MULTIMODAL</span>
        </div>

        <div class="route-input-group">
          <div class="route-input-row">
            <span class="route-dot-indicator" style="background:#2563eb;"></span>
            <input type="text" id="route-from" placeholder="Origen: 'Mi ubicación' o lugar (ej. Zócalo, Bellas Artes)" value="Mi ubicación">
          </div>
          <div class="route-input-row">
            <span class="route-dot-indicator" style="background:#ef4444;"></span>
            <input type="text" id="route-to" placeholder="Destino: Mercado, Tianguis o Lugar (ej. Jamaica)" value="Mercado Jamaica">
          </div>
        </div>

        <button class="btn-calc-route" onclick="calculateRouteUI()">
          <span>⚡</span>
          <span>Calcular Ruta Óptima</span>
        </button>

        <div id="route-result-box">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <div style="font-weight:800; color:#15803d; font-size:0.85rem;" id="route-summary-title">Ruta Calculada</div>
            <span style="font-size:0.65rem; background:#dcfce7; color:#166534; font-weight:800; padding:2px 6px; border-radius:4px;">RUTA LIMPIA</span>
          </div>
          <div id="route-summary-content" style="color:#334155; line-height:1.45; font-size:0.78rem;"></div>
          <button class="btn-clear-route-box" onclick="exitRouteFocusMode()">
            <span>✕</span>
            <span>Limpiar ruta y restaurar todas las capas</span>
          </button>
        </div>
      </div>

      <!-- Ficha de Detalle Dinámica -->
      <div id="detail-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
          <span class="detail-tag" id="panel-tag" style="background:var(--cdmx-green-dark);">MERCADO PÚBLICO</span>
          <button style="border:none; background:transparent; cursor:pointer; font-size:1.1rem; color:#64748b;" onclick="closeDetailCard()">✕</button>
        </div>
        <div class="detail-name" id="panel-name">Mercado</div>
        <div class="detail-loc" id="panel-sub">Alcaldía · Colonia</div>

        <div class="stats-2col">
          <div class="stat-pill">
            <div class="stat-pill-val" id="panel-stat1">--</div>
            <div class="stat-pill-lbl" id="panel-lbl1">Locales</div>
          </div>
          <div class="stat-pill">
            <div class="stat-pill-val" id="panel-stat2">--</div>
            <div class="stat-pill-lbl" id="panel-lbl2">Superficie</div>
          </div>
        </div>

        <div style="background:#ffffff; padding:8px; border-radius:8px; border:1px solid #dbeae8; margin-bottom:8px; font-size:0.75rem;">
          <div style="font-weight:700; color:var(--cdmx-green-dark); margin-bottom:2px;">🚌 Conexión de Movilidad:</div>
          <div id="panel-conn" style="color:#334155;">Cargando estación o corredor cercano...</div>
        </div>

        <div>
          <button onclick="setAsRouteDestination()" style="width:100%; background:#0f5953; color:#fff; border:none; padding:9px 12px; border-radius:8px; font-size:0.78rem; font-weight:700; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px;">
            <span>🎯</span>
            <span>Planificar Ruta hacia aquí</span>
          </button>
        </div>
      </div>

      <!-- Buscador Rápido -->
      <div class="section-block">
        <div class="section-heading">
          <span>Buscador de Mercados y Tianguis</span>
        </div>
        <div class="search-input-box">
          <svg class="search-icon-svg" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
          <input type="text" id="market-search" placeholder="Buscar mercado o tianguis...">
        </div>
      </div>

      <!-- Capas de Comercio Barrial -->
      <div class="section-block">
        <div class="section-heading">
          <span>Comercio Popular</span>
        </div>
        <div class="chips-flow">
          <button class="chip-btn active" id="chip-mercados" onclick="toggleLayer('mercados')">🏪 Mercados (329)</button>
          <button class="chip-btn active" id="chip-tianguis" onclick="toggleLayer('tianguis')">🧺 Tianguis (1,367)</button>
          <button class="chip-btn active" id="chip-msr" onclick="toggleLayer('msr')">🚚 Rutas MSR (51)</button>
          <button class="chip-btn" id="chip-dia-hoy" onclick="filterByToday()">📅 Abrir Hoy</button>
        </div>
      </div>

      <!-- Capas de Transporte -->
      <div class="section-block">
        <div class="section-heading">
          <span>Red de Transporte</span>
          <button class="btn-dropdown-main" onclick="toggleTransportDropdown(event)">
            <span>Líneas MI</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="#fff"><path d="M7 10l5 5 5-5z"/></svg>
          </button>
        </div>

        <div class="chips-flow">
          <button class="chip-btn active" id="chip-metro_icons" onclick="toggleLayer('metro_icons')">🚇 Íconos Metro (195)</button>
          <button class="chip-btn active" id="chip-metrobus_icons" onclick="toggleLayer('metrobus_icons')">🚍 Íconos Metrobús (324)</button>
          <button class="chip-btn active" id="chip-concesionado" onclick="toggleLayer('concesionado')">🚐 Rutas Secundarias (331)</button>
          <button class="chip-btn active" id="chip-alcaldias" onclick="toggleLayer('alcaldias')">🗺️ Alcaldías CDMX</button>
          <button class="chip-btn active" id="chip-zmvm" onclick="toggleLayer('zmvm')">🌐 Área Metropolitana</button>
        </div>

        <div id="transport-dropdown-menu">
          <div class="t-opt" onclick="toggleSubsystem('METRO')">
            <div class="t-badge" style="background:#ef4444;">M</div>
            <span>Metro (Líneas 1-12)</span>
          </div>
          <div class="t-opt" onclick="toggleSubsystem('MB')">
            <div class="t-badge" style="background:#ec4899;">MB</div>
            <span>Metrobús (L1-L7)</span>
          </div>
          <div class="t-opt" onclick="toggleSubsystem('TROLE')">
            <div class="t-badge" style="background:#10b981;">TE</div>
            <span>Trolebús</span>
          </div>
          <div class="t-opt" onclick="toggleSubsystem('CBB')">
            <div class="t-badge" style="background:#06b6d4;">CB</div>
            <span>Cablebús</span>
          </div>
          <div class="t-opt" onclick="toggleSubsystem('RTP')">
            <div class="t-badge" style="background:#15803d;">RTP</div>
            <span>RTP Pasajeros</span>
          </div>
          <div class="t-opt" onclick="toggleSubsystem('TL')">
            <div class="t-badge" style="background:#3b82f6;">TL</div>
            <span>Tren Ligero</span>
          </div>
          <div class="t-opt" onclick="toggleSubsystem('CC')">
            <div class="t-badge" style="background:#8e24aa;">CC</div>
            <span>Corredores Concesionados</span>
          </div>
        </div>
      </div>

      <!-- Accesos Rápidos -->
      <div class="section-block">
        <div class="section-heading">
          <span>Accesos Rápidos</span>
        </div>
        <div class="goto-row">
          <div class="goto-btn" onclick="showStreetClosures()">
            <div class="goto-btn-circle">
              <svg viewBox="0 0 24 24"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>
            </div>
            <div class="goto-btn-lbl">Cierres Vías</div>
          </div>

          <div class="goto-btn" onclick="showHoursModal()">
            <div class="goto-btn-circle">
              <svg viewBox="0 0 24 24"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/></svg>
            </div>
            <div class="goto-btn-lbl">Horarios</div>
          </div>

          <div class="goto-btn" onclick="showRoutesModal()">
            <div class="goto-btn-circle">
              <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
            </div>
            <div class="goto-btn-lbl">Secundarias</div>
          </div>
        </div>
      </div>

    </div>
  </aside>

  <main id="map-wrapper">
    <div id="map"></div>

    <!-- Banner Flotante de Modo Ruta Limpia -->
    <div id="route-focus-banner" class="route-focus-banner">
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="focus-pulse-dot"></span>
        <div>
          <div style="font-size:0.65rem; font-weight:800; color:#0f5953; letter-spacing:0.5px;">MODO RUTA LIMPIA ACTIVO</div>
          <div style="font-size:0.82rem; font-weight:700; color:#0f172a;" id="focus-banner-text">Mostrando únicamente el trayecto origen ➔ destino</div>
        </div>
      </div>
      <button class="btn-exit-focus" onclick="exitRouteFocusMode()" title="Restaurar capas completas">
        <span>✕</span>
        <span>Restaurar mapa completo</span>
      </button>
    </div>

    <div class="map-floating-actions">
      <button class="map-fab" onclick="locateUser()" title="Mi ubicación GPS (Punto Azul)">
        <svg viewBox="0 0 24 24" fill="#0d9488"><path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/></svg>
      </button>
      <button class="map-fab" onclick="resetMapView()" title="Centrar CDMX">
        <svg viewBox="0 0 24 24" fill="#0f5953"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 14h-2v-2h2v2zm0-4h-2V7h2v5z"/></svg>
      </button>
      <button class="map-fab" onclick="toggleBaseMap()" title="Alternar Mapa Base">
        <svg viewBox="0 0 24 24" fill="#0284c7"><path d="M11.99 18.54l-7.37-5.73L3 14.07l9 7 9-7-1.63-1.27-7.38 5.74zM12 16l7.36-5.73L21 9.07l-9-7-9 7 1.63 1.2L12 16z"/></svg>
      </button>
    </div>
  </main>

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <script>
    const MAP_DATA = {data_json_str};

    const map = L.map('map', {{
      center: [19.4326, -99.1332],
      zoom: 12,
      minZoom: 9,
      maxZoom: 18,
      zoomControl: false
    }});

    L.control.zoom({{ position: 'topright' }}).addTo(map);

    // Mapa base limpio sin marcas de agua (Esri Light Gray)
    let currentBase = 'esri';
    const esriLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
      attribution: 'Esri, HERE, Garmin, &copy; OpenStreetMap contributors',
      maxZoom: 18
    }}).addTo(map);

    const osmLayer = L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19
    }});

    function toggleBaseMap() {{
      if (currentBase === 'esri') {{
        map.removeLayer(esriLayer);
        osmLayer.addTo(map);
        currentBase = 'osm';
      }} else {{
        map.removeLayer(osmLayer);
        esriLayer.addTo(map);
        currentBase = 'esri';
      }}
    }}

    // Capas
    const layers = {{
      zmvm: L.geoJSON(null, {{
        style: {{
          color: '#94a3b8',
          weight: 1,
          dashArray: '3, 4',
          fillColor: '#f1f5f9',
          fillOpacity: 0.15
        }},
        onEachFeature: (feature, layer) => {{
          const nom = feature.properties.NOMGEO || 'Municipio Metropolitano';
          layer.bindTooltip(nom + ' (Edomex / ZMVM)', {{ sticky: true }});
        }}
      }}),
      alcaldias: L.geoJSON(null, {{
        style: {{
          color: '#0f5953',
          weight: 2,
          dashArray: '4, 4',
          fillColor: '#0f5953',
          fillOpacity: 0.03
        }},
        onEachFeature: (feature, layer) => {{
          const nom = feature.properties.nomgeo || feature.properties.alcaldia || 'Alcaldía';
          layer.bindTooltip('Alcaldía ' + nom, {{ sticky: true }});
        }}
      }}),
      metro: L.featureGroup(),
      metro_icons: L.featureGroup(),
      metrobus: L.featureGroup(),
      metrobus_icons: L.featureGroup(),
      rtp: L.featureGroup(),
      cablebus: L.featureGroup(),
      trolebus: L.featureGroup(),
      tren: L.featureGroup(),
      concesionado: L.featureGroup(),
      mercados: L.featureGroup(),
      msr: L.featureGroup(),
      tianguis: L.featureGroup(),
      routeLines: L.featureGroup(),
      userLocation: L.featureGroup()
    }};

    if (MAP_DATA.zmvm) {{
      layers.zmvm.addData(MAP_DATA.zmvm);
      layers.zmvm.addTo(map);
    }}
    if (MAP_DATA.alcaldias) {{
      layers.alcaldias.addData(MAP_DATA.alcaldias);
      layers.alcaldias.addTo(map);
    }}
    layers.routeLines.addTo(map);
    layers.userLocation.addTo(map);

    // Trazados de Transporte
    const transportMapping = {{
      'METRO': layers.metro,
      'MB': layers.metrobus,
      'RTP': layers.rtp,
      'CBB': layers.cablebus,
      'TROLE': layers.trolebus,
      'TL': layers.tren,
      'CC': layers.concesionado
    }};

    Object.keys(transportMapping).forEach(agency => {{
      const tData = MAP_DATA.transport[agency];
      if (tData && tData.features) {{
        const fg = transportMapping[agency];
        tData.features.forEach(f => {{
          const polyline = L.polyline(
            f.geometry.coordinates.map(c => [c[1], c[0]]),
            {{
              color: f.properties.color,
              weight: f.properties.weight,
              opacity: 0.9
            }}
          );

          polyline.bindPopup(`
            <div style="font-weight:800; color:${{f.properties.color}}; font-size:0.92rem; margin-bottom:2px;">
              ${{f.properties.agency_name}}
            </div>
            <div style="font-size:0.75rem; color:#334155; margin-bottom:4px;">
              Ruta: <b>${{f.properties.route_short || ''}} ${{f.properties.route_long || ''}}</b>
            </div>
            <div style="font-size:0.7rem; color:#64748b;">
              ${{f.properties.headsign || 'Servicio Concesionado / Red'}}
            </div>
          `);

          polyline.on('click', () => {{
            showTransportInDetail(f.properties);
          }});

          fg.addLayer(polyline);
        }});
        fg.addTo(map);
      }}
    }});

    // ESTACIONES DEL METRO CON ICONOGRAFÍA COMPLETA
    if (MAP_DATA.metro_stations) {{
      MAP_DATA.metro_stations.forEach(st => {{
        let glyphHtml = '';
        if (st.has_glyph) {{
          glyphHtml = `<em class="${{st.icon_class}}"></em>`;
        }} else {{
          glyphHtml = `<span style="font-size:8.5px; font-weight:800; color:#fff;">${{st.fallback_text || 'M'}}</span>`;
        }}

        const iconHtml = `
          <div class="metro-station-badge" style="background:${{st.color}};" title="${{st.nombre}} (Línea ${{st.linea}})">
            ${{glyphHtml}}
          </div>
        `;
        const customIcon = L.divIcon({{
          className: 'custom-metro-icon-container',
          html: iconHtml,
          iconSize: [22, 22],
          iconAnchor: [11, 11]
        }});

        const marker = L.marker([st.lat, st.lon], {{ icon: customIcon }});
        marker.bindPopup(`
          <div style="font-weight:800; color:${{st.color}}; font-size:0.92rem; margin-bottom:2px;">
            Metro ${{st.nombre}}
          </div>
          <div style="font-size:0.75rem; color:#475569; margin-bottom:4px;">
            Línea ${{st.linea}} · ${{st.tipo}} · ${{st.alcaldia}}
          </div>
          <span style="background:#fee2e2; color:#991b1b; font-size:0.7rem; font-weight:700; padding:2px 6px; border-radius:4px;">
            Tarifa: $5.00 MXN
          </span>
        `);

        marker.on('click', () => {{
          showMetroStationInDetail(st);
        }});

        layers.metro_icons.addLayer(marker);
      }});
      layers.metro_icons.addTo(map);
    }}

    // ESTACIONES METROBÚS
    if (MAP_DATA.metrobus_stations) {{
      MAP_DATA.metrobus_stations.forEach(st => {{
        const iconHtml = `<div class="mb-station-badge" title="${{st.nombre}} (${{st.linea}})">MB</div>`;
        const customIcon = L.divIcon({{
          className: 'custom-mb-icon-container',
          html: iconHtml,
          iconSize: [20, 20],
          iconAnchor: [10, 10]
        }});

        const marker = L.marker([st.lat, st.lon], {{ icon: customIcon }});
        marker.bindPopup(`
          <div style="font-weight:800; color:#d81b60; font-size:0.92rem; margin-bottom:2px;">
            Metrobús ${{st.nombre}}
          </div>
          <div style="font-size:0.75rem; color:#475569; margin-bottom:4px;">
            ${{st.linea}} · Alcaldía ${{st.alcaldia}}
          </div>
          <span style="background:#fce7f3; color:#9d174d; font-size:0.7rem; font-weight:700; padding:2px 6px; border-radius:4px;">
            Tarifa: $6.00 MXN
          </span>
        `);

        layers.metrobus_icons.addLayer(marker);
      }});
      layers.metrobus_icons.addTo(map);
    }}

    // Mercados Públicos
    let currentSelectedTarget = null;
    const marketMarkers = [];
    if (MAP_DATA.mercados) {{
      MAP_DATA.mercados.forEach(m => {{
        const marker = L.circleMarker([m.lat, m.lon], {{
          radius: m.radio,
          fillColor: '#f59e0b',
          color: '#ffffff',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.85
        }});

        marker.bindPopup(`
          <div style="font-weight:800; color:#b45309; font-size:0.95rem; margin-bottom:2px;">
            Mercado ${{m.nombre}}
          </div>
          <div style="font-size:0.75rem; color:#475569; margin-bottom:4px;">
            ${{m.alcaldia}} · ${{m.colonia}}
          </div>
          <div>
            <span style="background:#fef3c7; color:#92400e; font-size:0.7rem; font-weight:700; padding:2px 6px; border-radius:4px;">
              ${{m.locales}} locales
            </span>
            <span style="background:#e0f2fe; color:#0369a1; font-size:0.7rem; font-weight:700; padding:2px 6px; border-radius:4px;">
              ${{m.categoria}}
            </span>
          </div>
        `);

        marker.on('click', () => {{
          currentSelectedTarget = {{ name: 'Mercado ' + m.nombre, lat: m.lat, lon: m.lon }};
          showMarketInDetail(m);
        }});

        marker.marketData = m;
        marketMarkers.push(marker);
        layers.mercados.addLayer(marker);
      }});
      layers.mercados.addTo(map);
    }}

    // Mercados Sobre Ruedas
    if (MAP_DATA.msr) {{
      MAP_DATA.msr.forEach(m => {{
        const marker = L.circleMarker([m.lat, m.lon], {{
          radius: m.radio,
          fillColor: '#10b981',
          color: '#ffffff',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.85
        }});

        marker.bindPopup(`
          <div style="font-weight:800; color:#047857; font-size:0.95rem; margin-bottom:2px;">
            MSR: ${{m.ruta}}
          </div>
          <div style="font-size:0.75rem; color:#475569; margin-bottom:4px;">
            ${{m.alcaldia}} · ${{m.colonia}}
          </div>
          <div>
            <span style="background:#d1fae5; color:#065f46; font-size:0.7rem; font-weight:700; padding:2px 6px; border-radius:4px;">
              Día: ${{m.dia}}
            </span>
            <span style="background:#dbeafe; color:#1e40af; font-size:0.7rem; font-weight:700; padding:2px 6px; border-radius:4px;">
              ${{m.oferentes}} oferentes
            </span>
          </div>
        `);

        marker.on('click', () => {{
          currentSelectedTarget = {{ name: 'MSR ' + m.ruta, lat: m.lat, lon: m.lon }};
          showMSRInDetail(m);
        }});

        layers.msr.addLayer(marker);
      }});
      layers.msr.addTo(map);
    }}

    // Tianguis
    function renderTianguisMarkers(filterDay = null) {{
      layers.tianguis.clearLayers();
      MAP_DATA.tianguis.forEach(t => {{
        if (!filterDay || t.dia.includes(filterDay)) {{
          const marker = L.circleMarker([t.lat, t.lon], {{
            radius: 5.5,
            fillColor: '#0f5953',
            color: '#ffffff',
            weight: 1.5,
            opacity: 1,
            fillOpacity: 0.8
          }});

          marker.bindPopup(`
            <div style="font-weight:800; color:#0f5953; font-size:0.92rem; margin-bottom:2px;">
              Tianguis Móvil
            </div>
            <div style="font-size:0.75rem; color:#475569; margin-bottom:4px;">
              ${{t.alcaldia}} · ${{t.colonia}}
            </div>
            <div style="font-size:0.7rem; color:#64748b; margin-bottom:4px;">
              📍 ${{t.ubicacion}}
            </div>
            <span style="background:#ccfbf1; color:#0f766e; font-size:0.7rem; font-weight:700; padding:2px 6px; border-radius:4px;">
              ${{t.dia}}
            </span>
            <span style="background:#e2e8f0; color:#334155; font-size:0.7rem; padding:2px 6px; border-radius:4px;">
              ${{t.horario}}
            </span>
          `);

          marker.on('click', () => {{
            currentSelectedTarget = {{ name: 'Tianguis ' + t.colonia, lat: t.lat, lon: t.lon }};
            showTianguisInDetail(t);
          }});

          layers.tianguis.addLayer(marker);
        }}
      }});
      layers.tianguis.addTo(map);
    }}
    renderTianguisMarkers();

    // GEOLOCALIZACIÓN: PUNTO AZUL CON HALO PULSANTE
    let userCurrentCoords = [19.4326, -99.1332]; // Default Zócalo si no activa GPS
    function locateUser() {{
      map.locate({{ setView: true, maxZoom: 15, enableHighAccuracy: true }});
    }}

    map.on('locationfound', function(e) {{
      userCurrentCoords = [e.latlng.lat, e.latlng.lng];
      layers.userLocation.clearLayers();

      // Marcador con punto azul y halo pulsante animado
      const blueDotHtml = `
        <div style="position:relative; width:16px; height:16px;">
          <div class="user-gps-pulse-halo"></div>
          <div class="user-gps-blue-dot"></div>
        </div>
      `;
      const blueDotIcon = L.divIcon({{
        className: 'user-gps-container',
        html: blueDotHtml,
        iconSize: [16, 16],
        iconAnchor: [8, 8]
      }});

      const marker = L.marker(e.latlng, {{ icon: blueDotIcon }}).bindPopup(`
        <div style="font-weight:800; color:#2563eb; font-size:0.85rem;">📍 Tu Ubicación Actual</div>
        <div style="font-size:0.72rem; color:#64748b;">Precisión GPS: +/- ${{Math.round(e.accuracy)}} metros</div>
      `).openPopup();

      // Círculo de precisión semitransparente
      const radiusCircle = L.circle(e.latlng, {{
        radius: e.accuracy,
        color: '#2563eb',
        weight: 1,
        fillColor: '#3b82f6',
        fillOpacity: 0.12
      }});

      layers.userLocation.addLayer(radiusCircle);
      layers.userLocation.addLayer(marker);
    }});

    map.on('locationerror', function(err) {{
      alert('Aviso de Ubicación: Activa el permiso de ubicación en tu navegador para mostrar tu punto azul en el mapa.');
    }});

    // GESTIÓN DE CAPAS Y MODO RUTA LIMPIA
    const ALL_DATA_LAYERS = [
      'zmvm', 'alcaldias', 'metro', 'metro_icons', 'metrobus', 'metrobus_icons',
      'rtp', 'cablebus', 'trolebus', 'tren', 'concesionado',
      'mercados', 'msr', 'tianguis'
    ];
    let isFocusRouteMode = false;
    let savedActiveLayers = [];

    function enterRouteFocusMode(originLabel, destLabel) {{
      if (!isFocusRouteMode) {{
        savedActiveLayers = ALL_DATA_LAYERS.filter(k => layers[k] && map.hasLayer(layers[k]));
        savedActiveLayers.forEach(k => map.removeLayer(layers[k]));
        isFocusRouteMode = true;
      }}
      document.getElementById('route-focus-banner').style.display = 'flex';
      document.getElementById('focus-banner-text').innerText = `${{originLabel}} ➔ ${{destLabel}}`;
    }}

    function exitRouteFocusMode() {{
      if (isFocusRouteMode) {{
        savedActiveLayers.forEach(k => {{
          if (layers[k]) map.addLayer(layers[k]);
        }});
        isFocusRouteMode = false;
      }}
      layers.routeLines.clearLayers();
      document.getElementById('route-focus-banner').style.display = 'none';
      document.getElementById('route-result-box').style.display = 'none';
      resetMapView();
    }}

    // Grafo de la red del Metro CDMX para ruteo multi-estación y transbordos
    const METRO_GRAPH = {{
      lines: {{}},
      adj: {{}},
      built: false,
      build: function() {{
        if (this.built || !MAP_DATA.metro_stations) return;
        
        MAP_DATA.metro_stations.forEach(st => {{
          if (!this.lines[st.linea]) this.lines[st.linea] = [];
          this.lines[st.linea].push(st);
        }});

        const addEdge = (u, v, cost, line) => {{
          if (!this.adj[u]) this.adj[u] = [];
          if (!this.adj[v]) this.adj[v] = [];
          this.adj[u].push({{ target: v, cost: cost, line: line }});
          this.adj[v].push({{ target: u, cost: cost, line: line }});
        }};

        Object.keys(this.lines).forEach(lId => {{
          const stList = this.lines[lId];
          for (let i = 0; i < stList.length - 1; i++) {{
            const u = stList[i].nombre + '||' + lId;
            const v = stList[i+1].nombre + '||' + lId;
            addEdge(u, v, 1.8, lId);
          }}
        }});

        const nameMap = {{}};
        MAP_DATA.metro_stations.forEach(st => {{
          const baseName = st.nombre.split('/')[0].trim().toLowerCase();
          if (!nameMap[baseName]) nameMap[baseName] = [];
          nameMap[baseName].push(st);
        }});

        Object.keys(nameMap).forEach(base => {{
          const list = nameMap[base];
          if (list.length > 1) {{
            for (let i = 0; i < list.length; i++) {{
              for (let j = i + 1; j < list.length; j++) {{
                const u = list[i].nombre + '||' + list[i].linea;
                const v = list[j].nombre + '||' + list[j].linea;
                addEdge(u, v, 3.5, 'TRANSB');
              }}
            }}
          }}
        }});

        this.built = true;
      }},
      findPath: function(startStation, endStation) {{
        this.build();
        const startKey = startStation.nombre + '||' + startStation.linea;
        const endKey = endStation.nombre + '||' + endStation.linea;

        if (startKey === endKey) return [startStation];

        const dist = {{}};
        const prev = {{}};
        const visited = new Set();
        dist[startKey] = 0;
        const pq = [{{ node: startKey, cost: 0 }}];

        while (pq.length > 0) {{
          let minIdx = 0;
          for (let i = 1; i < pq.length; i++) {{
            if (pq[i].cost < pq[minIdx].cost) minIdx = i;
          }}
          const {{ node: u, cost: c }} = pq.splice(minIdx, 1)[0];

          if (visited.has(u)) continue;
          visited.add(u);

          if (u === endKey) {{
            const pathKeys = [];
            let curr = u;
            while (curr && curr !== startKey) {{
              pathKeys.unshift(curr);
              curr = prev[curr];
            }}
            pathKeys.unshift(startKey);
            return pathKeys.map(k => {{
              const [n, l] = k.split('||');
              return MAP_DATA.metro_stations.find(s => s.nombre === n && s.linea === l);
            }}).filter(Boolean);
          }}

          const neighbors = this.adj[u] || [];
          for (let edge of neighbors) {{
            const v = edge.target;
            const newCost = c + edge.cost;
            if (!visited.has(v) && newCost < (dist[v] !== undefined ? dist[v] : Infinity)) {{
              dist[v] = newCost;
              prev[v] = u;
              pq.push({{ node: v, cost: newCost }});
            }}
          }}
        }}
        return null;
      }}
    }};

    // PLANIFICADOR DE RUTAS (PUNTO A -> B) INTERACTIVO
    function setAsRouteDestination() {{
      if (currentSelectedTarget) {{
        document.getElementById('route-to').value = currentSelectedTarget.name;
        openSidebarIfClosed();
        calculateRouteUI();
      }}
    }}

    function findDestinationTarget(query) {{
      const q = query.toLowerCase().trim();
      if (!q) return null;

      // 1. Si currentSelectedTarget coincide
      if (currentSelectedTarget && currentSelectedTarget.name.toLowerCase().includes(q)) {{
        return {{
          name: currentSelectedTarget.name,
          lat: currentSelectedTarget.lat,
          lon: currentSelectedTarget.lon,
          type: 'Seleccionado'
        }};
      }}

      // 2. Buscar en Mercados Públicos
      for (let m of (MAP_DATA.mercados || [])) {{
        if (m.nombre.toLowerCase().includes(q) || q.includes(m.nombre.toLowerCase())) {{
          return {{
            name: 'Mercado ' + m.nombre,
            lat: m.lat,
            lon: m.lon,
            type: 'Mercado Público (' + m.alcaldia + ')'
          }};
        }}
      }}

      // 3. Buscar en Tianguis Móviles
      for (let t of (MAP_DATA.tianguis || [])) {{
        if (t.colonia.toLowerCase().includes(q) || t.ubicacion.toLowerCase().includes(q)) {{
          return {{
            name: 'Tianguis ' + t.colonia,
            lat: t.lat,
            lon: t.lon,
            type: 'Tianguis Móvil (' + t.dia + ')'
          }};
        }}
      }}

      // 4. Buscar en Mercados Sobre Ruedas
      for (let msr of (MAP_DATA.msr || [])) {{
        if (msr.ruta.toLowerCase().includes(q) || msr.colonia.toLowerCase().includes(q)) {{
          return {{
            name: 'MSR ' + msr.ruta,
            lat: msr.lat,
            lon: msr.lon,
            type: 'Mercado Sobre Ruedas (' + msr.dia + ')'
          }};
        }}
      }}

      // 5. Buscar en Estaciones de Metro
      for (let st of (MAP_DATA.metro_stations || [])) {{
        if (st.nombre.toLowerCase().includes(q)) {{
          return {{
            name: 'Metro ' + st.nombre,
            lat: st.lat,
            lon: st.lon,
            type: 'Estación Metro'
          }};
        }}
      }}

      return null;
    }}

    function calculateRouteUI() {{
      const fromVal = document.getElementById('route-from').value.trim();
      const toVal = document.getElementById('route-to').value.trim();
      const resultBox = document.getElementById('route-result-box');
      const titleEl = document.getElementById('route-summary-title');
      const contentEl = document.getElementById('route-summary-content');

      layers.routeLines.clearLayers();

      // Coordenadas origen
      let startCoords = userCurrentCoords;
      let originName = 'Tu Ubicación Actual';

      if (fromVal.toLowerCase().includes('bellas artes')) {{
        startCoords = [19.4352, -99.1412];
        originName = 'Bellas Artes';
      }} else if (fromVal.toLowerCase().includes('zocalo') || fromVal.toLowerCase().includes('zócalo')) {{
        startCoords = [19.4326, -99.1332];
        originName = 'Zócalo / Plaza de la Constitución';
      }} else if (fromVal.toLowerCase().includes('revolucion') || fromVal.toLowerCase().includes('revolución')) {{
        startCoords = [19.4354, -99.1542];
        originName = 'Monumento a la Revolución';
      }} else if (!fromVal.toLowerCase().includes('mi ubicaci') && !fromVal.toLowerCase().includes('ubicaci')) {{
        originName = fromVal;
      }}

      // Coordenadas destino
      let destTarget = findDestinationTarget(toVal);
      if (!destTarget) {{
        destTarget = {{
          name: toVal || 'Mercado Jamaica',
          lat: 19.4086,
          lon: -99.1228,
          type: 'Destino Barrial'
        }};
      }}
      const endCoords = [destTarget.lat, destTarget.lon];

      // Buscar estación de transporte más cercana al origen y al destino
      let nearestMetroStart = findClosestMetro(startCoords[0], startCoords[1]);
      let nearestMetroEnd = findClosestMetro(endCoords[0], endCoords[1]);

      if (!nearestMetroStart || !nearestMetroEnd) {{
        alert('No se encontraron estaciones cercanas para trazar la ruta.');
        return;
      }}

      // ACTIVAR MODO RUTA LIMPIA (Oculta todas las líneas, mercados y tianguis)
      enterRouteFocusMode(originName, destTarget.name);

      // Calcular trayecto del Metro (con transbordos si aplica)
      const metroPath = METRO_GRAPH.findPath(nearestMetroStart, nearestMetroEnd);
      const stationSequence = (metroPath && metroPath.length > 0) ? metroPath : [nearestMetroStart, nearestMetroEnd];

      // 1. PIN ORIGEN (PUNTO A)
      const originMarker = L.marker(startCoords, {{
        icon: L.divIcon({{
          className: 'custom-pin-a',
          html: `<div class="route-pin-badge route-pin-badge-a">📍 A: ${{originName}}</div>`,
          iconSize: [120, 26],
          iconAnchor: [60, 13]
        }})
      }}).bindPopup(`<b>Origen (Punto A):</b> ${{originName}}`);
      layers.routeLines.addLayer(originMarker);

      // 2. TRAMO 1: Caminata inicial hacia primera estación
      const walkDist1 = Math.round(getDistMeters(startCoords[0], startCoords[1], nearestMetroStart.lat, nearestMetroStart.lon));
      const walkMin1 = Math.max(1, Math.round(walkDist1 / 75));
      const walk1 = L.polyline([startCoords, [nearestMetroStart.lat, nearestMetroStart.lon]], {{
        color: '#2563eb',
        dashArray: '6, 8',
        weight: 4,
        opacity: 0.95
      }}).bindPopup(`🚶 <b>Tramo 1:</b> Caminar ${{walkDist1}} m (~${{walkMin1}} min) hacia Metro ${{nearestMetroStart.nombre}}`);
      layers.routeLines.addLayer(walk1);

      // 3. BADGE ESTACIÓN DE ABORDAJE
      const boardGlyph = nearestMetroStart.has_glyph ? `<em class="${{nearestMetroStart.icon_class}}"></em>` : `<span style="font-size:9px; font-weight:800; color:#fff;">M</span>`;
      const boardMarker = L.marker([nearestMetroStart.lat, nearestMetroStart.lon], {{
        icon: L.divIcon({{
          className: 'custom-station-badge',
          html: `<div class="metro-station-badge route-pin-badge-station" style="background:${{nearestMetroStart.color}}; width:26px; height:26px; font-size:12px;" title="Abordar Metro ${{nearestMetroStart.nombre}} (Línea ${{nearestMetroStart.linea}})">${{boardGlyph}}</div>`,
          iconSize: [26, 26],
          iconAnchor: [13, 13]
        }})
      }}).bindPopup(`🚇 <b>1. Abordar Metro:</b> ${{nearestMetroStart.nombre}} (Línea ${{nearestMetroStart.linea}})`);
      layers.routeLines.addLayer(boardMarker);

      // 4. TRAZADO DE LÍNEA DE TRANSPORTE A LO LARGO DE LAS ESTACIONES
      const lineSegments = [];
      let currentSegment = [];
      let currentLine = stationSequence[0].linea;
      let currentColor = stationSequence[0].color || '#ef4444';
      let transfersCount = 0;
      let transferSteps = [];

      for (let i = 0; i < stationSequence.length; i++) {{
        const st = stationSequence[i];
        if (st.linea !== currentLine) {{
          // Hubo transbordo
          transfersCount++;
          transferSteps.push(`🔄 Transbordo en <b>${{st.nombre}}</b> (de Línea ${{currentLine}} a Línea ${{st.linea}})`);
          if (currentSegment.length > 0) {{
            lineSegments.push({{ coords: currentSegment, color: currentColor, line: currentLine }});
          }}
          currentSegment = [[st.lat, st.lon]];
          currentLine = st.linea;
          currentColor = st.color;

          // Marcador de transbordo
          const transbMarker = L.marker([st.lat, st.lon], {{
            icon: L.divIcon({{
              className: 'custom-transb-icon',
              html: `<div style="background:#f59e0b; color:#fff; width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:11px; border:2px solid #fff; box-shadow:0 2px 6px rgba(0,0,0,0.35);" title="Transbordo en ${{st.nombre}}">🔄</div>`,
              iconSize: [22, 22],
              iconAnchor: [11, 11]
            }})
          }}).bindPopup(`🔄 <b>Transbordo:</b> ${{st.nombre}} (hacia Línea ${{st.linea}})`);
          layers.routeLines.addLayer(transbMarker);
        }} else {{
          currentSegment.push([st.lat, st.lon]);
        }}

        // Pequeño nodo intermedio
        if (i > 0 && i < stationSequence.length - 1 && st.linea === currentLine) {{
          const dotMarker = L.circleMarker([st.lat, st.lon], {{
            radius: 3.5,
            fillColor: currentColor,
            color: '#ffffff',
            weight: 1.5,
            fillOpacity: 1
          }}).bindTooltip(`Metro ${{st.nombre}} (Línea ${{st.linea}})`, {{ sticky: true }});
          layers.routeLines.addLayer(dotMarker);
        }}
      }}
      if (currentSegment.length > 0) {{
        lineSegments.push({{ coords: currentSegment, color: currentColor, line: currentLine }});
      }}

      // Dibujar polilíneas sólidas de cada línea del metro
      lineSegments.forEach(seg => {{
        if (seg.coords.length > 1) {{
          const tLine = L.polyline(seg.coords, {{
            color: seg.color,
            weight: 6,
            opacity: 0.95,
            lineCap: 'round',
            lineJoin: 'round'
          }}).bindPopup(`🚇 <b>Metro Línea ${{seg.line}}</b> (${{seg.coords.length}} estaciones)`);
          layers.routeLines.addLayer(tLine);
        }}
      }});

      // 5. BADGE ESTACIÓN DE DESCENSO
      const alightGlyph = nearestMetroEnd.has_glyph ? `<em class="${{nearestMetroEnd.icon_class}}"></em>` : `<span style="font-size:9px; font-weight:800; color:#fff;">M</span>`;
      const alightMarker = L.marker([nearestMetroEnd.lat, nearestMetroEnd.lon], {{
        icon: L.divIcon({{
          className: 'custom-station-badge',
          html: `<div class="metro-station-badge route-pin-badge-station" style="background:${{nearestMetroEnd.color}}; width:26px; height:26px; font-size:12px;" title="Descenso en Metro ${{nearestMetroEnd.nombre}} (Línea ${{nearestMetroEnd.linea}})">${{alightGlyph}}</div>`,
          iconSize: [26, 26],
          iconAnchor: [13, 13]
        }})
      }}).bindPopup(`🚶 <b>Descenso de Metro:</b> ${{nearestMetroEnd.nombre}} (Línea ${{nearestMetroEnd.linea}})`);
      layers.routeLines.addLayer(alightMarker);

      // 6. TRAMO 3: Caminata final desde estación hasta destino comercial
      const walkDist2 = Math.round(getDistMeters(nearestMetroEnd.lat, nearestMetroEnd.lon, endCoords[0], endCoords[1]));
      const walkMin2 = Math.max(1, Math.round(walkDist2 / 75));
      const walk2 = L.polyline([[nearestMetroEnd.lat, nearestMetroEnd.lon], endCoords], {{
        color: '#16a34a',
        dashArray: '6, 8',
        weight: 4,
        opacity: 0.95
      }}).bindPopup(`🚶 <b>Tramo Final:</b> Caminar ${{walkDist2}} m (~${{walkMin2}} min) hacia ${{destTarget.name}}`);
      layers.routeLines.addLayer(walk2);

      // 7. PIN DESTINO (PUNTO B)
      const destMarker = L.marker(endCoords, {{
        icon: L.divIcon({{
          className: 'custom-pin-b',
          html: `<div class="route-pin-badge route-pin-badge-b">🎯 B: ${{destTarget.name}}</div>`,
          iconSize: [140, 26],
          iconAnchor: [70, 13]
        }})
      }}).bindPopup(`<b>Destino (Punto B):</b> ${{destTarget.name}}<br><small style="color:#64748b;">${{destTarget.type}}</small>`);
      layers.routeLines.addLayer(destMarker);

      // Ajustar vista limpia
      map.fitBounds(layers.routeLines.getBounds(), {{ padding: [65, 65] }});

      // Tiempos e indicadores
      const transitTimeMin = Math.round(stationSequence.length * 2.2 + transfersCount * 4.0);
      const totalTimeMin = walkMin1 + transitTimeMin + walkMin2;
      const co2Kg = (totalTimeMin * 0.025).toFixed(2);

      // Actualizar tarjeta lateral
      resultBox.style.display = 'block';
      titleEl.innerText = `Ruta hacia ${{destTarget.name}}`;
      
      let stepsHtml = `
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:8px 10px; margin-bottom:8px;">
          <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
            <span>⏱️ <b>Tiempo estimado:</b></span>
            <span style="font-weight:800; color:#15803d;">~${{totalTimeMin}} min</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
            <span>💵 <b>Tarifa oficial MI:</b></span>
            <span style="font-weight:800; color:#0f5953;">$5.00 MXN</span>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span>🌱 <b>Ahorro de CO₂:</b></span>
            <span style="font-weight:700; color:#16a34a;">~${{co2Kg}} kg vs auto</span>
          </div>
        </div>

        <div style="font-size:0.75rem; color:#1e293b; display:flex; flex-direction:column; gap:6px;">
          <div><b>1.</b> 🚶 Caminar <b>${{walkDist1}} m (~${{walkMin1}} min)</b> hacia <b>Metro ${{nearestMetroStart.nombre}}</b>.</div>
          <div><b>2.</b> 🚇 Abordar <b>Metro Línea ${{nearestMetroStart.linea}}</b> en <b>${{nearestMetroStart.nombre}}</b>.</div>
      `;

      if (transferSteps.length > 0) {{
        transferSteps.forEach(ts => {{
          stepsHtml += `<div><b>•</b> ${{ts}}</div>`;
        }});
      }}

      stepsHtml += `
          <div><b>3.</b> 🚶 Descenso en <b>Metro ${{nearestMetroEnd.nombre}}</b> (Línea ${{nearestMetroEnd.linea}}).</div>
          <div><b>4.</b> 🚶 Caminar <b>${{walkDist2}} m (~${{walkMin2}} min)</b> hacia <b>${{destTarget.name}}</b>.</div>
        </div>
      `;

      contentEl.innerHTML = stepsHtml;
    }}

    function findClosestMetro(lat, lon) {{
      let nearest = null;
      let minD = Infinity;
      if (MAP_DATA.metro_stations) {{
        for (let st of MAP_DATA.metro_stations) {{
          const d = getDistMeters(lat, lon, st.lat, st.lon);
          if (d < minD) {{
            minD = d;
            nearest = st;
          }}
        }}
      }}
      return nearest;
    }}

    function getDistMeters(lat1, lon1, lat2, lon2) {{
      const R = 6371e3;
      const phi1 = lat1 * Math.PI/180;
      const phi2 = lat2 * Math.PI/180;
      const deltaPhi = (lat2-lat1) * Math.PI/180;
      const deltaLambda = (lon2-lon1) * Math.PI/180;
      const a = Math.sin(deltaPhi/2) * Math.sin(deltaPhi/2) +
                Math.cos(phi1) * Math.cos(phi2) *
                Math.sin(deltaLambda/2) * Math.sin(deltaLambda/2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
      return R * c;
    }}

    // Mostrar detalle
    function showMarketInDetail(m) {{
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      document.getElementById('panel-tag').innerText = 'MERCADO PÚBLICO';
      document.getElementById('panel-tag').style.background = '#d97706';
      document.getElementById('panel-name').innerText = 'Mercado ' + m.nombre;
      document.getElementById('panel-sub').innerText = m.alcaldia + ' · ' + m.colonia;

      document.getElementById('panel-stat1').innerText = m.locales;
      document.getElementById('panel-lbl1').innerText = 'Locales';

      document.getElementById('panel-stat2').innerText = m.superficie_m2 > 0 ? (m.superficie_m2.toLocaleString() + ' m²') : 'N/D';
      document.getElementById('panel-lbl2').innerText = 'Superficie';

      document.getElementById('panel-conn').innerHTML = `
        🚇 Metro / Metrobús conectado a pie.<br>
        <span style="color:#0f5953; font-weight:700;">Tarifa oficial MI: $5.00 - $6.00 MXN.</span>
      `;

      openSidebarIfClosed();
    }}

    function showTianguisInDetail(t) {{
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      document.getElementById('panel-tag').innerText = 'TIANGUIS MÓVIL';
      document.getElementById('panel-tag').style.background = '#0f5953';
      document.getElementById('panel-name').innerText = 'Tianguis ' + t.colonia;
      document.getElementById('panel-sub').innerText = t.alcaldia + ' · ' + t.colonia;

      document.getElementById('panel-stat1').innerText = t.dia;
      document.getElementById('panel-lbl1').innerText = 'Día';

      document.getElementById('panel-stat2').innerText = t.horario;
      document.getElementById('panel-lbl2').innerText = 'Horario';

      document.getElementById('panel-conn').innerHTML = `
        <b>Vía cerrada:</b> <i>${{t.ubicacion}}</i>
      `;

      openSidebarIfClosed();
    }}

    function showMSRInDetail(m) {{
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      document.getElementById('panel-tag').innerText = 'MERCADO SOBRE RUEDAS';
      document.getElementById('panel-tag').style.background = '#10b981';
      document.getElementById('panel-name').innerText = m.ruta + ' (' + m.colonia + ')';
      document.getElementById('panel-sub').innerText = m.alcaldia + ' · ' + m.direccion;

      document.getElementById('panel-stat1').innerText = m.dia;
      document.getElementById('panel-lbl1').innerText = 'Día en esta sede';

      document.getElementById('panel-stat2').innerText = m.oferentes;
      document.getElementById('panel-lbl2').innerText = 'Oferentes';

      document.getElementById('panel-conn').innerHTML = `
        <b>Ruta itinerante:</b> Se traslada de colonia a lo largo de la semana.
      `;

      openSidebarIfClosed();
    }}

    function showMetroStationInDetail(st) {{
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      document.getElementById('panel-tag').innerText = 'ESTACIÓN METRO CDMX';
      document.getElementById('panel-tag').style.background = st.color;
      document.getElementById('panel-name').innerText = 'Estación ' + st.nombre;
      document.getElementById('panel-sub').innerText = 'Línea ' + st.linea + ' · Alcaldía ' + st.alcaldia;

      document.getElementById('panel-stat1').innerText = '$5.00 MXN';
      document.getElementById('panel-lbl1').innerText = 'Tarifa Oficial';

      document.getElementById('panel-stat2').innerText = st.tipo;
      document.getElementById('panel-lbl2').innerText = 'Tipo';

      document.getElementById('panel-conn').innerHTML = `
        🚇 Estación de la red primaria que conecta con mercados y tianguis barriales.
      `;

      openSidebarIfClosed();
    }}

    function showTransportInDetail(p) {{
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      document.getElementById('panel-tag').innerText = p.agency_name;
      document.getElementById('panel-tag').style.background = p.color;
      document.getElementById('panel-name').innerText = (p.route_short || '') + ' ' + (p.route_long || '');
      document.getElementById('panel-sub').innerText = 'Destino: ' + (p.headsign || 'Servicio Concesionado/Red');

      document.getElementById('panel-stat1').innerText = p.agency === 'METRO' ? '$5.00' : (p.agency === 'MB' ? '$6.00' : (p.agency === 'CC' ? 'Por tramo' : '$2.00-$4.00'));
      document.getElementById('panel-lbl1').innerText = 'Tarifa';

      document.getElementById('panel-stat2').innerText = p.agency === 'CC' ? 'Efectivo / Mi' : 'Tarjeta MI';
      document.getElementById('panel-lbl2').innerText = 'Pago';

      document.getElementById('panel-conn').innerHTML = `
        <b>Corredor / Ruta:</b> Conexión de transporte que abastece y alimenta a la zona comercial.
      `;

      openSidebarIfClosed();
    }}

    function closeDetailCard() {{
      document.getElementById('detail-card').style.display = 'none';
    }}

    function toggleSidebar() {{
      const sb = document.getElementById('sidebar');
      const btn = document.getElementById('btn-open-sidebar');
      sb.classList.toggle('collapsed');
      if (sb.classList.contains('collapsed')) {{
        btn.style.display = 'flex';
      }} else {{
        btn.style.display = 'none';
      }}
      setTimeout(() => {{ map.invalidateSize(); }}, 300);
    }}

    function openSidebarIfClosed() {{
      const sb = document.getElementById('sidebar');
      const btn = document.getElementById('btn-open-sidebar');
      if (sb.classList.contains('collapsed')) {{
        sb.classList.remove('collapsed');
        btn.style.display = 'none';
        setTimeout(() => {{ map.invalidateSize(); }}, 300);
      }}
    }}

    function resetMapView() {{
      map.setView([19.4326, -99.1332], 12);
    }}

    function toggleTransportDropdown(e) {{
      e.stopPropagation();
      const menu = document.getElementById('transport-dropdown-menu');
      menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
      const btn = e.currentTarget;
      const rect = btn.getBoundingClientRect();
      menu.style.top = (rect.bottom + 6) + 'px';
      menu.style.left = rect.left + 'px';
    }}

    document.addEventListener('click', (e) => {{
      const menu = document.getElementById('transport-dropdown-menu');
      if (menu && menu.style.display === 'block' && !menu.contains(e.target)) {{
        menu.style.display = 'none';
      }}
    }});

    function toggleSubsystem(agency) {{
      const fg = transportMapping[agency];
      if (map.hasLayer(fg)) {{
        map.removeLayer(fg);
      }} else {{
        map.addLayer(fg);
      }}
      document.getElementById('transport-dropdown-menu').style.display = 'none';
    }}

    function toggleLayer(layerKey) {{
      const chip = document.getElementById('chip-' + layerKey);
      const fg = layers[layerKey];
      if (!fg) return;

      if (map.hasLayer(fg)) {{
        map.removeLayer(fg);
        if (chip) chip.classList.remove('active');
      }} else {{
        map.addLayer(fg);
        if (chip) chip.classList.add('active');
      }}
    }}

    function filterByToday() {{
      const days = ['DOMINGO', 'LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO'];
      const today = days[new Date().getDay()];
      renderTianguisMarkers(today);
      alert('Filtrado por los tianguis que abren hoy (' + today + ').');
    }}

    const searchInput = document.getElementById('market-search');
    searchInput.addEventListener('input', (e) => {{
      const term = e.target.value.toLowerCase().trim();
      if (!term) return;

      const found = marketMarkers.find(m => 
        m.marketData.nombre.toLowerCase().includes(term) ||
        m.marketData.colonia.toLowerCase().includes(term) ||
        m.marketData.alcaldia.toLowerCase().includes(term)
      );

      if (found) {{
        map.setView([found.marketData.lat, found.marketData.lon], 15);
        found.openPopup();
        showMarketInDetail(found.marketData);
      }}
    }});

    function showStreetClosures() {{
      alert('Aviso de Cierres Viales: 1,367 tianguis generan cortes y reducciones viales en días programados. Toca cualquier tianguis para ver la calle exacta ocupada.');
    }}

    function showHoursModal() {{
      alert('Horarios Oficiales: Metro 05:00 a 24:00 (L-V), 06:00 a 24:00 (Sáb), 07:00 a 24:00 (Dom). Mercados públicos: 08:00 a 18:00 hrs.');
    }}

    function showRoutesModal() {{
      alert('Rutas Secundarias Concesionadas: 331 ramales de microbuses y corredores que penetran en colonias conectando con tianguis y mercados.');
    }}
  </script>
</body>
</html>
'''

    output_path = 'mapa_comercio_movilidad_cdmx.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML generado con Planificador y GPS Azul: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == '__main__':
    generate()
