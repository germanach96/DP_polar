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
