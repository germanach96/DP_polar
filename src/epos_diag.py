"""Diagnóstico de EPOS (sell-out) frente a envíos (sell-in), foto sep-26.

Preguntas:
1. Cobertura: qué parte de los envíos tiene EPOS.
2. Desfase: cuántos meses antes del pico de venta se envía (correlación de perfiles mensuales).
3. Stock en el canal: envío − EPOS acumulado por casa y año fiscal.
4. ¿Anticipa? Para cada EAN Central y origen (ene–mar-26), qué predice mejor el crecimiento
   de los envíos de los 6 meses siguientes: el crecimiento pasado de envíos, el del EPOS, o
   la "carga" (envíos crecieron más que el EPOS).

Salida: work/results/epos_diag.md
"""
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST = "2026-09"
LAST_SHIP = pd.Timestamp("2026-08-01")   # sep-26 abierto
LAST_EPOS = pd.Timestamp("2026-07-01")   # EPOS llega con un mes de retraso


def panel():
    fr = pd.read_parquet(ROOT / "work" / "data.parquet")
    fr = fr[fr.house != "Kylie Makeup"]   # 9 EANs (pinceles) repetidos en KYMU.xlsx
    d = pd.concat([fr.assign(cat="Fragancias"),
                   pd.read_parquet(ROOT / "work" / "mu.parquet").assign(cat="Makeup")], ignore_index=True)
    v = d[d.version == LATEST]
    S = v[v.date <= LAST_SHIP].pivot_table(index="ean", columns="date", values="cons", aggfunc="sum").fillna(0)
    E = v[(v.date >= "2024-07-01") & (v.date <= LAST_EPOS)].pivot_table(
        index="ean", columns="date", values="epos", aggfunc="sum").reindex(S.index).fillna(0)
    A = v.groupby("ean").agg(cat=("cat", "first"), house=("house", "first"))
    A = A.reindex(S.index)
    A["house"] = A.house.str.replace("CP-", "", regex=False)
    return S, E, A


def fy(ts):
    return f"FY{(ts.year + (ts.month >= 7)) % 100}"


def coverage(S, E, A):
    win = pd.date_range("2025-08-01", LAST_EPOS, freq="MS")
    has = E[win].sum(axis=1) > 0
    rows = []
    for h, idx in A.groupby("house").groups.items():
        s = S.loc[idx, win].sum(axis=1); e = E.loc[idx, win].sum(axis=1)
        rows.append({"Casa": h, "Categoría": A.loc[idx[0], "cat"],
                     "% envío con EPOS": s[has[idx]].sum() / s.sum(),
                     "EPOS / envío (EANs con EPOS)": e[has[idx]].sum() / s[has[idx]].sum()})
    return pd.DataFrame(rows)


def profile_lag(S, E, A):
    """Perfil mensual (peso de cada mes en el año) de envíos y EPOS por categoría; desfase que maximiza la correlación."""
    months = pd.date_range("2024-07-01", "2026-06-01", freq="MS")
    out = []
    for c, idx in A.groupby("cat").groups.items():
        has = E.loc[idx, months].sum(axis=1) > 0
        ii = has[has].index
        s = S.loc[ii, months].sum(); e = E.loc[ii, months].sum()
        sp = s.groupby(s.index.month).sum(); ep = e.groupby(e.index.month).sum()
        sp, ep = sp / sp.mean(), ep / ep.mean()
        cors = {k: np.corrcoef(np.roll(sp.values, k), ep.values)[0, 1] for k in range(0, 5)}
        best = max(cors, key=cors.get)
        out.append({"cat": c, "ship": sp, "epos": ep, "cors": cors, "best": best})
    return out


def stability(S, E, A):
    """¿Se repite el perfil mensual de un año a otro? Diferencia media absoluta FY25 vs FY26 (puntos de peso)."""
    rows = []
    for c, idx in A.groupby("cat").groups.items():
        prof = {}
        for name, X in [("Envío", S), ("EPOS", E)]:
            for f, a in [("FY25", "2024-07-01"), ("FY26", "2025-07-01")]:
                mm = pd.date_range(a, periods=12, freq="MS"); v = X.loc[idx, mm].sum(); prof[(name, f)] = (v / v.mean()).values
            d = np.abs(prof[(name, "FY25")] - prof[(name, "FY26")])
            rows.append({"Categoría": c, "Serie": name, "Cambio medio del peso mensual": d.mean(),
                         "Mayor cambio": d.max(), "Correlación FY25-FY26": np.corrcoef(prof[(name, "FY25")], prof[(name, "FY26")])[0, 1]})
    return pd.DataFrame(rows)


