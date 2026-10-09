# Contexto: estrategia de forecast de demanda

## Quién soy y qué necesito
Soy demand planner en una empresa de consumo masivo (belleza / fragancias). Trabajamos con o9 como plataforma de forecast y un horizonte corto de 9 meses (excluyendo el mes en curso). La señal de supply se manda a nivel EAN.

Mi objetivo: **encontrar el método de forecast más defendible con datos** y tener un número / rango objetivo que pueda usar como guía en la reunión de consenso.

Actualmente el equipo calcula un trend YoY (p. ej. −6%) y lo aplica plano a todos los quarters. No me convence y quiero demostrar con evidencia si hay algo mejor.

## Problemas conocidos de los datos
- El histórico son **actuals (envíos reales) sin limpiar**: incluye promociones, pedidos puntuales y roturas de stock.
- Esto contamina los trends y hace que un % plano sea poco fiable.
- No hay que asumir que existe una columna de promociones o de stock; revisa qué hay en los datos antes de usarla.

## Cómo quiero que trabajes
1. **Primero inspecciona los datos**: columnas, granularidad (EAN / familia / cliente), rango de fechas, huecos, ceros, valores negativos. Resúmeme lo que hay y pregúntame lo que no esté claro antes de modelar.
2. **No limpies a mano ni inventes ajustes.** Usa reglas objetivas y reproducibles.
3. Explica cada resultado en lenguaje de negocio, en español, con ejemplos concretos. Nada de jerga estadística sin explicar.
4. Trabaja en Python (pandas, statsmodels). Deja el código ordenado en scripts para poder volver a correrlo con datos nuevos.

## Métodos a comparar
Calcula todos sobre los mismos datos y el mismo horizonte:

| Método | Descripción |
|---|---|
| Naïve estacional | Mismo mes del año anterior. Es el suelo: si un método no lo mejora, no aporta. |
| Trend plano actual | Trend YoY 6M (suma / suma − 1) aplicado plano a todos los meses futuros. Es el método actual del equipo. |
| Trend mediana | Mediana de los ratios YoY mensuales de los últimos 6 meses, aplicada al mes homólogo. |
| Trend media recortada | Igual, quitando el ratio mayor y el menor. |
| Trend 3M / 12M | Para ver sensibilidad a la ventana. |
| Histórico limpio + trend | Detectar outliers con regla automática (desviación > X% de la mediana móvil, X a calibrar, empezar en 40%) y sustituirlos por la mediana antes de calcular el trend. |
| Suavizado exponencial con damped trend | statsmodels ETS / Holt-Winters con tendencia amortiguada. |
| Agregado familia → SKU | Calcular el trend a nivel familia y aplicarlo a cada EAN (comparar contra hacerlo EAN a EAN). |

Si ves otro método razonable y simple de explicar, propónmelo.

## Backtesting (lo más importante)
- Simula varios puntos de corte en el pasado (rolling origin): en cada corte, usa solo los datos disponibles hasta ese momento y pronostica los 9 meses siguientes.
- Compara cada pronóstico contra los actuals reales.
- Métricas:
  - **WMAPE** (principal), calculado a nivel EAN.
  - **Bias %** (dirección del error: sobre o subestimación).
  - Desglose por **lag** (mes 1 a 8) y por **quarter**.
  - Si hay segmentación posible (ABC por volumen, o estables vs. volátiles), desglosa también.
- Marca los meses donde los actuals parezcan afectados por roturas (caídas bruscas o ceros) para no penalizar injustamente a ningún método.

## Banda de tolerancia
Para el método ganador, calcula un rango aceptable:
- Error relativo histórico = (actual − forecast) / forecast.
- Límite inferior = forecast × (1 + P10 del error); límite superior = forecast × (1 + P90).
- Calcúlalo por lag (la banda debe ensancharse con el horizonte) y, si hay datos suficientes, por segmento.

## Efecto base
Para cada quarter futuro, muestra qué pasó en el quarter homólogo del año anterior (picos o caídas anómalas). Quiero poder explicar por qué un % plano sobreestima o subestima quarters concretos.

