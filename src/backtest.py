"""Backtest rolling-origin: para cada mes de versión M, solo datos < M, forecast M+1..M+8.
Guarda work/bt.parquet con (method, origin, ean, lag, target, F, A)."""
import sys
import time
import numpy as np
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import methods as mt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"


def context():
    H = pd.read_pickle(W / "hist.pkl")
    months = H.columns
    C = pd.read_pickle(W / "cuts.pkl").reindex(columns=months).fillna(0)
    E = pd.read_pickle(W / "epos.pkl").reindex(columns=months)
    attr = pd.read_pickle(W / "attr.pkl")
    # EPOS: NaN antes de que exista dato EPOS del EAN; 0 después
    Ev = E.values.copy()
    started = np.nan_to_num(Ev).cumsum(1) > 0
    Ev = np.where(started, np.nan_to_num(Ev), np.nan)
    # EPOS empieza 2024.M07: meses anteriores = NaN
    Ev[:, months < "2024-07-01"] = np.nan
    ctx = dict(H=H.values, C=C.values, E=Ev, attr=attr, months=months, eans=H.index.values)
    return ctx


def method_registry(include_slow=True):
    R = {
        "naive": mt.naive,
        "flat6": mt.make_trend_method(mt.g_flat, w=6),
        "flat3": mt.make_trend_method(mt.g_flat, w=3),
        "flat12": mt.make_trend_method(mt.g_flat, w=12),
        "flat6_cap": mt.make_trend_method(mt.g_flat, cap=(-0.5, 0.5), w=6),
        "median6": mt.make_trend_method(mt.g_median, w=6),
        "median3": mt.make_trend_method(mt.g_median, w=3),
        "median12": mt.make_trend_method(mt.g_median, w=12),
        "trim6": mt.make_trend_method(mt.g_trimmed, w=6),
        "trim12": mt.make_trend_method(mt.g_trimmed, w=12),
        "pline6": mt.make_group_trend("pline", 6),
        "brand6": mt.make_group_trend("brand", 6),
        "house6": mt.make_group_trend("house", 6),
        "house3": mt.make_group_trend("house", 3),
        "house12": mt.make_group_trend("house", 12),
        "brand12": mt.make_group_trend("brand", 12),
        "pline12": mt.make_group_trend("pline", 12),
        "blend_brand6": mt.make_blend_trend("brand", 6, 0.5),
        "blend_house6": mt.make_blend_trend("house", 6, 0.5),
        "blend_house12": mt.make_blend_trend("house", 12, 0.5),
        "clean40": mt.make_clean_trend(0.4),
        "clean60": mt.make_clean_trend(0.6),
        "clean100": mt.make_clean_trend(1.0),
        "clean40_s": mt.make_clean_trend(0.4, seasonal=True),
        "clean60_s": mt.make_clean_trend(0.6, seasonal=True),
        "clean40_s12": mt.make_clean_trend(0.4, w=12, seasonal=True),
        "cutadj4": mt.make_cut_adjusted(4),
        "cutadj4_trend_only": mt.make_cut_adjusted(4, base_adj=False),
        "epos6": mt.make_epos_trend(6),
        "epos3": mt.make_epos_trend(3),
        "epos6_blend": mt.make_epos_trend(6, blend=0.5),
        "lvl3_house": mt.make_level_season(3, "house"),
        "lvl6_house": mt.make_level_season(6, "house"),
        "lvl3_brand": mt.make_level_season(3, "brand"),
        "ets_house_share": mt.ets_damped_house_share,
    }
    if include_slow:
        R["ets_damped"] = mt.ets_damped
    return R


def method_registry_v2():
    hc = mt.make_clean_trend(0.4, w=12, seasonal=True)
    return {
        "lvl3_brand": mt.make_level_season(3, "brand"),
        "lvl6_brand": mt.make_level_season(6, "brand"),
        "house12_clean": mt.make_group_trend_clean("house", 12),
        "brand12_clean": mt.make_group_trend_clean("brand", 12),
        "pline12_clean": mt.make_group_trend_clean("pline", 12),
        "house6_clean": mt.make_group_trend_clean("house", 6),
        "house12_half": mt.make_damped_group("house", 12, 0.5),
        "house6_half": mt.make_damped_group("house", 6, 0.5),
        "ytd_house": mt.make_ytd_house(),
        "combo_h12_lvl6": mt.make_combo(mt.make_group_trend("house", 12), mt.make_level_season(6, "house")),
        "combo_h12c_lvl6": mt.make_combo(mt.make_group_trend_clean("house", 12), mt.make_level_season(6, "house")),
        "combo_c12_lvl6": mt.make_combo(hc, mt.make_level_season(6, "house")),
        "combo_c12_h12": mt.make_combo(hc, mt.make_group_trend("house", 12)),
        "combo_3": mt.make_combo(hc, mt.make_group_trend("house", 12), mt.make_level_season(6, "house")),
    }


