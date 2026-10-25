import json
import base64
import os

def generate():
    print("Incrustando fuentes de iconografía y compilando HTML final...")
    with open('data/processed/map_bundle.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Cargar y codificar Woff en Base64
    with open('assets/fonts/estaciones.woff', 'rb') as f:
        woff_b64 = base64.b64encode(f.read()).decode('utf-8')

    # Cargar clases CSS de estaciones
    with open('assets/css/ui-transport-mx.css', 'r', encoding='utf-8') as f:
        css_icons = f.read()

    # Reemplazar la declaración font-face original por Base64
    font_face_inline = f"""
    @font-face {{
      font-family: 'estaciones';
      src: url('data:font/woff;base64,{woff_b64}') format('woff');
      font-weight: normal;
      font-style: normal;
    }}
    em[class^="estacion-"], em[class*=" estacion-"] {{
      color: #ffffff !important;
      font-size: 14px;
      font-family: 'estaciones' !important;
      font-style: normal;
      font-weight: normal;
      line-height: 1;
      display: inline-block;
    }}
    """

    data_json_str = json.dumps(data, ensure_ascii=False)

    html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Movilidad y Comercio CDMX · App CDMX Style</title>
  
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <!-- Google Fonts: Montserrat -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    {font_face_inline}

    :root {{
      --cdmx-green-dark: #0f5953;
      --cdmx-green-primary: #116962;
      --cdmx-green-light: #e8f5f4;
      --cdmx-green-chip: #d0eae7;
      --cdmx-bg: #f5fbfb;
      --cdmx-text-dark: #092c29;
      --cdmx-text-muted: #527370;
      --cdmx-border: #d4e7e5;
      --cdmx-card-shadow: 0 4px 20px rgba(15, 89, 83, 0.08);
      --cdmx-fab-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
      --font-main: 'Montserrat', sans-serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}

    body {{
      font-family: var(--font-main);
      background: var(--cdmx-bg);
      color: var(--cdmx-text-dark);
      height: 100vh;
      width: 100vw;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}

    #map-container {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
    }}

    #map {{
      width: 100%;
      height: 100%;
      background: #eef3f3;
    }}

    /* Botón flotante superior izquierda */
    .top-bar-controls {{
      position: absolute;
      top: 18px;
      left: 18px;
      z-index: 1000;
      display: flex;
      gap: 10px;
      align-items: center;
    }}

    .fab-btn {{
      width: 44px;
      height: 44px;
      background: #ffffff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--cdmx-fab-shadow);
      border: 1px solid rgba(0,0,0,0.06);
      cursor: pointer;
      transition: all 0.2s ease;
      color: #334155;
    }}

    .fab-btn:hover {{
      transform: scale(1.05);
    }}

    .fab-btn svg {{
      width: 20px;
      height: 20px;
      fill: #1e293b;
    }}

    .header-pill-tag {{
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(8px);
      padding: 8px 16px;
      border-radius: 24px;
      box-shadow: var(--cdmx-fab-shadow);
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--cdmx-green-dark);
      display: flex;
      align-items: center;
      gap: 8px;
      border: 1px solid var(--cdmx-border);
    }}

    /* Botones flotantes laterales derecha */
    .floating-right-actions {{
      position: absolute;
      right: 18px;
      bottom: 230px;
      z-index: 1000;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .fab-action {{
      width: 46px;
      height: 46px;
      background: #ffffff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--cdmx-fab-shadow);
      border: 1px solid rgba(0,0,0,0.06);
      cursor: pointer;
      transition: all 0.2s;
    }}

    .fab-action:hover {{
      transform: scale(1.06);
    }}

    .fab-action svg {{
      width: 22px;
      height: 22px;
    }}

    /* Botón flotante ovalado "Buscar en esta zona" */
    .floating-search-zone-btn {{
      position: absolute;
      bottom: 230px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
      background: var(--cdmx-green-dark);
      color: #ffffff;
      padding: 11px 22px;
      border-radius: 26px;
      font-size: 0.85rem;
      font-weight: 700;
      box-shadow: 0 6px 18px rgba(15, 89, 83, 0.35);
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
    }}

    .floating-search-zone-btn:hover {{
      background: #0b433e;
      transform: translateX(-50%) scale(1.03);
    }}

    /* Bottom Sheet Deslizante */
    #bottom-sheet {{
      position: absolute;
      bottom: 60px;
      left: 0;
      width: 100%;
      background: #ffffff;
      border-radius: 26px 26px 0 0;
      box-shadow: 0 -8px 30px rgba(15, 89, 83, 0.12);
      z-index: 1001;
      max-height: 72vh;
      display: flex;
      flex-direction: column;
      transition: max-height 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      border-top: 1px solid var(--cdmx-border);
    }}

    .sheet-handle {{
      width: 44px;
      height: 4px;
      background: #cbd5e1;
      border-radius: 2px;
      margin: 10px auto 6px auto;
      cursor: pointer;
    }}

    .sheet-content {{
      padding: 4px 20px 18px 20px;
      overflow-y: auto;
    }}

    .sheet-title {{
      font-size: 1.12rem;
      font-weight: 700;
      color: var(--cdmx-text-dark);
      text-align: center;
      margin-bottom: 12px;
    }}

    .filter-section-label {{
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--cdmx-text-dark);
      margin-bottom: 8px;
    }}

    .chips-row {{
      display: flex;
      gap: 8px;
      align-items: center;
      margin-bottom: 14px;
      overflow-x: auto;
      padding-bottom: 4px;
      scrollbar-width: none;
    }}

    .chips-row::-webkit-scrollbar {{
      display: none;
    }}

    .btn-dropdown-transport {{
      background: var(--cdmx-green-dark);
      color: #ffffff;
      border: none;
      padding: 9px 15px;
      border-radius: 10px;
      font-size: 0.83rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 7px;
      cursor: pointer;
      flex-shrink: 0;
    }}

    .btn-dropdown-transport svg {{
      width: 14px;
      height: 14px;
      fill: #ffffff;
    }}

    .pill-chip {{
      background: #ffffff;
      border: 1px solid #cbdad7;
      color: var(--cdmx-text-dark);
      padding: 8px 13px;
      border-radius: 10px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      flex-shrink: 0;
      transition: all 0.2s;
      white-space: nowrap;
    }}

    .pill-chip:hover, .pill-chip.active {{
      background: var(--cdmx-green-light);
      border-color: var(--cdmx-green-dark);
      color: var(--cdmx-green-dark);
    }}

    #transport-dropdown-menu {{
      background: #ffffff;
      border: 1px solid var(--cdmx-border);
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
      padding: 8px;
      display: none;
      position: absolute;
      top: 92px;
      left: 20px;
      z-index: 1050;
      width: 220px;
    }}

    .transport-option {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 8px 10px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.83rem;
      font-weight: 600;
      color: var(--cdmx-text-dark);
      transition: background 0.15s;
    }}

    .transport-option:hover {{
      background: var(--cdmx-green-light);
    }}

    .transport-badge-icon {{
      width: 26px;
      height: 26px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-weight: 800;
      font-size: 0.72rem;
    }}

    .sheet-divider {{
      height: 1px;
      background: #e2eceb;
      margin: 10px 0 14px 0;
    }}

    /* Sección Ir a */
    .goto-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      text-align: center;
    }}

    .goto-item {{
      display: flex;
      flex-direction: column;
      align-items: center;
      cursor: pointer;
      text-decoration: none;
    }}

    .goto-circle {{
      width: 52px;
      height: 52px;
      border-radius: 50%;
      background: var(--cdmx-green-dark);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 7px;
      box-shadow: 0 4px 10px rgba(15, 89, 83, 0.2);
      transition: transform 0.2s;
    }}

    .goto-item:hover .goto-circle {{
      transform: translateY(-2px);
      background: var(--cdmx-green-primary);
    }}

    .goto-circle svg {{
      width: 24px;
      height: 24px;
      fill: #ffffff;
    }}

    .goto-text {{
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--cdmx-text-dark);
      line-height: 1.2;
    }}

    /* Ficha de Detalle */
    #detail-card-panel {{
      display: none;
      background: var(--cdmx-green-light);
      border: 1px solid var(--cdmx-border);
      border-radius: 16px;
      padding: 14px;
      margin-bottom: 14px;
      animation: fadeIn 0.25s ease;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .detail-card-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 4px;
    }}

    .detail-tag {{
      display: inline-block;
      font-size: 0.65rem;
      font-weight: 800;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 6px;
      color: #fff;
    }}

    .detail-title {{
      font-size: 1.1rem;
      font-weight: 800;
      color: var(--cdmx-green-dark);
      margin-top: 3px;
    }}

    .detail-subtitle {{
      font-size: 0.78rem;
      color: var(--cdmx-text-muted);
      margin-bottom: 10px;
    }}

    .detail-stats-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 10px;
    }}

    .detail-stat-box {{
      background: #ffffff;
      padding: 8px;
      border-radius: 8px;
      border: 1px solid #dbeae8;
    }}

    .detail-stat-val {{
      font-size: 1rem;
      font-weight: 800;
      color: var(--cdmx-green-dark);
    }}

    .detail-stat-lbl {{
      font-size: 0.62rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--cdmx-text-muted);
    }}

    .detail-rtponky-btn {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      background: #15803d;
      color: #ffffff;
      text-decoration: none;
      padding: 9px 12px;
      border-radius: 10px;
      font-size: 0.78rem;
      font-weight: 700;
      transition: background 0.2s;
    }}

    /* Barra de Navegación Inferior (Limpia: solo Movilidad y Comercio) */
    #bottom-navbar {{
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 60px;
      background: #093733;
      background-image: radial-gradient(circle at 50% 120%, #115952 0%, #08332f 100%);
      display: flex;
      justify-content: space-around;
      align-items: center;
      z-index: 1002;
      border-top: 1px solid rgba(255,255,255,0.1);
    }}

    .nav-tab {{
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      color: #93b5b1;
      font-size: 0.8rem;
      font-weight: 700;
      padding: 8px 24px;
      border-radius: 20px;
      transition: all 0.2s;
    }}

    .nav-tab svg {{
      width: 22px;
      height: 22px;
      fill: #93b5b1;
    }}

    .nav-tab.active {{
      color: #ffffff;
      background: rgba(255, 255, 255, 0.16);
    }}

    .nav-tab.active svg {{
      fill: #ffffff;
    }}

    /* Marcadores con Íconos Oficiales de Estación (Metro y Metrobús) */
    .metro-station-icon-badge {{
      width: 22px;
      height: 22px;
      border-radius: 5px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 6px rgba(0,0,0,0.35);
      border: 1px solid rgba(255,255,255,0.9);
      cursor: pointer;
      transition: transform 0.15s ease;
    }}

    .metro-station-icon-badge:hover {{
      transform: scale(1.35);
      z-index: 9999 !important;
    }}

    .metrobus-icon-badge {{
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
      box-shadow: 0 2px 5px rgba(0,0,0,0.3);
      border: 1px solid #ffffff;
      cursor: pointer;
      transition: transform 0.15s ease;
    }}

    .metrobus-icon-badge:hover {{
      transform: scale(1.35);
      z-index: 9999 !important;
    }}

    /* Popups */
    .leaflet-popup-content-wrapper {{
      border-radius: 14px;
      font-family: var(--font-main);
      box-shadow: 0 6px 20px rgba(15, 89, 83, 0.15);
      border: 1px solid var(--cdmx-border);
      padding: 3px;
    }}

    .popup-cdmx-title {{
      font-size: 0.92rem;
      font-weight: 800;
      color: var(--cdmx-green-dark);
      margin-bottom: 2px;
    }}

    .popup-cdmx-sub {{
      font-size: 0.74rem;
      color: var(--cdmx-text-muted);
      margin-bottom: 5px;
    }}

    .popup-badge {{
      display: inline-block;
      font-size: 0.67rem;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 5px;
      background: var(--cdmx-green-chip);
      color: var(--cdmx-green-dark);
    }}
  </style>
