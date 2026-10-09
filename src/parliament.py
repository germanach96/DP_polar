"""Parlamento de 6 reglas: cada EAN vota por la regla que mejor le hubiera funcionado.

Partidos (todos suman los DAs de la foto en los meses del horizonte, positivos y negativos; suelo 0 por EAN-mes):
  Año pasado              mismo mes del año anterior
  Regla fragancias        (año pasado + 25% cortes - 50% DAs+) x (1 + trend 12M del grupo, tope ±30%)
  Año pasado × línea      año pasado x (1 + trend 12M de su product line, tope ±30%);
                          si la line tiene menos de 5 EANs Central, usa el trend del grupo
  Regla makeup            media de 6 meses ajustados x (1 + 50% del trend 12M del grupo)
  Media 3M                media de los últimos 3 meses, plana
  Media 6M estacional     nivel de los últimos 6 meses sin temporada x perfil mensual del año pasado de su grupo
Grupo: casa x tamaño (fragancias) / casa x función (makeup). Trends: suma 12M / 12M anteriores - 1, EANs Central.

Elección (la misma que antes):
  - 5 quarters: foto sep-25 (Q2, Q3, Q4 FY26) y foto mar-26 (Q4 FY26, Q1 FY27*). Real = foto sep-26. * Q1 FY27 = jul-ago.
  - En cada quarter gana el partido con menor |forecast del quarter - real del quarter| (si empatan los mejores, nadie suma).
  - El EAN vota por el partido que gana más quarters; si empatan, decide el menor error mes a mes entre los empatados.
  - Universo: EANs Central de cada foto con actividad.
Salida: work/parliament.json, work/parliament_ean.parquet, work/parliament_q.parquet"""
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import house_compare as hc  # noqa
import methods as mt  # noqa
import da_test as dt  # noqa
import mu_backtest as mb  # noqa
from ptype import add_types  # noqa
from wape90 import fq, cons_da, ages  # noqa
from votes import AGES, FLAGS  # noqa

warnings.filterwarnings("ignore")
W = hc.W; M = hc.M; LAST = hc.LAST
PARTIES = ["Año pasado", "Regla fragancias", "Año pasado × línea", "Media 6M estacional", "Regla makeup", "Media 3M"]
KEY = {"Año pasado": "ly", "Regla fragancias": "rf", "Año pasado × línea": "lyl", "Media 6M estacional": "m6s", "Regla makeup": "rm", "Media 3M": "m3"}
MIN_LINE = 5
FRAG = {"BURBERRY": "Burberry", "Gucci": "Gucci", "CP-Marc Jacobs": "Marc Jacobs"}
MU = {"GUMU": "Gucci Make up", "KYMU": "Kylie Makeup"}
QLAB = {("2025-09", "FY26.Q2"): "sep-25 · Q2 FY26", ("2025-09", "FY26.Q3"): "sep-25 · Q3 FY26", ("2025-09", "FY26.Q4"): "sep-25 · Q4 FY26",
        ("2026-03", "FY26.Q4"): "mar-26 · Q4 FY26", ("2026-03", "FY27.Q1"): "mar-26 · Q1 FY27*"}


def parties(H, C, DAp, group, line, m):
    """Los 6 partidos sin DAs futuros, n x 9 meses (m+1 .. m+9). Historia hasta el mes anterior a la foto, como las reglas."""
    Hm = H.copy(); Hm[:, m:] = np.nan
    H0 = np.nan_to_num(Hm)
    central = hc.central_mask(Hm, m)[0]
    fut = range(m + 1, m + 10)
    ly = np.stack([H0[:, j - 12] for j in fut], 1)
    rf = hc.frag_rule(H, C, DAp, group, m)[0]
    rm = hc.mu_rule(H, C, DAp, group, m)[0]
    # trend de la product line con vuelta al grupo si la line tiene pocos EANs Central
    g_grp = np.clip(np.nan_to_num(mt._group_g(Hm, m, 12, group, central)), -.3, .3)
    g_line = mt._group_g(Hm, m, 12, line, central)
    n_line = pd.Series(central.astype(int)).groupby(line).transform("sum").values
    g_l = np.where((n_line >= MIN_LINE) & np.isfinite(g_line), np.clip(np.nan_to_num(g_line), -.3, .3), g_grp)
    lyl = ly * (1 + g_l)[:, None]
    m3 = np.repeat(H0[:, m - 3:m].mean(1)[:, None], 9, 1)
    # media 6M estacional: perfil mensual del grupo en los últimos 12 meses (EANs Central)
    X = H0[:, m - 12:m] * central[:, None]
    G = pd.DataFrame(X).groupby(group).sum()
    prof = G.div(G.mean(1).where(lambda s: s > 0), axis=0).fillna(1.0)
    prof = prof.where(prof > 0, 1.0)
    idx = prof.reindex(group).values                       # n x 12: índice de los meses m-12 .. m-1
    level = (H0[:, m - 6:m] / idx[:, 6:]).mean(1)          # últimos 6 meses sin temporada
    m6s = level[:, None] * np.stack([idx[:, (j - 12) - (m - 12)] for j in fut], 1)   # mismo mes del año pasado
    return {"ly": ly, "rf": rf, "lyl": lyl, "rm": rm, "m3": m3, "m6s": m6s}, central, g_l, n_line


