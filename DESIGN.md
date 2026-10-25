---
name: Tianguis CDMX
description: Sistema visual cívico para información de tianguis, derivado de la captura de referencia CDMX.
colors:
  primary: "#166163"
  primary-deep: "#104f55"
  primary-mid: "#156266"
  primary-soft: "#276f75"
  primary-muted: "#3f7376"
  surface: "#f0fefe"
  surface-raised: "#ffffff"
  surface-sunken: "#dde3e3"
  ink: "#166163"
  ink-secondary: "#3f7376"
  ink-body: "#223a37"
  ink-inverse: "#ffffff"
  accent-transit-blue: "#2f4fb7"
  accent-metro-red: "#d02c3a"
  accent-cablebus-cyan: "#4cc4d8"
  accent-train-purple: "#7d3f8f"
  accent-metrobus-green: "#00843d"
  accent-mexibus-orange: "#e8622a"
  accent-trolley-gold: "#c89e3a"
typography:
  display:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "1.75rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  title:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "1.375rem"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "normal"
  body:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  body-strong:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: "normal"
  label:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "0.01em"
  tab:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "normal"
rounded:
  sm: "6px"
  md: "12px"
  lg: "16px"
  sheet: "20px"
  full: "999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  gutter: "20px"
components:
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "20px"
  card-heading:
    textColor: "{colors.primary}"
    typography: "{typography.title}"
  card-body:
    textColor: "{colors.ink}"
    typography: "{typography.body}"
  tab-active:
    textColor: "{colors.primary}"
    typography: "{typography.tab}"
  tab-inactive:
    textColor: "{colors.ink-secondary}"
    typography: "{typography.tab}"
  bottom-nav:
    backgroundColor: "{colors.primary-deep}"
    textColor: "{colors.ink-inverse}"
  bottom-nav-active:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.ink-inverse}"
    rounded: "{rounded.full}"
  filter-chip-active:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.ink-inverse}"
    rounded: "{rounded.full}"
    padding: "12px 20px"
  filter-chip-idle:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.primary}"
    rounded: "{rounded.full}"
    padding: "12px 20px"
  sheet:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.sheet}"
    padding: "24px"
  floating-control:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.primary}"
    size: "56px"
    rounded: "{rounded.full}"
---

# Tianguis CDMX — Sistema visual

## Overview

Este sistema no fue inventado: fue **medido**. Los tokens de arriba provienen de muestrear por regiones nueve capturas de una app cívica de movilidad de la Ciudad de México (`WhatsApp Image 2026-10-25 at *.jpeg`, en la raíz del proyecto), y declaran el lenguaje visual que la audiencia de Tianguis ya sabe leer.

La lógica central: **una institución civil, no una marca**. El color primario es un verde azulado profundo que aparece en barras, títulos y estados activos; las superficies de contenido son un menta casi blanco; el blanco puro queda reservado para controles flotantes sobre el mapa y para el texto sobre teal. La densidad de iconos es alta, pero cada icono va dentro de un contenedor circular teal, lo que crea el ritmo visual característico de la referencia.

La jerarquía viene de la saturación y del contenedor, no de la decoración. No hay sombras dramáticas, ni degradados de marca, ni tipografía expresiva. Esa austeridad es lo que produce la confianza institucional, y es el activo que Tianguis hereda.

## Colors

**Estrategia: Committed.** Un solo color saturado —`#166163`— ocupa las regiones que estructuran la pantalla (barra de navegación, encabezados, tabs activos, contenedores de iconos). El resto es neutro cálido-frío casi blanco. La saturación de la paleta secundaria se usa **solo** en iconografía de categoría.

Todos los valores fueron **medidos por mediana de cluster** sobre las capturas (ver *Método de extracción*), no elegidos.

| Rol | Token | Valor | Contraste s/`surface` | Uso |
|---|---|---|---|---|
| Primario | `primary` | `#166163` | 6.95 AA | Títulos de tarjeta, iconos, círculos |
| Primario profundo | `primary-deep` | `#104f55` | — | Barra de navegación inferior |
| Primario medio | `primary-mid` | `#156266` | — | Pines del mapa, marcadores |
| Primario suave | `primary-soft` | `#276f75` | — | Chip de filtro activo (relleno) |
| Primario apagado | `primary-muted` | `#3f7376` | 5.1 AA | Tab inactivo, texto secundario |
| Superficie | `surface` | `#f0fefe` | — | Tarjetas, hoja inferior |
| Superficie elevada | `surface-raised` | `#ffffff` | — | Controles flotantes, píldora activa, chips en reposo |
| Superficie hundida | `surface-sunken` | `#dde3e3` | — | Rieles, separadores, fondo de mapa |
| Tinta de cuerpo | `ink-body` | `#223a37` | 11.75 AAA | Texto de párrafo en tarjetas |
| Título | `ink` | `#166163` | 6.89 AA | Títulos y subtítulos teal |
| Tinta inversa | `ink-inverse` | `#ffffff` | 9.24 AAA s/`primary-deep` | Texto sobre teal |

