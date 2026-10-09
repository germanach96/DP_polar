"""Reporte PDF de la votación por EAN: consenso vs regla + DAs. Lee work/votes.json y work/votes_ean.parquet (correr antes src/votes.py).
Salida: reportes/REPORTE_VOTACION.pdf"""
import json
import math
import subprocess
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"
OUT = ROOT / "reportes" / "REPORTE_VOTACION.pdf"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
INK, INK2, MUTED, GRID = "#1C1A24", "#4A4756", "#8A8796", "#E7E3EC"
RG, CS, EM = "#5B34A0", "#D9822B", "#D9D5DF"   # regla + DAs, consenso, empate
HOUSES = ["Burberry", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"]
SEGS = ["Maduros (18+ meses)", "Jóvenes (6–17 meses)", "Forecast manual"]
SIZES = [("mini(<=15ml/penspray)", "Mini ≤15 ml"), ("pequeño(20-40)", "Pequeño 20–40"), ("medio(45-60)", "Medio 45–60"),
         ("grande(75-125)", "Grande 75–125"), ("refill/jumbo(>=150)", "Jumbo / refill ≥150"), ("ancilar(deo/BL/SG)", "Ancilares")]


def pc(x):
    return f"{x * 100:.0f}%"


def n0(x):
    return f"{x:,.0f}".replace(",", ".")


def hemicycle(r, e, c, w=520):
    """Hemiciclo: un punto por EAN. Izquierda regla + DAs, centro empate, derecha consenso."""
    n = r + e + c; rows = 14; R0, R1 = 0.42, 1.0
    radii = [R0 + (R1 - R0) * i / (rows - 1) for i in range(rows)]
    tot = sum(radii); per = [round(n * x / tot) for x in radii]; per[-1] += n - sum(per)
    pts = []
    for rad, k in zip(radii, per):
        for j in range(k):
            a = math.pi * (1 - j / (k - 1)) if k > 1 else math.pi / 2
            pts.append((a, rad))
    pts.sort(key=lambda p: -p[0])
    cx, cy, S = w / 2, w / 2 * 0.98, w / 2 * 0.96
    dot = S * (R1 - R0) / (rows - 1) * 0.36
    s = [f'<svg viewBox="0 0 {w} {w / 2 + 6:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg">']
    for i, (a, rad) in enumerate(pts):
        col = RG if i < r else (EM if i < r + e else CS)
        s.append(f'<circle cx="{cx + S * rad * math.cos(a):.1f}" cy="{cy - S * rad * math.sin(a):.1f}" r="{dot:.2f}" fill="{col}"/>')
    s.append(f'<text x="{cx}" y="{cy - 38}" text-anchor="middle" class="hc1">{n}</text>')
    s.append(f'<text x="{cx}" y="{cy - 18}" text-anchor="middle" class="hc2">EANs votan</text>')
    s.append("</svg>")
    return "".join(s)


def stack(t, key="eans"):
    """Barra apilada 100%: regla + DAs | empate | consenso, en EANs o en volumen."""
    if key == "eans":
        a, b, c = t["regla"] / t["eans"], t["empate"] / t["eans"], t["consenso"] / t["eans"]
    else:
        a, b, c = t["vol_regla"], t["vol_emp"], t["vol_cons"]
    seg = lambda v, col, cls: (f"<div class='{cls}' style='width:{v * 100:.2f}%;background:{col}'>{pc(v) if v >= .09 else ''}</div>" if v > 0 else "")
    return f"<div class='bar'>{seg(a, RG, 'sg')}{seg(b, EM, 'sg e')}{seg(c, CS, 'sg')}</div>"


def winner(t, key="eans"):
    a, c = (t["regla"], t["consenso"]) if key == "eans" else (t["vol_regla"], t["vol_cons"])
    return ("<span class='wn r'>Regla + DAs</span>" if a > c else "<span class='wn c'>Consenso</span>" if c > a else "<span class='wn'>Empate</span>")


def rows(items):
    h = ""
    for lab, t in items:
        h += (f"<tr><td class='gl'>{lab}<span>{t['eans']} EANs · real {n0(t['real'])}</span></td>"
              f"<td class='bc'>{stack(t)}</td><td class='w'>{winner(t)}</td><td class='bc'>{stack(t, 'vol')}</td><td class='w'>{winner(t, 'vol')}</td></tr>")
    return h


def margin_hist(v, w=520, h=150):
    m = (v.p_regla - v.p_cons).clip(-5, 5).value_counts().reindex(range(-5, 6), fill_value=0)
    vmax = m.max(); bw = (w - 40) / 11
    s = [f'<svg viewBox="0 0 {w} {h + 34}" width="100%" xmlns="http://www.w3.org/2000/svg">']
    for i, (k, n) in enumerate(m.items()):
        bh = h * n / vmax; x = 20 + i * bw
        col = RG if k > 0 else (CS if k < 0 else EM)
        s.append(f'<rect x="{x + 3:.1f}" y="{h - bh + 10:.1f}" width="{bw - 6:.1f}" height="{bh:.1f}" rx="3" fill="{col}"/>')
        s.append(f'<text x="{x + bw / 2:.1f}" y="{h - bh + 6:.1f}" text-anchor="middle" class="hv">{n}</text>')
        lab = f"+{k}" if k > 0 else (f"−{-k}" if k < 0 else "0")
        s.append(f'<text x="{x + bw / 2:.1f}" y="{h + 24}" text-anchor="middle" class="hl">{lab}</text>')
    s.append("</svg>")
    return "".join(s)


def main():
    V = json.loads((W / "votes.json").read_text()); v = pd.read_parquet(W / "votes_ean.parquet")
    T = V["total"]; P = V["por"]
    cat = rows([(k, P["Categoría"][k]) for k in ("Fragancias", "Makeup")])
    house = rows([(h, P["Casa"][h]) for h in HOUSES])
    segr = rows([(s, P["Tipo de EAN"][s]) for s in SEGS])
    abc = rows([(f"{k} · {d}", P["ABC por volumen"][k]) for k, d in [("A", "80% del volumen"), ("B", "siguiente 15%"), ("C", "último 5%")]])
    size = rows([(lab, P["Tamaño (fragancias)"][k]) for k, lab in SIZES if k in P["Tamaño (fragancias)"]])
    # matriz casa × tipo: % de EANs que gana la regla + DAs
    mx = ""
    for h in HOUSES:
        mx += f"<tr><td class='gl'>{h}</td>"
        for s in SEGS:
            t = V["casa_seg"].get(f"{h}|{s}")
            if not t:
                mx += "<td>–</td>"; continue
            r, c = t["regla"], t["consenso"]
            cls = "mr" if r > c else ("mc" if c > r else "")
            mx += f"<td class='{cls}'><b>{r}–{c}</b><span>de {t['eans']} · vol {pc(t['vol_regla'])}–{pc(t['vol_cons'])}</span></td>"
        mx += "</tr>"
    mat = P["Tipo de EAN"]["Maduros (18+ meses)"]
    mg = v.p_regla - v.p_cons; n1 = int((mg.abs() == 1).sum()); n5 = int((mg.abs() >= 4).sum())
    close_txt = (f"Lo más frecuente es ganar por 1 quarter (3–2 o 2–1): {n1} de {len(v)} EANs ({n1 / len(v):.0%}). "
                 f"Las victorias por 4 o 5 quarters de diferencia (5–0, 4–0) son {n5}: {int((mg <= -4).sum())} del consenso y {int((mg >= 4).sum())} de la regla + DAs.")
    html = f"""<!doctype html><html><head><meta charset='utf-8'><title>Votación por EAN</title><style>{CSS}</style></head><body>
<section class="page">
  <div class="blob"></div>
  <div class="kick">Votación por EAN · consenso vs regla + DAs · fotos sep-25 y mar-26</div>
  <h1>El consenso gana en EANs.<br/><span class="r">La regla + DAs gana en volumen.</span></h1>
  <div class="top">
    <div class="hemi">{hemicycle(T['regla'], T['empate'], T['consenso'])}
      <div class="lg"><div><i style="background:{RG}"></i>Regla + DAs<b>{T['regla']}</b><span>{pc(T['regla'] / T['eans'])}</span></div>
        <div><i style="background:{EM}"></i>Empate<b>{T['empate']}</b><span>{pc(T['empate'] / T['eans'])}</span></div>
        <div><i style="background:{CS}"></i>Consenso<b>{T['consenso']}</b><span>{pc(T['consenso'] / T['eans'])}</span></div></div></div>
    <div class="side">
      <div class="kpi"><div class="kl">Volumen real de los EANs que gana cada uno</div>
        <div class="kv"><span class="r">{pc(T['vol_regla'])}</span> <small>regla + DAs</small> · <span class="c">{pc(T['vol_cons'])}</span> <small>consenso</small></div>
        {stack(T, 'vol')}</div>
      <div class="kpi"><div class="kl">Quarters ganados (EAN × quarter)</div>
        <div class="kv"><span class="r">{n0(T['q_regla'])}</span> <small>regla + DAs</small> · <span class="c">{n0(T['q_cons'])}</span> <small>consenso</small></div>
        <div class="kl">de {n0(T['q_total'])}; el resto son empates (casi siempre los dos y el real en 0).</div></div>
      <div class="kpi"><div class="kl">EANs maduros (18+ meses), el núcleo de la regla</div>
        <div class="kv"><span class="r">{mat['regla']}</span> <small>regla + DAs</small> · <span class="c">{mat['consenso']}</span> <small>consenso</small></div>
        <div class="kl">Prácticamente empate en EANs; en volumen la regla + DAs se lleva el {pc(mat['vol_regla'])}.</div></div>
      <div class="note"><b>Cómo se vota.</b> Cada EAN tiene hasta 5 quarters: sep-25 (Q2, Q3, Q4 FY26) y mar-26 (Q4 FY26, Q1 FY27*).
        En cada quarter gana quien tiene menor |forecast − real| en el total del quarter. El EAN vota por quien gana más quarters; si ganan los mismos, es empate.
        Consenso tal cual en la foto; regla + todos los DAs de la foto. Real = foto sep-26. Universo: EANs Central con actividad ({n0(T['eans'])}; {V['inactivos']} sin actividad quedan fuera).
        <br/>* Sep-26 sin cerrar: Q1 FY27 = jul–ago.</div>
    </div>
  </div>
</section>
<section class="page">
  <div class="blob"></div>
  <div class="kick">Por categoría, casa y tipo de EAN</div>
  <h2>Los EANs jóvenes y los de forecast manual son del consenso; en los maduros la pelea está pareja.</h2>
  <table class="vt big"><tr><th></th><th>Votos por EAN</th><th>Gana</th><th>Votos ponderados por volumen</th><th>Gana</th></tr>
    <tr class="sec"><td colspan="5">Categoría</td></tr>{cat}
    <tr class="sec"><td colspan="5">Casa</td></tr>{house}
    <tr class="sec"><td colspan="5">Tipo de EAN (en la última foto)</td></tr>{segr}</table>
  <div class="leg2"><span><i style="background:{RG}"></i>Regla + DAs</span><span><i style="background:{EM}"></i>Empate</span><span><i style="background:{CS}"></i>Consenso</span></div>
</section>
<section class="page">
  <div class="blob"></div>
  <div class="kick">Casa × tipo de EAN · volumen · margen</div>
  <div class="g3">
    <div class="box"><div class="ct">Casa × tipo de EAN · votos regla + DAs – consenso</div>
      <table class="mx"><tr><th></th>{''.join(f'<th>{s}</th>' for s in SEGS)}</tr>{mx}</table>
      <p class="sm">Debajo: EANs del grupo y reparto del volumen (regla + DAs – consenso). Morado = gana la regla + DAs; naranja = gana el consenso.</p></div>
    <div class="box"><div class="ct">Margen de cada EAN: quarters ganados por la regla + DAs − por el consenso</div>
      {margin_hist(v)}
      <p class="sm">A la izquierda, EANs que el consenso gana por mucho; a la derecha, los que gana la regla + DAs. {close_txt}</p></div>
  </div>
  <table class="vt sm2"><tr><th></th><th>Votos por EAN</th><th>Gana</th><th>Votos ponderados por volumen</th><th>Gana</th></tr>
    <tr class="sec"><td colspan="5">ABC por volumen real (dentro de cada categoría)</td></tr>{abc}
    <tr class="sec"><td colspan="5">Tamaño (solo fragancias)</td></tr>{size}</table>
</section></body></html>"""
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
body {{ font-family: Inter, sans-serif; color: {INK}; background: #FBF9F6; }}
.page {{ width: 297mm; height: 210mm; padding: 11mm 13mm 9mm; position: relative; overflow: hidden; page-break-after: always; background: #FBF9F6; }}
.blob {{ position: absolute; right: -60mm; top: -85mm; width: 165mm; height: 165mm; border-radius: 50%;
  background: radial-gradient(circle at 30% 70%, #EDE6F7 0%, #F6EFE6 55%, rgba(251,249,246,0) 72%); }}
.kick {{ position: relative; font-size: 8pt; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: {RG}; }}
h1 {{ position: relative; font-family: InterDisplay, Inter; font-size: 26pt; letter-spacing: -.02em; line-height: 1.08; margin-top: 1.5mm; }}
h2 {{ position: relative; font-family: InterDisplay, Inter; font-size: 15pt; letter-spacing: -.01em; line-height: 1.15; margin: 1.5mm 0 3mm; }}
.r {{ color: {RG}; }} .c {{ color: {CS}; }}
.top {{ position: relative; display: grid; grid-template-columns: 1.08fr 1fr; gap: 7mm; margin-top: 5mm; }}
.hemi svg .hc1 {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 34px; fill: {INK}; }}
.hemi svg .hc2 {{ font-family: Inter; font-size: 11px; fill: {MUTED}; }}
.lg {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; margin-top: 3mm; }}
.lg div {{ background: #fff; border: 1px solid #EEEAF2; border-radius: 10px; padding: 2.4mm 3mm; font-size: 8pt; color: {INK2}; }}
.lg i, .leg2 i {{ display: inline-block; width: 3mm; height: 3mm; border-radius: 50%; margin-right: 1.4mm; vertical-align: -.4mm; }}
.lg b {{ display: block; font-family: InterDisplay, Inter; font-size: 20pt; color: {INK}; margin-top: .8mm; }}
.lg span {{ font-size: 8pt; color: {MUTED}; }}
.side {{ display: flex; flex-direction: column; gap: 3mm; }}
.kpi {{ background: #fff; border: 1px solid #EEEAF2; border-radius: 12px; padding: 2.8mm 4mm; }}
.kl {{ font-size: 7.8pt; color: {INK2}; }}
.kv {{ font-family: InterDisplay, Inter; font-size: 19pt; font-weight: 700; margin: .6mm 0 1.2mm; }}
.kv small {{ font-family: Inter; font-size: 8pt; font-weight: 400; color: {MUTED}; }}
.note {{ font-size: 7.4pt; line-height: 1.5; color: {INK2}; background: #fff; border: 1px solid #EEEAF2; border-left: 3px solid {RG}; border-radius: 10px; padding: 2.6mm 3.4mm; }}
.bar {{ display: flex; height: 5.2mm; border-radius: 4px; overflow: hidden; background: #F1EEF4; }}
.sg {{ color: #fff; font-size: 7pt; font-weight: 700; display: flex; align-items: center; justify-content: center; white-space: nowrap; }}
.sg.e {{ color: {INK2}; }}
.vt {{ position: relative; width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #EEEAF2; border-radius: 12px; }}
.vt th {{ font-size: 6.8pt; text-transform: uppercase; letter-spacing: .06em; color: {MUTED}; font-weight: 600; text-align: left; padding: 1.6mm 2.4mm; border-bottom: 1px solid {GRID}; }}
.vt td {{ padding: 1.1mm 2.4mm; border-bottom: 1px solid #F3F1F6; vertical-align: middle; }}
.vt tr.sec td {{ font-size: 7pt; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: {RG}; background: #F7F3FC; padding: 1.2mm 2.4mm; }}
.vt td.gl {{ font-size: 8.6pt; font-weight: 600; width: 48mm; white-space: nowrap; }}
.vt td.gl span {{ display: block; font-size: 6.6pt; font-weight: 400; color: {MUTED}; }}
.vt td.bc {{ width: 82mm; }}
.vt td.w {{ width: 24mm; }}
.wn {{ font-size: 7.4pt; font-weight: 700; }} .wn.r {{ color: {RG}; }} .wn.c {{ color: {CS}; }}
.leg2 {{ position: relative; margin-top: 2.5mm; font-size: 7.6pt; color: {INK2}; display: flex; gap: 6mm; }}
.g3 {{ position: relative; display: grid; grid-template-columns: 1.1fr 1fr; gap: 5mm; margin: 3mm 0 4mm; }}
.box {{ background: #fff; border: 1px solid #EEEAF2; border-radius: 12px; padding: 3mm 3.6mm; }}
.ct {{ font-weight: 700; font-size: 8.6pt; margin-bottom: 2mm; }}
.mx {{ width: 100%; border-collapse: collapse; }}
.mx th {{ font-size: 6.8pt; color: {MUTED}; font-weight: 600; padding: 1.2mm; text-align: center; }}
.mx td {{ text-align: center; padding: 1.6mm 1.2mm; font-size: 9pt; border-bottom: 1px solid #F3F1F6; border-left: 3px solid #fff; }}
.mx td.gl {{ text-align: left; font-weight: 600; font-size: 8.4pt; border-left: none; white-space: nowrap; }}
.mx td span {{ display: block; font-size: 6.4pt; color: {MUTED}; }}
.mx td.mr {{ background: #EFE8F9; }} .mx td.mr b {{ color: {RG}; }}
.mx td.mc {{ background: #FBEEDF; }} .mx td.mc b {{ color: #A85A12; }}
.sm {{ font-size: 7pt; color: {MUTED}; line-height: 1.45; margin-top: 1.6mm; }}
svg .hv {{ font-family: Inter; font-size: 9px; font-weight: 700; fill: {INK2}; }}
svg .hl {{ font-family: Inter; font-size: 9px; fill: {MUTED}; }}
.sm2 td {{ padding: .8mm 2.4mm; }}
.big td {{ padding: 2.1mm 2.4mm; }}
.big .bar {{ height: 6.4mm; }}
"""

if __name__ == "__main__":
    main()
