# Makeup backtest (src/mu_backtest.py)


## GUMU — sin_manual — 13 cortes mensuales

| tecnica                                                     |   wmape |   bias |   bias_abs |   gana_a_LY |
|:------------------------------------------------------------|--------:|-------:|-----------:|------------:|
| media6M x trend12M@función                                  |   0.648 | -0.013 |      0.194 |          13 |
| media6M x 50%trend12M@familia                               |   0.66  |  0.066 |      0.182 |          13 |
| media6M x 50%trend12M@función                               |   0.666 |  0.093 |      0.194 |          13 |
| media3M x trend12M@función                                  |   0.666 | -0.022 |      0.191 |          13 |
| media12M x trend12M@función                                 |   0.668 |  0.057 |      0.164 |          13 |
| media3M x 50%trend12M@familia                               |   0.676 |  0.052 |      0.18  |          13 |
| media3M x 50%trend12M@función                               |   0.685 |  0.082 |      0.196 |          13 |
| media6M_plana                                               |   0.703 |  0.199 |      0.231 |          13 |
| media12M x trend12M@función x estacionalidad_EPOS@familia   |   0.717 | -0.093 |      0.129 |          13 |
| media12M x trend12M@función x estacionalidad_EPOS@función   |   0.722 | -0.096 |      0.13  |          13 |
| media3M_plana                                               |   0.724 |  0.186 |      0.237 |          13 |
| media12M_plana                                              |   0.739 |  0.286 |      0.293 |          13 |
| media12M x trend12M@función x estacionalidad_envíos@familia |   0.75  |  0.054 |      0.209 |          13 |
| media12M x trend12M@función x estacionalidad_envíos@función |   0.76  |  0.053 |      0.208 |          13 |
| media12M x estacionalidad_EPOS@familia                      |   0.776 |  0.115 |      0.134 |          13 |
| media12M x estacionalidad_EPOS@función                      |   0.787 |  0.113 |      0.133 |          12 |
| media6M(desest.) x estacionalidad_envíos@familia            |   0.804 |  0.249 |      0.292 |          13 |
| media6M(desest.) x estacionalidad_envíos@función            |   0.816 |  0.262 |      0.304 |          13 |
| media12M x estacionalidad_envíos@familia                    |   0.822 |  0.279 |      0.321 |          13 |
| media12M x estacionalidad_envíos@función                    |   0.826 |  0.277 |      0.316 |          13 |
| LY x trend12M@familia                                       |   0.841 | -0.012 |      0.181 |          11 |
| LY x trend12M@product_line                                  |   0.845 |  0.053 |      0.133 |          13 |
| LY x trend12M@función                                       |   0.874 |  0.044 |      0.172 |           9 |
| LY x trend12M@EAN                                           |   0.88  |  0.154 |      0.209 |          13 |
| LY x 50%trend12M@familia                                    |   0.887 |  0.132 |      0.194 |          11 |
| LY x 50%trend12M@product_line                               |   0.89  |  0.164 |      0.209 |          13 |
| LY x 50%trend12M@función                                    |   0.904 |  0.16  |      0.216 |          10 |
| regla_fragancias(LY+25%cortes-50%DA) x trend12M@función     |   0.95  |  0.152 |      0.276 |           6 |
| LY_plano                                                    |   0.952 |  0.276 |      0.301 |           0 |
| media6M(desest.) x estacionalidad_EPOS@familia              |   0.979 |  0.37  |      0.388 |           9 |
| media6M(desest.) x estacionalidad_EPOS@función              |   1.003 |  0.383 |      0.393 |           9 |

## GUMU — todos — 13 cortes mensuales

| tecnica                                                     |   wmape |   bias |   bias_abs |   gana_a_LY |
|:------------------------------------------------------------|--------:|-------:|-----------:|------------:|
| media3M x trend12M@función                                  |   0.67  |  0.004 |      0.209 |          13 |
| media3M x 50%trend12M@familia                               |   0.674 |  0.066 |      0.193 |          13 |
| media3M x 50%trend12M@función                               |   0.686 |  0.101 |      0.214 |          13 |
| media6M x 50%trend12M@familia                               |   0.694 |  0.121 |      0.231 |          13 |
| media6M x trend12M@función                                  |   0.696 |  0.06  |      0.267 |          13 |
| media6M x 50%trend12M@función                               |   0.709 |  0.158 |      0.254 |          13 |
| media3M_plana                                               |   0.723 |  0.199 |      0.251 |          13 |
| media6M_plana                                               |   0.742 |  0.257 |      0.289 |          13 |
| media12M x trend12M@función                                 |   0.779 |  0.204 |      0.331 |          13 |
| media12M x trend12M@función x estacionalidad_EPOS@familia   |   0.788 |  0.019 |      0.164 |          13 |
| media12M x trend12M@función x estacionalidad_EPOS@función   |   0.791 |  0.015 |      0.157 |          13 |
| media6M(desest.) x estacionalidad_envíos@familia            |   0.837 |  0.3   |      0.361 |          13 |
| media12M x estacionalidad_EPOS@familia                      |   0.838 |  0.212 |      0.222 |          13 |
| media12M_plana                                              |   0.839 |  0.415 |      0.453 |          13 |
| media12M x estacionalidad_EPOS@función                      |   0.847 |  0.209 |      0.219 |          12 |
| media6M(desest.) x estacionalidad_envíos@función            |   0.85  |  0.315 |      0.377 |          13 |
| media12M x trend12M@función x estacionalidad_envíos@familia |   0.864 |  0.204 |      0.391 |          13 |
| media12M x trend12M@función x estacionalidad_envíos@función |   0.876 |  0.206 |      0.393 |          13 |
| media12M x estacionalidad_envíos@familia                    |   0.922 |  0.409 |      0.496 |          13 |
| media12M x estacionalidad_envíos@función                    |   0.929 |  0.41  |      0.494 |          13 |
| LY x trend12M@familia                                       |   0.948 |  0.091 |      0.306 |          11 |
| LY x trend12M@product_line                                  |   0.97  |  0.17  |      0.28  |          13 |
| media6M(desest.) x estacionalidad_EPOS@familia              |   0.984 |  0.389 |      0.374 |           9 |
| LY x 50%trend12M@familia                                    |   1.004 |  0.24  |      0.356 |          11 |
| media6M(desest.) x estacionalidad_EPOS@función              |   1.008 |  0.401 |      0.381 |           9 |
| LY x trend12M@EAN                                           |   1.009 |  0.272 |      0.369 |          13 |
| LY x trend12M@función                                       |   1.016 |  0.179 |      0.356 |           8 |
| LY x 50%trend12M@product_line                               |   1.016 |  0.28  |      0.371 |          13 |
| regla_fragancias(LY+25%cortes-50%DA) x trend12M@función     |   1.023 |  0.206 |      0.354 |          10 |
| LY x 50%trend12M@función                                    |   1.038 |  0.284 |      0.406 |           8 |
| LY_plano                                                    |   1.078 |  0.389 |      0.47  |           0 |

## KYMU — sin_manual — 13 cortes mensuales

| tecnica                                                     |   wmape |   bias |   bias_abs |   gana_a_LY |
|:------------------------------------------------------------|--------:|-------:|-----------:|------------:|
| media3M x 50%trend12M@función                               |   0.573 | -0.181 |      0.181 |          13 |
| media3M x 50%trend12M@familia                               |   0.574 | -0.206 |      0.195 |          13 |
| media6M x 50%trend12M@función                               |   0.577 | -0.216 |      0.199 |          13 |
| media3M x trend12M@función                                  |   0.579 | -0.289 |      0.275 |          13 |
| media6M x trend12M@función                                  |   0.58  | -0.321 |      0.296 |          13 |
| media6M x 50%trend12M@familia                               |   0.582 | -0.238 |      0.213 |          13 |
| media3M_plana                                               |   0.589 | -0.074 |      0.103 |          13 |
| media6M_plana                                               |   0.595 | -0.111 |      0.119 |          13 |
| media12M x trend12M@función                                 |   0.643 | -0.313 |      0.264 |          13 |
| media6M(desest.) x estacionalidad_envíos@familia            |   0.681 | -0.111 |      0.199 |          13 |
| media12M_plana                                              |   0.684 | -0.094 |      0.128 |          13 |
| media12M x trend12M@función x estacionalidad_envíos@familia |   0.695 | -0.33  |      0.294 |          13 |
| media12M x trend12M@función x estacionalidad_EPOS@familia   |   0.723 | -0.404 |      0.356 |          13 |
| media12M x trend12M@función x estacionalidad_envíos@función |   0.735 | -0.326 |      0.28  |          13 |
| media12M x trend12M@función x estacionalidad_EPOS@función   |   0.737 | -0.402 |      0.353 |          13 |
| media12M x estacionalidad_envíos@familia                    |   0.737 | -0.117 |      0.201 |          13 |
| media12M x estacionalidad_EPOS@familia                      |   0.753 | -0.213 |      0.189 |          12 |
| media6M(desest.) x estacionalidad_envíos@función            |   0.753 | -0.073 |      0.177 |          13 |
| media12M x estacionalidad_EPOS@función                      |   0.769 | -0.212 |      0.192 |          12 |
| media12M x estacionalidad_envíos@función                    |   0.786 | -0.115 |      0.192 |          13 |
| regla_fragancias(LY+25%cortes-50%DA) x trend12M@función     |   0.797 | -0.31  |      0.253 |          12 |
| media6M(desest.) x estacionalidad_EPOS@familia              |   0.806 | -0.038 |      0.303 |          11 |
| LY x trend12M@familia                                       |   0.81  | -0.349 |      0.295 |          12 |
| LY x trend12M@función                                       |   0.813 | -0.314 |      0.271 |          11 |
| LY x 50%trend12M@familia                                    |   0.843 | -0.223 |      0.244 |          12 |
| LY x 50%trend12M@función                                    |   0.845 | -0.205 |      0.238 |          12 |
| media6M(desest.) x estacionalidad_EPOS@función              |   0.846 | -0.023 |      0.296 |          10 |
| LY x trend12M@EAN                                           |   0.85  | -0.202 |      0.247 |          11 |
| LY x trend12M@product_line                                  |   0.857 | -0.255 |      0.27  |          10 |
| LY x 50%trend12M@product_line                               |   0.867 | -0.176 |      0.238 |          10 |
| LY_plano                                                    |   0.89  | -0.096 |      0.208 |           0 |

## KYMU — todos — 13 cortes mensuales

