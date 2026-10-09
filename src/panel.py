"""Construye el panel EAN x mes (fuente de verdad = última versión) y los snapshots de consenso.

Decisiones (ver work/NOTES.md):
- Histórico = 'Consensus - Final' de la última versión para meses ya cerrados (== Actuals; además
  cubre 2023.M07-M08, donde la última versión ya no trae Actuals).
- El mes de la versión es parcial -> se excluye.
- Antes de la primera venta del EAN = NaN (no lanzado); después, mes sin dato = 0.
"""
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST = "2026-09"


def build():
    d = pd.read_parquet(ROOT / "work" / "data.parquet")
    v = d[d.version == LATEST].copy()
    last_closed = pd.Timestamp(LATEST + "-01") - pd.offsets.MonthBegin(1)
    months = pd.date_range("2023-07-01", last_closed, freq="MS")

    hist = v[v.date <= last_closed].pivot_table(index="ean", columns="date", values="cons", aggfunc="sum")
    hist = hist.reindex(columns=months)
    eans = sorted(set(v.ean))
    hist = hist.reindex(eans)
    filled = hist.fillna(0.0)
    started = (filled.cumsum(axis=1) > 0)
    hist = filled.where(started)  # NaN antes del lanzamiento

    def piv(col, frame=v):
        return frame.pivot_table(index="ean", columns="date", values=col, aggfunc="sum").reindex(index=eans)

    cuts = piv("cuts").reindex(columns=months).fillna(0.0)
    epos = piv("epos")

    # atributos
    resp = d.groupby(["version", "ean"]).resp.agg(lambda s: "/".join(sorted(s.dropna().unique()))).unstack(0)
    attr = v.groupby("ean").agg(house=("house", "first"), brand=("brand", "first"), pline=("pline", "first"),
                                desc=("desc", "first"), isf=("isf", "max")).reindex(eans)
    attr["resp"] = resp[LATEST].reindex(eans).replace("", np.nan)
    attr["resp_2603"] = resp["2026-03"].reindex(eans).replace("", np.nan)
    attr["category"] = np.where(attr.house == "Kylie Makeup", "Makeup", "Fragrance")
    attr["first_sale"] = hist.apply(lambda r: r.first_valid_index(), axis=1)

    # snapshots de consenso: para cada versión, consenso de meses futuros (>= mes versión)
    snaps = d[d.date >= d.vdate].pivot_table(index=["version", "ean"], columns="date", values="cons", aggfunc="sum")
    da = d[d.date >= d.vdate].pivot_table(index=["version", "ean"], columns="date", values="da", aggfunc="sum")
    # fx futuro (última versión)
    fut = v[v.date > last_closed].pivot_table(index="ean", columns="date", values="cons", aggfunc="sum").reindex(eans)

    out = ROOT / "work"
    hist.to_pickle(out / "hist.pkl"); cuts.to_pickle(out / "cuts.pkl"); epos.to_pickle(out / "epos.pkl")
    attr.to_pickle(out / "attr.pkl"); snaps.to_pickle(out / "snaps.pkl"); da.to_pickle(out / "da_snaps.pkl")
    fut.to_pickle(out / "fut_latest.pkl")
    return hist, cuts, epos, attr, snaps


if __name__ == "__main__":
    h, c, e, a, s = build()
    print(h.shape, a.resp.value_counts(dropna=False).to_dict())
    print(h.sum().round(0).tail(14))
