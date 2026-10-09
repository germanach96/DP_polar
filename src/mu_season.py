"""Estacionalidad makeup (GUMU, KYMU): peso de cada mes calendario por año fiscal, estabilidad entre años,
fuerza de la estacionalidad (envíos y EPOS). Verdad = foto 2026-09. -> work/results/mu_season.md"""
import numpy as np, pandas as pd
from pathlib import Path
W = Path(__file__).resolve().parents[1] / "work"


def panel():
    d = pd.read_parquet(W / "mu.parquet")
    v = d[d.version == "2026-09"]
    last = pd.Timestamp("2026-08-01")
    H = v[v.date <= last].pivot_table(index="ean", columns="date", values="cons", aggfunc="sum")
    E = v.pivot_table(index="ean", columns="date", values="epos", aggfunc="sum")
    attr = v.groupby("ean").agg(fam=("fam", "first"), brand=("brand", "first"), pline=("pline", "first"), desc=("desc", "first"))
    return H, E, attr


def profile(M, attr, by):
    g = M.fillna(0).groupby(attr[by].reindex(M.index).values).sum().T
    g.index = pd.DatetimeIndex(g.index)
    g["FY"] = [f"FY{(x.year + (x.month >= 7)) % 100}" for x in g.index]
    res = {}
    for fy, x in g.groupby("FY"):
        x = x.drop(columns="FY")
        if len(x) == 12:
            s = x / x.sum(); s.index = s.index.month
            res[fy] = s
    return res


def strength(res):
    """Para cada grupo: correlación de perfiles entre años, rango del índice medio, y % de varianza mensual explicada por el perfil medio."""
    out = {}
    groups = list(next(iter(res.values())).columns)
    for gname in groups:
        P = pd.DataFrame({fy: r[gname] for fy, r in res.items()})
        idx = P.mean(1) * 12
        corr = P.corr().values[np.triu_indices(P.shape[1], 1)].mean() if P.shape[1] > 1 else np.nan
        resid = (P.sub(P.mean(1), axis=0)).values.ravel(); tot = (P - 1 / 12).values.ravel()
        out[gname] = dict(corr_entre_años=corr, indice_min=idx.min(), indice_max=idx.max(),
                          mes_pico=int(idx.idxmax()), mes_valle=int(idx.idxmin()),
                          var_explicada=1 - (resid ** 2).sum() / (tot ** 2).sum())
    return pd.DataFrame(out).T


def main():
    H, E, attr = panel()
    L = ["# Estacionalidad makeup (src/mu_season.py)\n",
         "Índice = peso del mes en el FY x 12 (1 = mes medio). corr_entre_años: correlación media de los perfiles mensuales entre FYs.",
         "var_explicada: cuánto de la diferencia entre meses repite el patrón medio (1 = estacionalidad perfecta, 0 = ruido).\n"]
    for name, M in [("ENVÍOS", H), ("EPOS", E.reindex(columns=pd.date_range("2024-07-01", "2026-06-01", freq="MS")))]:
        for by in ["fam", "brand"]:
            res = profile(M, attr, by)
            if not res:
                continue
            S = strength(res)
            L += [f"\n## {name} — por {by}: fuerza de la estacionalidad\n", S.round(2).to_markdown()]
            if by == "fam":
                for fy, r in res.items():
                    L += [f"\n### {name} {fy}: índice mensual (peso x 12)\n", (r * 12).T.round(2).to_markdown()]
    (W / "results" / "mu_season.md").write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