| tecnica                                                     |   wmape |   bias |   bias_abs |   gana_a_LY |
|:------------------------------------------------------------|--------:|-------:|-----------:|------------:|
| media3M x 50%trend12M@familia                               |   0.595 | -0.199 |      0.185 |          13 |
| media3M x 50%trend12M@función                               |   0.597 | -0.166 |      0.173 |          13 |
| media6M x 50%trend12M@función                               |   0.598 | -0.183 |      0.171 |          13 |
| media6M x 50%trend12M@familia                               |   0.6   | -0.214 |      0.202 |          13 |
| media6M x trend12M@función                                  |   0.602 | -0.28  |      0.251 |          13 |
| media3M x trend12M@función                                  |   0.607 | -0.261 |      0.252 |          13 |
| media3M_plana                                               |   0.609 | -0.071 |      0.114 |          13 |
| media6M_plana                                               |   0.614 | -0.087 |      0.095 |          13 |
| media6M(desest.) x estacionalidad_envíos@familia            |   0.699 | -0.074 |      0.149 |          13 |
| media12M x trend12M@función                                 |   0.713 | -0.213 |      0.198 |          13 |
| media12M x trend12M@función x estacionalidad_envíos@familia |   0.762 | -0.228 |      0.225 |          13 |
| media12M_plana                                              |   0.769 |  0.01  |      0.111 |          13 |
| media12M x trend12M@función x estacionalidad_EPOS@familia   |   0.777 | -0.318 |      0.294 |          13 |
| media12M x trend12M@función x estacionalidad_EPOS@función   |   0.783 | -0.31  |      0.277 |          13 |
| media6M(desest.) x estacionalidad_envíos@función            |   0.793 | -0.028 |      0.142 |          11 |
| media12M x trend12M@función x estacionalidad_envíos@función |   0.814 | -0.225 |      0.23  |          13 |
| media12M x estacionalidad_envíos@familia                    |   0.818 | -0.012 |      0.108 |          13 |
| media6M(desest.) x estacionalidad_EPOS@familia              |   0.823 | -0.04  |      0.331 |          11 |
| media12M x estacionalidad_EPOS@familia                      |   0.824 | -0.123 |      0.224 |          13 |
| media12M x estacionalidad_EPOS@función                      |   0.829 | -0.118 |      0.212 |          13 |
| media6M(desest.) x estacionalidad_EPOS@función              |   0.854 | -0.017 |      0.316 |          11 |
| media12M x estacionalidad_envíos@función                    |   0.879 | -0.01  |      0.11  |          13 |
| regla_fragancias(LY+25%cortes-50%DA) x trend12M@función     |   0.901 | -0.28  |      0.258 |          13 |
| LY x trend12M@familia                                       |   0.905 | -0.308 |      0.286 |          12 |
| LY x trend12M@función                                       |   0.918 | -0.259 |      0.239 |          10 |
| LY x 50%trend12M@familia                                    |   0.952 | -0.174 |      0.191 |          12 |
| LY x 50%trend12M@función                                    |   0.959 | -0.15  |      0.176 |          11 |
| LY x trend12M@EAN                                           |   0.973 | -0.129 |      0.164 |          11 |
| LY x 50%trend12M@product_line                               |   1.003 | -0.086 |      0.156 |           9 |
| LY x trend12M@product_line                                  |   1.004 | -0.132 |      0.17  |           7 |
| LY_plano                                                    |   1.013 | -0.04  |      0.142 |           0 |

## GUMU — sin_manual — foto inicial sep-25

| tecnica                                                                     |   wmape |   bias |
|:----------------------------------------------------------------------------|--------:|-------:|
| media3M x trend12M@función                                                  |   0.591 | -0.195 |
| media3M x 50%trend12M@familia                                               |   0.595 | -0.087 |
| media3M x 50%trend12M@función                                               |   0.6   | -0.063 |
| media6M x 50%trend12M@familia                                               |   0.628 | -0.09  |
| media6M x trend12M@función                                                  |   0.628 | -0.197 |
| mix50(consenso,media3M x 50%trend12M@familia)                               |   0.629 | -0.084 |
| mix50(consenso,media3M x trend12M@función)                                  |   0.631 | -0.138 |
| media6M x 50%trend12M@función                                               |   0.632 | -0.066 |
| media3M_plana                                                               |   0.632 |  0.069 |
| mix50(consenso,media3M x 50%trend12M@función)                               |   0.633 | -0.072 |
| media12M x trend12M@función                                                 |   0.633 | -0.077 |
| mix50(consenso,media3M_plana)                                               |   0.639 | -0.006 |
| mix50(consenso,media6M x 50%trend12M@familia)                               |   0.646 | -0.086 |
| mix50(consenso,media6M x trend12M@función)                                  |   0.648 | -0.139 |
| mix50(consenso,media6M x 50%trend12M@función)                               |   0.649 | -0.074 |
| mix50(consenso,media6M_plana)                                               |   0.654 | -0.008 |
| mix50(consenso,media12M x trend12M@función)                                 |   0.654 | -0.079 |
| media6M_plana                                                               |   0.655 |  0.065 |
| mix50(consenso,media12M_plana)                                              |   0.674 |  0.073 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@familia)   |   0.678 | -0.105 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@función)   |   0.68  | -0.105 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@familia) |   0.681 | -0.078 |
| media12M x trend12M@función x estacionalidad_envíos@familia                 |   0.685 | -0.074 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@función) |   0.686 | -0.079 |
| mix50(consenso,LY x trend12M@familia)                                       |   0.688 | -0.086 |
| mix50(consenso,LY x trend12M@product_line)                                  |   0.691 | -0.028 |
| media12M x trend12M@función x estacionalidad_envíos@función                 |   0.699 | -0.078 |
| mix50(consenso,LY x trend12M@función)                                       |   0.702 | -0.057 |
| mix50(consenso,LY x trend12M@EAN)                                           |   0.705 |  0.028 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@familia)            |   0.707 |  0.069 |
| mix50(consenso,media12M x estacionalidad_EPOS@familia)                      |   0.708 |  0.039 |
| mix50(consenso,media12M x estacionalidad_envíos@familia)                    |   0.709 |  0.075 |
| media12M_plana                                                              |   0.709 |  0.228 |
| mix50(consenso,media12M x estacionalidad_EPOS@función)                      |   0.711 |  0.037 |
| mix50(consenso,LY x 50%trend12M@familia)                                    |   0.715 |  0.008 |
| mix50(consenso,media12M x estacionalidad_envíos@función)                    |   0.716 |  0.074 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@función)            |   0.717 |  0.08  |
| mix50(consenso,LY x 50%trend12M@product_line)                               |   0.718 |  0.037 |
| mix50(consenso,LY x 50%trend12M@función)                                    |   0.723 |  0.022 |
| mix50(consenso,regla_fragancias(LY+25%cortes-50%DA) x trend12M@función)     |   0.726 | -0.045 |
| media12M x trend12M@función x estacionalidad_EPOS@familia                   |   0.737 | -0.129 |
| media12M x trend12M@función x estacionalidad_EPOS@función                   |   0.739 | -0.129 |
| mix50(consenso,LY_plano)                                                    |   0.749 |  0.102 |
| consenso                                                                    |   0.751 | -0.081 |
| LY x trend12M@familia                                                       |   0.771 | -0.09  |
| LY x trend12M@product_line                                                  |   0.781 |  0.025 |
| media12M x estacionalidad_envíos@familia                                    |   0.782 |  0.231 |
| media6M(desest.) x estacionalidad_envíos@familia                            |   0.784 |  0.22  |
| LY x trend12M@función                                                       |   0.788 | -0.033 |
| media12M x estacionalidad_envíos@función                                    |   0.796 |  0.23  |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@familia)              |   0.801 |  0.242 |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@función)              |   0.809 |  0.241 |
| media6M(desest.) x estacionalidad_envíos@función                            |   0.81  |  0.24  |
| LY x trend12M@EAN                                                           |   0.823 |  0.137 |
| LY x 50%trend12M@familia                                                    |   0.827 |  0.097 |
| LY x 50%trend12M@product_line                                               |   0.836 |  0.155 |
| media12M x estacionalidad_EPOS@familia                                      |   0.836 |  0.158 |
| LY x 50%trend12M@función                                                    |   0.84  |  0.126 |
| media12M x estacionalidad_EPOS@función                                      |   0.841 |  0.156 |
| regla_fragancias(LY+25%cortes-50%DA) x trend12M@función                     |   0.846 | -0.009 |
| LY_plano                                                                    |   0.911 |  0.285 |
| media6M(desest.) x estacionalidad_EPOS@familia                              |   1.091 |  0.566 |
| media6M(desest.) x estacionalidad_EPOS@función                              |   1.098 |  0.563 |

## GUMU — sin_manual — corrección en mar-26 (verdad hasta ago-26)

