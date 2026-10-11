---
name: Parlamento de la demanda
description: Páginas del parlamento de forecast por EAN como una carta de tonos de belleza: cada partido una pastilla con su código, cada EAN un chip.
colors:
  surface: "#FFFFFF"
  paper: "#E3E4E0"
  paper-2: "#D7D8D3"
  ink: "#151515"
  ink-2: "#46474A"
  muted: "#5E5F62"
  line: "#D2D3CE"
  soft: "#F1F1EE"
  spine: "#FFFFFF"
  spine-2: "#F1F1EE"
  label: "#FFFFFF"
  empate: "#B7BCC4"
  status-good: "#0ca30c"
  status-critical: "#d03b3b"
  party-regla-fragancias: "#6250d6"
  party-media-12m-estacional: "#eda100"
  party-media-6m-estacional: "#00a3c4"
  party-regla-makeup: "#eb6834"
  party-media-6m-prudente: "#2a78d6"
  party-ciclo-de-vida: "#e87ba4"
  rule-teal: "#0F8A86"   # regla + DAs (PRODUCT.md); lo usan otras páginas, no el explorador
  dark-surface: "#1A1B1D"
  dark-paper: "#232427"
  dark-paper-2: "#2E2F33"
  dark-ink: "#EDEDEA"
  dark-ink-2: "#C3C4C0"
  dark-muted: "#9B9C99"
  dark-line: "#36373B"
  dark-soft: "#242528"
  dark-spine: "#1A1B1D"
  dark-spine-2: "#26272A"
  dark-label: "#26272B"
  dark-empate: "#6E7380"
typography:
  numeral:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "50px"
    fontWeight: 850
    lineHeight: 1
    letterSpacing: "-0.03em"
  swatch-count:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "24px"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.02em"
  kpi:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "19px"
    fontWeight: 800
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  title-lg:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 700
    lineHeight: 1.2
  swatch-code:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "0.06em"
  code:
    fontFamily: "ui-monospace, SF Mono, Menlo, Consolas, monospace"
    fontSize: "12px"
    fontWeight: 400
rounded:
  mark: "1px"
  chip: "2px"
spacing:
  hair: "2px"
  xs: "4px"
  sm: "6px"
  md: "8px"
  lg: "12px"
  xl: "16px"
components:
  party-swatch:
    backgroundColor: "{colors.label}"
    textColor: "{colors.ink}"
    rounded: "{rounded.chip}"
    padding: "6px 8px 7px"
  party-swatch-selected:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.chip}"
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.chip}"
    padding: "8px 12px"
  filter-rail:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    width: "248px"
  filter-chip:
    backgroundColor: "{colors.spine-2}"
    textColor: "{colors.ink}"
    rounded: "{rounded.chip}"
    padding: "5px 6px 5px 9px"
  line-chip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.chip}"
    padding: "4px 9px 4px 6px"
  search-input:
    backgroundColor: "{colors.spine-2}"
    textColor: "{colors.ink}"
    rounded: "{rounded.chip}"
    padding: "8px 12px 8px 32px"
  segmented-selected:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.chip}"
    padding: "7px 4px"
  party-marker:
    backgroundColor: "{colors.party-regla-fragancias}"
    textColor: "{colors.surface}"
    rounded: "{rounded.chip}"
    size: "18px"
  tooltip:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.chip}"
    padding: "8px 10px"
---

# Design System: Parlamento de la demanda

## Overview

**Creative North Star: "Carta de tonos"**

Cada página es una carta de tonos de belleza, un abanico Pantone abierto sobre la mesa. Cada partido es una pastilla de color con su código («Partido 01») y su nombre impresos en la tira blanca de abajo; cada EAN es un chip cuadrado de su color en el hemiciclo. El color manda porque es el dato: la página no pone color en nada que no sea un partido, un estado o una selección.

El material es papel de muestrario: cartulina gris neutra para el carril de filtros, blanco de chip para la zona de trabajo y tinta casi negra para texto, reglas y selección. No hay tarjetas redondeadas ni cajas oscuras: las zonas se separan con reglas de 1px y cambios de tono, y las secciones se rematan con una regla de tinta. En oscuro, el abanico se cierra y se ve su tapa: grafito, no negro.

