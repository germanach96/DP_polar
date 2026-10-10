"""Comparación por casa: forecast de consenso (foto) vs regla decidida, contra actuals de la foto 2026-09.
Fotos: 2025-09 (oct-25..jun-26, 9 meses) y 2026-03 (abr-26..dic-26; verdad hasta ago-26 -> 5 meses).
Universo: EANs donde se aplica la regla (Central = >=6 meses de envíos en la foto). Local aparte.
Salida: work/house_compare.json (lo usa src/house_report.py)."""
import sys, json, warnings
import numpy as np, pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import methods as mt  # noqa
from ptype import add_types  # noqa
import snapshots as sn  # noqa
import da_test as dt  # noqa
import mu_backtest as mb  # noqa
warnings.filterwarnings("ignore")
W = Path(__file__).resolve().parents[1] / "work"
M = pd.date_range("2023-07-01", "2027-06-01", freq="MS")
LAST = pd.Timestamp("2026-08-01")
SNAPS = ["2025-09", "2026-03"]


def central_mask(Hm, m):
    first = np.argmax(np.isfinite(Hm), 1).astype(float); first[~np.isfinite(Hm).any(1)] = np.nan
    return (m - first) >= 6, np.isfinite(Hm).any(1)


def segments(H, m, isf):
    Hm = H.copy(); Hm[:, m:] = np.nan
    first = np.argmax(np.isfinite(Hm), 1)
    age = m - first
    return np.where(isf > 0, "Forecast manual", np.where(age >= 18, "Maduros (18+ meses)", "Jóvenes (6-17 meses)"))


def frag_rule(H, C, DAp, keys, m):
    Hm = H.copy(); Hm[:, m:] = np.nan
    central, alive = central_mask(Hm, m)
    g = np.clip(np.nan_to_num(mt._group_g(Hm, m, 12, keys, central)), -.3, .3)
    F = np.stack([np.clip(np.nan_to_num(Hm[:, j - 12]) + 0.25 * C[:, j - 12] - 0.5 * DAp[:, j - 12], 0, None) * (1 + g) for j in range(m + 1, m + 10)], 1)
    return F, central, alive, g


def mu_rule(H, C, DAp, keys, m):
    Hm = H.copy(); Hm[:, m:] = np.nan
    central, alive = central_mask(Hm, m)
    g = np.clip(np.nan_to_num(mt._group_g(Hm, m, 12, keys, central)), -.3, .3)
    adj = np.where(np.isfinite(Hm), np.clip(np.nan_to_num(Hm) + np.minimum(0.10 * C, 0.10 * np.nan_to_num(Hm)) - 0.25 * DAp, 0, None), np.nan)
    base = np.nan_to_num(np.nanmean(adj[:, m - 6:m], 1))
    return np.repeat((base * (1 + 0.5 * g))[:, None], 9, 1), central, alive, g


def summarize(house, snap, eans, F, Cn, A, central, alive, months, attr_desc, local_cons, local_act, g_by_group, seg=None):
    ok = [k for k, t in enumerate(months) if t <= LAST]
    mo = [months[k] for k in ok]
    sel = central
    f, c, a = F[sel][:, ok], Cn[sel][:, ok], A[sel][:, ok]
    wm = lambda x: float(np.abs(x - a).sum() / a.sum())
    bias = lambda x: float(x.sum() / a.sum() - 1)
    # mes a mes (total casa)
    monthly = [dict(mes=t.strftime("%b-%y"), real=float(a[:, i].sum()), consenso=float(c[:, i].sum()), regla=float(f[:, i].sum())) for i, t in enumerate(mo)]
    # por quarter fiscal
    fq = [f"FY{(t.year + (t.month >= 7)) % 100}.Q{((t.month - 7) % 12) // 3 + 1}" for t in mo]
    qs = []
    for q in dict.fromkeys(fq):
        idx = [i for i, x in enumerate(fq) if x == q]
        aa, cc, ff = a[:, idx], c[:, idx], f[:, idx]
        qs.append(dict(q=q, meses=len(idx), real=float(aa.sum()), consenso=float(cc.sum()), regla=float(ff.sum()),
                       err_cons=float(np.abs(cc - aa).sum() / aa.sum()), err_regla=float(np.abs(ff - aa).sum() / aa.sum())))
    # EAN a EAN
    e_cons = np.abs(c - a).sum(1); e_rule = np.abs(f - a).sum(1)
    vol = a.sum(1)
    better = int((e_rule < e_cons).sum()); worse = int((e_rule > e_cons).sum())
    ids = np.array(eans)[sel]
    diff = e_cons - e_rule  # + = la regla ahorra error
    order = np.argsort(-diff)
    top_win = [dict(ean=ids[i], desc=attr_desc.get(ids[i], ""), real=float(vol[i]), consenso=float(c[i].sum()), regla=float(f[i].sum()), ahorro=float(diff[i])) for i in order[:8]]
    top_loss = [dict(ean=ids[i], desc=attr_desc.get(ids[i], ""), real=float(vol[i]), consenso=float(c[i].sum()), regla=float(f[i].sum()), ahorro=float(diff[i])) for i in order[::-1][:5] if diff[i] < 0]
    segs = []
    if seg is not None:
        sg = seg[sel]
        for name in ["Maduros (18+ meses)", "Jóvenes (6-17 meses)", "Forecast manual"]:
            k = sg == name
            if k.sum() == 0:
                continue
            aa, cc, ff = a[k], c[k], f[k]
            segs.append(dict(seg=name, n=int(k.sum()), real=float(aa.sum()), err_cons=float(np.abs(cc - aa).sum() / aa.sum()) if aa.sum() else None,
                             err_regla=float(np.abs(ff - aa).sum() / aa.sum()) if aa.sum() else None,
                             bias_cons=float(cc.sum() / aa.sum() - 1) if aa.sum() else None, bias_regla=float(ff.sum() / aa.sum() - 1) if aa.sum() else None))
    hyb = None
    if seg is not None:
        mat = (seg[sel] == "Maduros (18+ meses)")[:, None]
        h = np.where(mat, f, c)
        hyb = dict(wmape=wm(h), bias=bias(h), total=float(h.sum()), monthly=[float(h[:, i].sum()) for i in range(h.shape[1])])
    return dict(house=house, snap=snap, segs=segs, hibrido=hyb, meses=[t.strftime("%b-%y") for t in mo], n_meses=len(mo),
                n_eans=int(sel.sum()), real=float(a.sum()), consenso=float(c.sum()), regla=float(f.sum()),
                wmape_cons=wm(c), wmape_regla=wm(f), bias_cons=bias(c), bias_regla=bias(f),
                err_total_cons=float(abs(c.sum() - a.sum())), err_total_regla=float(abs(f.sum() - a.sum())),
                eans_mejor=better, eans_peor=worse, monthly=monthly, quarters=qs, top_win=top_win, top_loss=top_loss,
                local_cons=float(local_cons), local_real=float(local_act), trends=g_by_group)


