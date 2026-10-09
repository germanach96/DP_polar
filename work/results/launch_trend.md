# Lanzamientos en el trend (src/launch_trend.py)

| trend                       |   2025-09 |   2025-12 |   2026-03 |   2026-06 |
|:----------------------------|----------:|----------:|----------:|----------:|
| central(>=6m)_con_manuales  |    -0.181 |    -0.175 |    -0.155 |    -0.097 |
| central(>=6m)_sin_manuales  |    -0.229 |    -0.238 |    -0.217 |    -0.183 |
| solo_LFL(>=24m)             |    -0.226 |    -0.243 |    -0.206 |    -0.164 |
| todo(incl.<6m)_con_manuales |    -0.15  |    -0.151 |    -0.121 |    -0.087 |

|                                                        |   wmape |   bias_medio |   bias_abs |
|:-------------------------------------------------------|--------:|-------------:|-----------:|
| ('jóvenes(6-17m)', 0.5, 'central(>=6m)_con_manuales')  |   1.086 |        0.441 |      0.441 |
| ('jóvenes(6-17m)', 0.5, 'central(>=6m)_sin_manuales')  |   1.058 |        0.403 |      0.408 |
| ('jóvenes(6-17m)', 0.5, 'solo_LFL(>=24m)')             |   1.049 |        0.388 |      0.395 |
| ('jóvenes(6-17m)', 0.5, 'todo(incl.<6m)_con_manuales') |   1.104 |        0.47  |      0.47  |
| ('jóvenes(6-17m)', 1.0, 'central(>=6m)_con_manuales')  |   1.029 |        0.317 |      0.344 |
| ('jóvenes(6-17m)', 1.0, 'central(>=6m)_sin_manuales')  |   0.976 |        0.241 |      0.309 |
| ('jóvenes(6-17m)', 1.0, 'solo_LFL(>=24m)')             |   0.961 |        0.212 |      0.3   |
| ('jóvenes(6-17m)', 1.0, 'todo(incl.<6m)_con_manuales') |   1.064 |        0.375 |      0.381 |
| ('maduros(>=18m)', 0.5, 'central(>=6m)_con_manuales')  |   0.65  |        0.067 |      0.098 |
| ('maduros(>=18m)', 0.5, 'central(>=6m)_sin_manuales')  |   0.636 |        0.029 |      0.074 |
| ('maduros(>=18m)', 0.5, 'solo_LFL(>=24m)')             |   0.638 |        0.033 |      0.077 |
| ('maduros(>=18m)', 0.5, 'todo(incl.<6m)_con_manuales') |   0.655 |        0.08  |      0.104 |
| ('maduros(>=18m)', 1.0, 'central(>=6m)_con_manuales')  |   0.624 |       -0.022 |      0.075 |
| ('maduros(>=18m)', 1.0, 'central(>=6m)_sin_manuales')  |   0.603 |       -0.097 |      0.097 |
| ('maduros(>=18m)', 1.0, 'solo_LFL(>=24m)')             |   0.608 |       -0.088 |      0.088 |
| ('maduros(>=18m)', 1.0, 'todo(incl.<6m)_con_manuales') |   0.632 |        0.006 |      0.074 |
| ('todo_central', 0.5, 'central(>=6m)_con_manuales')    |   0.667 |        0.079 |      0.101 |
| ('todo_central', 0.5, 'central(>=6m)_sin_manuales')    |   0.652 |        0.041 |      0.077 |
| ('todo_central', 0.5, 'solo_LFL(>=24m)')               |   0.654 |        0.045 |      0.08  |
| ('todo_central', 0.5, 'todo(incl.<6m)_con_manuales')   |   0.673 |        0.094 |      0.107 |
| ('todo_central', 1.0, 'central(>=6m)_con_manuales')    |   0.64  |       -0.01  |      0.071 |
| ('todo_central', 1.0, 'central(>=6m)_sin_manuales')    |   0.617 |       -0.086 |      0.086 |
| ('todo_central', 1.0, 'solo_LFL(>=24m)')               |   0.622 |       -0.079 |      0.079 |
| ('todo_central', 1.0, 'todo(incl.<6m)_con_manuales')   |   0.649 |        0.019 |      0.07  |