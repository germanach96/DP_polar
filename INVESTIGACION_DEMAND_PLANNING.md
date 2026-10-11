# Qué está demostrado en demand planning y qué aplicar aquí (investigación 2026-10-11)

Resumen de la evidencia publicada (competiciones M4/M5, estudios con datos reales de empresas, benchmarks recientes) cruzada con lo que ya medimos en este proyecto (`HISTORIAL.md`).

## 1. Lo que está demostrado (y cómo encaja con nuestros resultados)

| # | Hallazgo | Evidencia externa | Lo que ya vimos aquí |
|---|---|---|---|
| 1 | **Combinar varios métodos (media simple) gana a elegir el "mejor" por código.** | En las 5 competiciones M. M4: 12 de los 17 mejores eran combinaciones. M5: el ganador fue una media simple de 6 modelos; el 2.º y 3.º también usaban medias simples. La media simple suele ganar a pesos "óptimos" (el "puzzle de la combinación"). | El partido elegido por cada EAN solo es el mejor el 20% de las veces (al azar, 17%). La media de los 6 partidos es lo mejor a 1–3 meses (46%); la coalición de 2, la más estable. |
| 2 | **Elegir modelo por código solo funciona si el ranking es estable en el tiempo.** | Fildes y Petropoulos (2015): la selección individual ayuda solo en subgrupos claros (con temporada / con tendencia) y si el rendimiento relativo se mantiene. Las diferencias pequeñas entre modelos son azar. | Votar con oct–mar y aplicar en abr–jun falló: temporada alta ≠ temporada baja. |
| 3 | **Aprender de todos los códigos a la vez ("cross-learning", modelo global) gana a un modelo por código.** | M5: los 50 primeros usaron un modelo para todas las series. Montero-Manso y Hyndman: incluso un modelo lineal global (una regresión común) compite con modelos locales con 100 veces menos parámetros. Clave cuando las series son cortas (nuestro caso: ~39 meses). | Las reglas que mejor funcionan ya toman el trend de un grupo (casa × tamaño, función), no del propio EAN. |
| 4 | **Previsión a un nivel alto + reparto (o reconciliación) mejora el detalle.** | M5: los puestos 2.º y 5.º ajustaron el forecast del código con multiplicadores del nivel superior. Jerarquías temporales (Athanasopoulos y otros, 2017): prever también por quarter y repartir sube la precisión. | Error casa × quarter 11–20% frente a 50–65% EAN-mes: el nivel alto es mucho más predecible. |
| 5 | **Las variables externas (promos, precio, eventos) son las que más suman sobre la historia.** | M5: todos los ganadores usaron variables externas; el precio fue de lo más importante. Suavizado exponencial con promos y eventos: 6% mejor; ARIMA con variables: 13% mejor. | Los DAs son nuestra variable de promos, pero sin el real de la promo (solo lo planificado). |
| 6 | **Los ajustes manuales al alza empeoran; a la baja suelen mejorar.** | Fildes, Goodwin y De Baets: ~147.000 forecasts de 6 estudios; los ajustes mejoran apenas en algo más de la mitad de los SKUs y los positivos empeoran con más frecuencia. | Solo el 42% del DA planificado de fragancias se convierte en envío (23% sin bandera, 17% a 7–9 meses). Coincide con la literatura. |
| 7 | **Medir el valor añadido de cada paso (FVA) contra un método ingenuo.** | En estudios con empresas, alrededor de la mitad de los forecasts eran peores que el ingenuo. Gartner (2025): casi todas miden el error, pocas actúan sobre la causa. | El trend YoY 6M del equipo es peor que el año pasado sin más: FVA negativo. |
| 8 | **La demanda real no es lo que se envió cuando hay roturas.** | Literatura de "demanda censurada": con roturas la venta subestima la demanda y los sustitutos la inflan. Hay que marcar o reconstruir esos meses. | Los cortes están inflados por los re-pedidos; por eso solo suman al 10–25%. |
| 9 | **El sell-out (EPOS) mejora el corto plazo; para el largo plazo pesan más los pedidos/envíos.** | Williams y Waller (CPG): el forecast de pedidos con POS suele tener menos error que el basado en pedidos, sobre todo a corto plazo (inventario, transporte). Para producción a largo plazo, recomiendan los pedidos. El inventario del cliente explica la diferencia. | Tenemos EPOS desde jul-24 sin usar. El makeup tiene temporada en EPOS pero no en envíos: señal de que el stock del cliente amortigua. |
| 10 | **Lanzamientos: curvas de productos análogos.** | Fragancia y cosmética: los clusters de análogos funcionan para producto de venta continua; para productos de evento (navidad, ediciones limitadas) dependen del juicio experto. | Ciclo de vida en EANs de 6–11 meses: 105% de error frente a 276% de las reglas. |
| 11 | **Cola de poca venta (demanda intermitente): otro método.** | Clasificación de Syntetos-Boylan (intervalo medio entre ventas > 1,32 o variabilidad² > 0,49). M5: Croston es 13–27% mejor que el naive estacional en el nivel más bajo, pero peor arriba. | Los EANs C votaban distinto y cada uno pesaba igual que un A. |
| 12 | **Los modelos fundacionales (IA preentrenada) ya compiten, pero no ganan siempre.** | Chronos-2 (Amazon) y TimesFM-2.5 (Google) son los mejores en benchmarks independientes (TIME, 2026). En un caso de producción, un XGBoost ajustado les ganó. Sirven como rival barato a probar, no como solución por defecto. | Sin probar. |