La densidad es de muestrario profesional: mucha información en una pantalla, en tipo pequeño y firme (13px de cuerpo, nunca menos de 12px), con las cifras grandes reservadas para los escaños. El movimiento responde al tacto y explica cambios: el hemiciclo se recompone con un barrido corto y los puntos de la brújula viajan a su nueva posición.

**Key Characteristics:**
- Pastilla de partido = bloque de color con los escaños arriba, tira de etiqueta abajo con código y nombre.
- Esquina viva en todo (2px; 1px en marcas diminutas). Nada redondeado, nada en pastilla de 999px.
- Plano: reglas de 1px y cambio de tono; la sombra solo en lo que flota.
- Una grotesca (Schibsted Grotesk) en todos los papeles, de 12px a 50px.
- Funciona descargado y sin conexión, en claro y en oscuro.

## Colors

Neutros cálidos de cartulina y tinta casi negra, sin acento propio: los únicos colores saturados son los 6 partidos, Empate y los dos estados.

### Primary
- **Tinta** (`ink`): texto, reglas de remate (1px bajo cabeceras de tabla y sobre las cifras; 2px bajo la barra superior), foco de teclado, selección (pastilla, casilla, segmento, pestaña) y fondo de tooltip. Es el único «acento» del sistema.

### Party palette (categórica, orden fijo de bloques)
- **Regla fragancias** (`party-regla-fragancias`) · **Media 12M estacional** (`party-media-12m-estacional`) · **Media 6M estacional** (`party-media-6m-estacional`) · **Regla makeup** (`party-regla-makeup`) · **Media 6M prudente** (`party-media-6m-prudente`) · **Ciclo de vida** (`party-ciclo-de-vida`) · **Empate** (`empate`, gris; `dark-empate` en oscuro).
- Compromiso de marca de PRODUCT.md: no cambian entre claro y oscuro ni entre páginas. En oscuro, tres de ellos quedan fuera de la banda de luminosidad recomendada (aviso WARN de `validate_palette.js`); es una excepción aceptada porque son colores fijos de marca y siempre van con número y nombre.

### Neutral
- **Blanco de chip** (`surface`): zona de trabajo, tablas, tira de etiqueta de las pastillas (`label`) y barra superior (`spine`).
- **Cartulina** (`paper`) y **Cartulina 2** (`paper-2`): fondo del carril de filtros y sus divisores / hover de opción.
- **Tinta 2** (`ink-2`) y **Apagado** (`muted`): texto secundario, recuentos, ejes, códigos de pastilla.
- **Línea** (`line`) y **Suave** (`soft`): reglas de 1px entre zonas y filas, zona de proyección del gráfico, hover de fila, fondo del buscador (`spine-2`).

### Dark theme
Mismos roles con tonos de grafito propios (no inversión): `dark-surface`, `dark-paper`, `dark-paper-2`, `dark-ink`, `dark-ink-2`, `dark-muted`, `dark-line`, `dark-soft`, `dark-spine`, `dark-spine-2`, `dark-label` (tira de etiqueta un punto más clara que la superficie) y `dark-empate`. Se activa con `prefers-color-scheme` y se puede forzar con `data-theme`.

### Status
**Sube** (`status-good`) y **baja** (`status-critical`): solo en variaciones, siempre con triángulo ▲/▼ y la cifra en tinta; nunca solo color.

### Named Rules
**La Regla de Un Significado.** Un color = una cosa en todo el proyecto. El color de un partido sigue a la entidad, no a su posición; filtrar nunca repinta a los que quedan. Morado = fragancias, naranja = makeup y verde azulado = regla + DAs siguen reservados (PRODUCT.md).

**La Regla del Texto Legible.** Sobre un bloque de partido, el texto va en tinta (`ink`) si la luminancia del color supera 0,3 y en blanco si no. Se calcula, no se elige a ojo.

**La Regla Sin Acento.** El sistema no tiene color de marca propio: la selección y el foco son tinta. Si una pieza pide un color que no es partido ni estado, va en neutros.

## Typography

**Font:** Schibsted Grotesk (variable 400–900, woff2 autoalojada en base64 desde `src/fonts/`, licencia OFL), con alternativa Segoe UI / system-ui.
**Code Font:** ui-monospace (SF Mono, Menlo, Consolas), solo para el código EAN en tablas.

