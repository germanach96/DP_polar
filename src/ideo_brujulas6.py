"""Brújulas de las 3 preguntas para el parlamento de 6 (foto sep-25 → real sep-26).

Decisión del usuario: los DAs futuros de la foto se suman SIEMPRE al 100% (no son ideología). Lo que sí es ideología:
qué hacer en la base con los DAs que ya existían en la foto de sep-25 (meses pasados) y con los cortes.
Las 3 preguntas de cada código y sus brújulas:
  1 ¿De dónde parto?   x: plana ↔ con temporada · y: memoria reciente (6M) ↔ lejana (12M / año pasado)
  2 ¿A quién sigo?     x: individual (EAN, línea) ↔ colectivo (casa, categoría) · y: trend suave ↔ completo
  3 ¿Cómo limpio la base? x: deja los DAs pasados ↔ los resta · y: no suma cortes ↔ suma cortes
Partidos: los 6 fijados (src/ideo_six_fijo.py) con DAs futuros al 100%; para los 4 nuevos se vuelve a elegir con datos
(oct–mar) cuánto restan de DAs pasados y cuánto suman de cortes, ahora que todos suman los DAs futuros.
Puntos: cada EAN donde le lleva su ventaja (misma lógica que src/ideo_compass.py, solo con estrategias sin 3M y DAs futuros al 100%),
del color del partido al que vota (elección con el formato fijo, Q2–Q4). Círculo grande con número = posición del partido por su fórmula.
Salida: reportes/BRUJULAS_6_PARTIDOS.pdf y work/ideo_brujulas6.json"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_parties as ipp  # noqa
import ideo_six as s6  # noqa
import ideo_viz as iv  # noqa
import ideo_vs_cons as ivc  # noqa
import votes_report as vr  # noqa

W = ipp.W; ROOT = W.parent
OUT = ROOT / "reportes" / "BRUJULAS_6_PARTIDOS.pdf"
NAMES = ["Regla fragancias", "Regla makeup", "Ciclo de vida", "Media 6M prudente", "Media 6M estacional", "Media 12M estacional"]
KEY = ["base", "estac", "fuente", "tventana", "fuerza", "tope", "dap", "cortes", "daf", "pool"]
INK, INK2, MUTED = iv.INK, iv.INK2, iv.MUTED
pc = iv.pc
IDENT = {"EAN": -1.0, "línea": -0.65, "franquicia": -0.35, "segmento": -0.05, "fase": 0.2, "edad": 0.35, "casa": 0.65, "categoría": 1.0}
CUTX = {"0": -1.0, "10%·tope": -0.6, "25%": 0.0, "50%": 1.0}
MEMY = {"M6": -0.6, "M6e": -0.6, "CV": -0.6, "M12": 0.4, "M12e": 0.4, "LY+M6e": 0.2, "LY": 1.0}


def variants(st, i, daps=None, cuts=None):
    """Misma estrategia con DAs futuros al 100% y cada combinación de DAs pasados × cortes."""
    idx = {tuple(r): k for k, r in zip(st.id.values, st[KEY].astype(str).itertuples(index=False))}
    r = st.loc[i, KEY].astype(str).to_dict(); r["daf"] = "1.0"
    out = []
    for d in (daps or ["0.0", "0.25", "0.5", "0.75", "1.0"]):
        for c in (cuts or ["0", "10%·tope", "25%", "50%"]):
            out.append(idx[tuple({**r, "dap": d, "cortes": c}[k] for k in KEY)])
    return out


def position(r):
    """Coordenadas del partido en las 3 brújulas a partir de su fórmula."""
    b = r["base"]
    seas = 1.0 if b == "LY" else (0.8 if (b.endswith("e") or b == "LY+M6e") else -0.8)
    fuente = "edad" if b == "CV" else r["fuente"]
    fe = 0.6 if b == "CV" else (2 * min(r["fuerza"] * r["tope"] / 0.6, 1) - 1)
    return dict(c1=(seas, MEMY[b]), c2=(IDENT[fuente], fe), c3=(2 * float(r["dap"]) - 1, CUTX[r["cortes"]]))


class P6(iv.Parties):
    def __init__(self, st, ids):
        D = {"partidos": [dict(nombre=n, base=st.loc[i, "base"]) for n, i in zip(NAMES, ids)]}
        super().__init__(D)

    def short(self, n):
        return n


def main():
    st, FQ, Aq, a = ipp.load()
    cons = np.stack(a.cons_q.values); cat = a.cat.values; n = np.arange(len(a))
    old = json.loads((W / "ideo_six_fijo.json").read_text())["ids"]
    # ---- 1. DAs futuros al 100% para todos; los 4 nuevos vuelven a elegir DAs pasados y cortes (con oct–mar)
    ids = [ivc.with_da(st, [i])[0] for i in old]
    r23 = Aq[:, :2].sum(1); c = np.where(r23 > 0)[0]
    w = 0.5 / len(c) + 0.5 * r23[c] / r23[c].sum()
    sc = lambda rows: np.minimum(np.abs(FQ[rows][:, c][:, :, :2] - Aq[None, c][:, :, :2]).sum(2) / r23[c][None], ipp.CAPSCORE)
    V = {j: variants(st, old[j]) for j in range(2, 6)}
    S = {j: sc(V[j]) for j in V}
    Sfix = sc(ids)
    cx = ipp.complexity(st)
    for _ in range(10):
        ch = False
        for j in V:
            rest = np.delete(Sfix, j, 0).min(0)
            tot = (np.minimum(rest[None], S[j]) * w[None]).sum(1)
            near = np.where(tot <= tot.min() + ipp.SIMPLE_TOL)[0]
            k = near[np.lexsort((tot[near], cx[np.array(V[j])][near]))[0]]
            if V[j][k] != ids[j]:
                ids[j] = V[j][k]; Sfix[j] = S[j][k]; ch = True
        if not ch:
            break
    rows = st.loc[ids]
    print("Partidos con DAs futuros al 100%:")
    for nm, i in zip(NAMES, ids):
        print(f"  {nm}: {ipp.describe(st.loc[i])}")
    # ---- 2. prueba limpia (voto con oct–mar, medida abr–jun) y elección completa (Q2–Q4) para los colores
    P = FQ[ids]
    v23 = ivc.vote(P, Aq, [0, 1]); v23 = np.where(v23 < 0, np.where(cat == "Fragancias", 0, 1), v23)
    test = dict(s6.evaluate(a, P[v23, n], Aq, cons, 2))
    for t in s6.TRAMOS:
        test["ean_" + t] = s6.evaluate(a, P[v23, n], Aq, cons, 2, a.tramo.values == t)["ean"]
    Pold = FQ[old]
    vo = ivc.vote(Pold, Aq, [0, 1]); vo = np.where(vo < 0, np.where(cat == "Fragancias", 0, 1), vo)
    test_old = s6.evaluate(a, Pold[vo, n], Aq, cons, 2)
    for t in s6.TRAMOS:
        test_old["ean_" + t] = s6.evaluate(a, Pold[vo, n], Aq, cons, 2, a.tramo.values == t)["ean"]
    rule = np.where((cat == "Fragancias")[:, None], FQ[ids[0]], FQ[ids[1]])
    refs = dict(reglas=s6.evaluate(a, rule, Aq, cons, 2), consenso=s6.evaluate(a, cons, Aq, cons, 2))
    el = ipp.election(P, Aq, NAMES)
    a["voto6"] = el["final"]
    T = ipp.tally(a.voto6.values, a.real.values, NAMES)
    print("prueba limpia abr–jun:", {k: round(x, 3) for k, x in test.items()}, "| antes (sin DAs futuros en los nuevos):",
          {k: round(x, 3) for k, x in test_old.items()}, "| refs", refs)
    print("escaños:", T["seats"], {k: round(x, 3) for k, x in T["vol"].items()})
    # ---- 3. posiciones de los EANs (ventaja con cada lado, estrategias sin 3M y con DAs futuros al 100%)
    real = Aq.sum(1); cols = np.where(real > 0)[0]
    ok = (st.daf.values == 1.0) & ~st.base.isin(["M3", "M3e"]).values & (st.tventana.values != 3)
    rows_ok = np.where(ok)[0]
    Sc = np.empty((len(rows_ok), len(cols)), np.float32)
    for k in range(0, len(rows_ok), 20000):
        rr = rows_ok[k:k + 20000]
        Sc[k:k + 20000] = np.minimum(np.abs(FQ[rr][:, cols] - Aq[None, cols]).sum(2) / real[cols][None], ipp.CAPSCORE)
    sub = st.iloc[rows_ok]
    b = sub.base.values; f = sub.fuente.values; fz = sub.fuerza.values; es = sub.estac.values
    axes = {"c1x": (np.isin(b, ["M6", "M12"]), np.isin(b, ["M6e", "M12e"]) & (es == "casa")),
            "c1y": (np.isin(b, ["M6"]) | (np.isin(b, ["M6e"]) & (es == "casa")), np.isin(b, ["M12"]) | (np.isin(b, ["M12e"]) & (es == "casa"))),
            "c2x": (np.isin(f, ["EAN", "línea"]), np.isin(f, ["casa", "categoría"])),
            "c2y": (((f == "ninguna") & (b != "CV")) | ((f != "ninguna") & (fz <= 0.25)), (f != "ninguna") & (fz >= 0.75)),
            "c3x": (sub.dap.values == 0, sub.dap.values == 1),
            "c3y": (sub.cortes.values == "0", sub.cortes.values == "50%")}
    pos = pd.DataFrame(index=a.index[cols])
    for k_, (L, R) in axes.items():
        pos[k_] = np.tanh((Sc[L].min(0) - Sc[R].min(0)) / 0.05)
    del Sc
    pos = pos.join(a[["voto6", "real", "cat", "tramo"]])
    share = lambda col, side, g=pos: float(((g[col] > 0.3) if side > 0 else (g[col] < -0.3)).mean())
    fr, mu = pos[pos.cat == "Fragancias"], pos[pos.cat == "Makeup"]
    stats = {k_: dict(der=share(k_, 1), izq=share(k_, -1), centro=float((pos[k_].abs() <= 0.3).mean()),
                      der_fr=share(k_, 1, fr), izq_fr=share(k_, -1, fr), der_mu=share(k_, 1, mu), izq_mu=share(k_, -1, mu)) for k_ in axes}
    # ---- 4. PDF
    Pp = P6(st, ids)
    fixed = {nm: position(st.loc[i]) for nm, i in zip(NAMES, ids)}
    pts = lambda kx, ky: [dict(x=float(np.clip(r_[kx] + np.random.default_rng(abs(hash(e)) % 2**32).normal(0, .02), -1.08, 1.08)),
                               y=float(np.clip(r_[ky] + np.random.default_rng(abs(hash(e)) % 2**31).normal(0, .02), -1.08, 1.08)),
                               party=r_.voto6, vol=float(r_.real)) for e, r_ in pos.iterrows() if r_.voto6 in NAMES]
    specs = [("c1", "1 · ¿De dónde parto?", ("Plana", "Con temporada"), ("Memoria reciente (6M)", "Lejana (12M / año pasado)"),
              ("Planos de memoria larga", "Estacionales de memoria larga", "Planos de lo reciente", "Estacionales de lo reciente")),
             ("c2", "2 · ¿A quién sigo?", ("Individual: EAN, línea", "Colectivo: casa, categoría"), ("Trend suave", "Trend completo"),
              ("Individualistas creyentes", "Colectivistas creyentes", "Individualistas escépticos", "Colectivistas escépticos")),
             ("c3", "3 · ¿Cómo limpio la base?", ("Deja los DAs pasados", "Resta los DAs pasados"), ("No suma cortes", "Suma cortes"),
              ("Suma cortes, deja DAs", "Suma cortes y resta DAs", "Base tal cual", "Solo resta DAs"))]
    comps = "".join(iv.compass(Pp, pts(k + "x", k + "y"), xl, yl, t, q, w=330, h=440, xlim=(-1.14, 1.14), ylim=(-1.14, 1.14), fixed={nm: (fixed[nm][k][0] * .86, fixed[nm][k][1] * .86) for nm in NAMES}) for k, t, xl, yl, q in specs)
    notes = [
        f"<b>¿De dónde parto?</b> Con temporada gana en el {pc(stats['c1x']['der_fr'])} de los EANs de fragancias (plana, {pc(stats['c1x']['izq_fr'])}); "
        f"makeup se reparte ({pc(stats['c1x']['der_mu'])} / {pc(stats['c1x']['izq_mu'])}). Memoria: el {pc(stats['c1y']['centro'])} no distingue entre 6 y 12 meses; "
        f"de los que sí, {pc(stats['c1y']['izq'])} prefiere lo reciente y {pc(stats['c1y']['der'])} lo lejano.",
        f"<b>¿A quién sigo?</b> El {pc(stats['c2x']['centro'])} está en el centro: en sep-25 su trend y el de su casa caían igual (tope −30%). "
        f"De los que eligen, {pc(stats['c2x']['izq'])} sigue su propio trend o el de su línea y {pc(stats['c2x']['der'])} el de su casa o categoría. "
        f"El {pc(stats['c2y']['der'])} acierta más creyéndose el trend entero; solo el {pc(stats['c2y']['izq'])} lo suaviza.",
        f"<b>¿Cómo limpio la base?</b> Con los DAs futuros ya sumados para todos, al {pc(stats['c3x']['centro'])} le da igual restar o no los DAs pasados "
        f"({pc(stats['c3x']['der'])} prefiere restarlos, {pc(stats['c3x']['izq'])} dejarlos). Cortes: el {pc(stats['c3y']['centro'])} en el centro."]
    tab = ""
    for nm, i in zip(NAMES, ids):
        r = st.loc[i]; ide = ipp.ideas(r)
        tab += (f"<tr><td>{Pp.dot(nm, num=True)}<b>{nm}</b>{'<span class=fx>fijo</span>' if nm.startswith('Regla') else ''}</td>"
                f"<td>{ide['familia']}{'' if ide['familia'] == ide['memoria'] else ' · ' + ide['memoria']}</td><td>{ide['estac']}</td>"
                f"<td>{ide['fuente']}{'' if ide['trend'] == '—' else ' · ' + ide['trend']}</td><td class='n'>{'0' if ide['dap'] == '0%' else '−' + ide['dap']}</td><td class='n'>{'0' if ide['cortes'] == '0' else '+' + ide['cortes']}</td>"
                f"<td class='n'>{T['seats'][nm]}</td><td class='n'>{pc(T['vol'][nm])}</td></tr>")
    tl = test
    vi = pd.read_pickle(W / "ideo_panel.pkl"); idx = vi["attr"].index.get_indexer(a.index); DAf = vi["DAf"][idx]
    young = (a.tramo == "6–11").values
    dq = [(lab, float(Aq[young, q].sum()), float(DAf[young][:, ix].clip(0).sum()), float(cons[young, q].sum()))
          for q, (lab, ix) in enumerate([("oct–dic", [0, 1, 2]), ("ene–mar", [3, 4, 5]), ("abr–jun", [6, 7, 8])])]
    darow = "".join(f"<tr><td>{l}</td><td class='n'>{iv.n0(r)}</td><td class='n'>{iv.n0(d)}</td><td class='n'>{pc(d / r)}</td><td class='n'>{iv.n0(c_)}</td></tr>" for l, r, d, c_ in dq)
    body1 = (f"<section class='page'><div class='blob'></div><div class='kick'>Parlamento de 6 · DAs futuros de la foto al 100% para todos · foto sep-25 → real sep-26</div>"
             f"<h2>Las 3 preguntas de cada código: de dónde parto, a quién sigo y cómo limpio la base.</h2>"
             f"{iv.legend(Pp, 'Círculo grande con borde = dónde está el partido por su fórmula · punto = EAN (tamaño = volumen) del color del partido al que vota')}"
             f"<div class='g3c'>{comps}</div><div class='g3n'>{''.join(f'<div class=nt>{x}</div>' for x in notes)}</div></section>")
    body2 = (f"<section class='page'><div class='blob'></div><div class='kick'>Los 6 partidos con los DAs futuros fijos</div>"
             f"<h2>Con los DAs futuros sumados para todos, el parlamento de 6 se equivoca un {pc(tl['ean'])} EAN a EAN en abr–jun, "
             f"contra {pc(refs['reglas']['ean'])} de las reglas y {pc(refs['consenso']['ean'])} del consenso.</h2>"
             f"<table class='t6'><tr><th>Partido</th><th>Base</th><th>Temporada</th><th>Trend</th><th>DAs pasados</th><th>Cortes</th><th>EANs</th><th>Volumen</th></tr>{tab}</table>"
             f"<div class='g2'><div class='box'><div class='ct'>Prueba limpia: voto con oct–mar, medida en abr–jun</div><table class='t6 s'>"
             f"<tr><th></th><th>Error EAN</th><th>WAPE90 casa</th><th>6–11 m</th><th>12–17 m</th><th>18–25 m</th><th>26+</th></tr>"
             f"<tr><td><b>Parlamento de 6 + DAs</b></td><td class='n'><b>{pc(tl['ean'])}</b></td><td class='n'>{pc(tl['w90'])}</td>"
             + "".join(f"<td class='n'>{pc(tl['ean_' + t])}</td>" for t in s6.TRAMOS) + "</tr>"
             f"<tr><td>Reglas + DAs</td><td class='n'>{pc(refs['reglas']['ean'])}</td><td class='n'>{pc(refs['reglas']['w90'])}</td>"
             + "".join(f"<td class='n'>{pc(s6.evaluate(a, rule, Aq, cons, 2, a.tramo.values == t)['ean'])}</td>" for t in s6.TRAMOS) + "</tr>"
             f"<tr><td>Consenso</td><td class='n'>{pc(refs['consenso']['ean'])}</td><td class='n'>{pc(refs['consenso']['w90'])}</td>"
             + "".join(f"<td class='n'>{pc(s6.evaluate(a, cons, Aq, cons, 2, a.tramo.values == t)['ean'])}</td>" for t in s6.TRAMOS) + "</tr></table>"
             f"<p class='sm'>Antes, con los 4 partidos nuevos sin DAs futuros: {pc(test_old['ean'])} EAN a EAN y {pc(test_old['w90'])} de WAPE90.</p></div>"
             f"<div class='box'><div class='ct'>Cómo se colocan los partidos</div><p class='sm'><b>Brújula 1:</b> con temporada = año pasado o perfil mensual de un grupo; "
             f"memoria = 6M abajo, 12M arriba, año pasado arriba del todo.</p><p class='sm'><b>Brújula 2:</b> de izquierda a derecha, propio EAN → línea → franquicia → tamaño/función → fase → edad → casa → categoría; "
             f"en vertical, la caída máxima que se cree (fuerza × tope).</p><p class='sm'><b>Brújula 3:</b> % de DAs pasados que resta y % de cortes que suma.</p>"
             f"<p class='sm'><b>Los EANs</b> se colocan por la ventaja de cada lado con la misma flexibilidad a ambos (tanh de la ventaja / 5 puntos): en el centro, les da igual.</p></div></div>"
             f"<div class='box' style='margin-top:4mm'><div class='ct'>Ojo: los DAs futuros en los códigos nuevos</div>"
             f"<div class='g2'><table class='t6 s'><tr><th>EANs de 6–11 meses ({int(young.sum())})</th><th>Real</th><th>DAs+ de la foto</th><th>DAs / real</th><th>Consenso</th></tr>{darow}</table>"
             f"<p class='sm'>En la foto de sep-25, los DAs de los códigos recién lanzados ya superaban su venta real de cada quarter. Sumarlos al 100% lleva el error EAN a EAN de los "
             f"6–11 meses del {pc(test_old['ean_6–11'] if 'ean_6–11' in test_old else 0)} al {pc(tl['ean_6–11'])} y el total del parlamento de {pc(test_old['ean'])} a {pc(tl['ean'])}. "
             f"El consenso, que ya los lleva, también se pasa con los nuevos. Para los maduros (26+) apenas cambia.</p></div></div></section>")
    css = vr.CSS + iv.CSS_EXTRA + __import__("ideo_report").EXTRA + f"""
