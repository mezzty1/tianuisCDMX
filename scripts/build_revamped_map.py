import os
import json
import re

def build_map_html():
    print("Iniciando generación de mapa_comercio_movilidad_cdmx.html 100% enfocado en Comercio Popular y Barrial...")

    # Cargar estadísticas de cierres viales
    cierres_stats = {}
    cierres_dias = {}
    if os.path.exists('data/processed/cierres_viales_por_dia.json'):
        try:
            with open('data/processed/cierres_viales_por_dia.json', 'r', encoding='utf-8') as f:
                c_data = json.load(f)
                cierres_stats = c_data.get('resumen_semanal', {})
                cierres_dias = c_data.get('dias', {})
        except Exception as e:
            print("Notice: error al leer cierres_viales_por_dia.json:", e)

    cierres_json_str = json.dumps({'resumen_semanal': cierres_stats, 'dias': cierres_dias}, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Comercio Popular y Barrial CDMX · Tianguis, MSR y Concentraciones</title>

  <!-- Google Fonts: Montserrat -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">
  <!-- Leaflet MarkerCluster CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css">
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css">

  <style>
    :root {{
      --cdmx-green-dark: #0f5953;
      --cdmx-green-primary: #116962;
      --cdmx-green-light: #eef7f6;
      --cdmx-green-chip: #d5ece9;
      --cdmx-teal: #0f766e;
      --cdmx-teal-light: #ccfbf1;
      --cdmx-amber: #d97706;
      --cdmx-amber-light: #fef3c7;
      --cdmx-purple: #6d28d9;
      --cdmx-purple-light: #ede9fe;
      --cdmx-wine: #9f2241;
      --cdmx-gold: #bc955c;
      --cdmx-bg: #f8fafc;
      --cdmx-text-dark: #092c29;
      --cdmx-text-muted: #527370;
      --cdmx-border: #d4e7e5;
      --shadow-sidebar: 4px 0 24px rgba(15, 89, 83, 0.12);
      --shadow-card: 0 4px 16px rgba(15, 89, 83, 0.08);
      --shadow-fab: 0 4px 14px rgba(0, 0, 0, 0.16);
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

    /* ==========================================================================
       SIDEBAR PRINCIPAL (ESCRITORIO & MÓVIL)
       ========================================================================== */
    #sidebar {{
      width: 440px;
      height: 100vh;
      background: #ffffff;
      border-right: 1px solid var(--cdmx-border);
      box-shadow: var(--shadow-sidebar);
      display: flex;
      flex-direction: column;
      z-index: 1001;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), margin-left 0.3s ease;
      flex-shrink: 0;
    }}

    #sidebar.collapsed {{
      margin-left: -440px;
    }}

    .sidebar-header {{
      background: linear-gradient(135deg, var(--cdmx-green-dark) 0%, #15736c 100%);
      color: #ffffff;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 2px solid var(--cdmx-gold);
      flex-shrink: 0;
    }}

    .sidebar-brand-title {{
      font-size: 1.08rem;
      font-weight: 800;
      letter-spacing: -0.3px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .sidebar-brand-sub {{
      font-size: 0.68rem;
      color: #e0f2f1;
      font-weight: 500;
      margin-top: 2px;
      letter-spacing: 0.2px;
    }}

    .btn-toggle-sidebar {{
      background: rgba(255, 255, 255, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: #ffffff;
      border-radius: 8px;
      padding: 6px 10px;
      cursor: pointer;
      font-size: 0.85rem;
      transition: background 0.2s ease;
    }}
    .btn-toggle-sidebar:hover {{
      background: rgba(255, 255, 255, 0.28);
    }}

    .sidebar-scroll {{
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    /* Botón flotante para reabrir sidebar cuando está colapsado */
    #btn-open-sidebar {{
      position: absolute;
      top: 16px;
      left: 16px;
      z-index: 1000;
      background: var(--cdmx-green-dark);
      color: #ffffff;
      border: none;
      border-radius: 10px;
      padding: 10px 14px;
      font-family: var(--font-main);
      font-size: 0.82rem;
      font-weight: 700;
      box-shadow: var(--shadow-fab);
      cursor: pointer;
      display: none;
      align-items: center;
      gap: 8px;
      transition: transform 0.2s ease, background 0.2s ease;
    }}
    #btn-open-sidebar:hover {{
      background: var(--cdmx-green-primary);
      transform: translateY(-1px);
    }}

    /* ==========================================================================
       TARJETAS Y MÓDULOS DE CONTROL
       ========================================================================== */
    .section-card {{
      background: #ffffff;
      border: 1px solid var(--cdmx-border);
      border-radius: 12px;
      padding: 14px;
      box-shadow: var(--shadow-card);
    }}

    .section-title {{
      font-size: 0.76rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--cdmx-green-dark);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    /* Selector de Día de la Semana */
    .btn-today-highlight {{
      width: 100%;
      background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);
      color: #ffffff;
      border: none;
      border-radius: 10px;
      padding: 11px 14px;
      font-family: var(--font-main);
      font-size: 0.84rem;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 4px 12px rgba(15, 118, 110, 0.24);
      margin-bottom: 10px;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .btn-today-highlight:hover {{
      transform: translateY(-1px);
      box-shadow: 0 6px 16px rgba(15, 118, 110, 0.32);
    }}
    .btn-today-highlight.active {{
      background: linear-gradient(135deg, #047857 0%, #065f46 100%);
      border: 2px solid #a7f3d0;
    }}

    .days-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 5px;
    }}
    .day-btn {{
      background: var(--cdmx-bg);
      border: 1px solid var(--cdmx-border);
      color: var(--cdmx-text-dark);
      padding: 7px 4px;
      border-radius: 8px;
      font-family: var(--font-main);
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s ease;
    }}
    .day-btn:hover {{
      background: var(--cdmx-green-chip);
      border-color: var(--cdmx-green-primary);
    }}
    .day-btn.active {{
      background: var(--cdmx-green-dark);
      color: #ffffff;
      border-color: var(--cdmx-green-dark);
      box-shadow: 0 2px 6px rgba(15, 89, 83, 0.25);
    }}

    /* Selector de Alcaldía */
    .alcaldia-select-wrapper {{
      position: relative;
      margin-top: 6px;
    }}
    .alcaldia-select {{
      width: 100%;
      padding: 9px 12px;
      font-family: var(--font-main);
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--cdmx-text-dark);
      background: #ffffff;
      border: 1.5px solid var(--cdmx-border);
      border-radius: 9px;
      outline: none;
      cursor: pointer;
      appearance: none;
      -webkit-appearance: none;
      transition: border-color 0.2s ease;
    }}
    .alcaldia-select:focus {{
      border-color: var(--cdmx-green-primary);
      box-shadow: 0 0 0 3px rgba(17, 105, 98, 0.12);
    }}
    .alcaldia-select-arrow {{
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      pointer-events: none;
      color: var(--cdmx-green-dark);
      font-size: 0.75rem;
    }}

    /* Buscador Predictivo */
    .search-input-container {{
      position: relative;
    }}
    .search-input-box {{
      width: 100%;
      padding: 10px 38px 10px 12px;
      font-family: var(--font-main);
      font-size: 0.82rem;
      border: 1.5px solid var(--cdmx-border);
      border-radius: 9px;
      background: #ffffff;
      color: var(--cdmx-text-dark);
      outline: none;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .search-input-box:focus {{
      border-color: var(--cdmx-green-primary);
      box-shadow: 0 0 0 3px rgba(17, 105, 98, 0.12);
    }}
    .search-clear-btn {{
      position: absolute;
      right: 10px;
      top: 50%;
      transform: translateY(-50%);
      background: transparent;
      border: none;
      color: #94a3b8;
      font-size: 0.85rem;
      cursor: pointer;
      display: none;
    }}

    /* Dropdown de Autocompletado */
    .autocomplete-dropdown {{
      position: absolute;
      top: calc(100% + 4px);
      left: 0;
      right: 0;
      background: #ffffff;
      border: 1px solid var(--cdmx-border);
      border-radius: 10px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
      max-height: 280px;
      overflow-y: auto;
      z-index: 2000;
      display: none;
    }}
    .autocomplete-item {{
      padding: 9px 12px;
      border-bottom: 1px solid #f1f5f9;
      cursor: pointer;
      font-size: 0.77rem;
      transition: background 0.12s ease;
    }}
    .autocomplete-item:last-child {{
      border-bottom: none;
    }}
    .autocomplete-item:hover, .autocomplete-item.selected {{
      background: var(--cdmx-green-light);
    }}
    .autocomplete-title {{
      font-weight: 700;
      color: var(--cdmx-text-dark);
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .autocomplete-sub {{
      font-size: 0.69rem;
      color: var(--cdmx-text-muted);
      margin-top: 2px;
    }}
    .autocomplete-badge {{
      display: inline-block;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.62rem;
      font-weight: 800;
      text-transform: uppercase;
      color: #ffffff;
    }}

    /* Conmutadores de Capas de Comercio */
    .layers-toggle-grid {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .layer-toggle-btn {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 10px;
      border-radius: 8px;
      background: var(--cdmx-bg);
      border: 1px solid var(--cdmx-border);
      cursor: pointer;
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--cdmx-text-dark);
      transition: all 0.15s ease;
    }}
    .layer-toggle-btn:hover {{
      background: #f1f5f9;
    }}
    .layer-toggle-btn.active {{
      background: var(--cdmx-green-chip);
      border-color: var(--cdmx-green-primary);
      color: var(--cdmx-green-dark);
      font-weight: 700;
    }}
    .layer-pill-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      display: inline-block;
      margin-right: 6px;
    }}

    /* Banderas de Política Pública y Abasto */
    .policy-toggle-row {{
      display: flex;
      gap: 8px;
    }}
    .policy-toggle-btn {{
      flex: 1;
      padding: 7px 8px;
      border-radius: 7px;
      background: #ffffff;
      border: 1px solid var(--cdmx-border);
      font-family: var(--font-main);
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      color: var(--cdmx-text-dark);
      transition: all 0.15s ease;
    }}
    .policy-toggle-btn.active {{
      background: var(--cdmx-green-dark);
      color: #ffffff;
      border-color: var(--cdmx-green-dark);
    }}

    /* Contador y Filtros Activos */
    .results-counter-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 4px;
      font-size: 0.74rem;
      color: var(--cdmx-text-muted);
    }}
    .btn-reset-filters {{
      background: none;
      border: none;
      color: #dc2626;
      font-family: var(--font-main);
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      display: none;
    }}
    .btn-reset-filters:hover {{
      text-decoration: underline;
    }}

    /* ==========================================================================
       FICHA DE DETALLE EN EL SIDEBAR (DETAIL CARD)
       ========================================================================== */
    #detail-card {{
      background: #ffffff;
      border: 1.5px solid var(--cdmx-green-dark);
      border-radius: 12px;
      padding: 14px;
      box-shadow: 0 8px 24px rgba(15, 89, 83, 0.12);
      display: none;
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
      margin-bottom: 8px;
    }}
    .detail-space-badge {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 8px;
      border-radius: 5px;
      font-size: 0.65rem;
      font-weight: 800;
      text-transform: uppercase;
      color: #ffffff;
    }}
    .btn-close-card {{
      background: transparent;
      border: none;
      color: #94a3b8;
      font-size: 1.1rem;
      cursor: pointer;
      line-height: 1;
      padding: 2px 4px;
    }}
    .btn-close-card:hover {{
      color: var(--cdmx-text-dark);
    }}

    .detail-name {{
      font-size: 1.05rem;
      font-weight: 800;
      color: var(--cdmx-text-dark);
      line-height: 1.25;
      margin-bottom: 3px;
    }}
    .detail-sub {{
      font-size: 0.74rem;
      color: var(--cdmx-text-muted);
      font-weight: 600;
      margin-bottom: 10px;
    }}

    /* Estatus en Vivo */
    .status-live-banner {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 7px 10px;
      border-radius: 8px;
      font-size: 0.75rem;
      font-weight: 700;
      margin-bottom: 10px;
    }}
    .status-open {{
      background: #ecfdf5;
      color: #065f46;
      border: 1px solid #a7f3d0;
    }}
    .status-montaje {{
      background: #fefce8;
      color: #854d0e;
      border: 1px solid #fde047;
    }}
    .status-closed {{
      background: #fef2f2;
      color: #991b1b;
      border: 1px solid #fecaca;
    }}
    .status-dot-pulse {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      flex-shrink: 0;
    }}
    .status-open .status-dot-pulse {{
      background: #10b981;
      box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25);
    }}
    .status-montaje .status-dot-pulse {{
      background: #f59e0b;
      box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.25);
    }}
    .status-closed .status-dot-pulse {{
      background: #ef4444;
    }}

    /* Caja de Afectación Vial y Entrecalles */
    .closure-box {{
      background: #fffbeb;
      border: 1px solid #fde68a;
      border-radius: 8px;
      padding: 10px;
      font-size: 0.74rem;
      color: #92400e;
      margin-bottom: 10px;
      line-height: 1.4;
    }}
    .closure-box-title {{
      font-weight: 800;
      color: #78350f;
      margin-bottom: 3px;
      display: flex;
      align-items: center;
      gap: 5px;
    }}

    /* Grid de Estadísticas */
    .detail-stats-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
      margin-bottom: 10px;
    }}
    .stat-box {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 7px;
      padding: 6px;
      text-align: center;
    }}
    .stat-box-val {{
      font-size: 0.85rem;
      font-weight: 800;
      color: var(--cdmx-green-dark);
    }}
    .stat-box-lbl {{
      font-size: 0.62rem;
      color: #64748b;
      font-weight: 600;
      text-transform: uppercase;
      margin-top: 1px;
    }}

    /* Desglose de Horarios Operativos */
    .oper-schedule-box {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 8px 10px;
      font-size: 0.72rem;
      margin-bottom: 10px;
    }}
    .oper-schedule-row {{
      display: flex;
      justify-content: space-between;
      padding: 2px 0;
      color: #334155;
    }}

    /* Botones de Acción en Ficha */
    .detail-actions-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }}
    .btn-detail-action {{
      padding: 8px;
      border-radius: 7px;
      font-family: var(--font-main);
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      text-decoration: none;
      transition: all 0.15s ease;
      border: 1px solid transparent;
    }}
    .btn-action-primary {{
      background: var(--cdmx-green-dark);
      color: #ffffff;
    }}
    .btn-action-primary:hover {{
      background: var(--cdmx-green-primary);
    }}
    .btn-action-secondary {{
      background: #f1f5f9;
      color: var(--cdmx-text-dark);
      border-color: #cbd5e1;
    }}
    .btn-action-secondary:hover {{
      background: #e2e8f0;
    }}

    /* Botón Calles Ocupadas Hoy */
    .btn-open-cierres-modal {{
      background: linear-gradient(135deg, #b45309 0%, #78350f 100%);
      color: #ffffff;
      border: none;
      border-radius: 10px;
      padding: 11px 14px;
      font-family: var(--font-main);
      font-size: 0.8rem;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 12px rgba(180, 83, 9, 0.22);
      transition: transform 0.15s ease;
    }}
    .btn-open-cierres-modal:hover {{
      transform: translateY(-1px);
    }}

    /* ==========================================================================
       MAPA Y CONTROLES FLOTANTES
       ========================================================================== */
    #map-container {{
      flex: 1;
      height: 100vh;
      position: relative;
    }}
    #map {{
      width: 100%;
      height: 100%;
    }}

    /* Barra Superior Flotante */
    .top-floating-bar {{
      position: absolute;
      top: 16px;
      left: 16px;
      right: 16px;
      z-index: 999;
      display: flex;
      align-items: center;
      justify-content: space-between;
      pointer-events: none;
    }}
    .top-bar-left {{
      display: flex;
      align-items: center;
      gap: 8px;
      pointer-events: auto;
    }}
    .top-bar-right {{
      display: flex;
      align-items: center;
      gap: 8px;
      pointer-events: auto;
    }}

    .btn-fab {{
      background: #ffffff;
      color: var(--cdmx-text-dark);
      border: 1px solid var(--cdmx-border);
      border-radius: 10px;
      padding: 8px 12px;
      font-family: var(--font-main);
      font-size: 0.78rem;
      font-weight: 700;
      box-shadow: var(--shadow-fab);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}
    .btn-fab:hover {{
      background: var(--cdmx-green-light);
      border-color: var(--cdmx-green-primary);
    }}

    /* ==========================================================================
       MARKER CLUSTERS ESTILIZADOS
       ========================================================================== */
    .cluster-wrapper {{
      background: transparent !important;
      border: none !important;
    }}
    .custom-cluster-badge {{
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      font-family: var(--font-main);
      font-weight: 800;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(0,0,0,0.28), 0 0 0 3px rgba(255,255,255,0.9);
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      cursor: pointer;
      user-select: none;
    }}
    .custom-cluster-badge:hover {{
      transform: scale(1.12);
    }}
    .cluster-tianguis {{
      background: radial-gradient(circle at 35% 35%, #0f766e, #064e3b);
    }}
    .cluster-msr {{
      background: radial-gradient(circle at 35% 35%, #d97706, #92400e);
    }}
    .cluster-concentraciones {{
      background: radial-gradient(circle at 35% 35%, #6d28d9, #4c1d95);
    }}
    .cluster-mercados {{
      background: radial-gradient(circle at 35% 35%, #ca8a04, #854d0e);
    }}

    .cluster-small {{ width: 36px; height: 36px; font-size: 0.72rem; }}
    .cluster-medium {{ width: 44px; height: 44px; font-size: 0.78rem; }}
    .cluster-large {{ width: 52px; height: 52px; font-size: 0.84rem; }}

    /* ==========================================================================
       MODAL DE AFECTACIONES Y CALLES OCUPADAS
       ========================================================================== */
    .modal-overlay {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      z-index: 3000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 16px;
    }}
    .modal-card {{
      background: #ffffff;
      width: 100%;
      max-width: 760px;
      max-height: 88vh;
      border-radius: 16px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      border: 1px solid var(--cdmx-border);
      animation: modalPop 0.22s ease-out;
    }}
    @keyframes modalPop {{
      from {{ transform: scale(0.95); opacity: 0; }}
      to {{ transform: scale(1); opacity: 1; }}
    }}

    .modal-header {{
      background: linear-gradient(135deg, var(--cdmx-green-dark) 0%, #15736c 100%);
      color: #ffffff;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 2px solid var(--cdmx-gold);
    }}
    .modal-title {{
      font-size: 1.05rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .modal-close-btn {{
      background: rgba(255, 255, 255, 0.2);
      border: none;
      color: #ffffff;
      border-radius: 8px;
      width: 28px;
      height: 28px;
      font-size: 1rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .modal-tabs {{
      display: flex;
      background: #f1f5f9;
      border-bottom: 1px solid var(--cdmx-border);
      padding: 0 16px;
    }}
    .modal-tab-btn {{
      padding: 10px 14px;
      font-family: var(--font-main);
      font-size: 0.78rem;
      font-weight: 700;
      border: none;
      background: transparent;
      color: #64748b;
      cursor: pointer;
      border-bottom: 2.5px solid transparent;
      transition: all 0.15s ease;
    }}
    .modal-tab-btn.active {{
      color: var(--cdmx-green-dark);
      border-bottom-color: var(--cdmx-green-dark);
      background: #ffffff;
    }}

    .modal-body {{
      padding: 20px;
      overflow-y: auto;
      flex: 1;
    }}

    /* KPI Cards dentro del Modal */
    .kpi-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-bottom: 16px;
    }}
    .kpi-card {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      padding: 10px;
      text-align: center;
    }}
    .kpi-val {{
      font-size: 1.25rem;
      font-weight: 900;
      color: var(--cdmx-green-dark);
    }}
    .kpi-lbl {{
      font-size: 0.65rem;
      font-weight: 700;
      color: #64748b;
      text-transform: uppercase;
      margin-top: 2px;
    }}

    /* Tablas de Corredores y Afectaciones */
    .corredores-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.74rem;
      margin-top: 10px;
    }}
    .corredores-table th {{
      background: #f1f5f9;
      color: var(--cdmx-text-dark);
      padding: 8px 10px;
      text-align: left;
      font-weight: 800;
      border-bottom: 2px solid var(--cdmx-border);
    }}
    .corredores-table td {{
      padding: 8px 10px;
      border-bottom: 1px solid #e2e8f0;
      color: #334155;
    }}
    .corredores-table tr:hover td {{
      background: var(--cdmx-green-light);
    }}

    /* Loader Inicial */
    .map-loader-overlay {{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(248, 250, 252, 0.94);
      backdrop-filter: blur(6px);
      z-index: 2500;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: opacity 0.3s ease, visibility 0.3s ease;
    }}
    .map-loader-overlay.hidden {{
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
    }}
    .loader-card {{
      background: #ffffff;
      padding: 28px 34px;
      border-radius: 16px;
      box-shadow: 0 15px 35px rgba(15, 89, 83, 0.15);
      text-align: center;
      max-width: 420px;
      width: 90%;
      border: 1px solid var(--cdmx-border);
    }}
    .spinner-ring {{
      width: 40px;
      height: 40px;
      border: 3.5px solid #d5ece9;
      border-top-color: var(--cdmx-green-dark);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      margin: 0 auto 14px;
    }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}

    /* Toasts */
    .toast-container {{
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 4000;
      display: flex;
      flex-direction: column;
      gap: 8px;
      pointer-events: none;
    }}
    .toast-msg {{
      background: #0f172a;
      color: #ffffff;
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 0.75rem;
      font-weight: 600;
      box-shadow: 0 10px 25px rgba(0,0,0,0.2);
      pointer-events: auto;
      animation: toastIn 0.2s ease;
    }}
    @keyframes toastIn {{
      from {{ transform: translateY(10px); opacity: 0; }}
      to {{ transform: translateY(0); opacity: 1; }}
    }}

    /* Responsive */
    @media (max-width: 768px) {{
      #sidebar {{
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        width: 100vw;
        max-width: 380px;
        z-index: 2001;
      }}
      #sidebar.collapsed {{
        margin-left: -100vw;
      }}
      #btn-open-sidebar {{
        display: flex;
      }}
      .kpi-row {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}
  </style>
