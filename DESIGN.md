---
name: Explorador del parlamento
description: Una app de macOS para el parlamento de métodos. Paneles quietos sobre lienzo gris; cada EAN o partido se abre como una ventana translúcida que nace de su escaño, se lanza con inercia y se asienta con un muelle.
colors:
  canvas: "#F5F5F7"
  panel: "#FFFFFF"
  panel-2: "#FAFAFC"
  fill: "rgba(120,120,128,.12)"
  fill-2: "rgba(120,120,128,.07)"
  ink: "#1D1D1F"
  ink-2: "#424245"
  muted: "#6E6E73"
  hair: "rgba(0,0,0,.09)"
  accent-graphite: "#1D1D1F"
  accent-ink: "#FFFFFF"
  accent-soft: "rgba(0,0,0,.06)"
  glass: "rgba(255,255,255,.97)"
  glass-edge: "rgba(0,0,0,.10)"
  glass-hi: "rgba(255,255,255,.75)"
  thumb: "#FFFFFF"
  tl-red: "#FF5F57"
  tl-yellow: "#FEBC2E"
  tl-off: "#D5D5D8"
  tl-glyph: "rgba(0,0,0,.55)"
  empate: "#B7BCC4"
  status-good: "#0ca30c"
  status-critical: "#d03b3b"
  party-regla-fragancias: "#6250d6"
  party-media-12m-estacional: "#eda100"
  party-media-6m-estacional: "#00a3c4"
  party-regla-makeup: "#eb6834"
  party-media-6m-prudente: "#2a78d6"
  party-ciclo-de-vida: "#e87ba4"
  fragancias: "#6250d6"
  makeup: "#eb6834"
  rule-teal: "#0F8A86"
  consenso-navy: "#26408B"
  dark-canvas: "#000000"
  dark-panel: "#1C1C1E"
  dark-panel-2: "#232325"
  dark-fill: "rgba(118,118,128,.24)"
  dark-fill-2: "rgba(118,118,128,.14)"
  dark-ink: "#F5F5F7"
  dark-ink-2: "#D2D2D7"
  dark-muted: "#98989D"
  dark-hair: "rgba(255,255,255,.10)"
  dark-accent-graphite: "#F5F5F7"
  dark-accent-ink: "#1D1D1F"
  dark-accent-soft: "rgba(255,255,255,.12)"
  dark-glass: "rgba(40,40,42,.96)"
  dark-glass-edge: "rgba(255,255,255,.12)"
  dark-glass-hi: "rgba(255,255,255,.08)"
  dark-thumb: "#636366"
  dark-tl-off: "#4A4A4E"
  dark-tl-glyph: "rgba(0,0,0,.6)"
  dark-empate: "#6E7380"
typography:
  numeral:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Display, Inter Var, system-ui, sans-serif"
    fontSize: "58px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.035em"
    fontFeature: "'tnum'"
  large-title:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Display, Inter Var, system-ui, sans-serif"
    fontSize: "24px"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.028em"
  title:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Display, Inter Var, system-ui, sans-serif"
    fontSize: "21px"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Display, Inter Var, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.022em"
  window-title:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Display, Inter Var, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.02em"
  window-title-folded:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Display, Inter Var, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.02em"
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Text, Inter Var, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: "-0.003em"
  callout:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Text, Inter Var, system-ui, sans-serif"
    fontSize: "12.5px"
    fontWeight: 400
    lineHeight: 1.45
  footnote:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Text, Inter Var, system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Text, Inter Var, system-ui, sans-serif"
    fontSize: "11.5px"
    fontWeight: 600
    lineHeight: 1.2
  axis:
    fontFamily: "-apple-system, BlinkMacSystemFont, SF Pro Text, Inter Var, system-ui, sans-serif"
    fontSize: "11px"
    fontWeight: 400
    lineHeight: 1
    fontFeature: "'tnum'"
  code:
    fontFamily: "ui-monospace, SF Mono, Menlo, Consolas, monospace"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: 1.2
