# Historial de resultados (leer solo cuando haga falta)

Resultados de todas las pruebas hasta 2026-10-10. El contexto vigente está en `CLAUDE.md`.

## 1. Encargo original del usuario (brief inicial)
- Comparar sobre los mismos datos y horizonte:
  - Naïve estacional (año pasado).
  - Trend plano actual del equipo: YoY 6M (suma/suma − 1) plano.
  - Trend mediana y media recortada de los ratios YoY 6M.
  - Trend 3M y 12M.
  - Histórico limpio de outliers (desviación >40% de la mediana móvil) + trend.
  - ETS damped.
  - Agregado familia → SKU.
- Backtest rolling origin a 9 meses.
  - WMAPE a nivel EAN, bias, desglose por lag y quarter, segmentos ABC.
  - Marcar meses con roturas.
- Banda de tolerancia P10–P90 del error relativo por lag.
- Efecto base por quarter.
- Entregables:
  - Excel (ranking, forecast con banda, comparación contra el trend plano, efecto base, outliers).
  - Resumen de 1 página.
  - Scripts reutilizables.
- Resultado: se descartaron los métodos opacos (ETS no aporta) y se decidieron las reglas simples de `ESTRATEGIA_FRAGANCIAS.md` y `ESTRATEGIA_MAKEUP.md`.
- Detalle de esa fase: `work/STRATEGY.md`, `work/NOTES.md`, `work/results/*.md`.

## 2. Evidencia de las reglas decididas
- **Horizonte de 9 meses** (`src/horizon9.py`; 13 cortes mensuales jul-25 a jul-26; EANs Central sin forecast manual). Error EAN-mes:

  | Mes del horizonte | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
  |---|---|---|---|---|---|---|---|---|---|
  | Regla fragancias | 75% | 71% | 74% | 72% | 71% | 70% | 66% | 63% | 64% |
  | Año pasado | 83% | 79% | 85% | 86% | 86% | 86% | 75% | 69% | 72% |
  | Método actual (trend 6M EAN) | 83% | 83% | 89% | 89% | 87% | 94% | 82% | 81% | 81% |

  - Desvío total de los 9 meses: regla 0%, año pasado +23%, método actual +12%.
- **Cortes (fragancias, 25%):**
  - Desvío −6,3% → −2,0%; error EAN-mes 62,5% → 62,2%.
  - Mejora en 9 de 13 cortes.
  - Meter los cortes en el trend empeora.
- **DAs (fragancias, −50% de los DAs+ del año pasado):** error EAN-mes 74,8% → 70,9%; desvío +9,1% → −1,9%. Sumar los DAs de meses futuros a la regla empeoraba en EAN-mes.
- **Makeup:** sin estacionalidad en envíos, revisado también por EAN (el EPOS sí la tiene). Cortes al 10% con tope del 10% del envío, por los re-pedidos.
- **Tamaño (fragancias):**
  - No es un campo oficial: se lee de la descripción con `src/ptype.py`; el mapeo está en `MAPEO_TAMANOS_FRAGANCIAS.csv`.
  - Casa × tamaño explica el 12–19% de las diferencias de trend; la product line, el 57–60%, pero tiene grupos de 1–2 EANs.
  - Los trends por grupo rebotan de un año a otro (correlación −0,69), de ahí el tope de ±30%.
- **Consenso de fotos viejas:** usado tal cual. El ajuste por factor de reexpresión era erróneo: con el consenso sin ajustar, sep-25 quedaba entre −4% y +6% del real por casa.

## 3. Consenso vs regla
- **Reportes por casa** (`src/house_compare.py`):
  - En makeup, la regla gana EAN a EAN en las dos casas y las dos fotos.
  - En fragancias, la regla pierde contra el consenso EAN a EAN; falla en los EANs de 6–17 meses y en los de forecast manual.
  - Híbrido (regla solo en maduros) gana al consenso en mar-26 en las 3 casas de fragancias.