| tecnica                                                                     |   ('bias', 'congelar') |   ('bias', 'factor_100%') |   ('bias', 'factor_50%') |   ('bias', 'recalcular') |   ('wmape', 'congelar') |   ('wmape', 'factor_100%') |   ('wmape', 'factor_50%') |   ('wmape', 'recalcular') |
|:----------------------------------------------------------------------------|-----------------------:|--------------------------:|-------------------------:|-------------------------:|------------------------:|---------------------------:|--------------------------:|--------------------------:|
| LY x 50%trend12M@familia                                                    |                  0.139 |                    -0.05  |                    0.044 |                    0.184 |                   0.933 |                      0.857 |                     0.892 |                     0.946 |
| LY x 50%trend12M@función                                                    |                  0.156 |                    -0.062 |                    0.047 |                    0.204 |                   0.945 |                      0.855 |                     0.897 |                     0.964 |
| LY x 50%trend12M@product_line                                               |                  0.153 |                    -0.094 |                    0.03  |                    0.171 |                   0.93  |                      0.831 |                     0.877 |                     0.934 |
| LY x trend12M@EAN                                                           |                  0.137 |                    -0.098 |                    0.019 |                    0.159 |                   0.91  |                      0.819 |                     0.86  |                     0.919 |
| LY x trend12M@familia                                                       |                  0.025 |                     0.031 |                    0.028 |                    0.117 |                   0.896 |                      0.899 |                     0.897 |                     0.914 |
| LY x trend12M@función                                                       |                  0.061 |                    -0.002 |                    0.029 |                    0.155 |                   0.923 |                      0.897 |                     0.91  |                     0.962 |
| LY x trend12M@product_line                                                  |                  0.054 |                    -0.076 |                   -0.011 |                    0.091 |                   0.891 |                      0.84  |                     0.865 |                     0.9   |
| LY_plano                                                                    |                  0.252 |                    -0.108 |                    0.072 |                    0.252 |                   0.98  |                      0.831 |                     0.895 |                     0.98  |
| consenso                                                                    |                  0.103 |                     0.111 |                    0.107 |                    0.259 |                   0.703 |                      0.706 |                     0.705 |                     0.7   |
| media12M x estacionalidad_EPOS@familia                                      |                 -0.002 |                    -0.316 |                   -0.159 |                   -0.036 |                   0.687 |                      0.654 |                     0.66  |                     0.671 |
| media12M x estacionalidad_EPOS@función                                      |                 -0.001 |                    -0.315 |                   -0.158 |                   -0.034 |                   0.697 |                      0.66  |                     0.669 |                     0.68  |
| media12M x estacionalidad_envíos@familia                                    |                  0.228 |                    -0.093 |                    0.068 |                    0.187 |                   0.819 |                      0.708 |                     0.754 |                     0.778 |
| media12M x estacionalidad_envíos@función                                    |                  0.22  |                    -0.097 |                    0.062 |                    0.18  |                   0.812 |                      0.699 |                     0.746 |                     0.77  |
| media12M x trend12M@función                                                 |                  0.192 |                     0.28  |                    0.236 |                    0.217 |                   0.683 |                      0.726 |                     0.702 |                     0.655 |
| media12M x trend12M@función x estacionalidad_EPOS@familia                   |                 -0.133 |                    -0.212 |                   -0.172 |                   -0.111 |                   0.694 |                      0.683 |                     0.687 |                     0.67  |
| media12M x trend12M@función x estacionalidad_EPOS@función                   |                 -0.138 |                    -0.217 |                   -0.178 |                   -0.114 |                   0.694 |                      0.682 |                     0.687 |                     0.671 |
| media12M x trend12M@función x estacionalidad_envíos@familia                 |                  0.065 |                     0.043 |                    0.054 |                    0.094 |                   0.782 |                      0.775 |                     0.778 |                     0.75  |
| media12M x trend12M@función x estacionalidad_envíos@función                 |                  0.063 |                     0.045 |                    0.054 |                    0.093 |                   0.783 |                      0.777 |                     0.78  |                     0.756 |
| media12M_plana                                                              |                  0.405 |                     0.137 |                    0.271 |                    0.321 |                   0.796 |                      0.663 |                     0.724 |                     0.711 |
| media3M x 50%trend12M@familia                                               |                  0.16  |                     0.338 |                    0.249 |                    0.217 |                   0.678 |                      0.765 |                     0.719 |                     0.685 |
| media3M x 50%trend12M@función                                               |                  0.194 |                     0.34  |                    0.267 |                    0.254 |                   0.692 |                      0.767 |                     0.727 |                     0.702 |
| media3M x trend12M@función                                                  |                  0.113 |                     0.452 |                    0.283 |                    0.222 |                   0.684 |                      0.854 |                     0.762 |                     0.708 |
| media3M_plana                                                               |                  0.275 |                     0.256 |                    0.265 |                    0.286 |                   0.721 |                      0.711 |                     0.716 |                     0.715 |
| media6M x 50%trend12M@familia                                               |                  0.207 |                     0.35  |                    0.278 |                    0.273 |                   0.682 |                      0.751 |                     0.714 |                     0.65  |
| media6M x 50%trend12M@función                                               |                  0.232 |                     0.343 |                    0.287 |                    0.295 |                   0.687 |                      0.746 |                     0.716 |                     0.653 |
| media6M x trend12M@función                                                  |                  0.138 |                     0.444 |                    0.291 |                    0.246 |                   0.666 |                      0.83  |                     0.742 |                     0.637 |
| media6M(desest.) x estacionalidad_EPOS@familia                              |                  0.022 |                    -0.469 |                   -0.224 |                   -0.144 |                   0.653 |                      0.654 |                     0.618 |                     0.638 |
| media6M(desest.) x estacionalidad_EPOS@función                              |                  0.03  |                    -0.468 |                   -0.219 |                   -0.137 |                   0.67  |                      0.657 |                     0.632 |                     0.648 |
| media6M(desest.) x estacionalidad_envíos@familia                            |                  0.2   |                    -0.076 |                    0.062 |                    0.171 |                   0.783 |                      0.687 |                     0.728 |                     0.742 |
| media6M(desest.) x estacionalidad_envíos@función                            |                  0.212 |                    -0.08  |                    0.066 |                    0.181 |                   0.785 |                      0.68  |                     0.72  |                     0.743 |
| media6M_plana                                                               |                  0.326 |                     0.267 |                    0.296 |                    0.345 |                   0.727 |                      0.698 |                     0.713 |                     0.685 |
| mix50(consenso,LY x 50%trend12M@familia)                                    |                  0.121 |                     0.023 |                    0.072 |                    0.222 |                   0.735 |                      0.701 |                     0.717 |                     0.733 |
| mix50(consenso,LY x 50%trend12M@función)                                    |                  0.13  |                     0.015 |                    0.072 |                    0.231 |                   0.742 |                      0.702 |                     0.72  |                     0.741 |
| mix50(consenso,LY x 50%trend12M@product_line)                               |                  0.128 |                    -0.004 |                    0.062 |                    0.215 |                   0.733 |                      0.691 |                     0.709 |                     0.727 |
| mix50(consenso,LY x trend12M@EAN)                                           |                  0.12  |                    -0.006 |                    0.057 |                    0.209 |                   0.724 |                      0.685 |                     0.703 |                     0.722 |
| mix50(consenso,LY x trend12M@familia)                                       |                  0.064 |                     0.071 |                    0.068 |                    0.188 |                   0.718 |                      0.72  |                     0.719 |                     0.715 |
| mix50(consenso,LY x trend12M@función)                                       |                  0.082 |                     0.052 |                    0.067 |                    0.207 |                   0.732 |                      0.722 |                     0.727 |                     0.733 |
| mix50(consenso,LY x trend12M@product_line)                                  |                  0.079 |                     0.011 |                    0.045 |                    0.175 |                   0.714 |                      0.693 |                     0.703 |                     0.706 |
| mix50(consenso,LY_plano)                                                    |                  0.177 |                    -0.017 |                    0.08  |                    0.256 |                   0.755 |                      0.691 |                     0.718 |                     0.752 |
| mix50(consenso,media12M x estacionalidad_EPOS@familia)                      |                  0.05  |                    -0.143 |                   -0.046 |                    0.112 |                   0.639 |                      0.598 |                     0.614 |                     0.609 |
| mix50(consenso,media12M x estacionalidad_EPOS@función)                      |                  0.051 |                    -0.143 |                   -0.046 |                    0.113 |                   0.645 |                      0.602 |                     0.618 |                     0.61  |
| mix50(consenso,media12M x estacionalidad_envíos@familia)                    |                  0.166 |                    -0.007 |                    0.079 |                    0.223 |                   0.698 |                      0.642 |                     0.666 |                     0.664 |
| mix50(consenso,media12M x estacionalidad_envíos@función)                    |                  0.162 |                    -0.009 |                    0.076 |                    0.22  |                   0.691 |                      0.638 |                     0.662 |                     0.665 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@familia)   |                 -0.015 |                    -0.059 |                   -0.037 |                    0.074 |                   0.639 |                      0.629 |                     0.634 |                     0.6   |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@función)   |                 -0.017 |                    -0.062 |                   -0.04  |                    0.073 |                   0.64  |                      0.63  |                     0.635 |                     0.598 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@familia) |                  0.084 |                     0.076 |                    0.08  |                    0.177 |                   0.684 |                      0.682 |                     0.683 |                     0.648 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@función) |                  0.083 |                     0.077 |                    0.08  |                    0.176 |                   0.684 |                      0.682 |                     0.683 |                     0.654 |
| mix50(consenso,media12M x trend12M@función)                                 |                  0.147 |                     0.193 |                    0.17  |                    0.238 |                   0.654 |                      0.67  |                     0.662 |                     0.623 |
| mix50(consenso,media12M_plana)                                              |                  0.254 |                     0.125 |                    0.19  |                    0.29  |                   0.676 |                      0.624 |                     0.648 |                     0.643 |
| mix50(consenso,media3M x 50%trend12M@familia)                               |                  0.131 |                     0.216 |                    0.174 |                    0.238 |                   0.629 |                      0.665 |                     0.646 |                     0.638 |
| mix50(consenso,media3M x 50%trend12M@función)                               |                  0.148 |                     0.219 |                    0.184 |                    0.257 |                   0.638 |                      0.668 |                     0.653 |                     0.646 |
| mix50(consenso,media3M x trend12M@función)                                  |                  0.108 |                     0.259 |                    0.184 |                    0.241 |                   0.637 |                      0.704 |                     0.668 |                     0.643 |
| mix50(consenso,media3M_plana)                                               |                  0.189 |                     0.184 |                    0.186 |                    0.273 |                   0.644 |                      0.641 |                     0.643 |                     0.652 |
| mix50(consenso,media6M x 50%trend12M@familia)                               |                  0.155 |                     0.224 |                    0.189 |                    0.266 |                   0.643 |                      0.668 |                     0.655 |                     0.617 |
| mix50(consenso,media6M x 50%trend12M@función)                               |                  0.167 |                     0.222 |                    0.195 |                    0.277 |                   0.646 |                      0.669 |                     0.657 |                     0.622 |
| mix50(consenso,media6M x trend12M@función)                                  |                  0.12  |                     0.258 |                    0.189 |                    0.253 |                   0.644 |                      0.702 |                     0.672 |                     0.617 |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@familia)              |                  0.062 |                    -0.272 |                   -0.105 |                    0.058 |                   0.614 |                      0.583 |                     0.583 |                     0.588 |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@función)              |                  0.067 |                    -0.272 |                   -0.103 |                    0.061 |                   0.622 |                      0.588 |                     0.589 |                     0.593 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@familia)            |                  0.152 |                     0.005 |                    0.078 |                    0.215 |                   0.685 |                      0.635 |                     0.657 |                     0.65  |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@función)            |                  0.157 |                     0.002 |                    0.08  |                    0.22  |                   0.683 |                      0.629 |                     0.652 |                     0.654 |
| mix50(consenso,media6M_plana)                                               |                  0.214 |                     0.191 |                    0.202 |                    0.302 |                   0.654 |                      0.645 |                     0.65  |                     0.632 |
| mix50(consenso,regla_fragancias(LY+25%cortes-50%DA) x trend12M@función)     |                  0.166 |                     0.127 |                    0.146 |                    0.319 |                   0.792 |                      0.777 |                     0.784 |                     0.783 |
| regla_fragancias(LY+25%cortes-50%DA) x trend12M@función                     |                  0.228 |                     0.142 |                    0.185 |                    0.379 |                   1.054 |                      1.008 |                     1.03  |                     1.063 |

## GUMU — todos — foto inicial sep-25

