"""Piezas visuales del reporte de ideologías y de la infografía: colores y orden de los 10 partidos, hemiciclo, barra de
volumen, fila de escaños y brújula política (SVG). Geometría del hemiciclo y CSS base: src/votes_report.py."""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import votes_report as vr  # noqa

INK, INK2, MUTED, GRID = vr.INK, vr.INK2, vr.MUTED, "#E3E7EC"
FRAG, MU = "#6250d6", "#eb6834"                 # morado = fragancias, naranja = makeup
CONS, RGDA = "#26408B", "#12A594"               # azul marino = consenso, verde azulado = regla + DAs
EMPATE = "#C7CCD3"
# un color por forma de base (paleta validada para daltonismo entre vecinos del hemiciclo)
FORM_COL = {"LY": "#eda100", "LY+M6e": "#e34948", "M12e": "#00a3c4", "M6e": "#b5651d", "M3e": "#a64ca6",
            "M6": "#2a78d6", "M12": "#2a78d6", "M3": "#008300", "CV": "#e87ba4"}
BLOC_ORDER = ["fix_rf", "LY", "LY+M6e", "M12e", "M6e", "M3e", "fix_rm", "M12", "M6", "M3", "CV"]
BLOC = {"fix_rf": "Año pasado", "LY": "Año pasado", "LY+M6e": "Año pasado", "M12e": "Estacional reciente", "M6e": "Estacional reciente",
        "M3e": "Estacional reciente", "fix_rm": "Nivel plano", "M12": "Nivel plano", "M6": "Nivel plano", "M3": "Nivel plano", "CV": "Ciclo de vida"}


class Parties:
    """Orden, colores, números y nombres cortos de los partidos a partir de ideo.json."""

    def __init__(self, D):
        ps = D["partidos"]
        key = lambda p: ("fix_rf" if p["nombre"] == "Regla fragancias" else "fix_rm" if p["nombre"] == "Regla makeup" else p["base"])
        ps = sorted(ps, key=lambda p: BLOC_ORDER.index(key(p)))
        self.list = ps
        self.names = [p["nombre"] for p in ps]
        self.order = self.names + ["Empate"]
        self.col = {p["nombre"]: (FRAG if key(p) == "fix_rf" else MU if key(p) == "fix_rm" else FORM_COL[p["base"]]) for p in ps}
        self.col["Empate"] = EMPATE
        self.num = {n: i + 1 for i, n in enumerate(self.names)}
        self.bloc = {p["nombre"]: BLOC[key(p)] for p in ps}
        self.by = {p["nombre"]: p for p in ps}

    def short(self, n):
        if n == "Empate":
            return "Empate"
        return {"Regla fragancias": "R. fragancias", "Regla makeup": "R. makeup"}.get(n, n.replace(" estacional", " est.").replace("Media ", "M"))

    def dot(self, n, size=3, num=False):
        if num and n != "Empate":
            return (f"<i class='nb' style='background:{self.col[n]}'>{self.num[n]}</i>")
        return f"<i class='dt' style='background:{self.col[n]};width:{size}mm;height:{size}mm'></i>"


def pc(x):
    return f"{x * 100:.0f}%"


def pc1(x):
    return f"{x * 100:.1f}%".replace(".", ",")


def n0(x):
    return vr.n0(x)


def hemicycle(P, seats, w=300, big=False, label="EANs"):
    n = sum(seats.get(p, 0) for p in P.order)
    pts, d = vr.seats(n)
    S0 = w / 2
    r = min(0.40 * d * (S0 - 2) / (1 + 0.40 * d), 24)
    S = S0 - r - 2; cx = w / 2; cy = S + r + 2
    cols = [P.col[p] for p in P.order for _ in range(seats.get(p, 0))]
    s = [f'<svg viewBox="0 0 {w} {cy + r + 2:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg">']
    for (ang, rad), col in zip(pts, cols):
        s.append(f'<circle cx="{cx + S * rad * math.cos(ang):.1f}" cy="{cy - S * rad * math.sin(ang):.1f}" r="{r:.2f}" fill="{col}"/>')
    fs = 40 if big else 26
    s.append(f'<text x="{cx}" y="{cy - (28 if big else 15)}" text-anchor="middle" class="hc1" style="font-size:{fs}px">{n}</text>')
    s.append(f'<text x="{cx}" y="{cy - (10 if big else 2)}" text-anchor="middle" class="hc2">{label}</text>')
    s.append("</svg>")
    return "".join(s)


def volbar(P, vol, h=5, minlab=0.08):
    out = ""
    for p in P.order:
        v = vol.get(p, 0)
        if v > 0.002:
            txt = pc(v) if v >= minlab else ""
            out += (f"<div class='sg' style='width:{v * 100:.2f}%;background:{P.col[p]};"
                    f"color:{'#46505E' if p in ('Empate',) else '#fff'}'>{txt}</div>")
    return f"<div class='bar' style='height:{h}mm'>{out}</div>"