.t6 {{ position: relative; width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; margin: 2mm 0 4mm; }}
.t6 th {{ font-size: 6.6pt; text-transform: uppercase; letter-spacing: .05em; color: {MUTED}; text-align: left; padding: 1.8mm 2.6mm; border-bottom: 1px solid #E3E7EC; }}
.t6 td {{ font-size: 8.4pt; padding: 2mm 2.6mm; border-bottom: 1px solid #F1F3F5; }}
.t6 td.n {{ text-align: right; font-variant-numeric: tabular-nums; }}
.t6.s td {{ font-size: 8pt; padding: 1.5mm 2.2mm; }}
.fx {{ font-size: 6pt; color: {MUTED}; margin-left: 1.6mm; border: 1px solid #DDE1E6; border-radius: 5px; padding: 0 1mm; }}
"""
    html = f"<!doctype html><html><head><meta charset='utf-8'><title>Brújulas de 6 partidos</title><style>{css}</style></head><body>{body1}{body2}</body></html>"
    hp = W / "brujulas6.html"; hp.write_text(html, encoding="utf-8")
    subprocess.run([vr.CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={OUT}", f"file://{hp}"], check=True, capture_output=True)
    (W / "ideo_brujulas6.json").write_text(json.dumps(dict(ids=[int(i) for i in ids], partidos=[ipp.describe(st.loc[i]) for i in ids],
                                                           prueba=test, antes=test_old, refs=refs, escanos=T, stats=stats,
                                                           posiciones={k: {nm: fixed[nm][k] for nm in NAMES} for k in ["c1", "c2", "c3"]}),
                                                      indent=1, ensure_ascii=False, default=float))
    print(OUT)


if __name__ == "__main__":
    main()
