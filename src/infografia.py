"""Infographic (English, 2 landscape A4 pages): formula + reasoning + charts for the Fragrance and Makeup rules.
Builds HTML with inline SVG charts and prints it to PDF with headless Chromium.
Chart data: work/infog_data.json. Usage: python3 src/infografia.py  -> INFOGRAFIA_REGLAS.pdf (+ work/infografia.html)"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "work" / "infog_data.json").read_text())
HTML = ROOT / "work" / "infografia.html"
OUT = ROOT / "INFOGRAFIA_REGLAS.pdf"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FONT = "/usr/share/fonts/opentype/inter"
MONTHS = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"]

INK, INK2, MUTED, GRID = "#1C1A24", "#4A4756", "#8A8796", "#E7E3EC"
PLUM = {"light": "#C9B3E6", "mid": "#8E62C4", "dark": "#4B1F7A", "bg": "#F4EEFB"}
CLAY = {"light": "#F2B48E", "mid": "#DD6B2B", "dark": "#9A3412", "bg": "#FCEFE6"}


# ---------------------------------------------------------------- SVG helpers
def scale(v, lo, hi, a, b):
    return a + (v - lo) / (hi - lo) * (b - a)


def line_chart(series, w, h, ylo, yhi, yticks, xlabels, fmt, ref=None, pad=(30, 14, 22, 8), notes=()):
    """series: list of dict(values, color, width, label, dy). Returns an SVG string."""
    L, R, B, T = pad
    n = len(xlabels)
    X = lambda i: scale(i, 0, n - 1, L, w - R)
    Y = lambda v: scale(v, ylo, yhi, h - B, T)
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg">']
    for t in yticks:
        s.append(f'<line x1="{L}" x2="{w - R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="{L - 6}" y="{Y(t) + 3:.1f}" text-anchor="end" class="ax">{fmt(t)}</text>')
    if ref is not None:
        s.append(f'<line x1="{L}" x2="{w - R}" y1="{Y(ref):.1f}" y2="{Y(ref):.1f}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3 3"/>')
    for i, lab in enumerate(xlabels):
        if lab:
            s.append(f'<text x="{X(i):.1f}" y="{h - 6}" text-anchor="middle" class="ax">{lab}</text>')
    for x0, x1, txt in notes:
        s.append(f'<rect x="{X(x0) - 7:.1f}" y="{T}" width="{X(x1) - X(x0) + 14:.1f}" height="{h - B - T}" fill="#1C1A24" opacity="0.045" rx="5"/>')
        s.append(f'<text x="{(X(x0) + X(x1)) / 2:.1f}" y="{h - B - 4}" text-anchor="middle" class="note">{txt}</text>')
    for se in series:
        pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(se["values"]) if v is not None)
        s.append(f'<polyline points="{pts}" fill="none" stroke="{se["color"]}" stroke-width="{se.get("width", 2)}" '
                 f'stroke-linejoin="round" stroke-linecap="round"/>')
        if se.get("label"):
            i, v = [(i, v) for i, v in enumerate(se["values"]) if v is not None][-1]
            s.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="3.2" fill="{se["color"]}" stroke="#fff" stroke-width="1.5"/>')
            s.append(f'<text x="{X(i) + 7:.1f}" y="{Y(v) + se.get("dy", 0) + 3:.1f}" class="lab">{se["label"]}</text>')
    s.append("</svg>")
    return "".join(s)


def bar_chart(rows, w, xmax, color_for):
    """rows: (label, value, note). Horizontal bars; values and labels in ink."""
    L, R, bh, gap = 92, 74, 12, 5
    h = len(rows) * (bh + gap)
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg">']
    for i, (lab, v, note) in enumerate(rows):
        y = i * (bh + gap) + 2
        bw = scale(v, 0, xmax, 0, w - L - R)
        s.append(f'<text x="0" y="{y + 9}" class="blab">{lab}</text>')
        s.append(f'<rect x="{L}" y="{y}" width="{w - L - R}" height="{bh}" rx="4" fill="#F2EFF5"/>')
        s.append(f'<rect x="{L}" y="{y}" width="{bw:.1f}" height="{bh}" rx="4" fill="{color_for(lab)}"/>')
        s.append(f'<text x="{L + bw + 6:.1f}" y="{y + 9}" class="bval">{v * 100:.0f}%</text>')
        s.append(f'<text x="{w}" y="{y + 9}" text-anchor="end" class="bsub">{note}</text>')
    s.append("</svg>")
    return "".join(s)


pct = lambda t: f"{t * 100:+.0f}%" if abs(t) > 1e-9 else "0%"
idx = lambda t: f"{t:.1f}×"


# ---------------------------------------------------------------- charts
def chart_frag_season():
    fs = DATA["frag_season"]
    ser = [dict(values=fs["FY24"], color=PLUM["light"], width=1.8, label=None),
           dict(values=fs["FY25"], color=PLUM["mid"], width=1.8, label=None),
           dict(values=fs["FY26"], color=PLUM["dark"], width=2.2, label=None)]
    return line_chart(ser, 245, 128, 0.3, 2.15, [0.5, 1.0, 1.5, 2.0],
                      [m if m in ("Jul", "Sep", "Dec", "Mar", "Jun") else "" for m in MONTHS], idx, ref=1.0,
                      pad=(26, 8, 18, 14), notes=[(0, 2, "Xmas load")])


def chart_trend_windows():
    y3, y12 = DATA["yoy3"], DATA["yoy12"]
    keys = [k for k in y3 if k >= "2025-06"]
    lab = [{"2025-06": "Jun 25", "2025-12": "Dec 25", "2026-06": "Jun 26"}.get(k, "") for k in keys]
    ser = [dict(values=[y3[k] for k in keys], color=PLUM["light"], width=1.8, label=None),
           dict(values=[y12.get(k) for k in keys], color=PLUM["dark"], width=2.4, label=None)]
    return line_chart(ser, 245, 132, -0.4, 0.25, [-0.3, -0.15, 0.0, 0.15], lab, pct, ref=0.0, pad=(28, 8, 18, 6))


def chart_mu_season(kind):
    if kind == "ship":
        d = DATA["mu_ship"]
        ser = [dict(values=d["FY24"], color=CLAY["light"], width=1.8, label=None),
               dict(values=d["FY25"], color=CLAY["mid"], width=1.8, label=None),
               dict(values=d["FY26"], color=CLAY["dark"], width=2.3, label=None)]
    else:
        d = DATA["mu_epos"]
        ser = [dict(values=d["FY25"], color=CLAY["mid"], width=1.8, label=None),
               dict(values=d["FY26"], color=CLAY["dark"], width=2.3, label=None)]
    lab = [m if m in ("Jul", "Dec", "Jun") else "" for m in MONTHS]
    notes = [(5, 5, "Dec")] if kind == "epos" else []
    return line_chart(ser, 245, 88, 0.3, 2.3, [0.5, 1.0, 1.5, 2.0], lab, idx, ref=1.0, pad=(26, 8, 16, 10), notes=notes)


def chart_cuts():
    c = DATA["cuts"]
    rows = [("Fragrances", c["Fragrances"], "we count 25%"), ("Gucci Make up", c["Gucci Make up"], "we count 10%"),
            ("Kylie Makeup", c["Kylie Makeup"], "we count 10%")]
    return bar_chart(rows, 500, 0.8, lambda lab: PLUM["mid"] if lab == "Fragrances" else CLAY["mid"])


# ---------------------------------------------------------------- content
FRAG = dict(
    key="frag", acc=PLUM, title="Fragrances", kicker="Forecast rule",
    tagline="Keep last year's shape. Apply this year's direction.",
    formula=[("BASE", "= same month last year <span class='op'>+</span> <b>25%</b> of its supply cuts <span class='op'>−</span> <b>50%</b> of its positive DAs"),
             ("FORECAST", "= BASE <span class='op'>×</span> (1 + <b>12-month trend</b> of house × size)")],
    eg="1,000 shipped last October &nbsp;+50 cuts &nbsp;−50 DAs &nbsp;→ base 1,000 &nbsp;× 0.90 (trend −10%) &nbsp;= <b>900</b>",
    how=["<b>Trend</b> = last 12 closed months ÷ the 12 before − 1, on actual shipments only. Capped at ±30%.",
         "<b>Size groups</b>: minis ≤15 ml · 20–40 · 45–60 · 75–125 · 150 ml+ / refills · ancillaries.",
         "<b>In the trend</b>: every Central item, launches included once they have 6 months of shipments.",
         "<b>Every month</b>: recalculate the rule with the last 12 closed months and give the next 9 months."],
    why=[("Last year's month as the base", "Fragrance repeats the same calendar every year: retailers load for Christmas from July to September. Last year's month already carries that shape."),
         ("A 12-month trend", "A 3-month window jumps with every supply cut or shifted order. Twelve months cover a full season, so what moves is the real direction."),
         ("Grouped by house × size", "One EAN's trend is noise: a big order or a delisting flips it. Pooling products of the same house and size averages that noise out, and size adds a bit of real difference."),
         ("Launches inside the trend", "New products partly replace old ones. Leaving them out shows only the decline of the old range."),
         ("Only 25% of the cuts", "A cut month understates demand, so some of it goes back. But retailers re-order weekly while an item is cut, so most of the figure is duplicated."),
         ("Remove 50% of the positive DAs", "Last year's promotions should not repeat by default. Only half, because part of the DAs are market inputs that do come back."),
         ("Recalculate every month", "Each month the 12-month window moves forward one month, so the trend and the base already include the latest reality. No manual corrections needed.")],
    foot="Local items (under 6 months of shipments) are outside the rule: no history yet. Items with 6–17 months of life: review with care, their last year includes the launch pipeline fill.",
)

MU = dict(
    key="mu", acc=CLAY, title="Makeup", kicker="Forecast rule",
    tagline="No calendar to copy. Follow the current pace.",
    formula=[("MONTH", "= shipments <span class='op'>+</span> min(<b>10%</b> of cuts ; 10% of shipments) <span class='op'>−</span> <b>25%</b> of positive DAs"),
             ("BASE", "= average of the last <b>6</b> adjusted months"),
             ("FORECAST", "= BASE <span class='op'>×</span> (1 + <b>½</b> × 12-month trend of Face · Lips · Eyes) <span class='same'>same every month</span>")],
    eg="1,000 shipped &nbsp;+100 cuts (capped) &nbsp;−50 DAs &nbsp;→ 1,050 a month &nbsp;× 0.90 (½ of −20%) &nbsp;= <b>945</b> every month",
    how=["<b>Category</b> = Face, Lips or Eyes within each brand family.",
         "<b>Trend</b> = last 12 closed months ÷ the 12 before − 1, actual shipments only. Apply half of it, capped at ±30%.",
         "<b>In the average</b>: every Central item (6+ months of shipments).",
         "<b>Every month</b>: recalculate the 6-month average and the trend and give the next 9 months."],
    why=[("No seasonality", "Shoppers do buy more in December, but our shipments follow launches, pipeline fills and order timing, not the calendar. Copying last year's month copies noise."),
         ("Average of the last 6 months", "It reflects the current selling pace and smooths one-off spikes, without chasing a single big order."),
         ("Same number for every month", "With no stable monthly shape, a flat run-rate is the honest call. Peaks and dips get corrected as months arrive."),
         ("Only half of the trend", "The 6-month average already holds part of the recent trend. The full trend on top would count it twice."),
         ("Only 10% of the cuts", "When an item is cut, retailers keep re-ordering the same quantity week after week. In makeup that re-ordering is far heavier, so the cuts are heavily inflated."),
         ("Only 25% of the DAs", "A six-month average already dilutes a single promotion. Removing more would cut growing lines too hard."),
         ("Recalculate, don't correct", "A rolling average refreshes itself with the latest months every cycle. An extra correction factor would add noise.")],
    foot="Local items (under 6 months of shipments) are outside the rule: no history yet.",
)


def legend(items):
    return "<div class='lg'>" + "".join(f"<span><i style='background:{c}'></i>{t}</span>" for t, c in items) + "</div>"


def card(title, sub, svg, cls="", leg=None):
    head = f"<div class='ct'>{title}</div><div class='cs'>{sub}</div>{legend(leg) if leg else ''}"
    return f"<div class='card {cls}'>{head}{svg}</div>"


def charts_for(p):
    if p["key"] == "frag":
        return ("<div class='charts c2'>"
                + card("The year repeats itself", "Monthly shipments ÷ the year's average", chart_frag_season(),
                       leg=[("FY24", PLUM["light"]), ("FY25", PLUM["mid"]), ("FY26", PLUM["dark"])])
                + card("12 months see the direction", "Year-on-year change, rolling window", chart_trend_windows(),
                       leg=[("3-month window", PLUM["light"]), ("12-month window", PLUM["dark"])])
                + "</div>")
    return ("<div class='charts c3'>"
            + card("Shoppers are seasonal…", "Sell-out (EPOS) ÷ year's average", chart_mu_season("epos"),
                   leg=[("FY25", CLAY["mid"]), ("FY26", CLAY["dark"])])
            + card("…our shipments are not", "Shipments ÷ year's average", chart_mu_season("ship"),
                   leg=[("FY24", CLAY["light"]), ("FY25", CLAY["mid"]), ("FY26", CLAY["dark"])])
            + "</div>"
            + card("Cuts are inflated by re-ordering", "Supply cuts as a share of shipments, FY26", chart_cuts(), "cuts"))


def page_html(p, num):
    acc = p["acc"]
    formula = "".join(f"<div class='fl'><span class='fk'>{k}</span><span class='fv'>{v}</span></div>" for k, v in p["formula"])
    how = "".join(f"<li>{h}</li>" for h in p["how"])
    why = "".join(f"<div class='why'><div class='n'>{i + 1:02d}</div><div><div class='wt'>{t}</div><div class='wx'>{x}</div></div></div>"
                  for i, (t, x) in enumerate(p["why"]))
    extra = ""
    return f"""
