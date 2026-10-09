"""Backtest por FOTO real: en cada versión S&OP (2025-09, 2025-12, 2026-03, 2026-06) uso SOLO los datos de esa foto
(histórico en perímetro nuevo truncado a la fecha de la foto; consenso viejo x factor del mes calendario), aplico reglas simples (replicables en Excel) a distintos
niveles y comparo los 8 meses siguientes (sin el mes en curso) contra la verdad (última foto).

Universo: sin EANs Local (clasificación última foto) y sin forecast manual (isf>=1 en esa foto).
Salida: work/snap_fc.parquet (forecasts largos) y work/results/snapshots.md
"""
import sys
import itertools
import numpy as np
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import methods as mt  # noqa
from ptype import add_types  # noqa
from evaluate import fq  # noqa

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"
SNAPS = ["2025-09", "2025-12", "2026-03", "2026-06"]
SCALE = {"2025-09": 1.20, "2025-12": 1.20, "2026-03": 1.0, "2026-06": 1.0}
MONTHS = pd.date_range("2023-07-01", "2027-06-01", freq="MS")
LEVELS = ["ean", "pline", "house_ptype", "brand", "house", "total"]


def month_factors(d):
    """Factor de reexpresión por mes calendario (versión 2026-03 / 2025-12), media de los meses cerrados comunes."""
    p = d[d.version.isin(["2025-12", "2026-03"]) & (d.date < "2025-12-01")].pivot_table(
        index="date", columns="version", values="act", aggfunc="sum")
    r = p["2026-03"] / p["2025-12"]
    return r.groupby(r.index.month).mean()


def snapshot_ctx(d, v, attr_latest, truth, mfac):
    x = d[d.version == v]
    V = pd.Timestamp(v + "-01")
    m = MONTHS.get_loc(V)
    isf = x.groupby("ean").isf.max()
    eans = sorted(set(x.ean))
    eans = [e for e in eans if e in attr_latest.index and attr_latest.resp.get(e) != "Local" and not (isf.get(e, 0) >= 1)]
    # histórico: perímetro nuevo (última foto) truncado a la fecha de la foto = lo que se sabía, en perímetro homogéneo
    hist = truth.reindex(index=eans, columns=MONTHS)
    past = np.broadcast_to(np.arange(len(MONTHS))[None, :] < m, hist.shape)
    filled = hist.fillna(0.0).where(pd.DataFrame(past, index=eans, columns=MONTHS), np.nan)
    started = filled.fillna(0).cumsum(axis=1) > 0
    H = filled.where(started).values
    E = x.pivot_table(index="ean", columns="date", values="epos", aggfunc="sum").reindex(index=eans, columns=MONTHS)
    Ev = E.values.copy(); Ev[:, m:] = np.nan
    st = np.nan_to_num(Ev).cumsum(1) > 0
    Ev = np.where(st, np.nan_to_num(Ev), np.nan); Ev[:, MONTHS < "2024-07-01"] = np.nan
    attr = attr_latest.reindex(eans).copy()
    attr["ean"] = attr.index; attr["total"] = "TOTAL"
    cons = x[(x.date > V)].pivot_table(index="ean", columns="date", values="cons", aggfunc="sum").reindex(index=eans, columns=MONTHS).fillna(0)
    if SCALE[v] != 1.0:  # consenso en perímetro viejo -> factor del mes calendario
        cons = cons * np.array([mfac.get(c.month, 1.2) for c in MONTHS])[None, :]
    cons = cons.values
    ctx = dict(H=H, E=Ev, C=np.zeros_like(H), attr=attr, months=MONTHS, eans=np.array(eans))
    ctx["season_idx"] = mt.seasonal_index(H, m, attr.house.values, MONTHS, horizon=0)
    A = truth.reindex(index=eans, columns=MONTHS).values
    return ctx, m, cons, A


def ytd_window(V):
    return (V.month - 7) % 12  # meses cerrados del FY en curso


