"""Reporte PDF del parlamento de 6 partidos con la lógica de DAs reconstruida (fotos sep-25, dic-25 y mar-26 → real sep-26).
Lee work/six_multi.json, work/six_multi.parquet, work/six_multi_ean.parquet, work/ideo_brujulas6.json, work/ideo_brujulas6_ean.parquet,
work/da_conversion.json y work/ideo_panel.pkl. Correr antes: src/da_conversion.py, src/ideo_brujulas6.py, src/six_multi.py.
Salida: reportes/REPORTE_6_PARTIDOS.pdf y reportes/PARTIDOS6_EAN.xlsx"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_brujulas6 as b6  # noqa
import ideo_report as ir  # noqa
import ideo_viz as iv  # noqa
import votes_report as vr  # noqa

ROOT = Path(__file__).resolve().parents[1]; W = ROOT / "work"
OUT = ROOT / "reportes" / "REPORTE_6_PARTIDOS.pdf"
INK, INK2, MUTED = iv.INK, iv.INK2, iv.MUTED
pc, n0 = iv.pc, iv.n0
HOUSES = ["Burberry", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"]
FOTO = {"2025-09": "sep-25", "2025-12": "dic-25", "2026-03": "mar-26"}
QN = {"FY26.Q2": ("Q2 FY26", "oct–dic 25"), "FY26.Q3": ("Q3 FY26", "ene–mar 26"), "FY26.Q4": ("Q4 FY26", "abr–jun 26")}
LAG = {("2025-09", "FY26.Q2"): "1–3", ("2025-09", "FY26.Q3"): "4–6", ("2025-09", "FY26.Q4"): "7–9",
       ("2025-12", "FY26.Q3"): "1–3", ("2025-12", "FY26.Q4"): "4–6", ("2026-03", "FY26.Q4"): "1–3"}
FLAGS = [("0", "Sin bandera", "Forecast de sistema"), ("1", "Bandera 1", "1 customer ignorado"), ("2", "Bandera 2", "Los 2 ignorados: manual")]


def sec(kick, title, body, cls=""):
    return f"<section class='page {cls}'><div class='blob'></div><div class='kick'>{kick}</div><h2>{title}</h2>{body}</section>"


def flag_share():
    Pn = pd.read_pickle(W / "ideo_panel.pkl"); a = Pn["attr"]; v = a.votante.values
    out = {}
    for f in [0, 1, 2]:
        m = v & (a.isf.values == f)
        out[f] = dict(n=int(m.sum()), da_cons=float(Pn["DAf"][m].clip(0).sum() / Pn["cons"][m].sum()), cons_real=float(Pn["cons"][m].sum() / Pn["A"][m].sum()))
    return out


def timeline(w=620, h=165):
    """Esquema de la lógica de DAs con el ejemplo del usuario."""
    months = pd.date_range("2025-07-01", "2026-12-01", freq="MS")
    ml, mr = 20, 20
    X = lambda t: ml + (months.get_loc(t) + .5) / len(months) * (w - ml - mr)
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" class="tl">']
    y0 = 128
    s.append(f'<line x1="{ml}" x2="{w - mr}" y1="{y0}" y2="{y0}" stroke="#B9C0C8" stroke-width="1.2"/>')
    for t in months:
        x = X(t); lab = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"][t.month - 1]
        s.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y0 - 3}" y2="{y0 + 3}" stroke="#B9C0C8"/>')
        s.append(f'<text x="{x:.1f}" y="{y0 + 14}" text-anchor="middle" class="ax">{lab}</text>')
        if t.month == 1 or t == months[0]:
            s.append(f'<text x="{x:.1f}" y="{y0 + 25}" text-anchor="middle" class="ax b">{t.year}</text>')
    for t, lab, col in [(pd.Timestamp("2025-09-01"), "Foto sep-25", INK2), (pd.Timestamp("2026-09-01"), "Foto sep-26 (hoy)", INK)]:
        x = X(t)
        s.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="20" y2="{y0 + 30}" stroke="{col}" stroke-width="1.6" stroke-dasharray="4 3"/>')
        s.append(f'<text x="{x - 6:.1f}" y="14" text-anchor="end" class="ph">{lab}</text>')
    # DA de dic-25 (planificado en sep-25, borrado en sep-26)
    xd = X(pd.Timestamp("2025-12-01"))
    s.append(f'<rect x="{xd - 9:.1f}" y="{y0 - 52}" width="18" height="52" rx="2" fill="{iv.FRAG}" opacity=".85"/>')
    s.append(f'<text x="{xd:.1f}" y="{y0 - 57}" text-anchor="middle" class="dl">DA 1.000</text>')
    s.append(f'<text x="{xd + 14:.1f}" y="{y0 - 34}" class="nt2">visto en la foto sep-25</text><text x="{xd + 14:.1f}" y="{y0 - 24}" class="nt2">(o9 lo borra en sep-26)</text>')
    xb = X(pd.Timestamp("2026-12-01"))
    s.append(f'<path d="M{xd:.1f},{y0 - 62} C{xd + 70:.1f},{y0 - 100} {xb - 70:.1f},{y0 - 100} {xb - 4:.1f},{y0 - 8}" fill="none" stroke="{iv.FRAG}" stroke-width="1.4" marker-end="url(#ar)"/>')
    s.append(f'<text x="{xd + 18:.1f}" y="{y0 - 92}" class="nt3" fill="{iv.FRAG}">base de dic-26 = dic-25 → ¿cuánto del DA planificado le resto?</text>')
    # DA de nov-26 (insight de la foto actual)
    xn = X(pd.Timestamp("2026-11-01"))
    s.append(f'<rect x="{xn - 9:.1f}" y="{y0 - 26}" width="18" height="26" rx="2" fill="{iv.RGDA}" opacity=".9"/>')
    s.append(f'<text x="{xn:.1f}" y="{y0 - 31}" text-anchor="middle" class="dl">DA 500</text>')
    s.append(f'<text x="{xn - 14:.1f}" y="{y0 - 12}" text-anchor="end" class="nt2">foto sep-26: insight, se suma</text>')
    s.append(f'<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{iv.FRAG}"/></marker></defs>')
    s.append("</svg>")
    return "".join(s)


def bars(rows, w=300, lab_w=110, color=INK2, maxv=1.2, fmt=pc):
    bh, gap = 10, 6
    h = len(rows) * (bh + gap) + 4
    span = w - lab_w - 46
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" class="hb">']
    x100 = lab_w + span / maxv
    s.append(f'<line x1="{x100:.1f}" x2="{x100:.1f}" y1="0" y2="{h}" stroke="#B9C0C8" stroke-dasharray="3 3"/>')
    for i, (lab, v, col) in enumerate(rows):
        y = i * (bh + gap) + 2
        bw = max(min(v, maxv) / maxv * span, 0.5)
        s.append(f'<text x="{lab_w - 5}" y="{y + bh - 2:.1f}" text-anchor="end" class="hl">{lab}</text>')
        s.append(f'<rect x="{lab_w}" y="{y}" width="{bw:.1f}" height="{bh}" rx="2" fill="{col or color}"/>')
        s.append(f'<text x="{lab_w + bw + 4:.1f}" y="{y + bh - 2:.1f}" class="hv">{fmt(v)}</text>')
    s.append("</svg>")
    return "".join(s)


def cards_page(P, kick, title, items, cols, extra="", inside=""):
    return (f"<section class='page'><div class='blob'></div><div class='kick'>{kick}</div><h2>{title}</h2>{iv.legend(P)}"
            f"<div class='grid c{cols}'>{''.join(iv.card(P, t, s, d) for t, s, d in items)}{inside}</div>{extra}</section>")


def main():
    D = json.loads((W / "six_multi.json").read_text())
    Bj = json.loads((W / "ideo_brujulas6.json").read_text())
    C = json.loads((W / "da_conversion.json").read_text())
    B = pd.read_parquet(W / "six_multi.parquet")
    E = pd.read_parquet(W / "six_multi_ean.parquet").set_index("ean")
    POS = pd.read_parquet(W / "ideo_brujulas6_ean.parquet")
    P = b6.P6()
    T = D["por"]["Total"]["Total"]; per = D["persistencia"]; hor = D["horizonte"]
    fs = flag_share()
    conv = {(r["cat"],): r for r in C["total"]}; convf = {(r["cat"], r["flag"]): r for r in C["flag"]}
    convl = {(r["cat"], r["lag_g"]): r for r in C["lag"]}
    # ---------------- portada
    rows = "".join(f"<tr><td>{P.dot(p, num=True)}<b>{p}</b><span class='bl'>{P.bloc[p]}</span></td><td class='n'>{T['seats'][p]}</td>"
                   f"<td class='n'>{pc(T['seats'][p] / T['eans'])}</td><td class='n'>{pc(T['vol'][p])}</td></tr>" for p in P.names)
    rows += f"<tr><td>{P.dot('Empate')}<b>Empate</b></td><td class='n'>{T['seats']['Empate']}</td><td class='n'>{pc(T['seats']['Empate'] / T['eans'])}</td><td class='n'>{pc(T['vol']['Empate'])}</td></tr>"
    p9 = per["2025-09"]; p3 = per["2026-03"]; p12 = per["2025-12"]
    kp = (f"<div class='kpis3'>"
          f"<div class='kpi'><div class='kl'>A 7–9 meses (sep-25 → abr–jun)</div><div class='kv2'>{pc(p9['parl']['ean'])} <small>vs {pc(p9['cons']['ean'])} consenso</small></div><div class='kl'>error EAN a EAN; el EAN eligió partido con oct–mar</div></div>"
          f"<div class='kpi'><div class='kl'>A 4–6 meses (dic-25 → abr–jun)</div><div class='kv2'>{pc(p12['parl']['ean'])} <small>vs {pc(p12['cons']['ean'])} consenso</small></div><div class='kl'>el consenso ya gana</div></div>"
          f"<div class='kpi'><div class='kl'>A 1–3 meses (mar-26 → abr–jun)</div><div class='kv2'>{pc(p3['parl']['ean'])} <small>vs {pc(p3['cons']['ean'])} consenso</small></div><div class='kl'>de cerca, el consenso sabe más</div></div></div>")
    finds = [("DAs de la base", f"Se leen de la foto en la que el mes aún era futuro. En fragancias solo el {pc(conv[('Fragancias',)]['conversion'])} del DA planificado se convirtió en envío extra; en makeup, el {pc(conv[('Makeup',)]['conversion'])}."),
             ("DAs futuros", f"Insight: se suman. Con bandera 2 el consenso es {pc(fs[2]['da_cons'])} DAs: sumarlos duplica. Regla: 100% sin bandera, 50% con bandera 1, 0% con bandera 2."),
             ("Edad", "El ciclo de vida es el partido de los códigos nuevos: curva de los códigos de su casa y segmento hasta 17 meses; después manda su fase."),
             ("Horizonte", f"El parlamento gana lejos (7–9 meses: {pc(p9['parl']['ean'])} contra {pc(p9['cons']['ean'])}). A menos de 6 meses, el consenso es mejor."),
             ("Propuesta", "Sistema híbrido: consenso para los meses cercanos y el partido de cada EAN para el horizonte lejano; repetir con más fotos.")]
    fh = "".join(f"<div class='fd'><div class='fdt'>{t}</div><div class='fdx'>{x}</div></div>" for t, x in finds)
    p1 = f"""<section class='page'><div class='blob'></div>
  <div class='kick'>Parlamento de 6 · fotos sep-25, dic-25 y mar-26 → real sep-26 · {D['n_votantes']} EANs · 6 urnas</div>
  <h1>Con los DAs bien leídos, el parlamento gana lejos;<br/><span style='color:{INK2}'>a menos de 6 meses, manda el consenso.</span></h1>
  <div class='top'>
    <div class='hemi'>{iv.hemicycle(P, T['seats'], w=520, big=True)}
      <div class='vl' style='margin-top:2.6mm'>Volumen real de los EANs que gana cada partido (todas las urnas)</div>{iv.volbar(P, T['vol'], h=6)}{kp}</div>
    <div class='side'>
      <table class='st'><tr><th>Partido</th><th>EANs</th><th>%</th><th>Volumen</th></tr>{rows}</table>
      <div class='note'><b>Cómo se vota.</b> Urnas = quarters completos de cada foto: sep-25 (Q2, Q3, Q4 FY26), dic-25 (Q3, Q4; solo fragancias) y mar-26 (Q4).
        En cada urna el EAN vota al partido con menor WAPE del quarter; gana el que suma más votos (empate: menor WAPE sumado). Votan los EANs Central con actividad de cada foto.
        Los kpis de abajo son la prueba honesta: el EAN elige con oct–mar y se mide abr–jun.</div>
    </div></div><div class='finds'>{fh}</div></section>"""
    # ---------------- DAs: lógica
    ftab = "".join(f"<tr><td><b>{lab}</b><span class='bl'>{sub}</span></td><td class='n'>{fs[int(k)]['n']}</td><td class='n'>{pc(fs[int(k)]['da_cons'])}</td>"
                   f"<td class='n'>{fs[int(k)]['cons_real']:.2f}".replace(".", ",") + f"</td><td class='n'><b>{['100%', '50%', '0%'][int(k)]}</b></td></tr>" for k, lab, sub in FLAGS)
    p2 = sec("La lógica de los DAs", "Dos decisiones distintas: los DAs de los meses de la base se leen de la foto en la que aún eran futuro; los DAs futuros de la foto actual se suman según la bandera.",
             f"<div class='box'>{timeline()}</div>"
             f"<div class='g3b' style='margin-top:3.4mm'>"
             f"<div class='box'><div class='ct'>1 · El trend</div><p class='sm'>Se calcula con los actuals tal cual (suma 12M o 6M frente a los mismos meses del año anterior). Los DAs no lo tocan.</p>"
             f"<div class='ct' style='margin-top:2.4mm'>2 · La base</div><p class='sm'>Si un mes de la base tuvo un DA, ese volumen puede ser promoción que no se repite. "
             f"Como o9 borra los DAs viejos, el DA de cada mes se toma de la <b>última foto en la que ese mes todavía no estaba cerrado</b> (para dic-25: la foto de sep-25). "
             f"Antes de la primera foto, el que esa foto guarda como pasado. Cuánto restar es ideología de cada partido (brújula 3).</p></div>"
             f"<div class='box'><div class='ct'>3 · Los DAs futuros de la foto</div><p class='sm'>Son insight y se suman. Pero con la Ignore System Forecast Flag prendida el consenso ya son los DAs: sumarlos al partido duplica el volumen.</p>"
             f"<table class='t6 s'><tr><th>Bandera en la foto (sep-25)</th><th>EANs</th><th>DAs / consenso</th><th>Consenso / real</th><th>DAs que se suman</th></tr>{ftab}</table></div>"
             f"<div class='box'><div class='ct'>Por qué importa</div><ul class='ul'>"
             f"<li>Con bandera 2 el consenso es {pc(fs[2]['da_cons'])} DAs y se pasa un {pc(fs[2]['cons_real'] - 1)} del real.</li>"
             f"<li>48 de los 67 EANs con bandera 2 son lanzamientos de 6–11 meses: sus DAs superaban su venta real en cada quarter.</li>"
             f"<li>Con la regla de la bandera, el error EAN a EAN del parlamento en todas las urnas baja de {pc(D['total']['ean']['parl100'])} a {pc(D['total']['ean']['parl'])}.</li></ul></div></div>")
    # ---------------- DAs: conversión
    cr = lambda cat, col: [(f"{cat} · total", conv[(cat,)]["conversion"], col)] + \
        [(f"sin bandera" if f == "0" else f"bandera {f}", convf[(cat, f)]["conversion"], col) for f in ["0", "1", "2"]] + \
        [(f"a {l}", convl[(cat, l)]["conversion"], col) for l in ["1–3 meses", "4–6 meses", "7–9 meses"]]
    sig = "".join(f"<tr><td>{r['cat']}</td><td>foto {FOTO.get(r['foto'], r['foto'])}</td><td class='n'>{n0(r['da'])}</td><td class='n'><b>{pc(r['sigue'])}</b></td></tr>" for r in C["sigue"])
    casas = sorted(C["casa"], key=lambda r: -r["da"])
    crc = [(r["casa"], r["conversion"], iv.FRAG if r["casa"] in HOUSES[:3] else iv.MU) for r in casas]
    p3_ = sec("¿Se ejecutan los DAs planificados?",
              f"De cada DA planificado, en fragancias solo el {pc(conv[('Fragancias',)]['conversion'])} se convirtió en envío extra (sin bandera, el {pc(convf[('Fragancias', '0')]['conversion'])}); en makeup, el {pc(conv[('Makeup',)]['conversion'])}.",
              f"<div class='g3b'><div class='box'><div class='ct'>Fragancias</div><div class='cs'>Envío extra / DA planificado. Línea punteada = 100%. Bandera 1: solo {n0(convf[('Fragancias', '1')]['da'])} unidades de DA, poco fiable.</div>{bars(cr('Fragancias', iv.FRAG), w=220, lab_w=84, maxv=1.6)}</div>"
              f"<div class='box'><div class='ct'>Makeup</div><div class='cs'>Envío extra / DA planificado. Línea punteada = 100%.</div>{bars(cr('Makeup', iv.MU), w=220, lab_w=84, maxv=1.6)}</div>"
              f"<div class='box'><div class='ct'>Por casa</div>{bars(crc, w=220, lab_w=84, maxv=1.6)}<div class='ct' style='margin-top:2.6mm'>¿Sigue en la foto siguiente?</div>"
              f"<table class='t6 s'><tr><th>Categoría</th><th>Plan</th><th>DA planificado</th><th>Sigue</th></tr>{sig}</table></div></div>"
              f"<div class='box' style='margin-top:3mm'><div class='ct'>Cómo se mide</div><p class='sm'>Para cada foto y mes futuro hasta ago-26: envío extra = real − (consenso de la foto − DA), "
              f"corregido por el desvío medio de los EANs sin DA de la misma foto y casa. 100% = el DA se convirtió entero en envío extra. Con bandera 2 el consenso es el DA: ahí mide real / DA. "
              f"«Sigue» = parte del volumen planificado que la foto siguiente todavía tenía en ese mes (aún abierto).</p>"
              f"<p class='sm'><b>Lectura para la base:</b> restar el DA entero quita volumen que nunca fue promoción. Lo coherente con los datos es restar en torno a la conversión medida: "
              f"cerca del 50% en fragancias (lo que hace la regla) y más en makeup (la regla resta el 25%). Cuanto más lejos se planificó el DA, menos se cumple.</p></div>")
    # ---------------- partidos
    tab = ""
    w90 = pd.DataFrame(D["w90"])
    for nm in P.names:
        k = Bj["nombres"].index(nm); ide = Bj["ideas"][k]
        form = Bj["partidos"][k].replace(" · + 100% DAs de la foto", "").replace(" · sin DAs de la foto", "").replace(" · + 50% DAs de la foto", "")
        col = "F:" + nm
        tab += (f"<tr><td class='pn'>{P.dot(nm, num=True)}<b>{nm}</b><span class='bl'>{'Fijo · ' if nm.startswith('Regla') else ''}{P.bloc[nm]}</span></td>"
                f"<td class='f'>{form} · DAs futuros según bandera</td><td class='n'>{T['seats'][nm]}</td><td class='n'>{pc(T['vol'][nm])}</td>"
                f"<td class='n'>{pc(float((w90[col] * w90.real).sum() / w90.real.sum()))}</td><td class='n'>{pc(float(np.abs(B[col] - B.real).sum() / B.real.sum()))}</td></tr>")
    p4 = sec("Los 6 partidos", "Dos reglas fijas, el ciclo de vida para la edad y tres partidos de nivel reciente; ninguno usa solo los últimos 3 meses.",
             f"<table class='pt'><tr><th>Partido</th><th>Fórmula</th><th>EANs</th><th>Volumen</th><th>WAPE90 solo</th><th>Error EAN solo</th></tr>{tab}</table>"
             f"<div class='foot'>«Solo» = el partido aplicado a todos los EANs en las 6 urnas. WAPE90 = |Σ forecast − Σ real| por casa y urna, ponderado por volumen "
             f"(consenso {pc(D['total']['w90']['cons'])}); error EAN = Σ |forecast − real| por EAN y quarter / Σ real (consenso {pc(D['total']['ean']['cons'])}).</div>", "pp")
    # ---------------- brújulas
    pts = POS.join(E[["voto"]])
    st_ = Bj["stats"]
    def mk(kx, ky):
        out = []
        for e, r in pts.iterrows():
            if r.voto not in P.col or r.voto == "Empate":
                continue
            rng = np.random.default_rng(abs(hash(e)) % 2**32)
            out.append(dict(x=float(np.clip(r[kx] + rng.normal(0, .02), -1.08, 1.08)), y=float(np.clip(r[ky] + rng.normal(0, .02), -1.08, 1.08)), party=r.voto, vol=float(r.real)))
        return out
    specs = [("c1", "1 · ¿De dónde parto?", ("Plana", "Con temporada"), ("Memoria reciente (6M)", "Lejana (12M / año pasado)"),
              ("Planos de memoria larga", "Estacionales de memoria larga", "Planos de lo reciente", "Estacionales de lo reciente")),
             ("c2", "2 · ¿A quién sigo?", ("Individual: EAN, línea", "Colectivo: casa, categoría"), ("Trend suave", "Trend completo"),
              ("Individualistas creyentes", "Colectivistas creyentes", "Individualistas escépticos", "Colectivistas escépticos")),
             ("c3", "3 · ¿Cómo limpio la base?", ("Deja los DAs planificados", "Los resta"), ("No suma cortes", "Suma cortes"),
              ("Suma cortes, deja DAs", "Suma cortes y resta DAs", "Base tal cual", "Solo resta DAs"))]
    comps = "".join(iv.compass(P, mk(k + "x", k + "y"), xl, yl, t, q, w=330, h=420, xlim=(-1.14, 1.14), ylim=(-1.14, 1.14),
                               fixed={nm: (Bj["posiciones"][k][nm][0] * .86, Bj["posiciones"][k][nm][1] * .86) for nm in P.names}) for k, t, xl, yl, q in specs)
    notes = [f"<b>¿De dónde parto?</b> Con temporada gana en el {pc(st_['c1x']['der_fr'])} de los EANs de fragancias (plana, {pc(st_['c1x']['izq_fr'])}); makeup se reparte "
             f"({pc(st_['c1x']['der_mu'])} / {pc(st_['c1x']['izq_mu'])}). Al {pc(st_['c1y']['centro'])} le da igual 6 o 12 meses.",
             f"<b>¿A quién sigo?</b> El {pc(st_['c2x']['centro'])} está en el centro (en sep-25 casi todos los trends chocan con el tope de −30%). El {pc(st_['c2y']['der'])} acierta más creyéndose el trend entero.",
             f"<b>¿Cómo limpio la base?</b> Con los DAs planificados y los futuros según bandera, al {pc(st_['c3x']['centro'])} le da igual restar o no los DAs de la base y al {pc(st_['c3y']['centro'])} los cortes."]
    p5 = sec("Brújulas · las 3 preguntas de cada código", "Fragancias se inclina por la temporada; la mayoría cree en el trend completo; DAs de la base y cortes mueven a pocos EANs.",
             iv.legend(P, "Círculo con borde = partido por su fórmula · punto = EAN de la foto sep-25 (tamaño = volumen), color = partido al que vota")
             + f"<div class='g3c'>{comps}</div><div class='g3n'>{''.join(f'<div class=nt>{x}</div>' for x in notes)}</div>")
    # ---------------- tarjetas
    U = D["urnas"]
    uitems = [(f"{FOTO[k.split('|')[0]]} · {QN[k.split('|')[1]][0]}", f"{QN[k.split('|')[1]][1]} · a {LAG[tuple(k.split('|'))]} meses", U[k]) for k in U]
    p6 = cards_page(P, "Por urna (foto × quarter)", f"Cada urna es una elección: {max(P.names, key=lambda p: sum(U[k]['seats'][p] for k in U))} es el partido que más urnas-EAN gana.", uitems, 3)
    po = D["por"]
    citems = [("Fragancias", "Burberry, Gucci, Marc Jacobs", po["Categoría"]["Fragancias"]), ("Makeup", "Gucci Make up, Kylie", po["Categoría"]["Makeup"])] + \
             [(h, "Fragancias" if h in HOUSES[:3] else "Makeup", po["Casa"][h]) for h in HOUSES if h in po["Casa"]]
    p7 = cards_page(P, "Por categoría y casa", (f"Ningún partido pasa del 34% de los EANs en ninguna casa. En fragancias las dos reglas se llevan el "
                                                   f"{pc(po['Categoría']['Fragancias']['vol']['Regla fragancias'] + po['Categoría']['Fragancias']['vol']['Regla makeup'])} del volumen con el "
                                                   f"{pc((po['Categoría']['Fragancias']['seats']['Regla fragancias'] + po['Categoría']['Fragancias']['seats']['Regla makeup']) / po['Categoría']['Fragancias']['eans'])} de los EANs."), citems, 4)
    eitems = [(f"{k} meses", s, po["Edad"][k]) for k, s in ir.TRAMOS if k in po["Edad"]] + [(t, s, po["Bandera"][k]) for k, t, s in FLAGS if k in po["Bandera"]]
    young = po["Edad"].get("6–11", {}); yw = young.get("win_eans", "")
    p8 = cards_page(P, "Por edad y bandera", f"Los recién lanzados (6–11 meses) votan sobre todo {yw}; los maduros se reparten.", eitems, 4)
    fitems = [(k, s, po["Fase"][k]) for k, s in ir.FASES if k in po["Fase"]]
    p9_ = cards_page(P, "Por fase de madurez", "La fase reparte el voto: ningún partido domina una fase entera.", fitems, "5 c5")
    sizes = [("Mini ≤15", "≤15 ml"), ("Pequeño 20–40", "20–40 ml"), ("Medio 45–60", "45–60 ml"), ("Grande 75–125", "75–125 ml"), ("Jumbo/refill ≥150", "≥150 ml"), ("Ancilares", "deo, body lotion, gel")]
    p10 = cards_page(P, "Por tamaño · solo fragancias", "Por tamaño tampoco hay mayorías.", [(k, s, po["Tamaño"][k]) for k, s in sizes if k in po["Tamaño"]], 3)
    # ---------------- WAPE90
    cols = [("cons", "Consenso", iv.CONS), ("parl", "Parlamento", INK), ("regla_da", "Reglas + DAs", iv.RGDA)]
    head = "".join(f"<th>{lab}</th>" for _, lab, _ in cols) + "".join(f"<th>SPP3 {lab.split()[0]}</th>" for _, lab, _ in cols)
    body = ""
    for h in HOUSES:
        x = w90[w90.casa == h].sort_values(["foto", "q"])
        for i, (_, r) in enumerate(x.iterrows()):
            b_ = min(cols, key=lambda c: r[c[0]])[0]
            body += f"<tr class='{'hs' if i == 0 else ''}'>" + (f"<td rowspan='{len(x)}' class='hh'>{h}</td>" if i == 0 else "")
            body += f"<td class='qq'>{FOTO[r.foto]} · {QN[r.q][0]} <i>{QN[r.q][1]} · a {LAG[(r.foto, r.q)]} m</i></td>"
            for c, _, col in cols:
                body += (f"<td class='n' style='background:{col}1F;font-weight:700'>{pc(r[c])}</td>" if c == b_ else f"<td class='n'>{pc(r[c])}</td>")
            for c, _, _ in cols:
                v_ = r["spp3_" + c]; body += f"<td class='n sp'>{'+' if v_ > 0 else '−'}{pc(abs(v_))}</td>"
            body += "</tr>"
    tot = "".join(f"<td class='n tt'>{pc(D['total']['w90'][c])}</td>" for c, _, _ in cols) + "<td colspan='3'></td>"
    body += f"<tr class='hs tot'><td colspan='2' class='hh'>Ponderado por volumen</td>{tot}</tr>"
    p11 = sec("WAPE90 por casa y urna", f"En el total de la casa el parlamento empata con el consenso ({pc(D['total']['w90']['parl'])} contra {pc(D['total']['w90']['cons'])}) y gana {D['total']['gana']} de {D['total']['n']} filas; donde gana claro es EAN a EAN ({pc(D['total']['ean']['parl'])} contra {pc(D['total']['ean']['cons'])}).",
              f"<table class='wt w6'><tr><th>Casa</th><th>Urna</th>{head}</tr>{body}</table>"
              f"<div class='foot'>Parlamento = cada EAN con el partido que eligió en las 6 urnas (con trampa: eligió viendo esos mismos quarters) y DAs futuros según bandera. Reglas + DAs = comparación estándar (100% de los DAs de la foto). "
              f"SPP3 = (real − forecast) / real: negativo = overforecast. La prueba honesta está en la página siguiente.</div>", "w90p")
    # ---------------- horizonte
    hr = ""
    for f, lg in [("2025-09", "7–9"), ("2025-12", "4–6"), ("2026-03", "1–3")]:
        x = per[f]
        best = min(["cons", "parl", "regla_da"], key=lambda c: x[c]["ean"])
        cell = lambda c: (f"<td class='n' style='background:#F1F2F4;font-weight:700'>{pc(x[c]['ean'])}</td>" if c == best else f"<td class='n'>{pc(x[c]['ean'])}</td>")
        hr += (f"<tr><td><b>Foto {FOTO[f]}</b><span class='bl'>abr–jun a {lg} meses</span></td>{cell('cons')}{cell('parl')}{cell('regla_da')}"
               f"<td class='n'>{pc(x['parl100']['ean'])}</td><td class='n'>{pc(x['cons']['w90'])}</td><td class='n'>{pc(x['parl']['w90'])}</td><td class='n'>{pc(x['regla_da']['w90'])}</td></tr>")
    young = "".join(f"<tr><td>{f'Foto {FOTO[f]}'}</td>" + "".join(f"<td class='n'>{pc(per[f]['tramos'][t][c])}</td>" for c in ['cons', 'parl'] for t in ['6–11']) + "</tr>"
                    for f in per if "6–11" in per[f]["tramos"])
    p12_ = sec("Prueba honesta: elegir con oct–mar y medir en abr–jun",
               f"Lejos (7–9 meses) el parlamento gana con claridad: {pc(p9['parl']['ean'])} contra {pc(p9['cons']['ean'])}. Cerca (1–3 meses) el consenso sabe más: {pc(p3['cons']['ean'])} contra {pc(p3['parl']['ean'])}.",
               f"<table class='tt1'><tr><th></th><th>Consenso</th><th>Parlamento</th><th>Reglas + DAs</th><th>Parlamento con DAs al 100%</th><th>WAPE90 consenso</th><th>WAPE90 parlamento</th><th>WAPE90 reglas</th></tr>{hr}</table>"
               f"<div class='cs'>Error EAN a EAN en abr–jun (Σ |forecast − real| / Σ real). Cada EAN elige su partido con las urnas de oct–mar (Q2 y Q3 de las fotos que las tienen).</div>"
               f"<div class='box' style='margin-top:3mm'><div class='ct'>Error EAN a EAN en abr–jun según lo lejos que estaba la foto</div>"
               f"<div class='lg2'><span><i style='background:{iv.CONS}'></i>Consenso</span><span><i style='background:{INK}'></i>Parlamento (cada EAN su partido)</span></div>"
               + bars([(f"{lg} meses · {nm}", per[f][c]["ean"], col) for f, lg in [("2025-09", "7–9"), ("2025-12", "4–6"), ("2026-03", "1–3")]
                       for c, nm, col in [("cons", "consenso", iv.CONS), ("parl", "parlamento", INK)]], w=620, lab_w=150, maxv=1.0) + "</div>"
               f"<div class='g2' style='margin-top:3mm'><div class='box'><div class='ct'>Qué significa</div><ul class='ul'>"
               f"<li><b>El horizonte manda.</b> A 7–9 meses vista el consenso falla un {pc(p9['cons']['ean'])} EAN a EAN y el parlamento, un {pc(p9['parl']['ean'])}. A 1–3 meses, el consenso baja a {pc(p3['cons']['ean'])}: tiene pedidos e información que el histórico no tiene.</li>"
               f"<li><b>Votar por horizonte no lo arregla.</b> Elegir el partido solo con las urnas a 1–3 meses deja el error en {pc(D['extra_horizonte']['2026-03']['voto_horizonte'])}; "
               f"el mejor partido único a 1–3 meses ({D['extra_horizonte']['2026-03']['mejor_unico'][1]}) se queda en {pc(D['extra_horizonte']['2026-03']['mejor_unico'][0])}.</li>"
               f"<li><b>La regla de la bandera ayuda en todas las fotos:</b> con los DAs futuros al 100% el parlamento empeora ({pc(p9['parl100']['ean'])}, {pc(p12['parl100']['ean'])} y {pc(p3['parl100']['ean'])}).</li>"
               f"<li><b>En el total de la casa</b>, las reglas + DAs siguen siendo la referencia más estable en sep-25 y dic-25.</li></ul></div>"
               f"<div class='box'><div class='ct'>Propuesta</div><ul class='ul'>"
               f"<li><b>Sistema híbrido:</b> meses 1–6 del horizonte, consenso; meses 7–9, el partido de cada EAN. Es donde cada uno ha demostrado ser mejor.</li>"
               f"<li><b>Códigos nuevos:</b> ciclo de vida, y sin DAs futuros si tienen bandera 2.</li>"
               f"<li><b>Base:</b> restar los DAs planificados según su conversión medida (≈50% fragancias, más en makeup).</li>"
               f"<li><b>Guardar los DAs de cada foto</b> al cierre de mes: o9 los borra y sin ellos no se puede limpiar la base.</li>"
               f"<li><b>Siguiente:</b> confirmarlo con más fotos; con una sola urna a 7–9 meses, el resultado lejano descansa en un quarter.</li></ul></div></div>")
    css = vr.CSS + iv.CSS_EXTRA + ir.EXTRA + f"""
