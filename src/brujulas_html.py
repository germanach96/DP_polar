"""Página única con las tres brújulas políticas: dónde cae cada partido por su receta y qué lado de cada eje habría acertado
más con cada EAN en FY26. Lee work/explorador.json (src/explorador_data.py) y work/ideo_brujulas6.json (recetas de los partidos).
Salida: reportes/BRUJULAS.html (un archivo, sin internet; mismo sistema visual que DESIGN.md)."""
import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ideo_brujulas6 as b6  # noqa

ROOT = Path(__file__).resolve().parents[1]; W = ROOT / "work"
OUT = ROOT / "reportes" / "BRUJULAS.html"


def main():
    E = json.loads((W / "explorador.json").read_text())
    I = json.loads((W / "ideo_brujulas6.json").read_text())
    idea = dict(zip(I["nombres"], I["ideas"]))
    assert set(idea) == set(E["parties"]), "las recetas no cubren los 6 partidos"
    D = dict(parties=E["parties"], colors=[b6.COL6[p] for p in E["parties"]], markers=E["markers"], stats=E["stats"],
             ideas=[idea[p] for p in E["parties"]],
             eans=[[e["v"], e["d"], e["h"], [round(x, 3) for x in e["pos"]]] for e in E["eans"] if e.get("pos")])
    assert all(len(e[3]) == 6 for e in D["eans"]), "cada EAN necesita 6 coordenadas (3 brújulas × 2 ejes)"
    tpl = (Path(__file__).parent / "brujulas_template.html").read_text(encoding="utf-8")
    font = base64.b64encode((Path(__file__).parent / "fonts" / "inter-latin-opsz-normal.woff2").read_bytes()).decode()  # Inter (OFL): reserva de SF Pro, sin internet
    page = tpl.replace("/*__FONT__*/", font).replace("/*__DATA__*/null", json.dumps(D, ensure_ascii=False, separators=(",", ":")))
    assert "/*__FONT__*/" not in page and "/*__DATA__*/" not in page
    OUT.write_text("<!doctype html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>"
                   f"</head><body>{page}</body></html>", encoding="utf-8")
    print(OUT, f"{OUT.stat().st_size / 1e6:.2f} MB ·", len(D["eans"]), "EANs")


if __name__ == "__main__":
    main()
