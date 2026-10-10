"""Reporte de ideología del parlamento (modelo vigente): el EAN, sus 3 preguntas, los 6 partidos, las brújulas políticas, la coalición y la elección.
Sin consenso (es la salida de o9 que se quiere sustituir). Lee work/six_multi.json/.parquet/_ean.parquet (CICLO_MODE=uno),
work/six_sin_consenso.json, work/ideo_brujulas6.json y work/ideo_brujulas6_ean.parquet.
Salida: reportes/REPORTE_IDEOLOGIA.pdf"""
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
import six_multi as sm  # noqa
import six_report as sr  # noqa
import votes_report as vr  # noqa

ROOT = Path(__file__).resolve().parents[1]; W = ROOT / "work"
OUT = ROOT / "reportes" / "REPORTE_IDEOLOGIA.pdf"
INK, INK2, MUTED = iv.INK, iv.INK2, iv.MUTED
pc, n0 = iv.pc, iv.n0
LEMA = {"Regla fragancias": "Lo del año pasado, corregido por cómo va mi tamaño en mi casa",
        "Regla makeup": "Mi nivel de medio año, con medio trend de mi función",
        "Ciclo de vida": "¿Cómo les fue a los otros códigos a mi edad?",
        "Media 6M prudente": "Mi medio año, con la caída de mi categoría",
        "Media 6M estacional": "Mi medio año con la temporada de mi casa y el trend de mi fase",
        "Media 12M estacional": "Mi año entero con la temporada de mi línea y medio trend propio"}
RESP = {  # respuesta de cada partido a las 3 preguntas
    "Regla fragancias": ("Mismo mes del año pasado (temporada propia)", "Su casa × tamaño · trend 12M entero · tope ±30%", "Resta 50% de los DAs planificados · suma 25% de los cortes"),
    "Regla makeup": ("Media de 6 meses, plana", "Su casa × función · mitad del trend 12M · tope ±30%", "Resta 25% de los DAs · suma cortes (máx. 10% del envío)"),
    "Ciclo de vida": ("Nivel de 6 meses · fragancias con la temporada de su casa, makeup plano",
                      "Los que tuvieron su edad (fragancias: toda la categoría; makeup: su línea) hasta 17 meses · después, el trend 12M de su fase (±30%)",
                      "Base tal cual (los DAs de lanzamiento se repiten)"),
    "Media 6M prudente": ("Media de 6 meses, plana", "Su categoría · trend 6M entero · tope ±60%", "Resta 50% de los DAs planificados"),
    "Media 6M estacional": ("Media de 6 meses × perfil mensual de su casa", "Su fase (crecimiento / estable / declive) · trend 12M entero · tope ±60%", "Suma 25% de los cortes"),
    "Media 12M estacional": ("Media de 12 meses × perfil mensual de su línea", "Él mismo · mitad de su trend 12M · tope ±30%", "Base tal cual")}


def sec(kick, title, body, cls=""):
    return f"<section class='page {cls}'><div class='blob'></div><div class='kick'>{kick}</div><h2>{title}</h2>{body}</section>"


