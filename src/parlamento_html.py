"""Parlamento interactivo en HTML (didáctico, con animaciones): qué es, cómo se vota, los 6 partidos, sus brújulas, resultados y veredicto.
Usa lo mismo que el último reporte (src/ideologia_report.py → reportes/REPORTE_IDEOLOGIA.pdf): work/fy25_eleccion.json, decision_sep25.json,
fy25_brujulas.json, ideo_brujulas6.json. Los puntos de los EANs en las brújulas y el ejemplo de escrutinio se leen del HTML de ese reporte
(work/reporte_ideologia.html), así no hace falta regenerar los parquet.
Salida: reportes/PARLAMENTO.html (abrir en el navegador) y work/parlamento_artifact.html (mismo contenido sin el esqueleto <html>)."""
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ideo_brujulas6 as b6  # noqa
import ideologia_report as irp  # noqa  (LEMA y RESP de los partidos)

ROOT = Path(__file__).resolve().parents[1]; W = ROOT / "work"
TPL = Path(__file__).parent / "parlamento_template.html"
OUT = ROOT / "reportes" / "PARLAMENTO.html"
HZ = ["7–9", "4–6", "1–3", "total"]
# geometría de iv.compass en el reporte: w=330, h=420, márgenes 26/10/14/26, ejes ±1.14
ML, MT, PW, PH, LIM = 26, 14, 294, 380, 1.14


def compass_points(html):
    """Puntos de EAN de las 3 brújulas del reporte → [x1, y1, x2, y2, x3, y3, partido, volumen relativo]."""
    inv = {c: i for i, c in enumerate(b6.ORDER6) for c in [b6.COL6[c]]}
    svgs = [s for s in re.findall(r'<svg[^>]*class="cmp".*?</svg>', html, re.S)][:3]
    rx = r'<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)" fill="(#\w+)" fill-opacity=".55"'
    C = [re.findall(rx, s) for s in svgs]
    assert len(C) == 3 and len(C[0]) == len(C[1]) == len(C[2]) > 500, [len(c) for c in C]
    out = []
    for a, b, c in zip(*C):
        assert a[3] == b[3] == c[3] and a[2] == b[2] == c[2]   # mismo EAN en las 3 (mismo orden por volumen)
        xy = []
        for cx, cy, *_ in (a, b, c):
            xy += [round((float(cx) - ML) / PW * 2 * LIM - LIM, 3), round((1 - (float(cy) - MT) / PH) * 2 * LIM - LIM, 3)]
        out.append(xy + [inv[a[3]], round(((float(a[2]) - 1.3) / 4.2) ** 2, 4)])
    return out


def spread(pos, dmin=0.2):
    """Separa los marcadores de partido que se pisan (misma idea que iv.compass)."""
    C = {n: list(p) for n, p in pos.items()}
    ks = list(C)
    for _ in range(300):
        moved = False
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                a, b = C[ks[i]], C[ks[j]]
                dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy)
                if d < dmin:
                    if d < 1e-6:
                        dx, dy, d = 1.0, 0.3, 1.04
                    p = (dmin - d) / 2
                    a[0] -= dx / d * p; a[1] -= dy / d * p; b[0] += dx / d * p; b[1] += dy / d * p; moved = True
        for c in C.values():
            c[0] = min(max(c[0], -1.0), 1.0); c[1] = min(max(c[1], -1.0), 1.0)
        if not moved:
            break
    return {n: [round(C[n][0], 3), round(C[n][1], 3), round(pos[n][0], 3), round(pos[n][1], 3)] for n in C}


def example(html):
    """Escrutinio del EAN de ejemplo del reporte: urnas, error por partido y urna, forecast y real."""
    i = html.find("Ejemplo:"); seg = html[i:html.find("</table>", i) + 8]
    t = lambda s: re.sub(r"<[^>]+>", " ", s).split()
    name = re.sub(r"<[^>]+>", "", seg[: seg.find("</div>")]).replace("Ejemplo:", "").strip()
    urnas = [" ".join(t(h)) for h in re.findall(r"<th>(.*?)</th>", seg)[1:-2]]
    rows = {}
    for tr in re.findall(r"<tr class='[^']*'>(.*?)</tr>", seg):
        cells = [re.sub(r"<[^>]+>", "", c).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr)]
        nm = re.sub(r"^\d+", "", cells[0]).strip()
        rows[nm] = dict(err=[int(c.rstrip("%")) for c in cells[1:len(urnas) + 1]], fc=int(cells[-1].replace(".", "")))
    rest = re.sub(r"<[^>]+>", "", html[html.find("</table>", i): html.find("</table>", i) + 600])
    real = int(re.search(r"Real:\s*([\d.]+)", rest).group(1).replace(".", ""))
    ean = re.search(r"EAN (\d+)", seg).group(1)
    assert set(rows) == set(b6.NAMES) and len(urnas) == 6
    return dict(name=name, ean=ean, urnas=urnas, rows=rows, real=real)


def main():
    D = json.loads((W / "fy25_eleccion.json").read_text()); DS = json.loads((W / "decision_sep25.json").read_text())
    BS = json.loads((W / "fy25_brujulas.json").read_text()); Bj = json.loads((W / "ideo_brujulas6.json").read_text())
    html = (W / "reporte_ideologia.html").read_text(encoding="utf-8")
    pts = compass_points(html)
    fixed = {k: {n: [p * .86 for p in Bj["posiciones"][k][n]] for n in b6.NAMES} for k in ["c1", "c2", "c3"]}
    for k, v in {"c1": (0.0, -0.6), "c2": (0.35, 0.6), "c3": (-1.0, -1.0)}.items():   # mismos ajustes que ideologia_report
        fixed[k]["Ciclo de vida"] = [v[0] * .86, v[1] * .86]
    H = D["horizonte"]; R1 = DS["ensayo"]; R2 = DS["aplicacion"]
    pick = lambda R, c: {h: {m: round(R[h][c][m], 4) for m in ("ean", "wape90", "sesgo")} for h in HZ}
    cmp_rows = ["regla", "un_partido", "coalicion", "media6"] + ["F:" + n for n in b6.NAMES]
    data = dict(
        parties=[dict(name=n, col=b6.COL6[n], num=i + 1, bloc=b6.BLOC6[n], lema=irp.LEMA[n], resp=irp.RESP[n],
                      solo=[round(H[h]["F:" + n]["ean"], 4) for h in HZ]) for i, n in enumerate(b6.ORDER6)],
        empate=b6.COL6["Empate"], por=D["por"], coaliciones=D["coaliciones"][:6],
        n_votantes=D["n_votantes_fy25"], n_prueba=D["n_prueba"], sin_historia=D["sin_historia"],
        ensayo={c: pick(R1, c) for c in cmp_rows}, confirmacion={c: pick(R2, c) for c in cmp_rows},
        persistencia=DS["persistencia"], stats=BS["stats"], n_brujula=BS["n"], pts=pts,
        markers={k: spread(fixed[k]) for k in fixed}, ejemplo=example(html))
    assert len(pts) <= BS["n"]   # el reporte solo dibuja EANs con partido (sin empates)
    page = TPL.read_text(encoding="utf-8").replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    (W / "parlamento_artifact.html").write_text(page, encoding="utf-8")
    OUT.write_text("<!doctype html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>"
                   f"</head><body>{page}</body></html>", encoding="utf-8")
    print(OUT, f"{len(pts)} EANs en brújulas")


if __name__ == "__main__":
    main()
