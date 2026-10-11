"""Elección con FY25 y prueba en FY26 (diseño acordado con el usuario 2026-10-10).

- Voto: fotos simuladas sep-24, dic-24 y mar-25 (solo histórico; FY23 recuperado del LY, ver ideo_panel.extend). Cada EAN vota en las
  6 urnas cerradas antes de sep-25 (sep-24: Q2–Q4 FY25 · dic-24: Q3–Q4 · mar-25: Q4) con el formato fijo (sm.elect). En esas fotos no hay
  DAs ni bandera guardados como plan (o9 los borra): la base no se limpia y no hay DAs futuros.
- Prueba: foto sep-25 tal cual (DAs de base de la foto en la que el mes era futuro; DAs futuros según la bandera), pronóstico de
  oct-25..jun-26 = Q2 (1–3 meses), Q3 (4–6) y Q4 (7–9) de FY26 contra el real de la foto sep-26. Sin consenso.
- EANs sin historia en FY25 (no votaron): lo que votaron sus parecidos = códigos de su casa × tamaño/función que en sep-24 tenían
  su misma edad (si no hay 5: casa × edad, categoría × edad).
Opciones: regla de su categoría · un partido (su voto) · coalición (media de sus 2 partidos de menor error medio en FY25) · media de 6.
Salida: work/fy25_eleccion.json, work/fy25_eleccion.parquet (EAN × quarter de la prueba)"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_panel as ip  # noqa
import six_multi as sm  # noqa

W = ip.W
N = sm.NAMES_UNO
MIN_G = 5
PAST = ["2024-09", "2024-12", "2025-03"]               # fotos simuladas (solo histórico); urnas = quarters cerrados antes de sep-25
KNOWN = "2025-08-01"


def ballots(snap, sp, hasta=None):
    """Urnas (EAN × quarter completo) de la foto snap; con hasta, solo quarters cerrados hasta ese mes (lo que se sabía entonces)."""
    P = ip.build(snap, save=False); a = P["attr"]; v = a.votante.values
    F0 = sm.forecasts(P, sp)[:, v]
    flag = a.isf.values[v].astype(int).clip(0, 2)
    wf = np.array([sm.FLAGW[f] for f in flag])[:, None]
    F = np.clip(F0 + wf[None] * P["DAf"][v][None], 0, None)
    A = P["A"][v]; av = a[v]; out = []
    for k_q, (q, ix) in enumerate(zip(P["qlist"], P["qidx"])):
        if len(ix) < 3 or (hasta is not None and P["months"][ix[-1]] > pd.Timestamp(hasta)):
            continue
        df = pd.DataFrame(dict(ean=av.index, foto=snap, q=q, lag=["1–3", "4–6", "7–9"][k_q], cat=av.cat.values, casa=av.casa.values, seg=av.seg.values,
                               tramo=av.tramo.values, fase=av.fase.values, isf=flag, desc=av.desc.values, real=A[:, ix].sum(1)))
        for k, nm in enumerate(N):
            df["F:" + nm] = F[k][:, ix].sum(1)
        out.append(df)
    print(f"{snap}: {v.sum()} votantes · urnas {sorted(set(pd.concat(out).q))}")
    return pd.concat(out, ignore_index=True)


HIST = ("Con historia FY25", "Sin historia FY25 (parecidos)")


def choose(Btr, Bte):
    """Cada EAN de Bte elige con las urnas de Btr (formato fijo): un partido, coalición (sus 2 de menor error medio) y media de 6.
    Sin urnas en Btr: lo que votaron/erraron sus parecidos (casa × tamaño/función × edad en la última foto de Btr)."""
    voto, Bv = sm.elect(Btr)
    # error medio por EAN y partido en FY25 (tope 200%) -> coalición
    Wq = np.stack([sm.wq(Btr["F:" + n].values, Btr.real.values) for n in N], 1)
    err = pd.DataFrame(np.minimum(Wq, 2), columns=N); err["ean"] = Btr.ean.values
    e_ean = err.groupby("ean")[N].mean()
    a24 = Btr.sort_values("foto").drop_duplicates("ean", keep="last").set_index("ean")[["cat", "casa", "seg", "tramo"]]
    # parecidos: grupo en sep-24 (casa × tamaño/función × edad) -> votos y errores medios del grupo
    LEVELS = [["casa", "seg", "tramo"], ["casa", "tramo"], ["cat", "tramo"], ["cat"]]
    te = Bte.drop_duplicates("ean").set_index("ean")[["cat", "casa", "seg", "tramo"]]
    con = te.index.isin(voto.index)
    vt = a24.join(voto.rename("voto"))
    eg = a24.join(e_ean)
    pick_v = pd.Series(index=te.index, dtype=object); pick_e = {}; nivel = pd.Series("propio", index=te.index)
    for i in te.index[~con]:
        for lev in LEVELS:
            mk = np.ones(len(vt), bool)
            for c in lev:
                mk &= (vt[c] == te.loc[i, c]).values
            if mk.sum() >= MIN_G:
                cnt = vt.voto[mk][vt.voto[mk] != "Empate"].value_counts()
                pick_v[i] = cnt.index[0] if len(cnt) else "Empate"
                pick_e[i] = eg[N][mk].mean().values; nivel[i] = "parecidos: " + " × ".join({"casa": "casa", "seg": "tamaño/función", "tramo": "edad", "cat": "categoría"}[c] for c in lev)
                break
    partido = voto.reindex(te.index).where(con, pick_v).fillna("Empate")
    E2 = e_ean.reindex(te.index)
    for i, v in pick_e.items():
        E2.loc[i] = v
    top2 = pd.DataFrame(np.argsort(np.where(np.isfinite(E2.values), E2.values, 1.0), 1)[:, :2], index=te.index)
    B = Bte.copy()
    FF = np.stack([B["F:" + n].values for n in N], 1); n_ = np.arange(len(B))
    B["regla"] = np.where(B.cat == "Fragancias", B["F:Regla fragancias"], B["F:Regla makeup"])
    p = B.ean.map(partido).values
    p = np.where(p == "Empate", np.where(B.cat == "Fragancias", "Regla fragancias", "Regla makeup"), p)
    B["partido"] = p; B["un_partido"] = FF[n_, [N.index(x) for x in p]]
    o = top2.reindex(B.ean).values
    B["coal1"] = [N[k] for k in o[:, 0]]; B["coal2"] = [N[k] for k in o[:, 1]]
    B["coalicion"] = np.take_along_axis(FF, o, 1).mean(1)
    B["media6"] = FF.mean(1)
    B["historia"] = np.where(B.ean.isin(voto.index), HIST[0], HIST[1])
    B["nivel"] = B.ean.map(nivel).values
    return B, voto, Bv, partido


def main():
    sp = sm.specs()
    B24 = pd.concat([ballots(f, sp, hasta=KNOWN) for f in PAST], ignore_index=True)
    B25 = ballots(ip.SNAP, sp)
    B, voto, Bv, partido = choose(B24, B25)
    B.to_parquet(W / "fy25_eleccion.parquet")
    OPTS = {"regla": "Regla de su categoría", "un_partido": "Un partido (su voto FY25)", "coalicion": "Coalición de sus 2 mejores", "media6": "Media de los 6"}
    cols = list(OPTS) + ["F:" + n for n in N]
    ean_err = lambda x, c: float(np.abs(x[c] - x.real).sum() / x.real.sum())
    def w90(x, c):
        g = x.groupby("casa").agg(r=("real", "sum"), f=(c, "sum"))
        return dict(wape90=float((g.f - g.r).abs().sum() / g.r.sum()), sesgo=float(g.f.sum() / g.r.sum() - 1))
    res = {}
    for lg in ["7–9", "4–6", "1–3", "total"]:
        x = B if lg == "total" else B[B.lag == lg]
        res[lg] = {c: dict(ean=ean_err(x, c), **w90(x, c)) for c in cols}
    hist = {h: {lg: {c: ean_err(x[x.lag == lg] if lg != "total" else x, c) for c in cols} for lg in ["7–9", "4–6", "1–3", "total"]}
            for h, x in B.groupby("historia")}
    tram = {t: {c: ean_err(x, c) for c in cols} for t, x in B.groupby("tramo") if x.real.sum() > 0}
    casa = {}
    for (h, q), x in B.groupby(["casa", "q"]):
        R = x.real.sum(); casa.setdefault(h, {})[q] = {c: float(abs(x[c].sum() - R) / R) for c in list(OPTS)}
    print("\nError EAN a EAN (foto sep-25 → real sep-26), por meses de distancia:")
    print(pd.DataFrame({lg: {OPTS.get(c, c.replace("F:", "Solo ")): res[lg][c]["ean"] for c in cols} for lg in res}).mul(100).round(1).to_string())
    print("\nWAPE90 casa:"); print(pd.DataFrame({lg: {OPTS[c]: f"{res[lg][c]['wape90']:.1%} ({res[lg][c]['sesgo']:+.0%})" for c in OPTS} for lg in res}).to_string())
    print("\nPor historia (total):", {h: {OPTS[c]: round(v["total"][c] * 100, 1) for c in OPTS} for h, v in hist.items()})
    # escaños (EANs de la foto sep-25) y volumen real FY26 Q2–Q4
    E = B.groupby("ean").agg(real=("real", "sum"), cat=("cat", "first"), casa=("casa", "first"), seg=("seg", "first"), tramo=("tramo", "first"),
                             fase=("fase", "first"), isf=("isf", "first"), historia=("historia", "first"), nivel=("nivel", "first"))
    E["voto"] = partido.reindex(E.index).values; E["coal1"] = B.groupby("ean").coal1.first(); E["coal2"] = B.groupby("ean").coal2.first()
    def tally(x):
        t = dict(eans=int(len(x)), real=float(x.real.sum()), seats={}, vol={})
        for pp in N + ["Empate"]:
            mk = x.voto == pp; t["seats"][pp] = int(mk.sum()); t["vol"][pp] = float(x.real[mk].sum() / max(x.real.sum(), 1))
        t["win_eans"] = max(N, key=lambda q: t["seats"][q]); t["win_vol"] = max(N, key=lambda q: t["vol"][q])
        return t
    por = {"Total": {"Total": tally(E)}}
    for col, nm in [("cat", "Categoría"), ("casa", "Casa"), ("tramo", "Edad"), ("fase", "Fase"), ("historia", "Historia")]:
        por[nm] = {str(k): tally(g) for k, g in E.groupby(col)}
    pares = E.apply(lambda r: " + ".join(sorted([r.coal1, r.coal2], key=N.index)), axis=1)
    coal = [dict(par=k, eans=int(len(g)), vol=float(g.sum() / E.real.sum())) for k, g in E.real.groupby(pares)]
    coal = sorted(coal, key=lambda r: -r["eans"])
    E.reset_index().to_parquet(W / "fy25_eleccion_ean.parquet")
    Bv.to_parquet(W / "fy25_urnas.parquet")
    out = dict(names=N, opciones=OPTS, horizonte=res, historia=hist, tramo=tram, casa_q=casa, por=por, coaliciones=coal,
               n_votantes_fy25=int(len(voto)), n_prueba=int(len(E)), sin_historia=int((E.historia != "Con historia FY25").sum()),
               niveles=E.nivel.value_counts().to_dict(), real_fy25=float(B24.real.sum()), real_fy26=float(B.real.sum()))
    # ¿se repite el ganador? voto FY25 frente al ganador (con trampa) de FY26 en la foto sep-25
    v26, _ = sm.elect(B25)
    j = E[E.historia == "Con historia FY25"].join(v26.rename("v26"))
    out["persistencia"] = dict(igual=float((j.voto == j.v26).mean()), azar=1 / len(N), n=int(len(j)))
    out["sesgo_fy25"] = {n: float(B24["F:" + n].sum() / B24.real.sum() - 1) for n in N}
    out["error_fy25"] = {n: float(np.abs(B24["F:" + n] - B24.real).sum() / B24.real.sum()) for n in N}
    out["sesgo_fy26"] = {n: float(B["F:" + n].sum() / B.real.sum() - 1) for n in N}
    (W / "fy25_eleccion.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=float))
    print("\nescaños:", por["Total"]["Total"]["seats"]); print("niveles:", out["niveles"]); print("coaliciones:", coal[:8])


if __name__ == "__main__":
    main()