- **WAPE90 / SPP3, regla + DAs de la foto vs consenso tal cual** (`src/wape90.py`; sep-25 Q2–Q4 + mar-26 Q4, Q1 FY27 jul–ago):
  - Regla + DAs gana 15/25 casa × quarter (fragancias 10/15, makeup 5/10).
  - WAPE90 ponderado: consenso 13%, regla + DAs 11,5%, regla sola 18%.
  - Por foto (consenso / regla + DAs):

    | Casa | sep-25 | mar-26 |
    |---|---|---|
    | Burberry | 18 / 4 | 7 / 3 |
    | Gucci | 8 / 6 | 22 / 25 |
    | Marc Jacobs | 19 / 24 | 29 / 15 |
    | Gucci Make up | 8 / 18 | 26 / 32 |
    | Kylie | 7 / 7 | 8 / 16 |

  - El consenso hace overforecast a menudo: Burberry sep-25 Q4 −32%, Marc Jacobs −30% y −41%, Gucci jul–ago −35%.
- **Quitar los DAs al consenso lo empeora:** WAPE90 13% → 23%. Los DAs de la foto sí se convierten en envíos en el agregado.
- **Votación por EAN, consenso vs regla + DAs** (`src/votes.py`, `reportes/REPORTE_VOTACION.pdf`):
  - Consenso 530 EANs, regla + DAs 391, empates 37. Volumen: 47% contra 51%.
  - Jóvenes (<18 meses) y con bandera → consenso.
  - Maduros → 333 contra 361 EANs, pero 62% del volumen para la regla + DAs.
  - EANs A → regla + DAs; cola C → consenso.

## 4. Parlamentos de reglas (formato de elecciones previo, con fallos de planteamiento)
- **Varios partidos con consenso** (`src/multivote.py`; elección con sep-25 Q2+Q3, prueba con mar-26 Q4+Q1):
  - 5 partidos: WAPE90 14,7% contra 14,3% del consenso. La media 6M gana en oct–mar y duplica en abr–jun.
  - 2 partidos (consenso / regla + DAs): 11,3% contra 14,3%, pero el ganador repite solo el 53% (al azar sería 50%).
- **Regla fragancias vs regla makeup, aplicadas a todos** (`src/rulevote.py`, `reportes/REPORTE_VOTACION_REGLAS.pdf`):
  - Makeup 593 EANs, fragancias 380; volumen 51% contra 49%.
  - Cada categoría gana en volumen con su propia regla: fragancias 54%, makeup 61%.
  - La regla de fragancias solo se impone en abr–jun; la media plana falla un 63–75% en Burberry abr–jun.
- **Parlamento de 6 reglas, todas + DAs** (`src/parliament.py`, `reportes/REPORTE_PARLAMENTO.pdf`):
  - Escaños: Media 3M 374 (38%), Regla makeup 193, Media 6M estacional 101, Año pasado 85, Regla fragancias 85, Año pasado × línea 79, Empate 60.
  - Volumen: Regla makeup 23%, Media 3M 21%.
  - Desvío total / WAPE90:

    | Partido | Desvío total | WAPE90 |
    |---|---|---|
    | Regla fragancias | +6% | 14% |
    | Año pasado × línea | +12% | 16% |
    | Regla makeup | +13% | 19% |
    | Media 3M | +27% | 30% |
    | Media 6M estacional | +29% | 31% |
    | Año pasado | +30% | 31% |

  - Casa × quarter: Regla fragancias y Año pasado × línea ganan 7/25 cada una.
- **Por qué ganó Media 3M:**
  - El negocio cae frente al año pasado (fragancias ~−20%) y los partidos sin trend no lo recogen.
  - Voto dividido entre 3 partidos de "año pasado".
  - Cada EAN pequeño cuenta igual.
  - No es por el lag: su cuota de victorias es 24% en el quarter inmediato, 29% en el medio y 28% en el lejano.
- **Parlamento + DAs vs consenso** (`src/parliament_vs_cons.py`; elección con sep-25 Q2+Q3, prueba con mar-26):

  | Sistema | WAPE90 | Error EAN |
  |---|---|---|
  | Consenso | 14,3% | 48,6% |
  | Parlamento (cada EAN su partido) | 28,5% | 66,8% |
  | Techo: elección a posteriori | 15,3% | 49,2% |

  - El partido elegido es el mejor en la prueba solo el 20% de las veces (al azar sería 17%).
