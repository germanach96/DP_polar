"""Técnica inicial + técnica de corrección entre fotos.
Foto inicial sep-25 -> forecast inicial con varias técnicas. En cada foto siguiente (dic-25, mar-26, jun-26) se aplican
varias técnicas de corrección. Todo se mide contra la foto final (sep-26). Universo: sin Local ni isf>=1.
Salida: work/results/tracking.md"""
import sys
import warnings
import itertools
import numpy as np
import pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import methods as mt  # noqa
from ptype import add_types  # noqa
warnings.filterwarnings("ignore")
W = Path(__file__).resolve().parents[1] / "work"
MONTHS = pd.date_range("2023-07-01", "2027-06-01", freq="MS")
SNAPS = ["2025-09", "2025-12", "2026-03", "2026-06"]
LAST_TRUTH = pd.Timestamp("2026-08-01")


def load():
    H = pd.read_pickle(W / "hist.pkl").reindex(columns=MONTHS)
    a = add_types(pd.read_pickle(W / "attr.pkl")).reindex(H.index)
    a["total"] = "TOTAL"
    fc = pd.read_parquet(W / "snap_fc.parquet", columns=["snap", "rule", "ean", "target", "F"])
    cons = fc[fc.rule == "consenso_foto"]
    return H, a, cons, fc


def rule_matrix(H, a, eans, m, damp, lvl="house_ptype", cap=0.3, months_idx=None):
    """F = LY x (1 + damp*g12) para las columnas months_idx, con g12 calculado con datos < m."""
    Hm = H.loc[eans].values
    g = mt._group_g(Hm, m, 12, a.loc[eans, lvl].values)
    g = np.clip(np.nan_to_num(g), -cap, cap)
    out = {}
    for j in months_idx:
        ly = Hm[:, j - 12] if j - 12 >= 0 else np.full(len(eans), np.nan)
        out[MONTHS[j]] = np.clip(np.nan_to_num(ly) * (1 + damp * g), 0, None)
    return pd.DataFrame(out, index=eans)


def calib_ratio(F_back, A_back, keys, alpha, lo=0.7, hi=1.3):
    """Ratio real/forecast de los meses recientes por grupo, amortiguado (alpha) y acotado."""
    f = F_back.sum(axis=1).groupby(keys).sum(); a_ = A_back.sum(axis=1).groupby(keys).sum()
    r = (a_ / f.replace(0, np.nan)).clip(lo, hi).fillna(1.0)
    return (1 + alpha * (r - 1)).reindex(keys).values


def score(F, A):
    """F, A: DataFrames ean x target (solo meses con verdad). Devuelve métricas."""
    cols = [c for c in F.columns if c <= LAST_TRUTH]
    F = F[cols].fillna(0); A = A.reindex(index=F.index, columns=cols).fillna(0)
    em = (F - A).abs().values.sum() / A.values.sum()
    tot = F.values.sum() / A.values.sum() - 1
    return em, tot, A.values.sum()


