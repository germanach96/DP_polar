# Contexto: estrategia de forecast de demanda

## Quién soy y qué necesito
Soy demand planner en una empresa de consumo masivo (belleza / fragancias). Trabajamos con o9 como plataforma de forecast y un horizonte corto de 8 meses (excluyendo el mes en curso). La señal de supply se manda a nivel EAN.

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
- Simula varios puntos de corte en el pasado (rolling origin): en cada corte, usa solo los datos disponibles hasta ese momento y pronostica los 8 meses siguientes.
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
   - Forecast de los próximos 8 meses del método ganador con su banda P10–P90.
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
