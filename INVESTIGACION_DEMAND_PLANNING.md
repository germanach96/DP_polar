# Qué está demostrado en demand planning y qué hacer con tus datos (2026-10-11)

Investigación de la literatura (competiciones M, revistas de forecasting, estudios con empresas reales) cruzada con tus datos. El diagnóstico de EPOS es nuevo: `python3 src/epos_diag.py` → `work/results/epos_diag.md`.

## Resumen en 6 líneas
1. **No existe el santo grial.** En 50 años de competiciones, los métodos buenos ganan a los simples por poco, y lo que más se repite es que **combinar varios forecasts gana a elegir uno**.
2. **Elegir el "mejor modelo" por EAN según su pasado es frágil.** Sirve para descartar los peores, no para encontrar el mejor. Por eso el parlamento con un solo ganador por EAN rinde bien lejos y mal cerca.
3. **Lo que sí mueve la aguja es información nueva, no fórmulas nuevas:** demanda del consumidor (EPOS), stock en el canal, promos y lanzamientos con fecha.
4. **Tus datos lo confirman:** el EPOS repite su forma mes a mes casi idéntica de un año a otro (correlación 1,00 en fragancias). Los envíos no (0,74 en fragancias y −0,14 en makeup). El ruido no está en el consumidor: lo meten los pedidos de los clientes.
5. **El envío va 3 meses por delante de la venta** (se envía en septiembre lo que se vende en diciembre). Y cuando una casa envía más de lo que vende, después le toca corregir. Gucci Make up envió +10% en FY26 con un EPOS de −6%; en jul–ago-26 sus envíos caen un 50%.
6. **Propuesta:** cambiar la pregunta. En vez de "¿cuánto enviaré?", primero "¿cuánto venderá el consumidor?" (EPOS), y luego traducirlo a envío con el desfase y el stock del canal. Es lo que la literatura llama *sell-in a partir del sell-out*, y o9 lo soporta.

---

## 1. Lo que está demostrado (y qué significa para ti)

### 1.1 Combinar gana a elegir
- La revisión de referencia del sector (*Forecasting: theory and practice*, 2022, §2.6.1) concluye que **la evidencia de que combinar forecasts mejora la precisión es "casi unánime"**: competiciones M1 a M5 y estudios empíricos. La media simple es difícil de batir: es el llamado "puzzle de la combinación".
- En la M5 (Walmart, 42.840 series jerárquicas de ventas), **el ganador fue una media simple de 6 modelos**, y los dos siguientes también usaron medias a partes iguales. Combinar *top-down* y *bottom-up* ganó a cada uno por separado.
- **En tus datos ya se ve:** la media de los 6 partidos tiene un 46% de error a 1–3 meses, contra el 64% del voto de un solo partido. La coalición de los 2 mejores es la opción más estable (55/55/53%).
- **Qué hacer:** el parlamento debería **formar gobierno de coalición, no elegir presidente**. Que cada EAN vete a sus peores partidos y promedie el resto.

### 1.2 Elegir modelo por EAN: sirve para evitar el peor, no para acertar el mejor
- Petropoulos y coautores (2018, *Journal of Operations Management*, ~700 participantes) compararon la elección automática por EAN con la del planner. La automática acierta más veces el mejor modelo. La humana evita más veces el peor y, en el total, empata o gana. **La combinación de ambas elecciones ganó a las dos.**
- La M5 (hallazgo 6) insiste en validar con varias ventanas. Muchos equipos no supieron elegir cuál de sus propios forecasts era mejor.
- **Es lo que te pasó con el voto por EAN.** Con 2–3 urnas por EAN, el ganador cambia por ruido. Por eso gana lejos (53% vs 64%) y pierde cerca (64% vs 51%).

### 1.3 Aprender del grupo (*cross-learning*) y conciliar niveles
- En la M5, **los 50 mejores métodos aprendían de todas las series a la vez** (de los similares), no EAN a EAN. Ajustar el forecast de EAN para que cuadre con el de niveles superiores (casa, categoría) también mejoró (hallazgo 5): las tendencias se ven mejor arriba.
- **Tu regla ya lo hace bien** (trend de casa × tamaño o de función aplicado al EAN). El siguiente paso documentado es la **conciliación**: forecast a nivel casa/brand y a nivel EAN, y luego forzar que sumen lo mismo.