## Entregables
1. Un **Excel** con:
   - Resumen: ranking de métodos por WMAPE y bias, global y por lag/quarter.
   - Forecast de los próximos 9 meses del método ganador con su banda P10–P90.
   - Comparación contra el trend plano actual.
   - Hoja de efecto base por quarter.
   - Lista de outliers detectados y la regla usada.
2. Un **resumen corto en español** (1 página) con:
   - Qué método recomiendas y por qué, con números.
   - El "número para defender": cuánto mejor es que el método actual.
   - Limitaciones y riesgos (calidad de datos, horizonte, segmentos donde ningún método funciona bien).
3. Scripts reutilizables para repetir el análisis cada ciclo.

## Reglas
- No inventes datos ni supuestos de negocio; si falta algo, pregúntame.
- Si un resultado es sorprendente, compruébalo antes de reportarlo.
- Prioriza métodos que pueda explicar en una reunión sobre métodos marginalmente mejores pero opacos.

---

# Estado del proyecto (actualizado 2026-10-09)

## Reglas decididas
Detalle completo en `ESTRATEGIA_FRAGANCIAS.md` y `ESTRATEGIA_MAKEUP.md`. Infografía (inglés) en `INFOGRAFIA_REGLAS.pdf`.

**Fragancias** (Burberry, Gucci, Marc Jacobs):
- Base = mismo mes del año anterior + 25% de los supply cuts de ese mes − 50% de los DAs positivos de ese mes.
- Forecast = Base × (1 + trend 12M de house × tamaño).
- Trend = suma de los últimos 12 meses cerrados / suma de los 12 anteriores − 1.
  - Se calcula sobre actuals puros, con todos los Central (incluidos lanzamientos con 6 o más meses de envíos), y tiene tope de ±30%.
- Tamaños: ≤15 ml, 20–40, 45–60, 75–125, ≥150/refill, ancilares.
- Cada mes se recalcula la regla para los 9 meses siguientes. Sin factor de corrección y sin consenso: el forecast es solo la regla.

**Makeup** (GUMU = Gucci Make up, KYMU = Kylie Makeup):
- Mes ajustado = envío + mín(10% cortes ; 10% envío) − 25% DAs positivos.
- Base = media de los últimos 6 meses ajustados.
- Forecast = Base × (1 + 50% del trend 12M de la función: Face, Lips o Eyes), con tope de ±30%. Es el mismo número para todos los meses.
- Sin estacionalidad: los envíos no repiten patrón (el EPOS sí).
- Cada mes se recalcula todo para los 9 meses siguientes. Sin factor de corrección ni consenso.

**Horizonte:** 9 meses. La regla gana al año pasado y al método actual en cada uno de los 9 meses (`src/horizon9.py`, `work/results/horizon9.md`).

**Excepciones:**
- Local (menos de 6 meses de envíos): fuera de la regla, no tienen histórico.
- EANs de 6 a 17 meses: su año anterior incluye el llenado de canal; revisarlos con cuidado.

## Comparación estándar contra el consenso (decidida 2026-10-09)
- **Script:** `python3 src/wape90.py` → imprime la tabla y guarda `work/wape90.json`.
  - El usuario NO quiere más reportes PDF de esto: solo calcular y darle los resultados en el chat.
  - `src/wape90_report.py` queda solo por si lo pide.
- **Qué se compara:**
  - Consenso de la foto tal cual (ya lleva los DAs).
  - Contra **regla + todos los DAs de la foto** (positivos y negativos, suelo 0 por EAN-mes). Regla sola como referencia.
- **Fotos y quarters:** fotos de cierre de mes, así que el mes de la foto no entra.
  - Sep-25 → Q2 (oct–dic), Q3 (ene–mar), Q4 (abr–jun).
  - Mar-26 → Q4 (abr–jun), Q1 FY27 (jul–sep; sep-26 sin cerrar → jul–ago).
- **Real:** última foto.
- **Universo:** EANs Central de cada casa.
- **Métricas por casa × quarter:**
  - **WAPE90** = |Σ forecast − Σ actuals| / Σ actuals.
  - **SPP3** = (Σ actuals − Σ forecast) / Σ actuals. Negativo = overforecast, positivo = underforecast.
