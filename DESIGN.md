---
name: Parlamento de la demanda
description: Reportes y páginas del parlamento de forecast por EAN: serios como una institución, vivos al tocarlos.
colors:
  ink: "#17161D"
  ink-2: "#4B4958"
  muted: "#706E82"
  paper: "#F2F2F5"
  surface: "#FFFFFF"
  line: "#DEDDE6"
  soft: "#EAE9F0"
  chamber: "#15141B"
  chamber-2: "#1F1E27"
  chamber-ink: "#F1F0F6"
  chamber-muted: "#A3A1B4"
  chamber-line: "#302E3B"
  focus-violet: "#6250d6"
  rule-teal: "#0F8A86"
  empate-grey: "#B7BCC4"
  party-regla-fragancias: "#6250d6"
  party-media-12m-estacional: "#eda100"
  party-media-6m-estacional: "#00a3c4"
  party-regla-makeup: "#eb6834"
  party-media-6m-prudente: "#2a78d6"
  party-ciclo-de-vida: "#e87ba4"
typography:
  display:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2.6rem, 6vw, 4.9rem)"
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.9rem, 3.6vw, 2.9rem)"
    fontWeight: 700
    lineHeight: 1.04
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.15rem"
    fontWeight: 650
    lineHeight: 1.2
  body:
    fontFamily: "Public Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Public Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "0.78rem"
    fontWeight: 600
    letterSpacing: "0.1em"
rounded:
  sm: "6px"
  md: "10px"
  lg: "14px"
  pill: "999px"
spacing:
  s1: "0.75rem"
  s2: "1rem"
  s3: "1.5rem"
  s4: "2.25rem"
  s5: "3.5rem"
  s6: "5.5rem"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "0.65rem 1rem"
  chip-filter:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0.38rem 0.7rem"
  chip-filter-selected:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.pill}"
  panel:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.lg}"
    padding: "1.5rem"
  chamber-panel:
    backgroundColor: "{colors.chamber}"
    textColor: "{colors.chamber-ink}"
---

# Design System: Parlamento de la demanda

## Overview

**Creative North Star: "El Parlamento"**

Cada página es una sesión de una cámara moderna. El hemiciclo es el centro de gravedad: un punto por EAN, coloreado por el partido que elige, en una cámara oscura que da peso institucional. Alrededor, papel claro y tipografía firme: titulares con el hallazgo y la cifra, nunca un adjetivo vacío. El tono es serio porque la página defiende una regla con datos; la interacción es viva porque el usuario explora esos datos con la mano: filtrar, pulsar un escaño, cambiar de brújula.

La densidad es de informe, no de folleto: mucha información legible, bien jerarquizada, sin héroes gigantes ni decoración. El movimiento existe para explicar (los escaños que se llenan, el escrutinio urna a urna, los EANs que viajan entre brújulas) y para responder al tacto (pulsar, filtrar, seleccionar), con respuesta visible e inmediata.

**Key Characteristics:**
- Cámara oscura (`chamber`) para el hemiciclo y los momentos clave; papel claro (`paper`) para el análisis.
- Un significado por color: los 6 colores de partido, morado = fragancias, naranja = makeup, verde azulado = regla.
- Plano: profundidad por capas de tono y líneas finas, nunca por sombras.
- Interacción táctil: cada control responde al pasar el ratón y al pulsar.
- Funciona descargado y sin conexión, en claro y en oscuro.

## Colors

Neutros fríos con un leve sesgo violeta, una cámara casi negra y una paleta categórica de 6 partidos validada para daltonismo.

