"""Consenso vs Parlamento + DAs: ¿dejar que cada EAN elija su regla ayuda a ganarle al consenso?

Sin mirar el futuro:
  1. Elección: cada EAN vota (mismo sistema: más quarters ganados; empate -> error mes a mes) solo con los quarters
     de la foto sep-25 que ya estaban cerrados al hacer la foto de mar-26: Q2 FY26 (oct-dic) y Q3 FY26 (ene-mar).
     EAN sin historia en esos quarters -> la regla de su categoría (Regla fragancias / Regla makeup).
  2. Prueba: con la foto de mar-26, cada EAN usa su partido en Q4 FY26 (abr-jun) y Q1 FY27 (jul-ago*).
Referencias: consenso de la foto tal cual, cada partido para todos, y el "techo" (elección con los 5 quarters,
que incluye los de la prueba: no se puede saber de antemano).
Todos los partidos llevan los DAs de la foto. Real = foto sep-26. Solo resultados en texto (work/parliament_vs_cons.json).
Correr antes src/parliament.py (genera work/parliament_q.parquet)."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from parliament import PARTIES, KEY, W  # noqa

TRAIN = [("2025-09", "FY26.Q2"), ("2025-09", "FY26.Q3")]
TEST = [("2026-03", "FY26.Q4"), ("2026-03", "FY27.Q1")]
DEFAULT = {"Fragancias": "Regla fragancias", "Makeup": "Regla makeup"}


def vote(g):
    """Partido elegido por cada EAN con sus quarters (más quarters ganados; empate -> menor error mes a mes)."""
    ks = [KEY[p] for p in PARTIES]
    err = np.stack([(g[k] - g.real).abs().values for k in ks], 1)
    win = np.isclose(err, err.min(1, keepdims=True)); uniq = win.sum(1) == 1
    P = pd.DataFrame(np.where(uniq[:, None], win, False).astype(int), columns=PARTIES, index=g.index).groupby(g.ean).sum()
    MAE = g[["mae_" + k for k in ks]].groupby(g.ean).sum().values
    top = P.values.max(1, keepdims=True); tied = P.values == top
    mae_t = np.where(tied, MAE, np.inf)
    return pd.Series(np.array(PARTIES, dtype=object)[mae_t.argmin(1)], index=P.index)


def evaluate(te, col):
    tot = te.real.sum()
    w = [(abs(g[col].sum() - g.real.sum()), g.real.sum()) for _, g in te.groupby(["house", "q"])]
    return dict(wape90=sum(a for a, _ in w) / sum(b for _, b in w), ean=float((te[col] - te.real).abs().sum() / tot),
                bias=float(te[col].sum() / tot - 1))


def main():
    e = pd.read_parquet(W / "parliament_q.parquet")
    key = list(zip(e.snap, e.q))
    tr = e[[k in TRAIN for k in key]]; te = e[[k in TEST for k in key]].copy()
    te = te[(te.real + te.cons + te[[KEY[p] for p in PARTIES]].sum(1)) > 0]
    choice = vote(tr)
    ceiling = vote(e)                              # con los 5 quarters (incluye la prueba)
    te["eleccion"] = te.ean.map(choice)
    te["sin_hist"] = te.eleccion.isna()
    te.loc[te.sin_hist, "eleccion"] = te.loc[te.sin_hist, "cat"].map(DEFAULT)
    te["parlamento"] = [r[KEY[p]] for (_, r), p in zip(te.iterrows(), te.eleccion)]
    te["techo"] = [r[KEY[ceiling.get(r.ean, DEFAULT[r["cat"]])]] for _, r in te.iterrows()]
    systems = {"Consenso": "cons", "Parlamento + DAs": "parlamento", **{p: KEY[p] for p in PARTIES}, "Techo (elección a posteriori)": "techo"}
    res = {k: evaluate(te, c) for k, c in systems.items()}
    # por casa y quarter
    rows = []
    for (h, q), g in te.groupby(["house", "q"]):
        t = g.real.sum()
        rows.append(dict(casa=h, q=q, consenso=abs(g.cons.sum() - t) / t, parlamento=abs(g.parlamento.sum() - t) / t,
                         regla=abs(g[KEY["Regla fragancias" if g.cat.iloc[0] == "Fragancias" else "Regla makeup"]].sum() - t) / t,
                         spp3_cons=(t - g.cons.sum()) / t, spp3_parl=(t - g.parlamento.sum()) / t,
                         ean_cons=(g.cons - g.real).abs().sum() / t, ean_parl=(g.parlamento - g.real).abs().sum() / t))
    R = pd.DataFrame(rows)
    # duelo EAN a EAN (los 2 quarters de prueba)
    ec = (te.cons - te.real).abs(); ep = (te.parlamento - te.real).abs()
    pc_ = (ep < ec).groupby(te.ean).sum(); cc_ = (ec < ep).groupby(te.ean).sum()
    mc = ec.groupby(te.ean).sum(); mp = ep.groupby(te.ean).sum()
    duel = pd.Series(np.where(pc_ > cc_, "Parlamento", np.where(cc_ > pc_, "Consenso",
                     np.where(mp < mc, "Parlamento", np.where(mc < mp, "Consenso", "Empate")))), index=pc_.index)
    vol = te.groupby("ean").real.sum()
    dvol = (vol.groupby(duel).sum() / vol.sum()).to_dict()
    seats = te.drop_duplicates("ean").eleccion.value_counts().to_dict()
    # persistencia: ¿el partido elegido con el pasado es el que mejor le va en la prueba?
    best_test = vote(te)
    both = choice.index.intersection(best_test.index)
    persist = float((choice[both] == best_test[both]).mean())
    out = dict(res=res, casa_q=rows, duelo={k: int(v) for k, v in duel.value_counts().items()}, duelo_vol=dvol, escanos=seats,
               persistencia=persist, n_persist=int(len(both)), eans=int(te.ean.nunique()), sin_historia=int(te.drop_duplicates("ean").sin_hist.sum()))
    (W / "parliament_vs_cons.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=float))
    print(f"EANs en la prueba: {out['eans']} (sin historia en la elección -> regla de su categoría: {out['sin_historia']})")
    print("Escaños con los que llega cada EAN a la prueba:", seats)
    print(f"\n{'Sistema':<32}{'WAPE90':>8}{'Error EAN':>11}{'Desvío':>9}")
    for k, r in res.items():
        print(f"{k:<32}{r['wape90']:>8.1%}{r['ean']:>11.1%}{r['bias']:>+9.0%}")
    print("\nPor casa y quarter (WAPE90 consenso / parlamento / regla de la categoría; SPP3; error EAN):")
    print(R.round(3).to_string())
    print(f"\nDuelo EAN a EAN (abr-jun + jul-ago): {out['duelo']}  volumen: { {k: round(v, 3) for k, v in dvol.items()} }")
    print(f"Persistencia: el partido elegido con el pasado es el mejor en la prueba en el {persist:.0%} de {len(both)} EANs (al azar: {1 / len(PARTIES):.0%})")


if __name__ == "__main__":
    main()
