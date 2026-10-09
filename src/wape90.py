"""WAPE90 por casa y quarter: consenso de la foto vs regla, contra actuals de la foto sep-26.
WAPE90 = |suma forecast - suma actuals| / suma actuals de la casa en el quarter (desvío total en valor absoluto).
SPP3   = (suma actuals - suma forecast) / suma actuals (mismo desvío con signo: negativo = overforecast, positivo = underforecast).
Se guarda también el error EAN a EAN (suma |F - A| por EAN / suma actuals) como referencia.
Foto sep-25: Q2 (oct-dic 25), Q3 (ene-mar 26), Q4 (abr-jun 26). Foto mar-26: Q4 (abr-jun 26), Q1 FY27 (jul-sep 26; sep sin cerrar -> jul-ago).
Universo: EANs donde se aplica la regla (Central, 6+ meses de envíos en la foto).
Consenso = tal cual en la foto (ya incluye los DAs). Regla + DAs = regla + todos los DAs de la foto en esos meses (positivos y negativos), suelo 0 por EAN-mes.
Se guarda también la regla sin DAs (orig_*) como referencia.
Salida: work/wape90.json"""
import sys, json, warnings
import numpy as np, pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import house_compare as hc  # noqa
import da_test as dt  # noqa
import mu_backtest as mb  # noqa
from ptype import add_types  # noqa
warnings.filterwarnings("ignore")
W = hc.W; M = hc.M; LAST = hc.LAST


def fq(t):
    return f"FY{(t.year + (t.month >= 7)) % 100}.Q{((t.month - 7) % 12) // 3 + 1}"


QNAME = {"FY26.Q2": "Q2 FY26 · oct–dic 25", "FY26.Q3": "Q3 FY26 · ene–mar 26", "FY26.Q4": "Q4 FY26 · abr–jun 26", "FY27.Q1": "Q1 FY27 · jul–ago 26*"}


def quarters(house, snap, F, Cn, A, sel, months, Co):
    rows = []
    qs = [fq(t) for t in months]
    for q in dict.fromkeys(qs):
        idx = [i for i, (x, t) in enumerate(zip(qs, months)) if x == q and t <= LAST]
        if not idx:
            continue
        f = F[sel][:, idx].sum(1); c = Cn[sel][:, idx].sum(1); a = A[sel][:, idx].sum(1); o = Co[sel][:, idx].sum(1)
        rows.append(dict(house=house, snap=snap, q=q, label=QNAME[q], meses=len(idx), real=float(a.sum()),
                         consenso=float(c.sum()), regla=float(f.sum()),
                         wape_cons=float(abs(c.sum() - a.sum()) / a.sum()), wape_regla=float(abs(f.sum() - a.sum()) / a.sum()),
                         spp3_cons=float((a.sum() - c.sum()) / a.sum()), spp3_regla=float((a.sum() - f.sum()) / a.sum()),
                         orig=float(o.sum()), wape_orig=float(abs(o.sum() - a.sum()) / a.sum()), spp3_orig=float((a.sum() - o.sum()) / a.sum()),
                         ean_cons=float(np.abs(c - a).sum() / a.sum()), ean_regla=float(np.abs(f - a).sum() / a.sum()),
                         bias_cons=float(c.sum() / a.sum() - 1), bias_regla=float(f.sum() / a.sum() - 1), eans=int(sel.sum())))
    return rows


def cons_da(x, V, idx, months):
    """Consenso de la foto y DAs netos de la foto, EAN x mes."""
    y = x[x.date > V]
    pv = lambda col: y.pivot_table(index="ean", columns="date", values=col, aggfunc="sum").reindex(index=idx, columns=months).fillna(0).values
    co = pv("cons")
    return co, pv("da")


def main():
    out = []
    d = pd.read_parquet(W / "data.parquet")
    H = pd.read_pickle(W / "hist.pkl").reindex(columns=M)
    C = pd.read_pickle(W / "cuts.pkl").reindex(index=H.index, columns=M).fillna(0).values
    a = add_types(pd.read_pickle(W / "attr.pkl")).reindex(H.index)
    Hv = H.values; A = np.nan_to_num(Hv)
    for s in hc.SNAPS:
        V = pd.Timestamp(s + "-01"); m = M.get_loc(V); months = list(M[m + 1:m + 10])
        DAp = np.clip(np.nan_to_num(dt.da_known(d, H.index, V)[0].values), 0, None)
        F, central, alive, g = hc.frag_rule(Hv, C, DAp, a.house_ptype.values, m)
        x = d[d.version == s]
        Cn, Da = cons_da(x, V, H.index, months)
        Am = A[:, m + 1:m + 10]; in_snap = H.index.isin(set(x.ean))
        for house, lab in [("BURBERRY", "Burberry"), ("Gucci", "Gucci"), ("CP-Marc Jacobs", "Marc Jacobs")]:
            out += quarters(lab, s, np.clip(F + Da, 0, None), Cn, Am, (a.house == house).values & in_snap & central, months, F)
    dm, Hdf, Edf, Cdf, attr, fac = mb.load()
    Hm_ = Hdf.values; Cm = Cdf.values; eans = Hdf.index; Am_ = np.nan_to_num(Hm_)
    for s in hc.SNAPS:
        V = pd.Timestamp(s + "-01"); m = M.get_loc(V); months = list(M[m + 1:m + 10])
        DAp = np.clip(np.nan_to_num(mb.da_known(dm, eans, V).values), 0, None); DAp[:, m:] = 0
        F, central, alive, g = hc.mu_rule(Hm_, Cm, DAp, attr.fam_brand.values, m)
        x = dm[dm.version == s]
        Cn, Da = cons_da(x, V, eans, months)
        Am = Am_[:, m + 1:m + 10]; in_snap = eans.isin(set(x.ean))
        for fam, lab in [("GUMU", "Gucci Make up"), ("KYMU", "Kylie Makeup")]:
            out += quarters(lab, s, np.clip(F + Da, 0, None), Cn, Am, (attr.fam == fam).values & in_snap & central, months, F)
    (W / "wape90.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    df = pd.DataFrame(out)
    pd.set_option("display.width", 250)
    print(df[["house", "snap", "q", "meses", "real", "wape_cons", "wape_regla", "wape_orig", "wape_cons", "wape_regla", "spp3_orig", "spp3_cons", "spp3_regla"]].round(3).to_string())


if __name__ == "__main__":
    main()