### 1.4 Variables externas: promociones, precios y eventos
- En la M5 (hallazgo 7), **todos los métodos ganadores usaron información externa** (precio, eventos, promos). Sin ella, un método solo extrapola el pasado y las promos pasadas ensucian la base.
- Para ti, la información externa son **los DAs, los lanzamientos y el calendario comercial**. Su valor depende de lo fiables que sean (siguiente punto).

### 1.5 Los ajustes manuales: los positivos suelen empeorar
- Fildes, Goodwin y De Baets (2025, *International Journal of Forecasting*) reunieron ~147.000 forecasts de 6 estudios. Los ajustes manuales mejoran solo algo más de la mitad de los SKUs. **Los ajustes al alza tienden a empeorar** y los ajustes grandes a la baja tienden a mejorar. Corregir sistemáticamente el sesgo de los ajustes funcionó.
- En 2009 (60.000 forecasts, 4 empresas), los ajustes positivos de un retailer duplicaron el error: del 32% al 65%.
- **Encaja con lo que mediste:** solo el 42% del DA planificado de fragancias se convirtió en envío extra. La evidencia respalda tu decisión de no sumar el 100% de los DAs, y además da una vía documentada para ajustarlos: medir el sesgo de cada tipo de DA y aplicar un factor (≈40% en fragancias, ≈80% en makeup) en lugar de una bandera.

### 1.6 Datos del punto de venta (EPOS): ayudan, pero no por sí solos
La evidencia es mixta, y conviene saberlo antes de ponerle expectativas:

| Estudio | Qué encontró |
|---|---|
| Williams y Waller (Univ. Arkansas, varios artículos 2010–2014) | El forecast con EPOS gana al de pedidos en la mayoría de los casos. El de pedidos gana a nivel de cuenta y en horizontes largos (producción, capacidad). **Lo mejor es combinar EPOS + pedidos + "balance de inventario"** (si el cliente ha cargado stock, pedirá menos). |
| Van Belle, Guns y Verbeke (2021, *EJOR*) | Añadir el sell-through al histórico de pedidos **mejora el forecast en todos los horizontes probados**, sobre todo a 1 periodo vista. |
| Estudio con 684 series de 3 eslabones (arXiv 2022) | El forecast con pedidos ganó al de EPOS (6–15%), sobre todo con **promociones** y en series pequeñas y estables. |
| *IJOPM* 2025, "Revisiting the value of data sharing in retail" | Integrar datos del retailer **no suele mejorar mucho la precisión**. Su valor real está en alinear la planificación con el cliente. Proponen compartir los **forecasts de reposición del retailer**. |
| Revisión *FTP* §3.2.3 (efecto látigo) | Compartir la demanda de abajo reduce el efecto látigo (los pedidos amplifican la variación de la venta real). Tiene más valor cuando la empresa no conoce cómo pide su cliente. |
| Estée Lauder, 10-K FY2025 | Explica caídas de MAC (makeup) y Tom Ford (fragancia) por **ventas flojas en tienda → stock alto en el retailer → recorte de pedidos** (*destocking*). Es el mecanismo que se ve en tus datos. |

**Conclusión:** el EPOS no reemplaza a los envíos como serie a extrapolar. Aporta tres cosas que los envíos no tienen: **la forma de la temporada**, **la tendencia real del consumidor** y, comparado con los envíos, **cuánto stock está acumulando o soltando el canal**.

### 1.7 Lanzamientos: analogías, varias y con modestia
- Los forecasts de productos nuevos tienen errores altos en todos los estudios. Lo que más ayuda es **promediar varios análogos (5–6 bastan)** en vez de copiar el más parecido, y usar parámetros calculados con datos propios.
- Tu partido "Ciclo de vida" (curva de los EANs que tuvieron tu edad) ya va en esa línea: es la práctica recomendada.