- **Resultado 2026-10-09:**
  - Regla + DAs gana 15/25 (fragancias 10/15, makeup 5/10).
  - WAPE90 medio ponderado: consenso 13%, regla + DAs 11,5%, regla sola 18%.
- **Segunda comparación: votación por EAN** (`python3 src/votes.py`, PDF con `src/votes_report.py` → `reportes/REPORTE_VOTACION.pdf`).
  - Cada EAN vota por el sistema que gana más de sus 5 quarters (menor |forecast − real| en el quarter); también se mide el volumen de los EANs que gana cada uno.
  - Grupos: casa, tamaño, edad, Ignore System Forecast Flag. Colores: verde azulado = regla + DAs, azul marino = consenso (morado/naranja = fragancias/makeup).
  - Resultado 2026-10-09: consenso 530 EANs vs regla + DAs 391 (37 empates); volumen 47% vs 51%.
- **Votación con varios partidos** (`python3 src/multivote.py`, solo resultados en chat).
  - Cada EAN elige su método con sep-25 Q2+Q3 y se prueba con mar-26 Q4 FY26 + Q1 FY27.
  - Partidos: consenso, regla + DAs, año pasado + DAs, trend 6M + DAs, media 6M + DAs.
  - Resultado 2026-10-09:
    - 5 partidos empeora (WAPE90 14,7% contra 14,3% del consenso): la media 6M gana en oct–mar y duplica en abr–jun por la estacionalidad.
    - 2 partidos (consenso / regla + DAs): WAPE90 11,3% contra 14,3% del consenso; error EAN 47,6% contra 48,6%.
    - El ganador del pasado repite solo en el 53% de los EANs (al azar sería 50%). Un solo corte: falta confirmarlo.
- **Votación entre reglas** (`python3 src/rulevote.py` + `src/rulevote_report.py` → `reportes/REPORTE_VOTACION_REGLAS.pdf`).
  - Regla de fragancias vs regla de makeup, aplicadas a todos los EANs Central.
  - 5 quarters comunes: sep-25 Q2/Q3/Q4 FY26 y mar-26 Q4 FY26/Q1 FY27. Las dos reglas llevan los DAs de la foto.
  - Grupo del trend: casa × tamaño (fragancias) o casa × función (makeup).
  - Empate en quarters → decide el error mes a mes. Colores: morado = regla fragancias, naranja = regla makeup.
  - Resultado 2026-10-09: makeup 593 EANs vs fragancias 380 (4 empates); volumen 51% vs 49%.
    - EANs de fragancias: 151–169 en EANs, 54%–46% en volumen.
    - EANs de makeup: 229–424 en EANs, 39%–61% en volumen.
  - Pendiente: ampliar a 9 quarters con las fotos dic-25 y jun-26, que solo existen para fragancias.
- **Parlamento de 6 reglas** (`python3 src/parliament.py` + `src/parliament_report.py` → `reportes/REPORTE_PARLAMENTO.pdf`).
  - Partidos: Año pasado, Regla fragancias, Año pasado × línea (trend de la product line; grupo si la line tiene <5 EANs), Media 6M estacional, Regla makeup, Media 3M.
  - Todos suman los DAs de la foto. Mismo sistema de elección, mismos 5 quarters, todos los EANs.
  - Colores: gris oscuro, morado, azul, frambuesa, naranja y verde azulado.
  - Resultado 2026-10-09: parlamento fragmentado.
    - Media 3M es la primera fuerza en EANs: 374 (38%), pero solo el 21% del volumen. Regla makeup: 193 EANs, 23% del volumen.
    - WAPE90 ponderado: Regla fragancias 14%, Año pasado × línea 16%, Regla makeup 19%, el resto 30–31%.
    - Año pasado, Media 6M estacional y Media 3M se pasan un +27–30% en el total: no tienen trend y suman DAs encima de actuals con promos.
