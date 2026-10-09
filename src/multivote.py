"""Votación con varios partidos: cada EAN elige el método que mejor le funcionó en el pasado y se mide en el futuro.

Partidos (todos llevan los DAs de la foto en los meses del horizonte, como el consenso):
  Consenso            consenso de la foto tal cual
  Regla + DAs         la regla de su categoría (fragancias o makeup)
  Año pasado + DAs    mismo mes del año anterior
  Trend 6M + DAs      método actual del equipo: año pasado x (1 + trend 6M del propio EAN)
  Media 6M + DAs      media de los últimos 6 meses, plana

Sin mirar el futuro:
  1. Elección (foto sep-25): cada EAN elige el partido con menor error en Q2 FY26 (oct-dic 25) y Q3 FY26 (ene-mar 26),
     los dos quarters de la foto sep-25 que ya estaban cerrados al hacer la foto de mar-26.
     Error = suma de |forecast del quarter - real del quarter|. Empate -> Consenso. EAN sin historia -> Consenso.
  2. Prueba (foto mar-26): cada EAN usa los números de mar-26 de su partido en Q4 FY26 (abr-jun 26) y Q1 FY27 (jul-ago 26*).
  Se compara contra todos en consenso y todos en regla + DAs. Real = foto sep-26. Universo: EANs Central.
Variantes: 5 partidos y 2 partidos (consenso / regla + DAs).
Salida: work/multivote.json, work/multivote_ean_<n>.parquet"""
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

warnings.filterwarnings("ignore")
W = hc.W; M = hc.M; LAST = hc.LAST
PARTIES = ["Consenso", "Regla + DAs", "Año pasado + DAs", "Trend 6M + DAs", "Media 6M + DAs"]
TRAIN = ("2025-09", ["FY26.Q2", "FY26.Q3"])
TEST = ("2026-03", ["FY26.Q4", "FY27.Q1"])
FRAG = {"BURBERRY": "Burberry", "Gucci": "Gucci", "CP-Marc Jacobs": "Marc Jacobs"}
MU = {"GUMU": "Gucci Make up", "KYMU": "Kylie Makeup"}


def simple_methods(H, m):
    """Año pasado, trend 6M del EAN (método actual del equipo) y media 6M, con la historia hasta la foto. n x 9."""
    Hm = np.nan_to_num(H.copy()); Hm[:, m:] = 0
    ly = np.stack([Hm[:, j - 12] for j in range(m + 1, m + 10)], 1)
    num, den = Hm[:, m - 6:m].sum(1), Hm[:, m - 18:m - 12].sum(1)
    g6 = np.where(den > 0, num / np.where(den > 0, den, 1) - 1, 0)
    m6 = np.repeat(Hm[:, m - 6:m].mean(1)[:, None], 9, 1)
    return ly, np.clip(ly * (1 + g6)[:, None], 0, None), m6


def records(cat, lab_of, house_of, eans, s, F, Cn, Da, A, H, m, sel, isf, months):
    """EAN x quarter con el real y el forecast de cada partido."""
    ly, t6, m6 = simple_methods(H, m)
    P = {"Consenso": Cn, "Regla + DAs": F + Da, "Año pasado + DAs": ly + Da, "Trend 6M + DAs": t6 + Da, "Media 6M + DAs": m6 + Da}
    P = {k: np.clip(v, 0, None) for k, v in P.items()}
    age = ages(H, m); out = []
    qs = [fq(t) for t in months]
    for q in dict.fromkeys(qs):
        idx = [i for i, (x, t) in enumerate(zip(qs, months)) if x == q and t <= LAST]
        if not idx:
            continue
        df = pd.DataFrame(dict(ean=eans[sel], cat=cat, house=[lab_of[h] for h in house_of[sel]], snap=s, q=q,
                               age=age[sel], isf=isf[sel], real=A[sel][:, idx].sum(1)))
        for k, v in P.items():
            df[k] = v[sel][:, idx].sum(1)
        out.append(df)
    return out


def build():
    out = []
    d = pd.read_parquet(W / "data.parquet")
    Hd = pd.read_pickle(W / "hist.pkl").reindex(columns=M)
    C = pd.read_pickle(W / "cuts.pkl").reindex(index=Hd.index, columns=M).fillna(0).values
    a = add_types(pd.read_pickle(W / "attr.pkl")).reindex(Hd.index)
    Hv = Hd.values; A = np.nan_to_num(Hv)
    for s in hc.SNAPS:
        V = pd.Timestamp(s + "-01"); m = M.get_loc(V); months = list(M[m + 1:m + 10])
        DAp = np.clip(np.nan_to_num(dt.da_known(d, Hd.index, V)[0].values), 0, None)
        F, central, alive, g = hc.frag_rule(Hv, C, DAp, a.house_ptype.values, m)
        x = d[d.version == s]
        Cn, Da = cons_da(x, V, Hd.index, months)
        isf = x.groupby("ean").isf.max().reindex(Hd.index).fillna(0).values
        sel = a.house.isin(FRAG).values & Hd.index.isin(set(x.ean)) & central
        out += records("Fragancias", FRAG, a.house.values, Hd.index.values, s, F, Cn, Da, A[:, m + 1:m + 10], Hv, m, sel, isf, months)
    dm, Hdf, Edf, Cdf, attr, fac = mb.load()
    Hm_ = Hdf.values; eans = Hdf.index; Am_ = np.nan_to_num(Hm_)
    for s in hc.SNAPS:
        V = pd.Timestamp(s + "-01"); m = M.get_loc(V); months = list(M[m + 1:m + 10])
        DAp = np.clip(np.nan_to_num(mb.da_known(dm, eans, V).values), 0, None); DAp[:, m:] = 0
        F, central, alive, g = hc.mu_rule(Hm_, Cdf.values, DAp, attr.fam_brand.values, m)
        x = dm[dm.version == s]
        Cn, Da = cons_da(x, V, eans, months)
        isf = x.groupby("ean").isf.max().reindex(eans).fillna(0).values
        sel = attr.fam.isin(MU).values & eans.isin(set(x.ean)) & central
        out += records("Makeup", MU, attr.fam.values, eans.values, s, F, Cn, Da, Am_[:, m + 1:m + 10], Hm_, m, sel, isf, months)
    return pd.concat(out, ignore_index=True)


