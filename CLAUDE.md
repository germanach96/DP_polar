# Contexto (vigente a 2026-10-10)
Resultados históricos y evidencia: `HISTORIAL.md`. Léelo solo cuando haga falta un número o un resultado anterior.

## Usuario y objetivo
- Demand planner en belleza (fragancias y makeup). Usa o9; horizonte de 9 meses sin el mes en curso; la señal a supply va por EAN.
- Quiere una **regla base defendible con datos** a la que agarrarse.
- **El "consenso" (`cons`) es lo que calcula o9 (el programa) y es lo que quiere sustituir con el parlamento: no se usa como referencia ni como parte de la solución** (corregido 2026-10-10). Las referencias son las 2 reglas y los propios partidos.
- Hoy el equipo aplica un trend YoY 6M plano y es el peor método medido.
- Idea en curso: un **sistema de elecciones** (como el best-fit de o9) donde cada EAN elige su modelo por su rendimiento pasado, comparando también con casa, product line, tamaño y función.

## Cómo trabajar
- Español, lenguaje de negocio, ejemplos concretos, sin jerga sin explicar.
- No inventar datos ni supuestos: si falta algo, preguntar. Si un resultado sorprende, comprobarlo antes de reportarlo.
- Reglas objetivas y reproducibles; preferir lo explicable a lo marginalmente mejor y opaco.
- Python (pandas, statsmodels) en scripts reutilizables en `src/`.
- Git: trabajar en la rama de la sesión; PR a `main` solo cuando el usuario lo pida (él aprueba en GitHub).

## Datos
- **Archivos:** `DATA.xlsx` (fragancias: Burberry, Gucci, Marc Jacobs), `GUMU.xlsx` (Gucci Make up) y `KYMU.xlsx` (Kylie Makeup).
- **Pestañas:** una por foto S&OP (cierre de mes).
  - DATA: 2025-09, 2025-12, 2026-03, 2026-06, 2026-09.
  - GUMU / KYMU: 2025-09, 2026-03, 2026-09.
- **Año fiscal:** julio a junio. `cons` en meses pasados = actuals; también hay EPOS (desde jul-24), DAs, cortes, `isf` y Local/Central.
- **Verdad = última foto (sep-26).** Sep-26 no está cerrado (semana 38).
- **El histórico se reexpresa entre fotos:** oct/nov ~+44%, resto +15–20%. En cada foto se usa el histórico de la última foto truncado en esa fecha. El consenso de las fotos viejas va tal cual.
- **Local:** menos de 6 meses de envíos; quedan fuera. **Central:** 6 meses o más.
- **isf (Ignore System Forecast Flag):** customers ignorados de los 2 seleccionados; es forecast manual.
- **Supply cuts:** inflados por re-pedidos semanales.
- **DAs:** promos o inputs de mercado. Solo desde ene-25 y o9 borra los viejos; la foto sep-26 conserva desde ene-26.

## Reglas decididas (detalle en ESTRATEGIA_FRAGANCIAS.md / ESTRATEGIA_MAKEUP.md)
- **Fragancias:**
  - Base = mismo mes del año pasado + 25% de los cortes − 50% de los DAs+ de ese mes.
  - Forecast = Base × (1 + trend 12M de casa × tamaño, tope ±30%).
  - Trend = suma de 12M / 12M anteriores − 1, sobre actuals de los EANs Central.
  - Tamaños (`src/ptype.py`): ≤15, 20–40, 45–60, 75–125, ≥150/refill, ancilares.
- **Makeup:**
  - Mes ajustado = envío + mín(10% cortes; 10% envío) − 25% DAs+.
  - Forecast = media de 6 meses ajustados × (1 + 50% trend 12M de la función Face/Lips/Eyes, tope ±30%). Plano, sin estacionalidad.
- Se recalcula cada mes para 9 meses; sin factor de corrección ni consenso.