def channel(S, E, A):
    rows = []
    for (h), idx in A.groupby("house").groups.items():
        for f, mm in [("FY25", pd.date_range("2024-07-01", "2025-06-01", freq="MS")),
                      ("FY26", pd.date_range("2025-07-01", "2026-06-01", freq="MS"))]:
            has = E.loc[idx, mm].sum(axis=1) > 0
            ii = has[has].index
            s, e = S.loc[ii, mm].sum().sum(), E.loc[ii, mm].sum().sum()
            rows.append({"Casa": h, "FY": f, "Envío": s, "EPOS": e, "Envío − EPOS": s - e, "Envío / EPOS": s / e})
    t = pd.DataFrame(rows)
    p = t.pivot(index="Casa", columns="FY", values=["Envío", "EPOS", "Envío / EPOS"])
    yo = pd.DataFrame({"YoY envío FY26": p[("Envío", "FY26")] / p[("Envío", "FY25")] - 1,
                       "YoY EPOS FY26": p[("EPOS", "FY26")] / p[("EPOS", "FY25")] - 1,
                       "Envío/EPOS FY25": p[("Envío / EPOS", "FY25")],
                       "Envío/EPOS FY26": p[("Envío / EPOS", "FY26")]})
    return yo


def yoy(X, m, w):
    cols = X.columns
    j = cols.get_loc(m)
    a = X.iloc[:, j - w:j].sum(axis=1); b = X.iloc[:, j - w - 12:j - 12].sum(axis=1)
    return a, b


def predictive(S, E, A):
    """Origen m (ene–mar-26): crecimiento futuro de envíos (m..m+5 vs mismo período LY)."""
    res = []
    for m in pd.date_range("2026-01-01", "2026-03-01", freq="MS"):
        j = S.columns.get_loc(m)
        fut = S.iloc[:, j:j + 6].sum(axis=1); fut_ly = S.iloc[:, j - 12:j - 6].sum(axis=1)
        s6, s6ly = yoy(S, m, 6)
        Ej = E.columns.get_loc(m) if m in E.columns else None
        e6 = E.iloc[:, Ej - 6:Ej].sum(axis=1); e6ly = E.iloc[:, Ej - 18:Ej - 12].sum(axis=1)
        old = S.iloc[:, :j].gt(0).cumsum(1).iloc[:, -1] >= 18   # al menos 18 meses con envío
        ok = old & (s6ly > 0) & (e6ly > 0) & (fut_ly > 0) & (e6 > 0)
        df = pd.DataFrame({"cat": A.cat, "house": A.house, "fut_ly": fut_ly, "fut": fut,
                           "g_fut": fut / fut_ly - 1, "g_ship": s6 / s6ly - 1, "g_epos": e6 / e6ly - 1})[ok]
        df["m"] = m
        res.append(df)
    df = pd.concat(res)
    for c in ["g_fut", "g_ship", "g_epos"]:
        df[c] = df[c].clip(-.8, 1.5)
    df["carga"] = df.g_ship - df.g_epos   # envíos crecieron más que la venta al consumidor
    return df


def score(df):
    """Error del total 6M por EAN: LY × (1+g), g con tope ±30%, según la fuente del trend."""
    out = []
    srcs = {"Año pasado plano": lambda d: 0 * d.g_ship,
            "Trend envíos propio 6M": lambda d: d.g_ship,
            "Trend EPOS propio 6M": lambda d: d.g_epos,
            "Media envíos y EPOS": lambda d: (d.g_ship + d.g_epos) / 2}
    # versiones por casa (suma/suma), mismas ventanas
    for c, sub in df.groupby("cat"):
        for name, f in srcs.items():
            g = f(sub).clip(-.3, .3)
            F = sub.fut_ly * (1 + g)
            out.append({"Categoría": c, "Fuente del trend": name, "EANs×origen": len(sub),
                        "Error EAN (6M)": (F - sub.fut).abs().sum() / sub.fut.sum(),
                        "Desvío total": F.sum() / sub.fut.sum() - 1})
    return pd.DataFrame(out)


