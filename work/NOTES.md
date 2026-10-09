# NOTES — memoria de trabajo del análisis (para Claude; no es entregable)

Última actualización: 2026-10-09 (sesión 1)

## Cómo retomar
1. `pip install statsmodels openpyxl pyarrow`
2. `python3 src/load.py && python3 src/panel.py` (genera work/*.pkl)
3. Leer este archivo + work/results/*.md (resultados de cada experimento).

## Datos (DATA.xlsx)
- 5 pestañas = versiones: S&OP 2025.M09, 2025.M12, 2026.M03, 2026.M06, Month-2026.M09.W38. Columna `version` = 'YYYY-MM'.
- Columnas: House, Brand, Product Line, EAN, Desc, FY, FQ, Month, Final Responsibility, Ignore System Forecast Flag (isf),
  Consensus-Final LY M (cons_ly), EPOS, Total Demand Assumption (da), Consensus-Final (cons), Actuals (act), Supply Cuts (cuts).
- Año fiscal: julio–junio. FY24 = 2023.M07–2024.M06. FY26 = 2025.M07–2026.M06 (completo en la última versión). FY27 = jul-26..jun-27.
- 4 houses: BURBERRY, Gucci, CP-Marc Jacobs (fragancia; MJ incluye body mists), Kylie Makeup (solo 9 EANs de brochas/accesorios, ~75k u/año -> comparación fragancia vs maquillaje es muy débil).
- ~549 EANs en la última versión.
- Volumen histórico (unidades, última versión): FY24 7.64M, FY25 6.63M, FY26 6.13M -> caída ~-13% y ~-8%.

## Hallazgos de calidad de datos (IMPORTANTE)
- **Reexpresión del histórico**: desde la versión 2026-03 los actuals de TODO el histórico suben ~+20% (BBY 1.20, MJ 1.15-1.17, Gucci 1.26-1.29)
  vs versiones 2025-09/2025-12. Por EAN el ratio va de 1.0 a 1.7. Parece cambio de perímetro (¿cliente/canal añadido?). -> PREGUNTA ABIERTA al usuario.
  => Fuente de verdad = última versión. Los forecasts de consenso de 2025-09 y 2025-12 están en el perímetro viejo: compararlos con actuals nuevos los sesga ~-20%.
- `cons` en meses pasados == `act`. `cons_ly` == cons desplazado 12 meses (redundante = naïve estacional).
- La última versión no trae Actuals de 2023.M07-M08 pero sí cons (== actual). Uso cons como histórico.
- El mes de la versión trae actual parcial (p.ej. 2026.M09 = 265k de ~865k). Se excluye.
- Sin negativos. Faltantes = 0 tras la primera venta.
- EPOS: solo existe desde 2024.M07 (FY25) y solo en versiones >= 2026-03.
- DA: en meses futuros; en la última versión FY27 DA = 476k sobre cons 4.45M (oct-26..jun-27).
- isf toma valores 1 y 2 (constante por EAN). Usuario dijo 1 = forecast manual. **2 = ? PREGUNTA ABIERTA**. 62 EANs con 1, 50 con 2.
- Supply cuts: el usuario avisa de que pueden estar inflados hasta x4 (pedidos repetidos semanales). Muy altos en FY26.Q1-Q2 (518k y 452k vs ~200k/quarter habitual).

## Responsabilidad Local vs Central (IMPORTANTE)
- Versiones 2025-09/12: campo vacío. 2026-06: TODO 'Local' (sospechoso). 2026-03 y 2026-09: mayoría Central.
- Local en 2026-09: 85 EANs, ~2.4% del volumen histórico; Local en 2026-03: 122 EANs.
- Los Local son casi todos **lanzamientos/innovación** (Goddess Amber Vanilla, Flora Gorgeous Orchid Intense, Just Perfect,
  Guilty New27, Daisy Body Mist, Her 8th, Hero Elixir...) que pasan a Central tras unos meses. Casi todos isf=1/2.
  => "Local" ≈ lanzamientos sin histórico YoY: los métodos de trend YoY NO aplican directamente. -> PREGUNTA ABIERTA:
  ¿confirmar que local = innovación? ¿qué hacer con el campo de 2026-06?
- Plan: analizar portfolio completo (las reglas de trend sirven para todo lo maduro) + análisis específico de lanzamientos (curvas).

## Estructura de código
- src/load.py: Excel -> work/data.parquet (largo, todas las versiones).
- src/panel.py: panel EAN x mes de la última versión -> work/hist.pkl, cuts.pkl, epos.pkl, attr.pkl, snaps.pkl (consenso por versión), fut_latest.pkl.
