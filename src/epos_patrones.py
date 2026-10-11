"""Patrones envío ↔ EPOS (foto sep-26), solo en términos relativos (YoY o ratio frente a su propia historia),
porque no todos los clientes reportan EPOS.

1. Ruido: el YoY mensual de los envíos oscila mucho más que el del EPOS.
2. Tendencia: a 12 meses envío y EPOS van en la misma dirección; la tendencia del EPOS se mantiene de un semestre a otro.
3. Lanzamientos: el primer año se envía ~2× lo que se vende; el segundo, menos de lo normal.
4. Veteranos: el EPOS de los EANs con historia completa cae ~20% al año; la casa crece por los lanzamientos.
5. Carga acumulada en 12 meses (envío/EPOS vs su propia historia) y bajas de producto.

Salida: work/epos_patrones.json y work/results/epos_patrones.md. Reporte: src/epos_patrones_report.py
"""
import json
import numpy as np
import pandas as pd
from pathlib import Path
import epos_diag
import epos_pattern

ROOT = Path(__file__).resolve().parents[1]
R = lambda a, n=12: pd.date_range(a, periods=n, freq="MS")
F24, F25, F26 = R("2023-07-01"), R("2024-07-01"), R("2025-07-01")
MM = pd.date_range("2025-07-01", "2026-07-01", freq="MS")       # meses con EPOS y su año anterior
HOUSES = ["BURBERRY", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"]
NAME = {"BURBERRY": "Burberry"}


def launches(S):
    """Lanzamiento = primer mes de 2 seguidos con envío."""
    out = []
    for row in S.gt(0).values:
        k = next((j for j in range(len(row) - 1) if row[j] and row[j + 1]), None)
        out.append(S.columns[k] if k is not None else pd.NaT)
    return pd.Series(out, index=S.index)


def mature_set(S, E, L):
    d = pd.DataFrame({"s25": S[F25].sum(axis=1), "s26": S[F26].sum(axis=1), "e25": E[F25].sum(axis=1), "e26": E[F26].sum(axis=1)})
    return d.index[(d.s25 >= 500) & (d.s26 >= 500) & (d.e25 >= 200) & (d.e26 >= 200) & (L <= "2024-01-01")]


def noise(S, E, A, ii):
    ly = MM - pd.DateOffset(years=1)
    res = {"houses": {}}
    for h in HOUSES:
        g = [e for e in ii if A.house[e] == h]
        s, e = S.loc[g], E.loc[g]
        res["houses"][h] = {"ship": (s[MM].sum().values / s[ly].sum().values - 1).tolist(),
                            "epos": (e[MM].sum().values / e[ly].sum().values - 1).tolist(), "n": len(g)}
    lr = lambda X: np.std(np.log((X.loc[ii, MM].values + 1) / (X.loc[ii, ly].values + 1)), axis=1)
    ns, ne = pd.Series(lr(S), index=ii), pd.Series(lr(E), index=ii)
    res["months"] = [m.strftime("%b-%y") for m in MM]
    res["ruido"] = {h: {"ship": float(ns[A.house[ii] == h].median()), "epos": float(ne[A.house[ii] == h].median())} for h in HOUSES}
    res["pct_env_mas_ruidoso"] = float((ns > ne).mean())
    res["ratio_ruido"] = float((ns / ne).median())
    # amplitud de la casa: rango del YoY mensual
    res["rango"] = {h: {"ship": float(np.ptp(v["ship"])), "epos": float(np.ptp(v["epos"]))} for h, v in res["houses"].items()}
    return res


def trend(S, E, A, ii, L):
    d = pd.DataFrame({"cat": A.cat[ii], "house": A.house[ii],
                      "ys": S.loc[ii, F26].sum(axis=1) / S.loc[ii, F25].sum(axis=1) - 1,
                      "ye": E.loc[ii, F26].sum(axis=1) / E.loc[ii, F25].sum(axis=1) - 1,
                      "w": S.loc[ii, F25].sum(axis=1)})
    pts = [{"cat": r.cat, "x": float(np.clip(r.ye, -.8, 1.5)), "y": float(np.clip(r.ys, -.8, 1.5)), "w": float(r.w)} for r in d.itertuples()]
    c = lambda g: float(np.corrcoef(g.ys.clip(-1, 2), g.ye.clip(-1, 2))[0, 1])
    same = lambda g: float((np.sign(g.ys) == np.sign(g.ye)).mean())
    out = {"points": pts, "n": len(d), "corr": c(d), "same": same(d),
           "by_house": {h: {"corr": c(g), "same": same(g), "n": len(g)} for h, g in d.groupby("house")}}
    # persistencia: YoY jul–dic-25 vs ene–jun-26
    h1, h1l, h2, h2l = R("2025-07-01", 6), R("2024-07-01", 6), R("2026-01-01", 6), R("2025-01-01", 6)
    p = pd.DataFrame({"cat": A.cat})
    for n, X in [("s", S), ("e", E)]:
        p[n + "1"] = X[h1].sum(axis=1) / X[h1l].sum(axis=1) - 1
        p[n + "2"] = X[h2].sum(axis=1) / X[h2l].sum(axis=1) - 1
    ok = (S[h1l].sum(axis=1) >= 300) & (E[h1l].sum(axis=1) >= 150) & (E[h2l].sum(axis=1) >= 150) & (S[h2l].sum(axis=1) >= 300) & (L <= "2024-01-01")
    p = p[ok].replace([np.inf, -np.inf], np.nan).dropna()
    for k in ["s1", "s2", "e1", "e2"]:
        p[k] = p[k].clip(-1, 2)
    per = lambda g: {"n": len(g), "keep_epos": float((np.sign(g.e1) == np.sign(g.e2)).mean()),
                     "keep_ship": float((np.sign(g.s1) == np.sign(g.s2)).mean()),
                     "corr_epos": float(np.corrcoef(g.e1, g.e2)[0, 1]), "corr_ship": float(np.corrcoef(g.s1, g.s2)[0, 1]),
                     "epos_to_ship": float(np.corrcoef(g.e1, g.s2)[0, 1])}
    out["persist"] = {"Total": per(p), **{c_: per(g) for c_, g in p.groupby("cat")}}
    return out


def launch_curves(S, E, A, L):
    K = 13
    out = {}
    for c in ["Fragancias", "Makeup"]:
        rows = []
        for ean in L.index[(L >= "2024-07-01") & (L <= "2025-07-01") & (A.cat == c)]:
            j, ej = S.columns.get_loc(L[ean]), E.columns.get_loc(L[ean])
            s, e = S.loc[ean].values[j:j + K], E.loc[ean].values[ej:ej + K]
            if len(s) == K and len(e) == K and e.sum() >= 300:
                rows.append((s, e))
        s = np.array([r[0] for r in rows]); e = np.array([r[1] for r in rows])
        tot = e.sum()
        # año 1 vs año 2 (lanzados jul–dic-24, meses 12–19)
        y = []
        for ean in L.index[(L >= "2024-07-01") & (L <= "2024-12-01") & (A.cat == c)]:
            j, ej = S.columns.get_loc(L[ean]), E.columns.get_loc(L[ean])
            sv, ev = S.loc[ean].values, E.loc[ean].values
            if ev[ej:ej + 12].sum() >= 300:
                y.append((sv[j:j + 12].sum(), ev[ej:ej + 12].sum(), sv[j + 12:j + 20].sum(), ev[ej + 12:ej + 20].sum(), ev[ej + 4:ej + 12].sum()))
        y = np.array(y)
        out[c] = {"n": len(rows), "ship": (s.sum(0) / tot).tolist(), "epos": (e.sum(0) / tot).tolist(),
                  "cum": (np.cumsum(s.sum(0)) / np.cumsum(e.sum(0))).tolist(),
                  "m0_ship": float(s[:, 0].sum() / tot), "n_y2": len(y),
                  "y1": float(y[:, 0].sum() / y[:, 1].sum()), "y2": float(y[:, 2].sum() / y[:, 3].sum()),
                  "epos_y2_vs_y1": float(y[:, 3].sum() / y[:, 4].sum() - 1)}
    vet = S[R("2023-07-01", 3)].sum(axis=1) > 0
    f = pd.date_range("2024-07-01", "2026-06-01", freq="MS")
    for c in out:
        m = vet & (A.cat == c)
        out[c]["vet_ratio"] = float(S.loc[m, f].sum().sum() / E.loc[m, f].sum().sum())
    return out


def veterans(S, E, A, L):
    vet = S[R("2023-07-01", 3)].sum(axis=1) > 0
    act = S[R("2026-02-01", 6)].sum(axis=1) > 0.05 * S[F25].sum(axis=1)
    m = vet & act
    x = pd.DataFrame({"h": A.house, "e25": E[F25].sum(axis=1), "e26": E[F26].sum(axis=1)})[m]
    g = x.groupby("h")[["e25", "e26"]].sum()
    xx = x[x.e25 >= 300]
    res = {"houses": {h: {"epos_yoy": float(g.e26[h] / g.e25[h] - 1), "pct_caen": float((xx.e26 < xx.e25)[xx.h == h].mean()),
                          "n": int((xx.h == h).sum())} for h in HOUSES}}
    tot = pd.DataFrame({"h": A.house, "e25": E[F25].sum(axis=1), "e26": E[F26].sum(axis=1)}).groupby("h").sum()
    for h in HOUSES:
        res["houses"][h]["casa_epos_yoy"] = float(tot.e26[h] / tot.e25[h] - 1)
    coh = np.where(L <= "2023-07-01", "Antes de FY24", np.where(L < "2024-07-01", "Lanzados FY24",
                   np.where(L < "2025-07-01", "Lanzados FY25", "Lanzados FY26")))
    t = pd.DataFrame({f: S[r].sum(axis=1) for f, r in [("FY24", F24), ("FY25", F25), ("FY26", F26)]}).groupby([A.cat.values, coh]).sum()
    t = t / t.groupby(level=0).transform("sum")
    res["cohorts"] = {c: {k: t.loc[(c, k)].tolist() for k in t.loc[c].index} for c in ["Fragancias", "Makeup"]}
    return res


def load_and_exits(S, E, A):
    has = E.sum(axis=1) > 0
    Sh, Eh = S[has].groupby(A.house[has]).sum(), E[has].groupby(A.house[has]).sum()
    months = pd.date_range("2025-06-01", "2026-07-01", freq="MS")
    r12 = {h: [float(Sh.loc[h, t - pd.DateOffset(months=11):t].sum() / Eh.loc[h, t - pd.DateOffset(months=11):t].sum()) for t in months] for h in HOUSES}
    nxt = {}
    for h in HOUSES:
        v = []
        for t in months:
            c = [t + pd.DateOffset(months=k) for k in (1, 2, 3)]
            v.append(float(Sh.loc[h, c].sum() / Sh.loc[h, [x - pd.DateOffset(years=1) for x in c]].sum() - 1) if c[-1] in Sh.columns else None)
        nxt[h] = v
    # carga por EAN (de epos_pattern)
    started = S.gt(0).cumsum(axis=1)
    old = (started[pd.Timestamp("2025-06-01")] >= 12) & has
    e = epos_pattern.load_build(S[old], E[old], A.house[old], epos_pattern.MIN_LY)
    e["sig"] = np.where(e.dev > .15, "cargado", np.where(e.dev < -.15, "descargado", "normal"))
    f = lambda x: float((x.w * x.exc).sum() / x.w.sum())
    by = {}
    for h, g in e.groupby("key"):
        m = g.groupby(["t", "sig"]).apply(f).unstack()
        by[h] = {s: f(g[g.sig == s]) for s in ["cargado", "normal", "descargado"]}
        by[h]["meses"] = int((m.cargado < m.normal).sum()); by[h]["de"] = len(m)
    ef = e.assign(cat=A.cat.reindex(e.index).values)
    cat = {}
    for c, g in ef.groupby("cat"):
        m = g.groupby(["t", "sig"]).apply(f).unstack()
        cat[c] = {s: f(g[g.sig == s]) for s in ["cargado", "normal", "descargado"]}
        cat[c]["meses"] = int((m.cargado < m.normal).sum()); cat[c]["de"] = len(m)
    # bajas: EPOS alrededor del último mes con envío relevante
    out = []
    z = R("2026-02-01", 6)
    B = A.index[(S[F25].sum(axis=1) >= 1000) & (S[z].sum(axis=1) <= 0.02 * S[F25].sum(axis=1))]
    for ean in B:
        s, ev = S.loc[ean], E.loc[ean]
        last = s[s > 0.05 * s[F25].mean()].index.max()
        if last > pd.Timestamp("2026-01-01"):
            continue
        base = ev[(ev.index > last - pd.DateOffset(months=12)) & (ev.index <= last - pd.DateOffset(months=6))].mean()
        if base > 0:
            out.append({"cat": A.cat[ean], **{k: ev.get(last + pd.DateOffset(months=k), np.nan) / base for k in range(-6, 7)}})
    b = pd.DataFrame(out)
    exits = {c: {"n": len(g), "curve": [float(g[k].median()) for k in range(-6, 7)]} for c, g in b.groupby("cat")}
    return {"months": [m.strftime("%b-%y") for m in months], "r12": r12, "next": nxt, "ean_house": by, "ean_cat": cat, "exits": exits}


def main():
    S, E, A = epos_diag.panel()
    L = launches(S)
    ii = mature_set(S, E, L)
    D = {"noise": noise(S, E, A, ii), "trend": trend(S, E, A, ii, L), "launch": launch_curves(S, E, A, L),
         "veterans": veterans(S, E, A, L), "load": load_and_exits(S, E, A)}
    (ROOT / "work" / "epos_patrones.json").write_text(json.dumps(D, default=float))
    n, t, la, v, lo = D["noise"], D["trend"], D["launch"], D["veterans"], D["load"]
    P = lambda x: f"{x:+.0%}"
    L_ = ["# Patrones envío ↔ EPOS (foto sep-26)\n",
          "## 1. Ruido",
          f"- EANs maduros con EPOS: {len(ii)}. El {n['pct_env_mas_ruidoso']:.0%} tiene un YoY mensual de envíos más inestable que el de EPOS; "
          f"mediana {n['ratio_ruido']:.1f} veces.",
          *[f"- {h}: rango del YoY mensual de la casa envío {n['rango'][h]['ship']:.0%} vs EPOS {n['rango'][h]['epos']:.0%}" for h in HOUSES],
          "\n## 2. Tendencia",
          f"- YoY FY26 por EAN: correlación envío–EPOS {t['corr']:.2f}; mismo signo {t['same']:.0%} (n={t['n']}).",
          *[f"- Persistencia {k}: signo del EPOS se mantiene {p['keep_epos']:.0%} vs envío {p['keep_ship']:.0%}; "
            f"correlación semestre a semestre EPOS {p['corr_epos']:.2f} vs envío {p['corr_ship']:.2f}; EPOS→envío siguiente {p['epos_to_ship']:.2f} (n={p['n']})"
            for k, p in t["persist"].items()],
          "\n## 3. Lanzamientos (jul-24 → jul-25)",
          *[f"- {c} (n={x['n']}): mes 0 envía {x['m0_ship']:.0%} de lo que se vende en 13 meses; envío/EPOS año 1 {x['y1']:.2f}, "
            f"meses 12–19 {x['y2']:.2f} (veteranos {x['vet_ratio']:.2f}); EPOS meses 12–19 vs 4–11 {P(x['epos_y2_vs_y1'])} (n={x['n_y2']})"
            for c, x in la.items()],
          "\n## 4. Veteranos activos (con envío desde jul-23)",
          *[f"- {h}: EPOS FY26 {P(x['epos_yoy'])} (casa {P(x['casa_epos_yoy'])}); {x['pct_caen']:.0%} de los EANs caen" for h, x in v["houses"].items()],
          *[f"- Peso en envío {c}: " + "; ".join(f"{k} {'/'.join(f'{y:.0%}' for y in vals)}" for k, vals in x.items()) for c, x in v["cohorts"].items()],
          "\n## 5. Carga acumulada y bajas",
          *[f"- {h}: cargados {P(x['cargado'])} vs normales {P(x['normal'])} (envío − EPOS a 3 meses); se cumple {x['meses']} de {x['de']} meses"
            for h, x in lo["ean_house"].items()],
          *[f"- Bajas {c} (n={x['n']}): EPOS relativo meses −6…+6 = " + " ".join(f"{y:.2f}" for y in x["curve"]) for c, x in lo["exits"].items()]]
    out = ROOT / "work" / "results" / "epos_patrones.md"
    out.write_text("\n".join(L_) + "\n")
    print("\n".join(L_))


if __name__ == "__main__":
    main()