def records(cat, lab_of, house_of, eans, s, P, Da, A, H, m, sel, isf, months, size):
    P = {k: np.clip(v + Da, 0, None) for k, v in P.items()}
    age = ages(H, m); qs = [fq(t) for t in months]; out = []
    for q in dict.fromkeys(qs):
        idx = [i for i, (x, t) in enumerate(zip(qs, months)) if x == q and t <= LAST]
        if not idx:
            continue
        a = A[sel][:, idx]
        df = pd.DataFrame(dict(ean=eans[sel], cat=cat, house=[lab_of[h] for h in house_of[sel]], size=size[sel], snap=s, q=q,
                               age=age[sel], isf=isf[sel], real=a.sum(1)))
        for k, v in P.items():
            df[k] = v[sel][:, idx].sum(1)
            df["mae_" + k] = np.abs(v[sel][:, idx] - a).sum(1)
        out.append(df)
    return out


def build():
    out = []
    d = pd.read_parquet(W / "data.parquet")
    Hd = pd.read_pickle(W / "hist.pkl").reindex(columns=M)
    C = pd.read_pickle(W / "cuts.pkl").reindex(index=Hd.index, columns=M).fillna(0).values
    a = add_types(pd.read_pickle(W / "attr.pkl")).reindex(Hd.index)
    Hv = Hd.values; A = np.nan_to_num(Hv)
    group = a.house_ptype.values; line = (a.house.astype(str) + "|" + a.pline.astype(str)).values
    for s in hc.SNAPS:
        V = pd.Timestamp(s + "-01"); m = M.get_loc(V); months = list(M[m + 1:m + 10])
        DAp = np.clip(np.nan_to_num(dt.da_known(d, Hd.index, V)[0].values), 0, None)
        P, central, _, _ = parties(Hv, C, DAp, group, line, m)
        x = d[d.version == s]
        _, Da = cons_da(x, V, Hd.index, months)
        isf = x.groupby("ean").isf.max().reindex(Hd.index).fillna(0).values
        sel = a.house.isin(FRAG).values & Hd.index.isin(set(x.ean)) & central
        out += records("Fragancias", FRAG, a.house.values, Hd.index.values, s, P, Da, A[:, m + 1:m + 10], Hv, m, sel, isf, months, a.ptype.values)
    dm, Hdf, Edf, Cdf, attr, fac = mb.load()
    Hm_ = Hdf.values; eans = Hdf.index; Am_ = np.nan_to_num(Hm_)
    group = attr.fam_brand.values; line = (attr.fam.astype(str) + "|" + attr.pline.astype(str)).values
    for s in hc.SNAPS:
        V = pd.Timestamp(s + "-01"); m = M.get_loc(V); months = list(M[m + 1:m + 10])
        DAp = np.clip(np.nan_to_num(mb.da_known(dm, eans, V).values), 0, None); DAp[:, m:] = 0
        P, central, _, _ = parties(Hm_, Cdf.values, DAp, group, line, m)
        x = dm[dm.version == s]
        _, Da = cons_da(x, V, eans, months)
        isf = x.groupby("ean").isf.max().reindex(eans).fillna(0).values
        sel = attr.fam.isin(MU).values & eans.isin(set(x.ean)) & central
        out += records("Makeup", MU, attr.fam.values, eans.values, s, P, Da, Am_[:, m + 1:m + 10], Hm_, m, sel, isf, months,
                       np.full(len(eans), None))
    e = pd.concat(out, ignore_index=True)
    e["qlab"] = [QLAB[(s, q)] for s, q in zip(e.snap, e.q)]
    return e


def tally(g):
    n = len(g); vol = g.real.sum() or 1
    t = dict(eans=int(n), real=float(g.real.sum()), seats={}, vol={})
    for p in PARTIES + ["Empate"]:
        mk = g.voto == p
        t["seats"][p] = int(mk.sum()); t["vol"][p] = float(g.real[mk].sum() / vol)
    t["win_eans"] = max(PARTIES, key=lambda p: t["seats"][p]); t["win_vol"] = max(PARTIES, key=lambda p: t["vol"][p])
    return t


