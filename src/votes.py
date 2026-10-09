"""Votación por EAN: consenso vs regla + DAs (los mismos cálculos que src/wape90.py).
- Cada EAN tiene hasta 5 quarters: foto sep-25 (Q2, Q3, Q4 FY26) y foto mar-26 (Q4 FY26, Q1 FY27).
- En cada quarter gana el sistema con menor |forecast del quarter - real del quarter|. Si empatan, nadie suma.
- El EAN vota por el sistema que gana más quarters; si ganan los mismos, el EAN es empate.
- Fuera: EANs sin actividad (real, consenso y regla + DAs = 0 en todos sus quarters).
- Se reporta también el voto ponderado por volumen (real de los 5 quarters).
Lee work/wape90_ean.parquet (correr antes src/wape90.py). Salida: work/votes.json"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from ptype import add_types  # noqa

W = Path(__file__).resolve().parents[1] / "work"
FRAG = ("Burberry", "Gucci", "Marc Jacobs")
SEG = {"Maduros (18+ meses)": "Maduros (18+ meses)", "Jóvenes (6-17 meses)": "Jóvenes (6–17 meses)", "Forecast manual": "Forecast manual"}


def ean_votes():
    e = pd.read_parquet(W / "wape90_ean.parquet")
    ec, er = (e.consenso - e.real).abs(), (e.regla_da - e.real).abs()
    e["p_cons"] = (ec < er).astype(int); e["p_regla"] = (er < ec).astype(int)
    e["act"] = (e.real + e.consenso + e.regla_da) > 0
    last = e.sort_values("snap").groupby("ean").last()
    v = e.groupby("ean").agg(house=("house", "first"), quarters=("q", "size"), real=("real", "sum"), consenso=("consenso", "sum"),
                             regla_da=("regla_da", "sum"), p_cons=("p_cons", "sum"), p_regla=("p_regla", "sum"), act=("act", "any"))
    v["seg"] = last.seg.map(SEG)
    v = v[v.act].copy()
    v["voto"] = np.where(v.p_regla > v.p_cons, "Regla + DAs", np.where(v.p_cons > v.p_regla, "Consenso", "Empate"))
    v["cat"] = np.where(v.house.isin(FRAG), "Fragancias", "Makeup")
    # ABC por volumen real dentro de cada categoría (A = 80% del volumen, B = siguiente 15%, C = resto)
    v["abc"] = ""
    for c, g in v.groupby("cat"):
        s = g.real.sort_values(ascending=False); cum = s.cumsum() / s.sum()
        v.loc[s.index, "abc"] = np.where(cum.shift(fill_value=0) < .80, "A", np.where(cum.shift(fill_value=0) < .95, "B", "C"))
    a = add_types(pd.read_pickle(W / "attr.pkl"))
    v["size"] = a.ptype.reindex(v.index.astype(a.index.dtype)).values
    v.loc[v.cat == "Makeup", "size"] = None
    return v, int((~e.groupby("ean").act.any()).sum())


def tally(g):
    n = len(g); r = (g.voto == "Regla + DAs").sum(); c = (g.voto == "Consenso").sum(); t = n - r - c
    vol = g.real.sum() or 1
    return dict(eans=int(n), regla=int(r), consenso=int(c), empate=int(t),
                vol_regla=float(g.real[g.voto == "Regla + DAs"].sum() / vol), vol_cons=float(g.real[g.voto == "Consenso"].sum() / vol),
                vol_emp=float(g.real[g.voto == "Empate"].sum() / vol),
                q_regla=int(g.p_regla.sum()), q_cons=int(g.p_cons.sum()), q_total=int(g.quarters.sum()), real=float(g.real.sum()))


def main():
    v, inactive = ean_votes()
    out = {"inactivos": inactive, "total": tally(v), "por": {}}
    for col, name in [("cat", "Categoría"), ("house", "Casa"), ("seg", "Tipo de EAN"), ("abc", "ABC por volumen"), ("size", "Tamaño (fragancias)")]:
        out["por"][name] = {str(k): tally(g) for k, g in v.dropna(subset=[col]).groupby(col)}
    out["casa_seg"] = {f"{h}|{s}": tally(g) for (h, s), g in v.groupby(["house", "seg"])}
    out["casa_abc"] = {f"{h}|{s}": tally(g) for (h, s), g in v.groupby(["house", "abc"])}
    out["dist"] = {f"{int(r)}-{int(c)}": int(n) for (r, c), n in v.groupby(["p_regla", "p_cons"]).size().items()}
    (W / "votes.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    v.to_parquet(W / "votes_ean.parquet")
    fmt = lambda k, t: (f"{k:<28} EANs {t['eans']:>4} | Regla+DAs {t['regla']:>4} ({t['regla'] / t['eans']:.0%}) Consenso {t['consenso']:>4} "
                        f"({t['consenso'] / t['eans']:.0%}) Empate {t['empate']:>3} | vol regla {t['vol_regla']:.0%} cons {t['vol_cons']:.0%} | "
                        f"quarters regla {t['q_regla']} cons {t['q_cons']} de {t['q_total']}")
    print(f"EANs sin actividad (fuera): {inactive}")
    print(fmt("TOTAL", out["total"]))
    for name, d in out["por"].items():
        print(f"\n— {name}")
        for k, t in d.items():
            print(fmt(k, t))
    print("\n— Casa × tipo"); [print(fmt(k, t)) for k, t in out["casa_seg"].items()]
    print("\n— Casa × ABC"); [print(fmt(k, t)) for k, t in out["casa_abc"].items()]


if __name__ == "__main__":
    main()
