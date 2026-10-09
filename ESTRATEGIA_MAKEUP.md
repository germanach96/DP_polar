# Estrategia de forecast — Makeup (propuesta, pendiente de decisión)

Basada en GUMU (Gucci Make up) y KYMU (Kylie Makeup). Fotos: sep-25 (forecast inicial), mar-26 (corrección) y sep-26 (verdad), más 13 cortes mensuales (jul-25 a jul-26). Scripts: `src/mu_load.py`, `src/mu_season.py`, `src/mu_backtest.py`. Resultados: `work/results/mu_season.md` y `work/results/mu_backtest.md`.

## Regla

> **Forecast EAN, cada mes futuro = media de envíos de los últimos 6 meses cerrados × (1 + 50% del trend de 12 meses de su función)**

- **Función** = Face / Lips / Eyes (campo Brand) dentro de cada familia.
- **Trend** = suma de los últimos 12 meses / suma de los 12 anteriores − 1, calculado con todos los EANs Central (6 meses o más de envíos). Tope de ±30%.
- **Mismo número para todos los meses futuros.** No se aplica estacionalidad.
- **En cada foto nueva: recalcular la media de 6 meses y el trend.** No corregir con el factor real/forecast: la media móvil ya absorbe la realidad reciente, y el factor añade ruido.

## Por qué, y no la regla de fragancias

- **Estacionalidad:**
  - El sell-out (EPOS) sí tiene un patrón claro y estable: pico en diciembre (+50–70%), valle en enero, correlación entre años de ~0,8.
  - Los envíos no lo repiten: correlación entre años de 0,06 en KYMU y 0,39 en GUMU. Los mueven los lanzamientos, el llenado de canal y los pedidos.
  - Aplicar el patrón del EPOS o el de los envíos a la media empeora el resultado.
- **Mismo mes del año pasado:** es puro ruido en makeup. El año pasado tal cual tiene un 89–108% de error, y la regla de fragancias un 80–100%.

**Error EAN-mes (sin forecast manual / todos los Central):**

| Técnica | GUMU, 13 cortes | KYMU, 13 cortes | GUMU, foto sep-25 | KYMU, foto sep-25 | GUMU, mar-26 recalculado | KYMU, mar-26 recalculado |
|---|---|---|---|---|---|---|
| **Media 6M × (1 + 50% trend función)** | **67% / 71%** | **58% / 60%** | **63% / 65%** | **66% / 70%** | **65% / 71%** | **46% / 48%** |
| Media 6M plana | 70% / 74% | 60% / 61% | 66% / 68% | 66% / 72% | 69% / 73% | 49% / 49% |
| Año pasado tal cual | 95% / 108% | 89% / 101% | 91% / 99% | 84% / 106% | 98% / 119% | 94% / 87% |
| Regla de fragancias | 82–100% | 80–90% | – | – | 101–116% | 80–81% |
| Consenso | – | – | 75% / 77% | 87% / 102% | 70% / 70% | 78% / 65% |

## Notas

- **Media con el consenso:** no se recomienda de forma general. En GUMU ayuda un poco al sesgo; en KYMU empeora. El consenso de makeup es débil (75–102% de error en sep-25).
- **Desvío conocido:**
  - En GUMU, que está cayendo, la regla se queda algo alta: +9% a +16% de media.
  - En KYMU, que está creciendo, se queda baja: −18% a −22%.
  - Revisar el desvío en cada foto.
- **EANs con forecast manual:** pesan un 26% del volumen en GUMU y un 30% en KYMU. La conclusión es la misma con y sin ellos.
- **Reexpresión del histórico:** KYMU subió un 18% de sep-25 a mar-26; GUMU apenas cambió. Se trabaja con el histórico reexpresado.