</head>
<body>

  <!-- Botón para reabrir panel en móvil o vista colapsada -->
  <button id="btn-open-sidebar" onclick="toggleSidebar()">
    <span>☰</span>
    <span>Abrir Directorio</span>
  </button>

  <!-- SIDEBAR LATERAL -->
  <aside id="sidebar">
    <div class="sidebar-header">
      <div>
        <div class="sidebar-brand-title">
          <span>🧺</span> Comercio Popular CDMX
        </div>
        <div class="sidebar-brand-sub">Tianguis · MSR · Concentraciones Barriales</div>
      </div>
      <button class="btn-toggle-sidebar" onclick="toggleSidebar()" title="Colapsar panel lateral">◀</button>
    </div>

    <div class="sidebar-scroll">

      <!-- 1. SELECTOR RÁPIDO DE DÍA DE LA SEMANA -->
      <div class="section-card">
        <div class="section-title">
          <span>📅 Día de Instalación</span>
          <span id="active-day-badge" style="font-size:0.65rem; background:var(--cdmx-green-chip); color:var(--cdmx-green-dark); padding:2px 6px; border-radius:4px;">TODOS</span>
        </div>

        <!-- Botón destacado "Abiertos Hoy" -->
        <button id="btn-today-filter" class="btn-today-highlight" onclick="filterByToday()">
          <span style="display:flex; align-items:center; gap:6px;">
            <span>🧺</span>
            <span id="btn-today-text">Abiertos Hoy ({'LUNES'})</span>
          </span>
          <span id="btn-today-count" style="background:rgba(255,255,255,0.22); padding:2px 8px; border-radius:12px; font-size:0.75rem;">--</span>
        </button>

        <!-- Selector de Días -->
        <div class="days-grid">
          <button class="day-btn active" id="day-TODOS" onclick="filterByDay('TODOS')">Todos</button>
          <button class="day-btn" id="day-LUNES" onclick="filterByDay('LUNES')">Lun</button>
          <button class="day-btn" id="day-MARTES" onclick="filterByDay('MARTES')">Mar</button>
          <button class="day-btn" id="day-MIERCOLES" onclick="filterByDay('MIERCOLES')">Mié</button>
          <button class="day-btn" id="day-JUEVES" onclick="filterByDay('JUEVES')">Jue</button>
          <button class="day-btn" id="day-VIERNES" onclick="filterByDay('VIERNES')">Vie</button>
          <button class="day-btn" id="day-SABADO" onclick="filterByDay('SABADO')">Sáb</button>
          <button class="day-btn" id="day-DOMINGO" onclick="filterByDay('DOMINGO')">Dom</button>
        </div>
      </div>

      <!-- 2. FILTRO POR ALCALDÍA -->
      <div class="section-card">
        <div class="section-title">
          <span>🏛️ Alcaldía Oficial</span>
          <span id="alcaldia-count-badge" style="font-size:0.65rem; color:#64748b;">16 demarcaciones</span>
        </div>
        <div class="alcaldia-select-wrapper">
          <select id="alcaldia-select" class="alcaldia-select" onchange="onAlcaldiaSelectChange(this.value)">
            <option value="TODAS">Todas las Alcaldías (CDMX)</option>
            <option value="ALVARO OBREGON">Álvaro Obregón</option>
            <option value="AZCAPOTZALCO">Azcapotzalco</option>
            <option value="BENITO JUAREZ">Benito Juárez</option>
            <option value="COYOACAN">Coyoacán</option>
            <option value="CUAJIMALPA DE MORELOS">Cuajimalpa de Morelos</option>
            <option value="CUAUHTEMOC">Cuauhtémoc</option>
            <option value="GUSTAVO A. MADERO">Gustavo A. Madero</option>
            <option value="IZTACALCO">Iztacalco</option>
            <option value="IZTAPALAPA">Iztapalapa</option>
            <option value="LA MAGDALENA CONTRERAS">La Magdalena Contreras</option>
            <option value="MIGUEL HIDALGO">Miguel Hidalgo</option>
            <option value="MILPA ALTA">Milpa Alta</option>
            <option value="TLAHUAC">Tláhuac</option>
            <option value="TLALPAN">Tlalpan</option>
            <option value="VENUSTIANO CARRANZA">Venustiano Carranza</option>
            <option value="XOCHIMILCO">Xochimilco</option>
          </select>
          <span class="alcaldia-select-arrow">▼</span>
        </div>
      </div>

      <!-- 3. BUSCADOR PREDICTIVO ESPECIALIZADO -->
      <div class="section-card">
        <div class="section-title">
          <span>🔍 Búsqueda Rápida</span>
          <span style="font-size:0.65rem; color:#64748b;">Predictivo</span>
        </div>
        <div class="search-input-container">
          <input type="text" id="commerce-search-input" class="search-input-box"
                 placeholder="Tianguis, calle, entrecalle, colonia o giro (ej. El Salado, Texcoco, Frutas)..."
                 autocomplete="off"
                 oninput="onCommerceSearchInput(this.value)">
          <button id="commerce-search-clear" class="search-clear-btn" onclick="clearCommerceSearch()">✕</button>
          <div id="commerce-autocomplete-dropdown" class="autocomplete-dropdown"></div>
        </div>
      </div>

      <!-- 4. TIPOS DE COMERCIO POPULAR Y BANDERAS -->
      <div class="section-card">
        <div class="section-title">
          <span>🛒 Espacios Comerciales</span>
        </div>
        <div class="layers-toggle-grid">
          <div class="layer-toggle-btn active" id="chip-tianguis" onclick="toggleSpaceLayer('tianguis')">
            <span><span class="layer-pill-dot" style="background:#0f766e;"></span>🧺 Tianguis Itinerantes</span>
            <span id="badge-count-tianguis" style="font-size:0.7rem; color:#64748b;">1,365</span>
          </div>
          <div class="layer-toggle-btn active" id="chip-msr" onclick="toggleSpaceLayer('msr')">
            <span><span class="layer-pill-dot" style="background:#d97706;"></span>🚚 Mercados Sobre Ruedas (MSR)</span>
            <span id="badge-count-msr" style="font-size:0.7rem; color:#64748b;">51</span>
          </div>
          <div class="layer-toggle-btn active" id="chip-concentraciones" onclick="toggleSpaceLayer('concentraciones')">
            <span><span class="layer-pill-dot" style="background:#6d28d9;"></span>🏬 Concentraciones Barriales</span>
            <span id="badge-count-concentraciones" style="font-size:0.7rem; color:#64748b;">169</span>
          </div>
          <div class="layer-toggle-btn" id="chip-mercados" onclick="toggleSpaceLayer('mercados')">
            <span><span class="layer-pill-dot" style="background:#ca8a04;"></span>🏪 Mercados Públicos Fijos</span>
            <span id="badge-count-mercados" style="font-size:0.7rem; color:#64748b;">329 (Oculto)</span>
          </div>
        </div>

        <div style="margin-top:10px;">
          <div class="policy-toggle-row">
            <button class="policy-toggle-btn" id="btn-toggle-canasta" onclick="toggleCanastaFilter()">
              <span>🧺</span>
              <span>Canasta Básica</span>
            </button>
            <button class="policy-toggle-btn" id="btn-toggle-mercomuna" onclick="toggleMercomunaFilter()">
              <span>💳</span>
              <span>MERCOMUNA</span>
            </button>
          </div>
        </div>
      </div>

      <!-- 5. CONTADOR Y RESET -->
      <div class="results-counter-bar">
        <span id="results-counter-text">Cargando espacios...</span>
        <button id="btn-reset-filters" class="btn-reset-filters" onclick="resetAllFilters()">↺ Limpiar filtros</button>
      </div>

      <!-- 6. BOTÓN DESTACADO CALLLES OCUPADAS HOY -->
      <button class="btn-open-cierres-modal" onclick="openCierresModal()">
        <span>⚠️</span>
        <span>Afectaciones y Calles Ocupadas Hoy</span>
      </button>

      <!-- 7. FICHA DE DETALLE DINÁMICA (AL SELECCIONAR TIANGUIS / ESPACIO) -->
      <div id="detail-card">
        <div class="detail-card-header">
          <span class="detail-space-badge" id="card-tag" style="background:#0f766e;">🧺 TIANGUIS ITINERANTE</span>
          <button class="btn-close-card" onclick="closeDetailCard()" title="Cerrar ficha">✕</button>
        </div>

        <div id="card-status-banner" class="status-live-banner status-open">
          <span class="status-dot-pulse"></span>
          <span id="card-status-text">🟢 En operación hoy</span>
        </div>

        <div class="detail-name" id="card-name">Tianguis</div>
        <div class="detail-sub" id="card-sub">Alcaldía · Colonia</div>

        <!-- Ubicación exacta y entrecalles -->
        <div class="closure-box">
          <div class="closure-box-title">
            <span>📍</span>
            <span>Ubicación y Entrecalles Ocupadas:</span>
          </div>
          <div id="card-street-text" style="font-weight:600; color:#1e293b; margin-bottom:4px;">
            Tramo vial principal
          </div>
          <div id="card-closure-impact" style="font-size:0.7rem; color:#b45309;">
            🚗 Cierre temporal de calle vehicular durante el horario de venta.
          </div>
        </div>

        <!-- Estadísticas clave -->
        <div class="detail-stats-grid">
          <div class="stat-box">
            <div class="stat-box-val" id="card-stat-dia">--</div>
            <div class="stat-box-lbl">Día</div>
          </div>
          <div class="stat-box">
            <div class="stat-box-val" id="card-stat-horario">8:00-17:00</div>
            <div class="stat-box-lbl">Horario Venta</div>
          </div>
          <div class="stat-box">
            <div class="stat-box-val" id="card-stat-puestos">--</div>
            <div class="stat-box-lbl">Puestos Est.</div>
          </div>
        </div>

        <!-- Horarios operativos -->
        <div class="oper-schedule-box">
          <div style="font-weight:700; color:var(--cdmx-green-dark); margin-bottom:4px; font-size:0.69rem; text-transform:uppercase;">
            ⏰ Dinámica Horaria en Vía Pública:
          </div>
          <div class="oper-schedule-row">
            <span>🛠️ Montaje de estructuras:</span>
            <span style="font-weight:700;" id="card-time-montaje">06:00 a 08:00 hrs</span>
          </div>
          <div class="oper-schedule-row">
            <span>🧺 Venta al público:</span>
            <span style="font-weight:700; color:#065f46;" id="card-time-venta">08:00 a 17:00 hrs</span>
          </div>
          <div class="oper-schedule-row">
            <span>🧹 Desmontaje y limpieza vial:</span>
            <span style="font-weight:700;" id="card-time-desmontaje">17:00 a 19:00 hrs</span>
          </div>
        </div>

        <!-- Giros y Etiquetas -->
        <div style="margin-bottom:12px;">
          <div style="font-size:0.69rem; font-weight:700; color:#64748b; text-transform:uppercase; margin-bottom:4px;">
            🛍️ Giros y Abasto Popular:
          </div>
          <div id="card-tags-container" style="display:flex; flex-wrap:wrap; gap:4px;"></div>
        </div>

        <!-- Botones de Acción -->
        <div class="detail-actions-row">
          <button class="btn-detail-action btn-action-primary" onclick="copyCardCoords()">
            <span>📋</span>
            <span>Copiar GPS</span>
          </button>
          <a id="card-gmaps-link" class="btn-detail-action btn-action-secondary" href="#" target="_blank" rel="noopener">
            <span>📍</span>
            <span>Google Maps</span>
          </a>
        </div>
      </div>

    </div>
  </aside>

  <!-- CONTENEDOR DEL MAPA Y CONTROLES FLOTANTES -->
  <main id="map-container">
    
    <!-- Barra Superior Flotante -->
    <div class="top-floating-bar">
      <div class="top-bar-left">
        <button class="btn-fab" onclick="toggleSidebar()" title="Alternar panel de búsqueda">
          <span>☰</span>
          <span style="display:none;" class="mobile-hide">Menú</span>
        </button>
      </div>

      <div class="top-bar-right">
        <button class="btn-fab" onclick="locateUser()" title="Ubicar mi posición actual">
          <span>📍</span>
          <span>Mi Ubicación</span>
        </button>
        <button class="btn-fab" onclick="toggleBaseMap()" title="Cambiar capa base">
          <span>🗺️</span>
          <span>Mapa</span>
        </button>
        <button class="btn-fab" onclick="resetMapView()" title="Centrar mapa en la CDMX">
          <span>↺</span>
        </button>
      </div>
    </div>

    <!-- Div Mapa Leaflet -->
    <div id="map"></div>

    <!-- Skeleton Loader Inicial -->
    <div id="map-loader" class="map-loader-overlay">
      <div class="loader-card">
        <div class="spinner-ring"></div>
        <div style="font-size:1.05rem; font-weight:800; color:var(--cdmx-green-dark); margin-bottom:6px;">
          Comercio Popular y Barrial CDMX
        </div>
        <div id="loader-sub" style="font-size:0.75rem; color:#64748b;">
          Cargando 1,365 tianguis, mercados sobre ruedas y concentraciones...
        </div>
      </div>
    </div>
  </main>

  <!-- MODAL DE AFECTACIONES Y CALLES OCUPADAS HOY -->
  <div id="cierres-modal-overlay" class="modal-overlay" onclick="handleModalOverlayClick(event)">
    <div class="modal-card">
      <div class="modal-header">
        <div class="modal-title">
          <span>⚠️</span>
          <span>Afectaciones y Calles Ocupadas por Comercio Popular</span>
        </div>
        <button class="modal-close-btn" onclick="closeCierresModal()">✕</button>
      </div>

      <div class="modal-tabs">
        <button class="modal-tab-btn active" id="modal-tab-hoy" onclick="switchModalTab('hoy')">🧺 Ocupación Vial Hoy</button>
        <button class="modal-tab-btn" id="modal-tab-semana" onclick="switchModalTab('semana')">📅 Calendario Semanal CDMX</button>
        <button class="modal-tab-btn" id="modal-tab-normativa" onclick="switchModalTab('normativa')">ℹ️ Horarios y Montaje</button>
      </div>

      <div class="modal-body" id="modal-body-content">
        <!-- Contenido generado dinámicamente -->
      </div>
    </div>
  </div>

  <!-- Contenedor de Toasts -->
  <div id="toast-container" class="toast-container"></div>

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <!-- Leaflet MarkerCluster JS -->
  <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

  <!-- Bundle de datos unificado -->
  <script src="data/processed/map_bundle.js" onerror="console.log('map_bundle.js no cargado localmente, usando fetch')"></script>

  <script>
    // =========================================================================
    // DATOS DE CIERRES VIALES EMBEBIDOS PARA RENDERING OFFLINE INMEDIATO
    // =========================================================================
    const EMBEDDED_CIERRES = {cierres_json_str};

    // =========================================================================
    // INICIALIZACIÓN DEL MAPA LEAFLET (WGS84)
    // =========================================================================
    const map = L.map('map', {{
      center: [19.4326, -99.1332],
      zoom: 12,
      minZoom: 9,
      maxZoom: 18,
      zoomControl: false
    }});

    L.control.zoom({{ position: 'bottomright' }}).addTo(map);

    let currentBase = 'esri';
    const esriLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
      attribution: 'Esri, HERE &copy; OpenStreetMap contributors',
      maxZoom: 18
    }}).addTo(map);

    const osmLayer = L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{y}}/{{x}}.png', {{
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19
    }});

    function toggleBaseMap() {{
      if (currentBase === 'esri') {{
        map.removeLayer(esriLayer);
        osmLayer.addTo(map);
        currentBase = 'osm';
        showToast('Mapa base cambiado a OpenStreetMap.', 'info');
      }} else {{
        map.removeLayer(osmLayer);
        esriLayer.addTo(map);
        currentBase = 'esri';
        showToast('Mapa base cambiado a Esri Light Gray.', 'info');
      }}
    }}

    function resetMapView() {{
      map.flyTo([19.4326, -99.1332], 12, {{ duration: 0.8 }});
    }}

    // =========================================================================
    // CLUSTERS Y CAPAS DE COMERCIO POPULAR
    // =========================================================================
    const clusterOptionsBase = {{
      spiderfyOnMaxZoom: true,
      showCoverageOnHover: false,
      zoomToBoundsOnClick: true,
      disableClusteringAtZoom: 16
    }};

    const layers = {{
      alcaldias: L.geoJSON(null, {{
        style: {{
          color: '#0f5953',
          weight: 1.5,
          opacity: 0.7,
          fillColor: '#0f5953',
          fillOpacity: 0.03,
          dashArray: '4, 4'
        }}
      }}),
      tianguis: L.markerClusterGroup({{
        ...clusterOptionsBase,
        maxClusterRadius: 38,
        iconCreateFunction: function(cluster) {{
          const count = cluster.getChildCount();
          let sz = count < 15 ? 'cluster-small' : (count < 40 ? 'cluster-medium' : 'cluster-large');
          return L.divIcon({{
            html: `<div class="custom-cluster-badge cluster-tianguis ${{sz}}"><span>${{count}}</span></div>`,
            className: 'cluster-wrapper',
            iconSize: L.point(40, 40)
          }});
        }}
      }}),
      msr: L.markerClusterGroup({{
        ...clusterOptionsBase,
        maxClusterRadius: 36,
        iconCreateFunction: function(cluster) {{
          const count = cluster.getChildCount();
          let sz = count < 10 ? 'cluster-small' : 'cluster-medium';
          return L.divIcon({{
            html: `<div class="custom-cluster-badge cluster-msr ${{sz}}"><span>${{count}}</span></div>`,
            className: 'cluster-wrapper',
            iconSize: L.point(38, 38)
          }});
        }}
      }}),
      concentraciones: L.markerClusterGroup({{
        ...clusterOptionsBase,
        maxClusterRadius: 36,
        iconCreateFunction: function(cluster) {{
          const count = cluster.getChildCount();
          let sz = count < 10 ? 'cluster-small' : 'cluster-medium';
          return L.divIcon({{
            html: `<div class="custom-cluster-badge cluster-concentraciones ${{sz}}"><span>${{count}}</span></div>`,
            className: 'cluster-wrapper',
            iconSize: L.point(38, 38)
          }});
        }}
      }}),
      mercados: L.markerClusterGroup({{
        ...clusterOptionsBase,
        maxClusterRadius: 36,
        iconCreateFunction: function(cluster) {{
          const count = cluster.getChildCount();
          let sz = count < 10 ? 'cluster-small' : 'cluster-medium';
          return L.divIcon({{
            html: `<div class="custom-cluster-badge cluster-mercados ${{sz}}"><span>${{count}}</span></div>`,
            className: 'cluster-wrapper',
            iconSize: L.point(38, 38)
          }});
        }}
      }})
    }};

    // =========================================================================
    // ESTADO DE FILTRADO Y GESTIÓN DE VISTA
    // =========================================================================
    const filterState = {{
      day: 'TODOS',          // 'TODOS' o 'LUNES', 'MARTES', etc.
      isTodayActive: false,
      alcaldia: 'TODAS',
      showTianguis: true,
      showMSR: true,
      showConcentraciones: true,
      showMercados: false,  // Oculto por defecto
      canastaBasica: false,
      mercomuna: false,
      searchQuery: ''
    }};

    let SEARCH_INDEX = [];
    let currentSelectedCardData = null;

    const DIAS_SEMANA = ['DOMINGO', 'LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO'];
    const NOMBRE_DIAS = {{
      'DOMINGO': 'Domingo',
      'LUNES': 'Lunes',
      'MARTES': 'Martes',
      'MIERCOLES': 'Miércoles',
      'JUEVES': 'Jueves',
      'VIERNES': 'Viernes',
      'SABADO': 'Sábado'
    }};

    function getTodayDayName() {{
      const d = new Date().getDay();
      return DIAS_SEMANA[d];
    }}

    // =========================================================================
    // CARGA DE DATOS E INICIALIZACIÓN
    // =========================================================================
    async function initApplication() {{
      const loader = document.getElementById('map-loader');
      const loaderSub = document.getElementById('loader-sub');

      try {{
        let data = window.MAP_DATA;
        if (!data) {{
          loaderSub.innerText = "Descargando directorio de comercio popular...";
          const res = await fetch('data/processed/map_bundle.json');
          data = await res.json();
          window.MAP_DATA = data;
        }}

        // Capas base de alcaldías
        if (data.alcaldias) {{
          layers.alcaldias.addData(data.alcaldias);
          layers.alcaldias.addTo(map);
        }}

        // Configurar botón "Abiertos Hoy"
        const todayName = getTodayDayName();
        document.getElementById('btn-today-text').innerText = `Abiertos Hoy (${{NOMBRE_DIAS[todayName]}})`;

        // Calcular conteo inicial de hoy
        const countToday = countSpacesForDay(todayName, data);
        document.getElementById('btn-today-count').innerText = `${{countToday}} espacios`;

        // Construir índice de búsqueda predictiva
        buildSearchIndex(data);

        // Renderizar marcadores con filtros iniciales
        applyAllFilters();

        // Ocultar loader
        setTimeout(() => {{
          loader.classList.add('hidden');
          showToast(`Directorio cargado · ${{countToday}} espacios abiertos hoy en CDMX.`, 'success', 3500);
        }}, 250);

      }} catch (err) {{
        console.error("Error al inicializar aplicación:", err);
        loader.classList.add('hidden');
        showToast('Error cargando el directorio de comercio.', 'error');
      }}
    }}

    function countSpacesForDay(dayName, data) {{
      if (!data) return 0;
      let count = 0;
      if (data.tianguis) {{
        count += data.tianguis.filter(t => t.dia && t.dia.toUpperCase().includes(dayName)).length;
      }}
      if (data.msr) {{
        count += data.msr.filter(m => m.dia && m.dia.toUpperCase().includes(dayName)).length;
      }}
      if (data.concentraciones) {{
        count += data.concentraciones.filter(c => c.dias_operacion_lista && c.dias_operacion_lista.includes(dayName)).length;
      }}
      return count;
    }}

    // =========================================================================
    // FILTROS: DÍA, ALCALDÍA, TIPOS Y BANDERAS
    // =========================================================================
    function filterByToday() {{
      const today = getTodayDayName();
      const btn = document.getElementById('btn-today-filter');

      if (filterState.isTodayActive) {{
        // Desactivar
        filterState.isTodayActive = false;
        filterState.day = 'TODOS';
        btn.classList.remove('active');
        setActiveDayUI('TODOS');
        showToast('Mostrando todos los días de la semana', 'info');
      }} else {{
        // Activar hoy
        filterState.isTodayActive = true;
        filterState.day = today;
        btn.classList.add('active');
        setActiveDayUI(today);
        showToast(`Filtrado a espacios abiertos hoy (${{NOMBRE_DIAS[today]}})`, 'success');
      }}
      applyAllFilters();
    }}

    function filterByDay(day) {{
      filterState.day = day;
      filterState.isTodayActive = (day === getTodayDayName());
      const btnToday = document.getElementById('btn-today-filter');
      if (filterState.isTodayActive) {{
        btnToday.classList.add('active');
      }} else {{
        btnToday.classList.remove('active');
      }}
      setActiveDayUI(day);
      applyAllFilters();
    }}

    function setActiveDayUI(day) {{
      document.querySelectorAll('.day-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('day-' + day);
      if (activeBtn) activeBtn.classList.add('active');
      document.getElementById('active-day-badge').innerText = day === 'TODOS' ? 'TODOS' : NOMBRE_DIAS[day].toUpperCase();
    }}

    function onAlcaldiaSelectChange(alc) {{
      filterState.alcaldia = alc;
      applyAllFilters();

      if (alc !== 'TODAS' && window.MAP_DATA && window.MAP_DATA.alcaldias) {{
        // Zoom suave a la alcaldía seleccionada
        const feat = window.MAP_DATA.alcaldias.features.find(f => {{
          const nom = (f.properties.NOMGEO || f.properties.nomgeo || f.properties.name || '').toUpperCase();
          return nom.includes(alc) || alc.includes(nom);
        }});
        if (feat) {{
          const bbox = L.geoJSON(feat).getBounds();
          map.fitBounds(bbox, {{ padding: [30, 30], maxZoom: 14 }});
        }}
      }}
    }}

    function toggleSpaceLayer(layerKey) {{
      if (layerKey === 'tianguis') filterState.showTianguis = !filterState.showTianguis;
      if (layerKey === 'msr') filterState.showMSR = !filterState.showMSR;
      if (layerKey === 'concentraciones') filterState.showConcentraciones = !filterState.showConcentraciones;
      if (layerKey === 'mercados') filterState.showMercados = !filterState.showMercados;

      const chip = document.getElementById('chip-' + layerKey);
      if (chip) {{
        const isActive = filterState[layerKey === 'tianguis' ? 'showTianguis' : (layerKey === 'msr' ? 'showMSR' : (layerKey === 'concentraciones' ? 'showConcentraciones' : 'showMercados'))];
        if (isActive) chip.classList.add('active');
        else chip.classList.remove('active');
      }}
      applyAllFilters();
    }}

    function toggleCanastaFilter() {{
      filterState.canastaBasica = !filterState.canastaBasica;
      const btn = document.getElementById('btn-toggle-canasta');
      if (filterState.canastaBasica) btn.classList.add('active');
      else btn.classList.remove('active');
      applyAllFilters();
    }}

    function toggleMercomunaFilter() {{
      filterState.mercomuna = !filterState.mercomuna;
      const btn = document.getElementById('btn-toggle-mercomuna');
      if (filterState.mercomuna) btn.classList.add('active');
      else btn.classList.remove('active');
      applyAllFilters();
    }}

    function resetAllFilters() {{
      filterState.day = 'TODOS';
      filterState.isTodayActive = false;
      filterState.alcaldia = 'TODAS';
      filterState.showTianguis = true;
      filterState.showMSR = true;
      filterState.showConcentraciones = true;
      filterState.showMercados = false;
      filterState.canastaBasica = false;
      filterState.mercomuna = false;
      filterState.searchQuery = '';

      document.getElementById('commerce-search-input').value = '';
      document.getElementById('commerce-search-clear').style.display = 'none';
      document.getElementById('alcaldia-select').value = 'TODAS';
      document.getElementById('btn-today-filter').classList.remove('active');
      document.getElementById('btn-toggle-canasta').classList.remove('active');
      document.getElementById('btn-toggle-mercomuna').classList.remove('active');
      document.getElementById('chip-tianguis').classList.add('active');
      document.getElementById('chip-msr').classList.add('active');
      document.getElementById('chip-concentraciones').classList.add('active');
      document.getElementById('chip-mercados').classList.remove('active');
      setActiveDayUI('TODOS');

      applyAllFilters();
      resetMapView();
      showToast('Filtros restablecidos', 'info');
    }}

    // =========================================================================
    // APLICACIÓN DE FILTROS Y RENDERIZADO DE MARCADORES
    // =========================================================================
    function applyAllFilters() {{
      if (!window.MAP_DATA) return;
      const data = window.MAP_DATA;

      const q = filterState.searchQuery.toLowerCase().trim();
      const currentDay = filterState.day;
      const currentAlc = filterState.alcaldia;

      // 1. Filtrar Tianguis
      let filteredTianguis = [];
      if (filterState.showTianguis && data.tianguis) {{
        filteredTianguis = data.tianguis.filter(t => {{
          if (currentDay !== 'TODOS' && (!t.dia || !t.dia.toUpperCase().includes(currentDay))) return false;
          if (currentAlc !== 'TODAS' && t.alcaldia && !t.alcaldia.toUpperCase().includes(currentAlc)) return false;
          if (filterState.canastaBasica && !t.canasta_basica) return false;
          if (filterState.mercomuna && !t.mercomuna) return false;
          if (q) {{
            const searchStr = `${{t.nombre_popular || ''}} ${{t.nombre || ''}} ${{t.colonia || ''}} ${{t.ubicacion || ''}} ${{t.alcaldia || ''}} ${{t.giro || ''}}`.toLowerCase();
            if (!searchStr.includes(q)) return false;
          }}
          return true;
        }});
      }}

      // 2. Filtrar MSR
      let filteredMSR = [];
      if (filterState.showMSR && data.msr) {{
        filteredMSR = data.msr.filter(m => {{
          if (currentDay !== 'TODOS' && (!m.dia || !m.dia.toUpperCase().includes(currentDay))) return false;
          if (currentAlc !== 'TODAS' && m.alcaldia && !m.alcaldia.toUpperCase().includes(currentAlc)) return false;
          if (filterState.canastaBasica && !m.canasta_basica) return false;
          if (filterState.mercomuna && !m.mercomuna) return false;
          if (q) {{
            const searchStr = `${{m.nombre || ''}} ${{m.ruta || ''}} ${{m.colonia || ''}} ${{m.direccion || ''}} ${{m.alcaldia || ''}}`.toLowerCase();
            if (!searchStr.includes(q)) return false;
          }}
          return true;
        }});
      }}

      // 3. Filtrar Concentraciones
      let filteredConcentraciones = [];
      if (filterState.showConcentraciones && data.concentraciones) {{
        filteredConcentraciones = data.concentraciones.filter(c => {{
          if (currentDay !== 'TODOS' && c.dias_operacion_lista && !c.dias_operacion_lista.includes(currentDay)) return false;
          if (currentAlc !== 'TODAS' && c.alcaldia && !c.alcaldia.toUpperCase().includes(currentAlc)) return false;
          if (filterState.canastaBasica && !c.canasta_basica) return false;
          if (filterState.mercomuna && !c.mercomuna) return false;
          if (q) {{
            const searchStr = `${{c.nombre || ''}} ${{c.colonia || ''}} ${{c.ubicacion || ''}} ${{c.alcaldia || ''}} ${{c.giro || ''}}`.toLowerCase();
            if (!searchStr.includes(q)) return false;
          }}
          return true;
        }});
      }}

      // 4. Filtrar Mercados Fijos (Opcional)
      let filteredMercados = [];
      if (filterState.showMercados && data.mercados) {{
        filteredMercados = data.mercados.filter(m => {{
          if (currentAlc !== 'TODAS' && m.alcaldia && !m.alcaldia.toUpperCase().includes(currentAlc)) return false;
          if (filterState.canastaBasica && !m.canasta_basica) return false;
          if (filterState.mercomuna && !m.mercomuna) return false;
          if (q) {{
            const searchStr = `${{m.nombre || ''}} ${{m.colonia || ''}} ${{m.alcaldia || ''}} ${{m.giro || ''}}`.toLowerCase();
            if (!searchStr.includes(q)) return false;
          }}
          return true;
        }});
      }}

      // Render Tianguis Markers
      layers.tianguis.clearLayers();
      filteredTianguis.forEach(t => {{
        const marker = L.circleMarker([t.lat, t.lon], {{
          radius: 6,
          fillColor: '#0f766e',
          color: '#ffffff',
          weight: 1.5,
          opacity: 1,
          fillOpacity: 0.88
        }});
        marker.on('click', () => {{
          showSpaceDetail(t, 'tianguis');
        }});
        layers.tianguis.addLayer(marker);
      }});
      if (filterState.showTianguis) {{
        if (!map.hasLayer(layers.tianguis)) layers.tianguis.addTo(map);
      }} else {{
        if (map.hasLayer(layers.tianguis)) map.removeLayer(layers.tianguis);
      }}

      // Render MSR Markers
      layers.msr.clearLayers();
      filteredMSR.forEach(m => {{
        const marker = L.circleMarker([m.lat, m.lon], {{
          radius: 7,
          fillColor: '#d97706',
          color: '#ffffff',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.9
        }});
        marker.on('click', () => {{
          showSpaceDetail(m, 'msr');
        }});
        layers.msr.addLayer(marker);
      }});
      if (filterState.showMSR) {{
        if (!map.hasLayer(layers.msr)) layers.msr.addTo(map);
      }} else {{
        if (map.hasLayer(layers.msr)) map.removeLayer(layers.msr);
      }}

      // Render Concentraciones Markers
      layers.concentraciones.clearLayers();
      filteredConcentraciones.forEach(c => {{
        const marker = L.circleMarker([c.lat, c.lon], {{
          radius: 6.5,
          fillColor: '#6d28d9',
          color: '#ffffff',
          weight: 1.8,
          opacity: 1,
          fillOpacity: 0.88
        }});
        marker.on('click', () => {{
          showSpaceDetail(c, 'concentracion');
        }});
        layers.concentraciones.addLayer(marker);
      }});
      if (filterState.showConcentraciones) {{
        if (!map.hasLayer(layers.concentraciones)) layers.concentraciones.addTo(map);
      }} else {{
        if (map.hasLayer(layers.concentraciones)) map.removeLayer(layers.concentraciones);
      }}

      // Render Mercados Markers
      layers.mercados.clearLayers();
      filteredMercados.forEach(m => {{
        const marker = L.circleMarker([m.lat, m.lon], {{
          radius: m.radio || 7,
          fillColor: '#ca8a04',
          color: '#ffffff',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.88
        }});
        marker.on('click', () => {{
          showSpaceDetail(m, 'mercado');
        }});
        layers.mercados.addLayer(marker);
      }});
      if (filterState.showMercados) {{
        if (!map.hasLayer(layers.mercados)) layers.mercados.addTo(map);
      }} else {{
        if (map.hasLayer(layers.mercados)) map.removeLayer(layers.mercados);
      }}

      // Actualizar Badges y Contadores
      const totalActivos = filteredTianguis.length + filteredMSR.length + filteredConcentraciones.length + filteredMercados.length;
      document.getElementById('badge-count-tianguis').innerText = filteredTianguis.length.toLocaleString();
      document.getElementById('badge-count-msr').innerText = filteredMSR.length.toLocaleString();
      document.getElementById('badge-count-concentraciones').innerText = filteredConcentraciones.length.toLocaleString();
      document.getElementById('badge-count-mercados').innerText = filterState.showMercados ? filteredMercados.length.toLocaleString() : 'Inactivo';

      const counterText = document.getElementById('results-counter-text');
      const resetBtn = document.getElementById('btn-reset-filters');
      counterText.innerHTML = `Mostrando <b>${{totalActivos.toLocaleString()}}</b> espacios de abasto popular`;

      const isFilterModified = filterState.day !== 'TODOS' || filterState.alcaldia !== 'TODAS' || !filterState.showTianguis || !filterState.showMSR || !filterState.showConcentraciones || filterState.showMercados || filterState.canastaBasica || filterState.mercomuna || filterState.searchQuery !== '';
      resetBtn.style.display = isFilterModified ? 'inline-block' : 'none';
    }}

    // =========================================================================
    // FICHA DE DETALLE (SIDEBAR)
    // =========================================================================
    function showSpaceDetail(item, type) {{
      currentSelectedCardData = item;
      const card = document.getElementById('detail-card');
      card.style.display = 'block';

      // Abrir sidebar en pantallas móviles
      const sidebar = document.getElementById('sidebar');
      if (sidebar.classList.contains('collapsed')) {{
        sidebar.classList.remove('collapsed');
      }}

      // Centrar mapa suavemente
      map.flyTo([item.lat, item.lon], Math.max(map.getZoom(), 15), {{ duration: 0.7 }});

      // Configurar badge y colores
      const tagEl = document.getElementById('card-tag');
      if (type === 'tianguis') {{
        tagEl.innerText = '🧺 TIANGUIS ITINERANTE';
        tagEl.style.background = '#0f766e';
      }} else if (type === 'msr') {{
        tagEl.innerText = '🚚 MERCADO SOBRE RUEDAS';
        tagEl.style.background = '#d97706';
      }} else if (type === 'concentracion') {{
        tagEl.innerText = '🏬 CONCENTRACIÓN BARRIAL';
        tagEl.style.background = '#6d28d9';
      }} else {{
        tagEl.innerText = '🏪 MERCADO PÚBLICO';
        tagEl.style.background = '#ca8a04';
      }}

      // Título y subtítulo
      const popularName = item.nombre_popular || item.nombre || 'Tianguis Popular';
      document.getElementById('card-name').innerText = popularName;
      document.getElementById('card-sub').innerText = `${{item.alcaldia || 'CDMX'}} · Col. ${{item.colonia || 'Sin colonia'}}`;

      // Ubicación exacta y entrecalles
      const street = item.ubicacion || item.direccion || 'Vía pública local';
      document.getElementById('card-street-text').innerText = street;

      // Calcular Estatus en Vivo
      const statusBanner = document.getElementById('card-status-banner');
      const statusText = document.getElementById('card-status-text');

      const now = new Date();
      const currentHour = now.getHours() + (now.getMinutes() / 60);
      const today = getTodayDayName();

      let operatesToday = false;
      if (type === 'tianguis' || type === 'msr') {{
        operatesToday = item.dia && item.dia.toUpperCase().includes(today);
      }} else if (type === 'concentracion') {{
        operatesToday = item.dias_operacion_lista ? item.dias_operacion_lista.includes(today) : true;
      }} else {{
        operatesToday = true;
      }}

      const horaApertura = item.hora_apertura || 8.0;
      const horaCierre = item.hora_cierre || 17.0;

      if (!operatesToday) {{
        statusBanner.className = 'status-live-banner status-closed';
        statusText.innerText = `🔴 No opera hoy · Días habituales: ${{item.dia || item.dias_operacion || 'Programado'}}`;
      }} else {{
        if (currentHour >= horaApertura && currentHour <= horaCierre) {{
          statusBanner.className = 'status-live-banner status-open';
          statusText.innerText = `🟢 Abierto hoy · En venta hasta las ${{Math.floor(horaCierre)}}:00 hrs`;
        }} else if (currentHour >= (horaApertura - 2) && currentHour < horaApertura) {{
          statusBanner.className = 'status-live-banner status-montaje';
          statusText.innerText = `🟡 En instalación y montaje de puestos (Abre a las ${{Math.floor(horaApertura)}}:00 hrs)`;
        }} else if (currentHour > horaCierre && currentHour <= (horaCierre + 2)) {{
          statusBanner.className = 'status-live-banner status-montaje';
          statusText.innerText = `🟡 En desmontaje y aseo vial (Cerró a las ${{Math.floor(horaCierre)}}:00 hrs)`;
        }} else {{
          statusBanner.className = 'status-live-banner status-closed';
          statusText.innerText = `🔴 Cerrado por hoy (Horario regular: ${{Math.floor(horaApertura)}}:00 a ${{Math.floor(horaCierre)}}:00 hrs)`;
        }}
      }}

      // Estadísticas
      document.getElementById('card-stat-dia').innerText = item.dia || (item.dias_operacion ? 'L-D' : 'Semanal');
      document.getElementById('card-stat-horario').innerText = item.horario || `${{Math.floor(horaApertura)}}:00-${{Math.floor(horaCierre)}}:00`;
      document.getElementById('card-stat-puestos').innerText = item.oferentes ? `~${{item.oferentes}}` : (item.num_oferentes ? `~${{item.num_oferentes}}` : '--');

      // Horarios operativos
      document.getElementById('card-time-montaje').innerText = `${{Math.max(0, Math.floor(horaApertura - 2))}}:00 a ${{Math.floor(horaApertura)}}:00 hrs`;
      document.getElementById('card-time-venta').innerText = `${{Math.floor(horaApertura)}}:00 a ${{Math.floor(horaCierre)}}:00 hrs`;
      document.getElementById('card-time-desmontaje').innerText = `${{Math.floor(horaCierre)}}:00 a ${{Math.min(24, Math.floor(horaCierre + 2))}}:00 hrs`;

      // Giros y Banderas
      const tagsBox = document.getElementById('card-tags-container');
      tagsBox.innerHTML = '';

      if (item.canasta_basica) {{
        tagsBox.innerHTML += `<span style="background:#ecfdf5; color:#065f46; border:1px solid #a7f3d0; padding:2px 6px; border-radius:4px; font-size:0.68rem; font-weight:700;">🧺 Canasta Básica</span>`;
      }}
      if (item.mercomuna) {{
        tagsBox.innerHTML += `<span style="background:#eff6ff; color:#1e40af; border:1px solid #bfdbfe; padding:2px 6px; border-radius:4px; font-size:0.68rem; font-weight:700;">💳 MERCOMUNA</span>`;
      }}

      const tags = item.tags || ['Frutas y Verduras', 'Abarrotes', 'Ropa', 'Comida'];
      tags.slice(0, 6).forEach(tg => {{
        tagsBox.innerHTML += `<span style="background:#f1f5f9; color:#334155; padding:2px 6px; border-radius:4px; font-size:0.68rem; font-weight:600;">${{tg}}</span>`;
      }});

      // Enlace a Google Maps
      const gmapsLink = document.getElementById('card-gmaps-link');
      gmapsLink.href = `https://www.google.com/maps/search/?api=1&query=${{item.lat}},${{item.lon}}`;

      // Scroll hacia la ficha en el sidebar
      card.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
    }}

    function closeDetailCard() {{
      const card = document.getElementById('detail-card');
      card.style.display = 'none';
      currentSelectedCardData = null;
    }}

    function copyCardCoords() {{
      if (!currentSelectedCardData) return;
      const coords = `${{currentSelectedCardData.lat.toFixed(6)}}, ${{currentSelectedCardData.lon.toFixed(6)}}`;
      navigator.clipboard.writeText(coords).then(() => {{
        showToast(`Coordenadas GPS copiadas: ${{coords}}`, 'success');
      }}).catch(() => {{
        showToast(`Coordenadas: ${{coords}}`, 'info');
      }});
    }}

    // =========================================================================
    // BUSCADOR PREDICTIVO UNIFICADO
    // =========================================================================
    function buildSearchIndex(data) {{
      SEARCH_INDEX = [];
      if (data.tianguis) {{
        data.tianguis.forEach(t => {{
          SEARCH_INDEX.push({{
            type: 'tianguis',
            badge: 'TIANGUIS',
            badgeColor: '#0f766e',
            title: t.nombre_popular || `Tianguis ${{t.colonia}}`,
            subtitle: `${{t.alcaldia}} · ${{t.dia}} · ${{t.ubicacion || t.colonia}}`,
            lat: t.lat,
            lon: t.lon,
            data: t,
            searchStr: `tianguis ${{t.nombre_popular || ''}} ${{t.nombre || ''}} ${{t.colonia || ''}} ${{t.ubicacion || ''}} ${{t.alcaldia || ''}} ${{t.dia || ''}} ${{t.giro || ''}}`.toLowerCase()
          }});
        }});
      }}
      if (data.msr) {{
        data.msr.forEach(m => {{
          SEARCH_INDEX.push({{
            type: 'msr',
            badge: 'MSR',
            badgeColor: '#d97706',
            title: m.nombre || `MSR ${{m.ruta}}`,
            subtitle: `${{m.alcaldia}} · ${{m.dia}} · ${{m.colonia}}`,
            lat: m.lat,
            lon: m.lon,
            data: m,
            searchStr: `msr mercado sobre ruedas ${{m.nombre || ''}} ${{m.ruta || ''}} ${{m.colonia || ''}} ${{m.direccion || ''}} ${{m.alcaldia || ''}} ${{m.dia || ''}}`.toLowerCase()
          }});
        }});
      }}
      if (data.concentraciones) {{
        data.concentraciones.forEach(c => {{
          SEARCH_INDEX.push({{
            type: 'concentracion',
            badge: 'CONCENTRACIÓN',
            badgeColor: '#6d28d9',
            title: c.nombre_popular || c.nombre,
            subtitle: `${{c.alcaldia}} · Col. ${{c.colonia}}`,
            lat: c.lat,
            lon: c.lon,
            data: c,
            searchStr: `concentracion comerciante ${{c.nombre || ''}} ${{c.colonia || ''}} ${{c.ubicacion || ''}} ${{c.alcaldia || ''}} ${{c.giro || ''}}`.toLowerCase()
          }});
        }});
      }}
    }}

    function onCommerceSearchInput(val) {{
      filterState.searchQuery = val;
      const clearBtn = document.getElementById('commerce-search-clear');
      clearBtn.style.display = val.length > 0 ? 'block' : 'none';

      const dropdown = document.getElementById('commerce-autocomplete-dropdown');
      if (val.trim().length < 2) {{
        dropdown.style.display = 'none';
        applyAllFilters();
        return;
      }}

      const q = val.toLowerCase().trim();
      const matches = SEARCH_INDEX.filter(item => item.searchStr.includes(q)).slice(0, 8);

      if (matches.length === 0) {{
        dropdown.innerHTML = `<div style="padding:10px; font-size:0.75rem; color:#64748b; text-align:center;">No se encontraron tianguis o calles con "${{val}}"</div>`;
        dropdown.style.display = 'block';
      }} else {{
        dropdown.innerHTML = matches.map((m, idx) => `
          <div class="autocomplete-item" onclick="selectSearchMatch(${{idx}})">
            <div class="autocomplete-title">
              <span class="autocomplete-badge" style="background:${{m.badgeColor}};">${{m.badge}}</span>
              <span>${{highlightMatch(m.title, q)}}</span>
            </div>
            <div class="autocomplete-sub">${{highlightMatch(m.subtitle, q)}}</div>
          </div>
        `).join('');
        dropdown.style.display = 'block';
        window._currentMatches = matches;
      }}

      applyAllFilters();
    }}

    function highlightMatch(text, q) {{
      if (!text) return '';
      const idx = text.toLowerCase().indexOf(q);
      if (idx === -1) return text;
      return text.substring(0, idx) + '<b style="color:#0f5953; background:#ccfbf1;">' + text.substring(idx, idx + q.length) + '</b>' + text.substring(idx + q.length);
    }}

    function selectSearchMatch(idx) {{
      if (!window._currentMatches || !window._currentMatches[idx]) return;
      const item = window._currentMatches[idx];
      document.getElementById('commerce-search-input').value = item.title;
      document.getElementById('commerce-autocomplete-dropdown').style.display = 'none';

      showSpaceDetail(item.data, item.type);
    }}

    function clearCommerceSearch() {{
      document.getElementById('commerce-search-input').value = '';
      document.getElementById('commerce-search-clear').style.display = 'none';
      document.getElementById('commerce-autocomplete-dropdown').style.display = 'none';
      filterState.searchQuery = '';
      applyAllFilters();
    }}

    // Cerrar autocomplete si se hace click fuera
    document.addEventListener('click', (e) => {{
      const container = document.querySelector('.search-input-container');
      if (container && !container.contains(e.target)) {{
        const dropdown = document.getElementById('commerce-autocomplete-dropdown');
        if (dropdown) dropdown.style.display = 'none';
      }}
    }});

    // =========================================================================
    // MODAL DE AFECTACIONES Y CALLES OCUPADAS
    // =========================================================================
    function openCierresModal() {{
      const overlay = document.getElementById('cierres-modal-overlay');
      overlay.style.display = 'flex';
      switchModalTab('hoy');
    }}

    function closeCierresModal() {{
      document.getElementById('cierres-modal-overlay').style.display = 'none';
    }}

    function handleModalOverlayClick(e) {{
      if (e.target.id === 'cierres-modal-overlay') {{
        closeCierresModal();
      }}
    }}

    function switchModalTab(tabKey) {{
      document.querySelectorAll('.modal-tab-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('modal-tab-' + tabKey);
      if (activeBtn) activeBtn.classList.add('active');

      const contentBox = document.getElementById('modal-body-content');
      const today = getTodayDayName();

      const cierres = (window.MAP_DATA && window.MAP_DATA.cierres_viales) ? window.MAP_DATA.cierres_viales : EMBEDDED_CIERRES;
      const dayData = (cierres.dias && cierres.dias[today]) ? cierres.dias[today] : {{}};
      const semStats = cierres.resumen_semanal || {{}};

      if (tabKey === 'hoy') {{
        const tianguisCount = dayData.total_tianguis || 194;
        const kmOcupados = dayData.km_lineales_ocupados || 42.15;
        const oferentesTot = dayData.oferentes_totales || 29070;
        const corredores = dayData.top_corredores || [];

        let corredoresHtml = '';
        if (corredores.length > 0) {{
          corredoresHtml = corredores.map(c => `
            <tr>
              <td><b>${{c.corredor}}</b></td>
              <td>${{c.alcaldias ? c.alcaldias.join(', ') : 'CDMX'}}</td>
              <td><b>${{c.oferentes ? c.oferentes.toLocaleString() : '--'}}</b> puestos</td>
              <td>~${{c.km_lineales ? c.km_lineales.toFixed(2) : '--'}} km</td>
              <td><span style="background:#fef3c7; color:#92400e; padding:2px 6px; border-radius:4px; font-weight:700;">${{c.tipo_afectacion || 'Cierre de calle'}}</span></td>
            </tr>
          `).join('');
        }} else {{
          corredoresHtml = `<tr><td colspan="5" style="text-align:center; color:#64748b;">No hay corredores viales reportados.</td></tr>`;
        }}

        contentBox.innerHTML = `
          <div style="margin-bottom:14px;">
            <div style="font-size:0.95rem; font-weight:800; color:var(--cdmx-green-dark); margin-bottom:2px;">
              Ocupación de Espacio Público Hoy (${{NOMBRE_DIAS[today]}})
            </div>
            <div style="font-size:0.75rem; color:#64748b;">
              Datos derivados del Padrón de Tianguis y Mercados Sobre Ruedas de la Ciudad de México.
            </div>
          </div>

          <div class="kpi-row">
            <div class="kpi-card">
              <div class="kpi-val">${{tianguisCount}}</div>
              <div class="kpi-lbl">Tianguis Hoy</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-val">${{kmOcupados}} km</div>
              <div class="kpi-lbl">Vía Ocupada</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-val">${{oferentesTot.toLocaleString()}}</div>
              <div class="kpi-lbl">Oferentes Hoy</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-val">100%</div>
              <div class="kpi-lbl">Comunitario</div>
            </div>
          </div>

          <div style="margin-top:16px;">
            <div style="font-size:0.82rem; font-weight:800; color:#334155; margin-bottom:6px;">
              🚦 Top Avenidas y Corredores con Cierre Vial Hoy:
            </div>
            <table class="corredores-table">
              <thead>
                <tr>
                  <th>Avenida / Calle</th>
                  <th>Alcaldía</th>
                  <th>Puestos Est.</th>
                  <th>Longitud</th>
                  <th>Tipo Afectación</th>
                </tr>
              </thead>
              <tbody>
                ${{corredoresHtml}}
              </tbody>
            </table>
          </div>
        `;

      }} else if (tabKey === 'semana') {{
        const totalTianguis = semStats.total_tianguis_catalogo || 1367;
        const totalKmSem = semStats.km_lineales_acumulados_semana || 330.0;
        const totalOferentes = semStats.oferentes_acumulados_semana || 239628;
        const top10 = semStats.top_10_corredores_cdmx || [];

        let top10Html = top10.map((c, i) => `
          <tr>
            <td><b>#${{i+1}} ${{c.corredor}}</b></td>
            <td>${{c.alcaldias ? c.alcaldias.join(', ') : 'CDMX'}}</td>
            <td>${{c.tianguis_instalaciones_semana || 1}} por sem</td>
            <td><b>${{c.oferentes_totales ? c.oferentes_totales.toLocaleString() : '--'}}</b> oferentes</td>
            <td>${{c.km_ocupados_semana || '--'}} km</td>
          </tr>
        `).join('');

        contentBox.innerHTML = `
          <div style="margin-bottom:14px;">
            <div style="font-size:0.95rem; font-weight:800; color:var(--cdmx-green-dark); margin-bottom:2px;">
              Impacto Semanal del Comercio Popular en la CDMX
            </div>
            <div style="font-size:0.75rem; color:#64748b;">
              Balance acumulado semanal de tianguis en las 16 demarcaciones territoriales.
            </div>
          </div>

          <div class="kpi-row">
            <div class="kpi-card">
              <div class="kpi-val">${{totalTianguis}}</div>
              <div class="kpi-lbl">Tianguis en Padrón</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-val">${{totalKmSem}} km</div>
              <div class="kpi-lbl">Km Lineales / Sem</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-val">${{totalOferentes.toLocaleString()}}</div>
              <div class="kpi-lbl">Oferentes / Sem</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-val">16</div>
              <div class="kpi-lbl">Alcaldías</div>
            </div>
          </div>

          <div style="margin-top:16px;">
            <div style="font-size:0.82rem; font-weight:800; color:#334155; margin-bottom:6px;">
              🏆 Los 10 Corredores Populares Más Extensos de la CDMX:
            </div>
            <table class="corredores-table">
              <thead>
                <tr>
                  <th>Corredor</th>
                  <th>Alcaldías</th>
                  <th>Instalaciones</th>
                  <th>Oferentes Semanales</th>
                  <th>Km Ocupados</th>
                </tr>
              </thead>
              <tbody>
                ${{top10Html}}
              </tbody>
            </table>
          </div>
        `;

      }} else if (tabKey === 'normativa') {{
        contentBox.innerHTML = `
          <div style="font-size:0.82rem; line-height:1.6; color:#334155;">
            <div style="font-size:0.95rem; font-weight:800; color:var(--cdmx-green-dark); margin-bottom:8px;">
              Protocolos de Convivencia y Operación en Vía Pública
            </div>
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:12px; margin-bottom:12px;">
              <div style="font-weight:700; color:#0f766e; margin-bottom:4px;">⏰ Horarios Normativos Habituales (SEDECO):</div>
              <ul style="margin-left:18px; font-size:0.75rem; color:#475569;">
                <li><b>Montaje de estructuras:</b> 06:00 a 08:00 hrs.</li>
                <li><b>Horario de atención al público:</b> 08:00 a 17:00 hrs.</li>
                <li><b>Desmontaje, retiro y aseo barrial:</b> 17:00 a 19:00 hrs.</li>
              </ul>
            </div>

            <div style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:10px; padding:12px; margin-bottom:12px;">
              <div style="font-weight:700; color:#065f46; margin-bottom:4px;">🛡️ Principios Éticos y Soberanía Comunitaria:</div>
              <p style="font-size:0.75rem; color:#065f46; margin-bottom:6px;">
                Este portal reconoce la gobernanza histórica de las mesas directivas, comisiones electas en asamblea y dinámicas barriales de los tianguis de la Ciudad de México.
              </p>
              <p style="font-size:0.75rem; color:#065f46;">
                <b>No al extractivismo de datos:</b> Esta herramienta es de consulta libre para las familias y los comerciantes, sin intermediarios ni vigilancia punitiva.
              </p>
            </div>
          </div>
        `;
      }}
    }}

    // =========================================================================
    // UTILIDADES: TOASTS, GEOLOCALIZACIÓN Y UI
    // =========================================================================
    function toggleSidebar() {{
      const sidebar = document.getElementById('sidebar');
      sidebar.classList.toggle('collapsed');
      const btnOpen = document.getElementById('btn-open-sidebar');
      if (sidebar.classList.contains('collapsed')) {{
        btnOpen.style.display = 'flex';
      }} else {{
        btnOpen.style.display = 'none';
      }}
      setTimeout(() => map.invalidateSize(), 320);
    }}

    function locateUser() {{
      showToast('Buscando ubicación actual...', 'info');
      map.locate({{ setView: true, maxZoom: 15, timeout: 10000, enableHighAccuracy: true }});
    }}

    map.on('locationfound', (e) => {{
      const marker = L.circleMarker(e.latlng, {{
        radius: 8,
        fillColor: '#2563eb',
        color: '#ffffff',
        weight: 2.5,
        opacity: 1,
        fillOpacity: 0.95
      }}).addTo(map);
      marker.bindPopup('<b>Tu ubicación actual</b>').openPopup();
      showToast('Ubicación encontrada.', 'success');
    }});

    map.on('locationerror', (e) => {{
      showToast('No se pudo acceder a tu ubicación actual.', 'warning');
    }});

    function showToast(msg, type = 'info', duration = 3000) {{
      const container = document.getElementById('toast-container');
      const toast = document.createElement('div');
      toast.className = 'toast-msg';

      let borderCol = '#0f766e';
      if (type === 'success') borderCol = '#10b981';
      if (type === 'warning') borderCol = '#f59e0b';
      if (type === 'error') borderCol = '#ef4444';

      toast.style.borderLeft = `4px solid ${{borderCol}}`;
      toast.innerText = msg;
      container.appendChild(toast);

      setTimeout(() => {{
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(8px)';
        toast.style.transition = 'all 0.25s ease';
        setTimeout(() => toast.remove(), 260);
      }}, duration);
    }}

    // Iniciar aplicación al cargar el DOM
    window.addEventListener('DOMContentLoaded', () => {{
      initApplication();
    }});
  </script>
</body>
</html>
"""

    with open('mapa_comercio_movilidad_cdmx.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"mapa_comercio_movilidad_cdmx.html generado exitosamente ({len(html)} bytes).")

if __name__ == '__main__':
    build_map_html()