## Comparación contra el consenso (histórica; ya NO se usa: el consenso es la salida de o9 que se quiere sustituir)
- Consenso de la foto tal cual (ya lleva DAs) contra **regla + todos los DAs de la foto** (positivos y negativos, suelo 0).
- **WAPE90** = |Σ forecast − Σ real| / Σ real, por casa × quarter.
- **SPP3** = (Σ real − Σ forecast) / Σ real. Negativo = overforecast.

## Concepto: qué es un EAN y las 3 preguntas que se hace (acordado 2026-10-10)
- **DNI del EAN:** su ID (historia de envíos, cortes, DAs) · familia: categoría → casa → brand → product line · formato: tamaño (fragancias) o función (makeup) · edad (meses desde el lanzamiento = primer mes de 2 seguidos con envío; tramos 6–11, 12–17, 18–25, 26+) · fase (18+ meses: crecimiento / estable / declive frente a su casa, ±15%) · gestión: bandera isf y Central/Local.
- **Las 3 preguntas** (cada partido es una combinación de respuestas):
  1. **¿De dónde parto?** (base) Año pasado o nivel reciente (6M/12M); con temporada (propia, de su línea o casa) o plano.
     - Sustento: la forma de la base cambia el error en 9 de cada 10 EANs; fragancias tiene temporada (51% de sus EANs acierta más con ella), makeup casi plano. Firmeza alta.
  2. **¿A quién sigo?** (trend) Yo, mi línea, mi brand, mi tamaño/función, mi casa, mi categoría, mi fase o los de mi edad; y cuánto me lo creo (fuerza y tope).
     - La edad va aquí: ciclo de vida = seguir a los códigos que tuvieron mi edad (curva hasta 17 meses) y a mi fase después.
     - Sustento: en nuevos (6–11 meses) el ciclo de vida falla 105% vs 276% de las reglas; el 51% acierta más con el trend completo. La fuente del trend no se puede juzgar con sep-25 (casi todos en el tope de −30%; 64% indiferente). Firmeza alta en edad, baja en fuente.
     - Candidato: EPOS (sell-out desde jul-24) como otra fuente de trend.
  3. **¿Cómo limpio la base?** Cuánto resto de los DAs planificados de los meses base y cuánto sumo de cortes.
     - Sustento: solo el 42% del DA planificado de fragancias se convirtió en envío extra (80% makeup); al 72% de los EANs le da igual restar o no y al 79% los cortes. Firmeza media (DAs) y baja (cortes).
- **No son preguntas del EAN:**
  - **DAs futuros:** regla fija para todos (abajo).
  - **Quién elige las respuestas:** el mecanismo de elección (su pasado, sus similares o la coalición).

## Sistema de elecciones (formato fijo)
- **Votantes:** EANs Central con actividad. **Urnas:** quarters completos de cada foto.
- **Diseño (corregido por el usuario 2026-10-10):** los EANs **votan con FY25** (fotos simuladas sep-24, dic-24 y mar-25: 6 urnas = quarters cerrados antes de sep-25) y el partido elegido pronostica **desde la foto sep-25** los 9 meses (Q2 = 1–3 meses, Q3 = 4–6, Q4 = 7–9 de FY26). La foto sep-26 solo da el real. Sin FY25 (nuevos): lo que votaron sus parecidos (casa × tamaño/función con su edad).
- **FY23 recuperado:** jul-22..jun-23 = «Consensus - Final LY M» de la foto sep-26 (coincide al 100% con el histórico). En sep-24 no hay DAs ni bandera.
- **Quién gana cada quarter:**
  - WAPE del EAN en el quarter = |forecast − real| / real (si el real es 0, error absoluto). Gana el menor.
  - Empate exacto → el EAN vota a todos los empatados, hasta 3. Cada voto vale 1.
