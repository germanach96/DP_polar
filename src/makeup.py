"""Makeup (Kylie): qué trend/regla seguir. Cortes rolling 2025-01..2026-07 (mes en curso excluido), horizonte 8 meses.
Universo evaluado: EANs Kylie con >=6 meses de envíos en el corte (Local = <6m fuera). Verdad = última foto."""
import sys, warnings
import numpy as np, pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import methods as mt  # noqa
warnings.filterwarnings("ignore")
W = Path(__file__).resolve().parents[1] / "work"
M = pd.date_range("2023-07-01", "2027-06-01", freq="MS")
LAST = pd.Timestamp("2026-08-01")


def main():
    H = pd.read_pickle(W / "hist.pkl").reindex(columns=M); a = pd.read_pickle(W / "attr.pkl").reindex(H.index)
    a["all"] = "ALL"; a["frag"] = np.where(a.house == "Kylie Makeup", "MAKEUP", "FRAG")
    kyl = (a.house == "Kylie Makeup").values
    rows = []
    for V in pd.date_range("2025-01-01", "2026-07-01", freq="MS"):
        m = M.get_loc(V)
        Hm = H.values.copy(); Hm[:, m:] = np.nan
        first = np.argmax(np.isfinite(Hm), 1).astype(float); first[~np.isfinite(Hm).any(1)] = np.nan
        age = m - first
        central = age >= 6
        fi = [j for j in range(m + 1, m + 9) if M[j] <= LAST]
        A = np.nan_to_num(H.values[:, fi])
        ly = np.stack([np.nan_to_num(Hm[:, j - 12]) for j in fi], 1)
        R = {"LY_plano": ly}
        for lvl, lab in [("ean", "EAN"), ("brand", "función(brand)"), ("house", "house"), ("frag", "categoría_makeup"), ("all", "empresa_total")]:
            for w in (3, 6, 12):
                if lvl == "ean":
                    g = mt.g_flat(Hm, m, w)
                else:
                    g = mt._group_g(Hm, m, w, a[lvl].values, central)
                g = np.nan_to_num(g)
                for cap in (None, 0.3):
                    gg = g if cap is None else np.clip(g, -cap, cap)
                    for pct in (1.0, 0.5):
                        R[f"trend{w}M@{lab}{'|tope30' if cap else ''}x{pct}"] = np.clip(ly * (1 + pct * gg)[:, None], 0, None)
        # ritmo de venta (sin LY): media / mediana de los últimos meses, plano para el futuro
        for w in (3, 6, 12):
            X = Hm[:, m - w:m]
            R[f"media_{w}M_plano"] = np.repeat(np.nan_to_num(np.nanmean(X, 1))[:, None], len(fi), 1)
            R[f"mediana_{w}M_plano"] = np.repeat(np.nan_to_num(np.nanmedian(X, 1))[:, None], len(fi), 1)
        # media 12M x trend house 12M
        g12 = np.clip(np.nan_to_num(mt._group_g(Hm, m, 12, a.house.values, central)), -.3, .3)
        R["media_12M_x_trend12M@house|tope30"] = R["media_12M_plano"] * (1 + g12)[:, None]
        R["mediana_6M_x_trend12M@house|tope30"] = R["mediana_6M_plano"] * (1 + g12)[:, None]
        R["mix(LY_trend12M@house|tope30, mediana_6M)"] = 0.5 * R["trend12M@house|tope30x1.0"] + 0.5 * R["mediana_6M_plano"]
        sel = kyl & central
        for nm, F in R.items():
            f, aa = F[sel], A[sel]
            rows.append(dict(origin=V, rule=nm, ae=np.abs(f - aa).sum(), e=(f - aa).sum(), A=aa.sum(), F=f.sum()))
    D = pd.DataFrame(rows)
    g = D.groupby("rule")[["ae", "e", "A"]].sum()
    out = pd.DataFrame({"WMAPE_EAN_mes": g.ae / g.A, "bias": g.e / g.A})
    tot = D.assign(err=(D.F / D.A - 1)).groupby("rule").err
    out["error_total_8m_medio(abs)"] = tot.apply(lambda x: x.abs().mean())
    out["error_total_P10"] = tot.quantile(0.1); out["error_total_P90"] = tot.quantile(0.9)
    w_origin = D.assign(w=D.ae / D.A).pivot_table(index="rule", columns="origin", values="w")
    out["gana_a_LY(cortes)"] = (w_origin.lt(w_origin.loc["LY_plano"], axis=1)).sum(1)
    out = out.sort_values("WMAPE_EAN_mes")
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
    print(out.round(3).head(40).to_string())
    print(out.loc[[r for r in ["LY_plano", "trend12M@housex1.0", "trend12M@house|tope30x1.0", "trend6M@EANx1.0", "trend12M@EAN|tope30x1.0", "trend12M@función(brand)|tope30x1.0", "trend12M@categoría_makeup|tope30x1.0", "trend12M@empresa_total|tope30x1.0"] if r in out.index]].round(3).to_string())
    (W / "results" / "makeup.md").write_text("# Makeup (Kylie) — src/makeup.py\n\n19 cortes rolling, 8 meses, EANs >=6m.\n\n" + out.round(3).to_markdown())


if __name__ == "__main__":
    main()
