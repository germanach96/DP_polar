---
name: Parlamento de la demanda
description: Mesa de trabajo sobre tapete de corte. El parlamento es una hoja impresa y cada EAN, partido o grupo se abre como una ficha que se levanta, se mueve y se compara.
colors:
  mat: "#3D7862"
  mat-2: "#356B57"
  mat-line: "rgba(255,255,255,.09)"
  mat-line-5: "rgba(255,255,255,.2)"
  mat-ink: "#D8EDE2"
  paper: "#FCFCFA"
  paper-2: "#F2F3F0"
  card: "#FCFCFA"
  ink: "#1B1E1C"
  ink-2: "#474D49"
  muted: "#5E6561"
  line: "#DADDD7"
  shadow-tint: "rgba(12,34,26,.10)"
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
  dark-mat: "#1C362D"
  dark-mat-2: "#182F27"
  dark-mat-line: "rgba(255,255,255,.05)"
  dark-mat-line-5: "rgba(255,255,255,.11)"
  dark-mat-ink: "#9EC1AF"
  dark-paper: "#222624"
  dark-paper-2: "#2A2F2C"
  dark-card: "#2B302D"
  dark-card-edge: "rgba(255,255,255,.07)"
  dark-ink: "#E9EDEA"
  dark-ink-2: "#C1C8C3"
  dark-muted: "#9AA39E"
  dark-line: "#383E3B"
  dark-empate: "#6E7380"
typography:
  numeral:
    fontFamily: "Bricolage Grotesque, Segoe UI, system-ui, sans-serif"
    fontSize: "54px"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.035em"
    fontVariation: "'opsz' 96"
  brand:
    fontFamily: "Bricolage Grotesque, Segoe UI, system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.02em"
    fontVariation: "'opsz' 36"
  headline:
    fontFamily: "Bricolage Grotesque, Segoe UI, system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: 750
    lineHeight: 1.2
    letterSpacing: "-0.01em"
    fontVariation: "'opsz' 32"
  title:
    fontFamily: "Bricolage Grotesque, Segoe UI, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.01em"
    fontVariation: "'opsz' 28"
  card-title:
    fontFamily: "Bricolage Grotesque, Segoe UI, system-ui, sans-serif"
    fontSize: "15.5px"
    fontWeight: 750
    lineHeight: 1.25
    letterSpacing: "-0.01em"
    fontVariation: "'opsz' 24"
  body:
    fontFamily: "Bricolage Grotesque, Segoe UI, system-ui, sans-serif"
    fontSize: "13.5px"
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: "Bricolage Grotesque, Segoe UI, system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 650
    lineHeight: 1.2
  code:
    fontFamily: "ui-monospace, SF Mono, Menlo, Consolas, monospace"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.2
rounded:
  r: "3px"
  tick: "2px"
spacing:
  gutter: "14px"
  sheet: "16px"
  card: "12px"
  rule: "22px"
  grid: "1cm"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.r}"
    padding: "7px 12px"
  button-primary-hover:
    backgroundColor: "{colors.ink-2}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.r}"
    padding: "7px 12px"
  input-search:
    backgroundColor: "{colors.paper-2}"
    textColor: "{colors.ink}"
    rounded: "{rounded.r}"
    padding: "8px 12px 8px 32px"
  chip-filter:
    backgroundColor: "{colors.paper-2}"
    textColor: "{colors.ink}"
    rounded: "{rounded.r}"
    padding: "4px 6px 4px 9px"
  sheet:
    backgroundColor: "{colors.paper}"
    rounded: "{rounded.r}"
    padding: "{spacing.sheet}"
  card-floating:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.r}"
    width: "340px"
  card-compact:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.r}"
    width: "300px"
  tab-active:
    textColor: "{colors.ink}"
    typography: "{typography.label}"
---

# Design System: Parlamento de la demanda

## Overview

**Creative North Star: "La mesa de trabajo sobre el tapete de corte"**

