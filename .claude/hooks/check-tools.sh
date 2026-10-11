#!/bin/bash
# Comprueba las skills y plugins del proyecto y escribe una tabla de estado.
# Uso: .claude/hooks/check-tools.sh  (también lo llama session-start.sh)
set -uo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
SK="$ROOT/.claude/skills"
PJ="$HOME/.claude/plugins/installed_plugins.json"
export PATH="$HOME/.local/bin:$PATH"
FAIL=0

row() { printf '| %s | %s | %s |\n' "$1" "$2" "$3"; [ "$2" = "OK" ] || FAIL=1; }

# skills copiadas en el repo: todas las de skills-lock.json de ese origen deben tener SKILL.md
skills_from() {
  python3 - "$ROOT/skills-lock.json" "$SK" "$1" <<'EOF'
import json, sys, os
lock, sk, src = sys.argv[1:]
names = [n for n, v in json.load(open(lock))["skills"].items() if v["source"] == src]
miss = [n for n in names if not os.path.isfile(os.path.join(sk, n, "SKILL.md"))]
print(len(names), len(names) - len(miss), ",".join(miss))
EOF
}
skill_row() {
  read -r tot ok miss < <(skills_from "$2")
  if [ "$tot" -gt 0 ] && [ "$ok" = "$tot" ]; then row "$1" OK "$ok de $tot skills en .claude/skills"
  else row "$1" FALTA "$ok de $tot skills; faltan: ${miss:-todas}. Instalar: $3"; fi
}
plugin_row() {
  local path
  path=$(python3 -c "import json,sys;d=json.load(open('$PJ'))['plugins'].get('$2@$2');print(d[0]['installPath'] if d else '')" 2>/dev/null)
  if [ -n "$path" ] && [ -d "$path" ]; then
    row "$1" OK "plugin instalado (v$(basename "$path")); debe verse su skill /$2 en esta sesión"
  else row "$1" FALTA "plugin no instalado. Instalar: /plugin marketplace add $3 y /plugin install $2@$2"; fi
}

echo "## Check de skills y plugins (DP_polar)"
echo
echo "| Skill / plugin | Estado | Detalle |"
echo "|---|---|---|"
plugin_row "Ponytail" ponytail DietrichGebert/ponytail
skill_row "Agent Skills (addyosmani)" addyosmani/agent-skills "npx skills add addyosmani/agent-skills"
# OmniRoute: acordado con el usuario (2026-10-11) que hoy no se puede usar; se informa sin bloquear la sesión
if command -v omniroute >/dev/null 2>&1; then
  printf '| %s | %s | %s |\n' "OmniRoute" "NO OPERATIVO" "CLI v$(omniroute --version 2>/dev/null | tail -1) instalada, sin servidor ni API keys: no se usa (no bloquea)"
else printf '| %s | %s | %s |\n' "OmniRoute" "NO OPERATIVO" "CLI no instalada (npm install -g omniroute); sin servidor ni API keys no se usa (no bloquea)"; fi
if command -v graphify >/dev/null 2>&1 && [ -f "$SK/graphify/SKILL.md" ] && [ -f "$ROOT/graphify-out/graph.json" ]; then
  row "Graphify" OK "CLI, skill y grafo (graphify-out/graph.json, $(python3 -c "import json;d=json.load(open('$ROOT/graphify-out/graph.json'));print(len(d.get('nodes',[])))") nodos): usar graphify query para preguntas sobre el código"
elif command -v graphify >/dev/null 2>&1 && [ -f "$SK/graphify/SKILL.md" ]; then
  row "Graphify" FALTA "falta el grafo: correr /graphify . (con .graphifyignore del proyecto)"
else
  m=""; command -v graphify >/dev/null 2>&1 || m="CLI (uv tool install graphifyy)"; [ -f "$SK/graphify/SKILL.md" ] || m="$m skill (graphify install)"
  row "Graphify" FALTA "falta: $m"; fi
skill_row "Taste Skill (tasteskill.dev)" Leonxlnx/taste-skill "npx skills add Leonxlnx/taste-skill"
plugin_row "Impeccable (impeccable.style)" impeccable pbakaus/impeccable
skill_row "Emil Kowalski (emilkowal.ski/skill)" emilkowalski/skill "npx skills add emilkowalski/skill"
echo
if [ "$FAIL" = 0 ]; then echo "Resultado: todo instalado."
else echo "Resultado: FALTA algo. Detalle de instalación en /tmp/session-start-tools.log"; fi
