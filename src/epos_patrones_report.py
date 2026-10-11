"""Reporte PDF: patrones envío ↔ EPOS. Lee work/epos_patrones.json (correr antes src/epos_patrones.py).
Salida: reportes/REPORTE_EPOS_PATRONES.pdf"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reportes" / "REPORTE_EPOS_PATRONES.pdf"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
INK, INK2, MUTED, GRID = "#16202E", "#46505E", "#8792A0", "#E3E7EC"
FRAG, MU, SHIP = "#6250d6", "#eb6834", "#5B6573"     # morado = fragancias, naranja = makeup, gris = envío
FRAG_L, MU_L = "#C9C2F2", "#F7C3AD"
HOUSES = ["BURBERRY", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"]
NAME = {"BURBERRY": "Burberry"}
CATC = {"BURBERRY": FRAG, "Gucci": FRAG, "Marc Jacobs": FRAG, "Gucci Make up": MU, "Kylie Makeup": MU}
nm = lambda h: NAME.get(h, h)
pc = lambda x, s=True: (f"{x:+.0%}" if s else f"{x:.0%}").replace("-", "−")


def lerp(v, a, b, A, B):
    return A + (v - a) / (b - a) * (B - A)


def axis_y(x0, x1, y0, y1, lo, hi, ticks, fmt, zero=True):
    s = []
    for t in ticks:
        y = lerp(t, lo, hi, y1, y0)
        strong = zero and abs(t) < 1e-9
        s.append(f'<line x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{"#AEB6C1" if strong else GRID}" stroke-width="{1 if strong else .7}"/>')
        s.append(f'<text x="{x0 - 5}" y="{y + 3:.1f}" text-anchor="end" class="ax">{fmt(t)}</text>')
    return "".join(s)


def line(xs, ys, color, w=2, dash=None):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys) if y is not None)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{d}/>'


# ---------- página 2: ruido ----------
def noise_panel(h, d, months, W=250, H=150):
    x0, x1, y0, y1 = 34, W - 8, 14, H - 22
    lo, hi = -0.8, 0.8
    n = len(months)
    X = [lerp(i, 0, n - 1, x0, x1) for i in range(n)]
    cl = lambda v: max(lo, min(hi, v))
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%">', axis_y(x0, x1, y0, y1, lo, hi, [-.8, -.4, 0, .4, .8], lambda t: pc(t) if t else "0%")]
    for i, m in enumerate(months):
        if i % 3 == 0:
            anc = "end" if i == n - 1 else "middle"
            s.append(f'<text x="{X[i] + (4 if i == n - 1 else 0):.1f}" y="{H - 8}" text-anchor="{anc}" class="ax">{m}</text>')
    ys = [lerp(cl(v), lo, hi, y1, y0) for v in d["ship"]]
    ye = [lerp(cl(v), lo, hi, y1, y0) for v in d["epos"]]
    s.append(line(X, ys, SHIP, 1.6, "4 3"))
    s.append(line(X, ye, CATC[h], 2.2))
    for x, y in zip(X, ye):
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="{CATC[h]}" stroke="#fff" stroke-width="1"/>')
    s.append("</svg>")
    return "".join(s)


def page_noise(D):
    n = D["noise"]
    cards = []
    for h in HOUSES:
        r = n["rango"][h]
        cards.append(f'''<div class="card"><div class="ch"><div><div class="ct">{nm(h)}</div><div class="cs">{n["houses"][h]["n"]} EANs maduros · YoY de cada mes</div></div>
<div class="cv"><span style="color:{SHIP}">rango envío</span>{pc(r["ship"], False)}<span style="color:{CATC[h]}">rango EPOS</span>{pc(r["epos"], False)}</div></div>
{noise_panel(h, n["houses"][h], n["months"])}</div>''')
    side = f'''<div class="card kpi2"><div class="kl">EANs cuyo envío es más inestable que su EPOS</div><div class="kv">{pc(n["pct_env_mas_ruidoso"], False)}</div>
<div class="kl">Mediana: el YoY mensual del envío se mueve <b>{n["ratio_ruido"]:.1f} veces</b> más que el del EPOS (desviación típica del crecimiento de cada mes).</div>
<div class="kl" style="margin-top:2mm;color:{MUTED}">Rango = diferencia entre el mejor y el peor mes de la casa (jul-25 → jul-26).</div></div>'''
    return f'''<section class="page"><div class="kick">1 · Ruido</div>
<h2>El consumidor compra a ritmo constante; los pedidos van a saltos. El YoY mensual del envío oscila unas 4 veces más que el del EPOS</h2>
<div class="leg"><span><i class="ln" style="border-color:{SHIP};border-top-style:dashed"></i>Envío (sell-in) vs mismo mes del año anterior</span>
<span><i style="background:{FRAG}"></i>EPOS fragancias</span><span><i style="background:{MU}"></i>EPOS makeup</span>
<span class="lm">EANs lanzados antes de ene-24 con envío y EPOS en FY25 y FY26 · jul-25 → jul-26</span></div>
<div class="grid c3">{"".join(cards)}{side}</div>
<div class="note" style="margin-top:3mm">Ejemplo: en Burberry el EPOS de cada mes está entre −11% y −35% frente al año anterior; el envío salta de −50% a +33%. <b>Un mes de envíos no dice nada de la demanda</b>: un trimestre de EPOS sí.
Por eso el trend del envío a 3–6 meses falla y la forma mensual del envío cambia de un año a otro.</div></section>'''


# ---------- página 3: tendencia ----------
def scatter(pts, W=430, H=370):
    x0, x1, y0, y1 = 44, W - 10, 10, H - 30
    lo, hi = -0.8, 1.5
    X = lambda v: lerp(v, lo, hi, x0, x1)
    Y = lambda v: lerp(v, lo, hi, y1, y0)
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%">']
    s.append(f'<rect x="{X(0):.1f}" y="{y0}" width="{x1 - X(0):.1f}" height="{Y(0) - y0:.1f}" fill="#F4F6F3"/>')
    s.append(f'<rect x="{x0}" y="{Y(0):.1f}" width="{X(0) - x0:.1f}" height="{y1 - Y(0):.1f}" fill="#F4F6F3"/>')
    ticks = [-.5, 0, .5, 1, 1.5]
    s.append(axis_y(x0, x1, y0, y1, lo, hi, ticks, lambda t: pc(t) if t else "0%"))
    for t in ticks:
        s.append(f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{y0}" y2="{y1}" stroke="{"#AEB6C1" if t == 0 else GRID}" stroke-width="{1 if t == 0 else .7}"/>')
        s.append(f'<text x="{X(t):.1f}" y="{y1 + 12}" text-anchor="middle" class="ax">{pc(t) if t else "0%"}</text>')
    s.append(f'<line x1="{X(lo):.1f}" y1="{Y(lo):.1f}" x2="{X(hi):.1f}" y2="{Y(hi):.1f}" stroke="{MUTED}" stroke-dasharray="3 3"/>')
    s.append(f'<text x="{X(1.05):.1f}" y="{Y(1.15):.1f}" class="ax" transform="rotate(-37 {X(1.05):.1f} {Y(1.15):.1f})">envío = EPOS</text>')
    for p in sorted(pts, key=lambda p: -p["w"]):
        r = max(2.2, min(7, (p["w"] ** .5) / 12))
        c = FRAG if p["cat"] == "Fragancias" else MU
        s.append(f'<circle cx="{X(p["x"]):.1f}" cy="{Y(p["y"]):.1f}" r="{r:.1f}" fill="{c}" fill-opacity=".55" stroke="#fff" stroke-width=".8"/>')
    s.append(f'<text x="{(x0 + x1) / 2}" y="{H - 2}" text-anchor="middle" class="axl">EPOS FY26 vs FY25 →</text>')
    s.append(f'<text x="10" y="{(y0 + y1) / 2}" text-anchor="middle" class="axl" transform="rotate(-90 10 {(y0 + y1) / 2})">Envío FY26 vs FY25 →</text>')
    s.append("</svg>")
    return "".join(s)


def pair_bars(rows, W=360, H=108):
    """rows: [(etiqueta, epos, envío)] en %, barras horizontales emparejadas."""
    x0, x1 = 92, W - 40
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%">']
    for t in [0, .25, .5, .75, 1]:
        x = lerp(t, 0, 1, x0, x1)
        s.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="4" y2="{H - 16}" stroke="{GRID}" stroke-width=".7"/><text x="{x:.1f}" y="{H - 4}" text-anchor="middle" class="ax">{t:.0%}</text>')
    y = 10
    for lab, e, sh, c in rows:
        s.append(f'<text x="{x0 - 8}" y="{y + 14}" text-anchor="end" class="lb">{lab}</text>')
        s.append(f'<rect x="{x0}" y="{y}" width="{lerp(e, 0, 1, 0, x1 - x0):.1f}" height="11" rx="3" fill="{c}"/>')
        s.append(f'<text x="{x0 + lerp(e, 0, 1, 0, x1 - x0) + 4:.1f}" y="{y + 9}" class="vl2">{e:.0%}</text>')
        s.append(f'<rect x="{x0}" y="{y + 13}" width="{lerp(sh, 0, 1, 0, x1 - x0):.1f}" height="11" rx="3" fill="{SHIP}"/>')
        s.append(f'<text x="{x0 + lerp(sh, 0, 1, 0, x1 - x0) + 4:.1f}" y="{y + 22}" class="vl2">{sh:.0%}</text>')
        y += 40
    s.append("</svg>")
    return "".join(s)


def page_trend(D):
    t = D["trend"]
    p = t["persist"]
    rows = [("Fragancias", p["Fragancias"]["keep_epos"], p["Fragancias"]["keep_ship"], FRAG),
            ("Makeup", p["Makeup"]["keep_epos"], p["Makeup"]["keep_ship"], MU)]
    hb = "".join(f'<tr><td>{nm(h)}</td><td>{t["by_house"][h]["n"]}</td><td>{t["by_house"][h]["same"]:.0%}</td><td>{t["by_house"][h]["corr"]:.2f}</td></tr>' for h in HOUSES)
    return f'''<section class="page"><div class="kick">2 · Tendencia</div>
<h2>A 12 meses, envío y EPOS van en la misma dirección en 8 de cada 10 EANs. Y la tendencia del EPOS se mantiene de un semestre a otro; la del envío, no</h2>
<div class="two">
<div class="card"><div class="ct">Cada punto es un EAN: crecimiento FY26 del EPOS frente al del envío</div>
<div class="cs">{t["n"]} EANs maduros · tamaño = volumen · zonas sombreadas = misma dirección</div>
<div class="leg" style="margin:1.5mm 0 0"><span><i style="background:{FRAG}"></i>Fragancias</span><span><i style="background:{MU}"></i>Makeup</span></div>
{scatter(t["points"])}</div>
<div class="side">
<div class="card kpi2"><div class="kl">EANs donde envío y EPOS van en la misma dirección (FY26)</div><div class="kv">{t["same"]:.0%}</div>
<div class="kl">Correlación {t["corr"]:.2f}. Como el EPOS no cubre a todos los clientes, se compara cada EAN consigo mismo (FY26 vs FY25), nunca en unidades.</div>
<table class="tb"><tr><th>Casa</th><th>EANs</th><th>Misma dirección</th><th>Correlación</th></tr>{hb}</table></div>
<div class="card"><div class="ct" style="font-size:10.5pt">¿La tendencia de jul–dic sigue en ene–jun?</div>
<div class="cs">% de EANs que mantienen el signo de su crecimiento · <b style="color:{INK2}">color = EPOS</b> · <b style="color:{SHIP}">gris = envío</b></div>
{pair_bars(rows)}
<div class="kl">Total: {p["Total"]["keep_epos"]:.0%} frente a {p["Total"]["keep_ship"]:.0%}. Correlación de un semestre al siguiente: EPOS {p["Total"]["corr_epos"]:.2f} vs envío {p["Total"]["corr_ship"]:.2f}. En makeup el EPOS de jul–dic anticipa el envío de ene–jun mejor que el propio envío ({p["Makeup"]["epos_to_ship"]:.2f} vs {p["Makeup"]["corr_ship"]:.2f}).</div></div>
</div></div></section>'''


# ---------- página 4: lanzamientos ----------
def launch_chart(x, color, W=420, H=200):
    x0, x1, y0, y1 = 36, W - 8, 12, H - 24
    n = len(x["ship"])
    hi = 0.7 if max(x["ship"]) <= .7 else 0.6
    hi = 0.65
    bw = (x1 - x0) / n
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%">', axis_y(x0, x1, y0, y1, 0, hi, [0, .2, .4, .6], lambda t: f"{t:.0%}")]
    for i in range(n):
        cx = x0 + bw * i
        for k, (v, c) in enumerate([(x["ship"][i], SHIP), (x["epos"][i], color)]):
            vv = min(v, hi)
            h = lerp(vv, 0, hi, 0, y1 - y0)
            s.append(f'<rect x="{cx + bw * .14 + k * bw * .37:.1f}" y="{y1 - h:.1f}" width="{bw * .34:.1f}" height="{h:.1f}" rx="2" fill="{c}"/>')
        s.append(f'<text x="{cx + bw / 2:.1f}" y="{H - 10}" text-anchor="middle" class="ax">{i}</text>')
    s.append(f'<text x="{(x0 + x1) / 2}" y="{H}" text-anchor="middle" class="axl">meses desde el lanzamiento</text>')
    for i in range(2):
        v = x["ship"][i]
        if v > .3:
            s.append(f'<text x="{x0 + bw * i + bw * .31:.1f}" y="{lerp(min(v, hi), 0, hi, y1, y0) - 4:.1f}" text-anchor="middle" class="vl2">{v:.0%}</text>')
    s.append("</svg>")
    return "".join(s)


def ratio_bars(x, color, W=330, H=118):
    rows = [("Año 1 (meses 0–11)", x["y1"], color), ("Año 2 (meses 12–19)", x["y2"], color), ("Veteranos", x["vet_ratio"], SHIP)]
    x0, x1, hi = 112, W - 36, 2.6
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%">']
    xv = lerp(x["vet_ratio"], 0, hi, x0, x1)
    y = 6
    for lab, v, c in rows:
        s.append(f'<text x="{x0 - 8}" y="{y + 12}" text-anchor="end" class="lb">{lab}</text>')
        s.append(f'<rect x="{x0}" y="{y}" width="{lerp(v, 0, hi, 0, x1 - x0):.1f}" height="16" rx="3" fill="{c}" fill-opacity="{1 if lab != "Año 2 (meses 12–19)" else .55}"/>')
        s.append(f'<text x="{x0 + lerp(v, 0, hi, 0, x1 - x0) + 4:.1f}" y="{y + 12}" class="vl">{v:.2f}×</text>')
        y += 30
    s.append(f'<line x1="{xv:.1f}" x2="{xv:.1f}" y1="2" y2="{y - 8}" stroke="{INK2}" stroke-dasharray="2 2"/>')
    s.append("</svg>")
    return "".join(s)


def page_launch(D):
    la = D["launch"]
    cards = []
    for c, col in [("Fragancias", FRAG), ("Makeup", MU)]:
        x = la[c]
        cards.append(f'''<div class="card"><div class="ch"><div><div class="ct" style="color:{col}">{c}</div>
<div class="cs">{x["n"]} lanzamientos jul-24 → jul-25 · cada mes en % de lo que el consumidor compra en sus 13 primeros meses</div></div></div>
{launch_chart(x, col)}
<div class="sub2">Envío ÷ EPOS (la referencia es la de los veteranos: incluye los clientes que no reportan)</div>
{ratio_bars(x, col)}
<div class="kl">En el año 2 el EPOS {"se mantiene" if abs(x["epos_y2_vs_y1"]) < .05 else "cae " + pc(x["epos_y2_vs_y1"])} frente a los meses 4–11, pero el envío baja a {x["y2"]:.2f}× del EPOS (por debajo de los veteranos): <b>señal de que el cliente vende el stock del lanzamiento</b>. ({x["n_y2"]} lanzados jul–dic-24)</div></div>''')
    return f'''<section class="page"><div class="kick">3 · Lanzamientos</div>
<h2>Es tu patrón, y es el más claro: el primer año se envía el doble de lo que se vende; el segundo, menos de lo normal mientras el cliente vende ese stock</h2>
<div class="leg"><span><i style="background:{SHIP}"></i>Envío</span><span><i style="background:{FRAG}"></i>EPOS fragancias</span><span><i style="background:{MU}"></i>EPOS makeup</span>
<span class="lm">Lanzamiento = primer mes de 2 seguidos con envío</span></div>
<div class="grid c2">{"".join(cards)}</div>
<div class="note" style="margin-top:3mm">En fragancias el mes del lanzamiento se envía el {pc(la["Fragancias"]["m0_ship"], False)} de lo que el consumidor comprará en 13 meses.
<b>Consecuencia para la regla:</b> para un EAN de 12–23 meses, el "mismo mes del año pasado" es llenado de canal, y la base sale inflada. Es donde más falla la regla de fragancias (EANs de 6–17 meses). Para esos EANs, la base debería ser el EPOS × la relación de los veteranos (o algo menos), no el envío del año anterior.
Pregunta para ti: ¿los envíos de lanzamiento incluyen probadores o material de exposición? Si es así, parte del "doble" no es stock vendible.</div></section>'''


# ---------- página 5: veteranos ----------
def vet_bars(v, W=470, H=290):
    x0, x1, y0, y1 = 40, W - 10, 14, H - 34
    lo, hi = -0.3, 0.2
    n = len(HOUSES)
    bw = (x1 - x0) / n
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%">', axis_y(x0, x1, y0, y1, lo, hi, [-.3, -.2, -.1, 0, .1, .2], lambda t: pc(t) if t else "0%")]
    yz = lerp(0, lo, hi, y1, y0)
    for i, h in enumerate(HOUSES):
        x = v["houses"][h]
        cx = x0 + bw * i
        for k, (val, c, op) in enumerate([(x["epos_yoy"], CATC[h], 1), (x["casa_epos_yoy"], SHIP, .45)]):
            y = lerp(val, lo, hi, y1, y0)
            top, hgt = min(y, yz), abs(y - yz)
            bx = cx + bw * .18 + k * bw * .33
            s.append(f'<rect x="{bx:.1f}" y="{top:.1f}" width="{bw * .3:.1f}" height="{max(hgt, 1):.1f}" rx="3" fill="{c}" fill-opacity="{op}"/>')
            s.append(f'<text x="{bx + bw * .15:.1f}" y="{(y - 4) if val >= 0 else (y + 11):.1f}" text-anchor="middle" class="vl2">{pc(val)}</text>')
        s.append(f'<text x="{cx + bw / 2:.1f}" y="{H - 18}" text-anchor="middle" class="lb">{nm(h)}</text>')
        s.append(f'<text x="{cx + bw / 2:.1f}" y="{H - 6}" text-anchor="middle" class="ax">{x["pct_caen"]:.0%} de EANs caen</text>')
    s.append("</svg>")
    return "".join(s)


def cohort_bars(co, base, W=440, H=104):
    keys = ["Antes de FY24", "Lanzados FY24", "Lanzados FY25", "Lanzados FY26"]
    shades = {FRAG: ["#3E2FA3", "#6250d6", "#9A8CE6", "#CFC8F5"], MU: ["#B4441B", "#eb6834", "#F29B77", "#F9CFBE"]}[base]
    x0, x1 = 40, W - 6
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%">']
    for j, fy in enumerate(["FY24", "FY25", "FY26"]):
        y = 6 + j * 32
        s.append(f'<text x="{x0 - 6}" y="{y + 15}" text-anchor="end" class="lb">{fy}</text>')
        acc = x0
        for k, key in enumerate(keys):
            v = co.get(key, [0, 0, 0])[j]
            w = (x1 - x0) * v
            if w > 0.5:
                s.append(f'<rect x="{acc + 1:.1f}" y="{y}" width="{max(w - 2, 0):.1f}" height="22" rx="3" fill="{shades[k]}"/>')
                if v >= .07:
                    s.append(f'<text x="{acc + w / 2:.1f}" y="{y + 15}" text-anchor="middle" class="in" fill="{"#fff" if k < 2 else INK}">{v:.0%}</text>')
            acc += w
    s.append("</svg>")
    leg = "".join(f'<span><i style="background:{shades[k]}"></i>{key}</span>' for k, key in enumerate(keys))
    return "".join(s), leg


def page_vet(D):
    v = D["veterans"]
    cf, lf = cohort_bars(v["cohorts"]["Fragancias"], FRAG)
    cm, lm = cohort_bars(v["cohorts"]["Makeup"], MU)
    return f'''<section class="page"><div class="kick">4 · Ciclo de vida</div>
<h2>Los códigos veteranos pierden un 12–23% de venta al consumidor cada año (Marc Jacobs no). La casa crece por los lanzamientos: en dos años pasan a ser un tercio del envío en fragancias y dos tercios en makeup</h2>
<div class="two">
<div class="card"><div class="ct">EPOS FY26 vs FY25: veteranos activos frente al total de la casa</div>
<div class="cs">Veteranos = con envío desde jul-23 y todavía activos (sin bajas)</div>
<div class="leg" style="margin:1.5mm 0 0"><span><i style="background:{FRAG}"></i><i style="background:{MU};margin-left:-1mm"></i>Veteranos</span><span><i style="background:{SHIP};opacity:.45"></i>Total de la casa (con lanzamientos)</span></div>
{vet_bars(v)}</div>
<div class="side">
<div class="card"><div class="ct" style="font-size:10.5pt;color:{FRAG}">Fragancias: peso de cada generación en el envío</div>{cf}<div class="leg sm">{lf}</div></div>
<div class="card"><div class="ct" style="font-size:10.5pt;color:{MU}">Makeup: peso de cada generación en el envío</div>{cm}<div class="leg sm">{lm}</div></div>
</div></div>
<div class="note" style="margin-top:3mm"><b>Consecuencia para el trend:</b> el trend de la casa mezcla dos poblaciones. A un EAN veterano de Gucci no le aplica el −14% de la casa sino un −23%; a uno de Kylie, un −12% y no el +17%.
El trend de un EAN debería salir de su generación (los de su edad en su casa) y medirse en EPOS, que es lo que repite de un año a otro. Esto refuerza la pregunta 2 del EAN ("¿a quién sigo?") con la edad como primera respuesta.</div></section>'''


# ---------- página 6: carga y bajas ----------
def dumbbell(by, W=470, H=230):
    x0, x1, lo, hi = 120, W - 70, -0.3, 0.25
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%">']
    for t in [-.2, -.1, 0, .1, .2]:
        x = lerp(t, lo, hi, x0, x1)
        s.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="8" y2="{H - 22}" stroke="{"#AEB6C1" if t == 0 else GRID}" stroke-width="{1 if t == 0 else .7}"/>'
                 f'<text x="{x:.1f}" y="{H - 8}" text-anchor="middle" class="ax">{pc(t) if t else "0%"}</text>')
    y = 22
    for h in ["BURBERRY", "Gucci Make up", "Marc Jacobs", "Gucci", "Kylie Makeup"]:
        b = by[h]
        xc, xn = lerp(b["cargado"], lo, hi, x0, x1), lerp(b["normal"], lo, hi, x0, x1)
        ok = b["cargado"] < b["normal"]
        s.append(f'<text x="{x0 - 10}" y="{y + 4}" text-anchor="end" class="lb">{nm(h)}</text>')
        s.append(f'<line x1="{xc:.1f}" x2="{xn:.1f}" y1="{y}" y2="{y}" stroke="{GRID}" stroke-width="5" stroke-linecap="round"/>')
        s.append(f'<circle cx="{xn:.1f}" cy="{y}" r="5.5" fill="#fff" stroke="{SHIP}" stroke-width="2"/>')
        s.append(f'<circle cx="{xc:.1f}" cy="{y}" r="6" fill="{CATC[h]}" stroke="#fff" stroke-width="1.5"/>')
        s.append(f'<text x="{x1 + 8}" y="{y + 4}" class="{"okk" if ok and b["meses"] >= 6 else "nok"}">{b["meses"]} de {b["de"]} meses</text>')
        y += 40
    s.append("</svg>")
    return "".join(s)


def exits_chart(ex, W=420, H=200):
    x0, x1, y0, y1 = 36, W - 10, 12, H - 26
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%">', axis_y(x0, x1, y0, y1, 0, 1.1, [0, .25, .5, .75, 1], lambda t: f"{t:.0%}", zero=False)]
    X = [lerp(k, -6, 6, x0, x1) for k in range(-6, 7)]
    xl = lerp(0, -6, 6, x0, x1)
    s.append(f'<line x1="{xl:.1f}" x2="{xl:.1f}" y1="{y0}" y2="{y1}" stroke="{INK2}" stroke-dasharray="3 3"/>'
             f'<text x="{xl + 4:.1f}" y="{y0 + 8}" class="ax">último envío</text>')
    for k in range(-6, 7, 2):
        s.append(f'<text x="{X[k + 6]:.1f}" y="{H - 12}" text-anchor="middle" class="ax">{k:+d}</text>')
    s.append(f'<text x="{(x0 + x1) / 2}" y="{H}" text-anchor="middle" class="axl">meses frente al último envío relevante</text>')
    for c, col in [("Fragancias", FRAG), ("Makeup", MU)]:
        ys = [lerp(min(v, 1.1), 0, 1.1, y1, y0) for v in ex[c]["curve"]]
        s.append(line(X, ys, col, 2.2))
        s.append(f'<text x="{X[-1] - 2:.1f}" y="{ys[-1] - (16 if c == "Fragancias" else 6):.1f}" text-anchor="end" class="vl2" fill="{col}">{c} {ex[c]["curve"][-1]:.0%}</text>')
    s.append("</svg>")
    return "".join(s)


def page_load(D):
    lo = D["load"]
    c = lo["ean_cat"]
    return f'''<section class="page"><div class="kick">5 · Carga del canal y bajas</div>
<h2>Si un EAN acumula 12 meses enviando más de lo que vende, los 3 meses siguientes envía menos: en fragancias pasa los {c["Fragancias"]["meses"]} meses medidos. Kylie es la excepción</h2>
<div class="two">
<div class="card"><div class="ct">Envío − EPOS en los 3 meses siguientes (YoY): EANs cargados frente a normales</div>
<div class="cs">Cargado = envío/EPOS de los últimos 12 meses &gt;15% por encima de su propio FY25 · cortes sep-25 → abr-26</div>
<div class="leg" style="margin:1.5mm 0 0"><span><i style="background:{FRAG}"></i><i style="background:{MU};margin-left:-1mm"></i>Cargados</span><span><i style="background:#fff;border:2px solid {SHIP}"></i>Normales</span><span class="lm">derecha: meses en que cargados &lt; normales</span></div>
{dumbbell(lo["ean_house"])}
<div class="kl">Fragancias: cargados {pc(c["Fragancias"]["cargado"])} vs normales {pc(c["Fragancias"]["normal"])}. En Kylie los "cargados" siguen creciendo: puede ser que gane tiendas o clientes sin EPOS; con el EPOS solo no se puede distinguir.</div></div>
<div class="side">
<div class="card"><div class="ct" style="font-size:10.5pt">Bajas: el consumidor sigue comprando después del último envío</div>
<div class="cs">Mediana del EPOS de los EANs que dejaron de enviarse ({lo["exits"]["Fragancias"]["n"]} fragancias, {lo["exits"]["Makeup"]["n"]} makeup) · índice: su EPOS de 6–12 meses antes = 100%</div>
{exits_chart(lo["exits"])}
<div class="kl">En fragancias el EPOS sigue 6 meses después del último envío (aún al {lo["exits"]["Fragancias"]["curve"][-1]:.0%}); en makeup se agota en 3–4 meses. Antes del corte el EPOS ya cae: es la señal de declive.</div></div>
<div class="note">Gucci Make up, a nivel casa: acumuló carga 9 meses (de +7% a +16% sobre su FY25) sin dejar de enviar por encima del EPOS, y corrigió de golpe (−34% en may–jul-26). <b>La carga avisa, pero no dice cuándo llega la corrección.</b> El WOS lo diría.</div>
</div></div></section>'''


# ---------- página 7: qué hacer ----------
def page_rules(D):
    la, v, t = D["launch"], D["veterans"], D["trend"]
    items = [
        ("La tendencia, del EPOS", f"El EPOS mantiene su dirección de un semestre a otro en el {t['persist']['Total']['keep_epos']:.0%} de los EANs (el envío, en el {t['persist']['Total']['keep_ship']:.0%}). Trend del EAN = YoY de 12 meses del EPOS, comparando el EAN consigo mismo."),
        ("Seguir a mi generación", "Veteranos: el YoY del EPOS de los veteranos de su casa (−12% a −23%; Marc Jacobs 0%). Nunca el trend total de la casa, que incluye los lanzamientos."),
        ("Lanzamientos: año 2 ≠ año 1", f"Del mes 12 al 23, base = EPOS × {min(la['Fragancias']['y2'], la['Makeup']['y2']):.2f}–{max(la['Fragancias']['y2'], la['Makeup']['y2']):.2f} (lo que se envió en el año 2 por unidad vendida), no el envío del año pasado, que fue el llenado ({la['Fragancias']['y1']:.1f}× y {la['Makeup']['y1']:.1f}× el EPOS)."),
        ("Semáforo de carga", "Si envío/EPOS de 12 meses supera en un 15% su propio FY25, recortar los meses siguientes (fragancias y Gucci Make up; no Kylie hasta tener el WOS)."),
        ("Bajas", "Al planificar la salida de un código, contar con que el cliente sigue vendiendo unos 6 meses después del último envío en fragancias y 3–4 en makeup."),
    ]
    cards = "".join(f'<div class="rule"><div class="rn">{i + 1}</div><div><div class="rt">{a}</div><div class="rd">{b}</div></div></div>' for i, (a, b) in enumerate(items))
    return f'''<section class="page"><div class="kick">6 · Qué significa para el forecast</div>
<h2>El EPOS no sirve como número, pero sí como brújula: indica la dirección, la edad del producto y si el canal está lleno</h2>
<div class="two r">
<div class="rules">{cards}</div>
<div class="side">
<div class="card"><div class="ct" style="font-size:10.5pt">Por qué solo en relativo</div>
<div class="kl" style="margin-top:1.5mm">No todos los clientes reportan EPOS (suma ~80% del envío). Por eso todo el reporte compara cada EAN o casa consigo mismo: frente al año anterior o frente a su propia relación envío/EPOS. El nivel absoluto no se usa nunca.</div></div>
<div class="card"><div class="ct" style="font-size:10.5pt">Qué falta para cerrar el círculo</div>
<div class="kl" style="margin-top:1.5mm"><b>WOS</b> (semanas de stock) por EAN y cliente: stock = WOS × venta semanal. Convierte "cargado" en un dato y diría cuándo llega la corrección.<br><br>
<b>Probadores y material de exposición:</b> saber si están en el envío de lanzamiento.<br><br>
<b>Más historia de EPOS:</b> hoy hay 2 años (jul-24 → jul-26); cada mes nuevo refuerza o desmiente estos patrones.</div></div>
<div class="note">Siguiente paso: probar los puntos 1–3 como partido "Consumidor (EPOS)" en el parlamento, con cortes oct-25 → mar-26 y lo real hasta ago-26.</div>
</div></div></section>'''


def cover(D):
    n, t, la, v, lo = D["noise"], D["trend"], D["launch"], D["veterans"], D["load"]
    tiles = [
        (f'{n["ratio_ruido"]:.0f}×', "más ruido en el envío", f'El YoY mensual del envío oscila ~{n["ratio_ruido"]:.0f} veces más que el del EPOS ({pc(n["pct_env_mas_ruidoso"], False)} de los EANs).'),
        (f'{t["same"]:.0%}', "misma dirección a 12 meses", "Envío y EPOS crecen o caen juntos en 8 de cada 10 EANs en el año."),
        (f'{t["persist"]["Total"]["keep_epos"]:.0%} vs {t["persist"]["Total"]["keep_ship"]:.0%}', "la tendencia persiste", "El EPOS mantiene su dirección de un semestre a otro; el envío mucho menos."),
        (f'{la["Fragancias"]["y1"]:.1f}× → {la["Fragancias"]["y2"]:.2f}×', "lanzamientos (fragancias)", f'Envío/EPOS en el año 1 y en el año 2, con el consumidor estable (veteranos {la["Fragancias"]["vet_ratio"]:.2f}×).'),
        ("−12 a −23%", "veteranos al año", "Venta al consumidor de los códigos con historia; la casa crece por los lanzamientos (Marc Jacobs, 0%)."),
        (f'{lo["ean_cat"]["Fragancias"]["meses"]} de {lo["ean_cat"]["Fragancias"]["de"]}', "meses: la carga se corrige", "Fragancias: si en 12 meses se envía de más frente al EPOS, los 3 meses siguientes se envía menos."),
    ]
    tl = "".join(f'<div class="tile"><div class="tv">{a}</div><div class="tk">{b}</div><div class="td">{c}</div></div>' for a, b, c in tiles)
    return f'''<section class="page"><div class="blob"></div><div class="kick">EPOS · patrones · foto sep-26</div>
<h1>Lo que vende el consumidor es estable y predecible.<br>El ruido lo meten los pedidos.</h1>
<div class="lead">Seis patrones entre envío (sell-in) y EPOS (sell-out) en 5 casas, jul-24 → ago-26. Todo en relativo: cada EAN frente a sí mismo, porque no todos los clientes reportan EPOS.</div>
<div class="tiles">{tl}</div>
<div class="method"><div><b>Qué es "envío"</b>Sell-in de la foto sep-26 (actuals), jul-23 → ago-26.</div>
<div><b>Qué es "EPOS"</b>Venta al consumidor de los clientes que reportan (~80% del envío), jul-24 → jul-26.</div>
<div><b>Cómo se compara</b>Siempre en relativo: crecimiento frente al año anterior o relación envío/EPOS frente a la propia historia del EAN.</div>
<div><b>Qué EANs</b>Según el patrón: maduros (lanzados antes de ene-24), lanzamientos jul-24 → jul-25, veteranos (con envío desde jul-23) o bajas.</div></div>
<div class="foot">Datos: DATA.xlsx, GUMU.xlsx, KYMU.xlsx (foto sep-26). Cálculo: <code>src/epos_patrones.py</code> · reporte: <code>src/epos_patrones_report.py</code></div></section>'''


CSS = f"""
@font-face {{ font-family: Inter; src: url('file:///usr/share/fonts/opentype/inter/Inter-Regular.otf'); font-weight: 400; }}
@font-face {{ font-family: Inter; src: url('file:///usr/share/fonts/opentype/inter/Inter-SemiBold.otf'); font-weight: 600; }}
@font-face {{ font-family: Inter; src: url('file:///usr/share/fonts/opentype/inter/Inter-Bold.otf'); font-weight: 700; }}
@font-face {{ font-family: InterDisplay; src: url('file:///usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'); font-weight: 700; }}
@page {{ size: A4 landscape; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Inter, sans-serif; color: {INK}; background: #F7F8F6; }}
.page {{ width: 297mm; height: 210mm; padding: 10mm 13mm 8mm; position: relative; overflow: hidden; page-break-after: always; background: #F7F8F6; }}
.blob {{ position: absolute; right: -60mm; top: -90mm; width: 170mm; height: 170mm; border-radius: 50%;
  background: radial-gradient(circle at 30% 70%, #E6E2FA 0%, #FBE6DC 55%, rgba(247,248,246,0) 72%); }}
.kick {{ position: relative; font-size: 8pt; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: {FRAG}; }}
h1 {{ position: relative; font-family: InterDisplay, Inter; font-size: 30pt; letter-spacing: -.02em; line-height: 1.08; margin-top: 3mm; max-width: 220mm; }}
h2 {{ position: relative; font-family: InterDisplay, Inter; font-size: 14.5pt; letter-spacing: -.01em; line-height: 1.18; margin: 1.2mm 0 3mm; max-width: 262mm; }}
.lead {{ position: relative; font-size: 10.5pt; color: {INK2}; margin-top: 4mm; max-width: 200mm; line-height: 1.45; }}
.tiles {{ position: relative; display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; margin-top: 9mm; }}
.tile {{ background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; padding: 4mm 4.6mm; border-top: 3px solid {FRAG}; }}
.tile:nth-child(even) {{ border-top-color: {MU}; }}
.tv {{ font-family: InterDisplay, Inter; font-size: 22pt; font-weight: 700; letter-spacing: -.01em; }}
.tk {{ font-size: 8pt; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: {INK2}; margin: .8mm 0 1.6mm; }}
.td {{ font-size: 8.4pt; color: {INK2}; line-height: 1.45; }}
.method {{ position: relative; display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; margin-top: 7mm; font-size: 7.8pt; color: {INK2}; line-height: 1.45; }}
.method div {{ border-left: 2px solid {GRID}; padding-left: 3mm; }}
.method b {{ display: block; color: {INK}; font-size: 8pt; margin-bottom: .6mm; }}
.foot {{ position: absolute; left: 13mm; right: 13mm; bottom: 7mm; font-size: 7.2pt; color: {MUTED}; border-top: 1px solid {GRID}; padding-top: 2mm; }}
code {{ font-size: 7pt; }}
.leg {{ position: relative; display: flex; gap: 5mm; align-items: center; font-size: 7.6pt; color: {INK2}; margin-bottom: 3mm; flex-wrap: wrap; }}
.leg.sm {{ font-size: 6.8pt; gap: 3mm; margin: 1mm 0 0; }}
.leg i {{ display: inline-block; width: 3mm; height: 3mm; border-radius: 50%; margin-right: 1.4mm; vertical-align: -.4mm; }}
.leg i.ln {{ width: 6mm; height: 0; border-radius: 0; border-top: 2px solid; vertical-align: .8mm; }}
.leg .lm {{ color: {MUTED}; margin-left: auto; }}
.grid {{ position: relative; display: grid; gap: 4mm; }}
.grid.c3 {{ grid-template-columns: repeat(3, 1fr); }}
.grid.c2 {{ grid-template-columns: repeat(2, 1fr); }}
.two {{ position: relative; display: grid; grid-template-columns: 1.15fr 1fr; gap: 5mm; }}
.two.r {{ grid-template-columns: 1.25fr 1fr; }}
.side {{ display: flex; flex-direction: column; gap: 4mm; }}
.card {{ background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; padding: 3mm 3.8mm; }}
.ch {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1mm; }}
.ct {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 11.5pt; }}
.cs {{ font-size: 7pt; color: {MUTED}; margin-top: .4mm; }}
.cv {{ font-weight: 700; font-size: 9pt; text-align: right; line-height: 1.1; }}
.cv span {{ display: block; font-size: 6.2pt; font-weight: 600; }}
.kpi2 .kv {{ font-family: InterDisplay, Inter; font-size: 26pt; font-weight: 700; margin: .5mm 0 1mm; }}
.kl {{ font-size: 7.8pt; color: {INK2}; line-height: 1.45; }}
.sub2 {{ font-size: 7.2pt; font-weight: 600; color: {INK2}; margin: 1.5mm 0 .5mm; }}
.note {{ position: relative; font-size: 7.8pt; line-height: 1.5; color: {INK2}; background: #fff; border: 1px solid #E6EAEE; border-left: 3px solid {FRAG}; border-radius: 10px; padding: 2.6mm 3.6mm; }}
.tb {{ width: 100%; border-collapse: collapse; font-size: 7.6pt; margin-top: 2mm; }}
.tb th {{ font-size: 6.2pt; text-transform: uppercase; letter-spacing: .05em; color: {MUTED}; text-align: left; padding: 1mm 1.5mm; border-bottom: 1px solid {GRID}; font-weight: 600; }}
.tb td {{ padding: 1mm 1.5mm; border-bottom: 1px solid #F0F2F4; }}
.rules {{ display: flex; flex-direction: column; gap: 3mm; }}
.rule {{ display: grid; grid-template-columns: 9mm 1fr; gap: 3mm; background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; padding: 3mm 4mm; }}
.rn {{ width: 8mm; height: 8mm; border-radius: 50%; background: {FRAG}; color: #fff; font-weight: 700; display: flex; align-items: center; justify-content: center; font-size: 10pt; }}
.rule:nth-child(even) .rn {{ background: {MU}; }}
.rt {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 11pt; margin-bottom: .8mm; }}
.rd {{ font-size: 8.2pt; color: {INK2}; line-height: 1.45; }}
svg .ax {{ font-family: Inter; font-size: 8px; fill: {MUTED}; }}
svg .axl {{ font-family: Inter; font-size: 8.5px; fill: {INK2}; font-weight: 600; }}
svg .lb {{ font-family: Inter; font-size: 9px; fill: {INK}; font-weight: 600; }}
svg .vl {{ font-family: Inter; font-size: 9px; fill: {INK}; font-weight: 700; }}
svg .vl2 {{ font-family: Inter; font-size: 8px; fill: {INK2}; font-weight: 600; }}
svg .in {{ font-family: Inter; font-size: 8.5px; font-weight: 700; }}
svg .q {{ font-family: Inter; font-size: 8.5px; fill: {MUTED}; font-style: italic; }}
svg .okk {{ font-family: Inter; font-size: 9px; font-weight: 700; fill: #1B7F5B; }}
svg .nok {{ font-family: Inter; font-size: 9px; font-weight: 700; fill: {MUTED}; }}
"""


def main():
    D = json.loads((ROOT / "work" / "epos_patrones.json").read_text())
    html = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Patrones EPOS</title><style>{CSS}</style></head><body>' + \
        cover(D) + page_noise(D) + page_trend(D) + page_launch(D) + page_vet(D) + page_load(D) + page_rules(D) + "</body></html>"
    hp = ROOT / "work" / "epos_patrones.html"
    hp.write_text(html, encoding="utf-8")
    OUT.parent.mkdir(exist_ok=True)
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={OUT}", f"file://{hp}"], check=True, capture_output=True)
    print(OUT)


if __name__ == "__main__":
    main()
