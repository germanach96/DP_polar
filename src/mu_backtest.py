"""Makeup (GUMU, KYMU): técnicas de forecast y corrección.
- Histórico = foto 2026-09 (reexpresada) truncada al corte. Consenso de la foto 2025-09 x factor de reexpresión del mes (por familia).
- Fotos: inicial 2025-09, corrección 2026-03, verdad 2026-09. Además 13 cortes mensuales 2025-07..2026-07 (sin consenso).
- Universo: EANs Central (>=6 meses de envíos al corte). Principal: sin forecast manual (isf de la foto); secundario: todos.
Salida: work/results/mu_backtest.md"""
import sys, warnings, itertools
import numpy as np, pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import methods as mt  # noqa
warnings.filterwarnings("ignore")
W = Path(__file__).resolve().parents[1] / "work"
M = pd.date_range("2023-07-01", "2027-06-01", freq="MS")
LAST = pd.Timestamp("2026-08-01")
VERS = ["2025-09", "2026-03", "2026-09"]


def load():
    d = pd.read_parquet(W / "mu.parquet")
    v = d[d.version == "2026-09"]
    H = v[v.date <= LAST].pivot_table(index="ean", columns="date", values="cons", aggfunc="sum").reindex(columns=M)
    eans = H.index
    started = H.fillna(0).cumsum(axis=1) > 0
    H = H.fillna(0).where(started).where(pd.DataFrame(np.broadcast_to(M <= LAST, H.shape), index=eans, columns=M))
    E = v.pivot_table(index="ean", columns="date", values="epos", aggfunc="sum").reindex(index=eans, columns=M)
    C = v.pivot_table(index="ean", columns="date", values="cuts", aggfunc="sum").reindex(index=eans, columns=M).fillna(0)
    attr = v.groupby("ean").agg(fam=("fam", "first"), brand=("brand", "first"), pline=("pline", "first")).reindex(eans)
    attr["fam_brand"] = attr.fam + "|" + attr.brand
    # factores de reexpresión por familia y mes calendario (2026-03 / 2025-09)
    p = d[d.version.isin(["2025-09", "2026-03"]) & (d.date < "2025-09-01")].pivot_table(index=["fam", "date"], columns="version", values="act", aggfunc="sum")
    rr = p.reset_index(); rr["ratio"] = rr["2026-03"] / rr["2025-09"]; rr["mo"] = rr.date.dt.month
    fac = rr.groupby(["fam", "mo"]).ratio.mean()
    return d, H, E, C, attr, fac


def da_known(d, eans, V):
    out = pd.DataFrame(np.nan, index=eans, columns=M)
    for v in [v for v in VERS if pd.Timestamp(v + "-01") <= V]:
        p = d[d.version == v].pivot_table(index="ean", columns="date", values="da", aggfunc="sum").reindex(index=eans, columns=M)
        out = out.where(p.isna(), p)
    return out


def season_index(X, keys, m, months_back=24):
    """Índice estacional por grupo y mes calendario (media de peso del mes / media mensual) con datos < m."""
    lo = max(0, m - months_back)
    df = pd.DataFrame(np.nan_to_num(X[:, lo:m]), columns=M[lo:m]); df["k"] = keys
    G = df.groupby("k").sum().T; G.index = pd.DatetimeIndex(G.index)
    G = G.loc[:, G.sum() > 0]
    mm = G.rolling(12, center=True, min_periods=6).mean()
    ratio = (G / mm).replace([np.inf, -np.inf], np.nan)
    idx = ratio.groupby(ratio.index.month).mean().clip(0.2, 5)
    idx = idx / idx.mean()
    full = pd.DataFrame(1.0, index=range(1, 13), columns=pd.Index(sorted(set(keys))))
    full.update(idx)
    return full.fillna(1.0)


