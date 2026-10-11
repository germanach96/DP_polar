#!/usr/bin/env python3
"""Stop: no deja terminar el turno si la respuesta no da cuenta de las 7 skills/plugins de la lista, o si se escribió HTML o Python
sin cargar sus skills (.claude/CLAUDE.md, «Skills en cada tarea»). Ante cualquier error deja pasar: un hook roto no debe bloquear la sesión."""
import json
import sys

TOOLS = ["Ponytail", "Agent Skills", "OmniRoute", "Graphify", "Taste", "Impeccable", "Emil"]
TASTE = {"design-taste-frontend", "design-taste-frontend-v1", "high-end-visual-design", "minimalist-ui", "industrial-brutalist-ui",
         "redesign-existing-projects", "gpt-taste", "stitch-design-taste", "image-to-code"}
REVIEW = {"code-review-and-quality", "ponytail:ponytail-review", "code-review", "simplify"}


def is_prompt(e):
    """Mensaje escrito por el usuario (no un resultado de herramienta)."""
    if e.get("type") != "user":
        return False
    c = e.get("message", {}).get("content")
    return isinstance(c, str) or (any(b.get("type") == "text" for b in c) and not any(b.get("type") == "tool_result" for b in c))


def problems(lines):
    start = max([i for i, e in enumerate(lines) if is_prompt(e)], default=-1)
    skills, files, last = set(), [], ""
    for e in lines[start + 1:]:
        if e.get("type") != "assistant":
            continue
        for b in e.get("message", {}).get("content", []):
            if b.get("type") == "tool_use":
                inp = b.get("input", {})
                if b.get("name") == "Skill":
                    skills.add(inp.get("skill", ""))
                if b.get("name") in ("Write", "Edit") and inp.get("file_path"):
                    files.append(inp["file_path"])
            elif b.get("type") == "text" and b.get("text", "").strip():
                last = b["text"]
    out = []
    tail = last[last.find("Skills y plugins"):] if "Skills y plugins" in last else ""
    miss = [t for t in TOOLS if t.lower() not in tail.lower()]
    if miss:
        out.append("Falta la línea final «Skills y plugins: …» con las 7 (usado / no aplica: motivo). Sin nombrar: " + ", ".join(miss) + ".")
    if any(f.endswith((".html", ".css", ".svg")) for f in files):
        need = [n for n, ok in [("impeccable", bool({"impeccable", "impeccable:impeccable"} & skills)),
                                ("una skill de Taste", bool(TASTE & skills))] if not ok]
        if need:
            out.append("Se escribió HTML/CSS/SVG sin cargar con Skill: " + ", ".join(need) + ".")
    if any(f.endswith(".py") for f in files) and not REVIEW & skills:
        out.append("Se escribió Python sin cargar code-review-and-quality (o ponytail:ponytail-review) para revisarlo.")
    return out


def main():
    d = json.load(sys.stdin)
    if d.get("stop_hook_active"):          # ya bloqueó una vez en este turno: no entrar en bucle
        return
    lines = [json.loads(x) for x in open(d["transcript_path"], encoding="utf-8") if x.strip()]
    p = problems(lines)
    if p:
        print(json.dumps({"decision": "block", "reason": "Check de skills (DP_polar): " + " ".join(p) + " Corrígelo y termina con la línea."}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