**Character:** una grotesca de prensa, compacta y negrita en las etiquetas, como la impresión pequeña de una carta de tonos. Un solo tipo para todo; la jerarquía sale del peso y del tamaño, no de mezclar familias.

### Hierarchy
- **Numeral** (850, 50px, 1, −0.03em): solo el total del hemiciclo.
- **Swatch count** (800, 24px, 1, −0.02em): escaños en el bloque de color de cada pastilla.
- **KPI** (800, 19px, 1.1): cifras de la ficha de la derecha, alineadas a la derecha.
- **Title large** (800, 17px, 1.2): nombre del EAN o de la selección.
- **Title** (800, 15px, 1.2): nombre de la página y títulos de columna.
- **Body** (400, 13px, 1.45): cuerpo denso (filtros, pestañas, listas); tablas a 12.5px; notas con máximo 62ch.
- **Label** (700, 12px): cabeceras de tabla, grupos del desplegable, recuentos, ejes. 12px es el mínimo absoluto.
- **Swatch code** (500, 12px, tracking 0.06em): el código «Partido 0N» de la tira de etiqueta, con regla de 1px debajo. Es el código de tono del muestrario, solo dentro de la pastilla.

### Named Rules
**La Regla de los 12px.** Ningún texto baja de 12px, tampoco ejes, notas ni marcas.

**La Regla de la Cifra Tabular.** Toda cifra en tabla, recuento o KPI usa `font-variant-numeric: tabular-nums`.

**La Regla Sin Conexión.** La fuente va dentro del archivo y siempre con alternativa del sistema: sin internet la página se lee igual.

## Layout

Una sola pantalla sin scroll de página en escritorio: barra superior (marca con abanico de 6 colores, buscador de hasta 520px, filtros activos y «Todo el parlamento») sobre tres columnas: carril de filtros en cartulina (248px), zona central flexible en blanco (tira de 7 pastillas, hemiciclo con su total, barra de volumen y pestañas con el gráfico) y ficha de cifras, trends y perfil político (356px). Scroll solo dentro de cada panel. Columnas separadas por reglas de 1px, sin huecos ni tarjetas.

- **≤1180px:** columnas de 220 / flexible / 320px; la tira pasa a 4 pastillas por fila.
- **≤960px:** una columna con scroll de página, la tira a 2 por fila, los filtros activos bajan a su propia fila.

Ritmo: margen interior de zona 16px; huecos entre pastillas y chips 6px; separación interna 8 / 12px; 2px entre segmentos de la barra de volumen.

## Elevation & Depth

Plano. La profundidad la dan el cambio de tono (cartulina → blanco → suave) y las reglas: 1px de `line` entre zonas y filas, 1px de tinta para rematar una cabecera o un bloque de cifras, 2px de tinta bajo la barra superior.

### Shadow Vocabulary
- **Desplegable** (`box-shadow: 0 14px 32px rgba(20,20,18,.20)`): resultados del buscador.
- **Tooltip** (`box-shadow: 0 10px 28px rgba(20,20,18,.24)`): tooltips del gráfico y de los elementos con `data-tip`.

### Named Rules
**La Regla Plana.** Solo el desplegable y los tooltips llevan sombra, porque tapan otro contenido. Ninguna pastilla, chip, panel ni botón la lleva.

## Shapes

Esquina viva: 2px en pastillas, chips, botones, buscador, segmentado, tooltips, escaños del hemiciclo y marcadores de partido; 1px en marcas diminutas (cuadrado de leyenda de 10px, barras del abanico de la marca, segmentos de la barra de volumen). Los EANs son chips cuadrados, no puntos; el centro de una selección en la brújula es un rombo de tinta. Las casillas de filtro son cuadradas con borde de 1.5px.

## Components

### Pastilla de partido (componente firma)
- **Forma:** rectángulo de 2px con borde 1px `line`; arriba el bloque del color del partido (mín. 44px) con los escaños en Swatch count; abajo la tira de etiqueta (`label`) con «Partido 0N» (o «Sin partido» en Empate) sobre regla de 1px, el nombre en 800 a 12.5px (máx. 2 líneas) y el % de volumen en apagado.
- **Estados:** hover = borde `ink-2`; pulsada (filtro activo) = borde tinta y tira en tinta con texto blanco; sin EANs = 38% de opacidad. Pulsar filtra por ese partido.