- **Quién gana cada votante:** el partido con más votos; si empatan, el de menor WAPE sumado; si siguen empatados, "Empate".
- **Modelo vigente: 6 partidos** (decidido por el usuario): Regla fragancias, Regla makeup, Ciclo de vida, Media 6M prudente, Media 6M estacional, Media 12M estacional. Vetado usar solo los últimos 3 meses (base y trend). Detalle: `HISTORIAL.md` §8–9.
  - **Ciclo de vida = un partido con receta según el tipo** (elegido por Claude con autorización del usuario; probado contra dos partidos separados, que empeoran la elección):
    - Fragancias: parecidos = toda su categoría con su edad (±2 meses, mínimo 5) + temporada de su casa.
    - Makeup: parecidos = lanzamientos anteriores de su línea (si no hay 5: función, luego casa), plano.
    - Los dos: base sin restar DAs (los de lanzamiento se repiten como llenado de canal); curva hasta 17 meses; desde 18, trend 12M de su fase.
- **DAs (decidido):**
  - El trend usa actuals.
  - Base: el DA de cada mes se lee de la última foto en la que ese mes aún no estaba cerrado (o9 borra los viejos; `ideo_panel.da_plan`). Cuánto restar es ideología del partido.
  - DAs futuros de la foto = insight, se suman según la bandera de la foto: sin bandera 100%, bandera 1 50%, bandera 2 0% (con bandera 2 el forecast de o9 ya son los DAs: sumarlos duplica).
- **Decisión (solo con el pasado, `HISTORIAL.md` §11):** en sep-25 no existe la foto sep-26, así que se ensaya con el pasado: elegir con Q2–Q3 FY25 y medir en Q4 FY25.
  - Ensayo, error EAN a 7–9 / 4–6 / 1–3 meses: regla 115% / 107% / 88% (total 103%), un partido 99% / 119% / 105% (total 108%), coalición 104% / 113% / 86% (total 100%), **Ciclo de vida solo 98% / 83% / 65% (total 81%)**.
  - Elegir partido por EAN no mejora a la regla: el ganador del pasado repite en FY26 en el 18% de los EANs (azar 17%).
  - **Propuesta de Claude: Ciclo de vida para todos**; confirmada con sep-26: 63% / 50% / 49% (total 53%) vs regla 64% / 53% / 55% (total 57%). Pendiente de que el usuario la apruebe.
- **Ciclo de vida contra el consenso** (solo como comparación, no para decidir; `src/ciclo_vs_cons.py`, `HISTORIAL.md` §12; foto sep-25 → real sep-26, 7–9 / 4–6 / 1–3 meses):
  - EAN a EAN gana en los 3 plazos: 63 / 50 / 49% vs consenso 73 / 55 / 54%.
  - En el total de la casa NO: WAPE90 17.5 / 12.5 / 15.3% vs consenso 19.1 / 7.2 / 11.8% (gana en 3, 1 y 1 de 5 casas); se queda corto (sesgo −10 / −6 / −13%).
  - En el total de la casa acierta más la regla + 100% DAs: 13.9 / 6.2 / 7.8%.
  - Falla con bandera 1: 77% vs 57% del consenso; sumarle el 100% de los DAs lo empeora (102%). Gana en nuevos 6–11 (98 vs 128%) y bandera 2 (82 vs 121%).
- **No repetir:** quarters desbalanceados o incompletos · partidos sin trend · DAs contados dos veces · partidos casi iguales que dividen el voto · usar el consenso como referencia.
- Propuestas anteriores (reemplazadas): 10 partidos (`HISTORIAL.md` §7) y 8 partidos EAN/Línea/Segmento/Casa.
- **Estado al cerrar la conversación (2026-10-10):** el usuario quiere dar un paso atrás y seguir en otra conversación. Abierto:
  - Aprobar o no el Ciclo de vida como base para todos (propuesta de Claude).
  - Por qué el Ciclo de vida acierta EAN a EAN pero se queda corto en el total de la casa, donde la regla + DAs acierta más.
  - Qué hacer con la bandera 1 (ni el 50% ni el 100% de los DAs funcionan).
  - Si elegir por EAN sigue teniendo sentido con un solo año de voto (el ganador no se repite).
