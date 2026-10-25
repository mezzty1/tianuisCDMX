import os
import json

# Read data/processed/cierres_viales_por_dia.json if available to get exact numbers
cierres_stats = {}
try:
    with open('data/processed/cierres_viales_por_dia.json', 'r', encoding='utf-8') as f:
        cierres_data = json.load(f)
        cierres_stats = cierres_data.get('resumen_semanal', {})
except Exception as e:
    print("Notice: cierres_viales_por_dia.json error", e)

# Read base HTML to extract core theme styles
html_source = 'mapa_comercio_movilidad_cdmx.html'
with open(html_source, 'r', encoding='utf-8') as f:
    orig = f.read()

# Base HTML leído

# Extract existing style content up to UX/UI revamp marker
start_style = orig.find('<style>') + len('<style>')
revamp_marker = orig.find('/* ==========================================================================\n       UX/UI REVAMP')
if revamp_marker != -1 and revamp_marker > start_style:
    existing_style = orig[start_style:revamp_marker].strip()
else:
    end_style = orig.find('</style>')
    existing_style = orig[start_style:end_style].strip()

# Compose extra styles
extra_styles = """
    /* ==========================================================================
       UX/UI REVAMP: CLUSTERING, AUTOCOMPLETE, MODAL, TOASTS & DETAIL CARD
       ========================================================================== */

    /* MarkerCluster Custom Styles */
    .cluster-wrapper {
      background: transparent !important;
      border: none !important;
    }
    .custom-cluster-badge {
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      font-family: var(--font-main);
      font-weight: 800;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(0,0,0,0.28), 0 0 0 3px rgba(255,255,255,0.9);
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease;
      cursor: pointer;
      text-shadow: 0 1px 2px rgba(0,0,0,0.3);
      user-select: none;
    }
    .custom-cluster-badge:hover {
      transform: scale(1.12);
      box-shadow: 0 6px 18px rgba(0,0,0,0.36), 0 0 0 4px #ffffff;
    }
    .cluster-tianguis {
      background: radial-gradient(circle at 35% 35%, #14b8a6, #0f5953);
    }
    .cluster-mercados {
      background: radial-gradient(circle at 35% 35%, #fbbf24, #b45309);
    }
    .cluster-metro {
      background: radial-gradient(circle at 35% 35%, #f87171, #dc2626);
    }
    .cluster-metrobus {
      background: radial-gradient(circle at 35% 35%, #f472b6, #db2777);
    }

    .cluster-small {
      width: 38px;
      height: 38px;
      font-size: 0.72rem;
    }
    .cluster-medium {
      width: 46px;
      height: 46px;
      font-size: 0.78rem;
    }
    .cluster-large {
      width: 54px;
      height: 54px;
      font-size: 0.85rem;
    }

    /* Skeleton Loader */
    .map-loader-overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(248, 250, 252, 0.94);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      z-index: 1500;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: opacity 0.4s ease, visibility 0.4s ease;
    }
    .map-loader-overlay.hidden {
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
    }
    .map-loader-card {
      background: #ffffff;
      padding: 32px 36px;
      border-radius: 18px;
      box-shadow: 0 20px 45px rgba(15, 89, 83, 0.14);
      text-align: center;
      max-width: 440px;
      width: 90%;
      border: 1px solid var(--cdmx-border);
      animation: popIn 0.3s ease;
    }
    @keyframes popIn {
      from { transform: scale(0.92); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }
    .map-loader-icon-pulse {
      display: inline-flex;
      padding: 16px;
      border-radius: 50%;
      background: var(--cdmx-green-light);
      animation: pulseIcon 1.6s infinite ease-in-out;
      margin-bottom: 14px;
    }
    @keyframes pulseIcon {
      0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(15, 89, 83, 0.3); }
      70% { transform: scale(1.05); box-shadow: 0 0 0 16px rgba(15, 89, 83, 0); }
      100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(15, 89, 83, 0); }
    }
    .map-loader-title {
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--cdmx-green-dark);
      margin-bottom: 6px;
    }
    .map-loader-subtitle {
      font-size: 0.78rem;
      color: #64748b;
      margin-bottom: 18px;
      line-height: 1.45;
    }
    .map-loader-bar {
      width: 100%;
      height: 6px;
      background: #e2e8f0;
      border-radius: 999px;
      overflow: hidden;
      position: relative;
      margin-bottom: 12px;
    }
    .map-loader-progress {
      position: absolute;
      top: 0;
      left: 0;
      bottom: 0;
      width: 45%;
      background: linear-gradient(90deg, #10b981, #0f5953);
      border-radius: 999px;
      animation: indeterminateBar 1.4s infinite ease-in-out;
    }
    @keyframes indeterminateBar {
      0% { left: -40%; width: 40%; }
      50% { left: 20%; width: 70%; }
      100% { left: 100%; width: 40%; }
    }
    .map-loader-tip {
      font-size: 0.68rem;
      color: #94a3b8;
      font-weight: 500;
    }

    /* Autocomplete Dropdown */
    .search-autocomplete-dropdown {
      position: absolute;
      top: calc(100% + 4px);
      left: 0;
      right: 0;
      background: #ffffff;
      border-radius: 10px;
      border: 1px solid var(--cdmx-border);
      box-shadow: 0 14px 32px rgba(15, 89, 83, 0.16);
      max-height: 310px;
      overflow-y: auto;
      z-index: 1200;
    }
    .autocomplete-item {
      padding: 10px 14px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      border-bottom: 1px solid #f1f5f9;
      transition: background 0.15s;
    }
    .autocomplete-item:last-child {
      border-bottom: none;
    }
    .autocomplete-item:hover, .autocomplete-item.selected {
      background: var(--cdmx-green-light);
    }
    .autocomplete-badge {
      font-size: 0.62rem;
      font-weight: 800;
      color: #fff;
      padding: 3px 6px;
      border-radius: 4px;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      gap: 4px;
      letter-spacing: 0.3px;
    }
    .autocomplete-text {
      flex: 1;
      min-width: 0;
    }
    .autocomplete-title {
      font-weight: 700;
      font-size: 0.8rem;
      color: #0f172a;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .autocomplete-sub {
      font-size: 0.7rem;
      color: #64748b;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .autocomplete-highlight {
      background: #fef08a;
      color: #854d0e;
      border-radius: 2px;
      padding: 0 1px;
    }

    /* Detail Card Redesign */
    .panel-status-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 999px;
      margin-bottom: 10px;
      line-height: 1.2;
    }
    .status-open {
      background: #dcfce7;
      color: #15803d;
      border: 1px solid #bbf7d0;
    }
    .status-closed {
      background: #fee2e2;
      color: #991b1b;
      border: 1px solid #fecaca;
    }
    .status-warning {
      background: #fef3c7;
      color: #b45309;
      border: 1px solid #fde68a;
    }
    .status-indicator {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
      flex-shrink: 0;
    }
    .status-open .status-indicator { background: #16a34a; }
    .status-closed .status-indicator { background: #dc2626; }
    .status-warning .status-indicator { background: #f59e0b; }

    /* Modern Modal Dialog */
    .cdmx-modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(15, 23, 42, 0.65);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      z-index: 2500;
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
      padding: 16px;
    }
    .cdmx-modal-overlay.active {
      opacity: 1;
      pointer-events: auto;
    }
    .cdmx-modal-dialog {
      background: #ffffff;
      width: 100%;
      max-width: 660px;
      max-height: 88vh;
      border-radius: 18px;
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.35);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transform: scale(0.94);
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .cdmx-modal-overlay.active .cdmx-modal-dialog {
      transform: scale(1);
    }
    .cdmx-modal-header {
      background: var(--cdmx-green-dark);
      color: #ffffff;
      padding: 18px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .cdmx-modal-title {
      font-size: 1.08rem;
      font-weight: 800;
      letter-spacing: -0.01em;
    }
    .cdmx-modal-sub {
      font-size: 0.72rem;
      color: #bbf7d0;
      font-weight: 500;
      margin-top: 2px;
    }
    .cdmx-modal-close {
      background: rgba(255, 255, 255, 0.15);
      border: none;
      color: #ffffff;
      width: 32px;
      height: 32px;
      border-radius: 8px;
      font-size: 1.15rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s;
    }
    .cdmx-modal-close:hover {
      background: rgba(255, 255, 255, 0.3);
    }
    .cdmx-modal-tabs {
      display: flex;
      background: #f8fafc;
      border-bottom: 1px solid #e2e8f0;
      overflow-x: auto;
      flex-shrink: 0;
    }
    .modal-tab-btn {
      flex: 1;
      min-width: 130px;
      padding: 13px 14px;
      border: none;
      background: transparent;
      font-family: var(--font-main);
      font-size: 0.75rem;
      font-weight: 700;
      color: #64748b;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s;
      border-bottom: 3px solid transparent;
      white-space: nowrap;
    }
    .modal-tab-btn:hover {
      color: var(--cdmx-green-dark);
      background: rgba(255, 255, 255, 0.8);
    }
    .modal-tab-btn.active {
      color: var(--cdmx-green-dark);
      background: #ffffff;
      border-bottom: 3px solid var(--cdmx-green-dark);
    }
    .cdmx-modal-body {
      padding: 22px;
      overflow-y: auto;
      font-size: 0.82rem;
      color: #334155;
      line-height: 1.55;
    }
    .modal-tab-pane {
      display: none;
    }
    .modal-tab-pane.active {
      display: block;
      animation: fadeInPane 0.2s ease;
    }
    @keyframes fadeInPane {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Modal Component Elements */
    .modal-section-title {
      font-weight: 800;
      color: #0f172a;
      font-size: 0.92rem;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .modal-alert-box {
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      border-radius: 10px;
      padding: 12px 14px;
      margin-bottom: 14px;
      font-size: 0.78rem;
      color: #166534;
      line-height: 1.45;
    }
    .modal-alert-box.alert-amber {
      background: #fffbeb;
      border-color: #fde68a;
      color: #92400e;
    }
    .modal-grid-2col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 16px;
    }
    .modal-card-mini {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      padding: 12px;
    }
    .modal-card-mini-title {
      font-weight: 700;
      font-size: 0.78rem;
      color: #0f5953;
      margin-bottom: 4px;
    }
    .modal-card-mini-val {
      font-size: 0.72rem;
      color: #475569;
      line-height: 1.4;
    }
    .modal-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 16px;
      font-size: 0.76rem;
    }
    .modal-table th {
      background: #f1f5f9;
      color: #475569;
      font-weight: 700;
      text-align: left;
      padding: 8px 10px;
      border-bottom: 1px solid #cbd5e1;
    }
    .modal-table td {
      padding: 8px 10px;
      border-bottom: 1px solid #f1f5f9;
      color: #334155;
    }
    .modal-table tr:hover td {
      background: #f8fafc;
    }

    /* Toast Container */
    .toast-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 3000;
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: none;
    }
    .toast-item {
      pointer-events: auto;
      min-width: 290px;
      max-width: 390px;
      padding: 12px 16px;
      border-radius: 12px;
      background: #ffffff;
      box-shadow: 0 12px 28px rgba(0,0,0,0.18), 0 3px 8px rgba(0,0,0,0.08);
      font-size: 0.78rem;
      color: #1e293b;
      display: flex;
      align-items: center;
      gap: 10px;
      animation: toastSlideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      transition: opacity 0.3s ease, transform 0.3s ease;
      border-left: 4px solid var(--cdmx-green-dark);
      line-height: 1.4;
    }
    .toast-item.toast-success { border-left-color: #10b981; }
    .toast-item.toast-warning { border-left-color: #f59e0b; }
    .toast-item.toast-error { border-left-color: #ef4444; }
    .toast-item.toast-info { border-left-color: #0284c7; }
    @keyframes toastSlideIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* ==========================================================================
       FILTRO JERÁRQUICO DE COMPRAS (MICRO, MESO, MACRO & POLÍTICA SOCIAL)
       ========================================================================== */
    .badge-policy {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 0.68rem;
      font-weight: 800;
      letter-spacing: 0.2px;
    }
    .badge-canasta {
      background: #dcfce7;
      color: #15803d;
      border: 1px solid #86efac;
    }
    .badge-mercomuna {
      background: #f3e8ff;
      color: #7e22ce;
      border: 1px solid #d8b4fe;
    }
    .badge-cat-mini {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.65rem;
      font-weight: 700;
      background: #f1f5f9;
      color: #334155;
      border: 1px solid #e2e8f0;
    }
    .subgiro-pill {
      display: inline-block;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 0.66rem;
      font-weight: 600;
      background: #ecfdf5;
      color: #065f46;
      border: 1px solid #a7f3d0;
    }
    .macro-chips-container {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-bottom: 6px;
    }
    .macro-chip {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 8px;
      font-size: 0.68rem;
      font-weight: 600;
      background: #f8fafc;
      color: #334155;
      border: 1px solid #cbd5e1;
      border-radius: 16px;
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: inherit;
    }
    .macro-chip:hover {
      background: #e2e8f0;
      border-color: #94a3b8;
    }
    .macro-chip.active {
      background: #0f5953;
      color: #ffffff;
      border-color: #0f5953;
      box-shadow: 0 2px 6px rgba(15,89,83,0.3);
      font-weight: 700;
    }
    .subgiro-select-input {
      width: 100%;
      padding: 6px 10px;
      border-radius: 6px;
      border: 1px solid #cbd5e1;
      font-size: 0.74rem;
      background: #ffffff;
      color: #334155;
      font-family: inherit;
      outline: none;
      cursor: pointer;
    }
    .subgiro-select-input:focus {
      border-color: #0f5953;
      box-shadow: 0 0 0 2px rgba(15,89,83,0.15);
    }
    .policy-toggle-btn {
      flex: 1;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      padding: 6px 8px;
      border-radius: 6px;
      border: 1px solid #cbd5e1;
      background: #ffffff;
      color: #475569;
      font-size: 0.68rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s;
      font-family: inherit;
    }
    .policy-toggle-btn:hover {
      background: #f8fafc;
    }
    .policy-toggle-btn.active-canasta {
      background: #ecfdf5;
      color: #065f46;
      border-color: #10b981;
      font-weight: 800;
      box-shadow: 0 1px 3px rgba(16,185,129,0.2);
    }
    .policy-toggle-btn.active-mercomuna {
      background: #faf5ff;
      color: #6b21a8;
      border-color: #a855f7;
      font-weight: 800;
      box-shadow: 0 1px 3px rgba(168,85,247,0.2);
    }
    .compras-autocomplete-dropdown {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      z-index: 2100;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      box-shadow: 0 10px 25px -5px rgba(0,0,0,0.18);
      max-height: 280px;
      overflow-y: auto;
    }
    .compras-item {
      padding: 7px 10px;
      cursor: pointer;
      border-bottom: 1px solid #f1f5f9;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: background 0.12s;
    }
    .compras-item:hover, .compras-item.selected {
      background: #ecfdf5;
    }
    .compras-term-title {
      font-weight: 700;
      color: #1e293b;
      font-size: 0.78rem;
    }
    .compras-term-sub {
      font-size: 0.68rem;
      color: #64748b;
      display: flex;
      gap: 4px;
      align-items: center;
      margin-top: 2px;
    }
    .compras-badge {
      font-size: 0.6rem;
      font-weight: 700;
      padding: 1px 4px;
      border-radius: 3px;
    }
    .active-filter-pill {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      background: #e0f2fe;
      color: #0369a1;
      border: 1px solid #bae6fd;
      border-radius: 12px;
      padding: 2px 7px;
      font-size: 0.65rem;
      font-weight: 700;
    }
    .active-filter-pill .remove-pill {
      cursor: pointer;
      margin-left: 2px;
      font-weight: 800;
      color: #0284c7;
    }
    .active-filter-pill .remove-pill:hover {
      color: #b91c1c;
    }
"""

