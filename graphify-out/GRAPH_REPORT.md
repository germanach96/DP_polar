# Graph Report - DP_polar  (2026-10-11)

## Corpus Check
- 90 files · ~245,355 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .woff2 2, .csv 1)

## Summary
- 859 nodes · 2385 edges · 47 communities (41 shown, 6 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 88 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8c674cc8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- add_types
- ideo_panel.py
- numpy
- ideo_report.py
- _ly
- Contexto del proyecto (CLAUDE.md)
- epos_patrones_report.py
- epos_diag.py
- ideo_viz.py
- f
- Investigacion demand planning
- backtest.py
- pandas
- pathlib
- evaluate.py
- tracking.py
- ponytail-switch.py
- infografia.py
- epos_pattern.py
- votes_report.py
- _group_g
- rulevote_report.py
- epos_patrones.py
- subprocess
- da_conversion.py
- Explorador del parlamento (template)
- house_report.py
- Estrategia de forecast Makeup
- Check obligatorio de skills y plugins
- ideo_infografia.py
- epos_reco_test.py
- Parlamento de la demanda (template)
- Product
- parliament_report.py
- snapshots.py
- DAs (promos/inputs de mercado)
- wape90_report.py
- snap_eval.py
- Las 3 preguntas del EAN (base, trend, limpieza)
- panel.py
- mu_season_ean.py
- check-tools.sh
- six_infografia.py
- src-explorador-template-html.md
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
- `Buttons` --references--> `line()`  [INFERRED]
  DESIGN.md → src/epos_patrones_report.py
- `Cards / Containers` --references--> `line()`  [INFERRED]
  DESIGN.md → src/epos_patrones_report.py
- `Chips` --references--> `line()`  [INFERRED]
  DESIGN.md → src/epos_patrones_report.py
- `Inputs / Fields` --references--> `line()`  [INFERRED]
  DESIGN.md → src/epos_patrones_report.py
- `Neutral` --references--> `line()`  [INFERRED]
  DESIGN.md → src/epos_patrones_report.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Los 6 partidos del parlamento vigente** — claude_regla_fragancias, claude_regla_makeup, claude_ciclo_de_vida, claude_media_6m_prudente, claude_media_6m_estacional, claude_media_12m_estacional [EXTRACTED 1.00]
- **Renderizado del hemiciclo en reportes HTML** — src_parlamento_template_hemicycle, src_parlamento_template_seats, src_explorador_template_drawhemi, src_explorador_template_seats, claude_hemiciclo [INFERRED 0.85]
- **Flujo sell-in desde sell-out con EPOS** — claude_epos, claude_regla_por_edad, claude_partido_consumidor_epos, claude_semaforo_carga, investigacion_demand_planning_sell_in_desde_sell_out [INFERRED 0.85]

## Communities (47 total, 6 thin omitted)

### Community 0 - "add_types"
Cohesion: 0.07
Nodes (47): main(), da_known(), main(), central_mask(), frag_rule(), fragrances(), main(), makeup() (+39 more)

### Community 1 - "ideo_panel.py"
Cohesion: 0.06
Nodes (29): main(), main(), main(), scores(), show(), brujulas(), main(), main() (+21 more)

### Community 2 - "numpy"
Cohesion: 0.05
Nodes (55): main(), main(), flagged(), index(), main(), position(), twin(), main() (+47 more)

### Community 3 - "ideo_report.py"
Cohesion: 0.15
Nodes (21): cards_page(), compass_pts(), compasses(), curve_chart(), floor_chart(), hbars(), load(), main() (+13 more)

### Community 4 - "_ly"
Cohesion: 0.12
Nodes (17): method_registry_v3(), main(), _apply(), clean_history(), _ly(), make_clean_rescaled(), f(), f() (+9 more)

### Community 5 - "Contexto del proyecto (CLAUDE.md)"
Cohesion: 0.13
Nodes (16): Consenso de o9 (cons), Decision sep-25: Ciclo de vida para todos, Contexto del proyecto (CLAUDE.md), Media 12M estacional, Media 6M estacional, Media 6M prudente, Trend YoY 6M plano (metodo actual del equipo), WAPE90 (+8 more)

### Community 6 - "epos_patrones_report.py"
Cohesion: 0.07
Nodes (48): Buttons, Cards / Containers, Chips, Colors, Components, Design System: Parlamento de la demanda, Do:, Do's and Don'ts (+40 more)

### Community 7 - "epos_diag.py"
Cohesion: 0.14
Nodes (13): caps(), channel(), coverage(), house_next(), load_effect(), main(), panel(), predictive() (+5 more)

### Community 8 - "ideo_viz.py"
Cohesion: 0.10
Nodes (18): P6, page_cover(), card(), compass(), hemicycle(), legend(), pc(), seatrow() (+10 more)

### Community 9 - "f"
Cohesion: 0.13
Nodes (19): method_registry(), method_registry_v2(), make_blend_trend(), f(), make_clean_trend(), make_combo(), make_cut_adjusted(), make_damped_group() (+11 more)

### Community 10 - "Investigacion demand planning"
Cohesion: 0.16
Nodes (16): Partido Consumidor (EPOS) (proximo paso), Semaforo de carga del canal, WOS (semanas de stock), Conversion de DAs planificados (42% fragancias, 80% makeup), Ajustes manuales positivos empeoran (Fildes 2025), Cross-learning y conciliacion de niveles, Investigacion demand planning, Estee Lauder 10-K FY2025 (+8 more)

### Community 11 - "backtest.py"
Cohesion: 0.15
Nodes (10): consensus_rows(), context(), method_registry_v4(), run(), bands(), main(), make_resc_general(), f() (+2 more)

### Community 12 - "pandas"
Cohesion: 0.19
Nodes (7): main(), load(), load(), main(), panel(), profile(), strength()

### Community 13 - "pathlib"
Cohesion: 0.16
Nodes (6): ets_damped(), ets_damped_house_share(), g_median(), g_trimmed(), _ratios(), _window()

### Community 14 - "evaluate.py"
Cohesion: 0.18
Nodes (9): main(), agg(), fq(), prepare(), score(), table(), agg_level(), main() (+1 more)

### Community 15 - "tracking.py"
Cohesion: 0.25
Nodes (7): calib_ratio(), chain(), base_fc(), load(), main(), rule_matrix(), score()

### Community 16 - "ponytail-switch.py"
Cohesion: 0.12
Nodes (13): explicit(), flag_files(), main(), mode_for(), norm(), set_mode(), is_prompt(), main() (+5 more)

### Community 17 - "infografia.py"
Cohesion: 0.24
Nodes (12): bar_chart(), card(), chart_cuts(), chart_frag_season(), chart_mu_season(), chart_trend_windows(), charts_for(), legend() (+4 more)

### Community 18 - "epos_pattern.py"
Cohesion: 0.24
Nodes (9): agg(), constancy(), events(), load_build(), load_section(), main(), regress(), table() (+1 more)

### Community 19 - "votes_report.py"
Cohesion: 0.28
Nodes (11): card(), chip(), hemicycle(), lectura(), legend(), main(), n0(), page() (+3 more)

### Community 20 - "_group_g"
Cohesion: 0.42
Nodes (7): fragrances(), main(), makeup(), rows_for(), main(), g_flat(), _group_g()

### Community 21 - "rulevote_report.py"
Cohesion: 0.36
Nodes (8): card(), chip(), hemicycle(), legend(), main(), page(), rules_box(), volbar()

### Community 22 - "epos_patrones.py"
Cohesion: 0.31
Nodes (8): launch_curves(), launches(), load_and_exits(), main(), mature_set(), noise(), trend(), veterans()

### Community 23 - "subprocess"
Cohesion: 0.31
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
Cohesion: 0.19
Nodes (10): flow(), ideas_rows(), key(), main(), page1(), page2(), party_card(), voters() (+2 more)

### Community 30 - "epos_reco_test.py"
Cohesion: 0.31
Nodes (6): age_ratio(), main(), profile(), score(), test_vet(), test_young()

### Community 31 - "Parlamento de la demanda (template)"
Cohesion: 0.29
Nodes (8): Hemiciclo de escanos (reporte), camara(), /*__DATA__*/ placeholder (parlamento_html.py), Parlamento de la demanda (template), hemicycle(), resultados(), seats(), volbar()

### Community 32 - "Product"
Cohesion: 0.18
Nodes (10): Brand Commitments, Capabilities and Constraints, Evidence on Hand, Operating Context, Platform, Positioning, Product, Product Principles (+2 more)

### Community 33 - "parliament_report.py"
Cohesion: 0.42
Nodes (8): card(), dot(), hemicycle(), legend(), main(), page(), seatrow(), volbar()

### Community 34 - "snapshots.py"
Cohesion: 0.33
Nodes (5): main(), month_factors(), rules(), snapshot_ctx(), ytd_window()

### Community 35 - "DAs (promos/inputs de mercado)"
Cohesion: 0.33
Nodes (4): Central vs Local (6 meses de envios), ideo_panel.da_plan, Estrategia de forecast Fragancias, src/ptype.py y MAPEO_TAMANOS_FRAGANCIAS.csv

### Community 36 - "wape90_report.py"
Cohesion: 0.44
Nodes (6): bar_block(), cell(), get(), main(), n0(), pc()

### Community 37 - "snap_eval.py"
Cohesion: 0.60
Nodes (3): main(), summary(), wm()

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 254 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `PATH`, `PATH`, `Forecast Value Added contra metodo ingenuo` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `add_types` be split into smaller, more focused modules?**
  _Cohesion score 0.06596035543403965 - nodes in this community are weakly interconnected._
- **Should `ideo_panel.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06436487638533675 - nodes in this community are weakly interconnected._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.05219072164948454 - nodes in this community are weakly interconnected._
- **Should `_ly` be split into smaller, more focused modules?**
  _Cohesion score 0.12318840579710146 - nodes in this community are weakly interconnected._
- **Should `Contexto del proyecto (CLAUDE.md)` be split into smaller, more focused modules?**
  _Cohesion score 0.12648221343873517 - nodes in this community are weakly interconnected._
- **Should `epos_patrones_report.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06636500754147813 - nodes in this community are weakly interconnected._