| tecnica                                                                     |   wmape |   bias |
|:----------------------------------------------------------------------------|--------:|-------:|
| media3M x trend12M@función                                                  |   0.584 | -0.195 |
| media3M x 50%trend12M@familia                                               |   0.587 | -0.088 |
| media3M x 50%trend12M@función                                               |   0.593 | -0.064 |
| media3M_plana                                                               |   0.624 |  0.068 |
| mix50(consenso,media3M x 50%trend12M@familia)                               |   0.631 | -0.065 |
| media6M x trend12M@función                                                  |   0.633 | -0.171 |
| mix50(consenso,media3M x trend12M@función)                                  |   0.633 | -0.119 |
| mix50(consenso,media3M x 50%trend12M@función)                               |   0.635 | -0.053 |
| media6M x 50%trend12M@familia                                               |   0.641 | -0.057 |
| mix50(consenso,media3M_plana)                                               |   0.642 |  0.012 |
| media6M x 50%trend12M@función                                               |   0.645 | -0.033 |
| mix50(consenso,media6M x trend12M@función)                                  |   0.657 | -0.107 |
| mix50(consenso,media6M x 50%trend12M@familia)                               |   0.657 | -0.05  |
| mix50(consenso,media6M x 50%trend12M@función)                               |   0.66  | -0.038 |
| media12M x trend12M@función                                                 |   0.664 | -0.015 |
| mix50(consenso,media6M_plana)                                               |   0.668 |  0.03  |
| media6M_plana                                                               |   0.675 |  0.104 |
| mix50(consenso,media12M x trend12M@función)                                 |   0.679 | -0.029 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@familia)   |   0.701 | -0.057 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@función)   |   0.704 | -0.056 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@familia) |   0.706 | -0.028 |
| mix50(consenso,media12M_plana)                                              |   0.709 |  0.133 |
| mix50(consenso,LY x trend12M@familia)                                       |   0.713 | -0.042 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@función) |   0.713 | -0.029 |
| media12M x trend12M@función x estacionalidad_envíos@familia                 |   0.719 | -0.013 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@familia)            |   0.722 |  0.104 |
| mix50(consenso,LY x trend12M@product_line)                                  |   0.728 |  0.025 |
| mix50(consenso,LY x trend12M@función)                                       |   0.73  | -0.011 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@función)            |   0.733 |  0.115 |
| media12M x trend12M@función x estacionalidad_envíos@función                 |   0.735 | -0.014 |
| mix50(consenso,media12M x estacionalidad_EPOS@familia)                      |   0.74  |  0.096 |
| mix50(consenso,LY x trend12M@EAN)                                           |   0.744 |  0.086 |
| mix50(consenso,media12M x estacionalidad_EPOS@función)                      |   0.745 |  0.095 |
| mix50(consenso,media12M x estacionalidad_envíos@familia)                    |   0.745 |  0.135 |
| mix50(consenso,LY x 50%trend12M@familia)                                    |   0.746 |  0.057 |
| mix50(consenso,regla_fragancias(LY+25%cortes-50%DA) x trend12M@función)     |   0.75  | -0.005 |
| mix50(consenso,media12M x estacionalidad_envíos@función)                    |   0.754 |  0.135 |
| mix50(consenso,LY x 50%trend12M@product_line)                               |   0.754 |  0.091 |
| mix50(consenso,LY x 50%trend12M@función)                                    |   0.755 |  0.073 |
| media12M x trend12M@función x estacionalidad_EPOS@familia                   |   0.759 | -0.071 |
| media12M x trend12M@función x estacionalidad_EPOS@función                   |   0.765 | -0.07  |
| media12M_plana                                                              |   0.769 |  0.309 |
| consenso                                                                    |   0.773 | -0.043 |
| mix50(consenso,LY_plano)                                                    |   0.785 |  0.156 |
| media6M(desest.) x estacionalidad_envíos@familia                            |   0.799 |  0.252 |
| LY x trend12M@familia                                                       |   0.821 | -0.04  |
| media6M(desest.) x estacionalidad_envíos@función                            |   0.824 |  0.273 |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@familia)              |   0.826 |  0.29  |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@función)              |   0.84  |  0.294 |
| media12M x estacionalidad_envíos@familia                                    |   0.842 |  0.312 |
| LY x trend12M@función                                                       |   0.843 |  0.022 |
| LY x trend12M@product_line                                                  |   0.851 |  0.093 |
| media12M x estacionalidad_envíos@función                                    |   0.858 |  0.314 |
| media12M x estacionalidad_EPOS@familia                                      |   0.88  |  0.235 |
| media12M x estacionalidad_EPOS@función                                      |   0.887 |  0.234 |
| LY x 50%trend12M@familia                                                    |   0.89  |  0.158 |
| regla_fragancias(LY+25%cortes-50%DA) x trend12M@función                     |   0.899 |  0.033 |
| LY x trend12M@EAN                                                           |   0.904 |  0.215 |
| LY x 50%trend12M@función                                                    |   0.906 |  0.188 |
| LY x 50%trend12M@product_line                                               |   0.909 |  0.224 |
| LY_plano                                                                    |   0.987 |  0.355 |
| media6M(desest.) x estacionalidad_EPOS@familia                              |   1.13  |  0.624 |
| media6M(desest.) x estacionalidad_EPOS@función                              |   1.147 |  0.632 |

## GUMU — todos — corrección en mar-26 (verdad hasta ago-26)

