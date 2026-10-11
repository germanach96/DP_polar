# Graph Report - DP_polar  (2026-10-11)

## Corpus Check
- 83 files · ~123,269 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .csv 1)

## Summary
- 795 nodes · 2287 edges · 51 communities (47 shown, 4 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 82 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0c1ce0cb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DAs y horizonte 9M
- Ciclo de vida y decisión sep-25
- Selección de partidos (ideologías)
- Reporte de ideologías
- Pruebas de cortes y lanzamientos
- Parlamento de 6 y consenso
- Reporte de patrones EPOS
- Diagnóstico EPOS
- Infografía de 6 partidos
- Banco de métodos v1-v2
- Investigación: coalición y EPOS
- Piezas visuales (ideo_viz)
- Carga de datos y lanzamientos
- Trend de grupo
- Descriptivos y métricas
- Backtest y forecast final
- Infografía de ideologías
- Infografía de reglas
- Generadores HTML (EPOS, explorador)
- Brújulas de 6 partidos
- Parlamento de 6 (votación)
- Reporte de votación
- Tracking encadenado
- Patrón envío-EPOS
- Número de partidos y vs consenso
- Explorador (plantilla)
- Reporte por casa
- Regla makeup y cortes
- Skills y plugins
- Patrones EPOS (cálculo)
- Reporte votación de reglas
- Parlamento HTML (plantilla)
- Banco de métodos v3 (EPOS)
- Regla por edad con EPOS
- Reporte del parlamento
- Regla fragancias y DAs
- Parlamento HTML (generador)
- Reporte WAPE90
- DNI del EAN y 3 preguntas
- Reporte de backtest
- Estacionalidad makeup
- Check de herramientas
- Conversión de DAs
- Control de skills (Stop)
- Parlamento vs consenso
- Evaluación por foto
- Partidos por forma de base
- Panel EAN x mes
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
- `drawhemi()` --implements--> `Hemiciclo de escanos (reporte)`  [INFERRED]
  src/explorador_template.html → CLAUDE.md
- `drawtrends()` --references--> `EPOS (sell-out desde jul-24)`  [INFERRED]
  src/explorador_template.html → CLAUDE.md
- `Explorador del parlamento (template)` --conceptually_related_to--> `Check obligatorio de skills y plugins`  [INFERRED]
  src/explorador_template.html → .claude/CLAUDE.md
- `Contexto del proyecto (CLAUDE.md)` --references--> `Skills y plugins check (.claude/CLAUDE.md)`  [EXTRACTED]
  CLAUDE.md → .claude/CLAUDE.md
- `Parlamento de la demanda (template)` --conceptually_related_to--> `Check obligatorio de skills y plugins`  [INFERRED]
  src/parlamento_template.html → .claude/CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Los 6 partidos del parlamento vigente** — claude_regla_fragancias, claude_regla_makeup, claude_ciclo_de_vida, claude_media_6m_prudente, claude_media_6m_estacional, claude_media_12m_estacional [EXTRACTED 1.00]
- **Renderizado del hemiciclo en reportes HTML** — src_parlamento_template_hemicycle, src_parlamento_template_seats, src_explorador_template_drawhemi, src_explorador_template_seats, claude_hemiciclo [INFERRED 0.85]
- **Flujo sell-in desde sell-out con EPOS** — claude_epos, claude_regla_por_edad, claude_partido_consumidor_epos, claude_semaforo_carga, investigacion_demand_planning_sell_in_desde_sell_out [INFERRED 0.85]

## Communities (51 total, 4 thin omitted)

### Community 0 - "DAs y horizonte 9M"
Cohesion: 0.06
Nodes (48): da_known(), main(), fragrances(), main(), makeup(), rows_for(), central_mask(), frag_rule() (+40 more)

### Community 1 - "Ciclo de vida y decisión sep-25"
Cohesion: 0.06
Nodes (29): main(), main(), main(), scores(), show(), brujulas(), main(), main() (+21 more)

### Community 2 - "Selección de partidos (ideologías)"
Cohesion: 0.13
Nodes (19): axis_scores(), complexity(), describe(), dist_to(), elect_summary(), election(), excel(), ideas() (+11 more)

### Community 3 - "Reporte de ideologías"
Cohesion: 0.15
Nodes (21): cards_page(), compass_pts(), compasses(), curve_chart(), floor_chart(), hbars(), load(), main() (+13 more)

### Community 4 - "Pruebas de cortes y lanzamientos"
Cohesion: 0.17
Nodes (10): main(), main(), ets_damped(), ets_damped_house_share(), g_median(), g_trimmed(), naive(), _ratios() (+2 more)

### Community 5 - "Parlamento de 6 y consenso"
Cohesion: 0.13
Nodes (16): Consenso de o9 (cons), Decision sep-25: Ciclo de vida para todos, Contexto del proyecto (CLAUDE.md), Media 12M estacional, Media 6M estacional, Media 6M prudente, Trend YoY 6M plano (metodo actual del equipo), WAPE90 (+8 more)

### Community 6 - "Reporte de patrones EPOS"
Cohesion: 0.21
Nodes (20): axis_y(), cohort_bars(), cover(), dumbbell(), exits_chart(), launch_chart(), lerp(), line() (+12 more)

### Community 7 - "Diagnóstico EPOS"
Cohesion: 0.14
Nodes (13): caps(), channel(), coverage(), house_next(), load_effect(), main(), panel(), predictive() (+5 more)

### Community 8 - "Infografía de 6 partidos"
Cohesion: 0.14
Nodes (11): P6, legend(), card(), main(), voters(), bars(), cards_page(), flag_share() (+3 more)

### Community 9 - "Banco de métodos v1-v2"
Cohesion: 0.16
Nodes (15): method_registry(), method_registry_v2(), make_blend_trend(), make_clean_trend(), make_combo(), make_cut_adjusted(), make_damped_group(), f() (+7 more)

### Community 10 - "Investigación: coalición y EPOS"
Cohesion: 0.16
Nodes (16): Partido Consumidor (EPOS) (proximo paso), Semaforo de carga del canal, WOS (semanas de stock), Conversion de DAs planificados (42% fragancias, 80% makeup), Ajustes manuales positivos empeoran (Fildes 2025), Cross-learning y conciliacion de niveles, Investigacion demand planning, Estee Lauder 10-K FY2025 (+8 more)

### Community 11 - "Piezas visuales (ideo_viz)"
Cohesion: 0.18
Nodes (9): page_cover(), card(), compass(), hemicycle(), pc(), seatrow(), volbar(), main() (+1 more)

### Community 12 - "Carga de datos y lanzamientos"
Cohesion: 0.16
Nodes (8): consensus_rows(), main(), load(), load(), main(), panel(), profile(), strength()

### Community 13 - "Trend de grupo"
Cohesion: 0.22
Nodes (17): main(), main(), _apply(), clean_history(), g_flat(), _group_g(), _ly(), f() (+9 more)

### Community 14 - "Descriptivos y métricas"
Cohesion: 0.18
Nodes (9): main(), agg(), fq(), prepare(), main(), month_factors(), rules(), snapshot_ctx() (+1 more)

### Community 15 - "Backtest y forecast final"
Cohesion: 0.17
Nodes (9): context(), method_registry_v4(), run(), bands(), main(), make_group_trend_clean(), f(), make_resc_general() (+1 more)

### Community 16 - "Infografía de ideologías"
Cohesion: 0.19
Nodes (10): flow(), ideas_rows(), key(), main(), page1(), page2(), party_card(), voters() (+2 more)

### Community 17 - "Infografía de reglas"
Cohesion: 0.24
Nodes (12): bar_chart(), card(), chart_cuts(), chart_frag_season(), chart_mu_season(), chart_trend_windows(), charts_for(), legend() (+4 more)

### Community 18 - "Generadores HTML (EPOS, explorador)"
Cohesion: 0.20
Nodes (5): main(), main(), main(), twin(), fid()

### Community 19 - "Brújulas de 6 partidos"
Cohesion: 0.21
Nodes (8): flagged(), index(), main(), position(), twin(), main(), load(), main()

### Community 20 - "Parlamento de 6 (votación)"
Cohesion: 0.20
Nodes (9): objective(), choose(), evaluate(), main(), peer_groups(), scores(), select6(), best_in() (+1 more)

### Community 21 - "Reporte de votación"
Cohesion: 0.28
Nodes (11): card(), chip(), hemicycle(), lectura(), legend(), main(), n0(), page() (+3 more)

### Community 22 - "Tracking encadenado"
Cohesion: 0.25
Nodes (7): calib_ratio(), chain(), base_fc(), load(), main(), rule_matrix(), score()

### Community 23 - "Patrón envío-EPOS"
Cohesion: 0.24
Nodes (9): agg(), constancy(), events(), load_build(), load_section(), main(), regress(), table() (+1 more)

### Community 24 - "Número de partidos y vs consenso"
Cohesion: 0.22
Nodes (8): main(), metrics(), find(), fixed_ids(), main(), table(), vote(), with_da()

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

### Community 29 - "Patrones EPOS (cálculo)"
Cohesion: 0.31
Nodes (8): launch_curves(), launches(), load_and_exits(), main(), mature_set(), noise(), trend(), veterans()

### Community 30 - "Reporte votación de reglas"
Cohesion: 0.36
Nodes (8): card(), chip(), hemicycle(), legend(), main(), page(), rules_box(), volbar()

### Community 31 - "Parlamento HTML (plantilla)"
Cohesion: 0.29
Nodes (8): Hemiciclo de escanos (reporte), camara(), /*__DATA__*/ placeholder (parlamento_html.py), Parlamento de la demanda (template), hemicycle(), resultados(), seats(), volbar()

### Community 32 - "Banco de métodos v3 (EPOS)"
Cohesion: 0.20
Nodes (6): method_registry_v3(), make_clean_rescaled(), make_epos_group(), make_group_lfl(), make_young_level(), f()

### Community 33 - "Regla por edad con EPOS"
Cohesion: 0.31
Nodes (6): age_ratio(), main(), profile(), score(), test_vet(), test_young()

### Community 34 - "Reporte del parlamento"
Cohesion: 0.42
Nodes (8): card(), dot(), hemicycle(), legend(), main(), page(), seatrow(), volbar()

### Community 35 - "Regla fragancias y DAs"
Cohesion: 0.33
Nodes (4): Central vs Local (6 meses de envios), ideo_panel.da_plan, Estrategia de forecast Fragancias, src/ptype.py y MAPEO_TAMANOS_FRAGANCIAS.csv

### Community 36 - "Parlamento HTML (generador)"
Cohesion: 0.31
Nodes (4): compass_points(), example(), main(), spread()

### Community 37 - "Reporte WAPE90"
Cohesion: 0.44
Nodes (6): bar_block(), cell(), get(), main(), n0(), pc()

### Community 38 - "DNI del EAN y 3 preguntas"
Cohesion: 0.29
Nodes (5): DNI del EAN, Edad del EAN (tramos 6-11,12-17,18-25,26+), Fase del EAN (crecimiento/estable/declive), Bandera isf (Ignore System Forecast), brujulas()

### Community 39 - "Reporte de backtest"
Cohesion: 0.36
Nodes (5): score(), table(), agg_level(), main(), md()

### Community 40 - "Estacionalidad makeup"
Cohesion: 0.36
Nodes (4): analyse(), main(), shares(), summary()

### Community 41 - "Check de herramientas"
Cohesion: 0.52
Nodes (5): PATH, plugin_row(), row(), check-tools.sh script, skill_row()

### Community 42 - "Conversión de DAs"
Cohesion: 0.43
Nodes (4): conversion(), main(), rows_for(), summary()

### Community 43 - "Control de skills (Stop)"
Cohesion: 0.47
Nodes (3): is_prompt(), main(), problems()

### Community 44 - "Parlamento vs consenso"
Cohesion: 0.47
Nodes (3): evaluate(), main(), vote()

### Community 45 - "Evaluación por foto"
Cohesion: 0.60
Nodes (3): main(), summary(), wm()

### Community 46 - "Partidos por forma de base"
Cohesion: 0.67
Nodes (3): select_forms(), best_in(), lloyd()

## Knowledge Gaps
- **22 isolated node(s):** `PATH`, `PATH`, `Forecast Value Added contra metodo ingenuo`, `Estee Lauder 10-K FY2025`, `Revisiting the value of data sharing (IJOPM 2025)` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 220 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `Piezas visuales (ideo_viz)` to `Ciclo de vida y decisión sep-25`, `Pruebas de cortes y lanzamientos`, `Infografía de 6 partidos`, `Carga de datos y lanzamientos`, `Generadores HTML (EPOS, explorador)`, `Reporte votación de reglas`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **What connects `PATH`, `PATH`, `Forecast Value Added contra metodo ingenuo` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DAs y horizonte 9M` be split into smaller, more focused modules?**
  _Cohesion score 0.06419753086419754 - nodes in this community are weakly interconnected._
- **Why does `Contexto del proyecto (CLAUDE.md)` connect `Parlamento de 6 y consenso` to `Regla fragancias y DAs`, `DNI del EAN y 3 preguntas`, `Investigación: coalición y EPOS`, `Explorador (plantilla)`, `Regla makeup y cortes`, `Skills y plugins`, `Parlamento HTML (plantilla)`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Should `Ciclo de vida y decisión sep-25` be split into smaller, more focused modules?**
  _Cohesion score 0.06338028169014084 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `Infografía de 6 partidos` to `Pruebas de cortes y lanzamientos`, `Piezas visuales (ideo_viz)`, `Carga de datos y lanzamientos`, `Generadores HTML (EPOS, explorador)`, `Reporte votación de reglas`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Should `Selección de partidos (ideologías)` be split into smaller, more focused modules?**
  _Cohesion score 0.13227513227513227 - nodes in this community are weakly interconnected._