**Expectativa realista:** el ganador de M5 mejoró un 22% frente al mejor método estadístico simple. Los mejores métodos mejoraron de media un 40% en el total y solo un 3% en el detalle (producto-tienda). **No hay santo grial a nivel EAN-mes.** La ganancia está en el nivel donde se decide (casa, tamaño, quarter, plazo de aprovisionamiento) y en no meter error con ajustes.

## 2. Qué cambiar en lo que estamos haciendo

1. **Dejar de elegir un ganador por EAN y combinar.** Usar la media simple de 3–4 métodos distintos (p. ej. año pasado con trend de grupo + media 6M estacional + ciclo de vida/grupo). Es lo más demostrado de toda la literatura y lo que mejor nos ha funcionado. El "parlamento" puede seguir como explicación (qué método pesa en cada EAN), no como mecanismo de elección.
2. **Validar en cada mes, no solo en las fotos.** Sin el consenso como referencia, no hace falta la foto para el backtest: ya existe historia desde jul-23. Origen móvil mensual (como `horizon9.py`, 13+ orígenes), 9 meses por delante y error por mes de horizonte. Así cada método se juzga con un año entero de temporadas, no con un trimestre.
3. **Medir como lo usa supply.**
   - Error ponderado por volumen (WAPE) por EAN en el mes de horizonte que corresponde al plazo de aprovisionamiento (no la media de todos).
   - Desvío (bias) aparte.
   - Siempre contra el naive estacional (año pasado) como referencia de FVA.
4. **Prever arriba y repartir abajo.**
   - Fragancias: casa × tamaño × mes (con temporada). Makeup: casa × función.
   - Reparto al EAN por su peso de los últimos 3–6 meses.
   - Comparar con el forecast directo por EAN y con la media de ambos.
5. **Que los datos fijen los coeficientes, no nosotros.** Hoy el 25% de cortes, el −50% de DAs, el 50% del trend y el tope de ±30% están puestos a mano y probados de uno en uno. Una regresión común a todos los EANs (modelo lineal global) estima todos a la vez y sigue siendo explicable: "el forecast = 0,8 × año pasado + 0,2 × media 6M, el DA se convierte un 40%…".
6. **DAs como ajuste a medir, no como dato.** Guardar los DAs de cada foto (o9 los borra) y medir su valor añadido por casa y por bandera. Aplicar un factor de conversión medido (hoy 42% fragancias / 80% makeup) en lugar de 100/50/0%.
7. **Segmentar por tipo de EAN antes de pronosticar**, no por votación:
   - Lanzamientos (<12 meses): curva de análogos de su línea o casa.
   - Cola intermitente: nivel de grupo × cuota, o Croston/SBA.
   - Maduros: la combinación.
   - Phase-out: forecast a la baja con fecha de salida.
8. **Rivales modernos como prueba, no como fe:**
   - LightGBM global con las mismas variables (lo que ganó M5).
   - Chronos-2 sin entrenar (acepta variables externas).
   - Solo se adoptan si ganan en el backtest móvil por un margen claro y estable.

## 3. Información que necesitaríamos (por prioridad)

