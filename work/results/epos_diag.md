# Diagnóstico EPOS (sell-out) vs envíos (sell-in), foto sep-26

EPOS disponible jul-24 → jul-26 (ago-26 aún vacío). Envíos hasta ago-26.

## 1. Cobertura (ago-25 → jul-26)

| Casa          | Categoría   |   % envío con EPOS |   EPOS / envío (EANs con EPOS) |
|:--------------|:------------|-------------------:|-------------------------------:|
| BURBERRY      | Fragancias  |               100% |                            79% |
| Gucci         | Fragancias  |                99% |                            80% |
| Gucci Make up | Makeup      |               100% |                            78% |
| Kylie Makeup  | Makeup      |               100% |                            84% |
| Marc Jacobs   | Fragancias  |                98% |                            87% |


## 2. Perfil mensual (peso de cada mes; 1 = mes medio) y desfase envío → venta

### Fragancias

|       |   ene |   feb |   mar |   abr |   may |   jun |   jul |   ago |   sep |   oct |   nov |   dic |
|:------|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| Envío |  0.46 |  0.77 |  1.11 |  0.51 |  0.89 |  0.70 |  1.38 |  1.41 |  1.95 |  0.78 |  0.87 |  1.18 |
| EPOS  |  0.51 |  0.81 |  0.84 |  0.76 |  0.92 |  0.83 |  0.69 |  0.87 |  0.91 |  0.65 |  1.07 |  3.13 |

Correlación del perfil de envíos adelantado k meses con el de EPOS: k=0: 0.20, k=1: -0.17, k=2: -0.08, k=3: 0.72, k=4: 0.21 → mejor k=3

### Makeup

|       |   ene |   feb |   mar |   abr |   may |   jun |   jul |   ago |   sep |   oct |   nov |   dic |
|:------|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| Envío |  0.73 |  1.05 |  1.05 |  0.74 |  1.04 |  0.89 |  1.09 |  0.93 |  1.61 |  0.78 |  0.99 |  1.11 |
| EPOS  |  0.77 |  0.82 |  1.18 |  0.97 |  0.90 |  0.96 |  0.84 |  0.89 |  1.17 |  0.81 |  1.09 |  1.61 |

Correlación del perfil de envíos adelantado k meses con el de EPOS: k=0: 0.44, k=1: -0.14, k=2: -0.17, k=3: 0.72, k=4: -0.10 → mejor k=3

### Estabilidad del perfil de un año a otro

| Categoría   | Serie   |   Cambio medio del peso mensual |   Mayor cambio |   Correlación FY25-FY26 |
|:------------|:--------|--------------------------------:|---------------:|------------------------:|
| Fragancias  | Envío   |                            0.25 |           0.70 |                    0.74 |
| Fragancias  | EPOS    |                            0.04 |           0.12 |                    1.00 |
| Makeup      | Envío   |                            0.38 |           1.22 |                   -0.14 |
| Makeup      | EPOS    |                            0.13 |           0.23 |                    0.82 |


## 3. Envío frente a EPOS por casa (EANs con EPOS)

Si los envíos crecen más que el EPOS, el canal acumula stock (o cambia la cobertura del EPOS).

|               |   YoY envío FY26 |   YoY EPOS FY26 |   Envío/EPOS FY25 |   Envío/EPOS FY26 |   YoY envío jul–ago-26 |
|:--------------|-----------------:|----------------:|------------------:|------------------:|-----------------------:|
| BURBERRY      |            -0.09 |           -0.13 |              1.18 |              1.23 |                  -0.06 |
| Gucci         |            -0.11 |           -0.14 |              1.21 |              1.25 |                   0.01 |
| Gucci Make up |             0.10 |           -0.06 |              1.20 |              1.40 |                  -0.50 |
| Kylie Makeup  |             0.07 |            0.17 |              1.31 |              1.19 |                   0.18 |
| Marc Jacobs   |            -0.07 |            0.04 |              1.30 |              1.16 |                   0.28 |


## 4. ¿El EPOS anticipa los envíos? (EANs con 18+ meses, orígenes ene/feb/mar-26, 6 meses siguientes)

Forecast = envío del mismo período del año pasado × (1 + trend 6M, tope ±30%).

| Categoría   | Fuente del trend       |   EANs×origen |   Error EAN (6M) |   Desvío total |
|:------------|:-----------------------|--------------:|-----------------:|---------------:|
| Fragancias  | Año pasado plano       |           652 |            35.2% |          12.4% |
| Fragancias  | Trend envíos propio 6M |           652 |            33.0% |           3.2% |
| Fragancias  | Trend EPOS propio 6M   |           652 |            31.1% |          -2.7% |
| Fragancias  | Media envíos y EPOS    |           652 |            31.1% |           0.2% |
| Makeup      | Año pasado plano       |          1469 |            62.5% |          -9.1% |
| Makeup      | Trend envíos propio 6M |          1469 |            56.0% |         -13.2% |
| Makeup      | Trend EPOS propio 6M   |          1469 |            56.7% |         -10.6% |
| Makeup      | Media envíos y EPOS    |          1469 |            56.6% |         -11.4% |


Regresión ponderada por volumen: crecimiento futuro de envíos ~ trend envíos 6M + trend EPOS 6M

- Fragancias (n=652): intercepto -0.09; envíos +0.23 (±0.06); EPOS +0.00 (±0.10); R² 0.05
- Makeup (n=1469): intercepto -0.08; envíos +0.21 (±0.10); EPOS +0.66 (±0.11); R² 0.55

Error EAN (6M) según el tope del trend:

| Categoría   | Fuente   |   tope ±30% |   tope ±60% |   tope ±150% |
|:------------|:---------|------------:|------------:|-------------:|
| Fragancias  | Envíos   |       33.0% |       35.0% |        36.7% |
| Fragancias  | EPOS     |       31.1% |       32.2% |        33.2% |
| Makeup      | Envíos   |       56.0% |       53.0% |        46.8% |
| Makeup      | EPOS     |       56.7% |       52.2% |        43.9% |

Carga del canal (envíos crecieron más que el EPOS):

- Fragancias: envíos +0.23 (±0.09); carga -0.00 (±0.10)
- Makeup: envíos +0.87 (±0.03); carga -0.66 (±0.11)
