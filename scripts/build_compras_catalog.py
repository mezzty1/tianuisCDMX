#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compilador del Catálogo y Vocabulario Jerárquico de Compras Populares de la CDMX
Chilangotón 2026 - Reto 1: Comercio Popular y Barrial

Genera el índice de búsqueda predictiva NIVEL MICRO (productos de consumo popular),
su mapeo a NIVEL MESO (67 subgiros) y NIVEL MACRO (9 macro-categorías + canasta básica / Mercomuna).
Enriquece también el Directorio Unificado de Comercio Popular.
"""

import os
import json
import csv
import pandas as pd
from typing import Dict, List, Any

# Cargar catálogo de giros
CATALOG_PATH = 'data/catalog/giros_catalogo.json'
with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
    GIROS_CATALOG = json.load(f)

CATEGORIAS = {c['id']: c for c in GIROS_CATALOG['categorias']}
SUBGIROS = {s['id']: s for s in GIROS_CATALOG['subgiros']}

# Mapeo exhaustivo de términos populares de compra a subgiros
VOCABULARIO_RAW = [
    # --- CAT_ALIM_FRESCOS ---
    # recauderia_fruteria
    {"termino": "Jitomate", "subgiro": "recauderia_fruteria", "sinonimos": ["jitomates", "tomate rojo", "jitomate saladet"], "peso": 100},
    {"termino": "Aguacate", "subgiro": "recauderia_fruteria", "sinonimos": ["aguacates", "aguacate hass"], "peso": 100},
    {"termino": "Cebolla", "subgiro": "recauderia_fruteria", "sinonimos": ["cebollas", "cebolla blanca", "cebolla morada"], "peso": 95},
    {"termino": "Limón", "subgiro": "recauderia_fruteria", "sinonimos": ["limones", "limon con semilla", "limon colima"], "peso": 95},
    {"termino": "Papas", "subgiro": "recauderia_fruteria", "sinonimos": ["papa", "papa blanca", "papas cambray"], "peso": 90},
    {"termino": "Nopales", "subgiro": "recauderia_fruteria", "sinonimos": ["nopal", "nopalitos", "nopales limpios"], "peso": 90},
    {"termino": "Plátano", "subgiro": "recauderia_fruteria", "sinonimos": ["platanos", "platano tabasco", "platano macho", "platano dominico"], "peso": 90},
    {"termino": "Manzana", "subgiro": "recauderia_fruteria", "sinonimos": ["manzanas", "manzana gala", "manzana red", "manzana golden"], "peso": 85},
    {"termino": "Naranja", "subgiro": "recauderia_fruteria", "sinonimos": ["naranjas", "naranja para jugo", "naranja valencia"], "peso": 85},
    {"termino": "Papaya", "subgiro": "recauderia_fruteria", "sinonimos": ["papayas", "papaya maradol"], "peso": 80},
    {"termino": "Piña", "subgiro": "recauderia_fruteria", "sinonimos": ["piñas", "pina miel", "pina esmeralda"], "peso": 80},
    {"termino": "Mango", "subgiro": "recauderia_fruteria", "sinonimos": ["mangos", "mango manila", "mango ataulfo", "mango petacon"], "peso": 80},
    {"termino": "Zanahorias", "subgiro": "recauderia_fruteria", "sinonimos": ["zanahoria"], "peso": 80},
    {"termino": "Calabacitas", "subgiro": "recauderia_fruteria", "sinonimos": ["calabacita", "calabaza italiana"], "peso": 80},
    {"termino": "Lechuga", "subgiro": "recauderia_fruteria", "sinonimos": ["lechugas", "lechuga orejona", "lechuga romana", "lechuga italiana"], "peso": 80},
    {"termino": "Cilantro y Perejil", "subgiro": "recauderia_fruteria", "sinonimos": ["cilantro", "perejil", "epazote", "hierbabuena"], "peso": 80},
    {"termino": "Chiles Verdes", "subgiro": "recauderia_fruteria", "sinonimos": ["chile serrano", "chile jalapeño", "chile poblano", "chile cuaresmeño", "chile habanero"], "peso": 85},
    {"termino": "Tomate Verde", "subgiro": "recauderia_fruteria", "sinonimos": ["tomates", "tomate con cáscara", "tomatillo"], "peso": 85},
    {"termino": "Fresas", "subgiro": "recauderia_fruteria", "sinonimos": ["fresa", "fresas frescas"], "peso": 75},
    {"termino": "Sandía y Melón", "subgiro": "recauderia_fruteria", "sinonimos": ["sandia", "melon", "melon chino"], "peso": 75},
    {"termino": "Chayotes", "subgiro": "recauderia_fruteria", "sinonimos": ["chayote", "chayote sin espina"], "peso": 75},
    {"termino": "Ajo", "subgiro": "recauderia_fruteria", "sinonimos": ["ajos", "cabeza de ajo"], "peso": 75},

    # carniceria
    {"termino": "Bistec de Res", "subgiro": "carniceria", "sinonimos": ["bistec", "bisteces", "carne de res", "filete de res", "pulpa"], "peso": 95},
    {"termino": "Carne Molida", "subgiro": "carniceria", "sinonimos": ["molida de res", "molida mixta", "molida de sirloin"], "peso": 90},
    {"termino": "Cecina", "subgiro": "carniceria", "sinonimos": ["cecina de yecapixtla", "cecina enchilada"], "peso": 90},
    {"termino": "Carne de Cerdo", "subgiro": "carniceria", "sinonimos": ["puerco", "carne de puerco", "lomo de cerdo", "pierna de cerdo"], "peso": 85},
    {"termino": "Chuletas", "subgiro": "carniceria", "sinonimos": ["chuleta ahumada", "chuleta natural", "chuletas de cerdo"], "peso": 85},
    {"termino": "Costilla de Res / Cerdo", "subgiro": "carniceria", "sinonimos": ["costilla", "costillitas", "costilla para asar"], "peso": 85},
    {"termino": "Longaniza y Chorizo", "subgiro": "carniceria", "sinonimos": ["longaniza", "chorizo verde", "chorizo rojo", "chorizo de toluca"], "peso": 85},
    {"termino": "Suadero Crudo", "subgiro": "carniceria", "sinonimos": ["suadero", "trozo de suadero"], "peso": 80},
    {"termino": "Chicharrón de Cerdo", "subgiro": "carniceria", "sinonimos": ["chicharron", "chicharron crujiente", "chicharron de pella"], "peso": 85},
    {"termino": "Tocino", "subgiro": "carniceria", "sinonimos": ["tocino ahumado", "tocino en tiras"], "peso": 80},

    # polleria
    {"termino": "Pechuga de Pollo", "subgiro": "polleria", "sinonimos": ["pechuga", "pechugas", "pechuga aplanada", "pechuga deshuesada", "milanesa de pollo"], "peso": 100},
    {"termino": "Pollo Entero", "subgiro": "polleria", "sinonimos": ["pollo", "pollos", "pollo en canal", "medio pollo"], "peso": 95},
    {"termino": "Pierna y Muslo", "subgiro": "polleria", "sinonimos": ["piernas de pollo", "muslos de pollo"], "peso": 90},
    {"termino": "Alitas de Pollo", "subgiro": "polleria", "sinonimos": ["alitas crudas", "alas de pollo"], "peso": 85},
    {"termino": "Retazo de Pollo", "subgiro": "polleria", "sinonimos": ["retazo", "huacal", "rabadilla", "cuello"], "peso": 80},
    {"termino": "Pollo Rostizado", "subgiro": "polleria", "sinonimos": ["rosticería", "pollo asado", "pollo frito", "pollo con papas"], "peso": 85},
    {"termino": "Huevo Blanco y Rojo", "subgiro": "polleria", "sinonimos": ["huevo", "huevos", "kilo de huevo", "cono de huevo", "blanquillos"], "peso": 100},

    # pescaderia
    {"termino": "Pescado Fresco", "subgiro": "pescaderia", "sinonimos": ["pescado", "pescados", "pescaderia", "pescado entero"], "peso": 95},
    {"termino": "Mojarra", "subgiro": "pescaderia", "sinonimos": ["mojarras", "mojarra tilapia", "mojarra para freir"], "peso": 95},
    {"termino": "Filete de Pescado", "subgiro": "pescaderia", "sinonimos": ["filete de mojarra", "filete de basa", "filete blanco"], "peso": 90},
    {"termino": "Camarones", "subgiro": "pescaderia", "sinonimos": ["camaron", "camarones con cabeza", "camaron pacotilla", "camaron cristal"], "peso": 95},
    {"termino": "Huachinango", "subgiro": "pescaderia", "sinonimos": ["huachinango fresco", "pargo"], "peso": 85},
    {"termino": "Pulpo y Calamar", "subgiro": "pescaderia", "sinonimos": ["pulpo", "calamar", "tentaculos"], "peso": 80},
    {"termino": "Mariscos Mixtos", "subgiro": "pescaderia", "sinonimos": ["sopa de mariscos", "jaiba", "ostiones", "almejas"], "peso": 85},

    # cremeria_lacteos
    {"termino": "Queso Oaxaca", "subgiro": "cremeria_lacteos", "sinonimos": ["queso de hebra", "quesillo", "queso oaxaqueño"], "peso": 100},
    {"termino": "Queso Panela", "subgiro": "cremeria_lacteos", "sinonimos": ["panela", "queso canasto"], "peso": 95},
    {"termino": "Queso Manchego", "subgiro": "cremeria_lacteos", "sinonimos": ["manchego", "queso para fundir"], "peso": 90},
    {"termino": "Crema de Rancho", "subgiro": "cremeria_lacteos", "sinonimos": ["crema", "crema ácida", "crema fresca", "crema de vaca"], "peso": 95},
    {"termino": "Leche Entera", "subgiro": "cremeria_lacteos", "sinonimos": ["leche", "litro de leche", "leche bronca", "leche pasteurizada"], "peso": 95},
    {"termino": "Jamón de Pierna / Pavo", "subgiro": "cremeria_lacteos", "sinonimos": ["jamon", "jamon virginia", "salchichoneria"], "peso": 90},
    {"termino": "Salchichas", "subgiro": "cremeria_lacteos", "sinonimos": ["salchicha de pavo", "salchicha vienesa", "salchicha para hotdog"], "peso": 85},
    {"termino": "Mantequilla", "subgiro": "cremeria_lacteos", "sinonimos": ["mantequilla de rancho", "margarina"], "peso": 80},
    {"termino": "Requesón", "subgiro": "cremeria_lacteos", "sinonimos": ["requeson fresco", "ricotta"], "peso": 80},

    # --- CAT_ABARROTES_CANASTA ---
    # tienda_abarrotes
    {"termino": "Frijol Negro y Pinto", "subgiro": "tienda_abarrotes", "sinonimos": ["frijol", "frijoles", "frijol flor de mayo", "frijol peruano"], "peso": 100},
    {"termino": "Arroz Blanco", "subgiro": "tienda_abarrotes", "sinonimos": ["arroz", "arroz super extra", "kilo de arroz"], "peso": 100},
    {"termino": "Aceite Comestible", "subgiro": "tienda_abarrotes", "sinonimos": ["aceite", "aceite 1-2-3", "aceite nutrioli", "aceite vegetal"], "peso": 100},
    {"termino": "Azúcar", "subgiro": "tienda_abarrotes", "sinonimos": ["azucar estandar", "azucar morena", "azucar refinada"], "peso": 95},
    {"termino": "Sal de Mesa", "subgiro": "tienda_abarrotes", "sinonimos": ["sal fina", "sal de grano", "sal la fina"], "peso": 90},
    {"termino": "Atún en Lata", "subgiro": "tienda_abarrotes", "sinonimos": ["atun", "lata de atun", "atun dolores", "atun en agua", "atun en aceite"], "peso": 90},
    {"termino": "Pastas para Sopa", "subgiro": "tienda_abarrotes", "sinonimos": ["sopas de pasta", "fideo", "espagueti", "letritas", "coditos"], "peso": 90},
    {"termino": "Café Soluble y Molido", "subgiro": "tienda_abarrotes", "sinonimos": ["cafe", "nescafe", "cafe legal", "frasco de cafe"], "peso": 85},
    {"termino": "Mayonesa y Cátsup", "subgiro": "tienda_abarrotes", "sinonimos": ["mayonesa mc cormick", "catsup", "mostaza"], "peso": 80},
    {"termino": "Papel Higiénico", "subgiro": "tienda_abarrotes", "sinonimos": ["papel de baño", "rollo de papel", "servilletas", "kleenex"], "peso": 95},
    {"termino": "Jabón de Lavar", "subgiro": "tienda_abarrotes", "sinonimos": ["jabon zote", "zote rosa", "jabon foca", "detergente roma"], "peso": 90},

    # tortilleria_molino
    {"termino": "Tortillas de Maíz", "subgiro": "tortilleria_molino", "sinonimos": ["tortilla", "tortillas", "kilo de tortillas", "tortillas calientes"], "peso": 100},
    {"termino": "Masa de Nixtamal", "subgiro": "tortilleria_molino", "sinonimos": ["masa", "masa para tamales", "masa para tortillas", "nixtamal"], "peso": 95},
    {"termino": "Totopos y Tostadas", "subgiro": "tortilleria_molino", "sinonimos": ["totopos", "tostadas de maiz", "tostadas raspadas"], "peso": 90},
    {"termino": "Tortillas de Harina", "subgiro": "tortilleria_molino", "sinonimos": ["tortilla de harina", "tortillinas"], "peso": 85},

    # panaderia_expendio
    {"termino": "Bolillo y Telera", "subgiro": "panaderia_expendio", "sinonimos": ["bolillo", "bolillos", "telera", "teleras", "pan blanco"], "peso": 100},
    {"termino": "Pan de Dulce", "subgiro": "panaderia_expendio", "sinonimos": ["pan dulce", "panaderia", "pan tradicional"], "peso": 95},
    {"termino": "Conchas", "subgiro": "panaderia_expendio", "sinonimos": ["concha de vainilla", "concha de chocolate"], "peso": 90},
    {"termino": "Cuernitos y Orejas", "subgiro": "panaderia_expendio", "sinonimos": ["cuernito", "oreja", "bisquet", "dona"], "peso": 85},
    {"termino": "Cocoles y Pan de Pueblo", "subgiro": "panaderia_expendio", "sinonimos": ["cocol", "cocoles con anis", "pan de feria", "pan de muerto", "rosca de reyes"], "peso": 85},

    # semillas_chiles_granos
    {"termino": "Chiles Secos (Guajillo, Ancho, Pasilla)", "subgiro": "semillas_chiles_granos", "sinonimos": ["chile guajillo", "chile ancho", "chile pasilla", "chile chipotle seco", "chile cascabel", "chile de arbol"], "peso": 95},
    {"termino": "Mole Poblano y Almendrado", "subgiro": "semillas_chiles_granos", "sinonimos": ["mole", "pasta de mole", "mole verde", "pipian", "adobo"], "peso": 95},
    {"termino": "Semillas y Frutos Secos", "subgiro": "semillas_chiles_granos", "sinonimos": ["pepitas", "nuez", "almendras", "cacahuates crudos", "ajonjoli", "semillas de girasol"], "peso": 90},
    {"termino": "Especias y Hierbas de Olor", "subgiro": "semillas_chiles_granos", "sinonimos": ["canela en raja", "pimienta gorda", "comino", "oregano seco", "laurel", "clavo"], "peso": 85},
    {"termino": "Granos y Cereales (Avena, Chía, Lentejas)", "subgiro": "semillas_chiles_granos", "sinonimos": ["avena a granel", "chia", "lentejas a granel", "garbanzo", "haba seca"], "peso": 90},

    # dulceria_botanas
    {"termino": "Dulces y Confitería", "subgiro": "dulceria_botanas", "sinonimos": ["dulces", "dulceria", "paletas", "chocolates", "gomitas", "mazapan"], "peso": 85},
    {"termino": "Botanas y Frituras", "subgiro": "dulceria_botanas", "sinonimos": ["papas fritas", "cacahuates japoneses", "chicharrones preparados", "platanitos"], "peso": 80},

    # purificadora_agua
    {"termino": "Garrafón de Agua Purificada", "subgiro": "purificadora_agua", "sinonimos": ["garrafon", "relleno de garrafon", "agua de garrafon", "purificadora"], "peso": 95},
    {"termino": "Bolsa de Hielo", "subgiro": "purificadora_agua", "sinonimos": ["hielo", "cubos de hielo", "barra de hielo"], "peso": 85},

    # --- CAT_COMIDA_PREPARADA ---
    # taqueria
    {"termino": "Tacos al Pastor", "subgiro": "taqueria", "sinonimos": ["pastor", "taco al pastor", "tacos de trompo", "gringa de pastor"], "peso": 100},
    {"termino": "Tacos de Suadero", "subgiro": "taqueria", "sinonimos": ["suadero", "taco de suadero"], "peso": 100},
    {"termino": "Tacos de Carnitas", "subgiro": "taqueria", "sinonimos": ["carnitas", "maciza", "surtida", "costilla carnitas", "cuerito"], "peso": 100},
    {"termino": "Barbacoa de Borrego", "subgiro": "taqueria", "sinonimos": ["barbacoa", "tacos de barbacoa", "consome de barbacoa", "pancita"], "peso": 100},
    {"termino": "Tacos de Cabeza y Tripa", "subgiro": "taqueria", "sinonimos": ["tripa dorada", "tacos de tripa", "cabeza", "lengua", "sesos"], "peso": 90},
    {"termino": "Birria de Res", "subgiro": "taqueria", "sinonimos": ["birria", "quesabirrias", "consome de birria"], "peso": 95},

    # antojitos_mexicanos
    {"termino": "Quesadillas de Comal", "subgiro": "antojitos_mexicanos", "sinonimos": ["quesadillas", "quesadilla de queso", "quesadilla de tinga", "quesadilla de huitlacoche", "quesadilla de flor"], "peso": 100},
    {"termino": "Gorditas de Chicharrón", "subgiro": "antojitos_mexicanos", "sinonimos": ["gorditas", "gordita frita", "gordita de chicharron prensado"], "peso": 95},
    {"termino": "Sopes y Huaraches", "subgiro": "antojitos_mexicanos", "sinonimos": ["sopes", "huaraches", "huarache con bistec", "tlacoyos", "tlacoyo de frijol"], "peso": 95},
    {"termino": "Pambazos", "subgiro": "antojitos_mexicanos", "sinonimos": ["pambazo", "pambazos de papa con chorizo"], "peso": 90},
    {"termino": "Flautas y Tostadas", "subgiro": "antojitos_mexicanos", "sinonimos": ["flautas de pollo", "flautas ahogadas", "tostadas de tinga", "tostadas de pata"], "peso": 90},
    {"termino": "Chilaquiles y Enchiladas", "subgiro": "antojitos_mexicanos", "sinonimos": ["chilaquiles verdes", "chilaquiles con huevo", "enchiladas suizas"], "peso": 90},

    # tamales_atole
    {"termino": "Tamales (Verde, Mole, Rajas, Dulce)", "subgiro": "tamales_atole", "sinonimos": ["tamal", "tamales", "tamal verde", "tamal de mole", "tamal oaxaqueño"], "peso": 100},
    {"termino": "Guajolotas (Torta de Tamal)", "subgiro": "tamales_atole", "sinonimos": ["guajolota", "torta de tamal"], "peso": 95},
    {"termino": "Atole Caliente y Champurrado", "subgiro": "tamales_atole", "sinonimos": ["atole", "champurrado", "atole de arroz", "atole de fresa", "atole de chocolate"], "peso": 95},

    # cocina_economica_fonda
    {"termino": "Comida Corrida (Fonda)", "subgiro": "cocina_economica_fonda", "sinonimos": ["comida corrida", "menu del dia", "fonda", "cocina economica", "guisados"], "peso": 100},
    {"termino": "Milanesa con Papas", "subgiro": "cocina_economica_fonda", "sinonimos": ["milanesa de pollo empanizada", "milanesa de res"], "peso": 90},
    {"termino": "Sopa y Consomé", "subgiro": "cocina_economica_fonda", "sinonimos": ["sopa de fideo", "arroz con huevo", "consome con pollo"], "peso": 85},

    # torteria
    {"termino": "Tortas Calientes", "subgiro": "torteria", "sinonimos": ["torta", "tortas", "torteria", "torta de milanesa", "torta cubana", "torta de pierna"], "peso": 95},

    # elotes_esquites_botaneros
    {"termino": "Esquites con Tuétano y Mayonesa", "subgiro": "elotes_esquites_botaneros", "sinonimos": ["esquites", "esquite", "vaso de esquites", "esquites con chile"], "peso": 95},
    {"termino": "Elotes Hervidos y Asados", "subgiro": "elotes_esquites_botaneros", "sinonimos": ["elote", "elotes", "elote con mayonesa y queso"], "peso": 95},

    # cafeteria_fuente_sodas
    {"termino": "Jugos Naturales y Licuados", "subgiro": "cafeteria_fuente_sodas", "sinonimos": ["jugo verde", "jugo de naranja", "licuado de platano", "licuados", "jugueria"], "peso": 90},
    {"termino": "Café de Olla", "subgiro": "cafeteria_fuente_sodas", "sinonimos": ["cafe de olla", "cafeteria"], "peso": 85},

    # paleteria_helados
    {"termino": "Aguas Frescas (Horchata, Jamaica)", "subgiro": "paleteria_helados", "sinonimos": ["aguas frescas", "agua de horchata", "agua de jamaica", "agua de limon con chia"], "peso": 95},
    {"termino": "Helados y Paletas Artesanales", "subgiro": "paleteria_helados", "sinonimos": ["helado", "paleta de hielo", "nieve artesanal"], "peso": 85},

    # --- CAT_ROPA_CALZADO_TEXTIL ---
    # venta_ropa
    {"termino": "Ropa Deportiva y Pants", "subgiro": "venta_ropa", "sinonimos": ["ropa deportiva", "pants", "sudaderas", "playeras deportivas", "leggins"], "peso": 95},
    {"termino": "Pantalones de Mezclilla", "subgiro": "venta_ropa", "sinonimos": ["pantalones", "jeans", "mezclilla", "pantalon para dama", "pantalon para caballero"], "peso": 95},
    {"termino": "Playeras y Blusas", "subgiro": "venta_ropa", "sinonimos": ["playeras", "camisas", "blusas", "vestidos"], "peso": 90},
    {"termino": "Chamarras y Suéteres", "subgiro": "venta_ropa", "sinonimos": ["chamarra", "sueter", "chaleco", "abrigos"], "peso": 85},

    # zapateria_calzado
    {"termino": "Tenis Deportivos y Casuales", "subgiro": "zapateria_calzado", "sinonimos": ["tenis", "sneakers", "calzado deportivo", "tenis comodos"], "peso": 100},
    {"termino": "Zapatos Escolares y de Vestir", "subgiro": "zapateria_calzado", "sinonimos": ["zapatos", "calzado escolar", "zapateria", "zapatos de piel"], "peso": 95},
    {"termino": "Sandalias y Botas", "subgiro": "zapateria_calzado", "sinonimos": ["sandalias", "chanclas", "botas", "botas de trabajo"], "peso": 85},

    # ropa_paca_segunda
    {"termino": "Ropa de Paca Americana", "subgiro": "ropa_paca_segunda", "sinonimos": ["ropa de paca", "paca", "ropa americana", "ropa usada de marca", "vintage"], "peso": 95},

    # lenceria_boneteria
    {"termino": "Calcetines y Ropa Interior", "subgiro": "lenceria_boneteria", "sinonimos": ["calcetines", "calcetas", "tines", "calzones", "boxers", "brasieres", "boneteria"], "peso": 90},

    # telas_blancos
    {"termino": "Cobijas y Cobertores", "subgiro": "telas_blancos", "sinonimos": ["cobijas", "cobertores", "cobija san marcos", "edredones"], "peso": 90},
    {"termino": "Sábanas y Toallas", "subgiro": "telas_blancos", "sinonimos": ["sabanas", "toallas de baño", "manteles", "cortinas"], "peso": 85},

    # bolsos_mochilas
    {"termino": "Mochilas y Bolsas", "subgiro": "bolsos_mochilas", "sinonimos": ["mochilas", "mochila escolar", "bolsas de mano", "carteras", "cinturones"], "peso": 90},

    # --- CAT_HOGAR_FERRETERIA ---
    # ferreteria_tlapaleria
    {"termino": "Tornillos, Clavos y Taquetes", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["tornillos", "clavos", "taquetes", "tuercas", "rondanas"], "peso": 95},
    {"termino": "Herramientas de Mano", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["martillo", "desarmador", "pinzas", "llaves", "segueta", "taladro"], "peso": 90},
    {"termino": "Focos y Material Eléctrico", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["focos", "foco led", "cables", "contactos", "clavijas", "cinta de aislar"], "peso": 90},
    {"termino": "Pintura y Brochas", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["pintura", "brochas", "rodillos", "thiner", "sellador"], "peso": 85},

    # jarcieria_productos_limpieza
    {"termino": "Cloro y Desinfectantes a Granel", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["cloro", "fabuloso", "pino", "detergente liquido", "quimicos de limpieza"], "peso": 90},
    {"termino": "Escobas y Trapeadores", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["escoba", "trapeador", "jalador", "jergas", "franelas", "jarcieria"], "peso": 90},

    # plasticos_enseres_hogar
    {"termino": "Tuppers y Artículos de Plástico", "subgiro": "plasticos_enseres_hogar", "sinonimos": ["tuppers", "recipientes", "botes", "cubetas", "trastes de plastico"], "peso": 90},
    {"termino": "Sartenes y Ollas", "subgiro": "plasticos_enseres_hogar", "sinonimos": ["sartenes", "ollas", "vaporera", "cucharas de madera", "enseres de cocina"], "peso": 85},

    # floreria_plantas
    {"termino": "Flores Frescas y Ramos", "subgiro": "floreria_plantas", "sinonimos": ["flores", "rosas", "girasoles", "ramos de flores", "floreria"], "peso": 90},
    {"termino": "Plantas de Ornato y Macetas", "subgiro": "floreria_plantas", "sinonimos": ["plantas", "macetas", "tierra para plantas", "suculentas", "cactus"], "peso": 85},

    # mascotas_alimento
    {"termino": "Alimento para Perro y Gato (Croquetas)", "subgiro": "mascotas_alimento", "sinonimos": ["croquetas", "alimento para perro", "comida de gato", "croquetas a granel"], "peso": 90},

    # --- CAT_SALUD_BELLEZA ---
    # farmacia_botica
    {"termino": "Medicamentos Genéricos", "subgiro": "farmacia_botica", "sinonimos": ["farmacia", "medicamentos", "pastillas", "paracetamol", "ibuprofeno", "aspirinas"], "peso": 95},
    {"termino": "Alcohol, Gasas y Botiquín", "subgiro": "farmacia_botica", "sinonimos": ["alcohol", "gasas", "curitas", "vendas", "termometro"], "peso": 85},

    # herbolaria_esoterismo
    {"termino": "Plantas Medicinales y Tés", "subgiro": "herbolaria_esoterismo", "sinonimos": ["plantas medicinales", "herbolaria", "te de manzanilla", "arnica", "hierbas"], "peso": 90},
    {"termino": "Veladoras e Inciensos", "subgiro": "herbolaria_esoterismo", "sinonimos": ["veladoras", "incienso", "copal", "sahumerio"], "peso": 85},

    # estetica_peluqueria / barberia
    {"termino": "Corte de Cabello y Tinte", "subgiro": "estetica_peluqueria", "sinonimos": ["corte de cabello", "estetica", "peluqueria", "tinte", "despunte"], "peso": 90},
    {"termino": "Barbería y Fade", "subgiro": "barberia", "sinonimos": ["barberia", "fade", "perfilado de barba", "corte caballero"], "peso": 85},

    # unas_pestanas_cosmetologia
    {"termino": "Uñas Acrílicas y Gelish", "subgiro": "unas_pestanas_cosmetologia", "sinonimos": ["uñas", "gelish", "uñas acrilicas", "manicure", "pestañas"], "peso": 90},

    # cosmeticos_perfumeria
    {"termino": "Maquillaje y Cosméticos", "subgiro": "cosmeticos_perfumeria", "sinonimos": ["cosmeticos", "maquillaje", "labiales", "rimel", "perfumes"], "peso": 85},

    # optica_lentes
    {"termino": "Lentes Graduados y Armazones", "subgiro": "optica_lentes", "sinonimos": ["lentes", "optica", "armazones", "examen de la vista"], "peso": 85},

    # --- CAT_PAPELERIA_TECNOLOGIA ---
    # papeleria_copias
    {"termino": "Útiles Escolares y Cuadernos", "subgiro": "papeleria_copias", "sinonimos": ["utiles escolares", "cuadernos", "libretas", "lapices", "plumas", "colores"], "peso": 100},
    {"termino": "Copias e Impresiones", "subgiro": "papeleria_copias", "sinonimos": ["copias", "impresiones", "engargolados", "enmicados", "papeleria"], "peso": 95},

    # reparacion_celulares
    {"termino": "Reparación de Celulares y Pantallas", "subgiro": "reparacion_celulares", "sinonimos": ["reparacion de celulares", "cambio de pantalla", "centro de carga", "bateria celular"], "peso": 95},
    {"termino": "Fundas, Micas y Cargadores", "subgiro": "reparacion_celulares", "sinonimos": ["fundas celular", "micas", "cargador", "cables usb", "audifonos bluetooth"], "peso": 90},

    # ciber_internet_computo
    {"termino": "Internet y Trámites (CURP, RFC)", "subgiro": "ciber_internet_computo", "sinonimos": ["ciber", "internet", "impresion curp", "tramites", "escaneo"], "peso": 85},

    # jugueteria_novedades
    {"termino": "Juguetes y Novedades", "subgiro": "jugueteria_novedades", "sinonimos": ["juguetes", "carritos", "muñecas", "peluches", "juegos de mesa"], "peso": 85},

    # regalos_bisuteria
    {"termino": "Aretes, Cadenas y Bisutería", "subgiro": "regalos_bisuteria", "sinonimos": ["bisuteria", "aretes", "collares", "pulseras", "regalos", "acero inoxidable"], "peso": 85},

    # artesanias_manualidades
    {"termino": "Mercería y Manualidades", "subgiro": "artesanias_manualidades", "sinonimos": ["merceria", "hilos", "estambre", "fieltro", "listones", "manualidades"], "peso": 85},

    # --- CAT_OFICIOS_SERVICIOS ---
    # reparacion_calzado
    {"termino": "Reparación de Calzado y Suelas", "subgiro": "reparacion_calzado", "sinonimos": ["reparacion de calzado", "zapatero", "cambio de suela", "boleada", "costura de tenis"], "peso": 95},

    # cerrajeria
    {"termino": "Cerrajería y Duplicado de Llaves", "subgiro": "cerrajeria", "sinonimos": ["cerrajeria", "llaves", "duplicado de llaves", "apertura de chapas", "candados"], "peso": 95},

    # taller_costura_sastreria
    {"termino": "Ajuste de Ropa y Bastillas", "subgiro": "taller_costura_sastreria", "sinonimos": ["costura", "sastreria", "bastillas", "cambio de cierre", "ajuste de pantalon"], "peso": 90},

    # taller_bicicletas
    {"termino": "Reparación y Refacciones de Bicicletas", "subgiro": "taller_bicicletas", "sinonimos": ["taller de bicicletas", "bici", "parchado de llanta bici", "frenos bici"], "peso": 85},

    # reparacion_electrodomesticos
    {"termino": "Reparación de Licuadoras y Hornos", "subgiro": "reparacion_electrodomesticos", "sinonimos": ["reparacion de electrodomesticos", "cople licuadora", "reparacion de planchas", "microondas"], "peso": 85},

    # lavanderia_tintoreria
    {"termino": "Lavandería y Tintorería por Kilo", "subgiro": "lavanderia_tintoreria", "sinonimos": ["lavanderia", "tintoreria", "lavado de ropa", "planchaduria"], "peso": 80},

    # vulcanizadora_llantas
    {"termino": "Vulcanizadora y Talacha", "subgiro": "vulcanizadora_llantas", "sinonimos": ["vulcanizadora", "talacha", "parche de llanta", "inflado de llantas"], "peso": 80},

    # --- CAT_BAZAR_CHACHARAS ---
    # chacharas_segunda_mano
    {"termino": "Chácharas de Tianguis y Segunda Mano", "subgiro": "chacharas_segunda_mano", "sinonimos": ["chacharas", "chachara", "segunda mano", "bazar", "usados", "baratijas"], "peso": 95},

    # antiguedades_coleccionismo
    {"termino": "Libros Usados y Antigüedades", "subgiro": "antiguedades_coleccionismo", "sinonimos": ["libros usados", "antigüedades", "discos de vinilo", "coleccionables", "revistas"], "peso": 85},

    # comercio_mixto_general
    {"termino": "Puestos Mixtos de Tianguis", "subgiro": "comercio_mixto_general", "sinonimos": ["varios", "puesto mixto", "mercancia surtida", "abasto general"], "peso": 80}
]

def build_search_vocabulary() -> List[Dict[str, Any]]:
    """Construye el vocabulario estructurado con metadata completa para frontend."""
    items = []
    for raw in VOCABULARIO_RAW:
        sg_id = raw['subgiro']
        sg = SUBGIROS.get(sg_id, {})
        cat_id = sg.get('categoria_id', 'CAT_BAZAR_CHACHARAS')
        cat = CATEGORIAS.get(cat_id, {})

        search_tokens = [raw['termino'].lower()]
        for s in raw.get('sinonimos', []):
            search_tokens.append(s.lower())
        search_tokens.append(sg.get('nombre', '').lower())
        search_tokens.append(cat.get('nombre', '').lower())

        item = {
            "id": f"VOC-{len(items)+1:03d}",
            "termino": raw['termino'],
            "subgiro_id": sg_id,
            "subgiro_nombre": sg.get('nombre', ''),
            "categoria_id": cat_id,
            "categoria_nombre": cat.get('nombre', ''),
            "categoria_icono": cat.get('icono', '🏪'),
            "canasta_basica": sg.get('canasta_basica', False),
            "mercomuna": sg.get('mercomuna', False),
            "sinonimos": raw.get('sinonimos', []),
            "peso": raw.get('peso', 50),
            "tokens_busqueda": list(dict.fromkeys(search_tokens))
        }
        items.append(item)
    return items

def classify_space(space_type: str, raw_giro: str, nombre: str = "") -> Dict[str, Any]:
    """
    Asigna categorías y subgiros estructurados a un espacio comercial (Mercado, Tianguis, MSR, Concentración)
    según su tipología institucional de la CDMX y especialización.
    """
    norm_giro = (raw_giro or '').upper()
    norm_nom = (nombre or '').upper()

    # Mercados Sobre Ruedas (MSR): 100% Abasto Popular Canasta Básica
    if space_type == 'Mercado Sobre Ruedas':
        return {
            'categorias': ['CAT_ALIM_FRESCOS', 'CAT_ABARROTES_CANASTA', 'CAT_COMIDA_PREPARADA'],
            'subgiros': [
                'recauderia_fruteria', 'carniceria', 'polleria', 'pescaderia', 'cremeria_lacteos',
                'tienda_abarrotes', 'tortilleria_molino', 'panaderia_expendio', 'semillas_chiles_granos',
                'antojitos_mexicanos', 'cafeteria_fuente_sodas'
            ],
            'canasta_basica': True,
            'mercomuna': True,
            'popular_tags': ['jitomate', 'aguacate', 'pollo', 'carne', 'huevo', 'tortillas', 'frutas', 'verduras', 'lacteos']
        }

    # Tianguis Barriales: Gran abasto integral y diverso
    if space_type == 'Tianguis':
        return {
            'categorias': [
                'CAT_ALIM_FRESCOS', 'CAT_ABARROTES_CANASTA', 'CAT_COMIDA_PREPARADA',
                'CAT_ROPA_CALZADO_TEXTIL', 'CAT_HOGAR_FERRETERIA', 'CAT_BAZAR_CHACHARAS',
                'CAT_SALUD_BELLEZA', 'CAT_PAPELERIA_TECNOLOGIA'
            ],
            'subgiros': [
                'recauderia_fruteria', 'carniceria', 'polleria', 'pescaderia', 'cremeria_lacteos',
                'tienda_abarrotes', 'semillas_chiles_granos', 'panaderia_expendio', 'dulceria_botanas',
                'taqueria', 'antojitos_mexicanos', 'tamales_atole', 'elotes_esquites_botaneros',
                'venta_ropa', 'zapateria_calzado', 'ropa_paca_segunda', 'lenceria_boneteria', 'bolsos_mochilas',
                'chacharas_segunda_mano', 'comercio_mixto_general',
                'plasticos_enseres_hogar', 'jarcieria_productos_limpieza', 'ferreteria_tlapaleria',
                'cosmeticos_perfumeria', 'reparacion_celulares', 'jugueteria_novedades'
            ],
            'canasta_basica': True,
            'mercomuna': True,
            'popular_tags': ['verduras', 'frutas', 'carnes', 'ropa de paca', 'tenis', 'tacos', 'chacharas', 'huevo', 'abarrotes']
        }

    # Concentraciones Comerciales en vía pública
    if space_type == 'Concentración':
        return {
            'categorias': [
                'CAT_COMIDA_PREPARADA', 'CAT_ROPA_CALZADO_TEXTIL', 'CAT_BAZAR_CHACHARAS',
                'CAT_OFICIOS_SERVICIOS', 'CAT_HOGAR_FERRETERIA', 'CAT_PAPELERIA_TECNOLOGIA'
            ],
            'subgiros': [
                'taqueria', 'antojitos_mexicanos', 'torteria', 'comida_preparada_general',
                'venta_ropa', 'zapateria_calzado', 'lenceria_boneteria',
                'chacharas_segunda_mano', 'comercio_mixto_general',
                'reparacion_calzado', 'cerrajeria', 'taller_costura_sastreria',
                'reparacion_celulares', 'jarcieria_productos_limpieza'
            ],
            'canasta_basica': False,
            'mercomuna': False,
            'popular_tags': ['comida', 'antojitos', 'ropa', 'calzado', 'reparaciones', 'chacharas']
        }

    # Mercados Públicos: Analizar si es especializado o mixto tradicional
    if 'COMIDA PREPARADA' in norm_giro or 'COMIDAS' in norm_nom or 'PASAJE CHAPULTEPEC' in norm_nom:
        return {
            'categorias': ['CAT_COMIDA_PREPARADA', 'CAT_ALIM_FRESCOS'],
            'subgiros': [
                'taqueria', 'antojitos_mexicanos', 'cocina_economica_fonda', 'torteria',
                'cafeteria_fuente_sodas', 'postres_reposteria', 'paleteria_helados', 'comida_preparada_general'
            ],
            'canasta_basica': False,
            'mercomuna': False,
            'popular_tags': ['comida corrida', 'tacos', 'antojitos', 'milanesas', 'tortas', 'jugos']
        }

    if 'ROPA' in norm_giro or 'MIXCALCO' in norm_nom or 'LAGUNILLA ROPA' in norm_nom:
        return {
            'categorias': ['CAT_ROPA_CALZADO_TEXTIL', 'CAT_OFICIOS_SERVICIOS'],
            'subgiros': [
                'venta_ropa', 'zapateria_calzado', 'lenceria_boneteria', 'telas_blancos',
                'bolsos_mochilas', 'taller_costura_sastreria', 'reparacion_calzado'
            ],
            'canasta_basica': False,
            'mercomuna': False,
            'popular_tags': ['ropa', 'pantalones', 'vestidos', 'camisas', 'zapatos', 'tenis', 'costura']
        }

    if 'FLORES' in norm_giro or 'PLANTAS' in norm_giro or 'JAMAICA' in norm_nom or 'FLORES' in norm_nom:
        return {
            'categorias': ['CAT_HOGAR_FERRETERIA', 'CAT_PAPELERIA_TECNOLOGIA', 'CAT_ALIM_FRESCOS'],
            'subgiros': [
                'floreria_plantas', 'mascotas_alimento', 'artesanias_manualidades', 'recauderia_fruteria'
            ],
            'canasta_basica': False,
            'mercomuna': False,
            'popular_tags': ['flores', 'rosas', 'arreglos florales', 'macetas', 'plantas']
        }

    if 'SONORA' in norm_nom or 'ESOTERICO' in norm_giro or 'HIERBAS' in norm_giro:
        return {
            'categorias': ['CAT_SALUD_BELLEZA', 'CAT_PAPELERIA_TECNOLOGIA', 'CAT_BAZAR_CHACHARAS'],
            'subgiros': [
                'herbolaria_esoterismo', 'artesanias_manualidades', 'jugueteria_novedades',
                'chacharas_segunda_mano', 'mascotas_alimento'
            ],
            'canasta_basica': False,
            'mercomuna': False,
            'popular_tags': ['plantas medicinales', 'herbolaria', 'veladoras', 'artesanias', 'incienso']
        }

    if 'MUEBLES' in norm_giro or 'FERRETER' in norm_giro:
        return {
            'categorias': ['CAT_HOGAR_FERRETERIA', 'CAT_OFICIOS_SERVICIOS', 'CAT_SALUD_BELLEZA'],
            'subgiros': [
                'ferreteria_tlapaleria', 'jarcieria_productos_limpieza', 'plasticos_enseres_hogar',
                'muebles_colchones', 'cerrajeria', 'carpinteria_ebanisteria'
            ],
            'canasta_basica': False,
            'mercomuna': False,
            'popular_tags': ['herramientas', 'tornillos', 'muebles', 'limpieza', 'jarcieria']
        }

    if 'ARTESAN' in norm_giro or 'CURIOSIDADES' in norm_nom:
        return {
            'categorias': ['CAT_PAPELERIA_TECNOLOGIA', 'CAT_BAZAR_CHACHARAS'],
            'subgiros': [
                'artesanias_manualidades', 'jugueteria_novedades', 'regalos_bisuteria', 'antiguedades_coleccionismo'
            ],
            'canasta_basica': False,
            'mercomuna': False,
            'popular_tags': ['artesanias', 'recuerdos', 'regalos', 'juguetes', 'platería']
        }

    # Mercado Público Tradicional / Mixto (Canasta Básica y Abasto Barrial por Excelencia)
    return {
        'categorias': [
            'CAT_ALIM_FRESCOS', 'CAT_ABARROTES_CANASTA', 'CAT_COMIDA_PREPARADA',
            'CAT_ROPA_CALZADO_TEXTIL', 'CAT_HOGAR_FERRETERIA', 'CAT_SALUD_BELLEZA',
            'CAT_PAPELERIA_TECNOLOGIA', 'CAT_OFICIOS_SERVICIOS'
        ],
        'subgiros': [
            'recauderia_fruteria', 'carniceria', 'polleria', 'pescaderia', 'cremeria_lacteos',
            'tienda_abarrotes', 'tortilleria_molino', 'panaderia_expendio', 'semillas_chiles_granos',
            'taqueria', 'antojitos_mexicanos', 'cocina_economica_fonda', 'torteria', 'cafeteria_fuente_sodas',
            'venta_ropa', 'zapateria_calzado', 'jarcieria_productos_limpieza', 'plasticos_enseres_hogar',
            'floreria_plantas', 'estetica_peluqueria', 'herbolaria_esoterismo', 'papeleria_copias',
            'reparacion_calzado', 'cerrajeria', 'taller_costura_sastreria'
        ],
        'canasta_basica': True,
        'mercomuna': True,
        'popular_tags': ['frutas', 'verduras', 'carniceria', 'pollo', 'huevo', 'pescado', 'cremeria', 'abarrotes', 'tortillas', 'comida corrida']
    }

def enrich_directorio_unificado():
    """Enriquece el Directorio Unificado de Comercio Popular con las nuevas columnas taxonómicas."""
    json_path = 'data/processed/directorio_comercio_popular.json'
    csv_path = 'data/processed/directorio_comercio_popular.csv'

    with open(json_path, 'r', encoding='utf-8') as f:
        directorio = json.load(f)

    for item in directorio:
        tipo = item.get('tipo_espacio', '')
        giro_raw = item.get('giro', '')
        nom = item.get('nombre', '')
        classification = classify_space(tipo, giro_raw, nom)

        item['categorias'] = classification['categorias']
        item['subgiros'] = classification['subgiros']
        item['es_canasta_basica'] = classification['canasta_basica']
        item['apto_mercomuna'] = classification['mercomuna']
        item['etiquetas_busqueda'] = classification['popular_tags']

    # Guardar JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(directorio, f, ensure_ascii=False, indent=2)

    # Guardar CSV homogéneo
    csv_rows = []
    for d in directorio:
        row = dict(d)
        for k, v in row.items():
            if isinstance(v, list):
                row[k] = '; '.join(str(x) for x in v)
        csv_rows.append(row)

    df = pd.DataFrame(csv_rows)
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"✓ Directorio Unificado enriquecido exitosamente: {len(directorio)} registros actualizados.")

def main():
    print("=" * 70)
    print("COMPILANDO VOCABULARIO DE COMPRAS Y TAXONOMÍA POPULAR CDMX")
    print("=" * 70)

    vocabulario = build_search_vocabulary()
    print(f"• Vocabulario de compras populares generado: {len(vocabulario)} términos de consumo.")

    # Guardar en catalog y processed (formatos duales JSON y CSV)
    destinations = ['data/catalog', 'data/processed']
    for d in destinations:
        os.makedirs(d, exist_ok=True)
        j_path = os.path.join(d, 'vocabulario_compras.json')
        c_path = os.path.join(d, 'vocabulario_compras.csv')

        with open(j_path, 'w', encoding='utf-8') as f:
            json.dump(vocabulario, f, ensure_ascii=False, indent=2)

        csv_rows = []
        for v in vocabulario:
            r = dict(v)
            r['sinonimos'] = '; '.join(r['sinonimos'])
            r['tokens_busqueda'] = '; '.join(r['tokens_busqueda'])
            csv_rows.append(r)

        df = pd.DataFrame(csv_rows)
        df.to_csv(c_path, index=False, encoding='utf-8')
        print(f"✓ Guardado: {j_path} y {c_path}")

    # Enriquecer directorio unificado
    enrich_directorio_unificado()

if __name__ == '__main__':
    main()
