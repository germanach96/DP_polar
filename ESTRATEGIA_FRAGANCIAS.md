# Estrategia de forecast — Fragancias (decidida)

Fecha de decisión: 2026-10-09

## Regla

> **Base = mismo mes del año anterior + 25% de los supply cuts de ese mes − 50% de los DAs positivos de ese mes (año anterior)**
>
> **Forecast EAN, mes futuro = Base × (1 + trend de 12 meses de su house × tamaño)**

## Cálculo del trend, en cada foto o mes

1. **Datos:** extraer 24 meses cerrados, sin contar el mes en curso.
   - Ejemplo en sep-26: últimos 12 meses = sep-25 a ago-26; los 12 anteriores = sep-24 a ago-25.
2. **EANs que entran:** todos los **Central**, incluidos los lanzamientos que ya pasaron de Local a Central (6 meses o más de envíos) y los de forecast manual.
   - Solo se excluyen los **Local**, los que llevan menos de 6 meses de envíos.
3. **Grupo:** house × tamaño.

   | Tamaño | Criterio |
   |---|---|
   | Mini / pen spray | ≤15 ml |
   | Pequeño | 20–40 ml |
   | Medio | 45–60 ml |
   | Grande | 75–125 ml |
   | Jumbo / refill | ≥150 ml |
   | Ancilares | Desodorante, body lotion, shower gel, aceite |

4. **Trend del grupo** = suma de los últimos 12 meses / suma de los 12 anteriores − 1.
   - Es suma contra suma de todo el grupo, no una media de los % de cada EAN.
5. **Tope: ±30%.** Si sale por encima de +30% o por debajo de −30%, se corta en ±30%.
6. **Aplicación:** se calcula EAN por EAN y mes por mes, sobre el mismo mes del año anterior.
   - Es × (1 + trend), no + trend.
   - Todos los meses del grupo llevan el mismo %. La estacionalidad la da la base del año anterior.

## Sobre el grupo house × tamaño (revisado 2026-10-09)

- **El tamaño no es un campo oficial.**
  - Se lee de la descripción con `src/ptype.py`.
  - Mapeo listo para revisar y reutilizar: `MAPEO_TAMANOS_FRAGANCIAS.csv`. Hay 453 de 456 EANs con tamaño leído, que cubren el 100% del volumen.
- **Los EANs de un mismo house × tamaño NO se comportan igual.**
  - El grupo explica solo el 12–19% de las diferencias de trend entre EANs. House sola explica el 3% y la product line el 57–60%.
  - La product line no es usable para el trend: tiene grupos de 1–2 EANs y se distorsiona con los lanzamientos.
- **Los trends por grupo no se mantienen de un año a otro.**
  - El grupo que más cae un año tiende a rebotar al siguiente (correlación −0,69).
  - Por eso conviene el tope de ±30% y no extrapolar caídas fuertes.
- **El valor de house × tamaño es sobre todo estadístico:** junta suficientes EANs para que el ruido se compense y añade un poco de diferencia real por tamaño.
- **Alternativa válida si no se quiere mantener el mapeo:** trend por house. Se pierde poco en promedio (~0,4 puntos de error por quarter), algo más en un año malo.

## Ajuste por supply cuts (añadido 2026-10-09)

- **A la base** se le suma el **25%** de los cortes que tuvo ese EAN en ese mes del año anterior.
  - Motivo: no repetir un corte del año pasado como si fuera demanda.
  - El 25%, y no el 100%, porque los cortes están inflados: el retailer repite el pedido cada semana.
- **El trend se sigue calculando con las ventas reales, sin cortes.** Meterlos en el trend empeora el resultado.
- **Evidencia** (13 cortes, EANs maduros):

  | Variante | Desvío total | Desvío en meses con cortes el año anterior | Error EAN-mes | Mejor que sin ajuste en… |
  |---|---|---|---|---|
  | Sin ajuste | −6,3% | −9,9% | 62,5% | – |
  | 25% | −2,0% | +3,3% | 62,2% | 9 de 13 cortes |
  | 33% | −0,7% | +7,5% | 62,5% | 8 de 13 cortes |


## Ajuste por DAs / promociones (añadido 2026-10-09)

- **A la base** se le resta el **50% de los DAs positivos** que tuvo ese EAN en ese mes del año anterior.
  - Motivo: no repetir promos ni volúmenes puntuales del año pasado.
  - El 50%, y no el 100%, porque parte de los DAs son inputs de mercado que sí se repiten.
- **No sumar los DAs de los meses futuros.** Empeora con cualquier %: la base ya incluye el nivel normal de promos.
- **No quitar los DAs del cálculo del trend por ahora.** Solo hay DAs desde ene-25, así que la ventana anterior no tiene DAs y el trend saldría sesgado a la baja. Reevaluar con 24 meses de DAs o con el volumen real de promociones.
- **Evidencia** (11 cortes, todos los Central):

  | Variante | Error EAN-mes | Desvío |
  |---|---|---|
  | Sin ajuste | 74,8% | +9,1% |
  | −50% de DAs+ | 70,9% | −1,9% |

  En los maduros es prácticamente neutro (61,9% → 61,6%).
- **Pendiente:** cuando haya volumen exacto de promos o un histórico corregido por outliers (o9), sustituir este ajuste y comparar las tres variantes: regla actual, outliers puros e híbrido.

## Proceso mensual (decidido 2026-10-09)

- **Horizonte:** los 9 meses siguientes al mes en curso.
- **Cada mes se recalcula la regla completa** con los últimos 12 meses cerrados: base, cortes, DAs y trend. Los 9 meses se mueven con los números nuevos.
- **No se usa factor de corrección.** Al recalcular cada mes, el trend de 12 meses ya incorpora lo último que ha pasado.
- **Regla sola, recalculada cada mes** (13 cortes mensuales, EANs maduros): error EAN-mes 62,2%, desvío −2%.
- **Datos necesarios cada mes:**
  - Últimos 12 meses cerrados por EAN: actuals, actuals LY ("Consensus – Final LY M"), supply cuts y DAs.
  - House y descripción, más el mapeo de tamaños.
  - Los 9 meses del horizonte tienen su base dentro de esos 12 meses.
  - Ojo con los DAs de meses pasados: o9 no los conserva todos en cada extracción, así que conviene guardarlos mes a mes.

## Por qué 9 meses: la regla gana en cada mes del horizonte (`src/horizon9.py`)

Regla recalculada cada mes, 13 cortes mensuales (jul-25 a jul-26), EANs Central sin forecast manual. Error por EAN y mes:

| Mes del horizonte | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| **Regla** | **75%** | **71%** | **74%** | **72%** | **71%** | **70%** | **66%** | **63%** | **64%** |
| Año pasado tal cual | 83% | 79% | 85% | 86% | 86% | 86% | 75% | 69% | 72% |
| Método actual (trend 6M EAN) | 83% | 83% | 89% | 89% | 87% | 94% | 82% | 81% | 81% |

- **Mejor que las dos alternativas en los 9 meses.**
- **El error no crece con el horizonte:** el mes 9 es tan fiable como el mes 1, porque la base es el mismo mes del año anterior y el trend es de 12 meses.
- **Desvío total de los 9 meses: 0%.** El año pasado tal cual se pasa un +23% y el método actual un +12%.
