# Graph Report - DP_polar  (2026-10-11)

## Corpus Check
- 86 files · ~126,665 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .csv 1)

## Summary
- 832 nodes · 2324 edges · 47 communities (43 shown, 4 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 84 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ea84299b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- multivote.py
- six_multi.py
- ideo_parties.py
- Reporte de ideologías
- add_types
- Parlamento de 6 y consenso
- Reporte de patrones EPOS
- epos_diag.py
- Infografía de 6 partidos
- methods.py
- Investigación: coalición y EPOS
- Piezas visuales (ideo_viz)
- da_conversion.py
- pathlib
- snapshots.py
- Design System: Parlamento de la demanda
- ideo_infografia.py
- infografia.py
- json
- ideo_brujulas6.py
- numpy
- votes_report.py
- tracking.py
- mu_backtest.py
- ideo_vs_cons.py
- Explorador (plantilla)
- Reporte por casa
- Regla makeup y cortes
- Skills y plugins
- house_compare.py
- Reporte votación de reglas
- Parlamento HTML (plantilla)
- Product
- parliament.py
- Reporte del parlamento
- Regla fragancias y DAs
- parlamento_html.py
- Parties
- DNI del EAN y 3 preguntas
- votes.py
- Estacionalidad makeup
- Check de herramientas
- pandas
- describe
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

## Communities (47 total, 4 thin omitted)

### Community 0 - "multivote.py"
Cohesion: 0.14
Nodes (14): main(), records(), select(), simple_methods(), summarize(), build(), main(), records() (+6 more)

### Community 1 - "six_multi.py"
Cohesion: 0.09
Nodes (21): main(), main(), scores(), show(), brujulas(), main(), main(), choose() (+13 more)

### Community 2 - "ideo_parties.py"
Cohesion: 0.13
Nodes (19): run(), axis_scores(), complexity(), dist_to(), elect_summary(), election(), excel(), ideas() (+11 more)

### Community 3 - "Reporte de ideologías"
Cohesion: 0.15
Nodes (21): cards_page(), compass_pts(), compasses(), curve_chart(), floor_chart(), hbars(), load(), main() (+13 more)

### Community 4 - "add_types"
Cohesion: 0.16
Nodes (11): main(), da_known(), main(), fragrances(), main(), makeup(), rows_for(), main() (+3 more)

### Community 5 - "Parlamento de 6 y consenso"
Cohesion: 0.13
Nodes (16): Consenso de o9 (cons), Decision sep-25: Ciclo de vida para todos, Contexto del proyecto (CLAUDE.md), Media 12M estacional, Media 6M estacional, Media 6M prudente, Trend YoY 6M plano (metodo actual del equipo), WAPE90 (+8 more)

### Community 6 - "Reporte de patrones EPOS"
Cohesion: 0.21
Nodes (20): axis_y(), cohort_bars(), cover(), dumbbell(), exits_chart(), launch_chart(), lerp(), line() (+12 more)

### Community 7 - "epos_diag.py"
Cohesion: 0.06
Nodes (36): caps(), channel(), coverage(), house_next(), load_effect(), main(), panel(), predictive() (+28 more)

### Community 8 - "Infografía de 6 partidos"
Cohesion: 0.14
Nodes (11): P6, legend(), card(), main(), voters(), bars(), cards_page(), flag_share() (+3 more)

### Community 9 - "methods.py"
Cohesion: 0.06
Nodes (55): consensus_rows(), context(), method_registry(), method_registry_v2(), method_registry_v3(), method_registry_v4(), bands(), main() (+47 more)

### Community 10 - "Investigación: coalición y EPOS"
Cohesion: 0.16
Nodes (16): Partido Consumidor (EPOS) (proximo paso), Semaforo de carga del canal, WOS (semanas de stock), Conversion de DAs planificados (42% fragancias, 80% makeup), Ajustes manuales positivos empeoran (Fildes 2025), Cross-learning y conciliacion de niveles, Investigacion demand planning, Estee Lauder 10-K FY2025 (+8 more)

### Community 11 - "Piezas visuales (ideo_viz)"
Cohesion: 0.18
Nodes (9): page_cover(), card(), compass(), hemicycle(), pc(), seatrow(), volbar(), main() (+1 more)

### Community 12 - "da_conversion.py"
Cohesion: 0.20
Nodes (8): conversion(), main(), rows_for(), summary(), main(), panel(), profile(), strength()

### Community 13 - "pathlib"
Cohesion: 0.09
Nodes (9): main(), ballots(), strategies(), build(), da_plan(), extend(), launch_idx(), mu_function() (+1 more)

### Community 14 - "snapshots.py"
Cohesion: 0.13
Nodes (13): main(), agg(), fq(), prepare(), score(), table(), agg_level(), main() (+5 more)

### Community 15 - "Design System: Parlamento de la demanda"
Cohesion: 0.08
Nodes (24): Brújula política, Buttons, Chips / filtros, Colors, Components, Design System: Parlamento de la demanda, Do:, Do's and Don'ts (+16 more)

### Community 16 - "ideo_infografia.py"
Cohesion: 0.33
Nodes (9): flow(), ideas_rows(), key(), main(), page1(), page2(), party_card(), voters() (+1 more)

### Community 17 - "infografia.py"
Cohesion: 0.15
Nodes (18): bar_chart(), card(), chart_cuts(), chart_frag_season(), chart_mu_season(), chart_trend_windows(), charts_for(), legend() (+10 more)

### Community 18 - "json"
Cohesion: 0.22
Nodes (5): main(), main(), evaluate(), main(), vote()

### Community 19 - "ideo_brujulas6.py"
Cohesion: 0.29
Nodes (7): flagged(), index(), main(), position(), twin(), load(), main()

### Community 20 - "numpy"
Cohesion: 0.16
Nodes (9): main(), main(), twin(), choose(), evaluate(), main(), peer_groups(), scores() (+1 more)

### Community 21 - "votes_report.py"
Cohesion: 0.25
Nodes (12): Hemiciclo (componente firma), card(), chip(), hemicycle(), lectura(), legend(), main(), n0() (+4 more)

### Community 22 - "tracking.py"
Cohesion: 0.26
Nodes (7): calib_ratio(), chain(), base_fc(), load(), main(), rule_matrix(), score()

### Community 23 - "mu_backtest.py"
Cohesion: 0.20
Nodes (9): da_known(), evaluate(), load(), main(), season_index(), techniques(), main(), forecast() (+1 more)

### Community 24 - "ideo_vs_cons.py"
Cohesion: 0.18
Nodes (9): main(), metrics(), find(), fixed_ids(), fid(), main(), table(), vote() (+1 more)

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

### Community 29 - "house_compare.py"
Cohesion: 0.32
Nodes (10): central_mask(), frag_rule(), fragrances(), main(), makeup(), mu_rule(), segments(), summarize() (+2 more)

### Community 30 - "Reporte votación de reglas"
Cohesion: 0.36
Nodes (8): card(), chip(), hemicycle(), legend(), main(), page(), rules_box(), volbar()

### Community 31 - "Parlamento HTML (plantilla)"
Cohesion: 0.29
Nodes (8): Hemiciclo de escanos (reporte), camara(), /*__DATA__*/ placeholder (parlamento_html.py), Parlamento de la demanda (template), hemicycle(), resultados(), seats(), volbar()

### Community 32 - "Product"
Cohesion: 0.18
Nodes (10): Brand Commitments, Capabilities and Constraints, Evidence on Hand, Operating Context, Platform, Positioning, Product, Product Principles (+2 more)

### Community 33 - "parliament.py"
Cohesion: 0.53
Nodes (4): build(), main(), records(), tally()

### Community 34 - "Reporte del parlamento"
Cohesion: 0.42
Nodes (8): card(), dot(), hemicycle(), legend(), main(), page(), seatrow(), volbar()

### Community 35 - "Regla fragancias y DAs"
Cohesion: 0.33
Nodes (4): Central vs Local (6 meses de envios), ideo_panel.da_plan, Estrategia de forecast Fragancias, src/ptype.py y MAPEO_TAMANOS_FRAGANCIAS.csv

### Community 36 - "parlamento_html.py"
Cohesion: 0.17
Nodes (7): is_prompt(), main(), problems(), compass_points(), example(), main(), spread()

### Community 38 - "DNI del EAN y 3 preguntas"
Cohesion: 0.29
Nodes (5): DNI del EAN, Edad del EAN (tramos 6-11,12-17,18-25,26+), Fase del EAN (crecimiento/estable/declive), Bandera isf (Ignore System Forecast), brujulas()

### Community 39 - "votes.py"
Cohesion: 0.60
Nodes (3): ean_votes(), main(), tally()

### Community 40 - "Estacionalidad makeup"
Cohesion: 0.36
Nodes (4): analyse(), main(), shares(), summary()

### Community 41 - "Check de herramientas"
Cohesion: 0.52
Nodes (5): PATH, plugin_row(), row(), check-tools.sh script, skill_row()

### Community 45 - "pandas"
Cohesion: 0.26
Nodes (5): load(), load(), main(), summary(), wm()

### Community 46 - "describe"
Cohesion: 0.24
Nodes (8): describe(), objective(), select_forms(), best_in(), lloyd(), select6(), best_in(), lloyd()

## Knowledge Gaps
- **22 isolated node(s):** `PATH`, `PATH`, `Forecast Value Added contra metodo ingenuo`, `Estee Lauder 10-K FY2025`, `Revisiting the value of data sharing (IJOPM 2025)` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 249 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `line()` connect `Reporte de patrones EPOS` to `Design System: Parlamento de la demanda`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **What connects `PATH`, `PATH`, `Forecast Value Added contra metodo ingenuo` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `multivote.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14153846153846153 - nodes in this community are weakly interconnected._
- **Why does `Elevation & Depth` connect `Design System: Parlamento de la demanda` to `Reporte de patrones EPOS`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Should `six_multi.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09302325581395349 - nodes in this community are weakly interconnected._
- **Should `ideo_parties.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13105413105413105 - nodes in this community are weakly interconnected._
- **Should `Parlamento de 6 y consenso` be split into smaller, more focused modules?**
  _Cohesion score 0.12648221343873517 - nodes in this community are weakly interconnected._