def fragrances(out):
    d = pd.read_parquet(W / "data.parquet")
    H = pd.read_pickle(W / "hist.pkl").reindex(columns=M)
    C = pd.read_pickle(W / "cuts.pkl").reindex(index=H.index, columns=M).fillna(0).values
    a = add_types(pd.read_pickle(W / "attr.pkl")).reindex(H.index)
    mfac = sn.month_factors(d)
    Hv = H.values; A = np.nan_to_num(Hv)
    desc = a.desc.to_dict()
    for s in SNAPS:
        V = pd.Timestamp(s + "-01"); m = M.get_loc(V); months = list(M[m + 1:m + 10])
        DAp = np.clip(np.nan_to_num(dt.da_known(d, H.index, V)[0].values), 0, None)
        F, central, alive, g = frag_rule(Hv, C, DAp, a.house_ptype.values, m)
        x = d[d.version == s]
        cons = x[x.date > V].pivot_table(index="ean", columns="date", values="cons", aggfunc="sum").reindex(index=H.index, columns=months).fillna(0)
        # consenso tal cual estaba en la foto (sin factor de reexpresión: el consenso de o9 ya parece estar en el perímetro nuevo)
        Cn = cons.values; Am = A[:, m + 1:m + 10]
        in_snap = H.index.isin(set(x.ean))
        seg = segments(Hv, m, x.groupby("ean").isf.max().reindex(H.index).fillna(0).values)
        for house, lab in [("BURBERRY", "Burberry"), ("Gucci", "Gucci"), ("CP-Marc Jacobs", "Marc Jacobs")]:
            hs = (a.house == house).values & in_snap
            loc = hs & ~central
            ok = [k for k, t in enumerate(months) if t <= LAST]
            gg = pd.Series(g[hs & central], index=a.ptype.values[hs & central]).groupby(level=0).first().round(3).to_dict()
            out.append(summarize(lab, s, list(H.index[hs]), F[hs], Cn[hs], Am[hs], central[hs], alive[hs], months, desc,
                                 Cn[loc][:, ok].sum(), Am[loc][:, ok].sum(), gg, seg[hs]))


def makeup(out):
    d, Hdf, Edf, Cdf, attr, fac = mb.load()
    H = Hdf.values; C = Cdf.values; eans = Hdf.index; A = np.nan_to_num(H)
    desc = d[d.version == "2026-09"].groupby("ean").desc.first().to_dict()
    for s in SNAPS:
        V = pd.Timestamp(s + "-01"); m = M.get_loc(V); months = list(M[m + 1:m + 10])
        DAp = np.clip(np.nan_to_num(mb.da_known(d, eans, V).values), 0, None); DAp[:, m:] = 0
        F, central, alive, g = mu_rule(H, C, DAp, attr.fam_brand.values, m)
        x = d[d.version == s]
        cons = x[x.date > V].pivot_table(index="ean", columns="date", values="cons", aggfunc="sum").reindex(index=eans, columns=months).fillna(0)
        Cn = cons.values; Am = A[:, m + 1:m + 10]
        in_snap = eans.isin(set(x.ean))
        seg = segments(H, m, x.groupby("ean").isf.max().reindex(eans).fillna(0).values)
        for fam, lab in [("GUMU", "Gucci Make up"), ("KYMU", "Kylie Makeup")]:
            hs = (attr.fam == fam).values & in_snap
            loc = hs & ~central
            ok = [k for k, t in enumerate(months) if t <= LAST]
            gg = pd.Series(g[hs & central], index=attr.brand.values[hs & central]).groupby(level=0).first().round(3).to_dict()
            out.append(summarize(lab, s, list(eans[hs]), F[hs], Cn[hs], Am[hs], central[hs], alive[hs], months, desc,
                                 Cn[loc][:, ok].sum(), Am[loc][:, ok].sum(), gg, seg[hs]))


def main():
    out = []
    fragrances(out); makeup(out)
    (W / "house_compare.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    for r in out:
        print(f"{r['house']:15s} {r['snap']} meses={r['n_meses']} EANs={r['n_eans']:3d} real={r['real']:>10,.0f} cons={r['consenso']:>10,.0f} ({r['bias_cons']:+.1%}) "
              f"regla={r['regla']:>10,.0f} ({r['bias_regla']:+.1%}) | WMAPE cons {r['wmape_cons']:.1%} regla {r['wmape_regla']:.1%} | EANs mejor {r['eans_mejor']} peor {r['eans_peor']} | local real {r['local_real']:,.0f}")


if __name__ == "__main__":
    main()
