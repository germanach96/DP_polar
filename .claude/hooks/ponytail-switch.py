#!/usr/bin/env python3
"""UserPromptSubmit: en cada mensaje Ponytail empieza apagado y Claude pregunta al usuario si lo activa.

Lee el mensaje del usuario (JSON por stdin), apaga el flag del plugin (el que usan su barra de estado y sus
subagentes) e imprime la orden de preguntar, con una recomendación por palabras clave (código puro → Sí).
Si el mensaje ya lo dice («con ponytail» / «sin ponytail»), aplica eso y no pregunta.
Tras la respuesta, Claude fija el modo con: python3 .claude/hooks/ponytail-switch.py --set full|off
Si el usuario usa los comandos propios del plugin (/ponytail…, «stop ponytail», «normal mode»), no toca nada.
Si algo falla, no bloquea: sale sin imprimir.
"""
import hashlib, json, os, re, sys, unicodedata

DESIGN = r"html|css|svg|pdf|reportes?|report|paginas?|page|disen\w*|design|visual\w*|graficos?|grafica|chart|colou?r\w*|hemiciclo|explorador|infografia|animaci\w*|animat\w*|interfaz|ui|ux|estilo|tipograf\w*|layout|maqueta|dashboard|tarjetas?|brujulas?|capturas?|plantilla|template|presentacion|slides?|artifact|impeccable|taste|emil|dataviz"
CODE = r"python|scripts?|codigo|code|\w+\.py|funcion\w*|bugs?|errores?|tests?|refactor\w*|src|pandas|statsmodels|hooks?|regenerar|backtest|parquet|assert|depurar|debug"
OFF = ("Mientras esté apagado, ignora las reglas de Ponytail del arranque: mandan las skills de la tarea "
       "(Impeccable, Taste, Emil, dataviz, Agent Skills) y DESIGN.md; nada de recortar pulido ni pasos por «lo mínimo».")


def norm(text):
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))


def mode_for(prompt):
    """Recomendación: full si habla de código y de nada visual; si no, off."""
    p = norm(prompt)
    has = lambda pat: re.search(rf"\b(?:{pat})\b", p) is not None
    return "full" if has(CODE) and not has(DESIGN) else "off"


def explicit(p):
    """«con ponytail» → full, «sin ponytail» → off; si no lo dice, None."""
    m = re.search(r"\b(con|sin)\s+ponytail\b", p)
    return None if not m else ("full" if m.group(1) == "con" else "off")


def flag_files():
    claude = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")
    files = [os.path.join(claude, ".ponytail-active")]
    project = os.environ.get("CLAUDE_PROJECT_DIR", "").strip() or os.getcwd()
    # misma clave que ponytail-runtime.js: sha256 de la ruta del proyecto
    key = hashlib.sha256(os.path.normpath(project).encode()).hexdigest()
    files.append(os.path.join(claude, "ponytail-modes", key))
    return files


def set_mode(mode):
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


def main():
    prompt = json.loads(sys.stdin.read().lstrip("﻿") or "{}").get("prompt", "")
    p = norm(prompt).strip()
    if re.match(r"^[/@$]ponytail", p) or p.rstrip(".!? ") in ("stop ponytail", "normal mode"):
        return  # el comando lo gestiona el propio plugin
    said = explicit(p)
    set_mode(said or "off")
    if said == "full":
        print("PONYTAIL ACTIVO — level: full (lo pidió el usuario en el mensaje): aplica sus reglas.")
    elif said == "off":
        print("PONYTAIL APAGADO (lo pidió el usuario en el mensaje). " + OFF)
    else:
        reco = "Sí (parece código puro)" if mode_for(prompt) == "full" else "No (no es código puro: diseño, análisis o pregunta)"
        print("PONYTAIL: PREGUNTAR. Antes de hacer nada, pregunta al usuario con AskUserQuestion «¿Activo Ponytail en esta tarea?» "
              f"con las opciones Sí / No; recomendado: {reco}, ponlo primero con «(Recomendado)». "
              "Después fija el modo con `python3 .claude/hooks/ponytail-switch.py --set full` (Sí) o `--set off` (No). "
              "Hasta la respuesta está apagado. " + OFF)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--set"]:
        assert sys.argv[2:] in (["full"], ["off"]), "uso: --set full|off"
        set_mode(sys.argv[2])
        print("PONYTAIL ACTIVO — level: full" if sys.argv[2] == "full" else "PONYTAIL APAGADO")
        sys.exit(0)
    if sys.argv[1:] == ["--selftest"]:
        assert mode_for("arregla el bug de src/panel.py") == "full"
        assert mode_for("refactoriza el script de pandas") == "full"
        assert mode_for("mejora el diseño del reporte PDF") == "off"
        assert mode_for("cambia los colores del hemiciclo en el script") == "off"  # diseño gana
        assert mode_for("¿qué partido gana en Gucci?") == "off"  # pregunta de negocio
        assert mode_for("quiero que me cuides la UI") == "off" and mode_for("cuidado con el código") == "full"
        assert explicit("hazlo con ponytail") == "full" and explicit("sin ponytail, por favor") == "off"
        assert explicit("rediseña el explorador") is None
        print("ok")
        sys.exit(0)
    try:
        main()
    except Exception:
        pass