- **Variantes de selección** (misma elección y prueba; WAPE90 / error EAN):

  | Variante | WAPE90 | Error EAN |
  |---|---|---|
  | Regla fija de su categoría | 15,1% | 60,5% |
  | Regla fragancias para todos | 13,8% | 65,0% |
  | Elección por grupo | 25,1% | 61,5% |
  | Elección por casa | 25,6% | 62,9% |
  | Elección por EAN, solo partidos con trend | 23,3% | 65,3% |
  | Media de los 2 mejores del EAN | 26,7% | 62,9% |
  | Media de los 3 con trend, sin elegir | 17,3% | 59,3% |

  - Causa: se eligió solo con oct–mar (temporada alta) y se aplicó en abr–jun.
  - Con datos desde jul-23 y trend de 12M, el primer año completo de competición se cierra en jul-26.

## 5. DAs: impacto medido (parlamento de 6, con y sin los DAs de la foto)

| Partido | Desvío con / sin DAs | WAPE90 con / sin | Error EAN con / sin |
|---|---|---|---|
| Regla fragancias | +6% / −10% | 14% / 21% | 67% / 61% |
| Año pasado × línea | +12% / −5% | 16% / 18% | 73% / 65% |
| Regla makeup | +13% / −2% | 19% / 23% | 61% / 51% |
| Media 3M | +27% / +12% | 30% / 21% | 69% / 56% |
| Año pasado | +30% / +14% | 31% / 23% | 76% / 68% |
| Media 6M estacional | +29% / +14% | 31% / 23% | 65% / 54% |

- Los DAs suben el forecast unos 16 puntos.
- En el total ayudan solo a quien se queda corto (las reglas con trend). EAN a EAN empeoran a todos.
- La foto sep-26 solo conserva DAs desde ene-26: o9 borra los viejos.
- Propuesta pendiente:
  - Base limpia de DAs del pasado + DAs de la foto para todos.
  - Medir la precisión de los DAs.
  - Guardar los DAs de cada foto.

## 6. Consejo dado al usuario
- El consenso es el trabajo del departamento: no es el rival.
- El usuario busca una regla base defendible (como el best-fit de o9, pero comparando también con casa, línea, tamaño y función).
- Hoy la regla fija de cada categoría es la referencia más sólida.
- El motor de selección necesita un año completo de competición y partidos bien planteados: es el trabajo en curso con el nuevo formato de elecciones.

## 7. Ideologías por EAN y propuesta de 10 partidos (foto sep-25 → real sep-26, «con trampa»)
- Scripts: `src/ideo_panel.py` → `src/ideo_engine.py` → `src/ideo_parties.py` → `src/ideo_compass.py`; reportes `src/ideo_report.py` (`reportes/REPORTE_IDEOLOGIAS.pdf`) e `src/ideo_infografia.py` (`reportes/INFOGRAFIA_IDEOLOGIAS.pdf`); detalle por EAN en `reportes/IDEOLOGIAS_EAN.xlsx`.
- Banco: 203.160 estrategias por EAN (base, temporada, fuente/ventana/fuerza/tope del trend, DAs pasado, cortes, DAs foto); reproduce exactamente las dos reglas.
- 850 votantes (777 con real oct–jun). Edad: lanzamiento = primer mes de 2 seguidos con envío; tramos 6–11 / 12–17 / 18–25 / 26+. Fase (18+ meses): trend 6M propio vs su casa ±15%.
- Qué importa en la mejor estrategia de cada EAN: base 94% (fragancias) / 91% (makeup); trend 78% / 82%; DAs pasado 46% / 32%; cortes 35% / 22%; DAs foto 36% / 60%. En makeup el 59% del volumen acierta más sin DAs de la foto.
- En sep-25 los trends de grupo se amontonan entre −20% y −30% por el tope (6M: casa en el suelo para el 100% de fragancias): la fuente del trend no se puede juzgar bien con esta foto.
- 8 partidos nuevos, uno por forma de base (sale la media 12M plana). Error del parlamento 65% → 36% (libre 35%, techo 25%). Mitades de EANs: 65% → 39% fuera de muestra; formas estables, detalle no.
- Elección: Media 3M · categoría 189 EANs (5% vol); Media 3M estacional · fase 20% del volumen; ninguno pasa del 22% de los EANs.
- Prueba limpia (partidos y elección con oct–mar, medida abr–jun): error EAN 51% vs reglas 71% vs consenso 73% (fragancias 49% = regla; makeup 53% vs 100%). En el total de casa no siempre: Burberry 31% vs regla 4%.
- La regla de makeup falla 100% EAN a EAN en abr–jun por los DAs de la foto (sin ellos, 69%).
- WAPE90 como regla única: consenso 12,2%; Media 12M estacional · casa 12,2%; regla fragancias 13,7%.