def techniques(H, E, C, DA, attr, m, cons=None):
    """Devuelve dict nombre -> matriz n x 8 (meses m+1..m+8)."""
    n = H.shape[0]
    Hm = H.copy(); Hm[:, m:] = np.nan
    first = np.argmax(np.isfinite(Hm), 1).astype(float); first[~np.isfinite(Hm).any(1)] = np.nan
    age = m - first; central = age >= 6
    fi = list(range(m + 1, m + 9))
    T = {}
    ly = np.stack([np.nan_to_num(Hm[:, j - 12]) for j in fi], 1)
    DAp = np.clip(np.nan_to_num(DA), 0, None)
    ly_adj = np.clip(np.stack([np.nan_to_num(Hm[:, j - 12]) + 0.25 * C[:, j - 12] - 0.5 * DAp[:, j - 12] for j in fi], 1), 0, None)
    T["LY_plano"] = ly
    for lvl, lab in [("fam_brand", "función"), ("fam", "familia"), ("pline", "product_line")]:
        g = np.clip(np.nan_to_num(mt._group_g(Hm, m, 12, attr[lvl].values, central)), -.3, .3)
        T[f"LY x trend12M@{lab}"] = ly * (1 + g)[:, None]
        T[f"LY x 50%trend12M@{lab}"] = ly * (1 + 0.5 * g)[:, None]
        if lvl == "fam_brand":
            T["regla_fragancias(LY+25%cortes-50%DA) x trend12M@función"] = ly_adj * (1 + g)[:, None]
            gF = g
    ge = np.clip(np.nan_to_num(mt.g_flat(Hm, m, 12)), -.3, .3)
    T["LY x trend12M@EAN"] = ly * (1 + ge)[:, None]
    # ritmo de venta
    for w in (3, 6, 12):
        mean_w = np.nan_to_num(np.nanmean(Hm[:, m - w:m], 1))
        T[f"media{w}M_plana"] = np.repeat(mean_w[:, None], 8, 1)
    mean12 = T["media12M_plana"][:, 0]; mean6 = T["media6M_plana"][:, 0]
    T["media12M x trend12M@función"] = T["media12M_plana"] * (1 + gF)[:, None]
    gFam = np.clip(np.nan_to_num(mt._group_g(Hm, m, 12, attr["fam"].values, central)), -.3, .3)
    for nmw, base in [("media6M", mean6), ("media3M", T["media3M_plana"][:, 0])]:
        T[f"{nmw} x trend12M@función"] = np.repeat((base * (1 + gF))[:, None], 8, 1)
        T[f"{nmw} x 50%trend12M@función"] = np.repeat((base * (1 + 0.5 * gF))[:, None], 8, 1)
        T[f"{nmw} x 50%trend12M@familia"] = np.repeat((base * (1 + 0.5 * gFam))[:, None], 8, 1)
    # ritmo x estacionalidad (envíos / EPOS), por familia y por función
    for src_name, X in [("envíos", Hm), ("EPOS", np.where(np.isfinite(E) & (np.arange(len(M)) < m), E, np.nan))]:
        for lvl, lab in [("fam", "familia"), ("fam_brand", "función")]:
            S = season_index(X, attr[lvl].values, m)
            keys = attr[lvl].values
            idx = np.stack([[S.at[M[j].month, k] if k in S.columns else 1.0 for k in keys] for j in fi], 1)
            # desestacionalizar la media 12M no hace falta (12 meses completos = media anual); la 6M sí
            past6 = np.stack([[S.at[M[j].month, k] if k in S.columns else 1.0 for k in keys] for j in range(m - 6, m)], 1)
            des6 = np.nan_to_num(np.nanmean(Hm[:, m - 6:m] / past6, 1))
            T[f"media12M x estacionalidad_{src_name}@{lab}"] = mean12[:, None] * idx
            T[f"media6M(desest.) x estacionalidad_{src_name}@{lab}"] = des6[:, None] * idx
            T[f"media12M x trend12M@función x estacionalidad_{src_name}@{lab}"] = (mean12 * (1 + gF))[:, None] * idx
    if cons is not None:
        T["consenso"] = cons
    return {k: np.clip(np.nan_to_num(v), 0, None) for k, v in T.items()}, central, age, fi