### Método de extracción

Los valores salen de **mediana de cluster**, no de un selector de píxel. Para cada región de UI se recortó una zona uniforme (relleno de una tarjeta, interior de la barra inferior, glifos de un título) y se aplicó una máscara de color para excluir texto, iconos y bordes; el valor final es la mediana del canal R, G y B sobre los píxeles que pasaron la máscara.

Por qué la mediana y no el modo ni un picker:

- La barra inferior lleva una textura de patrón encima y el JPEG añade ruido: ningún color de esa zona supera el 2.5% de los píxeles. El modo devolvería un artefacto de compresión; la mediana devuelve el consenso.
- Un picker devuelve **un** píxel, que puede ser borde, antialiasing o ruido. Sirve para verificar, no para declarar un token.

Correcciones aplicadas tras el segundo pase: `primary` pasó de `#0f4e55` a `#166163` (se midió sobre glifos y contenedores, no sobre la barra), `primary-deep` de `#0b3e42` a `#104f55`, `primary-muted` de `#487f81` a `#3f7376` (el original daba 4.39:1 y fallaba AA para texto normal). `primary-soft` en `#1a797f` era un muestreo defectuoso: la píldora activa de la barra inferior es **blanca** (`#ffffff`), y el verde de relleno pertenece a los chips de filtro.

**Paleta de categoría.** Cada giro de tianguis hereda un color de línea de la referencia, siempre acompañado de icono y etiqueta de texto: `#d02c3a` comida preparada, `#00843d` fruta y verdura, `#2f4fb7` abarrotes, `#c89e3a` ropa y calzado, `#e8622a` hogar, `#7d3f8f` servicios, `#4cc4d8` artesanía.

Reglas:

- Teal sobre menta es la combinación normativa de texto. `primary-muted` sobre `surface` (5.1:1) es el límite: no bajar de ahí.
- `ink-body` (`#223a37`) es el color del texto de párrafo, no `primary`: el teal se reserva a títulos, iconos y estados. Un párrafo completo en teal pesa más de lo que la jerarquía pide.
- Los colores de categoría **nunca** se usan para texto. Son relleno de icono y trazo.
- Ningún estado se comunica solo por color: siempre icono + etiqueta.

## Typography

Una sola familia: la pila del sistema (`system-ui`). Es una decisión, no una omisión. El producto compite contra el sol en la pantalla, la prisa de un mercado y usuarios mayores; una fuente descargada aporta carácter y resta legibilidad en el único escenario que importa. La pila del sistema además hace que la app se sienta nativa en cada teléfono, que es exactamente el registro institucional que perseguimos.

La jerarquía se construye con **peso y tamaño**, no con familia:

- `display` 28px/700 — título de pantalla ("Pagos", "Tianguis")
- `title` 22px/700 — encabezado de tarjeta
- `body` 17px/400 — texto de tarjeta y descripciones
- `body-strong` 17px/600 — énfasis dentro del cuerpo
- `label` 13px/500 — etiquetas de la barra inferior
- `tab` 17px/600 — tabs superiores

El cuerpo base de 17px es deliberadamente mayor que el estándar de 16px: el usuario mayor fija el piso. `body` nunca baja de 17px; `label` es la única excepción y solo para texto de apoyo de la barra inferior, que va acompañado de icono.

## Layout

- **Móvil primero, una columna.** La referencia es una app vertical; el ancho útil va de 360px a 430px, con un contenedor máximo de 480px centrado en pantallas mayores.
- **Gutter de 20px.** El contenido nunca toca el borde.
- **El mapa es el lienzo.** Las pantallas de mapa son de borde a borde; el contenido se apoya encima en hojas y tarjetas.
- **Ritmo vertical:** 24px entre secciones, 16px entre elementos de una misma sección, 32px alrededor de bloques aislados.
- **Hoja inferior persistente.** Se ancla al borde inferior sobre la barra de navegación, con esquinas superiores de 20px y un asa de arrastre de 40×4px centrada.
- **Barra inferior fija** de 5 destinos máximo, icono sobre etiqueta, altura 88px más el área segura del dispositivo.

