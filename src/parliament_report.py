"""Reporte PDF del parlamento de 6 reglas: hemiciclos de varios partidos + volumen, por quarter, casa, tamaño, edad y bandera.
Lee work/parliament.json (correr antes src/parliament.py). Salida: reportes/REPORTE_PARLAMENTO.pdf"""
import json
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import votes_report as vr  # noqa  (geometría del hemiciclo, estilo base, tamaños, edades, banderas)
from parliament import PARTIES  # noqa

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"
OUT = ROOT / "reportes" / "REPORTE_PARLAMENTO.pdf"
COL = {"Año pasado": "#4B5563", "Regla fragancias": "#6B3FA0", "Año pasado × línea": "#2F6FD6",
       "Media 6M estacional": "#D6336C", "Regla makeup": "#D9822B", "Media 3M": "#12A594", "Empate": "#D3D8DF"}
BLOC = {"Año pasado": "Año pasado", "Regla fragancias": "Año pasado", "Año pasado × línea": "Año pasado",
        "Media 6M estacional": "Centro", "Regla makeup": "Nivel reciente", "Media 3M": "Nivel reciente"}
FORM = {"Año pasado": "Mismo mes del año anterior",
        "Regla fragancias": "(Año pasado + 25% cortes − 50% DAs+) × (1 + trend 12M del grupo)",
        "Año pasado × línea": "Año pasado × (1 + trend 12M de su product line; grupo si la line tiene &lt;5 EANs)",
        "Media 6M estacional": "Nivel de los últimos 6 meses sin temporada × perfil mensual de su grupo",
        "Regla makeup": "Media 6M ajustada (+ mín(10% cortes; 10% envío) − 25% DAs+) × (1 + 50% trend 12M)",
        "Media 3M": "Media de los últimos 3 meses, plana"}
SHORT = {"Año pasado": "Año pasado", "Regla fragancias": "R. fragancias", "Año pasado × línea": "AP × línea",
         "Media 6M estacional": "M6M estac.", "Regla makeup": "R. makeup", "Media 3M": "Media 3M", "Empate": "Empate"}
