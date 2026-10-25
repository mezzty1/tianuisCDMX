import json
import os

def generate_html():
    print("Leyendo bundle...")
    with open('data/processed/map_bundle.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    data_json_str = json.dumps(data, ensure_ascii=False)

    html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CDMX y Zona Metropolitana: Comercio Popular y Red de Movilidad</title>
  
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">

  <style>
    :root {{
      --bg-dark: #0f172a;
      --panel-bg: rgba(15, 23, 42, 0.94);
      --card-bg: #1e293b;
      --card-border: #334155;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #f59e0b;
      --rtp: #2e7d32;
      --metro: #ef4444;
      --metrobus: #ec4899;
      --cablebus: #06b6d4;
      --trolebus: #10b981;
      --tren: #3b82f6;
      --concesionado: #a855f7;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: var(--bg-dark);
      color: var(--text-main);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}

    /* Header Superior */
    header {{
      background: var(--panel-bg);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--card-border);
      padding: 10px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 1000;
    }}

    .header-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .badge-hackathon {{
      background: linear-gradient(135deg, #f59e0b, #ef4444);
      color: #fff;
      font-size: 0.7rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 4px 8px;
      border-radius: 6px;
    }}

    h1 {{
      font-size: 1.12rem;
      font-weight: 700;
      color: #fff;
    }}

    .header-subtitle {{
      font-size: 0.75rem;
      color: var(--text-muted);
    }}

    .kpis {{
      display: flex;
      gap: 12px;
      align-items: center;
    }}

    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      padding: 4px 10px;
      border-radius: 8px;
      text-align: right;
    }}

    .kpi-value {{
      font-size: 1rem;
      font-weight: 700;
      color: #f8fafc;
      font-family: 'JetBrains Mono', monospace;
    }}

    .kpi-label {{
      font-size: 0.62rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}

    /* Layout Principal */
    #workspace {{
      display: flex;
      flex: 1;
      position: relative;
      overflow: hidden;
    }}

    #map {{
      flex: 1;
      height: 100%;
      background: #0b1120;
    }}

    /* Barra Lateral de Controles */
    #sidebar {{
      width: 400px;
      background: var(--panel-bg);
      border-left: 1px solid var(--card-border);
      display: flex;
      flex-direction: column;
      z-index: 1000;
      overflow-y: auto;
      box-shadow: -4px 0 24px rgba(0,0,0,0.4);
    }}

    .sidebar-section {{
      padding: 14px 16px;
      border-bottom: 1px solid var(--card-border);
    }}

    .section-title {{
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #cbd5e1;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    /* Filtro por Día */
    .day-filter-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 5px;
    }}

    .day-btn {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      font-size: 0.73rem;
      font-weight: 600;
      padding: 6px 3px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s ease;
      text-align: center;
    }}

    .day-btn:hover {{
      border-color: var(--accent);
      color: #fff;
    }}

    .day-btn.active {{
      background: var(--accent);
      border-color: var(--accent);
      color: #0f172a;
      font-weight: 700;
    }}

    /* Toggles */
    .toggle-list {{
      display: flex;
      flex-direction: column;
      gap: 7px;
    }}

    .toggle-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      padding: 7px 11px;
      border-radius: 7px;
      cursor: pointer;
      user-select: none;
      transition: all 0.2s;
    }}

    .toggle-item:hover {{
      border-color: #475569;
    }}

    .toggle-left {{
      display: flex;
      align-items: center;
      gap: 9px;
      font-size: 0.8rem;
      font-weight: 500;
    }}

    .color-pill {{
      width: 13px;
      height: 13px;
      border-radius: 3px;
    }}

    .custom-switch {{
      width: 32px;
      height: 17px;
      background: #475569;
      border-radius: 12px;
      position: relative;
      transition: background 0.2s;
    }}

    .custom-switch::after {{
      content: '';
      position: absolute;
      width: 13px;
      height: 13px;
      background: #fff;
      border-radius: 50%;
      top: 2px;
      left: 2px;
      transition: transform 0.2s;
    }}

    .toggle-checkbox {{
      display: none;
    }}

    .toggle-checkbox:checked + .toggle-item .custom-switch {{
      background: #10b981;
    }}

    .toggle-checkbox:checked + .toggle-item .custom-switch::after {{
      transform: translateX(15px);
    }}

    /* Leyenda de Tamaños */
    .size-legend {{
      display: flex;
      flex-direction: column;
      gap: 5px;
      font-size: 0.75rem;
      color: var(--text-muted);
    }}

    .legend-row {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .circle-sample {{
      border-radius: 50%;
      background: #f59e0b;
      border: 1.5px solid #fff;
      display: inline-block;
    }}

    /* Buscador */
    .search-box {{
      position: relative;
    }}

    .search-input {{
      width: 100%;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      padding: 8px 12px 8px 32px;
      border-radius: 7px;
      color: #fff;
      font-size: 0.8rem;
      font-family: inherit;
    }}

    .search-input:focus {{
      outline: none;
      border-color: var(--accent);
    }}

    .search-icon {{
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 0.8rem;
    }}

    /* Ficha de Detalle */
    #detail-card {{
      background: #0b1329;
      border: 1px solid #38bdf8;
      border-radius: 10px;
      padding: 13px;
      display: none;
    }}

    .detail-badge {{
      display: inline-block;
      font-size: 0.65rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 4px;
      margin-bottom: 7px;
    }}

    .badge-mercado {{
      background: #d97706;
      color: #fff;
    }}

    .badge-tianguis {{
      background: #0284c7;
      color: #fff;
    }}

    .detail-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: #fff;
      margin-bottom: 4px;
    }}

    .detail-location {{
      font-size: 0.77rem;
      color: #94a3b8;
      margin-bottom: 11px;
    }}

    .detail-stat-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 7px;
      margin-bottom: 11px;
    }}

    .detail-stat {{
      background: #1e293b;
      padding: 7px;
      border-radius: 6px;
    }}

    .detail-stat-num {{
      font-size: 0.95rem;
      font-weight: 700;
      color: #38bdf8;
      font-family: 'JetBrains Mono', monospace;
    }}

    .detail-stat-txt {{
      font-size: 0.62rem;
      color: #94a3b8;
      text-transform: uppercase;
    }}

    .nearby-box {{
      background: #1e293b;
      border-left: 3px solid #10b981;
      padding: 9px;
      border-radius: 4px;
      font-size: 0.76rem;
      margin-bottom: 10px;
    }}

    .nearby-title {{
      font-weight: 700;
      color: #10b981;
      margin-bottom: 3px;
    }}

    /* Botón Sinergia RTPonky (Cero Fricción) */
    .rtponky-box {{
      background: rgba(46, 125, 50, 0.15);
      border: 1px solid #2e7d32;
      padding: 10px;
      border-radius: 8px;
      margin-top: 8px;
    }}

    .rtponky-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 4px;
    }}

    .rtponky-title {{
      font-size: 0.75rem;
      font-weight: 700;
      color: #4ade80;
    }}

    .rtponky-badge {{
      font-size: 0.62rem;
      background: #2e7d32;
      color: #fff;
      padding: 2px 5px;
      border-radius: 4px;
      font-weight: 600;
    }}

    .rtponky-desc {{
      font-size: 0.7rem;
      color: #cbd5e1;
      line-height: 1.3;
      margin-bottom: 8px;
    }}

    .rtponky-btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      width: 100%;
      background: #22c55e;
      color: #0f172a;
      text-decoration: none;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 7px 10px;
      border-radius: 6px;
      transition: background 0.2s;
    }}

    .rtponky-btn:hover {{
      background: #16a34a;
    }}

    /* Tooltips Leaflet */
    .leaflet-tooltip-dark {{
      background: rgba(15, 23, 42, 0.9);
      color: #f8fafc;
      border: 1px solid #334155;
      font-family: inherit;
      font-size: 0.72rem;
      font-weight: 600;
      border-radius: 4px;
      padding: 3px 6px;
    }}
  </style>