</head>
<body>

  <!-- Mapa Fullscreen -->
  <div id="map-container">
    <div id="map"></div>
  </div>

  <!-- Controles Superiores Flotantes -->
  <div class="top-bar-controls">
    <button class="fab-btn" onclick="resetMapView()" title="Centrar CDMX y Zona Metropolitana">
      <svg viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
    </button>
    <div class="header-pill-tag">
      <span>🇲🇽</span>
      <span>Movilidad y Comercio CDMX</span>
    </div>
  </div>

  <!-- Botones de Acción Flotantes (Derecha) -->
  <div class="floating-right-actions">
    <!-- Botón Mi Ubicación -->
    <button class="fab-action" onclick="locateUser()" title="Mi ubicación">
      <svg viewBox="0 0 24 24" fill="#0d9488"><path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/></svg>
    </button>
    
    <!-- Botón Logo Movilidad Integrada (MI) -->
    <button class="fab-action" onclick="toggleMIPanel()" title="Movilidad Integrada">
      <svg viewBox="0 0 24 24" fill="#0f5953"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 14h-2v-2h2v2zm0-4h-2V7h2v5z"/></svg>
    </button>
    
    <!-- Botón Selector de Capas -->
    <button class="fab-action" onclick="toggleLayerDialog()" title="Alternar Mapa Base">
      <svg viewBox="0 0 24 24" fill="#0284c7"><path d="M11.99 18.54l-7.37-5.73L3 14.07l9 7 9-7-1.63-1.27-7.38 5.74zM12 16l7.36-5.73L21 9.07l-9-7-9 7 1.63 1.2L12 16z"/></svg>
    </button>
  </div>

  <!-- Botón Flotante "Buscar en esta zona" -->
  <button class="floating-search-zone-btn" id="btn-search-zone" onclick="searchZone()">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="#ffffff"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
    <span>Buscar mercados y tianguis aquí</span>
  </button>

  <!-- Bottom Sheet Deslizante ("Elige tus medios de transporte") -->
  <div id="bottom-sheet">
    <div class="sheet-handle" onclick="toggleBottomSheet()"></div>
    
    <div class="sheet-content">
      <div class="sheet-title">Elige tus medios de transporte y comercio</div>

      <!-- Ficha de Detalle Dinámica -->
      <div id="detail-card-panel">
        <div class="detail-card-header">
          <span class="detail-tag" id="panel-tag" style="background: var(--cdmx-green-dark);">MERCADO PÚBLICO</span>
          <button style="border:none; background:transparent; cursor:pointer; font-size:1.1rem; color:#64748b;" onclick="closeDetailPanel()">✕</button>
        </div>
        <div class="detail-title" id="panel-name">Mercado</div>
        <div class="detail-subtitle" id="panel-sub">Alcaldía · Colonia</div>
        
        <div class="detail-stats-row">
          <div class="detail-stat-box">
            <div class="detail-stat-val" id="panel-stat1">--</div>
            <div class="detail-stat-lbl" id="panel-lbl1">Locales</div>
          </div>
          <div class="detail-stat-box">
            <div class="detail-stat-val" id="panel-stat2">--</div>
            <div class="detail-stat-lbl" id="panel-lbl2">Superficie</div>
          </div>
        </div>

        <div style="background:#ffffff; padding:9px; border-radius:10px; border:1px solid #dbeae8; margin-bottom:10px; font-size:0.77rem;">
          <div style="font-weight:700; color:var(--cdmx-green-dark); margin-bottom:2px;">🚌 Conexión de Movilidad Integrada:</div>
          <div id="panel-conn" style="color:#334155;">Cargando estación o corredor cercano...</div>
        </div>

        <a href="https://rtponky.lat/" target="_blank" class="detail-rtponky-btn" id="panel-rtponky-btn">
          <span>🚌</span>
          <span>Ver aproximación en vivo en RTPonky ↗</span>
        </a>
      </div>

      <!-- Filtra por -->
      <div class="filter-section-label">Filtra por</div>
      <div class="chips-row">
        
        <!-- Botón Desplegable Transporte (como en la captura de referencia) -->
        <button class="btn-dropdown-transport" onclick="toggleTransportDropdown()">
          <span>Transporte</span>
          <svg viewBox="0 0 24 24"><path d="M7 10l5 5 5-5z"/></svg>
        </button>

        <!-- Chips de Comercio y Modos -->
        <button class="pill-chip active" id="chip-iconos-metro" onclick="toggleLayer('metro_icons')">Íconos Estaciones</button>
        <button class="pill-chip active" id="chip-mercados" onclick="toggleLayer('mercados')">Mercados (Fijos)</button>
        <button class="pill-chip active" id="chip-tianguis" onclick="toggleLayer('tianguis')">Tianguis (Móviles)</button>
        <button class="pill-chip active" id="chip-concesionado" onclick="toggleLayer('concesionado')">Rutas Secundarias</button>
        <button class="pill-chip active" id="chip-msr" onclick="toggleLayer('msr')">Rutas MSR</button>
        <button class="pill-chip" id="chip-dia-hoy" onclick="filterByToday()">Abrir Hoy</button>
      </div>

      <!-- Menú Desplegable Flotante de Transportes -->
      <div id="transport-dropdown-menu">
        <div class="transport-option" onclick="toggleSubsystem('METRO')">
          <div class="transport-badge-icon" style="background: #ef4444;">M</div>
          <span>Metro (STC)</span>
        </div>
        <div class="transport-option" onclick="toggleSubsystem('MB')">
          <div class="transport-badge-icon" style="background: #ec4899;">MB</div>
          <span>Metrobús</span>
        </div>
        <div class="transport-option" onclick="toggleSubsystem('TROLE')">
          <div class="transport-badge-icon" style="background: #10b981;">TE</div>
          <span>T eléctrico</span>
        </div>
        <div class="transport-option" onclick="toggleSubsystem('CBB')">
          <div class="transport-badge-icon" style="background: #06b6d4;">CB</div>
          <span>Cablebús</span>
        </div>
        <div class="transport-option" onclick="toggleSubsystem('RTP')">
          <div class="transport-badge-icon" style="background: #15803d;">RTP</div>
          <span>RTP Pasajeros</span>
        </div>
        <div class="transport-option" onclick="toggleSubsystem('TL')">
          <div class="transport-badge-icon" style="background: #3b82f6;">TL</div>
          <span>Tren Ligero</span>
        </div>
        <div class="transport-option" onclick="toggleSubsystem('CC')">
          <div class="transport-badge-icon" style="background: #8e24aa;">CC</div>
          <span>Rutas Secundarias</span>
        </div>
      </div>

      <div class="sheet-divider"></div>

      <!-- Sección "Ir a" (Exacta como en la captura) -->
      <div class="section-goto">
        <div class="goto-label">Ir a</div>
        <div class="goto-grid">
          
          <div class="goto-item" onclick="showStreetClosures()">
            <div class="goto-circle">
              <svg viewBox="0 0 24 24"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>
            </div>
            <div class="goto-text">Cierres de Vías</div>
          </div>

          <div class="goto-item" onclick="showHoursModal()">
            <div class="goto-circle">
              <svg viewBox="0 0 24 24"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/></svg>
            </div>
            <div class="goto-text">Horarios</div>
          </div>

          <div class="goto-item" onclick="showRoutesModal()">
            <div class="goto-circle">
              <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
            </div>
            <div class="goto-text">Rutas Secundarias</div>
          </div>

          <a href="https://rtponky.lat/" target="_blank" class="goto-item">
            <div class="goto-circle" style="background: #15803d;">
              <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 14h-2v-2h2v2zm0-4h-2V7h2v5z"/></svg>
            </div>
            <div class="goto-text">RTPonky en vivo</div>
          </a>

        </div>
      </div>

    </div>
  </div>

  <!-- Barra de Navegación Inferior (Limpia: solo los dos ejes del proyecto) -->
  <nav id="bottom-navbar">
    <div class="nav-tab active" onclick="activateNavTab(this, 'movilidad')">
      <svg viewBox="0 0 24 24"><path d="M12 2c-4.42 0-8 .5-8 4v10c0 .88.39 1.67 1 2.22V20c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h8v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1.78c.61-.55 1-1.34 1-2.22V6c0-3.5-3.58-4-8-4zm0 2c3.5 0 6 .4 6 2H6c0-1.6 2.5-2 6-2zm6 12H6V8h12v8zm-9.5-3c.83 0 1.5-.67 1.5-1.5S9.33 10 8.5 10 7 10.67 7 11.5 7.67 13 8.5 13zm7 0c.83 0 1.5-.67 1.5-1.5s-.67-1.5-1.5-1.5-1.5.67-1.5 1.5.67 1.5 1.5 1.5z"/></svg>
      <span>Movilidad CDMX</span>
    </div>
    <div class="nav-tab" onclick="activateNavTab(this, 'comercio')">
      <svg viewBox="0 0 24 24"><path d="M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2z"/></svg>
      <span>Comercio Popular (329 Mercados / 1,367 Tianguis)</span>
    </div>
  </nav>

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <script>
    const MAP_DATA = {data_json_str};

    // Inicializar mapa
    const map = L.map('map', {{
      center: [19.4326, -99.1332],
      zoom: 12,
      minZoom: 9,
      maxZoom: 18,
      zoomControl: false
    }});

    // MAPA BASE LIMPIO SIN MARCAS DE AGUA (Esri World Light Gray)
    const baseTileLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
      attribution: 'Esri, HERE, Garmin, &copy; OpenStreetMap contributors',
      maxZoom: 18
    }}).addTo(map);

    // Grupos de capas
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
      tianguis: L.featureGroup()
    }};

    if (MAP_DATA.zmvm) {{
      layers.zmvm.addData(MAP_DATA.zmvm);
      layers.zmvm.addTo(map);
    }}
    if (MAP_DATA.alcaldias) {{
      layers.alcaldias.addData(MAP_DATA.alcaldias);
      layers.alcaldias.addTo(map);
    }}

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
            <div class="popup-cdmx-title" style="color:${{f.properties.color}}">${{f.properties.agency_name}}</div>
            <div class="popup-cdmx-sub">Ruta: <b>${{f.properties.route_short || ''}} ${{f.properties.route_long || ''}}</b></div>
            <span class="popup-badge">Destino: ${{f.properties.headsign || 'Servicio Concesionado/Red'}}</span>
          `);

          polyline.on('click', () => {{
            showTransportInPanel(f.properties);
          }});

          fg.addLayer(polyline);
        }});
        fg.addTo(map);
      }}
    }});

    // RENDERIZAR ÍCONOS OFICIALES DE ESTACIONES DEL METRO
    if (MAP_DATA.metro_stations) {{
      MAP_DATA.metro_stations.forEach(st => {{
        const iconHtml = `
          <div class="metro-station-icon-badge" style="background:${{st.color}};" title="${{st.nombre}} (Línea ${{st.linea}})">
            <em class="${{st.icon_class}}"></em>
          </div>
        `;
        const customIcon = L.divIcon({{
          className: 'custom-metro-icon',
          html: iconHtml,
          iconSize: [22, 22],
          iconAnchor: [11, 11]
        }});

        const marker = L.marker([st.lat, st.lon], {{ icon: customIcon }});
        marker.bindPopup(`
          <div class="popup-cdmx-title" style="color:${{st.color}}">Metro ${{st.nombre}}</div>
          <div class="popup-cdmx-sub">Línea ${{st.linea}} · ${{st.tipo}}</div>
          <div style="font-size:0.75rem; color:#475569; margin-bottom:4px;">Alcaldía: ${{st.alcaldia}}</div>
          <span class="popup-badge" style="background:#fee2e2; color:#991b1b;">Tarifa: $5.00 MXN</span>
        `);

        marker.on('click', () => {{
          showMetroStationInPanel(st);
        }});

        layers.metro_icons.addLayer(marker);
      }});
      layers.metro_icons.addTo(map);
    }}

    // RENDERIZAR ÍCONOS DE ESTACIONES METROBÚS
    if (MAP_DATA.metrobus_stations) {{
      MAP_DATA.metrobus_stations.forEach(st => {{
        const iconHtml = `<div class="metrobus-icon-badge" title="${{st.nombre}} (${{st.linea}})">MB</div>`;
        const customIcon = L.divIcon({{
          className: 'custom-mb-icon',
          html: iconHtml,
          iconSize: [20, 20],
          iconAnchor: [10, 10]
        }});

        const marker = L.marker([st.lat, st.lon], {{ icon: customIcon }});
        marker.bindPopup(`
          <div class="popup-cdmx-title" style="color:#d81b60">Metrobús ${{st.nombre}}</div>
          <div class="popup-cdmx-sub">${{st.linea}} · ${{st.alcaldia}}</div>
          <span class="popup-badge" style="background:#fce7f3; color:#9d174d;">Tarifa: $6.00 MXN</span>
        `);

        layers.metrobus_icons.addLayer(marker);
      }});
      layers.metrobus_icons.addTo(map);
    }}

    // Mercados Públicos
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
          <div class="popup-cdmx-title">Mercado ${{m.nombre}}</div>
          <div class="popup-cdmx-sub">${{m.alcaldia}} · ${{m.colonia}}</div>
          <div style="margin-top:4px;">
            <span class="popup-badge" style="background:#fef3c7; color:#92400e;">${{m.locales}} locales</span>
            <span class="popup-badge" style="background:#e0f2fe; color:#0369a1;">${{m.categoria}}</span>
          </div>
        `);

        marker.on('click', () => {{
          showMarketInPanel(m);
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
          <div class="popup-cdmx-title">MSR: ${{m.ruta}}</div>
          <div class="popup-cdmx-sub">${{m.alcaldia}} · ${{m.colonia}}</div>
          <div style="margin-top:4px;">
            <span class="popup-badge" style="background:#d1fae5; color:#065f46;">Día: ${{m.dia}}</span>
            <span class="popup-badge" style="background:#dbeafe; color:#1e40af;">${{m.oferentes}} oferentes</span>
          </div>
        `);

        marker.on('click', () => {{
          showMSRInPanel(m);
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
            <div class="popup-cdmx-title">Tianguis Móvil</div>
            <div class="popup-cdmx-sub">${{t.alcaldia}} · ${{t.colonia}}</div>
            <div style="font-size:0.72rem; color:#475569; margin-bottom:5px;">📍 ${{t.ubicacion}}</div>
            <span class="popup-badge" style="background:#ccfbf1; color:#0f766e;">${{t.dia}}</span>
            <span class="popup-badge">${{t.horario}}</span>
          `);

          marker.on('click', () => {{
            showTianguisInPanel(t);
          }});

          layers.tianguis.addLayer(marker);
        }}
      }});
      layers.tianguis.addTo(map);
    }}
    renderTianguisMarkers();

    // Detalle de Estación Metro
    function showMetroStationInPanel(st) {{
      const p = document.getElementById('detail-card-panel');
      p.style.display = 'block';

      document.getElementById('panel-tag').innerText = 'ESTACIÓN METRO CDMX';
      document.getElementById('panel-tag').style.background = st.color;
      document.getElementById('panel-name').innerText = 'Estación ' + st.nombre;
      document.getElementById('panel-sub').innerText = 'Línea ' + st.linea + ' · Alcaldía ' + st.alcaldia;

      document.getElementById('panel-stat1').innerText = '$5.00 MXN';
      document.getElementById('panel-lbl1').innerText = 'Tarifa Oficial';

      document.getElementById('panel-stat2').innerText = st.tipo;
      document.getElementById('panel-lbl2').innerText = 'Tipo de Estación';

      document.getElementById('panel-conn').innerHTML = `
        🚇 Estación nodal que conecta con tianguis y centros de abasto barriales cercanos.
      `;

      expandBottomSheet();
    }}

    function showMarketInPanel(m) {{
      const p = document.getElementById('detail-card-panel');
      p.style.display = 'block';
      
      document.getElementById('panel-tag').innerText = 'MERCADO PÚBLICO';
      document.getElementById('panel-tag').style.background = '#d97706';
      document.getElementById('panel-name').innerText = 'Mercado ' + m.nombre;
      document.getElementById('panel-sub').innerText = m.alcaldia + ' · ' + m.colonia;
      
      document.getElementById('panel-stat1').innerText = m.locales;
      document.getElementById('panel-lbl1').innerText = 'Locales';
      
      document.getElementById('panel-stat2').innerText = m.superficie_m2 > 0 ? (m.superficie_m2.toLocaleString() + ' m²') : 'N/D';
      document.getElementById('panel-lbl2').innerText = 'Superficie';

      document.getElementById('panel-conn').innerHTML = `
        🚇 Conexión a red de transporte primario y secundario.<br>
        <span style="color:#0f5953; font-weight:700;">Tarifa MI: $5.00 Metro / $6.00 MB / $2.00-$4.00 RTP.</span>
      `;

      expandBottomSheet();
    }}

    function showTianguisInPanel(t) {{
      const p = document.getElementById('detail-card-panel');
      p.style.display = 'block';
      
      document.getElementById('panel-tag').innerText = 'TIANGUIS MÓVIL';
      document.getElementById('panel-tag').style.background = '#0f5953';
      document.getElementById('panel-name').innerText = 'Tianguis ' + t.colonia;
      document.getElementById('panel-sub').innerText = t.alcaldia + ' · ' + t.colonia;
      
      document.getElementById('panel-stat1').innerText = t.dia;
      document.getElementById('panel-lbl1').innerText = 'Día';
      
      document.getElementById('panel-stat2').innerText = t.horario;
      document.getElementById('panel-lbl2').innerText = 'Horario';

      document.getElementById('panel-conn').innerHTML = `
        <b>Vía ocupada/cerrada:</b> <i>${{t.ubicacion}}</i>
      `;

      expandBottomSheet();
    }}

    function showMSRInPanel(m) {{
      const p = document.getElementById('detail-card-panel');
      p.style.display = 'block';
      
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

      expandBottomSheet();
    }}

    function showTransportInPanel(p) {{
      const panel = document.getElementById('detail-card-panel');
      panel.style.display = 'block';

      document.getElementById('panel-tag').innerText = p.agency_name;
      document.getElementById('panel-tag').style.background = p.color;
      document.getElementById('panel-name').innerText = (p.route_short || '') + ' ' + (p.route_long || '');
      document.getElementById('panel-sub').innerText = 'Destino: ' + (p.headsign || 'Servicio Concesionado/Red');

      document.getElementById('panel-stat1').innerText = p.agency === 'METRO' ? '$5.00' : (p.agency === 'MB' ? '$6.00' : (p.agency === 'CC' ? 'Por distancia' : '$2.00-$4.00'));
      document.getElementById('panel-lbl1').innerText = 'Tarifa';

      document.getElementById('panel-stat2').innerText = p.agency === 'CC' ? 'Efectivo / Mi' : 'Tarjeta MI';
      document.getElementById('panel-lbl2').innerText = 'Pago';

      document.getElementById('panel-conn').innerHTML = `
        <b>Corredor / Ruta:</b> Conecta con mercados y tianguis barriales.
      `;

      expandBottomSheet();
    }}

    function closeDetailPanel() {{
      document.getElementById('detail-card-panel').style.display = 'none';
    }}

    function expandBottomSheet() {{
      const sheet = document.getElementById('bottom-sheet');
      sheet.style.maxHeight = '78vh';
    }}

    function toggleBottomSheet() {{
      const sheet = document.getElementById('bottom-sheet');
      if (sheet.style.maxHeight === '78vh') {{
        sheet.style.maxHeight = '230px';
      }} else {{
        sheet.style.maxHeight = '78vh';
      }}
    }}

    function resetMapView() {{
      map.setView([19.4326, -99.1332], 12);
    }}

    function locateUser() {{
      map.locate({{ setView: true, maxZoom: 15 }});
    }}

    function toggleTransportDropdown() {{
      const menu = document.getElementById('transport-dropdown-menu');
      menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    }}

    document.addEventListener('click', (e) => {{
      const menu = document.getElementById('transport-dropdown-menu');
      const btn = document.querySelector('.btn-dropdown-transport');
      if (menu && btn && !menu.contains(e.target) && !btn.contains(e.target)) {{
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

    function searchZone() {{
      const center = map.getCenter();
      let nearest = null;
      let minD = Infinity;
      marketMarkers.forEach(m => {{
        const d = center.distanceTo([m.marketData.lat, m.marketData.lon]);
        if (d < minD) {{
          minD = d;
          nearest = m;
        }}
      }});
      if (nearest) {{
        map.setView([nearest.marketData.lat, nearest.marketData.lon], 15);
        nearest.openPopup();
        showMarketInPanel(nearest.marketData);
      }}
    }}

    function activateNavTab(el, type) {{
      document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
      el.classList.add('active');
      if (type === 'comercio') {{
        map.setView([19.4326, -99.1332], 12);
        expandBottomSheet();
      }}
    }}

    function showStreetClosures() {{
      alert('Aviso de Cierres Viales: 1,367 tianguis generan cortes y reducciones viales en días programados. Toca cualquier tianguis para ver la calle exacta ocupada.');
    }}

    function showHoursModal() {{
      alert('Horarios Oficiales: Metro 05:00 a 24:00 (L-V), 06:00 a 24:00 (Sáb), 07:00 a 24:00 (Dom). Mercados públicos: 08:00 a 18:00 hrs.');
    }}

    function showRoutesModal() {{
      alert('Rutas Secundarias Concesionadas: 331 ramales de microbuses y corredores que penetran en colonias conectando con tianguis y mercados.');
    }}

    function toggleLayerDialog() {{
      if (map.hasLayer(baseTileLayer)) {{
        map.removeLayer(baseTileLayer);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{ maxZoom: 19 }}).addTo(map);
      }} else {{
        baseTileLayer.addTo(map);
      }}
    }}
  </script>
</body>
</html>
'''

    output_path = 'mapa_comercio_movilidad_cdmx.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML final generado exitosamente: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == '__main__':
    generate()