| tecnica                                                                     |   ('bias', 'congelar') |   ('bias', 'factor_100%') |   ('bias', 'factor_50%') |   ('bias', 'recalcular') |   ('wmape', 'congelar') |   ('wmape', 'factor_100%') |   ('wmape', 'factor_50%') |   ('wmape', 'recalcular') |
|:----------------------------------------------------------------------------|-----------------------:|--------------------------:|-------------------------:|-------------------------:|------------------------:|---------------------------:|--------------------------:|--------------------------:|
| LY x 50%trend12M@familia                                                    |                  0.308 |                     0.239 |                    0.273 |                    0.349 |                   1.134 |                      1.095 |                     1.114 |                     1.146 |
| LY x 50%trend12M@función                                                    |                  0.358 |                     0.252 |                    0.305 |                    0.401 |                   1.18  |                      1.119 |                     1.149 |                     1.197 |
| LY x 50%trend12M@product_line                                               |                  0.334 |                     0.193 |                    0.264 |                    0.351 |                   1.146 |                      1.068 |                     1.106 |                     1.149 |
| LY x trend12M@EAN                                                           |                  0.319 |                     0.187 |                    0.253 |                    0.336 |                   1.128 |                      1.055 |                     1.091 |                     1.135 |
| LY x trend12M@familia                                                       |                  0.189 |                     0.358 |                    0.274 |                    0.273 |                   1.085 |                      1.183 |                     1.133 |                     1.101 |
| LY x trend12M@función                                                       |                  0.291 |                     0.381 |                    0.336 |                    0.375 |                   1.18  |                      1.234 |                     1.207 |                     1.214 |
| LY x trend12M@product_line                                                  |                  0.243 |                     0.242 |                    0.242 |                    0.275 |                   1.11  |                      1.109 |                     1.109 |                     1.117 |
| LY_plano                                                                    |                  0.426 |                     0.154 |                    0.29  |                    0.426 |                   1.193 |                      1.039 |                     1.111 |                     1.193 |
| consenso                                                                    |                  0.163 |                     0.065 |                    0.114 |                    0.259 |                   0.742 |                      0.702 |                     0.721 |                     0.703 |
| media12M x estacionalidad_EPOS@familia                                      |                  0.228 |                    -0.372 |                   -0.072 |                    0.115 |                   0.856 |                      0.73  |                     0.759 |                     0.772 |
| media12M x estacionalidad_EPOS@función                                      |                  0.232 |                    -0.367 |                   -0.067 |                    0.112 |                   0.869 |                      0.734 |                     0.77  |                     0.776 |
| media12M x estacionalidad_envíos@familia                                    |                  0.515 |                    -0.165 |                    0.175 |                    0.373 |                   1.048 |                      0.761 |                     0.873 |                     0.917 |
| media12M x estacionalidad_envíos@función                                    |                  0.512 |                    -0.155 |                    0.179 |                    0.37  |                   1.048 |                      0.766 |                     0.873 |                     0.915 |
| media12M x trend12M@función                                                 |                  0.531 |                     0.22  |                    0.376 |                    0.476 |                   0.972 |                      0.821 |                     0.889 |                     0.872 |
| media12M x trend12M@función x estacionalidad_EPOS@familia                   |                  0.095 |                    -0.261 |                   -0.083 |                    0.078 |                   0.854 |                      0.766 |                     0.797 |                     0.801 |
| media12M x trend12M@función x estacionalidad_EPOS@función                   |                  0.09  |                    -0.262 |                   -0.086 |                    0.069 |                   0.854 |                      0.765 |                     0.796 |                     0.798 |
| media12M x trend12M@función x estacionalidad_envíos@familia                 |                  0.347 |                    -0.021 |                    0.163 |                    0.327 |                   0.999 |                      0.834 |                     0.908 |                     0.928 |
| media12M x trend12M@función x estacionalidad_envíos@función                 |                  0.352 |                    -0.002 |                    0.175 |                    0.33  |                   1.008 |                      0.853 |                     0.921 |                     0.94  |
| media12M_plana                                                              |                  0.768 |                     0.068 |                    0.418 |                    0.527 |                   1.119 |                      0.745 |                     0.898 |                     0.88  |
| media3M x 50%trend12M@familia                                               |                  0.371 |                     0.104 |                    0.238 |                    0.22  |                   0.857 |                      0.732 |                     0.788 |                     0.683 |
| media3M x 50%trend12M@función                                               |                  0.418 |                     0.109 |                    0.263 |                    0.267 |                   0.883 |                      0.737 |                     0.803 |                     0.703 |
| media3M x trend12M@función                                                  |                  0.315 |                     0.19  |                    0.252 |                    0.244 |                   0.845 |                      0.786 |                     0.814 |                     0.712 |
| media3M_plana                                                               |                  0.522 |                     0.047 |                    0.284 |                    0.29  |                   0.942 |                      0.716 |                     0.809 |                     0.714 |
| media6M x 50%trend12M@familia                                               |                  0.455 |                     0.148 |                    0.302 |                    0.339 |                   0.889 |                      0.748 |                     0.81  |                     0.692 |
| media6M x 50%trend12M@función                                               |                  0.5   |                     0.15  |                    0.325 |                    0.381 |                   0.914 |                      0.742 |                     0.818 |                     0.713 |
| media6M x trend12M@función                                                  |                  0.388 |                     0.234 |                    0.311 |                    0.348 |                   0.867 |                      0.787 |                     0.825 |                     0.711 |
| media6M(desest.) x estacionalidad_EPOS@familia                              |                  0.141 |                    -0.429 |                   -0.144 |                   -0.106 |                   0.734 |                      0.676 |                     0.665 |                     0.652 |
| media6M(desest.) x estacionalidad_EPOS@función                              |                  0.156 |                    -0.422 |                   -0.133 |                   -0.103 |                   0.757 |                      0.682 |                     0.683 |                     0.658 |
| media6M(desest.) x estacionalidad_envíos@familia                            |                  0.356 |                    -0.161 |                    0.097 |                    0.232 |                   0.891 |                      0.706 |                     0.773 |                     0.776 |
| media6M(desest.) x estacionalidad_envíos@función                            |                  0.359 |                    -0.143 |                    0.108 |                    0.243 |                   0.889 |                      0.706 |                     0.772 |                     0.781 |
| media6M_plana                                                               |                  0.612 |                     0.086 |                    0.349 |                    0.415 |                   0.978 |                      0.726 |                     0.831 |                     0.731 |
| mix50(consenso,LY x 50%trend12M@familia)                                    |                  0.235 |                     0.151 |                    0.193 |                    0.304 |                   0.834 |                      0.798 |                     0.815 |                     0.824 |
| mix50(consenso,LY x 50%trend12M@función)                                    |                  0.261 |                     0.158 |                    0.209 |                    0.33  |                   0.856 |                      0.812 |                     0.833 |                     0.847 |
| mix50(consenso,LY x 50%trend12M@product_line)                               |                  0.249 |                     0.13  |                    0.189 |                    0.305 |                   0.838 |                      0.791 |                     0.813 |                     0.825 |
| mix50(consenso,LY x trend12M@EAN)                                           |                  0.241 |                     0.127 |                    0.184 |                    0.297 |                   0.83  |                      0.785 |                     0.807 |                     0.82  |
| mix50(consenso,LY x trend12M@familia)                                       |                  0.176 |                     0.196 |                    0.186 |                    0.266 |                   0.812 |                      0.82  |                     0.816 |                     0.8   |
| mix50(consenso,LY x trend12M@función)                                       |                  0.227 |                     0.211 |                    0.219 |                    0.317 |                   0.857 |                      0.85  |                     0.854 |                     0.849 |
| mix50(consenso,LY x trend12M@product_line)                                  |                  0.203 |                     0.15  |                    0.176 |                    0.267 |                   0.821 |                      0.801 |                     0.811 |                     0.806 |
| mix50(consenso,LY_plano)                                                    |                  0.294 |                     0.112 |                    0.203 |                    0.342 |                   0.859 |                      0.785 |                     0.818 |                     0.848 |
| mix50(consenso,media12M x estacionalidad_EPOS@familia)                      |                  0.195 |                    -0.215 |                   -0.01  |                    0.187 |                   0.742 |                      0.65  |                     0.672 |                     0.663 |
| mix50(consenso,media12M x estacionalidad_EPOS@función)                      |                  0.197 |                    -0.211 |                   -0.007 |                    0.185 |                   0.75  |                      0.653 |                     0.678 |                     0.662 |
| mix50(consenso,media12M x estacionalidad_envíos@familia)                    |                  0.339 |                    -0.079 |                    0.13  |                    0.316 |                   0.828 |                      0.684 |                     0.737 |                     0.733 |
| mix50(consenso,media12M x estacionalidad_envíos@función)                    |                  0.337 |                    -0.071 |                    0.133 |                    0.314 |                   0.825 |                      0.686 |                     0.739 |                     0.737 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@familia)   |                  0.129 |                    -0.122 |                    0.003 |                    0.168 |                   0.736 |                      0.669 |                     0.695 |                     0.668 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@función)   |                  0.126 |                    -0.123 |                    0.002 |                    0.164 |                   0.737 |                      0.67  |                     0.695 |                     0.664 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@familia) |                  0.255 |                     0.017 |                    0.136 |                    0.293 |                   0.807 |                      0.721 |                     0.76  |                     0.734 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@función) |                  0.257 |                     0.028 |                    0.143 |                    0.294 |                   0.812 |                      0.73  |                     0.767 |                     0.743 |
| mix50(consenso,media12M x trend12M@función)                                 |                  0.347 |                     0.148 |                    0.248 |                    0.367 |                   0.811 |                      0.72  |                     0.763 |                     0.724 |
| mix50(consenso,media12M_plana)                                              |                  0.465 |                     0.067 |                    0.266 |                    0.393 |                   0.853 |                      0.676 |                     0.752 |                     0.724 |
| mix50(consenso,media3M x 50%trend12M@familia)                               |                  0.267 |                     0.086 |                    0.176 |                    0.239 |                   0.74  |                      0.669 |                     0.7   |                     0.642 |
| mix50(consenso,media3M x 50%trend12M@función)                               |                  0.291 |                     0.089 |                    0.19  |                    0.263 |                   0.755 |                      0.67  |                     0.708 |                     0.652 |
| mix50(consenso,media3M x trend12M@función)                                  |                  0.239 |                     0.128 |                    0.183 |                    0.251 |                   0.739 |                      0.692 |                     0.714 |                     0.65  |
| mix50(consenso,media3M_plana)                                               |                  0.342 |                     0.055 |                    0.199 |                    0.274 |                   0.775 |                      0.657 |                     0.707 |                     0.657 |
| mix50(consenso,media6M x 50%trend12M@familia)                               |                  0.309 |                     0.11  |                    0.209 |                    0.299 |                   0.764 |                      0.684 |                     0.721 |                     0.642 |
| mix50(consenso,media6M x 50%trend12M@función)                               |                  0.331 |                     0.111 |                    0.221 |                    0.32  |                   0.777 |                      0.686 |                     0.728 |                     0.652 |
| mix50(consenso,media6M x trend12M@función)                                  |                  0.275 |                     0.151 |                    0.213 |                    0.303 |                   0.761 |                      0.707 |                     0.733 |                     0.652 |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@familia)              |                  0.152 |                    -0.314 |                   -0.081 |                    0.076 |                   0.673 |                      0.62  |                     0.618 |                     0.6   |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@función)              |                  0.159 |                    -0.312 |                   -0.077 |                    0.078 |                   0.686 |                      0.625 |                     0.626 |                     0.603 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@familia)            |                  0.259 |                    -0.07  |                    0.095 |                    0.245 |                   0.756 |                      0.651 |                     0.691 |                     0.669 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@función)            |                  0.261 |                    -0.058 |                    0.101 |                    0.251 |                   0.754 |                      0.651 |                     0.69  |                     0.676 |
| mix50(consenso,media6M_plana)                                               |                  0.388 |                     0.078 |                    0.233 |                    0.337 |                   0.797 |                      0.67  |                     0.728 |                     0.658 |
| mix50(consenso,regla_fragancias(LY+25%cortes-50%DA) x trend12M@función)     |                  0.229 |                     0.206 |                    0.217 |                    0.344 |                   0.844 |                      0.834 |                     0.839 |                     0.827 |
| regla_fragancias(LY+25%cortes-50%DA) x trend12M@función                     |                  0.295 |                     0.368 |                    0.331 |                    0.429 |                   1.154 |                      1.199 |                     1.176 |                     1.162 |

## KYMU — sin_manual — foto inicial sep-25

| tecnica                                                                     |   wmape |   bias |
|:----------------------------------------------------------------------------|--------:|-------:|
| media6M x 50%trend12M@familia                                               |   0.649 | -0.306 |
| media6M x 50%trend12M@función                                               |   0.655 | -0.281 |
| media6M x trend12M@función                                                  |   0.659 | -0.378 |
| media6M_plana                                                               |   0.661 | -0.185 |
| media3M x 50%trend12M@familia                                               |   0.692 | -0.224 |
| media6M(desest.) x estacionalidad_envíos@familia                            |   0.695 | -0.3   |
| media3M x 50%trend12M@función                                               |   0.697 | -0.2   |
| media3M x trend12M@función                                                  |   0.698 | -0.31  |
| media3M_plana                                                               |   0.71  | -0.09  |
| mix50(consenso,media6M x 50%trend12M@familia)                               |   0.712 | -0.116 |
| mix50(consenso,media6M x trend12M@función)                                  |   0.712 | -0.152 |
| mix50(consenso,media6M x 50%trend12M@función)                               |   0.715 | -0.104 |
| mix50(consenso,media6M_plana)                                               |   0.719 | -0.056 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@familia)            |   0.726 | -0.113 |
| media6M(desest.) x estacionalidad_envíos@función                            |   0.728 | -0.273 |
| mix50(consenso,media3M x trend12M@función)                                  |   0.736 | -0.118 |
| mix50(consenso,media3M x 50%trend12M@familia)                               |   0.737 | -0.075 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@función)            |   0.739 | -0.1   |
| mix50(consenso,media3M x 50%trend12M@función)                               |   0.741 | -0.063 |
| mix50(consenso,LY x trend12M@familia)                                       |   0.745 | -0.201 |
| mix50(consenso,regla_fragancias(LY+25%cortes-50%DA) x trend12M@función)     |   0.747 | -0.173 |
| mix50(consenso,media3M_plana)                                               |   0.749 | -0.008 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@familia) |   0.75  | -0.161 |
| media12M x trend12M@función                                                 |   0.753 | -0.286 |
| mix50(consenso,LY x trend12M@función)                                       |   0.755 | -0.175 |
| mix50(consenso,media12M x trend12M@función)                                 |   0.757 | -0.106 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@función) |   0.758 | -0.157 |
| mix50(consenso,LY x 50%trend12M@familia)                                    |   0.76  | -0.145 |
| media12M x trend12M@función x estacionalidad_envíos@familia                 |   0.762 | -0.395 |
| mix50(consenso,LY x trend12M@EAN)                                           |   0.763 | -0.131 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@familia)   |   0.763 | -0.166 |
| mix50(consenso,LY x 50%trend12M@función)                                    |   0.766 | -0.133 |
| mix50(consenso,LY x trend12M@product_line)                                  |   0.766 | -0.167 |
| mix50(consenso,media12M x estacionalidad_envíos@familia)                    |   0.766 | -0.071 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@función)   |   0.769 | -0.164 |
| mix50(consenso,LY x 50%trend12M@product_line)                               |   0.771 | -0.128 |
| mix50(consenso,LY_plano)                                                    |   0.78  | -0.09  |
| mix50(consenso,media12M x estacionalidad_envíos@función)                    |   0.78  | -0.066 |
| mix50(consenso,media12M_plana)                                              |   0.781 | -0     |
| media12M x estacionalidad_envíos@familia                                    |   0.783 | -0.216 |
| LY x trend12M@familia                                                       |   0.785 | -0.475 |
| media12M x trend12M@función x estacionalidad_envíos@función                 |   0.786 | -0.387 |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@familia)              |   0.787 |  0.027 |
| mix50(consenso,media12M x estacionalidad_EPOS@familia)                      |   0.788 | -0.077 |
| regla_fragancias(LY+25%cortes-50%DA) x trend12M@función                     |   0.789 | -0.42  |
| mix50(consenso,media12M x estacionalidad_EPOS@función)                      |   0.797 | -0.076 |
| LY x trend12M@función                                                       |   0.802 | -0.423 |
| media12M_plana                                                              |   0.802 | -0.074 |
| media12M x trend12M@función x estacionalidad_EPOS@familia                   |   0.807 | -0.405 |
| LY x 50%trend12M@familia                                                    |   0.807 | -0.365 |
| LY x trend12M@EAN                                                           |   0.809 | -0.336 |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@función)              |   0.817 |  0.032 |
| LY x 50%trend12M@función                                                    |   0.819 | -0.339 |
| media12M x estacionalidad_envíos@función                                    |   0.823 | -0.206 |
| LY x trend12M@product_line                                                  |   0.823 | -0.407 |
| media6M(desest.) x estacionalidad_EPOS@familia                              |   0.827 | -0.02  |
| media12M x trend12M@función x estacionalidad_EPOS@función                   |   0.827 | -0.402 |
| LY x 50%trend12M@product_line                                               |   0.827 | -0.331 |
| LY_plano                                                                    |   0.844 | -0.254 |
| media12M x estacionalidad_EPOS@familia                                      |   0.845 | -0.228 |
| media12M x estacionalidad_EPOS@función                                      |   0.869 | -0.225 |
| consenso                                                                    |   0.873 |  0.074 |
| media6M(desest.) x estacionalidad_EPOS@función                              |   0.893 | -0.01  |

