"""Infographic PDF (English): one landscape A4 page per rule (Fragrances, Makeup).
Formula + how it works + the reasoning behind each piece. No accuracy results on purpose.
Usage: python3 src/infografia.py  -> INFOGRAFIA_REGLAS.pdf"""
from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas

OUT = Path(__file__).resolve().parents[1] / "INFOGRAFIA_REGLAS.pdf"
W, H = landscape(A4)
INK = colors.HexColor("#1F2430")
MUTED = colors.HexColor("#5B6170")
LINE = colors.HexColor("#D9DCE3")
FRAG = colors.HexColor("#6B3FA0")
FRAG_BG = colors.HexColor("#F3EEFA")
MU = colors.HexColor("#C2410C")
MU_BG = colors.HexColor("#FDF1EA")
M = 32  # page margin


def st(size=9.6, color=INK, bold=False, lead=None):
    return ParagraphStyle("s", fontName="Helvetica-Bold" if bold else "Helvetica", fontSize=size,
                          leading=lead or size * 1.34, textColor=color)


def para(c, text, x, y, w, style):
    p = Paragraph(text, style)
    _, h = p.wrap(w, 2000)
    p.drawOn(c, x, y - h)
    return y - h


def section(c, title, x, y, w, color):
    c.setFillColor(color); c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y - 11, title.upper())
    c.setStrokeColor(color); c.setLineWidth(0.7); c.line(x, y - 15, x + w, y - 15)
    return y - 22


def bullets(c, items, x, y, w, color, size=9.6, gap=4):
    for it in items:
        c.setFillColor(color); c.circle(x + 2.4, y - 6.2, 1.8, fill=1, stroke=0)
        y = para(c, it, x + 10, y, w - 10, st(size)) - gap
    return y


def why_cards(c, items, x, y, w, color, bg):
    """items: (title, text). Each reason in a light card with a coloured left bar."""
    for title, text in items:
        p = Paragraph(f"<b>{title}</b><br/>{text}", st(9.2, lead=12))
        _, h = p.wrap(w - 22, 2000)
        hh = h + 10
        c.setFillColor(bg); c.roundRect(x, y - hh, w, hh, 4, fill=1, stroke=0)
        c.setFillColor(color); c.rect(x, y - hh, 3.2, hh, fill=1, stroke=0)
        p.drawOn(c, x + 12, y - 5 - h)
        y -= hh + 5
    return y


def formula_box(c, lines, x, y, w, color, bg):
    pad = 12
    ps = [Paragraph(t, st(s, color if b else INK, bold=b, lead=s * 1.28)) for t, s, b in lines]
    hs = [p.wrap(w - 2 * pad, 2000)[1] for p in ps]
    h = sum(hs) + 2 * pad + 5 * (len(ps) - 1)
    c.setFillColor(bg); c.setStrokeColor(color); c.setLineWidth(1.2)
    c.roundRect(x, y - h, w, h, 7, fill=1, stroke=1)
    yy = y - pad
    for p, hh in zip(ps, hs):
        p.drawOn(c, x + pad, yy - hh); yy -= hh + 5
    return y - h


def example(c, title, rows, x, y, w, color):
    c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 9); c.drawString(x, y - 10, title.upper())
    y -= 16
    for lab, val, strong in rows:
        c.setFont("Helvetica-Bold" if strong else "Helvetica", 9.4)
        c.setFillColor(color if strong else INK)
        c.drawString(x + 4, y - 10, lab); c.drawRightString(x + w - 4, y - 10, val)
        y -= 15
        c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(x + 4, y + 2, x + w - 4, y + 2)
    return y


def page(c, color, bg, title, tag, subtitle, formula, how, ex_title, ex_rows, whys, footer):
    c.setFillColor(colors.white); c.rect(0, 0, W, H, fill=1, stroke=0)
    # header band
    c.setFillColor(color); c.rect(0, H - 62, W, 62, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 24); c.drawString(M, H - 40, title)
    c.setFont("Helvetica", 10.5); c.drawRightString(W - M, H - 30, tag)
    c.setFont("Helvetica", 9.5); c.drawRightString(W - M, H - 45, subtitle)
    top = H - 80
    gap = 26
    lw = (W - 2 * M - gap) * 0.47
    rw = (W - 2 * M - gap) - lw
    xl, xr = M, M + lw + gap
    # left: formula, how it works, example
    y = formula_box(c, formula, xl, top, lw, color, bg) - 16
    y = section(c, "How it works", xl, y, lw, color)
    y = bullets(c, how, xl, y, lw, color) - 10
    example(c, ex_title, ex_rows, xl, y, lw, color)
    # right: why
    y = section(c, "Why each piece is there", xr, top, rw, color)
    why_cards(c, whys, xr, y, rw, color, bg)
    c.setStrokeColor(LINE); c.setLineWidth(0.8); c.line(M, 30, W - M, 30)
    c.setFillColor(MUTED); c.setFont("Helvetica", 8.2); c.drawString(M, 18, footer)
    c.showPage()


