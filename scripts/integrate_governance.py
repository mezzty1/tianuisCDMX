#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de integración del Módulo 5.4: Gobernanza Barrial y Auditoría Comunitaria
Modifica scripts/build_revamped_map.py para incorporar los componentes interactivos
y genera el mapa final mapa_comercio_movilidad_cdmx.html.
"""

import os
import re

BUILD_SCRIPT = 'scripts/build_revamped_map.py'

def run():
    with open(BUILD_SCRIPT, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Añadir script de governance_engine.js
    script_target = '  <!-- Datos empaquetados en JS (garantiza funcionamiento sin servidor ni problemas CORS) -->'
    script_replacement = '''  <!-- Módulo de Gobernanza Barrial y Auditoría Comunitaria Ponderada (Módulo 5.4) -->
  <script src="scripts/governance_engine.js"></script>

  <!-- Datos empaquetados en JS (garantiza funcionamiento sin servidor ni problemas CORS) -->'''
    if 'scripts/governance_engine.js' not in content:
        assert script_target in content, "No se encontró el target para el script"
        content = content.replace(script_target, script_replacement, 1)

    # 2. Añadir estilos CSS antes de </style>
    css_target = '      .stat-cards-grid {\n        grid-template-columns: 1fr;\n      }\n    }\n  </style>'
    css_to_add = '''      .stat-cards-grid {
        grid-template-columns: 1fr;
      }
    }

    /* =========================================================================
       GOBERNANZA BARRIAL Y AUDITORÍA COMUNITARIA PONDERADA (MÓDULO 5.4)
       ========================================================================= */
    .governance-card {
      background: #ffffff;
      border: 1px solid var(--slate-200);
      border-radius: 12px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }

    .gov-header-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }

    .gov-title {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: var(--slate-700);
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .badge-epistemic {
      font-size: 10px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 10px;
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }

    .badge-epistemic-confirmado {
      background: #ecfdf5;
      color: #065f46;
      border: 1px solid #a7f3d0;
    }

    .badge-epistemic-propuesto {
      background: #f8fafc;
      color: #475569;
      border: 1px dashed #94a3b8;
    }

    .badge-epistemic-disputa {
      background: #fef3c7;
      color: #92400e;
      border: 1px solid #fde68a;
    }

    .gov-btn-row {
      display: flex;
      gap: 8px;
    }

    .btn-gov-vote {
      flex: 1;
      padding: 8px 10px;
      border-radius: 8px;
      font-size: 11.5px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      transition: all 0.15s ease;
      font-family: inherit;
    }

    .btn-gov-vote:disabled {
      opacity: 0.55;
      cursor: not-allowed;
    }

    .btn-gov-yes {
      background: #ecfdf5;
      color: #065f46;
      border: 1.5px solid #10b981;
    }

    .btn-gov-yes:hover:not(:disabled) {
      background: #d1fae5;
      transform: translateY(-1px);
    }

    .btn-gov-no {
      background: #fef2f2;
      color: #991b1b;
      border: 1.5px solid #ef4444;
    }

    .btn-gov-no:hover:not(:disabled) {
      background: #fee2e2;
      transform: translateY(-1px);
    }

    .gov-balance-box {
      font-size: 11.5px;
      color: var(--slate-700);
      background: var(--slate-50);
      border: 1px solid var(--slate-200);
      border-radius: 8px;
      padding: 7px 10px;
      line-height: 1.4;
    }

    .gov-payment-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      padding: 6px 8px;
      background: var(--slate-50);
      border: 1px solid var(--slate-200);
      border-radius: 8px;
      font-size: 11.5px;
    }

    .btn-gov-small {
      background: #ffffff;
      border: 1px solid var(--slate-300);
      color: var(--slate-700);
      font-size: 10.5px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: inherit;
    }

    .btn-gov-small:hover:not(:disabled) {
      background: var(--cdmx-green-light);
      color: var(--cdmx-green-dark);
      border-color: var(--cdmx-green-primary);
    }

    .product-tag-chip.chip-confirmed {
      background: #ecfdf5;
      color: #065f46;
      border: 1px solid #a7f3d0;
      font-weight: 600;
    }

    .product-tag-chip.chip-proposed {
      background: #f8fafc;
      color: #334155;
      border: 1.5px dashed #94a3b8;
    }

    .product-tag-chip.chip-dispute {
      background: #fef3c7;
      color: #92400e;
      border: 1px solid #fde68a;
    }

    .marker-comm-dot {
      position: absolute;
      top: -3px;
      right: -3px;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      border: 1.5px solid #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 8.5px;
      font-weight: 800;
      box-shadow: 0 1px 3px rgba(0,0,0,0.3);
      z-index: 2;
    }

    .marker-comm-dot.confirmed {
      background: #059669;
      color: #ffffff;
    }

    .marker-comm-dot.dispute {
      background: #d97706;
      color: #ffffff;
      animation: pulse-dispute 1.8s infinite;
    }

    .marker-comm-dot.active {
      background: #0284c7;
      color: #ffffff;
    }

    @keyframes pulse-dispute {
      0% { transform: scale(1); }
      50% { transform: scale(1.25); }
      100% { transform: scale(1); }
    }

    .gov-toolbar {
      background: var(--slate-50);
      border: 1px solid var(--slate-200);
      border-radius: 10px;
      padding: 9px 12px;
      display: flex;
      flex-direction: column;
      gap: 7px;
      font-size: 11px;
    }

    .gov-toolbar-actions {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }
  </style>'''
    if '.governance-card' not in content:
        assert css_target in content, "No se encontró el target para CSS"
        content = content.replace(css_target, css_to_add, 1)

    # 3. Añadir tarjetas de Gobernanza en la ficha lateral (tianguis-sidebar)
    sidebar_target = '''        <!-- ESTATUS EN VIVO -->
        <div class="status-card" id="side-status-card">
          <div class="status-indicator-dot"></div>
          <div class="status-card-text">
            <div class="status-headline" id="side-status-headline">🟢 Abierto hoy hasta las 17:00 hrs</div>
            <div class="status-subline" id="side-status-subline">En horario de venta al público</div>
          </div>
        </div>

        <!-- ESPECIALIDAD / VOCACIÓN COMUNITARIA NLP -->
        <div class="detail-section">
          <span class="detail-label">Vocación y Especialidad Comunitaria</span>
          <div class="detail-value-bold" id="side-vocation-title">Ropa de Paca, Herramientas y Chácharas</div>
          <div class="detail-value" id="side-vocation-desc" style="font-size: 12.5px; line-height: 1.5; color: var(--slate-700); margin-top: 4px;">Megatianguis emblemático de segunda mano, antigüedades y antojitos.</div>
          
          <div style="margin-top: 10px;">
            <span style="font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--slate-500);">Artículos más elogiados por visitantes:</span>
            <div class="product-tags-cloud" id="side-product-tags" style="margin-top: 4px;"></div>
          </div>
        </div>'''

    sidebar_replacement = '''        <!-- ESTATUS EN VIVO OFICIAL (RELOJ SEDECO) -->
        <div class="status-card" id="side-status-card">
          <div class="status-indicator-dot"></div>
          <div class="status-card-text">
            <div class="status-headline" id="side-status-headline">🟢 Abierto hoy hasta las 17:00 hrs</div>
            <div class="status-subline" id="side-status-subline">En horario de venta al público</div>
          </div>
        </div>

        <!-- AUDITORÍA COMUNITARIA: ESTATUS EN VIVO HOY (MÓDULO 5.4) -->
        <div class="governance-card" id="gov-live-card">
          <div class="gov-header-row">
            <span class="gov-title"><span>👥</span> Auditoría Barrial en Vivo</span>
            <span class="badge-epistemic" id="gov-live-epistemic-badge">✓ Verificado</span>
          </div>
          <div style="font-size: 11.5px; font-weight: 600; color: var(--slate-800);">
            ¿Se instaló el tianguis hoy?
          </div>
          <div class="gov-btn-row">
            <button class="btn-gov-vote btn-gov-yes" id="btn-gov-live-yes">
              <span>🟢</span> Sí, está operando
            </button>
            <button class="btn-gov-vote btn-gov-no" id="btn-gov-live-no">
              <span>🔴</span> Hoy no se puso
            </button>
          </div>
          <div class="gov-balance-box" id="gov-live-balance-text">
            Balance comunitario de hoy: Evaluando...
          </div>
        </div>

        <!-- AUDITORÍA COMUNITARIA: MEDIOS DE PAGO REALES (MÓDULO 5.4) -->
        <div class="governance-card" id="gov-payments-card">
          <div class="gov-header-row">
            <span class="gov-title"><span>💳</span> Medios de Pago Auditados</span>
            <span style="font-size: 10px; color: var(--slate-500); font-weight: 600;">Validación Barrial</span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 6px;" id="gov-payments-list"></div>
        </div>

        <!-- ESPECIALIDAD / VOCACIÓN COMUNITARIA NLP Y AUDITORÍA CROWDSOURCING (MÓDULO 5.4 Y 5.5) -->
        <div class="detail-section">
          <div class="gov-header-row" style="margin-bottom: 2px;">
            <span class="detail-label">Vocación y Especialidad Comunitaria</span>
            <span class="badge-epistemic badge-epistemic-confirmado" style="font-size: 9.5px;">IA NLP + Barrio</span>
          </div>
          <div class="detail-value-bold" id="side-vocation-title">Ropa de Paca, Herramientas y Chácharas</div>
          <div class="detail-value" id="side-vocation-desc" style="font-size: 12.5px; line-height: 1.5; color: var(--slate-700); margin-top: 4px;">Megatianguis emblemático de segunda mano, antigüedades y antojitos.</div>
          
          <div style="margin-top: 10px;">
            <div class="gov-header-row" style="margin-bottom: 6px;">
              <span style="font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--slate-500);">Especialidades del tianguis:</span>
              <button class="btn-gov-small" id="btn-toggle-propose" style="font-size: 10px; padding: 2px 7px;">+ Proponer giro</button>
            </div>

            <!-- Mini-formulario para proponer especialidad -->
            <div id="gov-propose-form" style="display: none; background: var(--slate-50); border: 1px solid var(--slate-200); border-radius: 8px; padding: 8px 10px; margin-bottom: 8px;">
              <div style="font-size: 11px; font-weight: 700; color: var(--slate-800); margin-bottom: 4px;">Proponer nuevo artículo o giro popular:</div>
              <div style="display: flex; gap: 6px;">
                <input type="text" id="input-new-specialty" placeholder="Ej. Barbacoa de borrego, Tepache, Plantas..." style="flex: 1; font-size: 11px; padding: 5px 8px; border: 1px solid var(--slate-300); border-radius: 6px; font-family: inherit;">
                <button class="btn-gov-small" id="btn-submit-propose" style="background: var(--cdmx-green-primary); color: #fff; border: none;">Guardar</button>
              </div>
              <div style="font-size: 9.5px; color: var(--slate-500); margin-top: 3px;">Entra en estado [PROPUESTO] hasta acumular validaciones comunitarias.</div>
            </div>

            <div class="product-tags-cloud" id="side-product-tags" style="margin-top: 4px; display: flex; flex-wrap: wrap; gap: 6px;"></div>
          </div>
        </div>'''

    if 'id="gov-live-card"' not in content:
        assert sidebar_target in content, "No se encontró el target para sidebar"
        content = content.replace(sidebar_target, sidebar_replacement, 1)

    # 4. Añadir barra de gobernanza y testing al final del cuerpo del sidebar
    toolbar_target = '''        <!-- OPERACIÓN Y HORARIOS SEDECO -->
        <div class="detail-section">
          <span class="detail-label">Días y Horarios Oficiales (SEDECO)</span>
          <div class="detail-value">
            Días de instalación: <strong id="side-dias-list">DOMINGO</strong>
          </div>
          <div style="font-size: 11.5px; color: var(--slate-600); background: var(--slate-50); border: 1px solid var(--slate-200); border-radius: 8px; padding: 8px 10px; margin-top: 4px;">
            <div>• <strong>06:00 a 08:00</strong>: Montaje e instalación de puestos</div>
            <div>• <strong>08:00 a 17:00</strong>: Venta al público</div>
            <div>• <strong>17:00 a 19:00</strong>: Desmontaje y retiro ordenado</div>
          </div>
        </div>
      </div>'''

    toolbar_replacement = '''        <!-- OPERACIÓN Y HORARIOS SEDECO -->
        <div class="detail-section">
          <span class="detail-label">Días y Horarios Oficiales (SEDECO)</span>
          <div class="detail-value">
            Días de instalación: <strong id="side-dias-list">DOMINGO</strong>
          </div>
          <div style="font-size: 11.5px; color: var(--slate-600); background: var(--slate-50); border: 1px solid var(--slate-200); border-radius: 8px; padding: 8px 10px; margin-top: 4px;">
            <div>• <strong>06:00 a 08:00</strong>: Montaje e instalación de puestos</div>
            <div>• <strong>08:00 a 17:00</strong>: Venta al público</div>
            <div>• <strong>17:00 a 19:00</strong>: Desmontaje y retiro ordenado</div>
          </div>
        </div>

        <!-- BARRA CÍVICA Y HERRAMIENTAS DE AUDITORÍA ABIERTA (TESTING Y CARE) -->
        <div class="gov-toolbar">
          <div style="display: flex; align-items: center; justify-content: space-between;">
            <span style="font-weight: 700; color: var(--slate-700);">📍 Proof of Location:</span>
            <button class="btn-gov-small" id="btn-toggle-simulate" style="font-size: 10px; padding: 2px 8px;">
              GPS: Remoto (+1 pt)
            </button>
          </div>
          <div class="gov-toolbar-actions">
            <button class="btn-gov-small" id="btn-reload-demo">🎲 Datos demo</button>
            <button class="btn-gov-small" id="btn-reset-votes">🔄 Reset votos</button>
            <button class="btn-gov-small" id="btn-view-json">📋 Ver JSON</button>
          </div>
        </div>
      </div>'''

    if 'id="btn-toggle-simulate"' not in content:
        assert toolbar_target in content, "No se encontró el target para toolbar"
        content = content.replace(toolbar_target, toolbar_replacement, 1)

    # 5. Añadir modal de JSON antes de </body>
    modal_target = '''  <!-- TOAST FLOTANTE -->
  <div id="toast">
    <span id="toast-icon">✓</span>
    <span id="toast-msg">Mensaje de notificación</span>
  </div>'''

    modal_replacement = '''  <!-- MODAL DE INSPECCIÓN JSON DE AUDITORÍA COMUNITARIA (MÓDULO 5.4) -->
  <div id="json-modal-backdrop" style="display: none; position: fixed; inset: 0; background: rgba(15, 23, 42, 0.4); z-index: 2500; align-items: center; justify-content: center; padding: 20px;">
    <div style="background: #ffffff; border-radius: 16px; width: 100%; max-width: 600px; max-height: 80vh; display: flex; flex-direction: column; overflow: hidden; box-shadow: var(--shadow-xl); border: 1px solid var(--slate-200);">
      <div class="modal-header">
        <h3 class="modal-title">📋 Auditoría Abierta · Registro Local (JSON)</h3>
        <button class="btn-close-sidebar" id="btn-close-json-modal">✕</button>
      </div>
      <div style="padding: 16px; overflow-y: auto; flex: 1; background: #0f172a; color: #f8fafc; font-family: monospace; font-size: 11px; white-space: pre-wrap; line-height: 1.5;" id="json-modal-content"></div>
    </div>
  </div>

  <!-- TOAST FLOTANTE -->
  <div id="toast">
    <span id="toast-icon">✓</span>
    <span id="toast-msg">Mensaje de notificación</span>
  </div>'''

    if 'id="json-modal-backdrop"' not in content:
        assert modal_target in content, "No se encontró el target para modal"
        content = content.replace(modal_target, modal_replacement, 1)

    # 6. Inicializar GovernanceEngine en setupApp(data)
    setup_target = '''      function setupApp(data) {
        state.tianguis = data.tianguis || [];'''
    setup_replacement = '''      function setupApp(data) {
        state.tianguis = data.tianguis || [];
        if (window.GovernanceEngine) {
          window.GovernanceEngine.initializeOrSeed(state.tianguis);
        }'''
    if 'initializeOrSeed' not in content:
        assert setup_target in content, "No se encontró el target para setupApp"
        content = content.replace(setup_target, setup_replacement, 1)

    # 7. Marcadores de mapa con badges comunitarios en renderMapMarkers()
    markers_target = '''        filtered.forEach(t => {
          const status = getLiveStatus(t, state.activeDay);
          if (status.isOpenNow) openCount++;

          const iconHtml = `<div class="marker-pin ${status.markerClass}" title="${t.nombre_popular}">${t.escala_icono || '🎪'}</div>`;
          const customIcon = L.divIcon({
            html: iconHtml,
            className: 'tianguis-marker-icon',
            iconSize: [28, 28],
            iconAnchor: [14, 14]
          });

          const marker = L.marker([t.lat, t.lng], { icon: customIcon });

          // Tooltip sobrio
          marker.bindTooltip(`
            <div style="font-weight: 700; font-size: 12px; color: #0f172a;">${t.nombre_popular}</div>
            <div style="font-size: 10.5px; color: #64748b;">${status.headline} · ${t.oferentes} oferentes</div>
          `, { direction: 'top', offset: [0, -10] });'''

    markers_replacement = '''        filtered.forEach(t => {
          const status = getLiveStatus(t, state.activeDay);
          if (status.isOpenNow) openCount++;

          // Estado de gobernanza barrial comunitaria (Módulo 5.4)
          const commStatus = (window.GovernanceEngine) ? window.GovernanceEngine.getMarkerCommunityStatus(t.id) : null;
          let commBadgeHtml = '';
          let commTooltipHtml = '';
          if (commStatus) {
            commBadgeHtml = `<span class="marker-comm-dot ${commStatus.badgeType}" title="${commStatus.text}">${commStatus.icon}</span>`;
            commTooltipHtml = `<div style="font-size: 10px; font-weight: 700; color: ${commStatus.color}; margin-top: 2px;">${commStatus.icon} ${commStatus.text}</div>`;
          }

          const iconHtml = `<div class="marker-pin ${status.markerClass}" title="${t.nombre_popular}">${t.escala_icono || '🎪'}${commBadgeHtml}</div>`;
          const customIcon = L.divIcon({
            html: iconHtml,
            className: 'tianguis-marker-icon',
            iconSize: [28, 28],
            iconAnchor: [14, 14]
          });

          const marker = L.marker([t.lat, t.lng], { icon: customIcon });

          // Tooltip sobrio enriquecido con auditoría barrial
          marker.bindTooltip(`
            <div style="font-weight: 700; font-size: 12px; color: #0f172a;">${t.nombre_popular}</div>
            <div style="font-size: 10.5px; color: #64748b;">${status.headline} · ${t.oferentes} oferentes</div>
            ${commTooltipHtml}
          `, { direction: 'top', offset: [0, -10] });'''

    if 'marker-comm-dot' not in content:
        assert markers_target in content, "No se encontró el target para markers"
        content = content.replace(markers_target, markers_replacement, 1)

    # 8. Integrar renderCommunityAuditSections(t) en openTianguisSidebar(t)
    sidebar_call_target = '''        // Botones de acción
        const gmapsBtn = document.getElementById('side-btn-gmaps');'''
    sidebar_call_replacement = '''        // Renderizar Módulo 5.4: Gobernanza Barrial y Auditoría Comunitaria
        renderCommunityAuditSections(t);

        // Botones de acción
        const gmapsBtn = document.getElementById('side-btn-gmaps');'''
    if 'renderCommunityAuditSections(t);' not in content:
        assert sidebar_call_target in content, "No se encontró el target para sidebar_call"
        content = content.replace(sidebar_call_target, sidebar_call_replacement, 1)

    # 9. Agregar la función renderCommunityAuditSections y handlers de modal al script
    fn_target = '''      function closeTianguisSidebar() {
        document.getElementById('tianguis-sidebar').classList.remove('open');
        state.selectedTianguis = null;
      }

      document.getElementById('btn-close-sidebar').addEventListener('click', closeTianguisSidebar);'''

    fn_replacement = '''      function closeTianguisSidebar() {
        document.getElementById('tianguis-sidebar').classList.remove('open');
        state.selectedTianguis = null;
      }

      document.getElementById('btn-close-sidebar').addEventListener('click', closeTianguisSidebar);

      // =========================================================================
      // MOTOR DE RENDERIZADO: GOBERNANZA BARRIAL Y AUDITORÍA COMUNITARIA (MÓDULO 5.4)
      // =========================================================================
      function renderCommunityAuditSections(t) {
        if (!window.GovernanceEngine || !t) return;
        const audit = window.GovernanceEngine.getTianguisAuditData(t);
        if (!audit) return;

        // 1. Ámbito A: Estatus en vivo hoy ("¿Se instaló hoy?")
        const liveBadge = document.getElementById('gov-live-epistemic-badge');
        const balanceBox = document.getElementById('gov-live-balance-text');
        const btnYes = document.getElementById('btn-gov-live-yes');
        const btnNo = document.getElementById('btn-gov-live-no');

        liveBadge.className = `badge-epistemic ${audit.statusLive.badgeClass}`;
        liveBadge.textContent = `${audit.statusLive.icon} ${audit.statusLive.statusLabel}`;

        const isSim = window.GovernanceEngine.isSimulateTerritory();
        const proxHint = isSim ? '📍 Validado en territorio (+3 pts activado)' : '🌐 Validación ciudadana (+1 pt sin GPS)';

        if (audit.statusLive.yesScore === 0 && audit.statusLive.noScore === 0) {
          balanceBox.innerHTML = `<div>Sin reportes vecinales hoy todavía. ¡Sé el primero en validar!</div><div style="font-size: 10px; color: var(--slate-500); margin-top: 2px;">${proxHint}</div>`;
        } else if (audit.statusLive.status === 'EN_DISPUTA') {
          balanceBox.innerHTML = `<div style="color: #92400e; font-weight: 700;">⚠️ Estatus en disputa comunitaria</div><div>Reportes contradictorios (+${audit.statusLive.yesScore} pts a favor vs +${audit.statusLive.noScore} pts en contra).</div>`;
        } else if (audit.statusLive.status === 'CONFIRMADO') {
          balanceBox.innerHTML = `<div style="color: #065f46; font-weight: 700;">✓ Instalación confirmada por vecinos y oferentes</div><div>Balance neto: <strong>+${audit.statusLive.netScore} pts</strong> ponderados (${audit.statusLive.yesScore} a favor).</div>`;
        } else {
          balanceBox.innerHTML = `<div>Reporte propuesto (Score: <strong>${audit.statusLive.netScore > 0 ? '+' : ''}${audit.statusLive.netScore} pts</strong>). Faltan validaciones para quórum oficial.</div>`;
        }

        if (audit.statusLive.hasVotedToday) {
          btnYes.disabled = true;
          btnNo.disabled = true;
          balanceBox.innerHTML += `<div style="font-size: 10px; color: var(--slate-500); margin-top: 3px; border-top: 1px solid var(--slate-200); padding-top: 3px;">✓ Ya registraste tu auditoría de hoy (Cooldown 24h activo).</div>`;
        } else {
          btnYes.disabled = false;
          btnNo.disabled = false;
        }

        btnYes.onclick = () => {
          window.GovernanceEngine.submitLiveStatusVote(t, 'yes').then(res => {
            showToast(res.message);
            renderCommunityAuditSections(t);
            renderMapMarkers();
          });
        };

        btnNo.onclick = () => {
          window.GovernanceEngine.submitLiveStatusVote(t, 'no').then(res => {
            showToast(res.message);
            renderCommunityAuditSections(t);
            renderMapMarkers();
          });
        };

        // 2. Ámbito B: Medios de Pago Reales
        const payList = document.getElementById('gov-payments-list');
        payList.innerHTML = '';
        Object.keys(audit.pagos).forEach(k => {
          const p = audit.pagos[k];
          const itemDiv = document.createElement('div');
          itemDiv.className = 'gov-payment-item';
          
          const userHasVoted = audit.userVotes && audit.userVotes[`pago_${p.id}`];

          itemDiv.innerHTML = `
            <div style="display: flex; align-items: center; gap: 6px;">
              <span>${p.icon}</span>
              <div>
                <strong style="color: var(--slate-800);">${p.label}</strong>
                <div style="font-size: 10px; color: var(--slate-500);">${p.score} pts acumulados</div>
              </div>
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
              <span class="badge-epistemic ${p.badgeClass}">${p.iconStatus} ${p.status === 'CONFIRMADO' ? 'Confirmado' : 'Propuesto'}</span>
              <button class="btn-gov-small" ${userHasVoted ? 'disabled' : ''} title="${userHasVoted ? 'Ya votaste recientemente' : 'Respaldar este medio de pago'}">
                ${userHasVoted ? '✓ Votado' : '+ Validar'}
              </button>
            </div>
          `;

          const valBtn = itemDiv.querySelector('button');
          if (!userHasVoted) {
            valBtn.addEventListener('click', () => {
              window.GovernanceEngine.submitPaymentVote(t, p.id).then(res => {
                showToast(res.message);
                renderCommunityAuditSections(t);
                renderMapMarkers();
              });
            });
          }

          payList.appendChild(itemDiv);
        });

        // 3. Ámbito C: Especialidades y Artículos del Tianguis ("¿Qué se vende aquí?")
        const tagsContainer = document.getElementById('side-product-tags');
        tagsContainer.innerHTML = '';

        audit.especialidades.forEach(sp => {
          const chip = document.createElement('span');
          const chipClass = (sp.status === 'CONFIRMADO')
            ? 'chip-confirmed'
            : (sp.status === 'EN_DISPUTA' ? 'chip-dispute' : 'chip-proposed');
          
          chip.className = `product-tag-chip ${chipClass}`;
          
          if (sp.status === 'CONFIRMADO') {
            chip.innerHTML = `✓ #${sp.nombre} <span style="font-size: 9.5px; opacity: 0.85;">(${sp.score} pts)</span>`;
          } else if (sp.status === 'EN_DISPUTA') {
            chip.innerHTML = `⚠️ #${sp.nombre} <span style="font-size: 9.5px;">(${sp.score} pts)</span>`;
          } else {
            chip.innerHTML = `? #${sp.nombre} <span style="font-size: 9.5px; color: #b45309;">(${sp.score} pt · ¿Confirmas?)</span>`;
          }

          chip.title = `Clic para respaldar #${sp.nombre} (+1 o +3 pts)`;
          chip.addEventListener('click', () => {
            window.GovernanceEngine.submitSpecialtyVote(t, sp.nombre).then(res => {
              showToast(res.message);
              renderCommunityAuditSections(t);
              renderMapMarkers();
            });
          });

          tagsContainer.appendChild(chip);
        });

        // Toggle formulario de propuesta
        const formBox = document.getElementById('gov-propose-form');
        const toggleBtn = document.getElementById('btn-toggle-propose');
        const submitBtn = document.getElementById('btn-submit-propose');
        const inputSpec = document.getElementById('input-new-specialty');

        toggleBtn.onclick = () => {
          formBox.style.display = (formBox.style.display === 'none' || !formBox.style.display) ? 'block' : 'none';
          if (formBox.style.display === 'block') inputSpec.focus();
        };

        submitBtn.onclick = () => {
          const val = inputSpec.value.trim();
          if (!val) {
            showToast('Escribe un producto o giro para proponer.');
            return;
          }
          window.GovernanceEngine.proposeNewSpecialty(t, val).then(res => {
            showToast(res.message);
            inputSpec.value = '';
            formBox.style.display = 'none';
            renderCommunityAuditSections(t);
            renderMapMarkers();
          });
        };

        // 4. Barra Cívica y Testing de Auditoría Abierta
        const btnSim = document.getElementById('btn-toggle-simulate');
        const updateSimBtn = () => {
          const isSimNow = window.GovernanceEngine.isSimulateTerritory();
          if (isSimNow) {
            btnSim.textContent = '📍 En territorio ≤300m (+3 pts)';
            btnSim.style.background = '#d1fae5';
            btnSim.style.color = '#065f46';
            btnSim.style.borderColor = '#10b981';
          } else {
            btnSim.textContent = '🌐 Remoto / Sin GPS (+1 pt)';
            btnSim.style.background = '#ffffff';
            btnSim.style.color = 'var(--slate-700)';
            btnSim.style.borderColor = 'var(--slate-300)';
          }
        };
        updateSimBtn();

        btnSim.onclick = () => {
          const next = !window.GovernanceEngine.isSimulateTerritory();
          window.GovernanceEngine.setSimulateTerritory(next);
          updateSimBtn();
          renderCommunityAuditSections(t);
          showToast(next
            ? '📍 Modo Territorio ACTIVADO (+3 pts por Proof of Location)'
            : '🌐 Modo Remoto (+1 pt validación ciudadana)');
        };

        document.getElementById('btn-reload-demo').onclick = () => {
          window.GovernanceEngine.initializeOrSeed(state.tianguis, true);
          renderCommunityAuditSections(t);
          renderMapMarkers();
          showToast('🎲 Datos demo de gobernanza comunitaria recargados.');
        };

        document.getElementById('btn-reset-votes').onclick = () => {
          window.GovernanceEngine.resetLocalData();
          renderCommunityAuditSections(t);
          renderMapMarkers();
          showToast('🔄 Votos y datos locales restablecidos.');
        };

        document.getElementById('btn-view-json').onclick = () => {
          const jsonStr = window.GovernanceEngine.exportAuditJSON();
          document.getElementById('json-modal-content').textContent = jsonStr;
          document.getElementById('json-modal-backdrop').style.display = 'flex';
        };
      }

      // Cerrar modal de JSON
      document.getElementById('btn-close-json-modal').addEventListener('click', () => {
        document.getElementById('json-modal-backdrop').style.display = 'none';
      });
      document.getElementById('json-modal-backdrop').addEventListener('click', (e) => {
        if (e.target.id === 'json-modal-backdrop') {
          document.getElementById('json-modal-backdrop').style.display = 'none';
        }
      });'''

    if 'function renderCommunityAuditSections' not in content:
        assert fn_target in content, "No se encontró el target para fn"
        content = content.replace(fn_target, fn_replacement, 1)

    with open(BUILD_SCRIPT, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✓ scripts/build_revamped_map.py actualizado exitosamente.")

if __name__ == '__main__':
    run()