.t6 {{ position: relative; width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; margin: 1.6mm 0; }}
.t6 th {{ font-size: 6.2pt; text-transform: uppercase; letter-spacing: .05em; color: {MUTED}; text-align: left; padding: 1.4mm 2mm; border-bottom: 1px solid #E3E7EC; }}
.t6 td {{ font-size: 7.8pt; padding: 1.3mm 2mm; border-bottom: 1px solid #F1F3F5; }}
.t6 td.n {{ text-align: right; font-variant-numeric: tabular-nums; }}
.t6 td .bl {{ display: block; font-size: 6pt; color: {MUTED}; }}
svg.tl .ax {{ font-size: 7.4px; }} svg.tl .ax.b {{ font-weight: 700; fill: {INK2}; }}
svg.tl .ph {{ font-family: Inter; font-size: 8.6px; font-weight: 700; fill: {INK}; }}
svg.tl .dl {{ font-family: Inter; font-size: 8px; font-weight: 700; fill: {INK}; }}
svg.tl .nt2 {{ font-family: Inter; font-size: 7px; fill: {INK2}; }}
svg.tl .nt3 {{ font-family: Inter; font-size: 8px; font-weight: 700; }}
.wt.w6 th {{ font-size: 6.4pt; padding: 1mm 2mm; }} .wt.w6 td {{ font-size: 7.2pt; padding: .8mm 2mm; }} .wt td.sp {{ color: {MUTED}; }}
.wt.w6 td.qq i {{ font-style: normal; color: {MUTED}; font-size: 6pt; margin-left: 1.4mm; }} .wt.w6 td.hh {{ font-size: 7.6pt; }}
.tt1 td .bl {{ display: block; font-size: 6.2pt; color: {MUTED}; }}
.tt1, .wt, .pt {{ position: relative; }}
.c4 .sr span {{ font-size: 5pt; }}
"""
    html = (f"<!doctype html><html><head><meta charset='utf-8'><title>Parlamento de 6</title><style>{css}</style></head><body>"
            f"{p1}{p2}{p3_}{p4}{p5}{p6}{p7}{p8}{p9_}{p10}{p11}{p12_}</body></html>")
    hp = W / "reporte_6_partidos.html"; hp.write_text(html, encoding="utf-8")
    subprocess.run([vr.CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={OUT}", f"file://{hp}"], check=True, capture_output=True)
    print(OUT)
    # Excel por EAN y urna
    X = B.copy()
    v = E.voto.reindex(X.ean).values
    X.insert(1, "voto", v)
    keep = ["ean", "voto", "foto", "q", "cat", "casa", "linea", "seg", "tramo", "fase", "isf", "desc", "real", "cons", "da"] + ["F:" + n for n in P.names]
    X = X[keep].rename(columns={"F:" + n: n for n in P.names} | dict(ean="EAN", voto="Vota a", foto="Foto", q="Quarter", cat="Categoría", casa="Casa", linea="Línea",
                                                                     seg="Segmento", tramo="Tramo edad", fase="Fase", isf="Bandera", desc="Descripción",
                                                                     real="Real", cons="Consenso", da="DAs de la foto"))
    with pd.ExcelWriter(ROOT / "reportes" / "PARTIDOS6_EAN.xlsx") as xw:
        X.sort_values(["Categoría", "Casa", "EAN", "Foto", "Quarter"]).to_excel(xw, sheet_name="EAN x urna", index=False)
        E.reset_index().to_excel(xw, sheet_name="EAN", index=False)


if __name__ == "__main__":
    main()
