#!/bin/bash
# UserPromptSubmit: en cada mensaje del usuario recuerda que es una tarea nueva y qué skills cargar (lo que imprime entra en el contexto).
# Antes del recordatorio revisa que todas las skills funcionan (skills-health.py, < 1 s); si algo falla, lo dice y pide parar.
python3 "$(dirname "$0")/skills-health.py" --short 2>&1 || true
# Ponytail solo en código puro: lee el mensaje (stdin) y lo enciende o apaga (ponytail-switch.py).
python3 "$(dirname "$0")/ponytail-switch.py" 2>/dev/null || true
cat <<'EOF'
[Recordatorio de skills — DP_polar] Este mensaje es una tarea nueva: lo cargado antes en la conversación no cuenta.
Antes de trabajar, carga con la herramienta Skill las que encajen (.claude/CLAUDE.md, tabla «Skills en cada tarea»):
- Código Python: code-review-and-quality (+ ponytail, solo si la línea de arriba dice PONYTAIL ACTIVO) y un assert en cada script nuevo.
- HTML/página/reporte (Ponytail apagado): artifact-design, impeccable (con PRODUCT.md y DESIGN.md), una de Taste (design-taste-frontend o high-end-visual-design) y una de Emil (emil-design-eng); al final `impeccable detect`.
- Gráficos/colores: dataviz (validar todos los colores nuevos). Animación: animate + emil-design-eng. Página con datos/filtros: performance-optimization.
- Preguntas sobre el código o dónde está algo: graphify query primero (grafo en graphify-out/, se actualiza al arrancar). OmniRoute: no operativo (sin servidor ni API keys).
Termina SIEMPRE la respuesta con esta línea, nombrando las 7:
Skills y plugins: Ponytail (…) · Agent Skills (…) · OmniRoute (…) · Graphify (…) · Taste (…) · Impeccable (…) · Emil (…)
con «usado: qué skill» o «no aplica: motivo» en cada una. Un hook de Stop lo comprueba.
EOF
