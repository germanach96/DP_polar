# DA positivos (src/da_test.py)


## 11 cortes mensuales (sep-25..jul-26)

|                                                      |   WMAPE |   bias |   WMAPE_EAN-mes_con_DA |   bias_con_DA |   gana_a_k0 |   n_cortes |
|:-----------------------------------------------------|--------:|-------:|-----------------------:|--------------:|------------:|-----------:|
| ('central', 'base y futuro (DA+)', 0.0)              |   0.748 |  0.091 |                  0.86  |         0.211 |           0 |         11 |
| ('central', 'base y futuro (DA+)', 0.25)             |   0.729 |  0.078 |                  0.819 |         0.183 |           9 |         11 |
| ('central', 'base y futuro (DA+)', 0.5)              |   0.725 |  0.075 |                  0.81  |         0.177 |           9 |         11 |
| ('central', 'base y futuro (DA+)', 0.75)             |   0.735 |  0.082 |                  0.831 |         0.192 |           9 |         11 |
| ('central', 'base y futuro (DA+)', 1.0)              |   0.761 |  0.105 |                  0.887 |         0.242 |           4 |         11 |
| ('central', 'base: restar DA+ LY', 0.0)              |   0.748 |  0.091 |                  0.86  |         0.211 |           0 |         11 |
| ('central', 'base: restar DA+ LY', 0.25)             |   0.727 |  0.031 |                  0.813 |         0.08  |           9 |         11 |
| ('central', 'base: restar DA+ LY', 0.5)              |   0.709 | -0.019 |                  0.775 |        -0.029 |           9 |         11 |
| ('central', 'base: restar DA+ LY', 0.75)             |   0.704 | -0.059 |                  0.764 |        -0.117 |           9 |         11 |
| ('central', 'base: restar DA+ LY', 1.0)              |   0.711 | -0.084 |                  0.779 |        -0.17  |           8 |         11 |
| ('central', 'futuro: sumar DA (+ y -)', 0.0)         |   0.748 |  0.091 |                  0.86  |         0.211 |           0 |         11 |
| ('central', 'futuro: sumar DA (+ y -)', 0.25)        |   0.757 |  0.113 |                  0.876 |         0.302 |           2 |         11 |
| ('central', 'futuro: sumar DA (+ y -)', 0.5)         |   0.78  |  0.137 |                  0.92  |         0.393 |           0 |         11 |
| ('central', 'futuro: sumar DA (+ y -)', 0.75)        |   0.812 |  0.164 |                  0.978 |         0.486 |           0 |         11 |
| ('central', 'futuro: sumar DA (+ y -)', 1.0)         |   0.851 |  0.194 |                  1.052 |         0.58  |           0 |         11 |
| ('central', 'futuro: sumar DA+', 0.0)                |   0.748 |  0.091 |                  0.86  |         0.211 |           0 |         11 |
| ('central', 'futuro: sumar DA+', 0.25)               |   0.755 |  0.138 |                  0.875 |         0.314 |           1 |         11 |
| ('central', 'futuro: sumar DA+', 0.5)                |   0.774 |  0.185 |                  0.917 |         0.417 |           0 |         11 |
| ('central', 'futuro: sumar DA+', 0.75)               |   0.8   |  0.233 |                  0.974 |         0.52  |           0 |         11 |
| ('central', 'futuro: sumar DA+', 1.0)                |   0.833 |  0.28  |                  1.045 |         0.624 |           0 |         11 |
| ('central', 'trend: quitar DA+ del histórico', 0.0)  |   0.748 |  0.091 |                  0.86  |         0.211 |           0 |         11 |
| ('central', 'trend: quitar DA+ del histórico', 0.25) |   0.728 |  0.041 |                  0.832 |         0.156 |          11 |         11 |
| ('central', 'trend: quitar DA+ del histórico', 0.5)  |   0.714 |  0.005 |                  0.811 |         0.117 |          11 |         11 |
| ('central', 'trend: quitar DA+ del histórico', 0.75) |   0.705 | -0.02  |                  0.797 |         0.091 |          11 |         11 |
| ('central', 'trend: quitar DA+ del histórico', 1.0)  |   0.7   | -0.035 |                  0.789 |         0.075 |          11 |         11 |
| ('maduros', 'base y futuro (DA+)', 0.0)              |   0.619 | -0.016 |                  0.591 |         0.003 |           0 |         11 |
| ('maduros', 'base y futuro (DA+)', 0.25)             |   0.62  | -0.012 |                  0.593 |         0.013 |           5 |         11 |
| ('maduros', 'base y futuro (DA+)', 0.5)              |   0.628 | -0.006 |                  0.614 |         0.03  |           4 |         11 |
| ('maduros', 'base y futuro (DA+)', 0.75)             |   0.641 |  0.003 |                  0.648 |         0.051 |           2 |         11 |
| ('maduros', 'base y futuro (DA+)', 1.0)              |   0.661 |  0.016 |                  0.698 |         0.084 |           1 |         11 |
| ('maduros', 'base: restar DA+ LY', 0.0)              |   0.619 | -0.016 |                  0.591 |         0.003 |           0 |         11 |
| ('maduros', 'base: restar DA+ LY', 0.25)             |   0.616 | -0.038 |                  0.583 |        -0.052 |           7 |         11 |
| ('maduros', 'base: restar DA+ LY', 0.5)              |   0.616 | -0.057 |                  0.584 |        -0.1   |           6 |         11 |
| ('maduros', 'base: restar DA+ LY', 0.75)             |   0.62  | -0.074 |                  0.593 |        -0.143 |           6 |         11 |
| ('maduros', 'base: restar DA+ LY', 1.0)              |   0.626 | -0.087 |                  0.61  |        -0.176 |           4 |         11 |
| ('maduros', 'futuro: sumar DA (+ y -)', 0.0)         |   0.619 | -0.016 |                  0.591 |         0.003 |           0 |         11 |
| ('maduros', 'futuro: sumar DA (+ y -)', 0.25)        |   0.625 | -0.019 |                  0.603 |         0.052 |           4 |         11 |
| ('maduros', 'futuro: sumar DA (+ y -)', 0.5)         |   0.639 | -0.019 |                  0.626 |         0.103 |           3 |         11 |
| ('maduros', 'futuro: sumar DA (+ y -)', 0.75)        |   0.656 | -0.015 |                  0.656 |         0.155 |           2 |         11 |
| ('maduros', 'futuro: sumar DA (+ y -)', 1.0)         |   0.679 | -0.009 |                  0.698 |         0.208 |           2 |         11 |
| ('maduros', 'futuro: sumar DA+', 0.0)                |   0.619 | -0.016 |                  0.591 |         0.003 |           0 |         11 |
| ('maduros', 'futuro: sumar DA+', 0.25)               |   0.623 |  0.01  |                  0.602 |         0.068 |           2 |         11 |
| ('maduros', 'futuro: sumar DA+', 0.5)                |   0.632 |  0.035 |                  0.623 |         0.133 |           2 |         11 |
| ('maduros', 'futuro: sumar DA+', 0.75)               |   0.643 |  0.061 |                  0.651 |         0.198 |           2 |         11 |
| ('maduros', 'futuro: sumar DA+', 1.0)                |   0.658 |  0.087 |                  0.689 |         0.263 |           2 |         11 |
| ('maduros', 'trend: quitar DA+ del histórico', 0.0)  |   0.619 | -0.016 |                  0.591 |         0.003 |           0 |         11 |
| ('maduros', 'trend: quitar DA+ del histórico', 0.25) |   0.606 | -0.061 |                  0.578 |        -0.041 |          11 |         11 |
| ('maduros', 'trend: quitar DA+ del histórico', 0.5)  |   0.598 | -0.093 |                  0.568 |        -0.071 |          11 |         11 |
| ('maduros', 'trend: quitar DA+ del histórico', 0.75) |   0.593 | -0.114 |                  0.562 |        -0.092 |          11 |         11 |
| ('maduros', 'trend: quitar DA+ del histórico', 1.0)  |   0.591 | -0.128 |                  0.558 |        -0.104 |          11 |         11 |