<section class="page {p['key']}" style="--acc:{acc['mid']};--accd:{acc['dark']};--accl:{acc['light']};--accbg:{acc['bg']}">
  <div class="blob"></div><div class="blob2"></div>
  <header>
    <div class="kick"><span class="pill">{num:02d}</span>{p['kicker']}</div>
    <h1>{p['title']}<span class="dot">.</span></h1>
    <div class="tag">{p['tagline']}</div>
  </header>
  <div class="grid">
    <div class="left">
      <div class="formula">{formula}<div class="eg"><span>e.g.</span> {p['eg']}</div></div>
      <ul class="how">{how}</ul>
      {charts_for(p)}
    </div>
    <div class="right">
      <div class="wh">Why each piece is there</div>
      {why}
      {extra}
    </div>
  </div>
  <footer>{p['foot']}</footer>
</section>"""


CSS = f"""
@font-face {{ font-family: Inter; src: url('file://{FONT}/Inter-Regular.otf'); font-weight: 400; }}
@font-face {{ font-family: Inter; src: url('file://{FONT}/Inter-Medium.otf'); font-weight: 500; }}
@font-face {{ font-family: Inter; src: url('file://{FONT}/Inter-SemiBold.otf'); font-weight: 600; }}
@font-face {{ font-family: Inter; src: url('file://{FONT}/Inter-Bold.otf'); font-weight: 700; }}
@font-face {{ font-family: InterDisplay; src: url('file://{FONT}/InterDisplay-Bold.otf'); font-weight: 700; }}
@page {{ size: 297mm 210mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Inter, sans-serif; color: {INK}; background: #FBF9F6; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 297mm; height: 210mm; padding: 12mm 14mm 10mm; position: relative; overflow: hidden; page-break-after: always; background: #FBF9F6; }}
.blob {{ position: absolute; right: -55mm; top: -75mm; width: 165mm; height: 165mm; border-radius: 50%;
        background: radial-gradient(circle at 40% 40%, var(--accl) 0%, var(--accbg) 50%, rgba(255,255,255,0) 70%); opacity: .7; }}
.blob2 {{ position: absolute; left: -40mm; bottom: -60mm; width: 110mm; height: 110mm; border-radius: 50%;
         background: radial-gradient(circle, var(--accbg) 0%, rgba(255,255,255,0) 68%); }}
header {{ position: relative; margin-bottom: 4mm; }}
.kick {{ display: flex; align-items: center; gap: 2.4mm; font-size: 8.5pt; font-weight: 600; letter-spacing: .16em; text-transform: uppercase; color: var(--accd); }}
.pill {{ font-family: InterDisplay, Inter; letter-spacing: 0; font-size: 8pt; color: #fff; background: var(--accd); border-radius: 20px; padding: .5mm 2.2mm; }}
h1 {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 36pt; letter-spacing: -.025em; line-height: 1; margin-top: 1.6mm; }}
h1 .dot {{ color: var(--acc); }}
.tag {{ font-size: 12pt; color: {INK2}; margin-top: 1.4mm; }}
.grid {{ position: relative; display: grid; grid-template-columns: 1.1fr .9fr; gap: 8mm; }}
.formula {{ background: {INK}; color: #fff; border-radius: 16px; padding: 5mm 6mm 4.2mm; box-shadow: 0 10px 28px rgba(28,26,36,.16); position: relative; overflow: hidden; }}
.formula:after {{ content: ''; position: absolute; right: -14mm; top: -14mm; width: 40mm; height: 40mm; border-radius: 50%; background: var(--acc); opacity: .22; }}
.fl {{ position: relative; display: flex; gap: 3mm; align-items: baseline; margin-bottom: 2.2mm; font-size: 11pt; line-height: 1.38; z-index: 1; }}
.fk {{ flex: 0 0 23mm; font-family: InterDisplay, Inter; font-weight: 700; font-size: 10pt; letter-spacing: .08em; color: var(--accl); }}
.fv {{ color: #D9D6E0; }}
.fv b {{ color: #fff; font-weight: 700; }}
.op {{ color: var(--accl); font-weight: 700; padding: 0 .5mm; }}
.same {{ display: inline-block; font-size: 7pt; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: {INK};
         background: var(--accl); border-radius: 20px; padding: .3mm 2mm; margin-left: 1mm; vertical-align: 1px; }}
.eg {{ position: relative; z-index: 1; border-top: 1px solid rgba(255,255,255,.14); margin-top: 3mm; padding-top: 2.6mm; font-size: 8.5pt; color: #B9B5C4; }}
.eg span {{ font-weight: 700; color: var(--accl); margin-right: 1mm; }}
.eg b {{ color: #fff; }}
.how {{ list-style: none; margin: 4.5mm 0 4mm; display: grid; grid-template-columns: 1fr 1fr; gap: 2.4mm 6mm; }}
.how li {{ font-size: 8.3pt; line-height: 1.42; color: {INK2}; padding-left: 4mm; position: relative; }}
.how li:before {{ content: ''; position: absolute; left: 0; top: 1.5mm; width: 1.8mm; height: 1.8mm; border-radius: 50%; background: var(--acc); }}
.how b {{ color: {INK}; }}
.charts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; }}
.card {{ background: rgba(255,255,255,.92); border-radius: 14px; border: 1px solid #EEEAF2; padding: 3.4mm 4mm 2.4mm; }}
.ct {{ font-weight: 700; font-size: 9.6pt; }}
.cs {{ font-size: 7.4pt; color: {MUTED}; margin: .4mm 0 1.4mm; }}
.cuts {{ margin-top: 2.6mm; }}
.ch {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 2mm; }}
.lg {{ display: flex; gap: 3mm; font-size: 6.8pt; font-weight: 600; color: {INK2}; margin: -.4mm 0 .8mm; white-space: nowrap; }}
.lg i {{ display: inline-block; width: 2.2mm; height: 2.2mm; border-radius: 50%; margin-right: .8mm; vertical-align: -0.2mm; }}
.mu .how {{ margin: 3.2mm 0 3mm; gap: 1.6mm 6mm; }}
.mu .formula {{ padding: 4.2mm 6mm 3.6mm; }}
.mu .card {{ padding: 2.8mm 4mm 2mm; }}
svg {{ display: block; }}
svg .ax {{ font-family: Inter; font-size: 7.5px; fill: {MUTED}; }}
svg .lab {{ font-family: Inter; font-size: 8px; font-weight: 600; fill: {INK2}; }}
svg .note {{ font-family: Inter; font-size: 7px; font-weight: 700; fill: {INK2}; letter-spacing: .06em; text-transform: uppercase; }}
svg .blab {{ font-family: Inter; font-size: 9px; font-weight: 600; fill: {INK}; }}
svg .bval {{ font-family: Inter; font-size: 9px; font-weight: 700; fill: {INK}; }}
svg .bsub {{ font-family: Inter; font-size: 8.5px; font-weight: 600; fill: {MUTED}; }}
.right {{ display: flex; flex-direction: column; gap: 2.3mm; }}
.wh {{ font-size: 8.5pt; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: var(--accd); margin: .4mm 0 .4mm; }}
.why {{ display: grid; grid-template-columns: 9.5mm 1fr; gap: 1.6mm; background: rgba(255,255,255,.92); border: 1px solid #EEEAF2; border-radius: 12px; padding: 2.3mm 3.4mm 2.3mm 3mm; }}
.why .n {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 14pt; color: var(--acc); line-height: 1.05; }}
.wt {{ font-weight: 700; font-size: 9.2pt; margin-bottom: .4mm; }}
.wx {{ font-size: 7.9pt; line-height: 1.4; color: {INK2}; }}
footer {{ position: absolute; left: 14mm; right: 14mm; bottom: 6.5mm; font-size: 7.4pt; color: {MUTED}; border-top: 1px solid #E7E3EC; padding-top: 2mm; }}
"""


def main():
    html = (f"<!doctype html><html><head><meta charset='utf-8'><title>Forecast rules</title><style>{CSS}</style></head>"
            f"<body>{page_html(FRAG, 1)}{page_html(MU, 2)}</body></html>")
    HTML.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--allow-file-access-from-files", f"--print-to-pdf={OUT}", f"file://{HTML}"], check=True, capture_output=True)
    print(OUT)


if __name__ == "__main__":
    main()