rounded:
  window-tag: "2.5px"
  swatch: "3px"
  check: "4px"
  vbar: "4px"
  segment: "7px"
  control-small: "7px"
  list-row: "8px"
  segmented: "9px"
  control: "10px"
  tooltip: "10px"
  grouped-list: "12px"
  menu: "12px"
  window: "14px"
  panel: "20px"
  pill: "980px"
spacing:
  hair: "2px"
  xs: "6px"
  sm: "8px"
  md: "12px"
  gap: "14px"
  lg: "18px"
  xl: "22px"
components:
  panel:
    backgroundColor: "{colors.panel}"
    rounded: "{rounded.panel}"
    padding: "16px 18px"
  window:
    backgroundColor: "{colors.glass}"
    rounded: "{rounded.window}"
    width: "340px"
  window-folded:
    backgroundColor: "{colors.glass}"
    rounded: "{rounded.window}"
    width: "300px"
  button-primary:
    backgroundColor: "{colors.accent-graphite}"
    textColor: "{colors.accent-ink}"
    rounded: "{rounded.pill}"
    padding: "7px 15px"
  button-ghost:
    backgroundColor: "{colors.fill}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "7px 15px"
  filter-chip:
    backgroundColor: "{colors.fill}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "5px 8px 5px 11px"
  search-field:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    height: "34px"
  segmented-control:
    backgroundColor: "{colors.fill}"
    rounded: "{rounded.segmented}"
    padding: "2px"
  segmented-thumb:
    backgroundColor: "{colors.thumb}"
    textColor: "{colors.ink}"
    rounded: "{rounded.segment}"
  grouped-list:
    backgroundColor: "{colors.fill-2}"
    rounded: "{rounded.grouped-list}"
    padding: "0 12px"
  traffic-light-close:
    backgroundColor: "{colors.tl-red}"
    size: "12px"
  traffic-light-fold:
    backgroundColor: "{colors.tl-yellow}"
    size: "12px"
  traffic-light-inactive:
    backgroundColor: "{colors.tl-off}"
    size: "12px"
---

# Design System: Explorador del parlamento

## Overview

**Creative North Star: "La app de macOS del parlamento"**

El explorador se comporta como una app nativa de Apple a pantalla completa (lenguaje pedido por el usuario el 2026-10-12). Lienzo gris claro, negro en oscuro; encima, paneles blancos sin borde y quietos (filtros, parlamento, histórico, selección). Lo que se abre no sustituye la vista: cada EAN o partido nace como una ventana translúcida desde el escaño o la fila pulsada, se lanza con inercia, se asienta con un muelle y se pliega o se compara en fila sin tapar el parlamento.

Densidad de herramienta: texto de 13px, cifras tabulares, listas agrupadas tipo Ajustes, controles segmentados. El color es casi solo de los datos: el cromo es gris y grafito para que los seis colores de partido, el morado de fragancias y el naranja de makeup sean lo único que se lee como color. Funciona descargado y sin conexión: la letra es la del sistema de Apple y, fuera de Apple, Inter Var incrustada.

Rechazados por el usuario: la carta de tonos y la cámara oscura con tarjetas, y la mesa de trabajo sobre tapete de corte (el sistema anterior, sustituido entero).

**Key Characteristics:**
- Paneles de 20px sin borde con sombra difusa sobre lienzo #F5F5F7 / #000000.
- Ventanas de 14px en material translúcido con semáforo de macOS (rojo cierra, amarillo pliega).
- Acento grafito, nunca azul de sistema.
- Muelles por eje, proyección de la inercia, resistencia en los bordes; todo interrumpible.
- Un significado por color; el estado nunca va solo en el color.

## Colors

Cromo neutro de Apple (grises y grafito) al servicio de una paleta de datos fija.

