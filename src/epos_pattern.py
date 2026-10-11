"""¿Hay un patrón constante entre envíos y EPOS? (foto sep-26)

Pregunta del usuario: "los envíos subieron, el EPOS se mantuvo → los envíos bajaron los meses siguientes".

Para cada EAN (18+ meses, con EPOS) y cada mes de corte t (sep-25 → may-26):
- Envío ahora  = envío de t-2..t frente al mismo trimestre del año anterior (YoY 3M).
- EPOS ahora   = lo mismo con el EPOS.
- Envío después = envío de t+1..t+3 frente al año anterior.
- EPOS después  = lo mismo con el EPOS (si ya existe: hasta jul-26).
Comparar YoY quita la temporada (el EPOS repite su forma cada año).

Se agrupa por situación (envío y EPOS: sube > +15%, plano, baja < −15%) y se suma el volumen de
cada grupo (Σ después / Σ año anterior − 1), para que los EANs pequeños no hagan ruido.

Salida: work/results/epos_pattern.md
"""
import numpy as np
import pandas as pd
from pathlib import Path
import epos_diag

ROOT = Path(__file__).resolve().parents[1]
TH = 0.15            # umbral de "sube" / "baja"
MIN_LY = 300         # unidades mínimas del trimestre del año anterior (evita EANs diminutos)
ORIGINS = pd.date_range("2025-09-01", "2026-05-01", freq="MS")


def win(X, t, a, b):
    """Suma de los meses t+a..t+b (incluidos) si existen; NaN si falta alguno."""
    cols = [t + pd.DateOffset(months=k) for k in range(a, b + 1)]
    if not all(c in X.columns for c in cols):
        return pd.Series(np.nan, index=X.index)
    return X[cols].sum(axis=1)


def events(S, E, A):
    rows = []
    started = S.gt(0).cumsum(axis=1)
    for t in ORIGINS:
        age = started[t] if t in started.columns else None
        d = pd.DataFrame({
            "cat": A.cat, "house": A.house,
            "s_now": win(S, t, -2, 0), "s_now_ly": win(S, t, -14, -12),
            "e_now": win(E, t, -2, 0), "e_now_ly": win(E, t, -14, -12),
            "s_next": win(S, t, 1, 3), "s_next_ly": win(S, t, -11, -9),
            "e_next": win(E, t, 1, 3), "e_next_ly": win(E, t, -11, -9)})
        ok = (age >= 18) & (d.s_now_ly >= MIN_LY) & (d.e_now_ly > 0) & (d.s_next_ly >= MIN_LY) & (d.e_now > 0)
        d = d[ok].copy(); d["t"] = t
        rows.append(d)
    d = pd.concat(rows)
    d["gs"] = d.s_now / d.s_now_ly - 1
    d["ge"] = d.e_now / d.e_now_ly - 1
    lab = lambda g: np.where(g > TH, "sube", np.where(g < -TH, "baja", "plano"))
    d["env"] = lab(d["gs"]); d["epos"] = lab(d["ge"])
    gap = d["gs"] - d["ge"]
    d["canal"] = np.where(gap > 2 * TH, "Carga (envío > EPOS)", np.where(gap < -2 * TH, "Descarga (envío < EPOS)", "Alineado"))
    return d


def agg(g):
    out = {"EAN×mes": len(g), "% volumen": g.s_next_ly.sum(),
           "Envío ahora": g.s_now.sum() / g.s_now_ly.sum() - 1,
           "EPOS ahora": g.e_now.sum() / g.e_now_ly.sum() - 1,
           "Envío después": g.s_next.sum() / g.s_next_ly.sum() - 1}
    e = g.dropna(subset=["e_next"])
    out["EPOS después"] = e.e_next.sum() / e.e_next_ly.sum() - 1 if len(e) else np.nan
    # qué parte de los EANs baja sus envíos frente a lo que hacía su EPOS
    out["% EANs con envío después < EPOS ahora"] = ((g.s_next / g.s_next_ly - 1) < g["ge"]).mean()
    return pd.Series(out)