def evaluate(F, A, fi, sel):
    ok = [k for k, j in enumerate(fi) if M[j] <= LAST]
    f = F[sel][:, ok]; a = A[sel][:, [fi[k] for k in ok]]  # A es n x todos los meses -> columnas del horizonte
    return np.abs(f - a).sum() / a.sum(), f.sum() / a.sum() - 1, a.sum()


def main():
    d, Hdf, Edf, Cdf, attr, fac = load()
    H = Hdf.values; E = Edf.values; C = Cdf.values; eans = Hdf.index
    A_all = np.nan_to_num(H)
    rows = []
    # ---------- cortes mensuales (sin consenso) ----------
    for V in pd.date_range("2025-07-01", "2026-07-01", freq="MS"):
        m = M.get_loc(V)
        DA = da_known(d, eans, V).values
        T, central, age, fi = techniques(H, E, C, DA, attr, m)
        vv = [v for v in VERS if pd.Timestamp(v + "-01") <= V] or [VERS[0]]  # antes de sep-25: flag de la primera foto
        isf = d[d.version == vv[-1]].groupby("ean").isf.max().reindex(eans).fillna(0).values
        for fam in ["GUMU", "KYMU"]:
            for univ, sel in [("sin_manual", central & (isf == 0) & (attr.fam.values == fam)), ("todos", central & (attr.fam.values == fam))]:
                for k, F in T.items():
                    w, b, a = evaluate(F, A_all, fi, sel)
                    rows.append(dict(tipo="mensual", corte=V, fam=fam, univ=univ, tecnica=k, wmape=w, bias=b, A=a))
    R = pd.DataFrame(rows)
    R.to_pickle(W / "mu_monthly.pkl")
    # ---------- fotos: inicial 2025-09, corrección 2026-03 ----------
    snaps = {}
    for s in ["2025-09", "2026-03"]:
        V = pd.Timestamp(s + "-01"); m = M.get_loc(V)
        x = d[d.version == s]
        cons = x[x.date > V].pivot_table(index="ean", columns="date", values="cons", aggfunc="sum").reindex(index=eans, columns=M).fillna(0)
        if s == "2025-09":
            for fam in ["GUMU", "KYMU"]:
                rowsel = attr.fam.values == fam
                f = np.array([fac.get((fam, c.month), 1.0) for c in M])
                cons.loc[rowsel] = cons.loc[rowsel].values * f[None, :]
        DA = da_known(d, eans, V).values
        T, central, age, fi = techniques(H, E, C, DA, attr, m, cons=cons.values[:, m + 1:m + 9])
        isf = x.groupby("ean").isf.max().reindex(eans).fillna(0).values
        snaps[s] = dict(T=T, central=central, isf=isf, fi=fi, m=m)
    out = []
    for fam in ["GUMU", "KYMU"]:
        for univ in ["sin_manual", "todos"]:
            s0 = snaps["2025-09"]
            sel0 = s0["central"] & (attr.fam.values == fam) & ((s0["isf"] == 0) if univ == "sin_manual" else True)
            stat_names = [k for k in s0["T"] if k != "consenso"]
            init = dict(s0["T"])
            for k in stat_names:
                init[f"mix50(consenso,{k})"] = 0.5 * s0["T"]["consenso"] + 0.5 * s0["T"][k]
            for k, F in init.items():
                w, b, a = evaluate(F, A_all, s0["fi"], sel0)
                out.append(dict(foto="2025-09 inicial", fam=fam, univ=univ, tecnica=k, correccion="-", wmape=w, bias=b))
            # corrección en 2026-03: factor sobre oct-25..feb-26 (meses cerrados con forecast)
            s1 = snaps["2026-03"]
            sel1 = s1["central"] & (attr.fam.values == fam) & ((s1["isf"] == 0) if univ == "sin_manual" else True)
            el = [j for j in s0["fi"] if j < s1["m"]]
            ov = [j for j in s1["fi"] if j in s0["fi"]]
            for k, F0 in init.items():
                base_new = s1["T"].get(k) if not k.startswith("mix50") else 0.5 * s1["T"]["consenso"] + 0.5 * s1["T"][k[len("mix50(consenso,"):-1]]
                if base_new is None:
                    continue
                pos0 = {j: i for i, j in enumerate(s0["fi"])}; pos1 = {j: i for i, j in enumerate(s1["fi"])}
                Fe = F0[sel1][:, [pos0[j] for j in el]]; Ae = A_all[sel1][:, el]
                r = np.clip(Ae.sum() / max(Fe.sum(), 1e-9), 0.5, 1.5)
                for corr, alpha in [("recalcular", None), ("congelar", 0), ("factor_100%", 1.0), ("factor_50%", 0.5)]:
                    if corr == "recalcular":
                        F1 = base_new.copy()
                    else:
                        rf = 1 + alpha * (r - 1) if corr != "congelar" else 1.0
                        F1 = base_new * rf
                        for j in ov:
                            F1[:, pos1[j]] = F0[:, pos0[j]] * rf
                    w, b, a = evaluate(F1, A_all, s1["fi"], sel1)
                    out.append(dict(foto="2026-03 corregida", fam=fam, univ=univ, tecnica=k, correccion=corr, wmape=w, bias=b, factor=r))
    S = pd.DataFrame(out)
    S.to_pickle(W / "mu_snaps.pkl")
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 400)
    L = ["# Makeup backtest (src/mu_backtest.py)\n"]
    g = R.groupby(["fam", "univ", "tecnica"]).apply(lambda x: pd.Series(dict(wmape=(x.wmape * x.A).sum() / x.A.sum(), bias=(x.bias * x.A).sum() / x.A.sum(), bias_abs=x.bias.abs().mean())))
    wo = R.pivot_table(index=["fam", "univ", "tecnica"], columns="corte", values="wmape")
    ref = wo.xs("LY_plano", level="tecnica")
    g["gana_a_LY"] = [int((wo.loc[i] < ref.loc[(i[0], i[1])]).sum()) for i in wo.index]
    for fam in ["GUMU", "KYMU"]:
        for univ in ["sin_manual", "todos"]:
            t = g.loc[(fam, univ)].sort_values("wmape")
            L += [f"\n## {fam} — {univ} — 13 cortes mensuales\n", t.round(3).to_markdown()]
            if univ == "sin_manual":
                print(f"===== {fam} {univ} mensual"); print(t.round(3).head(15).to_string()); print(t.loc[["LY_plano"]].round(3).to_string())
    for fam in ["GUMU", "KYMU"]:
        for univ in ["sin_manual", "todos"]:
            t0 = S[(S.fam == fam) & (S.univ == univ) & (S.foto == "2025-09 inicial")].set_index("tecnica")[["wmape", "bias"]].sort_values("wmape")
            t1 = S[(S.fam == fam) & (S.univ == univ) & (S.foto == "2026-03 corregida")].pivot_table(index="tecnica", columns="correccion", values=["wmape", "bias"])
            L += [f"\n## {fam} — {univ} — foto inicial sep-25\n", t0.round(3).to_markdown(),
                  f"\n## {fam} — {univ} — corrección en mar-26 (verdad hasta ago-26)\n", t1.round(3).to_markdown()]
            if univ == "sin_manual":
                print(f"===== {fam} {univ} foto sep-25"); print(t0.round(3).head(12).to_string()); print(t0.loc[["LY_plano", "consenso"]].round(3).to_string())
    (W / "results" / "mu_backtest.md").write_text("\n".join(L))


if __name__ == "__main__":
    main()