def seatrow(P, t, cols=11):
    cells = "".join(f"<div><b style='color:{P.col[p] if p != 'Empate' else MUTED}'>{t['seats'].get(p, 0)}</b>"
                    f"<span>{P.num.get(p, '–')}</span></div>" for p in P.order)
    return f"<div class='sr' style='grid-template-columns:repeat({len(P.order)},1fr)'>{cells}</div>"


def card(P, title, sub, t, extra=""):
    we, wv = t["win_eans"], t["win_vol"]
    return (f"<div class='card'><div class='ch'><div><div class='ct'>{title}</div><div class='cs'>{sub}</div></div>"
            f"<div class='cv'>{n0(t['real'])}<span>unid. reales</span></div></div>"
            f"{hemicycle(P, t['seats'])}{seatrow(P, t)}"
            f"<div class='vl'>Volumen de los EANs que gana cada partido</div>{volbar(P, t['vol'])}"
            f"<div class='verd'><span>+ EANs: {P.dot(we, num=True)}<b>{P.short(we)}</b></span>"
            f"<span>+ volumen: {P.dot(wv, num=True)}<b>{P.short(wv)}</b></span></div>{extra}</div>")


def legend(P, note="Un punto = un EAN · la barra reparte el volumen real · número = partido"):
    return ("<div class='leg'>" + "".join(f"<span>{P.dot(p, num=True)}{p}</span>" for p in P.names) +
            f"<span>{P.dot('Empate')}Empate</span><span class='lm'>{note}</span></div>")