def method_registry_v3():
    return {
        "house12_lfl": mt.make_group_lfl("house", 12),
        "house6_lfl": mt.make_group_lfl("house", 6),
        "brand12_lfl": mt.make_group_lfl("brand", 12),
        "house12_lfl_clean": mt.make_group_lfl("house", 12, clean=True),
        "epos_house6": mt.make_epos_group("house", 6),
        "epos_brand6": mt.make_epos_group("brand", 6),
        "epos_house3": mt.make_epos_group("house", 3),
        "house12_clean_resc": mt.make_clean_rescaled("house", 12),
        "house12_clean_x30": mt.make_group_trend_clean("house", 12, x=0.3),
        "house12_clean_x60": mt.make_group_trend_clean("house", 12, x=0.6),
        "house12_clean_x100": mt.make_group_trend_clean("house", 12, x=1.0),
        "house9_clean": mt.make_group_trend_clean("house", 9),
    }


def run(origins, methods, ctx):
    H = ctx["H"]; T = H.shape[1]; months = ctx["months"]
    # índice estacional desestacionalizador para clean *_s (house), recalculado por origen
    rows = []
    for M in origins:
        m = months.get_loc(M) if M in months else T + (pd.Timestamp(M).to_period("M") - months[-1].to_period("M")).n - 1
        ctx["season_idx"] = mt.seasonal_index(H, m, ctx["attr"]["house"].values, months, horizon=24)
        for name, f in methods.items():
            t0 = time.time()
            F = f(ctx, m)
            for k in range(1, 9):
                t = m + k
                A = H[:, t] if t < T else np.full(H.shape[0], np.nan)
                tgt = pd.Timestamp(M) + pd.DateOffset(months=k)
                rows.append(pd.DataFrame(dict(method=name, origin=pd.Timestamp(M), ean=ctx["eans"], lag=k,
                                              target=tgt, F=F[:, k - 1], A=A)))
            print(f"{M:%Y-%m} {name:20s} {time.time()-t0:5.1f}s", flush=True)
    return pd.concat(rows, ignore_index=True)


def consensus_rows(ctx, origins):
    """Forecast de consenso real por versión (raw y ajustado por cambio de perímetro)."""
    snaps = pd.read_pickle(W / "snaps.pkl")
    d = pd.read_parquet(W / "data.parquet")
    H = pd.DataFrame(ctx["H"], index=ctx["eans"], columns=ctx["months"])
    rows = []
    for v in snaps.index.get_level_values(0).unique():
        M = pd.Timestamp(v + "-01")
        if M not in origins:
            continue
        S = snaps.loc[v].reindex(ctx["eans"])
        # factor de perímetro por EAN: actual última versión / actual de esa versión, 12 meses previos
        win = pd.date_range(M - pd.DateOffset(months=12), M - pd.DateOffset(months=1), freq="MS")
        own = d[(d.version == v) & d.date.isin(win)].groupby("ean").act.sum().reindex(ctx["eans"])
        new = H[win].sum(1)
        tot = new.sum() / own.sum()
        fac = (new / own).where(own > 0).clip(0.5, 3).fillna(tot)
        for k in range(1, 9):
            tgt = M + pd.DateOffset(months=k)
            A = H[tgt].values if tgt in H.columns else np.nan
            F = S[tgt].values if tgt in S.columns else np.nan
            for name, FF in (("consensus", F), ("consensus_scopeadj", F * fac.values)):
                rows.append(pd.DataFrame(dict(method=name, origin=M, ean=ctx["eans"], lag=k, target=tgt, F=FF, A=A)))
    return pd.concat(rows, ignore_index=True)


if __name__ == "__main__":
    ctx = context()
    origins = pd.date_range("2025-01-01", "2026-07-01", freq="MS")
    if "--v3" in sys.argv:
        bt = run(origins, method_registry_v3(), ctx)
        bt.to_parquet(W / "bt_v3.parquet")
        print(bt.shape)
        sys.exit()
    if "--v2" in sys.argv:
        bt = run(origins, method_registry_v2(), ctx)
        bt.to_parquet(W / "bt_v2.parquet")
        print(bt.shape)
        sys.exit()
    slow = "--fast" not in sys.argv
    bt = run(origins, method_registry(include_slow=slow), ctx)
    cs = consensus_rows(ctx, origins)
    bt = pd.concat([bt, cs], ignore_index=True)
    bt.to_parquet(W / ("bt.parquet" if slow else "bt_fast.parquet"))
    print(bt.shape)