| Prioridad | Dato | Para qué | ¿Lo tenemos? |
|---|---|---|---|
| 1 | **Histórico de DAs de cada foto** (guardar cada mes) | Medir si las promos se cumplen y estimar su conversión | Parcial: o9 borra los viejos |
| 1 | **Mapa predecesor → sucesor de EANs** (cambio de packaging, reformulación, coffrets) | Que un EAN "nuevo" herede la historia del viejo; si no, se trata como lanzamiento | Por confirmar |
| 1 | **Calendario de lanzamientos y de bajas** (fecha de discontinuación) | Curvas de análogos y cortar el forecast de lo que se va | Por confirmar |
| 2 | **Stock en cliente / sell-out EPOS por EAN y cliente** | Separar demanda real de llenado de canal; señal a 1–3 meses | EPOS desde jul-24; el stock en cliente, por confirmar |
| 2 | **Roturas reales** (fill rate, días sin stock), no solo cortes | Reconstruir la demanda censurada sin el inflado de los re-pedidos | Solo cortes |
| 2 | **Calendario comercial**: navidad, Día de la Madre/Padre, Black Friday, travel retail, sets de regalo | Variables de evento: lo que más sumó en M5 | No |
| 3 | **Precio / cambios de precio, distribución (nº de puertas)** | Variables explicativas de la tendencia | No |
| 3 | **Inversión en medios / lanzamientos de campaña** | Picos de lanzamiento y campañas | No |
| 3 | **Atributos del producto** (familia olfativa, tono, edición limitada sí/no) | Encontrar análogos para lanzamientos | Parcial (tamaño, función) |

Con datos desde FY24 (jul-23), hay ~39 meses: suficiente para un modelo global (≈900 EANs × ~27 meses con año anterior disponible ≈ 24.000 filas), justo para estacionalidad por grupo e insuficiente para estacionalidad fiable por EAN. Por eso conviene la temporada a nivel de grupo.

## 4. Fuentes
- Makridakis, Spiliotis y Assimakopoulos (2022), *The M5 Accuracy competition: Results, findings and conclusions*, IJF 38(4) — https://statmodeling.stat.columbia.edu/wp-content/uploads/2021/10/M5_accuracy_competition.pdf
- M4: resultados y comentario — https://blogs.sas.com/content/forecasting/2020/01/08/m4-forecasting-competition-results-and-commentary
- Puzzle de la combinación — https://arxiv.org/pdf/1505.00475
- Fildes y Petropoulos, *Simple versus complex selection rules for forecasting many time series* — https://eprints.lancs.ac.uk/67274
- Petropoulos y otros (2014), *'Horses for courses' in demand forecasting* — https://eprints.lancs.ac.uk/id/eprint/68604
- Montero-Manso y Hyndman, *Locality and globality* — https://arxiv.org/abs/2008.00444v1
- Athanasopoulos y otros (2017), *Forecasting with temporal hierarchies* — https://mpra.ub.uni-muenchen.de/66362/1/MPRA_paper_66362.pdf
- Fildes, Goodwin y De Baets, *Forecast value added in demand planning* — https://researchportal.bath.ac.uk/en/publications/forecast-value-added-in-demand-planning/
- Ajustes manuales y promociones — https://ideas.repec.org/a/eee/intfor/v29y2013i2p234-243.html
- FVA (Demand Planning) — https://demand-planning.com/?p=6193 · crítica de Lokad — https://lokad.com/forecast-value-added
- Williams y Waller, POS vs pedidos — https://news.uark.edu/articles/15691/suppliers-dilemma-top-down-versus-bottom-up · https://news.uark.edu/articles/13295/new-logistics-model-improves-forecast-accuracy-of-retail-and-packaged-goods-orders
- Demanda censurada — https://arxiv.org/html/2505.16319v1
- Análogos en cosmética — https://digital.car.chula.ac.th/chulaetd/17728 · https://journals.agh.edu.pl/dmms/article/view/543
- Intermitente (Syntetos-Boylan) — https://orca.cardiff.ac.uk/45026
- Chronos-2 — https://arxiv.org/html/2510.15821v1 · benchmark TIME — https://arxiv.org/html/2602.12147v3 · comparación en demanda — https://www.griddynamics.com/blog/ai-models-demand-forecasting-tsfm-comparison
- Gartner (2025), error medido pero sin acción sobre la causa — https://www.gartner.com/en/documents/6892666
