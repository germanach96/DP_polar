"""Reporte PDF: votación por EAN entre la regla de fragancias y la regla de makeup (hemiciclos + volumen).
Lee work/rulevote.json (correr antes src/rulevote.py). Salida: reportes/REPORTE_VOTACION_REGLAS.pdf
Colores: morado = regla de fragancias, naranja = regla de makeup (los colores de cada categoría)."""
import json
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import votes_report as vr  # noqa  (geometría del hemiciclo y estilo base)

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"
OUT = ROOT / "reportes" / "REPORTE_VOTACION_REGLAS.pdf"
PA, PB, EM = "#6B3FA0", "#D9822B", "#D3D8DF"   # regla fragancias, regla makeup, empate
INK, INK2, MUTED = vr.INK, vr.INK2, vr.MUTED
NA, NB = "Regla fragancias", "Regla makeup"
HOUSES = ["Burberry", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"]
QS = ["sep-25 · Q2 FY26", "sep-25 · Q3 FY26", "sep-25 · Q4 FY26", "mar-26 · Q4 FY26", "mar-26 · Q1 FY27*"]
QSUB = {"sep-25 · Q2 FY26": "oct–dic 25", "sep-25 · Q3 FY26": "ene–mar 26", "sep-25 · Q4 FY26": "abr–jun 26",
        "mar-26 · Q4 FY26": "abr–jun 26", "mar-26 · Q1 FY27*": "jul–ago 26 (sep sin cerrar)"}
pc, n0 = vr.pc, vr.n0


def hemicycle(a, e, b, w=300, big=False):
    n = a + e + b
    pts, d = vr.seats(n)
    S0 = w / 2
    dot = min(0.40 * d * (S0 - 2) / (1 + 0.40 * d), 24)
    S = S0 - dot - 2; cx = w / 2; cy = S + dot + 2
    s = [f'<svg viewBox="0 0 {w} {cy + dot + 2:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg">']
    for i, (ang, rad) in enumerate(pts):
        col = PA if i < a else (EM if i < a + e else PB)
        s.append(f'<circle cx="{cx + S * rad * math.cos(ang):.1f}" cy="{cy - S * rad * math.sin(ang):.1f}" r="{dot:.2f}" fill="{col}"/>')
    fs = 40 if big else 26
    s.append(f'<text x="{cx}" y="{cy - (28 if big else 15)}" text-anchor="middle" class="hc1" style="font-size:{fs}px">{n}</text>')
    s.append(f'<text x="{cx}" y="{cy - (10 if big else 2)}" text-anchor="middle" class="hc2">EANs</text>')
    s.append("</svg>")
    return "".join(s)


def volbar(t):
    seg = lambda v, col, cls: (f"<div class='{cls}' style='width:{v * 100:.2f}%;background:{col}'>{pc(v) if v >= .1 else ''}</div>" if v > 0.001 else "")
    return f"<div class='bar'>{seg(t['vol_a'], PA, 'sg')}{seg(t['vol_emp'], EM, 'sg e')}{seg(t['vol_b'], PB, 'sg')}</div>"


def chip(a, b):
    return "<b class='wa'>Fragancias</b>" if a > b else ("<b class='wb'>Makeup</b>" if b > a else "<b>Empate</b>")


def card(title, sub, t, extra=""):
    return (f"<div class='card'><div class='ch'><div><div class='ct'>{title}</div><div class='cs'>{sub}</div></div>"
            f"<div class='cv'>{n0(t['real'])}<span>unid. reales</span></div></div>"
            f"{hemicycle(t['a'], t['empate'], t['b'])}"
            f"<div class='nums'><div class='na'><b>{t['a']}</b>r. fragancias</div><div class='ne'><b>{t['empate']}</b>empate</div><div class='nb'><b>{t['b']}</b>r. makeup</div></div>"
            f"<div class='vl'>Volumen de los EANs que gana cada regla</div>{volbar(t)}"
            f"<div class='verd'><span>EANs: {chip(t['a'], t['b'])}</span><span>Volumen: {chip(t['vol_a'], t['vol_b'])}</span></div>{extra}</div>")


def legend():
    return (f"<div class='leg'><span><i style='background:{PA}'></i>{NA}</span><span><i style='background:{EM}'></i>Empate</span>"
            f"<span><i style='background:{PB}'></i>{NB}</span><span class='lm'>Un punto = un EAN. La barra reparte el volumen real según qué regla gana cada EAN.</span></div>")


def page(kick, title, cards, cols, extra=""):
    return (f"<section class='page'><div class='blob'></div><div class='kick'>{kick}</div><h2>{title}</h2>{legend()}"
            f"<div class='grid c{cols}'>{cards}</div>{extra}</section>")


def rules_box():
    return ("<div class='card txt'><div class='ct'>Las dos reglas</div>"
            "<p><b class='wa'>Fragancias:</b> mismo mes del año pasado (+25% cortes − 50% DAs+) × (1 + trend 12M del grupo, tope ±30%). Sigue la estacionalidad del año pasado.</p>"
            "<p><b class='wb'>Makeup:</b> media de los últimos 6 meses ajustados (+ mín(10% cortes; 10% envío) − 25% DAs+) × (1 + 50% del trend 12M del grupo). Número plano, sin estacionalidad.</p>"
            "<p>Grupo del trend: casa × tamaño en fragancias, casa × función en makeup. Las dos llevan los DAs de la foto.</p></div>")


def main():
    V = json.loads((W / "rulevote.json").read_text()); T = V["total"]; P = V["por"]; Q = V["por_q"]
    # página 1
    p1 = f"""<section class='page'><div class='blob'></div>
  <div class='kick'>Votación por EAN · regla de fragancias vs regla de makeup · 5 quarters</div>
  <h1><span class='b'>La regla de makeup gana en EANs.</span><br/>En volumen, empate técnico.</h1>
  <div class='top'>
    <div class='hemi'>{hemicycle(T['a'], T['empate'], T['b'], w=520, big=True)}
      <div class='lg3'><div class='a'><b>{T['a']}</b>{NA} · {pc(T['a'] / T['eans'])}</div>
        <div class='e'><b>{T['empate']}</b>Empate · {pc(T['empate'] / T['eans'])}</div>
        <div class='c'><b>{T['b']}</b>{NB} · {pc(T['b'] / T['eans'])}</div></div></div>
    <div class='side'>
      <div class='kpi'><div class='kl'>Volumen real de los EANs que gana cada regla</div>
        <div class='kv'><span class='a'>{pc(T['vol_a'])}</span> <small>r. fragancias</small> · <span class='b'>{pc(T['vol_b'])}</span> <small>r. makeup</small></div>{volbar(T)}</div>
      <div class='kpi'><div class='kl'>Quarters ganados (EAN × quarter)</div>
        <div class='kv'><span class='a'>{n0(T['q_a'])}</span> <small>r. fragancias</small> · <span class='b'>{n0(T['q_b'])}</span> <small>r. makeup</small></div>
        <div class='kl'>de {n0(T['q_total'])}. {T['desempate']} EANs empatados en quarters se decidieron por el error mes a mes.</div></div>
      <div class='kpi'><div class='kl'>Cada categoría con su regla</div>
        <div class='kv' style='font-size:13pt'>EANs de fragancias: <span class='a'>{P['Categoría']['Fragancias']['a']}</span>–<span class='b'>{P['Categoría']['Fragancias']['b']}</span>
          <small>(vol {pc(P['Categoría']['Fragancias']['vol_a'])}–{pc(P['Categoría']['Fragancias']['vol_b'])})</small><br/>
          EANs de makeup: <span class='a'>{P['Categoría']['Makeup']['a']}</span>–<span class='b'>{P['Categoría']['Makeup']['b']}</span>
          <small>(vol {pc(P['Categoría']['Makeup']['vol_a'])}–{pc(P['Categoría']['Makeup']['vol_b'])})</small></div>
        <div class='kl'>Fragancias – makeup. En los EANs de fragancias la regla de fragancias gana el volumen; en los de makeup, la de makeup gana todo.</div></div>
      <div class='note'><b>Cómo se vota.</b> Las dos reglas se aplican a todos los EANs Central con las fotos comunes: sep-25 (Q2, Q3, Q4 FY26) y mar-26 (Q4 FY26, Q1 FY27*).
        En cada quarter gana la regla con menor |forecast − real|. El EAN vota por la que gana más quarters; si empatan, decide el error mes a mes. Real = foto sep-26.
        {n0(T['eans'])} EANs con actividad ({V['inactivos']} sin actividad quedan fuera). * Sep-26 sin cerrar: Q1 FY27 = jul–ago.</div>
    </div></div></section>"""
    # página 2: por quarter
    qcards = ""
    for q in QS:
        t = Q[q]
        ex = (f"<div class='wq'><span>WAPE90 del quarter</span><b class='wa'>{pc(t['wape_a'])}</b><b class='wb'>{pc(t['wape_b'])}</b>"
              f"<em>consenso {pc(t['wape_c'])}</em></div>")
        qcards += card(q, QSUB[q], t, ex)
    p2 = page("Por quarter", "Cada quarter es una elección: la regla de fragancias solo se impone en abr–jun, cuando pesa la estacionalidad.",
              qcards + rules_box(), "3 qp")
    # página 3: WAPE90 casa x quarter
    w = {(r["house"], r["q"]): r for r in V["w90"]}
    head = "".join(f"<th>{q.split(' · ')[0]}<span>{q.split(' · ')[1]}<br/>{QSUB[q]}</span></th>" for q in QS)
    body = ""
    for h in HOUSES:
        body += f"<tr><td class='h'>{h}</td>"
        for q in QS:
            r = w.get((h, q))
            if not r:
                body += "<td>–</td>"; continue
            best = min(("a", r["a"]), ("b", r["b"]), ("c", r["c"]), key=lambda x: x[1])[0]
            cls = {"a": "ba", "b": "bb", "c": "bc"}[best]
            body += (f"<td class='{cls}'><div class='tri'><span class='wa'>{pc(r['a'])}</span><span class='wb'>{pc(r['b'])}</span>"
                     f"<span class='cc'>{pc(r['c'])}</span></div></td>")
        body += "</tr>"
    tot = "".join(f"<td><div class='tri'><span class='wa'>{pc(Q[q]['wape_a'])}</span><span class='wb'>{pc(Q[q]['wape_b'])}</span><span class='cc'>{pc(Q[q]['wape_c'])}</span></div></td>" for q in QS)
    p3 = (f"<section class='page'><div class='blob'></div><div class='kick'>WAPE90 por casa y quarter</div>"
          f"<h2>En el total, la regla de fragancias acierta más de ene a jun; la de makeup, en oct–dic y jul–ago.</h2>"
          f"<div class='leg'><span><i style='background:{PA}'></i>Regla fragancias</span><span><i style='background:{PB}'></i>Regla makeup</span>"
          f"<span><i style='background:#8792A0'></i>Consenso (referencia)</span><span class='lm'>Fondo = la que menos se desvía en ese quarter.</span></div>"
          f"<table class='wt'><tr><th class='hh'>Casa</th>{head}</tr>{body}<tr class='tt'><td class='h'>Total</td>{tot}</tr></table>"
          f"<div class='foot'>WAPE90 = |Σ forecast − Σ real| / Σ real de la casa en el quarter (desvío total en valor absoluto). "
          f"Las dos reglas llevan los DAs de la foto; el consenso va tal cual. EANs Central de cada foto.</div></section>")
    cat = P["Categoría"]; H = P["Casa"]
    p4 = page("Por categoría y casa", "Burberry prefiere su regla; en el resto de casas los EANs se inclinan por la regla de makeup.",
              card("EANs de fragancias", "Burberry, Gucci, Marc Jacobs", cat["Fragancias"]) + card("EANs de makeup", "Gucci Make up, Kylie", cat["Makeup"])
              + "".join(card(h, "Fragancias" if h in HOUSES[:3] else "Makeup", H[h]) for h in HOUSES)
              + "<div class='card txt'><div class='ct'>Cómo leerlo</div><p>El hemiciclo cuenta EANs: cada uno pesa igual.</p>"
                "<p>La barra pesa por volumen: qué parte del negocio está en EANs donde acierta más cada regla.</p>"
                "<p>Que la regla de makeup gane en EANs y la de fragancias en volumen indica que los EANs pequeños prefieren la media plana y los grandes de fragancias, el año pasado con su estacionalidad.</p></div>", 4)
    S_ = P["Tamaño"]
    p5 = page("Por tamaño · solo EANs de fragancias", "En volumen, la regla de fragancias gana en todos los tamaños salvo pequeños y ancilares.",
              "".join(card(lab, sub, S_[k]) for k, lab, sub in vr.SIZES if k in S_), 3)
    A_ = P["Edad"]
    p6 = page("Por edad del EAN", "La edad casi no cambia la preferencia: la regla de makeup gana en EANs en casi todos los tramos y el volumen queda repartido.",
              "".join(card(k, sub, A_[k]) for k, sub in vr.AGES if k in A_), 4,
              "<div class='foot'>Edad = meses con envíos hasta la última foto en la que aparece el EAN. Los datos empiezan en jul-23 (máximo visible: 32 meses).</div>")
    F_ = P["Bandera"]
    p7 = page("Por Ignore System Forecast Flag", "Con bandera, más EANs prefieren la regla de makeup (69–73%) que sin bandera (58%).",
              "".join(card(k, sub, F_[k]) for k, sub in vr.FLAGS if k in F_), 3,
              "<div class='foot'>Bandera = número de customers ignorados de los 2 seleccionados, en la última foto del EAN (sin bandera = forecast de sistema).</div>")
    css = (vr.CSS.replace(vr.RG, PA).replace(vr.CS, PB) + EXTRA)
    html = f"<!doctype html><html><head><meta charset='utf-8'><title>Votación entre reglas</title><style>{css}</style></head><body>{p1}{p2}{p3}{p4}{p5}{p6}{p7}</body></html>"
    hp = W / "reporte_votacion_reglas.html"
    hp.write_text(html, encoding="utf-8")
    subprocess.run([vr.CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={OUT}", f"file://{hp}"], check=True, capture_output=True)
    print(OUT)


EXTRA = f"""
.kick {{ color: {INK2}; }}
.a, .wa {{ color: {PA}; }} .b, .wb {{ color: {PB}; }}
.lg3 .a {{ border-top-color: {PA}; color: {INK2}; }} .lg3 .c {{ border-top-color: {PB}; color: {INK2}; }}
.na b {{ color: {PA}; }} .nb b {{ color: {PB}; }}
.blob {{ background: radial-gradient(circle at 30% 70%, #EEE6F7 0%, #FBEEDF 55%, rgba(247,248,246,0) 72%); }}
.note {{ border-left-color: {PA}; }}
.grid.qp svg {{ display: block; width: 74%; margin: 0 auto; }}
.grid.c3.qp, .grid.qp {{ gap: 3mm; }} .grid.qp .card {{ padding: 2.4mm 3.4mm; }}
.wq {{ display: flex; align-items: baseline; gap: 2.4mm; font-size: 7pt; color: {MUTED}; margin-top: 1.6mm; border-top: 1px solid #EEF1F4; padding-top: 1.4mm; }}
.wq b {{ font-family: InterDisplay, Inter; font-size: 11pt; }} .wq em {{ font-style: normal; margin-left: auto; }}
.c4 .card {{ padding: 2.4mm 3mm; }}
.c4 .ct {{ font-size: 10.5pt; }}
.c4 .nums b {{ font-size: 11pt; }}
.c4 .grid, .grid.c4 {{ gap: 3mm; }}
.wt {{ position: relative; width: 100%; border-collapse: separate; border-spacing: 0; background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; margin-top: 2mm; }}
.wt th {{ font-size: 8pt; font-weight: 700; color: {INK2}; padding: 2.4mm 2mm; text-align: center; border-bottom: 1px solid #E3E7EC; }}
.wt th span {{ display: block; font-weight: 400; color: {MUTED}; font-size: 7pt; }}
.wt th.hh {{ text-align: left; }}
.wt td {{ padding: 3mm 2mm; border-bottom: 1px solid #F1F3F5; border-left: 3px solid #fff; text-align: center; }}
.wt td.h {{ text-align: left; font-weight: 700; font-size: 10pt; border-left: none; }}
.wt td.ba {{ background: #F1EAFA; }} .wt td.bb {{ background: #FCEFE0; }} .wt td.bc {{ background: #EEF1F4; }}
.wt tr.tt td {{ border-top: 2px solid #E3E7EC; font-weight: 700; }}
.tri {{ display: flex; justify-content: center; gap: 3mm; font-family: InterDisplay, Inter; font-weight: 700; font-size: 11.5pt; }}
.tri .cc {{ color: {MUTED}; font-size: 9pt; font-weight: 400; font-family: Inter; align-self: center; }}
"""

if __name__ == "__main__":
    main()