## KYMU — sin_manual — corrección en mar-26 (verdad hasta ago-26)

| tecnica                                                                     |   ('bias', 'congelar') |   ('bias', 'factor_100%') |   ('bias', 'factor_50%') |   ('bias', 'recalcular') |   ('wmape', 'congelar') |   ('wmape', 'factor_100%') |   ('wmape', 'factor_50%') |   ('wmape', 'recalcular') |
|:----------------------------------------------------------------------------|-----------------------:|--------------------------:|-------------------------:|-------------------------:|------------------------:|---------------------------:|--------------------------:|--------------------------:|
| LY x 50%trend12M@familia                                                    |                  0.107 |                    -0.206 |                   -0.05  |                    0.106 |                   0.851 |                      0.764 |                     0.797 |                     0.851 |
| LY x 50%trend12M@función                                                    |                  0.155 |                    -0.197 |                   -0.021 |                    0.145 |                   0.881 |                      0.773 |                     0.816 |                     0.871 |
| LY x 50%trend12M@product_line                                               |                  0.204 |                    -0.24  |                   -0.018 |                    0.204 |                   0.91  |                      0.775 |                     0.822 |                     0.905 |
| LY x trend12M@EAN                                                           |                  0.158 |                    -0.219 |                   -0.03  |                    0.141 |                   0.895 |                      0.778 |                     0.821 |                     0.881 |
| LY x trend12M@familia                                                       |                 -0.088 |                    -0.207 |                   -0.148 |                   -0.089 |                   0.787 |                      0.764 |                     0.774 |                     0.786 |
| LY x trend12M@función                                                       |                  0.009 |                    -0.188 |                   -0.09  |                   -0.012 |                   0.843 |                      0.788 |                     0.811 |                     0.824 |
| LY x trend12M@product_line                                                  |                  0.107 |                    -0.278 |                   -0.085 |                    0.107 |                   0.901 |                      0.795 |                     0.831 |                     0.892 |
| LY_plano                                                                    |                  0.301 |                    -0.204 |                    0.048 |                    0.301 |                   0.936 |                      0.764 |                     0.829 |                     0.936 |
| consenso                                                                    |                  0.389 |                    -0.162 |                    0.113 |                    0.09  |                   1.124 |                      0.857 |                     0.967 |                     0.775 |
| media12M x estacionalidad_EPOS@familia                                      |                  0.061 |                    -0.408 |                   -0.174 |                   -0.04  |                   0.657 |                      0.641 |                     0.623 |                     0.594 |
| media12M x estacionalidad_EPOS@función                                      |                  0.045 |                    -0.419 |                   -0.187 |                   -0.059 |                   0.682 |                      0.665 |                     0.646 |                     0.612 |
| media12M x estacionalidad_envíos@familia                                    |                  0.506 |                     0.049 |                    0.277 |                    0.268 |                   0.95  |                      0.733 |                     0.828 |                     0.737 |
| media12M x estacionalidad_envíos@función                                    |                  0.52  |                     0.061 |                    0.291 |                    0.287 |                   1.002 |                      0.768 |                     0.874 |                     0.799 |
| media12M x trend12M@función                                                 |                  0.102 |                    -0.175 |                   -0.037 |                   -0.092 |                   0.702 |                      0.654 |                     0.666 |                     0.544 |
| media12M x trend12M@función x estacionalidad_EPOS@familia                   |                 -0.196 |                    -0.418 |                   -0.307 |                   -0.278 |                   0.634 |                      0.653 |                     0.636 |                     0.606 |
| media12M x trend12M@función x estacionalidad_EPOS@función                   |                 -0.206 |                    -0.429 |                   -0.318 |                   -0.288 |                   0.66  |                      0.678 |                     0.663 |                     0.624 |
| media12M x trend12M@función x estacionalidad_envíos@familia                 |                  0.144 |                     0.035 |                    0.09  |                   -0.046 |                   0.781 |                      0.737 |                     0.759 |                     0.649 |
| media12M x trend12M@función x estacionalidad_envíos@función                 |                  0.176 |                     0.07  |                    0.123 |                   -0.021 |                   0.846 |                      0.798 |                     0.822 |                     0.702 |
| media12M_plana                                                              |                  0.447 |                    -0.166 |                    0.141 |                    0.207 |                   0.839 |                      0.644 |                     0.7   |                     0.605 |
| media3M x 50%trend12M@familia                                               |                  0.004 |                    -0.145 |                   -0.07  |                   -0.142 |                   0.601 |                      0.587 |                     0.591 |                     0.461 |
| media3M x 50%trend12M@función                                               |                  0.039 |                    -0.149 |                   -0.055 |                   -0.117 |                   0.614 |                      0.591 |                     0.596 |                     0.468 |
| media3M x trend12M@función                                                  |                 -0.102 |                    -0.156 |                   -0.129 |                   -0.243 |                   0.602 |                      0.6   |                     0.6   |                     0.485 |
| media3M_plana                                                               |                  0.18  |                    -0.144 |                    0.018 |                    0.009 |                   0.649 |                      0.587 |                     0.604 |                     0.479 |
| media6M x 50%trend12M@familia                                               |                  0.005 |                    -0.078 |                   -0.036 |                   -0.082 |                   0.542 |                      0.527 |                     0.533 |                     0.45  |
| media6M x 50%trend12M@función                                               |                  0.04  |                    -0.084 |                   -0.022 |                   -0.055 |                   0.554 |                      0.53  |                     0.539 |                     0.455 |
| media6M x trend12M@función                                                  |                 -0.101 |                    -0.094 |                   -0.097 |                   -0.191 |                   0.54  |                      0.541 |                     0.54  |                     0.461 |
| media6M(desest.) x estacionalidad_EPOS@familia                              |                 -0.064 |                    -0.511 |                   -0.288 |                   -0.228 |                   0.51  |                      0.605 |                     0.524 |                     0.512 |
| media6M(desest.) x estacionalidad_EPOS@función                              |                 -0.068 |                    -0.534 |                   -0.301 |                   -0.233 |                   0.525 |                      0.627 |                     0.539 |                     0.531 |
| media6M(desest.) x estacionalidad_envíos@familia                            |                  0.334 |                     0.21  |                    0.272 |                    0.233 |                   0.763 |                      0.702 |                     0.73  |                     0.658 |
| media6M(desest.) x estacionalidad_envíos@función                            |                  0.371 |                     0.226 |                    0.298 |                    0.277 |                   0.82  |                      0.749 |                     0.783 |                     0.72  |
| media6M_plana                                                               |                  0.181 |                    -0.077 |                    0.052 |                    0.08  |                   0.601 |                      0.527 |                     0.555 |                     0.488 |
| mix50(consenso,LY x 50%trend12M@familia)                                    |                  0.248 |                    -0.182 |                    0.033 |                    0.098 |                   0.89  |                      0.75  |                     0.799 |                     0.738 |
| mix50(consenso,LY x 50%trend12M@función)                                    |                  0.272 |                    -0.179 |                    0.047 |                    0.117 |                   0.905 |                      0.752 |                     0.805 |                     0.749 |
| mix50(consenso,LY x 50%trend12M@product_line)                               |                  0.296 |                    -0.2   |                    0.048 |                    0.147 |                   0.918 |                      0.754 |                     0.808 |                     0.762 |
| mix50(consenso,LY x trend12M@EAN)                                           |                  0.273 |                    -0.189 |                    0.042 |                    0.115 |                   0.908 |                      0.755 |                     0.809 |                     0.748 |
| mix50(consenso,LY x trend12M@familia)                                       |                  0.151 |                    -0.181 |                   -0.015 |                    0     |                   0.852 |                      0.757 |                     0.793 |                     0.7   |
| mix50(consenso,LY x trend12M@función)                                       |                  0.199 |                    -0.173 |                    0.013 |                    0.039 |                   0.88  |                      0.761 |                     0.804 |                     0.721 |
| mix50(consenso,LY x trend12M@product_line)                                  |                  0.248 |                    -0.218 |                    0.015 |                    0.098 |                   0.908 |                      0.765 |                     0.813 |                     0.747 |
| mix50(consenso,LY_plano)                                                    |                  0.345 |                    -0.183 |                    0.081 |                    0.195 |                   0.935 |                      0.744 |                     0.81  |                     0.784 |
| mix50(consenso,media12M x estacionalidad_EPOS@familia)                      |                  0.225 |                    -0.29  |                   -0.033 |                    0.025 |                   0.823 |                      0.692 |                     0.727 |                     0.62  |
| mix50(consenso,media12M x estacionalidad_EPOS@función)                      |                  0.217 |                    -0.296 |                   -0.04  |                    0.015 |                   0.829 |                      0.702 |                     0.736 |                     0.623 |
| mix50(consenso,media12M x estacionalidad_envíos@familia)                    |                  0.447 |                    -0.064 |                    0.191 |                    0.179 |                   0.942 |                      0.738 |                     0.819 |                     0.689 |
| mix50(consenso,media12M x estacionalidad_envíos@función)                    |                  0.454 |                    -0.059 |                    0.198 |                    0.188 |                   0.961 |                      0.742 |                     0.83  |                     0.719 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@familia)   |                  0.096 |                    -0.279 |                   -0.091 |                   -0.094 |                   0.794 |                      0.713 |                     0.737 |                     0.609 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@función)   |                  0.091 |                    -0.284 |                   -0.096 |                   -0.099 |                   0.802 |                      0.722 |                     0.746 |                     0.614 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@familia) |                  0.267 |                    -0.084 |                    0.092 |                    0.022 |                   0.873 |                      0.746 |                     0.799 |                     0.647 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@función) |                  0.282 |                    -0.07  |                    0.106 |                    0.034 |                   0.893 |                      0.756 |                     0.815 |                     0.676 |
| mix50(consenso,media12M x trend12M@función)                                 |                  0.245 |                    -0.168 |                    0.039 |                   -0.001 |                   0.86  |                      0.731 |                     0.78  |                     0.617 |
| mix50(consenso,media12M_plana)                                              |                  0.418 |                    -0.164 |                    0.127 |                    0.148 |                   0.921 |                      0.715 |                     0.788 |                     0.649 |
| mix50(consenso,media3M x 50%trend12M@familia)                               |                  0.196 |                    -0.155 |                    0.021 |                   -0.026 |                   0.813 |                      0.715 |                     0.753 |                     0.564 |
| mix50(consenso,media3M x 50%trend12M@función)                               |                  0.214 |                    -0.157 |                    0.029 |                   -0.014 |                   0.818 |                      0.714 |                     0.753 |                     0.566 |
| mix50(consenso,media3M x trend12M@función)                                  |                  0.143 |                    -0.16  |                   -0.008 |                   -0.076 |                   0.807 |                      0.726 |                     0.757 |                     0.566 |
| mix50(consenso,media3M_plana)                                               |                  0.284 |                    -0.154 |                    0.065 |                    0.049 |                   0.838 |                      0.703 |                     0.752 |                     0.575 |
| mix50(consenso,media6M x 50%trend12M@familia)                               |                  0.197 |                    -0.129 |                    0.034 |                    0.004 |                   0.789 |                      0.694 |                     0.732 |                     0.576 |
| mix50(consenso,media6M x 50%trend12M@función)                               |                  0.214 |                    -0.131 |                    0.042 |                    0.017 |                   0.793 |                      0.692 |                     0.731 |                     0.577 |
| mix50(consenso,media6M x trend12M@función)                                  |                  0.144 |                    -0.137 |                    0.004 |                   -0.051 |                   0.782 |                      0.706 |                     0.736 |                     0.574 |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@familia)              |                  0.162 |                    -0.349 |                   -0.094 |                   -0.069 |                   0.761 |                      0.673 |                     0.682 |                     0.57  |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@función)              |                  0.16  |                    -0.375 |                   -0.107 |                   -0.072 |                   0.765 |                      0.68  |                     0.686 |                     0.574 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@familia)            |                  0.361 |                    -0.014 |                    0.174 |                    0.161 |                   0.857 |                      0.706 |                     0.769 |                     0.642 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@función)            |                  0.38  |                    -0.006 |                    0.187 |                    0.183 |                   0.882 |                      0.721 |                     0.79  |                     0.679 |
| mix50(consenso,media6M_plana)                                               |                  0.285 |                    -0.125 |                    0.08  |                    0.085 |                   0.81  |                      0.68  |                     0.729 |                     0.589 |
| mix50(consenso,regla_fragancias(LY+25%cortes-50%DA) x trend12M@función)     |                  0.175 |                    -0.189 |                   -0.007 |                    0.038 |                   0.863 |                      0.755 |                     0.793 |                     0.715 |
| regla_fragancias(LY+25%cortes-50%DA) x trend12M@función                     |                 -0.038 |                    -0.224 |                   -0.131 |                   -0.013 |                   0.827 |                      0.78  |                     0.799 |                     0.809 |