def table(d, by):
    t = d.groupby(by).apply(agg)
    t["% volumen"] = t["% volumen"] / d.s_next_ly.sum()
    return t


def constancy(d, by=None):
    """Por mes de corte: envío después de los EANs en carga, alineados y en descarga. ¿Se cumple el orden?"""
    rows = []
    keys = [by] if by else []
    for k, g in d.groupby(keys + ["t"]):
        r = {}
        for c, gg in g.groupby("canal"):
            r[c] = gg.s_next.sum() / gg.s_next_ly.sum() - 1 if len(gg) >= 5 else np.nan
        r["key"] = k
        rows.append(r)
    t = pd.DataFrame(rows)
    C, A_, D = "Carga (envío > EPOS)", "Alineado", "Descarga (envío < EPOS)"
    t["carga < alineado"] = t[C] < t[A_]
    t["descarga > alineado"] = t[D] > t[A_]
    return t


def regress(d):
    import statsmodels.formula.api as smf
    out = []
    d = d.assign(gs_c=d.gs.clip(-1, 3), ge_c=d["ge"].clip(-1, 3),
                 gn=(d.s_next / d.s_next_ly - 1).clip(-1, 3))
    for c, g in d.groupby("cat"):
        r = smf.wls("gn ~ gs_c + ge_c", data=g, weights=g.s_next_ly).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(g.index)[0]})
        out.append(f"- {c}: envío después = {r.params['Intercept']:+.2f} {r.params['gs_c']:+.2f}×envío ahora "
                   f"(±{r.bse['gs_c']:.2f}) {r.params['ge_c']:+.2f}×EPOS ahora (±{r.bse['ge_c']:.2f}); R² {r.rsquared:.2f}")
    return out


def load_build(Sx, Ex, keys, minv):
    """Carga acumulada: envío/EPOS de los últimos 12M frente al de FY25 (jul-24 → jun-25).
    Resultado: envío − EPOS (YoY) de los 3 meses siguientes."""
    ref_t = pd.Timestamp("2025-06-01")
    ref = win(Sx, ref_t, -11, 0) / win(Ex, ref_t, -11, 0)
    rows = []
    for t in pd.date_range("2025-09-01", "2026-04-01", freq="MS"):
        e12 = win(Ex, t, -11, 0)
        R = win(Sx, t, -11, 0) / e12
        sn, snl, en, enl = win(Sx, t, 1, 3), win(Sx, t, -11, -9), win(Ex, t, 1, 3), win(Ex, t, -11, -9)
        d = pd.DataFrame({"dev": R / ref - 1, "g_s": sn / snl - 1, "g_e": en / enl - 1, "w": snl, "key": keys})
        d["t"] = t
        rows.append(d[(snl >= minv) & (enl > 0) & (e12 > 0) & np.isfinite(d.dev)])
    d = pd.concat(rows)
    d["exc"] = (d.g_s - d.g_e).clip(-1, 2)
    d["dev"] = d.dev.clip(-.6, 1.5)
    return d