def rules(ctx, m, cons, V):
    """Devuelve dict nombre -> matriz n x 8."""
    H = ctx["H"]; attr = ctx["attr"]
    base = np.clip(mt._ly(H, m), 0, None)
    out = {"naive(LY)": base, "consenso_foto": cons[:, m + 1:m + 9]}
    wins = {"3M": 3, "6M": 6, "12M": 12, "YTD": max(ytd_window(V), 1)}
    for lvl, (wn, w) in itertools.product(LEVELS, wins.items()):
        keys = attr[lvl].values
        g = mt._group_g(H, m, w, keys) if lvl != "ean" else mt.g_flat(H, m, w)
        g = np.where(np.isfinite(g), g, 0.0)
        out[f"trend{wn}@{lvl}"] = np.clip(base * (1 + g)[:, None], 0, None)
        out[f"trend{wn}@{lvl}|tope30"] = np.clip(base * (1 + np.clip(g, -.3, .3))[:, None], 0, None)
        out[f"trend{wn}@{lvl}|medio"] = np.clip(base * (1 + 0.5 * g)[:, None], 0, None)
    # EPOS
    for lvl, w in itertools.product(["ean", "brand", "house", "total"], [3, 6]):
        keys = attr[lvl].values
        E = ctx["E"]
        if lvl == "ean":
            g = mt.g_flat(E, m, w)
        else:
            mask = np.isfinite(E[:, m - w - 12]) if m - w - 12 >= 0 else None
            g = mt._group_g(E, m, w, keys, mask)
        if np.isfinite(g).sum() == 0:
            continue
        g = np.where(np.isfinite(g), g, 0.0)
        out[f"EPOS{w}M@{lvl}"] = np.clip(base * (1 + g)[:, None], 0, None)
    # base suavizada (reparto) con trend 12M house/brand/house_ptype con tope
    for lvl in ["house", "brand", "house_ptype", "total"]:
        f = mt.make_resc_general(w=12, cap=(-0.3, 0.3), level=lvl)
        out[f"suavizado+trend12M@{lvl}|tope30"] = f(ctx, m)
    # mezcla consenso / estadístico
    st = out["suavizado+trend12M@house|tope30"]
    out["mix50(consenso,suav12M@house)"] = 0.5 * np.nan_to_num(st) + 0.5 * out["consenso_foto"]
    return out


def main():
    d = pd.read_parquet(W / "data.parquet")
    attr = add_types(pd.read_pickle(W / "attr.pkl"))
    truth = pd.read_pickle(W / "hist.pkl")
    mfac = month_factors(d)
    print("factores por mes:", mfac.round(3).to_dict())
    rows = []
    for v in SNAPS:
        V = pd.Timestamp(v + "-01")
        ctx, m, cons, A = snapshot_ctx(d, v, attr, truth, mfac)
        R = rules(ctx, m, cons, V)
        tg = MONTHS[m + 1:m + 9]
        Am = A[:, m + 1:m + 9]
        age = ((V.year - attr.first_sale.reindex(ctx["eans"]).dt.year) * 12 + V.month - attr.first_sale.reindex(ctx["eans"]).dt.month).values
        for name, F in R.items():
            F = np.where(np.isfinite(F), F, np.nan_to_num(R["naive(LY)"]))
            for k in range(8):
                if tg[k] > truth.columns[-1]:
                    continue
                rows.append(pd.DataFrame(dict(snap=v, rule=name, ean=ctx["eans"], lag=k + 1, target=tg[k], F=F[:, k],
                                              A=np.nan_to_num(Am[:, k]), age=age)))
        print(v, len(R), "reglas", flush=True)
    fc = pd.concat(rows, ignore_index=True)
    for c in ["house", "brand", "pline", "ptype", "house_ptype"]:
        fc[c] = attr[c].reindex(fc.ean).values
    fc["fq"] = fq(fc.target).values
    fc["mature"] = fc.age >= 18
    fc.to_parquet(W / "snap_fc.parquet")
    print(fc.shape)


if __name__ == "__main__":
    main()
