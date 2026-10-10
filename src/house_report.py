"""Reporte PDF por casa: consenso (cómo lo hacemos) vs regla decidida, fotos sep-25 y mar-26, real = foto sep-26.
Lee work/house_compare.json (src/house_compare.py). Salida: reportes/REPORTE_<casa>.pdf"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "work" / "house_compare.json").read_text())
OUTDIR = ROOT / "reportes"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FONT = "/usr/share/fonts/opentype/inter"
INK, INK2, MUTED, GRID = "#1C1A24", "#4A4756", "#8A8796", "#E7E3EC"
GREY = "#A9A6B4"
ACC = {"frag": ("#6B3FA0", "#C9B3E6", "#F4EEFB"), "mu": ("#C2410C", "#F2B48E", "#FCEFE6")}
FAMILY = {"Burberry": "frag", "Gucci": "frag", "Marc Jacobs": "frag", "Gucci Make up": "mu", "Kylie Makeup": "mu"}
RULE_TXT = {
    "frag": "Base = mismo mes del año anterior + 25% cortes − 50% DAs positivos · Forecast = Base × (1 + trend 12M de house × tamaño, tope ±30%)",
    "mu": "Mes ajustado = envío + mín(10% cortes ; 10% envío) − 25% DAs positivos · Forecast = media 6M × (1 + ½ trend 12M de la función, tope ±30%)",
}
SNAP_TXT = {"2025-09": "Foto sep-25", "2026-03": "Foto mar-26"}


def n0(x):
    return f"{x:,.0f}".replace(",", ".")


def pc(x, sign=True):
    return (f"{x * 100:+.0f}%" if sign else f"{x * 100:.0f}%").replace("+-", "−").replace("-", "−")


def chart(r, acc, w=360, h=150):
    mo = r["monthly"]; n = len(mo)
    series = [("Real", [m["real"] for m in mo], INK, 2.4), ("Consenso", [m["consenso"] for m in mo], GREY, 2),
              ("Regla", [m["regla"] for m in mo], acc, 2.4)]
    vmax = max(max(v) for _, v, _, _ in series) * 1.12
    L, R, T, B = 40, 10, 8, 20
    X = lambda i: L + (i / max(n - 1, 1)) * (w - L - R)
    Y = lambda v: T + (1 - v / vmax) * (h - T - B)
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg">']
    step = 10 ** (len(str(int(vmax / 4))) - 1)
    tick = max(step, round(vmax / 4 / step) * step)
    t = 0
    while t <= vmax:
        s.append(f'<line x1="{L}" x2="{w - R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="{GRID}"/>')
        s.append(f'<text x="{L - 5}" y="{Y(t) + 3:.1f}" text-anchor="end" class="ax">{n0(t / 1000)}k</text>')
        t += tick
    for i, m in enumerate(mo):
        s.append(f'<text x="{X(i):.1f}" y="{h - 5}" text-anchor="middle" class="ax">{m["mes"]}</text>')
    for name, vals, col, wd in series:
        pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{wd}" stroke-linejoin="round" stroke-linecap="round"/>')
        for i, v in enumerate(vals):
            s.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="2.3" fill="{col}"/>')
    s.append("</svg>")
    return "".join(s)


def verdict(r):
    """Frases de lectura automática (factuales)."""
    out = []
    bc, br = r["bias_cons"], r["bias_regla"]
    closer = "la regla" if abs(br) < abs(bc) else "el consenso"
    out.append(f"<b>Total de la casa:</b> el consenso se desvió {pc(bc)} y la regla {pc(br)}; más cerca del real estuvo <b>{closer}</b>.")
    wc, wr = r["wmape_cons"], r["wmape_regla"]
    if abs(wc - wr) < 0.02:
        out.append(f"<b>EAN a EAN:</b> prácticamente empate (consenso {pc(wc, False)}, regla {pc(wr, False)}).")
    else:
        better = "la regla" if wr < wc else "el consenso"
        out.append(f"<b>EAN a EAN:</b> acierta más <b>{better}</b> (error consenso {pc(wc, False)}, regla {pc(wr, False)}).")
    mat = next((x for x in r["segs"] if x["seg"].startswith("Maduros")), None)
    if mat:
        b2 = "la regla" if mat["err_regla"] < mat["err_cons"] else "el consenso"
        out.append(f"<b>EANs maduros</b> ({pc(mat['real'] / r['real'], False)} del volumen): mejor <b>{b2}</b> "
                   f"(consenso {pc(mat['err_cons'], False)}, regla {pc(mat['err_regla'], False)}).")
    bad = [x for x in r["segs"] if not x["seg"].startswith("Maduros") and x["err_regla"] is not None and x["err_regla"] > x["err_cons"] + 0.05]
    if bad:
        out.append("<b>Donde la regla falla:</b> " + "; ".join(f"{x['seg'].lower()} (regla {pc(x['err_regla'], False)} vs consenso {pc(x['err_cons'], False)})" for x in bad) + ".")
    h = r["hibrido"]
    out.append(f"<b>Regla solo en maduros</b> (resto con su proceso actual): error {pc(h['wmape'], False)}, desvío {pc(h['bias'])}.")
    return out


def panel(r, acc):
    months = f"{r['meses'][0]} a {r['meses'][-1]} · {r['n_meses']} meses"
    tiles = f"""
      <div class="tiles">
        <div class="tile"><div class="tl">Real</div><div class="tv">{n0(r['real'])}</div><div class="ts">unidades</div></div>
        <div class="tile"><div class="tl"><i style="background:{GREY}"></i>Consenso</div><div class="tv">{n0(r['consenso'])}</div><div class="ts">{pc(r['bias_cons'])} vs real</div></div>
        <div class="tile acc"><div class="tl"><i style="background:{acc}"></i>Regla</div><div class="tv">{n0(r['regla'])}</div><div class="ts">{pc(r['bias_regla'])} vs real</div></div>
      </div>"""
    h = r["hibrido"]
    tbl = f"""
      <table class="kt">
        <tr><th></th><th>Consenso</th><th>Regla</th><th>Regla solo en maduros</th></tr>
        <tr><td>Error EAN-mes</td><td>{pc(r['wmape_cons'], False)}</td><td class="b">{pc(r['wmape_regla'], False)}</td><td>{pc(h['wmape'], False)}</td></tr>
        <tr><td>Desvío del total</td><td>{pc(r['bias_cons'])}</td><td class="b">{pc(r['bias_regla'])}</td><td>{pc(h['bias'])}</td></tr>
        <tr><td>EANs donde la regla acierta más</td><td colspan="3">{r['eans_mejor']} de {r['eans_mejor'] + r['eans_peor']}</td></tr>
      </table>"""
    leg = (f"<div class='lg'><span><i style='background:{INK}'></i>Real</span><span><i style='background:{GREY}'></i>Consenso</span>"
           f"<span><i style='background:{acc}'></i>Regla</span></div>")
    return f"""
    <div class="panel">
      <div class="ph"><span class="pill">{SNAP_TXT[r['snap']]}</span><span class="pm">{months} · {r['n_eans']} EANs</span></div>
      {tiles}
      <div class="card"><div class="ct">Total mensual de la casa</div>{leg}{chart(r, acc)}</div>
      {tbl}
    </div>"""


def segs_table(r):
    rows = "".join(
        f"<tr><td>{x['seg']}</td><td>{x['n']}</td><td>{n0(x['real'])}</td><td>{pc(x['err_cons'], False)}</td><td class='b'>{pc(x['err_regla'], False)}</td>"
        f"<td>{pc(x['bias_cons'])}</td><td class='b'>{pc(x['bias_regla'])}</td></tr>" for x in r["segs"] if x["err_cons"] is not None)
    return (f"<table class='dt'><tr><th>Tipo de EAN</th><th>EANs</th><th>Real</th><th>Error consenso</th><th>Error regla</th>"
            f"<th>Desvío consenso</th><th>Desvío regla</th></tr>{rows}</table>")


def q_table(r):
    rows = "".join(
        f"<tr><td>{q['q']}</td><td>{q['meses']}</td><td>{n0(q['real'])}</td><td>{n0(q['consenso'])}</td><td class='b'>{n0(q['regla'])}</td>"
        f"<td>{pc(q['err_cons'], False)}</td><td class='b'>{pc(q['err_regla'], False)}</td></tr>" for q in r["quarters"])
    return (f"<table class='dt'><tr><th>Quarter</th><th>Meses</th><th>Real</th><th>Consenso</th><th>Regla</th><th>Error consenso</th>"
            f"<th>Error regla</th></tr>{rows}</table>")


def ean_table(rows, title):
    if not rows:
        return ""
    tr = "".join(f"<tr><td class='ds'>{x['desc']}</td><td>{n0(x['real'])}</td><td>{n0(x['consenso'])}</td><td class='b'>{n0(x['regla'])}</td>"
                 f"<td>{'+' if x['ahorro'] > 0 else '−'}{n0(abs(x['ahorro']))}</td></tr>" for x in rows)
    return (f"<div class='ct2'>{title}</div><table class='dt'><tr><th>EAN</th><th>Real</th><th>Consenso</th><th>Regla</th>"
            f"<th>Error ahorrado</th></tr>{tr}</table>")


def page(house):
    fam = FAMILY[house]
    acc, accl, accbg = ACC[fam]
    rs = {r["snap"]: r for r in DATA if r["house"] == house}
    s1, s2 = rs["2025-09"], rs["2026-03"]
    lect1 = "".join(f"<li>{t}</li>" for t in verdict(s1))
    lect2 = "".join(f"<li>{t}</li>" for t in verdict(s2))
    local_note = (f"Local (menos de 6 meses de envíos) fuera de la comparación: real {n0(s1['local_real'])} u en sep-25 "
                  f"y {n0(s2['local_real'])} u en mar-26.")
    return f"""
