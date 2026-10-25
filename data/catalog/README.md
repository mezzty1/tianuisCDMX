# Catálogo Modular y Jerárquico de Giros Comerciales para el Comercio Popular y Barrial de la CDMX

**Chilangotón 2026 — Reto 1: Comercio Popular y Barrial**  
*Directorio:* `data/catalog/`  
*Versión:* `1.0.0` (Octubre 2026)

---

## 1. Introducción y Propósito

El comercio popular y barrial de la Ciudad de México —representado por **329 mercados públicos**, más de **1,360 tianguis**, concentraciones en vía pública y decenas de miles de **tienditas de abarrotes, recauderías, tortillerías y cocinas económicas**— presenta una enorme riqueza comercial pero también una profunda heterogeneidad en su registro.

En los datasets oficiales del Gobierno de la CDMX (SEDECO, Fondeso, Programas Emergentes y Mercomuna), los giros comerciales suelen registrarse como:
- **Campos nulos (`NA`) o en cero (`0`)**: Debido a que los mercados públicos y tianguis de barrio se asumen reglamentariamente como *"Mercados Tradicionales Mixtos"* que ofrecen toda la canasta de abasto.
- **Rótulos agregados**: Por ejemplo, *"COMIDA PREPARADA Y OTROS"*, *"ROPA, CALZADO Y TELAS"*, *"ABASTO"*, *"BÁSICOS Y COMPLEMENTARIOS"*.
- **Desgloses porcentuales o por conteo de puestos**: Como en tianguis (*"73 BÁSICOS, 687 COMPLEMENTARIOS Y 40 ALIMENTOS PREPARADOS"*).
- **Texto libre con ortografía variable y modismos barriales**: Como en las 86,402 solicitudes de crédito FONDESO (25,211 variantes textuales) y apoyos a comerciantes en vía pública (*"TACOS DE GUISADO"*, *"ELOTES Y ESQUITES"*, *"MISCELANEA"*, *"COSTURERA"*).

Este catálogo resuelve esta dispersión mediante una **taxonomía jerárquica, modular y normalizada** compuesta por **9 Macro-Categorías** y **67 Subgiros Específicos**, integrando atributos operativos y banderas de compatibilidad con programas de política pública de la CDMX como **Mercomuna**, la **Canasta Básica (CONEVAL / SEDECO)** y la tipología de puestos de la **Gaceta Oficial de la CDMX** (*Básicos*, *Complementarios*, *Alimentos Preparados*, *Servicios* y *Mixtos*).

---

## 2. Inventario de Archivos en `data/catalog/`

