#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Tarifas y Horarios Dinámicos de Transporte (Schedule & Pricing Engine)
==============================================================================
Proyecto: Comercio Popular, Barrial y Movilidad Integrada en la CDMX (Chilangatón 2026)
Ubicación: scripts/schedule_pricing_engine.py

Capacidades:
1. Catálogo en memoria y lectura desde `data/catalog/tarifas_horarios_transporte.json`.
2. `consultar_transporte_por_hora(dia, hora_decimal)`:
   - Identifica sistemas de transporte abiertos vs. cerrados según día de la semana y hora.
   - Discrimina tarifas diurnas vs. recargos nocturnos en tiempo real.
3. `calcular_costo_tramo(sistema_id, distancia_km, hora_decimal, origen_edomex, dia)`:
   - Desglose tramo por tramo: tarifa base, escalonamiento por distancia, recargo nocturno y regla metropolitana (CDMX vs Edomex).
4. CLI interactivo y suite de pruebas (`--test`).
"""

import os
import sys
import json
import argparse
import unicodedata
from typing import Dict, List, Any, Optional, Tuple

# Constantes de Días
DIAS_MAP = {
    'lunes': 'lunes_viernes',
    'martes': 'lunes_viernes',
    'miercoles': 'lunes_viernes',
    'jueves': 'lunes_viernes',
    'viernes': 'lunes_viernes',
    'sabado': 'sabado',
    'domingo': 'domingo_festivo',
    'festivo': 'domingo_festivo',
    'lv': 'lunes_viernes',
    'sab': 'sabado',
    'dom': 'domingo_festivo'
}

def normalizar_dia(dia_str: str) -> str:
    """Normaliza el nombre del día a una de las 3 claves: lunes_viernes, sabado, domingo_festivo."""
    if not dia_str:
        return 'lunes_viernes'
    texto = dia_str.strip().lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return DIAS_MAP.get(texto, 'lunes_viernes')

def decimal_a_hora_str(hora_dec: float) -> str:
    """Convierte una hora decimal (ej. 2.5) a formato HH:MM (ej. 02:30)."""
    horas = int(hora_dec)
    minutos = int(round((hora_dec - horas) * 60))
    if minutos == 60:
        horas += 1
        minutos = 0
    return f"{horas:02d}:{minutos:02d}"

class TransitPricingEngine:
    """Motor de cálculo de tarifas y verificación de horarios de transporte en la CDMX y ZMVM."""

    def __init__(self, catalog_path: Optional[str] = None):
        if catalog_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            catalog_path = os.path.join(base_dir, "data", "catalog", "tarifas_horarios_transporte.json")

        self.catalog_path = catalog_path
        self.sistemas: Dict[str, Dict[str, Any]] = {}
        self.metadata: Dict[str, Any] = {}
        self._load_catalog()

    def _load_catalog(self):
        """Carga el catálogo desde JSON o genera la versión base si no existe."""
        if os.path.exists(self.catalog_path):
            with open(self.catalog_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.metadata = data.get("metadata", {})
                for s in data.get("sistemas", []):
                    self.sistemas[s["sistema_id"]] = s
        else:
            # Fallback dinámico importando desde el builder
            try:
                from scripts.build_transit_catalog import SISTEMAS_TRANSPORTE
                for s in SISTEMAS_TRANSPORTE:
                    self.sistemas[s["sistema_id"]] = s
            except ImportError:
                raise FileNotFoundError(f"No se encontró el catálogo en {self.catalog_path} ni el módulo constructor.")

    def esta_en_horario_nocturno(self, sistema: Dict[str, Any], hora_decimal: float) -> bool:
        """Verifica si a una hora determinada aplica tarifa/recargo nocturno para ese sistema."""
        if not sistema.get("aplica_recargo_nocturno", False):
            return False

        inicio = sistema.get("horario_nocturno_inicio")
        fin = sistema.get("horario_nocturno_fin")

        if inicio is None or fin is None:
            return False

        hora_normalizada = hora_decimal % 24.0

        if inicio > fin:
            # Cruza la medianoche (ej. 23:00 a 06:00)
            return hora_normalizada >= inicio or hora_normalizada < fin
        else:
            # Mismo día (ej. 00:00 a 05:00)
            return inicio <= hora_normalizada < fin

    def esta_en_servicio(self, sistema: Dict[str, Any], dia_clave: str, hora_decimal: float) -> Tuple[bool, str]:
        """
        Determina si el sistema está en servicio para el día y hora indicados.
        Retorna (en_servicio, detalle_horario).
        """
        horario_dia = sistema["horarios"].get(dia_clave)
        if not horario_dia:
            return False, "Sin servicio programado para este día"

        apertura = horario_dia["apertura"]
        cierre = horario_dia["cierre"]
        apertura_str = horario_dia.get("apertura_str", decimal_a_hora_str(apertura))
        cierre_str = horario_dia.get("cierre_str", decimal_a_hora_str(cierre))

        hora_norm = hora_decimal % 24.0

        # Caso especial 1: Sistemas exclusivamente nocturnos como RTP_NOCHEBUS (00:00 a 05:00)
        if sistema.get("sistema_id") == "RTP_NOCHEBUS":
            if 0.0 <= hora_norm < 5.0 or hora_norm >= 23.95:
                return True, f"En servicio nocturno Nochebús ({apertura_str} - {cierre_str})"
            else:
                return False, f"Servicio cerrado (opera únicamente de noche {apertura_str} a {cierre_str})"

        # Caso especial 2: Cierre después de medianoche (ej. Suburbano cierra a las 00:30 = 24.5)
        if cierre > 24.0:
            if hora_norm >= apertura or hora_norm < (cierre - 24.0):
                return True, f"En servicio ordinario ({apertura_str} - {cierre_str})"
            else:
                return False, f"Servicio cerrado (abre a las {apertura_str})"

        # Caso habitual: apertura < cierre
        if apertura <= hora_norm < cierre:
            return True, f"En servicio ({apertura_str} - {cierre_str})"
        else:
            return False, f"Servicio cerrado (horario de {apertura_str} a {cierre_str})"

    def consultar_transporte_por_hora(self, dia: str, hora_decimal: float) -> Dict[str, Any]:
        """
        Consulta integral de disponibilidad y costos de todos los transportes a una hora y día específicos.
        """
        dia_clave = normalizar_dia(dia)
        hora_norm = hora_decimal % 24.0
        hora_str = decimal_a_hora_str(hora_norm)

        abiertos: List[Dict[str, Any]] = []
        cerrados: List[Dict[str, Any]] = []

        es_madrugada = 0.0 <= hora_norm < 6.0
        es_noche = hora_norm >= 22.0 or es_madrugada

        for sistema_id, sistema in self.sistemas.items():
            en_servicio, desc_horario = self.esta_en_servicio(sistema, dia_clave, hora_norm)
            es_nocturno = self.esta_en_horario_nocturno(sistema, hora_norm)

            # Tarifa vigente a esta hora
            tarifa_vigente = sistema["tarifa_base_diurna"]
            recargo_monto = 0.0

            if es_nocturno:
                if sistema.get("tarifa_nocturna_fija") is not None:
                    tarifa_vigente = float(sistema["tarifa_nocturna_fija"])
                elif sistema.get("recargo_porcentaje", 0) > 0:
                    pct = sistema["recargo_porcentaje"]
                    recargo_monto = round(tarifa_vigente * (pct / 100.0), 2)
                    tarifa_vigente = round(tarifa_vigente + recargo_monto, 2)

            info_sistema = {
                "sistema_id": sistema_id,
                "nombre": sistema["nombre"],
                "jurisdiccion": sistema["jurisdiccion"],
                "red_tipo": sistema["red_tipo"],
                "tarifa_vigente_base": tarifa_vigente,
                "es_nocturno": es_nocturno,
                "recargo_nocturno_monto": recargo_monto,
                "esquema_cobro": sistema["esquema_cobro"],
                "medio_pago": sistema["medio_pago"],
                "estatus_servicio": "ABIERTO" if en_servicio else "CERRADO",
                "detalle_horario": desc_horario,
                "reglas_transbordo": sistema["reglas_transbordo"],
                "beneficios_gratuidad": sistema["beneficios_gratuidad"]
            }

            if en_servicio:
                abiertos.append(info_sistema)
            else:
                cerrados.append(info_sistema)

        # Estadísticas y síntesis
        tarifas_cdmx = [s["tarifa_vigente_base"] for s in abiertos if s["jurisdiccion"] == "CDMX"]
        tarifas_edomex = [s["tarifa_vigente_base"] for s in abiertos if s["jurisdiccion"] == "EDOMEX"]

        promedio_cdmx = round(sum(tarifas_cdmx) / len(tarifas_cdmx), 2) if tarifas_cdmx else 0.0
        promedio_edomex = round(sum(tarifas_edomex) / len(tarifas_edomex), 2) if tarifas_edomex else 0.0

        return {
            "consulta": {
                "dia_ingresado": dia,
                "dia_clave": dia_clave,
                "hora_decimal": hora_norm,
                "hora_formato": hora_str,
                "fase_dia": "MADRUGADA" if es_madrugada else ("NOCHE" if es_noche else "DIURNO")
            },
            "resumen_estadistico": {
                "total_sistemas": len(self.sistemas),
                "total_abiertos": len(abiertos),
                "total_cerrados": len(cerrados),
                "sistemas_abiertos_ids": [s["sistema_id"] for s in abiertos],
                "tarifa_promedio_abiertos_cdmx": promedio_cdmx,
                "tarifa_promedio_abiertos_edomex": promedio_edomex,
                "diferencial_metropolitano_pct": round(((promedio_edomex - promedio_cdmx) / promedio_cdmx * 100), 1) if promedio_cdmx > 0 else 0.0
            },
            "sistemas_abiertos": abiertos,
            "sistemas_cerrados": cerrados
        }

    def calcular_costo_tramo(
        self,
        sistema_id: str,
        distancia_km: float,
        hora_decimal: float = 12.0,
        origen_edomex: bool = False,
        dia: str = 'LUNES'
    ) -> Dict[str, Any]:
        """
        Calcula el precio exacto de un tramo considerando kilometraje, horario y jurisdicción CDMX vs Edomex.
        """
        sistema_id_norm = sistema_id.strip().upper()
        if sistema_id_norm not in self.sistemas:
            # Búsqueda difusa de coincidencia parcial
            coincidencias = [k for k in self.sistemas if sistema_id_norm in k]
            if coincidencias:
                sistema_id_norm = coincidencias[0]
            else:
                raise ValueError(f"Sistema '{sistema_id}' no reconocido. Opciones válidas: {list(self.sistemas.keys())}")

        sistema = self.sistemas[sistema_id_norm]
        dia_clave = normalizar_dia(dia)
        hora_norm = hora_decimal % 24.0
        en_servicio, desc_horario = self.esta_en_servicio(sistema, dia_clave, hora_norm)
        es_nocturno = self.esta_en_horario_nocturno(sistema, hora_norm)

        distancia = max(0.1, float(distancia_km))
        esquema = sistema["esquema_cobro"]
        jurisdiccion_operativa = sistema["jurisdiccion"]
        desglose_calculo = ""

        costo_base = sistema["tarifa_base_diurna"]

        # 1. Regla Metropolitana: Si el viaje parte de Edomex en transporte concesionado (micro/combi)
        # o si es la combi mexiquense hacia CDMX, aplica la tarifa oficial mexiquense ($14.00 base primeros 5 km)
        if origen_edomex and sistema_id_norm in ["CONCESIONADO_CDMX_MICROBUS", "CONCESIONADO_CDMX_CORREDOR"]:
            jurisdiccion_operativa = "EDOMEX_METROPOLITANO"
            # Regla de reciprocidad metropolitana Edomex
            if distancia <= 5.0:
                costo_base = 14.00
                desglose_calculo = "Tarifa metropolitana Edomex hacia CDMX: $14.00 base (hasta 5 km)"
            else:
                km_extra = distancia - 5.0
                adicional = km_extra * 0.25
                costo_base = round(14.00 + adicional, 2)
                desglose_calculo = f"Tarifa metropolitana Edomex: $14.00 base + {km_extra:.1f} km extra x $0.25 = ${costo_base:.2f}"

        elif esquema == "TARIFA_UNICA":
            # Caso especial Trolebús Elevado si se indica en notas o servicio nocturno
            if sistema_id_norm == "RTP_NOCHEBUS":
                costo_base = 7.00
                desglose_calculo = "Tarifa plana nocturna Nochebús ($7.00 MXN)"
            else:
                costo_base = sistema["tarifa_base_diurna"]
                desglose_calculo = f"Tarifa plana institucional de red (${costo_base:.2f} MXN sin límite de distancia)"

        elif esquema == "POR_DISTANCIA_KM":
            if sistema_id_norm == "CONCESIONADO_CDMX_MICROBUS":
                if distancia <= 5.0:
                    costo_base = 6.00
                    desglose_calculo = f"Tramo corto hasta 5 km: $6.00 MXN ({distancia:.1f} km)"
                elif distancia <= 12.0:
                    costo_base = 6.50
                    desglose_calculo = f"Tramo medio 5 a 12 km: $6.50 MXN ({distancia:.1f} km)"
                else:
                    costo_base = 7.50
                    desglose_calculo = f"Tramo largo >12 km: $7.50 MXN ({distancia:.1f} km)"

            elif sistema_id_norm == "CONCESIONADO_CDMX_CORREDOR":
                if distancia <= 12.0:
                    costo_base = 8.00
                    desglose_calculo = f"Corredor zonal servicio regular hasta 12 km: $8.00 MXN ({distancia:.1f} km)"
                else:
                    costo_base = 8.50
                    desglose_calculo = f"Corredor zonal trayecto largo >12 km: $8.50 MXN ({distancia:.1f} km)"

            elif sistema_id_norm == "CONCESIONADO_EDOMEX_COMBI":
                if distancia <= 5.0:
                    costo_base = 14.00
                    desglose_calculo = f"Tarifa base mínima Edomex primeros 5 km: $14.00 MXN ({distancia:.1f} km)"
                else:
                    km_extra = distancia - 5.0
                    adicional = km_extra * 0.25
                    costo_base = round(14.00 + adicional, 2)
                    desglose_calculo = f"Base Edomex $14.00 (5 km) + {km_extra:.1f} km extra x $0.25 = ${costo_base:.2f} MXN"

        elif esquema == "POR_ZONA_ESTACIONES":
            # Tren Suburbano
            if distancia <= 12.89:
                costo_base = 10.50
                desglose_calculo = f"Viaje corto Tren Suburbano (1 a 3 estaciones / <= 12.89 km): $10.50 MXN ({distancia:.1f} km)"
            else:
                costo_base = 24.50
                desglose_calculo = f"Viaje largo Tren Suburbano (4 o más estaciones / > 12.89 km): $24.50 MXN ({distancia:.1f} km)"

        # 2. Aplicar recargo nocturno si corresponde
        recargo_monto = 0.0
        costo_final = costo_base

        if es_nocturno:
            if sistema.get("tarifa_nocturna_fija") is not None:
                costo_final = float(sistema["tarifa_nocturna_fija"])
                recargo_monto = max(0.0, costo_final - costo_base)
                desglose_calculo += f" | Tarifa nocturna fija aplicada: ${costo_final:.2f} MXN"
            elif sistema.get("recargo_porcentaje", 0) > 0:
                pct = sistema["recargo_porcentaje"]
                recargo_monto = round(costo_base * (pct / 100.0), 2)
                costo_final = round(costo_base + recargo_monto, 2)
                desglose_calculo += f" | Recargo nocturno oficial +{pct:.0f}% (+${recargo_monto:.2f}) -> Total: ${costo_final:.2f} MXN"

        return {
            "sistema_id": sistema_id_norm,
            "nombre": sistema["nombre"],
            "jurisdiccion_nominal": sistema["jurisdiccion"],
            "jurisdiccion_aplicada": jurisdiccion_operativa,
            "red_tipo": sistema["red_tipo"],
            "distancia_km": round(distancia, 2),
            "hora_decimal": hora_norm,
            "hora_formato": decimal_a_hora_str(hora_norm),
            "dia": dia.upper(),
            "en_servicio": en_servicio,
            "detalle_horario": desc_horario,
            "es_nocturno": es_nocturno,
            "esquema_cobro": esquema,
            "costo_base": round(costo_base, 2),
            "recargo_nocturno_monto": round(recargo_monto, 2),
            "costo_final": round(costo_final, 2),
            "medio_pago": sistema["medio_pago"],
            "beneficios_gratuidad": sistema["beneficios_gratuidad"],
            "reglas_transbordo": sistema["reglas_transbordo"],
            "desglose_calculo": desglose_calculo
        }

def ejecutar_suite_pruebas(engine: TransitPricingEngine) -> bool:
    """Ejecuta una serie de validaciones automáticas para garantizar exactitud tarifaria."""
    print("=" * 70)
    print("🧪 EJECUTANDO SUITE DE PRUEBAS DEL MOTOR DE TARIFAS Y HORARIOS")
    print("=" * 70)

    # Prueba 1: Metro Lunes a las 10:00 (Diurno)
    r1 = engine.calcular_costo_tramo("METRO", distancia_km=15.0, hora_decimal=10.0, dia="LUNES")
    assert r1["en_servicio"] is True, "Metro debe estar en servicio Lunes a las 10:00"
    assert r1["costo_final"] == 5.00, f"Tarifa Metro esperada 5.00, obtenida {r1['costo_final']}"
    assert r1["es_nocturno"] is False, "Metro a las 10:00 no es nocturno"
    print("✅ Prueba 1 superada: Metro CDMX $5.00 tarifa única diurna.")

    # Prueba 2: Metro Domingo a las 02:30 (Cerrado)
    r2 = engine.calcular_costo_tramo("METRO", distancia_km=5.0, hora_decimal=2.5, dia="DOMINGO")
    assert r2["en_servicio"] is False, "Metro debe estar cerrado Domingo a las 02:30"
    print("✅ Prueba 2 superada: Metro cerrado de madrugada (02:30 hrs).")

    # Prueba 3: RTP Nochebús a las 02:30 (Abierto, tarifa $7.00)
    r3 = engine.calcular_costo_tramo("RTP_NOCHEBUS", distancia_km=12.0, hora_decimal=2.5, dia="DOMINGO")
    assert r3["en_servicio"] is True, "RTP Nochebús debe estar abierto a las 02:30"
    assert r3["costo_final"] == 7.00, f"Tarifa Nochebús esperada 7.00, obtenida {r3['costo_final']}"
    print("✅ Prueba 3 superada: RTP Nochebús abierto a las 02:30 ($7.00 tarifa fija).")

    # Prueba 4: Microbús Concesionado CDMX por distancia diurna
    r4_a = engine.calcular_costo_tramo("CONCESIONADO_CDMX_MICROBUS", distancia_km=4.0, hora_decimal=12.0)
    assert r4_a["costo_final"] == 6.00, f"Microbús <=5 km esperado 6.00, obtenido {r4_a['costo_final']}"

    r4_b = engine.calcular_costo_tramo("CONCESIONADO_CDMX_MICROBUS", distancia_km=8.0, hora_decimal=12.0)
    assert r4_b["costo_final"] == 6.50, f"Microbús 5-12 km esperado 6.50, obtenido {r4_b['costo_final']}"

    r4_c = engine.calcular_costo_tramo("CONCESIONADO_CDMX_MICROBUS", distancia_km=14.0, hora_decimal=12.0)
    assert r4_c["costo_final"] == 7.50, f"Microbús >12 km esperado 7.50, obtenido {r4_c['costo_final']}"
    print("✅ Prueba 4 superada: Escalamiento por tramos Microbús CDMX ($6.00 / $6.50 / $7.50).")

    # Prueba 5: Microbús Concesionado CDMX con recargo nocturno (+20% a la 01:00 am)
    r5 = engine.calcular_costo_tramo("CONCESIONADO_CDMX_MICROBUS", distancia_km=8.0, hora_decimal=1.0)
    # $6.50 * 1.20 = $7.80
    assert r5["es_nocturno"] is True, "A la 01:00 am debe aplicar recargo nocturno"
    assert r5["costo_final"] == 7.80, f"Recargo nocturno microbús esperado 7.80, obtenido {r5['costo_final']}"
    print("✅ Prueba 5 superada: Microbús CDMX recargo nocturno +20% a la 01:00 AM ($7.80).")

    # Prueba 6: Combi Concesionada Edomex ($14.00 base primeros 5 km + $0.25/km adicional)
    r6_base = engine.calcular_costo_tramo("CONCESIONADO_EDOMEX_COMBI", distancia_km=4.5, hora_decimal=12.0)
    assert r6_base["costo_final"] == 14.00, f"Combi Edomex base esperada 14.00, obtenida {r6_base['costo_final']}"

    r6_largo = engine.calcular_costo_tramo("CONCESIONADO_EDOMEX_COMBI", distancia_km=13.0, hora_decimal=12.0)
    # 14.00 + (13 - 5) * 0.25 = 14.00 + 2.00 = 16.00
    assert r6_largo["costo_final"] == 16.00, f"Combi Edomex 13km esperada 16.00, obtenida {r6_largo['costo_final']}"
    print("✅ Prueba 6 superada: Combi Edomex ($14.00 base + $0.25/km adicional).")

    # Prueba 7: Combi Concesionada Edomex nocturna (+20% a las 23:30)
    r7_noc = engine.calcular_costo_tramo("CONCESIONADO_EDOMEX_COMBI", distancia_km=13.0, hora_decimal=23.5)
    # $16.00 * 1.20 = $19.20
    assert r7_noc["es_nocturno"] is True, "23:30 debe ser nocturno en combi Edomex"
    assert r7_noc["costo_final"] == 19.20, f"Combi Edomex nocturna esperada 19.20, obtenida {r7_noc['costo_final']}"
    print("✅ Prueba 7 superada: Combi Edomex nocturna 23:30 (+20% -> $19.20).")

    # Prueba 8: Tren Suburbano (Viaje corto $10.50 vs Viaje largo $24.50)
    r8_corto = engine.calcular_costo_tramo("TREN_SUBURBANO", distancia_km=10.0, hora_decimal=15.0)
    assert r8_corto["costo_final"] == 10.50, f"Suburbano corto esperado 10.50, obtenido {r8_corto['costo_final']}"

    r8_largo = engine.calcular_costo_tramo("TREN_SUBURBANO", distancia_km=22.0, hora_decimal=15.0)
    assert r8_largo["costo_final"] == 24.50, f"Suburbano largo esperado 24.50, obtenido {r8_largo['costo_final']}"
    print("✅ Prueba 8 superada: Tren Suburbano viaje corto ($10.50) vs largo ($24.50).")

    # Prueba 9: Consulta por hora Domingo 02:30 AM
    r9_hora = engine.consultar_transporte_por_hora(dia="DOMINGO", hora_decimal=2.5)
    abiertos_ids = r9_hora["resumen_estadistico"]["sistemas_abiertos_ids"]
    assert "RTP_NOCHEBUS" in abiertos_ids, "RTP Nochebús debe estar en abiertos a las 02:30 AM"
    assert "METRO" not in abiertos_ids, "Metro NO debe estar en abiertos a las 02:30 AM"
    print(f"✅ Prueba 9 superada: Consulta general a las 02:30 AM identifica {len(abiertos_ids)} abiertos.")

    # Prueba 10: Cruce metropolitano origen Edomex en Microbús CDMX
    r10_metro = engine.calcular_costo_tramo("CONCESIONADO_CDMX_MICROBUS", distancia_km=10.0, hora_decimal=8.0, origen_edomex=True)
    # Regla metropolitana: aplica esquema Edomex ($14.00 base + 5*0.25 = $15.25)
    assert r10_metro["costo_final"] == 15.25, f"Esperado $15.25 por cruce metropolitano Edomex, obtenido {r10_metro['costo_final']}"
    print("✅ Prueba 10 superada: Cruce fronterizo Edomex a CDMX cobra tarifa metropolitana ($15.25).")

    print("=" * 70)
    print("🎉 TODAS LAS PRUEBAS (10/10) TERMINARON EXITOSAMENTE CON CÓDIGO 0.")
    print("=" * 70)
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Motor de Tarifas y Horarios Dinámicos CDMX / Edomex - Chilangatón 2026",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python3 scripts/schedule_pricing_engine.py --hora 2.5 --dia DOMINGO
  python3 scripts/schedule_pricing_engine.py --sistema METRO --distancia 10.0
  python3 scripts/schedule_pricing_engine.py --sistema CONCESIONADO_EDOMEX_COMBI --distancia 12.0 --hora 23.5
  python3 scripts/schedule_pricing_engine.py --sistema CONCESIONADO_CDMX_MICROBUS --distancia 8.0 --edomex
  python3 scripts/schedule_pricing_engine.py --test
        """
    )
    parser.add_argument("--hora", type=float, default=None, help="Hora del día en formato decimal (ej. 2.5 para 02:30, 14.75 para 14:45)")
    parser.add_argument("--dia", type=str, default="LUNES", help="Día de la semana (LUNES, MARTES, ..., SABADO, DOMINGO, FESTIVO)")
    parser.add_argument("--sistema", type=str, default=None, help="Identificador del subsistema de transporte (ej. METRO, METROBUS, CONCESIONADO_EDOMEX_COMBI)")
    parser.add_argument("--distancia", type=float, default=5.0, help="Distancia del tramo en kilómetros (default: 5.0 km)")
    parser.add_argument("--edomex", action="store_true", help="Bandera que indica si el tramo se origina o cruza en el Estado de México")
    parser.add_argument("--json", action="store_true", help="Imprimir la salida en formato JSON puro")
    parser.add_argument("--test", action="store_true", help="Ejecutar suite completa de pruebas unitarias y aserciones")

    args = parser.parse_args()

    engine = TransitPricingEngine()

    if args.test:
        ejecutar_suite_pruebas(engine)
        sys.exit(0)

    # Si se especificó un sistema específico para cotizar tramo
    if args.sistema:
        hora = args.hora if args.hora is not None else 12.0
        resultado = engine.calcular_costo_tramo(
            sistema_id=args.sistema,
            distancia_km=args.distancia,
            hora_decimal=hora,
            origen_edomex=args.edomex,
            dia=args.dia
        )
        if args.json:
            print(json.dumps(resultado, ensure_ascii=False, indent=2))
        else:
            print("\n" + "=" * 65)
            print(f"💰 CÁLCULO DE COSTO DE TRAYECTO: {resultado['nombre']}")
            print("=" * 65)
            print(f"• Jurisdicción:      {resultado['jurisdiccion_aplicada']} ({resultado['red_tipo']})")
            print(f"• Día y Hora:        {resultado['dia']} a las {resultado['hora_formato']} hrs")
            print(f"• Distancia:         {resultado['distancia_km']} km")
            print(f"• Estatus Servicio:  {'🟢 ABIERTO' if resultado['en_servicio'] else '🔴 CERRADO'}")
            print(f"• Detalle Horario:   {resultado['detalle_horario']}")
            print(f"• Medio de Pago:     {resultado['medio_pago']}")
            print(f"• Esquema Cobro:     {resultado['esquema_cobro']}")
            print(f"• Tarifa Base:       ${resultado['costo_base']:.2f} MXN")
            if resultado['es_nocturno']:
                print(f"• Recargo Nocturno:  +${resultado['recargo_nocturno_monto']:.2f} MXN (Tarifa nocturna activa)")
            print(f"• COSTO TOTAL:       ${resultado['costo_final']:.2f} MXN")
            print(f"• Desglose:          {resultado['desglose_calculo']}")
            print(f"• Gratuidad:         {resultado['beneficios_gratuidad']}")
            print(f"• Transbordos:       {resultado['reglas_transbordo']}")
            print("=" * 65 + "\n")
        sys.exit(0)

    # Si no se especificó sistema, se hace una consulta general por hora
    hora = args.hora if args.hora is not None else 12.0
    resultado = engine.consultar_transporte_por_hora(dia=args.dia, hora_decimal=hora)

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        consulta = resultado["consulta"]
        stats = resultado["resumen_estadistico"]
        print("\n" + "=" * 75)
        print(f"🕒 DISPONIBILIDAD Y TARIFAS DE TRANSPORTE - {consulta['dia_clave'].upper()} {consulta['hora_formato']} HRS ({consulta['fase_dia']})")
        print("=" * 75)
        print(f"• Total Sistemas Evaluados: {stats['total_sistemas']}")
        print(f"• Sistemas en Operación:    🟢 {stats['total_abiertos']}")
        print(f"• Sistemas Fuera de Horario:🔴 {stats['total_cerrados']}")
        print(f"• Tarifa Promedio CDMX:     ${stats['tarifa_promedio_abiertos_cdmx']:.2f} MXN")
        print(f"• Tarifa Promedio Edomex:   ${stats['tarifa_promedio_abiertos_edomex']:.2f} MXN")
        print(f"• Brecha Edomex vs CDMX:    +{stats['diferencial_metropolitano_pct']}% más costoso en zona conurbada")
        print("-" * 75)
        print(f"{'SISTEMA':<26} | {'JURISD':<7} | {'TARIFA':<8} | {'HORARIO':<10} | {'MEDIO DE PAGO'}")
        print("-" * 75)

        for s in resultado["sistemas_abiertos"]:
            noc_tag = " (NOC)" if s["es_nocturno"] else ""
            print(f"{s['sistema_id']:<26} | {s['jurisdiccion']:<7} | ${s['tarifa_vigente_base']:<5.2f}{noc_tag} | ABIERTO    | {s['medio_pago']}")

        if resultado["sistemas_cerrados"]:
            print("-" * 75)
            print("🔴 SISTEMAS CERRADOS A ESTA HORA:")
            for s in resultado["sistemas_cerrados"]:
                print(f"  ❌ {s['sistema_id']:<24} | {s['jurisdiccion']:<7} | {s['detalle_horario']}")

        print("=" * 75 + "\n")

if __name__ == "__main__":
    main()