La página es una mesa: un tapete verde de corte con cuadrícula de 1 cm (líneas finas cada centímetro y más marcadas cada 5 cm) y reglas numeradas en centímetros reales en el borde superior e izquierdo. Encima descansan hojas de papel blanco neutro (filtros, parlamento, histórico, selección) en una rejilla fija, y sobre ellas fichas flotantes que el planner levanta, arrastra, apila y compara sin perder de vista el parlamento.

Densidad de herramienta de análisis: texto de 13.5px, tablas de especificaciones con filete de tinta arriba, cifras tabulares. La tinta es casi negra; el color está reservado a los partidos y al estado. La profundidad es física y corta: el papel apoya, la ficha levantada proyecta una sombra larga y se inclina un poco. El modo oscuro es el mismo tapete de noche, no otro mundo.

Rechazados por el usuario: la «carta de tonos» y la cámara oscura con tarjetas (gritan IA), y el dashboard de tres columnas que sustituye la vista al pulsar.

**Key Characteristics:**
- Tapete verde con cuadrícula de 1 cm y 5 cm y reglas numeradas en cm reales.
- Hojas de papel con esquina de 3px y sombra corta tintada en verde.
- Fichas flotantes que nacen junto al punto pulsado, unidas a su escaño por un hilo del color del partido, y que se encajan en la cuadrícula de 1 cm.
- Una grotesca humanista variable (Bricolage Grotesque) y monoespaciada solo para códigos EAN.
- Colores de partido fijos; tinta para todo lo demás.

## Colors

Tapete verde, papel neutro y tinta casi negra; el único color vivo es el de los partidos y el estado.

### Primary
- **Tinta de imprenta** (`ink`): texto, botón principal, filete superior de tablas, subrayado de pestaña activa, foco, casilla marcada. En oscuro, `dark-ink`.

### Secondary
- **Verde tapete** (`mat`, `mat-2`): fondo de la página y de las reglas. Sus líneas (`mat-line` cada 1 cm, `mat-line-5` cada 5 cm) y números (`mat-ink`) son blancos translúcidos y verde pálido. En oscuro, `dark-mat*`.

### Tertiary (colores con significado fijo)
- **Partidos** (`party-*`): Regla fragancias, Media 12M estacional, Media 6M estacional, Regla makeup, Media 6M prudente, Ciclo de vida, en ese orden de bloques; **Empate** en gris (`empate` / `dark-empate`). Salen de `src/ideo_brujulas6.py` (`COL6`).
- **Categoría:** morado = fragancias (`fragancias`), naranja = makeup (`makeup`).
- **Regla + DAs:** verde azulado (`rule-teal`). No aparece en el explorador; lo usan otras páginas.
- **Consenso:** azul marino (`consenso-navy`), solo en reportes históricos.
- **Estado:** bueno (`status-good`) y crítico (`status-critical`), siempre con triángulo hacia arriba o hacia abajo.

### Neutral
- **Papel** (`paper`, `card`): hojas y fichas. **Papel 2** (`paper-2`): campos, chips, fila resaltada, zona de proyección del gráfico.
- **Tinta 2** (`ink-2`) para texto secundario fuerte y hover del botón; **gris de lápiz** (`muted`) para notas, ejes y contadores; **filete** (`line`) para divisores.
- **Sombra tintada** (`shadow-tint`): las sombras del modo claro son verde muy oscuro translúcido, nunca negro puro.
- En oscuro el papel baja a `dark-paper` y las fichas a `dark-card`, un punto más claras que la hoja, con un canto interior `dark-card-edge`.

### Named Rules
**La Regla de Un Significado.** Un color = una cosa en todo el proyecto. El color de un partido sigue a la entidad, no a su posición; filtrar nunca repinta a los que quedan. Morado = fragancias, naranja = makeup, verde azulado = regla + DAs, azul marino = consenso (solo histórico).

**La Regla del Triángulo.** Verde y rojo de estado nunca van solos: el signo va con un triángulo hacia arriba (bueno) o hacia abajo (crítico) y la cifra con su signo.

## Typography

**Display Font:** Bricolage Grotesque, autoalojada en el HTML (woff2 variable, ejes wght 200–800 y opsz), con Segoe UI y system-ui de reserva.
**Body Font:** Bricolage Grotesque.
**Label/Mono Font:** ui-monospace (SF Mono, Menlo, Consolas) solo para códigos EAN.