### 1.8 Medir el valor añadido (FVA) contra un método ingenuo
- Según los estudios de Morlidge que difunde SAS, **entre el 40% y el 50% de los forecasts a nivel SKU son peores que un método ingenuo**, y la mayoría de empresas no lo supera en más de un 10–15%.
- **Qué hacer:** fijar como suelo un método ingenuo (año pasado) y medir cuánto añade cada capa: regla → +DAs → +EPOS → ajuste del planner. Lo que no añade, se quita.

---

## 2. Lo que dicen TUS datos sobre el EPOS (diagnóstico nuevo, foto sep-26)

EPOS disponible de jul-24 a jul-26; envíos de jul-23 a ago-26.

**a) Cobertura.** Prácticamente todos los EANs tienen EPOS (98–100% del envío). El EPOS suma el 79–87% del envío: no todos los clientes reportan, o parte se queda en stock.

**b) El EPOS es estable; los envíos no.** Peso de cada mes en el año (1 = mes medio), comparando FY25 con FY26:

| | Cambio medio del peso de un mes | Correlación de la forma FY25 vs FY26 |
|---|---|---|
| Fragancias – envío | 0,25 | 0,74 |
| Fragancias – EPOS | **0,04** | **1,00** |
| Makeup – envío | 0,38 | −0,14 |
| Makeup – EPOS | **0,13** | **0,82** |

- En fragancias, diciembre pesa 3,16 en FY25 y 3,11 en FY26 en EPOS. En envíos, julio pasa de 1,56 a 1,16 y diciembre de 0,95 a 1,42.
- **Esto explica por qué "makeup no tiene estacionalidad en envíos".** El consumidor de makeup sí la tiene (diciembre ×1,6 y marzo ×1,1–1,2, repetidos dos años); los pedidos la desordenan.

**c) El envío va 3 meses por delante de la venta.** La forma de los envíos adelantada 3 meses es la que más se parece a la del EPOS: correlación 0,73 en las dos categorías. Con 0, 1 o 2 meses de adelanto se queda en 0,47 como máximo. Se carga el canal en julio–septiembre para vender en diciembre.

**d) La carga del canal anticipa el siguiente movimiento** (envío/EPOS en los EANs con EPOS):

| Casa | Envío FY26 | EPOS FY26 | Envío/EPOS FY25 → FY26 | Envío jul–ago-26 vs año pasado |
|---|---|---|---|---|
| Gucci Make up | +10% | −6% | 1,20 → **1,40** (carga) | **−50%** |
| Kylie Makeup | +7% | +17% | 1,31 → **1,19** (descarga) | **+18%** |
| Marc Jacobs | −7% | +4% | 1,30 → **1,16** (descarga) | **+28%** |
| Burberry | −9% | −13% | 1,18 → 1,23 (carga leve) | −6% |
| Gucci | −11% | −14% | 1,21 → 1,25 (carga leve) | +1% |

- 4 de las 5 casas se mueven en el sentido esperado; Gucci fragancias no está claro.
- **Aviso:** son 5 casas y 2 meses, y una caída del 50% puede tener otras causas (lanzamientos del año pasado, cambios de cliente). Es una señal fuerte, no una prueba. Hay que confirmarla EAN a EAN con más meses.

**e) ¿El EPOS anticipa los envíos de los 6 meses siguientes?** Prueba: EANs con 18+ meses, cortes de ene/feb/mar-26. Forecast = mismo periodo del año pasado × (1 + trend 6M del propio EAN).

| | Año pasado plano | Trend de envíos | Trend de EPOS | Media de los dos |
|---|---|---|---|---|
| Fragancias, error EAN, tope ±30% | 35,2% | 33,0% | **31,1%** | **31,1%** |
| Makeup, error EAN, tope ±30% | 62,5% | 56,0% | 56,7% | 56,6% |
| Makeup, error EAN, tope ±150% | — | 46,8% | **43,9%** | — |

- **Fragancias:** el trend del EPOS gana al de envíos (31% vs 33%) y la media de los dos deja el desvío total en 0%.
- **Makeup:**
  - El crecimiento del EPOS explica el crecimiento futuro de los envíos mucho mejor que el pasado de los envíos (coeficiente 0,66 frente a 0,21; R² 0,55, ponderado por volumen).
  - Cuando los envíos crecieron más que el EPOS, los envíos futuros bajan (coeficiente −0,66 ± 0,11).
  - **El tope de ±30% tapa esa señal:** sin tope, el error baja del 56% al 44%.