HOUSES = ["Burberry", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"]
QS = ["sep-25 · Q2 FY26", "sep-25 · Q3 FY26", "sep-25 · Q4 FY26", "mar-26 · Q4 FY26", "mar-26 · Q1 FY27*"]
QSUB = {"sep-25 · Q2 FY26": "oct–dic 25", "sep-25 · Q3 FY26": "ene–mar 26", "sep-25 · Q4 FY26": "abr–jun 26",
        "mar-26 · Q4 FY26": "abr–jun 26", "mar-26 · Q1 FY27*": "jul–ago 26 (sep sin cerrar)"}
ORDER = PARTIES + ["Empate"]
INK, INK2, MUTED = vr.INK, vr.INK2, vr.MUTED
pc, n0 = vr.pc, vr.n0


def dot(p, size=3):
    return f"<i class='dt' style='background:{COL[p]};width:{size}mm;height:{size}mm'></i>"


def hemicycle(seats, w=300, big=False):
    n = sum(seats[p] for p in ORDER)
    pts, d = vr.seats(n)
    S0 = w / 2
    r = min(0.40 * d * (S0 - 2) / (1 + 0.40 * d), 24)
    S = S0 - r - 2; cx = w / 2; cy = S + r + 2
    cols = [COL[p] for p in ORDER for _ in range(seats[p])]
    s = [f'<svg viewBox="0 0 {w} {cy + r + 2:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg">']
    for (ang, rad), col in zip(pts, cols):
        s.append(f'<circle cx="{cx + S * rad * math.cos(ang):.1f}" cy="{cy - S * rad * math.sin(ang):.1f}" r="{r:.2f}" fill="{col}"/>')
    fs = 40 if big else 26
    s.append(f'<text x="{cx}" y="{cy - (28 if big else 15)}" text-anchor="middle" class="hc1" style="font-size:{fs}px">{n}</text>')
    s.append(f'<text x="{cx}" y="{cy - (10 if big else 2)}" text-anchor="middle" class="hc2">EANs</text>')
    s.append("</svg>")
    return "".join(s)


def volbar(t):
    h = ""
    for p in ORDER:
        v = t["vol"][p]
        if v > 0.002:
            txt = pc(v) if v >= .09 else ""
            h += f"<div class='sg' style='width:{v * 100:.2f}%;background:{COL[p]};color:{'#46505E' if p == 'Empate' else '#fff'}'>{txt}</div>"
    return f"<div class='bar'>{h}</div>"


def seatrow(t):
    return "<div class='sr'>" + "".join(
        f"<div><b style='color:{COL[p] if p != 'Empate' else MUTED}'>{t['seats'][p]}</b><span>{SHORT[p]}</span></div>" for p in ORDER) + "</div>"


def card(title, sub, t, extra=""):
    we, wv = t["win_eans"], t["win_vol"]
    return (f"<div class='card'><div class='ch'><div><div class='ct'>{title}</div><div class='cs'>{sub}</div></div>"
            f"<div class='cv'>{n0(t['real'])}<span>unid. reales</span></div></div>"
            f"{hemicycle(t['seats'])}{seatrow(t)}"
            f"<div class='vl'>Volumen de los EANs que gana cada partido</div>{volbar(t)}"
            f"<div class='verd'><span>+ EANs: <b style='color:{COL[we]}'>{we}</b></span><span>+ volumen: <b style='color:{COL[wv]}'>{wv}</b></span></div>{extra}</div>")


def legend():
    return ("<div class='leg'>" + "".join(f"<span>{dot(p)}{p}</span>" for p in ORDER) +
            "<span class='lm'>Un punto = un EAN · la barra reparte el volumen real</span></div>")


def page(kick, title, cards, cols, extra=""):
    return (f"<section class='page'><div class='blob'></div><div class='kick'>{kick}</div><h2>{title}</h2>{legend()}"
            f"<div class='grid c{cols}'>{cards}</div>{extra}</section>")


def main():
    V = json.loads((W / "parliament.json").read_text()); T = V["total"]; P = V["por"]; Q = V["por_q"]; PT = V["partidos"]
    first = max(PARTIES, key=lambda p: T["seats"][p]); firstv = max(PARTIES, key=lambda p: T["vol"][p])
    best90 = min(PARTIES, key=lambda p: PT[p]["wape90"]); beste = min(PARTIES, key=lambda p: PT[p]["ean_error"])
    seats_tbl = "".join(
        f"<tr><td>{dot(p)}<b>{p}</b></td><td class='n'>{T['seats'][p]}</td><td class='n'>{pc(T['seats'][p] / T['eans'])}</td><td class='n'>{pc(T['vol'][p])}</td></tr>"
        for p in sorted(ORDER, key=lambda p: (p == "Empate", -T["seats"][p])))
    p1 = f"""<section class='page'><div class='blob'></div>
  <div class='kick'>Parlamento de reglas · 6 partidos · 5 quarters · {n0(T['eans'])} EANs</div>
  <h1>Parlamento fragmentado:<br/><span style='color:{COL[first]}'>ningún partido tiene mayoría.</span></h1>
  <div class='top'>
    <div class='hemi'>{hemicycle(T['seats'], w=520, big=True)}
      <div class='vl' style='margin-top:3mm'>Volumen real de los EANs que gana cada partido</div>{volbar(T)}</div>
    <div class='side'>
      <table class='st'><tr><th>Partido</th><th>Escaños</th><th>%</th><th>Volumen</th></tr>{seats_tbl}</table>
      <div class='kpi'><div class='kl'>Primera fuerza</div>
        <div class='kv' style='font-size:14pt'><span style='color:{COL[first]}'>{first}</span> en EANs ({pc(T['seats'][first] / T['eans'])}) ·
        <span style='color:{COL[firstv]}'>{firstv}</span> en volumen ({pc(T['vol'][firstv])})</div>
        <div class='kl'>Menor desvío total (WAPE90): <b style='color:{COL[best90]}'>{best90}</b> {pc(PT[best90]['wape90'])} ·
        menor error EAN a EAN: <b style='color:{COL[beste]}'>{beste}</b> {pc(PT[beste]['ean_error'])}</div></div>
      <div class='note'><b>Cómo se vota.</b> Cada EAN Central se simula con los 6 partidos en las fotos sep-25 (Q2, Q3, Q4 FY26) y mar-26 (Q4 FY26, Q1 FY27*), contra los actuals de la foto sep-26.
        En cada quarter gana el partido con menor |forecast − real|; el EAN vota por el que gana más quarters y, si empatan, por el de menor error mes a mes ({V['desempates']} EANs se decidieron así).
        Todos los partidos suman los DAs de la foto. {V['inactivos']} EANs sin actividad quedan fuera. * Q1 FY27 = jul–ago (sep-26 sin cerrar).</div>
    </div></div></section>"""
    rows = "".join(
        f"<tr><td>{dot(p, 3.4)}<b>{p}</b><span class='bl'>{BLOC[p]}</span></td><td class='f'>{FORM[p]}</td><td class='n'>{T['seats'][p]}</td>"
        f"<td class='n'>{pc(T['vol'][p])}</td><td class='n'>{PT[p]['quarters']}</td>"
        f"<td class='n {'bst' if p == best90 else ''}'>{pc(PT[p]['wape90'])}</td><td class='n {'bst' if p == beste else ''}'>{pc(PT[p]['ean_error'])}</td></tr>"
        for p in PARTIES)
    bias = " · ".join(f"<b style='color:{COL[p]}'>{p}</b> {PT[p]['bias']:+.0%}".replace("-", "−") for p in PARTIES)
    p2 = f"""<section class='page'><div class='blob'></div><div class='kick'>Los 6 partidos</div>
  <h2>Ganar votos no es lo mismo que acertar el total: Media 3M gana EANs; los partidos con trend aciertan mejor la casa.</h2>
  <table class='pt'><tr><th>Partido</th><th>Fórmula (todos + DAs de la foto)</th><th>Escaños</th><th>Volumen</th><th>Quarters ganados</th><th>WAPE90</th><th>Error EAN</th></tr>{rows}</table>
  <div class='g2'>
    <div class='box'><div class='ct'>Por qué tres partidos se pasan tanto en el total</div>
      <p>Desvío total de los 5 quarters (forecast / real − 1): {bias}.</p>
      <p>Año pasado, Media 6M estacional y Media 3M no llevan trend, así que no recogen la caída frente al año pasado, y además suman los DAs de la foto sobre actuals que ya traían promos: cuentan las promos dos veces.
      Año pasado × línea corrige con el trend de su línea. Las dos reglas decididas además restan los DAs del pasado (50% en fragancias, 25% en makeup).</p></div>
    <div class='box'><div class='ct'>Cómo leer las métricas</div>
      <p><b>Escaños:</b> EANs que eligen ese partido. <b>Volumen:</b> parte del real que está en esos EANs. <b>Quarters ganados:</b> de {n0(V['quarters_total'])} EAN × quarter ({n0(V['quarters_empate'])} empatados).</p>
      <p><b>WAPE90:</b> |Σ forecast − Σ real| / Σ real por casa y quarter, ponderado por volumen. <b>Error EAN:</b> Σ |forecast − real| EAN a EAN / Σ real.</p></div>
  </div></section>"""
    qcards = ""
    for q in QS:
        t = Q[q]; b = min(PARTIES, key=lambda p: t["wape"][p])
        qcards += card(q, QSUB[q], t, f"<div class='wq'><span>Menor WAPE90 del quarter</span><b style='color:{COL[b]}'>{b} {pc(t['wape'][b])}</b></div>")
    qcards += ("<div class='card txt'><div class='ct'>Cómo leerlo</div><p>Aquí cada quarter es una elección por separado: cada EAN vota por el partido que mejor le acertó en ese quarter.</p>"
               "<p>Los empates son sobre todo quarters con real = 0 o EANs sin año pasado o sin envíos recientes, donde varios partidos dan el mismo número.</p></div>")
    p3 = page("Por quarter", "Media 3M es la primera fuerza en EANs en los 5 quarters; el volumen se reparte entre varios partidos.", qcards, "3 qp")
    # página 4: WAPE90 casa x quarter
    w = {(r["house"], r["q"]): r for r in V["w90"]}
    wins = {p: sum(1 for r in V["w90"] if min(PARTIES, key=lambda x: r[x]) == p) for p in PARTIES}
    n_rf, n_lyl, n_tot = wins["Regla fragancias"], wins["Año pasado × línea"], len(V["w90"])
    head = "".join(f"<th>{q.split(' · ')[0]} · {q.split(' · ')[1]}<span>{QSUB[q]}</span></th>" for q in QS)
    body = ""
    for h in HOUSES:
        for i, p in enumerate(PARTIES):
            body += f"<tr class='{'hs' if i == 0 else ''}'>" + (f"<td rowspan='6' class='hh'>{h}</td>" if i == 0 else "") + f"<td class='pp'>{dot(p, 2.4)}{p}</td>"
            for q in QS:
                r = w.get((h, q))
                if not r:
                    body += "<td>–</td>"; continue
                b = min(PARTIES, key=lambda x: r[x])
                body += (f"<td class='n' style='background:{COL[p]}22;font-weight:700;color:{COL[p]}'>{pc(r[p])}</td>" if p == b else f"<td class='n'>{pc(r[p])}</td>")
            body += "</tr>"
    p4 = (f"<section class='page'><div class='blob'></div><div class='kick'>WAPE90 por casa y quarter</div>"
          f"<h2>Casa por casa, Regla fragancias y Año pasado × línea son las que más veces se desvían menos ({n_rf} y {n_lyl} de {n_tot}).</h2>"
          f"<table class='wt'><tr><th>Casa</th><th>Partido</th>{head}</tr>{body}</table>"
          f"<div class='foot'>WAPE90 = |Σ forecast − Σ real| / Σ real de la casa en el quarter. Resaltado: el partido con menor desvío en esa casa y quarter.</div></section>")
    cat = P["Categoría"]; H = P["Casa"]
    p5 = page("Por categoría y casa", "En todas las casas Media 3M gana en EANs; en volumen se reparten Regla makeup, Regla fragancias y Media 3M.",
              card("EANs de fragancias", "Burberry, Gucci, Marc Jacobs", cat["Fragancias"]) + card("EANs de makeup", "Gucci Make up, Kylie", cat["Makeup"])
              + "".join(card(h, "Fragancias" if h in HOUSES[:3] else "Makeup", H[h]) for h in HOUSES)
              + "<div class='card txt'><div class='ct'>Cómo leerlo</div><p>El hemiciclo cuenta EANs: cada uno pesa igual.</p>"
                "<p>La barra pesa por volumen: qué parte del negocio está en EANs donde acierta más cada partido.</p>"
                "<p>Partidos de la izquierda: año pasado. Centro: Media 6M estacional. Derecha: nivel reciente.</p></div>", 4)
    S_ = P["Tamaño"]
    p6 = page("Por tamaño · solo EANs de fragancias", "Por tamaño no hay un partido dominante: Media 3M y Regla makeup lideran en casi todos.",
              "".join(card(lab, sub, S_[k]) for k, lab, sub in vr.SIZES if k in S_), 3)
    A_ = P["Edad"]
    p7 = page("Por edad del EAN", "Los EANs de 12–17 meses se reparten entre Regla makeup, Media 3M y Regla fragancias; el resto, Media 3M.",
              "".join(card(k, sub, A_[k]) for k, sub in vr.AGES if k in A_), 4,
              "<div class='foot'>Edad = meses con envíos hasta la última foto del EAN. Los datos empiezan en jul-23 (máximo visible: 32 meses).</div>")
    F_ = P["Bandera"]
    p8 = page("Por Ignore System Forecast Flag", "Con bandera, Media 3M se lleva casi la mitad de los EANs y suben mucho los empates.",
              "".join(card(k, sub, F_[k]) for k, sub in vr.FLAGS if k in F_), 3,
              "<div class='foot'>Bandera = número de customers ignorados de los 2 seleccionados, en la última foto del EAN (sin bandera = forecast de sistema).</div>")
    css = vr.CSS + EXTRA
    html = f"<!doctype html><html><head><meta charset='utf-8'><title>Parlamento de reglas</title><style>{css}</style></head><body>{p1}{p2}{p3}{p4}{p5}{p6}{p7}{p8}</body></html>"
    hp = W / "reporte_parlamento.html"
    hp.write_text(html, encoding="utf-8")
    subprocess.run([vr.CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={OUT}", f"file://{hp}"], check=True, capture_output=True)
    print(OUT)


EXTRA = f"""
.kick {{ color: {INK2}; }}
.blob {{ background: radial-gradient(circle at 30% 70%, #EAF0FB 0%, #F6EEF2 55%, rgba(247,248,246,0) 72%); }}
.dt {{ display: inline-block; border-radius: 50%; margin-right: 1.6mm; vertical-align: -.3mm; }}
.leg {{ flex-wrap: wrap; gap: 2mm 4mm; }}
.sr {{ display: grid; grid-template-columns: repeat(7, 1fr); text-align: center; margin: 1mm 0 1.6mm; }}
.sr b {{ display: block; font-family: InterDisplay, Inter; font-size: 11pt; }}
.sr span {{ display: block; font-size: 5.4pt; color: {MUTED}; line-height: 1.15; }}
.c4 .sr b {{ font-size: 9.5pt; }} .c4 .sr span {{ font-size: 4.8pt; }}
.verd b {{ font-weight: 700; }}
.st {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; }}
.st th {{ font-size: 6.8pt; text-transform: uppercase; letter-spacing: .06em; color: {MUTED}; text-align: left; padding: 1.6mm 3mm; border-bottom: 1px solid #E3E7EC; }}
.st td {{ font-size: 9pt; padding: 1.5mm 3mm; border-bottom: 1px solid #F1F3F5; }}
.st td.n, .pt td.n, .wt td.n {{ text-align: right; font-variant-numeric: tabular-nums; }}
.pt {{ position: relative; width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; margin-top: 3mm; }}
.pt th {{ font-size: 6.8pt; text-transform: uppercase; letter-spacing: .05em; color: {MUTED}; text-align: left; padding: 2mm 2.6mm; border-bottom: 1px solid #E3E7EC; }}
.pt td {{ font-size: 9pt; padding: 3mm 2.6mm; border-bottom: 1px solid #F1F3F5; vertical-align: middle; }}
.pt td .bl {{ display: block; font-size: 6.8pt; color: {MUTED}; margin-left: 5mm; }}
.pt td.f {{ font-size: 8pt; color: {INK2}; width: 105mm; }}
.pt td.bst {{ font-weight: 700; color: #1F7A4D; background: #E6F4EC; }}
.g2 {{ position: relative; display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; margin-top: 4mm; }}
.box {{ background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; padding: 3mm 4mm; }}
.box p {{ font-size: 8pt; line-height: 1.55; color: {INK2}; margin-top: 1.4mm; }}
.grid.qp svg {{ display: block; width: 70%; margin: 0 auto; }}
.grid.qp {{ gap: 3mm; }} .grid.qp .card {{ padding: 2.4mm 3.4mm; }}
.wq {{ display: flex; justify-content: space-between; align-items: baseline; font-size: 7pt; color: {MUTED}; margin-top: 1.4mm; border-top: 1px solid #EEF1F4; padding-top: 1.2mm; }}
.wq b {{ font-size: 8.4pt; }}
.c4 .card {{ padding: 2.4mm 3mm; }}
.c4 .ct {{ font-size: 10.5pt; }}
.grid.c4 {{ gap: 3mm; }}
.c4 .verd {{ font-size: 6.2pt; }}
.wt {{ position: relative; width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; margin-top: 1mm; }}
.wt th {{ font-size: 7pt; font-weight: 700; color: {INK2}; padding: 1.4mm 2mm; text-align: right; border-bottom: 1px solid #E3E7EC; }}
.wt th:first-child, .wt th:nth-child(2) {{ text-align: left; }}
.wt th span {{ display: block; font-weight: 400; color: {MUTED}; font-size: 6.2pt; }}
.wt td {{ font-size: 7.4pt; padding: .62mm 2mm; border-bottom: 1px solid #F5F6F8; }}
.wt tr.hs td {{ border-top: 1.5px solid #D9DEE4; }}
.wt td.hh {{ font-weight: 700; font-size: 9pt; vertical-align: middle; border-right: 1px solid #EEF1F4; width: 30mm; }}
.wt td.pp {{ color: {INK2}; width: 42mm; }}
"""

if __name__ == "__main__":
    main()
