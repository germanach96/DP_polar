# Graph Report - DP_polar  (2026-10-11)

## Corpus Check
- 87 files · ~127,664 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .csv 1)

## Summary
- 843 nodes · 2348 edges · 42 communities (38 shown, 4 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 84 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bd3fa814`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- parliament.py
- json
- numpy
- ideo_report.py
- pathlib
- Contexto del proyecto (CLAUDE.md)
- epos_patrones_report.py
- epos_diag.py
- six_report.py
- methods.py
- Investigacion demand planning
- ideo_viz.py
- pandas
- add_types
- snapshots.py
- mu_backtest.py
- parlamento_html.py
- infografia.py
- house_compare.py
- votes_report.py
- da_test.py
- parliament_report.py
- multivote.py
- subprocess
- da_conversion.py
- Explorador del parlamento (template)
- house_report.py
- Estrategia de forecast Makeup
- Check obligatorio de skills y plugins
- ideo_infografia.py
- mu_season.py
- Parlamento de la demanda (template)
- Product
- parliament_vs_cons.py
- Parties
- DAs (promos/inputs de mercado)
- Las 3 preguntas del EAN (base, trend, limpieza)
- mu_season_ean.py
- check-tools.sh
- session-start.sh
- skills-reminder.sh
- SPP3

## God Nodes (most connected - your core abstractions)
1. `add_types()` - 30 edges
2. `main()` - 23 edges
3. `_group_g()` - 23 edges
4. `Contexto del proyecto (CLAUDE.md)` - 20 edges
5. `build()` - 19 edges
6. `_ly()` - 19 edges
7. `f()` - 18 edges
8. `Investigacion demand planning` - 18 edges
9. `main()` - 17 edges
10. `main()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Hemiciclo (componente firma)` --references--> `seats()`  [INFERRED]
  DESIGN.md → src/votes_report.py
- `Elevation & Depth` --references--> `line()`  [INFERRED]
  DESIGN.md → src/epos_patrones_report.py
- `drawhemi()` --implements--> `Hemiciclo de escanos (reporte)`  [INFERRED]
  src/explorador_template.html → CLAUDE.md
- `drawtrends()` --references--> `EPOS (sell-out desde jul-24)`  [INFERRED]
  src/explorador_template.html → CLAUDE.md
- `Explorador del parlamento (template)` --conceptually_related_to--> `Check obligatorio de skills y plugins`  [INFERRED]
  src/explorador_template.html → .claude/CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Los 6 partidos del parlamento vigente** — claude_regla_fragancias, claude_regla_makeup, claude_ciclo_de_vida, claude_media_6m_prudente, claude_media_6m_estacional, claude_media_12m_estacional [EXTRACTED 1.00]
- **Renderizado del hemiciclo en reportes HTML** — src_parlamento_template_hemicycle, src_parlamento_template_seats, src_explorador_template_drawhemi, src_explorador_template_seats, claude_hemiciclo [INFERRED 0.85]
- **Flujo sell-in desde sell-out con EPOS** — claude_epos, claude_regla_por_edad, claude_partido_consumidor_epos, claude_semaforo_carga, investigacion_demand_planning_sell_in_desde_sell_out [INFERRED 0.85]

## Communities (42 total, 4 thin omitted)

### Community 0 - "parliament.py"
Cohesion: 0.20
Nodes (13): build(), main(), records(), tally(), build(), main(), records(), tally() (+5 more)

### Community 1 - "json"
Cohesion: 0.08
Nodes (25): main(), main(), main(), scores(), show(), main(), brujulas(), main() (+17 more)

### Community 2 - "numpy"
Cohesion: 0.06
Nodes (51): flagged(), index(), main(), position(), twin(), main(), main(), twin() (+43 more)

### Community 3 - "ideo_report.py"
Cohesion: 0.15
Nodes (21): cards_page(), compass_pts(), compasses(), curve_chart(), floor_chart(), hbars(), load(), main() (+13 more)

### Community 4 - "pathlib"
Cohesion: 0.14
Nodes (5): build(), da_plan(), extend(), launch_idx(), mu_function()

### Community 5 - "Contexto del proyecto (CLAUDE.md)"
Cohesion: 0.13
Nodes (16): Consenso de o9 (cons), Decision sep-25: Ciclo de vida para todos, Contexto del proyecto (CLAUDE.md), Media 12M estacional, Media 6M estacional, Media 6M prudente, Trend YoY 6M plano (metodo actual del equipo), WAPE90 (+8 more)

### Community 6 - "epos_patrones_report.py"
Cohesion: 0.08
Nodes (40): Colors, Dark theme, Design System: Parlamento de la demanda, Do:, Do's and Don'ts, Don't:, Elevation & Depth, Hierarchy (+32 more)

### Community 7 - "epos_diag.py"
Cohesion: 0.06
Nodes (36): caps(), channel(), coverage(), house_next(), load_effect(), main(), panel(), predictive() (+28 more)

### Community 8 - "six_report.py"
Cohesion: 0.14
Nodes (11): P6, legend(), card(), main(), voters(), bars(), cards_page(), flag_share() (+3 more)

### Community 9 - "methods.py"
Cohesion: 0.06
Nodes (51): consensus_rows(), context(), method_registry(), method_registry_v2(), method_registry_v3(), method_registry_v4(), run(), bands() (+43 more)

### Community 10 - "Investigacion demand planning"
Cohesion: 0.16
Nodes (16): Partido Consumidor (EPOS) (proximo paso), Semaforo de carga del canal, WOS (semanas de stock), Conversion de DAs planificados (42% fragancias, 80% makeup), Ajustes manuales positivos empeoran (Fildes 2025), Cross-learning y conciliacion de niveles, Investigacion demand planning, Estee Lauder 10-K FY2025 (+8 more)

### Community 11 - "ideo_viz.py"
Cohesion: 0.18
Nodes (9): page_cover(), card(), compass(), hemicycle(), pc(), seatrow(), volbar(), main() (+1 more)

### Community 12 - "pandas"
Cohesion: 0.16
Nodes (7): main(), load(), main(), load(), main(), summary(), wm()

### Community 13 - "add_types"
Cohesion: 0.18
Nodes (9): main(), main(), main(), add_types(), classify(), size_ml(), ean_votes(), main() (+1 more)

### Community 14 - "snapshots.py"
Cohesion: 0.08
Nodes (22): main(), agg(), fq(), prepare(), score(), table(), strategies(), agg_level() (+14 more)

### Community 15 - "mu_backtest.py"
Cohesion: 0.20
Nodes (9): da_known(), evaluate(), load(), main(), season_index(), techniques(), main(), forecast() (+1 more)

### Community 16 - "parlamento_html.py"
Cohesion: 0.17
Nodes (7): is_prompt(), main(), problems(), compass_points(), example(), main(), spread()

### Community 17 - "infografia.py"
Cohesion: 0.15
Nodes (18): bar_chart(), card(), chart_cuts(), chart_frag_season(), chart_mu_season(), chart_trend_windows(), charts_for(), legend() (+10 more)

### Community 18 - "house_compare.py"
Cohesion: 0.33
Nodes (10): central_mask(), frag_rule(), fragrances(), main(), makeup(), mu_rule(), segments(), summarize() (+2 more)

### Community 19 - "votes_report.py"
Cohesion: 0.33
Nodes (10): card(), chip(), hemicycle(), lectura(), legend(), main(), n0(), page() (+2 more)

### Community 20 - "da_test.py"
Cohesion: 0.27
Nodes (7): da_known(), main(), fragrances(), main(), makeup(), rows_for(), g_flat()

### Community 21 - "parliament_report.py"
Cohesion: 0.12
Nodes (24): Brújula política, Buttons, Chips / filtros, Components, Hemiciclo (componente firma), Navigation, Panels, card() (+16 more)

### Community 22 - "multivote.py"
Cohesion: 0.24
Nodes (6): build(), main(), records(), select(), simple_methods(), summarize()

### Community 23 - "subprocess"
Cohesion: 0.27
Nodes (4): check(), plugin_dir(), run(), skill_ok()

### Community 24 - "da_conversion.py"
Cohesion: 0.43
Nodes (4): conversion(), main(), rows_for(), summary()

### Community 25 - "Explorador del parlamento (template)"
Cohesion: 0.28
Nodes (12): aggregate(), /*__DATA__*/ placeholder (explorador_data.py), Explorador del parlamento (template), drawchart(), drawhemi(), drawpol(), drawtally(), drawtrends() (+4 more)

### Community 26 - "house_report.py"
Cohesion: 0.37
Nodes (10): chart(), ean_table(), main(), n0(), page(), panel(), pc(), q_table() (+2 more)

### Community 27 - "Estrategia de forecast Makeup"
Cohesion: 0.21
Nodes (6): EPOS (sell-out desde jul-24), Supply cuts, Estrategia de forecast Makeup, Funcion Face/Lips/Eyes, mu_load / mu_backtest / mu_cuts_da / mu_season_ean, Diagnostico EPOS (epos_diag, epos_pattern, epos_patrones)

### Community 28 - "Check obligatorio de skills y plugins"
Cohesion: 0.18
Nodes (10): Agent Skills, dataviz skill, Skills y plugins check (.claude/CLAUDE.md), Emil Kowalski skill, Hooks (session-start, skills-reminder, skills-stop-check), Graphify, Impeccable plugin, OmniRoute CLI (+2 more)

### Community 29 - "ideo_infografia.py"
Cohesion: 0.33
Nodes (9): flow(), ideas_rows(), key(), main(), page1(), page2(), party_card(), voters() (+1 more)

### Community 30 - "mu_season.py"
Cohesion: 0.43
Nodes (4): main(), panel(), profile(), strength()

### Community 31 - "Parlamento de la demanda (template)"
Cohesion: 0.29
Nodes (8): Hemiciclo de escanos (reporte), camara(), /*__DATA__*/ placeholder (parlamento_html.py), Parlamento de la demanda (template), hemicycle(), resultados(), seats(), volbar()

### Community 32 - "Product"
Cohesion: 0.18
Nodes (10): Brand Commitments, Capabilities and Constraints, Evidence on Hand, Operating Context, Platform, Positioning, Product, Product Principles (+2 more)

### Community 33 - "parliament_vs_cons.py"
Cohesion: 0.47
Nodes (3): evaluate(), main(), vote()

### Community 35 - "DAs (promos/inputs de mercado)"
Cohesion: 0.33
Nodes (4): Central vs Local (6 meses de envios), ideo_panel.da_plan, Estrategia de forecast Fragancias, src/ptype.py y MAPEO_TAMANOS_FRAGANCIAS.csv

### Community 38 - "Las 3 preguntas del EAN (base, trend, limpieza)"
Cohesion: 0.29
Nodes (5): DNI del EAN, Edad del EAN (tramos 6-11,12-17,18-25,26+), Fase del EAN (crecimiento/estable/declive), Bandera isf (Ignore System Forecast), brujulas()

### Community 40 - "mu_season_ean.py"
Cohesion: 0.36
Nodes (4): analyse(), main(), shares(), summary()

### Community 41 - "check-tools.sh"
Cohesion: 0.52
Nodes (5): PATH, plugin_row(), row(), check-tools.sh script, skill_row()

## Knowledge Gaps
- **22 isolated node(s):** `PATH`, `PATH`, `Forecast Value Added contra metodo ingenuo`, `Estee Lauder 10-K FY2025`, `Revisiting the value of data sharing (IJOPM 2025)` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 253 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Design System: Parlamento de la demanda` connect `epos_patrones_report.py` to `parliament_report.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **What connects `PATH`, `PATH`, `Forecast Value Added contra metodo ingenuo` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.08345428156748912 - nodes in this community are weakly interconnected._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.056134723336006415 - nodes in this community are weakly interconnected._
- **Should `pathlib` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._
- **Should `Contexto del proyecto (CLAUDE.md)` be split into smaller, more focused modules?**
  _Cohesion score 0.12648221343873517 - nodes in this community are weakly interconnected._
- **Should `epos_patrones_report.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07928118393234672 - nodes in this community are weakly interconnected._