def main():
    e = build()
    ks = [KEY[p] for p in PARTIES]
    err = np.stack([(e[k] - e.real).abs().values for k in ks], 1)
    best = err.min(1, keepdims=True)
    winners = np.isclose(err, best)
    e["act"] = (e.real + e[ks].sum(1)) > 0
    unique = winners.sum(1) == 1
    e["ganador_q"] = np.where(unique, np.array(PARTIES, dtype=object)[err.argmin(1)], "Empate")
    for p in PARTIES:
        e["p:" + p] = (e.ganador_q == p).astype(int)
    e.to_parquet(W / "parliament_q.parquet")
    ea = e[e.act]
    last = e.sort_values("snap").groupby("ean").last()
    agg = {"cat": ("cat", "first"), "house": ("house", "first"), "size": ("size", "first"), "quarters": ("q", "size"), "real": ("real", "sum"),
           "act": ("act", "any")}
    agg.update({"p:" + p: ("p:" + p, "sum") for p in PARTIES}); agg.update({"mae:" + p: ("mae_" + KEY[p], "sum") for p in PARTIES})
    v = e.groupby("ean").agg(**{k.replace(":", "_"): vv for k, vv in agg.items()})
    v.columns = [c.replace("p_", "p:", 1) if c.startswith("p_") else c.replace("mae_", "mae:", 1) if c.startswith("mae_") else c for c in v.columns]
    v["edad"] = pd.cut(last.age, [0, 11, 17, 23, 999], labels=AGES).astype(str)
    v["bandera"] = last.isf.map(FLAGS)
    inactive = int((~v.act).sum()); v = v[v.act].copy()
    P = v[["p:" + p for p in PARTIES]].values; MAE = v[["mae:" + p for p in PARTIES]].values
    top = P.max(1, keepdims=True); tied = P == top
    mae_t = np.where(tied, MAE, np.inf); bm = mae_t.min(1, keepdims=True)
    win2 = np.isclose(mae_t, bm) & tied
    v["voto"] = np.where(win2.sum(1) == 1, np.array(PARTIES, dtype=object)[mae_t.argmin(1)], "Empate")
    v["desempate"] = (tied.sum(1) > 1) & (v.voto != "Empate")
    v["fuerza"] = top[:, 0] / v.quarters    # % de sus quarters que ganó el partido elegido
    v.to_parquet(W / "parliament_ean.parquet")
    out = {"inactivos": inactive, "desempates": int(v.desempate.sum()), "total": tally(v), "por": {}, "por_q": {}, "w90": [], "partidos": {}}
    for col, name in [("cat", "Categoría"), ("house", "Casa"), ("size", "Tamaño"), ("edad", "Edad"), ("bandera", "Bandera")]:
        out["por"][name] = {str(k): tally(g) for k, g in v.dropna(subset=[col]).groupby(col)}
    for lab, g in ea.groupby("qlab"):
        t = tally(g.assign(voto=g.ganador_q)); tot = g.real.sum()
        t["wape"] = {p: float(abs(g[KEY[p]].sum() - tot) / tot) for p in PARTIES}
        out["por_q"][lab] = t
    for (h, lab), g in ea.groupby(["house", "qlab"]):
        tot = g.real.sum()
        out["w90"].append(dict(house=h, q=lab, real=float(tot), **{p: float(abs(g[KEY[p]].sum() - tot) / tot) for p in PARTIES}))
    w = pd.DataFrame(out["w90"])
    for p in PARTIES:
        out["partidos"][p] = dict(wape90=float((w[p] * w.real).sum() / w.real.sum()),
                                  ean_error=float((ea[KEY[p]] - ea.real).abs().sum() / ea.real.sum()),
                                  quarters=int((ea.ganador_q == p).sum()), bias=float(ea[KEY[p]].sum() / ea.real.sum() - 1))
    out["quarters_total"] = int(len(ea)); out["quarters_empate"] = int((ea.ganador_q == "Empate").sum())
    (W / "parliament.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    # salida en texto
    T = out["total"]
    print(f"EANs que votan: {T['eans']} (sin actividad fuera: {inactive}; decididos por el detalle mensual: {out['desempates']})")
    print(f"{'Partido':<22}{'EANs':>6}{'%':>6}{'Vol':>7}{'Q ganados':>11}{'WAPE90':>9}{'Error EAN':>11}")
    for p in PARTIES + ["Empate"]:
        pp = out["partidos"].get(p, {})
        print(f"{p:<22}{T['seats'][p]:>6}{T['seats'][p] / T['eans']:>6.0%}{T['vol'][p]:>7.0%}{pp.get('quarters', 0):>11}"
              f"{pp.get('wape90', float('nan')):>9.1%}{pp.get('ean_error', float('nan')):>11.1%}")
    for name, dd in [("Por quarter", out["por_q"])] + list(out["por"].items()):
        print(f"\n— {name}")
        for k, t in dd.items():
            s = " ".join(f"{p.split()[0][:4]}{('×l' if 'línea' in p else '') + ('E' if 'estac' in p else '') + ('F' if 'fragancias' in p else '') + ('M' if 'makeup' in p else '')}:{t['seats'][p]}" for p in PARTIES)
            print(f"{k:<22} n={t['eans']:>4} | {s} Emp:{t['seats']['Empate']} | + EANs: {t['win_eans']} | + vol: {t['win_vol']} ({t['vol'][t['win_vol']]:.0%})")


if __name__ == "__main__":
    main()