def main():
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle("Forecast rules: Fragrances and Makeup")

    page(
        c, FRAG, FRAG_BG, "Fragrances", "Forecast rule  ·  Burberry · Gucci · Marc Jacobs",
        "Monthly forecast per EAN, 8-month horizon",
        [("BASE = same month last year + 25% of supply cuts - 50% of positive DAs", 11.2, True),
         ("cuts and DAs of that same month last year", 8.8, False),
         ("FORECAST = BASE × (1 + 12-month trend of house × size)", 13, True)],
        ["<b>Trend</b> = sum of the last 12 closed months / sum of the 12 months before - 1, using actual shipments only.",
         "<b>Group</b> = house × size: minis/pen sprays (up to 15 ml), 20-40 ml, 45-60 ml, 75-125 ml, 150 ml+/refills, ancillaries.",
         "<b>Products included</b> in the trend: everything Central, launches included once they have 6+ months of shipments.",
         "<b>Cap</b>: the trend is limited to ±30%. It multiplies: a -10% trend means base × 0.90.",
         "<b>Each S&amp;OP cycle</b>: final number = average of this rule and consensus; then scale the remaining months by actual / forecast of the months just closed."],
        "Example · one EAN, October",
        [("Shipments last October", "1,000", False), ("+ 25% of last October's cuts (200)", "+50", False),
         ("- 50% of last October's positive DAs (100)", "-50", False), ("Base", "1,000", True),
         ("× (1 + trend -10%)", "× 0.90", False), ("Forecast this October", "900", True)],
        [("Why last year's same month?",
          "Fragrance has a strong seasonality that repeats every year: retailers load stock for Christmas from August to December. "
          "Last year's month already carries that shape, so we don't have to model it."),
         ("Why a 12-month trend, not 3 or 6?",
          "Short windows overreact to one bad month: a supply cut or a shipment that moved from one month to the next. "
          "Twelve months cover a full season, so the direction is real and not noise."),
         ("Why house × size, not each EAN?",
          "A single EAN's trend is noisy: one big order or one delisting changes it completely. Grouping similar products gives a stable signal, "
          "and sizes really behave differently (minis do not move like 50 ml)."),
         ("Why include recent launches in the trend?",
          "New products partly replace older ones. Leaving them out would show only the decline of the old range and overstate the drop."),
         ("Why only 25% of the cuts?",
          "A cut month understates true demand, so we add some of it back. But cuts are inflated: retailers repeat the same order every week, "
          "so only a quarter is real lost demand."),
         ("Why remove 50% of the positive DAs?",
          "Last year's promotions and one-off volumes should not repeat automatically. Only half, because part of the DAs are market inputs that do come back."),
         ("Why average with consensus and correct each cycle?",
          "The statistical rule tends to be conservative and consensus tends to be optimistic; the average balances both. "
          "Scaling by actual / forecast lets the forecast react within months instead of waiting a year for the trend to catch up.")],
        "Exceptions: Local items (under 6 months of shipments) keep the consensus. Items with 6-17 months of life: lean more on consensus (their last year includes the launch pipeline fill).",
    )

    page(
        c, MU, MU_BG, "Makeup", "Forecast rule  ·  Gucci Make up · Kylie Makeup",
        "Monthly forecast per EAN, 8-month horizon",
        [("ADJUSTED MONTH = shipments + min(10% of cuts ; 10% of shipments) - 25% of positive DAs", 11.2, True),
         ("BASE = average of the last 6 adjusted months", 11.2, True),
         ("FORECAST = BASE × (1 + 50% of the 12-month trend of the category)", 13, True),
         ("same number for every future month", 8.8, False)],
        ["<b>Category</b> = Face, Lips or Eyes within each brand family.",
         "<b>Trend</b> = sum of the last 12 closed months / sum of the 12 months before - 1, actual shipments only. Apply half of it, capped at ±30%.",
         "<b>Cuts</b>: add the smaller of 10% of the month's cuts or 10% of the month's shipments.",
         "<b>Products included</b>: everything Central (6+ months of shipments).",
         "<b>Each S&amp;OP cycle</b>: recalculate the 6-month average and the trend with the latest months. No correction factor, no blend with consensus."],
        "Example · one month inside the average",
        [("Shipments", "1,000", False), ("+ min(10% of 3,000 cuts ; 10% of 1,000)", "+100", False),
         ("- 25% of positive DAs (200)", "-50", False), ("Adjusted month", "1,050", True),
         ("Base = average of 6 such months", "1,050", False), ("× (1 + 50% of a -20% trend)", "× 0.90", False),
         ("Forecast for every future month", "945", True)],
        [("Why no seasonality?",
          "Consumers do buy more makeup in December, but our shipments don't follow a repeatable monthly pattern: they are driven by launches, "
          "pipeline fills and order timing. Copying last year's month would copy that noise."),
         ("Why the average of the last 6 months?",
          "It shows the current selling pace and smooths out one-off spikes. Six months reacts to real changes without chasing a single big order."),
         ("Why the same number for every month?",
          "Without a stable seasonal shape, a flat run-rate is the honest forecast. Peaks and dips are corrected as the months arrive."),
         ("Why only half of the trend?",
          "The 6-month average already contains part of the recent trend. Applying the full trend on top would count the same movement twice."),
         ("Why a trend by Face / Lips / Eyes?",
          "The categories grow and decline at different speeds. One trend for the whole brand would hide that."),
         ("Why so little of the cuts, and capped?",
          "Makeup cuts are much bigger and more inflated than in fragrance (repeated weekly orders). We acknowledge them, "
          "but cap them so a month with huge cuts cannot blow up the base."),
         ("Why only 25% of the DAs?",
          "The base is already an average of six months, so a single promotion is diluted. Removing more would cut growing lines too hard."),
         ("Why recalculate instead of a correction factor?",
          "A rolling average updates itself with the latest reality every cycle. An extra correction factor would add noise, not accuracy.")],
        "Exceptions: Local items (under 6 months of shipments) keep the consensus. Rule status: proposal, pending final sign-off.",
    )
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
