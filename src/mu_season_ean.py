"""Estacionalidad EAN a EAN: makeup (GUMU, KYMU) vs fragancias como referencia.
Para cada EAN con 3 años fiscales completos (FY24-FY26) y volumen suficiente:
 - correlación del perfil mensual entre años,
 - % de la variación mes a mes que explica el mes del calendario (R²) y si es significativo (test de permutación),
 - prueba fuera de muestra: ¿el reparto mensual de FY25 predice el de FY26 mejor que un reparto plano (1/12)?
 - índice de diciembre y mes pico.
-> work/results/mu_season_ean.md"""
import numpy as np, pandas as pd
from pathlib import Path
W = Path(__file__).resolve().parents[1] / "work"
FYS = {"FY24": ("2023-07-01", "2024-06-01"), "FY25": ("2024-07-01", "2025-06-01"), "FY26": ("2025-07-01", "2026-06-01")}
RNG = np.random.default_rng(7)


def shares(H):
    """dict FY -> DataFrame (ean x 12) de pesos mensuales (suman 1)."""
    out = {}
    for fy, (a, b) in FYS.items():
        X = H.loc[:, pd.date_range(a, b, freq="MS")].fillna(0).values
        out[fy] = X
    return out


def analyse(H, min_month=50):
    X = shares(H)
    tot = {fy: x.sum(1) for fy, x in X.items()}
    ok = np.all([tot[fy] >= 12 * min_month for fy in FYS], axis=0)
    rows = []
    for i in np.where(ok)[0]:
        P = np.stack([X[fy][i] / tot[fy][i] for fy in FYS])  # 3 x 12
        corr = np.mean([np.corrcoef(P[a], P[b])[0, 1] for a, b in [(0, 1), (0, 2), (1, 2)]])
        D = P - 1 / 12
        def r2(M):
            mean_m = M.mean(0)
            return (3 * ((mean_m - 1 / 12) ** 2).sum()) / ((M - 1 / 12) ** 2).sum()
        r2_obs = r2(P)
        perm = np.array([r2(np.stack([RNG.permutation(p) for p in P])) for _ in range(300)])
        pval = (perm >= r2_obs).mean()
        err_seas = np.abs(P[2] - P[1]).sum(); err_flat = np.abs(P[2] - 1 / 12).sum()
        idx = P.mean(0) * 12
        rows.append(dict(ean=H.index[i], vol=sum(tot[fy][i] for fy in FYS), corr=corr, r2=r2_obs, pval=pval,
                         seasonal_gana=err_seas < err_flat, mejora_vs_plano=1 - err_seas / err_flat,
                         dic=idx[5], pico=["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"][idx.argmax()],
                         pico_idx=idx.max()))
    return pd.DataFrame(rows)


def summary(R, label):
    w = R.vol / R.vol.sum()
    return pd.Series({
        "EANs analizados": len(R),
        "corr. media entre años (pond. volumen)": (R["corr"] * w).sum(),
        "% EANs corr > 0,5": (R["corr"] > 0.5).mean(),
        "% EANs estacionalidad significativa (p<0,05)": (R.pval < 0.05).mean(),
        "% volumen con estacionalidad significativa": w[R.pval < 0.05].sum(),
        "% EANs donde el reparto del año pasado predice mejor que plano": R.seasonal_gana.mean(),
        "% volumen donde predice mejor que plano": w[R.seasonal_gana].sum(),
        "índice diciembre medio (1 = mes medio)": (R.dic * w).sum(),
    }, name=label)


def main():
    # makeup
    d = pd.read_parquet(W / "mu.parquet"); v = d[d.version == "2026-09"]
    Hm = v[v.date <= "2026-06-01"].pivot_table(index="ean", columns="date", values="cons", aggfunc="sum")
    am = v.groupby("ean").agg(fam=("fam", "first"), brand=("brand", "first"), desc=("desc", "first"))
    # fragancias (referencia)
    Hf = pd.read_pickle(W / "hist.pkl"); af = pd.read_pickle(W / "attr.pkl")
    Hf = Hf[(af.house != "Kylie Makeup").reindex(Hf.index).values]
    res = {}
    for lab, H in [("Gucci Make up", Hm[am.fam.reindex(Hm.index).values == "GUMU"]), ("Kylie Makeup", Hm[am.fam.reindex(Hm.index).values == "KYMU"]),
                   ("Fragancias (referencia)", Hf)]:
        res[lab] = analyse(H)
    S = pd.concat([summary(R, k) for k, R in res.items()], axis=1)
    L = ["# Estacionalidad EAN a EAN (src/mu_season_ean.py)\n",
         "EANs con FY24, FY25 y FY26 completos y >= 50 u/mes de media en cada año. Envíos = última foto.",
         "Significativa = el mes del calendario explica más variación de la que saldría barajando los meses al azar (p<0,05, 300 permutaciones).",
         "Predice mejor = el reparto mensual de FY25 acierta el reparto de FY26 mejor que repartir plano (1/12 por mes).\n",
         S.T.round(3).to_markdown()]
    # makeup por función
    R = pd.concat([res["Gucci Make up"].assign(fam="GUMU"), res["Kylie Makeup"].assign(fam="KYMU")])
    R["brand"] = am.brand.reindex(R.ean).values
    g = R.groupby(["fam", "brand"]).apply(lambda x: pd.Series(dict(n=len(x), corr=np.average(x["corr"], weights=x.vol),
                                                                   sig=(x.pval < 0.05).mean(), predice=x.seasonal_gana.mean(),
                                                                   dic=np.average(x.dic, weights=x.vol))))
    L += ["\n## Makeup por función\n", g.round(2).to_markdown()]
    # top EANs makeup con estacionalidad significativa
    top = R[R.pval < 0.05].sort_values("vol", ascending=False).head(15)
    top["desc"] = am.desc.reindex(top.ean).values
    L += ["\n## EANs de makeup con estacionalidad significativa (top 15 por volumen)\n",
          top[["fam", "desc", "vol", "corr", "pval", "pico", "pico_idx", "dic", "seasonal_gana"]].round(2).to_markdown(index=False)]
    L += ["\n## Picos más frecuentes (makeup, todos los EANs analizados)\n", R.pico.value_counts().to_frame("EANs").to_markdown()]
    (W / "results" / "mu_season_ean.md").write_text("\n".join(L))
    pd.set_option("display.width", 250)
    print(S.round(3).to_string()); print(g.round(2).to_string()); print(R.pico.value_counts().to_string())
    print(top[["fam", "desc", "vol", "corr", "pval", "pico", "dic"]].round(2).to_string())


if __name__ == "__main__":
    main()
