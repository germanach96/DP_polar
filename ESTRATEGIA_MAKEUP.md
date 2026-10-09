# Estrategia de forecast — Makeup (decidida)

Fecha de decisión: 2026-10-09

Basada en GUMU (Gucci Make up) y KYMU (Kylie Makeup). Fotos: sep-25 (forecast inicial), mar-26 (corrección) y sep-26 (verdad), más 13 cortes mensuales (jul-25 a jul-26). Scripts: `src/mu_load.py`, `src/mu_season.py`, `src/mu_backtest.py`. Resultados: `work/results/mu_season.md` y `work/results/mu_backtest.md`.

## Regla

> **Base = media de los últimos 6 meses cerrados de (envíos + 10% de los cortes, con tope del 10% del envío de ese mes − 25% de los DAs positivos)**
>
> **Forecast EAN, cada mes futuro = Base × (1 + 50% del trend de 12 meses de su función)**

- **Función** = Face / Lips / Eyes (campo Brand) dentro de cada familia.
- **Trend** = suma de los últimos 12 meses / suma de los 12 anteriores − 1, calculado con todos los EANs Central (6 meses o más de envíos). Tope de ±30%.
- **Mismo número para todos los meses futuros.** No se aplica estacionalidad.
- **En cada foto nueva: recalcular la media de 6 meses y el trend.** No corregir con el factor real/forecast: la media móvil ya absorbe la realidad reciente, y el factor añade ruido.

## Ajuste de cortes y DAs (probado, `src/mu_cuts_da.py`, `work/results/mu_cuts_da.md`)

Base probada = media 6M de (actual + kc × cortes − kd × DAs positivos), en 13 cortes mensuales. Variantes: solo en la base, o también en el trend.

- **Cortes: no sumarlos.**
  - En makeup los cortes son enormes (FY26: 68% de los envíos en GUMU y 42% en KYMU), claramente inflados por pedidos repetidos.
  - Sumar el 25% empeora GUMU de 67% a 75% de error.
  - En KYMU mejora un poco (58% → 56%), pero sobre todo porque compensa que KYMU va por debajo al estar creciendo.
- **Cortes con tope (decisión: los cortes no se ignoran, `src/mu_cuts2.py`):** se suma el 10% de los cortes del mes, pero nunca más del 10% de lo enviado ese mes.
  - Es la forma de incluirlos que menos daña.
  - Error medio −0,1 puntos; peor caso −0,5 puntos (GUMU todos). En KYMU mejora ~1 punto.
  - Sin tope, cualquier % empeora más:

    | % de cortes sin tope | Empeora de media |
    |---|---|
    | 5% | 0,1 puntos |
    | 10% | 0,8 puntos |
    | 15% | 1,8 puntos |
    | 25% | 4,5 puntos |

  - Motivo del 10%: cuando se corta un ítem, el retailer repite el mismo pedido semana tras semana, así que los cortes cuentan la misma demanda varias veces. En makeup ese re-pedido es mucho mayor que en fragancias: los cortes están muy inflados y solo ~una décima parte es demanda perdida real.
  - El tope evita que un mes con cortes desproporcionados dispare la base.
- **DAs positivos: restar el 25% en la base.** Es la única opción que no empeora en ningún caso:

  | Variante | GUMU sin manual | GUMU todos | KYMU sin manual | KYMU todos |
  |---|---|---|---|---|
  | Sin ajuste | 66,6% | 70,9% | 57,7% | 59,8% |
  | **−25% DAs+, solo base** | **66,0%** | **68,2%** | **57,5%** | **59,7%** |
  | −50% DAs+, base y trend | 64,8% | 65,7% | 58,0% | 61,8% |

- **Óptimos por familia, por si se quiere afinar:**
  - GUMU: −50% a −100% de DAs, también en el trend (65% → 64%).
  - KYMU: +25% cortes −25% DAs (56%).

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

## Estacionalidad revisada EAN a EAN (`src/mu_season_ean.py`, `work/results/mu_season_ean.md`)

Se analizaron los EANs con FY24, FY25 y FY26 completos y al menos 50 unidades al mes de media: 113 de Gucci Make up, 139 de Kylie y 170 de fragancias como referencia.

| | Gucci Make up | Kylie Makeup | Fragancias |
|---|---|---|---|
| Parecido del perfil mensual entre años (correlación; 1 = idéntico) | 0,08 | 0,10 | 0,36 |
| % de EANs con estacionalidad real (test de permutación) | 16% | 15% | 32% |
| % del volumen con estacionalidad real | 10% | 12% | 53% |
| % de EANs donde el reparto del año pasado predice mejor que plano | 14% | 13% | 38% |
| Índice de diciembre en envíos (1 = mes medio) | 0,85 | 0,71 | 0,91 |

- **Sin estacionalidad en makeup, confirmado.**
  - Por azar ya saldría alrededor de un 5% de EANs "estacionales".
  - En 6 de cada 7 EANs, copiar el reparto del año pasado es peor que repartir plano.
- **Diciembre no es pico en los envíos:** solo 1 EAN tiene su pico en diciembre.
  - El pico de Navidad del sell-out se abastece de forma estable a lo largo del año.
  - Los picos de los envíos caen en julio–septiembre (cargas y lanzamientos) y están repartidos sin patrón.
- **Única excepción menor:** algunos Skin Tint de Kylie (bases ligeras) tienden a pico en junio. Es poco volumen y no justifica cambiar la regla.

## Notas

- **Media con el consenso:** no se recomienda de forma general. En GUMU ayuda un poco al sesgo; en KYMU empeora. El consenso de makeup es débil (75–102% de error en sep-25).
- **Desvío conocido:**
  - En GUMU, que está cayendo, la regla se queda algo alta: +9% a +16% de media.
  - En KYMU, que está creciendo, se queda baja: −18% a −22%.
  - Revisar el desvío en cada foto.
- **EANs con forecast manual:** pesan un 26% del volumen en GUMU y un 30% en KYMU. La conclusión es la misma con y sin ellos.
- **Reexpresión del histórico:** KYMU subió un 18% de sep-25 a mar-26; GUMU apenas cambió. Se trabaja con el histórico reexpresado.
