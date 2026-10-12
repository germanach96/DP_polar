---
version: 1
slug: "src-explorador-template-html"
primary_target: "src/explorador_template.html"
related_targets: []
---

Scope: explorador del parlamento (una pantalla, modo Operate). Usuario: el demand planner; explora 839 EANs, abre varios a la vez, compara, filtra. Restricciones: sin internet, claro y oscuro según sistema, colores de partido fijos (PRODUCT.md), datos reales. Rechazadas: carta de tonos y cámara oscura con tarjetas («gritan IA»); mesa de trabajo sobre tapete de corte (sustituida por el lenguaje de Apple a petición del usuario).

## Direction contract
THESIS: El explorador es una app de macOS: el parlamento vive en paneles quietos y cada EAN o partido se abre como una ventana translúcida que nace del escaño pulsado, se lanza con inercia, se asienta con un muelle y se compara sin perder el parlamento. Rechaza el dashboard de tres columnas fijas que sustituye la vista al pulsar.
OWN-WORLD: Lenguaje de Apple pedido por el usuario (2026-10-12): lienzo gris claro (#F5F5F7) / negro en oscuro; paneles blancos de 20px sin borde con sombra difusa; ventanas de 14px en material translúcido con los botones de semáforo de macOS (rojo cierra, amarillo pliega; apagados en la ventana de detrás); controles segmentados con cursor que se desliza; acento grafito (el azul de sistema chocaba con el partido Media 6M prudente); letra del sistema de Apple (SF Pro) con Inter incrustada como reserva fuera de Apple. Movimiento: muelles por eje con respuesta y amortiguación, proyección de la inercia, resistencia en los bordes, interrumpible en cualquier momento.
STORY: El planner ve el parlamento entero, pulsa escaños y partidos para abrir ventanas junto al parlamento, las lanza y ordena, pliega las que no necesita, compara varios EANs en fila y filtra solo cuando lo decide.
FIRST VIEWPORT: Título grande sobre el lienzo con buscador y filtros activos; panel de filtros a la izquierda (lista de barra lateral); panel del parlamento en el centro (hemiciclo, leyenda, barra de volumen) y debajo el panel de histórico y proyección con control segmentado (Histórico, Partidos, Lista de EANs); panel de la selección a la derecha (cifras en lista agrupada, trends, perfil). Ventanas flotantes encima, nacidas junto al parlamento y fuera de él; al pasar por una, su escaño se ilumina.
FORM: app de macOS / lenguaje de Apple, fijado por el usuario (sustituye a la mesa de trabajo; semilla del sorteo anterior 89e31015 sin uso).
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
