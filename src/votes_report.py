"""Reporte PDF de la votación por EAN (consenso vs regla + DAs): hemiciclos por grupo con el reparto del volumen.
Grupos: total, casa, tamaño (fragancias), edad del EAN e Ignore System Forecast Flag.
Lee work/votes.json (correr antes src/wape90.py y src/votes.py). Salida: reportes/REPORTE_VOTACION.pdf"""
import json
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"
OUT = ROOT / "reportes" / "REPORTE_VOTACION.pdf"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
INK, INK2, MUTED, GRID = "#16202E", "#46505E", "#8792A0", "#E3E7EC"
RG, CS, EM = "#12A594", "#26408B", "#D3D8DF"   # regla + DAs (verde azulado), consenso (azul marino), empate (gris)
ACC = "#26408B"
HOUSES = ["Burberry", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"]
SIZES = [("mini(<=15ml/penspray)", "Mini", "≤15 ml"), ("pequeño(20-40)", "Pequeño", "20–40 ml"), ("medio(45-60)", "Medio", "45–60 ml"),
         ("grande(75-125)", "Grande", "75–125 ml"), ("refill/jumbo(>=150)", "Jumbo / refill", "≥150 ml"), ("ancilar(deo/BL/SG)", "Ancilares", "deo, body lotion, gel")]
AGES = [("6–11 meses", "Recién pasados a Central"), ("12–17 meses", "Su año pasado es el llenado de canal"),
        ("18–23 meses", "Ya tienen un año comparable"), ("24+ meses", "Historia completa en los datos")]
FLAGS = [("Sin bandera", "Forecast de sistema"), ("Bandera 1", "1 customer ignorado (normalmente el más grande)"), ("Bandera 2", "Los 2 customers ignorados: forecast manual")]
K_SIZE, K_AGE, K_FLAG = "Tamaño (fragancias)", "Edad (meses con envíos en la última foto)", "Ignore System Forecast Flag"


def pc(x):
    return f"{x * 100:.0f}%"


def n0(x):
    return f"{x:,.0f}".replace(",", ".")


def seats(n, R0=0.5):
    """Posiciones de un hemiciclo con separación uniforme: (ángulo, radio) por escaño y diámetro relativo del punto.
    Usa el menor número de filas en el que caben los n escaños; cada fila lleva escaños según su longitud."""
    opts = []   # (d, huecos, filas); se elige el punto más grande con pocos huecos (≤15% de n)
    for rows in range(1 if n <= 10 else 2, 40):
        for i in range(20, 1001):
            d = i / 1000
            r0 = 1 - (rows - 1) * d
            if rows > 1 and not 0.479 <= r0 <= 0.641:
                continue
            if rows == 1 and d < math.pi / max(n - 1, 1):
                continue
            cap = sum(int(math.pi * (r0 + (1 - r0) * j / (rows - 1)) / d) + 1 for j in range(rows)) if rows > 1 else int(math.pi / d) + 1
            if cap >= n:
                opts.append((d, cap - n, rows))
    ok = [o for o in opts if o[1] <= max(1, 0.15 * n)] or [min(opts, key=lambda o: o[1])]
    d, _, rows = max(ok); R0 = 1 - (rows - 1) * d
    radii = [1.0] if rows == 1 else [R0 + (1 - R0) * i / (rows - 1) for i in range(rows)]
    cap = [int(math.pi * r / d) + 1 for r in radii]
    k = [n * c / sum(cap) for c in cap]
    k = [int(x) for x in k]
    rest = sorted(range(rows), key=lambda i: -(n * cap[i] / sum(cap) - k[i]))
    for i in rest[: n - sum(k)]:
        k[i] += 1
    pts = []
    for r, ki in zip(radii, k):
        for j in range(ki):
            pts.append((math.pi * (1 - j / (ki - 1)) if ki > 1 else math.pi / 2, r))
    pts.sort(key=lambda p: (-round(p[0], 6), p[1]))
    return pts, min(d, min(math.pi * r / max(ki - 1, 1) for r, ki in zip(radii, k) if ki))


def hemicycle(r, e, c, w=300, big=False):
    """Hemiciclo: un punto por EAN; izquierda regla + DAs, centro empate, derecha consenso."""
    n = r + e + c
    pts, d = seats(n)
    S0 = w / 2
    dot = min(0.40 * d * (S0 - 2) / (1 + 0.40 * d), 24)   # radio del punto = 40% de la separación, ya descontado el margen
    S = S0 - dot - 2; cx = w / 2; cy = S + dot + 2
    s = [f'<svg viewBox="0 0 {w} {cy + dot + 2:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg">']
    for i, (a, rad) in enumerate(pts):
        col = RG if i < r else (EM if i < r + e else CS)
        s.append(f'<circle cx="{cx + S * rad * math.cos(a):.1f}" cy="{cy - S * rad * math.sin(a):.1f}" r="{dot:.2f}" fill="{col}"/>')
    fs = 40 if big else 26
    s.append(f'<text x="{cx}" y="{cy - (28 if big else 15)}" text-anchor="middle" class="hc1" style="font-size:{fs}px">{n}</text>')
    s.append(f'<text x="{cx}" y="{cy - (10 if big else 2)}" text-anchor="middle" class="hc2">EANs</text>')
    s.append("</svg>")
    return "".join(s)


def volbar(t):
    seg = lambda v, col, cls: (f"<div class='{cls}' style='width:{v * 100:.2f}%;background:{col}'>{pc(v) if v >= .1 else ''}</div>" if v > 0.001 else "")
    return f"<div class='bar'>{seg(t['vol_regla'], RG, 'sg')}{seg(t['vol_emp'], EM, 'sg e')}{seg(t['vol_cons'], CS, 'sg')}</div>"


def chip(a, c):
    return "<b class='wr'>Regla + DAs</b>" if a > c else ("<b class='wc'>Consenso</b>" if c > a else "<b>Empate</b>")


def card(title, sub, t):
    return (f"<div class='card'><div class='ch'><div><div class='ct'>{title}</div><div class='cs'>{sub}</div></div>"
            f"<div class='cv'>{n0(t['real'])}<span>unid. reales</span></div></div>"
            f"{hemicycle(t['regla'], t['empate'], t['consenso'])}"
            f"<div class='nums'><div class='nr'><b>{t['regla']}</b>regla + DAs</div><div class='ne'><b>{t['empate']}</b>empate</div><div class='nc'><b>{t['consenso']}</b>consenso</div></div>"
            f"<div class='vl'>Volumen de los EANs que gana cada uno</div>{volbar(t)}"
            f"<div class='verd'><span>EANs: {chip(t['regla'], t['consenso'])}</span><span>Volumen: {chip(t['vol_regla'], t['vol_cons'])}</span></div></div>")


def legend():
    return (f"<div class='leg'><span><i style='background:{RG}'></i>Regla + DAs</span><span><i style='background:{EM}'></i>Empate</span>"
            f"<span><i style='background:{CS}'></i>Consenso</span><span class='lm'>Un punto = un EAN. La barra reparte el volumen real de los 5 quarters según quién gana cada EAN.</span></div>")


def lectura(D, items):
    li = "".join(f"<li><b>{lab}:</b> regla + DAs {D[k]['regla']} – consenso {D[k]['consenso']} en EANs; "
                 f"{pc(D[k]['vol_regla'])} – {pc(D[k]['vol_cons'])} del volumen.</li>" for k, lab in items if k in D)
    return f"<div class='lect'><div class='ct'>Lectura</div><ul>{li}</ul></div>"


def page(kick, title, cards, cols, extra=""):
    return (f"<section class='page'><div class='blob'></div><div class='kick'>{kick}</div><h2>{title}</h2>{legend()}"
            f"<div class='grid c{cols}'>{cards}</div>{extra}</section>")


def main():
    V = json.loads((W / "votes.json").read_text()); P = V["por"]; T = V["total"]
    H = P["Casa"]; S_ = P[K_SIZE]; A_ = P[K_AGE]; F_ = P[K_FLAG]
    hv = [h for h in HOUSES if H[h]["vol_regla"] > H[h]["vol_cons"]]
    p1 = f"""<section class='page'><div class='blob'></div>
  <div class='kick'>Votación por EAN · consenso vs regla + DAs · fotos sep-25 y mar-26</div>
  <h1>El consenso gana en EANs.<br/><span class='r'>La regla + DAs gana en volumen.</span></h1>
  <div class='top'>
    <div class='hemi'>{hemicycle(T['regla'], T['empate'], T['consenso'], w=520, big=True)}
      <div class='lg3'><div class='r'><b>{T['regla']}</b>Regla + DAs · {pc(T['regla'] / T['eans'])}</div>
        <div class='e'><b>{T['empate']}</b>Empate · {pc(T['empate'] / T['eans'])}</div>
        <div class='c'><b>{T['consenso']}</b>Consenso · {pc(T['consenso'] / T['eans'])}</div></div></div>
    <div class='side'>
      <div class='kpi'><div class='kl'>Volumen real de los EANs que gana cada uno</div>
        <div class='kv'><span class='r'>{pc(T['vol_regla'])}</span> <small>regla + DAs</small> · <span class='c'>{pc(T['vol_cons'])}</span> <small>consenso</small></div>{volbar(T)}</div>
      <div class='kpi'><div class='kl'>Quarters ganados (EAN × quarter)</div>
        <div class='kv'><span class='r'>{n0(T['q_regla'])}</span> <small>regla + DAs</small> · <span class='c'>{n0(T['q_cons'])}</span> <small>consenso</small></div>
        <div class='kl'>de {n0(T['q_total'])}; el resto son empates.</div></div>
      <div class='kpi'><div class='kl'>Casas donde la regla + DAs gana en volumen</div>
        <div class='kv'><span class='r'>{len(hv)}</span><small> de 5</small></div><div class='kl'>{', '.join(hv)}</div></div>
      <div class='note'><b>Cómo se vota.</b> Cada EAN tiene hasta 5 quarters: sep-25 (Q2, Q3, Q4 FY26) y mar-26 (Q4 FY26, Q1 FY27*).
        En cada quarter gana quien tiene menor |forecast − real| en el total del quarter. El EAN vota por quien gana más quarters; si ganan los mismos, es empate.
        Consenso tal cual en la foto; regla + todos los DAs de la foto. Real = foto sep-26. Universo: EANs Central con actividad ({n0(T['eans'])}; {V['inactivos']} sin actividad quedan fuera).
        <br/>* Sep-26 sin cerrar: Q1 FY27 = jul–ago.</div>
    </div></div></section>"""
    p2 = page("Por casa", "Burberry y Gucci: la regla + DAs se lleva el volumen aunque pierda en número de EANs.",
              "".join(card(h, "Fragancias" if h in HOUSES[:3] else "Makeup", H[h]) for h in HOUSES)
              + "<div class='card txt'><div class='ct'>Cómo leerlo</div><p>El hemiciclo cuenta EANs: cada uno pesa igual, sea grande o pequeño.</p>"
                "<p>La barra pesa por volumen: dice qué parte del negocio real está en EANs donde acierta más cada sistema.</p>"
                "<p>Cuando no coinciden, el consenso acierta en muchos EANs pequeños y la regla + DAs en pocos EANs grandes.</p></div>", 3)
    p3 = page("Por tamaño · solo fragancias", "Por tamaño: la regla + DAs gana el volumen en medios, grandes, jumbo y ancilares.",
              "".join(card(lab, sub, S_[k]) for k, lab, sub in SIZES if k in S_), 3)
    p4 = page("Por edad del EAN", "La regla + DAs necesita historia: con menos de 18 meses el consenso arrasa.",
              "".join(card(k, sub, A_[k]) for k, sub in AGES if k in A_), 4,
              "<div class='foot'>Edad = meses con envíos hasta la última foto en la que aparece el EAN. Los datos empiezan en jul-23, así que 24+ incluye todos los EANs con historia completa (máximo visible: 32 meses). Los empates de 6–11 meses son EANs que solo están en la foto de mar-26 (2 quarters, 1–1).</div>"
              + lectura(A_, [(k, k) for k, _ in AGES]))
    p5 = page("Por Ignore System Forecast Flag", "Con la bandera puesta, el forecast manual acierta más que la regla + DAs.",
              "".join(card(k, sub, F_[k]) for k, sub in FLAGS if k in F_), 3,
              "<div class='foot'>Bandera = número de customers ignorados de los 2 seleccionados, en la última foto del EAN (sin bandera = forecast de sistema). "
              "Los empates son casi todos EANs que solo están en la foto de mar-26: tienen 2 quarters y quedan 1–1 (sobre todo lanzamientos de Kylie con bandera 2).</div>"
              + lectura(F_, [("Sin bandera", "Con forecast de sistema"), ("Bandera 1", "Con 1 customer ignorado"), ("Bandera 2", "Con los 2 ignorados")]))
    html = f"<!doctype html><html><head><meta charset='utf-8'><title>Votación por EAN</title><style>{CSS}</style></head><body>{p1}{p2}{p3}{p4}{p5}</body></html>"
    hp = W / "reporte_votacion.html"
    hp.write_text(html, encoding="utf-8")
    OUT.parent.mkdir(exist_ok=True)
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={OUT}", f"file://{hp}"], check=True, capture_output=True)
    print(OUT)


CSS = f"""
@font-face {{ font-family: Inter; src: url('file:///usr/share/fonts/opentype/inter/Inter-Regular.otf'); font-weight: 400; }}
@font-face {{ font-family: Inter; src: url('file:///usr/share/fonts/opentype/inter/Inter-SemiBold.otf'); font-weight: 600; }}
@font-face {{ font-family: Inter; src: url('file:///usr/share/fonts/opentype/inter/Inter-Bold.otf'); font-weight: 700; }}
@font-face {{ font-family: InterDisplay; src: url('file:///usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'); font-weight: 700; }}
@page {{ size: A4 landscape; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Inter, sans-serif; color: {INK}; background: #F7F8F6; }}
.page {{ width: 297mm; height: 210mm; padding: 10mm 13mm 8mm; position: relative; overflow: hidden; page-break-after: always; background: #F7F8F6; }}
.blob {{ position: absolute; right: -60mm; top: -90mm; width: 165mm; height: 165mm; border-radius: 50%;
  background: radial-gradient(circle at 30% 70%, #DDF2EF 0%, #E6EAF5 55%, rgba(247,248,246,0) 72%); }}
.kick {{ position: relative; font-size: 8pt; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: {ACC}; }}
h1 {{ position: relative; font-family: InterDisplay, Inter; font-size: 26pt; letter-spacing: -.02em; line-height: 1.08; margin-top: 1.5mm; }}
h2 {{ position: relative; font-family: InterDisplay, Inter; font-size: 15pt; letter-spacing: -.01em; line-height: 1.15; margin: 1.2mm 0 1.6mm; }}
.r {{ color: {RG}; }} .c {{ color: {CS}; }}
.top {{ position: relative; display: grid; grid-template-columns: 1.08fr 1fr; gap: 7mm; margin-top: 5mm; }}
svg .hc1 {{ font-family: InterDisplay, Inter; font-weight: 700; fill: {INK}; }}
svg .hc2 {{ font-family: Inter; font-size: 10px; fill: {MUTED}; }}
.lg3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; margin-top: 3mm; }}
.lg3 div {{ background: #fff; border: 1px solid #E6EAEE; border-radius: 10px; padding: 2.4mm 3mm; font-size: 8pt; color: {INK2}; border-top: 3px solid; }}
.lg3 .r {{ border-top-color: {RG}; }} .lg3 .e {{ border-top-color: {EM}; }} .lg3 .c {{ border-top-color: {CS}; }}
.lg3 b {{ display: block; font-family: InterDisplay, Inter; font-size: 20pt; color: {INK}; }}
.side {{ display: flex; flex-direction: column; gap: 3mm; }}
.kpi {{ background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; padding: 2.8mm 4mm; }}
.kl {{ font-size: 7.8pt; color: {INK2}; }}
.kv {{ font-family: InterDisplay, Inter; font-size: 19pt; font-weight: 700; margin: .6mm 0 1.2mm; }}
.kv small {{ font-family: Inter; font-size: 8pt; font-weight: 400; color: {MUTED}; }}
.note {{ font-size: 7.4pt; line-height: 1.5; color: {INK2}; background: #fff; border: 1px solid #E6EAEE; border-left: 3px solid {ACC}; border-radius: 10px; padding: 2.6mm 3.4mm; }}
.bar {{ display: flex; height: 5mm; border-radius: 4px; overflow: hidden; background: #EEF1F4; }}
.sg {{ color: #fff; font-size: 7pt; font-weight: 700; display: flex; align-items: center; justify-content: center; white-space: nowrap; }}
.sg.e {{ color: {INK2}; }}
.leg {{ position: relative; display: flex; gap: 5mm; align-items: center; font-size: 7.6pt; color: {INK2}; margin-bottom: 3mm; }}
.leg i {{ display: inline-block; width: 3mm; height: 3mm; border-radius: 50%; margin-right: 1.4mm; vertical-align: -.4mm; }}
.leg .lm {{ color: {MUTED}; margin-left: auto; }}
.grid {{ position: relative; display: grid; gap: 4mm; }}
.grid.c3 {{ grid-template-columns: repeat(3, 1fr); }}
.grid.c4 {{ grid-template-columns: repeat(4, 1fr); }}
.card {{ background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; padding: 3mm 3.6mm 3mm; }}
.ch {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1mm; }}
.ct {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 12pt; }}
.cs {{ font-size: 7pt; color: {MUTED}; margin-top: .3mm; }}
.cv {{ font-weight: 700; font-size: 8.4pt; text-align: right; }}
.cv span {{ display: block; font-size: 6.4pt; font-weight: 400; color: {MUTED}; }}
.nums {{ display: grid; grid-template-columns: repeat(3, 1fr); text-align: center; font-size: 6.6pt; color: {MUTED}; margin: 1mm 0 2mm; }}
.nums b {{ display: block; font-family: InterDisplay, Inter; font-size: 13pt; color: {INK}; }}
.nr b {{ color: {RG}; }} .nc b {{ color: {CS}; }}
.vl {{ font-size: 6.6pt; color: {MUTED}; margin-bottom: .8mm; }}
.verd {{ display: flex; justify-content: space-between; font-size: 7pt; color: {INK2}; margin-top: 1.6mm; }}
.wr {{ color: {RG}; }} .wc {{ color: {CS}; }}
.card.txt p {{ font-size: 8pt; line-height: 1.5; color: {INK2}; margin-top: 2mm; }}
.c4 .ct {{ font-size: 11pt; }}
.lect {{ position: relative; background: #fff; border: 1px solid #E6EAEE; border-left: 3px solid {RG}; border-radius: 12px; padding: 3mm 4mm; margin-top: 4mm; }}
.lect ul {{ margin: 1.5mm 0 0 4mm; font-size: 8.4pt; line-height: 1.7; color: {INK2}; }}
.foot {{ position: relative; font-size: 7.4pt; color: {MUTED}; margin-top: 3mm; }}
"""

if __name__ == "__main__":
    main()