## KYMU — todos — foto inicial sep-25

| tecnica                                                                     |   wmape |   bias |
|:----------------------------------------------------------------------------|--------:|-------:|
| media6M x 50%trend12M@familia                                               |   0.694 | -0.239 |
| media6M x trend12M@función                                                  |   0.696 | -0.318 |
| media6M x 50%trend12M@función                                               |   0.701 | -0.212 |
| media6M_plana                                                               |   0.716 | -0.107 |
| media6M(desest.) x estacionalidad_envíos@familia                            |   0.742 | -0.226 |
| media3M x trend12M@función                                                  |   0.749 | -0.251 |
| media3M x 50%trend12M@familia                                               |   0.749 | -0.16  |
| media3M x 50%trend12M@función                                               |   0.757 | -0.132 |
| media3M_plana                                                               |   0.779 | -0.014 |
| media6M(desest.) x estacionalidad_envíos@función                            |   0.781 | -0.193 |
| mix50(consenso,media6M x trend12M@función)                                  |   0.799 | -0.041 |
| mix50(consenso,media6M x 50%trend12M@familia)                               |   0.802 | -0.002 |
| mix50(consenso,media6M x 50%trend12M@función)                               |   0.806 |  0.011 |
| mix50(consenso,media6M_plana)                                               |   0.816 |  0.064 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@familia)            |   0.816 |  0.004 |
| mix50(consenso,media3M x trend12M@función)                                  |   0.829 | -0.008 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@función)            |   0.832 |  0.021 |
| mix50(consenso,media3M x 50%trend12M@familia)                               |   0.834 |  0.038 |
| mix50(consenso,media3M x 50%trend12M@función)                               |   0.84  |  0.051 |
| mix50(consenso,media3M_plana)                                               |   0.853 |  0.111 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@familia) |   0.875 | -0.006 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@función) |   0.877 | -0.007 |
| media12M x trend12M@función x estacionalidad_envíos@familia                 |   0.879 | -0.247 |
| mix50(consenso,LY x trend12M@familia)                                       |   0.88  | -0.046 |
| mix50(consenso,regla_fragancias(LY+25%cortes-50%DA) x trend12M@función)     |   0.882 | -0.023 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@familia)   |   0.89  | -0.012 |
| mix50(consenso,LY x trend12M@función)                                       |   0.892 | -0.019 |
| media12M x trend12M@función x estacionalidad_envíos@función                 |   0.892 | -0.249 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@función)   |   0.893 | -0.013 |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@familia)              |   0.895 |  0.157 |
| mix50(consenso,media12M x trend12M@función)                                 |   0.898 |  0.062 |
| media12M x trend12M@función                                                 |   0.898 | -0.111 |
| media6M(desest.) x estacionalidad_EPOS@familia                              |   0.909 |  0.079 |
| mix50(consenso,LY x 50%trend12M@familia)                                    |   0.912 |  0.025 |
| mix50(consenso,media12M x estacionalidad_envíos@familia)                    |   0.919 |  0.11  |
| mix50(consenso,LY x 50%trend12M@función)                                    |   0.919 |  0.039 |
| mix50(consenso,LY x trend12M@EAN)                                           |   0.925 |  0.048 |
| mix50(consenso,media12M x estacionalidad_envíos@función)                    |   0.925 |  0.108 |
| media12M x trend12M@función x estacionalidad_EPOS@familia                   |   0.926 | -0.259 |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@función)              |   0.927 |  0.167 |
| LY x trend12M@familia                                                       |   0.939 | -0.327 |
| media12M x trend12M@función x estacionalidad_EPOS@función                   |   0.939 | -0.261 |
| mix50(consenso,media12M x estacionalidad_EPOS@familia)                      |   0.941 |  0.103 |
| mix50(consenso,media12M x estacionalidad_EPOS@función)                      |   0.945 |  0.1   |
| regla_fragancias(LY+25%cortes-50%DA) x trend12M@función                     |   0.946 | -0.28  |
| mix50(consenso,LY_plano)                                                    |   0.949 |  0.096 |
| mix50(consenso,LY x 50%trend12M@product_line)                               |   0.95  |  0.07  |
| media12M x estacionalidad_envíos@familia                                    |   0.954 | -0.015 |
| mix50(consenso,media12M_plana)                                              |   0.954 |  0.199 |
| mix50(consenso,LY x trend12M@product_line)                                  |   0.956 |  0.044 |
| LY x trend12M@función                                                       |   0.958 | -0.272 |
| media6M(desest.) x estacionalidad_EPOS@función                              |   0.978 |  0.098 |
| media12M x estacionalidad_envíos@función                                    |   0.978 | -0.019 |
| LY x 50%trend12M@familia                                                    |   0.993 | -0.185 |
| LY x 50%trend12M@función                                                    |   1.006 | -0.158 |
| media12M_plana                                                              |   1.009 |  0.164 |
| LY x trend12M@EAN                                                           |   1.016 | -0.139 |
| media12M x estacionalidad_EPOS@familia                                      |   1.017 | -0.03  |
| consenso                                                                    |   1.019 |  0.235 |
| media12M x estacionalidad_EPOS@función                                      |   1.032 | -0.035 |
| LY_plano                                                                    |   1.062 | -0.043 |
| LY x 50%trend12M@product_line                                               |   1.067 | -0.095 |
| LY x trend12M@product_line                                                  |   1.083 | -0.147 |

## KYMU — todos — corrección en mar-26 (verdad hasta ago-26)

