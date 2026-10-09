"""Demand Assumptions (DA) positivos: ¿restar k% de los DA del año pasado a la base? ¿sumar k% de los DA futuros? ¿quitar DA del histórico del trend?
Regla base: (LY + 25% cortes LY) x (1 + trend12M house x tamaño, Central>=6m, tope ±30%). Solo fragancias.
Información disponible en cada corte: DA de las versiones con fecha <= corte (para el pasado, la versión más reciente que tenga ese mes;
para el futuro, la última versión <= corte). Cortes: 2025-09..2026-07 (mensual) y aparte las 4 fotos."""
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
VERS = ["2025-09", "2025-12", "2026-03", "2026-06", "2026-09"]


def da_known(d, eans, V):
    """Matriz DA (ean x M) conocida en el corte V: por mes, la versión más reciente <= V que tenga dato."""
    vs = [v for v in VERS if pd.Timestamp(v + "-01") <= V]
    out = pd.DataFrame(np.nan, index=eans, columns=M)
    for v in vs:  # en orden: las más recientes sobreescriben
        p = d[d.version == v].pivot_table(index="ean", columns="date", values="da", aggfunc="sum").reindex(index=eans, columns=M)
        out = p.combine_first(out) if False else out.where(p.isna(), p)
    return out, vs[-1]


def main():
    d = pd.read_parquet(W / "data.parquet")
    H = pd.read_pickle(W / "hist.pkl").reindex(columns=M)
    C = pd.read_pickle(W / "cuts.pkl").reindex(index=H.index, columns=M).fillna(0)
    a = add_types(pd.read_pickle(W / "attr.pkl")).reindex(H.index)
    eans = H.index
    frag = (a.house != "Kylie Makeup").values
    isf0 = (a.isf.fillna(0) == 0).values
    keys = a.house_ptype.values
    rows = []
    for V in pd.date_range("2025-09-01", "2026-07-01", freq="MS"):
        m = M.get_loc(V)
        DA, vlast = da_known(d, eans, V)
        DAv = DA.values
        DAp = np.clip(np.nan_to_num(DAv), 0, None)          # solo positivos
        DAall = np.nan_to_num(DAv)
        Hm = H.values.copy(); Hm[:, m:] = np.nan
        first = np.argmax(np.isfinite(Hm), 1).astype(float); first[~np.isfinite(Hm).any(1)] = np.nan
        age = m - first; central = age >= 6
        fi = [j for j in range(m + 1, m + 9) if M[j] <= LAST]
        A = np.nan_to_num(H.values[:, fi])
        g0 = np.clip(np.nan_to_num(mt._group_g(Hm, m, 12, keys, central)), -.3, .3)
        ly = np.stack([np.nan_to_num(Hm[:, j - 12]) + 0.25 * C.values[:, j - 12] for j in fi], 1)
        daLY = np.stack([DAp[:, j - 12] for j in fi], 1)
        daF = np.stack([DAp[:, j] for j in fi], 1)
        daFall = np.stack([DAall[:, j] for j in fi], 1)
        ev = frag & central & isf0
        variants = {}
        for k in (0, 0.25, 0.5, 0.75, 1.0):
            variants[("base: restar DA+ LY", k)] = np.clip(ly - k * daLY, 0, None) * (1 + g0)[:, None]
            variants[("futuro: sumar DA+", k)] = ly * (1 + g0)[:, None] + k * daF
            variants[("futuro: sumar DA (+ y -)", k)] = np.clip(ly * (1 + g0)[:, None] + k * daFall, 0, None)
            variants[("base y futuro (DA+)", k)] = np.clip(ly - k * daLY, 0, None) * (1 + g0)[:, None] + k * daF
            Ht = np.where(np.isfinite(Hm), np.clip(np.nan_to_num(Hm) - k * DAp, 0, None), np.nan)
            gt = np.clip(np.nan_to_num(mt._group_g(Ht, m, 12, keys, central)), -.3, .3)
            variants[("trend: quitar DA+ del histórico", k)] = ly * (1 + gt)[:, None]
        for (nm, k), F in variants.items():
            for seg, sel in [("maduros", ev & (age >= 18)), ("central", ev)]:
                f, aa = F[sel], A[sel]
                hit = (daLY[sel] > 0) | (daF[sel] > 0)
                rows.append(dict(origin=V, uso=nm, k=k, seg=seg, ae=np.abs(f - aa).sum(), e=(f - aa).sum(), A=aa.sum(),
                                 ae_h=np.abs(f - aa)[hit].sum(), e_h=(f - aa)[hit].sum(), A_h=aa[hit].sum(),
                                 snap=V.strftime("%Y-%m") in VERS))
    D = pd.DataFrame(rows)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
    L = ["# DA positivos (src/da_test.py)\n"]
    for lab, sub in [("11 cortes mensuales (sep-25..jul-26)", D), ("solo las 4 fotos S&OP", D[D.snap])]:
        g = sub.groupby(["seg", "uso", "k"])[["ae", "e", "A", "ae_h", "e_h", "A_h"]].sum()
        out = pd.DataFrame({"WMAPE": g.ae / g.A, "bias": g.e / g.A, "WMAPE_EAN-mes_con_DA": g.ae_h / g.A_h, "bias_con_DA": g.e_h / g.A_h})
        w = sub.assign(w=sub.ae / sub.A).pivot_table(index=["seg", "uso", "k"], columns="origin", values="w")
        out["gana_a_k0"] = [int((w.loc[i] < w.loc[(i[0], i[1], 0)]).sum()) for i in w.index]
        out["n_cortes"] = w.notna().sum(1)
        print("====", lab); print(out.round(3).to_string())
        L += [f"\n## {lab}\n", out.round(3).to_markdown()]
    (W / "results" / "da_test.md").write_text("\n".join(L))


if __name__ == "__main__":
    main()