## 8. Parlamento de 6 y lógica de DAs reconstruida (vigente)
- Scripts: `src/da_conversion.py`, `src/ideo_brujulas6.py`, `src/six_multi.py`, `src/six_report.py` (`reportes/REPORTE_6_PARTIDOS.pdf`), `src/six_infografia.py` (`reportes/INFOGRAFIA_6_PARTIDOS.pdf`); detalle en `reportes/PARTIDOS6_EAN.xlsx`.
- 6 partidos (sin 3M): Regla fragancias, Regla makeup, Ciclo de vida (curva por edad hasta 17 meses; después trend de su fase), Media 6M prudente (trend 6M categoría ±60%), Media 6M estacional (perfil casa × trend fase ±60%), Media 12M estacional (perfil línea × 50% trend propio).
- DAs: trend con actuals; base limpia con el DA planificado (última foto en la que el mes aún no estaba cerrado: `ideo_panel.da_plan`); DAs futuros según la bandera de la foto: 100% / 50% / 0% (con bandera 2 el consenso es 100% DAs y se pasa un 84%).
- Conversión de DAs planificados en envío extra (hasta ago-26): fragancias 42% (sin bandera 23%; a 7–9 meses 17%), makeup 80%. Solo el 36–57% del DA planificado sigue en la foto siguiente.
- Urnas: sep-25 Q2–Q4, dic-25 Q3–Q4 (fragancias), mar-26 Q4. 929 EANs. Con trampa: WAPE90 parlamento 12,7% vs consenso 12,4%; error EAN 40% vs 54%.
- Prueba honesta (voto con oct–mar, medido abr–jun), error EAN: a 7–9 meses parlamento 53% vs consenso 73%; a 4–6 meses 60% vs 54%; a 1–3 meses 64% vs 42%. Votar por horizonte no lo arregla (62%); mejor partido único a 1–3 meses 54%.
- Propuesta: híbrido (consenso meses 1–6, partido del EAN meses 7–9); ciclo de vida para códigos nuevos; guardar los DAs de cada foto.
- **Corrección del usuario (2026-10-10):** el consenso es la salida de o9 que se quiere sustituir; no es referencia. Prueba honesta sin consenso (`src/six_sin_consenso.py`), error EAN en abr–jun a 7–9 / 4–6 / 1–3 meses: regla de su categoría 64 / 61 / 51%; voto del EAN 53 / 60 / 64%; voto del grupo 53 / 62 / 57%; media de los 6 partidos 64 / 60 / 46%; **media de sus 2 mejores partidos (coalición) 55 / 55 / 53%**. WAPE90 casa coalición 21 / 20 / 12% (reglas 19 / 21 / 13%).
- **¿Todas las estrategias o 6 partidos?** (`src/todas_vs_partidos.py`, foto sep-25, elegir con oct–mar y medir abr–jun, 690 EANs, 34.020 estrategias sin 3M): la mejor de todas 51,3% (en oct–mar parecía 17%); media de sus 10 mejores 50,4%; mejor de los 6 partidos 50,8% (en oct–mar 28%); coalición de 2 52,8%; regla 61,5%. Con validación cruzada de los 3 quarters de sep-25 (elegir con 2, probar el 3.º, rotando), error EAN medio: mejor de los 6 partidos 43,4%, coalición de 2 44,0%, media de las 10 mejores de todas 47,4%, mejor de todas 48,6%, regla 54,9%. Los 6 partidos ganan en ene–mar (39% vs 44%) y oct–dic (40% vs 51%) y empatan en abr–jun. Dentro de muestra la mejor de todas parece 17% y la de 6 partidos 29%: más opciones = más espejismo, no más puntería.
