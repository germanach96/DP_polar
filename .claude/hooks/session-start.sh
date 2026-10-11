#!/bin/bash
# Arranque de cada sesión: instala lo que falte de las skills y plugins del proyecto
# y deja un informe (stdout -> contexto de Claude) con el estado de cada uno.
# Idempotente y no interactivo. Si una instalación falla, no corta la sesión: lo marca en el informe.
set -uo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
LOG="/tmp/session-start-tools.log"
: > "$LOG"
export PATH="$HOME/.local/bin:$PATH"

# ---------- instalar lo que falte ----------
if ! command -v graphify >/dev/null 2>&1; then
  command -v uv >/dev/null 2>&1 && uv tool install graphifyy >>"$LOG" 2>&1
fi
if ! command -v omniroute >/dev/null 2>&1; then
  npm install -g omniroute >>"$LOG" 2>&1
fi
if command -v claude >/dev/null 2>&1; then
  for spec in "ponytail DietrichGebert/ponytail" "impeccable pbakaus/impeccable"; do
    set -- $spec
    if ! grep -q "\"$1@$1\"" "$HOME/.claude/plugins/installed_plugins.json" 2>/dev/null; then
      timeout 180 claude plugin marketplace add "$2" >>"$LOG" 2>&1
      timeout 180 claude plugin install "$1@$1" >>"$LOG" 2>&1
    fi
  done
fi

# ---------- informe ----------
"$ROOT/.claude/hooks/check-tools.sh"
exit 0
