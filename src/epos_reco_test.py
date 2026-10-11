"""Prueba de las recomendaciones con EPOS (foto sep-26). Sin consenso: referencias = base de las reglas.

A) EANs jóvenes en Central (6–17 meses en el corte, lanzados desde jul-24): ¿de dónde parto?
   - "Año pasado": envío del mismo periodo del año anterior (base de la regla de fragancias; en 12–17 meses cae en el Local).
   - "Media 6M envío": media de los últimos 6 meses de envío × 6 (base de la regla de makeup, plana).
   - "Media de las dos": media de "Media 6M envío" y "EPOS × relación" (coalición).
   - "EPOS × relación": venta al consumidor de los últimos 6 meses, quitada la temporada (perfil EPOS de la categoría,
     FY25), × temporada de los 6 meses siguientes adelantada 3 meses (el envío va 3 meses antes que la venta) ×
     envío/EPOS de su categoría en Central (meses 6–17, de lanzamientos anteriores al corte).
B) EANs veteranos (18+ meses): ¿a quién sigo? Base = envío del año pasado × (1 + trend):
   - trend envíos 12M de la casa (como la regla, sin tamaño), tope ±30%;
   - trend EPOS 6M de los veteranos de su casa, tope ±30%;
   - trend EPOS 6M propio, tope ±30%.
Cortes: A oct-25 → feb-26 (6 meses siguientes hasta ago-26); B ene → mar-26.
Error = Σ|forecast − real| / Σ real del total de 6 meses por EAN; desvío = Σ forecast / Σ real − 1.
Salida: work/results/epos_reco_test.md
"""
import numpy as np
import pandas as pd
from pathlib import Path
import epos_diag
import epos_patrones as P

ROOT = Path(__file__).resolve().parents[1]
H = 6


def profile(E, A):
    """Peso de cada mes calendario en el EPOS de la categoría (FY25). 1 = mes medio."""
    f = pd.date_range("2024-07-01", periods=12, freq="MS")
    out = {}
    for c in ["Fragancias", "Makeup"]:
        v = E.loc[A.cat == c, f].sum()
        out[c] = pd.Series((v / v.mean()).values, index=f.month)
    return out


def age_ratio(S, E, A, L, t):
    """Envío/EPOS en meses 6–17 de lanzamientos con datos antes del corte t (sin mirar el futuro)."""
    out = {}
    for c in ["Fragancias", "Makeup"]:
        s = e = 0.0
        for ean in L.index[(L >= "2024-07-01") & (A.cat == c)]:
            j, ej = S.columns.get_loc(L[ean]), E.columns.get_loc(L[ean])
            for k in range(6, 18):
                m = L[ean] + pd.DateOffset(months=k)
                if m < t and j + k < S.shape[1] and ej + k < E.shape[1]:
                    s += S.loc[ean].iat[j + k]; e += E.loc[ean].iat[ej + k]
        out[c] = s / e if e > 0 else np.nan
    return out


def score(df, cols):
    rows = []
    for c, g in df.groupby("cat"):
        for k in cols:
            rows.append({"Categoría": c, "Base": k, "EAN×corte": len(g),
                         "Error EAN (6M)": (g[k] - g.real).abs().sum() / g.real.sum(), "Desvío": g[k].sum() / g.real.sum() - 1})
    return pd.DataFrame(rows)


def test_young(S, E, A, L, prof):
    rows = []
    for t in pd.date_range("2025-10-01", "2026-02-01", freq="MS"):
        ratio = age_ratio(S, E, A, L, t)
        j = S.columns.get_loc(t)
        fut = [t + pd.DateOffset(months=k) for k in range(H)]
        past = [t - pd.DateOffset(months=k) for k in range(1, 7)]
        for ean in L.index[(L >= "2024-07-01")]:
            age = (t.year - L[ean].year) * 12 + t.month - L[ean].month
            if not 6 <= age <= 17:
                continue
            c = A.cat[ean]
            real = S.loc[ean, fut].sum()
            ep = E.loc[ean, [m for m in past if m in E.columns]]
            if ep.sum() <= 0:
                continue
            lvl = (ep / prof[c].reindex(ep.index.month).values).mean()
            seas = sum(prof[c][(m + pd.DateOffset(months=3)).month] for m in fut)
            rows.append({"cat": c, "edad": "6–11" if age < 12 else "12–17", "real": real,
                         "Año pasado": S.loc[ean, [m - pd.DateOffset(years=1) for m in fut]].sum(),
                         "Media 6M envío": S.loc[ean, past].mean() * H,
                         "EPOS × relación": lvl * seas * ratio[c]})
    return pd.DataFrame(rows)


def test_vet(S, E, A, L):
    rows = []
    vet_all = (L <= "2024-01-01")
    for t in pd.date_range("2026-01-01", "2026-03-01", freq="MS"):
        fut = [t + pd.DateOffset(months=k) for k in range(H)]
        ly = [m - pd.DateOffset(years=1) for m in fut]
        w12 = lambda X, off: X[[t - pd.DateOffset(months=k + off) for k in range(1, 13)]].sum(axis=1)
        w6 = lambda X, off: X[[t - pd.DateOffset(months=k + off) for k in range(1, 7)]].sum(axis=1)
        cen = S[[t - pd.DateOffset(months=k) for k in range(1, 7)]].gt(0).any(axis=1) & (L <= t - pd.DateOffset(months=6))
        g_house = (w12(S[cen], 0).groupby(A.house[cen]).sum() / w12(S[cen], 12).groupby(A.house[cen]).sum() - 1).clip(-.3, .3)
        v = vet_all & cen
        g_vet = (w6(E[v], 0).groupby(A.house[v]).sum() / w6(E[v], 12).groupby(A.house[v]).sum() - 1).clip(-.3, .3)
        e6, e6l = w6(E, 0), w6(E, 12)
        for ean in A.index[vet_all & cen]:
            base = S.loc[ean, ly].sum(); real = S.loc[ean, fut].sum()
            if base <= 0 or e6l[ean] <= 0:
                continue
            h = A.house[ean]
            rows.append({"cat": A.cat[ean], "real": real,
                         "Trend envíos casa": base * (1 + g_house[h]),
                         "Trend EPOS veteranos casa": base * (1 + g_vet[h]),
                         "Trend EPOS propio": base * (1 + np.clip(e6[ean] / e6l[ean] - 1, -.3, .3))})
    return pd.DataFrame(rows)


def main():
    S, E, A = epos_diag.panel()
    L = P.launches(S)
    prof = profile(E, A)
    ya = test_young(S, E, A, L, prof)
    ya["Media de las dos"] = (ya["Media 6M envío"] + ya["EPOS × relación"]) / 2
    cols = ["Año pasado", "Media 6M envío", "EPOS × relación", "Media de las dos"]
    out = ["# Prueba de recomendaciones con EPOS (foto sep-26)\n",
           "## A) Jóvenes en Central (6–17 meses): ¿de dónde parto?\n",
           score(ya, cols).to_markdown(index=False, floatfmt=".0%"), ""]
    for e_, g in ya.groupby("edad"):
        out += [f"### Edad {e_} meses\n", score(g, cols).to_markdown(index=False, floatfmt=".0%"), ""]
    vb = test_vet(S, E, A, L)
    out += ["## B) Veteranos (18+ meses): ¿a quién sigo? (base = envío del año pasado)\n",
            score(vb, ["Trend envíos casa", "Trend EPOS veteranos casa", "Trend EPOS propio"]).to_markdown(index=False, floatfmt=".0%")]
    p = ROOT / "work" / "results" / "epos_reco_test.md"
    p.write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
