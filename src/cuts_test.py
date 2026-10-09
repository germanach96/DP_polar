"""¿Sumar un % de los supply cuts del año pasado a la base? Regla decidida: LY x (1 + trend12M house x tamaño, Central>=6m, tope ±30%).
Variantes: k = % de cortes añadido (0, 0.25, 0.33, 0.5); dónde: solo base LY / base + cálculo del trend.
Cortes rolling 2025-07..2026-07, 8 meses, verdad = última foto. Evaluación: EANs Central sin manual."""
import sys, warnings
import numpy as np, pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import methods as mt  # noqa
from ptype import add_types  # noqa
warnings.filterwarnings("ignore")
W = Path(__file__).resolve().parents[1] / "work"
M = pd.date_range("2023-07-01", "2027-06-01", freq="MS")
LAST = pd.Timestamp("2026-08-01")


def main():
    H = pd.read_pickle(W / "hist.pkl").reindex(columns=M)
    C = pd.read_pickle(W / "cuts.pkl").reindex(index=H.index, columns=M).fillna(0)
    a = add_types(pd.read_pickle(W / "attr.pkl")).reindex(H.index)
    frag = (a.house != "Kylie Makeup").values
    isf0 = (a.isf.fillna(0) == 0).values
    keys = a.house_ptype.values
    rows = []
    for V in pd.date_range("2025-07-01", "2026-07-01", freq="MS"):
        m = M.get_loc(V)
        Hm = H.values.copy(); Hm[:, m:] = np.nan
        Cm = C.values.copy(); Cm[:, m:] = 0
        first = np.argmax(np.isfinite(Hm), 1).astype(float); first[~np.isfinite(Hm).any(1)] = np.nan
        age = m - first
        central = age >= 6
        fi = [j for j in range(m + 1, m + 9) if M[j] <= LAST]
        A = np.nan_to_num(H.values[:, fi]); Cf = C.values[:, fi]
        for k in (0.0, 0.25, 0.33, 0.5):
            Ha = np.where(np.isfinite(Hm), np.nan_to_num(Hm) + k * Cm, np.nan)
            for where in ("solo_base", "base+trend"):
                if k == 0 and where == "base+trend":
                    continue
                g = mt._group_g(Ha if where == "base+trend" else Hm, m, 12, keys, central)
                g = np.clip(np.nan_to_num(g), -.3, .3)
                base = np.stack([np.nan_to_num(Ha[:, j - 12]) for j in fi], 1)
                F = np.clip(base * (1 + g)[:, None], 0, None)
                ev = frag & central & isf0
                for seg, sel in [("maduros", ev & (age >= 18)), ("central", ev)]:
                    f, aa, cf = F[sel], A[sel], Cf[sel]
                    lyc = np.stack([C.values[sel, j - 12] for j in fi], 1)
                    hit = lyc > 0  # meses cuya base LY tuvo cortes
                    rows.append(dict(origin=V, k=k, where=where, seg=seg, ae=np.abs(f - aa).sum(), e=(f - aa).sum(), A=aa.sum(),
                                     ae_hit=np.abs(f - aa)[hit].sum(), A_hit=aa[hit].sum(), e_hit=(f - aa)[hit].sum(),
                                     ae_dem=np.abs(f - (aa + k * cf)).sum(), A_dem=(aa + k * cf).sum()))
    D = pd.DataFrame(rows)
    g = D.groupby(["seg", "where", "k"])[["ae", "e", "A", "ae_hit", "A_hit", "e_hit", "ae_dem", "A_dem"]].sum()
    out = pd.DataFrame({"WMAPE": g.ae / g.A, "bias": g.e / g.A,
                        "WMAPE_meses_con_cortes_LY": g.ae_hit / g.A_hit, "bias_meses_con_cortes_LY": g.e_hit / g.A_hit,
                        "WMAPE_vs_real+k*cortes": g.ae_dem / g.A_dem})
    w = D.assign(w=D.ae / D.A).pivot_table(index=["seg", "where", "k"], columns="origin", values="w")
    base = w.xs(0.0, level="k", drop_level=False)
    out["gana_a_k0(cortes)"] = [int((w.loc[i] < w.loc[(i[0], "solo_base", 0.0)]).sum()) for i in w.index]
    pd.set_option("display.width", 250)
    print(out.round(3).to_string())
    (W / "results" / "cuts_test.md").write_text("# Cortes en la base (src/cuts_test.py)\n\n" + out.round(3).to_markdown())


if __name__ == "__main__":
    main()