# ------------------------------------------------------------------ brújula
def compass(P, pts, xl, yl, title, quads, w=330, h=330, ylim=(-1, 1), xlim=(-1, 1), yband=None, cent=True, yticks=None, small=False):
    """pts: lista de dict(x, y, party, vol). xl/yl: (izquierda, derecha) / (abajo, arriba). quads: (sup-izq, sup-der, inf-izq, inf-der).
    Cuadrantes con fondo suave, EANs como puntos de su partido (tamaño por volumen) y el centro de cada partido (mediana de sus votantes)."""
    ml, mr, mt, mb = 26, 10, 14, 26
    W, H = w - ml - mr, h - mt - mb
    X = lambda x: ml + (x - xlim[0]) / (xlim[1] - xlim[0]) * W
    Y = lambda y: mt + (1 - (y - ylim[0]) / (ylim[1] - ylim[0])) * H
    x0, y0 = X((xlim[0] + xlim[1]) / 2), Y((ylim[0] + ylim[1]) / 2)
    qcol = ["#F3F0FB", "#EEF6FB", "#F6F7F1", "#FBF2EE"]
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" class="cmp">']
    s.append(f'<rect x="{ml}" y="{mt}" width="{x0 - ml:.1f}" height="{y0 - mt:.1f}" fill="{qcol[0]}"/>')
    s.append(f'<rect x="{x0:.1f}" y="{mt}" width="{ml + W - x0:.1f}" height="{y0 - mt:.1f}" fill="{qcol[1]}"/>')
    s.append(f'<rect x="{ml}" y="{y0:.1f}" width="{x0 - ml:.1f}" height="{mt + H - y0:.1f}" fill="{qcol[2]}"/>')
    s.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{ml + W - x0:.1f}" height="{mt + H - y0:.1f}" fill="{qcol[3]}"/>')
    if yband is not None:
        s.append(f'<rect x="{ml}" y="{Y(yband[1]):.1f}" width="{W}" height="{Y(yband[0]) - Y(yband[1]):.1f}" fill="#000" opacity=".035"/>')
    s.append(f'<line x1="{x0:.1f}" y1="{mt}" x2="{x0:.1f}" y2="{mt + H}" stroke="#C9CFD6" stroke-width="1"/>')
    s.append(f'<line x1="{ml}" y1="{y0:.1f}" x2="{ml + W}" y2="{y0:.1f}" stroke="#C9CFD6" stroke-width="1"/>')
    fq = 6.2 if small else 7
    for (tx, anchor, xx, yy) in [(quads[0], "start", ml + 4, mt + 10), (quads[1], "end", ml + W - 4, mt + 10),
                                 (quads[2], "start", ml + 4, mt + H - 5), (quads[3], "end", ml + W - 4, mt + H - 5)]:
        s.append(f'<text x="{xx}" y="{yy}" text-anchor="{anchor}" class="cq" style="font-size:{fq}px">{tx}</text>')
    vmax = max([p["vol"] for p in pts] + [1])
    order = sorted(pts, key=lambda p: -p["vol"])
    for p in order:
        r = 1.3 + 4.2 * math.sqrt(p["vol"] / vmax)
        s.append(f'<circle cx="{X(p["x"]):.1f}" cy="{Y(p["y"]):.1f}" r="{r:.2f}" fill="{P.col[p["party"]]}" fill-opacity=".55" stroke="#fff" stroke-width=".5"/>')
    if cent:
        C = []
        for n in P.names:
            sel = [p for p in pts if p["party"] == n]
            if len(sel) < 3:
                continue
            C.append([X(float(np.median([p["x"] for p in sel]))), Y(float(np.median([p["y"] for p in sel]))), n])
        orig = [(c[0], c[1]) for c in C]
        for _ in range(200):                      # separa los círculos que se pisan (mínimo 15 px entre centros)
            moved = False
            for i in range(len(C)):
                for j in range(i + 1, len(C)):
                    dx, dy = C[j][0] - C[i][0], C[j][1] - C[i][1]
                    dd = math.hypot(dx, dy)
                    if dd < 15:
                        if dd < 1e-6:
                            dx, dy, dd = 1.0, 0.3, 1.04
                        push = (15 - dd) / 2
                        C[i][0] -= dx / dd * push; C[i][1] -= dy / dd * push
                        C[j][0] += dx / dd * push; C[j][1] += dy / dd * push
                        moved = True
            for c in C:
                c[0] = min(max(c[0], ml + 8), ml + W - 8); c[1] = min(max(c[1], mt + 8), mt + H - 8)
            if not moved:
                break
        for (cx_, cy_, n), (ox, oy) in zip(C, orig):
            if math.hypot(cx_ - ox, cy_ - oy) > 3:
                s.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{cx_:.1f}" y2="{cy_:.1f}" stroke="{P.col[n]}" stroke-width="1"/>'
                         f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="1.8" fill="{P.col[n]}"/>')
            s.append(f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="7.2" fill="{P.col[n]}" stroke="#fff" stroke-width="2"/>')
            s.append(f'<text x="{cx_:.1f}" y="{cy_ + 2.9:.1f}" text-anchor="middle" class="cn">{P.num[n]}</text>')
    s.append(f'<rect x="{ml}" y="{mt}" width="{W}" height="{H}" fill="none" stroke="#D5DAE0"/>')
    fa = 7.4 if small else 8
    s.append(f'<text x="{ml}" y="{h - 8}" class="ca" style="font-size:{fa}px">← {xl[0]}</text>')
    s.append(f'<text x="{ml + W}" y="{h - 8}" text-anchor="end" class="ca" style="font-size:{fa}px">{xl[1]} →</text>')
    s.append(f'<text transform="translate(11,{mt + H}) rotate(-90)" class="ca" style="font-size:{fa}px">← {yl[0]}</text>')
    s.append(f'<text transform="translate(11,{mt}) rotate(-90)" text-anchor="end" class="ca" style="font-size:{fa}px">{yl[1]} →</text>')
    if yticks:
        for v, lab in yticks:
            s.append(f'<text x="{ml - 3}" y="{Y(v) + 2.5:.1f}" text-anchor="end" class="ct2">{lab}</text>')
    s.append("</svg>")
    return f"<div class='cmpw'><div class='cmpt'>{title}</div>{''.join(s)}</div>"


CSS_EXTRA = f"""
.dt {{ display: inline-block; border-radius: 50%; margin-right: 1.6mm; vertical-align: -.3mm; }}
.nb, .leg i.nb, .verd i.nb {{ display: inline-flex; align-items: center; justify-content: center; width: 3.6mm; height: 3.6mm; border-radius: 50%; color: #fff;
  font-style: normal; font-size: 5.6pt; font-weight: 700; margin-right: 1.4mm; vertical-align: -.5mm; }}
.leg {{ flex-wrap: wrap; gap: 1.6mm 3.6mm; }}
.sr {{ display: grid; text-align: center; margin: 1mm 0 1.6mm; }}
.sr b {{ display: block; font-family: InterDisplay, Inter; font-size: 10pt; }}
.sr span {{ display: block; font-size: 5.6pt; color: {MUTED}; line-height: 1.15; }}
.c4 .sr b {{ font-size: 8.4pt; }}
.verd b {{ font-weight: 700; }}
.verd i.nb {{ width: 3mm; height: 3mm; font-size: 5pt; }}
svg.cmp .cq {{ font-family: Inter; font-weight: 600; fill: #8792A0; letter-spacing: .02em; }}
svg.cmp .ca {{ font-family: Inter; font-weight: 600; fill: {INK2}; }}
svg.cmp .cn {{ font-family: Inter; font-weight: 700; font-size: 7.6px; fill: #fff; }}
svg.cmp .ct2 {{ font-family: Inter; font-size: 6.4px; fill: {MUTED}; }}
.cmpw {{ background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; padding: 2.4mm 2.6mm 1mm; }}
.cmpt {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 10.5pt; margin: 0 0 1mm 1mm; }}
"""