## solo las 4 fotos S&OP

|                                                      |   WMAPE |   bias |   WMAPE_EAN-mes_con_DA |   bias_con_DA |   gana_a_k0 |   n_cortes |
|:-----------------------------------------------------|--------:|-------:|-----------------------:|--------------:|------------:|-----------:|
| ('central', 'base y futuro (DA+)', 0.0)              |   0.75  |  0.087 |                  0.874 |         0.204 |           0 |          4 |
| ('central', 'base y futuro (DA+)', 0.25)             |   0.737 |  0.086 |                  0.842 |         0.2   |           3 |          4 |
| ('central', 'base y futuro (DA+)', 0.5)              |   0.735 |  0.091 |                  0.838 |         0.214 |           3 |          4 |
| ('central', 'base y futuro (DA+)', 0.75)             |   0.744 |  0.105 |                  0.86  |         0.246 |           3 |          4 |
| ('central', 'base y futuro (DA+)', 1.0)              |   0.767 |  0.129 |                  0.914 |         0.305 |           1 |          4 |
| ('central', 'base: restar DA+ LY', 0.0)              |   0.75  |  0.087 |                  0.874 |         0.204 |           0 |          4 |
| ('central', 'base: restar DA+ LY', 0.25)             |   0.735 |  0.042 |                  0.838 |         0.096 |           3 |          4 |
| ('central', 'base: restar DA+ LY', 0.5)              |   0.723 |  0.004 |                  0.808 |         0.005 |           3 |          4 |
| ('central', 'base: restar DA+ LY', 0.75)             |   0.718 | -0.026 |                  0.798 |        -0.067 |           3 |          4 |
| ('central', 'base: restar DA+ LY', 1.0)              |   0.724 | -0.045 |                  0.81  |        -0.113 |           3 |          4 |
| ('central', 'futuro: sumar DA (+ y -)', 0.0)         |   0.75  |  0.087 |                  0.874 |         0.204 |           0 |          4 |
| ('central', 'futuro: sumar DA (+ y -)', 0.25)        |   0.755 |  0.102 |                  0.886 |         0.296 |           2 |          4 |
| ('central', 'futuro: sumar DA (+ y -)', 0.5)         |   0.775 |  0.12  |                  0.926 |         0.389 |           0 |          4 |
| ('central', 'futuro: sumar DA (+ y -)', 0.75)        |   0.802 |  0.141 |                  0.98  |         0.484 |           0 |          4 |
| ('central', 'futuro: sumar DA (+ y -)', 1.0)         |   0.837 |  0.165 |                  1.052 |         0.579 |           0 |          4 |
| ('central', 'futuro: sumar DA+', 0.0)                |   0.75  |  0.087 |                  0.874 |         0.204 |           0 |          4 |
| ('central', 'futuro: sumar DA+', 0.25)               |   0.755 |  0.131 |                  0.885 |         0.308 |           1 |          4 |
| ('central', 'futuro: sumar DA+', 0.5)                |   0.771 |  0.174 |                  0.923 |         0.412 |           0 |          4 |
| ('central', 'futuro: sumar DA+', 0.75)               |   0.793 |  0.218 |                  0.976 |         0.517 |           0 |          4 |
| ('central', 'futuro: sumar DA+', 1.0)                |   0.821 |  0.261 |                  1.044 |         0.621 |           0 |          4 |
| ('central', 'trend: quitar DA+ del histórico', 0.0)  |   0.75  |  0.087 |                  0.874 |         0.204 |           0 |          4 |
| ('central', 'trend: quitar DA+ del histórico', 0.25) |   0.733 |  0.043 |                  0.85  |         0.155 |           4 |          4 |
| ('central', 'trend: quitar DA+ del histórico', 0.5)  |   0.72  |  0.013 |                  0.831 |         0.122 |           4 |          4 |
| ('central', 'trend: quitar DA+ del histórico', 0.75) |   0.713 | -0.01  |                  0.818 |         0.098 |           4 |          4 |
| ('central', 'trend: quitar DA+ del histórico', 1.0)  |   0.708 | -0.024 |                  0.811 |         0.083 |           4 |          4 |
| ('maduros', 'base y futuro (DA+)', 0.0)              |   0.631 | -0.013 |                  0.611 |        -0.01  |           0 |          4 |
| ('maduros', 'base y futuro (DA+)', 0.25)             |   0.631 | -0.003 |                  0.61  |         0.017 |           2 |          4 |
| ('maduros', 'base y futuro (DA+)', 0.5)              |   0.638 |  0.009 |                  0.628 |         0.05  |           2 |          4 |
| ('maduros', 'base y futuro (DA+)', 0.75)             |   0.649 |  0.022 |                  0.66  |         0.085 |           1 |          4 |
| ('maduros', 'base y futuro (DA+)', 1.0)              |   0.667 |  0.037 |                  0.709 |         0.129 |           0 |          4 |
| ('maduros', 'base: restar DA+ LY', 0.0)              |   0.631 | -0.013 |                  0.611 |        -0.01  |           0 |          4 |
| ('maduros', 'base: restar DA+ LY', 0.25)             |   0.629 | -0.028 |                  0.604 |        -0.054 |           2 |          4 |
| ('maduros', 'base: restar DA+ LY', 0.5)              |   0.629 | -0.042 |                  0.605 |        -0.092 |           2 |          4 |
| ('maduros', 'base: restar DA+ LY', 0.75)             |   0.632 | -0.055 |                  0.612 |        -0.127 |           2 |          4 |
| ('maduros', 'base: restar DA+ LY', 1.0)              |   0.637 | -0.065 |                  0.627 |        -0.154 |           1 |          4 |
| ('maduros', 'futuro: sumar DA (+ y -)', 0.0)         |   0.631 | -0.013 |                  0.611 |        -0.01  |           0 |          4 |
| ('maduros', 'futuro: sumar DA (+ y -)', 0.25)        |   0.634 | -0.018 |                  0.619 |         0.046 |           2 |          4 |
| ('maduros', 'futuro: sumar DA (+ y -)', 0.5)         |   0.645 | -0.021 |                  0.638 |         0.104 |           2 |          4 |
| ('maduros', 'futuro: sumar DA (+ y -)', 0.75)        |   0.661 | -0.02  |                  0.667 |         0.163 |           1 |          4 |
| ('maduros', 'futuro: sumar DA (+ y -)', 1.0)         |   0.683 | -0.016 |                  0.711 |         0.222 |           1 |          4 |
| ('maduros', 'futuro: sumar DA+', 0.0)                |   0.631 | -0.013 |                  0.611 |        -0.01  |           0 |          4 |
| ('maduros', 'futuro: sumar DA+', 0.25)               |   0.634 |  0.013 |                  0.617 |         0.061 |           1 |          4 |
| ('maduros', 'futuro: sumar DA+', 0.5)                |   0.64  |  0.038 |                  0.635 |         0.132 |           1 |          4 |
| ('maduros', 'futuro: sumar DA+', 0.75)               |   0.65  |  0.064 |                  0.662 |         0.203 |           1 |          4 |
| ('maduros', 'futuro: sumar DA+', 1.0)                |   0.664 |  0.09  |                  0.702 |         0.273 |           1 |          4 |
| ('maduros', 'trend: quitar DA+ del histórico', 0.0)  |   0.631 | -0.013 |                  0.611 |        -0.01  |           0 |          4 |
| ('maduros', 'trend: quitar DA+ del histórico', 0.25) |   0.62  | -0.053 |                  0.598 |        -0.05  |           4 |          4 |
| ('maduros', 'trend: quitar DA+ del histórico', 0.5)  |   0.612 | -0.08  |                  0.589 |        -0.075 |           4 |          4 |
| ('maduros', 'trend: quitar DA+ del histórico', 0.75) |   0.607 | -0.1   |                  0.583 |        -0.094 |           4 |          4 |
| ('maduros', 'trend: quitar DA+ del histórico', 1.0)  |   0.605 | -0.113 |                  0.58  |        -0.105 |           4 |          4 |