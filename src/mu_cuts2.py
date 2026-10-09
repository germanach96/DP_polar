"""Makeup: formas prudentes de incluir cortes. base = media6M de (actual + ajuste_cortes - 25% DA+), x (1 + 50% trend12M función).
ajuste_cortes: k% de cortes, o k% de cortes con tope = t% del envío del mes. -> work/results/mu_cuts2.md"""
import sys, warnings, itertools
import numpy as np, pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import methods as mt  # noqa
import mu_backtest as mb  # noqa
warnings.filterwarnings("ignore")
W = Path(__file__).resolve().parents[1] / "work"
M = mb.M


def main():
    d, Hdf, Edf, Cdf, attr, fac = mb.load()
    H = Hdf.values; C = Cdf.values; eans = Hdf.index; A = np.nan_to_num(H)
    variants = [("sin cortes", 0, None)] + [(f"{int(k*100)}% cortes", k, None) for k in (0.05, 0.10, 0.15, 0.25)] + \
               [(f"{int(k*100)}% cortes, tope {int(t*100)}% envío", k, t) for k in (0.10, 0.25, 0.5) for t in (0.10, 0.25, 0.5)]
    rows = []
    for V in pd.date_range("2025-07-01", "2026-07-01", freq="MS"):
        m = M.get_loc(V); fi = list(range(m + 1, m + 9))
        DAp = np.clip(np.nan_to_num(mb.da_known(d, eans, V).values), 0, None); DAp[:, m:] = 0
        vv = [v for v in mb.VERS if pd.Timestamp(v + "-01") <= V] or [mb.VERS[0]]
        isf = d[d.version == vv[-1]].groupby("ean").isf.max().reindex(eans).fillna(0).values
        Hm = H.copy(); Hm[:, m:] = np.nan
        first = np.argmax(np.isfinite(Hm), 1).astype(float); first[~np.isfinite(Hm).any(1)] = np.nan
        central = (m - first) >= 6
        g = np.clip(np.nan_to_num(mt._group_g(Hm, m, 12, attr.fam_brand.values, central)), -.3, .3)
        for nm, k, t in variants:
            add = k * C
            if t is not None:
                add = np.minimum(add, t * np.nan_to_num(Hm))
            adj = np.where(np.isfinite(Hm), np.clip(np.nan_to_num(Hm) + add - 0.25 * DAp, 0, None), np.nan)
            base = np.nan_to_num(np.nanmean(adj[:, m - 6:m], 1))
            F = np.repeat((base * (1 + 0.5 * g))[:, None], 8, 1)
            for fam in ["GUMU", "KYMU"]:
                for univ, sel in [("sin_manual", central & (isf == 0) & (attr.fam.values == fam)), ("todos", central & (attr.fam.values == fam))]:
                    w, b, a = mb.evaluate(F, A, fi, sel)
                    rows.append(dict(corte=V, fam=fam, univ=univ, variante=nm, wmape=w, bias=b, A=a))
    R = pd.DataFrame(rows); R.to_pickle(W / "mu_cuts2.pkl")
    agg = lambda x: pd.Series(dict(wmape=(x.wmape * x.A).sum() / x.A.sum(), bias=(x.bias * x.A).sum() / x.A.sum()))
    g = R.groupby(["variante", "fam", "univ"]).apply(agg)
    w = g.wmape.unstack(["fam", "univ"]); b = g.bias.unstack(["fam", "univ"])
    w.columns = [f"{f}_{u}" for f, u in w.columns]; b.columns = [f"bias_{f}_{u}" for f, u in b.columns]
    d0 = w - w.loc["sin cortes"]
    out = pd.DataFrame({"mejora_media_pts": -d0.mean(1) * 100, "peor_caso_pts": -d0.max(1) * 100}).join(w.round(3)).join(b.round(3))
    wo = R.pivot_table(index=["variante", "fam", "univ"], columns="corte", values="wmape")
    out = out.sort_values("mejora_media_pts", ascending=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 100)
    print(out.round(2).to_string())
    (W / "results" / "mu_cuts2.md").write_text("# Makeup: cortes prudentes (src/mu_cuts2.py)\n\n" + out.round(3).to_markdown())


if __name__ == "__main__":
    main()