- **Límites:** solo 3 cortes seguidos de medio año, y la base de año pasado no es la de tu regla de makeup (media 6M). Es una pista sólida para el backtest, no una regla.

---

## 3. Recomendación: forecast del consumidor primero, envío después

### 3.1 La lógica (explicable a supply y a dirección)
> **Envío del mes t = Venta al consumidor prevista para t+3 × factor envío/EPOS del EAN − corrección por stock acumulado en el canal**

1. **Prever el EPOS** del EAN (es la serie estable):
   - Base: EPOS del mismo mes del año pasado, o nivel de 12M × la forma mensual del EPOS (estable de un año a otro).
   - Tendencia: trend 12M del EPOS de casa × tamaño (fragancias) o de función (makeup); en makeup, más fuerza y menos tope.
   - Sin DAs ni cortes que limpiar: el EPOS no los lleva.
2. **Pasarlo a envío.** Multiplicar por la relación envío/EPOS de los últimos 12 meses del EAN (recoge los clientes que no reportan) y adelantar 3 meses (desfase medido; se puede afinar por casa).
3. **Corregir el canal.** Si la relación envío/EPOS de los últimos 12 meses está por encima de la del año anterior, el canal está cargado: restar parte de ese exceso en los 6 meses siguientes. Si está por debajo, sumarlo.
4. **Añadir los DAs futuros** con un factor de conversión medido (≈40% fragancias, ≈80% makeup) en lugar de la bandera.

### 3.2 Cómo encaja con el parlamento
- Añadir un partido **"Consumidor (EPOS)"** con la lógica de arriba. Es la única ideología nueva con información que los otros no tienen; los demás partidos son variantes del mismo histórico de envíos.
- Cambiar el mecanismo de elección: **coalición** (media de los partidos que no son los peores del EAN) en vez de un ganador. Es lo que respalda la evidencia y lo que ya mide mejor en tu prueba honesta.
- Mantener "Ciclo de vida" para los lanzamientos (analogías) y la regla de su categoría como suelo de referencia (FVA).

### 3.3 Backtest propuesto (antes de decidir nada)
- Cortes mensuales de oct-25 a mar-26 (el primero con 12M de EPOS y su año anterior), horizonte hasta ago-26.
- Comparar: regla actual · partido EPOS · media regla + EPOS · coalición con y sin EPOS.
- Medir error EAN-mes, WAPE90 por casa × quarter y desvío, por horizonte (1–3, 4–6, 7–9).
- Limitación honesta: con EPOS desde jul-24 solo hay ~1 año de cortes válidos. Cada mes que pase la prueba gana peso. **Guardar cada foto** es imprescindible.

---

## 4. Información que necesitarías (por prioridad)

| # | Dato | Para qué | Respaldo |
|---|---|---|---|
| 1 | **Stock del cliente (tienda + almacén) por EAN y mes**, al menos de los 5–10 principales clientes | Medir la carga del canal directamente en vez de deducirla de envío − EPOS. Es la pieza que convierte el EPOS en forecast de envío. | Williams y Waller (balance de inventario); demand sensing de P&G (EPOS + stock del retailer) |
| 2 | **EPOS por cliente** y **número de puertas activas** por EAN | Separar "vende más por tienda" de "está en más tiendas"; saber qué parte del envío tiene EPOS | Cobertura actual del 79–87% |
| 3 | **Forecast de reposición de los clientes** (si lo comparten) | Señal directa de pedidos a corto plazo | *IJOPM* 2025 |
| 4 | **Calendario de promos, lanzamientos, listados y bajas con fechas**, separado de los DAs | Variables externas limpias; no restar promos a ciegas | M5, hallazgo 7 |
| 5 | **Archivo de cada foto** (forecast, DAs, consenso) mes a mes | Medir el valor añadido (FVA) de cada capa y el sesgo de los DAs; o9 borra los DAs viejos | Fildes et al. 2025; Gilliland/Morlidge |
| 6 | **Roturas reales** (fuera de stock en tienda y pedido no servido sin re-pedidos duplicados) | Corregir la demanda censurada: un mes con rotura no es demanda baja | Literatura de demanda censurada |
| 7 | **Sustituciones de código** (EAN viejo → nuevo, cambios de packaging) | Enlazar historias y no tratar como lanzamiento lo que es un cambio de código | Práctica estándar |

