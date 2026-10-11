# Graph Report - DP_polar  (2026-10-11)

## Corpus Check
- 86 files · ~126,841 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .csv 1)

## Summary
- 834 nodes · 2326 edges · 39 communities (35 shown, 4 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 84 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b15718cd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- add_types
- json
- numpy
- ideo_report.py
- f
- Parlamento de 6 y consenso
- Reporte de patrones EPOS
- epos_diag.py
- epos_pattern.py
- _group_g
- Investigación: coalición y EPOS
- backtest.py
- pandas
- methods.py
- evaluate.py
- Design System: Parlamento de la demanda
- epos_patrones.py
- infografia.py
- seasonal_index
- epos_reco_test.py
- panel.py
- votes_report.py
- tracking.py
- snapshots.py
- da_conversion.py
- Explorador (plantilla)
- Reporte por casa
- Regla makeup y cortes
- Skills y plugins
- Parlamento HTML (plantilla)
- Product
- Regla fragancias y DAs
- DNI del EAN y 3 preguntas
- Estacionalidad makeup
- Check de herramientas
- snap_eval.py
- Arranque de sesión
- Recordatorio de skills
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
- `Elevation & Depth` --references--> `line()`  [INFERRED]
  DESIGN.md → src/epos_patrones_report.py
- `Hemiciclo (componente firma)` --references--> `seats()`  [INFERRED]
  DESIGN.md → src/votes_report.py
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

## Communities (39 total, 4 thin omitted)

### Community 0 - "add_types"
Cohesion: 0.05
Nodes (54): is_prompt(), main(), problems(), main(), da_known(), main(), fragrances(), main() (+46 more)

### Community 1 - "json"
Cohesion: 0.05
Nodes (33): main(), main(), main(), scores(), show(), main(), brujulas(), main() (+25 more)

### Community 2 - "numpy"
Cohesion: 0.06
Nodes (51): run(), flagged(), index(), main(), position(), twin(), main(), main() (+43 more)

### Community 3 - "ideo_report.py"
Cohesion: 0.05
Nodes (51): P6, flow(), ideas_rows(), key(), main(), page1(), page2(), party_card() (+43 more)

### Community 4 - "f"
Cohesion: 0.20
Nodes (13): method_registry(), method_registry_v2(), make_blend_trend(), make_clean_trend(), make_combo(), make_cut_adjusted(), make_damped_group(), make_group_trend() (+5 more)

### Community 5 - "Parlamento de 6 y consenso"
Cohesion: 0.13
Nodes (16): Consenso de o9 (cons), Decision sep-25: Ciclo de vida para todos, Contexto del proyecto (CLAUDE.md), Media 12M estacional, Media 6M estacional, Media 6M prudente, Trend YoY 6M plano (metodo actual del equipo), WAPE90 (+8 more)

### Community 6 - "Reporte de patrones EPOS"
Cohesion: 0.21
Nodes (20): axis_y(), cohort_bars(), cover(), dumbbell(), exits_chart(), launch_chart(), lerp(), line() (+12 more)

### Community 7 - "epos_diag.py"
Cohesion: 0.14
Nodes (13): caps(), channel(), coverage(), house_next(), load_effect(), main(), panel(), predictive() (+5 more)

### Community 8 - "epos_pattern.py"
Cohesion: 0.24
Nodes (9): agg(), constancy(), events(), load_build(), load_section(), main(), regress(), table() (+1 more)

### Community 9 - "_group_g"
Cohesion: 0.12
Nodes (21): main(), main(), _apply(), clean_history(), g_flat(), _group_g(), _ly(), f() (+13 more)

### Community 10 - "Investigación: coalición y EPOS"
Cohesion: 0.16
Nodes (16): Partido Consumidor (EPOS) (proximo paso), Semaforo de carga del canal, WOS (semanas de stock), Conversion de DAs planificados (42% fragancias, 80% makeup), Ajustes manuales positivos empeoran (Fildes 2025), Cross-learning y conciliacion de niveles, Investigacion demand planning, Estee Lauder 10-K FY2025 (+8 more)

### Community 11 - "backtest.py"
Cohesion: 0.21
Nodes (7): consensus_rows(), context(), method_registry_v4(), bands(), main(), make_resc_general(), f()

### Community 12 - "pandas"
Cohesion: 0.19
Nodes (7): main(), load(), load(), main(), panel(), profile(), strength()

### Community 13 - "methods.py"
Cohesion: 0.23
Nodes (6): ets_damped(), ets_damped_house_share(), g_median(), g_trimmed(), _ratios(), _window()

### Community 14 - "evaluate.py"
Cohesion: 0.18
Nodes (9): main(), agg(), fq(), prepare(), score(), table(), agg_level(), main() (+1 more)

### Community 15 - "Design System: Parlamento de la demanda"
Cohesion: 0.07
Nodes (26): Brújula política, Buttons, Chips / filtros, Colors, Components, Dark theme, Design System: Parlamento de la demanda, Do: (+18 more)

### Community 16 - "epos_patrones.py"
Cohesion: 0.31
Nodes (8): launch_curves(), launches(), load_and_exits(), main(), mature_set(), noise(), trend(), veterans()

### Community 17 - "infografia.py"
Cohesion: 0.15
Nodes (18): bar_chart(), card(), chart_cuts(), chart_frag_season(), chart_mu_season(), chart_trend_windows(), charts_for(), legend() (+10 more)

### Community 18 - "seasonal_index"
Cohesion: 0.20
Nodes (7): method_registry_v3(), make_epos_group(), f(), f(), make_young_level(), f(), seasonal_index()

### Community 19 - "epos_reco_test.py"
Cohesion: 0.31
Nodes (6): age_ratio(), main(), profile(), score(), test_vet(), test_young()

### Community 21 - "votes_report.py"
Cohesion: 0.09
Nodes (32): Hemiciclo (componente firma), compass_points(), example(), main(), spread(), card(), dot(), hemicycle() (+24 more)

### Community 22 - "tracking.py"
Cohesion: 0.23
Nodes (8): strategies(), calib_ratio(), chain(), base_fc(), load(), main(), rule_matrix(), score()

### Community 23 - "snapshots.py"
Cohesion: 0.33
Nodes (5): main(), month_factors(), rules(), snapshot_ctx(), ytd_window()

### Community 24 - "da_conversion.py"
Cohesion: 0.43
Nodes (4): conversion(), main(), rows_for(), summary()

### Community 25 - "Explorador (plantilla)"
Cohesion: 0.28
Nodes (12): aggregate(), /*__DATA__*/ placeholder (explorador_data.py), Explorador del parlamento (template), drawchart(), drawhemi(), drawpol(), drawtally(), drawtrends() (+4 more)

### Community 26 - "Reporte por casa"
Cohesion: 0.37
Nodes (10): chart(), ean_table(), main(), n0(), page(), panel(), pc(), q_table() (+2 more)

### Community 27 - "Regla makeup y cortes"
Cohesion: 0.21
Nodes (6): EPOS (sell-out desde jul-24), Supply cuts, Estrategia de forecast Makeup, Funcion Face/Lips/Eyes, mu_load / mu_backtest / mu_cuts_da / mu_season_ean, Diagnostico EPOS (epos_diag, epos_pattern, epos_patrones)

### Community 28 - "Skills y plugins"
Cohesion: 0.18
Nodes (10): Agent Skills, dataviz skill, Skills y plugins check (.claude/CLAUDE.md), Emil Kowalski skill, Hooks (session-start, skills-reminder, skills-stop-check), Graphify, Impeccable plugin, OmniRoute CLI (+2 more)

### Community 31 - "Parlamento HTML (plantilla)"
Cohesion: 0.29
Nodes (8): Hemiciclo de escanos (reporte), camara(), /*__DATA__*/ placeholder (parlamento_html.py), Parlamento de la demanda (template), hemicycle(), resultados(), seats(), volbar()

### Community 32 - "Product"
Cohesion: 0.18
Nodes (10): Brand Commitments, Capabilities and Constraints, Evidence on Hand, Operating Context, Platform, Positioning, Product, Product Principles (+2 more)

### Community 35 - "Regla fragancias y DAs"
Cohesion: 0.33
Nodes (4): Central vs Local (6 meses de envios), ideo_panel.da_plan, Estrategia de forecast Fragancias, src/ptype.py y MAPEO_TAMANOS_FRAGANCIAS.csv

### Community 38 - "DNI del EAN y 3 preguntas"
Cohesion: 0.29
Nodes (5): DNI del EAN, Edad del EAN (tramos 6-11,12-17,18-25,26+), Fase del EAN (crecimiento/estable/declive), Bandera isf (Ignore System Forecast), brujulas()

### Community 40 - "Estacionalidad makeup"
Cohesion: 0.36
Nodes (4): analyse(), main(), shares(), summary()

### Community 41 - "Check de herramientas"
Cohesion: 0.52
Nodes (5): PATH, plugin_row(), row(), check-tools.sh script, skill_row()

### Community 45 - "snap_eval.py"
Cohesion: 0.60
Nodes (3): main(), summary(), wm()

## Knowledge Gaps
- **22 isolated node(s):** `PATH`, `PATH`, `Forecast Value Added contra metodo ingenuo`, `Estee Lauder 10-K FY2025`, `Revisiting the value of data sharing (IJOPM 2025)` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 251 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `line()` connect `Reporte de patrones EPOS` to `Design System: Parlamento de la demanda`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **What connects `PATH`, `PATH`, `Forecast Value Added contra metodo ingenuo` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `add_types` be split into smaller, more focused modules?**
  _Cohesion score 0.0506578947368421 - nodes in this community are weakly interconnected._
- **Why does `Elevation & Depth` connect `Design System: Parlamento de la demanda` to `Reporte de patrones EPOS`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.05347985347985348 - nodes in this community are weakly interconnected._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.06111111111111111 - nodes in this community are weakly interconnected._
- **Should `ideo_report.py` be split into smaller, more focused modules?**
  _Cohesion score 0.051791629027401385 - nodes in this community are weakly interconnected._