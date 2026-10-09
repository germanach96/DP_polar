"""Reporte único PDF: WAPE90 por casa y quarter, consenso vs regla (fotos sep-25 y mar-26). Lee work/wape90.json.
Salida: reportes/REPORTE_WAPE90.pdf"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = json.loads((ROOT / "work" / "wape90.json").read_text())
OUT = ROOT / "reportes" / "REPORTE_WAPE90.pdf"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FONT = "/usr/share/fonts/opentype/inter"
INK, INK2, MUTED, GRID = "#1C1A24", "#4A4756", "#8A8796", "#E7E3EC"
GREY = "#A9A6B4"
WIN, WINBG = "#1F7A4D", "#E6F4EC"
LOSE, LOSEBG = "#B4232A", "#FBE9EA"
HOUSES = [("Burberry", "frag"), ("Gucci", "frag"), ("Marc Jacobs", "frag"), ("Gucci Make up", "mu"), ("Kylie Makeup", "mu")]
ACC = {"frag": "#6B3FA0", "mu": "#C2410C"}
SNAPS = [("2025-09", "Foto sep-25", ["FY26.Q2", "FY26.Q3", "FY26.Q4"]), ("2026-03", "Foto mar-26", ["FY26.Q4", "FY27.Q1"])]
QL = {"FY26.Q2": ("Q2 FY26", "oct–dic 25"), "FY26.Q3": ("Q3 FY26", "ene–mar 26"), "FY26.Q4": ("Q4 FY26", "abr–jun 26"), "FY27.Q1": ("Q1 FY27", "jul–ago 26*")}


def get(h, s, q):
    return next((r for r in R if r["house"] == h and r["snap"] == s and r["q"] == q), None)


def pc(x, sign=False):
    s = f"{x * 100:+.0f}%" if sign else f"{x * 100:.0f}%"
    return s.replace("-", "−")


def n0(x):
    return f"{x:,.0f}".replace(",", ".")


def cell(r):
    if r is None:
        return "<td class='na'>–</td>"
    c, g = r["wape_cons"], r["wape_regla"]
    d = g - c
    win = g < c
    cls = "win" if win else "lose"
    return (f"<td class='{cls}'><div class='pair'><span class='c'>{pc(c)}</span><span class='g'>{pc(g)}</span></div>"
            f"<div class='d'>{'▼' if win else '▲'} {abs(d) * 100:.0f} pts</div></td>")


def bar_block(h, fam):
    """Barras horizontales WAPE90 consenso vs regla por quarter (las 5 combinaciones de la casa)."""
    rows = []
    for s, sl, qs in SNAPS:
        for q in qs:
            r = get(h, s, q)
            if r:
                rows.append((f"{sl[5:]} · {QL[q][0]}", r["wape_cons"], r["wape_regla"]))
    w, L, R_, bh, gap = 330, 92, 34, 7, 9
    h_ = len(rows) * (2 * bh + 2 + gap)
    vmax = max(max(c, g) for _, c, g in rows) * 1.05
    sx = lambda v: (w - L - R_) * v / vmax
    s = [f'<svg viewBox="0 0 {w} {h_}" width="100%" xmlns="http://www.w3.org/2000/svg">']
    y = 2
    for lab, c, g in rows:
        s.append(f'<text x="0" y="{y + bh + 3}" class="bl">{lab}</text>')
        s.append(f'<rect x="{L}" y="{y}" width="{sx(c):.1f}" height="{bh}" rx="2" fill="{GREY}"/>')
        s.append(f'<text x="{L + sx(c) + 4:.1f}" y="{y + bh - 0.5}" class="bv">{pc(c)}</text>')
        s.append(f'<rect x="{L}" y="{y + bh + 2}" width="{sx(g):.1f}" height="{bh}" rx="2" fill="{ACC[fam]}"/>')
        s.append(f'<text x="{L + sx(g) + 4:.1f}" y="{y + 2 * bh + 1.5}" class="bv b">{pc(g)}</text>')
        y += 2 * bh + 2 + gap
    s.append("</svg>")
    return "".join(s)


def main():
    wins = sum(1 for r in R if r["wape_regla"] < r["wape_cons"])
    fw = sum(1 for r in R if r["wape_regla"] < r["wape_cons"] and r["house"] in ("Burberry", "Gucci", "Marc Jacobs"))
    ft = sum(1 for r in R if r["house"] in ("Burberry", "Gucci", "Marc Jacobs"))
    mw = wins - fw; mt = len(R) - ft
    # WAPE90 agregado por casa y foto (suma de errores trimestrales / suma real)
    agg = {}
    for h, _ in HOUSES:
        for s, _, qs in SNAPS:
            rr = [get(h, s, q) for q in qs if get(h, s, q)]
            real = sum(r["real"] for r in rr)
            agg[(h, s)] = (sum(r["wape_cons"] * r["real"] for r in rr) / real, sum(r["wape_regla"] * r["real"] for r in rr) / real)
    head = "".join(f"<th colspan='{len(qs)}' class='sn'>{sl}</th>" for _, sl, qs in SNAPS)
    qhead = "".join(f"<th>{QL[q][0]}<span>{QL[q][1]}</span></th>" for _, _, qs in SNAPS for q in qs)
    body = ""
    for h, fam in HOUSES:
        body += f"<tr><td class='h'><i style='background:{ACC[fam]}'></i>{h}</td>" + "".join(cell(get(h, s, q)) for s, _, qs in SNAPS for q in qs) + "</tr>"
    aggrows = "".join(
        f"<tr><td class='h'><i style='background:{ACC[fam]}'></i>{h}</td>"
        + "".join(f"<td>{pc(agg[(h, s)][0])}</td><td class='{'gw' if agg[(h, s)][1] < agg[(h, s)][0] else 'gl'}'>{pc(agg[(h, s)][1])}</td>" for s, _, _ in SNAPS)
        + "</tr>" for h, fam in HOUSES)
    detail = ""
    for h, fam in HOUSES:
        for s, sl, qs in SNAPS:
            for q in qs:
                r = get(h, s, q)
                if r:
                    detail += (f"<tr><td>{h}</td><td>{sl[5:]}</td><td>{QL[q][0]} · {QL[q][1]}</td><td>{r['eans']}</td><td>{n0(r['real'])}</td>"
                               f"<td>{n0(r['consenso'])}</td><td>{n0(r['regla'])}</td><td>{pc(r['bias_cons'], True)}</td><td>{pc(r['bias_regla'], True)}</td>"
                               f"<td>{pc(r['wape_cons'])}</td><td class='{'gw' if r['wape_regla'] < r['wape_cons'] else 'gl'}'>{pc(r['wape_regla'])}</td></tr>")
    cards = "".join(f"<div class='card'><div class='ct'><i style='background:{ACC[fam]}'></i>{h}</div>{bar_block(h, fam)}</div>" for h, fam in HOUSES)
    html = f"""<!doctype html><html><head><meta charset='utf-8'><title>WAPE90 · consenso vs regla</title><style>{CSS}</style></head><body>
