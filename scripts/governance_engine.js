/**
 * Módulo de Gobernanza Barrial y Auditoría Comunitaria Ponderada (Módulo 5.4)
 * Chilangatón 2026 - Reto 1: Comercio Popular y Barrial (SEDECO / SECTEI / SAF)
 *
 * Principios:
 * - Soberanía de datos y no extractivismo (Principios CARE).
 * - Arquitectura Local-First (localStorage con fallback en memoria) con UUID efímero anónimo.
 * - Factor de ponderación por proximidad física (Proof of Location):
 *     * Proximidad <= 300 metros: +3 puntos ("Validado en territorio").
 *     * Remoto o sin GPS: +1 punto ("Validación ciudadana").
 *     * Modo de simulación de territorio para evaluación y auditoría.
 * - Cooldown anti-spam de 24 horas por tianguis/acción.
 * - Ciclo de estados epistémicos:
 *     * CONFIRMADO: score >= 3 pts (estilo sólido con checkmark ✓).
 *     * PROPUESTO: score < 3 pts (estilo punteado o badge sutil ?).
 *     * EN_DISPUTA: votos contradictorios significativos (badge ámbar ⚠️).
 * - 3 Ámbitos de Auditoría Comunitaria:
 *     a) Estatus en vivo hoy ("¿Se instaló hoy?").
 *     b) Medios de pago reales (Efectivo, CoDi/Transferencia, Tarjeta/Terminal).
 *     c) Catálogo comunitario de especialidades ("¿Qué se vende aquí?") con propuesta abierta.
 * - Precarga de datos semilla (Seed Data) verosímil y diversa para exploración inmediata en el mapa.
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.GovernanceEngine = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var STORAGE_KEY = 'cdmx_barrial_governance_v1';
  var DEVICE_UUID_KEY = 'cdmx_barrial_device_uuid';
  var MEMORY_FALLBACK = {};
  var simulateTerritoryMode = false;
  var cachedUserLocation = null;

  // =========================================================================
  // 1. UTILIDADES Y IDENTIDAD ANÓNIMA (LOCAL-FIRST & CARE)
  // =========================================================================

  function isStorageAvailable() {
    try {
      var testKey = '__storage_test__';
      window.localStorage.setItem(testKey, testKey);
      window.localStorage.removeItem(testKey);
      return true;
    } catch (e) {
      return false;
    }
  }

  function getDeviceId() {
    if (!isStorageAvailable()) {
      if (!MEMORY_FALLBACK[DEVICE_UUID_KEY]) {
        MEMORY_FALLBACK[DEVICE_UUID_KEY] = 'anon_' + Math.random().toString(36).substring(2, 12);
      }
      return MEMORY_FALLBACK[DEVICE_UUID_KEY];
    }
    var id = window.localStorage.getItem(DEVICE_UUID_KEY);
    if (!id) {
      if (window.crypto && typeof window.crypto.randomUUID === 'function') {
        id = window.crypto.randomUUID();
      } else {
        id = 'anon_' + Date.now().toString(36) + '_' + Math.random().toString(36).substring(2, 10);
      }
      window.localStorage.setItem(DEVICE_UUID_KEY, id);
    }
    return id;
  }

  function loadStore() {
    if (!isStorageAvailable()) {
      return MEMORY_FALLBACK[STORAGE_KEY] || { tianguis: {} };
    }
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) return { tianguis: {} };
      return JSON.parse(raw);
    } catch (e) {
      console.warn('[GovernanceEngine] Error parseando localStorage, reiniciando tienda:', e);
      return { tianguis: {} };
    }
  }

  function saveStore(store) {
    if (!isStorageAvailable()) {
      MEMORY_FALLBACK[STORAGE_KEY] = store;
      return;
    }
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
    } catch (e) {
      console.error('[GovernanceEngine] Error guardando en localStorage:', e);
    }
  }

  function getTodayString() {
    var d = new Date();
    var year = d.getFullYear();
    var month = String(d.getMonth() + 1).padStart(2, '0');
    var day = String(d.getDate()).padStart(2, '0');
    return year + '-' + month + '-' + day;
  }

  // Haversine formula (metros)
  function calculateDistanceMeters(lat1, lon1, lat2, lon2) {
    if (lat1 == null || lon1 == null || lat2 == null || lon2 == null) return null;
    var R = 6371000;
    var dLat = (lat2 - lat1) * (Math.PI / 180);
    var dLon = (lon2 - lon1) * (Math.PI / 180);
    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * (Math.PI / 180)) * Math.cos(lat2 * (Math.PI / 180)) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return Math.round(R * c);
  }

  // =========================================================================
  // 2. GEOLOCALIZACIÓN Y PROOF OF LOCATION (PONDERACIÓN TERRITORIAL)
  // =========================================================================

  function setSimulateTerritory(enabled) {
    simulateTerritoryMode = !!enabled;
  }

  function isSimulateTerritory() {
    return simulateTerritoryMode;
  }

  function requestUserLocation(timeoutMs) {
    timeoutMs = timeoutMs || 5000;
    return new Promise(function (resolve) {
      if (simulateTerritoryMode) {
        resolve({
          lat: 19.4326,
          lng: -99.1332,
          simulated: true
        });
        return;
      }
      if (!navigator.geolocation) {
        resolve(null);
        return;
      }
      var resolved = false;
      var timer = setTimeout(function () {
        if (!resolved) {
          resolved = true;
          resolve(cachedUserLocation);
        }
      }, timeoutMs);

      navigator.geolocation.getCurrentPosition(
        function (pos) {
          if (!resolved) {
            resolved = true;
            clearTimeout(timer);
            cachedUserLocation = {
              lat: pos.coords.latitude,
              lng: pos.coords.longitude,
              accuracy: pos.coords.accuracy,
              timestamp: pos.timestamp,
              simulated: false
            };
            resolve(cachedUserLocation);
          }
        },
        function (err) {
          if (!resolved) {
            resolved = true;
            clearTimeout(timer);
            resolve(cachedUserLocation);
          }
        },
        { enableHighAccuracy: true, timeout: timeoutMs, maximumAge: 60000 }
      );
    });
  }

  function evaluateProximity(tianguisLat, tianguisLng, userLocationOpt) {
    if (simulateTerritoryMode) {
      return {
        weight: 3,
        isTerritory: true,
        distanceM: 65,
        badge: 'Validado en territorio (simulado)',
        label: 'Proof of Location (≤ 300m)'
      };
    }

    var loc = userLocationOpt || cachedUserLocation;
    if (!loc || loc.lat == null || loc.lng == null || tianguisLat == null || tianguisLng == null) {
      return {
        weight: 1,
        isTerritory: false,
        distanceM: null,
        badge: 'Validación ciudadana',
        label: 'Sin confirmación de proximidad'
      };
    }

    var dist = calculateDistanceMeters(loc.lat, loc.lng, tianguisLat, tianguisLng);
    if (dist !== null && dist <= 300) {
      return {
        weight: 3,
        isTerritory: true,
        distanceM: dist,
        badge: 'Validado en territorio',
        label: 'A ' + dist + ' m del tianguis (≤ 300m)'
      };
    } else {
      return {
        weight: 1,
        isTerritory: false,
        distanceM: dist,
        badge: 'Validación ciudadana',
        label: dist !== null ? 'A ' + (dist > 1000 ? (dist / 1000).toFixed(1) + ' km' : dist + ' m') : 'Ubicación remota'
      };
    }
  }

  // =========================================================================
  // 3. ESTADOS EPISTÉMICOS Y MODELO DE REPUTACIÓN
  // =========================================================================

  function computeEpistemicStatus(positiveScore, negativeScore) {
    positiveScore = positiveScore || 0;
    negativeScore = negativeScore || 0;
    var netScore = positiveScore - negativeScore;

    // Disputa si hay reportes significativos encontrados
    if (positiveScore >= 2 && negativeScore >= 2) {
      var minVal = Math.min(positiveScore, negativeScore);
      var maxVal = Math.max(positiveScore, negativeScore);
      if (maxVal > 0 && (minVal / maxVal) >= 0.35) {
        return {
          status: 'EN_DISPUTA',
          label: 'En Disputa',
          badgeClass: 'badge-epistemic-disputa',
          icon: '⚠️',
          score: netScore
        };
      }
    }

    if (netScore >= 3) {
      return {
        status: 'CONFIRMADO',
        label: 'Confirmado Comunitariamente',
        badgeClass: 'badge-epistemic-confirmado',
        icon: '✓',
        score: netScore
      };
    }

    return {
      status: 'PROPUESTO',
      label: 'Propuesto',
      badgeClass: 'badge-epistemic-propuesto',
      icon: '?',
      score: netScore
    };
  }

  // =========================================================================
  // 4. CONTROL DE COOLDOWN (ANTI-SPAM 24 HORAS)
  // =========================================================================

  var COOLDOWN_MS = 24 * 60 * 60 * 1000;

  function checkCooldown(tianguisId, actionKey) {
    var store = loadStore();
    var tRecord = (store.tianguis && store.tianguis[tianguisId]) || {};
    var userVotes = tRecord.userVotes || {};
    var lastVote = userVotes[actionKey];

    if (!lastVote || !lastVote.timestamp) {
      return { allowed: true, remainingMs: 0 };
    }

    var elapsed = Date.now() - lastVote.timestamp;
    if (elapsed < COOLDOWN_MS) {
      var remainingMs = COOLDOWN_MS - elapsed;
      var remainingHours = Math.ceil(remainingMs / (60 * 60 * 1000));
      return {
        allowed: false,
        remainingMs: remainingMs,
        remainingHours: remainingHours,
        lastVote: lastVote
      };
    }

    return { allowed: true, remainingMs: 0 };
  }

  function recordUserVote(tianguisId, actionKey, voteData) {
    var store = loadStore();
    if (!store.tianguis) store.tianguis = {};
    if (!store.tianguis[tianguisId]) store.tianguis[tianguisId] = {};
    if (!store.tianguis[tianguisId].userVotes) store.tianguis[tianguisId].userVotes = {};

    voteData.timestamp = Date.now();
    voteData.deviceId = getDeviceId();
    store.tianguis[tianguisId].userVotes[actionKey] = voteData;
    saveStore(store);
  }

  // =========================================================================
  // 5. DATOS SEMILLA (SEED DATA) VEROSÍMIL PARA EVALUACIÓN INMEDIATA
  // =========================================================================

  function generateSeedData(tianguisList) {
    var todayStr = getTodayString();
    var store = { tianguis: {} };

    // Casos emblemáticos con interacciones diversas:
    // 1. El Salado (TIANG-0662): CONFIRMADO masivo (+9 pts), CoDi/Transferencia CONFIRMADO (+6 pts), especialidades ricas
    store.tianguis['TIANG-0662'] = {
      statusLive: { date: todayStr, yes: 9, no: 0, reportsCount: 4 },
      pagos: {
        efectivo: { score: 18, votes: 6 },
        transferencia: { score: 7, votes: 3 },
        tarjeta: { score: 2, votes: 2 }
      },
      especialidades: [
        { nombre: 'Ropa de paca premium', score: 11, origen: 'comunidad', votes: 4 },
        { nombre: 'Herramientas de uso rudo', score: 8, origen: 'nlp', votes: 3 },
        { nombre: 'Barbacoa de borrego', score: 9, origen: 'nlp', votes: 3 },
        { nombre: 'Antigüedades y chácharas', score: 7, origen: 'comunidad', votes: 3 },
        { nombre: 'Refacciones para bicicleta', score: 2, origen: 'comunidad', votes: 1 } // Propuesto
      ]
    };

    // 2. Cultural del Chopo (TIANG-0774): CONFIRMADO (+8 pts), Transferencia muy alta, Música y Ropa gótica
    store.tianguis['TIANG-0774'] = {
      statusLive: { date: todayStr, yes: 8, no: 0, reportsCount: 3 },
      pagos: {
        efectivo: { score: 14, votes: 5 },
        transferencia: { score: 9, votes: 4 },
        tarjeta: { score: 5, votes: 2 }
      },
      especialidades: [
        { nombre: 'Discos de vinil y cassettes', score: 12, origen: 'comunidad', votes: 4 },
        { nombre: 'Ropa oscura y botas góticas', score: 8, origen: 'nlp', votes: 3 },
        { nombre: 'Playeras de bandas de rock', score: 9, origen: 'nlp', votes: 3 },
        { nombre: 'Parches y pines artesanales', score: 4, origen: 'comunidad', votes: 2 },
        { nombre: 'Libros y fanzines contracultura', score: 2, origen: 'comunidad', votes: 1 } // Propuesto
      ]
    };

    // 3. San Felipe de Jesús / La Bola (TIANG-0356): CONFIRMADO (+12 pts), Mayor tianguis de AL, pago mixto
    store.tianguis['TIANG-0356'] = {
      statusLive: { date: todayStr, yes: 12, no: 1, reportsCount: 5 },
      pagos: {
        efectivo: { score: 21, votes: 7 },
        transferencia: { score: 8, votes: 3 },
        tarjeta: { score: 3, votes: 2 }
      },
      especialidades: [
        { nombre: 'Herramientas eléctricas usadas', score: 10, origen: 'nlp', votes: 4 },
        { nombre: 'Tenis y calzado deportivo', score: 9, origen: 'nlp', votes: 3 },
        { nombre: 'Carnitas de Michoacán', score: 8, origen: 'nlp', votes: 3 },
        { nombre: 'Tepache frío de barril', score: 6, origen: 'comunidad', votes: 2 },
        { nombre: 'Laptops y cables de segunda mano', score: 2, origen: 'comunidad', votes: 1 } // Propuesto
      ]
    };

    // 4. Sullivan Sábado (TIANG-0276): CONFIRMADO (+6 pts), Arte y comida
    store.tianguis['TIANG-0276'] = {
      statusLive: { date: todayStr, yes: 6, no: 0, reportsCount: 2 },
      pagos: {
        efectivo: { score: 10, votes: 4 },
        transferencia: { score: 6, votes: 3 },
        tarjeta: { score: 4, votes: 2 }
      },
      especialidades: [
        { nombre: 'Pintura al óleo y acuarelas', score: 8, origen: 'nlp', votes: 3 },
        { nombre: 'Mariscos frescos estilo Sinaloa', score: 7, origen: 'nlp', votes: 3 },
        { nombre: 'Esculturas y marcos de madera', score: 5, origen: 'comunidad', votes: 2 },
        { nombre: 'Café de especialidad orgánico', score: 2, origen: 'comunidad', votes: 1 } // Propuesto
      ]
    };

    // 5. Sullivan Miércoles (TIANG-0258): EN_DISPUTA (3 a favor vs 3 en contra por obras/lluvia)
    store.tianguis['TIANG-0258'] = {
      statusLive: { date: todayStr, yes: 3, no: 3, reportsCount: 3 },
      pagos: {
        efectivo: { score: 7, votes: 3 },
        transferencia: { score: 2, votes: 1 },
        tarjeta: { score: 0, votes: 0 }
      },
      especialidades: [
        { nombre: 'Frutas y verduras de temporada', score: 5, origen: 'nlp', votes: 2 },
        { nombre: 'Quesadillas y gorditas', score: 4, origen: 'nlp', votes: 2 },
        { nombre: 'Flores cortadas frescas', score: 1, origen: 'comunidad', votes: 1 } // Propuesto
      ]
    };

    // 6. Tianguis Cuernavaca / Condesa (TIANG-0243): CONFIRMADO (+7 pts), alta transferencia y tarjeta
    store.tianguis['TIANG-0243'] = {
      statusLive: { date: todayStr, yes: 7, no: 0, reportsCount: 3 },
      pagos: {
        efectivo: { score: 11, votes: 4 },
        transferencia: { score: 9, votes: 4 }, // Confirmado
        tarjeta: { score: 7, votes: 3 }       // Confirmado
      },
      especialidades: [
        { nombre: 'Quesos y lácteos artesanales', score: 9, origen: 'nlp', votes: 3 },
        { nombre: 'Fruta deshidratada y nueces', score: 8, origen: 'nlp', votes: 3 },
        { nombre: 'Comida vegana y sin gluten', score: 6, origen: 'comunidad', votes: 2 },
        { nombre: 'Plantas y macetas de barro', score: 2, origen: 'comunidad', votes: 1 }
      ]
    };

    // 7. Tianguis Apatlaco (TIANG-0543): CONFIRMADO (+5 pts)
    store.tianguis['TIANG-0543'] = {
      statusLive: { date: todayStr, yes: 5, no: 0, reportsCount: 2 },
      pagos: {
        efectivo: { score: 12, votes: 4 },
        transferencia: { score: 3, votes: 2 },
        tarjeta: { score: 1, votes: 1 }
      },
      especialidades: [
        { nombre: 'Pescado y mariscos al mayoreo', score: 9, origen: 'nlp', votes: 3 },
        { nombre: 'Ropa deportiva nacional', score: 6, origen: 'nlp', votes: 2 },
        { nombre: 'Ceviche y cócteles preparados', score: 5, origen: 'nlp', votes: 2 }
      ]
    };

    // 8. Tianguis Santa Cruz Meyehualco (TIANG-0705): EN_DISPUTA (4 a favor vs 3 en contra por operativo vial)
    store.tianguis['TIANG-0705'] = {
      statusLive: { date: todayStr, yes: 4, no: 3, reportsCount: 3 },
      pagos: {
        efectivo: { score: 14, votes: 5 },
        transferencia: { score: 4, votes: 2 },
        tarjeta: { score: 1, votes: 1 }
      },
      especialidades: [
        { nombre: 'Ropa de segunda mano y saldos', score: 10, origen: 'nlp', votes: 4 },
        { nombre: 'Herramientas y refacciones mecánicas', score: 8, origen: 'nlp', votes: 3 },
        { nombre: 'Tacos de carnitas y tripa', score: 7, origen: 'nlp', votes: 3 }
      ]
    };

    // 9. Tianguis Portales (TIANG-0167): CONFIRMADO (+6 pts)
    store.tianguis['TIANG-0167'] = {
      statusLive: { date: todayStr, yes: 6, no: 0, reportsCount: 2 },
      pagos: {
        efectivo: { score: 13, votes: 5 },
        transferencia: { score: 5, votes: 2 },
        tarjeta: { score: 2, votes: 1 }
      },
      especialidades: [
        { nombre: 'Muebles y antigüedades de madera', score: 8, origen: 'nlp', votes: 3 },
        { nombre: 'Libros y revistas antiguas', score: 7, origen: 'nlp', votes: 3 },
        { nombre: 'Cerrajería y ferretería vintage', score: 5, origen: 'comunidad', votes: 2 }
      ]
    };

    // Generar muestras procedurales en ~40 tianguis adicionales si hay lista
    if (tianguisList && tianguisList.length) {
      for (var i = 0; i < tianguisList.length; i += 28) {
        var t = tianguisList[i];
        if (!t || !t.id || store.tianguis[t.id]) continue;

        var seedMod = i % 7;
        if (seedMod === 0) {
          // Confirmado con alta actividad
          store.tianguis[t.id] = {
            statusLive: { date: todayStr, yes: 6, no: 0, reportsCount: 2 },
            pagos: {
              efectivo: { score: 9, votes: 3 },
              transferencia: { score: 4, votes: 2 },
              tarjeta: { score: 1, votes: 1 }
            },
            especialidades: [
              { nombre: 'Verduras frescas de Xochimilco', score: 6, origen: 'comunidad', votes: 2 },
              { nombre: 'Pan de pueblo con nata', score: 2, origen: 'comunidad', votes: 1 } // Propuesto
            ]
          };
        } else if (seedMod === 2) {
          // En Disputa
          store.tianguis[t.id] = {
            statusLive: { date: todayStr, yes: 3, no: 3, reportsCount: 2 },
            pagos: {
              efectivo: { score: 7, votes: 2 },
              transferencia: { score: 1, votes: 1 },
              tarjeta: { score: 0, votes: 0 }
            },
            especialidades: [
              { nombre: 'Ropa y calzado económico', score: 4, origen: 'comunidad', votes: 2 }
            ]
          };
        } else if (seedMod === 4) {
          // Propuesto incipiente
          store.tianguis[t.id] = {
            statusLive: { date: todayStr, yes: 1, no: 0, reportsCount: 1 },
            pagos: {
              efectivo: { score: 6, votes: 2 },
              transferencia: { score: 2, votes: 1 }, // Propuesto
              tarjeta: { score: 1, votes: 1 }
            },
            especialidades: [
              { nombre: 'Artesanías y barro vidriado', score: 1, origen: 'comunidad', votes: 1 } // Propuesto
            ]
          };
        }
      }
    }

    return store;
  }

  function initializeOrSeed(tianguisList, forceReset) {
    var store = loadStore();
    var hasData = store && store.tianguis && Object.keys(store.tianguis).length > 0;

    if (!hasData || forceReset) {
      console.log('[GovernanceEngine] Inicializando datos demo de gobernanza comunitaria...');
      var seeded = generateSeedData(tianguisList || []);
      saveStore(seeded);
      return seeded;
    }
    return store;
  }

  // =========================================================================
  // 6. MÓDULOS DE AUDITORÍA COMUNITARIA
  // =========================================================================

  function getTianguisAuditData(tianguis) {
    if (!tianguis || !tianguis.id) return null;
    var tid = tianguis.id;
    var store = loadStore();
    var tRecord = (store.tianguis && store.tianguis[tid]) || {};
    var todayStr = getTodayString();

    // 1. Estatus en vivo hoy
    var liveRecord = tRecord.statusLive || {};
    var liveDate = liveRecord.date || todayStr;
    var liveYes = (liveDate === todayStr) ? (liveRecord.yes || 0) : 0;
    var liveNo = (liveDate === todayStr) ? (liveRecord.no || 0) : 0;
    var liveEpistemic = computeEpistemicStatus(liveYes, liveNo);

    // 2. Medios de pago
    var pagosRecord = tRecord.pagos || {};
    var pagos = {
      efectivo: {
        id: 'efectivo',
        label: 'Solo efectivo',
        icon: '💵',
        score: (pagosRecord.efectivo && pagosRecord.efectivo.score != null) ? pagosRecord.efectivo.score : 6,
        votes: (pagosRecord.efectivo && pagosRecord.efectivo.votes != null) ? pagosRecord.efectivo.votes : 2,
        desc: 'Medio de pago soberano universal en tianguis'
      },
      transferencia: {
        id: 'transferencia',
        label: 'Transferencia / CoDi',
        icon: '📱',
        score: (pagosRecord.transferencia && pagosRecord.transferencia.score != null) ? pagosRecord.transferencia.score : 1,
        votes: (pagosRecord.transferencia && pagosRecord.transferencia.votes != null) ? pagosRecord.transferencia.votes : 1,
        desc: 'Transferencias SPEI o cobro móvil sin comisiones'
      },
      tarjeta: {
        id: 'tarjeta',
        label: 'Tarjeta / Terminal bancaria',
        icon: '💳',
        score: (pagosRecord.tarjeta && pagosRecord.tarjeta.score != null) ? pagosRecord.tarjeta.score : 0,
        votes: (pagosRecord.tarjeta && pagosRecord.tarjeta.votes != null) ? pagosRecord.tarjeta.votes : 0,
        desc: 'Cobro con tarjeta de débito o crédito'
      }
    };

    Object.keys(pagos).forEach(function (k) {
      var p = pagos[k];
      var ep = computeEpistemicStatus(p.score, 0);
      p.status = ep.status;
      p.statusLabel = ep.label;
      p.badgeClass = ep.badgeClass;
      p.iconStatus = ep.icon;
    });

    // 3. Especialidades / Artículos comunitarios
    var baseArticles = tianguis.top_articulos_mencionados || tianguis.tags || [];
    var specsRecord = tRecord.especialidades || [];
    var specsMap = {};

    baseArticles.forEach(function (art) {
      var clean = String(art).replace(/^#/, '').trim();
      if (!clean) return;
      var key = clean.toLowerCase();
      specsMap[key] = {
        nombre: clean,
        score: 3,
        origen: 'nlp',
        votes: 1
      };
    });

    specsRecord.forEach(function (sp) {
      if (!sp || !sp.nombre) return;
      var key = sp.nombre.toLowerCase();
      if (specsMap[key]) {
        specsMap[key].score = Math.max(specsMap[key].score, sp.score);
        specsMap[key].votes = (specsMap[key].votes || 1) + (sp.votes || 0);
        if (sp.origen) specsMap[key].origen = sp.origen;
      } else {
        specsMap[key] = {
          nombre: sp.nombre,
          score: sp.score || 1,
          origen: sp.origen || 'comunidad',
          votes: sp.votes || 1
        };
      }
    });

    var finalSpecs = Object.keys(specsMap).map(function (k) {
      var item = specsMap[k];
      var ep = computeEpistemicStatus(item.score, 0);
      item.status = ep.status;
      item.statusLabel = ep.label;
      item.badgeClass = ep.badgeClass;
      item.iconStatus = ep.icon;
      return item;
    });

    finalSpecs.sort(function (a, b) {
      if (a.status === 'CONFIRMADO' && b.status !== 'CONFIRMADO') return -1;
      if (a.status !== 'CONFIRMADO' && b.status === 'CONFIRMADO') return 1;
      return b.score - a.score;
    });

    var userVotes = tRecord.userVotes || {};

    return {
      tianguisId: tid,
      statusLive: {
        date: liveDate,
        yesScore: liveYes,
        noScore: liveNo,
        netScore: liveYes - liveNo,
        status: liveEpistemic.status,
        statusLabel: liveEpistemic.label,
        badgeClass: liveEpistemic.badgeClass,
        icon: liveEpistemic.icon,
        hasVotedToday: !!(userVotes['statusLive_' + todayStr])
      },
      pagos: pagos,
      especialidades: finalSpecs,
      userVotes: userVotes
    };
  }

  function getMarkerCommunityStatus(tianguisId) {
    if (!tianguisId) return null;
    var store = loadStore();
    var tRecord = (store.tianguis && store.tianguis[tianguisId]);
    if (!tRecord) return null;

    var todayStr = getTodayString();
    var live = tRecord.statusLive;
    if (live && live.date === todayStr) {
      var ep = computeEpistemicStatus(live.yes, live.no);
      if (ep.status === 'EN_DISPUTA') {
        return {
          badgeType: 'dispute',
          icon: '⚠️',
          text: 'Comunidad: En Disputa',
          color: '#d97706'
        };
      }
      if (ep.status === 'CONFIRMADO' && live.yes >= 3) {
        return {
          badgeType: 'confirmed',
          icon: '✓',
          text: 'Comunidad: Verificado hoy (+' + live.yes + ' pts)',
          color: '#059669'
        };
      }
    }

    // Si tiene pagos o especialidades activas por comunidad
    var specs = tRecord.especialidades || [];
    var commSpecs = specs.filter(function (s) { return s.origen === 'comunidad'; });
    if (commSpecs.length > 0) {
      return {
        badgeType: 'active',
        icon: '👥',
        text: 'Auditoría barrial activa (' + commSpecs.length + ' propuestas)',
        color: '#0284c7'
      };
    }

    return null;
  }

  function submitLiveStatusVote(tianguis, vote, locationOverride) {
    if (!tianguis || !tianguis.id) return Promise.reject(new Error('Tianguis inválido'));
    var tid = tianguis.id;
    var todayStr = getTodayString();
    var actionKey = 'statusLive_' + todayStr;

    var cd = checkCooldown(tid, actionKey);
    if (!cd.allowed) {
      return Promise.resolve({
        success: false,
        cooldown: true,
        remainingHours: cd.remainingHours,
        message: 'Ya registraste tu auditoría de estatus hoy para este tianguis. Cooldown de 24h activo para prevenir spam.'
      });
    }

    return requestUserLocation().then(function (loc) {
      var prox = evaluateProximity(tianguis.lat, tianguis.lng, locationOverride || loc);
      var store = loadStore();
      if (!store.tianguis) store.tianguis = {};
      if (!store.tianguis[tid]) store.tianguis[tid] = {};

      var current = store.tianguis[tid].statusLive || { date: todayStr, yes: 0, no: 0 };
      if (current.date !== todayStr) {
        current = { date: todayStr, yes: 0, no: 0 };
      }

      if (vote === 'yes') {
        current.yes = (current.yes || 0) + prox.weight;
      } else {
        current.no = (current.no || 0) + prox.weight;
      }
      current.date = todayStr;
      store.tianguis[tid].statusLive = current;
      saveStore(store);

      recordUserVote(tid, actionKey, {
        vote: vote,
        weight: prox.weight,
        isTerritory: prox.isTerritory,
        distanceM: prox.distanceM
      });

      var audit = getTianguisAuditData(tianguis);
      return {
        success: true,
        cooldown: false,
        weight: prox.weight,
        isTerritory: prox.isTerritory,
        distanceM: prox.distanceM,
        proximityLabel: prox.badge,
        message: '¡Reporte registrado! +' + prox.weight + ' pt' + (prox.weight > 1 ? 's' : '') + ' (' + prox.badge + ')',
        audit: audit
      };
    });
  }

  function submitPaymentVote(tianguis, methodId, locationOverride) {
    if (!tianguis || !tianguis.id || !methodId) return Promise.reject(new Error('Parámetros inválidos'));
    var tid = tianguis.id;
    var actionKey = 'pago_' + methodId;

    var cd = checkCooldown(tid, actionKey);
    if (!cd.allowed) {
      return Promise.resolve({
        success: false,
        cooldown: true,
        remainingHours: cd.remainingHours,
        message: 'Ya confirmaste este medio de pago recientemente. Cooldown de 24h activo.'
      });
    }

    return requestUserLocation().then(function (loc) {
      var prox = evaluateProximity(tianguis.lat, tianguis.lng, locationOverride || loc);
      var store = loadStore();
      if (!store.tianguis) store.tianguis = {};
      if (!store.tianguis[tid]) store.tianguis[tid] = {};
      if (!store.tianguis[tid].pagos) store.tianguis[tid].pagos = {};

      var current = store.tianguis[tid].pagos[methodId] || { score: (methodId === 'efectivo' ? 6 : (methodId === 'transferencia' ? 1 : 0)), votes: 1 };
      current.score = (current.score || 0) + prox.weight;
      current.votes = (current.votes || 0) + 1;
      store.tianguis[tid].pagos[methodId] = current;
      saveStore(store);

      recordUserVote(tid, actionKey, {
        methodId: methodId,
        weight: prox.weight,
        isTerritory: prox.isTerritory,
        distanceM: prox.distanceM
      });

      var audit = getTianguisAuditData(tianguis);
      return {
        success: true,
        cooldown: false,
        weight: prox.weight,
        isTerritory: prox.isTerritory,
        distanceM: prox.distanceM,
        proximityLabel: prox.badge,
        message: '¡Medio de pago confirmado! +' + prox.weight + ' pt' + (prox.weight > 1 ? 's' : '') + ' (' + prox.badge + ')',
        audit: audit
      };
    });
  }

  function submitSpecialtyVote(tianguis, specName, locationOverride) {
    if (!tianguis || !tianguis.id || !specName) return Promise.reject(new Error('Parámetros inválidos'));
    var tid = tianguis.id;
    var cleanName = String(specName).replace(/^#/, '').trim();
    var actionKey = 'spec_' + cleanName.toLowerCase();

    var cd = checkCooldown(tid, actionKey);
    if (!cd.allowed) {
      return Promise.resolve({
        success: false,
        cooldown: true,
        remainingHours: cd.remainingHours,
        message: 'Ya confirmaste #' + cleanName + ' hoy. Cooldown de 24h activo.'
      });
    }

    return requestUserLocation().then(function (loc) {
      var prox = evaluateProximity(tianguis.lat, tianguis.lng, locationOverride || loc);
      var store = loadStore();
      if (!store.tianguis) store.tianguis = {};
      if (!store.tianguis[tid]) store.tianguis[tid] = {};
      if (!store.tianguis[tid].especialidades) store.tianguis[tid].especialidades = [];

      var list = store.tianguis[tid].especialidades;
      var found = null;
      for (var i = 0; i < list.length; i++) {
        if (list[i].nombre.toLowerCase() === cleanName.toLowerCase()) {
          found = list[i];
          break;
        }
      }

      if (found) {
        found.score = (found.score || 1) + prox.weight;
        found.votes = (found.votes || 1) + 1;
      } else {
        var isFromBase = false;
        var baseArticles = tianguis.top_articulos_mencionados || tianguis.tags || [];
        for (var b = 0; b < baseArticles.length; b++) {
          if (String(baseArticles[b]).replace(/^#/, '').trim().toLowerCase() === cleanName.toLowerCase()) {
            isFromBase = true;
            break;
          }
        }
        var baseScore = isFromBase ? 3 : 0;
        list.push({
          nombre: cleanName,
          score: baseScore + prox.weight,
          origen: isFromBase ? 'nlp' : 'comunidad',
          votes: 2
        });
      }

      saveStore(store);

      recordUserVote(tid, actionKey, {
        specName: cleanName,
        weight: prox.weight,
        isTerritory: prox.isTerritory,
        distanceM: prox.distanceM
      });

      var audit = getTianguisAuditData(tianguis);
      return {
        success: true,
        cooldown: false,
        weight: prox.weight,
        isTerritory: prox.isTerritory,
        distanceM: prox.distanceM,
        proximityLabel: prox.badge,
        message: '¡Especialidad #' + cleanName + ' respaldada! +' + prox.weight + ' pt' + (prox.weight > 1 ? 's' : '') + ' (' + prox.badge + ')',
        audit: audit
      };
    });
  }

  function proposeNewSpecialty(tianguis, rawName, locationOverride) {
    if (!tianguis || !tianguis.id || !rawName) return Promise.reject(new Error('Nombre requerido'));
    var cleanName = String(rawName).replace(/^#/, '').trim();
    if (cleanName.length < 3) {
      return Promise.resolve({
        success: false,
        message: 'Por favor escribe un giro o artículo válido (mínimo 3 letras).'
      });
    }

    cleanName = cleanName.charAt(0).toUpperCase() + cleanName.slice(1);
    var tid = tianguis.id;
    var actionKey = 'spec_' + cleanName.toLowerCase();

    var currentAudit = getTianguisAuditData(tianguis);
    var existing = currentAudit.especialidades.find(function (s) {
      return s.nombre.toLowerCase() === cleanName.toLowerCase();
    });

    if (existing) {
      return submitSpecialtyVote(tianguis, cleanName, locationOverride);
    }

    return requestUserLocation().then(function (loc) {
      var prox = evaluateProximity(tianguis.lat, tianguis.lng, locationOverride || loc);
      var store = loadStore();
      if (!store.tianguis) store.tianguis = {};
      if (!store.tianguis[tid]) store.tianguis[tid] = {};
      if (!store.tianguis[tid].especialidades) store.tianguis[tid].especialidades = [];

      store.tianguis[tid].especialidades.push({
        nombre: cleanName,
        score: prox.weight,
        origen: 'comunidad',
        votes: 1
      });

      saveStore(store);

      recordUserVote(tid, actionKey, {
        specName: cleanName,
        weight: prox.weight,
        isTerritory: prox.isTerritory,
        distanceM: prox.distanceM,
        isProposal: true
      });

      var audit = getTianguisAuditData(tianguis);
      var ep = computeEpistemicStatus(prox.weight, 0);

      return {
        success: true,
        cooldown: false,
        isNew: true,
        itemStatus: ep.status,
        weight: prox.weight,
        isTerritory: prox.isTerritory,
        distanceM: prox.distanceM,
        proximityLabel: prox.badge,
        message: '¡Propuesta agregada! #' + cleanName + ' entra como [' + ep.label + '] con +' + prox.weight + ' pt' + (prox.weight > 1 ? 's' : ''),
        audit: audit
      };
    });
  }

  // =========================================================================
  // 7. HERRAMIENTAS DE TESTING Y AUDITORÍA ABIERTA
  // =========================================================================

  function resetLocalData() {
    if (isStorageAvailable()) {
      window.localStorage.removeItem(STORAGE_KEY);
    }
    MEMORY_FALLBACK = {};
    return { success: true, message: 'Datos locales de auditoría comunitaria restablecidos.' };
  }

  function clearCooldowns(tianguisId) {
    var store = loadStore();
    if (tianguisId) {
      if (store.tianguis && store.tianguis[tianguisId]) {
        store.tianguis[tianguisId].userVotes = {};
      }
    } else {
      if (store.tianguis) {
        Object.keys(store.tianguis).forEach(function (tid) {
          store.tianguis[tid].userVotes = {};
        });
      }
    }
    saveStore(store);
    return { success: true, message: 'Cooldowns de votación reiniciados.' };
  }

  function exportAuditJSON() {
    var store = loadStore();
    return JSON.stringify(store, null, 2);
  }

  // =========================================================================
  // API PÚBLICA
  // =========================================================================

  return {
    getDeviceId: getDeviceId,
    requestUserLocation: requestUserLocation,
    evaluateProximity: evaluateProximity,
    setSimulateTerritory: setSimulateTerritory,
    isSimulateTerritory: isSimulateTerritory,
    computeEpistemicStatus: computeEpistemicStatus,
    checkCooldown: checkCooldown,
    initializeOrSeed: initializeOrSeed,
    getTianguisAuditData: getTianguisAuditData,
    getMarkerCommunityStatus: getMarkerCommunityStatus,
    submitLiveStatusVote: submitLiveStatusVote,
    submitPaymentVote: submitPaymentVote,
    submitSpecialtyVote: submitSpecialtyVote,
    proposeNewSpecialty: proposeNewSpecialty,
    resetLocalData: resetLocalData,
    clearCooldowns: clearCooldowns,
    exportAuditJSON: exportAuditJSON
  };
}));