**Character:** Grotesca humanista con tamaño óptico: los titulares grandes cierran el tracking y suben el eje opsz; el texto de trabajo queda abierto y legible. La monoespaciada marca que algo es un código, no un nombre.

### Hierarchy
- **Numeral** (800, 54px, opsz 96): total de escaños en el centro del hemiciclo.
- **Brand** (800, 18px, opsz 36): nombre en la tira superior.
- **Headline** (750, 18px, opsz 32): nombre de la selección.
- **Title** (700, 17px, opsz 28): título de cada hoja; cifras grandes de la tabla de especificaciones (750, 17px).
- **Card title** (750, 15.5px, opsz 24): nombre dentro de la ficha.
- **Body** (400, 13.5px, 1.45): todo el texto de trabajo; notas a 12px en `muted`, máximo 64ch.
- **Label** (650, 12px): cabeceras de tabla, pestañas (650 al tamaño del cuerpo), facetas (650, 13px).
- **Code** (600, 12px, monoespaciada): código EAN en tablas y en la cabecera de la ficha.

### Named Rules
**La Regla del Código.** La monoespaciada es solo para códigos EAN; nombres, cifras y etiquetas van en Bricolage con cifras tabulares.

## Layout

La mesa es una rejilla fija bajo las reglas (22px): tira superior a lo ancho; filtros (252px) | parlamento encima del histórico (flexible) | selección (372px); separación de 14px y margen de 16px. Por debajo de 1240px las columnas laterales bajan a 228px y 330px.

La cuadrícula del tapete arranca en (22px, 22px) y mide centímetros CSS reales (1cm ≈ 37.8px). Las fichas sueltas se encajan en sus líneas de 1 cm al soltarlas; al arrastrar, la ficha proyecta su ancho y alto como una marca en las reglas. «Comparar en fila» pliega las fichas (300px) y las coloca en rejilla bajo la hoja del parlamento, que sigue entera a la vista, con un paso redondeado a centímetros y medio centímetro entre filas.

Por debajo de 960px la mesa pasa a una columna: desaparecen la regla vertical, la capa flotante, los hilos y la bandeja; las fichas se apilan en flujo entre el parlamento y el histórico.

## Elevation & Depth

Profundidad física y corta, de objeto sobre una mesa: cada sombra tiene un canto de 1px (el grosor del papel) y una difusa. La hoja apoya; la ficha levantada se separa con una sombra larga. En claro las sombras van tintadas en verde muy oscuro; en oscuro, negras y más densas.

### Shadow Vocabulary
- **Apoyada** (`box-shadow: 0 1px 0 rgba(12,34,26,.10), 0 2px 7px rgba(12,34,26,.20)`): hojas y fichas en reposo. Oscuro: `0 1px 0 rgba(0,0,0,.35), 0 3px 10px rgba(0,0,0,.45)`.
- **Encima** (`--sh-top: 0 1px 0 rgba(12,34,26,.10), 0 8px 22px rgba(12,34,26,.28)`; en oscuro, la misma sombra en negro): la ficha que está delante del montón.
- **Levantada** (`box-shadow: 0 2px 0 rgba(12,34,26,.08), 0 22px 44px rgba(12,34,26,.38)`): ficha arrastrándose, desplegable de búsqueda, tooltips. Oscuro: `0 2px 0 rgba(0,0,0,.3), 0 24px 48px rgba(0,0,0,.6)`.

### Named Rules
**La Regla del Levantar.** Al coger una ficha crece la sombra a «levantada», se inclina −0.8deg y escala a 1.015; al soltarla vuelve a apoyar y se encaja en la cuadrícula.

## Shapes

Esquina de papel cortado: 3px (`rounded.r`) en hojas, fichas, botones, campos, chips, tooltips y filas. 2px (`rounded.tick`) para muestras de color, casillas y segmentos de la barra de volumen. Escaños del hemiciclo, círculos. Los divisores son filetes de 1px en `line`; las tablas abren con un filete de tinta de 1.5px.

## Components