- **Reportes:** `reportes/REPORTE_IDEOLOGIA.pdf` es el vigente; el resto, en pausa.

## Reportes (preferencias)
- PDF A4 horizontal: HTML + SVG impreso con Chromium (`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`), fuente Inter. Diseño cuidado, con gráficos, nada que parezca hecho con prisa.
- **Hemiciclo de escaños:**
  - Un punto por EAN, filas uniformes, nada cortado, número en el centro.
  - Partidos por bloque de izquierda a derecha; Empate en gris.
  - Debajo, una **barra de volumen** con el % del real de los EANs que gana cada partido.
- **Tarjetas por grupo:** total, quarter, categoría y casa, tamaño, edad, bandera. Cada una con unidades, hemiciclo, votos, barra de volumen y ganador en EANs y en volumen.
- **Tabla de WAPE90** casa × quarter.
- **Colores** (un significado por color):
  - Morado = fragancias. Naranja = makeup.
  - Verde azulado = regla + DAs. Azul marino = consenso (solo en reportes históricos).
- Titulares con el hallazgo y cifras, comprobados con los datos.
- Revisar todas las páginas en alta resolución antes de enviar.
- Base de código reutilizable: `src/votes_report.py` (geometría `seats()`, CSS) y `src/parliament_report.py` (hemiciclo de varios partidos).

## Código
- **Regenerar datos** (los parquet y pkl de `work/` no se versionan):
  `pip install pandas statsmodels openpyxl pyarrow tabulate reportlab` y luego `python3 src/load.py && python3 src/panel.py && python3 src/mu_load.py`
- **Piezas clave:**
  - `src/house_compare.py`: `frag_rule`, `mu_rule`, `central_mask`, `segments`.
  - `src/methods.py`: `_group_g`, trend por grupo.
  - `src/wape90.py`: `fq`, `cons_da`, `ages`.
  - `src/da_test.py` / `src/mu_backtest.py`: `da_known`, `load()` de makeup.
- **Elecciones:**
  - `src/parliament.py`: partidos y elección; base para el nuevo parlamento.
  - `src/parliament_report.py`: reporte.
  - `src/parliament_vs_cons.py`: prueba contra el consenso.
- **Ideologías (propuesta de 10 partidos, foto sep-25):** `python3 src/ideo_panel.py && python3 src/ideo_engine.py && python3 src/ideo_parties.py && python3 src/ideo_compass.py && python3 src/ideo_report.py && python3 src/ideo_infografia.py`
  - `ideo_engine.py`: banco de 203k estrategias por EAN; `ideo_parties.py`: mejor por EAN, partidos (uno por forma de base), elección, robustez; `ideo_viz.py`: colores y piezas visuales de 10 partidos.
- **Parlamento de 6 (vigente):** `python3 src/fy25_eleccion.py && python3 src/decision_sep25.py && python3 src/fy25_brujulas.py && python3 src/ideologia_report.py` (las posiciones de los partidos salen de `ideo_brujulas6.py`, que requiere antes el bloque de ideologías).
  - `decision_sep25.py`: ensayo con el pasado y decisión. `fy25_eleccion.py`: voto con FY25 (6 urnas), prueba desde sep-25, coalición, parecidos para los nuevos. `fy25_brujulas.py`: posición de cada EAN en las brújulas con FY25.
  - `ciclo_vs_cons.py`: comparación histórica Ciclo de vida vs consenso (no se usa para decidir).
  - `six_multi.py` / `six_sin_consenso.py`: diseño anterior (votar con quarters de FY26 de varias fotos), reemplazado.
  - `ideologia_report.py` → `reportes/REPORTE_IDEOLOGIA.pdf`: concepto (DNI, 3 preguntas, diseño de la prueba), los 6 partidos, brújulas, coalición, prueba honesta y elección.
  - `six_report.py` / `six_infografia.py`: versiones anteriores que comparan con el consenso (históricas).
- **Resto de scripts y reportes:** ver `HISTORIAL.md`.