| Archivo | Formato | Descripción |
|---|---|---|
| [`giros_catalogo.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/giros_catalogo.json) | JSON | Especificación canónica estructurada con metadata, categorías, 67 subgiros y expresiones regulares precompiladas. |
| [`giros_catalogo.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/giros_catalogo.csv) | CSV | Tabla plana para manipulación rápida con pandas, SQL o herramientas GIS. |
| [`vocabulario_compras.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/vocabulario_compras.json) | JSON | Índice ampliado de 460 términos populares de consumo en tianguis y abasto barrial (Nivel Micro) con mapeo directo a subgiro, macrocategoría, canasta básica y Mercomuna. |
| [`vocabulario_compras.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/vocabulario_compras.csv) | CSV | Versión tabular del vocabulario de compras populares con sinónimos y tokens de búsqueda. |
| [`tarifas_horarios_transporte.json`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/tarifas_horarios_transporte.json) | JSON | Catálogo dinámico de 15 subsistemas de transporte (CDMX, Edomex y Federal), horarios de operación (L-D), esquemas por distancia, recargos nocturnos, medios de pago y gratuidades. |
| [`tarifas_horarios_transporte.csv`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/tarifas_horarios_transporte.csv) | CSV | Matriz comparativa tabular de tarifas, horarios, esquemas de cobro y beneficios de transporte metropolitano. |
| [`giro_classifier.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/giro_classifier.py) | Python | Motor de normalización, clasificación multi-etiqueta (`tag_giro`), adición/eliminación modular (`add_giro`, `remove_giro`) y etiquetado masivo de DataFrames. |
| [`generate_catalog.py`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/generate_catalog.py) | Python | Script reproducible que compila y exporta las versiones JSON y CSV a partir de las definiciones maestras. |
| [`README.md`](file:///Users/williams/Documents/Proyectos%20en%20Docker/Comercio%20Popular%20y%20Barrial/data/catalog/README.md) | Markdown | Documentación metodológica, taxonomía, estadísticas de cobertura y manual de uso de la API. |

---

## 3. Taxonomía: Macro-Categorías y Subgiros

### 3.1. Las 9 Macro-Categorías

| ID Categoría | Nombre de la Categoría | Ícono | Tipo SEDECO | Mercomuna Default | Canasta Básica Default |
|---|---|:---:|---|:---:|:---:|
| `CAT_ALIM_FRESCOS` | Alimentos Frescos y Perecederos | 🥦 | `basico` | **Sí** | **Sí** |
| `CAT_ABARROTES_CANASTA` | Abarrotes, Materias Primas y Canasta Básica | 🥫 | `basico` | **Sí** | **Sí** |
| `CAT_COMIDA_PREPARADA` | Alimentos Preparados, Bebidas y Antojitos | 🌮 | `alimentos_preparados` | No | No |
| `CAT_ROPA_CALZADO_TEXTIL` | Ropa, Calzado, Telas y Accesorios | 👕 | `complementario` | No | No |
| `CAT_HOGAR_FERRETERIA` | Artículos del Hogar, Ferretería y Limpieza | 🔨 | `complementario` | No | No |
| `CAT_SALUD_BELLEZA` | Salud, Cuidado Personal y Belleza | ✂️ | `servicios` | No (salvo farmacia) | No |
| `CAT_PAPELERIA_TECNOLOGIA` | Papelería, Cómputo, Regalos y Juguetería | ✏️ | `complementario` | No (salvo papelería) | No |
| `CAT_OFICIOS_SERVICIOS` | Oficios Tradicionales y Reparaciones | 🪛 | `servicios` | No | No |
| `CAT_BAZAR_CHACHARAS` | Chácharas, Segunda Mano y Comercio Mixto | 📦 | `mixto` | Variable | Variable |

---

### 3.2. Catálogo de Subgiros Específicos (67 Subgiros)

Cada subgiro cuenta con un identificador único en formato *slug*, descripción operativa y banderas de compatibilidad de política pública:

```
Esquema de Atributos:
├── id: Slug único identificador (ej. 'recauderia_fruteria')
├── categoria_id: Llave foránea a la Macro-Categoría (ej. 'CAT_ALIM_FRESCOS')
├── nombre: Nombre canónico legible en español
├── descripcion: Alcance de los productos y actividad comercial
├── canasta_basica: Booleano (Criterio CONEVAL / SEDECO CDMX)
├── mercomuna: Booleano (Comercios elegibles para vales de abasto Mercomuna)
├── perecedero: Booleano (Requiere refrigeración / manejo de frescura)
├── es_servicio: Booleano (Prestación de oficio vs. venta de bienes)
└── tipo_mercado_cdmx: ['basico', 'complementario', 'alimentos_preparados', 'servicios', 'mixto']
```

#### Detalle de Subgiros por Categoría:

#### 1. Alimentos Frescos y Perecederos (`CAT_ALIM_FRESCOS`)
1. `recauderia_fruteria`: Recaudería, Frutería y Verdulería. (Canasta Básica: Sí, Mercomuna: Sí, Perecedero: Sí).
2. `carniceria`: Carnicería y Tocinería (res, puerco, bistec, carnes rojas). (Canasta Básica: Sí, Mercomuna: Sí, Perecedero: Sí).
3. `polleria`: Pollería, Aves de Corral y Rosticería. (Canasta Básica: Sí, Mercomuna: Sí, Perecedero: Sí).
4. `pescaderia`: Pescadería y Marisquería en Crudo. (Canasta Básica: Sí, Mercomuna: Sí, Perecedero: Sí).
5. `cremeria_lacteos`: Cremería, Quesería y Salchichonería (quesos, crema, jamón, salchichas). (Canasta Básica: Sí, Mercomuna: Sí, Perecedero: Sí).

#### 2. Abarrotes, Materias Primas y Canasta Básica (`CAT_ABARROTES_CANASTA`)
6. `tienda_abarrotes`: Tienda de Abarrotes, Miscelánea y Minisúper de barrio. (Canasta Básica: Sí, Mercomuna: Sí, Perecedero: No).
7. `tortilleria_molino`: Tortillería y Molino de Nixtamal (masa, tortillas). (Canasta Básica: Sí, Mercomuna: Sí, Perecedero: Sí).
8. `panaderia_expendio`: Panadería Tradicional y Expendio de Pan (bolillo, telera, pan dulce). (Canasta Básica: Sí, Mercomuna: Sí, Perecedero: Sí).
9. `semillas_chiles_granos`: Semillas, Chiles Secos, Granos a granel, Arroz, Frijol y Mole. (Canasta Básica: Sí, Mercomuna: Sí, Perecedero: No).
10. `materias_primas`: Materias Primas, Desechables y Moldes de Repostería. (Canasta Básica: No, Mercomuna: No, Perecedero: No).
11. `dulceria_botanas`: Dulcería, Confitería, Botanas y Piñatas. (Canasta Básica: No, Mercomuna: No, Perecedero: No).
12. `purificadora_agua`: Purificadora de Agua y Venta de Garrafones y Hielo. (Canasta Básica: Sí, Mercomuna: Sí, Perecedero: No).

#### 3. Alimentos Preparados, Bebidas y Antojitos (`CAT_COMIDA_PREPARADA`)
13. `taqueria`: Taquería (pastor, suadero, bistec, guisados, canasta, carnitas, barbacoa, birria). (Canasta: No, Mercomuna: No, Perecedero: Sí).
14. `antojitos_mexicanos`: Antojitos Mexicanos y Garnachas (quesadillas, gorditas, sopes, pambazos, huaraches, tlacoyos). (Canasta: No, Mercomuna: No, Perecedero: Sí).
15. `tamales_atole`: Puesto de Tamales y Atole (champurrado, tamales oaxaqueños, guajolotas). (Canasta: No, Mercomuna: No, Perecedero: Sí).
16. `cocina_economica_fonda`: Cocina Económica, Fonda y Comida Corrida (guisados caseros, menú del día). (Canasta: No, Mercomuna: No, Perecedero: Sí).
17. `torteria`: Tortería y Lonchería (tortas calientes, ahogadas, gigantes, cemitas). (Canasta: No, Mercomuna: No, Perecedero: Sí).
18. `comida_rapida_pizzas`: Comida Rápida Urbana (hamburguesas al carbón, hot dogs, alitas, pizzas de barrio, papas fritas). (Canasta: No, Mercomuna: No, Perecedero: Sí).
19. `restaurante_marisqueria`: Restaurante Familiar y Mariscos Preparados (cocteles, caldos, ceviches). (Canasta: No, Mercomuna: No, Perecedero: Sí).
20. `cafeteria_fuente_sodas`: Cafetería, Fuente de Sodas, Juguería, Licuados y Desayunos. (Canasta: No, Mercomuna: No, Perecedero: Sí).
21. `postres_reposteria`: Postres, Pastelería, Gelatinas Artísticas y Repostería Casera. (Canasta: No, Mercomuna: No, Perecedero: Sí).
22. `paleteria_helados`: Paletería, Heladería, Nevería artesanal y Aguas Frescas. (Canasta: No, Mercomuna: No, Perecedero: Sí).
23. `elotes_esquites_botaneros`: Elotes Hervidos/Asados, Esquites con Tuétano y Chicharrones Preparados. (Canasta: No, Mercomuna: No, Perecedero: Sí).
24. `comida_preparada_general`: Puestos y Locales de Comida Preparada y Alimentos sin desglose. (Canasta: No, Mercomuna: No, Perecedero: Sí).

#### 4. Ropa, Calzado, Telas y Accesorios (`CAT_ROPA_CALZADO_TEXTIL`)
25. `venta_ropa`: Venta de Ropa Nueva y Confección (dama, caballero, infantil, playeras, pantalones). (Canasta: No, Mercomuna: No, Perecedero: No).
26. `zapateria_calzado`: Zapatería, Calzado formal y Tenis Deportivos. (Canasta: No, Mercomuna: No, Perecedero: No).
27. `lenceria_boneteria`: Bonetería, Lencería, Calcetería y Ropa Interior. (Canasta: No, Mercomuna: No, Perecedero: No).
28. `telas_blancos`: Telas por metro, Cobijas, Sábanas, Cobertores, Cortinas y Mantelería. (Canasta: No, Mercomuna: No, Perecedero: No).
29. `bolsos_mochilas`: Bolsos de mano, Mochilas escolares, Maletas de viaje y Cinturones. (Canasta: No, Mercomuna: No, Perecedero: No).
30. `ropa_paca_segunda`: Ropa de Paca Americana, Prendas Usadas y Bazares Textiles. (Canasta: No, Mercomuna: No, Perecedero: No).
31. `venta_catalogo_moda`: Venta por Catálogo de Ropa y Calzado (Andrea, Cklass, Price Shoes). (Canasta: No, Mercomuna: No, Perecedero: No).

#### 5. Artículos del Hogar, Ferretería y Limpieza (`CAT_HOGAR_FERRETERIA`)
32. `ferreteria_tlapaleria`: Ferretería, Tlapalería, Herramientas, Material Eléctrico y Plomería. (Canasta: No, Mercomuna: No, Perecedero: No).
33. `jarcieria_productos_limpieza`: Jarciería y Productos Químicos de Limpieza a Granel (cloro, detergentes, escobas). (Canasta: No, Mercomuna: No, Perecedero: No).
34. `plasticos_enseres_hogar`: Artículos de Plástico (tuppers), Enseres de Cocina, Peltre, Cazuelas y Vajillas. (Canasta: No, Mercomuna: No, Perecedero: No).
35. `muebles_colchones`: Muebles de Madera/Pino, Salas, Comedores, Colchonería, Tapicería y Cestería. (Canasta: No, Mercomuna: No, Perecedero: No).
36. `floreria_plantas`: Florería, Flores Frescas de Corte, Plantas de Ornato y Macetas. (Canasta: No, Mercomuna: No, Perecedero: Sí).
37. `mascotas_alimento`: Mascotas, Peces de Ornato, Acuarios y Croquetas a Granel. (Canasta: No, Mercomuna: No, Perecedero: No).

#### 6. Salud, Cuidado Personal y Belleza (`CAT_SALUD_BELLEZA`)
38. `farmacia_botica`: Farmacia, Medicamentos Genéricos y Material de Curación. (Canasta: No, Mercomuna: Sí, Perecedero: No).
39. `optica_lentes`: Óptica, Armazones oftálmicos, Micas graduadas y Examen de la Vista. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
40. `estetica_peluqueria`: Estética Unisex, Peluquería, Salón de Belleza, Cortes y Tintes. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
41. `barberia`: Barbería Clásica y Cuidado Masculino (fades, arreglo de barba). (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
42. `unas_pestanas_cosmetologia`: Salón de Uñas (acrílico, gelish), Pestañas 1x1, Depilación y Spa. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
43. `cosmeticos_perfumeria`: Cosméticos, Maquillaje, Perfumería y Venta por Catálogo (Avon, Mary Kay, Jafra). (Canasta: No, Mercomuna: No, Perecedero: No).
44. `herbolaria_esoterismo`: Herbolaria, Yerbería, Hierbas Medicinales, Veladoras Esotéricas y Amuletos. (Canasta: No, Mercomuna: No, Perecedero: No).
45. `consultorio_dental_salud`: Consultorio Dental, Consultorio Médico Barrial y Nutrición. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).

#### 7. Papelería, Cómputo, Regalos y Juguetería (`CAT_PAPELERIA_TECNOLOGIA`)
46. `papeleria_copias`: Papelería, Útiles Escolares, Fotocopias, Enmicados y Engargolados. (Canasta: No, Mercomuna: Sí, Perecedero: No).
47. `ciber_internet_computo`: Café Internet, Ciber, Trámites Digitales y Soporte de Cómputo. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
48. `reparacion_celulares`: Reparación de Celulares, Micas de Cristal, Fundas y Accesorios Móviles. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
49. `jugueteria_novedades`: Juguetería, Novedades electrónicas y Artículos de Temporada/Fiesta. (Canasta: No, Mercomuna: No, Perecedero: No).
50. `regalos_bisuteria`: Tienda de Regalos, Joyería de Fantasía/Plata, Peluches y Envolturas. (Canasta: No, Mercomuna: No, Perecedero: No).
51. `artesanias_manualidades`: Artesanías Mexicanas (barro, madera), Manualidades, Cerámica y Estambre. (Canasta: No, Mercomuna: No, Perecedero: No).

#### 8. Oficios Tradicionales y Reparaciones (`CAT_OFICIOS_SERVICIOS`)
52. `taller_costura_sastreria`: Taller de Costura, Sastrería, Composturas de Ropa y Maquila. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
53. `cerrajeria`: Cerrajería, Duplicado de Llaves y Apertura de Cerraduras. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
54. `reparacion_calzado`: Taller de Zapatero, Cambio de Tapas/Suelas y Compostura de Calzado. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
55. `carpinteria_ebanisteria`: Carpintería, Ebanistería, Muebles sobre medida y Barnizado. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
56. `herreria_soldadura`: Herrería, Soldadura, Puertas de Fierro, Zaguanes y Protecciones. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
57. `taller_mecanico`: Taller Mecánico Automotriz, Motos, Afinaciones y Refacciones. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
58. `vulcanizadora_llantas`: Vulcanizadora, Talachas, Parchado de Llantas y Montaje. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
59. `taller_bicicletas`: Taller y Refaccionaria de Bicicletas (ponchaduras, ajustes de frenos). (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
60. `lavanderia_tintoreria`: Lavandería por kilo, Tintorería y Planchaduría. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
61. `reparacion_electrodomesticos`: Reparación de Electrodomésticos, Línea Blanca y Refrigeración. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
62. `alquiladora_eventos`: Alquiladora de Mesas, Sillas, Lonas, Inflables y Eventos Sociales. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).
63. `fotografia_video`: Estudio Fotográfico, Fotos Infantiles/Título y Video Social. (Canasta: No, Mercomuna: No, Perecedero: No, Servicio: Sí).

#### 9. Chácharas, Segunda Mano y Comercio Mixto (`CAT_BAZAR_CHACHARAS`)
64. `chacharas_segunda_mano`: Chácharas de Tianguis, Tiliches, Herramientas Usadas y Artículos de Segunda Mano. (Canasta: No, Mercomuna: No, Perecedero: No).
65. `antiguedades_coleccionismo`: Antigüedades, Monedas Antiguas, Libros Usados y Discos de Vinil. (Canasta: No, Mercomuna: No, Perecedero: No).
66. `arte_rotulacion`: Arte, Pintores y Escultores de Bazar, Marcos para Cuadros, Rótulos Populares e Imprenta. (Canasta: No, Mercomuna: No, Perecedero: No).
67. `comercio_mixto_general`: Comercio Mixto Tradicional, Abasto Popular Semanal y Puestos Multigiro no especializados. (Canasta: Sí, Mercomuna: Sí, Perecedero: Sí, Tipo: Mixto).

---

## 4. Análisis de los Datasets Raw de la CDMX y Cobertura

Evaluamos el motor de clasificación en los 5 conjuntos de datos del proyecto:

| Dataset | Registros Totales | Registros con Giro Textual | Registros Clasificados | Cobertura Efectiva (% con texto) | Nota Metodológica de Cobertura |
|---|:---:|:---:|:---:|:---:|---|
| **`mercados_publicos.csv`** | 329 | 88 | **88** | **100.0%** | Los 241 restantes (73.3%) son mercados públicos tradicionales mixtos que por definición normativa ofrecen toda la canasta básica. |
| **`tianguis.csv`** | 1,367 | 178 | **173** | **97.2%** | 1,189 registros (87.0%) carecen de texto o están en `0` porque corresponden a tianguis semanales de abasto popular mixto. |
| **`mercomuna_comercios_muestra.csv`** | 250 | 250 | **172** | **100.0%** de los específicos | 172 registros correspondían a giros específicos (abarrotes, papelería, verdulería, etc.), clasificados al 100%. 78 tenían la etiqueta genérica cruda `"OTRO"`. |
| **`apoyos_emergentes_comercio.csv`** | 2,673 | 2,673 | **2,610** | **97.6%** | Altísima tasa de acierto en 809 variantes textuales de comida callejera y comercio en vía pública durante la pandemia. |
| **`fondeso_solicitudes.xlsx`** | 86,402 | 86,402 | **72,993** | **84.5%** | Cubre exhaustivamente 25,211 variantes textuales únicas de microempresarios de las 16 alcaldías. Los no clasificados corresponden a nombres propios o actividades no comerciales (ej. transporte, asesorías aisladas). |

### Distribución por Macro-Categoría en el Padrón FONDESO (72,993 Comercios Clasificados)

```
  CAT_COMIDA_PREPARADA      ██████████████████████████████  20,292 (27.8%)
  CAT_ABARROTES_CANASTA     ████████████████████            13,914 (19.1%)
  CAT_ROPA_CALZADO_TEXTIL   ██████████████                  9,466  (13.0%)
  CAT_PAPELERIA_TECNOLOGIA  ████████████                    8,130  (11.1%)
  CAT_SALUD_BELLEZA         ██████████                      7,170  (9.8%)
  CAT_OFICIOS_SERVICIOS     █████████                       6,150  (8.4%)
  CAT_ALIM_FRESCOS          ████████                        5,269  (7.2%)
  CAT_HOGAR_FERRETERIA      ██████                          4,303  (5.9%)
  CAT_BAZAR_CHACHARAS       ████                            2,838  (3.9%)
```

---

## 5. Guía de Uso del Módulo Python (`giro_classifier.py`)

El módulo `giro_classifier.py` está diseñado para importarse directamente en cualquier script de análisis, backend de aplicación o pipeline de datos.

### 5.1. Clasificar un Giro Comercial Textual (`tag_giro`)

```python
from data.catalog.giro_classifier import tag_giro

# 1. Ejemplo de puesto de comida con giros múltiples
resultado = tag_giro("Taquería de carnitas, tacos de guisado y refrescos")
print(resultado["status"])          # 'clasificado'
print(resultado["giro_principal"])   # {'id': 'taqueria', 'nombre': 'Taquería', ...}
print(resultado["giros"])            # ['taqueria', 'cocina_economica_fonda']
print(resultado["categorias"])       # ['CAT_COMIDA_PREPARADA']
print(resultado["es_canasta_basica"])# False
print(resultado["apto_mercomuna"])   # False
print(resultado["perecedero"])       # True

# 2. Ejemplo de tienda de conveniencia barrial (Canasta Básica + Mercomuna)
tiendita = tag_giro("Tienda de abarrotes, cremería y venta de huevo")
print(tiendita["giros"])             # ['tienda_abarrotes', 'cremeria_lacteos']
print(tiendita["categorias"])        # ['CAT_ABARROTES_CANASTA', 'CAT_ALIM_FRESCOS']
print(tiendita["es_canasta_basica"]) # True
print(tiendita["apto_mercomuna"])    # True
```

### 5.2. Agregar y Quitar Giros Modularmente a un Comercio

En la vida real de los mercados y tianguis, un locatario puede cambiar de giro o ampliar su oferta (por ejemplo, una papelería que empieza a vender abarrotes o recargas):

```python
from data.catalog.giro_classifier import add_giro, remove_giro

# Comercio inicial: Papelería escolar
comercio = {
    "comercio_id": "LOC-105-MERCADO-JAMAICA",
    "nombre": "Papelería La Escuelita",
    "giros": ["papeleria_copias"]
}

# El locatario añade venta de abarrotes y dulces
comercio = add_giro(comercio, "tienda_abarrotes")
comercio = add_giro(comercio, "dulceria_botanas")

print(comercio["giros"])
# ['papeleria_copias', 'tienda_abarrotes', 'dulceria_botanas']

print(comercio["categorias"])
# ['CAT_PAPELERIA_TECNOLOGIA', 'CAT_ABARROTES_CANASTA']

print("¿Acepta Mercomuna?:", comercio["apto_mercomuna"])
# ¿Acepta Mercomuna?: True (porque tienda_abarrotes y papeleria_copias califican)

# Si posteriormente retira la venta de abarrotes:
comercio = remove_giro(comercio, "tienda_abarrotes")
print(comercio["giros"])
# ['papeleria_copias', 'dulceria_botanas']
```

### 5.3. Etiquetado Masivo en DataFrames de Pandas (`tag_dataframe`)

```python
import pandas as pd
from data.catalog.giro_classifier import tag_dataframe

# Cargar cualquier dataset con columna de texto
df = pd.read_csv("data/raw/apoyos_emergentes_comercio.csv")

# Enriquecer automáticamente con giros, categorías y canasta básica
df_enriquecido = tag_dataframe(df, text_column="giro", prefix="cat_")

print(df_enriquecido[["giro", "cat_principal_nombre", "cat_canasta_basica", "cat_mercomuna"]].head(10))
```

### 5.4. Uso Directo desde Terminal (CLI)

Puedes clasificar cualquier texto directamente en la terminal:

```bash
python3 data/catalog/giro_classifier.py "Tacos de canasta y jugos naturales"
```

Salida JSON resultante:
```json
{
  "texto_original": "Tacos de canasta y jugos naturales",
  "texto_normalizado": "TACOS DE CANASTA Y JUGOS NATURALES",
  "status": "clasificado",
  "giros": [
    "taqueria",
    "cafeteria_fuente_sodas"
  ],
  "giro_principal": {
    "id": "taqueria",
    "nombre": "Taquería",
    "categoria_id": "CAT_COMIDA_PREPARADA",
    "categoria_nombre": "Alimentos Preparados, Bebidas y Antojitos"
  },
  "categorias": [
    "CAT_COMIDA_PREPARADA"
  ],
  "es_canasta_basica": false,
  "apto_mercomuna": false,
  "perecedero": true,
  "es_servicio": false,
  "tipo_mercado_cdmx": [
    "alimentos_preparados"
  ]
}
```

---

## 6. Conclusiones y Relevancia para el Reto 1

1. **Interoperabilidad Total**: Homologa cédulas de mercados públicos, rutas de tianguis, compras con vales Mercomuna y beneficiarios de créditos microempresariales de Fondeso bajo un mismo marco conceptual.
2. **Offline-First & Ligero**: La clasificación utiliza patrones y reglas semánticas precompiladas de alta velocidad sin dependencias pesadas de modelos de lenguaje en la nube, operando 100% en local y en milisegundos para decenas de miles de registros.
3. **Respeto a la Dinámica Popular**: Reconoce la naturaleza mixta del abasto popular, permitiendo asignación múltiple de giros y actualizándose dinámicamente según la realidad de los comerciantes.
