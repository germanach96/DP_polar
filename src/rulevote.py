"""Votación por EAN entre las dos reglas: regla de fragancias vs regla de makeup, aplicadas a TODOS los EANs.

- Fotos comunes a las dos categorías: sep-25 (Q2, Q3, Q4 FY26) y mar-26 (Q4 FY26, Q1 FY27*) -> 5 quarters. Real = foto sep-26.
  * sep-26 no está cerrado: Q1 FY27 = jul-ago.
- Las dos reglas llevan los DAs de la foto en el horizonte (como la comparación estándar contra el consenso).
- Grupo del trend: el natural del EAN en las dos reglas (fragancias: casa x tamaño; makeup: casa x función Face/Lips/Eyes).
- En cada quarter gana la regla con menor |forecast del quarter - real del quarter|.
- El EAN vota por la regla que gana más quarters. Si empatan, se va al detalle: gana la de menor error mes a mes
  (suma de |forecast del mes - real del mes| en esos quarters). Si sigue el empate, el EAN es empate.
- Fuera: EANs sin actividad (real y las dos reglas = 0 en todos sus quarters). Universo: EANs Central de cada foto.
Salida: work/rulevote.json, work/rulevote_ean.parquet"""
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import house_compare as hc  # noqa
import da_test as dt  # noqa
import mu_backtest as mb  # noqa
from ptype import add_types  # noqa
from wape90 import fq, cons_da, ages  # noqa
from votes import AGES, FLAGS  # noqa

warnings.filterwarnings("ignore")
W = hc.W; M = hc.M; LAST = hc.LAST
A_, B_ = "Regla fragancias", "Regla makeup"
FRAG = {"BURBERRY": "Burberry", "Gucci": "Gucci", "CP-Marc Jacobs": "Marc Jacobs"}
MU = {"GUMU": "Gucci Make up", "KYMU": "Kylie Makeup"}
QLAB = {("2025-09", "FY26.Q2"): "sep-25 · Q2 FY26", ("2025-09", "FY26.Q3"): "sep-25 · Q3 FY26", ("2025-09", "FY26.Q4"): "sep-25 · Q4 FY26",
        ("2026-03", "FY26.Q4"): "mar-26 · Q4 FY26", ("2026-03", "FY27.Q1"): "mar-26 · Q1 FY27*"}


def records(cat, lab_of, house_of, eans, s, Ff, Fm, Cn, Da, A, H, m, sel, isf, months, size):
    Ff = np.clip(Ff + Da, 0, None); Fm = np.clip(Fm + Da, 0, None)
    age = ages(H, m); qs = [fq(t) for t in months]; out = []
    for q in dict.fromkeys(qs):
        idx = [i for i, (x, t) in enumerate(zip(qs, months)) if x == q and t <= LAST]
        if not idx:
            continue
        a = A[sel][:, idx]
        out.append(pd.DataFrame(dict(
            ean=eans[sel], cat=cat, house=[lab_of[h] for h in house_of[sel]], size=size[sel], snap=s, q=q, age=age[sel], isf=isf[sel],
            real=a.sum(1), frag=Ff[sel][:, idx].sum(1), mu=Fm[sel][:, idx].sum(1), cons=Cn[sel][:, idx].sum(1),
            mae_frag=np.abs(Ff[sel][:, idx] - a).sum(1), mae_mu=np.abs(Fm[sel][:, idx] - a).sum(1))))
    return out


def build():
    out = []
    d = pd.read_parquet(W / "data.parquet")
    Hd = pd.read_pickle(W / "hist.pkl").reindex(columns=M)
    C = pd.read_pickle(W / "cuts.pkl").reindex(index=Hd.index, columns=M).fillna(0).values
    a = add_types(pd.read_pickle(W / "attr.pkl")).reindex(Hd.index)
    Hv = Hd.values; A = np.nan_to_num(Hv); keys = a.house_ptype.values
    for s in hc.SNAPS:
        V = pd.Timestamp(s + "-01"); m = M.get_loc(V); months = list(M[m + 1:m + 10])
        DAp = np.clip(np.nan_to_num(dt.da_known(d, Hd.index, V)[0].values), 0, None)
        Ff, central, _, _ = hc.frag_rule(Hv, C, DAp, keys, m)
        Fm = hc.mu_rule(Hv, C, DAp, keys, m)[0]
        x = d[d.version == s]
        Cn, Da = cons_da(x, V, Hd.index, months)
        isf = x.groupby("ean").isf.max().reindex(Hd.index).fillna(0).values
        sel = a.house.isin(FRAG).values & Hd.index.isin(set(x.ean)) & central
        out += records("Fragancias", FRAG, a.house.values, Hd.index.values, s, Ff, Fm, Cn, Da, A[:, m + 1:m + 10], Hv, m, sel, isf, months, a.ptype.values)
    dm, Hdf, Edf, Cdf, attr, fac = mb.load()
    Hm_ = Hdf.values; eans = Hdf.index; Am_ = np.nan_to_num(Hm_); keys = attr.fam_brand.values
    for s in hc.SNAPS:
        V = pd.Timestamp(s + "-01"); m = M.get_loc(V); months = list(M[m + 1:m + 10])
        DAp = np.clip(np.nan_to_num(mb.da_known(dm, eans, V).values), 0, None); DAp[:, m:] = 0
        Fm, central, _, _ = hc.mu_rule(Hm_, Cdf.values, DAp, keys, m)
        Ff = hc.frag_rule(Hm_, Cdf.values, DAp, keys, m)[0]
        x = dm[dm.version == s]
        Cn, Da = cons_da(x, V, eans, months)
        isf = x.groupby("ean").isf.max().reindex(eans).fillna(0).values
        sel = attr.fam.isin(MU).values & eans.isin(set(x.ean)) & central
        out += records("Makeup", MU, attr.fam.values, eans.values, s, Ff, Fm, Cn, Da, Am_[:, m + 1:m + 10], Hm_, m, sel, isf, months,
                       np.full(len(eans), None))
    return pd.concat(out, ignore_index=True)