<section class="page">
  <div class="blob"></div>
  <header>
    <div class="kick">Reporte · WAPE90 por casa y quarter</div>
    <h1>Consenso vs regla<span class="dot">.</span></h1>
    <div class="tag">Forecast que había en cada foto frente a la regla aplicada con la información de ese momento. Real = foto sep-26.</div>
  </header>
  <div class="kpis">
    <div class="kpi big"><div class="kv">{wins}<span>/{len(R)}</span></div><div class="kl">casa × quarter donde la regla tiene menor WAPE90</div></div>
    <div class="kpi"><div class="kv">{mw}<span>/{mt}</span></div><div class="kl">Makeup (Gucci Make up, Kylie)</div></div>
    <div class="kpi"><div class="kv">{fw}<span>/{ft}</span></div><div class="kl">Fragancias (Burberry, Gucci, Marc Jacobs)</div></div>
    <div class="legend"><div><span class="sw c"></span>Consenso (gris)</div><div><span class="sw g"></span>Regla (negrita)</div>
      <div><span class="sw w"></span>La regla acierta más</div><div><span class="sw l"></span>El consenso acierta más</div></div>
  </div>
  <table class="hm"><tr><th rowspan="2" class="hh">Casa</th>{head}</tr><tr>{qhead}</tr>{body}</table>
  <div class="row2">
    <div class="note"><b>WAPE90</b> = Σ |forecast del quarter − real del quarter| / Σ real del quarter, EAN a EAN. Es el error sobre el total trimestral de cada EAN, así que no penaliza que un pedido caiga un mes antes o después dentro del mismo quarter.
    <br/><b>Universo:</b> EANs donde se aplica la regla (Central, 6+ meses de envíos en la foto); los Local quedan fuera. Consenso tal cual estaba en cada foto.
    <br/><b>*</b> Septiembre 2026 no está cerrado en los datos (la foto de sep-26 es de la semana 38), así que el Q1 FY27 se mide con julio y agosto.</div>
    <div class="aggw"><div class="ct">WAPE90 de toda la foto (todos sus quarters)</div>
      <table class="ag"><tr><th>Casa</th><th>Cons. sep-25</th><th>Regla sep-25</th><th>Cons. mar-26</th><th>Regla mar-26</th></tr>{aggrows}</table></div>
  </div>