def caps(df):
    """Mismo forecast con distintos topes del trend (el tope de ±30% puede estar tapando la señal)."""
    out = []
    for c, sub in df.groupby("cat"):
        for name, g in [("Envíos", sub.g_ship), ("EPOS", sub.g_epos)]:
            row = {"Categoría": c, "Fuente": name}
            for cap in [.3, .6, 1.5]:
                F = sub.fut_ly * (1 + g.clip(-cap, cap))
                row[f"tope ±{cap:.0%}"] = (F - sub.fut).abs().sum() / sub.fut.sum()
            out.append(row)
    return pd.DataFrame(out)


def load_effect(df):
    """Efecto 'carga del canal': crecimiento futuro ~ trend envíos + (trend envíos − trend EPOS)."""
    import statsmodels.formula.api as smf
    out = []
    for c, sub in df.groupby("cat"):
        r = smf.wls("g_fut ~ g_ship + carga", data=sub, weights=sub.fut_ly).fit(cov_type="HC1")
        out.append(f"- {c}: envíos {r.params['g_ship']:+.2f} (±{r.bse['g_ship']:.2f}); "
                   f"carga {r.params['carga']:+.2f} (±{r.bse['carga']:.2f})")
    return out


def house_next(S, A):
    m = pd.date_range("2026-07-01", "2026-08-01", freq="MS"); ly = m - pd.DateOffset(years=1)
    return (S[m].sum(axis=1).groupby(A.house).sum() / S[ly].sum(axis=1).groupby(A.house).sum() - 1).rename("YoY envío jul–ago-26")


def regress(df):
    import statsmodels.formula.api as smf
    out = []
    for c, sub in df.groupby("cat"):
        w = sub.fut_ly / sub.fut_ly.mean()
        r = smf.wls("g_fut ~ g_ship + g_epos", data=sub, weights=w).fit(cov_type="HC1")
        out.append((c, len(sub), r.params, r.bse, r.rsquared))
    return out


def main():
    S, E, A = panel()
    L = ["# Diagnóstico EPOS (sell-out) vs envíos (sell-in), foto sep-26\n",
         "EPOS disponible jul-24 → jul-26 (ago-26 aún vacío). Envíos hasta ago-26.\n"]
    cov = coverage(S, E, A)
    L += ["## 1. Cobertura (ago-25 → jul-26)\n", cov.to_markdown(index=False, floatfmt=".0%"), "\n"]
    L += ["## 2. Perfil mensual (peso de cada mes; 1 = mes medio) y desfase envío → venta\n"]
    for p in profile_lag(S, E, A):
        t = pd.DataFrame({"Envío": p["ship"], "EPOS": p["epos"]}).T
        t.columns = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
        L += [f"### {p['cat']}\n", t.to_markdown(floatfmt=".2f"),
              "\nCorrelación del perfil de envíos adelantado k meses con el de EPOS: " +
              ", ".join(f"k={k}: {v:.2f}" for k, v in p["cors"].items()) + f" → mejor k={p['best']}\n"]
    L += ["### Estabilidad del perfil de un año a otro\n", stability(S, E, A).to_markdown(index=False, floatfmt=".2f"), "\n"]
    L += ["## 3. Envío frente a EPOS por casa (EANs con EPOS)\n",
          "Si los envíos crecen más que el EPOS, el canal acumula stock (o cambia la cobertura del EPOS).\n",
          pd.concat([channel(S, E, A), house_next(S, A)], axis=1).to_markdown(floatfmt=".2f"), "\n"]
    df = predictive(S, E, A)
    L += ["## 4. ¿El EPOS anticipa los envíos? (EANs con 18+ meses, orígenes ene/feb/mar-26, 6 meses siguientes)\n",
          "Forecast = envío del mismo período del año pasado × (1 + trend 6M, tope ±30%).\n",
          score(df).to_markdown(index=False, floatfmt=".1%"), "\n",
          "Regresión ponderada por volumen: crecimiento futuro de envíos ~ trend envíos 6M + trend EPOS 6M\n"]
    for c, n, pr, se, r2 in regress(df):
        L.append(f"- {c} (n={n}): intercepto {pr['Intercept']:+.2f}; envíos {pr['g_ship']:+.2f} (±{se['g_ship']:.2f}); "
                 f"EPOS {pr['g_epos']:+.2f} (±{se['g_epos']:.2f}); R² {r2:.2f}")
    L += ["\nError EAN (6M) según el tope del trend:\n", caps(df).to_markdown(index=False, floatfmt=".1%"),
          "\nCarga del canal (envíos crecieron más que el EPOS):\n"] + load_effect(df)
    out = ROOT / "work" / "results" / "epos_diag.md"
    out.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