### Hemiciclo de chips
- Un chip cuadrado de 2px por EAN con la geometría `seats()` de `src/votes_report.py`, partidos por bloque de izquierda a derecha, Empate al final, total en Numeral con «escaños» debajo. Hover = contorno de tinta 1.5px; clic abre el EAN. Entra con un barrido único `clip-path` de izquierda a derecha (260ms, ease-out). Debajo, la barra de volumen (10px, segmentos de 1px de radio, 2px de hueco).

### Carril de filtros
- Cartulina, facetas plegables separadas por `paper-2`; cabecera en 700 13px con recuento de seleccionados en un recuadro de tinta; opciones con casilla cuadrada (tinta al marcar), cuadrado de color de 10px si es partido y recuento tabular. Opciones sin EANs al 45%.

### Ficha de cifras (spec list)
- Nombre en Title large con el mini chip del partido (44×52px, bloque de color y tira con el número); lista de cifras abierta por una regla de tinta, cada fila con etiqueta a la izquierda, cifra KPI a la derecha y explicación debajo, separadas por reglas de 1px.

### Marcador de partido
- Cuadrado de 2px del color del partido con su número (18px en leyendas y chips de línea; 20px con trazo de superficie en la brújula). Sustituye a los discos numerados.

### Botones y chips
- **Primario** («Todo el parlamento»): fondo tinta, texto blanco, 700; desactivado = transparente con hairline `line` y texto apagado.
- **Chip de filtro activo:** fondo `spine-2`, 12px, con ✕ apagado. **Chip de serie** del gráfico: borde `line` sobre blanco; apagado = texto `muted` y marcador al 35%.
- **Pulsación:** todo control pulsable hace `scale(.97)` en 160ms ease-out y transiciona color/borde en 160ms.

### Pestañas y segmentado
- **Pestañas:** texto 700 13px apagado; activa = tinta con subrayado de 2px.
- **Segmentado:** borde 1px tinta, divisores de tinta; activo = fondo tinta, texto blanco.

### Buscador, desplegable y tooltip
- **Buscador:** fondo `spine-2`, sin borde; en foco, borde `spine-muted`. **Desplegable:** blanco, borde `line`, sombra de desplegable, entra en 150ms. **Tooltip:** fondo tinta, texto blanco 12px, aparece en 120ms. Son los únicos elementos con sombra.

### Brújula
- Cuadrantes con puntos de EAN por color de partido, marcadores cuadrados y rombo de centro. Al cambiar de pregunta, los puntos viajan en 700ms `cubic-bezier(0.77, 0, 0.175, 1)`.

## Do's and Don'ts

### Do:
- **Do** poner el número y el nombre del partido junto a cada color, como en la tira de la pastilla.
- **Do** usar esquina de 2px (1px en marcas de menos de 12px) en todo lo que tenga forma.
- **Do** separar zonas con reglas de 1px y cambio de tono, y rematar cabeceras y bloques de cifras con una regla de tinta.
- **Do** dar respuesta a cada control: `scale(.97)` al pulsar, 160ms ease-out; hover solo en `(hover: hover) and (pointer: fine)`.
- **Do** respetar `prefers-reduced-motion`: el barrido pasa a un fundido de 150ms y se quitan desplazamientos y escalas.
- **Do** validar con `dataviz` (`validate_palette.js`) cualquier color nuevo, en claro y en oscuro.

### Don't:
- **Don't** usar radios grandes ni pastillas de 999px: es la estética de dashboard que este sistema sustituye.
- **Don't** poner sombra en pastillas, chips, paneles o botones; solo desplegable y tooltip.
- **Don't** usar discos ni círculos numerados para los partidos: el marcador es cuadrado.
- **Don't** reutilizar un color de partido, de categoría o de estado para otra cosa.
- **Don't** bajar de 12px en ningún texto.
- **Don't** depender de recursos de internet: fuente y datos van dentro del archivo.
- **Don't** usar el consenso de o9 como referencia fuera de reportes históricos.