</section>
<section class="page">
  <div class="blob"></div>
  <header class="sm"><div class="kick">Detalle por casa</div></header>
  <div class="cards">{cards}<div class="card legend2"><div class="ct">Cómo leerlo</div>
    <p>Cada par de barras es un quarter: <b style="color:{GREY}">gris = consenso</b>, color = regla. Más corta = menos error.</p>
    <p>Las fotos se toman al cierre del mes, por eso el mes de la foto no entra: sep-25 mide oct–jun, mar-26 mide abr–ago.</p></div></div>
</section>
<section class="page">
  <div class="blob"></div>
  <header class="sm"><div class="kick">Detalle por casa · números</div></header>
  <table class="dt"><tr><th>Casa</th><th>Foto</th><th>Quarter</th><th>EANs</th><th>Real</th><th>Consenso</th><th>Regla</th>
    <th>Desvío cons.</th><th>Desvío regla</th><th>WAPE90 cons.</th><th>WAPE90 regla</th></tr>{detail}</table>
</section></body></html>"""
    hp = ROOT / "work" / "reporte_wape90.html"
    hp.write_text(html, encoding="utf-8")
    OUT.parent.mkdir(exist_ok=True)
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={OUT}", f"file://{hp}"], check=True, capture_output=True)
    print(OUT)


CSS = f"""
@font-face {{ font-family: Inter; src: url('file://{FONT}/Inter-Regular.otf'); font-weight: 400; }}
@font-face {{ font-family: Inter; src: url('file://{FONT}/Inter-SemiBold.otf'); font-weight: 600; }}
@font-face {{ font-family: Inter; src: url('file://{FONT}/Inter-Bold.otf'); font-weight: 700; }}
@font-face {{ font-family: InterDisplay; src: url('file://{FONT}/InterDisplay-Bold.otf'); font-weight: 700; }}
@page {{ size: 297mm 210mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Inter, sans-serif; color: {INK}; background: #FBF9F6; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 297mm; height: 210mm; padding: 11mm 13mm 9mm; position: relative; overflow: hidden; page-break-after: always; background: #FBF9F6; }}
.blob {{ position: absolute; right: -60mm; top: -85mm; width: 165mm; height: 165mm; border-radius: 50%;
        background: radial-gradient(circle at 40% 40%, #D9CCEB 0%, #F4EEFB 45%, rgba(255,255,255,0) 70%); opacity: .7; }}
header {{ position: relative; margin-bottom: 4mm; }}
header.sm {{ margin-bottom: 3mm; }}
.kick {{ font-size: 8pt; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: #6B3FA0; }}
h1 {{ font-family: InterDisplay, Inter; font-size: 30pt; letter-spacing: -.02em; line-height: 1.05; margin-top: 1mm; }}
h1 .dot {{ color: #C2410C; }}
.tag {{ font-size: 10.5pt; color: {INK2}; margin-top: 1mm; }}
.kpis {{ position: relative; display: grid; grid-template-columns: 1.2fr 1fr 1fr 1.3fr; gap: 3mm; margin-bottom: 4mm; }}
.kpi {{ background: #fff; border: 1px solid #EEEAF2; border-radius: 12px; padding: 2.6mm 4mm; }}
.kpi.big {{ background: {INK}; color: #fff; border: none; }}
.kv {{ font-family: InterDisplay, Inter; font-size: 22pt; font-weight: 700; line-height: 1.05; }}
.kv span {{ font-size: 12pt; opacity: .6; }}
.kl {{ font-size: 8pt; color: {INK2}; margin-top: .6mm; }}
.kpi.big .kl {{ color: #CFCBD8; }}
.legend {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.2mm 3mm; align-content: center; font-size: 7.6pt; color: {INK2}; padding: 0 2mm; }}
.sw {{ display: inline-block; width: 3mm; height: 3mm; border-radius: 3px; margin-right: 1.4mm; vertical-align: -.5mm; }}
.sw.c {{ background: {GREY}; }} .sw.g {{ background: {INK}; }} .sw.w {{ background: {WINBG}; border: 1px solid {WIN}; }} .sw.l {{ background: {LOSEBG}; border: 1px solid {LOSE}; }}
table {{ width: 100%; border-collapse: separate; border-spacing: 0; }}
.hm {{ position: relative; background: #fff; border: 1px solid #EEEAF2; border-radius: 14px; overflow: hidden; }}
.hm th {{ font-size: 7.6pt; font-weight: 700; color: {INK2}; padding: 1.8mm 2mm; text-align: center; border-bottom: 1px solid {GRID}; }}
.hm th span {{ display: block; font-weight: 400; color: {MUTED}; font-size: 7pt; }}
.hm th.sn {{ font-size: 8pt; letter-spacing: .12em; text-transform: uppercase; color: #6B3FA0; background: #F7F3FC; }}
.hm th.hh {{ text-align: left; }}
.hm td {{ text-align: center; padding: 2mm 1.5mm; border-bottom: 1px solid #F1EEF4; border-left: 3px solid #fff; }}
.hm td.h {{ text-align: left; font-weight: 700; font-size: 9.5pt; border-left: none; white-space: nowrap; }}
.h i, .ct i {{ display: inline-block; width: 2.4mm; height: 2.4mm; border-radius: 50%; margin-right: 1.6mm; }}
.hm td.win {{ background: {WINBG}; }} .hm td.lose {{ background: {LOSEBG}; }}
.pair {{ display: flex; justify-content: center; gap: 2.4mm; align-items: baseline; }}
.pair .c {{ color: {MUTED}; font-size: 9pt; }}
.pair .g {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 13pt; }}
.d {{ font-size: 7pt; font-weight: 700; margin-top: .3mm; }}
.win .d {{ color: {WIN}; }} .lose .d {{ color: {LOSE}; }}
.row2 {{ position: relative; display: grid; grid-template-columns: 1.15fr 1fr; gap: 5mm; margin-top: 4mm; }}
.note {{ font-size: 7.6pt; line-height: 1.5; color: {INK2}; background: #fff; border: 1px solid #EEEAF2; border-left: 3px solid #6B3FA0; border-radius: 10px; padding: 2.6mm 3.4mm; }}
.aggw {{ background: #fff; border: 1px solid #EEEAF2; border-radius: 12px; padding: 2.4mm 3.4mm; }}
.ct {{ font-weight: 700; font-size: 9pt; margin-bottom: 1.4mm; }}
.ag th, .dt th {{ font-size: 6.8pt; text-transform: uppercase; letter-spacing: .05em; color: {MUTED}; font-weight: 600; text-align: right; padding: 1mm 1.6mm; border-bottom: 1px solid {GRID}; }}
.ag th:first-child, .dt th:first-child {{ text-align: left; }}
.ag td, .dt td {{ font-size: 7.8pt; text-align: right; padding: 1mm 1.6mm; border-bottom: 1px solid #F3F1F6; }}
.ag td:first-child, .dt td:first-child {{ text-align: left; }}
td.gw {{ color: {WIN}; font-weight: 700; }} td.gl {{ color: {LOSE}; font-weight: 700; }}
.cards {{ position: relative; display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; margin-bottom: 3mm; }}
.card {{ background: #fff; border: 1px solid #EEEAF2; border-radius: 12px; padding: 2.6mm 3.4mm 2mm; }}
.legend2 p {{ font-size: 7.8pt; color: {INK2}; line-height: 1.45; margin-bottom: 1.2mm; }}
svg .bl {{ font-family: Inter; font-size: 7.6px; fill: {INK2}; }}
svg .bv {{ font-family: Inter; font-size: 7.2px; fill: {MUTED}; }}
svg .bv.b {{ fill: {INK}; font-weight: 700; }}
.dt {{ position: relative; background: #fff; border: 1px solid #EEEAF2; border-radius: 12px; }}
.dt td {{ font-size: 8pt; padding: 1.5mm 2mm; }}
.dt {{ width: 100%; }}
"""

if __name__ == "__main__":
    main()
