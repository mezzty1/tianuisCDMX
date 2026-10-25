#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Maestro de Íconos de Puestos de Tianguis en PNG con Variantes de Color por Giro
Chilangatón 2026 - Reto 1: Comercio Popular y Barrial

Este script realiza:
1. Extracción limpia con transparencia antialiasing (PNG RGBA) de la imagen fuente
   'photo_2026-10-25 13.18.03.jpeg', defringiendo bordes y protegiendo elementos interiores
   (toalla de rayas, foco cálido, ojillos metálicos, letreros y fruta).
2. Segmentación semántica de componentes rojos (lona superior, parche, faldón inferior,
   caja plástica central y subrayados de letreros) preservando de forma 100% natural los
   jitomates, naranjas, plátanos, sandías, aguacates y estructura tubular.
3. Generación de las variantes cromáticas oficiales para:
   - Las 9 Macro-Categorías de giros comerciales populares (giros_catalogo.json)
   - Los 5 Sectores Canónicos de Tianguis de la SEDECO / Gaceta Oficial CDMX
   - El puesto original rojo tradicional
4. Exportación en resoluciones:
   - Master HD (903 x 952 px)
   - Marcador Web / Mapa Grande (256 x 256 px)
   - Marcador Web / Leaflet Estándar (128 x 128 px)
   - Marcador Mapa Compacto (64 x 64 px)
