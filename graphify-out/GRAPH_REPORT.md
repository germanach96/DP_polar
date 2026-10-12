# Graph Report - DP_polar  (2026-10-12)

## Corpus Check
- 88 files · ~128,543 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .csv 1)

## Summary
- 855 nodes · 2377 edges · 40 communities (35 shown, 5 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 84 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `30f3a225`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- add_types
- json
- numpy
- ideo_report.py
- tracking.py
- Contexto del proyecto (CLAUDE.md)
- epos_patrones_report.py
- epos_diag.py
- subprocess
- methods.py
- Investigacion demand planning
- ideo_viz.py
- pandas
- epos_pattern.py
- snapshots.py
- epos_patrones.py
- ponytail-switch.py
- infografia.py
- epos_reco_test.py
- votes_report.py
- parliament_report.py
- rulevote_report.py
- wape90_report.py
- P6
- snap_eval.py
- Explorador del parlamento (template)
- house_report.py
- Estrategia de forecast Makeup
- Check obligatorio de skills y plugins
- ideo_infografia.py
- panel.py
- Parlamento de la demanda (template)
- Product
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

## Communities (40 total, 5 thin omitted)

### Community 0 - "add_types"
Cohesion: 0.06
Nodes (52): main(), da_known(), main(), fragrances(), main(), makeup(), rows_for(), central_mask() (+44 more)

### Community 1 - "json"
Cohesion: 0.05
Nodes (38): main(), main(), conversion(), main(), rows_for(), summary(), main(), scores() (+30 more)

### Community 2 - "numpy"
Cohesion: 0.06
Nodes (50): flagged(), index(), main(), position(), twin(), main(), main(), twin() (+42 more)

### Community 3 - "ideo_report.py"
Cohesion: 0.15
Nodes (22): cards_page(), compass_pts(), compasses(), curve_chart(), floor_chart(), hbars(), load(), main() (+14 more)

### Community 4 - "tracking.py"
Cohesion: 0.25
Nodes (7): calib_ratio(), chain(), base_fc(), load(), main(), rule_matrix(), score()

### Community 5 - "Contexto del proyecto (CLAUDE.md)"
Cohesion: 0.13
Nodes (16): Consenso de o9 (cons), Decision sep-25: Ciclo de vida para todos, Contexto del proyecto (CLAUDE.md), Media 12M estacional, Media 6M estacional, Media 6M prudente, Trend YoY 6M plano (metodo actual del equipo), WAPE90 (+8 more)

### Community 6 - "epos_patrones_report.py"
Cohesion: 0.07
Nodes (46): Brújula política, Buttons, Chips / filtros, Colors, Components, Dark theme, Design System: Parlamento de la demanda, Do: (+38 more)

### Community 7 - "epos_diag.py"
Cohesion: 0.14
Nodes (13): caps(), channel(), coverage(), house_next(), load_effect(), main(), panel(), predictive() (+5 more)

### Community 8 - "subprocess"
Cohesion: 0.17
Nodes (11): compass(), legend(), card(), main(), voters(), bars(), cards_page(), flag_share() (+3 more)

### Community 9 - "methods.py"
Cohesion: 0.05
Nodes (53): consensus_rows(), context(), method_registry(), method_registry_v2(), method_registry_v3(), method_registry_v4(), run(), bands() (+45 more)

### Community 10 - "Investigacion demand planning"
Cohesion: 0.16
Nodes (16): Partido Consumidor (EPOS) (proximo paso), Semaforo de carga del canal, WOS (semanas de stock), Conversion de DAs planificados (42% fragancias, 80% makeup), Ajustes manuales positivos empeoran (Fildes 2025), Cross-learning y conciliacion de niveles, Investigacion demand planning, Estee Lauder 10-K FY2025 (+8 more)

### Community 11 - "ideo_viz.py"
Cohesion: 0.22
Nodes (7): card(), hemicycle(), pc(), seatrow(), volbar(), main(), sec()

### Community 12 - "pandas"
Cohesion: 0.19
Nodes (7): main(), load(), load(), main(), panel(), profile(), strength()

### Community 13 - "epos_pattern.py"
Cohesion: 0.24
Nodes (9): agg(), constancy(), events(), load_build(), load_section(), main(), regress(), table() (+1 more)

### Community 14 - "snapshots.py"
Cohesion: 0.12
Nodes (15): main(), agg(), fq(), prepare(), score(), table(), main(), agg_level() (+7 more)

### Community 15 - "epos_patrones.py"
Cohesion: 0.31
Nodes (8): launch_curves(), launches(), load_and_exits(), main(), mature_set(), noise(), trend(), veterans()

### Community 16 - "ponytail-switch.py"
Cohesion: 0.09
Nodes (17): explicit(), flag_files(), main(), mode_for(), norm(), set_mode(), check(), plugin_dir() (+9 more)

### Community 17 - "infografia.py"
Cohesion: 0.24
Nodes (12): bar_chart(), card(), chart_cuts(), chart_frag_season(), chart_mu_season(), chart_trend_windows(), charts_for(), legend() (+4 more)

### Community 18 - "epos_reco_test.py"
Cohesion: 0.31
Nodes (6): age_ratio(), main(), profile(), score(), test_vet(), test_young()

### Community 19 - "votes_report.py"
Cohesion: 0.25
Nodes (12): Hemiciclo (componente firma), card(), chip(), hemicycle(), lectura(), legend(), main(), n0() (+4 more)

### Community 20 - "parliament_report.py"
Cohesion: 0.42
Nodes (8): card(), dot(), hemicycle(), legend(), main(), page(), seatrow(), volbar()

### Community 21 - "rulevote_report.py"
Cohesion: 0.36
Nodes (8): card(), chip(), hemicycle(), legend(), main(), page(), rules_box(), volbar()

### Community 22 - "wape90_report.py"
Cohesion: 0.44
Nodes (6): bar_block(), cell(), get(), main(), n0(), pc()

### Community 24 - "snap_eval.py"
Cohesion: 0.60
Nodes (3): main(), summary(), wm()

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
Cohesion: 0.19
Nodes (10): flow(), ideas_rows(), key(), main(), page1(), page2(), party_card(), voters() (+2 more)

### Community 31 - "Parlamento de la demanda (template)"
Cohesion: 0.29
Nodes (8): Hemiciclo de escanos (reporte), camara(), /*__DATA__*/ placeholder (parlamento_html.py), Parlamento de la demanda (template), hemicycle(), resultados(), seats(), volbar()

### Community 32 - "Product"
Cohesion: 0.18
Nodes (10): Brand Commitments, Capabilities and Constraints, Evidence on Hand, Operating Context, Platform, Positioning, Product, Product Principles (+2 more)

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 256 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `PATH`, `PATH`, `Forecast Value Added contra metodo ingenuo` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `add_types` be split into smaller, more focused modules?**
  _Cohesion score 0.059822361546499475 - nodes in this community are weakly interconnected._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.05039193729003359 - nodes in this community are weakly interconnected._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.060240963855421686 - nodes in this community are weakly interconnected._
- **Should `ideo_report.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1455026455026455 - nodes in this community are weakly interconnected._
- **Should `Contexto del proyecto (CLAUDE.md)` be split into smaller, more focused modules?**
  _Cohesion score 0.12648221343873517 - nodes in this community are weakly interconnected._
- **Should `epos_patrones_report.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06612244897959184 - nodes in this community are weakly interconnected._