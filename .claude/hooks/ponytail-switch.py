#!/usr/bin/env python3
"""UserPromptSubmit: enciende Ponytail solo en tareas de código puro y lo apaga en el resto (diseño incluido).

Lee el mensaje del usuario (JSON por stdin), lo clasifica por palabras clave y:
- escribe el modo en el flag del plugin (el mismo que usan su barra de estado y sus subagentes);
- imprime una línea que entra en el contexto: «PONYTAIL ACTIVO» o «PONYTAIL APAGADO».
Si el usuario usa los comandos propios del plugin (/ponytail…, «stop ponytail», «normal mode»), no toca nada.
Si algo falla, no bloquea: sale sin imprimir.
"""
import hashlib, json, os, re, sys, unicodedata

DESIGN = r"html|css|svg|pdf|reportes?|report|paginas?|page|disen\w*|design|visual\w*|graficos?|grafica|chart|colou?r\w*|hemiciclo|explorador|infografia|animaci\w*|animat\w*|interfaz|ui|ux|estilo|tipograf\w*|layout|maqueta|dashboard|tarjetas?|brujulas?|capturas?|plantilla|template|presentacion|slides?|artifact|impeccable|taste|emil|dataviz"
CODE = r"python|scripts?|codigo|code|\w+\.py|funcion\w*|bugs?|errores?|tests?|refactor\w*|src|pandas|statsmodels|hooks?|regenerar|backtest|parquet|assert|depurar|debug"


def norm(text):
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))


def mode_for(prompt):
    p = norm(prompt)
    has = lambda pat: re.search(rf"\b(?:{pat})\b", p) is not None
    return "full" if has(CODE) and not has(DESIGN) else "off"


def flag_files():
    claude = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")
    files = [os.path.join(claude, ".ponytail-active")]
    project = os.environ.get("CLAUDE_PROJECT_DIR", "").strip()
    if project:  # misma clave que ponytail-runtime.js: sha256 de la ruta del proyecto
        key = hashlib.sha256(os.path.normpath(project).encode()).hexdigest()
        files.append(os.path.join(claude, "ponytail-modes", key))
    return files


def main():
    prompt = json.loads(sys.stdin.read().lstrip("﻿") or "{}").get("prompt", "")
    p = norm(prompt).strip()
    if re.match(r"^[/@$]ponytail", p) or p.rstrip(".!? ") in ("stop ponytail", "normal mode"):
        return  # el comando lo gestiona el propio plugin
    mode = mode_for(prompt)
    for f in flag_files():
        if mode == "off":
            try:
                os.unlink(f)
            except FileNotFoundError:
                pass
        else:
            os.makedirs(os.path.dirname(f), exist_ok=True)
            with open(f, "w") as fh:
                fh.write(mode)
    if mode == "off":
        print("PONYTAIL APAGADO en esta tarea (no es código puro): ignora las reglas de Ponytail del arranque. "
              "Mandan las skills de la tarea (Impeccable, Taste, Emil, dataviz, Agent Skills) y DESIGN.md; nada de recortar pulido ni pasos por «lo mínimo».")
    else:
        print("PONYTAIL ACTIVO — level: full (tarea de código puro): aplica sus reglas al código.")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        assert mode_for("arregla el bug de src/panel.py") == "full"
        assert mode_for("refactoriza el script de pandas") == "full"
        assert mode_for("mejora el diseño del reporte PDF") == "off"
        assert mode_for("cambia los colores del hemiciclo en el script") == "off"  # diseño gana
        assert mode_for("¿qué partido gana en Gucci?") == "off"  # pregunta de negocio
        assert mode_for("quiero que me cuides la UI") == "off" and mode_for("cuidado con el código") == "full"
        print("ok")
        sys.exit(0)
    try:
        main()
    except Exception:
        pass