def main():
    H, a, cons, fc = load()
    keep = (a.resp != "Local") & (a.isf.fillna(0) == 0)
    snap_eans = {s: sorted(set(fc[fc.snap == s].ean)) for s in SNAPS}
    res = []
    # ---------- 1) TÉCNICA INICIAL en cada foto (sin memoria) ----------
    base_specs = {
        "LY_plano": dict(damp=0.0),
        "trend12M_completo": dict(damp=1.0),
        "trend12M_75%": dict(damp=0.75),
        "trend12M_50%": dict(damp=0.5),
        "trend12M_25%": dict(damp=0.25),
    }
    stateless = {}
    for s in SNAPS:
        V = pd.Timestamp(s + "-01"); m = MONTHS.get_loc(V); eans = snap_eans[s]
        fidx = list(range(m + 1, m + 9)); bidx = list(range(m - 3, m))
        A = H.loc[eans]
        Cs = cons[cons.snap == s].pivot_table(index="ean", columns="target", values="F").reindex(index=eans, columns=MONTHS[fidx]).fillna(0)
        cand = {}
        for nm, sp in base_specs.items():
            for lvl in ["house_ptype", "house", "total"]:
                if sp["damp"] == 0 and lvl != "total":
                    continue
                key = nm if sp["damp"] == 0 else f"{nm}@{lvl}"
                F = rule_matrix(H, a, eans, m, sp["damp"], lvl, months_idx=fidx)
                cand[key] = F
                # + calibración con los últimos 3 meses cerrados (nivel del grupo), alpha 0.5 y 1
                Fb = rule_matrix(H, a, eans, m - 3, sp["damp"], lvl, months_idx=bidx)  # backcast hecho 3 meses antes
                for alpha in (0.5, 1.0):
                    for clvl in ["house_ptype", "total"]:
                        r = calib_ratio(Fb, A[MONTHS[bidx]], a.loc[eans, clvl].values, alpha)
                        cand[f"{key}+calib3M{int(alpha*100)}%@{clvl}"] = F.mul(r, axis=0)
        cand["consenso"] = Cs
        cand["mix50(consenso,trend12M_50%@house_ptype)"] = 0.5 * Cs + 0.5 * cand["trend12M_50%@house_ptype"]
        stateless[s] = cand
        for k, F in cand.items():
            em, tot, n = score(F, A)
            res.append(dict(fase="inicial(sin memoria)", snap=s, tecnica=k, wmape_EANmes=em, bias_total=tot))
    R1 = pd.DataFrame(res)
    # ---------- 2) TÉCNICAS DE CORRECCIÓN entre fotos ----------
    # parto del forecast de la foto anterior (técnica base fija) y lo corrijo al llegar la nueva foto
    res2 = []
    bases = ["trend12M_50%@house_ptype", "LY_plano", "consenso", "trend12M_completo@house_ptype"]
    for base in bases:
        prev = stateless["2025-09"][base].copy()
        for s_prev, s in zip(SNAPS[:-1], SNAPS[1:]):
            V = pd.Timestamp(s + "-01"); m = MONTHS.get_loc(V); eans = snap_eans[s]
            Vp = pd.Timestamp(s_prev + "-01")
            elapsed = [c for c in MONTHS if Vp <= c < V and c in prev.columns]  # meses cerrados desde la foto anterior que tenían forecast
            fut = list(MONTHS[m + 1:m + 9])
            new = stateless[s][base].reindex(eans)
            P = prev.reindex(eans)
            A = H.loc[eans]
            Pe = P.reindex(columns=elapsed).fillna(0); Ae = A[elapsed].fillna(0)
            techs = {}
            techs["recalcular_desde_cero"] = new
            frozen = new.copy()
            ov = [c for c in fut if c in P.columns]
            frozen[ov] = P[ov].fillna(0).values
            techs["congelar_lo_anterior"] = frozen
            for lvl, alpha in itertools.product(["ean", "house_ptype", "total"], [0.5, 1.0]):
                keys = a.loc[eans, lvl].values if lvl != "ean" else np.array(eans)
                r = calib_ratio(Pe, Ae, keys, alpha, 0.5, 1.5)
                corr = new.copy()
                corr[ov] = P[ov].fillna(0).mul(r, axis=0).values
                techs[f"anterior_x_real/fc_{int(alpha*100)}%@{lvl}"] = corr
                techs[f"recalcular_x_real/fc_{int(alpha*100)}%@{lvl}"] = new.mul(r, axis=0)
            techs["media(anterior,recalculo)"] = new.copy()
            techs["media(anterior,recalculo)"][ov] = 0.5 * P[ov].fillna(0).values + 0.5 * new[ov].values
            for k, F in techs.items():
                em, tot, n = score(F, A)
                res2.append(dict(base=base, snap=s, tecnica=k, wmape_EANmes=em, bias_total=tot, n=n))
            prev = techs["recalcular_desde_cero"]  # la siguiente corrección parte del recálculo (idéntico para todas: comparación por paso)
    R2 = pd.DataFrame(res2)
    # ---------- salida ----------
    L = ["# Técnica inicial y técnica de corrección (generado por src/tracking.py)\n",
         "Foto inicial sep-25, correcciones en dic-25, mar-26, jun-26; verdad = foto sep-26. Horizonte 8 meses tras el mes en curso.",
         "WMAPE a nivel EAN-mes; bias_total = forecast total / real total - 1. jun-26 solo tiene 2 meses con verdad.\n"]
    p = R1.pivot_table(index="tecnica", columns="snap", values="wmape_EANmes")
    b = R1.pivot_table(index="tecnica", columns="snap", values="bias_total")
    p["media"] = p.mean(1); p["peor"] = p[SNAPS].max(1)
    b.columns = ["bias_" + c for c in b.columns]; b["|bias|medio"] = b.abs().mean(1)
    T1 = p.join(b).sort_values("media")
    L += ["## 1. Técnica para el forecast (cada foto, sin memoria)\n", T1.round(3).to_markdown()]
    p2 = R2.pivot_table(index=["base", "tecnica"], columns="snap", values="wmape_EANmes"); p2["media"] = p2.mean(1)
    b2 = R2.pivot_table(index=["base", "tecnica"], columns="snap", values="bias_total"); b2.columns = ["bias_" + c for c in b2.columns]
    b2["|bias|medio"] = b2.abs().mean(1)
    T2 = p2.join(b2).sort_values("media")
    L += ["\n## 2. Técnica de corrección al llegar una foto nueva\n", T2.round(3).to_markdown()]
    (W / "results" / "tracking.md").write_text("\n".join(L))
    T1.to_pickle(W / "track_T1.pkl"); T2.to_pickle(W / "track_T2.pkl")
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
    print(T1.round(3).head(30).to_string()); print(T1.loc[[i for i in T1.index if i in ("LY_plano", "consenso")]].round(3))
    for bs in bases:
        print("\n== base", bs); print(T2.loc[bs].round(3).to_string())