def load_section(S, E, A):
    import statsmodels.formula.api as smf
    has = E.sum(axis=1) > 0
    Sh, Eh = S[has].groupby(A.house[has]).sum(), E[has].groupby(A.house[has]).sum()
    h = load_build(Sh, Eh, Sh.index.to_series(), 0)
    mm = lambda c: c.strftime("%b%y")
    L = ["## 5. Carga acumulada en 12 meses (envío/EPOS 12M frente a FY25)\n",
         "### Por casa: desvío del ratio (positivo = canal más cargado que en FY25)\n",
         h.pivot_table(index="key", columns="t", values="dev").rename(columns=mm).to_markdown(floatfmt="+.0%"),
         "\n### Por casa: envío − EPOS de los 3 meses siguientes (YoY, puntos)\n",
         h.pivot_table(index="key", columns="t", values="exc").rename(columns=mm).to_markdown(floatfmt="+.0%")]
    r = smf.ols("exc ~ dev", data=h).fit()
    L.append(f"\nCasa: envío − EPOS siguiente = {r.params['Intercept']:+.2f} {r.params['dev']:+.2f}×desvío "
             f"(±{r.bse['dev']:.2f}); correlación {np.corrcoef(h.dev, h.exc)[0, 1]:+.2f}; n={len(h)} casa×mes\n")
    started = S.gt(0).cumsum(axis=1)
    old = (started[pd.Timestamp("2025-06-01")] >= 12) & has
    e = load_build(S[old], E[old], A.cat[old], MIN_LY)
    L.append("### Por EAN (12+ meses en jun-25): cargado / descargado = desvío > +15% / < −15%\n")
    for c, g in e.groupby("key"):
        r = smf.wls("exc ~ dev", data=g, weights=g.w).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(g.index)[0]})
        g = g.assign(sig=np.where(g.dev > TH, "cargado", np.where(g.dev < -TH, "descargado", "normal")))
        m = g.groupby(["t", "sig"]).apply(lambda x: (x.w * x.exc).sum() / x.w.sum()).unstack().rename(index=mm)
        tot = g.groupby("sig").apply(lambda x: (x.w * x.exc).sum() / x.w.sum()).rename("Total")
        L += [f"#### {c} (coeficiente {r.params['dev']:+.2f} ± {r.bse['dev']:.2f}; R² {r.rsquared:.3f})\n",
              pd.concat([m, tot.to_frame().T]).to_markdown(floatfmt="+.0%"),
              f"\nCargado < normal en {(m.cargado < m.normal).sum()} de {len(m)} meses; "
              f"descargado > normal en {(m.descargado > m.normal).sum()} de {len(m)}.\n"]
    return L


def main():
    S, E, A = epos_diag.panel()
    d = events(S, E, A)
    pct = lambda x: f"{x:+.0%}" if isinstance(x, float) and np.isfinite(x) else ""
    L = ["# Patrón envío ↔ EPOS (foto sep-26)\n",
         f"Cortes mensuales sep-25 → may-26; trimestre móvil frente al año anterior. Sube/baja = ±{TH:.0%}. "
         f"EANs con 18+ meses y ≥{MIN_LY} uds en el trimestre del año anterior. {len(d)} EAN×mes, {d.index.nunique()} EANs.\n"]

    L += ["## 1. Las 9 situaciones (envío × EPOS) y qué pasa en los 3 meses siguientes\n"]
    for c, g in [("Total", d)] + list(d.groupby("cat")):
        t = table(g, ["env", "epos"])
        L += [f"### {c}\n", t.to_markdown(floatfmt=".0%"), ""]

    L += ["## 2. Carga / descarga del canal (envío ahora − EPOS ahora, ±30 puntos)\n"]
    for c, g in [("Total", d)] + list(d.groupby("cat")) + list(d.groupby("house")):
        L += [f"### {c}\n", table(g, "canal").to_markdown(floatfmt=".0%"), ""]

    L += ["## 3. ¿Es constante? Envío después por mes de corte\n"]
    t = constancy(d)
    L += [t.set_index("key").to_markdown(floatfmt=".0%"),
          f"\nCarga < alineado en {t['carga < alineado'].sum()} de {len(t)} meses; "
          f"descarga > alineado en {t['descarga > alineado'].sum()} de {len(t)}.\n"]
    th = constancy(d, "house")
    th["casa"] = th.key.str[0]
    s = th.groupby("casa")[["carga < alineado", "descarga > alineado"]].agg(["sum", "count"])
    L += ["Por casa (meses en que se cumple / meses):\n", s.to_markdown(), ""]

    L += ["## 4. Regresión (ponderada por volumen, error agrupado por EAN)\n"] + regress(d) + [""]
    L += load_section(S, E, A)
    out = ROOT / "work" / "results" / "epos_pattern.md"
    out.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
