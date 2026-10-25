import os
import re

with open('mapa_comercio_movilidad_cdmx.html.bak', 'r', encoding='utf-8') as f:
    orig = f.read()

# Extract the font-face definition from the beginning of <style>
# The @font-face is from index 714 up to where the normal css rules start.
style_content_start = orig.find('<style>') + len('<style>')
style_content_end = orig.find('</style>')
existing_css = orig[style_content_start:style_content_end]

# Additional CSS to append before </style>
extra_css = """
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
"""

full_style = existing_css + extra_css

print("Full style generated, length:", len(full_style))