### Primary
- **Grafito** (`accent-graphite`; en oscuro, `dark-accent-graphite`): botón principal, casilla marcada, contador de filtro, resultado activo del buscador, foco (anillo de 3.5px al 45% del acento), caret. Su versión suave (`accent-soft`) marca fila caliente, selección de texto y botón de icono activo.

### Secondary (datos; colores fijos de PRODUCT.md)
- **Partidos:** Regla fragancias (`party-regla-fragancias`), Media 12M estacional, Media 6M estacional, Regla makeup, Media 6M prudente, Ciclo de vida. Salen de `COL6` en `src/ideo_brujulas6.py`; el número sobre el color va en #151515 o blanco según luminancia.
- **Categoría:** morado = fragancias (`fragancias`), naranja = makeup (`makeup`).
- **Empate** (`empate` / `dark-empate`): gris, siempre al final del hemiciclo.
- **Regla + DAs** (`rule-teal`) y **consenso** (`consenso-navy`, solo en reportes históricos): reservados aunque el explorador no los pinte.

### Tertiary (estado)
- **Bueno / crítico** (`status-good`, `status-critical`): solo en el triángulo de 8×7px junto a una variación; el número va en tinta.

### Neutral
- **Lienzo** (`canvas`), **panel** (`panel`, `panel-2` para el fondo de la lista agrupada dentro de ventanas), **rellenos** (`fill` para controles y chips, `fill-2` para hover, listas agrupadas y campos), **tinta** (`ink`, `ink-2` secundaria), **apagado** (`muted`: ejes, pistas, metadatos), **filete** (`hair`, siempre como sombra interior de .5px, no como borde).
- **Semáforo:** `tl-red`, `tl-yellow`, `tl-off` (ventana de detrás), `tl-glyph` (× y − que aparecen al pasar).