### Buttons
- **Shape:** esquina de papel (3px).
- **Primary:** tinta sobre papel invertido (`ink` de fondo, `paper` de texto), 7px 12px, peso 600.
- **Hover / Focus:** hover a `ink-2` (solo con puntero fino); foco con contorno de 2px en tinta y 2px de separación; al pulsar escala a 0.97 en 160ms.
- **Ghost:** transparente con filete `line`; en hover el filete pasa a `ink-2`.
- **Icono (28px):** sin borde, `muted`; activo (chincheta) en `ink` sobre `paper-2`.

### Chips
- **Filtro activo:** `paper-2` con filete `line`, 12.5px, etiqueta de la faceta en `muted` y aspa para quitarlo.
- **Leyenda del gráfico:** papel con filete; apagada = texto `muted` y muestra al 30%.

### Cards / Containers
- **Hoja:** `paper`, 3px, sombra apoyada, cabecera con título a 16px de margen y pista en `muted` a la derecha.
- **Ficha flotante:** 340px, `card`, canto interior `card-edge`, cabecera arrastrable con muestra del partido, código o nombre, chincheta y cierre; cuerpo 11px 13px.
- **Ficha plegada (comparar):** 300px; solo nombre, una cifra y su curva (la curva se quita si no cabe).
- **Tabla de especificaciones:** filete de tinta arriba, filas con filete `line`, etiqueta a la izquierda y cifra tabular grande a la derecha con su triángulo.

### Inputs / Fields
- **Style:** `paper-2`, filete `line`, 3px, icono de lupa en `muted`.
- **Focus:** el campo pasa a `paper` y el filete a `ink-2` (160ms).

### Navigation
- **Pestañas:** texto 650 en `muted`; la activa en `ink` con subrayado de 2px que crece desde la izquierda (220ms).
- **Segmentado:** borde de tinta; la opción activa invertida.

### Hemiciclo
Un punto por EAN en filas uniformes, número total en el centro, partidos por bloques de izquierda a derecha, Empate en gris; aparece con un barrido de 320ms. Escaño abierto con contorno de tinta de 2.4px. Debajo, la barra de volumen (9px, segmentos de 2px de radio).

### Hilos
Línea de 1.6px del color del partido entre la ficha y su escaño, con un punto de anclaje bordeado en papel. Rodea la hoja por el tapete sin tachar nombres; en la fila de comparar no se dibujan.

### Movimiento
- **Curva:** `cubic-bezier(0.23, 1, 0.32, 1)` para casi todo; `cubic-bezier(0.77, 0, 0.175, 1)` para los puntos de la brújula (700ms).
- **Duraciones:** abrir ficha 230ms (desde escala 0.93), cerrar 150ms (a 0.96), encajar 180ms, deslizar 220ms, recolocar en fila 360ms; pulsación y hover 160ms.
- **Movimiento reducido:** sin escala, inclinación ni deslizamiento; las fichas se colocan al instante, el barrido del hemiciclo pasa a fundido de 150ms y el resto de transiciones solo cambia la opacidad.

## Do's and Don'ts

### Do:
- **Do** poner el contenido en hojas de papel (3px, sombra apoyada) sobre el tapete verde con su cuadrícula de 1 cm y 5 cm.
- **Do** abrir el detalle como ficha junto al punto pulsado, unida por un hilo, sin sustituir la vista.
- **Do** encajar en la cuadrícula de 1 cm todo lo que se suelta o se recoloca.
- **Do** usar la sombra tintada en verde (`rgba(12,34,26,…)`) en claro y la negra en oscuro.
- **Do** emparejar siempre verde y rojo de estado con su triángulo.
- **Do** respetar `prefers-reduced-motion` con fundidos de 150ms.

### Don't:
- **Don't** repintar un partido ni reutilizar sus colores para otra cosa.
- **Don't** usar el consenso de o9 como referencia fuera de reportes históricos.
- **Don't** usar la monoespaciada para nada que no sea un código EAN.
- **Don't** usar sombras negras puras en modo claro.
- **Don't** volver a la carta de tonos, a la cámara oscura con tarjetas ni al dashboard de tres columnas que sustituye la vista.
