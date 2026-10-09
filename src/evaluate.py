"""Métricas del backtest: WMAPE (nivel EAN) y bias, global / por lag / quarter / segmentos."""
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"


def fq(ts):
    """Quarter fiscal (FY empieza en julio)."""
    ts = pd.DatetimeIndex(ts)
    fy = ts.year + (ts.month >= 7)
    q = ((ts.month - 7) % 12) // 3 + 1
    return pd.Series([f"FY{y % 100}.Q{x}" for y, x in zip(fy, q)])


def prepare(bt_file="bt.parquet"):
    if isinstance(bt_file, (list, tuple)):
        bt = pd.concat([pd.read_parquet(W / f) for f in bt_file], ignore_index=True)
        bt = bt.drop_duplicates(["method", "origin", "ean", "lag"], keep="last")
    else:
        bt = pd.read_parquet(W / bt_file)
    attr = pd.read_pickle(W / "attr.pkl")
    H = pd.read_pickle(W / "hist.pkl")
    C = pd.read_pickle(W / "cuts.pkl")
    bt = bt[bt.A.notna()].copy()
    # fallback: método sin forecast -> naïve
    nv = bt[bt.method == "naive"].set_index(["origin", "ean", "lag"]).F
    key = pd.MultiIndex.from_frame(bt[["origin", "ean", "lag"]])
    bt["F"] = bt.F.fillna(pd.Series(nv.reindex(key).values, index=bt.index)).fillna(0.0)
    # madurez: primera venta <= origen - 18 meses
    fs = attr.first_sale.reindex(bt.ean).values
    bt["age_m"] = ((bt.origin.dt.year - pd.DatetimeIndex(fs).year) * 12 + bt.origin.dt.month - pd.DatetimeIndex(fs).month).values
    bt["mature"] = bt.age_m >= 18
    # segmentos
    for c in ["house", "brand", "resp", "resp_2603", "isf", "category"]:
        bt[c] = attr[c].reindex(bt.ean).values
    bt["isf"] = bt.isf.fillna(0).astype(int)
    bt["fq"] = fq(bt.target).values
    # rotura: cortes/4 > 20% del actual del mes objetivo
    Cl = C.stack(); Cl.index.names = ["ean", "target"]
    cut = Cl.reindex(pd.MultiIndex.from_frame(bt[["ean", "target"]])).fillna(0).values
    bt["cut"] = cut
    bt["cut_flag"] = (cut / 4) > 0.2 * bt.A.values
    # ABC por volumen de los 12 meses previos al origen (calculado por origen)
    Hl = H.T
    abc = {}
    for o in bt.origin.unique():
        win = pd.date_range(o - pd.DateOffset(months=12), o - pd.DateOffset(months=1), freq="MS")
        v = Hl.reindex(win).sum().sort_values(ascending=False)
        cs = v.cumsum() / v.sum()
        abc[o] = pd.Series(np.where(cs <= 0.8, "A", np.where(cs <= 0.95, "B", "C")), index=v.index)
        # volatilidad: CV de la serie desestacionalizada simple (ratio a la media móvil 12m)
    bt["abc"] = [abc[o].get(e, "C") for o, e in zip(bt.origin, bt.ean)]
    # estable vs volátil: CV de los últimos 12 meses (sin desestacionalizar) por origen
    vol = {}
    for o in bt.origin.unique():
        win = pd.date_range(o - pd.DateOffset(months=12), o - pd.DateOffset(months=1), freq="MS")
        x = Hl.reindex(win)
        cv = x.std() / x.mean()
        vol[o] = cv
    bt["cv"] = [vol[o].get(e, np.nan) for o, e in zip(bt.origin, bt.ean)]
    bt["volat"] = np.where(bt.cv <= 0.75, "estable", "volatil")
    return bt


def score(df, by=None):
    df = df.assign(ae=(df.F - df.A).abs(), e=df.F - df.A)
    keys = ["method"] + ([by] if isinstance(by, str) else (by or []))
    g = df.groupby(keys)
    out = pd.DataFrame({"wmape": g.ae.sum() / g.A.sum(), "bias": g.e.sum() / g.A.sum(), "A": g.A.sum(), "n": g.size()})
    return out


def table(df, by, metric="wmape"):
    s = score(df, by)[metric].unstack(by)
    return s


if __name__ == "__main__":
    import sys
    files = sys.argv[1:] or ["bt.parquet", "bt_v2.parquet"]
    bt = prepare(files)
    bt.to_parquet(W / "ev.parquet")
    print(bt.shape)
