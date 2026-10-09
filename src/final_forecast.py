"""Método ganador -> forecast desde la última versión, bandas P10-P90 por lag, comparación con consenso y efecto base.
Escribe work/results/forecast.md y work/forecast_winner.parquet."""
import sys
import numpy as np
import pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import methods as mt  # noqa
from backtest import context  # noqa
from evaluate import fq  # noqa

W = Path(__file__).resolve().parents[1] / "work"
WINNER = "resc_x40_cap"
TEAM = "flat6"


def bands(ev, method, level):
    u = ev[(ev.method == method) & ev.mature & (ev.origin >= "2025-07-01")]
    if level != "ean":
        u = u.groupby(["origin", "lag", "target", level], as_index=False)[["F", "A"]].sum()
    u = u[u.F > 0]
    e = (u.A - u.F) / u.F
    q = e.groupby(u.lag).quantile([0.1, 0.5, 0.9]).unstack()
    q.columns = ["P10", "P50", "P90"]
    q["n"] = e.groupby(u.lag).size()
    return q


def main():
    ev = pd.read_parquet(W / "ev.parquet")
    ctx = context()
    H = ctx["H"]; T = H.shape[1]; months = ctx["months"]; attr = ctx["attr"]
    m = T  # versión 2026-09 (mes en curso, parcial)
    ctx["season_idx"] = mt.seasonal_index(H, m, attr["house"].values, months, horizon=24)
    M = pd.Timestamp(months[-1]) + pd.DateOffset(months=1)
    tg = [M + pd.DateOffset(months=k) for k in range(1, 9)]
    Fw = mt.make_resc_general(cap=(-0.3, 0.3))(ctx, m)
    Ft = mt.make_trend_method(mt.g_flat, w=6)(ctx, m)
    Fn = mt.naive(ctx, m)
    # trend house usado (12M, histórico limpio)
    Hc, outl = mt.clean_history(H, m, 0.4, 5, True, ctx)
    g12 = pd.Series(mt._group_g(Hc, m, 12, attr.house.values), index=attr.index).groupby(attr.house).first()
    g12raw = pd.Series(mt._group_g(H, m, 12, attr.house.values), index=attr.index).groupby(attr.house).first()
    g6raw = pd.Series(mt._group_g(H, m, 6, attr.house.values), index=attr.index).groupby(attr.house).first()
    age = ((M.year - attr.first_sale.dt.year) * 12 + M.month - attr.first_sale.dt.month)
    mature = (age >= 18).values
    fut = pd.read_pickle(W / "fut_latest.pkl").reindex(columns=tg).fillna(0)
    rows = []
    for i, e in enumerate(ctx["eans"]):
        for k, t in enumerate(tg):
            rows.append((e, t, k + 1, Fw[i, k], Ft[i, k], Fn[i, k], fut.loc[e, t] if e in fut.index else 0.0, mature[i]))
    F = pd.DataFrame(rows, columns=["ean", "target", "lag", "winner", "team_flat6", "naive", "consensus", "mature"])
    for c in ["house", "brand", "pline", "desc", "resp"]:
        F[c] = attr[c].reindex(F.ean).values
    F["fq"] = fq(F.target).values
    # híbrido: maduros = ganador; jóvenes = consenso
    F["hybrid"] = np.where(F.mature, F.winner.fillna(0), F.consensus)
    bE = bands(ev, WINNER, "ean"); bH = bands(ev, WINNER, "house")
    F = F.merge(bH[["P10", "P90"]], left_on="lag", right_index=True)
    F.to_parquet(W / "forecast_winner.parquet")

    L = [f"# Forecast desde versión {M:%Y-%m} (generado por src/final_forecast.py)\n",
         f"Ganador: {WINNER} = total house-mes = LY real x (1 + trend 12M house sobre histórico limpio, tope ±30%); reparto por EAN/mes según base LY limpia.\n",
         "## Trends house usados\n",
         pd.DataFrame({"g12_limpio": g12, "g12_bruto": g12raw, "g6_bruto(equipo-like)": g6raw}).round(3).to_markdown(),
         "\n## Bandas de error relativo (A-F)/F del ganador por lag — nivel EAN-mes\n", bE.round(3).to_markdown(),
         "\n## Bandas — nivel house-mes\n", bH.round(3).to_markdown(),
         "\n## Bandas — nivel house-quarter\n"]
    u = ev[(ev.method == WINNER) & ev.mature & (ev.origin >= "2025-07-01")]
    uq = u.groupby(["origin", "fq", "house"], as_index=False)[["F", "A"]].sum()
    uq["first_lag"] = u.groupby(["origin", "fq", "house"]).lag.min().values
    uq = uq[uq.F > 0]; e = (uq.A - uq.F) / uq.F
    L.append(e.quantile([0.1, 0.5, 0.9]).round(3).to_frame("err").T.to_markdown())
    # comparación por house x quarter (solo maduros y total híbrido)
    for nm, sub in [("EANs maduros", F[F.mature]), ("TOTAL (maduros=ganador, jóvenes=consenso)", F)]:
        p = sub.groupby(["house", "fq"])[["winner", "hybrid", "team_flat6", "naive", "consensus"]].sum()
        p["winner_vs_cons"] = p.winner / p.consensus - 1
        p["hybrid_vs_cons"] = p.hybrid / p.consensus - 1
        L += [f"\n## Forecast por house x quarter — {nm}\n", p.round(3).to_markdown()]
    # efecto base: para cada quarter futuro, quarter homólogo LY: real vs limpio, YoY LY, cortes LY
    Hd = pd.DataFrame(np.nan_to_num(H), index=ctx["eans"], columns=months)
    Hcd = pd.DataFrame(np.nan_to_num(Hc[:, :T]), index=ctx["eans"], columns=months)
    Cd = pd.DataFrame(ctx["C"], index=ctx["eans"], columns=months)
    rows = []
    for q in sorted(F.fq.unique()):
        tq = sorted(F[F.fq == q].target.unique())
        ly = [pd.Timestamp(t) - pd.DateOffset(years=1) for t in tq]
        ly2 = [pd.Timestamp(t) - pd.DateOffset(years=2) for t in tq]
        for h in sorted(attr.house.unique()):
            sel = (attr.house == h).values
            a_ly = Hd.loc[sel, ly].sum().sum(); a_ly2 = Hd.loc[sel, [x for x in ly2 if x in months]].sum().sum()
            c_ly = Hcd.loc[sel, ly].sum().sum()
            rows.append(dict(fq=q, house=h, months=",".join(pd.DatetimeIndex(tq).strftime("%m")), LY=a_ly,
                             LY_limpio=c_ly, pico_LY=a_ly / c_ly - 1 if c_ly else np.nan,
                             yoy_LY=a_ly / a_ly2 - 1 if a_ly2 else np.nan, cuts4_LY_pct=Cd.loc[sel, ly].sum().sum() / 4 / a_ly if a_ly else np.nan))
    L += ["\n## Efecto base: quarter homólogo del año anterior\n",
          "pico_LY = cuánto estaba el LY por encima (+) / debajo (-) de su versión limpia; yoy_LY = cómo creció ese quarter vs 2 años antes; cuts4 = cortes/4 sobre envíos.\n",
          pd.DataFrame(rows).round(3).to_markdown(index=False)]
    # outliers detectados (último corte)
    O = pd.DataFrame(outl, index=ctx["eans"], columns=months[:m])
    ol = O.stack(); ol = ol[ol]
    L += [f"\n## Outliers detectados con datos hasta {months[-1]:%Y-%m}: {len(ol)} EAN-mes "
          f"({len(ol) / np.isfinite(H).sum():.1%} de los puntos con dato). Regla: |A - mediana móvil 5m (desestacionalizada house)| > 40% de esa mediana.\n"]
    (W / "results" / "forecast.md").write_text("\n".join(L))
    print("ok")


if __name__ == "__main__":
    main()