### Named Rules
**The Graphite Rule.** El acento es grafito. El azul de sistema de Apple se midió a ΔE 3.3 del partido Media 6M prudente (#2a78d6): se leería como ese partido. Ningún color de cromo puede acercarse a un color de partido.

**The One Meaning Rule.** Cada color significa una sola cosa en todo el proyecto: partido, categoría, regla + DAs, consenso o estado. El cromo no usa ninguno de ellos.

**The Triangle Rule.** Verde y rojo solo aparecen como triángulo (arriba bueno, abajo crítico) al lado de la cifra; nunca colorean el número ni van solos.

## Typography

**Display Font:** SF Pro Display (vía `-apple-system`), con Inter Var incrustada en base64 (OFL) como reserva
**Body Font:** SF Pro Text (vía `-apple-system`), con Inter Var
**Label/Mono Font:** SF Mono / ui-monospace para EAN y códigos

**Character:** la letra del sistema de Apple, ajustada como en macOS: tracking negativo en los titulares, cifras tabulares en todo lo que se compara.

### Hierarchy
- **Numeral** (700, 58px, 1): el número de escaños en el centro del hemiciclo.
- **Large title** (700, 24px, 1.08): título de la app sobre el lienzo.
- **Title** (700, 21px, 1.15): nombre de la selección en el panel derecho.
- **Headline** (600, 17px, 1.2): título de panel y cifra de la lista agrupada.
- **Window title** (700, 16px, 1.25): nombre dentro de la ventana; 14px plegada.
- **Body** (400, 13px, 1.45): filas, leyenda, filtros.
- **Callout** (12.5px): tablas, chips, segmentos, subtítulos.
- **Footnote** (12px, 1.5): notas (máx. 64ch), pistas, tooltips.
- **Label** (600, 11.5px): cabeceras de tabla, grupos del buscador.
- **Axis** (11px, tabular): ejes de los gráficos y etiqueta de proyección.

### Named Rules
**The Display Tracking Rule.** De 16px hacia arriba se aprieta: −0.02em (16–17px) a −0.035em (58px). El cuerpo lleva −0.003em.

**The One Unit Rule.** Cada eje usa una sola unidad, elegida por el valor más alto (`k` desde 1.000, `M` desde 1.000.000, coma decimal española): nunca «10 k» junto a «5000».

## Layout

App a pantalla completa con rejilla de tres columnas (filtros 256px | parlamento + histórico | selección 372px; 232/332px por debajo de 1240px), separación de 14px y margen 6/18/18px. La barra de título no es panel: va sobre el lienzo con título, buscador (máx. 440px), chips de filtros y, con ventanas abiertas, «Comparar en fila» / «Misma escala» / «Cerrar fichas». Los paneles rellenan con 16–18px. Por debajo de 960px todo pasa a una columna que se desplaza; las ventanas flotantes desaparecen y las fichas se apilan como paneles normales con el semáforo encendido.

## Elevation & Depth

Profundidad por capas de Apple: lienzo, paneles con sombra casi imperceptible y ventanas que flotan con sombra larga. La ventana activa sube de sombra; la que se arrastra sube más y crece al 102%. Los filetes son sombras interiores de .5px; no hay bordes de 1px salvo en la casilla vacía y el chip de leyenda apagado.

### Shadow Vocabulary
- **Panel** (`0 1px 1px rgba(0,0,0,.02), 0 6px 20px rgba(0,0,0,.04)`; oscuro: `0 0 0 .5px rgba(255,255,255,.06)`): paneles y buscador.
- **Win** (`0 0 0 .5px edge, 0 2px 6px rgba(0,0,0,.05), 0 18px 44px rgba(0,0,0,.12)`): ventana de detrás y tooltips.
- **Top** (`… 0 4px 10px rgba(0,0,0,.06), 0 24px 56px rgba(0,0,0,.16)`): ventana delante.
- **Lift** (`… 0 8px 18px rgba(0,0,0,.08), 0 36px 80px rgba(0,0,0,.22)`): ventana arrastrada y menú del buscador.
- **Thumb** (`0 0 0 .5px rgba(0,0,0,.04), 0 1px 3px rgba(0,0,0,.12), 0 3px 8px rgba(0,0,0,.06)`): cursor del control segmentado.

### Material translúcido
Ventanas: `glass` con `backdrop-filter: blur(40px) saturate(180%)` y filo de luz `inset 0 .5px 0 glass-hi`. Menú del buscador: blur 30px; tooltips: blur 24px. El vidrio claro es casi opaco (.97; .96 en oscuro) para que las cifras se lean encima del hemiciclo.

### Named Rules
**The Reduced Transparency Rule.** Con `prefers-reduced-transparency: reduce`, ventanas, menú y tooltips pasan a `panel` macizo sin desenfoque.

**The Still Panels Rule.** Los paneles no se mueven ni suben de sombra; solo las ventanas tienen elevación variable.

## Shapes

Esquinas continuas de Apple en escala fija: 20px paneles, 14px ventanas, 12px listas agrupadas y menú, 10px campo de búsqueda y tooltips, 9px fondo del control segmentado con segmentos de 7px, 8px filas de la leyenda, 7px filas y campos pequeños, 4px casilla y barra de volumen, píldora (980px) en botones y chips. Formas de dato: escaño y punto de leyenda en círculo; cuadrado de partido de 10px con radio 3px; etiqueta de ventana de 8px con radio 2.5px.

## Components

### Buttons
- **Shape:** píldora (980px).
- **Primary:** grafito con texto blanco (negro en oscuro), 7px 15px, 500 13px; hover mezcla 88% acento con tinta.
- **Ghost:** relleno `fill`, tinta; es el de la barra de título.
- **Press:** escala .97 al pulsar, 160ms `cubic-bezier(.23,1,.32,1)`. Desactivado al 40%.

### Chips
- **Filtro activo:** píldora `fill`, clave en apagado, valor en tinta, círculo de 16px para quitar.
- **Leyenda del gráfico:** `fill-2` encendida; apagada transparente con filete de 1px y muestra al 30%.

### Cards / Containers
- **Panel:** 20px, blanco, sombra panel, sin borde, título 17px.
- **Lista agrupada** (estilo Ajustes): `fill-2`, 12px, filas de 9px separadas por filete de .5px; etiqueta a la izquierda con subtítulo de 11.5px, cifra de 17px a la derecha.

### Inputs / Fields
- **Buscador:** 34px, 10px, panel con sombra panel y filete interior; foco con anillo de 3.5px al 40% del acento. Resultados en menú de vidrio con grupos de 11.5px y fila activa en grafito.
- **Filtro de faceta:** `fill-2`, 7px; casilla de 15px y 4px que se rellena de grafito con la marca dibujada.

### Navigation
- **Control segmentado:** fondo `fill` de 9px con 2px de aire; segmentos de 7px en 500 12.5px y tinta 2; el seleccionado en 600 y tinta. En las pestañas un cursor (`thumb`, sombra thumb) se desliza en transform y ancho, 340ms `cubic-bezier(.32,.72,0,1)`.
- **Barra lateral de filtros:** facetas plegables con chevron que gira 90° (260ms) y separador de .5px.

### Ventana flotante (firma)
- 340px (plegada 300px), radio 14px, material translúcido.
- **Semáforo:** dos botones de 12px separados 8px, área táctil ampliada 6px; rojo cierra, amarillo pliega; el × y el − aparecen al pasar. En la ventana de detrás, sin hover, los dos se apagan a `tl-off`. La etiqueta del partido es un cuadrado de 8px separado 10px, para que no se lea como tercer semáforo.
- Título en mono de 12px (EAN) o 600 13px (partido); al pasar por la ventana, su escaño se ilumina en el hemiciclo.

### Movimiento
- **Muelles por eje** (respuesta, amortiguación): apertura .48 / .92; asentar tras soltar .45 / 1, o .8 si se lanzó a más de 500 px/s; «Comparar en fila» .5 / .9 con 40ms de escalonado por ventana.
- **Inercia:** proyección de Apple `v/1000 · d/(1−d)` con d = .995. **Resistencia** en los bordes: `o·dim·.55/(dim + .55·o)`.
- **Abrir:** desde el punto pulsado, WAAPI 340ms de escala .6 y blur 8px a nada, `cubic-bezier(.23,1,.32,1)`. **Cerrar:** 200ms a escala .7 y blur 6px, con el origen en su escaño o fila. Reabrir una ya abierta: salto de 5px en 260ms.
- **Hemiciclo:** entra en 520ms desde escala .96 y blur 6px.
- **Reduced motion:** las ventanas se colocan sin muelle, abren y cierran sin animación, nada escala al pulsar ni al arrastrar y el resto se reduce a fundidos de 150ms.

## Do's and Don'ts

### Do:
- **Do** usar grafito como único acento de interfaz y dejar el color a los datos.
- **Do** separar con sombras interiores de .5px (`hair`) en vez de bordes.
- **Do** dar a cada ventana su semáforo (rojo cierra, amarillo pliega) y apagarlo cuando queda detrás.
- **Do** mover ventanas con muelles por eje interrumpibles y respetar `prefers-reduced-motion` y `prefers-reduced-transparency`.
- **Do** usar cifras tabulares y una sola unidad por eje.
- **Do** acompañar cada variación con su triángulo verde o rojo.
- **Do** incrustar Inter Var para que la página funcione sin conexión fuera de Apple.

### Don't:
- **Don't** usar el azul de sistema ni ningún color de cromo cercano a un color de partido.
- **Don't** reasignar colores de partido, categoría, regla + DAs o consenso, ni pintar el consenso fuera de reportes históricos.
- **Don't** poner bordes de 1px a los paneles ni elevar los paneles al pasar.
- **Don't** hacer redonda la etiqueta de partido de una ventana ni ponerla junto al semáforo.
- **Don't** sustituir la vista al abrir un EAN: se abre una ventana encima y el parlamento sigue visible.
- **Don't** mezclar unidades en un mismo eje.