| tecnica                                                                     |   ('bias', 'congelar') |   ('bias', 'factor_100%') |   ('bias', 'factor_50%') |   ('bias', 'recalcular') |   ('wmape', 'congelar') |   ('wmape', 'factor_100%') |   ('wmape', 'factor_50%') |   ('wmape', 'recalcular') |
|:----------------------------------------------------------------------------|-----------------------:|--------------------------:|-------------------------:|-------------------------:|------------------------:|---------------------------:|--------------------------:|--------------------------:|
| LY x 50%trend12M@familia                                                    |                 -0.264 |                    -0.096 |                   -0.18  |                   -0.265 |                   0.827 |                      0.88  |                     0.851 |                     0.827 |
| LY x 50%trend12M@función                                                    |                 -0.23  |                    -0.082 |                   -0.156 |                   -0.231 |                   0.843 |                      0.893 |                     0.865 |                     0.834 |
| LY x 50%trend12M@product_line                                               |                 -0.174 |                    -0.103 |                   -0.139 |                   -0.165 |                   0.858 |                      0.885 |                     0.871 |                     0.846 |
| LY x trend12M@EAN                                                           |                 -0.199 |                    -0.077 |                   -0.138 |                   -0.207 |                   0.847 |                      0.895 |                     0.869 |                     0.84  |
| LY x trend12M@familia                                                       |                 -0.393 |                    -0.098 |                   -0.246 |                   -0.394 |                   0.804 |                      0.879 |                     0.832 |                     0.804 |
| LY x trend12M@función                                                       |                 -0.325 |                    -0.066 |                   -0.196 |                   -0.327 |                   0.831 |                      0.91  |                     0.864 |                     0.815 |
| LY x trend12M@product_line                                                  |                 -0.213 |                    -0.114 |                   -0.163 |                   -0.195 |                   0.858 |                      0.897 |                     0.876 |                     0.835 |
| LY_plano                                                                    |                 -0.135 |                    -0.094 |                   -0.114 |                   -0.135 |                   0.865 |                      0.881 |                     0.873 |                     0.865 |
| consenso                                                                    |                  0.013 |                    -0.255 |                   -0.121 |                   -0.035 |                   0.89  |                      0.792 |                     0.834 |                     0.653 |
| media12M x estacionalidad_EPOS@familia                                      |                 -0.237 |                    -0.449 |                   -0.343 |                   -0.278 |                   0.666 |                      0.67  |                     0.66  |                     0.616 |
| media12M x estacionalidad_EPOS@función                                      |                 -0.224 |                    -0.434 |                   -0.329 |                   -0.265 |                   0.664 |                      0.665 |                     0.658 |                     0.609 |
| media12M x estacionalidad_envíos@familia                                    |                  0.063 |                    -0.042 |                    0.011 |                   -0.046 |                   0.835 |                      0.794 |                     0.813 |                     0.689 |
| media12M x estacionalidad_envíos@función                                    |                  0.087 |                    -0.02  |                    0.034 |                   -0.032 |                   0.923 |                      0.87  |                     0.896 |                     0.794 |
| media12M x trend12M@función                                                 |                 -0.222 |                    -0.239 |                   -0.23  |                   -0.294 |                   0.687 |                      0.685 |                     0.686 |                     0.564 |
| media12M x trend12M@función x estacionalidad_EPOS@familia                   |                 -0.41  |                    -0.441 |                   -0.425 |                   -0.439 |                   0.665 |                      0.669 |                     0.667 |                     0.634 |
| media12M x trend12M@función x estacionalidad_EPOS@función                   |                 -0.397 |                    -0.425 |                   -0.411 |                   -0.423 |                   0.665 |                      0.669 |                     0.667 |                     0.628 |
| media12M x trend12M@función x estacionalidad_envíos@familia                 |                 -0.18  |                    -0.03  |                   -0.105 |                   -0.258 |                   0.753 |                      0.802 |                     0.775 |                     0.651 |
| media12M x trend12M@función x estacionalidad_envíos@función                 |                 -0.144 |                     0.017 |                   -0.064 |                   -0.241 |                   0.834 |                      0.906 |                     0.868 |                     0.735 |
| media12M_plana                                                              |                  0.009 |                    -0.247 |                   -0.119 |                   -0.093 |                   0.744 |                      0.684 |                     0.707 |                     0.578 |
| media3M x 50%trend12M@familia                                               |                 -0.219 |                    -0.237 |                   -0.228 |                   -0.29  |                   0.623 |                      0.622 |                     0.623 |                     0.518 |
| media3M x 50%trend12M@función                                               |                 -0.187 |                    -0.23  |                   -0.209 |                   -0.256 |                   0.626 |                      0.622 |                     0.624 |                     0.512 |
| media3M x trend12M@función                                                  |                 -0.293 |                    -0.223 |                   -0.258 |                   -0.347 |                   0.624 |                      0.627 |                     0.625 |                     0.526 |
| media3M_plana                                                               |                 -0.082 |                    -0.236 |                   -0.159 |                   -0.165 |                   0.645 |                      0.622 |                     0.63  |                     0.518 |
| media6M x 50%trend12M@familia                                               |                 -0.227 |                    -0.171 |                   -0.199 |                   -0.251 |                   0.587 |                      0.594 |                     0.59  |                     0.486 |
| media6M x 50%trend12M@función                                               |                 -0.194 |                    -0.163 |                   -0.178 |                   -0.213 |                   0.591 |                      0.596 |                     0.593 |                     0.478 |
| media6M x trend12M@función                                                  |                 -0.296 |                    -0.155 |                   -0.225 |                   -0.308 |                   0.59  |                      0.601 |                     0.592 |                     0.493 |
| media6M(desest.) x estacionalidad_EPOS@familia                              |                 -0.284 |                    -0.546 |                   -0.415 |                   -0.375 |                   0.579 |                      0.639 |                     0.595 |                     0.575 |
| media6M(desest.) x estacionalidad_EPOS@función                              |                 -0.261 |                    -0.535 |                   -0.398 |                   -0.344 |                   0.582 |                      0.638 |                     0.595 |                     0.572 |
| media6M(desest.) x estacionalidad_envíos@familia                            |                  0.003 |                     0.152 |                    0.077 |                   -0.006 |                   0.73  |                      0.801 |                     0.763 |                     0.624 |
| media6M(desest.) x estacionalidad_envíos@función                            |                  0.082 |                     0.174 |                    0.128 |                    0.053 |                   0.859 |                      0.908 |                     0.883 |                     0.777 |
| media6M_plana                                                               |                 -0.091 |                    -0.17  |                   -0.131 |                   -0.119 |                   0.61  |                      0.594 |                     0.601 |                     0.486 |
| mix50(consenso,LY x 50%trend12M@familia)                                    |                 -0.125 |                    -0.195 |                   -0.16  |                   -0.15  |                   0.782 |                      0.766 |                     0.774 |                     0.674 |
| mix50(consenso,LY x 50%trend12M@función)                                    |                 -0.108 |                    -0.189 |                   -0.149 |                   -0.133 |                   0.791 |                      0.771 |                     0.78  |                     0.679 |
| mix50(consenso,LY x 50%trend12M@product_line)                               |                 -0.08  |                    -0.194 |                   -0.137 |                   -0.1   |                   0.798 |                      0.769 |                     0.782 |                     0.683 |
| mix50(consenso,LY x trend12M@EAN)                                           |                 -0.093 |                    -0.186 |                   -0.139 |                   -0.121 |                   0.791 |                      0.768 |                     0.778 |                     0.678 |
| mix50(consenso,LY x trend12M@familia)                                       |                 -0.19  |                    -0.203 |                   -0.196 |                   -0.215 |                   0.767 |                      0.764 |                     0.765 |                     0.658 |
| mix50(consenso,LY x trend12M@función)                                       |                 -0.156 |                    -0.189 |                   -0.173 |                   -0.181 |                   0.782 |                      0.774 |                     0.778 |                     0.666 |
| mix50(consenso,LY x trend12M@product_line)                                  |                 -0.1   |                    -0.199 |                   -0.15  |                   -0.115 |                   0.796 |                      0.772 |                     0.783 |                     0.675 |
| mix50(consenso,LY_plano)                                                    |                 -0.061 |                    -0.189 |                   -0.125 |                   -0.085 |                   0.803 |                      0.768 |                     0.783 |                     0.694 |
| mix50(consenso,media12M x estacionalidad_EPOS@familia)                      |                 -0.112 |                    -0.353 |                   -0.232 |                   -0.157 |                   0.727 |                      0.69  |                     0.699 |                     0.583 |
| mix50(consenso,media12M x estacionalidad_EPOS@función)                      |                 -0.105 |                    -0.345 |                   -0.225 |                   -0.15  |                   0.725 |                      0.689 |                     0.698 |                     0.579 |
| mix50(consenso,media12M x estacionalidad_envíos@familia)                    |                  0.038 |                    -0.159 |                   -0.06  |                   -0.041 |                   0.8   |                      0.74  |                     0.764 |                     0.618 |
| mix50(consenso,media12M x estacionalidad_envíos@función)                    |                  0.05  |                    -0.149 |                   -0.05  |                   -0.033 |                   0.835 |                      0.76  |                     0.793 |                     0.663 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@familia)   |                 -0.198 |                    -0.336 |                   -0.267 |                   -0.237 |                   0.717 |                      0.701 |                     0.706 |                     0.582 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_EPOS@función)   |                 -0.192 |                    -0.329 |                   -0.261 |                   -0.229 |                   0.717 |                      0.701 |                     0.706 |                     0.58  |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@familia) |                 -0.083 |                    -0.169 |                   -0.126 |                   -0.147 |                   0.766 |                      0.743 |                     0.754 |                     0.601 |
| mix50(consenso,media12M x trend12M@función x estacionalidad_envíos@función) |                 -0.066 |                    -0.151 |                   -0.108 |                   -0.138 |                   0.796 |                      0.768 |                     0.781 |                     0.639 |
| mix50(consenso,media12M x trend12M@función)                                 |                 -0.104 |                    -0.248 |                   -0.176 |                   -0.165 |                   0.747 |                      0.718 |                     0.729 |                     0.571 |
| mix50(consenso,media12M_plana)                                              |                  0.011 |                    -0.251 |                   -0.12  |                   -0.064 |                   0.772 |                      0.71  |                     0.733 |                     0.58  |
| mix50(consenso,media3M x 50%trend12M@familia)                               |                 -0.103 |                    -0.247 |                   -0.175 |                   -0.163 |                   0.718 |                      0.691 |                     0.702 |                     0.544 |
| mix50(consenso,media3M x 50%trend12M@función)                               |                 -0.087 |                    -0.244 |                   -0.166 |                   -0.145 |                   0.72  |                      0.69  |                     0.702 |                     0.542 |
| mix50(consenso,media3M x trend12M@función)                                  |                 -0.14  |                    -0.242 |                   -0.191 |                   -0.191 |                   0.716 |                      0.698 |                     0.706 |                     0.547 |
| mix50(consenso,media3M_plana)                                               |                 -0.034 |                    -0.246 |                   -0.14  |                   -0.1   |                   0.729 |                      0.684 |                     0.7   |                     0.546 |
| mix50(consenso,media6M x 50%trend12M@familia)                               |                 -0.107 |                    -0.221 |                   -0.164 |                   -0.143 |                   0.706 |                      0.684 |                     0.694 |                     0.542 |
| mix50(consenso,media6M x 50%trend12M@función)                               |                 -0.09  |                    -0.217 |                   -0.154 |                   -0.124 |                   0.708 |                      0.682 |                     0.694 |                     0.539 |
| mix50(consenso,media6M x trend12M@función)                                  |                 -0.141 |                    -0.217 |                   -0.179 |                   -0.171 |                   0.705 |                      0.691 |                     0.698 |                     0.541 |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@familia)              |                 -0.135 |                    -0.411 |                   -0.273 |                   -0.205 |                   0.692 |                      0.67  |                     0.669 |                     0.561 |
| mix50(consenso,media6M(desest.) x estacionalidad_EPOS@función)              |                 -0.124 |                    -0.406 |                   -0.265 |                   -0.19  |                   0.693 |                      0.671 |                     0.668 |                     0.558 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@familia)            |                  0.008 |                    -0.096 |                   -0.044 |                   -0.02  |                   0.759 |                      0.723 |                     0.74  |                     0.586 |
| mix50(consenso,media6M(desest.) x estacionalidad_envíos@función)            |                  0.048 |                    -0.082 |                   -0.017 |                    0.009 |                   0.811 |                      0.76  |                     0.783 |                     0.656 |
| mix50(consenso,media6M_plana)                                               |                 -0.039 |                    -0.217 |                   -0.128 |                   -0.077 |                   0.715 |                      0.675 |                     0.691 |                     0.541 |
| mix50(consenso,regla_fragancias(LY+25%cortes-50%DA) x trend12M@función)     |                 -0.164 |                    -0.195 |                   -0.179 |                   -0.176 |                   0.776 |                      0.768 |                     0.772 |                     0.663 |
| regla_fragancias(LY+25%cortes-50%DA) x trend12M@función                     |                 -0.341 |                    -0.082 |                   -0.211 |                   -0.316 |                   0.823 |                      0.896 |                     0.853 |                     0.801 |