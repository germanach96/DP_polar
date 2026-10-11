#!/usr/bin/env python3
"""Revisa que TODAS las skills y plugins funcionan, no solo que están instalados.

- Cada SKILL.md (repo y plugins) se abre y debe tener frontmatter con name y description.
- Pruebas reales: Impeccable analiza un HTML mínimo, Graphify responde una consulta,
  Ponytail tiene sus skills. OmniRoute se informa como no operativo (acordado 2026-10-11).
Uso: skills-health.py [--short]   (salida 1 si algo falla). Lo llaman check-tools.sh y skills-reminder.sh.
"""
import json, os, re, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
SK = ROOT / ".claude" / "skills"
PLUG = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
os.environ["PATH"] = str(Path.home() / ".local/bin") + os.pathsep + os.environ.get("PATH", "")
GROUPS = {"addyosmani/agent-skills": "Agent Skills", "Leonxlnx/taste-skill": "Taste", "emilkowalski/skill": "Emil"}


def skill_ok(p: Path):
    """None si el SKILL.md es válido; si no, el motivo."""
    try:
        txt = p.read_text(encoding="utf-8")
    except OSError as e:
        return f"no se puede leer ({e.strerror})"
    m = re.match(r"---\s*\n(.*?)\n---", txt, re.S)
    if not m:
        return "sin frontmatter"
    miss = [k for k in ("name", "description") if not re.search(rf"^{k}:\s*\S", m.group(1), re.M)]
    return f"frontmatter sin {', '.join(miss)}" if miss else None


def run(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
        return r.returncode, r.stdout
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)


def plugin_dir(name):
    try:
        d = json.loads(PLUG.read_text())["plugins"].get(f"{name}@{name}")
        return Path(d[0]["installPath"]) if d else None
    except (OSError, ValueError, KeyError):
        return None


def check():
    rows, lock = [], json.loads((ROOT / "skills-lock.json").read_text())["skills"]
    # skills del repo, agrupadas por origen; cada una revisada
    for src, label in GROUPS.items():
        names = [n for n, v in lock.items() if v["source"] == src]
        bad = {n: skill_ok(SK / n / "SKILL.md") for n in names}
        bad = {n: r for n, r in bad.items() if r}
        rows.append((label, not bad and bool(names), f"{len(names) - len(bad)} de {len(names)} skills revisadas" + (": " + "; ".join(f"{n} {r}" for n, r in bad.items()) if bad else "")))
    # plugins: sus skills + prueba real
    for label, name in (("Ponytail", "ponytail"), ("Impeccable", "impeccable")):
        d = plugin_dir(name)
        files = sorted(d.glob("skills/*/SKILL.md")) if d else []
        bad = [f"{f.parent.name} {r}" for f in files if (r := skill_ok(f))]
        ok, det = bool(files) and not bad, f"{len(files) - len(bad)} skills del plugin revisadas" if files else "plugin no instalado"
        if ok and name == "impeccable":
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as t:
                t.write("<p>x</p>")
            rc, out = run([str(d / "skills/impeccable/scripts/impeccable"), "detect", "--json", t.name])
            os.unlink(t.name)
            ok = rc == 0 and out.strip().startswith("[")
            det += "; detect responde" if ok else "; detect NO responde"
        rows.append((label, ok, det + (": " + "; ".join(bad) if bad else "")))
    # graphify: skill + consulta real al grafo
    r = skill_ok(SK / "graphify" / "SKILL.md")
    rc, out = run(["graphify", "query", "parlamento", "--budget", "50"]) if not r else (1, "")
    ok = not r and rc == 0 and "Graph:" in out
    rows.append(("Graphify", ok, "skill revisada; graphify query responde" if ok else f"falla: {r or 'graphify query no responde (falta CLI o graphify-out/graph.json)'}"))
    rows.append(("OmniRoute", None, "no operativo: sin servidor ni API keys (acordado, no bloquea)"))
    return rows


if __name__ == "__main__":
    rows = check()
    assert {r[0] for r in rows} == {"Ponytail", "Agent Skills", "OmniRoute", "Graphify", "Taste", "Impeccable", "Emil"}, "faltan herramientas en la revisión"
    bad = [r for r in rows if r[1] is False]
    if "--short" in sys.argv:
        print("Revisión de skills: " + ("todas funcionan (" + " · ".join(f"{l} OK" for l, o, _ in rows if o) + "; OmniRoute no operativo)." if not bad
              else "FALLA " + " · ".join(f"{l}: {d}" for l, _, d in bad) + ". PARA: dile al usuario qué falta y no sigas con la tarea."))
    else:
        for label, ok, det in rows:
            print(f"| {label} | {'OK' if ok else 'NO OPERATIVO' if ok is None else 'FALLA'} | {det} |")
    sys.exit(1 if bad else 0)