- **Consenso vs Parlamento + DAs** (`python3 src/parliament_vs_cons.py`, solo chat).
  - Cada EAN elige su partido con sep-25 Q2+Q3 y se prueba con mar-26 Q4 FY26 + Q1 FY27.
  - Resultado 2026-10-09: el parlamento pierde.
    - WAPE90: parlamento 28,5% contra 14,3% del consenso. Error EAN: 66,8% contra 48,6%.
    - Duelo EAN a EAN: consenso 478 contra parlamento 362; volumen 66% contra 34%.
    - Ni eligiendo a posteriori con los 5 quarters se gana al consenso: WAPE90 15,3%.
    - El partido elegido repite como el mejor solo el 20% de las veces (al azar sería 17%).
    - Mejor partido único: Regla fragancias para todos, WAPE90 13,8%, pero error EAN 65%.
- **DAs (hablado 2026-10-09):**
  - Suben el forecast unos 16 puntos: ayudan en el total solo a las reglas con trend y empeoran el error EAN de todos los partidos.
  - La foto sep-26 solo conserva DAs desde ene-26. Propuesta pendiente: base limpia de DAs del pasado + DAs futuros para todos, medir la precisión de los DAs y guardar los DAs de cada foto.

## Decisiones / respuestas del usuario
- **Local** = iniciativas con menos de ~6 meses de envíos; luego pasan a Central. Se ignoran en la regla.
- **Ignore System Forecast Flag** = número de customers ignorados de los 2 seleccionados (1 = normalmente el más grande; 2 = ambos). Es forecast manual: darle poco peso.
- **Supply cuts:** inflados por re-pedidos semanales.
- **DAs:** pueden ser promos o inputs de mercado. Más adelante el usuario pasará el volumen de promos a restar.
- **Pendiente:** probar el histórico corregido por outliers de o9 cuando el usuario lo extraiga, comparando regla actual, outliers puros e híbrido.

## Datos (DATA.xlsx, GUMU.xlsx, KYMU.xlsx)
- Una pestaña por foto S&OP.
  - DATA: 2025-09, 2025-12, 2026-03, 2026-06, 2026-09.
  - GUMU/KYMU: 2025-09, 2026-03, 2026-09.
- Año fiscal de julio a junio. `cons` en meses pasados = actuals.
- **El histórico se reexpresa entre fotos.** No es un 20% plano: oct/nov ~+44%, resto ~+15–20%; KYMU +18%.
  - Verdad = última foto. En cada foto se usa el histórico reexpresado truncado.
  - El consenso de las fotos viejas se ajusta por el factor del mes calendario.
- EPOS desde 2024.M07. DAs solo desde ene-25.

## Código (Python: pandas, statsmodels, reportlab, pyarrow)
- **Carga:** `src/load.py` (fragancias) y `src/mu_load.py` (makeup).
  - `src/panel.py` genera `work/*.pkl`; el parquet y los pkl no están versionados, se regeneran.
- **Backtests:**
  - Rolling por EAN: `src/backtest.py` + `src/evaluate.py` + `src/report.py`.
  - Por foto: `src/snapshots.py` + `src/snap_eval.py`.
  - Técnica inicial + corrección: `src/tracking.py`.
  - Lanzamientos: `src/launch_trend.py`.
  - Cortes / DAs: `src/cuts_test.py`, `src/da_test.py`.
  - Makeup: `src/mu_season.py`, `src/mu_backtest.py`, `src/mu_cuts_da.py`, `src/mu_cuts2.py`.
- **Resultados:** `work/results/*.md`. Memoria de trabajo: `work/STRATEGY.md` y `work/NOTES.md`.
- **Reportes por casa (consenso vs regla, fotos sep-25 y mar-26):** `src/house_compare.py` + `src/house_report.py` → `reportes/REPORTE_<casa>.pdf`.
- **Infografía:** `src/infografia.py` (HTML + SVG → PDF con Chromium). Datos de los gráficos en `work/infog_data.json`.

**Cómo regenerar:**
```
pip install pandas statsmodels openpyxl pyarrow tabulate reportlab
python3 src/load.py && python3 src/panel.py && python3 src/mu_load.py
python3 src/infografia.py
```
