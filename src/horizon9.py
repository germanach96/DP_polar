"""Justificación del horizonte de 9 meses: error por mes del horizonte (lag 1-9) de las reglas decididas, recalculadas cada mes.
Fragancias: base = LY + 25% cortes LY - 50% DA+ LY ; x (1 + trend12M house x tamaño, Central >=6m, tope ±30%).
Makeup: base = media 6M de (envío + min(10% cortes;10% envío) - 25% DA+) ; x (1 + 50% trend12M función, tope ±30%).
Comparadas con: año pasado tal cual y método actual del equipo (trend YoY 6M EAN a EAN aplicado al año pasado).
Cortes mensuales 2025-07..2026-07; verdad hasta 2026-08. -> work/results/horizon9.md"""
import sys, warnings
import numpy as np, pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import methods as mt  # noqa
from ptype import add_types  # noqa
import mu_backtest as mb  # noqa
import da_test as dt  # noqa
warnings.filterwarnings("ignore")
W = Path(__file__).resolve().parents[1] / "work"
M = pd.date_range("2023-07-01", "2027-06-01", freq="MS")
LAST = pd.Timestamp("2026-08-01")
NL = 9


def rows_for(F, A, sel, m, rule, fam):
    out = []
    for k in range(1, NL + 1):
        j = m + k
        if M[j] > LAST:
            break
        f, a = F[sel, k - 1], A[sel, j]
        out.append(dict(regla=rule, fam=fam, lag=k, ae=np.abs(f - a).sum(), e=(f - a).sum(), A=a.sum()))
    return out


def fragrances():
    d = pd.read_parquet(W / "data.parquet")
    H = pd.read_pickle(W / "hist.pkl").reindex(columns=M)
    C = pd.read_pickle(W / "cuts.pkl").reindex(index=H.index, columns=M).fillna(0).values
    a = add_types(pd.read_pickle(W / "attr.pkl")).reindex(H.index)
    Hv = H.values; A = np.nan_to_num(Hv)
    frag = (a.house != "Kylie Makeup").values; isf0 = (a.isf.fillna(0) == 0).values
    rows = []
    for V in pd.date_range("2025-07-01", "2026-07-01", freq="MS"):
        m = M.get_loc(V)
        Hm = Hv.copy(); Hm[:, m:] = np.nan
        first = np.argmax(np.isfinite(Hm), 1).astype(float); first[~np.isfinite(Hm).any(1)] = np.nan
        central = (m - first) >= 6
        DAp = (np.clip(np.nan_to_num(dt.da_known(d, H.index, V)[0].values), 0, None) if V >= pd.Timestamp("2025-09-01")
               else np.zeros(Hv.shape))  # antes de la primera foto no hay DAs conocidos
        g = np.clip(np.nan_to_num(mt._group_g(Hm, m, 12, a.house_ptype.values, central)), -.3, .3)
        ly = np.stack([np.nan_to_num(Hm[:, m + k - 12]) for k in range(1, NL + 1)], 1)
        base = np.clip(np.stack([np.nan_to_num(Hm[:, m + k - 12]) + 0.25 * C[:, m + k - 12] - 0.5 * DAp[:, m + k - 12] for k in range(1, NL + 1)], 1), 0, None)
        g6 = np.nan_to_num(mt.g_flat(Hm, m, 6))
        sel = frag & central & isf0
        for nm, F in [("Regla", base * (1 + g)[:, None]), ("Año pasado tal cual", ly), ("Método actual (trend 6M EAN)", np.clip(ly * (1 + g6)[:, None], 0, None))]:
            rows += rows_for(F, A, sel, m, nm, "Fragancias")
    return rows


def makeup():
    d, Hdf, Edf, Cdf, attr, fac = mb.load()
    H = Hdf.values; C = Cdf.values; eans = Hdf.index; A = np.nan_to_num(H)
    rows = []
    for V in pd.date_range("2025-07-01", "2026-07-01", freq="MS"):
        m = M.get_loc(V)
        DAp = np.clip(np.nan_to_num(mb.da_known(d, eans, V).values), 0, None); DAp[:, m:] = 0
        Hm = H.copy(); Hm[:, m:] = np.nan
        first = np.argmax(np.isfinite(Hm), 1).astype(float); first[~np.isfinite(Hm).any(1)] = np.nan
        central = (m - first) >= 6
        g = np.clip(np.nan_to_num(mt._group_g(Hm, m, 12, attr.fam_brand.values, central)), -.3, .3)
        adj = np.where(np.isfinite(Hm), np.clip(np.nan_to_num(Hm) + np.minimum(0.10 * C, 0.10 * np.nan_to_num(Hm)) - 0.25 * DAp, 0, None), np.nan)
        base = np.nan_to_num(np.nanmean(adj[:, m - 6:m], 1))
        F = np.repeat((base * (1 + 0.5 * g))[:, None], NL, 1)
        ly = np.stack([np.nan_to_num(Hm[:, m + k - 12]) for k in range(1, NL + 1)], 1)
        g6 = np.nan_to_num(mt.g_flat(Hm, m, 6))
        for fam in ["GUMU", "KYMU"]:
            sel = central & (attr.fam.values == fam)
            lab = "Gucci Make up" if fam == "GUMU" else "Kylie Makeup"
            for nm, FF in [("Regla", F), ("Año pasado tal cual", ly), ("Método actual (trend 6M EAN)", np.clip(ly * (1 + g6)[:, None], 0, None))]:
                rows += rows_for(FF, A, sel, m, nm, lab)
    return rows


def main():
    R = pd.DataFrame(fragrances() + makeup())
    g = R.groupby(["fam", "regla", "lag"])[["ae", "e", "A"]].sum()
    g["wmape"] = g.ae / g.A; g["bias"] = g.e / g.A
    tw = g.wmape.unstack("lag"); tb = g.bias.unstack("lag")
    n = R[R.regla == "Regla"].groupby(["fam", "lag"]).size().unstack("lag").iloc[0] // 1
    L = ["# Horizonte de 9 meses (src/horizon9.py)\n",
         "Error EAN-mes (WMAPE) por mes del horizonte. Reglas recalculadas cada mes con los últimos 12 meses cerrados. "
         "Cortes mensuales jul-25..jul-26; el mes 9 solo tiene verdad para 5 cortes.\n",
         "## WMAPE por mes del horizonte\n", tw.round(3).to_markdown(), "\n## Desvío (bias) por mes del horizonte\n", tb.round(3).to_markdown()]
    tot = R.groupby(["fam", "regla"])[["ae", "e", "A"]].sum(); tot["wmape"] = tot.ae / tot.A; tot["bias"] = tot.e / tot.A
    L += ["\n## Total meses 1-9\n", tot[["wmape", "bias"]].round(3).to_markdown()]
    (W / "results" / "horizon9.md").write_text("\n".join(L))
    pd.set_option("display.width", 250)
    print(tw.round(2).to_string()); print(tb.round(2).to_string()); print(tot[["wmape", "bias"]].round(3).to_string())


if __name__ == "__main__":
    main()