<section class="page" style="--acc:{acc};--accl:{accl};--accbg:{accbg}">
  <div class="blob"></div>
  <header>
    <div class="kick">Reporte por casa · consenso vs regla</div>
    <h1>{house}<span class="dot">.</span></h1>
    <div class="tag">¿Qué hubiera pasado si hubiéramos seguido la regla desde sep-25? Real según la foto de sep-26.</div>
  </header>
  <div class="rule">{RULE_TXT[fam]}</div>
  <div class="two">{panel(s1, acc)}{panel(s2, acc)}</div>
  <footer>Consenso = forecast tal cual estaba en cada foto. Regla calculada solo con la información disponible en esa fecha. Comparación sobre EANs Central (6+ meses de envíos). {local_note}</footer>
</section>
<section class="page" style="--acc:{acc};--accl:{accl};--accbg:{accbg}">
  <div class="blob"></div>
  <header class="sm"><div class="kick">{house} · detalle</div></header>
  <div class="two">
    <div>
      <div class="sh">{SNAP_TXT['2025-09']} · lectura</div><ul class="lect">{lect1}</ul>
      <div class="ct2">Por tipo de EAN</div>{segs_table(s1)}
      <div class="ct2">Por quarter</div>{q_table(s1)}
      {ean_table(s1['top_win'][:5], 'EANs donde la regla hubiera ayudado más')}
    </div>
    <div>
      <div class="sh">{SNAP_TXT['2026-03']} · lectura</div><ul class="lect">{lect2}</ul>
      <div class="ct2">Por tipo de EAN</div>{segs_table(s2)}
      <div class="ct2">Por quarter</div>{q_table(s2)}
      {ean_table(s1['top_loss'][:5], 'EANs donde la regla hubiera fallado más (foto sep-25)')}
    </div>
  </div>
  <footer>Error EAN-mes = suma de |forecast − real| / suma real, EAN a EAN y mes a mes. Desvío = forecast total / real total − 1.
  "Regla solo en maduros" = la regla en EANs de 18+ meses y el consenso en jóvenes y manuales.</footer>
