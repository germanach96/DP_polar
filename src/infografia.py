"""Infografía PDF (1 página, A4 horizontal) con las reglas de forecast de Fragancias y Makeup.
Uso: python3 src/infografia.py  -> INFOGRAFIA_REGLAS.pdf"""
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
FRAG = colors.HexColor("#6B3FA0")      # fragancias
FRAG_BG = colors.HexColor("#F3EEFA")
MU = colors.HexColor("#C2410C")        # makeup
MU_BG = colors.HexColor("#FDF1EA")


def st(size=8.6, color=INK, bold=False, lead=None, align=0):
    return ParagraphStyle("s", fontName="Helvetica-Bold" if bold else "Helvetica", fontSize=size,
                          leading=lead or size * 1.32, textColor=color, alignment=align)


def para(c, text, x, y, w, style):
    """Dibuja un párrafo con la esquina superior izquierda en (x, y). Devuelve la nueva y (debajo)."""
    p = Paragraph(text, style)
    _, h = p.wrap(w, 1000)
    p.drawOn(c, x, y - h)
    return y - h


def section(c, title, x, y, w, color):
    c.setFillColor(color); c.setFont("Helvetica-Bold", 9.4)
    c.drawString(x, y - 10, title.upper())
    c.setStrokeColor(color); c.setLineWidth(0.6); c.line(x, y - 14, x + w, y - 14)
    return y - 20


def bullets(c, items, x, y, w, color, size=9.6):
    for it in items:
        c.setFillColor(color); c.circle(x + 2.2, y - 6, 1.7, fill=1, stroke=0)
        y = para(c, it, x + 9, y, w - 9, st(size)) - 3.4
    return y


def formula_box(c, lines, x, y, w, color, bg):
    pad = 11
    ps = [Paragraph(t, st(s, color if b else INK, bold=b, lead=s * 1.28)) for t, s, b in lines]
    hs = [p.wrap(w - 2 * pad, 1000)[1] for p in ps]
    h = sum(hs) + 2 * pad + 4 * (len(ps) - 1)
    c.setFillColor(bg); c.setStrokeColor(color); c.setLineWidth(1)
    c.roundRect(x, y - h, w, h, 6, fill=1, stroke=1)
    yy = y - pad
    for p, hh in zip(ps, hs):
        p.drawOn(c, x + pad, yy - hh); yy -= hh + 4
    return y - h


def example(c, title, rows, x, y, w, color):
    c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 8.6); c.drawString(x, y - 9, title)
    y -= 14
    for lab, val, strong in rows:
        c.setFont("Helvetica-Bold" if strong else "Helvetica", 8.8)
        c.setFillColor(color if strong else INK)
        c.drawString(x + 4, y - 9.5, lab); c.drawRightString(x + w - 4, y - 9.5, val)
        y -= 13.5
        c.setStrokeColor(LINE); c.setLineWidth(0.4); c.line(x + 4, y + 1.5, x + w - 4, y + 1.5)
    return y


def evidence(c, rows, x, y, w, color):
    """rows: (etiqueta, valor_float 0-1, destacado). Barras horizontales de error (menos = mejor)."""
    lab_w = w * 0.52
    bar_w = w - lab_w - 34
    for lab, v, strong in rows:
        c.setFont("Helvetica-Bold" if strong else "Helvetica", 8.6)
        c.setFillColor(INK); c.drawString(x, y - 9, lab)
        c.setFillColor(color if strong else colors.HexColor("#B9BEC9"))
        c.roundRect(x + lab_w, y - 11, bar_w * min(v, 1.1) / 1.1, 9, 2, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont("Helvetica-Bold" if strong else "Helvetica", 8.6)
        c.drawString(x + lab_w + bar_w * min(v, 1.1) / 1.1 + 3, y - 9.5, f"{v*100:.0f}%".replace(".", ","))
        y -= 15
    return y


def column(c, x, w, top, color, bg, title, tag, formula, steps, extras, ex_title, ex_rows, ev_title, ev_rows, note):
    # cabecera de columna
    c.setFillColor(color); c.roundRect(x, top - 30, w, 30, 6, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 15); c.drawString(x + 12, top - 20, title)
    c.setFont("Helvetica", 8.4); c.drawRightString(x + w - 12, top - 19, tag)
    y = top - 40
    y = formula_box(c, formula, x, y, w, color, bg) - 14
    y = section(c, "Cómo se calcula", x, y, w, color)
    y = bullets(c, steps, x, y, w, color) - 7
    y = section(c, "Cada foto / mes", x, y, w, color)
    y = bullets(c, extras, x, y, w, color) - 9
    half = (w - 12) / 2
    y0 = y
    y1 = example(c, ex_title, ex_rows, x, y0, half, color)
    c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 8.6); c.drawString(x + half + 12, y0 - 9, ev_title)
    y2 = evidence(c, ev_rows, x + half + 12, y0 - 16, half, color)
    y = min(y1, y2) - 8
    para(c, note, x, y, w, st(8.2, MUTED))


