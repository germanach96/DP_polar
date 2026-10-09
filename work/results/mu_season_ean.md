# Estacionalidad EAN a EAN (src/mu_season_ean.py)

EANs con FY24, FY25 y FY26 completos y >= 50 u/mes de media en cada año. Envíos = última foto.
Significativa = el mes del calendario explica más variación de la que saldría barajando los meses al azar (p<0,05, 300 permutaciones).
Predice mejor = el reparto mensual de FY25 acierta el reparto de FY26 mejor que repartir plano (1/12 por mes).

|                         |   EANs analizados |   corr. media entre años (pond. volumen) |   % EANs corr > 0,5 |   % EANs estacionalidad significativa (p<0,05) |   % volumen con estacionalidad significativa |   % EANs donde el reparto del año pasado predice mejor que plano |   % volumen donde predice mejor que plano |   índice diciembre medio (1 = mes medio) |
|:------------------------|------------------:|-----------------------------------------:|--------------------:|-----------------------------------------------:|---------------------------------------------:|-----------------------------------------------------------------:|------------------------------------------:|-----------------------------------------:|
| Gucci Make up           |               113 |                                    0.083 |               0.053 |                                          0.159 |                                        0.095 |                                                            0.142 |                                     0.114 |                                    0.851 |
| Kylie Makeup            |               139 |                                    0.098 |               0.036 |                                          0.151 |                                        0.118 |                                                            0.129 |                                     0.093 |                                    0.706 |
| Fragancias (referencia) |               170 |                                    0.362 |               0.153 |                                          0.324 |                                        0.533 |                                                            0.376 |                                     0.527 |                                    0.914 |

## Makeup por función

|                                        |   n |   corr |   sig |   predice |   dic |
|:---------------------------------------|----:|-------:|------:|----------:|------:|
| ('GUMU', 'Gucci Eyes (01199)')         |   5 |   0.05 |  0    |      0    |  0.83 |
| ('GUMU', 'Gucci Face (01201)')         |  43 |   0.02 |  0.07 |      0.12 |  0.79 |
| ('GUMU', 'Gucci Lips (01200)')         |  65 |   0.15 |  0.23 |      0.17 |  0.92 |
| ('KYMU', 'Collection (01319)')         |   5 |  -0.05 |  0    |      0.2  |  0.38 |
| ('KYMU', 'Eyes (01244)')               |  11 |   0.05 |  0.09 |      0    |  0.89 |
| ('KYMU', 'Face (01243)')               |  44 |   0.12 |  0.16 |      0.07 |  0.63 |
| ('KYMU', 'Kylie Makeup Other (01223)') |   4 |  -0.09 |  0    |      0    |  0.89 |
| ('KYMU', 'Lips (01245)')               |  75 |   0.11 |  0.17 |      0.19 |  0.73 |

## EANs de makeup con estacionalidad significativa (top 15 por volumen)

| fam   | desc                                     |   vol |   corr |   pval | pico   |   pico_idx |   dic | seasonal_gana   |
|:------|:-----------------------------------------|------:|-------:|-------:|:-------|-----------:|------:|:----------------|
| KYMU  | KJ MU TNT BB LCAREM 2.4G SHES LVLY619 IV | 65977 |   0.35 |   0.01 | Jul    |       2.82 |  0.68 | False           |
| KYMU  | KJ MU V LIQ K MLTLPK 3G 1G PSK 100 VP IV | 62999 |   0.26 |   0.04 | May    |       3.35 |  0.7  | False           |
| KYMU  | KJ MU SKN TINT LIQFND 30 ML 3.5WARM IV   | 61933 |   0.32 |   0.02 | Jun    |       5.44 |  0.49 | False           |
| KYMU  | KJ MU PWD BL PWDBLU 10G 336WR KSD VP  IV | 60600 |   0.44 |   0.01 | Aug    |       2.82 |  0.64 | False           |
| KYMU  | KJ MU V LIQ K MLTLPK 3ML 1.1G BARE IV    | 54965 |   0.35 |   0.03 | May    |       2.93 |  0.65 | False           |
| KYMU  | KJ MU TNT BB LCAREM 2.4G THTS TEA 211 IV | 40058 |   0.55 |   0.01 | Jul    |       3.05 |  0.7  | True            |
| KYMU  | KJ MU SPP GLZ LG 3 ML 005LOVABLE IV      | 34233 |   0.45 |   0.03 | Jun    |       6.07 |  0.31 | False           |
| KYMU  | KJ MU V LIQ K MLTLPK 3ML 1.1G RD VL IV   | 32923 |   0.44 |   0.02 | Nov    |       1.52 |  1.39 | False           |
| KYMU  | KJ MU LIPS ML LIQLPK 315 LOST ANGEL 21IV | 31535 |   0.48 |   0.01 | Sep    |       4.01 |  0.65 | True            |
| KYMU  | KJ MU SKN TINT LIQFND 30 ML 6NEUTRAL IV  | 27992 |   0.43 |   0.03 | Jun    |       5.9  |  0.2  | False           |
| KYMU  | KJ MU HIGH GLS LIQLPK 3 G 802CANDY VP IV | 26421 |   0.43 |   0.01 | Sep    |       3.83 |  0.75 | True            |
| KYMU  | KJ MU SKN TINT LIQFND30ML 6.5WNEUTRAL IV | 25239 |   0.53 |   0.01 | Jun    |       5.98 |  0.28 | False           |
| KYMU  | KJ MU SKN TINT LIQFND 30 ML 5WARM IV     | 24949 |   0.33 |   0.02 | Jun    |       5.58 |  0.46 | False           |
| KYMU  | KJ MU LSE PWD FACE ML 5G 400 BEIGE VP IV | 22707 |   0.28 |   0.03 | Sep    |       1.73 |  1.05 | True            |
| KYMU  | KJ MU SKN TINT LIQFND 30 ML 1WNEUTRAL IV | 21622 |   0.41 |   0.02 | Jun    |       5.12 |  0.53 | True            |

## Picos más frecuentes (makeup, todos los EANs analizados)

| pico   |   EANs |
|:-------|-------:|
| Aug    |     57 |
| Sep    |     39 |
| Jul    |     34 |
| Feb    |     29 |
| Jun    |     24 |
| Jan    |     20 |
| May    |     17 |
| Oct    |     14 |
| Nov    |      9 |
| Mar    |      8 |
| Dec    |      1 |