</section>"""


CSS = f"""
@font-face {{ font-family: Inter; src: url('file://{FONT}/Inter-Regular.otf'); font-weight: 400; }}
@font-face {{ font-family: Inter; src: url('file://{FONT}/Inter-SemiBold.otf'); font-weight: 600; }}
@font-face {{ font-family: Inter; src: url('file://{FONT}/Inter-Bold.otf'); font-weight: 700; }}
@font-face {{ font-family: InterDisplay; src: url('file://{FONT}/InterDisplay-Bold.otf'); font-weight: 700; }}
@page {{ size: 297mm 210mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Inter, sans-serif; color: {INK}; background: #FBF9F6; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 297mm; height: 210mm; padding: 11mm 13mm 10mm; position: relative; overflow: hidden; page-break-after: always; background: #FBF9F6; }}
.blob {{ position: absolute; right: -60mm; top: -80mm; width: 160mm; height: 160mm; border-radius: 50%;
        background: radial-gradient(circle at 40% 40%, var(--accl) 0%, var(--accbg) 50%, rgba(255,255,255,0) 70%); opacity: .6; }}
header {{ position: relative; margin-bottom: 3mm; }}
header.sm {{ margin-bottom: 4mm; }}
.kick {{ font-size: 8pt; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: var(--acc); }}
h1 {{ font-family: InterDisplay, Inter; font-size: 32pt; letter-spacing: -.02em; line-height: 1.05; margin-top: 1mm; }}
h1 .dot {{ color: var(--acc); }}
.tag {{ font-size: 11pt; color: {INK2}; margin-top: 1mm; }}
.rule {{ position: relative; font-size: 8pt; color: #D9D6E0; background: {INK}; border-radius: 10px; padding: 2.4mm 4mm; margin-bottom: 4mm; }}
.two {{ position: relative; display: grid; grid-template-columns: 1fr 1fr; gap: 7mm; }}
.panel {{ display: flex; flex-direction: column; gap: 2.6mm; }}
.ph {{ display: flex; align-items: center; gap: 2.5mm; }}
.pill {{ font-weight: 700; font-size: 9pt; color: #fff; background: var(--acc); border-radius: 20px; padding: .6mm 3mm; }}
.pm {{ font-size: 8.5pt; color: {INK2}; }}
.tiles {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.4mm; }}
.tile {{ background: #fff; border: 1px solid #EEEAF2; border-radius: 12px; padding: 2.4mm 3.2mm; }}
.tile.acc {{ border-color: var(--accl); background: var(--accbg); }}
.tl {{ font-size: 7.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: {INK2}; }}
.tl i, .lg i {{ display: inline-block; width: 2.2mm; height: 2.2mm; border-radius: 50%; margin-right: 1mm; vertical-align: -.2mm; }}
.tv {{ font-family: InterDisplay, Inter; font-size: 16pt; font-weight: 700; margin-top: .6mm; }}
.ts {{ font-size: 7.6pt; color: {INK2}; }}
.card {{ background: #fff; border: 1px solid #EEEAF2; border-radius: 12px; padding: 2.6mm 3.4mm 1.4mm; }}
.ct {{ font-weight: 700; font-size: 9pt; }}
.ct2 {{ font-weight: 700; font-size: 8.6pt; margin: 2.6mm 0 1.2mm; }}
.lg {{ display: flex; gap: 3mm; font-size: 7pt; font-weight: 600; color: {INK2}; margin: .6mm 0 .6mm; }}
svg .ax {{ font-family: Inter; font-size: 7.5px; fill: {MUTED}; }}
table {{ width: 100%; border-collapse: collapse; font-size: 7.8pt; }}
.kt {{ background: #fff; border: 1px solid #EEEAF2; border-radius: 12px; overflow: hidden; }}
th {{ text-align: right; font-weight: 600; color: {MUTED}; font-size: 7pt; text-transform: uppercase; letter-spacing: .05em; padding: 1.4mm 2mm; border-bottom: 1px solid {GRID}; }}
th:first-child {{ text-align: left; }}
td {{ text-align: right; padding: 1.2mm 2mm; border-bottom: 1px solid #F1EEF4; }}
td:first-child {{ text-align: left; color: {INK2}; }}
td.b {{ font-weight: 700; color: var(--acc); }}
td.ds {{ font-size: 7pt; max-width: 52mm; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }}
.kt td[colspan] {{ text-align: center; font-weight: 600; }}
.dt {{ background: #fff; border: 1px solid #EEEAF2; border-radius: 10px; }}
.sh {{ font-size: 8.5pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--acc); margin-bottom: 1.4mm; }}
.lect {{ list-style: none; background: #fff; border: 1px solid #EEEAF2; border-left: 3px solid var(--acc); border-radius: 10px; padding: 2.4mm 3.4mm; }}
.lect li {{ font-size: 8pt; line-height: 1.42; color: {INK2}; margin-bottom: 1mm; }}
.lect b {{ color: {INK}; }}
footer {{ position: absolute; left: 13mm; right: 13mm; bottom: 6mm; font-size: 6.9pt; color: {MUTED}; border-top: 1px solid #E7E3EC; padding-top: 1.6mm; line-height: 1.4; }}
"""


def main():
    OUTDIR.mkdir(exist_ok=True)
    for house in FAMILY:
        html = f"<!doctype html><html><head><meta charset='utf-8'><title>{house} · consenso vs regla</title><style>{CSS}</style></head><body>{page(house)}</body></html>"
        slug = house.replace(" ", "_")
        hp = ROOT / "work" / f"reporte_{slug}.html"
        hp.write_text(html, encoding="utf-8")
        out = OUTDIR / f"REPORTE_{slug}.pdf"
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        "--allow-file-access-from-files", f"--print-to-pdf={out}", f"file://{hp}"], check=True, capture_output=True)
        print(out)


if __name__ == "__main__":
    main()
