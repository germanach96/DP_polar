# STRATEGY — conclusiones del análisis (memoria para Claude; base para el resumen al usuario)

## 0. DECISIONES DEL USUARIO (sesión 2, 2026-10-09) — PREVALECEN sobre lo de abajo
1. Reexpresión del histórico: asumir +20% fijo -> consenso de versiones 2025-09 y 2025-12 x1.20 (`consensus_adj20`).
   Medido: ratio total 1.21 / 1.20 (BBY 1.18-1.20, MJ 1.15-1.16, Gucci 1.26-1.27).
   OJO: con x1.20 ese consenso pasa a bias +17% (maduros) vs +4% sin ajustar -> o ya estaba en perímetro nuevo, o sobreestimaba. Comentar al usuario si sale.
2. Local: IGNORAR (no hay datos). Excluidos del universo (resp 2026-09 == Local).
3. isf = nº de customers ignorados de 2 seleccionados (1 = normalmente el más grande; 2 = todos) -> forecast manual. Excluidos también (isf>=1).
   => UNIVERSO OFICIAL = sin Local y sin isf>=1. Archivos con sufijo _f (bt_*_f.parquet, ev_f.parquet, results/backtest_f.md, results/forecast_f.md).
   `python3 src/backtest.py --fast|--v2|--v3|--v4|--cons` (filtra por defecto; `--all` = universo completo antiguo).
4. Pregunta 4 (consenso maduros FY27 muy por debajo de LY) quedó resuelta: era contaminación de Local/isf. En el universo filtrado el ganador queda a -7%..+11% del consenso actual.

## 0b. RESULTADOS EN UNIVERSO OFICIAL (13 cortes, maduros)
- EAN-mes WMAPE: resc_median 55.0% (bias -1.5%), resc_x40_cap 56.2% (-2.2%), house12 62.3%, naive 68.1% (+10.8%), flat6 (equipo) 73.3% (-0.7%).
  -> **número para defender: -17/-18 puntos de error vs método actual a nivel EAN**; gana en 13/13 cortes.
- House-quarter: resc_x40_cap 12.4% (mejor) vs flat6 ~20.7%, naive 18%.
- Total house 8 meses (todos los EANs del universo, incl. lanzamientos Central): house12 9.9% (bias +3%), resc_x40_cap 10.3% (bias 0%), flat6 17.8% (+9%), naive 19.6% (+20%).
  Por house (resc_x40_cap): BBY 7.3%, MJ 13.2%, Gucci 12.3%.
  => SIN Local, el LY plano YA NO es la guía: sobreestima ~20%. **La guía total = LY x (1 + trend 12M de la house)**. (Sustituye §1.A de abajo.)
- Vs consenso real (maduros, 4 versiones): resc_median 55.0% / resc_x40_cap 56.5% / consenso 65.3% (bias +4%) / consenso x1.20 70.1% (bias +17%).
- Trends 12M house (limpios) a 2026-08: BBY -10.4%, MJ -9.6%, Gucci -17.0%, Kylie +57% (tope ±30%). Trend 6M bruto (estilo equipo): -14.6%, -14.1%, -30.4% -> 6M exagera la caída.
- Bandas ganador: house-quarter P10 -26% / P50 0% / P90 +46%; house-mes por lag: lag1 -46%/+95% ... lag8 -39%/+38%. EAN-mes no sirve (P10=-100%).
- Forecast oct-26..may-27 vs consenso actual (universo oficial): BBY +1..+6%, MJ -7..+6%, Gucci +4..+11% -> consenso actual razonable; Gucci algo bajo.
- Efecto base FY27.Q2 (oct-dic): LY por encima de su base limpia +19% BBY, +22% MJ, +22% Gucci (carga de Navidad desplazada a Q2 en FY26 por cortes en Q1). Q3 también inflado ~+13..23%.

(Secciones siguientes = sesión 1, universo completo incl. Local; mantener como contexto, §1.A superado por §0b.)


Estado: sesión 1 (2026-10-09). Evidencia de 13 cortes rolling (orígenes 2025-07..2026-07, horizonte 8 meses
excluyendo mes en curso) + 4 versiones reales de consenso (2025-09, 2025-12, 2026-03, 2026-06). Verdad = última versión.
OJO: todo el backtest cae en un solo "régimen" (FY26: caída que se desacelera). Validar con más años cuando haya.

## 1. Respuesta corta ("estrella polar")
Separar SIEMPRE el número en dos piezas:

A) **Número total por house (lo que se defiende en consenso)**:
   - Regla: **total próximos meses ≈ mismo período del año anterior (LY plano, sin aplicar trend)**, revisado con el efecto base.
   - Evidencia (total house, 8 meses, incl. lanzamientos, sin Kylie): naive WMAPE 8.5% bias -1%; consenso real 10.3% bias +6%;
     trend 12M (flat12) 10.4% bias -10%; trend house 12M 18.9% bias -19%; trend 6M EAN (método equipo) 11.6% bias -9%.
     House-quarter: naive 12.2%, flat12 11.7%, consenso 15.1%.
   - Por qué: los maduros caen (~-10%/-20% LFL) pero los lanzamientos lo compensan casi exacto -> a nivel total el año pasado es la mejor guía.
     Aplicar el trend YoY de la house al total DOBLE-CUENTA la caída (el trend ya refleja canibalización pero la nueva innovación vuelve a llegar).
   - Banda total 8 meses (naive, house): P10 -8% / P50 +1% / P90 +19% (error rel. (A-F)/F). House-quarter: P10 -15% / P50 +1% / P90 +28%.
   - Excepción: **CP-Marc Jacobs** crece por lanzamientos (Daisy body mists, Just Perfect): naive lo subestimó +11..+33% en 10/13 cortes
     -> para MJ el LY plano es suelo, no punto medio. BBY y Gucci: naive dentro de ±8% en los 13 cortes.

B) **Reparto a EAN (señal a supply)**: método ganador `resc_x40_cap`:
   1. Total house-mes = LY real de la house en ese mes x (1 + g), g = trend 12M de la house calculado sobre histórico limpio, con tope ±30%.
   2. Reparto a EAN = peso de cada EAN en la base LY "limpia" (outliers sustituidos por la mediana móvil 5m, desestacionalizada con el índice de la house; regla |A-med|>40% med).
   Resultados (EANs maduros, 13 cortes): WMAPE EAN-mes 56.8% vs naive 69.4% vs trend plano 6M EAN (equipo) 74.9% -> **-18 pts vs método actual, -13 pts vs naive**.
   Gana a flat6 en 13/13 cortes (EAN) y 11/13 (house). Brand-mes 33.0% (mejor), house-quarter 12.9% (mejor), bias -3%.
   Variante casi igual y más simple de explicar: `resc_median` (suavizar toda la base con mediana 5m): EAN 55.5%, house-q 13.8%.
   Vs consenso real (maduros, 4 versiones): consenso 65.3% / combo 55.8% / house12_clean 55.9%.
   NOTA: el % de outliers con x=40% es 38% de los puntos -> en la práctica es SUAVIZADO, no limpieza de excepciones. Explicarlo así.

C) **Lanzamientos / Local** (los EANs 'Local' son ~todos innovación; 0 EANs Local en el universo maduro):
   - Ningún método estadístico funciona bien (WMAPE ~100%). El consenso mejora con las versiones (EANs jóvenes: bias +41% (2025-09), +27%, +10%, +1% (2026-06)).
   - Regla de forma (curva de vida, 89 lanzamientos): mes 0 = llenado de canal ≈ 60% de los 3 primeros meses; después ritmo mensual ≈ 7-8% del mes de lanzamiento
     (mediana 0.13-0.15 x media mensual de los 3 primeros meses). Primer año: 58% del volumen en los 3 primeros meses, 16% meses 3-5, 23% meses 6-11.
   - Ritmo post-lanzamiento (young_lvl3_skip2: media desestacionalizada de los últimos 3 meses sin los 2 primeros de vida) ≈ consenso (97.5% vs 103% WMAPE) -> sirve como sanity check, no sustituto.
   - Sesgo histórico del consenso en lanzamientos = sobreestimar. Regla: desconfiar de cualquier forecast de lanzamiento cuyo mes 6+ supere ~15% del mes 0.

## 2. Lo que NO funciona (con números, EAN maduros WMAPE)
- Trend YoY 6M EAN a EAN (método equipo) 74.9%: peor que naive (69.4%). 3M aún peor (87.7%). Mediana/media recortada 6M ≈ 75-83%.
  Cuanto más corta la ventana y más bajo el nivel (EAN), peor: el ratio YoY de un EAN-mes es ruido (pedidos puntuales, timing).
- ETS/Holt-Winters damped por EAN: 166% (explota con 3 años de historia lumpy). ETS a nivel house + reparto: 73.6%. Descartado.
- Ajustar por supply cuts (sumar cuts/4): 76.5%, peor -> los cortes no son "demanda perdida" fiable (confirmado lo que dijo el usuario).
- Trend de product line: explota en líneas nuevas (bias +190% en lanzamientos). Nunca usar trend de línea para EANs jóvenes.

