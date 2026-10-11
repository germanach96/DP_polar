---
version: 1
slug: "src-explorador-template-html"
primary_target: "src/explorador_template.html"
related_targets: []
---

Scope: explorador del parlamento (una pantalla, modo Operate). Usuario: el demand planner; explora 839 EANs, abre varios a la vez, compara, filtra. Restricciones: sin internet, claro y oscuro según sistema, colores de partido fijos (PRODUCT.md), datos reales. Rechazadas: carta de tonos y cámara oscura con tarjetas («gritan IA»).

## Direction contract
THESIS: El explorador es una mesa de trabajo sobre un tapete de corte: el parlamento es una hoja impresa y cada EAN, partido o grupo se abre como una ficha que levantas, mueves, apilas y comparas sin perder el parlamento. Rechaza el dashboard de tres columnas fijas que sustituye la vista al pulsar.
OWN-WORLD: Tapete verde de corte con cuadrícula de 1 cm y regla numerada en los bordes; hojas de papel blanco neutro con esquina de 3px y sombra corta que crece al levantarlas; tinta casi negra; grotesca humanista (Bricolage Grotesque) y cifras de código en monoespaciada. Oscuro = el mismo tapete de noche.
STORY: El planner ve el parlamento entero, pulsa escaños y partidos para abrir fichas junto al punto pulsado, las ordena en la mesa, compara dos EANs lado a lado y filtra solo cuando lo decide.
FIRST VIEWPORT: Tira superior de papel con nombre, buscador y filtros activos; hoja de filtros plegable a la izquierda; hoja grande del parlamento en el centro (hemiciclo, tira de partidos, barra de volumen) y, debajo en la misma columna, la hoja de histórico y proyección con sus pestañas Partidos y Lista de EANs; hoja de la selección a la derecha (cifras en tabla de especificaciones, trends, perfil). Fichas flotantes encima: nacen junto a la hoja del parlamento, fuera de ella, con un hilo al escaño, para poder seguir pinchando escaños.
FORM: mesa de trabajo / tapete de corte, elegido por el usuario (dirección fijada por el usuario; semilla del sorteo registrada: 89e31015, en .impeccable/questions/roll.json).
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