html_head = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Movilidad y Comercio CDMX · Portal de Datos</title>
  
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <!-- Leaflet MarkerCluster CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
  <!-- Google Fonts: Montserrat -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet">

  <style>
{existing_style}
{extra_styles}
  </style>
</head>
"""

html_body = """<body>

  <button id="btn-open-sidebar" onclick="toggleSidebar()">
    <span>☰</span>
    <span>Abrir Menú</span>
  </button>

  <aside id="sidebar">
    <div class="sidebar-header">
      <div>
        <div class="sidebar-brand-title">Movilidad y Comercio CDMX</div>
        <div class="sidebar-brand-sub">Chilangatón 2026 · Reto 1</div>
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
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
          <span class="detail-tag" id="panel-tag" style="background:var(--cdmx-green-dark);">MERCADO PÚBLICO</span>
          <button style="border:none; background:transparent; cursor:pointer; font-size:1.15rem; color:#64748b;" onclick="closeDetailCard()" title="Cerrar ficha">✕</button>
        </div>

        <div id="panel-status-pill" class="panel-status-pill status-open">
          <span class="status-indicator"></span>
          <span id="panel-status-text">Abierto hoy hasta 18:00</span>
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

        <!-- Categorías y Banderas de Política Pública -->
        <div id="panel-policy-badges" style="display:flex; flex-wrap:wrap; gap:4px; margin-bottom:8px;"></div>
        
        <!-- Subgiros y Oferta Comercial Disponibles -->
        <div id="panel-subgiros-box" style="display:none; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:8px; margin-bottom:8px; font-size:0.73rem;">
          <div style="font-weight:700; color:#0f5953; margin-bottom:4px; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.3px;">
            🛍️ Oferta Comercial y Giros Disponibles:
          </div>
          <div id="panel-subgiros-content" style="display:flex; flex-wrap:wrap; gap:4px;"></div>
        </div>

        <!-- Alerta de Cierre Vial -->
        <div id="panel-closure-box" style="display:none; background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:10px; margin-bottom:8px; font-size:0.75rem; color:#92400e;">
          <div style="font-weight:700; margin-bottom:2px; display:flex; align-items:center; gap:4px;">
            <span>⚠️ Afectación Vial Programada:</span>
          </div>
          <div id="panel-closure-text" style="color:#78350f; line-height:1.35;"></div>
        </div>

        <!-- Conexión de Transporte -->
        <div style="background:#ffffff; padding:10px; border-radius:8px; border:1px solid #dbeae8; margin-bottom:10px; font-size:0.75rem;">
          <div style="font-weight:700; color:var(--cdmx-green-dark); margin-bottom:3px; display:flex; align-items:center; gap:4px;">
            <span>🚇 Conexión de Movilidad Integrada:</span>
          </div>
          <div id="panel-conn" style="color:#334155; line-height:1.4;">Cargando estación o corredor cercano...</div>
        </div>

        <div style="display:flex; gap:6px;">
          <button onclick="setAsRouteDestination()" style="flex:1.2; background:#0f5953; color:#fff; border:none; padding:8px; border-radius:6px; font-size:0.74rem; font-weight:700; cursor:pointer;" title="Fijar como destino de viaje">
            🎯 Ir hacia aquí
          </button>
          <button onclick="copyCurrentCoords()" style="flex:1; background:#f1f5f9; color:#334155; border:1px solid #cbd5e1; padding:8px; border-radius:6px; font-size:0.72rem; font-weight:700; cursor:pointer;" title="Copiar coordenadas geográficas">
            📋 Copiar GPS
          </button>
          <a href="https://rtponky.lat/" target="_blank" class="rtponky-link-btn" style="flex:0.9;" id="panel-rtponky-btn" title="Consultar en RTPonky">
            <span>RTPonky ↗</span>
          </a>
        </div>
      </div>

      <!-- Buscador Unificado con Autocompletado Predictivo -->
      <div class="section-block">
        <div class="section-heading">
          <span>Buscador Unificado</span>
          <span style="font-size:0.65rem; background:#dcfce7; color:#166534; font-weight:700; padding:2px 6px; border-radius:4px;">PREDICTIVO</span>
        </div>
        <div class="search-input-box" style="position:relative;">
          <svg class="search-icon-svg" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 14z"/></svg>
          <input type="text" id="market-search" placeholder="Buscar mercado, tianguis, metro, RTP..." autocomplete="off">
          <button id="clear-search-btn" onclick="clearUnifiedSearch()" style="display:none; background:transparent; border:none; color:#94a3b8; cursor:pointer; padding:4px 8px; font-size:0.9rem;" title="Limpiar búsqueda">✕</button>
        </div>
        <div id="search-autocomplete-dropdown" class="search-autocomplete-dropdown" style="display:none;"></div>
      </div>

      <!-- Filtro Jerárquico de Compras Populares (Micro -> Meso -> Macro) -->
      <div class="section-block" id="compras-filter-section" style="background:#ffffff; border:1px solid #d1fae5; border-radius:10px; padding:12px; margin-bottom:12px; box-shadow:0 2px 6px rgba(15,89,83,0.06);">
        <div class="section-heading" style="margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
          <div style="display:flex; align-items:center; gap:6px;">
            <span style="font-size:1.05rem;">🛒</span>
            <span style="font-weight:800; color:#0f5953; font-size:0.85rem;">Filtro de Compras Barriales</span>
          </div>
          <span style="font-size:0.62rem; background:#ecfdf5; color:#047857; font-weight:800; padding:2px 6px; border-radius:4px; border:1px solid #a7f3d0;">3 NIVELES</span>
        </div>

        <!-- 1. NIVEL MICRO: Búsqueda predictiva de productos concretos -->
        <div style="font-size:0.7rem; font-weight:700; color:#475569; margin-bottom:4px; display:flex; justify-content:space-between;">
          <span>1. ¿QUÉ QUIERES COMPRAR HOY?</span>
          <span style="color:#0f5953; font-size:0.65rem;">Nivel Micro</span>
        </div>
        <div class="search-input-box" style="position:relative; margin-bottom:8px;">
          <svg class="search-icon-svg" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 14z"/></svg>
          <input type="text" id="compras-search-input" placeholder="Ej. jitomate, barbacoa, tenis, clavos, útiles..." autocomplete="off">
          <button id="clear-compras-btn" onclick="clearComprasSearch()" style="display:none; background:transparent; border:none; color:#94a3b8; cursor:pointer; padding:4px 8px; font-size:0.9rem;" title="Limpiar término">✕</button>
        </div>
        <div id="compras-autocomplete-dropdown" class="compras-autocomplete-dropdown" style="display:none;"></div>

        <!-- 2. NIVEL MACRO: 9 Macro-Categorías -->
        <div style="font-size:0.7rem; font-weight:700; color:#475569; margin-bottom:4px; display:flex; justify-content:space-between;">
          <span>2. MACRO-CATEGORÍAS</span>
          <span style="color:#0f5953; font-size:0.65rem;">9 Sectores</span>
        </div>
        <div class="macro-chips-container" id="macro-chips-container"></div>

        <!-- 3. NIVEL MESO: 67 Subgiros del Catálogo -->
        <div style="font-size:0.7rem; font-weight:700; color:#475569; margin:8px 0 4px 0; display:flex; justify-content:space-between;">
          <span>3. SUBGIRO ESPECÍFICO</span>
          <span style="color:#0f5953; font-size:0.65rem;">67 Giros Oficiales</span>
        </div>
        <div style="position:relative; margin-bottom:8px;">
          <select id="subgiro-select" class="subgiro-select-input" onchange="onSubgiroSelectChange(this.value)">
            <option value="">Todos los subgiros comerciales...</option>
          </select>
        </div>

        <!-- 4. CONMUTADORES DE POLÍTICA PÚBLICA -->
        <div style="display:flex; flex-direction:column; gap:5px; margin-top:8px; padding-top:8px; border-top:1px dashed #e2e8f0;">
          <div style="display:flex; gap:6px;">
            <button class="policy-toggle-btn" id="btn-toggle-canasta" onclick="toggleFilterCanasta()">
              <span class="p-icon">🛒</span>
              <span class="p-txt">Canasta Básica SEDECO</span>
            </button>
            <button class="policy-toggle-btn" id="btn-toggle-mercomuna" onclick="toggleFilterMercomuna()">
              <span class="p-icon">💳</span>
              <span class="p-txt">Vales Mercomuna</span>
            </button>
          </div>
        </div>

        <!-- CONTADOR DE RESULTADOS Y ETIQUETAS ACTIVAS -->
        <div id="compras-feedback-box" style="margin-top:10px; padding:6px 8px; background:#f8fafc; border-radius:6px; border:1px solid #e2e8f0;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span id="compras-results-counter" style="font-size:0.72rem; font-weight:800; color:#0f5953;">Mostrando 1,747 espacios</span>
            <button id="compras-reset-all-btn" onclick="resetAllCommerceFilters()" style="display:none; background:#fee2e2; color:#b91c1c; border:none; border-radius:4px; padding:2px 6px; font-size:0.65rem; font-weight:700; cursor:pointer;">Limpiar Filtros ✕</button>
          </div>
          <div id="compras-active-pills" style="display:flex; flex-wrap:wrap; gap:4px; margin-top:4px;"></div>
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
          <div class="goto-btn" onclick="openInfoModal('closures')" title="Ver detalle de cierres viales">
            <div class="goto-btn-circle">
              <svg viewBox="0 0 24 24"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>
            </div>
            <div class="goto-btn-lbl">Cierres Vías</div>
          </div>

          <div class="goto-btn" onclick="openInfoModal('hours')" title="Consultar horarios semanales">
            <div class="goto-btn-circle">
              <svg viewBox="0 0 24 24"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/></svg>
            </div>
            <div class="goto-btn-lbl">Horarios</div>
          </div>

          <div class="goto-btn" onclick="openInfoModal('fares')" title="Consultar tarifas de Movilidad Integrada">
            <div class="goto-btn-circle">
              <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
            </div>
            <div class="goto-btn-lbl">Tarifas MI</div>
          </div>

          <a href="https://rtponky.lat/" target="_blank" class="goto-btn" title="Abrir RTPonky en ventana nueva">
            <div class="goto-btn-circle" style="background:#15803d;">
              <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 14h-2v-2h2v2zm0-4h-2V7h2v5z"/></svg>
            </div>
            <div class="goto-btn-lbl">RTPonky</div>
          </a>
        </div>
      </div>

    </div>
  </aside>

  <main id="map-wrapper">
    <div id="map"></div>

    <!-- Skeleton Loader Inicial -->
    <div id="map-loader" class="map-loader-overlay">
      <div class="map-loader-card">
        <div class="map-loader-icon-pulse">
          <svg width="42" height="42" viewBox="0 0 24 24" fill="#0f5953">
            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
          </svg>
        </div>
        <div class="map-loader-title">Movilidad y Comercio CDMX</div>
        <div class="map-loader-subtitle" id="loader-sub">Inicializando 329 mercados, 1,367 tianguis, 519 estaciones y red MI...</div>
        <div class="map-loader-bar">
          <div class="map-loader-progress"></div>
        </div>
        <div class="map-loader-tip">Chilangatón 2026 · Plataforma Barrial y Movilidad Sustentable</div>
      </div>
    </div>

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

  <!-- Modal Flotante / Drawer con Pestañas -->
  <div id="info-modal-overlay" class="cdmx-modal-overlay" onclick="handleModalOverlayClick(event)">
    <div class="cdmx-modal-dialog">
      <div class="cdmx-modal-header">
        <div>
          <div class="cdmx-modal-title">Movilidad y Comercio Popular CDMX</div>
          <div class="cdmx-modal-sub">Chilangatón 2026 · Información Operativa y Barrial</div>
        </div>
        <button class="cdmx-modal-close" onclick="closeInfoModal()" title="Cerrar ventana">✕</button>
      </div>

      <div class="cdmx-modal-tabs">
        <button class="modal-tab-btn active" id="tab-btn-closures" onclick="switchModalTab('closures')">
          <span>🚧 Cierres Viales</span>
        </button>
        <button class="modal-tab-btn" id="tab-btn-hours" onclick="switchModalTab('hours')">
          <span>⏰ Horarios Semanales</span>
        </button>
        <button class="modal-tab-btn" id="tab-btn-fares" onclick="switchModalTab('fares')">
          <span>💳 Tarifas MI</span>
        </button>
        <button class="modal-tab-btn" id="tab-btn-today" onclick="switchModalTab('today')">
          <span>📅 Aviso Hoy</span>
        </button>
      </div>

      <div class="cdmx-modal-body">
        <!-- Tab 1: Cierres Viales -->
        <div id="tab-pane-closures" class="modal-tab-pane active">
          <div class="modal-section-title">
            <span>🚧 Afectaciones y Reducciones Viales por Tianguis</span>
          </div>
          <div class="modal-alert-box alert-amber">
            <b>1,367 tianguis semanales</b> operan sobre el arroyo vehicular en las 16 alcaldías de la CDMX, generando cortes programados y reducciones viales en horarios de <b>07:00 a 18:30 hrs</b>.
          </div>

          <div style="font-weight:700; color:#0f5953; margin-bottom:8px; font-size:0.8rem;">Distribución Semanal de Tianguis en Vía Pública:</div>
          <div class="modal-grid-2col">
            <div class="modal-card-mini">
              <div class="modal-card-mini-title">📅 Domingo (Pico Máximo)</div>
              <div class="modal-card-mini-val"><b>341 tianguis</b> · Alta afectación barrial en Iztapalapa, GAM y Cuauhtémoc.</div>
            </div>
            <div class="modal-card-mini">
              <div class="modal-card-mini-title">📅 Sábado (Pico Comercial)</div>
              <div class="modal-card-mini-val"><b>283 tianguis</b> · Zonas de abastecimiento familiar y abasto fresco.</div>
            </div>
            <div class="modal-card-mini">
              <div class="modal-card-mini-title">📅 Viernes</div>
              <div class="modal-card-mini-val"><b>215 tianguis</b> · Conexión directa con corredores y paraderos.</div>
            </div>
            <div class="modal-card-mini">
              <div class="modal-card-mini-title">📅 Jueves</div>
              <div class="modal-card-mini-val"><b>201 tianguis</b> · Actividad regular en colonias populares.</div>
            </div>
            <div class="modal-card-mini">
              <div class="modal-card-mini-title">📅 Miércoles</div>
              <div class="modal-card-mini-val"><b>198 tianguis</b> · Operación barrial coordinada con SEDECO.</div>
            </div>
            <div class="modal-card-mini">
              <div class="modal-card-mini-title">📅 Martes y Lunes</div>
              <div class="modal-card-mini-val"><b>172 tianguis (Mar)</b> / <b>89 tianguis (Lun)</b> · Menor impacto vial en la red.</div>
            </div>
          </div>

          <div style="font-weight:700; color:#334155; margin-bottom:6px; font-size:0.78rem;">💡 Recomendaciones para la Ciudadanía:</div>
          <ul style="padding-left:18px; line-height:1.5; color:#64748b; font-size:0.75rem;">
            <li>Toca cualquier tianguis en el mapa para ver la calle exacta ocupada.</li>
            <li>En días domingo y sábado, priorizar traslados en Metro, Metrobús o Cablebús para evitar desvíos vehiculares.</li>
            <li>El horario de carga y descarga pesada ocurre de 06:30 a 08:00 hrs y de 17:30 a 18:30 hrs.</li>
          </ul>
        </div>

        <!-- Tab 2: Horarios Semanales -->
        <div id="tab-pane-hours" class="modal-tab-pane">
          <div class="modal-section-title">
            <span>⏰ Horarios Oficiales de la Red y Comercio Popular</span>
          </div>

          <table class="modal-table">
            <thead>
              <tr>
                <th>Sistema / Comercio</th>
                <th>Lunes a Viernes</th>
                <th>Sábados</th>
                <th>Domingos / Festivos</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><b>🚇 Metro CDMX</b></td>
                <td>05:00 - 24:00 hrs</td>
                <td>06:00 - 24:00 hrs</td>
                <td>07:00 - 24:00 hrs <i>(Bici en Metro)</i></td>
              </tr>
              <tr>
                <td><b>🚍 Metrobús CDMX</b></td>
                <td>04:30 - 24:00 hrs</td>
                <td>04:30 - 24:00 hrs</td>
                <td>05:00 - 24:00 hrs</td>
              </tr>
              <tr>
                <td><b>🚎 Trolebús</b></td>
                <td>05:00 - 00:00 hrs</td>
                <td>05:00 - 00:00 hrs</td>
                <td>05:30 - 23:30 hrs</td>
              </tr>
              <tr>
                <td><b>🚡 Cablebús (L1, L2, L3)</b></td>
                <td>05:00 - 23:00 hrs</td>
                <td>06:00 - 23:00 hrs</td>
                <td>07:00 - 23:00 hrs</td>
              </tr>
              <tr>
                <td><b>🏪 Mercados Públicos (329)</b></td>
                <td>08:00 - 18:00 hrs</td>
                <td>08:00 - 18:00 hrs</td>
                <td>08:00 - 17:00 hrs</td>
              </tr>
              <tr>
                <td><b>🧺 Tianguis y MSR</b></td>
                <td>08:30 - 17:30 hrs</td>
                <td>08:30 - 17:30 hrs</td>
                <td>08:30 - 17:30 hrs</td>
              </tr>
            </tbody>
          </table>

          <div class="modal-alert-box">
            <b>Nota sobre Mercados:</b> Las naves de comida corrida, antojitos y recauderías suelen iniciar servicio desde las 07:30 hrs para abastecer a trabajadoras y trabajadores de la zona.
          </div>
        </div>

        <!-- Tab 3: Tarifas MI -->
        <div id="tab-pane-fares" class="modal-tab-pane">
          <div class="modal-section-title">
            <span>💳 Tarifas Oficiales · Sistema de Movilidad Integrada (MI)</span>
          </div>

          <table class="modal-table">
            <thead>
              <tr>
                <th>Modo de Transporte</th>
                <th>Tarifa Oficial</th>
                <th>Medio de Pago</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><b>🚇 Metro CDMX</b></td>
                <td>$5.00 MXN</td>
                <td>Tarjeta MI</td>
              </tr>
              <tr>
                <td><b>🚍 Metrobús</b></td>
                <td>$6.00 MXN (L1-L7) / $30.00 (Aeropuerto)</td>
                <td>Tarjeta MI / CoDi / Bancaria</td>
              </tr>
              <tr>
                <td><b>🚡 Cablebús</b></td>
                <td>$7.00 MXN</td>
                <td>Tarjeta MI</td>
              </tr>
              <tr>
                <td><b>🚎 Trolebús</b></td>
                <td>$4.00 MXN regular / $7.00 (Elevado)</td>
                <td>Tarjeta MI</td>
              </tr>
              <tr>
                <td><b>🚌 RTP Pasajeros</b></td>
                <td>$2.00 (Atenea / Ordinario) / $4.00 (Expreso) / $5.00 (Ecobús)</td>
                <td>Tarjeta MI / Efectivo exacto</td>
              </tr>
              <tr>
                <td><b>🚋 Tren Ligero</b></td>
                <td>$3.00 MXN</td>
                <td>Tarjeta MI</td>
              </tr>
              <tr>
                <td><b>🚐 Corredores Concesionados</b></td>
                <td>$6.00 - $8.50 MXN (según distancia y tipo de unidad)</td>
                <td>Efectivo / Tarjeta MI (algunas rutas)</td>
              </tr>
            </tbody>
          </table>

          <div class="modal-alert-box">
            <b>Exenciones de Pago (Gratuidad):</b> Personas adultas mayores (60+ años con credencial INAPAM), personas con discapacidad y menores de 5 años viajan gratis en toda la red pública de la CDMX.
          </div>
        </div>

        <!-- Tab 4: Aviso Hoy -->
        <div id="tab-pane-today" class="modal-tab-pane">
          <div class="modal-section-title">
            <span>📅 Estado y Operación Comercial de Hoy</span>
          </div>
          <div id="modal-today-banner" class="modal-alert-box">
            Calculando tianguis y mercados operando en este momento...
          </div>

          <div style="display:flex; gap:10px; margin-top:16px;">
            <button onclick="filterByToday(); closeInfoModal();" style="flex:1; background:var(--cdmx-green-dark); color:#fff; border:none; padding:12px; border-radius:8px; font-weight:700; font-size:0.78rem; cursor:pointer;">
              🔍 Filtrar Mapa a Tianguis de Hoy
            </button>
            <button onclick="renderTianguisMarkers(null); closeInfoModal();" style="flex:1; background:#f1f5f9; color:#334155; border:1px solid #cbd5e1; padding:12px; border-radius:8px; font-weight:700; font-size:0.78rem; cursor:pointer;">
              🌐 Ver Todos los Días (1,367)
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>

  <!-- Toast Container -->
  <div id="toast-container" class="toast-container"></div>

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <!-- Leaflet MarkerCluster JS -->
  <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

  <!-- Bundle de datos optimizado para modo local y offline -->
  <script src="data/processed/map_bundle.js" onerror="console.log('map_bundle.js no cargado localmente, se intentará fetch asíncrono')"></script>

  <script>
    // =========================================================================
    // INICIALIZACIÓN DEL MAPA Y MAPAS BASE
    // =========================================================================
    const map = L.map('map', {
      center: [19.4326, -99.1332],
      zoom: 12,
      minZoom: 9,
      maxZoom: 18,
      zoomControl: false
    });

    L.control.zoom({ position: 'topright' }).addTo(map);

    let currentBase = 'esri';
    const esriLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
      attribution: 'Esri, HERE, Garmin, &copy; OpenStreetMap contributors',
      maxZoom: 18
    }).addTo(map);

    const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19
    });

    function toggleBaseMap() {
      if (currentBase === 'esri') {
        map.removeLayer(esriLayer);
        osmLayer.addTo(map);
        currentBase = 'osm';
        showToast('Mapa base cambiado a OpenStreetMap.', 'info');
      } else {
        map.removeLayer(osmLayer);
        esriLayer.addTo(map);
        currentBase = 'esri';
        showToast('Mapa base cambiado a Esri Light Gray.', 'info');
      }
    }

    // =========================================================================
    // SISTEMA DE CAPAS CON CLUSTERING INTELIGENTE (LEAFLET.MARKERCLUSTER)
    // =========================================================================
    const clusterOptionsBase = {
      disableClusteringAtZoom: 14,
      maxClusterRadius: 45,
      showCoverageOnHover: false,
      zoomToBoundsOnClick: true,
      spiderfyOnMaxZoom: true,
      animate: true
    };

    const layers = {
      zmvm: L.geoJSON(null, {
        style: {
          color: '#94a3b8',
          weight: 1,
          dashArray: '3, 4',
          fillColor: '#f1f5f9',
          fillOpacity: 0.15
        },
        onEachFeature: (feature, layer) => {
          const nom = feature.properties.NOMGEO || 'Municipio Metropolitano';
          layer.bindTooltip(nom + ' (Edomex / ZMVM)', { sticky: true });
        }
      }),
      alcaldias: L.geoJSON(null, {
        style: {
          color: '#0f5953',
          weight: 2,
          dashArray: '4, 4',
          fillColor: '#0f5953',
          fillOpacity: 0.03
        },
        onEachFeature: (feature, layer) => {
          const nom = feature.properties.nomgeo || feature.properties.alcaldia || 'Alcaldía';
          layer.bindTooltip('Alcaldía ' + nom, { sticky: true });
        }
      }),
      metro: L.featureGroup(),
      metro_icons: L.markerClusterGroup({
        ...clusterOptionsBase,
        maxClusterRadius: 36,
        iconCreateFunction: function(cluster) {
          const count = cluster.getChildCount();
          let size = count < 10 ? 'small' : (count < 20 ? 'medium' : 'large');
          return L.divIcon({
            html: `<div class="custom-cluster-badge cluster-metro cluster-${size}">🚇 ${count}</div>`,
            className: 'cluster-wrapper',
            iconSize: L.point(44, 44)
          });
        }
      }),
      metrobus: L.featureGroup(),
      metrobus_icons: L.markerClusterGroup({
        ...clusterOptionsBase,
        maxClusterRadius: 36,
        iconCreateFunction: function(cluster) {
          const count = cluster.getChildCount();
          let size = count < 10 ? 'small' : (count < 20 ? 'medium' : 'large');
          return L.divIcon({
            html: `<div class="custom-cluster-badge cluster-metrobus cluster-${size}">🚍 ${count}</div>`,
            className: 'cluster-wrapper',
            iconSize: L.point(44, 44)
          });
        }
      }),
      rtp: L.featureGroup(),
      cablebus: L.featureGroup(),
      trolebus: L.featureGroup(),
      tren: L.featureGroup(),
      concesionado: L.featureGroup(),
      mercados: L.markerClusterGroup({
        ...clusterOptionsBase,
        maxClusterRadius: 40,
        iconCreateFunction: function(cluster) {
          const count = cluster.getChildCount();
          let size = count < 10 ? 'small' : (count < 25 ? 'medium' : 'large');
          return L.divIcon({
            html: `<div class="custom-cluster-badge cluster-mercados cluster-${size}">🏪 ${count}</div>`,
            className: 'cluster-wrapper',
            iconSize: L.point(44, 44)
          });
        }
      }),
      msr: L.featureGroup(),
      tianguis: L.markerClusterGroup({
        ...clusterOptionsBase,
        maxClusterRadius: 48,
        iconCreateFunction: function(cluster) {
          const count = cluster.getChildCount();
          let size = count < 20 ? 'small' : (count < 60 ? 'medium' : 'large');
          return L.divIcon({
            html: `<div class="custom-cluster-badge cluster-tianguis cluster-${size}">🧺 ${count}</div>`,
            className: 'cluster-wrapper',
            iconSize: L.point(44, 44)
          });
        }
      }),
      routeLines: L.featureGroup(),
      userLocation: L.featureGroup()
    };

    layers.routeLines.addTo(map);
    layers.userLocation.addTo(map);

    const transportMapping = {
      'METRO': layers.metro,
      'MB': layers.metrobus,
      'RTP': layers.rtp,
      'CBB': layers.cablebus,
      'TROLE': layers.trolebus,
      'TL': layers.tren,
      'CC': layers.concesionado
    };

    let currentSelectedTarget = null;
    let SEARCH_INDEX = [];

    // =========================================================================
    // CARGA ASÍNCRONA DE DATOS Y CONSTRUCCIÓN DE CAPAS
    // =========================================================================
    async function loadDataBundle() {
      if (typeof window.MAP_DATA !== 'undefined' && window.MAP_DATA && window.MAP_DATA.mercados) {
        return window.MAP_DATA;
      }
      try {
        const res = await fetch('data/processed/map_bundle.json');
        if (!res.ok) throw new Error('Status ' + res.status);
        const data = await res.json();
        window.MAP_DATA = data;
        return data;
      } catch (err) {
        console.error("Error al cargar map_bundle.json", err);
        showToast('Aviso: cargando capas con modo de contingencia.', 'warning');
        return window.MAP_DATA || {};
      }
    }

    async function initApplication() {
      const loader = document.getElementById('map-loader');
      const loaderSub = document.getElementById('loader-sub');

      try {
        loaderSub.innerText = "Descargando geometrías y directorio de comercio...";
        const data = await loadDataBundle();

        loaderSub.innerText = "Construyendo capas base y polígonos...";
        if (data.zmvm) {
          layers.zmvm.addData(data.zmvm);
          layers.zmvm.addTo(map);
        }
        if (data.alcaldias) {
          layers.alcaldias.addData(data.alcaldias);
          layers.alcaldias.addTo(map);
        }

        // Trazados de Red de Transporte
        if (data.transport) {
          Object.keys(transportMapping).forEach(agency => {
            const tData = data.transport[agency];
            if (tData && tData.features) {
              const fg = transportMapping[agency];
              tData.features.forEach(f => {
                const polyline = L.polyline(
                  f.geometry.coordinates.map(c => [c[1], c[0]]),
                  {
                    color: f.properties.color,
                    weight: f.properties.weight,
                    opacity: 0.9
                  }
                );
                polyline.on('click', () => {
                  showTransportInDetail(f.properties);
                });
                fg.addLayer(polyline);
              });
              fg.addTo(map);
            }
          });
        }

        loaderSub.innerText = "Configurando clusters para estaciones y comercio popular...";

        // Estaciones de Metro
        if (data.metro_stations) {
          data.metro_stations.forEach(st => {
            let glyphHtml = st.has_glyph ? `<em class="${st.icon_class}"></em>` : `<span style="font-size:8.5px; font-weight:800; color:#fff;">${st.fallback_text || 'M'}</span>`;
            const iconHtml = `<div class="metro-station-badge" style="background:${st.color};" title="${st.nombre} (Línea ${st.linea})">${glyphHtml}</div>`;
            const customIcon = L.divIcon({
              className: 'custom-metro-icon-container',
              html: iconHtml,
              iconSize: [22, 22],
              iconAnchor: [11, 11]
            });
            const marker = L.marker([st.lat, st.lon], { icon: customIcon });
            marker.on('click', () => {
              currentSelectedTarget = { name: 'Metro ' + st.nombre, lat: st.lat, lon: st.lon };
              map.flyTo([st.lat, st.lon], Math.max(map.getZoom(), 15), { duration: 0.8 });
              showMetroStationInDetail(st);
            });
            layers.metro_icons.addLayer(marker);
          });
          layers.metro_icons.addTo(map);
        }

        // Estaciones de Metrobús
        if (data.metrobus_stations) {
          data.metrobus_stations.forEach(st => {
            const iconHtml = `<div class="mb-station-badge" title="${st.nombre} (${st.linea})">MB</div>`;
            const customIcon = L.divIcon({
              className: 'custom-mb-icon-container',
              html: iconHtml,
              iconSize: [20, 20],
              iconAnchor: [10, 10]
            });
            const marker = L.marker([st.lat, st.lon], { icon: customIcon });
            marker.on('click', () => {
              currentSelectedTarget = { name: 'Metrobús ' + st.nombre, lat: st.lat, lon: st.lon };
              map.flyTo([st.lat, st.lon], Math.max(map.getZoom(), 15), { duration: 0.8 });
              showMetroStationInDetail({
                nombre: st.nombre,
                linea: st.linea,
                alcaldia: st.alcaldia,
                color: '#ec4899',
                tipo: 'Metrobús CDMX'
              });
            });
            layers.metrobus_icons.addLayer(marker);
          });
          layers.metrobus_icons.addTo(map);
        }

        // Inicializar Filtro Jerárquico de Compras y desplegar marcadores reactivos
        initCommerceFilters();
        applyCommerceFilters();

        // Indexador para Buscador Unificado
        buildUnifiedSearchIndex(data);

        // Actualizar datos del día en Modal
        updateTodayModalInfo();

        // Finalizar carga
        setTimeout(() => {
          loader.classList.add('hidden');
          showToast('Portal listo · 1,367 tianguis y 329 mercados sincronizados.', 'success', 3500);
        }, 300);

      } catch (err) {
        console.error("Error inicializando mapa:", err);
        loader.classList.add('hidden');
        showToast('Se cargó el mapa con funcionalidad básica.', 'warning');
      }
    }

    // =========================================================================
    // ESTADO Y SISTEMA DE FILTRADO JERÁRQUICO DE COMPRAS (MICRO, MESO, MACRO)
    // =========================================================================
    const filterState = {
      macroCategory: null,
      subgiro: null,
      product: null,
      canastaBasica: false,
      mercomuna: false,
      openToday: false
    };

    let COMPRAS_VOCAB = [];
    let highlightedComprasIdx = -1;

    function initCommerceFilters() {
      if (!window.MAP_DATA) return;
      COMPRAS_VOCAB = window.MAP_DATA.vocabulario_compras || [];

      // 1. Render Macro Chips (9 Categorías)
      const chipsContainer = document.getElementById('macro-chips-container');
      if (chipsContainer && window.MAP_DATA.catalog_categorias) {
        chipsContainer.innerHTML = '';
        window.MAP_DATA.catalog_categorias.forEach(c => {
          const chip = document.createElement('button');
          chip.className = 'macro-chip';
          chip.id = 'macro-chip-' + c.id;
          const shortName = c.nombre.split(',')[0];
          chip.innerHTML = `<span>${c.icono}</span> <span>${shortName}</span>`;
          chip.title = `${c.nombre}: ${c.descripcion || ''}`;
          chip.onclick = () => toggleMacroCategory(c.id);
          chipsContainer.appendChild(chip);
        });
      }

      // 2. Poblar selector de 67 Subgiros agrupados por categoría
      const subgiroSel = document.getElementById('subgiro-select');
      if (subgiroSel && window.MAP_DATA.catalog_subgiros && window.MAP_DATA.catalog_categorias) {
        subgiroSel.innerHTML = '<option value="">Todos los subgiros comerciales (67 opciones)...</option>';
        window.MAP_DATA.catalog_categorias.forEach(c => {
          const optGroup = document.createElement('optgroup');
          optGroup.label = `${c.icono} ${c.nombre}`;
          const subgiros = window.MAP_DATA.catalog_subgiros.filter(sg => sg.categoria_id === c.id);
          subgiros.forEach(sg => {
            const opt = document.createElement('option');
            opt.value = sg.id;
            opt.textContent = (sg.canasta_basica ? '🛒 ' : '') + sg.nombre;
            optGroup.appendChild(opt);
          });
          subgiroSel.appendChild(optGroup);
        });
      }

      // 3. Listeners de Búsqueda Predictiva Nivel Micro
      const comprasInput = document.getElementById('compras-search-input');
      const comprasDropdown = document.getElementById('compras-autocomplete-dropdown');
      const clearBtn = document.getElementById('clear-compras-btn');

      if (comprasInput && comprasDropdown) {
        comprasInput.addEventListener('input', (e) => {
          const query = e.target.value.trim();
          if (!query) {
            comprasDropdown.style.display = 'none';
            if (clearBtn) clearBtn.style.display = 'none';
            if (filterState.product) {
              filterState.product = null;
              applyCommerceFilters();
            }
            return;
          }
          if (clearBtn) clearBtn.style.display = 'block';
          renderComprasAutocompleteDropdown(query);
        });

        comprasInput.addEventListener('focus', (e) => {
          const query = e.target.value.trim();
          if (query) renderComprasAutocompleteDropdown(query);
        });

        comprasInput.addEventListener('keydown', (e) => {
          const items = comprasDropdown.querySelectorAll('.compras-item');
          if (items.length === 0 || comprasDropdown.style.display === 'none') return;

          if (e.key === 'ArrowDown') {
            e.preventDefault();
            highlightedComprasIdx = (highlightedComprasIdx + 1) % items.length;
            updateHighlightedCompras(items);
          } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            highlightedComprasIdx = (highlightedComprasIdx - 1 + items.length) % items.length;
            updateHighlightedCompras(items);
          } else if (e.key === 'Enter') {
            e.preventDefault();
            if (highlightedComprasIdx >= 0 && highlightedComprasIdx < items.length) {
              items[highlightedComprasIdx].click();
            }
          } else if (e.key === 'Escape') {
            comprasDropdown.style.display = 'none';
          }
        });

        document.addEventListener('click', (e) => {
          if (!e.target.closest('#compras-filter-section')) {
            comprasDropdown.style.display = 'none';
          }
        });
      }
    }

    function updateHighlightedCompras(items) {
      items.forEach((el, idx) => {
        if (idx === highlightedComprasIdx) {
          el.classList.add('selected');
          el.scrollIntoView({ block: 'nearest' });
        } else {
          el.classList.remove('selected');
        }
      });
    }

    function renderComprasAutocompleteDropdown(query) {
      const dropdown = document.getElementById('compras-autocomplete-dropdown');
      if (!dropdown || !COMPRAS_VOCAB.length) return;

      const normQ = query.toLowerCase().trim();
      const tokens = normQ.split(/\\s+/).filter(Boolean);

      const matches = [];
      COMPRAS_VOCAB.forEach(item => {
        let matched = false;
        let score = item.peso || 50;

        const termLower = item.termino.toLowerCase();
        if (termLower.startsWith(normQ)) score += 40;
        else if (termLower.includes(normQ)) score += 20;

        const allTokens = item.tokens_busqueda || [];
        const matchesAll = tokens.every(t => allTokens.some(tok => tok.includes(t)));
        if (matchesAll) {
          matched = true;
          if (item.canasta_basica) score += 5;
          if (item.mercomuna) score += 5;
          matches.push({ item, score });
        }
      });

      matches.sort((a, b) => b.score - a.score);
      const topMatches = matches.slice(0, 8).map(m => m.item);

      if (topMatches.length === 0) {
        dropdown.innerHTML = `
          <div style="padding:10px; font-size:0.75rem; color:#64748b; text-align:center;">
            No se encontró el producto "<b>${query}</b>". Prueba con jitomate, barbacoa, tenis, clavos, útiles...
          </div>
        `;
        dropdown.style.display = 'block';
        return;
      }

      dropdown.innerHTML = topMatches.map((m, idx) => `
        <div class="compras-item" onclick="selectComprasItem('${m.id}')" data-idx="${idx}">
          <div>
            <div class="compras-term-title">${m.termino}</div>
            <div class="compras-term-sub">
              <span>${m.categoria_icono}</span>
              <span>${m.subgiro_nombre}</span>
            </div>
          </div>
          <div style="display:flex; flex-direction:column; align-items:flex-end; gap:2px;">
            ${m.canasta_basica ? '<span class="compras-badge badge-canasta">🛒 Canasta Básica</span>' : ''}
            ${m.mercomuna ? '<span class="compras-badge badge-mercomuna">💳 Mercomuna</span>' : ''}
          </div>
        </div>
      `).join('');

      dropdown.style.display = 'block';
      highlightedComprasIdx = -1;
    }

    function selectComprasItem(itemId) {
      const item = COMPRAS_VOCAB.find(v => v.id === itemId);
      if (!item) return;

      filterState.product = item;
      filterState.subgiro = item.subgiro_id;
      filterState.macroCategory = item.categoria_id;

      const input = document.getElementById('compras-search-input');
      if (input) input.value = item.termino;
      const clearBtn = document.getElementById('clear-compras-btn');
      if (clearBtn) clearBtn.style.display = 'block';
      const dropdown = document.getElementById('compras-autocomplete-dropdown');
      if (dropdown) dropdown.style.display = 'none';

      // Sincronizar select de subgiro y chip de macro-categoría
      const subgiroSel = document.getElementById('subgiro-select');
      if (subgiroSel) subgiroSel.value = item.subgiro_id;

      updateMacroChipsUI();
      applyCommerceFilters();
      showToast(`Filtrando por: ${item.termino} (${item.categoria_icono} ${item.subgiro_nombre})`, 'success', 3000);
    }

    function clearComprasSearch() {
      const input = document.getElementById('compras-search-input');
      if (input) input.value = '';
      const clearBtn = document.getElementById('clear-compras-btn');
      if (clearBtn) clearBtn.style.display = 'none';
      const dropdown = document.getElementById('compras-autocomplete-dropdown');
      if (dropdown) dropdown.style.display = 'none';

      filterState.product = null;
      applyCommerceFilters();
    }

    function toggleMacroCategory(catId) {
      if (filterState.macroCategory === catId) {
        filterState.macroCategory = null;
      } else {
        filterState.macroCategory = catId;
      }
      if (filterState.subgiro && filterState.macroCategory && window.MAP_DATA && window.MAP_DATA.catalog_subgiros) {
        const sg = window.MAP_DATA.catalog_subgiros.find(s => s.id === filterState.subgiro);
        if (sg && sg.categoria_id !== filterState.macroCategory) {
          filterState.subgiro = null;
          const subgiroSel = document.getElementById('subgiro-select');
          if (subgiroSel) subgiroSel.value = '';
        }
      }
      filterState.product = null;
      const input = document.getElementById('compras-search-input');
      if (input) input.value = '';
      const clearBtn = document.getElementById('clear-compras-btn');
      if (clearBtn) clearBtn.style.display = 'none';

      updateMacroChipsUI();
      applyCommerceFilters();
    }

    function updateMacroChipsUI() {
      const chips = document.querySelectorAll('.macro-chip');
      chips.forEach(chip => {
        const cid = chip.id.replace('macro-chip-', '');
        if (filterState.macroCategory === cid) {
          chip.classList.add('active');
        } else {
          chip.classList.remove('active');
        }
      });
    }

    function onSubgiroSelectChange(subgiroId) {
      if (!subgiroId) {
        filterState.subgiro = null;
      } else {
        filterState.subgiro = subgiroId;
        if (window.MAP_DATA && window.MAP_DATA.catalog_subgiros) {
          const sg = window.MAP_DATA.catalog_subgiros.find(s => s.id === subgiroId);
          if (sg) {
            filterState.macroCategory = sg.categoria_id;
            updateMacroChipsUI();
          }
        }
      }
      filterState.product = null;
      const input = document.getElementById('compras-search-input');
      if (input) input.value = '';
      const clearBtn = document.getElementById('clear-compras-btn');
      if (clearBtn) clearBtn.style.display = 'none';

      applyCommerceFilters();
    }

    function toggleFilterCanasta() {
      filterState.canastaBasica = !filterState.canastaBasica;
      const btn = document.getElementById('btn-toggle-canasta');
      if (btn) {
        btn.classList.toggle('active-canasta', filterState.canastaBasica);
      }
      applyCommerceFilters();
      showToast(filterState.canastaBasica ? '🛒 Canasta Básica SEDECO: Activado' : 'Canasta Básica: Desactivado', 'info', 2000);
    }

    function toggleFilterMercomuna() {
      filterState.mercomuna = !filterState.mercomuna;
      const btn = document.getElementById('btn-toggle-mercomuna');
      if (btn) {
        btn.classList.toggle('active-mercomuna', filterState.mercomuna);
      }
      applyCommerceFilters();
      showToast(filterState.mercomuna ? '💳 Vales Mercomuna: Activado' : 'Vales Mercomuna: Desactivado', 'info', 2000);
    }

    function resetAllCommerceFilters() {
      filterState.macroCategory = null;
      filterState.subgiro = null;
      filterState.product = null;
      filterState.canastaBasica = false;
      filterState.mercomuna = false;
      filterState.openToday = false;

      const input = document.getElementById('compras-search-input');
      if (input) input.value = '';
      const clearBtn = document.getElementById('clear-compras-btn');
      if (clearBtn) clearBtn.style.display = 'none';

      const sel = document.getElementById('subgiro-select');
      if (sel) sel.value = '';

      const btnCanasta = document.getElementById('btn-toggle-canasta');
      if (btnCanasta) btnCanasta.classList.remove('active-canasta');

      const btnMercomuna = document.getElementById('btn-toggle-mercomuna');
      if (btnMercomuna) btnMercomuna.classList.remove('active-mercomuna');

      const chipHoy = document.getElementById('chip-dia-hoy');
      if (chipHoy) chipHoy.classList.remove('active');

      updateMacroChipsUI();
      applyCommerceFilters();
      showToast('Filtros de compras restablecidos.', 'info', 2000);
    }

    function removeProductFilter() {
      filterState.product = null;
      const input = document.getElementById('compras-search-input');
      if (input) input.value = '';
      const clearBtn = document.getElementById('clear-compras-btn');
      if (clearBtn) clearBtn.style.display = 'none';
      applyCommerceFilters();
    }

    function removeSubgiroFilter() {
      filterState.subgiro = null;
      const sel = document.getElementById('subgiro-select');
      if (sel) sel.value = '';
      applyCommerceFilters();
    }

    function removeCategoryFilter() {
      filterState.macroCategory = null;
      updateMacroChipsUI();
      applyCommerceFilters();
    }

    function applyCommerceFilters() {
      if (!window.MAP_DATA) return;

      const days = ['DOMINGO', 'LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO'];
      const today = days[new Date().getDay()];

      let matchingMercados = [];
      let matchingTianguis = [];
      let matchingMSR = [];

      // 1. Mercados
      if (window.MAP_DATA.mercados) {
        window.MAP_DATA.mercados.forEach(m => {
          if (filterState.macroCategory && (!m.cats || !m.cats.includes(filterState.macroCategory))) return;
          if (filterState.subgiro && (!m.subgiros || !m.subgiros.includes(filterState.subgiro))) return;
          if (filterState.product && (!m.subgiros || !m.subgiros.includes(filterState.product.subgiro_id))) return;
          if (filterState.canastaBasica && !m.canasta_basica) return;
          if (filterState.mercomuna && !m.mercomuna) return;
          matchingMercados.push(m);
        });
      }

      // 2. Tianguis
      if (window.MAP_DATA.tianguis) {
        window.MAP_DATA.tianguis.forEach(t => {
          if (filterState.macroCategory && (!t.cats || !t.cats.includes(filterState.macroCategory))) return;
          if (filterState.subgiro && (!t.subgiros || !t.subgiros.includes(filterState.subgiro))) return;
          if (filterState.product && (!t.subgiros || !t.subgiros.includes(filterState.product.subgiro_id))) return;
          if (filterState.canastaBasica && !t.canasta_basica) return;
          if (filterState.mercomuna && !t.mercomuna) return;
          if (filterState.openToday && (!t.dia || !t.dia.toUpperCase().includes(today))) return;
          matchingTianguis.push(t);
        });
      }

      // 3. MSR
      if (window.MAP_DATA.msr) {
        window.MAP_DATA.msr.forEach(m => {
          if (filterState.macroCategory && (!m.cats || !m.cats.includes(filterState.macroCategory))) return;
          if (filterState.subgiro && (!m.subgiros || !m.subgiros.includes(filterState.subgiro))) return;
          if (filterState.product && (!m.subgiros || !m.subgiros.includes(filterState.product.subgiro_id))) return;
          if (filterState.canastaBasica && !m.canasta_basica) return;
          if (filterState.mercomuna && !m.mercomuna) return;
          if (filterState.openToday && (!m.dia || !m.dia.toUpperCase().includes(today))) return;
          matchingMSR.push(m);
        });
      }

      // Render Mercados en Cluster
      layers.mercados.clearLayers();
      matchingMercados.forEach(m => {
        const marker = L.circleMarker([m.lat, m.lon], {
          radius: m.radio || 7,
          fillColor: '#f59e0b',
          color: '#ffffff',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.88
        });
        marker.on('click', () => {
          currentSelectedTarget = { name: 'Mercado ' + m.nombre, lat: m.lat, lon: m.lon };
          map.flyTo([m.lat, m.lon], Math.max(map.getZoom(), 15), { duration: 0.8 });
          showMarketInDetail(m);
        });
        layers.mercados.addLayer(marker);
      });
      if (!map.hasLayer(layers.mercados)) layers.mercados.addTo(map);

      // Render Tianguis en Cluster
      layers.tianguis.clearLayers();
      matchingTianguis.forEach(t => {
        const marker = L.circleMarker([t.lat, t.lon], {
          radius: 5.5,
          fillColor: '#0f5953',
          color: '#ffffff',
          weight: 1.5,
          opacity: 1,
          fillOpacity: 0.85
        });
        marker.on('click', () => {
          currentSelectedTarget = { name: 'Tianguis ' + t.colonia, lat: t.lat, lon: t.lon };
          map.flyTo([t.lat, t.lon], Math.max(map.getZoom(), 15), { duration: 0.8 });
          showTianguisInDetail(t);
        });
        layers.tianguis.addLayer(marker);
      });
      if (!map.hasLayer(layers.tianguis)) layers.tianguis.addTo(map);

      // Render MSR
      layers.msr.clearLayers();
      matchingMSR.forEach(m => {
        const marker = L.circleMarker([m.lat, m.lon], {
          radius: m.radio || 6,
          fillColor: '#10b981',
          color: '#ffffff',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.88
        });
        marker.on('click', () => {
          currentSelectedTarget = { name: 'MSR ' + m.ruta, lat: m.lat, lon: m.lon };
          map.flyTo([m.lat, m.lon], Math.max(map.getZoom(), 15), { duration: 0.8 });
          showMSRInDetail(m);
        });
        layers.msr.addLayer(marker);
      });
      if (!map.hasLayer(layers.msr)) layers.msr.addTo(map);

      const total = matchingMercados.length + matchingTianguis.length + matchingMSR.length;
      updateFilterCounterAndPills(total, matchingMercados.length, matchingTianguis.length, matchingMSR.length);
    }

    function updateFilterCounterAndPills(total, countM, countT, countMSR) {
      const counterEl = document.getElementById('compras-results-counter');
      const resetBtn = document.getElementById('compras-reset-all-btn');
      const pillsContainer = document.getElementById('compras-active-pills');

      if (counterEl) {
        counterEl.innerHTML = `Mostrando <b>${total.toLocaleString()}</b> espacios (${countM} merc, ${countT} tian, ${countMSR} MSR)`;
      }

      const isAnyActive = filterState.macroCategory || filterState.subgiro || filterState.product || filterState.canastaBasica || filterState.mercomuna || filterState.openToday;

      if (resetBtn) {
        resetBtn.style.display = isAnyActive ? 'inline-block' : 'none';
      }

      if (pillsContainer) {
        let pillsHtml = '';
        if (filterState.product) {
          pillsHtml += `<span class="active-filter-pill">🛍️ ${filterState.product.termino} <span class="remove-pill" onclick="removeProductFilter()" title="Quitar">✕</span></span>`;
        }
        if (filterState.subgiro && window.MAP_DATA && window.MAP_DATA.catalog_subgiros) {
          const sg = window.MAP_DATA.catalog_subgiros.find(s => s.id === filterState.subgiro);
          const sgName = sg ? sg.nombre.split(',')[0] : filterState.subgiro;
          pillsHtml += `<span class="active-filter-pill">⚙️ ${sgName} <span class="remove-pill" onclick="removeSubgiroFilter()" title="Quitar">✕</span></span>`;
        }
        if (filterState.macroCategory && window.MAP_DATA && window.MAP_DATA.catalog_categorias) {
          const cat = window.MAP_DATA.catalog_categorias.find(c => c.id === filterState.macroCategory);
          const catName = cat ? `${cat.icono} ${cat.nombre.split(',')[0]}` : filterState.macroCategory;
          pillsHtml += `<span class="active-filter-pill">${catName} <span class="remove-pill" onclick="removeCategoryFilter()" title="Quitar">✕</span></span>`;
        }
        if (filterState.canastaBasica) {
          pillsHtml += `<span class="active-filter-pill" style="background:#ecfdf5; color:#065f46; border-color:#86efac;">🛒 Canasta Básica <span class="remove-pill" onclick="toggleFilterCanasta()" title="Quitar">✕</span></span>`;
        }
        if (filterState.mercomuna) {
          pillsHtml += `<span class="active-filter-pill" style="background:#faf5ff; color:#6b21a8; border-color:#d8b4fe;">💳 Mercomuna <span class="remove-pill" onclick="toggleFilterMercomuna()" title="Quitar">✕</span></span>`;
        }
        if (filterState.openToday) {
          pillsHtml += `<span class="active-filter-pill" style="background:#fef3c7; color:#92400e; border-color:#fde68a;">📅 Abierto Hoy <span class="remove-pill" onclick="filterByToday()" title="Quitar">✕</span></span>`;
        }
        pillsContainer.innerHTML = pillsHtml;
      }
    }

    function renderDetailPolicyAndSubgiros(item) {
      const policyBox = document.getElementById('panel-policy-badges');
      const subgirosBox = document.getElementById('panel-subgiros-box');
      const subgirosContent = document.getElementById('panel-subgiros-content');
      if (!policyBox || !subgirosContent) return;

      // 1. Badges de políticas y categorías
      let badgesHtml = '';
      if (item.canasta_basica) {
        badgesHtml += '<span class="badge-policy badge-canasta">🛒 Canasta Básica Oficial SEDECO</span>';
      }
      if (item.mercomuna) {
        badgesHtml += '<span class="badge-policy badge-mercomuna">💳 Acepta Vales Mercomuna</span>';
      }

      // Macro-categorías presentes
      if (item.cats && window.MAP_DATA && window.MAP_DATA.catalog_categorias) {
        const catMap = {};
        window.MAP_DATA.catalog_categorias.forEach(c => { catMap[c.id] = c; });
        item.cats.forEach(cid => {
          const c = catMap[cid];
          if (c) {
            badgesHtml += `<span class="badge-cat-mini" title="${c.nombre}">${c.icono} ${c.nombre.split(',')[0]}</span>`;
          }
        });
      }
      policyBox.innerHTML = badgesHtml;

      // 2. Subgiros disponibles
      if (item.subgiros && window.MAP_DATA && window.MAP_DATA.catalog_subgiros) {
        subgirosBox.style.display = 'block';
        const sgMap = {};
        window.MAP_DATA.catalog_subgiros.forEach(s => { sgMap[s.id] = s; });
        let subHtml = '';
        const displaySg = item.subgiros.slice(0, 10);
        displaySg.forEach(sid => {
          const s = sgMap[sid];
          if (s) {
            subHtml += `<span class="subgiro-pill">${s.canasta_basica ? '🛒 ' : ''}${s.nombre}</span>`;
          }
        });
        if (item.subgiros.length > 10) {
          subHtml += `<span class="subgiro-pill" style="background:#f1f5f9; color:#64748b;">+${item.subgiros.length - 10} giros más...</span>`;
        }
        subgirosContent.innerHTML = subHtml;
      } else {
        subgirosBox.style.display = 'none';
      }
    }

    // Tianguis con filtrado por día (retrocompatibilidad)
    function renderTianguisMarkers(filterDay = null) {
      if (filterDay) {
        filterState.openToday = true;
      }
      applyCommerceFilters();
    }

    // =========================================================================
    // BUSCADOR UNIFICADO CON AUTOCOMPLETADO PREDICTIVO
    // =========================================================================
    function buildUnifiedSearchIndex(data) {
      SEARCH_INDEX = [];
      if (data.mercados) {
        data.mercados.forEach(m => {
          SEARCH_INDEX.push({
            type: 'mercado',
            icon: '🏪',
            badge: 'MERCADO',
            badgeColor: '#d97706',
            title: 'Mercado ' + m.nombre,
            subtitle: m.alcaldia + ' · ' + m.colonia,
            lat: m.lat,
            lon: m.lon,
            data: m,
            searchStr: `mercado ${m.nombre} ${m.alcaldia} ${m.colonia}`.toLowerCase()
          });
        });
      }
      if (data.tianguis) {
        data.tianguis.forEach(t => {
          SEARCH_INDEX.push({
            type: 'tianguis',
            icon: '🧺',
            badge: 'TIANGUIS',
            badgeColor: '#0f5953',
            title: 'Tianguis ' + t.colonia,
            subtitle: t.alcaldia + ' · ' + t.dia + (t.ubicacion ? ' (' + t.ubicacion + ')' : ''),
            lat: t.lat,
            lon: t.lon,
            data: t,
            searchStr: `tianguis ${t.colonia} ${t.alcaldia} ${t.dia} ${t.ubicacion || ''}`.toLowerCase()
          });
        });
      }
      if (data.msr) {
        data.msr.forEach(m => {
          SEARCH_INDEX.push({
            type: 'msr',
            icon: '🚚',
            badge: 'MSR',
            badgeColor: '#10b981',
            title: 'MSR ' + m.ruta,
            subtitle: m.alcaldia + ' · ' + m.colonia + ' · ' + m.dia,
            lat: m.lat,
            lon: m.lon,
            data: m,
            searchStr: `msr ruta mercado sobre ruedas ${m.ruta} ${m.alcaldia} ${m.colonia} ${m.dia}`.toLowerCase()
          });
        });
      }
      if (data.metro_stations) {
        data.metro_stations.forEach(st => {
          SEARCH_INDEX.push({
            type: 'metro',
            icon: '🚇',
            badge: 'METRO',
            badgeColor: st.color || '#ef4444',
            title: 'Metro ' + st.nombre,
            subtitle: 'Línea ' + st.linea + ' · Alcaldía ' + st.alcaldia,
            lat: st.lat,
            lon: st.lon,
            data: st,
            searchStr: `metro estacion ${st.nombre} linea ${st.linea} ${st.alcaldia}`.toLowerCase()
          });
        });
      }
      if (data.metrobus_stations) {
        data.metrobus_stations.forEach(st => {
          SEARCH_INDEX.push({
            type: 'metrobus',
            icon: '🚍',
            badge: 'METROBÚS',
            badgeColor: '#ec4899',
            title: 'Metrobús ' + st.nombre,
            subtitle: st.linea + ' · Alcaldía ' + st.alcaldia,
            lat: st.lat,
            lon: st.lon,
            data: st,
            searchStr: `metrobus estacion ${st.nombre} ${st.linea} ${st.alcaldia}`.toLowerCase()
          });
        });
      }
    }

    const searchInput = document.getElementById('market-search');
    const searchDropdown = document.getElementById('search-autocomplete-dropdown');
    const clearSearchBtn = document.getElementById('clear-search-btn');
    let highlightedItemIdx = -1;

    searchInput.addEventListener('input', (e) => {
      const term = e.target.value.trim();
      if (!term) {
        searchDropdown.style.display = 'none';
        clearSearchBtn.style.display = 'none';
        return;
      }
      clearSearchBtn.style.display = 'block';
      renderAutocompleteDropdown(term);
    });

    searchInput.addEventListener('focus', (e) => {
      const term = e.target.value.trim();
      if (term) renderAutocompleteDropdown(term);
    });

    searchInput.addEventListener('keydown', (e) => {
      const items = searchDropdown.querySelectorAll('.autocomplete-item');
      if (items.length === 0 || searchDropdown.style.display === 'none') return;

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        highlightedItemIdx = (highlightedItemIdx + 1) % items.length;
        updateHighlightedItem(items);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        highlightedItemIdx = (highlightedItemIdx - 1 + items.length) % items.length;
        updateHighlightedItem(items);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (highlightedItemIdx >= 0 && highlightedItemIdx < items.length) {
          items[highlightedItemIdx].click();
        }
      } else if (e.key === 'Escape') {
        searchDropdown.style.display = 'none';
      }
    });

    function updateHighlightedItem(items) {
      items.forEach((el, idx) => {
        if (idx === highlightedItemIdx) {
          el.classList.add('selected');
          el.scrollIntoView({ block: 'nearest' });
        } else {
          el.classList.remove('selected');
        }
      });
    }

    function renderAutocompleteDropdown(query) {
      if (!SEARCH_INDEX || SEARCH_INDEX.length === 0) return;
      const terms = query.toLowerCase().split(/\\s+/).filter(Boolean);

      const matches = [];
      for (let item of SEARCH_INDEX) {
        const matchesAll = terms.every(t => item.searchStr.includes(t));
        if (matchesAll) {
          let score = 0;
          if (item.title.toLowerCase().startsWith(terms[0])) score += 30;
          if (item.title.toLowerCase().includes(terms[0])) score += 15;
          matches.push({ item, score });
        }
      }

      matches.sort((a, b) => b.score - a.score);
      const topMatches = matches.slice(0, 6).map(m => m.item);

      if (topMatches.length === 0) {
        searchDropdown.innerHTML = `
          <div style="padding:14px; text-align:center; color:#94a3b8; font-size:0.75rem;">
            No se encontraron coincidencias para "${query}".
          </div>
        `;
        searchDropdown.style.display = 'block';
        return;
      }

      searchDropdown.innerHTML = topMatches.map((item, idx) => `
        <div class="autocomplete-item" onclick="selectSearchItem(${idx})" data-idx="${idx}">
          <div class="autocomplete-badge" style="background:${item.badgeColor};">
            <span>${item.icon}</span>
            <span>${item.badge}</span>
          </div>
          <div class="autocomplete-text">
            <div class="autocomplete-title">${highlightMatch(item.title, query)}</div>
            <div class="autocomplete-sub">${highlightMatch(item.subtitle, query)}</div>
          </div>
        </div>
      `).join('');

      highlightedItemIdx = -1;
      searchDropdown.style.display = 'block';
      window._currentTopMatches = topMatches;
    }

    function highlightMatch(text, query) {
      if (!query) return text;
      const terms = query.split(/\\s+/).filter(Boolean);
      let res = text;
      terms.forEach(t => {
        const reg = new RegExp('(' + t.replace(/[-\\/\\\\^$*+?.()|[\\]{}]/g, '\\\\$&') + ')', 'gi');
        res = res.replace(reg, '<span class="autocomplete-highlight">$1</span>');
      });
      return res;
    }

    function selectSearchItem(idx) {
      if (!window._currentTopMatches || !window._currentTopMatches[idx]) return;
      const item = window._currentTopMatches[idx];
      searchInput.value = item.title;
      searchDropdown.style.display = 'none';

      currentSelectedTarget = { name: item.title, lat: item.lat, lon: item.lon };
      map.flyTo([item.lat, item.lon], 16, { duration: 1.0 });

      if (item.type === 'mercado') {
        showMarketInDetail(item.data);
      } else if (item.type === 'tianguis') {
        showTianguisInDetail(item.data);
      } else if (item.type === 'msr') {
        showMSRInDetail(item.data);
      } else if (item.type === 'metro' || item.type === 'metrobus') {
        showMetroStationInDetail(item.data);
      }

      openSidebarIfClosed();
      showToast(`Ubicado: ${item.title}`, 'info');
    }

    function clearUnifiedSearch() {
      searchInput.value = '';
      clearSearchBtn.style.display = 'none';
      searchDropdown.style.display = 'none';
      searchInput.focus();
    }

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.search-input-box') && !e.target.closest('#search-autocomplete-dropdown')) {
        searchDropdown.style.display = 'none';
      }
    });

    // =========================================================================
    // FICHA LATERAL (DETAIL CARD) REDISEÑADA Y DINÁMICA
    // =========================================================================
    function showMarketInDetail(m) {
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      document.getElementById('panel-tag').innerText = 'MERCADO PÚBLICO';
      document.getElementById('panel-tag').style.background = '#d97706';

      // Estado operativo dinámico
      const now = new Date();
      const hour = now.getHours();
      const pill = document.getElementById('panel-status-pill');
      const text = document.getElementById('panel-status-text');
      if (hour >= 8 && hour < 18) {
        pill.className = 'panel-status-pill status-open';
        text.innerText = '🟢 Abierto hoy hasta las 18:00 hrs';
      } else {
        pill.className = 'panel-status-pill status-closed';
        text.innerText = '🔴 Cerrado en este momento (Abre a las 08:00 hrs)';
      }

      document.getElementById('panel-name').innerText = 'Mercado ' + m.nombre;
      document.getElementById('panel-sub').innerText = m.alcaldia + ' · ' + m.colonia;

      document.getElementById('panel-stat1').innerText = m.locales || '--';
      document.getElementById('panel-lbl1').innerText = 'Locales';

      document.getElementById('panel-stat2').innerText = m.superficie_m2 > 0 ? (m.superficie_m2.toLocaleString() + ' m²') : 'N/D';
      document.getElementById('panel-lbl2').innerText = 'Superficie';

      document.getElementById('panel-closure-box').style.display = 'none';
      renderDetailPolicyAndSubgiros(m);

      // Conexión calculada con estación de metro más cercana
      const nearest = findClosestMetro(m.lat, m.lon);
      if (nearest && nearest.station) {
        const distM = Math.round(nearest.distance);
        const mins = Math.max(1, Math.round(distM / 75));
        document.getElementById('panel-conn').innerHTML = `
          <div style="font-weight:700; color:#0f5953; margin-bottom:2px;">
            🚇 Metro ${nearest.station.nombre} (Línea ${nearest.station.linea})
          </div>
          <div style="color:#64748b; font-size:0.72rem;">
            A pie: <b>${distM} metros (~${mins} min)</b> · Tarifa MI: $5.00 MXN.
          </div>
        `;
      } else {
        document.getElementById('panel-conn').innerHTML = `🚇 Conectado a la Red de Movilidad Integrada (MI).`;
      }

      openSidebarIfClosed();
    }

    function showTianguisInDetail(t) {
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      document.getElementById('panel-tag').innerText = 'TIANGUIS BARRIAL';
      document.getElementById('panel-tag').style.background = '#0f5953';

      const now = new Date();
      const days = ['DOMINGO', 'LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO'];
      const today = days[now.getDay()];
      const opensToday = t.dia && t.dia.toUpperCase().includes(today);

      const pill = document.getElementById('panel-status-pill');
      const text = document.getElementById('panel-status-text');
      if (opensToday) {
        pill.className = 'panel-status-pill status-open';
        text.innerText = `🟢 En operación hoy (${t.horario || '08:30 - 17:30'})`;
      } else {
        pill.className = 'panel-status-pill status-closed';
        text.innerText = `🔴 No opera hoy · Días asignados: ${t.dia}`;
      }

      document.getElementById('panel-name').innerText = 'Tianguis ' + t.colonia;
      document.getElementById('panel-sub').innerText = t.alcaldia + ' · ' + t.colonia;

      document.getElementById('panel-stat1').innerText = t.dia || '--';
      document.getElementById('panel-lbl1').innerText = 'Día de Instalación';

      document.getElementById('panel-stat2').innerText = t.horario || '08:30 - 17:30';
      document.getElementById('panel-lbl2').innerText = 'Horario de Venta';

      // Alerta de afectación vial
      const closureBox = document.getElementById('panel-closure-box');
      closureBox.style.display = 'block';
      document.getElementById('panel-closure-text').innerHTML = `
        <b>Vía ocupada:</b> ${t.ubicacion || 'Tramo barrial asignado'}<br>
        <span style="font-size:0.71rem; color:#78350f;">⚠️ Reducción y corte de circulación vehicular en día de tianguis.</span>
      `;
      renderDetailPolicyAndSubgiros(t);

      // Conexión calculada
      const nearest = findClosestMetro(t.lat, t.lon);
      if (nearest && nearest.station) {
        const distM = Math.round(nearest.distance);
        const mins = Math.max(1, Math.round(distM / 75));
        document.getElementById('panel-conn').innerHTML = `
          <div style="font-weight:700; color:#0f5953; margin-bottom:2px;">
            🚇 Metro ${nearest.station.nombre} (Línea ${nearest.station.linea})
          </div>
          <div style="color:#64748b; font-size:0.72rem;">
            A pie: <b>${distM} metros (~${mins} min)</b> · Tarifa MI: $5.00 MXN.
          </div>
        `;
      } else {
        document.getElementById('panel-conn').innerHTML = `Conexión con rutas secundarias de transporte concesionado.`;
      }

      openSidebarIfClosed();
    }

    function showMSRInDetail(m) {
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      document.getElementById('panel-tag').innerText = 'MERCADO SOBRE RUEDAS';
      document.getElementById('panel-tag').style.background = '#10b981';

      const now = new Date();
      const days = ['DOMINGO', 'LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO'];
      const today = days[now.getDay()];
      const opensToday = m.dia && m.dia.toUpperCase().includes(today);

      const pill = document.getElementById('panel-status-pill');
      const text = document.getElementById('panel-status-text');
      if (opensToday) {
        pill.className = 'panel-status-pill status-open';
        text.innerText = `🟢 En ruta hoy (${m.dia})`;
      } else {
        pill.className = 'panel-status-pill status-closed';
        text.innerText = `🔴 Sede inactiva hoy · Día: ${m.dia}`;
      }

      document.getElementById('panel-name').innerText = m.ruta + ' (' + m.colonia + ')';
      document.getElementById('panel-sub').innerText = m.alcaldia + ' · ' + (m.direccion || m.colonia);

      document.getElementById('panel-stat1').innerText = m.dia || '--';
      document.getElementById('panel-lbl1').innerText = 'Día en esta Sede';

      document.getElementById('panel-stat2').innerText = m.oferentes ? (m.oferentes + ' puestos') : 'Itinerante';
      document.getElementById('panel-lbl2').innerText = 'Oferentes';

      document.getElementById('panel-closure-box').style.display = 'none';
      renderDetailPolicyAndSubgiros(m);

      document.getElementById('panel-conn').innerHTML = `
        <b>Circuito Itinerante SEDECO:</b> Se traslada diariamente de colonia para llevar abasto a precio accesible.
      `;

      openSidebarIfClosed();
    }

    function showMetroStationInDetail(st) {
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      const pol = document.getElementById('panel-policy-badges');
      if (pol) pol.innerHTML = '';
      const sgBox = document.getElementById('panel-subgiros-box');
      if (sgBox) sgBox.style.display = 'none';

      document.getElementById('panel-tag').innerText = st.tipo || 'ESTACIÓN RED MI';
      document.getElementById('panel-tag').style.background = st.color || '#ef4444';

      const pill = document.getElementById('panel-status-pill');
      const text = document.getElementById('panel-status-text');
      pill.className = 'panel-status-pill status-open';
      text.innerText = '🟢 En servicio · Tarjeta MI';

      document.getElementById('panel-name').innerText = (st.tipo ? st.tipo + ' ' : 'Estación ') + st.nombre;
      document.getElementById('panel-sub').innerText = (st.linea ? st.linea + ' · ' : '') + 'Alcaldía ' + (st.alcaldia || 'CDMX');

      document.getElementById('panel-stat1').innerText = st.color === '#ec4899' ? '$6.00 MXN' : '$5.00 MXN';
      document.getElementById('panel-lbl1').innerText = 'Tarifa Oficial';

      document.getElementById('panel-stat2').innerText = st.linea || 'Red MI';
      document.getElementById('panel-lbl2').innerText = 'Línea / Corredor';

      document.getElementById('panel-closure-box').style.display = 'none';

      document.getElementById('panel-conn').innerHTML = `
        Estación clave de transbordo e interconexión con mercados públicos y tianguis barriales.
      `;

      openSidebarIfClosed();
    }

    function showTransportInDetail(p) {
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      document.getElementById('panel-tag').innerText = p.agency_name || 'TRANSPORTE CONCESIONADO';
      document.getElementById('panel-tag').style.background = p.color || '#64748b';

      const pill = document.getElementById('panel-status-pill');
      const text = document.getElementById('panel-status-text');
      pill.className = 'panel-status-pill status-open';
      text.innerText = '🟢 Corredor en operación continua';

      document.getElementById('panel-name').innerText = (p.route_short || '') + ' ' + (p.route_long || 'Corredor');
      document.getElementById('panel-sub').innerText = 'Destino: ' + (p.headsign || 'Servicio de Conexión Barrial');

      document.getElementById('panel-stat1').innerText = p.agency === 'METRO' ? '$5.00' : (p.agency === 'MB' ? '$6.00' : (p.agency === 'CC' ? '$6.00-$8.50' : '$2.00-$4.00'));
      document.getElementById('panel-lbl1').innerText = 'Tarifa';

      document.getElementById('panel-stat2').innerText = p.agency === 'CC' ? 'Efectivo / Tarjeta MI' : 'Tarjeta MI';
      document.getElementById('panel-lbl2').innerText = 'Método de Pago';

      document.getElementById('panel-closure-box').style.display = 'none';

      document.getElementById('panel-conn').innerHTML = `
        <b>Corredor Alimentador:</b> Brinda cobertura de última milla penetrando en colonias para conectar hogares con mercados.
      `;

      openSidebarIfClosed();
    }

    function closeDetailCard() {
      document.getElementById('detail-card').style.display = 'none';
    }

    function copyCurrentCoords() {
      if (currentSelectedTarget && currentSelectedTarget.lat && currentSelectedTarget.lon) {
        const text = `${currentSelectedTarget.lat.toFixed(5)}, ${currentSelectedTarget.lon.toFixed(5)}`;
        navigator.clipboard.writeText(text).then(() => {
          showToast(`Coordenadas copiadas: ${text}`, 'success', 3000);
        }).catch(() => {
          showToast(`Coordenadas: ${text}`, 'info', 4000);
        });
      } else {
        showToast('Selecciona primero un mercado o tianguis en el mapa.', 'warning');
      }
    }

    // =========================================================================
    // MODALES MODERNOS CON PESTAÑAS (REEMPLAZO TOTAL DE WINDOW.ALERT)
    // =========================================================================
    function openInfoModal(initialTab = 'closures') {
      const modal = document.getElementById('info-modal-overlay');
      modal.classList.add('active');
      switchModalTab(initialTab);
    }

    function closeInfoModal() {
      const modal = document.getElementById('info-modal-overlay');
      modal.classList.remove('active');
    }

    function handleModalOverlayClick(e) {
      if (e.target.id === 'info-modal-overlay') {
        closeInfoModal();
      }
    }

    function switchModalTab(tabName) {
      const tabs = ['closures', 'hours', 'fares', 'today'];
      tabs.forEach(t => {
        const btn = document.getElementById('tab-btn-' + t);
        const pane = document.getElementById('tab-pane-' + t);
        if (btn) btn.classList.toggle('active', t === tabName);
        if (pane) pane.classList.toggle('active', t === tabName);
      });
    }

    function updateTodayModalInfo() {
      const banner = document.getElementById('modal-today-banner');
      if (!banner) return;
      const now = new Date();
      const days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
      const today = days[now.getDay()];
      const todayUpper = today.toUpperCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");

      let countToday = 0;
      if (window.MAP_DATA && window.MAP_DATA.tianguis) {
        countToday = window.MAP_DATA.tianguis.filter(t => t.dia && t.dia.toUpperCase().includes(todayUpper)).length;
      }

      banner.innerHTML = `
        <div style="font-weight:800; font-size:0.95rem; color:#0f5953; margin-bottom:4px;">
          📅 Hoy es ${today}: ${countToday} tianguis en operación
        </div>
        <div style="font-size:0.75rem; color:#334155; line-height:1.45;">
          Los 329 mercados públicos están abiertos en su horario habitual (08:00 a 18:00 hrs). Puedes enfocar el mapa únicamente en los puntos que abren hoy pulsando el botón inferior.
        </div>
      `;
    }

    function filterByToday() {
      filterState.openToday = !filterState.openToday;
      const chip = document.getElementById('chip-dia-hoy');
      if (chip) chip.classList.toggle('active', filterState.openToday);
      applyCommerceFilters();
      const days = ['DOMINGO', 'LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO'];
      const today = days[new Date().getDay()];
      showToast(filterState.openToday ? `Filtro activo: mostrando espacios que abren hoy (${today}).` : 'Filtro de día desactivado.', 'info', 3000);
    }

    // =========================================================================
    // SISTEMA DE NOTIFICACIONES TOAST FLOTANTES
    // =========================================================================
    function showToast(message, type = 'info', duration = 3500) {
      const container = document.getElementById('toast-container');
      if (!container) return;

      const icons = {
        success: '✅',
        warning: '⚠️',
        error: '❌',
        info: 'ℹ️'
      };

      const toast = document.createElement('div');
      toast.className = `toast-item toast-${type}`;
      toast.innerHTML = `
        <span style="font-size:1.1rem; flex-shrink:0;">${icons[type] || 'ℹ️'}</span>
        <span style="flex:1;">${message}</span>
      `;

      container.appendChild(toast);

      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(15px)';
        setTimeout(() => toast.remove(), 300);
      }, duration);
    }

    // =========================================================================
    // GEOLOCALIZACIÓN Y MI UBICACIÓN (PUNTO AZUL PULSANTE)
    // =========================================================================
    let userCurrentCoords = [19.4326, -99.1332]; // Default Zócalo si no activa GPS
    function locateUser() {
      showToast('Obteniendo tu ubicación GPS...', 'info', 2000);
      map.locate({ setView: true, maxZoom: 15, enableHighAccuracy: true });
    }

    map.on('locationfound', function(e) {
      userCurrentCoords = [e.latlng.lat, e.latlng.lng];
      layers.userLocation.clearLayers();

      const blueDotHtml = `
        <div style="position:relative; width:16px; height:16px;">
          <div class="user-gps-pulse-halo"></div>
          <div class="user-gps-blue-dot"></div>
        </div>
      `;
      const blueDotIcon = L.divIcon({
        className: 'user-gps-container',
        html: blueDotHtml,
        iconSize: [16, 16],
        iconAnchor: [8, 8]
      });

      const marker = L.marker(e.latlng, { icon: blueDotIcon });
      marker.on('click', () => {
        showToast(`📍 Tu ubicación actual (Precisión +/- ${Math.round(e.accuracy)} m)`, 'info');
      });

      const radiusCircle = L.circle(e.latlng, {
        radius: e.accuracy,
        color: '#2563eb',
        weight: 1,
        fillColor: '#3b82f6',
        fillOpacity: 0.12
      });

      layers.userLocation.addLayer(radiusCircle);
      layers.userLocation.addLayer(marker);
      showToast('Ubicación fijada con éxito en el mapa.', 'success', 3000);
    });

    map.on('locationerror', function(err) {
      showToast('Activa los permisos de ubicación en tu navegador para ver tu punto azul.', 'warning', 4500);
    });

    // =========================================================================
    // GESTIÓN DE CAPAS Y MODO RUTA LIMPIA (FOCUS MODE)
    // =========================================================================
    const ALL_DATA_LAYERS = [
      'zmvm', 'alcaldias', 'metro', 'metro_icons', 'metrobus', 'metrobus_icons',
      'rtp', 'cablebus', 'trolebus', 'tren', 'concesionado',
      'mercados', 'msr', 'tianguis'
    ];
    let isFocusRouteMode = false;
    let savedActiveLayers = [];

    function enterRouteFocusMode(originLabel, destLabel) {
      if (!isFocusRouteMode) {
        savedActiveLayers = ALL_DATA_LAYERS.filter(k => layers[k] && map.hasLayer(layers[k]));
        savedActiveLayers.forEach(k => map.removeLayer(layers[k]));
        isFocusRouteMode = true;
      }
      document.getElementById('route-focus-banner').style.display = 'flex';
      document.getElementById('focus-banner-text').innerText = `${originLabel} ➔ ${destLabel}`;
    }

    function exitRouteFocusMode() {
      if (isFocusRouteMode) {
        savedActiveLayers.forEach(k => {
          if (layers[k]) map.addLayer(layers[k]);
        });
        isFocusRouteMode = false;
      }
      layers.routeLines.clearLayers();
      document.getElementById('route-focus-banner').style.display = 'none';
      document.getElementById('route-result-box').style.display = 'none';
      resetMapView();
      showToast('Mapa completo restaurado con todas las capas.', 'info', 3000);
    }

    // =========================================================================
    // GRAFO DEL METRO CDMX Y PLANIFICADOR DE RUTAS INTERACTIVO (A -> B)
    // =========================================================================
    const METRO_GRAPH = {
      lines: {},
      adj: {},
      built: false,
      build: function() {
        if (this.built || !window.MAP_DATA || !window.MAP_DATA.metro_stations) return;
        
        window.MAP_DATA.metro_stations.forEach(st => {
          if (!this.lines[st.linea]) this.lines[st.linea] = [];
          this.lines[st.linea].push(st);
        });

        const addEdge = (u, v, cost, line) => {
          if (!this.adj[u]) this.adj[u] = [];
          if (!this.adj[v]) this.adj[v] = [];
          this.adj[u].push({ target: v, cost: cost, line: line });
          this.adj[v].push({ target: u, cost: cost, line: line });
        };

        Object.keys(this.lines).forEach(lId => {
          const stList = this.lines[lId];
          for (let i = 0; i < stList.length - 1; i++) {
            const u = stList[i].nombre + '||' + lId;
            const v = stList[i+1].nombre + '||' + lId;
            addEdge(u, v, 1.8, lId);
          }
        });

        const nameMap = {};
        window.MAP_DATA.metro_stations.forEach(st => {
          const baseName = st.nombre.split('/')[0].trim().toLowerCase();
          if (!nameMap[baseName]) nameMap[baseName] = [];
          nameMap[baseName].push(st);
        });

        Object.keys(nameMap).forEach(base => {
          const list = nameMap[base];
          if (list.length > 1) {
            for (let i = 0; i < list.length; i++) {
              for (let j = i + 1; j < list.length; j++) {
                const u = list[i].nombre + '||' + list[i].linea;
                const v = list[j].nombre + '||' + list[j].linea;
                addEdge(u, v, 3.5, 'TRANSB');
              }
            }
          }
        });

        this.built = true;
      },
      findPath: function(startStation, endStation) {
        this.build();
        const startKey = startStation.nombre + '||' + startStation.linea;
        const endKey = endStation.nombre + '||' + endStation.linea;

        if (startKey === endKey) return [startStation];

        const dist = {};
        const prev = {};
        const visited = new Set();
        dist[startKey] = 0;
        const pq = [{ node: startKey, cost: 0 }];

        while (pq.length > 0) {
          let minIdx = 0;
          for (let i = 1; i < pq.length; i++) {
            if (pq[i].cost < pq[minIdx].cost) minIdx = i;
          }
          const { node: u, cost: c } = pq.splice(minIdx, 1)[0];
          if (visited.has(u)) continue;
          visited.add(u);

          if (u === endKey) {
            const pathKeys = [];
            let curr = u;
            while (curr) {
              pathKeys.unshift(curr);
              curr = prev[curr];
            }
            return pathKeys.map(k => {
              const [n, l] = k.split('||');
              return window.MAP_DATA.metro_stations.find(st => st.nombre === n && st.linea === l);
            }).filter(Boolean);
          }

          const neighbors = this.adj[u] || [];
          for (let edge of neighbors) {
            const v = edge.target;
            const newCost = c + edge.cost;
            if (dist[v] === undefined || newCost < dist[v]) {
              dist[v] = newCost;
              prev[v] = u;
              pq.push({ node: v, cost: newCost });
            }
          }
        }
        return null;
      }
    };

    function setAsRouteDestination() {
      if (currentSelectedTarget) {
        document.getElementById('route-to').value = currentSelectedTarget.name;
        openSidebarIfClosed();
        calculateRouteUI();
      }
    }

    function findDestinationTarget(query) {
      const q = query.toLowerCase().trim();
      if (!q) return null;

      if (currentSelectedTarget && currentSelectedTarget.name.toLowerCase().includes(q)) {
        return {
          name: currentSelectedTarget.name,
          lat: currentSelectedTarget.lat,
          lon: currentSelectedTarget.lon,
          type: 'Seleccionado'
        };
      }

      if (window.MAP_DATA) {
        for (let m of (window.MAP_DATA.mercados || [])) {
          if (m.nombre.toLowerCase().includes(q) || q.includes(m.nombre.toLowerCase())) {
            return {
              name: 'Mercado ' + m.nombre,
              lat: m.lat,
              lon: m.lon,
              type: 'Mercado Público'
            };
          }
        }
        for (let t of (window.MAP_DATA.tianguis || [])) {
          if (t.colonia.toLowerCase().includes(q) || (t.ubicacion && t.ubicacion.toLowerCase().includes(q))) {
            return {
              name: 'Tianguis ' + t.colonia,
              lat: t.lat,
              lon: t.lon,
              type: 'Tianguis Móvil'
            };
          }
        }
        for (let m of (window.MAP_DATA.msr || [])) {
          if (m.ruta.toLowerCase().includes(q) || m.colonia.toLowerCase().includes(q)) {
            return {
              name: 'MSR ' + m.ruta,
              lat: m.lat,
              lon: m.lon,
              type: 'Mercado Sobre Ruedas'
            };
          }
        }
        for (let st of (window.MAP_DATA.metro_stations || [])) {
          if (st.nombre.toLowerCase().includes(q)) {
            return {
              name: 'Metro ' + st.nombre,
              lat: st.lat,
              lon: st.lon,
              type: 'Estación Metro'
            };
          }
        }
      }

      return {
        name: query,
        lat: 19.4168,
        lon: -99.1252,
        type: 'Mercado Jamaica (Default)'
      };
    }

    function calculateRouteUI() {
      const fromVal = document.getElementById('route-from').value.trim();
      const toVal = document.getElementById('route-to').value.trim();
      const resultBox = document.getElementById('route-result-box');
      const titleEl = document.getElementById('route-summary-title');
      const contentEl = document.getElementById('route-summary-content');

      let startCoords = userCurrentCoords;
      let originName = 'Tu Ubicación Actual';
      if (fromVal.toLowerCase() !== 'mi ubicación' && fromVal.length > 0) {
        const customOrigin = findDestinationTarget(fromVal);
        if (customOrigin) {
          startCoords = [customOrigin.lat, customOrigin.lon];
          originName = customOrigin.name;
        }
      }

      let destTarget = findDestinationTarget(toVal);
      if (!destTarget) {
        showToast('Por favor escribe un destino válido (ej. Mercado Jamaica, Tepito).', 'warning');
        return;
      }
      const endCoords = [destTarget.lat, destTarget.lon];

      let nearestMetroStart = findClosestMetro(startCoords[0], startCoords[1]);
      let nearestMetroEnd = findClosestMetro(endCoords[0], endCoords[1]);

      if (!nearestMetroStart || !nearestMetroEnd) {
        showToast('No se encontraron estaciones cercanas para trazar la ruta.', 'error');
        return;
      }

      enterRouteFocusMode(originName, destTarget.name);
      layers.routeLines.clearLayers();

      const metroPath = METRO_GRAPH.findPath(nearestMetroStart.station, nearestMetroEnd.station);
      const stationSequence = (metroPath && metroPath.length > 0) ? metroPath : [nearestMetroStart.station, nearestMetroEnd.station];

      // Pin Origen
      const originMarker = L.marker(startCoords, {
        icon: L.divIcon({
          className: 'route-pin-container',
          html: '<div style="background:#2563eb; color:#fff; width:26px; height:26px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; border:2px solid #fff; box-shadow:0 3px 8px rgba(0,0,0,0.3); font-size:12px;">A</div>',
          iconSize: [26, 26],
          iconAnchor: [13, 13]
        })
      });
      layers.routeLines.addLayer(originMarker);

      // Tramo 1: Caminata inicial
      const walkDist1 = Math.round(getDistMeters(startCoords[0], startCoords[1], nearestMetroStart.station.lat, nearestMetroStart.station.lon));
      const walkMin1 = Math.max(1, Math.round(walkDist1 / 75));
      const walk1 = L.polyline([startCoords, [nearestMetroStart.station.lat, nearestMetroStart.station.lon]], {
        color: '#2563eb',
        weight: 4,
        dashArray: '6, 6',
        opacity: 0.95
      });
      layers.routeLines.addLayer(walk1);

      // Estación de abordaje
      const boardGlyph = nearestMetroStart.station.has_glyph ? `<em class="${nearestMetroStart.station.icon_class}"></em>` : `<span style="font-size:9px; font-weight:800; color:#fff;">M</span>`;
      const boardMarker = L.marker([nearestMetroStart.station.lat, nearestMetroStart.station.lon], {
        icon: L.divIcon({
          className: 'route-station-container',
          html: `<div style="background:${nearestMetroStart.station.color}; width:28px; height:28px; border-radius:6px; display:flex; align-items:center; justify-content:center; border:2px solid #fff; box-shadow:0 4px 10px rgba(0,0,0,0.3);">${boardGlyph}</div>`,
          iconSize: [28, 28],
          iconAnchor: [14, 14]
        })
      });
      layers.routeLines.addLayer(boardMarker);

      // Trazado de metro y transbordos
      const lineSegments = [];
      let currentSegment = [];
      let currentLine = stationSequence[0].linea;
      let currentColor = stationSequence[0].color || '#ef4444';
      let transfersCount = 0;
      let transferSteps = [];

      for (let i = 0; i < stationSequence.length; i++) {
        const st = stationSequence[i];
        if (st.linea !== currentLine) {
          transfersCount++;
          transferSteps.push(`Transbordo en <b>${st.nombre}</b> hacia Línea ${st.linea}`);
          lineSegments.push({ line: currentLine, color: currentColor, coords: currentSegment });
          currentSegment = [[st.lat, st.lon]];
          currentLine = st.linea;
          currentColor = st.color || '#ef4444';

          const transbMarker = L.marker([st.lat, st.lon], {
            icon: L.divIcon({
              className: 'route-transb-container',
              html: `<div style="background:#ffffff; color:#0f172a; width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; border:2px solid ${currentColor}; font-size:10px; box-shadow:0 2px 6px rgba(0,0,0,0.25);">⇄</div>`,
              iconSize: [22, 22],
              iconAnchor: [11, 11]
            })
          });
          layers.routeLines.addLayer(transbMarker);
        } else {
          currentSegment.push([st.lat, st.lon]);
          if (i > 0 && i < stationSequence.length - 1) {
            const dotMarker = L.circleMarker([st.lat, st.lon], {
              radius: 4,
              fillColor: '#ffffff',
              color: currentColor,
              weight: 2,
              fillOpacity: 1
            });
            layers.routeLines.addLayer(dotMarker);
          }
        }
      }
      if (currentSegment.length > 0) {
        lineSegments.push({ line: currentLine, color: currentColor, coords: currentSegment });
      }

      lineSegments.forEach(seg => {
        if (seg.coords.length >= 2) {
          const tLine = L.polyline(seg.coords, {
            color: seg.color,
            weight: 6,
            opacity: 0.95
          });
          layers.routeLines.addLayer(tLine);
        }
      });

      // Estación de descenso
      const alightGlyph = nearestMetroEnd.station.has_glyph ? `<em class="${nearestMetroEnd.station.icon_class}"></em>` : `<span style="font-size:9px; font-weight:800; color:#fff;">M</span>`;
      const alightMarker = L.marker([nearestMetroEnd.station.lat, nearestMetroEnd.station.lon], {
        icon: L.divIcon({
          className: 'route-station-container',
          html: `<div style="background:${nearestMetroEnd.station.color}; width:28px; height:28px; border-radius:6px; display:flex; align-items:center; justify-content:center; border:2px solid #fff; box-shadow:0 4px 10px rgba(0,0,0,0.3);">${alightGlyph}</div>`,
          iconSize: [28, 28],
          iconAnchor: [14, 14]
        })
      });
      layers.routeLines.addLayer(alightMarker);

      // Tramo final
      const walkDist2 = Math.round(getDistMeters(nearestMetroEnd.station.lat, nearestMetroEnd.station.lon, endCoords[0], endCoords[1]));
      const walkMin2 = Math.max(1, Math.round(walkDist2 / 75));
      const walk2 = L.polyline([[nearestMetroEnd.station.lat, nearestMetroEnd.station.lon], endCoords], {
        color: '#16a34a',
        weight: 4,
        dashArray: '6, 6',
        opacity: 0.95
      });
      layers.routeLines.addLayer(walk2);

      // Pin Destino
      const destMarker = L.marker(endCoords, {
        icon: L.divIcon({
          className: 'route-pin-container',
          html: '<div style="background:#16a34a; color:#fff; width:26px; height:26px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; border:2px solid #fff; box-shadow:0 3px 8px rgba(0,0,0,0.3); font-size:12px;">B</div>',
          iconSize: [26, 26],
          iconAnchor: [13, 13]
        })
      });
      layers.routeLines.addLayer(destMarker);

      const bounds = L.latLngBounds([startCoords, endCoords, [nearestMetroStart.station.lat, nearestMetroStart.station.lon], [nearestMetroEnd.station.lat, nearestMetroEnd.station.lon]]);
      map.fitBounds(bounds, { padding: [60, 60] });

      const transitTimeMin = Math.round(stationSequence.length * 2.2 + transfersCount * 4.5);
      const totalTimeMin = walkMin1 + transitTimeMin + walkMin2;
      const co2Kg = (totalTimeMin * 0.025).toFixed(2);

      titleEl.innerText = `${totalTimeMin} min · Ruta Sustentable`;
      let stepsHtml = `
        <div style="margin-bottom:8px;">
          <b>Trayecto:</b> ${originName} ➔ ${destTarget.name}
        </div>
        <div style="display:flex; gap:6px; margin-bottom:8px; flex-wrap:wrap;">
          <span style="background:#e0e7ff; color:#3730a3; font-weight:700; font-size:0.7rem; padding:2px 6px; border-radius:4px;">🚶 ${walkDist1}m (${walkMin1} min)</span>
          <span style="background:#fce7f3; color:#9d174d; font-weight:700; font-size:0.7rem; padding:2px 6px; border-radius:4px;">🚇 ${stationSequence.length} estaciones (${transitTimeMin} min)</span>
          <span style="background:#dcfce7; color:#166534; font-weight:700; font-size:0.7rem; padding:2px 6px; border-radius:4px;">🚶 ${walkDist2}m (${walkMin2} min)</span>
        </div>
        <ol style="padding-left:18px; margin-bottom:8px; font-size:0.75rem; color:#475569;">
          <li>Camina hacia <b>Metro ${nearestMetroStart.station.nombre}</b> (${walkDist1}m).</li>
          <li>Aborda en dirección adecuada (Línea ${nearestMetroStart.station.linea}).</li>
          ${transferSteps.map(s => `<li>${s}</li>`).join('')}
          <li>Desciende en <b>Metro ${nearestMetroEnd.station.nombre}</b>.</li>
          <li>Camina <b>${walkDist2}m</b> hasta llegar a <b>${destTarget.name}</b>.</li>
        </ol>
        <div style="background:#f8fafc; padding:6px 8px; border-radius:6px; border:1px solid #e2e8f0; font-size:0.7rem; color:#64748b;">
          🌱 <b>Impacto:</b> Ahorras ~${co2Kg} kg de CO2 comparado con uso de automóvil particular. Tarifa: <b>$5.00 MXN</b>.
        </div>
      `;
      contentEl.innerHTML = stepsHtml;
      resultBox.style.display = 'block';
      showToast(`Ruta calculada: ${totalTimeMin} min hacia ${destTarget.name}`, 'success');
    }

    function findClosestMetro(lat, lon) {
      if (!window.MAP_DATA || !window.MAP_DATA.metro_stations) return null;
      let nearest = null;
      let minD = Infinity;
      window.MAP_DATA.metro_stations.forEach(st => {
        const d = getDistMeters(lat, lon, st.lat, st.lon);
        if (d < minD) {
          minD = d;
          nearest = st;
        }
      });
      return nearest ? { station: nearest, distance: minD } : null;
    }

    function getDistMeters(lat1, lon1, lat2, lon2) {
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
    }

    // =========================================================================
    // CONTROLES DE INTERFAZ Y SIDEBAR
    // =========================================================================
    function toggleSidebar() {
      const sb = document.getElementById('sidebar');
      const btn = document.getElementById('btn-open-sidebar');
      sb.classList.toggle('collapsed');
      if (sb.classList.contains('collapsed')) {
        btn.style.display = 'flex';
      } else {
        btn.style.display = 'none';
      }
      setTimeout(() => map.invalidateSize(), 300);
    }

    function openSidebarIfClosed() {
      const sb = document.getElementById('sidebar');
      const btn = document.getElementById('btn-open-sidebar');
      if (sb.classList.contains('collapsed')) {
        sb.classList.remove('collapsed');
        btn.style.display = 'none';
        setTimeout(() => map.invalidateSize(), 300);
      }
    }

    function resetMapView() {
      map.setView([19.4326, -99.1332], 12);
    }

    function toggleTransportDropdown(e) {
      e.stopPropagation();
      const menu = document.getElementById('transport-dropdown-menu');
      if (menu.style.display === 'flex') {
        menu.style.display = 'none';
      } else {
        const btn = e.currentTarget;
        const rect = btn.getBoundingClientRect();
        menu.style.top = (rect.bottom + 6) + 'px';
        menu.style.left = Math.min(rect.left, window.innerWidth - 240) + 'px';
        menu.style.display = 'flex';
      }
    }

    document.addEventListener('click', (e) => {
      const menu = document.getElementById('transport-dropdown-menu');
      if (menu && menu.style.display === 'flex' && !e.target.closest('#transport-dropdown-menu') && !e.target.closest('.btn-dropdown-main')) {
        menu.style.display = 'none';
      }
    });

    function toggleSubsystem(agency) {
      const fg = transportMapping[agency];
      if (map.hasLayer(fg)) {
        map.removeLayer(fg);
        showToast(`Capa oculta: ${agency}`, 'info', 2000);
      } else {
        map.addLayer(fg);
        showToast(`Capa visible: ${agency}`, 'success', 2000);
      }
    }

    function toggleLayer(layerKey) {
      const chip = document.getElementById('chip-' + layerKey);
      const fg = layers[layerKey];
      if (!fg) return;

      if (map.hasLayer(fg)) {
        map.removeLayer(fg);
        if (chip) chip.classList.remove('active');
        showToast(`Capa oculta: ${layerKey}`, 'info', 2000);
      } else {
        map.addLayer(fg);
        if (chip) chip.classList.add('active');
        showToast(`Capa activa: ${layerKey}`, 'success', 2000);
      }
    }

    // Iniciar aplicación
    window.addEventListener('DOMContentLoaded', () => {
      initApplication();
    });
  </script>
</body>
</html>
"""

full_html = html_head + html_body
with open('mapa_comercio_movilidad_cdmx.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Generated mapa_comercio_movilidad_cdmx.html successfully! Size:", len(full_html))
