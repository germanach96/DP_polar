"""Reporte de ideología del parlamento (modelo vigente): el EAN, sus 3 preguntas, los 6 partidos, las brújulas políticas, la coalición y la elección.
Diseño: los EANs votan con FY25 (foto simulada sep-24), el partido elegido pronostica desde la foto sep-25 y se compara con el real de sep-26.
Sin consenso (es la salida de o9 que se quiere sustituir). Lee work/fy25_eleccion.json/.parquet/_ean.parquet, work/fy25_urnas.parquet,
work/fy25_brujulas.json/_ean.parquet (src/fy25_eleccion.py, src/fy25_brujulas.py) y las posiciones de los partidos de work/ideo_brujulas6.json.
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
    D = json.loads((W / "fy25_eleccion.json").read_text())
    assert D["names"] == sm.NAMES_UNO
    Bj = json.loads((W / "ideo_brujulas6.json").read_text()); BS = json.loads((W / "fy25_brujulas.json").read_text())
    B = pd.read_parquet(W / "fy25_eleccion.parquet"); E = pd.read_parquet(W / "fy25_eleccion_ean.parquet").set_index("ean")
    U = pd.read_parquet(W / "fy25_urnas.parquet")
    POS = pd.read_parquet(W / "fy25_brujulas_ean.parquet")
    P = b6.P6(); T = D["por"]["Total"]["Total"]; HZ = ["7–9", "4–6", "1–3"]; H = D["horizonte"]
    N = sm.NAMES_UNO
    he = lambda c: [H[h][c]["ean"] for h in HZ]
    desc = B.drop_duplicates("ean").set_index("ean").desc
    nsin = D["sin_historia"]; nprue = D["n_prueba"]
    # ---------------- 1. concepto
    dni = [("ID", "Su historia de envíos, cortes y DAs"), ("Familia", "Categoría → casa → brand → línea"), ("Formato", "Tamaño (fragancias) o función (makeup)"),
           ("Edad", "Meses desde el lanzamiento (2 meses seguidos con envío): 6–11 · 12–17 · 18–25 · 26+"),
           ("Fase", "Desde 18 meses: crecimiento / estable / declive frente a su casa"), ("Gestión", "Ignore System Forecast Flag (0, 1, 2) · Central / Local")]
    dh = "".join(f"<div class='dn'><b>{a}</b><span>{b}</span></div>" for a, b in dni)
    qs = [("1", "¿De dónde parto?", "La base", "Año pasado o nivel reciente (6 o 12 meses); con temporada (propia, de su línea o de su casa) o plano.",
           "La forma de la base cambia el error en 9 de cada 10 EANs. Fragancias tiene temporada (51% de sus EANs acierta más con ella); makeup es casi plano.", "Alta"),
          ("2", "¿A quién sigo?", "El trend", "Yo, mi línea, mi brand, mi tamaño o función, mi casa, mi categoría, mi fase o los de mi edad; y cuánto me lo creo (fuerza y tope).",
           f"Con ciclo de vida los nuevos fallan mucho menos. En FY25 el {pc(BS['stats']['c2y']['der'])} de los EANs acertaba más creyéndose el trend entero; "
           f"la fuente (yo o mi casa) le da igual al {pc(BS['stats']['c2x']['centro'])}.", "Alta en edad · baja en fuente"),
          ("3", "¿Cómo limpio la base?", "DAs y cortes", "Cuánto resto de los DAs planificados de los meses de la base (leídos de la foto en la que aún eran futuro) y cuánto sumo de cortes.",
           "Solo el 42% del DA planificado de fragancias se convirtió en envío extra (80% en makeup). A 3 de cada 4 EANs les cambia poco.", "Media (DAs) · baja (cortes)")]
    qh = "".join(f"<div class='qc'><div class='qn'>{n}</div><div class='qt'>{t}</div><div class='qs'>{s_}</div><p>{o}</p><div class='qf'><b>En qué se sustenta.</b> {f}</div>"
                 f"<div class='qk'>Firmeza: <b>{k}</b></div></div>" for n, t, s_, o, f, k in qs)
    steps = [("Vota con FY25", f"Foto simulada en sep-24 (solo histórico hasta ago-24). Cada partido pronostica oct-24 a jun-25 y el EAN vota en 3 urnas: Q2, Q3 y Q4 de FY25. "
              f"Votan {D['n_votantes_fy25']} EANs Central."),
             ("Pronostica desde sep-25", "Con la foto sep-25 tal cual (DAs de la base y DAs futuros según la bandera), el partido elegido pronostica los 9 meses: oct-25 a jun-26."),
             ("Se compara con sep-26", "El real de la foto sep-26: Q2 FY26 está a 1–3 meses de la foto, Q3 a 4–6 y Q4 a 7–9. Sin consenso: las referencias son las reglas y los partidos."),
             ("Sin historia: sus parecidos", f"{nsin} de los {nprue} EANs de sep-25 no tenían FY25. Toman lo que votaron los códigos de su casa × tamaño/función que en sep-24 tenían su edad.")]
    sh = "".join(f"<div class='stp'><div class='sn'>{i + 1}</div><div><b>{t}</b><span>{x}</span></div></div>" for i, (t, x) in enumerate(steps))
    p1 = (f"<section class='page'><div class='blob'></div><div class='kick'>Ideología del parlamento · modelo vigente · voto con FY25 → prueba foto sep-25 → real sep-26</div>"
          f"<h1>Cada EAN es como una persona:<br/><span style='color:{INK2}'>se conoce, mira su año pasado y elige su partido.</span></h1>"
          f"<div class='dni'><div class='dnt'>El DNI del EAN</div>{dh}</div><div class='q3'>{qh}</div>"
          f"<div class='steps'>{sh}</div>"
          f"<div class='g2' style='margin-top:3mm'><div class='box'><div class='ct'>Igual para todos (no es ideología)</div><p class='sm'><b>DAs futuros de la foto:</b> son insight y se suman según la bandera: "
          f"100% sin bandera, 50% con bandera 1, 0% con bandera 2 (ahí el forecast de o9 ya son los DAs). <b>El trend</b> siempre con actuals.</p></div>"
          f"<div class='box'><div class='ct'>Quién elige las respuestas</div><p class='sm'>En cada quarter de FY25 el EAN vota al partido que menos se equivocó con él; gana el más votado "
          f"(empate: menor error sumado). Su DNI entra dentro de los partidos (la temporada de <i>su</i> casa, la curva de <i>su</i> edad, el trend de <i>su</i> fase).</p></div></div></section>")
    # ---------------- 2. los 6 partidos
    cards = ""
    smax = max(T["seats"][x] for x in P.names)
    for nm in P.names:
        r1, r2, r3 = RESP[nm]
        se = he("F:" + nm)
        cards += (f"<div class='pc' style='--c:{P.col[nm]}'><div class='ph'><div class='pn'>{P.num[nm]}</div><div><div class='pt'>{nm}</div>"
                  f"<div class='pb'>{'Fijo · ' if nm.startswith('Regla') else ''}{P.bloc[nm]}</div></div></div><div class='pl'>«{LEMA[nm]}»</div>"
                  f"<div class='ir'><span>1 · Parto de</span><b>{r1}</b></div><div class='ir'><span>2 · Sigo a</span><b>{r2}</b></div><div class='ir'><span>3 · Limpio</span><b>{r3}</b></div>"
                  f"<div class='pm'><div><span>EANs que lo eligen</span><b>{T['seats'][nm]}</b><i style='width:{T['seats'][nm] / smax * 100:.0f}%'></i></div>"
                  f"<div><span>Volumen</span><b>{pc(T['vol'][nm])}</b></div><div><span>Solo, a 7–9 / 4–6 / 1–3 m</span><b class='sm3'>{' / '.join(pc(x) for x in se)}</b></div></div></div>")
    best = min(N, key=lambda n: H["total"]["F:" + n]["ean"])
    p2 = sec("Los 6 partidos", f"Dos reglas fijas, el ciclo de vida y tres partidos de nivel reciente. Usado solo para todos, el {best} es el que menos falla ({pc(H['total']['F:' + best]['ean'])} contra {pc(H['total']['regla']['ean'])} de la regla).",
             f"<div class='cards c3'>{cards}</div><div class='foot'>«EANs que lo eligen» = EANs de la foto sep-25 que se quedan con ese partido (su voto de FY25 o, sin historia, el de sus parecidos). "
             f"«Solo» = error EAN a EAN desde la foto sep-25 si ese partido se usara para todos: Q4 FY26 (7–9 meses), Q3 (4–6) y Q2 (1–3). "
             f"Regla de su categoría: {' / '.join(pc(x) for x in he('regla'))}. A todos se les suman los DAs futuros según la bandera.</div>")
    # ---------------- 3. brújulas (posición del EAN con lo que vio en FY25)
    fixed = {k: {nm: tuple(Bj["posiciones"][k][nm]) for nm in Bj["nombres"]} for k in ["c1", "c2", "c3"]}
    fixed["c1"]["Ciclo de vida"] = (0.0, -0.6); fixed["c2"]["Ciclo de vida"] = (0.35, 0.6); fixed["c3"]["Ciclo de vida"] = (-1.0, -1.0)
    pts = POS.join(E[["voto"]], how="inner")

    def mk(kx, ky):
        out = []
        for e, r in pts.iterrows():
            if r.voto not in P.col or r.voto == "Empate":
                continue
            rng = np.random.default_rng(int(e[-6:]) if e[-6:].isdigit() else 7)
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
    st_ = BS["stats"]
    notes = [f"<b>¿De dónde parto?</b> En FY25, con temporada gana en el {pc(st_['c1x']['der'])} y plana en el {pc(st_['c1x']['izq'])}; "
             f"lo reciente (6M) gana en el {pc(st_['c1y']['izq'])} y lo lejano en el {pc(st_['c1y']['der'])}. Nadie domina.",
             f"<b>¿A quién sigo?</b> El {pc(st_['c2y']['der'])} acierta más creyéndose el trend entero: FY25 cayó y hacía falta poder bajar hasta un 60%. "
             f"Seguirse a sí mismo o a su casa le da igual al {pc(st_['c2x']['centro'])}.",
             f"<b>¿Cómo limpio la base?</b> En sep-24 no hay DAs guardados (o9 los borra y existen desde ene-25): el eje de DAs no se puede juzgar con FY25. "
             f"Los cortes le dan igual al {pc(st_['c3y']['centro'])}."]
    p3 = sec("Brújulas políticas · las 3 preguntas · lo que vio cada EAN en FY25", "Los partidos ocupan rincones distintos; los EANs se reparten por todas las brújulas, sin un rincón ganador.",
             iv.legend(P, f"Círculo con borde = partido por su fórmula · punto = EAN con historia en FY25 (tamaño = volumen FY26), color = partido que elige · {BS['n']} EANs")
             + f"<div class='g3c'>{comps}</div><div class='g3n'>{''.join(f'<div class=nt>{x}</div>' for x in notes)}</div>")
    # ---------------- 4. coalición
    pt = pd.DataFrame(D["coaliciones"]).head(8)
    prow = "".join(f"<tr><td>{' + '.join(P.dot(x, num=True) + x for x in r.par.split(' + '))}</td><td class='n'>{int(r.eans)}</td><td class='n'>{pc(r.vol)}</td></tr>" for r in pt.itertuples())
    # ejemplo: 4.º EAN de fragancias con más volumen FY26 entre los que votaron en FY25
    cand = E[(E.cat == "Fragancias") & (E.historia == "Con historia FY25")].real.sort_values(ascending=False)
    ex = cand.index[3]
    tr = U[U.ean == ex].sort_values("q")
    etr = {n: float(np.mean(np.minimum(sm.wq(tr["F:" + n].values, tr.real.values), 2))) for n in N}
    o2 = sorted(N, key=lambda n: etr[n])[:2]
    xe = B[B.ean == ex]; f26 = {n: float(xe["F:" + n].sum()) for n in N}; r26 = float(xe.real.sum())
    erow = "".join(f"<tr class='{'hl' if n in o2 else ''}'><td>{P.dot(n, num=True)}{n}</td>" + "".join(f"<td class='n'>{pc(min(sm.wq(np.array([r['F:' + n]]), np.array([r.real]))[0], 9))}</td>" for _, r in tr.iterrows())
                   + f"<td class='n'>{pc(etr[n])}</td><td class='n'>{n0(f26[n])}</td></tr>" for n in N)
    coal = (f26[o2[0]] + f26[o2[1]]) / 2
    win = E.loc[ex, "voto"]
    p4 = sec("La coalición", "Gobierno de coalición: el forecast del EAN es la media de los 2 partidos que menos fallaron con él en FY25. Si uno se equivoca, el otro amortigua.",
             f"<div class='g3'><div class='box'><div class='ct'>Cómo funciona</div><ul class='ul'>"
             f"<li>Con la foto simulada de sep-24, cada partido pronostica Q2, Q3 y Q4 de FY25 y se mide su error con el EAN en cada quarter.</li>"
             f"<li><b>Un partido:</b> el EAN se queda con el que gana más quarters. Si se equivoca de partido, se equivoca del todo.</li>"
             f"<li><b>Coalición:</b> se queda con los 2 de menor error medio y usa la media de sus dos forecasts.</li>"
             f"<li>Sin historia en FY25: errores medios de sus parecidos (casa × tamaño/función con su edad).</li></ul>"
             f"<div class='ct' style='margin-top:2.4mm'>Coaliciones más frecuentes</div><table class='t6 s'><tr><th>Coalición</th><th>EANs</th><th>Volumen</th></tr>{prow}</table></div>"
             f"<div class='box'><div class='ct'>Ejemplo: {desc.get(ex, ex)}</div><div class='cs'>EAN {ex}. Error de cada partido en los quarters de FY25 (foto simulada sep-24); "
             f"los 2 de menor error medio forman la coalición. Forecast = oct-25 a jun-26 desde la foto sep-25.</div>"
             f"<table class='t6 s'><tr><th>Partido</th><th>Q2 FY25</th><th>Q3</th><th>Q4</th><th>Media</th><th>Forecast FY26</th></tr>{erow}</table>"
             f"<p class='sm'>Coalición = media de <b>{o2[0]}</b> y <b>{o2[1]}</b>: <b>{n0(coal)}</b> unidades para oct-25 a jun-26. Real: <b>{n0(r26)}</b> "
             f"(con un solo partido, {win}: {n0(f26[win]) if win in f26 else '—'}).</p></div>"
             f"<div class='box'><div class='ct'>Qué consigue (desde la foto sep-25)</div><div class='cs'>Error EAN a EAN según lo lejos que estaba la foto</div>"
             f"<table class='t6 s'><tr><th></th>{''.join(f'<th>{h} m</th>' for h in HZ)}<th>Total</th></tr>"
             + "".join(f"<tr class='{'hl' if c == 'coalicion' else ''}'><td><b>{lab}</b></td>" + "".join(f"<td class='n'>{pc(H[h][c]['ean'])}</td>" for h in HZ + ['total']) + "</tr>"
                       for c, lab in [("regla", "Regla de su categoría"), ("un_partido", "Un partido (su voto)"), ("coalicion", "Coalición de 2")])
             + f"</table><p class='sm'>La coalición falla menos que el voto de un solo partido en todos los plazos ({pc(H['total']['coalicion']['ean'])} contra {pc(H['total']['un_partido']['ean'])}) "
             f"y algo menos que la regla ({pc(H['total']['regla']['ean'])}). Pero arrastra el pesimismo de FY25: en el total de la casa queda por debajo del real "
             f"(sesgo {pc(H['total']['coalicion']['sesgo'])}) y su WAPE90 ({pc(H['total']['coalicion']['wape90'])}) es peor que el de la regla ({pc(H['total']['regla']['wape90'])}).</p></div></div>")
    # ---------------- 5. la prueba honesta
    rows5 = [("regla", "Regla de su categoría"), ("un_partido", "Un partido (su voto FY25)"), ("coalicion", "Coalición de 2"), ("media6", "Media de los 6")] + [("F:" + n, "Solo " + n) for n in N]
    bestc = min([c for c, _ in rows5], key=lambda c: H["total"][c]["ean"])
    t5 = "".join(f"<tr class='{'hl' if c in ('media6', 'F:Ciclo de vida') else ''}'><td>{P.dot(c[2:], num=True) if c.startswith('F:') else ''}<b>{lab}</b></td>"
                 + "".join(f"<td class='n'>{pc(H[h][c]['ean'])}</td>" for h in HZ + ["total"]) + f"<td class='n'>{pc(H['total'][c]['wape90'])} <i>({'+' if H['total'][c]['sesgo'] > 0 else '−'}{pc(abs(H['total'][c]['sesgo']))})</i></td></tr>"
                 for c, lab in rows5)
    hs = D["historia"]; kh = list(hs)
    th = "".join(f"<tr><td><b>{lab}</b></td>" + "".join(f"<td class='n'>{pc(hs[k]['total'][c])}</td>" for k in kh) + "</tr>"
                 for c, lab in [("regla", "Regla de su categoría"), ("un_partido", "Un partido"), ("coalicion", "Coalición de 2"), ("media6", "Media de los 6")])
    sg = D["sesgo_fy25"]; pe = D["persistencia"]
    sgb = "".join(f"<div class='sgr'><span>{P.dot(n, num=True)}{n}</span><i class='bar' style='width:{min(sg[n], 1.2) / 1.2 * 100:.0f}%;background:{P.col[n]}'></i><b>+{pc(sg[n])}</b></div>" for n in N)
    p5 = sec("La prueba honesta · voto con FY25, forecast desde sep-25, real sep-26",
             f"Elegir con FY25 no mejora a la regla: el ganador de FY25 repite en FY26 en el {pc(pe['igual'])} de los EANs, casi lo mismo que al azar ({pc(pe['azar'])}).",
             f"<div class='g2w'><div class='box'><div class='ct'>Error EAN a EAN y WAPE90 de la casa</div><div class='cs'>Foto sep-25 contra el real de sep-26 · resaltado: las dos mejores opciones</div>"
             f"<table class='t6 s'><tr><th></th>{''.join(f'<th>{h} m</th>' for h in HZ)}<th>Total</th><th>WAPE90 (sesgo)</th></tr>{t5}</table>"
             f"<p class='sm'>Lo que más acierta no es elegir, sino promediar: la <b>media de los 6 partidos</b> falla {pc(H['total']['media6']['ean'])} EAN a EAN y {pc(H['total']['media6']['wape90'])} en la casa, "
             f"y el <b>Ciclo de vida</b> solo, {pc(H['total']['F:Ciclo de vida']['ean'])}; la regla, {pc(H['total']['regla']['ean'])} y {pc(H['total']['regla']['wape90'])}.</p>"
             f"<div class='ct' style='margin-top:2.4mm'>Qué nos dice</div><ul class='ul'>"
             f"<li>EAN a EAN, la media de los 6 iguala a la regla a 7–9 meses ({pc(H['7–9']['media6']['ean'])} contra {pc(H['7–9']['regla']['ean'])}) y la mejora a 4–6 y 1–3 "
             f"({pc(H['4–6']['media6']['ean'])} y {pc(H['1–3']['media6']['ean'])} contra {pc(H['4–6']['regla']['ean'])} y {pc(H['1–3']['regla']['ean'])}).</li>"
             f"<li>Los partidos sirven, pero un solo año de voto no basta para elegir por EAN: el ganador cambia con el mercado.</li>"
             f"<li>Con un año de voto, la coalición es la forma de elegir que menos falla EAN a EAN, pero hereda el sesgo del año de voto.</li></ul></div>"
             f"<div><div class='box'><div class='ct'>Por qué el voto de FY25 acierta poco</div><div class='cs'>Sobrepronóstico de cada partido en FY25 desde la foto simulada sep-24</div>{sgb}"
             f"<p class='sm'>FY25 fue un año de caída para los códigos que ya existían: todos los partidos se pasaron entre un {pc(min(sg.values()))} y un {pc(max(sg.values()))}. "
             f"El voto premió al menos optimista, no al que mejor entiende al EAN. En FY26 los partidos acertaron mejor el nivel (regla {pc(abs(H['total']['regla']['sesgo']))} por debajo) "
             f"y el pesimismo premiado se paga: Media 6M prudente queda un {pc(abs(H['total']['F:Media 6M prudente']['sesgo']))} por debajo del real.</p></div>"
             f"<div class='box' style='margin-top:3mm'><div class='ct'>Con y sin historia en FY25</div><table class='t6 s'><tr><th></th>{''.join(f'<th>{k}</th>' for k in kh)}</tr>{th}</table>"
             f"<p class='sm'>Sin historia (nuevos) todo falla mucho; ahí la coalición de lo que votaron sus parecidos es la mejor opción.</p></div></div></div>")
    # ---------------- 6. elección
    po = D["por"]
    items = [("Fragancias", "Burberry, Gucci, Marc Jacobs", po["Categoría"]["Fragancias"]), ("Makeup", "Gucci Make up, Kylie", po["Categoría"]["Makeup"])] + \
            [(f"{k} meses", s_, po["Edad"][k]) for k, s_ in [("6–11", "Recién lanzados"), ("26+", "Maduros")] if k in po["Edad"]]

    def top(d, k):
        return max(P.names, key=lambda x: d[k][x])
    lect = "".join(f"<li><b>{t}:</b> más EANs con <b>{top(d, 'seats')}</b> ({d['seats'][top(d, 'seats')]}); más volumen con <b>{top(d, 'vol')}</b> ({pc(d['vol'][top(d, 'vol')])}).</li>" for t, _, d in items)
    lect += f"<li>{T['eans'] - nsin} EANs eligen con su propio FY25 y {nsin} con el de sus parecidos. Empate (se queda la regla): {T['seats']['Empate']}.</li>"
    p6 = (f"<section class='page'><div class='blob'></div><div class='kick'>La elección · 3 urnas por EAN (Q2, Q3 y Q4 de FY25) · {T['eans']} EANs de la foto sep-25</div>"
          f"<h2>Ningún partido tiene mayoría: el más elegido se queda con el {pc(max(T['seats'][x] for x in P.names) / T['eans'])} de los EANs.</h2>"
          f"{iv.legend(P)}<div class='el'><div class='box'>{iv.hemicycle(P, T['seats'], w=520, big=True)}<div class='vl'>Volumen real FY26 (oct–jun) de los EANs que elige cada partido</div>"
          f"{iv.volbar(P, T['vol'], h=6)}{iv.seatrow(P, T)}<ul class='ul' style='margin-top:4mm'>{lect}</ul></div><div class='grid c2x'>{''.join(iv.card(P, t, s_, d) for t, s_, d in items)}</div></div></section>")
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
.steps {{ position: relative; display: grid; grid-template-columns: repeat(4, 1fr); gap: 2.4mm; margin-top: 3mm; }}
.stp {{ display: flex; gap: 2mm; background: #fff; border: 1px solid #E6EAEE; border-radius: 9px; padding: 1.8mm 2.4mm; }}
.stp .sn {{ flex: none; width: 5.4mm; height: 5.4mm; border-radius: 50%; background: {INK}; color: #fff; font-size: 7.4pt; font-weight: 700; display: flex; align-items: center; justify-content: center; }}
.stp b {{ display: block; font-size: 8pt; margin-bottom: .4mm; }} .stp span {{ font-size: 6.8pt; line-height: 1.38; color: {INK2}; }}
.g2w {{ position: relative; display: grid; grid-template-columns: 1.35fr 1fr; gap: 3.4mm; }}
.sgr {{ display: grid; grid-template-columns: 46mm 1fr 11mm; white-space: nowrap; align-items: center; gap: 2mm; font-size: 7.2pt; margin: 1.1mm 0; }}
.sgr span {{ display: flex; align-items: center; gap: 1.2mm; }} .sgr i.bar {{ display: block; height: 3.2mm; border-radius: 2px; }} .sgr b {{ text-align: right; font-variant-numeric: tabular-nums; }}
.grid.c2x {{ grid-template-columns: repeat(2, 1fr); gap: 3mm; }}
.c2x .sr span {{ font-size: 5pt; }}
"""
    html = f"<!doctype html><html><head><meta charset='utf-8'><title>Ideología del parlamento</title><style>{css}</style></head><body>{p1}{p2}{p3}{p4}{p5}{p6}</body></html>"
    hp = W / "reporte_ideologia.html"; hp.write_text(html, encoding="utf-8")
    subprocess.run([vr.CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={OUT}", f"file://{hp}"], check=True, capture_output=True)
    print(OUT)


if __name__ == "__main__":
    main()
