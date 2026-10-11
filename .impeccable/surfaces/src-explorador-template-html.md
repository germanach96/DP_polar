---
version: 1
slug: "src-explorador-template-html"
primary_target: "src/explorador_template.html"
related_targets: []
---

Scope: explorador del parlamento (una pantalla, modo Operate). Usuario: el demand planner; filtra 839 EANs y lee hemiciclo, histórico + proyección, trends y perfil político. Restricciones: sin internet, claro y oscuro, colores de partido fijos (PRODUCT.md), datos reales.

## Direction contract
THESIS: El parlamento como carta de tonos de belleza: cada partido es una pastilla de color con su código y cada EAN un chip. Rechaza el dashboard de tarjetas redondeadas con caja oscura y discos numerados.
OWN-WORLD: Cartulina gris neutra en el carril de filtros, blanco de chip en la zona de trabajo, tinta casi negra. Chips rectangulares de esquina viva (2px): bloque de color arriba, tira blanca de etiqueta abajo con número y nombre en grotesca negrita pequeña. Sin sombras ni cajas redondeadas; separación por reglas de 1px y cambio de tono. Oscuro = tapa del abanico (grafito).
STORY: El planner ve de un vistazo cuántos escaños tiene cada partido en su tira de pastillas, filtra y ve el hemiciclo de chips recomponerse, y abre un EAN para ver su chip, su historia y su proyección.
FIRST VIEWPORT: Barra superior (nombre, buscador, volver a todo). Carril izquierdo de filtros sobre cartulina. Centro: tira de 6 pastillas de partido + Empate (escaños grandes en el bloque de color) y debajo el hemiciclo de chips cuadrados con el total; abajo pestañas con el gráfico. Derecha: resumen en cifras y trends.
FORM: carta de tonos / abanico Pantone, puesto 1 de mi lista; seed 89e31015 (pick).
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
