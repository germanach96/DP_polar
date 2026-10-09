# Horizonte de 9 meses (src/horizon9.py)

Error EAN-mes (WMAPE) por mes del horizonte. Reglas recalculadas cada mes con los últimos 12 meses cerrados. Cortes mensuales jul-25..jul-26; el mes 9 solo tiene verdad para 5 cortes.

## WMAPE por mes del horizonte

|                                                   |     1 |     2 |     3 |     4 |     5 |     6 |     7 |     8 |     9 |
|:--------------------------------------------------|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| ('Fragancias', 'Año pasado tal cual')             | 0.832 | 0.794 | 0.852 | 0.859 | 0.858 | 0.864 | 0.753 | 0.689 | 0.723 |
| ('Fragancias', 'Método actual (trend 6M EAN)')    | 0.834 | 0.834 | 0.895 | 0.893 | 0.866 | 0.936 | 0.819 | 0.808 | 0.807 |
| ('Fragancias', 'Regla')                           | 0.748 | 0.713 | 0.744 | 0.721 | 0.709 | 0.696 | 0.657 | 0.628 | 0.642 |
| ('Gucci Make up', 'Año pasado tal cual')          | 1.084 | 1.05  | 1.103 | 1.093 | 1.093 | 1.114 | 1.06  | 0.992 | 0.978 |
| ('Gucci Make up', 'Método actual (trend 6M EAN)') | 0.994 | 0.978 | 0.997 | 1.036 | 1.004 | 1.095 | 1.073 | 1.017 | 1.057 |
| ('Gucci Make up', 'Regla')                        | 0.638 | 0.66  | 0.671 | 0.703 | 0.72  | 0.724 | 0.736 | 0.716 | 0.707 |
| ('Kylie Makeup', 'Año pasado tal cual')           | 1.128 | 1.116 | 1.002 | 1.005 | 1.015 | 0.901 | 0.899 | 0.864 | 0.843 |
| ('Kylie Makeup', 'Método actual (trend 6M EAN)')  | 1.311 | 1.292 | 1.224 | 1.163 | 1.15  | 1.077 | 1.03  | 0.984 | 0.98  |
| ('Kylie Makeup', 'Regla')                         | 0.546 | 0.557 | 0.57  | 0.591 | 0.605 | 0.634 | 0.662 | 0.683 | 0.699 |

## Desvío (bias) por mes del horizonte

|                                                   |      1 |      2 |      3 |      4 |      5 |      6 |      7 |      8 |      9 |
|:--------------------------------------------------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| ('Fragancias', 'Año pasado tal cual')             |  0.242 |  0.181 |  0.209 |  0.238 |  0.266 |  0.32  |  0.211 |  0.14  |  0.252 |
| ('Fragancias', 'Método actual (trend 6M EAN)')    |  0.114 |  0.074 |  0.128 |  0.141 |  0.128 |  0.224 |  0.104 |  0.052 |  0.133 |
| ('Fragancias', 'Regla')                           |  0.088 |  0.021 | -0.006 | -0.058 | -0.059 | -0.033 | -0.033 | -0.081 |  0.004 |
| ('Gucci Make up', 'Año pasado tal cual')          |  0.382 |  0.346 |  0.44  |  0.417 |  0.414 |  0.43  |  0.365 |  0.28  |  0.262 |
| ('Gucci Make up', 'Método actual (trend 6M EAN)') |  0.229 |  0.2   |  0.282 |  0.264 |  0.251 |  0.348 |  0.313 |  0.225 |  0.242 |
| ('Gucci Make up', 'Regla')                        |  0.056 |  0.066 |  0.127 |  0.126 |  0.146 |  0.121 |  0.211 |  0.177 |  0.163 |
| ('Kylie Makeup', 'Año pasado tal cual')           |  0.046 |  0.057 | -0.074 | -0.057 | -0.009 | -0.11  | -0.117 | -0.192 | -0.15  |
| ('Kylie Makeup', 'Método actual (trend 6M EAN)')  |  0.305 |  0.294 |  0.181 |  0.12  |  0.104 |  0.022 | -0.063 | -0.207 | -0.171 |
| ('Kylie Makeup', 'Regla')                         | -0.193 | -0.209 | -0.225 | -0.251 | -0.242 | -0.262 | -0.285 | -0.295 | -0.276 |

## Total meses 1-9

|                                                   |   wmape |   bias |
|:--------------------------------------------------|--------:|-------:|
| ('Fragancias', 'Año pasado tal cual')             |   0.815 |  0.227 |
| ('Fragancias', 'Método actual (trend 6M EAN)')    |   0.857 |  0.12  |
| ('Fragancias', 'Regla')                           |   0.708 | -0.006 |
| ('Gucci Make up', 'Año pasado tal cual')          |   1.073 |  0.382 |
| ('Gucci Make up', 'Método actual (trend 6M EAN)') |   1.019 |  0.257 |
| ('Gucci Make up', 'Regla')                        |   0.688 |  0.118 |
| ('Kylie Makeup', 'Año pasado tal cual')           |   1.003 | -0.046 |
| ('Kylie Makeup', 'Método actual (trend 6M EAN)')  |   1.169 |  0.116 |
| ('Kylie Makeup', 'Regla')                         |   0.601 | -0.24  |