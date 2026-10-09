"""Makeup: ¿ajustar la base (media 6M) con cortes y DAs positivos? Regla: media6M x (1 + 50% trend12M función, tope ±30%).
base = media de los últimos 6 meses de (actual + kc*cortes - kd*DA+). Variante: aplicar el mismo ajuste también al histórico del trend.
DA conocidos en cada corte = versiones <= corte (no hay DA antes de la foto 2025-09 -> cortes anteriores sin ajuste DA).
13 cortes mensuales jul-25..jul-26 + foto sep-25 + recálculo mar-26. -> work/results/mu_cuts_da.md"""
import sys, warnings, itertools
import numpy as np, pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import methods as mt  # noqa
import mu_backtest as mb  # noqa
warnings.filterwarnings("ignore")
W = Path(__file__).resolve().parents[1] / "work"
M = mb.M


def forecast(H, C, DAp, attr, m, kc, kd, in_trend):
    Hm = H.copy(); Hm[:, m:] = np.nan
    first = np.argmax(np.isfinite(Hm), 1).astype(float); first[~np.isfinite(Hm).any(1)] = np.nan
    central = (m - first) >= 6
    adj = np.where(np.isfinite(Hm), np.clip(np.nan_to_num(Hm) + kc * C - kd * DAp, 0, None), np.nan)
    base = np.nan_to_num(np.nanmean(adj[:, m - 6:m], 1))
    g = mt._group_g(adj if in_trend else Hm, m, 12, attr.fam_brand.values, central)
    g = np.clip(np.nan_to_num(g), -.3, .3)
    return np.repeat((base * (1 + 0.5 * g))[:, None], 8, 1), central


def main():
    d, Hdf, Edf, Cdf, attr, fac = mb.load()
    H = Hdf.values; C = Cdf.values; eans = Hdf.index; A = np.nan_to_num(H)
    rows = []
    cutoffs = [(V, "mensual") for V in pd.date_range("2025-07-01", "2026-07-01", freq="MS")]
    for V, tipo in cutoffs:
        m = M.get_loc(V); fi = list(range(m + 1, m + 9))
        DAp = np.clip(np.nan_to_num(mb.da_known(d, eans, V).values), 0, None); DAp[:, m:] = 0
        vv = [v for v in mb.VERS if pd.Timestamp(v + "-01") <= V] or [mb.VERS[0]]
        isf = d[d.version == vv[-1]].groupby("ean").isf.max().reindex(eans).fillna(0).values
        for kc, kd, it in itertools.product([0, 0.25, 0.5], [0, 0.25, 0.5, 0.75, 1.0], [False, True]):
            if it and kc == 0 and kd == 0:
                continue
            F, central = forecast(H, C, DAp, attr, m, kc, kd, it)
            for fam in ["GUMU", "KYMU"]:
                for univ, sel in [("sin_manual", central & (isf == 0) & (attr.fam.values == fam)), ("todos", central & (attr.fam.values == fam))]:
                    w, b, a = mb.evaluate(F, A, fi, sel)
                    rows.append(dict(corte=V, fam=fam, univ=univ, kc=kc, kd=kd, trend_ajustado=it, wmape=w, bias=b, A=a,
                                     foto=V.strftime("%Y-%m") in ("2025-09", "2026-03")))
    R = pd.DataFrame(rows)
    R.to_pickle(W / "mu_cuts_da.pkl")
    agg = lambda x: pd.Series(dict(wmape=(x.wmape * x.A).sum() / x.A.sum(), bias=(x.bias * x.A).sum() / x.A.sum(), bias_abs=x.bias.abs().mean()))
    L = ["# Makeup: cortes y DAs en la base (src/mu_cuts_da.py)\n"]
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
    for fam in ["GUMU", "KYMU"]:
        for univ in ["sin_manual", "todos"]:
            x = R[(R.fam == fam) & (R.univ == univ)]
            g = x.groupby(["trend_ajustado", "kc", "kd"]).apply(agg)
            wo = x.pivot_table(index=["trend_ajustado", "kc", "kd"], columns="corte", values="wmape")
            ref = wo.loc[(False, 0, 0)]
            g["gana_a_sin_ajuste"] = [int((wo.loc[i] < ref).sum()) for i in wo.index]
            fx = x[x.foto].pivot_table(index=["trend_ajustado", "kc", "kd"], columns="corte", values="wmape")
            fx.columns = ["foto_" + c.strftime("%Y-%m") for c in fx.columns]
            g = g.join(fx).sort_values("wmape")
            L += [f"\n## {fam} — {univ}\n", g.round(3).to_markdown()]
            print(f"===== {fam} {univ}"); print(g.round(3).head(10).to_string()); print(g.loc[[(False, 0, 0)]].round(3).to_string())
    (W / "results" / "mu_cuts_da.md").write_text("\n".join(L))


if __name__ == "__main__":
    main()
