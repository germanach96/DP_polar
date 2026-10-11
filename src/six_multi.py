"""Parlamento de 7 partidos (6 + el ciclo de vida partido en fragancias y makeup) en todas las fotos con quarters completos, con la lógica de DAs reconstruida.

DAs:
  - Base: cada partido limpia sus meses base con los DAs+ PLANIFICADOS (src/ideo_panel.da_plan: el de la última foto en la que el mes
    aún no estaba cerrado), en el % de su ideología. El trend se calcula con actuals tal cual.
  - Futuro: los DAs de la foto se suman según la Ignore System Forecast Flag de esa foto: sin flag 100%, flag 1 50%, flag 2 0%
    (con flag 2 el consenso es 100% DAs: sumarlos duplica). Variante de control: 100% para todos.
Fotos y urnas (quarters completos; verdad = foto sep-26, sep-26 sin cerrar):
  sep-25 -> Q2, Q3, Q4 FY26 (fragancias y makeup) · dic-25 -> Q3, Q4 (solo fragancias) · mar-26 -> Q4 (fragancias y makeup).
  jun-26 no tiene ningún quarter completo.
Elección (formato fijo): cada EAN vota en cada urna (foto × quarter) al partido con menor WAPE del quarter (si el real es 0, error absoluto);
empates exactos -> vota a todos, hasta 3. Gana el partido con más votos; si empatan, menor WAPE sumado; si no, Empate.
Prueba de persistencia: el EAN elige con las urnas de Q2 y Q3 y se aplica a Q4 de las tres fotos.
Salida: work/six_multi.parquet (EAN × foto × quarter), work/six_multi.json"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_engine as ie  # noqa
import ideo_panel as ip  # noqa
import ideo_parties as ipp  # noqa

W = ie.W
SNAPS = ["2025-09", "2025-12", "2026-03"]
NAMES_DOS = ["Regla fragancias", "Regla makeup", "Ciclo de vida fragancias", "Ciclo de vida makeup", "Media 6M prudente", "Media 6M estacional",
             "Media 12M estacional"]
NAMES_UNO = ["Regla fragancias", "Regla makeup", "Ciclo de vida", "Media 6M prudente", "Media 6M estacional", "Media 12M estacional"]
# Ciclo de vida (src/ciclo_vida.py): fragancias = parecidos de toda su categoría + temporada de su casa; makeup = parecidos de su línea, plano.
# Los dos: base sin restar DAs (los DAs de lanzamiento se repiten como llenado de canal); desde 18 meses, trend 12M de su fase.
import os
CICLO_MODE = os.environ.get("CICLO_MODE", "uno")      # "uno": un partido con receta por tipo · "dos": un partido por tipo
NAMES = NAMES_UNO if CICLO_MODE == "uno" else NAMES_DOS
CICLO = [dict(base="CV", estac="casa", fuente="ninguna", tventana=0, fuerza=0.0, tope=0.0, dap=0.0, cortes="0", daf=1.0, pool="categoría"),
         dict(base="CV", estac="sin", fuente="ninguna", tventana=0, fuerza=0.0, tope=0.0, dap=0.0, cortes="0", daf=1.0, pool="línea")]
FLAGW = {0: 1.0, 1: 0.5, 2: 0.0}
HOUSES = ["Burberry", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"]


def specs():
    st = pd.read_parquet(W / "ideo_strats.parquet")
    ids = json.loads((W / "ideo_brujulas6.json").read_text())["ids"]
    sp = [st.loc[i].to_dict() for i in ids]
    if CICLO_MODE == "uno":
        return sp[:2] + [dict(CICLO[0], pool="por tipo")] + sp[3:]
    return sp[:2] + CICLO + sp[3:]


def forecasts(P, sp):
    """Forecast mensual (n x 9) de cada partido sin DAs futuros, y DAs futuros de la foto."""
    ctx = ie.Ctx(P)
    out = []
    for r in sp:
        X = ie.adjusted(ctx, float(r["dap"]), r["cortes"])
        S = ctx.season(r["estac"]) if r["estac"] != "sin" else None
        if r["base"] == "CV" and r["pool"] == "por tipo":          # receta según el tipo del EAN
            Bf = ie.base_matrix(ctx, X, "CV", ctx.season("casa"), ctx.curve("categoría", "casa"))
            Bm = ie.base_matrix(ctx, X, "CV", None, ctx.curve("línea", None))
            B = np.where((P["attr"].cat.values == "Fragancias")[:, None], Bf, Bm)
            mult = np.ones(len(B))
        elif r["base"] == "CV":
            CV = ctx.curve(r["pool"], None if r["estac"] == "sin" else r["estac"])
            B = ie.base_matrix(ctx, X, "CV", S, CV)
            mult = np.ones(len(B))
        else:
            B = ie.base_matrix(ctx, X, r["base"], S)
            mult = 1 + float(r["fuerza"]) * np.clip(ctx.trend(r["fuente"], int(r["tventana"])), -float(r["tope"]), float(r["tope"])) \
                if r["fuente"] != "ninguna" else np.ones(len(B))
        out.append(np.clip(B * mult[:, None], 0, None))
    return np.stack(out)


def ballots():
    sp = specs()
    recs = []
    for snap in SNAPS:
        P = ip.build(snap, save=False)
        a = P["attr"]; v = a.votante.values
        F0 = forecasts(P, sp)[:, v]                                        # partidos x EAN x 9
        DAf = P["DAf"][v]; flag = a.isf.values[v].astype(int).clip(0, 2)
        wf = np.array([FLAGW[f] for f in flag])[:, None]
        Fflag = np.clip(F0 + wf[None] * DAf[None], 0, None)
        Fall = np.clip(F0 + DAf[None], 0, None)
        A = P["A"][v]; cons = P["cons"][v]
        ok = []
        for q, ix in zip(P["qlist"], P["qidx"]):
            if len(ix) == 3 and P["valid"][ix].all():
                ok.append((q, ix))
        av = a[v]
        for q, ix in ok:
            df = pd.DataFrame(dict(ean=av.index, foto=snap, q=q, cat=av.cat.values, casa=av.casa.values, seg=av.seg.values, linea=av.linea.values,
                                   tramo=av.tramo.values, fase=av.fase.values, isf=flag, desc=av.desc.values,
                                   real=A[:, ix].sum(1), cons=cons[:, ix].sum(1), da=DAf[:, ix].sum(1), da_pos=DAf[:, ix].clip(0).sum(1)))
            for k, nm in enumerate(NAMES):
                df["F:" + nm] = Fflag[k][:, ix].sum(1)
                df["F100:" + nm] = Fall[k][:, ix].sum(1)
            recs.append(df)
        print(f"{snap}: {v.sum()} votantes · urnas {[q for q, _ in ok]}")
    return pd.concat(recs, ignore_index=True)


def wq(f, r):
    e = np.abs(f - r)
    return np.where(r > 0, e / np.where(r > 0, r, 1), e)


def elect(B, pref="F:"):
    """Elección con el formato fijo sobre todas las urnas de B. Devuelve voto por EAN y voto por urna."""
    Wq = np.stack([wq(B[pref + n].values, B.real.values) for n in NAMES], 1)          # urnas x partidos
    best = Wq.min(1, keepdims=True); tie = np.isclose(Wq, best, rtol=1e-9, atol=1e-9)
    nt = tie.sum(1)
    votes = np.where((nt <= 3)[:, None], tie, False).astype(int)
    B = B.assign(**{"v:" + n: votes[:, k] for k, n in enumerate(NAMES)}, **{"w:" + n: Wq[:, k] for k, n in enumerate(NAMES)})
    B["ganador_urna"] = np.where(nt == 1, np.array(NAMES, dtype=object)[Wq.argmin(1)], "Empate")
    g = B.groupby("ean")
    V = g[["v:" + n for n in NAMES]].sum().values; S = g[["w:" + n for n in NAMES]].sum().values
    top = V.max(1, keepdims=True); cand = V == top
    sw = np.where(cand, S, np.inf); bm = sw.min(1, keepdims=True)
    win = cand & np.isclose(sw, bm, rtol=1e-9, atol=1e-9)
    voto = np.where(win.sum(1) == 1, np.array(NAMES, dtype=object)[sw.argmin(1)], "Empate")
    return pd.Series(voto, index=g.size().index), B


def apply_vote(B, voto, pref="F:"):
    v = B.ean.map(voto).fillna("Empate").values
    fb = np.where(B.cat.values == "Fragancias", "Regla fragancias", "Regla makeup")
    v = np.where(v == "Empate", fb, v)
    return np.array([B[pref + p].values[i] for i, p in enumerate(v)]), v


def wape_table(B, cols):
    rows = []
    for (f, q, h), x in B.groupby(["foto", "q", "casa"]):
        R = x.real.sum()
        rows.append(dict(foto=f, q=q, casa=h, real=float(R), **{c: float(abs(x[c].sum() - R) / R) for c in cols},
                         **{"spp3_" + c: float((R - x[c].sum()) / R) for c in cols}))
    return pd.DataFrame(rows)


def main():
    B = ballots()
    B.to_parquet(W / "six_multi.parquet")
    voto, Bv = elect(B)
    B["parl"], B["partido"] = apply_vote(B, voto)
    B["parl100"], _ = apply_vote(B, voto, "F100:")
    B["regla_da"] = np.where(B.cat == "Fragancias", B["F100:Regla fragancias"], B["F100:Regla makeup"])
    cols = ["cons", "parl", "parl100", "regla_da"] + ["F:" + n for n in NAMES]
    w90 = wape_table(B, cols)
    pw = lambda c, x=w90: float((x[c] * x.real).sum() / x.real.sum())
    ean = lambda c, x=B: float(np.abs(x[c] - x.real).sum() / x.real.sum())
    print(f"\nTodas las urnas: WAPE90 consenso {pw('cons'):.1%} · parlamento {pw('parl'):.1%} · parlamento DAs 100% {pw('parl100'):.1%} · reglas + DAs {pw('regla_da'):.1%}")
    print(f"error EAN: consenso {ean('cons'):.1%} · parlamento {ean('parl'):.1%} · DAs 100% {ean('parl100'):.1%} · reglas {ean('regla_da'):.1%}")
    print(f"casa × urna donde gana el parlamento al consenso: {int((w90.parl < w90.cons).sum())}/{len(w90)}")
    # persistencia: votar con Q2 y Q3, aplicar en Q4
    tr = B[B.q.isin(["FY26.Q2", "FY26.Q3"])]
    vt, _ = elect(tr)
    te = B[B.q == "FY26.Q4"].copy()
    te["parl"], te["partido"] = apply_vote(te, vt)
    te["parl100"], _ = apply_vote(te, vt, "F100:")
    w4 = wape_table(te, cols)
    pers = {}
    for f in SNAPS:
        x = te[te.foto == f]; y = w4[w4.foto == f]
        if len(x):
            pers[f] = {c: dict(ean=ean(c, x), w90=pw(c, y)) for c in ["cons", "parl", "parl100", "regla_da"]}
            pers[f]["gana_casas"] = int((y.parl < y.cons).sum()); pers[f]["casas"] = int(len(y))
            pers[f]["tramos"] = {t: {c: ean(c, x[x.tramo == t]) for c in ["cons", "parl", "regla_da"]} for t in ["6–11", "12–17", "18–25", "26+"] if (x.tramo == t).any() and x[x.tramo == t].real.sum() > 0}
            pers[f]["flags"] = {str(k): {c: ean(c, x[x.isf == k]) for c in ["cons", "parl", "parl100", "regla_da"]} for k in [0, 1, 2] if x[x.isf == k].real.sum() > 0}
            print(f"persistencia Q4 {f}: " + " · ".join(f"{c} EAN {pers[f][c]['ean']:.1%} WAPE90 {pers[f][c]['w90']:.1%}" for c in ["cons", "parl", "parl100", "regla_da"]))
    # por horizonte (meses entre la foto y el quarter): con trampa (voto con todas las urnas) y persistencia (voto con Q2+Q3 -> Q4)
    LAG = {("2025-09", "FY26.Q2"): "1–3 meses", ("2025-09", "FY26.Q3"): "4–6 meses", ("2025-09", "FY26.Q4"): "7–9 meses",
           ("2025-12", "FY26.Q3"): "1–3 meses", ("2025-12", "FY26.Q4"): "4–6 meses", ("2026-03", "FY26.Q4"): "1–3 meses"}
    B["lag"] = [LAG[(f, q)] for f, q in zip(B.foto, B.q)]; w90["lag"] = [LAG[(f, q)] for f, q in zip(w90.foto, w90.q)]
    hor = {}
    for lg in ["1–3 meses", "4–6 meses", "7–9 meses"]:
        x = B[B.lag == lg]; y = w90[w90.lag == lg]
        hor[lg] = {c: dict(ean=ean(c, x), w90=pw(c, y)) for c in ["cons", "parl", "regla_da"]}
        hor[lg]["gana"] = int((y.parl < y.cons).sum()); hor[lg]["n"] = int(len(y))
        print(f"horizonte {lg}: " + " · ".join(f"{c} EAN {hor[lg][c]['ean']:.1%} WAPE90 {hor[lg][c]['w90']:.1%}" for c in ["cons", "parl", "regla_da"]) + f" · gana {hor[lg]['gana']}/{hor[lg]['n']}")
    # votar solo con urnas del mismo horizonte y mejor partido único (referencias)
    LAGN = {k: int(v[0]) for k, v in LAG.items()}
    B["lagn"] = [LAGN[(f, q)] for f, q in zip(B.foto, B.q)]
    extra = {}
    for f, lgn in [("2026-03", 1), ("2025-12", 4)]:
        trh = tr[[LAGN[(a_, b_)] == lgn for a_, b_ in zip(tr.foto, tr.q)]]
        vh, _ = elect(trh); x = B[(B.foto == f) & (B.q == "FY26.Q4")].copy()
        x["ph"], _ = apply_vote(x, vh)
        extra[f] = dict(voto_horizonte=ean("ph", x), mejor_unico=min((ean("F:" + n, x), n) for n in NAMES))
    print("votar por horizonte / mejor partido único:", extra)
    # escaños
    last = B.sort_values("foto").groupby("ean").last()
    real_t = B.groupby("ean").real.sum()
    E = last.assign(voto=voto, real=real_t)
    def tally(x):
        t = dict(eans=int(len(x)), real=float(x.real.sum()), seats={}, vol={})
        for p in NAMES + ["Empate"]:
            mk = x.voto == p; t["seats"][p] = int(mk.sum()); t["vol"][p] = float(x.real[mk].sum() / max(x.real.sum(), 1))
        t["win_eans"] = max(NAMES, key=lambda p: t["seats"][p]); t["win_vol"] = max(NAMES, key=lambda p: t["vol"][p])
        return t
    por = {"Total": {"Total": tally(E)}}
    for col, nm in [("cat", "Categoría"), ("casa", "Casa"), ("seg", "Tamaño"), ("tramo", "Edad"), ("fase", "Fase"), ("isf", "Bandera")]:
        x = E if col != "seg" else E[E.cat == "Fragancias"]
        por[nm] = {str(k): tally(g) for k, g in x.groupby(col)}
    urnas = {}
    for (f, q), x in Bv.groupby(["foto", "q"]):
        t = dict(eans=int(len(x)), real=float(x.real.sum()), seats={}, vol={})
        for p in NAMES + ["Empate"]:
            mk = x.ganador_urna == p; t["seats"][p] = int(mk.sum()); t["vol"][p] = float(x.real[mk].sum() / max(x.real.sum(), 1))
        t["win_eans"] = max(NAMES, key=lambda p: t["seats"][p]); t["win_vol"] = max(NAMES, key=lambda p: t["vol"][p])
        urnas[f"{f}|{q}"] = t
    E.reset_index().rename(columns={"index": "ean"}).to_parquet(W / "six_multi_ean.parquet")
    out = dict(names=NAMES, w90=w90.to_dict("records"), total=dict(w90={c: pw(c) for c in cols}, ean={c: ean(c) for c in cols},
               gana=int((w90.parl < w90.cons).sum()), n=int(len(w90))), persistencia=pers, horizonte=hor, extra_horizonte=extra, por=por, urnas=urnas,
               partidos=[ipp.describe(pd.Series(r)) for r in specs()], n_votantes=int(len(E)),
               por_foto={f: int((B.foto == f).groupby(B.ean).any().sum()) for f in SNAPS})
    (W / "six_multi.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=float))
    print("escaños:", por["Total"]["Total"]["seats"])


if __name__ == "__main__":
    main()