## 3. EPOS
- Solo desde 2024.M07 -> trend YoY EPOS disponible desde 2025.M07 (7 cortes con ventana 6M).
- Con datos justos (orígenes >=2026-01): trend EPOS house 6M EAN 58.0% vs trend envíos house 12M 59.6% vs naive 66.3%. House-mes: EPOS ~23% vs flat12 20.5%.
  => EPOS ≈ tan bueno como trend de envíos de 12M, mejor que trend envíos 6M. Útil como **semáforo**, no como motor.
- Señal actual (12M a 2026-08, EANs con EPOS ≈ 82-88% del volumen): sell-out YoY BBY -20%, MJ -7%, Gucci -23%; envíos mismos EANs -9%, -12.5%, -17.5%.
  -> BBY y Gucci venden fuera bastante peor de lo que enviamos: riesgo de stock en retailer / corrección futura. MJ: sell-out mejor que sell-in.
  Ratio EPOS/envíos (sell-through) 81% BBY, 90% MJ, 87% Gucci.

## 4. Efecto base / estacionalidad
- Fragancia: Q1 fiscal (jul-sep) = pico de carga de Navidad. Peso Q1 en H1: FY24 66%, FY25 67-70%, **FY26 55-58%** -> en FY26 la carga se desplazó a Q2
  (cortes de supply FY26.Q1 = 518k, 6% de envíos vs 2-3% normal). Por eso FY26.Q1 -24% YoY y FY26.Q2 +19% YoY.
  => Para FY27: Q1 tiene comparable fácil, **Q2 (oct-dic) tiene comparable inflado** (LY por encima de su base limpia: BBY +23%, MJ +31%, Gucci +41%).
  Un % plano sobreestima FY27.Q2 y subestima FY27.Q1. Recomendación: pronosticar H1 como bloque (YoY H1: FY25 -4%, FY26 -10%) y fasear Q1/Q2 con la media de fases de años "normales".
- Todos los métodos fallaron igual por quarter en FY26: Q1 sobreestimado, Q2 subestimado (-25/-33% bias) -> es fasing, no tendencia.
- FY27.Q4 (abr-may) MJ: LY inflado +81% vs base limpia (pico puntual) -> no extrapolar.

## 5. Diferencias por house / categoría
- Kylie Makeup = 9 EANs de accesorios, ~75k u/año: demasiado pequeño para concluir fragancia vs maquillaje. Trend explosivo (+105%): usar tope ±30%.
- BBY: el más estable y predecible (house-quarter WMAPE ~11%). Gucci ~11-12%. MJ ~19-21% (más dependiente de lanzamientos).
- isf (Ignore System Forecast): valor 1 = EANs viejos/en salida (última venta mediana 2024-12, poco volumen); valor 2 = lanzamientos recientes (primera venta mediana 2025-11).
  Error enorme para cualquier método en isf=1 (forecast manual sobre items casi muertos). PREGUNTA: confirmar significado de 2.

## 6. Forecast actual (versión 2026-09, oct-26..may-27) — en work/results/forecast.md
- EANs maduros: consenso actual = -11% BBY, -6% MJ, -24% Gucci vs LY; método ganador ≈ LY (0%/+15%/+5%). El consenso recorta fuerte a los maduros
  (especialmente Gucci) y mete mucho volumen en lanzamientos (BBY Q2: 37% del consenso son EANs jóvenes). Backtest: consenso en maduros tuvo bias +4% -> el recorte actual parece agresivo, pero puede haber info de negocio (delistings) -> PREGUNTAR.

## 7. Preguntas abiertas para el usuario
1. Reexpresión +20% del histórico desde versión 2026-03: ¿cambio de perímetro? (afecta comparar consensos 2025-09/12).
2. "Local" = innovación? En 2026-06 todo figura Local (¿error de extracción?). Lista en work/local_list.txt.
3. isf = 2 significa?
4. ¿Hay delistings / cambios de surtido que expliquen el -24% de Gucci maduro en el consenso FY27?
5. ¿El número a defender es a nivel house total o por brand?

## 8. Ideas pendientes (siguiente sesión)
- Excel + resumen 1 página (entregables CLAUDE.md) cuando el usuario lo pida.
- Banda por segmento (ABC) y por house del ganador; banda del total naive por house.
- Probar "H1 en bloque + fasing medio" como método explícito en backtest (requiere más años para validar).
- Regla explícita de lanzamientos con curva (mes0 -> decaimiento) en backtest vs consenso.
- Revisar si 'consensus' en versión vieja es perímetro viejo (scope adj empeoró -> parece que ya estaba en perímetro nuevo?).