VARIANTS = {"5 partidos": PARTIES, "2 partidos": ["Consenso", "Regla + DAs"]}


def select(e, parties):
    """Elección con el pasado (sep-25 Q2+Q3) y prueba en mar-26 (Q4 FY26 + Q1 FY27)."""
    tr = e[(e.snap == TRAIN[0]) & e.q.isin(TRAIN[1])]
    te = e[(e.snap == TEST[0]) & e.q.isin(TEST[1])].copy()
    err = pd.DataFrame({p: (tr[p] - tr.real).abs() for p in parties}).groupby(tr.ean).sum()
    ok = (tr.real + tr[parties].sum(1)).groupby(tr.ean).sum() > 0
    choice = err.idxmin(axis=1).where(ok.reindex(err.index), "Consenso")   # empate -> el primero (Consenso)
    te["eleccion"] = te.ean.map(choice).fillna("Consenso")
    te["sin_historia"] = ~te.ean.isin(choice.index)
    te["Selección"] = [r[k] for (_, r), k in zip(te.iterrows(), te.eleccion)]
    errt = pd.DataFrame({p: (te[p] - te.real).abs() for p in parties}).groupby(te.ean).sum()
    best = errt.idxmin(axis=1)
    te["Óptimo a posteriori"] = [r[best[r.ean]] for _, r in te.iterrows()]
    both = choice[ok.reindex(choice.index)].index.intersection(best.index)
    return te, float((choice[both] == best[both]).mean()), int(len(both))


def summarize(te, parties, persist, npers):
    systems = list(dict.fromkeys(parties + ["Regla + DAs", "Selección", "Óptimo a posteriori"]))
    real_by = te.groupby("ean").real.sum()
    rows = []
    for (h, q), g in te.groupby(["house", "q"]):
        rows.append(dict(house=h, q=q, real=float(g.real.sum()),
                         **{f"w:{k}": float(abs(g[k].sum() - g.real.sum()) / g.real.sum()) for k in systems},
                         **{f"e:{k}": float((g[k] - g.real).abs().sum() / g.real.sum()) for k in systems}))
    W90 = pd.DataFrame(rows)
    ch = te.drop_duplicates("ean").set_index("ean")

    def duel(a, b):
        ea = (te[a] - te.real).abs(); eb = (te[b] - te.real).abs()
        pa = (ea < eb).groupby(te.ean).sum(); pb = (eb < ea).groupby(te.ean).sum()
        v = pd.Series(np.where(pa > pb, a, np.where(pb > pa, b, "Empate")), index=pa.index)
        return {"eans": v.value_counts().to_dict(), "vol": (real_by.groupby(v).sum() / real_by.sum()).to_dict()}
    seats = lambda g: g.eleccion.value_counts().reindex(parties, fill_value=0).to_dict()
    return dict(
        seats=seats(ch), seats_cat={c: seats(g) for c, g in ch.groupby("cat")}, seats_house={h: seats(g) for h, g in ch.groupby("house")},
        vol_seats=(real_by.groupby(ch.eleccion).sum() / real_by.sum()).reindex(parties, fill_value=0).to_dict(),
        wape90={k: float((W90[f"w:{k}"] * W90.real).sum() / W90.real.sum()) for k in systems},
        ean_error={k: float((te[k] - te.real).abs().sum() / te.real.sum()) for k in systems},
        w90_rows=rows, duel_cons=duel("Selección", "Consenso"), duel_regla=duel("Selección", "Regla + DAs"),
        persist=persist, n_persist=npers, eans_test=int(te.ean.nunique()), sin_historia=int(ch.sin_historia.sum()))


def main():
    e = build()
    out = {}
    pd.set_option("display.width", 250)
    for name, parties in VARIANTS.items():
        te, persist, npers = select(e, parties)
        te.to_parquet(W / f"multivote_ean_{len(parties)}.parquet")
        r = out[name] = summarize(te, parties, persist, npers)
        print(f"\n===== {name}: {', '.join(parties)} =====")
        print("Escaños (elección con sep-25 Q2+Q3):", r["seats"])
        print("  volumen de los EANs que eligen cada partido:", {k: round(v, 3) for k, v in r["vol_seats"].items()})
        print(f"EANs en la prueba: {r['eans_test']} (sin historia -> consenso: {r['sin_historia']})")
        print("Prueba mar-26 (Q4 FY26 + Q1 FY27):")
        for k in r["wape90"]:
            print(f"  {k:<22} WAPE90 {r['wape90'][k]:.1%}   error EAN {r['ean_error'][k]:.1%}")
        W90 = pd.DataFrame(r["w90_rows"])
        print(W90[["house", "q"] + [f"w:{k}" for k in ["Consenso", "Regla + DAs", "Selección"]]].round(3).to_string())
        print("Duelo EAN a EAN — Selección vs Consenso:", r["duel_cons"])
        print(f"Persistencia: el ganador de sep-25 repite en mar-26 en el {persist:.0%} de {npers} EANs (al azar: {1 / len(parties):.0%})")
    (W / "multivote.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
