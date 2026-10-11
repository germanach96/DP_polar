#!/bin/bash
# UserPromptSubmit: en cada mensaje del usuario recuerda que es una tarea nueva y qué skills cargar (lo que imprime entra en el contexto).
cat <<'EOF'
[Recordatorio de skills — DP_polar] Este mensaje es una tarea nueva: lo cargado antes en la conversación no cuenta.
Antes de trabajar, carga con la herramienta Skill las que encajen (.claude/CLAUDE.md, tabla «Skills en cada tarea»):
- Código Python: code-review-and-quality (+ ponytail, ya activo) y un assert en cada script nuevo.
- HTML/página/reporte: artifact-design, impeccable y una de Taste (design-taste-frontend o high-end-visual-design); al final `impeccable detect`.
- Gráficos/colores: dataviz (validar todos los colores nuevos). Animación: animate + emil-design-eng. Página con datos/filtros: performance-optimization.
- Preguntas sobre el código: graphify. OmniRoute solo si hay servidor y API keys.
Termina SIEMPRE la respuesta con esta línea, nombrando las 7:
Skills y plugins: Ponytail (…) · Agent Skills (…) · OmniRoute (…) · Graphify (…) · Taste (…) · Impeccable (…) · Emil (…)
con «usado: qué skill» o «no aplica: motivo» en cada una. Un hook de Stop lo comprueba.
EOF
