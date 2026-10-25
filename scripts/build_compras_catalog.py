#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compilador del Catálogo y Vocabulario Jerárquico de Compras Populares de la CDMX
Chilangatón 2026 - Reto 1: Comercio Popular y Barrial

Genera el índice de búsqueda predictiva NIVEL MICRO (+300 artículos de consumo popular en tianguis y mercados),
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

# Mapeo exhaustivo (+300 términos populares de compra en tianguis y comercio barrial de México)
VOCABULARIO_RAW = [
    # =========================================================================
    # CAT_ALIM_FRESCOS: Alimentos Frescos y Perecederos
    # =========================================================================

    # --- recauderia_fruteria (Verduras, Hortalizas y Frutas) ---
    {"termino": "Jitomate", "subgiro": "recauderia_fruteria", "sinonimos": ["jitomates", "tomate rojo", "jitomate saladet", "jitomate bola"], "peso": 100},
    {"termino": "Aguacate", "subgiro": "recauderia_fruteria", "sinonimos": ["aguacates", "aguacate hass", "aguacate criollo", "palta"], "peso": 100},
    {"termino": "Cebolla Blanca", "subgiro": "recauderia_fruteria", "sinonimos": ["cebolla", "cebollas", "cebolla blanca grande"], "peso": 95},
    {"termino": "Cebolla Morada", "subgiro": "recauderia_fruteria", "sinonimos": ["cebolla morada", "cebollitas moradas"], "peso": 90},
    {"termino": "Limón con Semilla", "subgiro": "recauderia_fruteria", "sinonimos": ["limon", "limones", "limon colima", "limon criollo"], "peso": 95},
    {"termino": "Limón sin Semilla", "subgiro": "recauderia_fruteria", "sinonimos": ["limon persa", "limon sin semilla"], "peso": 85},
    {"termino": "Papas Blancas", "subgiro": "recauderia_fruteria", "sinonimos": ["papa", "papas", "papa blanca", "papa alpha"], "peso": 95},
    {"termino": "Papas Cambray", "subgiro": "recauderia_fruteria", "sinonimos": ["papa cambray", "papas chicas"], "peso": 80},
    {"termino": "Nopales", "subgiro": "recauderia_fruteria", "sinonimos": ["nopal", "nopalitos", "nopales limpios", "nopal sin espinas"], "peso": 95},
    {"termino": "Plátano Tabasco", "subgiro": "recauderia_fruteria", "sinonimos": ["platano", "platanos", "platano de seda", "platano roatan"], "peso": 90},
    {"termino": "Plátano Macho", "subgiro": "recauderia_fruteria", "sinonimos": ["platano macho", "platano para freir"], "peso": 85},
    {"termino": "Plátano Dominico", "subgiro": "recauderia_fruteria", "sinonimos": ["platano dominico", "platano chiquito"], "peso": 75},
    {"termino": "Manzana Gala", "subgiro": "recauderia_fruteria", "sinonimos": ["manzana", "manzanas", "manzana gala"], "peso": 85},
    {"termino": "Manzana Golden", "subgiro": "recauderia_fruteria", "sinonimos": ["manzana amarilla", "golden delicious"], "peso": 85},
    {"termino": "Manzana Red", "subgiro": "recauderia_fruteria", "sinonimos": ["manzana roja", "red delicious"], "peso": 80},
    {"termino": "Naranja para Jugo", "subgiro": "recauderia_fruteria", "sinonimos": ["naranja", "naranjas", "naranja valencia"], "peso": 90},
    {"termino": "Papaya Maradol", "subgiro": "recauderia_fruteria", "sinonimos": ["papaya", "papayas"], "peso": 85},
    {"termino": "Piña Miel", "subgiro": "recauderia_fruteria", "sinonimos": ["piña", "piñas", "pina gota de miel"], "peso": 85},
    {"termino": "Mango Manila", "subgiro": "recauderia_fruteria", "sinonimos": ["mango", "mangos", "mango manila dulce"], "peso": 85},
    {"termino": "Mango Ataulfo", "subgiro": "recauderia_fruteria", "sinonimos": ["mango ataulfo", "ataulfo de chiapas"], "peso": 85},
    {"termino": "Mango Petacón", "subgiro": "recauderia_fruteria", "sinonimos": ["mango petacon", "mango kent", "mango tommy"], "peso": 80},
    {"termino": "Zanahorias", "subgiro": "recauderia_fruteria", "sinonimos": ["zanahoria", "zanahorias tiernas"], "peso": 85},
    {"termino": "Calabacita Italiana", "subgiro": "recauderia_fruteria", "sinonimos": ["calabacitas", "calabacita", "calabaza tierna"], "peso": 85},
    {"termino": "Calabaza Criolla", "subgiro": "recauderia_fruteria", "sinonimos": ["calabaza redonda", "calabacita redonda"], "peso": 75},
    {"termino": "Lechuga Orejona", "subgiro": "recauderia_fruteria", "sinonimos": ["lechuga", "lechugas", "lechuga orejona fresca"], "peso": 85},
    {"termino": "Lechuga Romana e Italiana", "subgiro": "recauderia_fruteria", "sinonimos": ["lechuga romana", "lechuga italiana", "lechuga sangria"], "peso": 80},
    {"termino": "Cilantro", "subgiro": "recauderia_fruteria", "sinonimos": ["cilantro fresco", "manojo de cilantro"], "peso": 90},
    {"termino": "Perejil", "subgiro": "recauderia_fruteria", "sinonimos": ["perejil liso", "perejil chino"], "peso": 80},
    {"termino": "Epazote", "subgiro": "recauderia_fruteria", "sinonimos": ["epazote verde", "epazote morado", "manojo de epazote"], "peso": 85},
    {"termino": "Hierbabuena y Menta", "subgiro": "recauderia_fruteria", "sinonimos": ["hierbabuena", "menta fresca"], "peso": 80},
    {"termino": "Berros", "subgiro": "recauderia_fruteria", "sinonimos": ["berro", "berros frescos"], "peso": 75},
    {"termino": "Espinacas", "subgiro": "recauderia_fruteria", "sinonimos": ["espinaca", "manojo de espinacas"], "peso": 85},
    {"termino": "Acelgas", "subgiro": "recauderia_fruteria", "sinonimos": ["acelga", "manojo de acelgas"], "peso": 80},
    {"termino": "Quelites", "subgiro": "recauderia_fruteria", "sinonimos": ["quelite", "cenizo", "quintonil"], "peso": 80},
    {"termino": "Verdolagas", "subgiro": "recauderia_fruteria", "sinonimos": ["verdolaga", "verdolagas para cerdo"], "peso": 80},
    {"termino": "Romeritos", "subgiro": "recauderia_fruteria", "sinonimos": ["romerito", "romeritos limpios"], "peso": 75},
    {"termino": "Huitlacoche", "subgiro": "recauderia_fruteria", "sinonimos": ["cuitlacoche", "hongo de maiz"], "peso": 85},
    {"termino": "Flor de Calabaza", "subgiro": "recauderia_fruteria", "sinonimos": ["guías de calabaza", "flores de calabaza"], "peso": 85},
    {"termino": "Chiles Serranos", "subgiro": "recauderia_fruteria", "sinonimos": ["chile verde", "chile serrano"], "peso": 90},
    {"termino": "Chile Jalapeño / Cuaresmeño", "subgiro": "recauderia_fruteria", "sinonimos": ["chile cuaresmeño", "chile jalapeño"], "peso": 90},
    {"termino": "Chile Poblano", "subgiro": "recauderia_fruteria", "sinonimos": ["chile para rellenar", "chiles poblanos"], "peso": 90},
    {"termino": "Chile Habanero", "subgiro": "recauderia_fruteria", "sinonimos": ["habanero", "chile habanero naranja"], "peso": 85},
    {"termino": "Chile Manzano", "subgiro": "recauderia_fruteria", "sinonimos": ["chile manzano amarillo", "peron"], "peso": 80},
    {"termino": "Tomate Verde con Cáscara", "subgiro": "recauderia_fruteria", "sinonimos": ["tomate", "tomates", "tomatillo", "tomate verde"], "peso": 95},
    {"termino": "Fresas Frescas", "subgiro": "recauderia_fruteria", "sinonimos": ["fresa", "fresas", "canasta de fresas"], "peso": 85},
    {"termino": "Sandía", "subgiro": "recauderia_fruteria", "sinonimos": ["sandia roja", "rebanada de sandia"], "peso": 85},
    {"termino": "Melón Chino", "subgiro": "recauderia_fruteria", "sinonimos": ["melon", "melon cantaloupe"], "peso": 80},
    {"termino": "Chayote sin Espina", "subgiro": "recauderia_fruteria", "sinonimos": ["chayote", "chayotes"], "peso": 85},
    {"termino": "Chayote con Espina", "subgiro": "recauderia_fruteria", "sinonimos": ["chayote espinudo", "chayote criollo"], "peso": 75},
    {"termino": "Ajo y Cabezas de Ajo", "subgiro": "recauderia_fruteria", "sinonimos": ["ajo", "ajos", "diente de ajo"], "peso": 85},
    {"termino": "Guayabas", "subgiro": "recauderia_fruteria", "sinonimos": ["guayaba", "guayaba dulce"], "peso": 80},
    {"termino": "Tunas Blancas y Rojas", "subgiro": "recauderia_fruteria", "sinonimos": ["tuna", "tunas", "tuna tapona"], "peso": 80},
    {"termino": "Tejocotes", "subgiro": "recauderia_fruteria", "sinonimos": ["tejocote", "tejocotes para ponche"], "peso": 75},
    {"termino": "Jícama", "subgiro": "recauderia_fruteria", "sinonimos": ["jicamas", "jicama con limon y chile"], "peso": 85},
    {"termino": "Toronja", "subgiro": "recauderia_fruteria", "sinonimos": ["toronjas", "toronja roja"], "peso": 75},
    {"termino": "Uvas sin Semilla", "subgiro": "recauderia_fruteria", "sinonimos": ["uvas", "uva roja", "uva verde globe"], "peso": 80},
    {"termino": "Mamey", "subgiro": "recauderia_fruteria", "sinonimos": ["mameyes", "zapote mamey"], "peso": 85},
    {"termino": "Chicozapote y Zapote Negro", "subgiro": "recauderia_fruteria", "sinonimos": ["chicozapote", "zapote negro"], "peso": 75},
    {"termino": "Ciruelas Rojas y Amarillas", "subgiro": "recauderia_fruteria", "sinonimos": ["ciruela", "ciruelas"], "peso": 75},
    {"termino": "Betabel", "subgiro": "recauderia_fruteria", "sinonimos": ["betabeles", "remolacha"], "peso": 80},
    {"termino": "Brócoli", "subgiro": "recauderia_fruteria", "sinonimos": ["brocolis", "arbolitos de brocoli"], "peso": 85},
    {"termino": "Coliflor", "subgiro": "recauderia_fruteria", "sinonimos": ["coliflores"], "peso": 80},
    {"termino": "Col Blanca y Morada", "subgiro": "recauderia_fruteria", "sinonimos": ["col", "repollo", "col morada"], "peso": 80},
    {"termino": "Ejotes Tiernos", "subgiro": "recauderia_fruteria", "sinonimos": ["ejote", "ejotes verdes"], "peso": 80},
    {"termino": "Habas Verdes", "subgiro": "recauderia_fruteria", "sinonimos": ["haba verde", "vainas de haba"], "peso": 75},
    {"termino": "Chícharos en Vaina", "subgiro": "recauderia_fruteria", "sinonimos": ["chicharo", "chicharos", "arveja"], "peso": 80},
    {"termino": "Poro y Apio", "subgiro": "recauderia_fruteria", "sinonimos": ["poro", "apio", "tallos de apio"], "peso": 75},
    {"termino": "Calabaza de Castilla", "subgiro": "recauderia_fruteria", "sinonimos": ["calabaza para dulce", "trozo de calabaza"], "peso": 75},
    {"termino": "Rábanos", "subgiro": "recauderia_fruteria", "sinonimos": ["rabano", "manojo de rabanos"], "peso": 80},

    # --- carniceria (Carnes de Res, Cerdo y Embutidos) ---
    {"termino": "Bistec de Res", "subgiro": "carniceria", "sinonimos": ["bistec", "bisteces", "carne de res", "filete de res", "pulpa de res"], "peso": 95},
    {"termino": "Carne Molida de Res", "subgiro": "carniceria", "sinonimos": ["molida de res", "carne molida", "molida mixta", "molida especial"], "peso": 95},
    {"termino": "Cecina de Yecapixtla", "subgiro": "carniceria", "sinonimos": ["cecina", "cecina morelense", "cecina delgada"], "peso": 95},
    {"termino": "Cecina Enchilada", "subgiro": "carniceria", "sinonimos": ["cecina adobada", "tasajo enchilado"], "peso": 90},
    {"termino": "Carne de Cerdo", "subgiro": "carniceria", "sinonimos": ["puerco", "lomo de cerdo", "pierna de cerdo", "trozo de puerco"], "peso": 90},
    {"termino": "Chuletas de Cerdo", "subgiro": "carniceria", "sinonimos": ["chuleta ahumada", "chuleta natural", "chuletas"], "peso": 90},
    {"termino": "Costilla de Res y Cerdo", "subgiro": "carniceria", "sinonimos": ["costilla", "costillitas", "costilla para asar", "costilla cargada"], "peso": 90},
    {"termino": "Longaniza de Toluca", "subgiro": "carniceria", "sinonimos": ["longaniza", "longaniza de cerdo", "longaniza casera"], "peso": 95},
    {"termino": "Chorizo Verde y Rojo", "subgiro": "carniceria", "sinonimos": ["chorizo", "chorizo verde", "chorizo de toluca", "chorizo artesanal"], "peso": 90},
    {"termino": "Suadero Crudo", "subgiro": "carniceria", "sinonimos": ["suadero", "corte de suadero", "suadero de res"], "peso": 90},
    {"termino": "Chicharrón de Cerdo Crujiente", "subgiro": "carniceria", "sinonimos": ["chicharron", "chicharron de pella", "chicharrón botanero"], "peso": 95},
    {"termino": "Chicharrón Prensado", "subgiro": "carniceria", "sinonimos": ["chicharron prensado", "prensado para gorditas"], "peso": 95},
    {"termino": "Tocino Ahumado", "subgiro": "carniceria", "sinonimos": ["tocino", "tocino en rebanadas", "tocino grueso"], "peso": 85},
    {"termino": "Tripa de Res Cruda", "subgiro": "carniceria", "sinonimos": ["tripa", "tripas de res", "tripita"], "peso": 85},
    {"termino": "Machitos de Res", "subgiro": "carniceria", "sinonimos": ["machito", "machitos"], "peso": 80},
    {"termino": "Cabeza de Res", "subgiro": "carniceria", "sinonimos": ["cabeza de res", "ojo de res", "sesos", "cachete de res"], "peso": 85},
    {"termino": "Lengua de Res", "subgiro": "carniceria", "sinonimos": ["lengua de res", "lengua limpia"], "peso": 85},
    {"termino": "Moronga y Rellena", "subgiro": "carniceria", "sinonimos": ["moronga", "rellena", "morcilla"], "peso": 80},
    {"termino": "Manitas de Cerdo", "subgiro": "carniceria", "sinonimos": ["manitas de puerco", "patitas de cerdo"], "peso": 80},
    {"termino": "Manteca de Cerdo Criolla", "subgiro": "carniceria", "sinonimos": ["manteca", "manteca de puerco", "kilo de manteca"], "peso": 85},
    {"termino": "Milanesas Empanizadas", "subgiro": "carniceria", "sinonimos": ["milanesa preparada", "milanesa de res empanizada"], "peso": 90},
    {"termino": "Carne al Pastor Marinada", "subgiro": "carniceria", "sinonimos": ["carne adobada", "bistec enchilado pastor"], "peso": 85},
    {"termino": "Chamorro de Cerdo", "subgiro": "carniceria", "sinonimos": ["chamorros", "chamorro para carnitas"], "peso": 85},
    {"termino": "Arrachera Marinada", "subgiro": "carniceria", "sinonimos": ["arrachera", "arrachera para asar"], "peso": 90},
    {"termino": "Tuétano de Res", "subgiro": "carniceria", "sinonimos": ["huesos con tuetano", "tuetanos"], "peso": 85},

    # --- polleria (Aves de Corral y Huevo) ---
    {"termino": "Pechuga de Pollo", "subgiro": "polleria", "sinonimos": ["pechuga", "pechugas", "pechuga aplanada", "pechuga en bistec", "milanesa de pollo"], "peso": 100},
    {"termino": "Pollo Entero en Canal", "subgiro": "polleria", "sinonimos": ["pollo", "pollos", "medio pollo", "pollo limpio"], "peso": 95},
    {"termino": "Pierna y Muslo de Pollo", "subgiro": "polleria", "sinonimos": ["piernas de pollo", "muslos de pollo", "pierna con muslo"], "peso": 95},
    {"termino": "Alitas de Pollo Crudas", "subgiro": "polleria", "sinonimos": ["alitas", "alas de pollo"], "peso": 90},
    {"termino": "Retazo de Pollo", "subgiro": "polleria", "sinonimos": ["retazo", "huacal", "rabadilla", "cuellos de pollo"], "peso": 85},
    {"termino": "Mollejas de Pollo", "subgiro": "polleria", "sinonimos": ["molleja", "mollejitas"], "peso": 80},
    {"termino": "Patitas de Pollo Limpias", "subgiro": "polleria", "sinonimos": ["patitas de pollo", "patas para caldo"], "peso": 85},
    {"termino": "Hígado de Pollo", "subgiro": "polleria", "sinonimos": ["higaditos de pollo", "higado"], "peso": 80},
    {"termino": "Pollo Rostizado con Papas", "subgiro": "polleria", "sinonimos": ["pollo rostizado", "rosticeria", "pollo asado"], "peso": 90},
    {"termino": "Huevo Blanco por Kilo", "subgiro": "polleria", "sinonimos": ["huevo", "huevos", "cono de huevo", "blanquillos"], "peso": 100},
    {"termino": "Huevo Rojo de Rancho", "subgiro": "polleria", "sinonimos": ["huevo rojo", "huevo organico", "huevo criollo"], "peso": 90},
    {"termino": "Huevo de Codorniz", "subgiro": "polleria", "sinonimos": ["huevitos de codorniz", "huevo codorniz"], "peso": 75},

    # --- pescaderia (Pescados y Mariscos) ---
    {"termino": "Mojarra Tilapia para Freír", "subgiro": "pescaderia", "sinonimos": ["mojarra", "mojarras", "mojarra fresca", "tilapia"], "peso": 95},
    {"termino": "Filete de Pescado Blanco", "subgiro": "pescaderia", "sinonimos": ["filete de pescado", "filete de basa", "filete de mojarra", "filete sin espinas"], "peso": 95},
    {"termino": "Huachinango Fresco", "subgiro": "pescaderia", "sinonimos": ["huachinango", "pargo rojo"], "peso": 90},
    {"termino": "Pescado Sierra para Ceviche", "subgiro": "pescaderia", "sinonimos": ["sierra", "pescado para ceviche"], "peso": 85},
    {"termino": "Camarón con Cabeza Crudo", "subgiro": "pescaderia", "sinonimos": ["camaron", "camarones", "camaron para caldo"], "peso": 95},
    {"termino": "Camarón Pacotilla Cocido", "subgiro": "pescaderia", "sinonimos": ["camaron pacotilla", "camaron para coctel"], "peso": 95},
    {"termino": "Camarón Cristal Mediano", "subgiro": "pescaderia", "sinonimos": ["camaron cristal", "camaron pelado"], "peso": 90},
    {"termino": "Camarón Seco para Caldo", "subgiro": "pescaderia", "sinonimos": ["camaron seco", "camaron en polvo", "camaron salado"], "peso": 85},
    {"termino": "Pulpo Crudo y Cocido", "subgiro": "pescaderia", "sinonimos": ["pulpo", "tentaculos de pulpo"], "peso": 85},
    {"termino": "Calamar Entero y Anillas", "subgiro": "pescaderia", "sinonimos": ["calamar", "anillas de calamar"], "peso": 80},
    {"termino": "Jaiba Fresca", "subgiro": "pescaderia", "sinonimos": ["jaiba", "jaibas para caldo", "cangrejo"], "peso": 85},
    {"termino": "Ostiones Frescos en Concha", "subgiro": "pescaderia", "sinonimos": ["ostion", "ostiones", "ostiones en su concha"], "peso": 85},
    {"termino": "Almejas Chocolatas", "subgiro": "pescaderia", "sinonimos": ["almeja", "almejas", "almeja viva"], "peso": 80},
    {"termino": "Filete de Cazón", "subgiro": "pescaderia", "sinonimos": ["cazon", "cazon para empanadas"], "peso": 85},
    {"termino": "Charales Secos y Fritos", "subgiro": "pescaderia", "sinonimos": ["charal", "charales", "charales con sal y limon"], "peso": 85},
    {"termino": "Salmón Fresco", "subgiro": "pescaderia", "sinonimos": ["salmon", "filete de salmon"], "peso": 80},
    {"termino": "Bagre para Caldo", "subgiro": "pescaderia", "sinonimos": ["bagre", "bagre fresco"], "peso": 75},

    # --- cremeria_lacteos (Quesos, Crema, Leche y Salchichonería) ---
    {"termino": "Queso Oaxaca / Quesillo", "subgiro": "cremeria_lacteos", "sinonimos": ["queso oaxaca", "quesillo", "queso de hebra", "quesillo artesanal"], "peso": 100},
    {"termino": "Queso Panela de Canasto", "subgiro": "cremeria_lacteos", "sinonimos": ["queso panela", "panela", "queso de canasta"], "peso": 95},
    {"termino": "Queso Manchego Artesanal", "subgiro": "cremeria_lacteos", "sinonimos": ["queso manchego", "manchego", "queso para fundir"], "peso": 95},
    {"termino": "Queso Cotija Añejo", "subgiro": "cremeria_lacteos", "sinonimos": ["queso cotija", "cotija rallado", "queso seco"], "peso": 90},
    {"termino": "Queso Doble Crema Chiapaneco", "subgiro": "cremeria_lacteos", "sinonimos": ["doble crema", "queso chiapas"], "peso": 85},
    {"termino": "Requesón Fresco Artesanal", "subgiro": "cremeria_lacteos", "sinonimos": ["requeson", "requeson de rancho", "ricotta"], "peso": 90},
    {"termino": "Queso Canasto y Frescal", "subgiro": "cremeria_lacteos", "sinonimos": ["queso blanco", "queso fresco"], "peso": 85},
    {"termino": "Crema de Rancho Ácida", "subgiro": "cremeria_lacteos", "sinonimos": ["crema", "crema de rancho", "crema acida", "crema de vaca"], "peso": 95},
    {"termino": "Crema Dulce de Vaca", "subgiro": "cremeria_lacteos", "sinonimos": ["crema dulce", "crema para fresas"], "peso": 85},
    {"termino": "Leche Entera y Pasteurizada", "subgiro": "cremeria_lacteos", "sinonimos": ["leche", "litro de leche", "leche bronca", "leche fresca"], "peso": 95},
    {"termino": "Jamón de Pierna y Pavo", "subgiro": "cremeria_lacteos", "sinonimos": ["jamon", "jamon de pavo", "jamon virginia", "jamon de pierna"], "peso": 95},
    {"termino": "Salchicha de Pavo y Vienesa", "subgiro": "cremeria_lacteos", "sinonimos": ["salchichas", "salchicha de pavo", "salchicha para hotdog"], "peso": 90},
    {"termino": "Salchicha para Asar Polaca", "subgiro": "cremeria_lacteos", "sinonimos": ["salchicha para asar", "salchicha polaca"], "peso": 85},
    {"termino": "Mortadela y Pastel de Pollo", "subgiro": "cremeria_lacteos", "sinonimos": ["mortadela", "pastel de pollo", "queso de puerco"], "peso": 80},
    {"termino": "Mantequilla de Rancho", "subgiro": "cremeria_lacteos", "sinonimos": ["mantequilla", "mantequilla pura", "mantequilla amarilla"], "peso": 85},
    {"termino": "Margarina y Manteca Vegetal", "subgiro": "cremeria_lacteos", "sinonimos": ["margarina", "manteca vegetal"], "peso": 75},
    {"termino": "Queso Amarillo Americano", "subgiro": "cremeria_lacteos", "sinonimos": ["queso amarillo", "queso americano", "queso para sandwich"], "peso": 85},

    # =========================================================================
    # CAT_ABARROTES_CANASTA: Abarrotes, Materias Primas y Canasta Básica
    # =========================================================================

    # --- tienda_abarrotes (Canasta Básica y Despensa) ---
    {"termino": "Frijol Negro por Kilo", "subgiro": "tienda_abarrotes", "sinonimos": ["frijol", "frijoles", "frijol negro", "frijol michoacan"], "peso": 100},
    {"termino": "Frijol Pinto y Bayo", "subgiro": "tienda_abarrotes", "sinonimos": ["frijol pinto", "frijol bayo", "frijol flor de mayo", "frijol peruano"], "peso": 95},
    {"termino": "Arroz Blanco Súper Extra", "subgiro": "tienda_abarrotes", "sinonimos": ["arroz", "kilo de arroz", "arroz grano largo"], "peso": 100},
    {"termino": "Aceite Comestible Vegetal", "subgiro": "tienda_abarrotes", "sinonimos": ["aceite", "aceite 1-2-3", "aceite nutrioli", "litro de aceite"], "peso": 100},
    {"termino": "Azúcar Estándar y Morena", "subgiro": "tienda_abarrotes", "sinonimos": ["azucar", "azucar estandar", "azucar morena", "kilo de azucar"], "peso": 95},
    {"termino": "Sal de Mesa Fina y de Grano", "subgiro": "tienda_abarrotes", "sinonimos": ["sal fina", "sal de grano", "sal la fina"], "peso": 90},
    {"termino": "Café Soluble y de Grano", "subgiro": "tienda_abarrotes", "sinonimos": ["cafe", "nescafe", "cafe legal", "cafe de veracruz"], "peso": 90},
    {"termino": "Mayonesa y Mostaza", "subgiro": "tienda_abarrotes", "sinonimos": ["mayonesa mc cormick", "mayonesa con limon", "mostaza"], "peso": 85},
    {"termino": "Atún en Lata Agua y Aceite", "subgiro": "tienda_abarrotes", "sinonimos": ["atun", "lata de atun", "atun dolores"], "peso": 90},
    {"termino": "Sardinas en Jitomate", "subgiro": "tienda_abarrotes", "sinonimos": ["sardina", "lata de sardina", "sardina guaymex"], "peso": 85},
    {"termino": "Sopas de Pasta Surtidas", "subgiro": "tienda_abarrotes", "sinonimos": ["pasta", "sopa de fideo", "sopa de codito", "espagueti", "pasta la moderna"], "peso": 90},
    {"termino": "Harina de Trigo y Maíz", "subgiro": "tienda_abarrotes", "sinonimos": ["harina", "harina maseca", "harina selecta", "harina para hot cakes"], "peso": 90},
    {"termino": "Leche Condensada y Evaporada", "subgiro": "tienda_abarrotes", "sinonimos": ["lechera", "leche clavel", "leche evaporada"], "peso": 90},
    {"termino": "Chiles Jalapeños en Vinagre", "subgiro": "tienda_abarrotes", "sinonimos": ["chiles en lata", "chiles la costeña", "rajas en vinagre"], "peso": 90},
    {"termino": "Vinagre Blanco y de Manzana", "subgiro": "tienda_abarrotes", "sinonimos": ["vinagre", "vinagre de caña", "vinagre para desinfectar"], "peso": 85},
    {"termino": "Consomé de Pollo en Polvo", "subgiro": "tienda_abarrotes", "sinonimos": ["knorr suiza", "caldo de pollo", "consome"], "peso": 85},
    {"termino": "Lentejas Seleccionadas", "subgiro": "tienda_abarrotes", "sinonimos": ["lenteja", "lentejas", "kilo de lentejas"], "peso": 90},
    {"termino": "Garbanzo Seco", "subgiro": "tienda_abarrotes", "sinonimos": ["garbanzos", "garbanzo para caldo"], "peso": 85},
    {"termino": "Habas Secas Amarillas", "subgiro": "tienda_abarrotes", "sinonimos": ["habas", "habas secas", "habas para sopa"], "peso": 85},
    {"termino": "Avena en Hojuelas", "subgiro": "tienda_abarrotes", "sinonimos": ["avena", "avena quaker", "hojuelas de avena"], "peso": 90},
    {"termino": "Maíz Pozolero Cacahuazintle", "subgiro": "tienda_abarrotes", "sinonimos": ["maiz pozolero", "cacahuazintle", "maiz para pozole"], "peso": 90},
    {"termino": "Puré de Tomate", "subgiro": "tienda_abarrotes", "sinonimos": ["pure de tomate", "puré condimentado"], "peso": 85},
    {"termino": "Galletas Marías y Saladas", "subgiro": "tienda_abarrotes", "sinonimos": ["galletas marias", "galletas saladas", "galletas gamesa"], "peso": 85},

    # --- tortilleria_molino ---
    {"termino": "Tortillas de Maíz Calientes", "subgiro": "tortilleria_molino", "sinonimos": ["tortilla", "tortillas", "kilo de tortillas", "tortilla de maiz nixtamalizado"], "peso": 100},
    {"termino": "Masa de Nixtamal Fresca", "subgiro": "tortilleria_molino", "sinonimos": ["masa", "masa para tamales", "masa para tortillas", "masa preparada"], "peso": 95},
    {"termino": "Tortillas Hechas a Mano en Comal", "subgiro": "tortilleria_molino", "sinonimos": ["tortillas de comal", "tortillas a mano", "tortillas gruesas"], "peso": 95},
    {"termino": "Tortillas de Harina estilo Norteño", "subgiro": "tortilleria_molino", "sinonimos": ["tortilla de harina", "tortillas para burritos"], "peso": 90},
    {"termino": "Tostadas de Maíz Caseras", "subgiro": "tortilleria_molino", "sinonimos": ["tostadas", "tostadas fritas", "tostadas horneadas"], "peso": 90},
    {"termino": "Tlayudas Oaxaqueñas", "subgiro": "tortilleria_molino", "sinonimos": ["tlayuda", "tlayudas con asiento"], "peso": 85},
    {"termino": "Totopos para Chilaquiles", "subgiro": "tortilleria_molino", "sinonimos": ["totopos", "totopos fritos", "nachos"], "peso": 85},

    # --- panaderia_expendio ---
    {"termino": "Bolillo Caliente y Crujiente", "subgiro": "panaderia_expendio", "sinonimos": ["bolillo", "bolillos", "pan blanco"], "peso": 100},
    {"termino": "Telera para Tortas", "subgiro": "panaderia_expendio", "sinonimos": ["telera", "teleras", "pan para torta"], "peso": 95},
    {"termino": "Conchas de Vainilla y Chocolate", "subgiro": "panaderia_expendio", "sinonimos": ["concha", "conchas", "pan de dulce"], "peso": 95},
    {"termino": "Cuernitos de Mantequilla", "subgiro": "panaderia_expendio", "sinonimos": ["cuernito", "croissant"], "peso": 85},
    {"termino": "Orejas de Hojaldre", "subgiro": "panaderia_expendio", "sinonimos": ["oreja", "orejas hojaldradas"], "peso": 85},
    {"termino": "Donas de Azúcar y Chocolate", "subgiro": "panaderia_expendio", "sinonimos": ["dona", "donas", "donitas"], "peso": 85},
    {"termino": "Cocoles de Piloncillo y Anís", "subgiro": "panaderia_expendio", "sinonimos": ["cocol", "cocoles tradicionales"], "peso": 85},
    {"termino": "Panqué de Nuez y Pasas", "subgiro": "panaderia_expendio", "sinonimos": ["panque", "panqué con nuez"], "peso": 80},
    {"termino": "Polvorones y Galletas Tradicionales", "subgiro": "panaderia_expendio", "sinonimos": ["polvoron", "galletas de canela"], "peso": 80},
    {"termino": "Pan de Muerto Artesanal", "subgiro": "panaderia_expendio", "sinonimos": ["pan de muerto", "pan con ajonjolí"], "peso": 85},
    {"termino": "Rosca de Reyes Tradicional", "subgiro": "panaderia_expendio", "sinonimos": ["rosca de reyes", "rosca con ate"], "peso": 85},

    # --- semillas_chiles_granos (Especias, Chiles Secos y Semillas) ---
    {"termino": "Chile Guajillo Seco", "subgiro": "semillas_chiles_granos", "sinonimos": ["chile guajillo", "guajillo del que pica", "guajillo liso"], "peso": 95},
    {"termino": "Chile Ancho Seco", "subgiro": "semillas_chiles_granos", "sinonimos": ["chile ancho", "chile colorado", "ancho para mole"], "peso": 95},
    {"termino": "Chile Pasilla Negro", "subgiro": "semillas_chiles_granos", "sinonimos": ["chile pasilla", "pasilla mexicano"], "peso": 90},
    {"termino": "Chile Chipotle Seco / Meco", "subgiro": "semillas_chiles_granos", "sinonimos": ["chile chipotle", "chipotle meco", "mora"], "peso": 90},
    {"termino": "Chile Morita", "subgiro": "semillas_chiles_granos", "sinonimos": ["chile morita", "morita ahumado"], "peso": 90},
    {"termino": "Chile de Árbol Seco", "subgiro": "semillas_chiles_granos", "sinonimos": ["chile de arbol", "chile cola de rata"], "peso": 90},
    {"termino": "Canela Entera en Raja", "subgiro": "semillas_chiles_granos", "sinonimos": ["canela", "rajas de canela", "canela de ceilán"], "peso": 90},
    {"termino": "Pimienta Negra y Gorda", "subgiro": "semillas_chiles_granos", "sinonimos": ["pimienta", "pimienta gorda", "pimienta tabasco"], "peso": 85},
    {"termino": "Clavo de Olor Entero", "subgiro": "semillas_chiles_granos", "sinonimos": ["clavo de olor", "clavos de olor"], "peso": 85},
    {"termino": "Comino Molido y Entero", "subgiro": "semillas_chiles_granos", "sinonimos": ["comino", "cominos"], "peso": 85},
    {"termino": "Orégano Seco Aromático", "subgiro": "semillas_chiles_granos", "sinonimos": ["oregano", "oregano para pozole"], "peso": 85},
    {"termino": "Hojas de Laurel Secas", "subgiro": "semillas_chiles_granos", "sinonimos": ["laurel", "hojas de laurel"], "peso": 80},
    {"termino": "Ajonjolí Blanco y Tostado", "subgiro": "semillas_chiles_granos", "sinonimos": ["ajonjoli", "sesamo", "ajonjoli para mole"], "peso": 85},
    {"termino": "Pepitas de Calabaza con Sal", "subgiro": "semillas_chiles_granos", "sinonimos": ["pepitas", "pepita verde", "pepitas tostadas"], "peso": 85},
    {"termino": "Cacahuates Tostados con Cáscara", "subgiro": "semillas_chiles_granos", "sinonimos": ["cacahuates", "cacahuate tostado"], "peso": 90},
    {"termino": "Cacahuates Garapiñados y Japoneses", "subgiro": "semillas_chiles_granos", "sinonimos": ["cacahuates japoneses", "garapiñados"], "peso": 85},
    {"termino": "Nuez de Castilla y Pecana", "subgiro": "semillas_chiles_granos", "sinonimos": ["nuez", "nueces", "mitades de nuez"], "peso": 85},
    {"termino": "Pasas y Arándanos Secos", "subgiro": "semillas_chiles_granos", "sinonimos": ["pasitas", "uvas pasas", "arandanos"], "peso": 80},
    {"termino": "Almendras Enteras", "subgiro": "semillas_chiles_granos", "sinonimos": ["almendra", "almendras"], "peso": 80},
    {"termino": "Semillas de Girasol Tostadas", "subgiro": "semillas_chiles_granos", "sinonimos": ["semillas de girasol", "pipas"], "peso": 75},
    {"termino": "Amaranto Natural y Tostado", "subgiro": "semillas_chiles_granos", "sinonimos": ["amaranto", "semilla de amaranto"], "peso": 80},
    {"termino": "Flor de Jamaica Nacional", "subgiro": "semillas_chiles_granos", "sinonimos": ["jamaica", "flor de jamaica", "jamaica criolla"], "peso": 90},
    {"termino": "Tamarindo Entero para Agua", "subgiro": "semillas_chiles_granos", "sinonimos": ["tamarindo", "vainas de tamarindo"], "peso": 85},

    # --- materias_primas ---
    {"termino": "Bolsas de Plástico Biodegradables", "subgiro": "materias_primas", "sinonimos": ["bolsas de plastico", "bolsas camiseta", "rollo de bolsas"], "peso": 85},
    {"termino": "Desechables para Fiestas (Vasos y Platos)", "subgiro": "materias_primas", "sinonimos": ["vasos desechables", "platos desechables", "cucharas de plastico"], "peso": 85},
    {"termino": "Servilletas de Papel por Paquete", "subgiro": "materias_primas", "sinonimos": ["servilletas", "paquete de servilletas"], "peso": 85},
    {"termino": "Papel Aluminio y Papel Encerado", "subgiro": "materias_primas", "sinonimos": ["papel aluminio", "papel para hornear"], "peso": 80},
    {"termino": "Hieleras de Unicel", "subgiro": "materias_primas", "sinonimos": ["hielera", "caja termica"], "peso": 75},
    {"termino": "Moldes para Gelatina y Pastel", "subgiro": "materias_primas", "sinonimos": ["moldes", "moldes de reposteria"], "peso": 75},
    {"termino": "Colorantes y Esencias Vegetales", "subgiro": "materias_primas", "sinonimos": ["esencia de vainilla", "colorante vegetal"], "peso": 75},

    # --- dulceria_botanas ---
    {"termino": "Dulces Típicos Mexicanos (Alegrías y Cocadas)", "subgiro": "dulceria_botanas", "sinonimos": ["dulces tipicos", "alegrias", "palanquetas", "cocadas", "ate"], "peso": 90},
    {"termino": "Dulces de Tamarindo y Chamoy", "subgiro": "dulceria_botanas", "sinonimos": ["pulparindo", "chamoy", "pelon pelo rico"], "peso": 90},
    {"termino": "Gomitas a Granel por Kilo", "subgiro": "dulceria_botanas", "sinonimos": ["gomitas", "panditas", "gomitas enchiladas"], "peso": 85},
    {"termino": "Chocolates Artesanales", "subgiro": "dulceria_botanas", "sinonimos": ["chocolate de mesa", "chocolates surtidos"], "peso": 85},
    {"termino": "Papas Fritas y Frituras Artesanales", "subgiro": "dulceria_botanas", "sinonimos": ["papas caseras", "botanas", "platanitos fritos"], "peso": 90},
    {"termino": "Chicharrones de Harina y Rueda", "subgiro": "dulceria_botanas", "sinonimos": ["chicharrones de harina", "rueditas de harina"], "peso": 85},

    # --- purificadora_agua ---
    {"termino": "Garrafón de Agua Purificada 20L", "subgiro": "purificadora_agua", "sinonimos": ["garrafon de agua", "llenado de garrafon", "agua purificada"], "peso": 95},
    {"termino": "Hielo en Bolsa y Cilindro", "subgiro": "purificadora_agua", "sinonimos": ["hielo", "bolsa de hielo", "cubos de hielo"], "peso": 85},

    # =========================================================================
    # CAT_COMIDA_PREPARADA: Alimentos Preparados, Bebidas y Antojitos
    # =========================================================================

    # --- taqueria ---
    {"termino": "Tacos de Suadero", "subgiro": "taqueria", "sinonimos": ["suadero", "tacos suadero", "orden de suadero"], "peso": 100},
    {"termino": "Tacos de Pastor con Piña", "subgiro": "taqueria", "sinonimos": ["tacos al pastor", "pastor", "tacos de trompo"], "peso": 100},
    {"termino": "Tacos de Longaniza y Chorizo", "subgiro": "taqueria", "sinonimos": ["tacos de longaniza", "tacos campechanos"], "peso": 95},
    {"termino": "Tacos de Carnitas (Maciza y Cuerito)", "subgiro": "taqueria", "sinonimos": ["tacos de carnitas", "taco de surtida", "taco de costilla"], "peso": 95},
    {"termino": "Tacos de Tripa Dorada", "subgiro": "taqueria", "sinonimos": ["tacos de tripa", "tripitas doradas"], "peso": 95},
    {"termino": "Tacos de Cabeza de Res", "subgiro": "taqueria", "sinonimos": ["tacos de cabeza", "taco de lengua", "taco de sesos", "taco de ojo"], "peso": 90},
    {"termino": "Tacos de Cecina Enchilada", "subgiro": "taqueria", "sinonimos": ["taco de cecina", "cecina con papas"], "peso": 90},
    {"termino": "Quesabirrias con Consomé", "subgiro": "taqueria", "sinonimos": ["quesabirria", "tacos de birria con queso", "birria"], "peso": 95},
    {"termino": "Tacos de Guisado Surtidos", "subgiro": "taqueria", "sinonimos": ["tacos de guisado", "taco placero", "tacos de cazuela"], "peso": 95},

    # --- antojitos_mexicanos ---
    {"termino": "Barbacoa de Borrego de Horno", "subgiro": "antojitos_mexicanos", "sinonimos": ["barbacoa", "barbacha", "kilo de barbacoa", "tacos de barbacoa"], "peso": 100},
    {"termino": "Consomé de Barbacoa Caliente", "subgiro": "antojitos_mexicanos", "sinonimos": ["consome", "consome de barbacoa con garbanzos"], "peso": 95},
    {"termino": "Birria de Res en Caldo", "subgiro": "antojitos_mexicanos", "sinonimos": ["birria", "plato de birria", "caldo de birria"], "peso": 95},
    {"termino": "Carnitas Estilo Michoacán", "subgiro": "antojitos_mexicanos", "sinonimos": ["carnitas", "kilo de carnitas", "carnitas de michoacan"], "peso": 100},
    {"termino": "Quesadillas Fritas de Comal", "subgiro": "antojitos_mexicanos", "sinonimos": ["quesadillas", "quesadilla de flor", "quesadilla de huitlacoche", "quesadilla de chicharron"], "peso": 100},
    {"termino": "Gorditas de Chicharrón Prensado", "subgiro": "antojitos_mexicanos", "sinonimos": ["gorditas", "gordita de chicharron", "gorditas de requeson"], "peso": 100},
    {"termino": "Sopes Sencillos y con Carne", "subgiro": "antojitos_mexicanos", "sinonimos": ["sopes", "sope de cecina", "sope con bistec"], "peso": 95},
    {"termino": "Tlacoyos de Haba y Frijol con Nopales", "subgiro": "antojitos_mexicanos", "sinonimos": ["tlacoyos", "tlacoyo de haba", "tlacoyo de requeson"], "peso": 95},
    {"termino": "Pambazos de Papa con Chorizo", "subgiro": "antojitos_mexicanos", "sinonimos": ["pambazo", "pambazos"], "peso": 95},
    {"termino": "Flautas Doradas de Pollo y Res", "subgiro": "antojitos_mexicanos", "sinonimos": ["flautas", "tacos dorados", "flautas con crema y queso"], "peso": 90},
    {"termino": "Pozole Blanco y Rojo", "subgiro": "antojitos_mexicanos", "sinonimos": ["pozole", "plato de pozole", "pozoleria"], "peso": 95},
    {"termino": "Pancita / Menudo Caliente", "subgiro": "antojitos_mexicanos", "sinonimos": ["pancita", "menudo", "caldo de panza"], "peso": 95},
    {"termino": "Chicharrones Preparados con Cueritos", "subgiro": "antojitos_mexicanos", "sinonimos": ["chicharron preparado", "chicharron con cueritos y crema"], "peso": 95},
    {"termino": "Dorilocos con Cueritos y Cacahuates", "subgiro": "antojitos_mexicanos", "sinonimos": ["dorilocos", "tostilocos", "papalocas"], "peso": 90},

    # --- tamales_atole ---
    {"termino": "Tamales Oaxaqueños en Hoja de Plátano", "subgiro": "tamales_atole", "sinonimos": ["tamal oaxaqueño", "tamales oaxaqueños de mole"], "peso": 95},
    {"termino": "Tamales Verdes y de Mole en Hoja de Maíz", "subgiro": "tamales_atole", "sinonimos": ["tamal verde", "tamal de mole", "tamales", "guajolota"], "peso": 100},
    {"termino": "Tamales de Dulce con Pasas", "subgiro": "tamales_atole", "sinonimos": ["tamal de dulce", "tamal rosa"], "peso": 90},
    {"termino": "Atole de Champurrado", "subgiro": "tamales_atole", "sinonimos": ["champurrado", "atole de chocolate"], "peso": 95},
    {"termino": "Atole de Arroz con Leche", "subgiro": "tamales_atole", "sinonimos": ["atole blanco", "arroz con leche"], "peso": 90},
    {"termino": "Atole de Guayaba y Fresa", "subgiro": "tamales_atole", "sinonimos": ["atole de frutas", "atole de guayaba"], "peso": 85},

    # --- cocina_economica_fonda ---
    {"termino": "Comida Corrida del Día", "subgiro": "cocina_economica_fonda", "sinonimos": ["comida corrida", "fonda", "menu del dia", "tres tiempos"], "peso": 95},
    {"termino": "Milanesa de Res con Ensalada y Papas", "subgiro": "cocina_economica_fonda", "sinonimos": ["milanesa con papas", "guisado de milanesa"], "peso": 90},
    {"termino": "Chiles Rellenos de Queso", "subgiro": "cocina_economica_fonda", "sinonimos": ["chile relleno", "chile capeado"], "peso": 90},
    {"termino": "Enchiladas Verdes y Suizas", "subgiro": "cocina_economica_fonda", "sinonimos": ["enchiladas", "enchiladas verdes con pollo"], "peso": 90},
    {"termino": "Mole con Pollo y Arroz", "subgiro": "cocina_economica_fonda", "sinonimos": ["mole con pollo", "mole poblano"], "peso": 90},

    # --- torteria ---
    {"termino": "Tortas Gigantes Chilangas", "subgiro": "torteria", "sinonimos": ["torta", "tortas", "torta cubana", "torta de pierna", "torta de milanesa"], "peso": 100},
    {"termino": "Tortas de Chilaquiles (Tecolotas)", "subgiro": "torteria", "sinonimos": ["torta de chilaquiles", "tecolota"], "peso": 95},
    {"termino": "Torta Ahogada", "subgiro": "torteria", "sinonimos": ["torta ahogada jalisciense"], "peso": 80},

    # --- cafeteria_fuente_sodas ---
    {"termino": "Aguas Frescas de Frutas Naturales", "subgiro": "cafeteria_fuente_sodas", "sinonimos": ["aguas frescas", "agua de horchata", "agua de jamaica", "agua de limon con chia"], "peso": 100},
    {"termino": "Jugos Naturales y Antigripales", "subgiro": "cafeteria_fuente_sodas", "sinonimos": ["jugo verde", "jugo de naranja", "jugo de toronja", "antigripal"], "peso": 95},
    {"termino": "Licuados de Frutas con Leche", "subgiro": "cafeteria_fuente_sodas", "sinonimos": ["licuado", "licuados", "licuado de platano", "licuado de fresa", "chocomilk"], "peso": 95},
    {"termino": "Café de Olla con Canela y Piloncillo", "subgiro": "cafeteria_fuente_sodas", "sinonimos": ["cafe de olla", "jarrito de cafe"], "peso": 90},

    # --- elotes_esquites_botaneros ---
    {"termino": "Elotes Hervidos con Mayonesa y Queso", "subgiro": "elotes_esquites_botaneros", "sinonimos": ["elote", "elotes", "elote preparado", "elote con chile"], "peso": 100},
    {"termino": "Esquites Calientes con Tuétano", "subgiro": "elotes_esquites_botaneros", "sinonimos": ["esquites", "esquite con tuetano", "vaso de esquites"], "peso": 100},
    {"termino": "Elotes Asados al Carbón", "subgiro": "elotes_esquites_botaneros", "sinonimos": ["elote asado", "elotes a las brasas"], "peso": 90},

    # --- postres_reposteria ---
    {"termino": "Fresas con Crema y Granola", "subgiro": "postres_reposteria", "sinonimos": ["fresas con crema", "vaso de fresas con crema"], "peso": 90},
    {"termino": "Gelatinas Artísticas de Leche y Agua", "subgiro": "postres_reposteria", "sinonimos": ["gelatina", "gelatinas", "gelatina de mosaico"], "peso": 85},
    {"termino": "Plátanos Fritos con Crema y Lechera", "subgiro": "postres_reposteria", "sinonimos": ["platanos machos fritos", "platanos con lechera"], "peso": 85},
    {"termino": "Buñuelos de Viento con Miel de Piloncillo", "subgiro": "postres_reposteria", "sinonimos": ["buñuelos", "buñuelo crujiente"], "peso": 85},

    # --- paleteria_helados ---
    {"termino": "Nieves Artesanales de Garrafa", "subgiro": "paleteria_helados", "sinonimos": ["nieve", "nieves de garrafa", "nieve de limon", "nieve de mamey"], "peso": 95},
    {"termino": "Paletas de Hielo de Agua y Leche", "subgiro": "paleteria_helados", "sinonimos": ["paleta de hielo", "paletas michoacanas"], "peso": 90},

    # =========================================================================
    # CAT_ROPA_CALZADO_TEXTIL: Ropa, Calzado, Telas y Accesorios
    # =========================================================================

    # --- ropa_paca_segunda (Paca y Ropa de Segunda Mano) ---
    {"termino": "Ropa de Paca Americana", "subgiro": "ropa_paca_segunda", "sinonimos": ["ropa de paca", "paca americana", "paca", "ropa usada", "segunda mano"], "peso": 100},
    {"termino": "Chamarras de Pluma y Rompevientos Usadas", "subgiro": "ropa_paca_segunda", "sinonimos": ["chamarras de paca", "rompevientos vintage", "chamarras north face paca"], "peso": 95},
    {"termino": "Sudaderas con Capucha Americanas (Hoodies)", "subgiro": "ropa_paca_segunda", "sinonimos": ["sudaderas de paca", "hoodie vintage", "sudadera oversize"], "peso": 95},
    {"termino": "Pantalones de Mezclilla Vintage Levi's", "subgiro": "ropa_paca_segunda", "sinonimos": ["levis vintage", "jeans de paca", "mezclilla usada"], "peso": 95},
    {"termino": "Playeras Gráficas y de Bandas Retro", "subgiro": "ropa_paca_segunda", "sinonimos": ["playeras de bandas", "playeras vintage", "t-shirt retro"], "peso": 90},
    {"termino": "Jerseys Deportivos Vintage (NBA, NFL, Fútbol)", "subgiro": "ropa_paca_segunda", "sinonimos": ["jersey de basquetbol", "jerseys vintage", "camisetas deportivas"], "peso": 90},
    {"termino": "Abrigos de Lana y Gabardinas de Paca", "subgiro": "ropa_paca_segunda", "sinonimos": ["abrigos de segunda", "gabardinas vintage"], "peso": 85},

    # --- venta_ropa (Ropa Nueva) ---
    {"termino": "Pantalones de Mezclilla Nuevos", "subgiro": "venta_ropa", "sinonimos": ["pantalones de mezclilla", "jeans", "pantalones vaqueros"], "peso": 95},
    {"termino": "Playeras Lisas y Estampadas Nuevas", "subgiro": "venta_ropa", "sinonimos": ["playeras", "camisetas", "playeras de moda"], "peso": 90},
    {"termino": "Sudaderas con Gorro Nuevas", "subgiro": "venta_ropa", "sinonimos": ["sudaderas", "sudadera con cierre"], "peso": 90},
    {"termino": "Chamarras Térmicas e Impermeables", "subgiro": "venta_ropa", "sinonimos": ["chamarras", "chamarra de invierno"], "peso": 90},
    {"termino": "Vestidos Casuales y de Fiesta", "subgiro": "venta_ropa", "sinonimos": ["vestidos", "vestido para dama"], "peso": 85},
    {"termino": "Blusas y Camisas para Caballero", "subgiro": "venta_ropa", "sinonimos": ["blusas", "camisas de vestir", "camisa casual"], "peso": 85},
    {"termino": "Pants Deportivos y Shorts", "subgiro": "venta_ropa", "sinonimos": ["pants", "ropa deportiva", "shorts"], "peso": 85},
    {"termino": "Trajes de Baño y Ropa Playera", "subgiro": "venta_ropa", "sinonimos": ["traje de baño", "bikini", "bermudas"], "peso": 80},
    {"termino": "Pijamas Térmicas Abrigadoras", "subgiro": "venta_ropa", "sinonimos": ["pijamas", "mamelucos", "pijama polar"], "peso": 85},

    # --- zapateria_calzado (Calzado, Tenis y Zapatos) ---
    {"termino": "Tenis Deportivos de Marca (Nike, Adidas, Jordan)", "subgiro": "zapateria_calzado", "sinonimos": ["tenis", "sneakers", "tenis nike", "tenis jordan", "zapatillas"], "peso": 100},
    {"termino": "Tenis Casuales de Lona (Converse, Vans)", "subgiro": "zapateria_calzado", "sinonimos": ["tenis de bota", "tenis de lona", "choclos"], "peso": 95},
    {"termino": "Zapatos Escolares de Piel", "subgiro": "zapateria_calzado", "sinonimos": ["zapatos escolares", "zapato negro para escuela", "calzado infantil"], "peso": 90},
    {"termino": "Botines y Botas de Moda para Dama", "subgiro": "zapateria_calzado", "sinonimos": ["botines", "botas de tacon", "botas vaqueras"], "peso": 85},
    {"termino": "Botas de Trabajo con Casquillo", "subgiro": "zapateria_calzado", "sinonimos": ["botas industriales", "botas con casquillo", "calzado de seguridad"], "peso": 90},
    {"termino": "Chanclas de Baño y Sandalias", "subgiro": "zapateria_calzado", "sinonimos": ["chanclas", "sandalias", "pata de gallo", "crocs"], "peso": 90},
    {"termino": "Pantuflas de Peluche Abrigadoras", "subgiro": "zapateria_calzado", "sinonimos": ["pantuflas", "zapatillas de descanso"], "peso": 80},

    # --- lenceria_boneteria ---
    {"termino": "Calcetines y Tines por Paquete", "subgiro": "lenceria_boneteria", "sinonimos": ["calcetines", "tines", "docena de calcetines"], "peso": 95},
    {"termino": "Bóxers de Algodón y Trusas", "subgiro": "lenceria_boneteria", "sinonimos": ["boxer", "calzones", "ropa interior de hombre"], "peso": 95},
    {"termino": "Brasieres y Tops Deportivos", "subgiro": "lenceria_boneteria", "sinonimos": ["brasier", "sosten", "top deportivo"], "peso": 90},
    {"termino": "Medias de Licra y Mallas Térmicas", "subgiro": "lenceria_boneteria", "sinonimos": ["medias", "mallas", "leggins"], "peso": 85},
    {"termino": "Camisetas Interiores de Algodón", "subgiro": "lenceria_boneteria", "sinonimos": ["camiseta de tirantes", "playera interior"], "peso": 85},

    # --- telas_blancos (Cobijas, Sábanas y Toallas) ---
    {"termino": "Cobijas San Marcos y Frazadas Térmicas", "subgiro": "telas_blancos", "sinonimos": ["cobija", "cobijas con tigre", "cobertor", "cobija polar"], "peso": 95},
    {"termino": "Sábanas Matrimoniales e Individuales", "subgiro": "telas_blancos", "sinonimos": ["juego de sabanas", "sabanas de algodon", "sabanas termicas"], "peso": 90},
    {"termino": "Toallas de Baño Absorbentes", "subgiro": "telas_blancos", "sinonimos": ["toalla", "toallas de medio baño", "toallitas"], "peso": 90},
    {"termino": "Cortinas Decorativas para Hogar", "subgiro": "telas_blancos", "sinonimos": ["cortinas", "cortinero", "cortinas blackout"], "peso": 85},
    {"termino": "Manteles de Hule para Mesa por Metro", "subgiro": "telas_blancos", "sinonimos": ["mantel de hule", "plastico para mesa"], "peso": 85},
    {"termino": "Colchas Acolchadas y Edredones", "subgiro": "telas_blancos", "sinonimos": ["edredon", "colcha", "cubrecama"], "peso": 85},

    # --- bolsos_mochilas ---
    {"termino": "Mochilas Escolares Reforzadas", "subgiro": "bolsos_mochilas", "sinonimos": ["mochila", "mochilas con llantitas", "mochilas juveniles"], "peso": 95},
    {"termino": "Bolsas de Mano para Dama", "subgiro": "bolsos_mochilas", "sinonimos": ["bolsa de mujer", "bolso", "crossbody"], "peso": 90},
    {"termino": "Cangureras y Mariconeras Urbanas", "subgiro": "bolsos_mochilas", "sinonimos": ["cangurera", "mariconera", "pechera"], "peso": 90},
    {"termino": "Maletas de Viaje con Ruedas", "subgiro": "bolsos_mochilas", "sinonimos": ["maleta", "equipaje de mano", "petate"], "peso": 85},
    {"termino": "Carteras y Billeteras de Piel", "subgiro": "bolsos_mochilas", "sinonimos": ["cartera", "monedero", "billetera"], "peso": 85},
    {"termino": "Cinturones de Piel y Reata", "subgiro": "bolsos_mochilas", "sinonimos": ["cinturon", "cinto", "cinturon vaquero"], "peso": 85},

    # =========================================================================
    # CAT_HOGAR_FERRETERIA: Artículos del Hogar, Ferretería y Limpieza
    # =========================================================================

    # --- ferreteria_tlapaleria (Herramientas, Tornillos y Electricidad) ---
    {"termino": "Clavos para Madera y Concreto", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["clavos", "clavo con cabeza", "kilo de clavos"], "peso": 95},
    {"termino": "Tornillos, Tuercas y Pijas", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["tornillos", "pijas para tablaroca", "tuerca"], "peso": 90},
    {"termino": "Martillos de Uña y Macetas", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["martillo", "marro", "mazo de fierro"], "peso": 90},
    {"termino": "Desarmadores de Cruz y Planos", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["desarmador", "destornilladores", "puntas"], "peso": 90},
    {"termino": "Pinzas de Chofer y de Electricista", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["pinzas", "alicates", "pinzas de presion"], "peso": 90},
    {"termino": "Cinta de Aislar y Cinta Canela", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["cinta de aislar", "cinta canela", "cinta de aislar 3m", "diurex"], "peso": 90},
    {"termino": "Extensiones Eléctricas y Multicontactos", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["extension electrica", "multicontacto", "barra de enchufes"], "peso": 90},
    {"termino": "Focos LED Ahorradores", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["focos", "foco led", "bombilla led luz blanca"], "peso": 95},
    {"termino": "Candados de Seguridad con Llave de Puntos", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["candado", "candados", "candado hermex"], "peso": 90},
    {"termino": "Mangueras de Jardín Reforzadas", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["manguera", "manguera de media"], "peso": 85},
    {"termino": "Llaves de Paso y Conexiones de Agua", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["llave de paso", "cespol", "cinta teflon", "tubos cpvc"], "peso": 85},
    {"termino": "Alambre Recocido y Galvanizado", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["alambre", "rollo de alambre"], "peso": 85},
    {"termino": "Brochas para Pintar y Rodillos", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["brocha", "rodillo", "charola para pintar"], "peso": 85},
    {"termino": "Thinner y Aguarrás", "subgiro": "ferreteria_tlapaleria", "sinonimos": ["solvente", "thinner americano", "aguarras"], "peso": 80},

    # --- jarcieria_productos_limpieza ---
    {"termino": "Escobas de Mijo y Cepillos de Plástico", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["escoba", "escobas", "cepillo de barrer"], "peso": 95},
    {"termino": "Trapeadores de Microfibra y Algodón", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["trapeador", "mechudo", "trapeador de hilo"], "peso": 95},
    {"termino": "Jergas de Algodón Gruesas por Metro", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["jerga", "jergas", "trapo de piso"], "peso": 95},
    {"termino": "Cubetas de Plástico con Asa", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["cubeta", "cubetas de 19 litros", "bote con asa"], "peso": 90},
    {"termino": "Jabón Zote en Barra (Rosa y Blanco)", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["jabon zote", "zote", "jabon de barra"], "peso": 100},
    {"termino": "Jabón Roma y Foca en Polvo", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["detergente en polvo", "jabon roma", "jabon foca"], "peso": 95},
    {"termino": "Cloro Líquido a Granel por Litro", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["cloro", "blanqueador", "cloro concentrado"], "peso": 95},
    {"termino": "Limpiador tipo Fabuloso y Aromatizante", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["fabuloso", "limpiapisos", "aromatizante de lavanda"], "peso": 95},
    {"termino": "Pinol Desinfectante Concentrado", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["pinol", "aceite de pino"], "peso": 90},
    {"termino": "Fibras Verdes y Esponjas para Trastes", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["fibra para trastes", "esponja scotch brite"], "peso": 90},
    {"termino": "Guantes de Látex para Limpieza", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["guantes de hule", "guantes amarillos"], "peso": 85},
    {"termino": "Pastillas Desodorantes para Baño", "subgiro": "jarcieria_productos_limpieza", "sinonimos": ["pastillas de baño", "canastilla desodorante"], "peso": 80},

    # --- plasticos_enseres_hogar ---
    {"termino": "Topers Herméticos para Comida", "subgiro": "plasticos_enseres_hogar", "sinonimos": ["topers", "tupperware", "recipientes plasticos", "portaviandas"], "peso": 95},
    {"termino": "Platos, Vasos y Jarras de Plástico", "subgiro": "plasticos_enseres_hogar", "sinonimos": ["vajilla de plastico", "jarras plasticas"], "peso": 90},
    {"termino": "Botes de Basura con Tapa Balancín", "subgiro": "plasticos_enseres_hogar", "sinonimos": ["bote de basura", "cesto de basura"], "peso": 90},
    {"termino": "Ganchos de Plástico para Ropa por Docena", "subgiro": "plasticos_enseres_hogar", "sinonimos": ["ganchos de ropa", "ganchos plasticos"], "peso": 90},
    {"termino": "Cestos para Ropa Sucia y Palanganas", "subgiro": "plasticos_enseres_hogar", "sinonimos": ["cesto de ropa", "tina de plastico", "palangana"], "peso": 85},
    {"termino": "Tablas de Picar y Coladores", "subgiro": "plasticos_enseres_hogar", "sinonimos": ["tabla de picar", "colador de cocina"], "peso": 85},
    {"termino": "Sartenes Antiadherentes y Peltre", "subgiro": "plasticos_enseres_hogar", "sinonimos": ["sarten", "sartenes", "pocillo de peltre"], "peso": 90},
    {"termino": "Cuchillos de Cocina con Filo", "subgiro": "plasticos_enseres_hogar", "sinonimos": ["cuchillo", "cuchillos chef", "pelador"], "peso": 85},
    {"termino": "Cubiertos de Acero Inoxidable", "subgiro": "plasticos_enseres_hogar", "sinonimos": ["cucharas", "tenedores", "juego de cubiertos"], "peso": 85},

    # --- floreria_plantas ---
    {"termino": "Plantas de Ornato y Suculentas", "subgiro": "floreria_plantas", "sinonimos": ["plantas", "suculentas", "helechos", "cunas de moises", "cactus"], "peso": 95},
    {"termino": "Flores Frescas en Ramo (Rosas, Girasoles)", "subgiro": "floreria_plantas", "sinonimos": ["flores", "rosas", "girasoles", "ramos de flores", "nochebuenas"], "peso": 95},
    {"termino": "Macetas de Barro y Plástico", "subgiro": "floreria_plantas", "sinonimos": ["maceta", "macetas", "jardineras"], "peso": 85},
    {"termino": "Tierra Preparada con Hoja para Macetas", "subgiro": "floreria_plantas", "sinonimos": ["tierra para maceta", "tierra de hoja", "sustrato"], "peso": 85},
    {"termino": "Abono Orgánico y Fertilizantes", "subgiro": "floreria_plantas", "sinonimos": ["abono", "fertilizante", "humus de lombriz"], "peso": 80},

    # --- mascotas_alimento ---
    {"termino": "Croquetas para Perro por Kilo a Granel", "subgiro": "mascotas_alimento", "sinonimos": ["croquetas de perro", "alimento de perro", "pedigree suelto"], "peso": 95},
    {"termino": "Alimento para Gato en Croquetas y Sobres", "subgiro": "mascotas_alimento", "sinonimos": ["croquetas para gato", "whiskas", "comida de gato"], "peso": 90},
    {"termino": "Alpiste y Semillas para Aves", "subgiro": "mascotas_alimento", "sinonimos": ["alpiste", "comida para periquitos", "semillas para canario"], "peso": 85},
    {"termino": "Correas, Pecheras y Collares para Perro", "subgiro": "mascotas_alimento", "sinonimos": ["collar para perro", "correa", "pechera"], "peso": 85},
    {"termino": "Juguetes Masticables y Premios para Mascotas", "subgiro": "mascotas_alimento", "sinonimos": ["carnazas", "premios para perro", "pelotas para perro"], "peso": 80},
    {"termino": "Camas y Colchonetas para Mascotas", "subgiro": "mascotas_alimento", "sinonimos": ["cama de perro", "colchoneta para gato"], "peso": 80},

    # =========================================================================
    # CAT_SALUD_BELLEZA: Salud, Cuidado Personal y Belleza
    # =========================================================================

    # --- herbolaria_esoterismo (Hierbas Medicinales, Pomadas y Esoterismo) ---
    {"termino": "Árnica Mexicana en Flor y Pomada", "subgiro": "herbolaria_esoterismo", "sinonimos": ["arnica", "pomada de arnica", "arnica para golpes"], "peso": 95},
    {"termino": "Manzanilla Seca para Té Digestivo", "subgiro": "herbolaria_esoterismo", "sinonimos": ["manzanilla", "flores de manzanilla"], "peso": 90},
    {"termino": "Cuachalalate para Gastritis", "subgiro": "herbolaria_esoterismo", "sinonimos": ["cuachalalate", "corteza de cuachalalate"], "peso": 90},
    {"termino": "Té de Tila y Valeriana Relajante", "subgiro": "herbolaria_esoterismo", "sinonimos": ["tila", "valeriana", "te para los nervios"], "peso": 85},
    {"termino": "Hierba del Sapo para Colesterol", "subgiro": "herbolaria_esoterismo", "sinonimos": ["hierba del sapo", "planta del sapo"], "peso": 85},
    {"termino": "Hojas de Sen y Boldo Depurativo", "subgiro": "herbolaria_esoterismo", "sinonimos": ["hojas de sen", "boldo para el higado"], "peso": 80},
    {"termino": "Pomada de Caléndula y Manzana", "subgiro": "herbolaria_esoterismo", "sinonimos": ["pomada de calendula", "pomada de la campana"], "peso": 85},
    {"termino": "Veladoras Aromáticas y Esotéricas", "subgiro": "herbolaria_esoterismo", "sinonimos": ["veladora", "veladoras", "cirio", "veladora abre caminos"], "peso": 90},
    {"termino": "Copal, Mirra e Inciensos en Varita", "subgiro": "herbolaria_esoterismo", "sinonimos": ["incienso", "copal", "inciensos aromaticos"], "peso": 90},
    {"termino": "Lociones Esotéricas y de Romero", "subgiro": "herbolaria_esoterismo", "sinonimos": ["locion 7 machos", "agua de rosas", "locion de ruda"], "peso": 85},
    {"termino": "Pulseras Rojas de Ojo de Venado", "subgiro": "herbolaria_esoterismo", "sinonimos": ["ojo de venado", "amuleto", "pulsera roja contra envidia"], "peso": 85},

    # --- cosmeticos_perfumeria ---
    {"termino": "Labiales Indelebles y Brillos Labiales", "subgiro": "cosmeticos_perfumeria", "sinonimos": ["labiales", "pintalabios", "gloss"], "peso": 90},
    {"termino": "Rímel con Fibras para Pestañas", "subgiro": "cosmeticos_perfumeria", "sinonimos": ["rimel", "mascara de pestañas", "rimel de hueso de mamey"], "peso": 90},
    {"termino": "Sombras de Ojos y Rubores", "subgiro": "cosmeticos_perfumeria", "sinonimos": ["paleta de sombras", "maquillaje", "rubor"], "peso": 85},
    {"termino": "Esmaltes de Uñas y Gelish", "subgiro": "cosmeticos_perfumeria", "sinonimos": ["barniz de uñas", "esmaltes", "gelish"], "peso": 85},
    {"termino": "Cremas Faciales de Concha Nácar y Sábila", "subgiro": "cosmeticos_perfumeria", "sinonimos": ["crema concha nacar", "crema de sabila", "humectante"], "peso": 85},
    {"termino": "Perfumes de Equivalencia e Inspiración", "subgiro": "cosmeticos_perfumeria", "sinonimos": ["perfumes fraiche", "perfumes en contratipo", "fragancias"], "peso": 90},
    {"termino": "Desodorantes en Barra y Aerosol", "subgiro": "cosmeticos_perfumeria", "sinonimos": ["desodorante", "antitranspirante"], "peso": 85},
    {"termino": "Shampoo Artesanal de Chile y Biotina", "subgiro": "cosmeticos_perfumeria", "sinonimos": ["shampoo de chile", "shampoo anticaida", "shampoo suelto"], "peso": 85},
    {"termino": "Jabones Artesanales de Avena y Miel", "subgiro": "cosmeticos_perfumeria", "sinonimos": ["jabon de avena", "jabon neutro", "jabon de azufre"], "peso": 85},
    {"termino": "Toallitas Desmaquillantes Húmedas", "subgiro": "cosmeticos_perfumeria", "sinonimos": ["toallitas humedas", "desmaquillante"], "peso": 80},

    # --- estetica_peluqueria ---
    {"termino": "Corte de Cabello Económico Dama y Caballero", "subgiro": "estetica_peluqueria", "sinonimos": ["corte de cabello", "peluquero", "degrafilado"], "peso": 90},
    {"termino": "Tintes para Cabello y Decolorantes", "subgiro": "estetica_peluqueria", "sinonimos": ["tinte para pelo", "peroxido", "cubrecana"], "peso": 85},
    {"termino": "Planchas y Secadoras de Pelo", "subgiro": "estetica_peluqueria", "sinonimos": ["plancha de cabello", "secadora"], "peso": 80},

    # --- optica_lentes ---
    {"termino": "Lentes para Lectura con Graduación", "subgiro": "optica_lentes", "sinonimos": ["lentes para vista cansada", "lentes graduados economicos"], "peso": 90},
    {"termino": "Lentes de Sol Polarizados UV", "subgiro": "optica_lentes", "sinonimos": ["gafas de sol", "lentes oscuros", "lentes polarizados"], "peso": 90},
    {"termino": "Estuches y Microfibras para Lentes", "subgiro": "optica_lentes", "sinonimos": ["estuche de lentes", "limpiador de gafas"], "peso": 75},

    # --- farmacia_botica ---
    {"termino": "Alcohol Etílico al 70%", "subgiro": "farmacia_botica", "sinonimos": ["alcohol", "alcohol de curacion", "bote de alcohol"], "peso": 90},
    {"termino": "Agua Oxigenada y Antisépticos", "subgiro": "farmacia_botica", "sinonimos": ["agua oxigenada", "mertiolate", "yodo"], "peso": 85},
    {"termino": "Algodón Plisado y Gasas Estériles", "subgiro": "farmacia_botica", "sinonimos": ["algodon", "gasas", "vendas"], "peso": 85},
    {"termino": "Curitas Adhesivas y Micropore", "subgiro": "farmacia_botica", "sinonimos": ["curitas", "cinta micropore", "parches"], "peso": 85},
    {"termino": "Paracetamol e Ibuprofeno Genéricos", "subgiro": "farmacia_botica", "sinonimos": ["paracetamol", "ibuprofeno", "aspirina"], "peso": 85},
    {"termino": "Vida Suero Oral en Polvo", "subgiro": "farmacia_botica", "sinonimos": ["suero oral", "electrolitos en polvo"], "peso": 85},

    # =========================================================================
    # CAT_BAZAR_CHACHARAS: Chácharas, Segunda Mano y Comercio Mixto
    # =========================================================================

    # --- chacharas_segunda_mano (Chácharas, Herramientas Usadas, Vinilos) ---
    {"termino": "Chácharas Surtidas a Granel", "subgiro": "chacharas_segunda_mano", "sinonimos": ["chacharas", "chacharear", "chachara", "chacharitas", "curiosidades"], "peso": 100},
    {"termino": "Herramientas de Segunda Mano", "subgiro": "chacharas_segunda_mano", "sinonimos": ["herramienta usada", "llaves españolas usadas", "dados usados"], "peso": 95},
    {"termino": "Taladros y Pulidoras Usadas", "subgiro": "chacharas_segunda_mano", "sinonimos": ["taladro usado", "rotomartillo de uso", "esmeriladora usada"], "peso": 90},
    {"termino": "Discos de Vinilo LP (Rock, Cumbia, Salsa)", "subgiro": "chacharas_segunda_mano", "sinonimos": ["acetatos", "discos de vinil", "lps", "vinilos retro", "chopo vinilos"], "peso": 95},
    {"termino": "Cassettes de Audio y Walkmans", "subgiro": "chacharas_segunda_mano", "sinonimos": ["casetes", "caset", "walkman", "reproductor de cassette"], "peso": 85},
    {"termino": "Libros Usados y Enciclopedias", "subgiro": "chacharas_segunda_mano", "sinonimos": ["libros viejos", "libros de segunda mano", "novelas usadas"], "peso": 90},
    {"termino": "Cómics, Mangas y Revistas Vintage", "subgiro": "chacharas_segunda_mano", "sinonimos": ["comics retro", "historietas de coleccion", "mangas usados"], "peso": 90},
    {"termino": "Juguetes Coleccionables y Hot Wheels", "subgiro": "chacharas_segunda_mano", "sinonimos": ["hot wheels sueltos", "carritos usados", "juguetes retro"], "peso": 95},
    {"termino": "Figuras de Acción y Anime (Dragon Ball, Marvel)", "subgiro": "chacharas_segunda_mano", "sinonimos": ["figuras de accion", "muñecos de coleccion", "goku", "marvel legends"], "peso": 95},
    {"termino": "Videojuegos Retro (Nintendo, PlayStation, Xbox)", "subgiro": "chacharas_segunda_mano", "sinonimos": ["videojuegos retro", "cartuchos de nintendo", "juegos de play 2"], "peso": 95},
    {"termino": "Consolas de Videojuegos Usadas", "subgiro": "chacharas_segunda_mano", "sinonimos": ["consola retro", "nintendo usado", "game boy", "xbox 360"], "peso": 90},
    {"termino": "Relojes de Pulso Vintage Usados", "subgiro": "chacharas_segunda_mano", "sinonimos": ["relojes antiguos", "reloj casio vintage", "reloj mecanico"], "peso": 85},
    {"termino": "Lámparas Decorativas Retro", "subgiro": "chacharas_segunda_mano", "sinonimos": ["lamparas vintage", "lampara de mesa antigua"], "peso": 80},
    {"termino": "Artículos Militares y Chamarras Bomber", "subgiro": "chacharas_segunda_mano", "sinonimos": ["ropa militar", "chamarras camuflaje", "cantimplora militar"], "peso": 85},

    # --- antiguedades_coleccionismo ---
    {"termino": "Monedas Antiguas de Plata y Centenarios", "subgiro": "antiguedades_coleccionismo", "sinonimos": ["monedas antiguas", "plata mexicana", "pesos antiguos", "numismatica"], "peso": 95},
    {"termino": "Billetes Antiguos de Colección", "subgiro": "antiguedades_coleccionismo", "sinonimos": ["billetes revolucionarios", "billetes viejos"], "peso": 90},
    {"termino": "Cámaras Fotográficas Análogas 35mm", "subgiro": "antiguedades_coleccionismo", "sinonimos": ["camaras mecanicas", "camara de rollo", "canon vintage"], "peso": 90},
    {"termino": "Máquinas de Escribir Mecánicas", "subgiro": "antiguedades_coleccionismo", "sinonimos": ["maquina de escribir", "olivetti", "remington"], "peso": 85},
    {"termino": "Platería Antigua y Cobre Martillado", "subgiro": "antiguedades_coleccionismo", "sinonimos": ["plateria de taxco", "cobre de santa clara", "charolas de plata"], "peso": 85},
    {"termino": "Instrumentos Musicales Usados (Guitarras)", "subgiro": "antiguedades_coleccionismo", "sinonimos": ["guitarra acustica", "teclado usado", "ukelele"], "peso": 85},

    # --- comercio_mixto_general ---
    {"termino": "Pilas Alcalinas AA, AAA y de Botón", "subgiro": "comercio_mixto_general", "sinonimos": ["pilas", "baterias", "paquete de pilas duracell"], "peso": 90},
    {"termino": "Linternas Tácticas y Lámparas de Mano", "subgiro": "comercio_mixto_general", "sinonimos": ["linterna recargable", "lampara sorda"], "peso": 85},
    {"termino": "Paraguas Portátiles y Sombrillas de Tianguis", "subgiro": "comercio_mixto_general", "sinonimos": ["paraguas", "sombrilla para sol", "sombrilla grande"], "peso": 90},
    {"termino": "Lonas Impermeables para Toldos", "subgiro": "comercio_mixto_general", "sinonimos": ["lona azul", "lona para puesto", "toldo impermeable"], "peso": 90},
    {"termino": "Lazos, Mecates y Reatas para Amarre", "subgiro": "comercio_mixto_general", "sinonimos": ["mecate", "lazo plastico", "reata de tendedero"], "peso": 85},

    # =========================================================================
    # CAT_PAPELERIA_TECNOLOGIA: Papelería, Cómputo, Regalos y Juguetería
    # =========================================================================

    # --- reparacion_celulares (Accesorios Celulares y Tecnología Portátil) ---
    {"termino": "Cargadores Rápidos para Celular (Tipo C y Lightning)", "subgiro": "reparacion_celulares", "sinonimos": ["cargador de celular", "cubo cargador", "cargador rapido"], "peso": 95},
    {"termino": "Cables de Carga Reforzados para Celular", "subgiro": "reparacion_celulares", "sinonimos": ["cable tipo c", "cable para iphone", "cable usb"], "peso": 95},
    {"termino": "Fundas y Protectores de Celular", "subgiro": "reparacion_celulares", "sinonimos": ["funda de celular", "funda uso rudo", "protector de silicona"], "peso": 95},
    {"termino": "Micas de Cristal Templado Instaladas", "subgiro": "reparacion_celulares", "sinonimos": ["mica de cristal", "mica de privacidad", "protector de pantalla"], "peso": 95},
    {"termino": "Bocinas Portátiles Bluetooth con Luces", "subgiro": "reparacion_celulares", "sinonimos": ["bocina bluetooth", "bocina recargable", "bocina para fiesta"], "peso": 95},
    {"termino": "Audífonos Inalámbricos Bluetooth", "subgiro": "reparacion_celulares", "sinonimos": ["audifonos bluetooth", "airpods replica", "manos libres"], "peso": 95},
    {"termino": "Soportes de Celular para Carro y Moto", "subgiro": "reparacion_celulares", "sinonimos": ["soporte de celular", "base para auto"], "peso": 85},
    {"termino": "Memorias USB Flash y MicroSD", "subgiro": "reparacion_celulares", "sinonimos": ["memoria usb", "tarjeta micro sd", "pendrive"], "peso": 90},

    # --- papeleria_copias ---
    {"termino": "Cuadernos Profesionales Cosidos y Espiral", "subgiro": "papeleria_copias", "sinonimos": ["cuaderno", "libreta escolar", "cuaderno de raya", "cuaderno cuadro chico"], "peso": 90},
    {"termino": "Bolígrafos, Lápices y Plumas de Gel", "subgiro": "papeleria_copias", "sinonimos": ["plumas bic", "lapiz del no 2", "plumas de colores"], "peso": 90},
    {"termino": "Colores de Madera y Plumones Escolares", "subgiro": "papeleria_copias", "sinonimos": ["colores prismacolor", "plumones lavables", "crayolas"], "peso": 85},
    {"termino": "Cartulinas, Papel Bond y Hojas Blancas", "subgiro": "papeleria_copias", "sinonimos": ["hojas blancas paquete", "cartulina", "papel cascaron"], "peso": 85},
    {"termino": "Pegamento Blanco Líquido y en Barra (Pritt)", "subgiro": "papeleria_copias", "sinonimos": ["resistol", "pegamento en barra", "pritt"], "peso": 85},
    {"termino": "Tijeras Escolares y Sacapuntas de Metal", "subgiro": "papeleria_copias", "sinonimos": ["tijeras de punta roma", "sacapuntas"], "peso": 80},
    {"termino": "Lapiceras y Estuches Escolares", "subgiro": "papeleria_copias", "sinonimos": ["lapicera", "estuche para lapices"], "peso": 85},

    # --- jugueteria_novedades ---
    {"termino": "Carritos a Control Remoto y Pistas", "subgiro": "jugueteria_novedades", "sinonimos": ["carro a control remoto", "pistas de autos"], "peso": 90},
    {"termino": "Muñecas con Accesorios y Bebés", "subgiro": "jugueteria_novedades", "sinonimos": ["muñeca", "carriola de juguete", "bebe lloron"], "peso": 90},
    {"termino": "Juegos de Mesa Familiares (Turista, Lotería, Uno)", "subgiro": "jugueteria_novedades", "sinonimos": ["loteria mexicana", "turista mundial", "jenga", "baraja"], "peso": 90},
    {"termino": "Pelotas de Fútbol y Básquetbol Inflables", "subgiro": "jugueteria_novedades", "sinonimos": ["balon de futbol", "pelota de hule"], "peso": 85},
    {"termino": "Papalotes de Plástico con Hilo", "subgiro": "jugueteria_novedades", "sinonimos": ["papalote", "cometa"], "peso": 80},
    {"termino": "Juguetes Luminosos y Burbujas", "subgiro": "jugueteria_novedades", "sinonimos": ["burbujero", "espadas de luz"], "peso": 80},

    # --- regalos_bisuteria ---
    {"termino": "Cadenas y Aretes de Acero Inoxidable", "subgiro": "regalos_bisuteria", "sinonimos": ["cadenitas", "aretes", "joyeria quirurgica"], "peso": 90},
    {"termino": "Pulseras Tejidas de Hilo y Piedras", "subgiro": "regalos_bisuteria", "sinonimos": ["pulseras artesanales", "pulsera de cuarzo"], "peso": 85},
    {"termino": "Anillos de Plata y Fantasía Fina", "subgiro": "regalos_bisuteria", "sinonimos": ["anillo de compromiso fantasia", "anillos"], "peso": 85},
    {"termino": "Peluches Gigantes y Medianos", "subgiro": "regalos_bisuteria", "sinonimos": ["osito de peluche", "peluches de amor"], "peso": 85},
    {"termino": "Bolsas de Regalo y Envolturas", "subgiro": "regalos_bisuteria", "sinonimos": ["bolsa de regalo", "papel de regalo", "moños"], "peso": 80},

    # --- artesanias_manualidades ---
    {"termino": "Alebrijes Tallados en Madera Pintados a Mano", "subgiro": "artesanias_manualidades", "sinonimos": ["alebrije", "alebrijes de oaxaca"], "peso": 90},
    {"termino": "Barro Negro y Talavera Poblana", "subgiro": "artesanias_manualidades", "sinonimos": ["artesanias de barro", "talavera", "platos de talavera"], "peso": 85},
    {"termino": "Rebozos Tradicionales de Telar", "subgiro": "artesanias_manualidades", "sinonimos": ["rebozo", "rebozos mexicanos"], "peso": 85},
    {"termino": "Sombreros de Palma y Charros", "subgiro": "artesanias_manualidades", "sinonimos": ["sombrero de paja", "sombreros campesinos"], "peso": 85},
    {"termino": "Figuras de Estambre y Amigurumi", "subgiro": "artesanias_manualidades", "sinonimos": ["muñecos tejidos", "amigurumis"], "peso": 80},

    # =========================================================================
    # CAT_OFICIOS_SERVICIOS: Oficios Tradicionales y Reparaciones Barriales
    # =========================================================================

    # --- reparacion_calzado ---
    {"termino": "Cambio de Suelas para Zapatos y Tenis", "subgiro": "reparacion_calzado", "sinonimos": ["reparadora de calzado", "cambio de suela", "suelas corrida"], "peso": 90},
    {"termino": "Colocación de Tapas para Tacones", "subgiro": "reparacion_calzado", "sinonimos": ["tapas de tacón", "reparacion de tacones"], "peso": 85},
    {"termino": "Costura y Pegado de Tenis y Mochilas", "subgiro": "reparacion_calzado", "sinonimos": ["coser tenis", "pegar tenis despegados"], "peso": 85},
    {"termino": "Grasa y Tinta para Calzado de Piel", "subgiro": "reparacion_calzado", "sinonimos": ["grasa de zapato", "bolear zapatos", "tinta negra calzado"], "peso": 80},

    # --- taller_costura_sastreria ---
    {"termino": "Ajuste de Dobladillo y Bastilla de Pantalón", "subgiro": "taller_costura_sastreria", "sinonimos": ["dobladillo", "bastilla", "ajuste de pantalon"], "peso": 90},
    {"termino": "Cambio de Cierres para Chamarras y Mochilas", "subgiro": "taller_costura_sastreria", "sinonimos": ["cambio de cierre", "cierre descompuesto", "sastre"], "peso": 90},
    {"termino": "Remiendos y Zurcido de Ropa", "subgiro": "taller_costura_sastreria", "sinonimos": ["zurcido invisible", "poner parches"], "peso": 85},

    # --- cerrajeria ---
    {"termino": "Duplicado de Llaves Estándar para Casa", "subgiro": "cerrajeria", "sinonimos": ["copia de llaves", "cerrajero", "sacar llaves"], "peso": 95},
    {"termino": "Duplicado de Llaves de Seguridad y Puntos", "subgiro": "cerrajeria", "sinonimos": ["llaves de seguridad", "llave de puntos", "llave tetra"], "peso": 90},
    {"termino": "Copia de Llaves para Automóvil con Chip", "subgiro": "cerrajeria", "sinonimos": ["llave de auto", "llave con chip carro"], "peso": 85},

    # --- reparacion_electrodomesticos ---
    {"termino": "Reparación de Licuadoras y Aspas", "subgiro": "reparacion_electrodomesticos", "sinonimos": ["reparar licuadora", "aspas oster", "cople de licuadora"], "peso": 90},
    {"termino": "Refacciones y Cable para Planchas", "subgiro": "reparacion_electrodomesticos", "sinonimos": ["reparar plancha", "cable de plancha"], "peso": 85},
    {"termino": "Reparación de Ventiladores de Pedestal", "subgiro": "reparacion_electrodomesticos", "sinonimos": ["reparar ventilador", "motor de ventilador"], "peso": 85},

    # --- taller_bicicletas ---
    {"termino": "Parche de Cámaras y Vulcanizado de Llanta de Bici", "subgiro": "taller_bicicletas", "sinonimos": ["parchar llanta de bici", "ponchadura de bicicleta"], "peso": 90},
    {"termino": "Cámaras para Bicicleta Rodadas 20 a 29", "subgiro": "taller_bicicletas", "sinonimos": ["camaras de bici", "camara r26", "camara r29"], "peso": 85},
    {"termino": "Ajuste de Frenos y Cambios de Bicicleta", "subgiro": "taller_bicicletas", "sinonimos": ["frenos de bicicleta", "engrasado de cadena bici"], "peso": 85}
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
            'popular_tags': ['frutas', 'verduras', 'carnes', 'pescados', 'cremeria', 'abarrotes', 'antojitos']
        }

    # Tianguis Semanales: Mixto, Canasta Básica, Ropa de Paca y Chácharas
    if space_type == 'Tianguis':
        # Tianguis especializados emblemáticos
        if 'CHOPO' in norm_nom:
            return {
                'categorias': ['CAT_ROPA_CALZADO_TEXTIL', 'CAT_BAZAR_CHACHARAS', 'CAT_PAPELERIA_TECNOLOGIA'],
                'subgiros': ['ropa_paca_segunda', 'venta_ropa', 'chacharas_segunda_mano', 'antiguedades_coleccionismo', 'regalos_bisuteria'],
                'canasta_basica': False,
                'mercomuna': False,
                'popular_tags': ['rock', 'vinilos', 'ropa negra', 'chacharas', 'coleccionismo', 'musica']
            }
        if 'SALADO' in norm_nom:
            return {
                'categorias': ['CAT_ROPA_CALZADO_TEXTIL', 'CAT_BAZAR_CHACHARAS', 'CAT_HOGAR_FERRETERIA', 'CAT_COMIDA_PREPARADA', 'CAT_ALIM_FRESCOS'],
                'subgiros': ['ropa_paca_segunda', 'chacharas_segunda_mano', 'ferreteria_tlapaleria', 'reparacion_celulares', 'antojitos_mexicanos', 'recauderia_fruteria'],
                'canasta_basica': True,
                'mercomuna': False,
                'popular_tags': ['paca', 'herramientas', 'chacharas', 'ropa usada', 'antojitos', 'megatianguis']
            }
        if 'SAN FELIPE' in norm_nom or 'BOLA' in norm_nom:
            return {
                'categorias': ['CAT_ROPA_CALZADO_TEXTIL', 'CAT_BAZAR_CHACHARAS', 'CAT_HOGAR_FERRETERIA', 'CAT_COMIDA_PREPARADA', 'CAT_ALIM_FRESCOS'],
                'subgiros': ['ropa_paca_segunda', 'venta_ropa', 'zapateria_calzado', 'chacharas_segunda_mano', 'ferreteria_tlapaleria', 'antojitos_mexicanos'],
                'canasta_basica': True,
                'mercomuna': False,
                'popular_tags': ['megatianguis', 'ropa', 'tenis', 'autopartes', 'paca', 'comida', 'chacharas']
            }

        # Tianguis general barrial: Canasta fresca + Ropa + Comida + Chácharas
        return {
            'categorias': [
                'CAT_ALIM_FRESCOS', 'CAT_ABARROTES_CANASTA', 'CAT_COMIDA_PREPARADA',
                'CAT_ROPA_CALZADO_TEXTIL', 'CAT_BAZAR_CHACHARAS', 'CAT_HOGAR_FERRETERIA'
            ],
            'subgiros': [
                'recauderia_fruteria', 'carniceria', 'polleria', 'pescaderia', 'cremeria_lacteos',
                'tienda_abarrotes', 'tortilleria_molino', 'semillas_chiles_granos',
                'taqueria', 'antojitos_mexicanos', 'elotes_esquites_botaneros',
                'ropa_paca_segunda', 'venta_ropa', 'zapateria_calzado', 'lenceria_boneteria',
                'chacharas_segunda_mano', 'jarcieria_productos_limpieza', 'ferreteria_tlapaleria'
            ],
            'canasta_basica': True,
            'mercomuna': True,
            'popular_tags': ['frutas', 'verduras', 'carniceria', 'barbacoa', 'ropa de paca', 'tenis', 'chacharas', 'cremeria', 'antojitos']
        }

    # Concentraciones de Comerciantes (Vía Pública consolidada)
    if space_type == 'Concentración':
        return {
            'categorias': ['CAT_COMIDA_PREPARADA', 'CAT_ROPA_CALZADO_TEXTIL', 'CAT_OFICIOS_SERVICIOS', 'CAT_PAPELERIA_TECNOLOGIA'],
            'subgiros': ['taqueria', 'antojitos_mexicanos', 'torteria', 'venta_ropa', 'reparacion_celulares', 'cerrajeria', 'reparacion_calzado'],
            'canasta_basica': False,
            'mercomuna': True,
            'popular_tags': ['antojitos', 'tacos', 'tortas', 'ropa', 'accesorios celular', 'reparaciones']
        }

    # Mercados Públicos Tradicionales
    # Especialidades emblemáticas
    if 'FLORES' in norm_giro or 'FLOR' in norm_nom or 'JAMAICA' in norm_nom:
        return {
            'categorias': ['CAT_HOGAR_FERRETERIA', 'CAT_ALIM_FRESCOS', 'CAT_COMIDA_PREPARADA'],
            'subgiros': ['floreria_plantas', 'recauderia_fruteria', 'antojitos_mexicanos', 'cremeria_lacteos'],
            'canasta_basica': True,
            'mercomuna': True,
            'popular_tags': ['flores', 'arreglos florales', 'plantas', 'rosas', 'frutas']
        }

    if 'SONORA' in norm_nom or 'HERBOLARIA' in norm_giro or 'ESOTER' in norm_giro:
        return {
            'categorias': ['CAT_SALUD_BELLEZA', 'CAT_BAZAR_CHACHARAS', 'CAT_PAPELERIA_TECNOLOGIA', 'CAT_HOGAR_FERRETERIA'],
            'subgiros': ['herbolaria_esoterismo', 'artesanias_manualidades', 'mascotas_alimento', 'chacharas_segunda_mano'],
            'canasta_basica': False,
            'mercomuna': False,
            'popular_tags': ['hierbas medicinales', 'esoterismo', 'veladoras', 'artesanias', 'amuletos', 'animales']
        }

    if 'SAN JUAN' in norm_nom or 'GOURMET' in norm_giro:
        return {
            'categorias': ['CAT_ALIM_FRESCOS', 'CAT_COMIDA_PREPARADA', 'CAT_ABARROTES_CANASTA'],
            'subgiros': ['carniceria', 'pescaderia', 'cremeria_lacteos', 'restaurante_marisqueria', 'antojitos_mexicanos'],
            'canasta_basica': True,
            'mercomuna': False,
            'popular_tags': ['carnes exoticas', 'mariscos gourmet', 'quesos importados', 'embutidos', 'pescaderia']
        }

    if 'MUEBLES' in norm_giro or 'VASCO DE QUIROGA' in norm_nom:
        return {
            'categorias': ['CAT_HOGAR_FERRETERIA', 'CAT_OFICIOS_SERVICIOS'],
            'subgiros': ['muebles_colchones', 'carpinteria_ebanisteria', 'telas_blancos'],
            'canasta_basica': False,
            'mercomuna': False,
            'popular_tags': ['muebles', 'comedores', 'recamaras', 'carpinteria', 'madera']
        }

    if 'ROPA' in norm_giro or 'MIXCALCO' in norm_nom:
        return {
            'categorias': ['CAT_ROPA_CALZADO_TEXTIL', 'CAT_SALUD_BELLEZA'],
            'subgiros': ['venta_ropa', 'lenceria_boneteria', 'zapateria_calzado', 'telas_blancos', 'bolsos_mochilas'],
            'canasta_basica': False,
            'mercomuna': False,
            'popular_tags': ['ropa de mayoreo', 'vestidos', 'uniformes', 'calzado', 'mochilas']
        }

    if 'HERRAMIENTAS' in norm_giro or 'FERRETER' in norm_giro:
        return {
            'categorias': ['CAT_HOGAR_FERRETERIA', 'CAT_OFICIOS_SERVICIOS'],
            'subgiros': ['ferreteria_tlapaleria', 'cerrajeria', 'reparacion_electrodomesticos'],
            'canasta_basica': False,
            'mercomuna': False,
            'popular_tags': ['herramientas', 'tornillos', 'muebles', 'limpieza', 'jarcieria']
        }

    if 'ARTESAN' in norm_giro or 'CURIOSIDADES' in norm_nom:
        return {
            'categorias': ['CAT_PAPELERIA_TECNOLOGIA', 'CAT_BAZAR_CHACHARAS'],
            'subgiros': ['artesanias_manualidades', 'jugueteria_novedades', 'regalos_bisuteria', 'antiguedades_coleccionismo'],
            'canasta_basica': False,
            'mercomuna': False,
            'popular_tags': ['artesanias', 'recuerdos', 'regalos', 'juguetes', 'platería']
        }

    # Mercado Público Tradicional / Mixto estándar
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
    print("COMPILANDO VOCABULARIO DE COMPRAS Y TAXONOMÍA POPULAR CDMX (+300 ARTÍCULOS)")
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