if __name__ == "__main__" and "--chain" not in sys.argv:
    main()


def chain():
    """Simulación encadenada: técnica inicial en sep-25 y corrección en cada foto, arrastrando el forecast corregido."""
    H, a, cons, fc = load()
    snap_eans = {s: sorted(set(fc[fc.snap == s].ean)) for s in SNAPS}

    def base_fc(name, s):
        V = pd.Timestamp(s + "-01"); m = MONTHS.get_loc(V); eans = snap_eans[s]; fidx = list(range(m + 1, m + 9))
        Cs = cons[cons.snap == s].pivot_table(index="ean", columns="target", values="F").reindex(index=eans, columns=MONTHS[fidx]).fillna(0)
        if name == "consenso":
            return Cs
        if name == "LY_plano":
            return rule_matrix(H, a, eans, m, 0.0, "total", months_idx=fidx)
        if name.startswith("trend"):
            d = float(name.split("_")[1].rstrip("%")) / 100
            return rule_matrix(H, a, eans, m, d, "house_ptype", months_idx=fidx)
        if name.startswith("mix50"):
            return 0.5 * Cs + 0.5 * rule_matrix(H, a, eans, m, 0.5, "house_ptype", months_idx=fidx)

    rows = []
    for start, corr in itertools.product(["trend_50%", "trend_75%", "trend_100%", "LY_plano", "consenso", "mix50"],
                                         ["ninguna(recalcular)", "congelar", "real/fc_50%@total", "real/fc_100%@total", "real/fc_50%@house_ptype"]):
        prev = base_fc(start, SNAPS[0])
        A0 = H.loc[prev.index]
        em, tot, _ = score(prev, A0)
        rows.append(dict(inicio=start, correccion=corr, snap=SNAPS[0], wmape=em, bias=tot))
        for s_prev, s in zip(SNAPS[:-1], SNAPS[1:]):
            V = pd.Timestamp(s + "-01"); m = MONTHS.get_loc(V); eans = snap_eans[s]
            Vp = pd.Timestamp(s_prev + "-01")
            elapsed = [c for c in MONTHS if Vp <= c < V and c in prev.columns]
            fut = list(MONTHS[m + 1:m + 9])
            new = base_fc(start, s)
            P = prev.reindex(eans)
            ov = [c for c in fut if c in P.columns]
            A = H.loc[eans]
            if corr == "ninguna(recalcular)":
                cur = new
            elif corr == "congelar":
                cur = new.copy(); cur[ov] = P[ov].fillna(0).values
            else:
                alpha = 0.5 if "50%" in corr else 1.0
                lvl = corr.split("@")[1]
                keys = a.loc[eans, lvl].values
                r = calib_ratio(P.reindex(columns=elapsed).fillna(0), A[elapsed].fillna(0), keys, alpha, 0.5, 1.5)
                cur = new.mul(r, axis=0)            # meses nuevos: técnica base x corrección
                cur[ov] = P[ov].fillna(0).mul(r, axis=0).values  # meses ya pronosticados: anterior x corrección
            em, tot, _ = score(cur, A)
            rows.append(dict(inicio=start, correccion=corr, snap=s, wmape=em, bias=tot))
            prev = cur
    R = pd.DataFrame(rows)
    w = R.pivot_table(index=["inicio", "correccion"], columns="snap", values="wmape"); w["media"] = w.mean(1)
    b = R.pivot_table(index=["inicio", "correccion"], columns="snap", values="bias"); b.columns = ["bias_" + c for c in b.columns]
    b["|bias|medio"] = b.abs().mean(1)
    T = w.join(b).sort_values("|bias|medio")
    txt = (W / "results" / "tracking.md").read_text()
    txt += "\n\n## 3. Cadena completa: técnica inicial (sep-25) + corrección en cada foto (forecast corregido se arrastra)\n" + T.round(3).to_markdown()
    (W / "results" / "tracking.md").write_text(txt)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
    print(T.round(3).to_string())


if __name__ == "__main__" and "--chain" in sys.argv:
    chain()
