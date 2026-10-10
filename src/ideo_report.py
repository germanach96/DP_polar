"""Reporte PDF: ideologías por EAN y propuesta de 10 partidos (foto sep-25 contra la verdad de sep-26).
Lee work/ideo.json, work/ideo_ean.parquet, work/ideo_compass.parquet, work/ideo_aux.pkl y work/ideo_panel.pkl
(correr antes src/ideo_panel.py, src/ideo_engine.py, src/ideo_parties.py y src/ideo_compass.py).
Salida: reportes/REPORTE_IDEOLOGIAS.pdf"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_viz as iv  # noqa
import votes_report as vr  # noqa

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"
OUT = ROOT / "reportes" / "REPORTE_IDEOLOGIAS.pdf"
INK, INK2, MUTED = iv.INK, iv.INK2, iv.MUTED
pc, pc1, n0 = iv.pc, iv.pc1, iv.n0
HOUSES = ["Burberry", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"]
QN = {"FY26.Q2": ("Q2 FY26", "oct–dic 25"), "FY26.Q3": ("Q3 FY26", "ene–mar 26"), "FY26.Q4": ("Q4 FY26", "abr–jun 26")}
TRAMOS = [("6–11", "Lanzamiento reciente"), ("12–17", "Segundo año"), ("18–25", "Estabilizándose"), ("26+", "Maduros · edad desconocida")]
FASES = [("Lanzamiento", "6–11 meses"), ("Consolidación", "12–17 meses"), ("Crecimiento", "trend 6M > casa +15%"),
         ("Estable", "trend 6M ±15% de su casa"), ("Declive", "trend 6M < casa −15%")]
FLAGS = [("0.0", "Sin bandera", "Forecast de sistema"), ("1.0", "Bandera 1", "1 customer ignorado"), ("2.0", "Bandera 2", "Los 2 ignorados: manual")]


def load():
    D = json.loads((W / "ideo.json").read_text())
    E = pd.read_parquet(W / "ideo_ean.parquet")
    C = pd.read_parquet(W / "ideo_compass.parquet")
    X = pd.read_pickle(W / "ideo_aux.pkl")
    Pn = pd.read_pickle(W / "ideo_panel.pkl")
    return D, E, C, X, Pn


def sec(kick, title, body, cls=""):
    return f"<section class='page {cls}'><div class='blob'></div><div class='kick'>{kick}</div><h2>{title}</h2>{body}</section>"


# ------------------------------------------------------------------ gráficos simples
def hbars(rows, w=250, lab_w=96, val_w=40, bh=8.5, gap=4.5, color=INK2, fmt=pc, maxv=None, sub=None):
    """rows: (label, value, color|None, note|None)."""
    maxv = maxv or max([r[1] for r in rows] + [1e-9])
    h = len(rows) * (bh + gap) + 2
    s = [f'<svg viewBox="0 0 {w} {h:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" class="hb">']
    for i, r in enumerate(rows):
        lab, v, col = r[0], r[1], (r[2] if len(r) > 2 and r[2] else color)
        y = i * (bh + gap) + 1
        bw = max((w - lab_w - val_w) * v / maxv, 0.5 if v > 0 else 0)
        s.append(f'<text x="{lab_w - 5}" y="{y + bh - 1.6:.1f}" text-anchor="end" class="hl">{lab}</text>')
        s.append(f'<rect x="{lab_w}" y="{y:.1f}" width="{bw:.1f}" height="{bh}" rx="2" fill="{col}"/>')
        note = r[3] if len(r) > 3 and r[3] else ""
        s.append(f'<text x="{lab_w + bw + 4:.1f}" y="{y + bh - 1.6:.1f}" class="hv">{fmt(v)}<tspan class="hn"> {note}</tspan></text>')
    s.append("</svg>")
    return "".join(s)


def pairbars(cats, fr, mu, w=205, lab_w=80):
    """Dos barras por fila: fragancias (morado) y makeup (naranja); % de EANs y del volumen en texto."""
    bh, gap, ig = 7.4, 7.5, 1.4
    h = len(cats) * (2 * bh + ig + gap) + 2
    s = [f'<svg viewBox="0 0 {w} {h:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" class="hb">']
    span = w - lab_w - 64
    for i, c in enumerate(cats):
        y = i * (2 * bh + ig + gap) + 1
        s.append(f'<text x="{lab_w - 5}" y="{y + bh + 2.6:.1f}" text-anchor="end" class="hl{" mutedl" if c == "No importa" else ""}">{c}</text>')
        for j, (dd, col) in enumerate([(fr, iv.FRAG), (mu, iv.MU)]):
            e, v = dd.get(c, (0, 0))
            yy = y + j * (bh + ig)
            op = ".35" if c == "No importa" else "1"
            s.append(f'<rect x="{lab_w}" y="{yy:.1f}" width="{max(span * e, .5 if e else 0):.1f}" height="{bh}" rx="1.6" fill="{col}" opacity="{op}"/>')
            s.append(f'<text x="{lab_w + span * e + 3:.1f}" y="{yy + bh - 1:.1f}" class="hv2">{pc(e)} <tspan class="hn">· vol {pc(v)}</tspan></text>')
    s.append("</svg>")
    return "".join(s)


def curve_chart(X, E, Pn, w=300, h=150):
    """Curva de vida mediana (multiplicador sobre el nivel 6M) por tramo y categoría, pool casa × segmento sin temporada."""
    a = Pn["attr"]; CV = X["CV"]["casa×seg|None"]
    v = a.votante.values
    ml, mr, mt, mb = 30, 74, 8, 18
    W_, H_ = w - ml - mr, h - mt - mb
    lo, hi = 0.2, 1.8
    Xf = lambda i: ml + i / 8 * W_
    Yf = lambda y: mt + (1 - (y - lo) / (hi - lo)) * H_
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" class="lc">']
    for t in [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]:
        s.append(f'<line x1="{ml}" x2="{ml + W_}" y1="{Yf(t):.1f}" y2="{Yf(t):.1f}" stroke="{"#B9C0C8" if t == 1 else "#EDF0F3"}" stroke-width="{1 if t == 1 else .8}"/>')
        s.append(f'<text x="{ml - 4}" y="{Yf(t) + 2.5:.1f}" text-anchor="end" class="ax">×{t:.1f}</text>')
    for i, mlab in enumerate(["oct", "nov", "dic", "ene", "feb", "mar", "abr", "may", "jun"]):
        s.append(f'<text x="{Xf(i):.1f}" y="{h - 5}" text-anchor="middle" class="ax">{mlab}</text>')
    labs = []
    for cat, col in [("Fragancias", iv.FRAG), ("Makeup", iv.MU)]:
        for tr, dash in [("6–11", ""), ("12–17", "4 3"), ("18–25", "1.5 2.5")]:
            sel = v & (a.cat.values == cat) & (a.tramo.values == tr)
            if sel.sum() < 3:
                continue
            med = np.median(CV[sel], 0)
            pts = " ".join(f"{Xf(i):.1f},{Yf(min(max(y, lo), hi)):.1f}" for i, y in enumerate(med))
            s.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="{dash}" stroke-linecap="round"/>')
            labs.append((Yf(min(max(med[-1], lo), hi)), f"{cat[:4]}. {tr}", col, med[-1]))
    labs.sort()
    last = -99
    for y, t, col, val in labs:
        y = max(y, last + 9); last = y
        s.append(f'<text x="{ml + W_ + 5}" y="{y + 2.5:.1f}" class="cl" fill="{col}">{t} · ×{val:.2f}</text>')
    s.append("</svg>")
    return "".join(s)


def trend_range(X, Pn, w=250):
    """Rango (P10–P90) y mediana del trend 12M con tope ±30% que recibe cada EAN según la fuente, por categoría."""
    a = Pn["attr"]; v = a.votante.values
    srcs = [("casa", "Casa"), ("categoría", "Categoría"), ("segmento", "Segmento"), ("franquicia", "Franquicia"), ("línea", "Línea"), ("fase", "Fase"), ("EAN", "Propio EAN")]
    lab_w, rr = 62, 13
    h = len(srcs) * 2 * rr + 30
    X0 = lambda g: lab_w + (g + 0.3) / 0.6 * (w - lab_w - 10)
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" class="hb">']
    s.append(f'<rect x="{X0(-0.3) - 3:.1f}" y="4" width="6" height="{h - 26}" fill="#000" opacity=".05"/>')
    for g in [-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3]:
        s.append(f'<line x1="{X0(g):.1f}" x2="{X0(g):.1f}" y1="4" y2="{h - 22}" stroke="{"#B9C0C8" if g in (0, -0.3) else "#EDF0F3"}"/>')
        s.append(f'<text x="{X0(g):.1f}" y="{h - 12}" text-anchor="middle" class="ax">{g * 100:+.0f}%</text>'.replace("+0%", "0%"))
    s.append(f'<text x="{X0(-0.3) + 4:.1f}" y="{h - 2}" class="ax">← suelo del tope</text>')
    for i, (src, lab) in enumerate(srcs):
        g = np.clip(X["G"][f"{src}|12"], -0.3, 0.3)
        y0 = 8 + i * 2 * rr
        s.append(f'<text x="{lab_w - 6}" y="{y0 + rr + 2:.1f}" text-anchor="end" class="hl">{lab}</text>')
        for j, (cat, col) in enumerate([("Fragancias", iv.FRAG), ("Makeup", iv.MU)]):
            x = g[v & (a.cat.values == cat)]
            p10, p50, p90 = np.percentile(x, [10, 50, 90])
            y = y0 + 5 + j * 9
            s.append(f'<line x1="{X0(p10):.1f}" x2="{max(X0(p90), X0(p10) + 1):.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="4" stroke-linecap="round" opacity=".45"/>')
            s.append(f'<circle cx="{X0(p50):.1f}" cy="{y:.1f}" r="3.2" fill="{col}" stroke="#fff" stroke-width="1"/>')
    s.append("</svg>")
    return "".join(s)


def floor_chart(X, Pn, w=300):
    a = Pn["attr"]; v = a.votante.values
    rows = []
    for src, lab in [("casa", "Casa"), ("categoría", "Categoría"), ("segmento", "Segmento"), ("franquicia", "Franquicia"),
                     ("línea", "Línea"), ("fase", "Fase"), ("EAN", "Propio EAN")]:
        g = X["G"][f"{src}|12"]
        fr = float((g[v & (a.cat.values == "Fragancias")] <= -0.2999).mean()); mu = float((g[v & (a.cat.values == "Makeup")] <= -0.2999).mean())
        rows.append((lab, fr, mu))
    cats = [r[0] for r in rows]
    return pairbars(cats, {r[0]: (r[1], 0) for r in rows}, {r[0]: (r[2], 0) for r in rows}, w=w).replace(" <tspan class=\"hn\">· vol 0%</tspan>", "")


def waterfall(P, D, w=620, h=150):
    ap = D["aportes"]
    vals = [x["obj"] for x in ap]
    names = [x["partido"] for x in ap]
    ml, mr, mt, mb = 34, 8, 14, 40
    W_, H_ = w - ml - mr, h - mt - mb
    hi = 0.7; lo = 0.0
    Y = lambda y: mt + (1 - (y - lo) / (hi - lo)) * H_
    n = len(vals) + 1
    bw = W_ / n * 0.62
    Xc = lambda i: ml + (i + 0.5) * W_ / n
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" class="wf">']
    for t in [0, .1, .2, .3, .4, .5, .6, .7]:
        s.append(f'<line x1="{ml}" x2="{ml + W_}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="#EDF0F3"/>')
        s.append(f'<text x="{ml - 4}" y="{Y(t) + 2.5:.1f}" text-anchor="end" class="ax">{t * 100:.0f}%</text>')
    # barra inicial: reglas
    s.append(f'<rect x="{Xc(0) - bw / 2:.1f}" y="{Y(vals[0]):.1f}" width="{bw:.1f}" height="{Y(0) - Y(vals[0]):.1f}" rx="2" fill="#9AA3AE"/>')
    s.append(f'<text x="{Xc(0):.1f}" y="{Y(vals[0]) - 3:.1f}" text-anchor="middle" class="bv">{pc(vals[0])}</text>')
    s.append(f'<text x="{Xc(0):.1f}" y="{h - 26}" text-anchor="middle" class="xl">2 reglas</text>')
    for i in range(1, len(vals)):
        a_, b_ = vals[i - 1], vals[i]; p = names[i]
        s.append(f'<rect x="{Xc(i) - bw / 2:.1f}" y="{Y(a_):.1f}" width="{bw:.1f}" height="{max(Y(b_) - Y(a_), 1):.1f}" rx="2" fill="{P.col[p]}"/>')
        s.append(f'<text x="{Xc(i):.1f}" y="{Y(b_) + 9:.1f}" text-anchor="middle" class="bd">−{f"{(a_ - b_) * 100:.1f}".replace(".", ",")}</text>')
        s.append(f'<circle cx="{Xc(i):.1f}" cy="{h - 29}" r="5" fill="{P.col[p]}"/><text x="{Xc(i):.1f}" y="{h - 26.6}" text-anchor="middle" class="nbs">{P.num[p]}</text>')
        if i < len(vals) - 1:
            s.append(f'<line x1="{Xc(i) + bw / 2:.1f}" x2="{Xc(i + 1) - bw / 2:.1f}" y1="{Y(b_):.1f}" y2="{Y(b_):.1f}" stroke="#B9C0C8" stroke-dasharray="2 2"/>')
    i = len(vals)
    s.append(f'<rect x="{Xc(i) - bw / 2:.1f}" y="{Y(vals[-1]):.1f}" width="{bw:.1f}" height="{Y(0) - Y(vals[-1]):.1f}" rx="2" fill="{INK}"/>')
    s.append(f'<text x="{Xc(i):.1f}" y="{Y(vals[-1]) - 3:.1f}" text-anchor="middle" class="bv">{pc(vals[-1])}</text>')
    s.append(f'<text x="{Xc(i):.1f}" y="{h - 26}" text-anchor="middle" class="xl">10 partidos</text>')
    orc = D["oraculo"]
    s.append(f'<line x1="{ml}" x2="{ml + W_}" y1="{Y(orc):.1f}" y2="{Y(orc):.1f}" stroke="{INK2}" stroke-dasharray="4 3"/>')
    s.append(f'<text x="{Xc(len(vals)) - bw / 2 - 6:.1f}" y="{Y(orc) - 3:.1f}" text-anchor="end" class="xl">techo: cada EAN con su mejor estrategia de 203.160 · {pc(orc)}</text>')
    s.append(f'<text x="{ml}" y="{h - 8}" class="xl2">Error del parlamento: cada EAN usa el partido que mejor le va; Σ|forecast − real| por quarter / real, tope 200%, 50% por EAN y 50% por volumen.</text>')
    s.append("</svg>")
    return "".join(s)


def robust_chart(D, w=300, h=112):
    R = D["robustez"]
    ml, mr, mt, mb = 30, 6, 8, 22
    W_, H_ = w - ml - mr, h - mt - mb
    lo, hi = 0.25, 0.75
    Y = lambda y: mt + (1 - (y - lo) / (hi - lo)) * H_
    X = lambda i: ml + (i + .5) * W_ / len(R)
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" class="rc">']
    for t in [.3, .4, .5, .6, .7]:
        s.append(f'<line x1="{ml}" x2="{ml + W_}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="#EDF0F3"/><text x="{ml - 4}" y="{Y(t) + 2.5:.1f}" text-anchor="end" class="ax">{t * 100:.0f}%</text>')
    for i, r in enumerate(R):
        x = X(i)
        s.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(r["solo_reglas"]):.1f}" y2="{Y(r["fuera"]):.1f}" stroke="#D5DAE0" stroke-width="1.4"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{Y(r["solo_reglas"]):.1f}" r="3.4" fill="#9AA3AE"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{Y(r["techo_fuera"]):.1f}" r="3.4" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{Y(r["fuera"]):.1f}" r="3.4" fill="{INK}"/>')
        s.append(f'<text x="{x:.1f}" y="{h - 9}" text-anchor="middle" class="ax">{i + 1}</text>')
    s.append("</svg>")
    return "".join(s)


# ------------------------------------------------------------------ páginas
def page_cover(P, D, E, C):
    T = D["eleccion"]["total"]
    cc = C.join(E[["cat", "tramo", "real"]]); mu_ = cc[cc.cat == "Makeup"]
    imp = D["imp"]; tl0 = D["temporal_limpio"]
    bur = [x for x in tl0["w90"] if x["casa"] == "Burberry"][0]
    nodaf = sum(1 for p in D["partidos"][2:] if p["daf"] == 0)
    finds = [("La base decide", f"Cómo se construye la base importa en el {pc(imp['Fragancias']['base']['importa'])} de los EANs de fragancias y el {pc(imp['Makeup']['base']['importa'])} de makeup. Cortes y DAs del pasado, en una minoría."),
             ("Sin DAs de la foto", f"{nodaf} de los 8 partidos nuevos no los suman. En makeup, el {pc(D['pop']['Makeup']['daf']['0%']['vol'])} del volumen acierta más sin ellos."),
             ("La edad cuenta", f"La curva de los códigos de su edad gana en el {pc(float((cc[cc.tramo == '6–11'].ciclo > 0.3).mean()))} de los recién lanzados. Para los maduros, manda su fase."),
             ("De quién, aún no se sabe", "En sep-25 casi todos los trends de grupo están entre −20% y −30% por el tope: el propio EAN es el más elegido, pero hacen falta más fotos."),
             ("Ojo con el total", f"EAN a EAN gana; en la casa no siempre: Burberry abr–jun se desvía {pc(bur['elegido'])} con los partidos y {pc(bur['regla'])} con la regla.")]
    fh = "".join(f"<div class='fd'><div class='fdt'>{t}</div><div class='fdx'>{x}</div></div>" for t, x in finds)
    tl = D["temporal_limpio"]["Total"]
    first = max(P.names, key=lambda p: T["seats"][p]); firstv = max(P.names, key=lambda p: T["vol"][p])
    rows = "".join(f"<tr><td>{P.dot(p, num=True)}<b>{p}</b><span class='bl'>{P.bloc[p]}</span></td><td class='n'>{T['seats'][p]}</td>"
                   f"<td class='n'>{pc(T['seats'][p] / T['eans'])}</td><td class='n'>{pc(T['vol'][p])}</td></tr>" for p in P.names)
    rows += f"<tr><td>{P.dot('Empate')}<b>Empate</b><span class='bl'>sin ganador</span></td><td class='n'>{T['seats']['Empate']}</td><td class='n'>{pc(T['seats']['Empate'] / T['eans'])}</td><td class='n'>{pc(T['vol']['Empate'])}</td></tr>"
    return f"""<section class='page'><div class='blob'></div>
  <div class='kick'>Ideologías por EAN · foto sep-25 → real sep-26 · {n0(D['n_estrategias'])} estrategias · {D['n_votantes']} EANs</div>
  <h1>Diez partidos y ninguna mayoría:<br/><span style='color:{INK2}'>cada EAN tiene su forma de acertar.</span></h1>
  <div class='top'>
    <div class='hemi'>{iv.hemicycle(P, T['seats'], w=520, big=True)}
      <div class='vl' style='margin-top:2.6mm'>Volumen real oct–jun de los EANs que gana cada partido</div>{iv.volbar(P, T['vol'], h=6)}
      <div class='kpis3'>
        <div class='kpi'><div class='kl'>Primera fuerza en EANs</div><div class='kv2' style='color:{P.col[first]}'>{first}</div><div class='kl'>{T['seats'][first]} EANs ({pc(T['seats'][first] / T['eans'])}) · solo {pc(T['vol'][first])} del volumen</div></div>
        <div class='kpi'><div class='kl'>Primera fuerza en volumen</div><div class='kv2' style='color:{P.col[firstv]}'>{firstv}</div><div class='kl'>{pc(T['vol'][firstv])} del volumen · {T['seats'][firstv]} EANs</div></div>
        <div class='kpi'><div class='kl'>Prueba limpia en el tiempo (abr–jun)</div><div class='kv2'>{pc(tl['ean_elegido'])} <small>vs {pc(tl['ean_regla'])} reglas · {pc(tl['ean_cons'])} consenso</small></div><div class='kl'>error EAN a EAN, eligiendo partido solo con oct–mar</div></div>
      </div></div>
    <div class='side'>
      <table class='st'><tr><th>Partido</th><th>EANs</th><th>%</th><th>Volumen</th></tr>{rows}</table>
      <div class='note'><b>Qué es.</b> Con la foto de sep-25 se calcularon {n0(D['n_estrategias'])} formas de hacer el forecast de oct-25 a jun-26 para cada EAN Central con actividad
        ({D['n_votantes']}) y se comparó con el real de la foto sep-26: «con trampa», sabiendo ya qué pasó. Las mejores estrategias se agruparon en 8 partidos nuevos, que se suman a las dos reglas actuales.
        Elección con el formato fijo: en cada quarter (Q2, Q3, Q4 FY26) el EAN vota al partido con menor error; gana el que más quarters gana. {D['eleccion']['desempates']} EANs se decidieron por el error sumado.</div>
    </div></div><div class='finds'>{fh}</div></section>"""


def page_method(P, D, X, E, Pn):
    a = Pn["attr"]; v = a[a.votante]
    tr = v.tramo.value_counts(); fa = v.fase.value_counts()
    steps = [("1", "El universo", f"<b>{D['n_votantes']} EANs</b> Central con actividad en la foto sep-25 ({(v.cat == 'Fragancias').sum()} de fragancias, {(v.cat == 'Makeup').sum()} de makeup). "
                                   f"{D['n_muertos']} no vendieron nada de oct a jun: votan, pero no cuentan para buscar estrategias."),
             ("2", "El banco de estrategias", f"<b>{n0(D['n_estrategias'])}</b> combinaciones de 9 ideas: base (año pasado, media 3/6/12M plana o con temporada, mixta, ciclo de vida), "
                                              "perfil estacional (casa, casa × segmento, línea, categoría), trend (de quién, 3/6/12M, fuerza 25–100%, tope ±30% o ±60%), DAs del pasado (0–100%), cortes (0, 10% con tope, 25%, 50%) y DAs de la foto (0, 50, 100%)."),
             ("3", "La mejor de cada EAN", "Error del EAN = Σ |forecast − real| de cada quarter / real (tope 200%). Para cada EAN, la estrategia con menos error y qué ideas de ella importan: "
                                           "una idea importa si cambiarla, dejando lo demás igual, empeora más de medio punto."),
             ("4", "Agrupar en partidos", "Las 2 reglas actuales quedan fijas. Se añade un partido por forma de base; dentro de cada forma, los datos eligen la estacionalidad, el trend, los DAs y los cortes "
                                          "que más bajan el error del parlamento (cada EAN usa su mejor partido; pesa 50% el EAN y 50% su volumen). Se quita la forma que menos aporta hasta quedar 8."),
             ("5", "Elegir y comprobar", "Elección con el formato fijo por quarters. Pruebas: elegir con media muestra de EANs y medir en la otra mitad (10 veces), y elegir solo con oct–mar y medir en abr–jun.")]
    st_html = "".join(f"<div class='stp'><div class='sn'>{n}</div><div><div class='stt'>{t}</div><div class='stx'>{x}</div></div></div>" for n, t, x in steps)
    edad = (f"<div class='box'><div class='ct'>Edad y madurez: las dos preguntas del ciclo de vida</div>"
            f"<p><b>Edad</b> = meses desde el lanzamiento hasta sep-25. Lanzamiento = primer mes de <b>dos meses seguidos</b> con envío (evita falsos inicios). "
            f"Si el primer envío es jul-23, inicio de los datos, la edad real es desconocida: tramo 26+. "
            f"Votantes por tramo: 6–11 {tr.get('6–11', 0)} · 12–17 {tr.get('12–17', 0)} · 18–25 {tr.get('18–25', 0)} · 26+ {tr.get('26+', 0)}.</p>"
            f"<p><b>Madurez (fase)</b>, solo con 18+ meses: trend 6M propio frente al de su casa. <b>Crecimiento</b> si crece más de 15 puntos por encima de su casa, "
            f"<b>declive</b> si va 15 por debajo, <b>estable</b> en medio. Se mide contra la casa porque en mar–ago 25 todo el mercado cayó un 36–51%: en absoluto, casi todo saldría «declive». "
            f"Votantes: crecimiento {fa.get('Crecimiento', 0)} · estable {fa.get('Estable', 0)} · declive {fa.get('Declive', 0)}.</p>"
            f"<p><b>«¿Cómo les fue a los otros códigos a mi edad?»</b> Para un EAN de a meses se buscan los códigos que en su día tuvieron a ± 2 meses (mínimo 5) y se mide cuánto vendieron "
            f"en los 9 meses siguientes frente a su media de los 6 anteriores. Los maduros, que no tienen pares de su edad en los datos, siguen el trend 12M de los códigos de su misma fase.</p></div>")
    chart = (f"<div class='box'><div class='ct'>La curva de vida que sale de los datos</div><div class='cs'>Multiplicador mediano sobre el nivel de los últimos 6 meses, "
             f"por tramo de edad (pares de su casa × segmento). Morado = fragancias, naranja = makeup.</div>{curve_chart(X, E, Pn)}"
             f"<p class='sm'>Un perfume recién lanzado vende, de oct a jun, la mitad de su nivel de los 6 meses anteriores: el llenado de canal no se repite. En makeup la caída de los 12–17 meses llega en primavera, cuando los pares cumplían 2 años.</p></div>")
    body = f"<div class='g2m'><div class='steps'>{st_html}</div><div class='col'>{edad}{chart}</div></div>"
    return sec("Cómo se hizo", "Del EAN a los partidos: 203.160 estrategias por EAN, la mejor de cada uno y 8 partidos que las resumen.", body)


def page_ideas(P, D):
    pop = D["pop"]; imp = D["imp"]
    blocks = []
    spec = [("familia", "Forma de la base", ["Año pasado", "Mixta", "Media estacional", "Media plana", "Ciclo de vida", "No importa"]),
            ("memoria", "Memoria de la base", ["Año pasado", "Año pasado + 6M", "12M", "6M", "3M", "No importa"]),
            ("daf", "DAs de la foto que suma", ["0%", "50%", "100%", "No importa"]),
            ("dap", "DAs+ del pasado que resta", ["0%", "25%", "50%", "75%", "100%", "No importa"]),
            ("cortes", "Cortes que suma", ["0", "10% con tope", "25%", "50%", "No importa"])]
    for k, title, cats in spec:
        fr = {c: (pop["Fragancias"][k].get(c, {}).get("eans", 0) / sum(x["eans"] for x in pop["Fragancias"][k].values()),
                  pop["Fragancias"][k].get(c, {}).get("vol", 0)) for c in cats}
        mu = {c: (pop["Makeup"][k].get(c, {}).get("eans", 0) / sum(x["eans"] for x in pop["Makeup"][k].values()),
                  pop["Makeup"][k].get(c, {}).get("vol", 0)) for c in cats}
        g = {"familia": "base", "memoria": "base", "daf": "daf", "dap": "dap", "cortes": "cortes"}[k]
        blocks.append(f"<div class='box ib'><div class='ct'>{title}</div><div class='cs'>Importa en {pc(imp['Fragancias'][g]['importa'])} de los EANs de fragancias y "
                      f"{pc(imp['Makeup'][g]['importa'])} de makeup</div>{pairbars(cats, fr, mu)}</div>")
    lead = (f"<div class='box ib lead'><div class='ct'>Cómo leerlo</div><p>Para cada EAN se tomó su mejor estrategia a posteriori y se miró qué decía en cada idea. "
            f"<b>«No importa»</b>: cambiar esa idea, dejando el resto igual, empeora menos de medio punto el error del EAN.</p>"
            f"<p><span class='sw' style='background:{iv.FRAG}'></span>% de los EANs de fragancias · <span class='sw' style='background:{iv.MU}'></span>% de los EANs de makeup; "
            f"«vol» = % del real de esos EANs.</p><p><b>Lo que manda:</b> la forma de la base importa en 9 de cada 10 EANs. Los cortes y los DAs del pasado, en 2–5 de cada 10: "
            f"su efecto se compensa con otras ideas. Los DAs de la foto importan sobre todo en makeup, y casi siempre para quitarlos.</p></div>")
    body = f"<div class='g3'>{lead}{''.join(blocks)}</div>"
    tit = ("La base decide: importa en 9 de cada 10 EANs. En makeup, el 59% del volumen acierta más sin los DAs de la foto; "
           "los cortes y los DAs del pasado solo pesan en una minoría.")
    return sec("Qué hubiera sido lo mejor para cada EAN", tit, body)


def page_trend(P, D, X, Pn):
    pop = D["pop"]; imp = D["imp"]
    cats = ["EAN", "línea", "franquicia", "segmento", "casa", "categoría", "fase", "No importa"]
    lab = {"EAN": "Propio EAN", "línea": "Línea", "franquicia": "Franquicia", "segmento": "Segmento", "casa": "Casa", "categoría": "Categoría", "fase": "Fase", "No importa": "No importa"}
    tot = lambda c: sum(x["eans"] for x in pop[c]["fuente"].values())
    fr = {lab[c]: (pop["Fragancias"]["fuente"].get(c, {}).get("eans", 0) / tot("Fragancias"), pop["Fragancias"]["fuente"].get(c, {}).get("vol", 0)) for c in cats}
    mu = {lab[c]: (pop["Makeup"]["fuente"].get(c, {}).get("eans", 0) / tot("Makeup"), pop["Makeup"]["fuente"].get(c, {}).get("vol", 0)) for c in cats}
    b1 = (f"<div class='box'><div class='ct'>¿De quién toma el trend su mejor estrategia?</div><div class='cs'>Llevar trend importa en {pc(imp['Fragancias']['fuente']['importa'])} de los EANs de fragancias "
          f"y {pc(imp['Makeup']['fuente']['importa'])} de makeup (frente a quitarlo).</div>{pairbars([lab[c] for c in cats], fr, mu)}</div>")
    a = Pn["attr"]; v = a.votante.values
    at6 = {c: float((X["G"]["casa|6"][v & (a.cat.values == c)] <= -0.2999).mean()) for c in ["Fragancias", "Makeup"]}
    b2 = (f"<div class='box'><div class='ct'>Por qué casi da igual en esta foto: el tope</div><div class='cs'>Trend 12M que recibe cada EAN según la fuente, con tope ±30%: "
          f"barra = 80% central de los EANs, punto = mediana. Morado = fragancias, naranja = makeup.</div>{trend_range(X, Pn)}"
          f"<p class='sm'>En sep-25 las casas caían entre un 22% y un 32% en 12 meses: casa, categoría y segmento dan a casi todos los EANs un trend de −20% a −30%. "
          f"Con ventana de 6M es peor: el trend de la casa está en el suelo de −30% para el {pc(at6['Fragancias'])} de los EANs de fragancias y el {pc(at6['Makeup'])} de makeup. "
          f"La franquicia, la línea, la fase y el propio EAN sí dan trends distintos según el EAN. El banco probó también un tope de ±60%: lo eligen "
          f"{sum(1 for p in D['partidos'][2:] if p['tope'] == 0.6)} de los 8 partidos nuevos.</p></div>")
    b3 = ("<div class='box'><div class='ct'>Lectura</div><ul class='ul'>"
          "<li>Donde el trend importa, el <b>propio EAN</b> es la fuente más elegida en las dos categorías (59 EANs de fragancias, 112 de makeup), pero no es mayoría.</li>"
          "<li>En makeup, el trend de su <b>fase</b> se lleva el 44% del volumen: a los EANs grandes de makeup les va mejor seguir a los códigos que crecen o caen como ellos.</li>"
          "<li>Con una sola foto y el mercado en caída fuerte, esta pregunta no se puede cerrar: hace falta repetirla con fotos donde los grupos no estén todos en el tope.</li></ul></div>")
    body = f"<div class='g3b'>{b1}{b2}{b3}</div>"
    return sec("De quién toma el trend", "El propio EAN es la fuente más elegida, pero en sep-25 los trends de grupo se amontonan entre −20% y −30%: esta foto no deja ver bien a quién conviene seguir.", body)


def compass_pts(E, C, key_x, key_y, P, age=False, known_age=False):
    df = C.join(E[["voto", "real", "edad", "tramo"]])
    if known_age:
        df = df[df.tramo != "26+"]
    rng = np.random.default_rng(3)
    pts = []
    for ean, r in df.iterrows():
        if r.voto not in P.col:
            continue
        x = float(r[key_x]) + rng.normal(0, 0.02)
        if age:
            y = float(r.edad) if r.tramo != "26+" else 28 + rng.uniform(-1.2, 1.2)
        else:
            y = float(r[key_y]) + rng.normal(0, 0.02)
        pts.append(dict(x=float(np.clip(x, -1.08, 1.08)), y=y if age else float(np.clip(y, -1.08, 1.08)), party=r.voto, vol=float(r.real)))
    return pts


def compasses(P, E, C, specs, small=False, w=330, h=425):
    out = []
    for kx, ky, xl, yl, title, quads in specs:
        age = ky == "edad"
        known = kx == "ciclo"
        pts = compass_pts(E, C, kx, ky, P, age, known)
        if age and known:
            out.append(iv.compass(P, pts, xl, yl, title, quads, w=w, h=h, ylim=(4, 26), xlim=(-1.1, 1.1),
                                  yticks=[(6, "6"), (12, "12"), (18, "18"), (24, "24")], small=small))
        elif age:
            out.append(iv.compass(P, pts, xl, yl, title, quads, w=w, h=h, ylim=(4, 31), xlim=(-1.1, 1.1), yband=(26, 31),
                                  yticks=[(6, "6"), (12, "12"), (18, "18"), (24, "24"), (28, "26+")], small=small))
        else:
            out.append(iv.compass(P, pts, xl, yl, title, quads, w=w, h=h, xlim=(-1.1, 1.1), ylim=(-1.1, 1.1), small=small))
    return out


SPECS1 = [("estacional", "corto", ("Nivel plano", "Estacional"), ("Memoria larga (12M)", "Memoria corta (3M)"), "Estacionalidad × memoria",
           ("Estacionales de corto plazo", "", "", "Estacionales de largo plazo")),
          ("individual", "edad", ("Colectivo: casa o categoría", "Individual: EAN o línea"), ("Joven", "Maduro"), "Individualismo × edad",
           ("Maduros colectivistas", "Maduros individualistas", "Jóvenes colectivistas", "Jóvenes individualistas")),
          ("ciclo", "edad", ("Nivel 6M sin curva", "Curva de su edad"), ("Joven", "Mayor"), "Curva de vida × edad (edad conocida)",
           ("", "Maduros: siguen a su fase", "", "Jóvenes que siguen la curva"))]
SPECS1[0] = (SPECS1[0][0], SPECS1[0][1], SPECS1[0][2], SPECS1[0][3], SPECS1[0][4],
             ("Planos de corto plazo", "Estacionales de corto plazo", "Planos de largo plazo", "Estacionales de largo plazo"))
SPECS1[2] = (SPECS1[2][0], SPECS1[2][1], SPECS1[2][2], SPECS1[2][3], SPECS1[2][4],
             ("Mayores sin curva", "Mayores con curva", "Jóvenes sin curva", "Jóvenes que siguen la curva"))
SPECS2 = [("fe", "tventana", ("Trend suave (≤25%)", "Trend completo (≥75%)"), ("Trend de 12M", "Trend de 3M"), "Fe en el trend × ventana",
           ("Escépticos de corto plazo", "Creyentes de corto plazo", "Escépticos de largo plazo", "Creyentes de largo plazo")),
          ("dap", "daf", ("No limpia DAs del pasado", "Limpia el 100%"), ("Ignora DAs de la foto", "Suma el 100%"), "Promociones: pasado × futuro",
           ("Cree en las futuras", "Limpia el pasado y suma las futuras", "Ignora las promociones", "Solo limpia el pasado")),
          ("cortes", "daf", ("No suma cortes", "Suma el 50%"), ("Ignora DAs de la foto", "Suma el 100%"), "Cortes × DAs de la foto",
           ("Solo DAs", "Cortes y DAs", "Ni cortes ni DAs", "Solo cortes"))]


def page_compass(P, E, C, specs, kick, title, notes):
    cs = compasses(P, E, C, specs)
    body = (iv.legend(P, "Punto = EAN (tamaño = volumen) del color del partido al que vota · círculo con número = mediana de sus votantes")
            + f"<div class='g3c'>{''.join(cs)}</div><div class='g3n'>{''.join(f'<div class=nt>{n}</div>' for n in notes)}</div>")
    return sec(kick, title, body)


def page_parties(P, D, E):
    T = D["eleccion"]["total"]
    rows = ""
    for p in P.list:
        n = p["nombre"]; ide = p["ideas"]
        g = E[E.real > 0]
        err = float(g["err:" + n].sum() / g.real.sum())
        w90 = pd.DataFrame(D["w90"]); w90v = float((w90[n] * w90.real).sum() / w90.real.sum()); bias = float(-(w90["spp3_" + n] * w90.real).sum() / w90.real.sum())
        chips = (f"<span class='chip'>{ide['familia']} · {ide['memoria']}</span><span class='chip'>Temporada: {ide['estac']}</span>"
                 f"<span class='chip'>Trend: {ide['fuente']}{'' if ide['trend'] == '—' else ' · ' + ide['trend']}</span>"
                 f"<span class='chip'>DAs pasado −{ide['dap']}</span><span class='chip'>Cortes +{ide['cortes']}</span><span class='chip'>DAs foto +{ide['daf']}</span>")
        rows += (f"<tr><td class='pn'>{P.dot(n, num=True)}<b>{n}</b><span class='bl'>{'Fijo · ' if p['fijo'] else ''}{P.bloc[n]}</span></td>"
                 f"<td class='f'>{p['formula']}<div class='chips'>{chips}</div></td><td class='n'>{T['seats'][n]}</td><td class='n'>{pc(T['vol'][n])}</td>"
                 f"<td class='n'>{pc(w90v)}</td><td class='n'>{('+' if bias > 0 else '−') + pc(abs(bias))}</td><td class='n'>{pc(err)}</td></tr>")
    tab = (f"<table class='pt'><tr><th>Partido</th><th>Fórmula e ideas</th><th>EANs</th><th>Volumen</th><th>WAPE90</th><th>Desvío</th><th>Error EAN</th></tr>{rows}</table>"
           f"<div class='foot'>Como partido único para todos los EANs: <b>WAPE90</b> = |Σ forecast − Σ real| por casa y quarter, ponderado por volumen (consenso: {pc(pd.DataFrame(D['w90']).pipe(lambda w: (w.Consenso * w.real).sum() / w.real.sum()))}); "
           f"<b>desvío</b> = Σ forecast / Σ real − 1; <b>error EAN</b> = Σ |forecast − real| por EAN y quarter / Σ real. Los partidos nuevos no están pensados para todos: cada uno gana en su nicho.</div>")
    return sec("Los 10 partidos", "Ocho partidos nuevos, uno por forma de base: el dato elige de quién toma el trend y qué hace con DAs y cortes. Siete de los ocho no suman los DAs de la foto.", tab, "pp")


def page_grouping(P, D):
    R = D["robustez"]
    fuera = np.mean([r["fuera"] for r in R]); techo = np.mean([r["techo_fuera"] for r in R]); reg = np.mean([r["solo_reglas"] for r in R])
    forms = pd.Series([f for r in R for f in r["formas_A"]]).value_counts()
    fl = {"LY": "Año pasado", "LY+M6e": "Mixta", "M3": "Media 3M", "M6": "Media 6M", "M12": "Media 12M", "M3e": "Media 3M est.", "M6e": "Media 6M est.", "M12e": "Media 12M est.", "CV": "Ciclo de vida"}
    fr = "".join(f"<tr><td>{fl[k]}</td><td class='n'>{v} de {len(R)}</td></tr>" for k, v in forms.items())
    drop = D["descartes"][0] if D["descartes"] else None
    b1 = (f"<div class='box'><div class='ct'>Qué aporta cada partido</div><div class='cs'>Error del parlamento al ir sumando partidos, en el orden en que más aportan</div>{waterfall(P, D)}</div>")
    b2 = (f"<div class='box'><div class='ct'>¿Sirven para EANs que no se usaron al elegirlos?</div><div class='cs'>10 veces: partidos elegidos con la mitad de los EANs y medidos en la otra mitad</div>"
          f"{robust_chart(D)}<div class='lg2'><span><i style='background:#9AA3AE'></i>Solo las 2 reglas</span><span><i style='background:{INK}'></i>Partidos de la otra mitad</span>"
          f"<span><i class='o'></i>Techo: partidos elegidos con esa misma mitad</span></div>"
          f"<p class='sm'>Media: reglas {pc(reg)} → partidos ajenos {pc(fuera)}, a {f"{abs(fuera - techo) * 100:.1f}".replace(".", ",")} puntos del techo. Los partidos funcionan con EANs que no los eligieron.</p></div>")
    b3 = (f"<div class='box'><div class='ct'>Qué es estable y qué no</div><table class='mini'><tr><th>Forma de base elegida</th><th>Veces</th></tr>{fr}</table>"
          f"<p class='sm'><b>Estable:</b> las formas de base. {', '.join(fl[k] for k, v in forms.items() if v >= len(R) - 1)} salen siempre o casi siempre.</p>"
          f"<p class='sm'><b>No estable:</b> el detalle de cada partido (de quién toma el trend, cuántos DAs y cortes). Con otra mitad de EANs cambia casi siempre, porque muchas combinaciones dan casi el mismo error. "
          f"Hacer la selección libre, sin «una forma por partido», solo bajaría el error de {pc(D['obj_final'])} a {pc(D['obj_libre'])}.</p>"
          + (f"<p class='sm'><b>Forma descartada:</b> {drop['formula']}; quitarla cuesta {f"{abs(drop['obj_sin'] - drop['obj_con']) * 100:.1f}".replace(".", ",")} puntos.</p>" if drop else "")
          + "</div>")
    body = f"<div class='gw'>{b1}<div class='g2'>{b2}{b3}</div></div>"
    ap = [x["obj"] for x in D["aportes"]]
    share3 = (ap[0] - ap[3]) / (ap[0] - ap[-1])
    return sec("Cómo se agruparon", f"Ocho partidos bajan el error del parlamento de {pc(D['obj_reglas'])} a {pc(D['obj_final'])}; los tres primeros hacen el {pc(share3)} del trabajo.", body)


def cards_page(P, kick, title, items, cols, extra="", inside=""):
    return (f"<section class='page'><div class='blob'></div><div class='kick'>{kick}</div><h2>{title}</h2>{iv.legend(P)}"
            f"<div class='grid c{cols}'>{''.join(iv.card(P, t, s, d) for t, s, d in items)}{inside}</div>{extra}</section>")


def page_w90(P, D):
    w = pd.DataFrame(D["w90"])
    cols = ["Consenso"] + P.names
    head = "".join(f"<th>{'<i class=\"cs0\"></i>' if c == 'Consenso' else P.dot(c, num=True)}<span>{'Consenso' if c == 'Consenso' else P.short(c)}</span></th>" for c in cols)
    body = ""
    for h in HOUSES:
        for i, q in enumerate(["FY26.Q2", "FY26.Q3", "FY26.Q4"]):
            r = w[(w.casa == h) & (w.q == q)].iloc[0]
            b = min(cols, key=lambda c: r[c])
            body += f"<tr class='{'hs' if i == 0 else ''}'>" + (f"<td rowspan='3' class='hh'>{h}</td>" if i == 0 else "") + f"<td class='qq'>{QN[q][0]}<span>{QN[q][1]}</span></td>"
            for c in cols:
                col = iv.CONS if c == "Consenso" else P.col[c]
                body += (f"<td class='n' style='background:{col}1F;font-weight:700;color:{INK}'>{pc(r[c])}</td>" if c == b else f"<td class='n'>{pc(r[c])}</td>")
            body += "</tr>"
    tot = "".join(f"<td class='n tt'>{pc((w[c] * w.real).sum() / w.real.sum())}</td>" for c in cols)
    body += f"<tr class='hs tot'><td colspan='2' class='hh'>Ponderado por volumen</td>{tot}</tr>"
    wins = {c: int(sum(min(cols, key=lambda x: r[x]) == c for _, r in w.iterrows())) for c in cols}
    best_new = max(P.names[2:], key=lambda c: -((w[c] * w.real).sum() / w.real.sum()))
    tab = (f"<table class='wt'><tr><th>Casa</th><th>Quarter</th>{head}</tr>{body}</table>"
           f"<div class='foot'>WAPE90 = |Σ forecast − Σ real| / Σ real de la casa en el quarter, con cada partido aplicado a todos los EANs. Resaltado: el menor de la fila. "
           f"Filas ganadas: consenso {wins['Consenso']}, " + ", ".join(f"{P.short(c)} {wins[c]}" for c in P.names if wins[c]) + ".</div>")
    tit = (f"Como regla única para todos, ningún partido nuevo mejora al consenso en el total; {best_new} lo iguala "
           f"({pc((w[best_new] * w.real).sum() / w.real.sum())} contra {pc((w.Consenso * w.real).sum() / w.real.sum())}).")
    return sec("WAPE90 por casa y quarter · cada partido para todos los EANs", tit, tab, "w90p")


def page_time(P, D):
    tl = D["temporal_limpio"]; tt = D["temporal"]
    rows = ""
    for c in ["Fragancias", "Makeup", "Total"]:
        rows += (f"<tr><td><b>{c}</b></td><td class='n hl1'>{pc(tl[c]['ean_elegido'])}</td><td class='n'>{pc(tt[c]['ean_elegido'])}</td>"
                 f"<td class='n'>{pc(tl[c]['ean_regla'])}</td><td class='n'>{pc(tl[c]['ean_cons'])}</td><td class='n'>{pc(tl[c]['acierto'])}</td></tr>")
    t1 = (f"<table class='tt1'><tr><th></th><th>Partidos elegidos con oct–mar</th><th>Partidos de este reporte*</th><th>Regla de su categoría</th><th>Consenso</th><th>Acierta el mejor partido</th></tr>{rows}</table>"
          f"<div class='cs'>Error EAN a EAN en abr–jun (Σ |forecast − real| / Σ real). Cada EAN elige su partido con su error de oct–mar. Al azar se acertaría el mejor partido 1 de cada 10 veces.<br/>"
          f"* Los partidos de este reporte se definieron viendo también abr–jun: su columna es optimista.</div>")
    r2 = ""
    for x in tl["w90"]:
        b = min(["elegido", "regla", "consenso"], key=lambda k: x[k])
        cell = lambda k, col: (f"<td class='n' style='background:{col}1F;font-weight:700'>{pc(x[k])}</td>" if k == b else f"<td class='n'>{pc(x[k])}</td>")
        r2 += f"<tr><td><b>{x['casa']}</b></td>{cell('elegido', INK)}{cell('regla', iv.RGDA)}{cell('consenso', iv.CONS)}</tr>"
    t2 = (f"<table class='tt1'><tr><th>WAPE90 abr–jun</th><th>Cada EAN su partido</th><th>Regla de su categoría + DAs</th><th>Consenso</th></tr>{r2}</table>"
          f"<div class='cs'>Desvío del total de la casa en abr–jun con la prueba limpia (partidos elegidos con oct–mar).</div>")
    lect = ("<div class='box'><div class='ct'>Qué significa</div><ul class='ul'>"
            f"<li><b>EAN a EAN, el sistema de partidos gana con claridad</b>: {pc(tl['Total']['ean_elegido'])} de error contra {pc(tl['Total']['ean_regla'])} de las reglas y {pc(tl['Total']['ean_cons'])} del consenso. "
            f"En fragancias empata con la regla ({pc(tl['Fragancias']['ean_elegido'])} contra {pc(tl['Fragancias']['ean_regla'])}); la ganancia está en makeup ({pc(tl['Makeup']['ean_elegido'])} contra {pc(tl['Makeup']['ean_regla'])}).</li>"
            "<li><b>En el total de la casa no siempre</b>: Burberry abr–jun se desvía un 31% con los partidos y un 4% con la regla. Cuando cada EAN elige su partido, los errores dejan de compensarse entre EANs.</li>"
            "<li><b>Por qué la regla de makeup llega al 100%:</b> por los DAs de la foto. Sin ellos falla un 69% EAN a EAN en abr–jun; con ellos, el 100%: "
            "suman 143 mil unidades en EANs que no las vendieron, aunque en el total de makeup casi se compensan.</li>"
            f"<li><b>El EAN acierta con su partido {pc(tl['Total']['acierto'])} de las veces</b> (al azar, 10%): elegir por el pasado funciona, pero lejos de la perfección.</li>"
            "<li><b>Límite de la prueba:</b> una sola foto, un solo año y un mercado en caída fuerte. Antes de usarlo, hace falta repetir la elección con las fotos de dic-25, mar-26 y jun-26.</li></ul></div>")
    nxt = ("<div class='box'><div class='ct'>Propuesta y siguientes pasos</div><ul class='ul'>"
           "<li><b>Para confirmar:</b> los 8 partidos nuevos. Las formas de base son estables; el detalle de cada una (trend, DAs, cortes) puede simplificarse sin perder casi nada.</li>"
           "<li><b>Los DAs de la foto:</b> 7 de 8 partidos nuevos ganan sin ellos. Merece una prueba propia: sumarlos solo en el total de casa y no EAN a EAN.</li>"
           f"<li><b>El tope de ±30%:</b> {sum(1 for p in D['partidos'][2:] if p['tope'] == 0.6)} de los 8 partidos nuevos prefieren ±60%. Hay que confirmarlo en fotos donde el mercado no esté en caída.</li>"
           "<li><b>Elección con varias fotos:</b> votar con sep-25, dic-25 y mar-26, y usar el ganador en la siguiente, como el best-fit de o9.</li></ul></div>")
    body = f"<div class='g2'><div>{t1}{t2}</div><div class='col'>{lect}{nxt}</div></div>"
    return sec("Prueba en el tiempo", f"Elegir partido con oct–mar y usarlo en abr–jun baja el error EAN a EAN de {pc(tl['Total']['ean_regla'])} a {pc(tl['Total']['ean_elegido'])}. En el total de la casa, la regla sigue siendo más segura.", body)


def main():
    D, E, C, X, Pn = load()
    P = iv.Parties(D)
    EL = D["eleccion"]; PO = EL["por"]
    pages = [page_cover(P, D, E, C), page_method(P, D, X, E, Pn), page_ideas(P, D), page_trend(P, D, X, Pn)]
    cc = C.join(E[["cat", "tramo", "real"]])
    sh = lambda g, k, side: float(((g[k] > 0.3) if side > 0 else (g[k] < -0.3)).mean())
    fr_, mu_ = cc[cc.cat == "Fragancias"], cc[cc.cat == "Makeup"]
    notes1 = [f"<b>Estacionalidad.</b> Con la misma flexibilidad a cada lado, el {pc(sh(fr_, 'estacional', 1))} de los EANs de fragancias acierta más con el perfil mensual de su casa "
              f"(el {pc(sh(fr_, 'estacional', -1))}, con la media plana). Makeup se reparte: {pc(sh(mu_, 'estacional', 1))} estacional, {pc(sh(mu_, 'estacional', -1))} plano. "
              f"Memoria: la mitad está en el centro; 3 y 12 meses le dan casi lo mismo.",
              f"<b>Individualismo.</b> El {pc(float((cc.individual.abs() <= 0.3).mean()))} está en el centro: en sep-25 el trend propio y el de la casa acaban casi en el mismo número. "
              f"De los que se inclinan, los maduros prefieren su propio trend ({pc(sh(cc[cc.tramo == '26+'], 'individual', 1))} contra {pc(sh(cc[cc.tramo == '26+'], 'individual', -1))}) "
              f"y los recién lanzados, el de su casa o categoría ({pc(sh(cc[cc.tramo == '6–11'], 'individual', -1))} contra {pc(sh(cc[cc.tramo == '6–11'], 'individual', 1))}).",
              f"<b>Curva de vida.</b> Solo EANs con edad conocida. La curva de su edad gana en el {pc(sh(cc[cc.tramo == '6–11'], 'ciclo', 1))} de los de 6–11 meses y el "
              f"{pc(sh(cc[cc.tramo == '18–25'], 'ciclo', 1))} de los de 18–25; en los de 12–17 solo en el {pc(sh(cc[cc.tramo == '12–17'], 'ciclo', 1))}. "
              f"La pregunta «¿cómo les fue a los otros a mi edad?» sirve sobre todo al principio y al final del segundo año."]
    notes2 = [f"<b>Fe en el trend.</b> El {pc(sh(cc, 'fe', 1))} acierta más aplicando el trend completo (hasta el tope) y solo el {pc(sh(cc, 'fe', -1))} suavizándolo. "
              f"Ventana: el {pc(float((cc.tventana.abs() <= 0.3).mean()))} no tiene preferencia; de los que sí, más por 3 meses ({pc(sh(cc, 'tventana', 1))}) que por 12 ({pc(sh(cc, 'tventana', -1))}).",
              f"<b>Promociones.</b> En makeup, el {pc(sh(mu_, 'daf', -1))} de los EANs (el {pc(float(mu_.real[mu_.daf < -0.3].sum() / mu_.real.sum()))} del volumen) acierta más sin los DAs de la foto; "
              f"en fragancias, {pc(sh(fr_, 'daf', -1))} sin y {pc(sh(fr_, 'daf', 1))} con. Limpiar o no los DAs del pasado deja al {pc(float((cc.dap.abs() <= 0.3).mean()))} en el centro.",
              f"<b>Cortes.</b> El {pc(float((cc.cortes.abs() <= 0.3).mean()))} está en el centro: sumar o no la mitad de los cortes del pasado apenas cambia el error del EAN."]
    pages.append(page_compass(P, E, C, SPECS1, "Brújulas políticas · 1", f"Fragancias se inclina por la estacionalidad ({pc(sh(fr_, 'estacional', 1))} de sus EANs); los recién lanzados, por la curva de su edad ({pc(sh(cc[cc.tramo == '6–11'], 'ciclo', 1))}).", notes1))
    pages.append(page_compass(P, E, C, SPECS2, "Brújulas políticas · 2", f"Casi la mitad cree en el trend completo; en makeup, el {pc(sh(mu_, 'daf', -1))} de los EANs acierta más sin los DAs de la foto. Los cortes no separan a nadie.", notes2))
    pages.append(page_parties(P, D, E))
    pages.append(page_grouping(P, D))
    qitems = [(QN[q][0], QN[q][1], EL["por_q"][q]) for q in ["FY26.Q2", "FY26.Q3", "FY26.Q4"]]
    qitems += [("Fragancias", "Burberry, Gucci, Marc Jacobs", PO["Categoría"]["Fragancias"]), ("Makeup", "Gucci Make up, Kylie", PO["Categoría"]["Makeup"])]
    pq = EL["por_q"]
    pages.append(cards_page(P, "Por quarter y categoría", f"En los tres quarters, {pq['FY26.Q2']['win_eans']} gana en EANs ({min(pq[q]['seats'][pq[q]['win_eans']] for q in pq)}–{max(pq[q]['seats'][pq[q]['win_eans']] for q in pq)}) "
                            f"y {pq['FY26.Q2']['win_vol']} en volumen ({pc(min(pq[q]['vol'][pq[q]['win_vol']] for q in pq))}–{pc(max(pq[q]['vol'][pq[q]['win_vol']] for q in pq))}).", qitems, 3, "",
                            "<div class='card txt'><div class='ct'>Cómo leerlo</div><p>Hemiciclo: un punto por EAN, todos pesan igual. Barra: parte del real de esos EANs.</p>"
                            "<p>En los quarters, cada EAN vota al partido con menor error de ese quarter; en las categorías, al ganador de su elección.</p>"
                            "<p>Los dos partidos fijos ganan más volumen que EANs: aciertan en EANs grandes.</p></div>"))
    pages.append(cards_page(P, "Por casa", f"En volumen, Burberry y Gucci se quedan con una regla fija ({pc(PO['Casa']['Burberry']['vol']['Regla fragancias'])} y {pc(PO['Casa']['Gucci']['vol']['Regla makeup'])}); Marc Jacobs, Gucci Make up y Kylie, con la media 3M estacional por fase.",
                            [(h, "Fragancias" if h in HOUSES[:3] else "Makeup", PO["Casa"][h]) for h in HOUSES], 3))
    sizes = [("Mini ≤15", "≤15 ml"), ("Pequeño 20–40", "20–40 ml"), ("Medio 45–60", "45–60 ml"), ("Grande 75–125", "75–125 ml"), ("Jumbo/refill ≥150", "≥150 ml"), ("Ancilares", "deo, body lotion, gel")]
    pages.append(cards_page(P, "Por tamaño · solo fragancias", f"Los pequeños (20–40 ml) votan la media 12M estacional de su casa en EANs y en volumen ({pc(PO['Tamaño']['Pequeño 20–40']['vol']['Media 12M estacional · casa'])}); en los grandes, el volumen va al año pasado por franquicia ({pc(PO['Tamaño']['Grande 75–125']['vol']['Año pasado · franquicia'])}).",
                            [(k, s, PO["Tamaño"][k]) for k, s in sizes if k in PO["Tamaño"]], 3))
    pages.append(cards_page(P, "Por edad", f"La edad separa: los de 12–17 meses votan la media 3M estacional ({PO['Edad']['12–17']['seats']['Media 3M estacional · fase']} de 71); los de 18–25, el ciclo de vida, por poco ({PO['Edad']['18–25']['seats']['Ciclo de vida']} contra {PO['Edad']['18–25']['seats']['Media 3M estacional · fase']}).",
                            [(f"{k} meses", s, PO["Edad"][k]) for k, s in TRAMOS], 4,
                            "<div class='foot'>Edad = meses desde el lanzamiento (primer mes de dos seguidos con envío) hasta sep-25. 26+ incluye todo lo lanzado antes de jul-23.</div>"))
    pages.append(cards_page(P, "Por fase de madurez", f"En consolidación gana la media 3M estacional; en declive, la media 3M con el trend de la categoría en EANs y la regla de fragancias en volumen ({pc(PO['Fase']['Declive']['vol']['Regla fragancias'])}).",
                            [(k, s, PO["Fase"][k]) for k, s in FASES], "5 c5"))
    pages.append(cards_page(P, "Por Ignore System Forecast Flag", f"Con bandera 2 (forecast manual), {PO['Bandera']['2.0']['seats']['Media 3M · categoría']} de {PO['Bandera']['2.0']['eans']} EANs votan la media 3M con el trend de la categoría: la más prudente.",
                            [(t, s, PO["Bandera"][k]) for k, t, s in FLAGS], 3))
    pages.append(page_w90(P, D))
    pages.append(page_time(P, D))
    css = vr.CSS + iv.CSS_EXTRA + EXTRA
    html = f"<!doctype html><html><head><meta charset='utf-8'><title>Ideologías por EAN</title><style>{css}</style></head><body>{''.join(pages)}</body></html>"
    hp = W / "reporte_ideologias.html"
    hp.write_text(html, encoding="utf-8")
    subprocess.run([vr.CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={OUT}", f"file://{hp}"], check=True, capture_output=True)
    print(OUT)


EXTRA = f"""
.kick {{ color: {INK2}; }}
.blob {{ background: radial-gradient(circle at 30% 70%, #EEEAFB 0%, #FBEFE8 55%, rgba(247,248,246,0) 72%); }}
h1 {{ font-size: 24pt; }}
.top {{ grid-template-columns: 1.12fr 1fr; gap: 6mm; margin-top: 3mm; }}
.finds {{ position: relative; display: grid; grid-template-columns: repeat(5, 1fr); gap: 2.6mm; margin-top: 3.4mm; }}
.fd {{ background: #fff; border: 1px solid #E6EAEE; border-top: 3px solid {INK}; border-radius: 10px; padding: 2.2mm 2.8mm; }}
.fdt {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 9.4pt; margin-bottom: .8mm; }}
.fdx {{ font-size: 7.2pt; line-height: 1.42; color: {INK2}; }}
.kpis3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.4mm; margin-top: 3mm; }}
.kv2 {{ font-family: InterDisplay, Inter; font-size: 11.5pt; font-weight: 700; margin: .6mm 0 .8mm; line-height: 1.15; }}
.kv2 small {{ font-family: Inter; font-size: 7pt; font-weight: 400; color: {MUTED}; }}
.st {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; }}
.st th {{ font-size: 6.6pt; text-transform: uppercase; letter-spacing: .06em; color: {MUTED}; text-align: left; padding: 1.4mm 2.6mm; border-bottom: 1px solid #E3E7EC; }}
.st td {{ font-size: 8.2pt; padding: .95mm 2.6mm; border-bottom: 1px solid #F1F3F5; }}
.st td .bl, .pt td .bl {{ display: block; font-size: 6.2pt; color: {MUTED}; margin-left: 5mm; }}
.st td.n, .pt td.n, .wt td.n, .tt1 td.n {{ text-align: right; font-variant-numeric: tabular-nums; }}
.box {{ position: relative; background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; padding: 3mm 3.6mm; }}
.box p {{ font-size: 7.8pt; line-height: 1.5; color: {INK2}; margin-top: 1.4mm; }}
.box p.sm, p.sm {{ font-size: 7.3pt; line-height: 1.45; color: {INK2}; margin-top: 1.2mm; }}
.box .cs {{ margin-bottom: 1.4mm; }}
.g2 {{ position: relative; display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; }}
.g2m {{ position: relative; display: grid; grid-template-columns: 1fr 1.1fr; gap: 5mm; margin-top: 2mm; }}
.col {{ display: flex; flex-direction: column; gap: 3mm; }}
.steps {{ display: flex; flex-direction: column; gap: 2.6mm; }}
.stp {{ display: grid; grid-template-columns: 9mm 1fr; gap: 2mm; background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; padding: 2.6mm 3.4mm; }}
.sn {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 17pt; color: {INK2}; line-height: 1; }}
.stt {{ font-weight: 700; font-size: 9.2pt; margin-bottom: .6mm; }}
.stx {{ font-size: 7.7pt; line-height: 1.45; color: {INK2}; }}
.g3 {{ position: relative; display: grid; grid-template-columns: repeat(3, 1fr); gap: 3.4mm; margin-top: 1mm; }}
.g3b {{ position: relative; display: grid; grid-template-columns: 1.05fr 1.05fr .9fr; gap: 4mm; margin-top: 2mm; }}
.ib .ct {{ font-size: 10pt; }}
.lead p {{ font-size: 7.6pt; }}
.sw {{ display: inline-block; width: 2.6mm; height: 2.6mm; border-radius: 1px; vertical-align: -.3mm; margin-right: .6mm; }}
svg.hb .hl {{ font-family: Inter; font-size: 7.6px; font-weight: 600; fill: {INK}; }}
svg.hb .hl.mutedl {{ fill: {MUTED}; font-weight: 400; font-style: italic; }}
svg.hb .hv, svg.hb .hv2 {{ font-family: Inter; font-size: 6.6px; font-weight: 700; fill: {INK}; }}
svg.hb .hn {{ font-weight: 400; fill: {MUTED}; }}
svg .ax {{ font-family: Inter; font-size: 7px; fill: {MUTED}; }}
svg .cl {{ font-family: Inter; font-size: 7px; font-weight: 700; }}
svg .bv {{ font-family: Inter; font-size: 8px; font-weight: 700; fill: {INK}; }}
svg .bd {{ font-family: Inter; font-size: 6.4px; font-weight: 700; fill: #fff; }}
svg .xl {{ font-family: Inter; font-size: 7px; font-weight: 600; fill: {INK2}; }}
svg .xl2 {{ font-family: Inter; font-size: 6.6px; fill: {MUTED}; }}
svg .nbs {{ font-family: Inter; font-size: 6.4px; font-weight: 700; fill: #fff; }}
.ul {{ margin: 1.4mm 0 0 3.6mm; font-size: 7.8pt; line-height: 1.5; color: {INK2}; }}
.ul li {{ margin-bottom: 1.2mm; }}
.g3c {{ position: relative; display: grid; grid-template-columns: repeat(3, 1fr); gap: 3.4mm; }}
.g3n {{ position: relative; display: grid; grid-template-columns: repeat(3, 1fr); gap: 3.4mm; margin-top: 2.4mm; }}
.nt {{ font-size: 7.6pt; line-height: 1.45; color: {INK2}; background: #fff; border: 1px solid #E6EAEE; border-radius: 10px; padding: 2.2mm 3mm; }}
.pp .pt {{ position: relative; width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; margin-top: 1mm; }}
.pt th {{ font-size: 6.4pt; text-transform: uppercase; letter-spacing: .05em; color: {MUTED}; text-align: left; padding: 1.6mm 2.2mm; border-bottom: 1px solid #E3E7EC; }}
.pt td {{ font-size: 8pt; padding: 1.3mm 2.2mm; border-bottom: 1px solid #F1F3F5; vertical-align: middle; }}
.pt td.pn {{ width: 46mm; }}
.pt td.f {{ font-size: 7pt; color: {INK2}; line-height: 1.35; }}
.chips {{ margin-top: .8mm; display: flex; flex-wrap: wrap; gap: .8mm; }}
.chip {{ font-size: 5.8pt; color: {INK2}; background: #F1F3F6; border-radius: 6px; padding: .2mm 1.4mm; }}
.gw {{ position: relative; display: flex; flex-direction: column; gap: 3.4mm; }}
.lg2 {{ display: flex; gap: 4mm; font-size: 6.6pt; color: {INK2}; margin-top: .6mm; flex-wrap: wrap; }}
.lg2 i {{ display: inline-block; width: 2.4mm; height: 2.4mm; border-radius: 50%; margin-right: .8mm; vertical-align: -.3mm; }}
.lg2 i.o {{ background: #fff; border: 1.2px solid {INK}; }}
.mini {{ width: 100%; border-collapse: collapse; margin: 1mm 0; }}
.mini th {{ font-size: 6.4pt; color: {MUTED}; text-align: left; text-transform: uppercase; letter-spacing: .05em; padding: .8mm 1mm; border-bottom: 1px solid #E3E7EC; }}
.mini td {{ font-size: 7.4pt; padding: .5mm 1mm; border-bottom: 1px solid #F3F4F6; }}
.mini td.n {{ text-align: right; }}
.grid.c5 {{ grid-template-columns: repeat(5, 1fr); gap: 2.6mm; }}
.c5 .card {{ padding: 2.2mm 2.4mm; }} .c5 .ct {{ font-size: 10pt; }} .c5 .sr b {{ font-size: 7.4pt; }} .c5 .sr span {{ font-size: 4.8pt; }}
.c5 .verd {{ font-size: 5.8pt; flex-direction: column; gap: .6mm; }}
.c4 .verd {{ font-size: 6.2pt; flex-direction: column; gap: .6mm; }}
.w90p .wt {{ position: relative; width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; }}
.wt th {{ font-size: 6.2pt; font-weight: 700; color: {INK2}; padding: 1.2mm 1.2mm; text-align: right; border-bottom: 1px solid #E3E7EC; vertical-align: bottom; }}
.wt th span {{ display: block; font-weight: 400; color: {MUTED}; font-size: 5.6pt; margin-top: .4mm; }}
.wt th:first-child, .wt th:nth-child(2) {{ text-align: left; }}
.wt td {{ font-size: 7.2pt; padding: .7mm 1.2mm; border-bottom: 1px solid #F5F6F8; }}
.wt tr.hs td {{ border-top: 1.4px solid #D9DEE4; }}
.wt td.hh {{ font-weight: 700; font-size: 8pt; vertical-align: middle; }}
.wt td.qq {{ color: {INK2}; font-size: 7pt; }} .wt td.qq span {{ display: block; color: {MUTED}; font-size: 5.8pt; }}
.wt tr.tot td {{ font-weight: 700; background: #F7F8FA; }}
.cs0 {{ display: inline-block; width: 3.6mm; height: 3.6mm; border-radius: 50%; background: {iv.CONS}; vertical-align: -.5mm; }}
.wt th .nb {{ margin: 0; }}
.tt1 {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; margin: 1mm 0 1.2mm; }}
.tt1 th {{ font-size: 6.4pt; color: {MUTED}; text-transform: uppercase; letter-spacing: .04em; text-align: right; padding: 1.6mm 2.4mm; border-bottom: 1px solid #E3E7EC; }}
.tt1 th:first-child {{ text-align: left; }}
.tt1 td {{ font-size: 8.6pt; padding: 1.5mm 2.4mm; border-bottom: 1px solid #F1F3F5; }}
.tt1 td.hl1 {{ font-weight: 700; background: #F1F2F4; }}
.cs {{ font-size: 7pt; color: {MUTED}; line-height: 1.4; }}
"""

if __name__ == "__main__":
    main()