Con los datos desde FY24 ya tienes lo esencial para envíos. El cuello de botella es el EPOS (desde FY25) y **la falta de stock del canal**, que es el dato con más palanca.

---

## 5. Qué dejar de buscar
- **Un modelo más sofisticado sobre los mismos envíos** (ETS, ARIMA, ML por EAN): ya viste que ETS no aporta. La M5 la ganó el *machine learning* con miles de series diarias y variables externas, no con 24–36 meses por EAN.
- **Un ganador único por EAN** elegido con 2–3 urnas: no es estable.
- **Topes y trends de envíos cada vez más finos:** el ruido está en los pedidos, y la señal limpia está en el EPOS.

---

## Fuentes
- Petropoulos et al. (2022). *Forecasting: theory and practice*. IJF. §2.6.1 combinaciones, §2.11.3 elección de modelo, §3.2.3 efecto látigo. https://arxiv.org/abs/2012.03854
- Makridakis, Spiliotis y Assimakopoulos (2022). *M5 accuracy competition: Results, findings and conclusions*. IJF. https://statmodeling.stat.columbia.edu/wp-content/uploads/2021/10/M5_accuracy_competition.pdf
- Petropoulos, Kourentzes, Nikolopoulos y Siemsen (2018). *Judgmental selection of forecasting models*. JOM. https://www.lancaster.ac.uk/lums/news/archive/can-we-rely-on-judgment-to-select-the-best-forecasting-model
- Fildes, Goodwin y De Baets (2025). *Forecast value added in demand planning*. IJF. https://researchportal.bath.ac.uk/en/publications/forecast-value-added-in-demand-planning/
- Fildes, Goodwin, Lawrence y Nikolopoulos (2009). *Effective forecasting and judgmental adjustments*. IJF. https://researchportal.bath.ac.uk/en/publications/effective-forecasting-and-judgmental-adjustments-an-empirical-eva/
- Williams, Waller, Ahire y Ferrier (2014). *Predicting retailer orders with POS and order data: The inventory balance effect*. EJOR. https://www.semanticscholar.org/paper/Predicting-retailer-orders-with-POS-and-order-data:-Williams-Waller/4b977a949e3851beba69d3aa98a89ba38d3b258c
- Univ. Arkansas, *Suppliers' dilemma: top-down versus bottom-up*. https://news.uark.edu/articles/15691/suppliers-dilemma-top-down-versus-bottom-up
- Van Belle, Guns y Verbeke (2021). *Using shared sell-through data to forecast wholesaler demand in multi-echelon supply chains*. EJOR. https://ideas.repec.org/a/eee/ejores/v288y2021i2p466-479.html
- *The value of point of sales information in upstream supply chain forecasting* (2022). https://arxiv.org/abs/2201.10555
- *Revisiting the value of data sharing in retail supply chain demand planning*. IJOPM 45(11). https://doi.org/10.1108/IJOPM-07-2024-0560
- Estée Lauder, 10-K FY2025 (destocking por stock alto en retailers). https://www.sec.gov/Archives/edgar/data/1001250/000100125025000099/el-20250630.htm
- P&G y demand sensing. https://consumergoods.com/procter-gamble-uses-demand-sensing-solution
- Goodwin et al., *The use of analogies in forecasting the annual sales of new electronics products*. https://researchportal.bath.ac.uk/en/publications/the-use-of-analogies-in-forecasting-the-annual-sales-of-new-elect/
- Gilliland (SAS), FVA y método ingenuo. https://www.sas.com/en_in/insights/articles/analytics/practical-advice-for-better-business-forecasting.html · https://blogs.sas.com/content/forecasting/2015/04/27/fva-interview-with-steve-morlidge
- Athanasopoulos et al. (2017). *Forecasting with temporal hierarchies*. EJOR. https://pkg.robjhyndman.com/thief/reference/thief.html
