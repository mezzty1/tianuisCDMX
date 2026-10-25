#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Catálogo Modular y Jerárquico de Giros Comerciales para la CDMX
Chilangotón 2026 - Reto 1: Comercio Popular y Barrial
"""

import os
import json
import re
import unicodedata
import pandas as pd
from collections import Counter

# 1. Macro-categorías
CATEGORIAS = [
    {
        "id": "CAT_ALIM_FRESCOS",
        "nombre": "Alimentos Frescos y Perecederos",
        "descripcion": "Productos perecederos no procesados de la canasta básica: carnes, aves, pescados, frutas, verduras, lácteos y huevo.",
        "icono": "🥦",
        "color_hex": "#059669",
        "icono_png": "assets/icons/puestos/puesto_cat_alim_frescos_verde.png",
        "tipo_mercado_cdmx": "basico",
        "mercomuna_default": True,
        "canasta_basica_default": True
    },
    {
        "id": "CAT_ABARROTES_CANASTA",
        "nombre": "Abarrotes, Materias Primas y Canasta Básica",
        "descripcion": "Comercio de alimentos secos, granos, semillas, tortillas, panadería tradicional y abastos de primera necesidad.",
        "icono": "🥫",
        "color_hex": "#D97706",
        "icono_png": "assets/icons/puestos/puesto_cat_abarrotes_canasta_ambar.png",
        "tipo_mercado_cdmx": "basico",
        "mercomuna_default": True,
        "canasta_basica_default": True
    },
    {
        "id": "CAT_COMIDA_PREPARADA",
        "nombre": "Alimentos Preparados, Bebidas y Antojitos",
        "descripcion": "Venta de comida elaborada para consumo inmediato en el local o para llevar: antojitos mexicanos, tacos, fondas, tortas y bebidas.",
        "icono": "🌮",
        "color_hex": "#EA580C",
        "icono_png": "assets/icons/puestos/puesto_cat_comida_preparada_naranja.png",
        "tipo_mercado_cdmx": "alimentos_preparados",
        "mercomuna_default": False,
        "canasta_basica_default": False
    },
    {
        "id": "CAT_ROPA_CALZADO_TEXTIL",
        "nombre": "Ropa, Calzado, Telas y Accesorios",
        "descripcion": "Prendas de vestir nuevas o de paca, calzado formal y deportivo, blancos, telas y artículos personales de moda.",
        "icono": "👕",
        "color_hex": "#2563EB",
        "icono_png": "assets/icons/puestos/puesto_cat_ropa_calzado_textil_azul.png",
        "tipo_mercado_cdmx": "complementario",
        "mercomuna_default": False,
        "canasta_basica_default": False
    },
    {
        "id": "CAT_HOGAR_FERRETERIA",
        "nombre": "Artículos del Hogar, Ferretería y Limpieza",
        "descripcion": "Insumos para mantenimiento de vivienda, herramientas, jarciería, enseres de cocina, muebles, plantas y mascotas.",
        "icono": "🔨",
        "color_hex": "#0891B2",
        "icono_png": "assets/icons/puestos/puesto_cat_hogar_ferreteria_cian.png",
        "tipo_mercado_cdmx": "complementario",
        "mercomuna_default": False,
        "canasta_basica_default": False
    },
    {
        "id": "CAT_SALUD_BELLEZA",
        "nombre": "Salud, Cuidado Personal y Belleza",
        "descripcion": "Medicamentos genéricos, cosmética, estética, barbería, uñas, herbolaria tradicional y cuidado corporal.",
        "icono": "✂️",
        "color_hex": "#DB2777",
        "icono_png": "assets/icons/puestos/puesto_cat_salud_belleza_rosa.png",
        "tipo_mercado_cdmx": "servicios",
        "mercomuna_default": False,
        "canasta_basica_default": False
    },
    {
        "id": "CAT_PAPELERIA_TECNOLOGIA",
        "nombre": "Papelería, Cómputo, Regalos y Juguetería",
        "descripcion": "Artículos escolares, de oficina, copias, telefonía celular, novedades, juguetería, artesanías y regalos.",
        "icono": "✏️",
        "color_hex": "#7C3AED",
        "icono_png": "assets/icons/puestos/puesto_cat_papeleria_tecnologia_morado.png",
        "tipo_mercado_cdmx": "complementario",
        "mercomuna_default": False,
        "canasta_basica_default": False
    },
    {
        "id": "CAT_OFICIOS_SERVICIOS",
        "nombre": "Oficios Tradicionales y Reparaciones",
        "descripcion": "Servicios barriales técnicos, manuales y artesanales: cerrajería, costura, zapateros, mecánica, carpintería y herrería.",
        "icono": "🪛",
        "color_hex": "#65A30D",
        "icono_png": "assets/icons/puestos/puesto_cat_oficios_servicios_olivo.png",
        "tipo_mercado_cdmx": "servicios",
        "mercomuna_default": False,
        "canasta_basica_default": False
    },
    {
        "id": "CAT_BAZAR_CHACHARAS",
        "nombre": "Chácharas, Segunda Mano y Comercio Mixto",
        "descripcion": "Artículos usados, antigüedades, bazares, chácharas y puestos tradicionales de abasto y mercancía combinada.",
        "icono": "📦",
        "color_hex": "#9F1239",
        "icono_png": "assets/icons/puestos/puesto_cat_bazar_chacharas_terracota.png",
        "tipo_mercado_cdmx": "mixto",
        "mercomuna_default": False,
        "canasta_basica_default": False
    }
]

# 2. Subgiros específicos con atributos, metadatos y keywords
SUBGIROS = [
    # --- CAT_ALIM_FRESCOS ---
    {
        "id": "recauderia_fruteria",
        "categoria_id": "CAT_ALIM_FRESCOS",
        "nombre": "Recaudería, Frutería y Verdulería",
        "descripcion": "Venta al por menor de frutas frescas, verduras, hortalizas, legumbres y recaudería a granel.",
        "canasta_basica": True, "mercomuna": True, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "basico",
        "keywords": [
            r"\bRECAUD[EA]RIA\b", r"\bVERDULERIA\b", r"\bFRUTERIA\b", r"\bFRUTAS?\b", r"\bVERDURAS?\b",
            r"\bLEGUMBRES?\b", r"\bHORTALIZAS?\b", r"\bJITOMATE\b", r"\bCEBOLLA\b", r"\bAGUACATE\b",
            r"\bNOPALES?\b", r"\bPAPAS?\b", r"\bPLATANOS?\b", r"\bNARANJAS?\b", r"\bMANZANAS?\b",
            r"\bVENTA DE VERDURAS\b", r"\bVENTA DE FRUTAS?\b", r"\bPRODUCTOS AGRICOLAS\b"
        ]
    },
    {
        "id": "carniceria",
        "categoria_id": "CAT_ALIM_FRESCOS",
        "nombre": "Carnicería y Tocinería",
        "descripcion": "Venta de carnes rojas frescas: res, cerdo, ternera, chuletas, bistec y tocinería.",
        "canasta_basica": True, "mercomuna": True, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "basico",
        "keywords": [
            r"\bCARNICERIA\b", r"\bTOCINERIA\b", r"\bCARNIC[AO]S\b", r"\bCARNE DE RES\b", r"\bCARNE DE CERDO\b",
            r"\bCARNE DE PUERCO\b", r"\bVENTA DE CARNE\b", r"\bBISTEC\b", r"\bCHULETAS?\b", r"\bOBRADOR\b"
        ]
    },
    {
        "id": "polleria",
        "categoria_id": "CAT_ALIM_FRESCOS",
        "nombre": "Pollería, Aves de Corral y Rosticería",
        "descripcion": "Venta de pollo fresco en canal, pechugas, retazo, gallina, pavo y expendio de pollo rostizado.",
        "canasta_basica": True, "mercomuna": True, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "basico",
        "keywords": [
            r"\bPOLLERIA\b", r"\bPOLLOS?\b", r"\bPECHUGAS?\b", r"\bVENTA DE POLLO\b", r"\bAVES DE CORRAL\b",
            r"\bGALLINAS?\b", r"\bPAVO CRUDO\b", r"\bRETAZO DE POLLO\b", r"\bROSTICERIA\b"
        ]
    },
    {
        "id": "pescaderia",
        "categoria_id": "CAT_ALIM_FRESCOS",
        "nombre": "Pescadería y Marisquería en Crudo",
        "descripcion": "Venta de pescados frescos de mar y río, mariscos y moluscos crudos o enhielados.",
        "canasta_basica": True, "mercomuna": True, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "basico",
        "keywords": [
            r"\bPESCADERIA\b", r"\bPESCADOS?\b", r"\bMARISCOS?\b", r"\bCAMARON\b", r"\bMOJARRA\b",
            r"\bFILETE DE PESCADO\b"
        ]
    },
    {
        "id": "cremeria_lacteos",
        "categoria_id": "CAT_ALIM_FRESCOS",
        "nombre": "Cremería, Quesería y Salchichonería",
        "descripcion": "Venta de productos lácteos, quesos artesanales, crema, mantequilla, jamón y salchichonería.",
        "canasta_basica": True, "mercomuna": True, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "basico",
        "keywords": [
            r"\bCREMERIA\b", r"\bQUESERIA\b", r"\bSALCHICHONERIA\b", r"\bLACTEOS\b", r"\bQUESOS?\b",
            r"\bCREMA\b", r"\bJAMON\b", r"\bSALCHICHAS?\b", r"\bEMBUTIDOS\b", r"\bMANTEQUILLA\b"
        ]
    },

    # --- CAT_ABARROTES_CANASTA ---
    {
        "id": "tienda_abarrotes",
        "categoria_id": "CAT_ABARROTES_CANASTA",
        "nombre": "Tienda de Abarrotes, Miscelánea y Minisúper",
        "descripcion": "Comercio minorista tradicional de abarrotes empacados, latería y productos esenciales de conveniencia.",
        "canasta_basica": True, "mercomuna": True, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "basico",
        "keywords": [
            r"\bTIENDA\s+DE\s+ABARROTES\b", r"\bABARROTES\b", r"\bABARROTERA\b", r"\bMISCELANEA\b",
            r"\bTIENDITA\b", r"\bMINISUPER\b", r"\bULTRAMARINOS\b", r"\bSUPERCITO\b", r"^\s*TIENDA\s*$"
        ]
    },
    {
        "id": "tortilleria_molino",
        "categoria_id": "CAT_ABARROTES_CANASTA",
        "nombre": "Tortillería y Molino de Nixtamal",
        "descripcion": "Elaboración y venta de tortillas de maíz nixtamalizado, harina de trigo, masa fresca y totopos.",
        "canasta_basica": True, "mercomuna": True, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "basico",
        "keywords": [
            r"\bTORTILLERIA\b", r"\bMOLINO\b", r"\bMOLINO DE NIXTAMAL\b", r"\bTORTILLAS?\b", r"\bMASA DE MAIZ\b",
            r"\bNIXTAMAL\b", r"\bTOTOPOS\b"
        ]
    },
    {
        "id": "panaderia_expendio",
        "categoria_id": "CAT_ABARROTES_CANASTA",
        "nombre": "Panadería Tradicional y Expendio de Pan",
        "descripcion": "Producción y despacho de pan tradicional dulce y blanco (bolillo, telera, baguettes).",
        "canasta_basica": True, "mercomuna": True, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "basico",
        "keywords": [
            r"\bPANADERIA\b", r"\bPANIFICADORA\b", r"\bEXPENDIO DE PAN\b", r"\bPAN DULCE\b", r"\bBOLILLOS?\b",
            r"\bTELERAS?\b", r"\bPAN TRADICIONAL\b", r"\bVENTA DE PAN\b", r"^\s*PAN\s*$"
        ]
    },
    {
        "id": "semillas_chiles_granos",
        "categoria_id": "CAT_ABARROTES_CANASTA",
        "nombre": "Semillas, Chiles Secos, Granos y Especias",
        "descripcion": "Venta a granel de frijol, arroz, maíz, chiles secos, especias, condimentos y mole en pasta.",
        "canasta_basica": True, "mercomuna": True, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "basico",
        "keywords": [
            r"\bCHILES SECOS\b", r"\bSEMILLAS?\b", r"\bGRANOS?\b", r"\bFRIJOL\b", r"\bESPECIAS\b",
            r"\bCONDIMENTOS\b", r"\bCEREALES\b", r"\bFRUTOS SECOS\b", r"\bMOLE EN PASTA\b"
        ]
    },
    {
        "id": "materias_primas",
        "categoria_id": "CAT_ABARROTES_CANASTA",
        "nombre": "Materias Primas y Artículos Desechables",
        "descripcion": "Insumos para repostería, desechables, bolsas plásticas, moldes y veladoras.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bMATERIAS PRIMAS\b", r"\bMATERIA PRIMA\b", r"\bDESECHABLES?\b", r"\bBOLSAS DE PLASTICO\b",
            r"\bINSUMOS DE REPOSTERIA\b"
        ]
    },
    {
        "id": "dulceria_botanas",
        "categoria_id": "CAT_ABARROTES_CANASTA",
        "nombre": "Dulcería, Confitería y Botanas",
        "descripcion": "Venta al mayoreo y menudeo de dulces, confitería, botanas empacadas, frituras y piñatas.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bDULCERIA\b", r"\bDULCES?\b", r"\bCONFITERIA\b", r"\bBOTANAS?\b", r"\bFRITURAS?\b",
            r"\bCHOCOLATES?\b", r"\bGOMITAS\b", r"\bPI[NÑ]ATAS\b", r"\bSNACKS?\b"
        ]
    },
    {
        "id": "purificadora_agua",
        "categoria_id": "CAT_ABARROTES_CANASTA",
        "nombre": "Purificadora de Agua y Venta de Hielo",
        "descripcion": "Purificación, llenado y venta de garrafones de agua potable y hielo en cubos.",
        "canasta_basica": True, "mercomuna": True, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "basico",
        "keywords": [
            r"\bPURIFICADORA\b", r"\bAGUA PURIFICADA\b", r"\bGARRAFON(ES)?\b", r"\bVENTA DE AGUA\b",
            r"\bHIELO\b", r"\bAGUA POTABLE\b", r"^\s*AGUA\s*$"
        ]
    },

    # --- CAT_COMIDA_PREPARADA ---
    {
        "id": "taqueria",
        "categoria_id": "CAT_COMIDA_PREPARADA",
        "nombre": "Taquería",
        "descripcion": "Preparación y venta de tacos: pastor, suadero, bistec, tripa, carnitas, barbacoa, birria, guisados y canasta.",
        "canasta_basica": False, "mercomuna": False, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "alimentos_preparados",
        "keywords": [
            r"\bTAQUERIA\b", r"\bTACOS?\b", r"\bTAQUERO\b", r"\bCARNITAS\b", r"\bBARBACOA\b", r"\bBIRRIA\b",
            r"\bSUADERO\b", r"\bPASTOR\b"
        ]
    },
    {
        "id": "antojitos_mexicanos",
        "categoria_id": "CAT_COMIDA_PREPARADA",
        "nombre": "Antojitos Mexicanos y Garnachas",
        "descripcion": "Venta de quesadillas, gorditas, sopes, pambazos, huaraches, tlacoyos y tostadas.",
        "canasta_basica": False, "mercomuna": False, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "alimentos_preparados",
        "keywords": [
            r"\bANTOJITOS?\b", r"\bQUESADILLAS?\b", r"\bGORDITAS?\b", r"\bSOPES?\b", r"\bPAMBAZOS?\b",
            r"\bHUARACHES?\b", r"\bTLACOYOS?\b", r"\bTOSTADAS?\b", r"\bCHILAQUILES\b", r"\bGARNACHAS?\b"
        ]
    },
    {
        "id": "tamales_atole",
        "categoria_id": "CAT_COMIDA_PREPARADA",
        "nombre": "Puesto de Tamales y Atole",
        "descripcion": "Venta matutina y nocturna de tamales tradicionales y atoles (champurrado, arroz, avena).",
        "canasta_basica": False, "mercomuna": False, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "alimentos_preparados",
        "keywords": [
            r"\bTAMAL(ES)?\b", r"\bATOLE?S?\b", r"\bCHAMPURRADO\b", r"\bTAMALERIA\b", r"\bGUAJOLOTAS?\b"
        ]
    },
    {
        "id": "cocina_economica_fonda",
        "categoria_id": "CAT_COMIDA_PREPARADA",
        "nombre": "Cocina Económica, Fonda y Comida Corrida",
        "descripcion": "Establecimiento barrial que ofrece menús caseros completos y guisados del día a precio accesible.",
        "canasta_basica": False, "mercomuna": False, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "alimentos_preparados",
        "keywords": [
            r"\bCOCINA ECONOMICA\b", r"\bFONDA\b", r"\bCOMIDA CORRIDA\b", r"\bGUISADOS?\b",
            r"\bCOCINA CASERA\b", r"\bCOMEDOR COMUNITARIO\b"
        ]
    },
    {
        "id": "torteria",
        "categoria_id": "CAT_COMIDA_PREPARADA",
        "nombre": "Tortería y Lonchería",
        "descripcion": "Preparación y venta de tortas frías y calientes, cemitas, lonches y chapatas.",
        "canasta_basica": False, "mercomuna": False, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "alimentos_preparados",
        "keywords": [
            r"\bTORTERIA\b", r"\bTORTAS?\b", r"\bLONCHERIA\b", r"\bCEMITAS?\b"
        ]
    },
    {
        "id": "comida_rapida_pizzas",
        "categoria_id": "CAT_COMIDA_PREPARADA",
        "nombre": "Comida Rápida, Hamburguesas, Alitas y Pizzas",
        "descripcion": "Hamburguesas al carbón, hot dogs, alitas, pizzas artesanales, boneless y papas fritas.",
        "canasta_basica": False, "mercomuna": False, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "alimentos_preparados",
        "keywords": [
            r"\bCOMIDA RAPIDA\b", r"\bHAMBURGUESAS?\b", r"\bHOT DOGS?\b", r"\bHOTDOGS?\b", r"\bALITAS\b",
            r"\bBONELESS\b", r"\bPIZZERIA\b", r"\bPIZZAS?\b", r"\bSALCHIPULPOS\b", r"\bPAPAS A LA FRANCESA\b"
        ]
    },
    {
        "id": "restaurante_marisqueria",
        "categoria_id": "CAT_COMIDA_PREPARADA",
        "nombre": "Restaurante Familiar y Mariscos Preparados",
        "descripcion": "Restaurantes familiares, marisquerías preparadas, coctelerías de mariscos y caldos.",
        "canasta_basica": False, "mercomuna": False, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "alimentos_preparados",
        "keywords": [
            r"\bRESTAURANTE?S?\b", r"\bMARISQUERIA\b", r"\bCOCTELERIA\b", r"\bCEVICHE\b", r"\bAGUACHILE\b",
            r"\bCALDO DE GALLINA\b", r"\bCALDO DE CAMARON\b"
        ]
    },
    {
        "id": "cafeteria_fuente_sodas",
        "categoria_id": "CAT_COMIDA_PREPARADA",
        "nombre": "Cafetería, Fuente de Sodas, Juguería y Licuados",
        "descripcion": "Jugos naturales, licuados nutritivos, café de olla o espresso, desayunos ligeros y smoothies.",
        "canasta_basica": False, "mercomuna": False, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "alimentos_preparados",
        "keywords": [
            r"\bCAFETERIA\b", r"\bCAFE\b", r"\bFUENTE DE SODAS\b", r"\bJUGOS?\b", r"\bLICUADOS?\b",
            r"\bJUGUERIA\b", r"\bLICUADERIA\b", r"\bDESAYUNOS?\b", r"\bDESAYUNADOR\b", r"\bFRAPPES?\b", r"\bSMOOTHIES\b"
        ]
    },
    {
        "id": "postres_reposteria",
        "categoria_id": "CAT_COMIDA_PREPARADA",
        "nombre": "Postres, Pastelería y Repostería Casera",
        "descripcion": "Pasteles, gelatinas artísticas, flanes caseros, pays, repostería, donas, crepas y galletas.",
        "canasta_basica": False, "mercomuna": False, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "alimentos_preparados",
        "keywords": [
            r"\bPOSTRES?\b", r"\bPASTELERIA\b", r"\bREPOSTERIA\b", r"\bGELATINAS?\b", r"\bFLANES?\b",
            r"\bPASTELES?\b", r"\bCUPCAKES?\b", r"\bDONAS?\b", r"\bPAYS?\b", r"\bCREPAS?\b", r"\bWAFFLES?\b"
        ]
    },
    {
        "id": "paleteria_helados",
        "categoria_id": "CAT_COMIDA_PREPARADA",
        "nombre": "Paletería, Heladería y Nevería",
        "descripcion": "Paletas de agua y crema, helados artesanales, nieves de garrafa y aguas frescas tradicionales.",
        "canasta_basica": False, "mercomuna": False, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "alimentos_preparados",
        "keywords": [
            r"\bPALETERIA\b", r"\bHELADERIA\b", r"\bNEVERIA\b", r"\bPALETAS?\b", r"\bHELADOS?\b",
            r"\bNIEVES\b", r"\bAGUAS FRESCAS\b", r"\bESQUIMOS\b"
        ]
    },
    {
        "id": "elotes_esquites_botaneros",
        "categoria_id": "CAT_COMIDA_PREPARADA",
        "nombre": "Elotes, Esquites y Botanas Calientes",
        "descripcion": "Elotes hervidos o asados, esquites con tuétano, dorilocos y chicharrones preparados con cueritos.",
        "canasta_basica": False, "mercomuna": False, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "alimentos_preparados",
        "keywords": [
            r"\bELOTES?\b", r"\bESQUITES?\b", r"\bDORILOCOS\b", r"\bCHICHARRONES PREPARADOS\b",
            r"\bCHICHARRON PREPARADO\b"
        ]
    },
    {
        "id": "comida_preparada_general",
        "categoria_id": "CAT_COMIDA_PREPARADA",
        "nombre": "Comida Preparada y Venta de Alimentos (General)",
        "descripcion": "Puestos y locales de venta de alimentos y comida preparada sin desglose o combinada.",
        "canasta_basica": False, "mercomuna": False, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "alimentos_preparados",
        "keywords": [
            r"\bCOMIDA PREPARADA\b", r"\bVENTA DE COMIDA\b", r"\bALIMENTOS PREPARADOS\b", r"\bVENTA DE ALIMENTOS\b",
            r"\bCOMIDA PARA LLEVAR\b", r"\bNEGOCIO DE COMIDA\b", r"\bPUESTO DE COMIDA\b", r"\bALIMENTOS Y BEBIDAS\b",
            r"\bCOMIDAS?\b", r"\bALIMENTOS\b", r"\bALIMENTICIO\b", r"^\s*COCINA\s*$", r"\bPRODUCTOS ALIMENTICIOS\b"
        ]
    },

    # --- CAT_ROPA_CALZADO_TEXTIL ---
    {
        "id": "venta_ropa",
        "categoria_id": "CAT_ROPA_CALZADO_TEXTIL",
        "nombre": "Venta de Ropa Nueva y Confección",
        "descripcion": "Prendas de vestir nuevas para dama, caballero, niños y bebés: pantalones, vestidos, playeras, camisas.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bROPA\b", r"\bVENTA DE ROPA\b", r"\bTIENDA DE ROPA\b", r"\bBOUTIQUE\b", r"\bPANTALONES?\b",
            r"\bPLAYERAS?\b", r"\bVESTIDOS?\b", r"\bCHAMARRAS?\b", r"\bBLUSAS?\b", r"\bCAMISAS?\b",
            r"\bROPA DE DAMA\b", r"\bROPA INFANTIL\b", r"\bCONFECCION\b"
        ]
    },
    {
        "id": "zapateria_calzado",
        "categoria_id": "CAT_ROPA_CALZADO_TEXTIL",
        "nombre": "Zapatería, Calzado y Tenis",
        "descripcion": "Calzado formal, de vestir, tenis deportivos, botas, sandalias, zapatillas y pantuflas.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bZAPATERIA\b", r"\bCALZADO\b", r"\bZAPATOS?\b", r"\bTENIS\b", r"\bTENNIS\b",
            r"\bSANDALIAS?\b", r"\bBOTAS?\b", r"\bZAPATILLAS?\b", r"\bHUARACHES DE PIEL\b"
        ]
    },
    {
        "id": "lenceria_boneteria",
        "categoria_id": "CAT_ROPA_CALZADO_TEXTIL",
        "nombre": "Bonetería, Lencería y Ropa Interior",
        "descripcion": "Calcetería, calcetines, medias, ropa interior para dama y caballero, fajas y batas.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bBONETERIA\b", r"\bLENCERIA\b", r"\bROPA INTERIOR\b", r"\bCALCETINES\b", r"\bCALCETERIA\b",
            r"\bMEDIAS\b", r"\bFAJAS\b", r"\bBRASIERES\b", r"\bBOXERS\b"
        ]
    },
    {
        "id": "telas_blancos",
        "categoria_id": "CAT_ROPA_CALZADO_TEXTIL",
        "nombre": "Telas, Blancos, Cobijas y Cortinas",
        "descripcion": "Telas por metro, cobijas, sábanas, colchas, cobertores, toallas, cortinas y mantelería.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bTELAS?\b", r"\bBLANCOS\b", r"\bCOBIJAS?\b", r"\bSABANAS?\b", r"\bCOLCHAS?\b",
            r"\bCOBERTORES?\b", r"\bTOALLAS?\b", r"\bCORTINAS?\b", r"\bMANTELES?\b", r"\bTEXTIL(ES)?\b"
        ]
    },
    {
        "id": "bolsos_mochilas",
        "categoria_id": "CAT_ROPA_CALZADO_TEXTIL",
        "nombre": "Bolsos, Mochilas, Maletas y Accesorios",
        "descripcion": "Mochilas escolares, bolsas de mano para dama, carteras, cinturones y maletas de viaje.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bMOCHILAS?\b", r"\bBOLSOS?\b", r"\bBOLSAS PARA DAMA\b", r"\bCARTERAS?\b", r"\bMONEDEROS?\b",
            r"\bCINTURONES?\b", r"\bMALETAS?\b", r"\bMARICONERAS?\b"
        ]
    },
    {
        "id": "ropa_paca_segunda",
        "categoria_id": "CAT_ROPA_CALZADO_TEXTIL",
        "nombre": "Ropa de Paca y Ropa de Segunda Mano",
        "descripcion": "Prendas seminuevas, ropa usada de paca americana y saldos textiles en tianguis y bazares.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bROPA DE PACA\b", r"\bPACA\b", r"\bROPA USADA\b", r"\bROPA SEMINUEVA\b", r"\bROPA AMERICANA\b",
            r"\bBAZAR DE ROPA\b"
        ]
    },
    {
        "id": "venta_catalogo_moda",
        "categoria_id": "CAT_ROPA_CALZADO_TEXTIL",
        "nombre": "Venta por Catálogo de Moda y Calzado",
        "descripcion": "Comercio por catálogo multinivel y por pedido: Price Shoes, Andrea, Cklass, Ilusión.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bVENTAS? POR CATALOGO\b", r"\bCATALOGO\b", r"\bPRICE SHOES\b", r"\bANDREA\b",
            r"\bCKLASS\b", r"\bILUSION\b"
        ]
    },

    # --- CAT_HOGAR_FERRETERIA ---
    {
        "id": "ferreteria_tlapaleria",
        "categoria_id": "CAT_HOGAR_FERRETERIA",
        "nombre": "Ferretería, Tlapalería y Materiales",
        "descripcion": "Herramientas de mano, tornillos, clavos, material eléctrico menor, plomería, pinturas y solventes.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bFERRETERIA\b", r"\bTLAPALERIA\b", r"\bTLAPELERIA\b", r"\bHERRAMIENTAS?\b", r"\bTORNILLOS?\b",
            r"\bPLOMERIA\b", r"\bPINTURAS?\b", r"\bBROCHAS\b", r"\bMATERIAL ELECTRICO\b", r"\bMATERIALES PARA CONSTRUCCION\b",
            r"\bCONSTRUCCION\b"
        ]
    },
    {
        "id": "jarcieria_productos_limpieza",
        "categoria_id": "CAT_HOGAR_FERRETERIA",
        "nombre": "Jarciería y Productos de Limpieza a Granel",
        "descripcion": "Químicos de limpieza a granel (cloro, desinfectantes, jabón líquido), escobas y trapeadores.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bJARC[I]?ERIA\b", r"\bPRODUCTOS DE LIMPIEZA\b", r"\bLIMPIEZA\b", r"\bCLORO\b",
            r"\bDETERGENTES?\b", r"\bESCOBAS\b", r"\bTRAPEADORES?\b"
        ]
    },
    {
        "id": "plasticos_enseres_hogar",
        "categoria_id": "CAT_HOGAR_FERRETERIA",
        "nombre": "Artículos de Plástico y Enseres para Cocina",
        "descripcion": "Recipientes plásticos, cubetas, peltre, sartenes, cazuelas, ollas y vajillas populares.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bPLASTICOS?\b", r"\bTUPPERS?\b", r"\bENSERES DE COCINA\b", r"\bARTICULOS PARA COCINA\b",
            r"\bCUBETAS\b", r"\bPELTRE\b", r"\bOLLAS\b", r"\bSARTENES?\b", r"\bVAJILLAS?\b", r"\bTRASTES\b",
            r"\bPRODUCTOS PARA EL HOGAR\b", r"\bARTICULOS PARA EL HOGAR\b"
        ]
    },
    {
        "id": "muebles_colchones",
        "categoria_id": "CAT_HOGAR_FERRETERIA",
        "nombre": "Muebles para el Hogar, Colchonería y Tapicería",
        "descripcion": "Muebles de madera y pino, comedores, salas, colchones, cunas, tapicería y cestería de mimbre.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bMUEBLES?\b", r"\bCOLCHONERIA\b", r"\bCOLCHON(ES)?\b", r"\bMUEBLERIA\b", r"\bCESTERIA\b",
            r"\bMIMBRE\b", r"\bSALAS\b", r"\bCOMEDORES\b", r"\bTAPICERIA\b", r"\bTAPICERO\b"
        ]
    },
    {
        "id": "floreria_plantas",
        "categoria_id": "CAT_HOGAR_FERRETERIA",
        "nombre": "Florería, Flores Frescas y Plantas de Ornato",
        "descripcion": "Flores frescas de corte, arreglos florales para eventos, plantas en maceta, jardinería y tierra.",
        "canasta_basica": False, "mercomuna": False, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bFLORERIA\b", r"\bFLORES?\b", r"\bPLANTAS?\b", r"\bPLANTAS DE ORNATO\b", r"\bARREGLOS FLORALES\b",
            r"\bROSAS\b", r"\bMACETAS\b", r"\bVIVERO\b", r"\bJARDINERIA\b"
        ]
    },
    {
        "id": "mascotas_alimento",
        "categoria_id": "CAT_HOGAR_FERRETERIA",
        "nombre": "Mascotas, Peces de Ornato y Alimento Animal",
        "descripcion": "Croquetas a granel para perros y gatos, peces de ornato, peceras y accesorios para animales de compañía.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bMASCOTAS?\b", r"\bALIMENTO PARA MASCOTAS\b", r"\bCROQUETAS?\b", r"\bPECES DE ORNATO\b",
            r"\bACUARIO\b", r"\bPECERAS?\b", r"\bVETERINARIA\b"
        ]
    },

    # --- CAT_SALUD_BELLEZA ---
    {
        "id": "farmacia_botica",
        "categoria_id": "CAT_SALUD_BELLEZA",
        "nombre": "Farmacia y Botica Tradicional",
        "descripcion": "Medicamentos genéricos y de patente, material de curación, sueros e higiene de primeros auxilios.",
        "canasta_basica": False, "mercomuna": True, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "basico",
        "keywords": [
            r"\bFARMACIA\b", r"\bBOTICA\b", r"\bMEDICAMENTOS?\b", r"\bGENERICOS\b", r"\bMATERIAL DE CURACION\b",
            r"\bDROGUERIA\b"
        ]
    },
    {
        "id": "optica_lentes",
        "categoria_id": "CAT_SALUD_BELLEZA",
        "nombre": "Óptica y Lentes Graduados",
        "descripcion": "Examen de la vista, armazones oftálmicos, micas graduadas y lentes de sol.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bOPTICA\b", r"\bLENTES?\b", r"\bANTEOJOS\b", r"\bARMAZONES\b", r"\bEXAMEN DE LA VISTA\b"
        ]
    },
    {
        "id": "estetica_peluqueria",
        "categoria_id": "CAT_SALUD_BELLEZA",
        "nombre": "Estética, Peluquería y Salón de Belleza",
        "descripcion": "Cortes de cabello para toda la familia, tintes, peinados, alaciados y tratamientos capilares.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bESTETICA\b", r"\bPELUQUERIA\b", r"\bSALON DE BELLEZA\b", r"\bCORTE DE CABELLO\b",
            r"\bESTILISTA\b", r"\bESTILISMO\b", r"\bPEINADOS?\b", r"\bTINTES?\b"
        ]
    },
    {
        "id": "barberia",
        "categoria_id": "CAT_SALUD_BELLEZA",
        "nombre": "Barbería y Cuidado Masculino",
        "descripcion": "Afeitado clásico a navaja, perfilado de barba, cortes urbanos y cuidado estético masculino.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bBARBERIA\b", r"\bBARBER SHOP\b", r"\bBARBERO\b", r"\bCORTE DE BARBA\b", r"\bAFEITADO\b"
        ]
    },
    {
        "id": "unas_pestanas_cosmetologia",
        "categoria_id": "CAT_SALUD_BELLEZA",
        "nombre": "Aplicación de Uñas, Pestañas y Spa",
        "descripcion": "Uñas acrílicas, gelish, extensiones de pestañas 1x1, depilación y cuidado facial.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bU[NÑ]AS\b", r"\bAPLICACION DE U[NÑ]AS\b", r"\bSALON DE U[NÑ]AS\b", r"\bGELISH\b",
            r"\bMANICURE\b", r"\bPEDICURE\b", r"\bPESTA[NÑ]AS\b", r"\bSPA\b", r"\bCOSMETOLOGIA\b"
        ]
    },
    {
        "id": "cosmeticos_perfumeria",
        "categoria_id": "CAT_SALUD_BELLEZA",
        "nombre": "Cosméticos, Maquillaje y Perfumería",
        "descripcion": "Maquillaje, labiales, cremas faciales, perfumería y venta de belleza por catálogo (Avon, Jafra, Mary Kay).",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bCOSM[EÉ]?TICOS?\b", r"\bMAQUILLAJE\b", r"\bPRODUCTOS DE BELLEZA\b", r"\bPERFUMERIA\b",
            r"\bPERFUMES?\b", r"\bBELLEZA\b", r"\bAVON\b", r"\bMARY KAY\b", r"\bJAFRA\b", r"\bNATURA\b"
        ]
    },
    {
        "id": "herbolaria_esoterismo",
        "categoria_id": "CAT_SALUD_BELLEZA",
        "nombre": "Herbolaria, Medicina Tradicional y Esoterismo",
        "descripcion": "Hierbas medicinales secas, tés curativos, pomadas de árnica, veladoras esotéricas y amuletos.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bHERBOLARIA\b", r"\bARTICULOS ESOTERICOS\b", r"\bESOTERISMO\b", r"\bESOTERICOS?\b",
            r"\bYERBERIA\b", r"\bHIERBAS MEDICINALES\b", r"\bVELADORAS ESOTERICAS\b", r"\bAMULETOS\b",
            r"\bINCIENSOS\b", r"\bMEDICINA TRADICIONAL\b"
        ]
    },
    {
        "id": "consultorio_dental_salud",
        "categoria_id": "CAT_SALUD_BELLEZA",
        "nombre": "Consultorio Dental y Servicios de Salud Barriales",
        "descripcion": "Atención odontológica, salud bucal, consultorio médico barrial, fisioterapia y medicina preventiva.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bCONSULTORIO DENTAL\b", r"\bDENTISTA\b", r"\bODONTOLOG[I]?A\b", r"\bCONSULTORIO MEDICO\b",
            r"\bSALUD\b", r"\bCLUB DE NUTRICION\b", r"\bSUPLEMENTOS ALIMENTICIOS\b", r"\bGIMNASIO\b"
        ]
    },

    # --- CAT_PAPELERIA_TECNOLOGIA ---
    {
        "id": "papeleria_copias",
        "categoria_id": "CAT_PAPELERIA_TECNOLOGIA",
        "nombre": "Papelería, Artículos Escolares y Copias",
        "descripcion": "Útiles escolares, libretas, cartulinas, fotocopiado, impresiones, enmicados y engargolados.",
        "canasta_basica": False, "mercomuna": True, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bPAPELERIA\b", r"\bUTILES ESCOLARES\b", r"\bCOPIAS\b", r"\bFOTOCOPIAS\b",
            r"\bENMICADOS\b", r"\bENGARGOLADOS\b"
        ]
    },
    {
        "id": "ciber_internet_computo",
        "categoria_id": "CAT_PAPELERIA_TECNOLOGIA",
        "nombre": "Café Internet, Ciber y Soporte Digital",
        "descripcion": "Renta de tiempo de computadoras, escaneos, trámites digitales ciudadanos e impresiones.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bCIBER\b", r"\bCAFE INTERNET\b", r"\bINTERNET\b", r"\bCOMPUTO\b", r"\bCYBER\b",
            r"\bTECNOLOGIA\b", r"\bELECTRONICA\b"
        ]
    },
    {
        "id": "reparacion_celulares",
        "categoria_id": "CAT_PAPELERIA_TECNOLOGIA",
        "nombre": "Reparación de Celulares y Accesorios Móviles",
        "descripcion": "Cambio de pantallas y baterías, fundas, micas de cristal, cargadores y accesorios para celular.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bCELULARES?\b", r"\bREPARACION DE CELULARES\b", r"\bACCESORIOS PARA CELULAR\b",
            r"\bFUNDAS PARA CELULAR\b", r"\bMICAS DE CRISTAL\b", r"\bCARGADORES\b", r"\bTELEFONIA\b"
        ]
    },
    {
        "id": "jugueteria_novedades",
        "categoria_id": "CAT_PAPELERIA_TECNOLOGIA",
        "nombre": "Juguetería, Novedades y Temporada",
        "descripcion": "Juguetes infantiles, novedades electrónicas, figuras de acción y artículos para fiestas y celebraciones.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bJUGUETERIA\b", r"\bJUGUETES?\b", r"\bNOVEDADES\b", r"\bARTICULOS DE TEMPORADA\b",
            r"\bARTICULOS PARA FIESTA\b"
        ]
    },
    {
        "id": "regalos_bisuteria",
        "categoria_id": "CAT_PAPELERIA_TECNOLOGIA",
        "nombre": "Tienda de Regalos, Bisutería y Joyería",
        "descripcion": "Bisutería de fantasía, aretes, collares, joyería de plata, peluches, envolturas de regalo y detalles.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bREGALOS?\b", r"\bTIENDA DE REGALOS\b", r"\bBISUTERIA\b", r"\bJOYERIA\b", r"\bPELUCHES?\b",
            r"\bENVOLTURAS\b", r"\bDETALLES\b", r"\bPLATA\b", r"\bVENTA DE PLATA\b"
        ]
    },
    {
        "id": "artesanias_manualidades",
        "categoria_id": "CAT_PAPELERIA_TECNOLOGIA",
        "nombre": "Artesanías, Manualidades y Mercería Creativa",
        "descripcion": "Artesanías populares de barro o madera, figuras de yeso para pintar, estambre, listones y mercería.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bARTESANIAS?\b", r"\bMANUALIDADES\b", r"\bMERCERIA\b", r"\bCERAMICA\b", r"\bBARRO\b",
            r"\bESTAMBRE\b", r"\bYESO PARA PINTAR\b"
        ]
    },

    # --- CAT_OFICIOS_SERVICIOS ---
    {
        "id": "taller_costura_sastreria",
        "categoria_id": "CAT_OFICIOS_SERVICIOS",
        "nombre": "Taller de Costura, Sastrería y Maquila",
        "descripcion": "Ajuste de bastillas, cierres, compostura de prendas, sastrería a medida y maquila de confección.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bCOSTURA\b", r"\bCOSTURERA\b", r"\bCOSTURERIA\b", r"\bCOSTURAS\b", r"\bSASTRERIA\b",
            r"\bSASTRE\b", r"\bCOMPOSTURAS?\b", r"\bARREGLOS DE ROPA\b", r"\bCORTE Y CONFECCION\b",
            r"\bMAQUILA\b", r"\bMAQUILADORA\b"
        ]
    },
    {
        "id": "cerrajeria",
        "categoria_id": "CAT_OFICIOS_SERVICIOS",
        "nombre": "Cerrajería y Duplicado de Llaves",
        "descripcion": "Duplicado de llaves domésticas y automotrices, apertura de cerraduras, candados y cerrojos.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bCERRAJERIA\b", r"\bCERRAJERO\b", r"\bLLAVES\b", r"\bDUPLICADO DE LLAVES\b", r"\bCANDADOS\b",
            r"\bCHAPAS\b"
        ]
    },
    {
        "id": "reparacion_calzado",
        "categoria_id": "CAT_OFICIOS_SERVICIOS",
        "nombre": "Reparación de Calzado y Artículos de Piel",
        "descripcion": "Taller artesanal de zapatero: cambio de tapas, suelas, costura de tenis, teñido y boleado.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bREPARACION DE CALZADO\b", r"\bZAPATERO\b", r"\bRENOVADORA DE CALZADO\b", r"\bCAMBIO DE TAPAS\b",
            r"\bSUELAS\b", r"\bBOLEADA?\b"
        ]
    },
    {
        "id": "carpinteria_ebanisteria",
        "categoria_id": "CAT_OFICIOS_SERVICIOS",
        "nombre": "Carpintería y Ebanistería",
        "descripcion": "Fabricación, reparación y barnizado de muebles de madera, puertas, closets y repisas.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bCARPINTERIA\b", r"\bCARPINTERO\b", r"\bEBANISTERIA\b", r"\bBARNIZ\b", r"\bBARNIZADO\b"
        ]
    },
    {
        "id": "herreria_soldadura",
        "categoria_id": "CAT_OFICIOS_SERVICIOS",
        "nombre": "Herrería, Soldadura y Pailería",
        "descripcion": "Estructuras de acero, puertas de fierro, zaguanes, protecciones de ventana y soldadura eléctrica.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bHERRERIA\b", r"\bHERRERO\b", r"\bSOLDADURA\b", r"\bPAILERIA\b", r"\bZAGUAN(ES)?\b",
            r"\bPROTECCIONES DE HERRERIA\b"
        ]
    },
    {
        "id": "taller_mecanico",
        "categoria_id": "CAT_OFICIOS_SERVICIOS",
        "nombre": "Taller Mecánico Automotriz, Motos y Refacciones",
        "descripcion": "Mantenimiento preventivo automotriz y motocicletas: afinación, frenos, clutch, hojalatería y refacciones.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bMECANICO\b", r"\bMECANICA\b", r"\bTALLER MECANICO\b", r"\bHOJALATERIA\b", r"\bHOJALATERIA Y PINTURA\b",
            r"\bAFINACION\b", r"\bFRENOS\b", r"\bREFACCIONARIA\b", r"\bAUTOMOTRIZ\b", r"\bTALLER AUTOMOTRIZ\b",
            r"\bTALLER DE MOTOS\b", r"\bMOTOS\b"
        ]
    },
    {
        "id": "vulcanizadora_llantas",
        "categoria_id": "CAT_OFICIOS_SERVICIOS",
        "nombre": "Vulcanizadora y Talachera",
        "descripcion": "Parchado de llantas de auto y moto, talachas, montaje y suministro de aire.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bVULCANIZADORA\b", r"\bTALACHERA\b", r"\bTALACHAS\b", r"\bPARCHADO DE LLANTAS\b",
            r"\bREPARACION DE LLANTAS\b"
        ]
    },
    {
        "id": "taller_bicicletas",
        "categoria_id": "CAT_OFICIOS_SERVICIOS",
        "nombre": "Taller y Refaccionaria de Bicicletas",
        "descripcion": "Reparación de ponchaduras de bici, ajuste de frenos y velocidades, refacciones para ciclismo.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bBICICLETAS?\b", r"\bTALLER DE BICICLETAS\b", r"\bREFACCIONES PARA BICICLETA\b",
            r"\bPONCHADURAS DE BICI\b"
        ]
    },
    {
        "id": "lavanderia_tintoreria",
        "categoria_id": "CAT_OFICIOS_SERVICIOS",
        "nombre": "Lavandería, Tintorería y Planchaduría",
        "descripcion": "Lavado por encargo y autoservicio por kilo, lavado en seco y servicio de planchaduría.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bLAVANDERIA\b", r"\bTINTORERIA\b", r"\bPLANCHADURIA\b", r"\bLAVADO POR KILO\b"
        ]
    },
    {
        "id": "reparacion_electrodomesticos",
        "categoria_id": "CAT_OFICIOS_SERVICIOS",
        "nombre": "Reparación de Electrodomésticos y Refrigeración",
        "descripcion": "Reparación de licuadoras, lavadoras, refrigeradores, microondas y motores eléctricos menores.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bREPARACION DE ELECTRODOMESTICOS\b", r"\bELECTRODOMESTICOS\b", r"\bLAVADORAS\b",
            r"\bREFRIGERADORES\b", r"\bREFRIGERACION\b"
        ]
    },
    {
        "id": "alquiladora_eventos",
        "categoria_id": "CAT_OFICIOS_SERVICIOS",
        "nombre": "Alquiladora de Mobiliario, Lonas y Eventos",
        "descripcion": "Renta de sillas, mesas, lonas, inflables, mantelería, vajilla y equipo para celebraciones populares.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bALQUILADORA\b", r"\bRENTA DE SILLAS\b", r"\bSILLAS Y MESAS\b", r"\bEVENTOS SOCIALES\b",
            r"\bBANQUETES\b", r"\bLONAS\b", r"\bINFLABLES\b"
        ]
    },
    {
        "id": "fotografia_video",
        "categoria_id": "CAT_OFICIOS_SERVICIOS",
        "nombre": "Estudio Fotográfico, Foto y Video",
        "descripcion": "Fotografía infantil, retratos para certificados, fotos de estudio para bodas y XV años, y video social.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": True, "tipo_mercado_cdmx": "servicios",
        "keywords": [
            r"\bFOTOGRAFIA\b", r"\bESTUDIO FOTOGRAFICO\b", r"\bFOTO Y VIDEO\b", r"\bFOTOGRAFO\b",
            r"\bPUBLICIDAD\b"
        ]
    },

    # --- CAT_BAZAR_CHACHARAS ---
    {
        "id": "chacharas_segunda_mano",
        "categoria_id": "CAT_BAZAR_CHACHARAS",
        "nombre": "Chácharas, Bazar y Segunda Mano",
        "descripcion": "Herramientas usadas, tiliches, piezas de reuso, cachivaches y artículos varios de segunda mano.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bCHACHARAS\b", r"\bBAZAR\b", r"\bSEGUNDA MANO\b", r"\bCOSAS USADAS\b", r"\bTILICHES\b",
            r"\bCACHIVACHES\b", r"\bARTICULOS USADOS\b"
        ]
    },
    {
        "id": "antiguedades_coleccionismo",
        "categoria_id": "CAT_BAZAR_CHACHARAS",
        "nombre": "Antigüedades, Coleccionables y Libros Usados",
        "descripcion": "Objetos antiguos, monedas, billetes, vinilos, libros usados y piezas de colección.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bANTIGUEDADES\b", r"\bANTIGUEDAD\b", r"\bCOLECCIONISMO\b", r"\bLIBROS USADOS\b",
            r"\bDISCOS DE VINIL\b", r"\bMONEDAS ANTIGUAS\b"
        ]
    },
    {
        "id": "arte_rotulacion",
        "categoria_id": "CAT_BAZAR_CHACHARAS",
        "nombre": "Arte, Pintura, Marcos y Rotulación Tradicional",
        "descripcion": "Pintura, escultura, enmarcado de fotos y cuadros, rótulos populares e imprenta serigráfica.",
        "canasta_basica": False, "mercomuna": False, "perecedero": False, "es_servicio": False, "tipo_mercado_cdmx": "complementario",
        "keywords": [
            r"\bARTE\b", r"\bPINTORES Y ESCULTORES\b", r"\bMARCOS PARA CUADROS\b", r"\bROTULACION\b",
            r"\bSERIGRAFIA\b", r"\bIMPRENTA\b"
        ]
    },
    {
        "id": "comercio_mixto_general",
        "categoria_id": "CAT_BAZAR_CHACHARAS",
        "nombre": "Comercio Mixto, Tradicional y Abasto General",
        "descripcion": "Puestos y locales con giros combinados no especializados, abasto semanal o comercio tradicional.",
        "canasta_basica": True, "mercomuna": True, "perecedero": True, "es_servicio": False, "tipo_mercado_cdmx": "mixto",
        "keywords": [
            r"\bCOMERCIO MIXTO\b", r"\bTRADICIONAL\b", r"\bMIXTO\b", r"\bABASTO\b", r"\bCOMIDA Y ABASTO\b",
            r"\bBASICOS Y COMPLEMENTARIOS\b", r"\bVARIOS\b", r"\bPASAJE COMERCIAL\b",
            r"^\s*COMERCIO\s*$", r"^\s*COMERCIAL\s*$", r"^\s*VENTAS?\s*$", r"^\s*COMERCIANTES?\s*$",
            r"^\s*PUESTO(\s+AMBULANTE)?\s*$", r"^\s*AMBULANTE\s*$", r"^\s*TIANGUIS\s*$", r"^\s*TALLER\s*$",
            r"^\s*SERVICIOS?\s*$", r"^\s*ACCESORIOS\s*$", r"^\s*VENTA\s+DE\s+PRODUCTOS\s*$"
        ]
    }
]

def export_catalog(output_dir="data/catalog"):
    """Exporta el catálogo a JSON y CSV."""
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. JSON
    cat_json = {
        "metadata": {
            "version": "1.0.0",
            "fecha": "2026-10-25",
            "titulo": "Catálogo Jerárquico de Giros Comerciales para el Comercio Popular y Barrial de la CDMX",
            "proyecto": "Chilangotón 2026 - Reto 1: Comercio Popular y Barrial",
            "total_categorias": len(CATEGORIAS),
            "total_subgiros": len(SUBGIROS)
        },
        "categorias": CATEGORIAS,
        "subgiros": [
            {k: v for k, v in sg.items() if k != "keywords"} | {"keywords_regex": sg["keywords"]}
            for sg in SUBGIROS
        ]
    }
    
    json_path = os.path.join(output_dir, "giros_catalogo.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cat_json, f, ensure_ascii=False, indent=2)
    print(f"JSON exportado en: {json_path}")
    
    # 2. CSV
    cat_map = {c["id"]: c["nombre"] for c in CATEGORIAS}
    csv_rows = []
    for sg in SUBGIROS:
        csv_rows.append({
            "id": sg["id"],
            "categoria_id": sg["categoria_id"],
            "categoria_nombre": cat_map.get(sg["categoria_id"], ""),
            "nombre": sg["nombre"],
            "descripcion": sg["descripcion"],
            "canasta_basica": sg["canasta_basica"],
            "mercomuna": sg["mercomuna"],
            "perecedero": sg["perecedero"],
            "es_servicio": sg["es_servicio"],
            "tipo_mercado_cdmx": sg["tipo_mercado_cdmx"],
            "keywords_total": len(sg["keywords"])
        })
    df_cat = pd.DataFrame(csv_rows)
    csv_path = os.path.join(output_dir, "giros_catalogo.csv")
    df_cat.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"CSV exportado en: {csv_path}")

if __name__ == "__main__":
    export_catalog()