5. Generación de catálogo JSON con metadatos y vínculos a cada asset.
"""

import os
import json
import colorsys
import numpy as np
from PIL import Image
from scipy import ndimage

SOURCE_IMAGE_PATH = "photo_2026-10-25 13.18.03.jpeg"
OUTPUT_DIR = "assets/icons/puestos"
CATALOG_PATH = "data/catalog/giros_catalogo.json"

# Especificación de variantes de color alineadas al catálogo y la normatividad de la CDMX
VARIANTS_CONFIG = [
    {
        "id": "original_rojo",
        "categoria_id": "CAT_ALIM_FRESCOS",
        "sector_sedeco": "basico",
        "nombre_giro": "Puesto Tradicional Rojo (Canasta Básica Oficial)",
        "nombre_archivo_base": "puesto_original_rojo",
        "target_hue_deg": 358.4,
        "sat_mult": 1.0,
        "val_mult": 1.0,
        "hex_color": "#DC2626",
        "is_original": True,
        "descripcion": "Lona roja emblemática del abasto tradicional en tianguis y mercados sobre ruedas."
    },
    {
        "id": "alim_frescos_verde",
        "categoria_id": "CAT_ALIM_FRESCOS",
        "sector_sedeco": "basico",
        "nombre_giro": "Alimentos Frescos y Perecederos (Recaudería / Frutas y Verduras)",
        "nombre_archivo_base": "puesto_cat_alim_frescos_verde",
        "target_hue_deg": 142.0,
        "sat_mult": 0.95,
        "val_mult": 0.90,
        "hex_color": "#059669",
        "is_original": False,
        "descripcion": "Verde esmeralda fresco característico de verdulerías, recauderías y legumbres."
    },
    {
        "id": "abarrotes_canasta_ambar",
        "categoria_id": "CAT_ABARROTES_CANASTA",
        "sector_sedeco": "basico",
        "nombre_giro": "Abarrotes, Materias Primas y Canasta Básica",
        "nombre_archivo_base": "puesto_cat_abarrotes_canasta_ambar",
        "target_hue_deg": 38.0,
        "sat_mult": 1.00,
        "val_mult": 0.98,
        "hex_color": "#D97706",
        "is_original": False,
        "descripcion": "Ámbar dorado y color maíz para granos, semillas, chiles secos, huevo y abarrotes secos."
    },
    {
        "id": "comida_preparada_naranja",
        "categoria_id": "CAT_COMIDA_PREPARADA",
        "sector_sedeco": "alimentos_preparados",
        "nombre_giro": "Alimentos Preparados, Bebidas y Antojitos",
        "nombre_archivo_base": "puesto_cat_comida_preparada_naranja",
        "target_hue_deg": 22.0,
        "sat_mult": 1.00,
        "val_mult": 0.98,
        "hex_color": "#EA580C",
        "is_original": False,
        "descripcion": "Naranja cempasúchil / garnacha para taquerías, antojitos, fondas y aguas frescas."
    },
    {
        "id": "ropa_calzado_azul",
        "categoria_id": "CAT_ROPA_CALZADO_TEXTIL",
        "sector_sedeco": "complementario",
        "nombre_giro": "Ropa, Calzado, Telas y Accesorios",
        "nombre_archivo_base": "puesto_cat_ropa_calzado_textil_azul",
        "target_hue_deg": 218.0,
        "sat_mult": 0.95,
        "val_mult": 0.95,
        "hex_color": "#2563EB",
        "is_original": False,
        "descripcion": "Azul rey vibrante para puestos de ropa nueva, ropa de paca, tenis, calzado y blancos."
    },
    {
        "id": "hogar_ferreteria_cian",
        "categoria_id": "CAT_HOGAR_FERRETERIA",
        "sector_sedeco": "complementario",
        "nombre_giro": "Artículos del Hogar, Ferretería y Limpieza",
        "nombre_archivo_base": "puesto_cat_hogar_ferreteria_cian",
        "target_hue_deg": 188.0,
        "sat_mult": 0.95,
        "val_mult": 0.90,
        "hex_color": "#0891B2",
        "is_original": False,
        "descripcion": "Cian turquesa para jarciería, artículos de limpieza, herramientas, plásticos y enseres."
    },
    {
        "id": "salud_belleza_rosa",
        "categoria_id": "CAT_SALUD_BELLEZA",
        "sector_sedeco": "servicios",
        "nombre_giro": "Salud, Cuidado Personal y Belleza",
        "nombre_archivo_base": "puesto_cat_salud_belleza_rosa",
        "target_hue_deg": 336.0,
        "sat_mult": 0.92,
        "val_mult": 0.96,
        "hex_color": "#DB2777",
        "is_original": False,
        "descripcion": "Rosa mexicano tradicional para cosméticos, barbería, estética, uñas y cuidado personal."
    },
    {
        "id": "papeleria_tecnologia_morado",
        "categoria_id": "CAT_PAPELERIA_TECNOLOGIA",
        "sector_sedeco": "complementario",
        "nombre_giro": "Papelería, Cómputo, Regalos y Juguetería",
        "nombre_archivo_base": "puesto_cat_papeleria_tecnologia_morado",
        "target_hue_deg": 268.0,
        "sat_mult": 0.90,
        "val_mult": 0.95,
        "hex_color": "#7C3AED",
        "is_original": False,
        "descripcion": "Morado eléctrico para tecnología, accesorios de celular, juguetes, novedades y papelería."
    },
    {
        "id": "oficios_servicios_olivo",
        "categoria_id": "CAT_OFICIOS_SERVICIOS",
        "sector_sedeco": "servicios",
        "nombre_giro": "Oficios Tradicionales y Reparaciones",
        "nombre_archivo_base": "puesto_cat_oficios_servicios_olivo",
        "target_hue_deg": 82.0,
        "sat_mult": 0.90,
        "val_mult": 0.82,
        "hex_color": "#65A30D",
        "is_original": False,
        "descripcion": "Verde olivo / artesanal para cerrajería, reparación de calzado, afiladores y sastrería."
    },
    {
        "id": "bazar_chacharas_terracota",
        "categoria_id": "CAT_BAZAR_CHACHARAS",
        "sector_sedeco": "mixto",
        "nombre_giro": "Chácharas, Segunda Mano y Comercio Mixto",
        "nombre_archivo_base": "puesto_cat_bazar_chacharas_terracota",
        "target_hue_deg": 348.0,
        "sat_mult": 0.80,
        "val_mult": 0.75,
        "hex_color": "#9F1239",
        "is_original": False,
        "descripcion": "Terracota / vino tinto barrial para chácharas, antigüedades, curiosidades y bazares mixtos."
    }
]

# Aliases normativos para los 5 sectores oficiales de tianguis según SEDECO
SECTORES_SEDECO_ALIASES = [
    {
        "sector_id": "SECTOR_BASICOS",
        "sector_nombre": "Productos Básicos (Alimentos Frescos y Abarrotes)",
        "source_variant_id": "alim_frescos_verde",
        "alias_filename": "puesto_sector_basicos",
        "hex_color": "#059669"
    },
    {
        "sector_id": "SECTOR_COMPLEMENTARIOS",
        "sector_nombre": "Productos Complementarios (Ropa, Calzado y Novedades)",
        "source_variant_id": "ropa_calzado_azul",
        "alias_filename": "puesto_sector_complementarios",
        "hex_color": "#2563EB"
    },
    {
        "sector_id": "SECTOR_ALIMENTOS_PREPARADOS",
        "sector_nombre": "Alimentos Preparados (Comida Caliente y Antojitos)",
        "source_variant_id": "comida_preparada_naranja",
        "alias_filename": "puesto_sector_alimentos_preparados",
        "hex_color": "#EA580C"
    },
    {
        "sector_id": "SECTOR_SERVICIOS",
        "sector_nombre": "Servicios (Belleza, Oficios y Reparaciones)",
        "source_variant_id": "salud_belleza_rosa",
        "alias_filename": "puesto_sector_servicios",
        "hex_color": "#DB2777"
    },
    {
        "sector_id": "SECTOR_MIXTOS_CHACHARAS",
        "sector_nombre": "Mercancías Mixtas y Chácharas (Segunda Mano y Bazar)",
        "source_variant_id": "bazar_chacharas_terracota",
        "alias_filename": "puesto_sector_mixtos_chacharas",
        "hex_color": "#9F1239"
    }
]


def extract_clean_transparent_png(source_path: str) -> np.ndarray:
    """
    Extrae la imagen del puesto con canal alfa de alta precisión:
    - Conserva las rayas blancas y rosas de la toalla interior.
    - Respeta el foco cálido suspendido y los ojillos metálicos.
    - Abre el fondo transparente bajo el techo y entre postes.
    - Defringe bordes eliminando cualquier halo blanco contra fondos oscuros.
    """
    img = Image.open(source_path).convert("RGB")
    arr = np.array(img, dtype=np.float32)
    dist_white = np.linalg.norm(255.0 - arr, axis=2)

    # 1. Delimitar el interior de la toalla para proteger sus franjas blancas
    towel_interior = np.zeros(dist_white.shape, dtype=bool)
    for y in range(300, 525):
        row = arr[y, 810:902]
        non_white = np.where(np.any(row < 248, axis=1))[0]
        if len(non_white) > 0:
            min_x = non_white.min() + 810
            max_x = non_white.max() + 810
            towel_interior[y, min_x:max_x+1] = True

    # 2. Identificar núcleos de fondo blanco puro
    bg_seed = (dist_white < 18.0) & (~towel_interior)
    labeled, num_features = ndimage.label(bg_seed)

    border_mask = np.zeros(bg_seed.shape, dtype=bool)
    border_mask[0, :] = border_mask[-1, :] = border_mask[:, 0] = border_mask[:, -1] = True
    border_labels = set(np.unique(labeled[border_mask]))
    border_labels.discard(0)

    bg_labels = set(border_labels)
    for lbl in range(1, num_features + 1):
        if lbl not in bg_labels:
            size = np.sum(labeled == lbl)
            if size > 60:
                bg_labels.add(lbl)
            else:
                # Comprobar si corresponde a huecos de ojillos
                ys, xs = np.where(labeled == lbl)
                cy, cx = np.mean(ys), np.mean(xs)
                for oy, ox in [(150, 45), (12, 425), (188, 940), (318, 640)]:
                    if np.hypot(cy - oy, cx - ox) < 25:
                        bg_labels.add(lbl)

    bg_core = np.isin(labeled, list(bg_labels)) & (~towel_interior)

    # 3. Transición de bordes alfa suave
    alpha = np.ones(dist_white.shape, dtype=np.float32)
    alpha[bg_core] = 0.0

    edge_mask = ~bg_core & (dist_white < 70.0) & (ndimage.distance_transform_edt(bg_core) < 3.0) & (~towel_interior)
    alpha[edge_mask] = np.clip((dist_white[edge_mask] - 18.0) / (70.0 - 18.0), 0.0, 1.0)
    alpha = np.clip(alpha, 0.0, 1.0)

    # 4. Desvanecimiento y defringing contra blanco
    rgb_clean = arr.copy()
    for c in range(3):
        rgb_c = (arr[:, :, c] - (1.0 - alpha) * 255.0) / np.maximum(alpha, 1e-4)
        rgb_clean[:, :, c] = np.clip(rgb_c, 0.0, 255.0)

    # Restaurar cuerpo de la toalla
    rgb_clean[towel_interior] = arr[towel_interior]
    alpha[towel_interior] = 1.0

    rgba = np.dstack([rgb_clean, (alpha * 255.0)]).astype(np.float32)
    return rgba


def build_tarp_recolor_mask(master_rgba: np.ndarray) -> np.ndarray:
    """
    Segmenta con precisión quirúrgica todas las áreas rojas correspondientes
    a la lona, faldón y letreros, excluyendo jitomates, naranjas y plátanos.
    """
    arr = master_rgba
    r = arr[:, :, 0] / 255.0
    g = arr[:, :, 1] / 255.0
    b = arr[:, :, 2] / 255.0

    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    delta = max_c - min_c

    h = np.zeros_like(r)
    mask_d = delta > 1e-4
    mask_r = mask_d & (r == max_c)
    h[mask_r] = ((g[mask_r] - b[mask_r]) / delta[mask_r]) % 6.0
    mask_g = mask_d & (g == max_c)
    h[mask_g] = ((b[mask_g] - r[mask_g]) / delta[mask_g]) + 2.0
    mask_b = mask_d & (b == max_c)
    h[mask_b] = ((r[mask_b] - g[mask_b]) / delta[mask_b]) + 4.0
    h = h * 60.0

    s = np.zeros_like(r)
    s[max_c > 0] = delta[max_c > 0] / max_c[max_c > 0]
    v = max_c

    # Máscara roja estricta
    red_mask = ((h < 12.0) | (h > 348.0)) & (s > 0.45) & (v > 0.25)
    labeled, num_features = ndimage.label(red_mask)

    # Identificar componente de jitomates (caja de madera frontal)
    tomatoes_lbl = None
    for lbl in range(1, num_features + 1):
        ys, xs = np.where(labeled == lbl)
        if len(ys) > 5000:
            if ys.min() > 500 and ys.max() < 660 and xs.min() > 390 and xs.max() < 580:
                tomatoes_lbl = lbl

    tarp_mask = red_mask.copy()
    if tomatoes_lbl is not None:
        tarp_mask &= (labeled != tomatoes_lbl)
    
    # Garantizar exclusión de cualquier jitomate residual
    tarp_mask[520:650, 400:580] = False

    # Dilatar 1 pixel para capturar bordes anti-aliased de tela
    tarp_mask_dilated = ndimage.binary_dilation(tarp_mask, iterations=1) & (s > 0.25) & (v > 0.20)
    tarp_mask_dilated[520:650, 400:580] = False

    return tarp_mask_dilated, h, s, v


def generate_color_variant(master_rgba: np.ndarray, tarp_mask: np.ndarray, h: np.ndarray, s: np.ndarray, v: np.ndarray, target_h_deg: float, s_mult: float, v_mult: float) -> Image.Image:
    """Genera una variante cromática manteniendo volumen, sombras, arrugas y textura."""
    res = master_rgba.copy()
    target_h = target_h_deg / 360.0
    ys, xs = np.where(tarp_mask)

    for y, x in zip(ys, xs):
        cur_s = s[y, x]
        cur_v = v[y, x]
        new_s = np.clip(cur_s * s_mult, 0.0, 1.0)
        new_v = np.clip(cur_v * v_mult, 0.0, 1.0)
        nr, ng, nb = colorsys.hsv_to_rgb(target_h, new_s, new_v)
        res[y, x, 0] = nr * 255.0
        res[y, x, 1] = ng * 255.0
        res[y, x, 2] = nb * 255.0

    return Image.fromarray(res.astype(np.uint8), mode="RGBA")


def save_multiresolution(img: Image.Image, base_dir: str, base_filename: str) -> dict:
    """Guarda la imagen en alta definición y tamaños optimizados para interfaz web."""
    paths = {}
    
    # 1. Master HD
    hd_path = os.path.join(base_dir, f"{base_filename}.png")
    img.save(hd_path, "PNG", optimize=True)
    paths["master_hd"] = hd_path

    # Subcarpetas para resoluciones web
    for size in [256, 128, 64]:
        size_dir = os.path.join(base_dir, str(size))
        os.makedirs(size_dir, exist_ok=True)
        size_path = os.path.join(size_dir, f"{base_filename}_{size}px.png")
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(size_path, "PNG", optimize=True)
        paths[f"{size}px"] = size_path

    return paths


def main():
    print(f"=== Generador de Íconos de Tianguis CDMX por Giro ===")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Extracción limpia en PNG transparente
    print(f"[1/5] Extrayendo máster transparente de '{SOURCE_IMAGE_PATH}'...")
    master_rgba = extract_clean_transparent_png(SOURCE_IMAGE_PATH)
    
    # Guardar en raíz del workspace como solicita el punto 1 del usuario:
    root_png_path = "puesto_tianguis.png"
    Image.fromarray(master_rgba.astype(np.uint8), mode="RGBA").save(root_png_path, "PNG", optimize=True)
    print(f"  -> Guardado PNG principal en la raíz: '{root_png_path}' ({master_rgba.shape[1]}x{master_rgba.shape[0]} px)")

    # 2. Segmentación del toldo y faldón
    print("[2/5] Segmentando máscara cromática de lona y faldón...")
    tarp_mask, h, s, v = build_tarp_recolor_mask(master_rgba)
    print(f"  -> Píxeles de lona segmentados: {np.sum(tarp_mask):,}")

    # 3. Generación de las variantes cromáticas
    print("[3/5] Procesando las 10 variantes cromáticas por giro...")
    manifest = {
        "metadata": {
            "version": "1.0.0",
            "autor": "Chilangotón 2026 - Reto 1: Comercio Popular y Barrial",
            "fecha": "2026-10-25",
            "dimensiones_master": [master_rgba.shape[1], master_rgba.shape[0]],
            "resoluciones_adicionales": [256, 128, 64],
            "formato": "PNG RGBA (Transparente)"
        },
        "variantes_giros": [],
        "sectores_sedeco": []
    }

    generated_images = {}

    for var in VARIANTS_CONFIG:
        print(f"  - Generando: {var['nombre_giro']} ({var['hex_color']})...")
        if var["is_original"]:
            variant_img = Image.fromarray(master_rgba.astype(np.uint8), mode="RGBA")
        else:
            variant_img = generate_color_variant(
                master_rgba, tarp_mask, h, s, v,
                var["target_hue_deg"], var["sat_mult"], var["val_mult"]
            )
        
        generated_images[var["id"]] = variant_img
        paths = save_multiresolution(variant_img, OUTPUT_DIR, var["nombre_archivo_base"])
        
        item = {
            "id": var["id"],
            "categoria_id": var["categoria_id"],
            "sector_sedeco": var["sector_sedeco"],
            "nombre_giro": var["nombre_giro"],
            "hex_color": var["hex_color"],
            "target_hue_deg": var["target_hue_deg"],
            "descripcion": var["descripcion"],
            "archivos": paths
        }
        manifest["variantes_giros"].append(item)

    # 4. Generación de copias y aliases para los 5 sectores canónicos SEDECO
    print("[4/5] Generando alias directos para los 5 Sectores Canónicos SEDECO...")
    for sec in SECTORES_SEDECO_ALIASES:
        src_img = generated_images[sec["source_variant_id"]]
        paths = save_multiresolution(src_img, OUTPUT_DIR, sec["alias_filename"])
        sec_item = {
            "sector_id": sec["sector_id"],
            "sector_nombre": sec["sector_nombre"],
            "source_variant_id": sec["source_variant_id"],
            "hex_color": sec["hex_color"],
            "archivos": paths
        }
        manifest["sectores_sedeco"].append(sec_item)

    # 5. Exportar catálogo JSON
    catalog_json_path = os.path.join(OUTPUT_DIR, "iconos_catalogo.json")
    with open(catalog_json_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"[5/5] Catálogo de íconos exportado en '{catalog_json_path}'")

    print(f"\n✓ Proceso completado exitosamente: 15 variantes y aliases generados en 4 resoluciones (60 archivos PNG).")


if __name__ == "__main__":
    main()