### Primary
- **Tinta de Cámara** (#17161D): texto principal, botón primario, regla gruesa de sección.
- **Cámara** (#15141B): fondo del panel del hemiciclo, veredictos y barra de navegación.

### Secondary
- **Violeta Foco** (#6250d6): foco de teclado, partido elegido en gráficos, selección activa. También es el color de Regla fragancias (morado = fragancias).
- **Verde Azulado Regla** (#0F8A86): la regla de referencia en comparaciones (regla + DAs).

### Party palette (categórica, orden fijo de bloques)
- **Regla fragancias** (#6250d6) · **Media 12M estacional** (#eda100) · **Media 6M estacional** (#00a3c4) · **Regla makeup** (#eb6834) · **Media 6M prudente** (#2a78d6) · **Ciclo de vida** (#e87ba4) · **Empate** (#B7BCC4).

### Neutral
- **Papel** (#F2F2F5): fondo de página.
- **Superficie** (#FFFFFF): paneles y tablas.
- **Tinta 2** (#4B4958) y **Apagado** (#706E82): texto secundario y etiquetas.
- **Línea** (#DEDDE6) y **Suave** (#EAE9F0): divisores, fondos de barra, filas al pasar el ratón.
- **Cámara 2 / Tinta de cámara / Línea de cámara** (#1F1E27 / #F1F0F6 / #302E3B): superficies y texto dentro de la cámara.

### Named Rules
**La Regla de Un Significado.** Un color = una cosa en todo el proyecto. El color de un partido sigue a la entidad, no a su posición; filtrar nunca repinta a los que quedan.

**La Regla del Texto Legible.** Sobre un color de partido claro (amarillo, turquesa, rosa) el texto va en Tinta de Cámara; sobre los oscuros, en blanco. Se calcula por luminancia, no a ojo.

**La Regla del Consenso Ausente.** El azul marino del consenso de o9 solo aparece en reportes históricos.

## Typography

**Display Font:** Archivo, con eje de anchura (Helvetica Neue, Arial)
**Body Font:** Public Sans (Segoe UI, system-ui)

**Character:** Archivo comprimido y pesado da voz institucional a los titulares; Public Sans, la tipografía del gobierno de EE. UU., aporta lectura cívica y neutra. En los PDF impresos con Chromium se usa Inter / Inter Display, instaladas en el sistema.

### Hierarchy
- **Display** (800, clamp(2.6rem, 6vw, 4.9rem), 0.95, anchura 78%): solo el título de la cámara.
- **Headline** (700, clamp(1.9rem, 3.6vw, 2.9rem), 1.04, anchura 88%): el hallazgo de cada sección, máximo unos 22 caracteres por línea.
- **Title** (650, 1.15rem, 1.2): títulos de panel y tabla.
- **Body** (400, 1rem, 1.6): texto corrido, máximo unos 62 caracteres por línea.
- **Label** (600, 0.78rem, tracking 0.1em, mayúsculas): orden del día y cabeceras de tabla.

### Named Rules
**La Regla de la Cifra Tabular.** Toda cifra en tabla, recuento o KPI usa `font-variant-numeric: tabular-nums`.

**La Regla Sin Conexión.** Las fuentes web siempre llevan alternativa del sistema: sin internet la página se lee igual de bien.

## Layout

Columna de 1160px como máximo, con margen lateral `clamp(16px, 4vw, 40px)`. Las páginas didácticas avanzan como un orden del día: cada sección tiene una cabecera de dos columnas (titular a la izquierda, explicación a la derecha) y su contenido debajo. Los exploradores ocupan una sola pantalla: filtros a la izquierda (250px), hemiciclo y gráfico en el centro, volúmenes, trends y perfil político a la derecha (360px), con scroll solo dentro de cada panel. Por debajo de 900px todo pasa a una columna. El ritmo de espacios sigue s1–s6 (0.75 a 5.5rem).

## Elevation & Depth

Sistema plano. La profundidad se consigue con capas de tono (papel → superficie → suave) y con el contraste entre la cámara oscura y el papel claro. Las separaciones son líneas de 1px (`line`) o rejillas con `gap: 1px` sobre fondo de línea. Única excepción funcional: el desplegable de búsqueda y los tooltips flotan sobre el contenido con una sombra difusa (`0 12px 32px rgba(0,0,0,.22)`), porque tapan otros elementos.

### Named Rules
**La Regla Plana.** Ninguna tarjeta ni panel lleva sombra en reposo. La sombra solo existe en lo que flota sobre otra cosa.

## Shapes

Radios contenidos: 6px en botones y pestañas, 10–14px en paneles, pastilla (999px) en chips y filtros. Los marcadores de partido son círculos con número; el centro de una selección es un rombo. Las barras de datos tienen el extremo redondeado en 3–5px y 2px de separación entre segmentos.

## Components

### Buttons
- **Shape:** 6px, padding 0.65rem 1rem.
- **Primary:** fondo Tinta de Cámara, texto Papel, peso 600.
- **Interacción (vivo y táctil):** al pasar el ratón, cambio de tono en 160ms; al pulsar, `scale(.97)` con `cubic-bezier(0.23, 1, 0.32, 1)`; `disabled` al 50% de opacidad.

### Chips / filtros
- **Style:** pastilla con borde Línea sobre Superficie; número de partido en un disco de su color.
- **State:** seleccionado = borde o fondo Tinta; los no seleccionados se atenúan al 45% cuando hay foco en uno.

### Panels
- **Corner Style:** 14px. **Background:** Superficie. **Border:** 1px Línea. **Shadow:** ninguna. **Padding:** 1.5rem.

### Navigation
- Barra fija de cámara (92% de opacidad, desenfoque 10px) con el orden del día; la sección activa se marca con fondo Cámara 2. En móvil se oculta la lista.

### Hemiciclo (componente firma)
- Un punto por EAN, filas uniformes con la geometría `seats()` de `src/votes_report.py`, partidos por bloque de izquierda a derecha, Empate en gris al final y número total en el centro. Entra barriendo de izquierda a derecha (stagger por ángulo, unos 1.2s), con el número contando. Debajo, la barra de volumen con el % de cada partido.

### Brújula política
- Cuadrícula de 4 cuadrantes en tonos alternos (Suave / Papel); puntos de EAN coloreados por partido con tamaño por volumen; marcadores de partido numerados. Al cambiar de pregunta, los puntos viajan a su nueva posición (`cubic-bezier(0.77, 0, 0.175, 1)`, 0.95s, con desfase por punto).

## Do's and Don'ts

### Do:
- **Do** abrir cada sección con el hallazgo y su cifra en el titular, comprobada con los datos.
- **Do** dar respuesta visible a cada control: tono al pasar el ratón, `scale(.97)` al pulsar, transiciones de 150–250ms con ease-out fuerte.
- **Do** respetar `prefers-reduced-motion`: sin desplazamientos, solo fundidos.
- **Do** validar con `dataviz` cualquier color nuevo, en claro y en oscuro.
- **Do** poner nombre y número visibles junto a cada color de partido.

### Don't:
- **Don't** poner sombras en paneles o tarjetas en reposo.
- **Don't** reutilizar un color de partido o de categoría para otra cosa.
- **Don't** depender de recursos de internet sin alternativa local: la página debe funcionar descargada.
- **Don't** usar el consenso de o9 como referencia fuera de reportes históricos.
- **Don't** animar por decorar: si una animación no explica ni responde a un gesto, no va.