</head>
<body>

  <!-- Header -->
  <header>
    <div class="header-brand">
      <span class="badge-hackathon">Reto 1 · Chilangatón 2026</span>
      <div>
        <h1>CDMX y Zona Metropolitana: Comercio Barrial y Movilidad</h1>
        <div class="header-subtitle">Atlas geoespacial metropolitano · Sinergia de transporte cero fricción</div>
      </div>
    </div>
    <div class="kpis">
      <div class="kpi-card">
        <div class="kpi-value" id="kpi-mercados">329</div>
        <div class="kpi-label">Mercados Públicos</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value" id="kpi-tianguis">1,367</div>
        <div class="kpi-label">Tianguis Empadronados</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value" id="kpi-mi">146</div>
        <div class="kpi-label">Rutas MI (Metro/MB/RTP)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value" id="kpi-muns">76</div>
        <div class="kpi-label">Alcaldías y Municipios ZMVM</div>
      </div>
    </div>
  </header>

  <!-- Workspace -->
  <div id="workspace">
    
    <!-- Mapa -->
    <div id="map"></div>

    <!-- Sidebar de Controles -->
    <div id="sidebar">

      <!-- Ficha de Detalle Dinámica -->
      <div class="sidebar-section" id="detail-section">
        <div id="detail-empty" style="text-align: center; padding: 12px; color: #64748b; font-size: 0.8rem;">
          👆 Haz clic en cualquier mercado, tianguis o línea de transporte para ver su ficha de accesibilidad y sinergia.
        </div>
        <div id="detail-card">
          <span class="detail-badge badge-mercado" id="detail-badge">MERCADO PÚBLICO</span>
          <div class="detail-title" id="detail-name">Mercado</div>
          <div class="detail-location" id="detail-loc">Alcaldía · Colonia</div>
          <div class="detail-stat-grid">
            <div class="detail-stat">
              <div class="detail-stat-num" id="detail-stat1">--</div>
              <div class="detail-stat-txt" id="detail-label1">Locales</div>
            </div>
            <div class="detail-stat">
              <div class="detail-stat-num" id="detail-stat2">--</div>
              <div class="detail-stat-txt" id="detail-label2">Superficie</div>
            </div>
          </div>
          <div class="nearby-box">
            <div class="nearby-title">🚌 Acceso de Transporte</div>
            <div id="detail-transport">Cargando conexión...</div>
          </div>

          <!-- Componente Sinergia RTPonky -->
          <div class="rtponky-box" id="rtponky-container">
            <div class="rtponky-header">
              <span class="rtponky-title">🚌 Sinergia con RTPonky</span>
              <span class="rtponky-badge">CERO FRICCIÓN</span>
            </div>
            <div class="rtponky-desc">
              Consulta en tiempo real la aproximación de autobuses RTP hacia este mercado sin registros ni descargas pesadas.
            </div>
            <a href="https://rtponky.lat/" target="_blank" class="rtponky-btn">
              Ver unidades RTP en vivo en RTPonky ↗
            </a>
          </div>

        </div>
      </div>

      <!-- Buscador -->
      <div class="sidebar-section">
        <div class="section-title">🔍 Buscador Rápido</div>
        <div class="search-box">
          <span class="search-icon">🔎</span>
          <input type="text" id="market-search" class="search-input" placeholder="Buscar mercado (ej. Merced, Jamaica, Sonora, Coyoacán)...">
        </div>
      </div>

      <!-- Filtro por Día (Tianguis Móviles) -->
      <div class="sidebar-section">
        <div class="section-title">📅 Día de Instalación (Tianguis Móviles)</div>
        <div class="day-filter-grid">
          <button class="day-btn active" data-day="ALL">Todos</button>
          <button class="day-btn" data-day="LUNES">Lunes</button>
          <button class="day-btn" data-day="MARTES">Martes</button>
          <button class="day-btn" data-day="MIERCOLES">Miércoles</button>
          <button class="day-btn" data-day="JUEVES">Jueves</button>
          <button class="day-btn" data-day="VIERNES">Viernes</button>
          <button class="day-btn" data-day="SABADO">Sábado</button>
          <button class="day-btn" data-day="DOMINGO">Domingo</button>
        </div>
      </div>

      <!-- Capas de Unidades Económicas -->
      <div class="sidebar-section">
        <div class="section-title">🏪 Unidades Económicas (Comercio)</div>
        <div class="toggle-list">
          
          <label>
            <input type="checkbox" id="layer-mercados" class="toggle-checkbox" checked>
            <div class="toggle-item">
              <div class="toggle-left">
                <div class="color-pill" style="background: #f59e0b;"></div>
                <span>Mercados Públicos (Fijos)</span>
              </div>
              <div class="custom-switch"></div>
            </div>
          </label>

          <label>
            <input type="checkbox" id="layer-tianguis" class="toggle-checkbox" checked>
            <div class="toggle-item">
              <div class="toggle-left">
                <div class="color-pill" style="background: #0284c7;"></div>
                <span>Tianguis en Vía Pública (Móviles)</span>
              </div>
              <div class="custom-switch"></div>
            </div>
          </label>

          <label>
            <input type="checkbox" id="layer-msr" class="toggle-checkbox" checked>
            <div class="toggle-item">
              <div class="toggle-left">
                <div class="color-pill" style="background: #10b981;"></div>
                <span>Mercados Sobre Ruedas (Rutas)</span>
              </div>
              <div class="custom-switch"></div>
            </div>
          </label>

        </div>

        <!-- Leyenda de Tamaño -->
        <div style="margin-top: 12px;">
          <div style="font-size: 0.68rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px; font-weight: 600;">
            Escala por número de locales / concentración:
          </div>
          <div class="size-legend">
            <div class="legend-row">
              <span class="circle-sample" style="width: 22px; height: 22px;"></span>
              <span>Macro (500+ locales / Central de Abasto, Merced)</span>
            </div>
            <div class="legend-row">
              <span class="circle-sample" style="width: 16px; height: 16px;"></span>
              <span>Grande (250 a 499 locales)</span>
            </div>
            <div class="legend-row">
              <span class="circle-sample" style="width: 12px; height: 12px;"></span>
              <span>Mediano (100 a 249 locales)</span>
            </div>
            <div class="legend-row">
              <span class="circle-sample" style="width: 8px; height: 8px;"></span>
              <span>Barrial (&lt; 100 locales)</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Capas de Red de Movilidad -->
      <div class="sidebar-section">
        <div class="section-title">🚇 Red de Movilidad Integrada (MI)</div>
        <div class="toggle-list">

          <label>
            <input type="checkbox" id="layer-metro" class="toggle-checkbox" checked>
            <div class="toggle-item">
              <div class="toggle-left">
                <div class="color-pill" style="background: #ef4444;"></div>
                <span>Metro (STC) · $5.00</span>
              </div>
              <div class="custom-switch"></div>
            </div>
          </label>

          <label>
            <input type="checkbox" id="layer-metrobus" class="toggle-checkbox" checked>
            <div class="toggle-item">
              <div class="toggle-left">
                <div class="color-pill" style="background: #ec4899;"></div>
                <span>Metrobús · $6.00</span>
              </div>
              <div class="custom-switch"></div>
            </div>
          </label>

          <label>
            <input type="checkbox" id="layer-rtp" class="toggle-checkbox" checked>
            <div class="toggle-item">
              <div class="toggle-left">
                <div class="color-pill" style="background: #2e7d32;"></div>
                <span>RTP (Red de Pasajeros) · $2.00-$4.00</span>
              </div>
              <div class="custom-switch"></div>
            </div>
          </label>

          <label>
            <input type="checkbox" id="layer-cablebus" class="toggle-checkbox" checked>
            <div class="toggle-item">
              <div class="toggle-left">
                <div class="color-pill" style="background: #06b6d4;"></div>
                <span>Cablebús · $7.00</span>
              </div>
              <div class="custom-switch"></div>
            </div>
          </label>

          <label>
            <input type="checkbox" id="layer-trolebus" class="toggle-checkbox" checked>
            <div class="toggle-item">
              <div class="toggle-left">
                <div class="color-pill" style="background: #10b981;"></div>
                <span>Trolebús (STE) · $4.00</span>
              </div>
              <div class="custom-switch"></div>
            </div>
          </label>

          <label>
            <input type="checkbox" id="layer-tren" class="toggle-checkbox" checked>
            <div class="toggle-item">
              <div class="toggle-left">
                <div class="color-pill" style="background: #3b82f6;"></div>
                <span>Tren Ligero · $3.00</span>
              </div>
              <div class="custom-switch"></div>
            </div>
          </label>

          <label>
            <input type="checkbox" id="layer-concesionado" class="toggle-checkbox" checked>
            <div class="toggle-item">
              <div class="toggle-left">
                <div class="color-pill" style="background: #a855f7;"></div>
                <span>Corredores Concesionados (Secundario)</span>
              </div>
              <div class="custom-switch"></div>
            </div>
          </label>

        </div>
      </div>

      <!-- Capas Cartográficas de Contexto -->
      <div class="sidebar-section">
        <div class="section-title">🗺️ Límites y Contexto Territorial</div>
        <div class="toggle-list">

          <label>
            <input type="checkbox" id="layer-alcaldias" class="toggle-checkbox" checked>
            <div class="toggle-item">
              <div class="toggle-left">
                <div class="color-pill" style="background: #64748b; border: 1px dashed #fff;"></div>
                <span>16 Alcaldías de la CDMX</span>
              </div>
              <div class="custom-switch"></div>
            </div>
          </label>

          <label>
            <input type="checkbox" id="layer-zmvm" class="toggle-checkbox" checked>
            <div class="toggle-item">
              <div class="toggle-left">
                <div class="color-pill" style="background: #334155; border: 1px dotted #94a3b8;"></div>
                <span>Área Metropolitana (60 Muns. Edomex/Hgo)</span>
              </div>
              <div class="custom-switch"></div>
            </div>
          </label>

        </div>
      </div>

    </div>
  </div>

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <script>
    const MAP_DATA = {data_json_str};

    // Inicializar mapa con perspectiva metropolitana completa
    const map = L.map('map', {{
      center: [19.4500, -99.1200],
      zoom: 11,
      minZoom: 9,
      maxZoom: 18,
      zoomControl: false
    }});

    L.control.zoom({{ position: 'bottomright' }}).addTo(map);

    // Tiles oscuros CartoDB Dark Matter
    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
      attribution: '&copy; OpenStreetMap &copy; CARTO',
      subdomains: 'abcd',
      maxZoom: 19
    }}).addTo(map);

    // Capas
    const layers = {{
      zmvm: L.geoJSON(null, {{
        style: {{
          color: '#475569',
          weight: 1,
          dashArray: '3, 4',
          fillColor: '#1e293b',
          fillOpacity: 0.1
        }},
        onEachFeature: (feature, layer) => {{
          const nom = feature.properties.NOMGEO || feature.properties.nomgeo || 'Municipio Metropolitano';
          layer.bindTooltip(nom + ' (Área Metropolitana)', {{ sticky: true, className: 'leaflet-tooltip-dark' }});
        }}
      }}),
      alcaldias: L.geoJSON(null, {{
        style: {{
          color: '#94a3b8',
          weight: 1.8,
          fillColor: '#334155',
          fillOpacity: 0.15
        }},
        onEachFeature: (feature, layer) => {{
          const nom = feature.properties.nomgeo || feature.properties.alcaldia || feature.properties.nombre || 'Alcaldía';
          layer.bindTooltip('Alcaldía ' + nom, {{ sticky: true, className: 'leaflet-tooltip-dark' }});
        }}
      }}),
      metro: L.featureGroup(),
      metrobus: L.featureGroup(),
      rtp: L.featureGroup(),
      cablebus: L.featureGroup(),
      trolebus: L.featureGroup(),
      tren: L.featureGroup(),
      concesionado: L.featureGroup(),
      mercados: L.featureGroup(),
      msr: L.featureGroup(),
      tianguis: L.featureGroup()
    }};

    // Añadir Área Metropolitana (Edomex e Hidalgo)
    if (MAP_DATA.zmvm) {{
      layers.zmvm.addData(MAP_DATA.zmvm);
      layers.zmvm.addTo(map);
    }}

    // Añadir Alcaldías CDMX
    if (MAP_DATA.alcaldias) {{
      layers.alcaldias.addData(MAP_DATA.alcaldias);
      layers.alcaldias.addTo(map);
    }}

    // Mapeo de transporte
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
              opacity: f.properties.opacity
            }}
          );
          
          polyline.bindPopup(`
            <div style="font-weight:700; color:${{f.properties.color}}; font-size:0.92rem; margin-bottom:3px;">
              ${{f.properties.agency_name}}
            </div>
            <div style="font-size:0.75rem; color:#cbd5e1; margin-bottom:4px;">
              Ruta: <b>${{f.properties.route_short || ''}} ${{f.properties.route_long || ''}}</b>
            </div>
            <div style="font-size:0.7rem; color:#94a3b8;">
              Destino: ${{f.properties.headsign || 'Servicio de red'}}
            </div>
          `);

          polyline.on('click', () => {{
            showTransportDetail(f.properties);
          }});

          fg.addLayer(polyline);
        }});
        fg.addTo(map);
      }}
    }});

    // Mercados Públicos
    const marketMarkers = [];
    if (MAP_DATA.mercados) {{
      MAP_DATA.mercados.forEach(m => {{
        const marker = L.circleMarker([m.lat, m.lon], {{
          radius: m.radio,
          fillColor: '#f59e0b',
          color: '#ffffff',
          weight: 1.5,
          opacity: 0.9,
          fillOpacity: 0.75
        }});

        marker.bindPopup(`
          <div style="font-weight:700; color:#f59e0b; font-size:0.95rem; margin-bottom:3px;">
            Mercado ${{m.nombre}}
          </div>
          <div style="font-size:0.75rem; color:#cbd5e1; margin-bottom:5px;">
            ${{m.alcaldia}} · ${{m.colonia}}
          </div>
          <div>
            <span style="background:#334155; color:#38bdf8; font-size:0.7rem; font-weight:600; padding:2px 6px; border-radius:4px;">
              ${{m.locales}} locales
            </span>
            <span style="background:#0f766e; color:#5eead4; font-size:0.7rem; font-weight:600; padding:2px 6px; border-radius:4px;">
              ${{m.categoria}}
            </span>
          </div>
        `);

        marker.on('click', () => {{
          showMarketDetail(m);
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
          weight: 1.5,
          opacity: 0.9,
          fillOpacity: 0.8
        }});

        marker.bindPopup(`
          <div style="font-weight:700; color:#10b981; font-size:0.95rem; margin-bottom:3px;">
            MSR: ${{m.ruta}}
          </div>
          <div style="font-size:0.75rem; color:#cbd5e1; margin-bottom:5px;">
            ${{m.alcaldia}} · ${{m.colonia}}
          </div>
          <div>
            <span style="background:#065f46; color:#a7f3d0; font-size:0.7rem; font-weight:600; padding:2px 6px; border-radius:4px;">
              Día: ${{m.dia}}
            </span>
            <span style="background:#1e40af; color:#bfdbfe; font-size:0.7rem; font-weight:600; padding:2px 6px; border-radius:4px;">
              ${{m.oferentes}} oferentes
            </span>
          </div>
        `);

        marker.on('click', () => {{
          showMSRDetail(m);
        }});

        layers.msr.addLayer(marker);
      }});
      layers.msr.addTo(map);
    }}

    // Tianguis con filtro de día
    let currentDayFilter = 'ALL';
    function renderTianguis() {{
      layers.tianguis.clearLayers();
      let count = 0;
      MAP_DATA.tianguis.forEach(t => {{
        if (currentDayFilter === 'ALL' || t.dia.includes(currentDayFilter)) {{
          count++;
          const marker = L.circleMarker([t.lat, t.lon], {{
            radius: 5,
            fillColor: '#0284c7',
            color: '#e0f2fe',
            weight: 1,
            opacity: 0.8,
            fillOpacity: 0.7
          }});

          marker.bindPopup(`
            <div style="font-weight:700; color:#38bdf8; font-size:0.92rem; margin-bottom:3px;">
              Tianguis Móvil
            </div>
            <div style="font-size:0.75rem; color:#cbd5e1; margin-bottom:3px;">
              ${{t.alcaldia}} · ${{t.colonia}}
            </div>
            <div style="font-size:0.7rem; color:#94a3b8; margin-bottom:5px;">
              📍 ${{t.ubicacion}}
            </div>
            <span style="background:#0369a1; color:#fff; font-size:0.7rem; padding:2px 6px; border-radius:4px;">
              Día: ${{t.dia}}
            </span>
            <span style="background:#334155; color:#cbd5e1; font-size:0.7rem; padding:2px 6px; border-radius:4px;">
              ⏰ ${{t.horario}}
            </span>
          `);

          marker.on('click', () => {{
            showTianguisDetail(t);
          }});

          layers.tianguis.addLayer(marker);
        }}
      }});
      layers.tianguis.addTo(map);
      document.getElementById('kpi-tianguis').innerText = count.toLocaleString();
    }}
    renderTianguis();

    // Cálculo espacial de transporte más próximo
    function findNearestTransport(lat, lon) {{
      let nearestMetro = null;
      let minMetroDist = Infinity;
      let nearestRTP = null;
      let minRTPDist = Infinity;

      if (MAP_DATA.transport['METRO']) {{
        MAP_DATA.transport['METRO'].features.forEach(f => {{
          f.geometry.coordinates.forEach(c => {{
            const d = getDistKm(lat, lon, c[1], c[0]);
            if (d < minMetroDist) {{
              minMetroDist = d;
              nearestMetro = {{
                agency: f.properties.agency_name,
                route: f.properties.route_short || f.properties.route_long,
                distMeters: Math.round(d * 1000),
                fare: '$5.00 MXN'
              }};
            }}
          }});
        }});
      }}

      if (MAP_DATA.transport['RTP']) {{
        MAP_DATA.transport['RTP'].features.forEach(f => {{
          f.geometry.coordinates.forEach(c => {{
            const d = getDistKm(lat, lon, c[1], c[0]);
            if (d < minRTPDist) {{
              minRTPDist = d;
              nearestRTP = {{
                agency: 'RTP',
                route: f.properties.route_short || f.properties.route_long,
                distMeters: Math.round(d * 1000),
                fare: '$2.00-$4.00 MXN'
              }};
            }}
          }});
        }});
      }}

      return {{ metro: nearestMetro, rtp: nearestRTP }};
    }}

    function getDistKm(lat1, lon1, lat2, lon2) {{
      const R = 6371;
      const dLat = (lat2 - lat1) * Math.PI / 180;
      const dLon = (lon2 - lon1) * Math.PI / 180;
      const a = Math.sin(dLat/2)*Math.sin(dLat/2) + Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLon/2)*Math.sin(dLon/2);
      return R * (2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)));
    }}

    // Mostrar detalle de Mercado
    function showMarketDetail(m) {{
      document.getElementById('detail-empty').style.display = 'none';
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      document.getElementById('detail-badge').className = 'detail-badge badge-mercado';
      document.getElementById('detail-badge').innerText = 'MERCADO PÚBLICO (FIJO)';
      document.getElementById('detail-name').innerText = 'Mercado ' + m.nombre;
      document.getElementById('detail-loc').innerText = m.alcaldia + ' · ' + m.colonia;
      
      document.getElementById('detail-stat1').innerText = m.locales;
      document.getElementById('detail-label1').innerText = 'Locales empadronados';
      
      document.getElementById('detail-stat2').innerText = m.superficie_m2 > 0 ? (m.superficie_m2.toLocaleString() + ' m²') : 'N/D';
      document.getElementById('detail-label2').innerText = 'Superficie de predio';

      const conn = findNearestTransport(m.lat, m.lon);
      let tText = '';
      if (conn.metro) {{
        tText += `🚇 <b>${{conn.metro.agency}} (${{conn.metro.route}})</b> a <b>${{conn.metro.distMeters}}m</b> (${{conn.metro.fare}}).<br>`;
      }}
      if (conn.rtp) {{
        tText += `🚌 <b>${{conn.rtp.agency}} (${{conn.rtp.route}})</b> a <b>${{conn.rtp.distMeters}}m</b> (${{conn.rtp.fare}}).`;
      }}
      if (!tText) {{
        tText = 'Conectado a la red de transporte barrial.';
      }}
      document.getElementById('detail-transport').innerHTML = tText;
    }}

    // Mostrar detalle de Tianguis
    function showTianguisDetail(t) {{
      document.getElementById('detail-empty').style.display = 'none';
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      document.getElementById('detail-badge').className = 'detail-badge badge-tianguis';
      document.getElementById('detail-badge').innerText = 'TIANGUIS MÓVIL EN VÍA PÚBLICA';
      document.getElementById('detail-name').innerText = 'Tianguis ' + t.colonia;
      document.getElementById('detail-loc').innerText = t.alcaldia + ' · ' + t.colonia;
      
      document.getElementById('detail-stat1').innerText = t.dia;
      document.getElementById('detail-label1').innerText = 'Día de instalación';
      
      document.getElementById('detail-stat2').innerText = t.horario;
      document.getElementById('detail-label2').innerText = 'Horario de operación';

      const conn = findNearestTransport(t.lat, t.lon);
      document.getElementById('detail-transport').innerHTML = `
        <b>Vía ocupada/cerrada:</b> <i>${{t.ubicacion}}</i><br>
        ${{conn.metro ? `🚇 ${{conn.metro.agency}} a ${{conn.metro.distMeters}}m.` : ''}}
        ${{conn.rtp ? `🚌 RTP a ${{conn.rtp.distMeters}}m.` : ''}}
      `;
    }}

    // Mostrar detalle de Mercado Sobre Ruedas
    function showMSRDetail(m) {{
      document.getElementById('detail-empty').style.display = 'none';
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      document.getElementById('detail-badge').className = 'detail-badge';
      document.getElementById('detail-badge').style.background = '#10b981';
      document.getElementById('detail-badge').innerText = 'MERCADO SOBRE RUEDAS (' + m.ruta + ')';
      document.getElementById('detail-name').innerText = m.ruta + ' · ' + m.colonia;
      document.getElementById('detail-loc').innerText = m.alcaldia + ' · ' + m.direccion;
      
      document.getElementById('detail-stat1').innerText = m.dia;
      document.getElementById('detail-label1').innerText = 'Día en esta locación';
      
      document.getElementById('detail-stat2').innerText = m.oferentes;
      document.getElementById('detail-label2').innerText = 'Oferentes empadronados';

      document.getElementById('detail-transport').innerHTML = `
        <b>Ruta itinerante:</b> Se traslada de colonia a lo largo de la semana.<br>
        <span style="color:#6ee7b7;">Sigue a esta ruta para tus compras semanales.</span>
      `;
    }}

    // Detalle de ruta de transporte
    function showTransportDetail(p) {{
      document.getElementById('detail-empty').style.display = 'none';
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      document.getElementById('detail-badge').className = 'detail-badge';
      document.getElementById('detail-badge').style.background = p.color;
      document.getElementById('detail-badge').innerText = p.agency_name;
      document.getElementById('detail-name').innerText = p.route_short + ' ' + (p.route_long || '');
      document.getElementById('detail-loc').innerText = 'Destino: ' + (p.headsign || 'Servicio de red');

      document.getElementById('detail-stat1').innerText = p.agency === 'METRO' ? '$5.00' : (p.agency === 'MB' ? '$6.00' : '$2.00-$4.00');
      document.getElementById('detail-label1').innerText = 'Tarifa unitaria';

      document.getElementById('detail-stat2').innerText = 'MI Tarjeta';
      document.getElementById('detail-label2').innerText = 'Sistema integrado';

      document.getElementById('detail-transport').innerHTML = `
        Corredor clave de movilidad que conecta áreas residenciales periféricas con centros de abasto y tianguis.
      `;
    }}

    // Toggles de Capas
    const toggleBindings = [
      ['layer-mercados', layers.mercados],
      ['layer-tianguis', layers.tianguis],
      ['layer-msr', layers.msr],
      ['layer-metro', layers.metro],
      ['layer-metrobus', layers.metrobus],
      ['layer-rtp', layers.rtp],
      ['layer-cablebus', layers.cablebus],
      ['layer-trolebus', layers.trolebus],
      ['layer-tren', layers.tren],
      ['layer-concesionado', layers.concesionado],
      ['layer-alcaldias', layers.alcaldias],
      ['layer-zmvm', layers.zmvm]
    ];

    toggleBindings.forEach(([chkId, layerGroup]) => {{
      const chk = document.getElementById(chkId);
      if (chk) {{
        chk.addEventListener('change', (e) => {{
          if (e.target.checked) {{
            map.addLayer(layerGroup);
          }} else {{
            map.removeLayer(layerGroup);
          }}
        }});
      }}
    }});

    // Filtro por Día
    const dayButtons = document.querySelectorAll('.day-btn');
    dayButtons.forEach(btn => {{
      btn.addEventListener('click', () => {{
        dayButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentDayFilter = btn.getAttribute('data-day');
        renderTianguis();
      }});
    }});

    // Buscador
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
        showMarketDetail(found.marketData);
      }}
    }});
  </script>
</body>
</html>
'''

    output_path = 'mapa_comercio_movilidad_cdmx.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML generado exitosamente en: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == '__main__':
    generate_html()
