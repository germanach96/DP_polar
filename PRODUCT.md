# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Una sola persona: el demand planner de belleza (fragancias y makeup) que lleva este proyecto. Usa los reportes y páginas HTML para su propio análisis: entender los datos por EAN y decidir qué regla base de forecast usar. No hay otros públicos confirmados (equipo, dirección o supply no son destinatarios por ahora).

## Product Purpose
Encontrar y **defender con datos** una regla base de forecast por EAN, objetiva y reproducible, que sustituya al consenso que calcula o9 y mejore el trend YoY 6M plano que aplica hoy el equipo. Las páginas sirven para explicar y justificar la regla: que se entienda qué se prueba, contra qué y con qué resultado. Éxito = una regla explicable, con cifras comprobadas, que el planner pueda sostener.

## Positioning
Un «parlamento» de métodos: cada EAN vota con su propio pasado al partido (receta de forecast) que menos se equivocó con él, como el best-fit de o9 pero a la vista y explicable. Se prefiere lo explicable a lo marginalmente mejor y opaco.

## Operating Context
- Datos: fotos S&OP mensuales de o9 en Excel (`DATA.xlsx` fragancias; `GUMU.xlsx`, `KYMU.xlsx` makeup). Horizonte de 9 meses sin el mes en curso; la señal a supply va por EAN.
- Flujo: scripts Python en `src/` generan JSON/parquet en `work/` y de ahí reportes PDF (A4 horizontal, impresos con Chromium) y páginas HTML interactivas en `reportes/`.
- Las páginas se abren descargadas, como archivo suelto.

## Capabilities and Constraints
- **Los HTML deben funcionar sin internet** (confirmado): un solo archivo con datos, CSS y JS dentro. Cualquier recurso externo (p. ej. fuentes) necesita una alternativa local que mantenga la página legible y funcional.
- Todo en español y en lenguaje de negocio, sin jerga sin explicar (de `CLAUDE.md`).
- Titulares con el hallazgo y cifras, comprobados con los datos. No inventar datos.
- El consenso de o9 no se usa como referencia (solo en reportes históricos).
- Terminología fija: EAN, foto S&OP, casa, línea, tamaño/función, edad, fase, bandera isf, Central/Local, DAs, cortes, EPOS, partido, urna, escaño, WAPE90.

## Brand Commitments
Sin marca corporativa. Compromisos de color ya acordados (un significado por color): morado = fragancias, naranja = makeup, verde azulado = regla + DAs, azul marino = consenso (solo histórico). Hemiciclo con un punto por EAN, filas uniformes, número en el centro, Empate en gris y barra de volumen debajo.

## Evidence on Hand
Resultados reales en `work/*.json` y `HISTORIAL.md`; reportes vigentes en `reportes/` (`REPORTE_IDEOLOGIA.pdf`, `PARLAMENTO.html`, `EXPLORADOR_PARLAMENTO.html`). No hay testimonios, clientes ni benchmarks externos: no fabricarlos.

## Product Principles
1. Explicable antes que marginalmente mejor.
2. Cada cifra mostrada sale de los datos y se puede reproducir con un script de `src/`.
3. Una página = un hallazgo claro arriba; el detalle, después.
4. Funciona en cualquier sitio: descargada, sin conexión, en claro y en oscuro.