def main():
    D = json.loads((W / "six_multi.json").read_text())
    assert D["names"] == sm.NAMES_UNO, "correr src/six_multi.py con CICLO_MODE=uno"
    S = json.loads((W / "six_sin_consenso.json").read_text())
    Bj = json.loads((W / "ideo_brujulas6.json").read_text())
    B = pd.read_parquet(W / "six_multi.parquet"); E = pd.read_parquet(W / "six_multi_ean.parquet").set_index("ean")
    POS = pd.read_parquet(W / "ideo_brujulas6_ean.parquet")
    P = b6.P6(); T = D["por"]["Total"]["Total"]
    HZ = list(S["error_ean"].keys())                     # columnas: 7–9, 4–6, 1–3 meses
    ee = lambda k: [S["error_ean"][h][k] for h in HZ]
    # ---------------- 1. concepto
    dni = [("ID", "Su historia de envíos, cortes y DAs"), ("Familia", "Categoría → casa → brand → línea"), ("Formato", "Tamaño (fragancias) o función (makeup)"),
           ("Edad", "Meses desde el lanzamiento (2 meses seguidos con envío): 6–11 · 12–17 · 18–25 · 26+"),
           ("Fase", "Desde 18 meses: crecimiento / estable / declive frente a su casa"), ("Gestión", "Ignore System Forecast Flag (0, 1, 2) · Central / Local")]
    dh = "".join(f"<div class='dn'><b>{a}</b><span>{b}</span></div>" for a, b in dni)
    qs = [("1", "¿De dónde parto?", "La base", "Año pasado o nivel reciente (6 o 12 meses); con temporada (propia, de su línea o de su casa) o plano.",
           "La forma de la base cambia el error en 9 de cada 10 EANs. Fragancias tiene temporada (51% de sus EANs acierta más con ella); makeup es casi plano.", "Alta"),
          ("2", "¿A quién sigo?", "El trend", "Yo, mi línea, mi brand, mi tamaño o función, mi casa, mi categoría, mi fase o los de mi edad; y cuánto me lo creo (fuerza y tope).",
           "Con ciclo de vida los nuevos fallan mucho menos; el 51% acierta más con el trend entero. La fuente del trend no se puede juzgar con sep-25: casi todos chocan con el tope de −30%.", "Alta en edad · baja en fuente"),
          ("3", "¿Cómo limpio la base?", "DAs y cortes", "Cuánto resto de los DAs planificados de los meses de la base (leídos de la foto en la que aún eran futuro) y cuánto sumo de cortes.",
           "Solo el 42% del DA planificado de fragancias se convirtió en envío extra (80% en makeup). A 3 de cada 4 EANs les cambia poco.", "Media (DAs) · baja (cortes)")]
    qh = "".join(f"<div class='qc'><div class='qn'>{n}</div><div class='qt'>{t}</div><div class='qs'>{s}</div><p>{o}</p><div class='qf'><b>En qué se sustenta.</b> {f}</div>"
                 f"<div class='qk'>Firmeza: <b>{k}</b></div></div>" for n, t, s, o, f, k in qs)
    p1 = (f"<section class='page'><div class='blob'></div><div class='kick'>Ideología del parlamento · modelo vigente · fotos sep-25, dic-25 y mar-26 → real sep-26</div>"
          f"<h1>Cada EAN es como una persona:<br/><span style='color:{INK2}'>se conoce, mira su pasado y elige su partido.</span></h1>"
          f"<div class='dni'><div class='dnt'>El DNI del EAN</div>{dh}</div><div class='q3'>{qh}</div>"
          f"<div class='g2' style='margin-top:3mm'><div class='box'><div class='ct'>Igual para todos (no es ideología)</div><p class='sm'><b>DAs futuros de la foto:</b> son insight y se suman según la bandera: "
          f"100% sin bandera, 50% con bandera 1, 0% con bandera 2 (ahí el forecast de o9 ya son los DAs). <b>El trend</b> siempre con actuals.</p></div>"
          f"<div class='box'><div class='ct'>Quién elige las respuestas</div><p class='sm'>El EAN mira sus quarters pasados y, en cada uno, vota al partido que menos se equivocó con él. "
          f"Su DNI entra dentro de los partidos (la temporada de <i>su</i> casa, la curva de <i>su</i> edad, el trend de <i>su</i> fase). Sin historia, pregunta a sus parecidos.</p></div></div></section>")
    # ---------------- 2. los 6 partidos
    cards = ""
    smax = max(T["seats"][x] for x in P.names)
    for nm in P.names:
        r1, r2, r3 = RESP[nm]
        se = ee("Solo " + nm)
        cards += (f"<div class='pc' style='--c:{P.col[nm]}'><div class='ph'><div class='pn'>{P.num[nm]}</div><div><div class='pt'>{nm}</div>"
                  f"<div class='pb'>{'Fijo · ' if nm.startswith('Regla') else ''}{P.bloc[nm]}</div></div></div><div class='pl'>«{LEMA[nm]}»</div>"
                  f"<div class='ir'><span>1 · Parto de</span><b>{r1}</b></div><div class='ir'><span>2 · Sigo a</span><b>{r2}</b></div><div class='ir'><span>3 · Limpio</span><b>{r3}</b></div>"
                  f"<div class='pm'><div><span>EANs que lo votan</span><b>{T['seats'][nm]}</b><i style='width:{T['seats'][nm] / smax * 100:.0f}%'></i></div>"
                  f"<div><span>Volumen</span><b>{pc(T['vol'][nm])}</b></div><div><span>Solo, a 7–9 / 4–6 / 1–3 m</span><b class='sm3'>{' / '.join(pc(x) for x in se)}</b></div></div></div>")
    p2 = sec("Los 6 partidos", "Dos reglas fijas, el ciclo de vida y tres partidos de nivel reciente. Cada uno es una combinación de respuestas a las 3 preguntas.",
             f"<div class='cards c3'>{cards}</div><div class='foot'>«Solo» = error EAN a EAN en abr–jun si ese partido se usara para todos los EANs, según lo lejos que estaba la foto "
             f"(sep-25 a 7–9 meses, dic-25 a 4–6, mar-26 a 1–3). Regla de su categoría: {' / '.join(pc(x) for x in ee('Regla de su categoría'))}. "
             f"A todos se les suman los DAs futuros según la bandera.</div>")
    # ---------------- 3. brújulas
    fixed = {k: {nm: tuple(Bj["posiciones"][k][nm]) for nm in Bj["nombres"]} for k in ["c1", "c2", "c3"]}
    fixed["c1"]["Ciclo de vida"] = (0.0, -0.6); fixed["c2"]["Ciclo de vida"] = (0.35, 0.6); fixed["c3"]["Ciclo de vida"] = (-1.0, -1.0)
    pts = POS.join(E[["voto"]])

    def mk(kx, ky):
        out = []
        for e, r in pts.iterrows():
            if r.voto not in P.col or r.voto == "Empate":
                continue
            rng = np.random.default_rng(abs(hash(e)) % 2**32)
            out.append(dict(x=float(np.clip(r[kx] + rng.normal(0, .02), -1.08, 1.08)), y=float(np.clip(r[ky] + rng.normal(0, .02), -1.08, 1.08)), party=r.voto, vol=float(r.real)))
        return out
    specs = [("c1", "1 · ¿De dónde parto?", ("Plana", "Con temporada"), ("Reciente (6M)", "Lejana (12M / año pasado)"),
              ("Planos de memoria larga", "Estacionales de memoria larga", "Planos de lo reciente", "Estacionales de lo reciente")),
             ("c2", "2 · ¿A quién sigo?", ("Individual: EAN, línea", "Colectivo: casa, categoría"), ("Trend suave", "Trend completo"),
              ("Individualistas creyentes", "Colectivistas creyentes", "Individualistas escépticos", "Colectivistas escépticos")),
             ("c3", "3 · ¿Cómo limpio la base?", ("Deja los DAs planificados", "Los resta"), ("No suma cortes", "Suma cortes"),
              ("Suma cortes, deja DAs", "Suma cortes y resta DAs", "Base tal cual", "Solo resta DAs"))]
    comps = "".join(iv.compass(P, mk(k + "x", k + "y"), xl, yl, t, q, w=330, h=420, xlim=(-1.14, 1.14), ylim=(-1.14, 1.14),
                               fixed={nm: (fixed[k][nm][0] * .86, fixed[k][nm][1] * .86) for nm in P.names}) for k, t, xl, yl, q in specs)
    st_ = Bj["stats"]
    notes = [f"<b>¿De dónde parto?</b> Con temporada gana en el {pc(st_['c1x']['der_fr'])} de los EANs de fragancias (plana, {pc(st_['c1x']['izq_fr'])}); makeup se reparte "
             f"({pc(st_['c1x']['der_mu'])} / {pc(st_['c1x']['izq_mu'])}). El ciclo de vida está en medio: con temporada en fragancias y plano en makeup.",
             f"<b>¿A quién sigo?</b> El {pc(st_['c2x']['centro'])} está en el centro: en sep-25 su trend y el de su casa caían igual (tope −30%). El {pc(st_['c2y']['der'])} acierta más creyéndose el trend entero. "
             f"El ciclo de vida sigue a los de su edad o a su fase.",
             f"<b>¿Cómo limpio la base?</b> Al {pc(st_['c3x']['centro'])} le da igual restar o no los DAs planificados y al {pc(st_['c3y']['centro'])} los cortes: son ideas de poco peso."]
    p3 = sec("Brújulas políticas · las 3 preguntas", "Los partidos ocupan rincones distintos de las brújulas: ninguno es casi igual a otro.",
             iv.legend(P, "Círculo con borde = partido por su fórmula · punto = EAN de la foto sep-25 (tamaño = volumen), color = partido al que vota")
             + f"<div class='g3c'>{comps}</div><div class='g3n'>{''.join(f'<div class=nt>{x}</div>' for x in notes)}</div>")
    # ---------------- 4. coalición
    N = sm.NAMES
    Wq = np.stack([np.minimum(sm.wq(B["F:" + n].values, B.real.values), 2) for n in N], 1)
    err = pd.DataFrame(Wq, columns=N); err["ean"] = B.ean.values
    m = err.groupby("ean")[N].mean()
    top2 = np.argsort(m.values, 1)[:, :2]
    pairs = pd.Series([" + ".join(sorted([N[i], N[j]], key=N.index)) for i, j in top2], index=m.index)
    realt = B.groupby("ean").real.sum()
    pt = pd.DataFrame(dict(n=pairs.value_counts(), vol=realt.groupby(pairs).sum() / realt.sum())).sort_values("n", ascending=False).head(8)
    prow = "".join(f"<tr><td>{' + '.join(P.dot(x, num=True) + x for x in k.split(' + '))}</td><td class='n'>{int(r.n)}</td><td class='n'>{pc(r.vol)}</td></tr>" for k, r in pt.iterrows())
    # ejemplo: EAN de fragancias con mucho volumen y las 3 urnas de sep-25
    x9 = B[(B.foto == "2025-09") & (B.cat == "Fragancias")]
    cand = x9.groupby("ean").real.sum().sort_values(ascending=False)
    ex = cand.index[min(3, len(cand) - 1)]
    xe = B[(B.ean == ex) & (B.foto == "2025-09")].sort_values("q")
    tr = xe[xe.q.isin(["FY26.Q2", "FY26.Q3"])]
    etr = {n: float(np.mean(np.minimum(sm.wq(tr["F:" + n].values, tr.real.values), 2))) for n in N}
    o2 = sorted(N, key=lambda n: etr[n])[:2]
    q4 = xe[xe.q == "FY26.Q4"].iloc[0]
    erow = "".join(f"<tr class='{'hl' if n in o2 else ''}'><td>{P.dot(n, num=True)}{n}</td>" + "".join(f"<td class='n'>{pc(min(sm.wq(np.array([r['F:' + n]]), np.array([r.real]))[0], 9))}</td>" for _, r in tr.iterrows())
                   + f"<td class='n'>{pc(etr[n])}</td><td class='n'>{n0(q4['F:' + n])}</td></tr>" for n in N)
    coal = (q4["F:" + o2[0]] + q4["F:" + o2[1]]) / 2
    desc = str(E.loc[ex, "desc"]) if "desc" in E.columns else ex
    tab = "".join(f"<tr><td><b>{k}</b></td>" + "".join(f"<td class='n'>{pc(S['error_ean'][h][k])}</td>" for h in HZ) + "</tr>"
                  for k in ["Regla de su categoría", "Parlamento (voto del EAN)", "Media de sus 2 mejores", "Media de los 6 partidos", "Solo Ciclo de vida"])
    tab = tab.replace("Media de sus 2 mejores", "Coalición: media de sus 2 mejores").replace("Parlamento (voto del EAN)", "Un partido: el que más votó")
    w9 = S["wape90"]
    wt = "".join(f"<tr><td><b>{lab}</b></td>" + "".join(f"<td class='n'>{pc(w9[k][h]['wape90'])} <i>({'+' if w9[k][h]['sesgo'] > 0 else '−'}{pc(abs(w9[k][h]['sesgo']))})</i></td>" for h in ["7–9", "4–6", "1–3"]) + "</tr>"
                 for k, lab in [("regla", "Regla de su categoría"), ("parlamento", "Un partido"), ("coalición 2", "Coalición de 2")])
    p4 = sec("La coalición", "Gobierno de coalición: el forecast del EAN es la media de los 2 partidos que mejor le acertaron. Es la forma más estable de usar el parlamento.",
             f"<div class='g3b'><div class='box'><div class='ct'>Cómo funciona</div><ul class='ul'>"
             f"<li>Cada EAN mira sus quarters pasados y mide el error de cada partido en cada uno.</li>"
             f"<li><b>Un partido:</b> se queda con el que gana más quarters. Si se equivoca de partido, se equivoca del todo.</li>"
             f"<li><b>Coalición:</b> se queda con los 2 de menor error medio y usa la media de los dos forecasts. Si uno falla, el otro amortigua.</li>"
             f"<li>No necesita el consenso ni ningún dato nuevo: los mismos 6 partidos, solo cambia cómo se combinan.</li></ul>"
             f"<div class='ct' style='margin-top:2.4mm'>Coaliciones más frecuentes</div><table class='t6 s'><tr><th>Coalición</th><th>EANs</th><th>Volumen</th></tr>{prow}</table></div>"
             f"<div class='box'><div class='ct'>Ejemplo: {desc}</div><div class='cs'>EAN {ex} · foto sep-25. Error de cada partido en oct–dic y ene–mar; los 2 mejores forman la coalición.</div>"
             f"<table class='t6 s'><tr><th>Partido</th><th>oct–dic</th><th>ene–mar</th><th>Media</th><th>Forecast abr–jun</th></tr>{erow}</table>"
             f"<p class='sm'>Coalición = media de <b>{o2[0]}</b> y <b>{o2[1]}</b>: <b>{n0(coal)}</b> unidades para abr–jun. Real: <b>{n0(q4.real)}</b> "
             f"(con un solo partido, {o2[0]}: {n0(q4['F:' + o2[0]])}).</p></div>"
             f"<div class='box'><div class='ct'>Prueba honesta: elegir con oct–mar, medir en abr–jun</div><div class='cs'>Error EAN a EAN según lo lejos que estaba la foto</div>"
             f"<table class='t6 s'><tr><th></th><th>7–9 m</th><th>4–6 m</th><th>1–3 m</th></tr>{tab}</table>"
             f"<div class='cs' style='margin-top:2mm'>WAPE90 del total de la casa (sesgo)</div><table class='t6 s'><tr><th></th><th>7–9 m</th><th>4–6 m</th><th>1–3 m</th></tr>{wt}</table>"
             f"<p class='sm'>La coalición nunca es la peor: gana a la regla lejos y a medio plazo, y queda a la par cerca. En el total de la casa iguala o mejora a las reglas.</p></div></div>")
    # ---------------- 5. elección
    po = D["por"]
    items = [("Fragancias", "Burberry, Gucci, Marc Jacobs", po["Categoría"]["Fragancias"]), ("Makeup", "Gucci Make up, Kylie", po["Categoría"]["Makeup"])] + \
            [(f"{k} meses", s, po["Edad"][k]) for k, s in [("6–11", "Recién lanzados"), ("26+", "Maduros")] if k in po["Edad"]]
    def top(d, k):
        return max(P.names, key=lambda x: d[k][x])
    lect = "".join(f"<li><b>{t}:</b> más EANs con <b>{top(d, 'seats')}</b> ({d['seats'][top(d, 'seats')]}); más volumen con <b>{top(d, 'vol')}</b> ({pc(d['vol'][top(d, 'vol')])}).</li>" for t, _, d in items)
    lect += "<li>Ningún partido gana en todos los grupos, y el que gana en EANs no es el que gana en volumen: por eso cada EAN elige el suyo (o forma coalición).</li>"
    p5 = (f"<section class='page'><div class='blob'></div><div class='kick'>La elección · 6 urnas (sep-25 Q2–Q4, dic-25 Q3–Q4, mar-26 Q4) · {T['eans']} EANs</div>"
          f"<h2>Ningún partido tiene mayoría: el más votado se queda con el {pc(max(T['seats'][x] for x in P.names) / T['eans'])} de los EANs. Cada EAN encuentra el suyo.</h2>"
          f"{iv.legend(P)}<div class='el'><div class='box'>{iv.hemicycle(P, T['seats'], w=520, big=True)}<div class='vl'>Volumen real de los EANs que gana cada partido</div>"
          f"{iv.volbar(P, T['vol'], h=6)}{iv.seatrow(P, T)}<ul class='ul' style='margin-top:4mm'>{lect}</ul></div><div class='grid c2x'>{''.join(iv.card(P, t, s, d) for t, s, d in items)}</div></div></section>")
    css = vr.CSS + iv.CSS_EXTRA + ir.EXTRA + __import__("ideo_infografia").CSS + f"""
.dni {{ position: relative; display: grid; grid-template-columns: 22mm repeat(6, 1fr); gap: 2mm; margin-top: 3.4mm; align-items: stretch; }}
.dnt {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 10pt; display: flex; align-items: center; }}
.dn {{ background: #fff; border: 1px solid #E6EAEE; border-radius: 9px; padding: 1.6mm 2.2mm; }}
.dn b {{ display: block; font-size: 8pt; }} .dn span {{ font-size: 6.6pt; color: {INK2}; line-height: 1.3; }}
.q3 {{ position: relative; display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; margin-top: 3.4mm; }}
.qc {{ background: #fff; border: 1px solid #E6EAEE; border-top: 3px solid {INK}; border-radius: 12px; padding: 3mm 3.4mm; }}
.qn {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 20pt; color: {INK2}; line-height: 1; }}
.qt {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 13pt; margin-top: 1mm; }}
.qs {{ font-size: 7pt; text-transform: uppercase; letter-spacing: .08em; color: {MUTED}; margin-bottom: 1.4mm; }}
.qc p {{ font-size: 8pt; line-height: 1.45; color: {INK}; }}
.qf {{ font-size: 7.4pt; line-height: 1.45; color: {INK2}; margin-top: 1.8mm; background: #F6F7F9; border-radius: 8px; padding: 1.6mm 2.2mm; }}
.qk {{ font-size: 7pt; color: {MUTED}; margin-top: 1.4mm; }}
.cards.c3 {{ grid-template-columns: repeat(3, 1fr); gap: 3mm; margin-top: 2mm; }}
.c3 .pt {{ font-size: 11pt; }} .c3 .pl {{ font-size: 8.2pt; min-height: 0; }} .c3 .ir {{ font-size: 6.9pt; grid-template-columns: 15mm 1fr; padding: .8mm 0; }}
.c3 .pm b {{ font-size: 11pt; }} .c3 .pm b.sm3 {{ font-size: 7.6pt; white-space: nowrap; }}
.t6 {{ width: 100%; border-collapse: collapse; background: #fff; margin: 1.4mm 0; }}
.t6 th {{ font-size: 6.2pt; text-transform: uppercase; letter-spacing: .05em; color: {MUTED}; text-align: left; padding: 1.2mm 1.6mm; border-bottom: 1px solid #E3E7EC; }}
.t6 td {{ font-size: 7.4pt; padding: 1mm 1.6mm; border-bottom: 1px solid #F1F3F5; }} .t6 td.n {{ text-align: right; font-variant-numeric: tabular-nums; }}
.t6 td i {{ font-style: normal; color: {MUTED}; font-size: 6.4pt; }} .t6 tr.hl td {{ background: #F1F2F4; font-weight: 700; }}
.el {{ position: relative; display: grid; grid-template-columns: 1fr 1.25fr; gap: 4mm; }}
.grid.c2x {{ grid-template-columns: repeat(2, 1fr); gap: 3mm; }}
.c2x .sr span {{ font-size: 5pt; }}
"""
    html = f"<!doctype html><html><head><meta charset='utf-8'><title>Ideología del parlamento</title><style>{css}</style></head><body>{p1}{p2}{p3}{p4}{p5}</body></html>"
    hp = W / "reporte_ideologia.html"; hp.write_text(html, encoding="utf-8")
    subprocess.run([vr.CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={OUT}", f"file://{hp}"], check=True, capture_output=True)
    print(OUT)


if __name__ == "__main__":
    main()