def tally(g):
    n = len(g); ra = int((g.voto == A_).sum()); rb = int((g.voto == B_).sum()); vol = g.real.sum() or 1
    return dict(eans=n, a=ra, b=rb, empate=n - ra - rb, desempate=int(g.desempate.sum()),
                vol_a=float(g.real[g.voto == A_].sum() / vol), vol_b=float(g.real[g.voto == B_].sum() / vol),
                vol_emp=float(g.real[g.voto == "Empate"].sum() / vol), q_a=int(g.p_a.sum()), q_b=int(g.p_b.sum()),
                q_total=int(g.quarters.sum()), real=float(g.real.sum()))


def main():
    e = build()
    ea, eb = (e.frag - e.real).abs(), (e.mu - e.real).abs()
    e["p_a"] = (ea < eb).astype(int); e["p_b"] = (eb < ea).astype(int)
    e["act"] = (e.real + e.frag + e.mu) > 0
    e["qlab"] = [QLAB[(s, q)] for s, q in zip(e.snap, e.q)]
    last = e.sort_values("snap").groupby("ean").last()
    v = e.groupby("ean").agg(cat=("cat", "first"), house=("house", "first"), size=("size", "first"), quarters=("q", "size"),
                             real=("real", "sum"), p_a=("p_a", "sum"), p_b=("p_b", "sum"),
                             mae_a=("mae_frag", "sum"), mae_b=("mae_mu", "sum"), act=("act", "any"))
    v["edad"] = pd.cut(last.age, [0, 11, 17, 23, 999], labels=AGES).astype(str)
    v["bandera"] = last.isf.map(FLAGS)
    inactive = int((~v.act).sum()); v = v[v.act].copy()
    tie = v.p_a == v.p_b
    v["desempate"] = tie & (v.mae_a != v.mae_b)
    v["voto"] = np.where(v.p_a > v.p_b, A_, np.where(v.p_b > v.p_a, B_,
                         np.where(v.mae_a < v.mae_b, A_, np.where(v.mae_b < v.mae_a, B_, "Empate"))))
    v.to_parquet(W / "rulevote_ean.parquet")
    # voto por quarter (cada quarter es una elección: gana la regla con menor error del quarter en ese EAN)
    ea_act = e[e.act]
    per_q = {}
    for lab in QLAB.values():
        g = ea_act[ea_act.qlab == lab]
        if g.empty:
            continue
        vq = np.where(g.p_a > 0, A_, np.where(g.p_b > 0, B_, "Empate"))
        gg = g.assign(voto=vq, quarters=1, desempate=False)
        per_q[lab] = tally(gg)
        tot = g.real.sum()
        per_q[lab].update(wape_a=float(abs(g.frag.sum() - tot) / tot), wape_b=float(abs(g.mu.sum() - tot) / tot),
                          wape_c=float(abs(g.cons.sum() - tot) / tot),
                          ean_a=float((g.frag - g.real).abs().sum() / tot), ean_b=float((g.mu - g.real).abs().sum() / tot))
    # WAPE90 por casa x quarter
    w90 = []
    for (h, lab), g in ea_act.groupby(["house", "qlab"]):
        tot = g.real.sum()
        w90.append(dict(house=h, q=lab, real=float(tot), a=float(abs(g.frag.sum() - tot) / tot), b=float(abs(g.mu.sum() - tot) / tot),
                        c=float(abs(g.cons.sum() - tot) / tot)))
    out = {"inactivos": inactive, "total": tally(v), "por_q": per_q, "w90": w90, "por": {}}
    for col, name in [("cat", "Categoría"), ("house", "Casa"), ("size", "Tamaño"), ("edad", "Edad"), ("bandera", "Bandera")]:
        out["por"][name] = {str(k): tally(g) for k, g in v.dropna(subset=[col]).groupby(col)}
    (W / "rulevote.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    fmt = lambda k, t: (f"{k:<24} EANs {t['eans']:>4} | Fragancias {t['a']:>4} ({t['a'] / t['eans']:.0%}) Makeup {t['b']:>4} ({t['b'] / t['eans']:.0%}) "
                        f"Empate {t['empate']:>3} | vol frag {t['vol_a']:.0%} mu {t['vol_b']:.0%}")
    print(f"EANs sin actividad (fuera): {inactive}; desempatados por el detalle mensual: {out['total']['desempate']}")
    print(fmt("TOTAL", out["total"]))
    print("\n— Por quarter (WAPE90 frag / makeup / consenso)")
    for k, t in per_q.items():
        print(fmt(k, t), f"| WAPE90 {t['wape_a']:.1%} / {t['wape_b']:.1%} / {t['wape_c']:.1%} | error EAN {t['ean_a']:.1%} / {t['ean_b']:.1%}")
    for name, dd in out["por"].items():
        print(f"\n— {name}")
        for k, t in dd.items():
            print(fmt(k, t))
    print("\n— WAPE90 casa x quarter (frag / makeup / consenso)")
    print(pd.DataFrame(w90).round(3).to_string())


if __name__ == "__main__":
    main()
