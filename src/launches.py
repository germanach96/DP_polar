"""Lanzamientos (≈ EANs Local): curva de vida y precisión del consenso en lanzamientos."""
import numpy as np
import pandas as pd
from pathlib import Path

W = Path(__file__).resolve().parents[1] / "work"


def main():
    H = pd.read_pickle(W / "hist.pkl"); attr = pd.read_pickle(W / "attr.pkl"); snaps = pd.read_pickle(W / "snaps.pkl")
    months = H.columns
    L = ["# Lanzamientos (generado por src/launches.py)\n"]
    fs = attr.first_sale
    launch = attr[(fs >= "2024-01-01")].copy()
    launch["vol"] = H.loc[launch.index].sum(1)
    launch = launch[launch.vol > 500]
    L.append(f"EANs con primera venta >= 2024-01 y >500 u: {len(launch)}; Local(2026-09) entre ellos: {(launch.resp=='Local').sum()}, "
             f"Local(2026-03): {(launch.resp_2603=='Local').sum()}\n")
    # cuántos Local son lanzamientos
    loc = attr[(attr.resp == "Local") | (attr.resp_2603 == "Local")]
    L.append(f"EANs Local (2026-09 o 2026-03): {len(loc)}; con primera venta >= 2024-07: {(loc.first_sale >= '2024-07-01').sum()}; "
             f"sin ventas: {loc.first_sale.isna().sum()}\n")
    # curva: volumen mes k desde lanzamiento / volumen meses 0-2
    rows = []
    for e in launch.index:
        s = H.loc[e].dropna().values
        if len(s) < 6:
            continue
        b = s[:3].sum()
        if b <= 0:
            continue
        rows.append(pd.Series(s[:18] / b * 3, index=range(len(s[:18])), name=e))  # relativo a la media mensual de los 3 primeros meses
    C = pd.DataFrame(rows)
    q = C.quantile([0.25, 0.5, 0.75]).T
    q["n"] = C.notna().sum()
    L += ["## Curva de vida: volumen del mes k / media mensual de los 3 primeros meses\n", q.round(2).to_markdown()]
    # share primeros 3 meses vs 12 meses
    rows = []
    for e in launch.index:
        s = H.loc[e].dropna().values
        if len(s) >= 12:
            rows.append(dict(ean=e, house=attr.house[e], m0_2=s[:3].sum() / s[:12].sum(), m3_5=s[3:6].sum() / s[:12].sum(),
                             m6_11=s[6:12].sum() / s[:12].sum()))
    S = pd.DataFrame(rows)
    L += ["\n## Peso de cada tramo en el primer año (EANs con >=12 meses)\n", S.groupby("house")[["m0_2", "m3_5", "m6_11"]].median().round(3).to_markdown(),
          f"\nTotal mediana: {S[['m0_2','m3_5','m6_11']].median().round(3).to_dict()} (n={len(S)})\n"]
    # precisión del consenso en lanzamientos: para cada versión, EANs con <12 meses de vida (o sin venta) al corte
    rows = []
    for v in snaps.index.get_level_values(0).unique():
        M = pd.Timestamp(v + "-01")
        S_ = snaps.loc[v]
        tg = [M + pd.DateOffset(months=k) for k in range(1, 9) if M + pd.DateOffset(months=k) in months]
        if not tg:
            continue
        young = attr.index[(attr.first_sale.isna()) | (attr.first_sale > M - pd.DateOffset(months=12))]
        young = [e for e in young if e in S_.index]
        F = S_.reindex(young)[tg].fillna(0).sum(1); A = H.reindex(young)[tg].fillna(0).sum(1)
        df = pd.DataFrame(dict(F=F, A=A)); df = df[(df.F > 0) | (df.A > 0)]
        loc_ = df.index.isin(loc.index)
        for nm, x in [("young_all", df), ("young_local", df[loc_]), ("young_central", df[~loc_])]:
            if len(x):
                rows.append(dict(version=v, seg=nm, n=len(x), F=x.F.sum(), A=x.A.sum(), bias=x.F.sum() / x.A.sum() - 1,
                                 wmape_8m=(x.F - x.A).abs().sum() / x.A.sum(),
                                 med_ratio=(x.A / x.F.replace(0, np.nan)).median()))
    L += ["\n## Consenso en EANs jóvenes (<12m vida al corte): total 8 meses forecast vs actual\n",
          pd.DataFrame(rows).round(3).to_markdown(index=False),
          "\nbias = F/A-1 (+ = sobreforecast). wmape_8m sobre el total de 8 meses por EAN. med_ratio = mediana de A/F por EAN."]
    (W / "results" / "launches.md").write_text("\n".join(L))


if __name__ == "__main__":
    main()
