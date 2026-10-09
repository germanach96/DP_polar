# Estrategia de forecast — Fragancias (decidida)

Fecha de decisión: 2026-10-09

## Regla

> **Forecast EAN, mes futuro = (mismo mes del año anterior + 25% de los supply cuts de ese mes del año anterior) × (1 + trend de su house × tamaño)**

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

- Dentro del proceso completo (media con consenso y factor) el efecto es neutro. Aporta sobre todo cuando se usa la regla sola.

## Complementos validados en el backtest por fotos (sep-25 → sep-26)

- **Número final** = media entre esta regla y el consenso.
- **En cada foto nueva:**
  - factor = real / forecast de los meses cerrados desde la foto anterior, calculado sobre el total;
  - se multiplica todo el forecast restante por ese factor;
  - los meses nuevos del horizonte se calculan con la regla y también se multiplican por el factor.
- **Resultado de la cadena completa:** error EAN-mes 62,6%; desvío del total +2%, +9%, −7% y +5% en las 4 fotos.

## Excepciones

- **Local (menos de 6 meses de envíos):** no se aplica la regla; se usa el consenso.
- **EANs de 6 a 17 meses de vida:** su año anterior incluye el llenado de canal y la regla los infla entre un 20% y un 47%. Apoyarse más en el consenso. Pendiente: definir una regla de ritmo de venta para ellos.
- **Makeup:** no aplica esta regla. Ver `work/STRATEGY.md`: media de los últimos 12 meses del EAN, plana.

## Qué no hacer

- Trend de 3 o 6 meses, o YTD: se van con los baches de supply.
- Trend EAN a EAN o por product line.
- Ajustar el nivel con los últimos 3 meses si hubo cortes.

Evidencia y scripts: `src/snapshots.py`, `src/tracking.py`, `src/launch_trend.py`, `work/results/` y `work/STRATEGY.md`.
