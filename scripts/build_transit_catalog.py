#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Catálogo de Tarifas, Horarios Dinámicos y Reglas Metropolitanas de Transporte
==========================================================================================
Proyecto: Comercio Popular, Barrial y Movilidad Integrada en la CDMX (Chilangatón 2026)
Ubicación de Salida:
  - data/catalog/tarifas_horarios_transporte.json
  - data/catalog/tarifas_horarios_transporte.csv

Estructura 15 subsistemas de transporte masivo y secundario de CDMX y Zona Metropolitana
(Edomex y Federal), especificando horarios de lunes a domingo, esquemas de cobro por distancia,
recargos nocturnos, medios de pago, gratuidades y reglas de transbordo.
"""

import os
import json
import csv
from typing import List, Dict, Any

SISTEMAS_TRANSPORTE: List[Dict[str, Any]] = [
    {
        "sistema_id": "METRO",
        "nombre": "Sistema de Transporte Colectivo Metro (STC)",
        "jurisdiccion": "CDMX",
        "red_tipo": "PRIMARIA_MI",
        "horarios": {
            "lunes_viernes": {"apertura": 5.0, "cierre": 24.0, "apertura_str": "05:00", "cierre_str": "24:00"},
            "sabado": {"apertura": 6.0, "cierre": 24.0, "apertura_str": "06:00", "cierre_str": "24:00"},
            "domingo_festivo": {"apertura": 7.0, "cierre": 24.0, "apertura_str": "07:00", "cierre_str": "24:00"}
        },
        "tarifa_base_diurna": 5.00,
        "esquema_cobro": "TARIFA_UNICA",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": None,
                "costo": 5.00,
                "descripcion": "Tarifa plana única en toda la red de 12 líneas sin límite de distancia ni transbordo"
            }
        ],
        "aplica_recargo_nocturno": False,
        "horario_nocturno_inicio": None,
        "horario_nocturno_fin": None,
        "tarifa_nocturna_fija": None,
        "recargo_porcentaje": 0.0,
        "medio_pago": "Tarjeta MI",
        "beneficios_gratuidad": "Adultos mayores (+60 años con credencial INAPAM/Bienestar), personas con discapacidad y menores de 5 años acompañados.",
        "reglas_transbordo": "Transbordos gratuitos e ilimitados entre las 12 líneas de la red sin salir de torniquetes."
    },
    {
        "sistema_id": "METROBUS",
        "nombre": "Sistema Metrobús CDMX (BRT)",
        "jurisdiccion": "CDMX",
        "red_tipo": "PRIMARIA_MI",
        "horarios": {
            "lunes_viernes": {"apertura": 4.5, "cierre": 24.0, "apertura_str": "04:30", "cierre_str": "24:00"},
            "sabado": {"apertura": 4.5, "cierre": 24.0, "apertura_str": "04:30", "cierre_str": "24:00"},
            "domingo_festivo": {"apertura": 5.0, "cierre": 24.0, "apertura_str": "05:00", "cierre_str": "24:00"}
        },
        "tarifa_base_diurna": 6.00,
        "esquema_cobro": "TARIFA_UNICA",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": None,
                "costo": 6.00,
                "descripcion": "Tarifa plana red general ($30.00 especial Línea 4 servicio Aeropuerto AICM T1/T2)"
            }
        ],
        "aplica_recargo_nocturno": False,
        "horario_nocturno_inicio": None,
        "horario_nocturno_fin": None,
        "tarifa_nocturna_fija": None,
        "recargo_porcentaje": 0.0,
        "medio_pago": "Tarjeta MI",
        "beneficios_gratuidad": "Adultos mayores (+60 años), personas con discapacidad y niños menores de 5 años.",
        "reglas_transbordo": "Transbordo gratuito entre diferentes líneas de Metrobús durante una ventana de 2 horas (120 min) desde el primer acceso con la misma tarjeta en la misma dirección de viaje."
    },
    {
        "sistema_id": "CABLEBUS",
        "nombre": "Cablebús CDMX (Teleférico Urbano)",
        "jurisdiccion": "CDMX",
        "red_tipo": "PRIMARIA_MI",
        "horarios": {
            "lunes_viernes": {"apertura": 5.0, "cierre": 23.0, "apertura_str": "05:00", "cierre_str": "23:00"},
            "sabado": {"apertura": 6.0, "cierre": 23.0, "apertura_str": "06:00", "cierre_str": "23:00"},
            "domingo_festivo": {"apertura": 7.0, "cierre": 23.0, "apertura_str": "07:00", "cierre_str": "23:00"}
        },
        "tarifa_base_diurna": 7.00,
        "esquema_cobro": "TARIFA_UNICA",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": None,
                "costo": 7.00,
                "descripcion": "Tarifa plana por viaje en Líneas 1, 2 y 3"
            }
        ],
        "aplica_recargo_nocturno": False,
        "horario_nocturno_inicio": None,
        "horario_nocturno_fin": None,
        "tarifa_nocturna_fija": None,
        "recargo_porcentaje": 0.0,
        "medio_pago": "Tarjeta MI",
        "beneficios_gratuidad": "Personas mayores de 60 años, personas con discapacidad evidente o credencial, y niños menores de 5 años.",
        "reglas_transbordo": "Transbordo gratuito entre ramales de la misma línea (ej. L1 Cuautepec - Tlalpexco). Conexión externa a Metro o RTP requiere pago individual."
    },
    {
        "sistema_id": "TROLEBUS",
        "nombre": "Servicio de Transportes Eléctricos - Trolebús (STE)",
        "jurisdiccion": "CDMX",
        "red_tipo": "PRIMARIA_MI",
        "horarios": {
            "lunes_viernes": {"apertura": 5.0, "cierre": 24.0, "apertura_str": "05:00", "cierre_str": "24:00"},
            "sabado": {"apertura": 5.0, "cierre": 24.0, "apertura_str": "05:00", "cierre_str": "24:00"},
            "domingo_festivo": {"apertura": 5.5, "cierre": 23.5, "apertura_str": "05:30", "cierre_str": "23:30"}
        },
        "tarifa_base_diurna": 4.00,
        "esquema_cobro": "TARIFA_UNICA",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": None,
                "costo": 4.00,
                "descripcion": "Tarifa ordinaria líneas superficiales 1 a 9"
            },
            {
                "min_km": 0.0,
                "max_km": None,
                "costo": 7.00,
                "descripcion": "Línea 10 Elevada (Constitución de 1917 - Santa Martha)"
            }
        ],
        "aplica_recargo_nocturno": True,
        "horario_nocturno_inicio": 0.0,
        "horario_nocturno_fin": 5.0,
        "tarifa_nocturna_fija": 7.00,
        "recargo_porcentaje": 0.0,
        "medio_pago": "Tarjeta MI",
        "beneficios_gratuidad": "Adultos mayores (+60 años), personas con discapacidad y menores de 5 años.",
        "reglas_transbordo": "Sin transbordo gratuito general entre líneas de trolebús. Servicio nocturno Nochebús en Línea 1 Eje Central opera de 00:00 a 05:00 con tarifa fija de $7.00 MXN."
    },
    {
        "sistema_id": "TREN_LIGERO",
        "nombre": "Servicio de Transportes Eléctricos - Tren Ligero",
        "jurisdiccion": "CDMX",
        "red_tipo": "PRIMARIA_MI",
        "horarios": {
            "lunes_viernes": {"apertura": 5.0, "cierre": 23.5, "apertura_str": "05:00", "cierre_str": "23:30"},
            "sabado": {"apertura": 5.5, "cierre": 23.5, "apertura_str": "05:30", "cierre_str": "23:30"},
            "domingo_festivo": {"apertura": 6.5, "cierre": 23.5, "apertura_str": "06:30", "cierre_str": "23:30"}
        },
        "tarifa_base_diurna": 3.00,
        "esquema_cobro": "TARIFA_UNICA",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": None,
                "costo": 3.00,
                "descripcion": "Tarifa plana única en todo el trayecto Taxqueña - Xochimilco"
            }
        ],
        "aplica_recargo_nocturno": False,
        "horario_nocturno_inicio": None,
        "horario_nocturno_fin": None,
        "tarifa_nocturna_fija": None,
        "recargo_porcentaje": 0.0,
        "medio_pago": "Tarjeta MI",
        "beneficios_gratuidad": "Adultos mayores (+60 años), personas con discapacidad y menores de 5 años.",
        "reglas_transbordo": "Conexión en CETRAM Taxqueña a Metro Línea 2 requiere pago por separado con Tarjeta MI ($5.00 MXN)."
    },
    {
        "sistema_id": "RTP_ORDINARIO",
        "nombre": "Red de Transporte de Pasajeros - Servicio Ordinario y Atenea",
        "jurisdiccion": "CDMX",
        "red_tipo": "PRIMARIA_MI",
        "horarios": {
            "lunes_viernes": {"apertura": 5.0, "cierre": 23.0, "apertura_str": "05:00", "cierre_str": "23:00"},
            "sabado": {"apertura": 5.0, "cierre": 23.0, "apertura_str": "05:00", "cierre_str": "23:00"},
            "domingo_festivo": {"apertura": 6.0, "cierre": 23.0, "apertura_str": "06:00", "cierre_str": "23:00"}
        },
        "tarifa_base_diurna": 2.00,
        "esquema_cobro": "TARIFA_UNICA",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": None,
                "costo": 2.00,
                "descripcion": "Tarifa plana social ordinaria"
            }
        ],
        "aplica_recargo_nocturno": False,
        "horario_nocturno_inicio": None,
        "horario_nocturno_fin": None,
        "tarifa_nocturna_fija": None,
        "recargo_porcentaje": 0.0,
        "medio_pago": "Tarjeta MI / Efectivo exacto operador",
        "beneficios_gratuidad": "Adultos mayores (+60 años), personas con discapacidad y menores de 5 años. Servicio Atenea exclusivo para mujeres, niñas y niños.",
        "reglas_transbordo": "Transbordo gratuito en servicios de apoyo temporal por modernización de Metro Línea 1 y Línea 9 con Tarjeta MI."
    },
    {
        "sistema_id": "RTP_EXPRESO",
        "nombre": "Red de Transporte de Pasajeros - Servicio Expreso",
        "jurisdiccion": "CDMX",
        "red_tipo": "PRIMARIA_MI",
        "horarios": {
            "lunes_viernes": {"apertura": 5.0, "cierre": 23.0, "apertura_str": "05:00", "cierre_str": "23:00"},
            "sabado": {"apertura": 5.0, "cierre": 23.0, "apertura_str": "05:00", "cierre_str": "23:00"},
            "domingo_festivo": {"apertura": 6.0, "cierre": 23.0, "apertura_str": "06:00", "cierre_str": "23:00"}
        },
        "tarifa_base_diurna": 4.00,
        "esquema_cobro": "TARIFA_UNICA",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": None,
                "costo": 4.00,
                "descripcion": "Tarifa plana servicio expreso con paradas limitadas"
            }
        ],
        "aplica_recargo_nocturno": False,
        "horario_nocturno_inicio": None,
        "horario_nocturno_fin": None,
        "tarifa_nocturna_fija": None,
        "recargo_porcentaje": 0.0,
        "medio_pago": "Tarjeta MI / Efectivo exacto operador",
        "beneficios_gratuidad": "Adultos mayores (+60 años), personas con discapacidad y menores de 5 años.",
        "reglas_transbordo": "Tarifa unitaria por abordaje."
    },
    {
        "sistema_id": "RTP_ECOBUS",
        "nombre": "Red de Transporte de Pasajeros - Servicio Ecobús Bajas Emisiones",
        "jurisdiccion": "CDMX",
        "red_tipo": "PRIMARIA_MI",
        "horarios": {
            "lunes_viernes": {"apertura": 5.0, "cierre": 23.0, "apertura_str": "05:00", "cierre_str": "23:00"},
            "sabado": {"apertura": 5.0, "cierre": 23.0, "apertura_str": "05:00", "cierre_str": "23:00"},
            "domingo_festivo": {"apertura": 6.0, "cierre": 23.0, "apertura_str": "06:00", "cierre_str": "23:00"}
        },
        "tarifa_base_diurna": 5.00,
        "esquema_cobro": "TARIFA_UNICA",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": None,
                "costo": 5.00,
                "descripcion": "Tarifa plana corredores Ecobús (Santa Fe - Balderas / M.A. Quevedo)"
            }
        ],
        "aplica_recargo_nocturno": False,
        "horario_nocturno_inicio": None,
        "horario_nocturno_fin": None,
        "tarifa_nocturna_fija": None,
        "recargo_porcentaje": 0.0,
        "medio_pago": "Tarjeta MI / Efectivo exacto operador",
        "beneficios_gratuidad": "Adultos mayores (+60 años), personas con discapacidad y menores de 5 años.",
        "reglas_transbordo": "Tarifa unitaria por abordaje."
    },
    {
        "sistema_id": "RTP_NOCHEBUS",
        "nombre": "Red de Transporte de Pasajeros - Circuito Especial Nochebús",
        "jurisdiccion": "CDMX",
        "red_tipo": "PRIMARIA_MI",
        "horarios": {
            "lunes_viernes": {"apertura": 0.0, "cierre": 5.0, "apertura_str": "00:00", "cierre_str": "05:00"},
            "sabado": {"apertura": 0.0, "cierre": 5.0, "apertura_str": "00:00", "cierre_str": "05:00"},
            "domingo_festivo": {"apertura": 0.0, "cierre": 5.0, "apertura_str": "00:00", "cierre_str": "05:00"}
        },
        "tarifa_base_diurna": 7.00,
        "esquema_cobro": "TARIFA_UNICA",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": None,
                "costo": 7.00,
                "descripcion": "Tarifa plana nocturna de 00:00 a 05:00 horas los 365 días del año"
            }
        ],
        "aplica_recargo_nocturno": True,
        "horario_nocturno_inicio": 0.0,
        "horario_nocturno_fin": 5.0,
        "tarifa_nocturna_fija": 7.00,
        "recargo_porcentaje": 0.0,
        "medio_pago": "Tarjeta MI / Efectivo exacto operador",
        "beneficios_gratuidad": "Adultos mayores (+60 años), personas con discapacidad y menores de 5 años.",
        "reglas_transbordo": "Sin transbordo gratuito."
    },
    {
        "sistema_id": "CONCESIONADO_CDMX_MICROBUS",
        "nombre": "Transporte Concesionado CDMX - Microbús y Vagoneta",
        "jurisdiccion": "CDMX",
        "red_tipo": "SECUNDARIA_CONCESIONADA",
        "horarios": {
            "lunes_viernes": {"apertura": 5.0, "cierre": 23.0, "apertura_str": "05:00", "cierre_str": "23:00"},
            "sabado": {"apertura": 5.5, "cierre": 23.0, "apertura_str": "05:30", "cierre_str": "23:00"},
            "domingo_festivo": {"apertura": 6.0, "cierre": 22.5, "apertura_str": "06:00", "cierre_str": "22:30"}
        },
        "tarifa_base_diurna": 6.00,
        "esquema_cobro": "POR_DISTANCIA_KM",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": 5.0,
                "costo": 6.00,
                "descripcion": "Primeros 5 kilómetros de recorrido"
            },
            {
                "min_km": 5.01,
                "max_km": 12.0,
                "costo": 6.50,
                "descripcion": "De 5 a 12 kilómetros de recorrido"
            },
            {
                "min_km": 12.01,
                "max_km": 999.0,
                "costo": 7.50,
                "descripcion": "Más de 12 kilómetros de recorrido"
            }
        ],
        "aplica_recargo_nocturno": True,
        "horario_nocturno_inicio": 23.0,
        "horario_nocturno_fin": 6.0,
        "tarifa_nocturna_fija": None,
        "recargo_porcentaje": 20.0,
        "medio_pago": "Efectivo exacto operador",
        "beneficios_gratuidad": "Sin gratuidad para adultos mayores; menores de 3 a 5 años en regazo sin ocupar asiento.",
        "reglas_transbordo": "Sin transbordo gratuito. Se paga tarifa completa por cada unidad abordada."
    },
    {
        "sistema_id": "CONCESIONADO_CDMX_CORREDOR",
        "nombre": "Transporte Concesionado CDMX - Corredor Zonal y Metropolitano",
        "jurisdiccion": "CDMX",
        "red_tipo": "SECUNDARIA_CONCESIONADA",
        "horarios": {
            "lunes_viernes": {"apertura": 5.0, "cierre": 23.5, "apertura_str": "05:00", "cierre_str": "23:30"},
            "sabado": {"apertura": 5.5, "cierre": 23.0, "apertura_str": "05:30", "cierre_str": "23:00"},
            "domingo_festivo": {"apertura": 6.0, "cierre": 22.5, "apertura_str": "06:00", "cierre_str": "22:30"}
        },
        "tarifa_base_diurna": 8.00,
        "esquema_cobro": "POR_DISTANCIA_KM",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": 12.0,
                "costo": 8.00,
                "descripcion": "Servicio ordinario corredor zonal hasta 12 km"
            },
            {
                "min_km": 12.01,
                "max_km": 999.0,
                "costo": 8.50,
                "descripcion": "Servicio ejecutivo o recorrido largo mayor a 12 km"
            }
        ],
        "aplica_recargo_nocturno": True,
        "horario_nocturno_inicio": 23.0,
        "horario_nocturno_fin": 6.0,
        "tarifa_nocturna_fija": None,
        "recargo_porcentaje": 20.0,
        "medio_pago": "Tarjeta MI / Efectivo exacto operador",
        "beneficios_gratuidad": "Sujeto a normas de corredor; generalmente sin gratuidad obligatoria para personas mayores.",
        "reglas_transbordo": "Sin transbordo gratuito intercorredor."
    },
    {
        "sistema_id": "CONCESIONADO_EDOMEX_COMBI",
        "nombre": "Transporte Concesionado Edomex - Combi y Microbús Metropolitano",
        "jurisdiccion": "EDOMEX",
        "red_tipo": "METROPOLITANA_EDOMEX",
        "horarios": {
            "lunes_viernes": {"apertura": 4.5, "cierre": 23.0, "apertura_str": "04:30", "cierre_str": "23:00"},
            "sabado": {"apertura": 4.5, "cierre": 23.0, "apertura_str": "04:30", "cierre_str": "23:00"},
            "domingo_festivo": {"apertura": 5.5, "cierre": 22.5, "apertura_str": "05:30", "cierre_str": "22:30"}
        },
        "tarifa_base_diurna": 14.00,
        "esquema_cobro": "POR_DISTANCIA_KM",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": 5.0,
                "costo": 14.00,
                "descripcion": "Tarifa mínima oficial primeros 5 km (Gaceta Oficial Edomex)"
            },
            {
                "min_km": 5.01,
                "max_km": 999.0,
                "costo_base": 14.00,
                "costo_adicional_por_km": 0.25,
                "descripcion": "+$0.25 MXN por cada kilómetro adicional después del km 5"
            }
        ],
        "aplica_recargo_nocturno": True,
        "horario_nocturno_inicio": 23.0,
        "horario_nocturno_fin": 5.0,
        "tarifa_nocturna_fija": None,
        "recargo_porcentaje": 20.0,
        "medio_pago": "Efectivo exacto operador",
        "beneficios_gratuidad": "Ninguno. En Edomex no existe gratuidad por ley para adultos mayores ni personas con discapacidad en concesionado.",
        "reglas_transbordo": "Sin transbordo. Si cruza frontera hacia CETRAMs de CDMX (Indios Verdes, Pantitlán, Cuatro Caminos, Taxqueña) se cobra tarifa Edomex completa ($14.00+ MXN)."
    },
    {
        "sistema_id": "MEXIBUS",
        "nombre": "Sistema de Transporte Masivo Mexibús (BRT Edomex)",
        "jurisdiccion": "EDOMEX",
        "red_tipo": "METROPOLITANA_EDOMEX",
        "horarios": {
            "lunes_viernes": {"apertura": 4.5, "cierre": 24.0, "apertura_str": "04:30", "cierre_str": "24:00"},
            "sabado": {"apertura": 4.5, "cierre": 24.0, "apertura_str": "04:30", "cierre_str": "24:00"},
            "domingo_festivo": {"apertura": 5.0, "cierre": 23.5, "apertura_str": "05:00", "cierre_str": "23:30"}
        },
        "tarifa_base_diurna": 9.00,
        "esquema_cobro": "TARIFA_UNICA",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": None,
                "costo": 9.00,
                "descripcion": "Tarifa plana por viaje en Líneas 1, 2, 3 y 4"
            }
        ],
        "aplica_recargo_nocturno": False,
        "horario_nocturno_inicio": None,
        "horario_nocturno_fin": None,
        "tarifa_nocturna_fija": None,
        "recargo_porcentaje": 0.0,
        "medio_pago": "Tarjeta Mexipase",
        "beneficios_gratuidad": "Adultos mayores (+60 INAPAM), personas con discapacidad y menores de 5 años.",
        "reglas_transbordo": "Transbordo gratuito entre líneas troncales Mexibús en nodos autorizados; no transborda gratis a Metrobús ni Metro CDMX."
    },
    {
        "sistema_id": "MEXICABLE",
        "nombre": "Sistema de Teleférico Mexicable Edomex",
        "jurisdiccion": "EDOMEX",
        "red_tipo": "METROPOLITANA_EDOMEX",
        "horarios": {
            "lunes_viernes": {"apertura": 4.5, "cierre": 23.0, "apertura_str": "04:30", "cierre_str": "23:00"},
            "sabado": {"apertura": 5.5, "cierre": 22.0, "apertura_str": "05:30", "cierre_str": "22:00"},
            "domingo_festivo": {"apertura": 7.0, "cierre": 21.0, "apertura_str": "07:00", "cierre_str": "21:00"}
        },
        "tarifa_base_diurna": 9.00,
        "esquema_cobro": "TARIFA_UNICA",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": None,
                "costo": 9.00,
                "descripcion": "Tarifa plana por viaje en Línea 1 (La Cañada) y Línea 2 (Indios Verdes)"
            }
        ],
        "aplica_recargo_nocturno": False,
        "horario_nocturno_inicio": None,
        "horario_nocturno_fin": None,
        "tarifa_nocturna_fija": None,
        "recargo_porcentaje": 0.0,
        "medio_pago": "Tarjeta Mexipase",
        "beneficios_gratuidad": "Adultos mayores (+60 INAPAM), personas con discapacidad y menores de 5 años.",
        "reglas_transbordo": "Transbordo entre estaciones de la misma línea. Transferencia a CETRAM Indios Verdes hacia Metro o Cablebús CDMX requiere validación y pago separado con Tarjeta MI."
    },
    {
        "sistema_id": "TREN_SUBURBANO",
        "nombre": "Ferrocarril Suburbano de la ZMVM (Buenavista - Cuautitlán)",
        "jurisdiccion": "FEDERAL",
        "red_tipo": "METROPOLITANA_EDOMEX",
        "horarios": {
            "lunes_viernes": {"apertura": 5.0, "cierre": 24.5, "apertura_str": "05:00", "cierre_str": "00:30"},
            "sabado": {"apertura": 6.0, "cierre": 24.5, "apertura_str": "06:00", "cierre_str": "00:30"},
            "domingo_festivo": {"apertura": 7.0, "cierre": 24.5, "apertura_str": "07:00", "cierre_str": "00:30"}
        },
        "tarifa_base_diurna": 10.50,
        "esquema_cobro": "POR_ZONA_ESTACIONES",
        "tramos_distancia": [
            {
                "min_km": 0.0,
                "max_km": 12.89,
                "costo": 10.50,
                "descripcion": "Viaje corto: de 0 a 12.89 km (1 a 3 estaciones)"
            },
            {
                "min_km": 12.90,
                "max_km": 25.59,
                "costo": 24.50,
                "descripcion": "Viaje largo: de 12.90 a 25.59 km (4 o más estaciones)"
            }
        ],
        "aplica_recargo_nocturno": False,
        "horario_nocturno_inicio": None,
        "horario_nocturno_fin": None,
        "tarifa_nocturna_fija": None,
        "recargo_porcentaje": 0.0,
        "medio_pago": "Tarjeta Suburbano",
        "beneficios_gratuidad": "Menores de 5 años acompañados. Adultos mayores pagan pasaje completo (tarifa federal concesionada sin subsidio local).",
        "reglas_transbordo": "Conexión a Metro L8B/B en Buenavista o Metrobús L1/L3/L4 requiere cobro independiente con Tarjeta MI."
    }
]

def build_catalog_files():
    """Genera los archivos JSON y CSV del catálogo."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    catalog_dir = os.path.join(base_dir, "data", "catalog")
    os.makedirs(catalog_dir, exist_ok=True)

    json_path = os.path.join(catalog_dir, "tarifas_horarios_transporte.json")
    csv_path = os.path.join(catalog_dir, "tarifas_horarios_transporte.csv")

    metadata = {
        "titulo": "Catálogo Integral de Tarifas, Horarios Dinámicos y Reglas Metropolitanas de Transporte CDMX - Edomex",
        "version": "1.0.0",
        "fecha_actualizacion": "2026-10-25",
        "proyecto": "Comercio Popular, Barrial y Movilidad Integrada en la CDMX (Chilangatón 2026)",
        "jurisdicciones": ["CDMX", "EDOMEX", "FEDERAL"],
        "tipos_red": ["PRIMARIA_MI", "SECUNDARIA_CONCESIONADA", "METROPOLITANA_EDOMEX"],
        "total_sistemas": len(SISTEMAS_TRANSPORTE)
    }

    full_payload = {
        "metadata": metadata,
        "sistemas": SISTEMAS_TRANSPORTE
    }

    # 1. Guardar JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_payload, f, ensure_ascii=False, indent=2)
    print(f"✅ Catálogo JSON exportado exitosamente en: {json_path}")

    # 2. Guardar CSV
    csv_headers = [
        "sistema_id",
        "nombre",
        "jurisdiccion",
        "red_tipo",
        "lv_apertura",
        "lv_cierre",
        "sab_apertura",
        "sab_cierre",
        "dom_apertura",
        "dom_cierre",
        "tarifa_base_diurna",
        "esquema_cobro",
        "tramos_resumen",
        "aplica_recargo_nocturno",
        "nocturno_inicio",
        "nocturno_fin",
        "tarifa_nocturna_fija",
        "recargo_porcentaje",
        "medio_pago",
        "beneficios_gratuidad",
        "reglas_transbordo"
    ]

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()

        for s in SISTEMAS_TRANSPORTE:
            # Resumen de tramos
            tramos = s.get("tramos_distancia", [])
            tramos_str_list = []
            for t in tramos:
                if "costo_adicional_por_km" in t:
                    tramos_str_list.append(f"> {t.get('min_km')} km: ${t.get('costo_base', s['tarifa_base_diurna']):.2f} + ${t['costo_adicional_por_km']:.2f}/km")
                elif t.get("max_km") is None:
                    tramos_str_list.append(f"Red completa: ${t['costo']:.2f}")
                else:
                    tramos_str_list.append(f"{t['min_km']}-{t['max_km']} km: ${t['costo']:.2f}")
            tramos_resumen = " | ".join(tramos_str_list)

            writer.writerow({
                "sistema_id": s["sistema_id"],
                "nombre": s["nombre"],
                "jurisdiccion": s["jurisdiccion"],
                "red_tipo": s["red_tipo"],
                "lv_apertura": s["horarios"]["lunes_viernes"]["apertura"],
                "lv_cierre": s["horarios"]["lunes_viernes"]["cierre"],
                "sab_apertura": s["horarios"]["sabado"]["apertura"],
                "sab_cierre": s["horarios"]["sabado"]["cierre"],
                "dom_apertura": s["horarios"]["domingo_festivo"]["apertura"],
                "dom_cierre": s["horarios"]["domingo_festivo"]["cierre"],
                "tarifa_base_diurna": s["tarifa_base_diurna"],
                "esquema_cobro": s["esquema_cobro"],
                "tramos_resumen": tramos_resumen,
                "aplica_recargo_nocturno": "SI" if s["aplica_recargo_nocturno"] else "NO",
                "nocturno_inicio": s["horario_nocturno_inicio"] if s["horario_nocturno_inicio"] is not None else "",
                "nocturno_fin": s["horario_nocturno_fin"] if s["horario_nocturno_fin"] is not None else "",
                "tarifa_nocturna_fija": s["tarifa_nocturna_fija"] if s["tarifa_nocturna_fija"] is not None else "",
                "recargo_porcentaje": s["recargo_porcentaje"],
                "medio_pago": s["medio_pago"],
                "beneficios_gratuidad": s["beneficios_gratuidad"],
                "reglas_transbordo": s["reglas_transbordo"]
            })
    print(f"✅ Catálogo CSV exportado exitosamente en: {csv_path}")

if __name__ == "__main__":
    build_catalog_files()