## Elevation & Depth

La profundidad es **mínima y funcional**. La referencia no usa sombras para jerarquizar; usa color de superficie y contenedores.

- Tarjetas sobre el fondo de página: sin sombra. El `#f0fefe` contra blanco ya separa.
- Controles flotantes sobre el mapa: sombra única `0 2px 8px rgba(15,78,85,0.18)`.
- Hoja inferior y barra de navegación: sombra hacia arriba `0 -4px 16px rgba(15,78,85,0.12)`.
- La barra inferior lleva una textura de patrón tonal apenas perceptible sobre `primary-deep`; es el único ornamento del sistema y no debe subir de ~6% de opacidad.

No hay glassmorphism, ni blur, ni degradados de marca.

## Shapes

- **Radios:** 6px para elementos pequeños (chips de icono interno), 12px para tarjetas, 16px para bloques grandes, 20px para la hoja inferior, y píldora completa (`999px`) para chips de filtro y la píldora de la barra inferior.
- **Círculos.** El sistema tiene una gramática circular fuerte: iconos dentro de círculos teal, controles flotantes circulares de 56px, botón de acción primaria circular. Es la firma formal de la referencia.
- **Bordes:** 1px `#dde3e3` cuando hace falta separar dos superficies del mismo color. Nunca bordes de 2px ni dobles.

## Components

**Tarjeta de acción.** Superficie `#f0fefe`, radio 12px, padding 20px. A la izquierda, un icono teal grande (32–40px) sin círculo contenedor cuando va dentro de la tarjeta. Título en `title` teal, descripción en `body`. Es el patrón de "Agregar servicio" / "Pagar servicio" de la referencia, y aquí carga las acciones de tianguis.

**Tab superior.** Dos o tres opciones, icono + etiqueta, `tab` 17px/600. Activo en `primary` con subrayado de 3px que cubre todo el ancho de la pestaña; inactivo en `primary-muted` sin subrayado. No hay subrayado parcial ni animación de pastilla.

**Chip de filtro.** Píldora. Activo: relleno `primary-soft`, texto `ink-inverse`. Inactivo: `surface-raised` con texto `primary` y borde `surface-sunken`. Altura mínima 44px, padding horizontal 20px.

**Círculo de acceso rápido.** Círculo teal sólido de 56px con icono blanco de línea, y etiqueta debajo en `label`. Tres o cuatro por fila como máximo. Es el patrón "Ir a: Incidentes / Horarios / Rutas".

**Barra de navegación inferior.** Fondo `primary-deep` con patrón tonal. Cinco destinos como máximo: `Inicio`, `Mapa`, `Tianguis`, `Favoritos`, `Mi perfil`. El destino activo lleva una **píldora blanca** detrás del icono (el catálogo original: no es teal claro), el icono en `primary-deep` y la etiqueta en blanco 600; los inactivos en blanco al 80%.

**Pin de mapa.** Forma de gota con relleno `primary-mid` (o el color de la categoría) e icono blanco de línea. Los pines de categoría nunca son más grandes que 32px.

**Botón de acción flotante.** 56px, circular, `primary` sólido con icono blanco, anclado abajo a la derecha con 20px de margen. Uno por pantalla como máximo.

**Hoja inferior.** Superficie `surface`, esquinas superiores 20px, asa de arrastre, título `display`, y contenido con el ritmo vertical del sistema.

## Do's and Don'ts

**Sí**

- Usa `primary` (`#166163`) para toda la estructura: títulos, tabs activos, iconos, trazos de estado.
- Usa `ink-body` (`#223a37`) para párrafos y descripciones.
- Deja que el mapa ocupe la pantalla completa y apoya el contenido encima.
- Acompaña cada color de categoría con un icono y una etiqueta de texto.
- Mantén el cuerpo en 17px o más y los objetivos táctiles en 44px o más.
- Usa contenedores circulares para iconos; es la firma formal del sistema.
- Reserva el blanco puro para lo que flota sobre el mapa y para el texto sobre teal.

**No**

- No introduzcas una segunda familia tipográfica, ni una fuente display decorativa.
- No uses los colores de categoría como color de texto.
- No agregues sombras, degradados ni blur fuera de las tres elevaciones definidas.
- No superes los cinco destinos en la barra inferior.
- No uses `primary-muted` para texto de cuerpo sobre `surface` (es el límite de 5.1:1, no el default).
- No conviertas la información en una página que reemplaza al mapa: la hoja inferior es el patrón.
- No inventes datos de tianguis, horarios, colonias ni cifras para llenar una pantalla.