def main():
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle("Reglas de forecast: Fragancias y Makeup")
    c.setFillColor(colors.white); c.rect(0, 0, W, H, fill=1, stroke=0)
    m = 28
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 21); c.drawString(m, H - 42, "Reglas de forecast")
    c.setFillColor(MUTED); c.setFont("Helvetica", 9.5)
    c.drawString(m, H - 58, "Validadas con backtest: cada foto S&OP usa solo la información disponible en su momento y se compara contra la foto final (sep-26).")
    c.setStrokeColor(LINE); c.setLineWidth(0.8); c.line(m, H - 68, W - m, H - 68)
    gap = 22
    cw = (W - 2 * m - gap) / 2
    top = H - 80

    column(
        c, m, cw, top, FRAG, FRAG_BG, "Fragancias", "Decidida  ·  BBY · Gucci · Marc Jacobs",
        [("BASE = mismo mes del año anterior + 25% cortes - 50% DAs positivos", 10.6, True),
         ("cortes y DAs del mismo mes del año anterior", 8.4, False),
         ("FORECAST = BASE × (1 + trend 12M de house × tamaño)", 12, True)],
        ["<b>Trend</b> = suma últimos 12 meses cerrados / suma 12 anteriores - 1 (con actuals puros, sin cortes ni DAs).",
         "<b>Grupo</b>: house × tamaño: <=15 ml · 20-40 · 45-60 · 75-125 · >=150/refill · ancilares.",
         "<b>Entran</b> todos los Central, incluidos lanzamientos con 6 meses o más. Fuera solo los Local (menos de 6 meses).",
         "<b>Tope</b> del trend: ±30%. Se multiplica: trend -10% = base × 0,90.",
         "<b>Estacionalidad</b>: la da el propio mes del año anterior."],
        ["Número final = media entre la regla y el consenso.",
         "Factor = real / forecast de los meses cerrados (total). Se multiplica todo el forecast restante por el factor."],
        "Ejemplo: EAN, oct-26",
        [("Venta oct-25", "1.000", False), ("+ 25% cortes oct-25 (200)", "+50", False),
         ("- 50% DAs+ oct-25 (100)", "-50", False), ("Base", "1.000", True),
         ("× (1 + trend -10%)", "× 0,90", False), ("Forecast oct-26", "900", True)],
        "Error EAN-mes (menos = mejor)",
        [("Regla completa", 0.626, True), ("Consenso", 0.717, False),
         ("Año pasado tal cual", 0.720, False), ("Actual: trend 6M EAN", 0.785, False)],
        "Error medio por EAN y mes en las fotos sep-25 a jun-26 (EANs Central sin forecast manual). Desvío del total con la cadena completa: entre -7% y +9%.",
    )
    column(
        c, m + cw + gap, cw, top, MU, MU_BG, "Makeup", "Propuesta  ·  Gucci Make up · Kylie Makeup",
        [("MES AJUSTADO = envío + mín(10% cortes ; 10% envío) - 25% DAs positivos", 10.6, True),
         ("BASE = media de los últimos 6 meses ajustados", 10.6, True),
         ("FORECAST = BASE × (1 + 50% trend 12M de la función)", 12, True),
         ("mismo número para todos los meses futuros", 8.4, False)],
        ["<b>Cortes con tope</b>: se suma el menor entre el 10% de los cortes y el 10% del envío del mes (en makeup se corta mucho más que en fragancias).",
         "<b>Trend</b> = suma últimos 12 meses / 12 anteriores - 1, por <b>función</b>: Face · Lips · Eyes. Se aplica el 50% y con tope ±30%.",
         "<b>Sin estacionalidad</b>: los envíos no repiten patrón (correlación entre años 0,06 KYMU, 0,39 GUMU), aunque el sell-out sí (pico en diciembre).",
         "<b>Entran</b> todos los Central (6 meses o más de envíos)."],
        ["Recalcular la media de 6 meses y el trend con los últimos datos. Sin factor de corrección y sin media con el consenso."],
        "Ejemplo: un mes de la media",
        [("Envío", "1.000", False), ("+ mín(10% de 3.000; 10% de 1.000)", "+100", False),
         ("- 25% DAs+ (200)", "-50", False), ("Mes ajustado", "1.050", True),
         ("Base (media 6M, meses iguales)", "1.050", False), ("× (1 + 50% de -20%)", "× 0,90", False),
         ("Forecast de cada mes", "945", True)],
        "Error EAN-mes (menos = mejor)",
        [("Regla: Kylie (KYMU)", 0.57, True), ("Regla: Gucci (GUMU)", 0.66, True),
         ("Consenso", 0.81, False), ("Año pasado tal cual", 0.92, False)],
        "Error medio por EAN y mes, 13 cortes mensuales (jul-25 a jul-26), sin forecast manual. Consenso: foto sep-25.",
    )
    c.setStrokeColor(LINE); c.line(m, 30, W - m, 30)
    c.setFillColor(MUTED); c.setFont("Helvetica", 7.4)
    c.drawString(m, 18, "Excepciones: los Local (menos de 6 meses de envíos) se quedan con el consenso; EANs de 6 a 17 meses: apoyarse más en el consenso.")
    c.drawRightString(W - m, 18, "Detalle: ESTRATEGIA_FRAGANCIAS.md · ESTRATEGIA_MAKEUP.md")
    c.showPage(); c.save()
    print(OUT)


if __name__ == "__main__":
    main()
