"""Posición de cada EAN en las 3 brújulas con lo que vio en FY25 (foto simulada sep-24 → real oct-24..jun-25), mismas reglas que
src/ideo_brujulas6.py: para cada eje, la mejor estrategia de un lado frente a la mejor del otro (puntos de error, tanh(Δ/5 pts)).
Estrategias del banco sin bases ni trends de 3 meses (vetados). En sep-24 no hay DAs guardados: el eje de DAs queda en el centro.
Salida: work/fy25_brujulas_ean.parquet y work/fy25_brujulas.json (reparto por lado)"""
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


def main():
    P = ip.build(ip.VOTE_SNAP, save=False); ctx = ie.Ctx(P); a = P["attr"]
    assert P["DAp"].sum() == 0 and P["DAf"].sum() == 0
    v = np.where(ctx.vote)[0]
    A = P["A"][v]; Aq = np.stack([A[:, ix].sum(1) for ix in P["qidx"]], 1); real = Aq.sum(1)
    qmat = np.zeros((9, 3))
    for q, ix in enumerate(P["qidx"]):
        qmat[ix, q] = 1
    seas = {s: ctx.season(s) for s in ie.SEAS}
    CV = {(p, s): ctx.curve(p, s) for p in ie.CURVE_POOLS for s in [None, "casa"]}
    trends = [t for t in ie.TRENDS if t[1] != 3]
    G = {(s, w): ctx.trend(s, w) for s, w, _, _ in trends[1:]}
    MULT = np.stack([np.ones(len(a))] + [1 + f * np.clip(G[(s, w)], -c, c) for s, w, f, c in trends[1:]], 0)[:, v]
    rows, scores = [], []
    for cut in ie.CUTS:
        X = ie.adjusted(ctx, 0.0, cut)
        cores = [("LY", None, None)] + [(b, None, None) for b in ["M6", "M12"]] + [(b + "e", s, None) for b in ["M6", "M12"] for s in ie.SEAS]
        cores += [("LY+M6e", s, None) for s in ie.SEAS] + [("CV", s, p) for p in ie.CURVE_POOLS for s in [None, "casa"]]
        for b, s, pool in cores:
            B = ie.base_matrix(ctx, X, b, seas[s] if s else None, CV[(pool, s)] if b == "CV" else None)[v]
            tl = trends if b != "CV" else trends[:1]
            Fq = np.clip(B[None] * MULT[:len(tl), :, None], 0, None) @ qmat
            sc = np.minimum(np.abs(Fq - Aq[None]).sum(2) / np.where(real > 0, real, 1)[None], ipp.CAPSCORE)
            scores.append(sc)
            rows += [dict(base=b, estac=s or "sin", fuente=src, fuerza=f, cortes=cut) for src, w, f, c in tl]
    Sc = np.concatenate(scores); st = pd.DataFrame(rows)
    b = st.base.values; f_ = st.fuente.values; fz = st.fuerza.values; es = st.estac.values
    axes = {"c1x": (np.isin(b, ["M6", "M12"]), np.isin(b, ["M6e", "M12e"]) & (es == "casa")),
            "c1y": (np.isin(b, ["M6"]) | (np.isin(b, ["M6e"]) & (es == "casa")), np.isin(b, ["M12"]) | (np.isin(b, ["M12e"]) & (es == "casa"))),
            "c2x": (np.isin(f_, ["EAN", "línea"]), np.isin(f_, ["casa", "categoría"])),
            "c2y": (((f_ == "ninguna") & (b != "CV")) | ((f_ != "ninguna") & (fz <= 0.25)), (f_ != "ninguna") & (fz >= 0.75)),
            "c3y": (st.cortes.values == "0", st.cortes.values == "50%")}
    ok = real > 0
    pos = pd.DataFrame(index=a.index[v][ok])
    for k, (L, R) in axes.items():
        pos[k] = np.tanh((Sc[L][:, ok].min(0) - Sc[R][:, ok].min(0)) / 0.05)
    pos["c3x"] = 0.0                                     # sin DAs en FY25: no se puede juzgar
    pos = pos.join(a[["cat"]]); pos["real"] = real[ok]
    pos.to_parquet(W / "fy25_brujulas_ean.parquet")
    share = lambda col, side, g=pos: float(((g[col] > 0.3) if side > 0 else (g[col] < -0.3)).mean())
    fr, mu = pos[pos.cat == "Fragancias"], pos[pos.cat == "Makeup"]
    stats = {k: dict(der=share(k, 1), izq=share(k, -1), centro=float((pos[k].abs() <= 0.3).mean()),
                     der_fr=share(k, 1, fr), izq_fr=share(k, -1, fr), der_mu=share(k, 1, mu), izq_mu=share(k, -1, mu)) for k in list(axes) + ["c3x"]}
    (W / "fy25_brujulas.json").write_text(json.dumps(dict(stats=stats, n=int(len(pos)), estrategias=int(len(st))), indent=1, ensure_ascii=False))
    print(len(st), "estrategias ·", len(pos), "EANs"); print({k: {kk: round(x, 2) for kk, x in s.items()} for k, s in stats.items()})


if __name__ == "__main__":
    main()
