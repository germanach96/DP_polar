"""Comparación estándar: consenso de la foto sep-25 tal cual vs parlamento de 10 partidos + todos los DAs de la foto.

Cada EAN usa el partido al que vota; a ese partido se le ponen el 100% de los DAs de la foto (positivos y negativos, suelo 0
por EAN-mes), sin contarlos dos veces: se toma la misma estrategia con 'DAs de la foto = 100%'. EANs en empate -> regla de su categoría.
Dos versiones:
  A) Con trampa: partidos y voto con oct–jun (los del reporte de ideologías); se mide en Q2, Q3 y Q4 FY26.
  B) Limpia: partidos y voto solo con oct–mar (Q2+Q3); se mide en Q4 (abr–jun), que nadie vio al elegir.
Métricas (src/wape90.py): WAPE90 = |Σ forecast − Σ real| / Σ real y SPP3 = (Σ real − Σ forecast) / Σ real por casa × quarter;
error EAN = Σ |forecast − real| por EAN y quarter / Σ real.
Salida: work/ideo_vs_cons.json"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_parties as ipp  # noqa
import ideo_panel as ip  # noqa

W = ipp.W
HOUSES = ["Burberry", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"]
KEY = ["base", "estac", "fuente", "tventana", "fuerza", "tope", "dap", "cortes", "daf", "pool"]


def with_da(st, ids):
    """Misma estrategia con el 100% de los DAs de la foto."""
    idx = {tuple(r): i for i, r in zip(st.id.values, st[KEY].astype(str).itertuples(index=False))}
    out = []
    for i in ids:
        r = st.loc[i, KEY].astype(str).to_dict(); r["daf"] = "1.0"
        out.append(idx[tuple(r[k] for k in KEY)])
    return out


def vote(FQp, Aq, qs):
    """Elección con el formato fijo usando solo los quarters qs. Devuelve el índice de partido por EAN (-1 = empate)."""
    el = ipp.election(FQp[:, :, qs], Aq[:, qs], [str(i) for i in range(len(FQp))])
    return np.array([int(x) if x != "Empate" else -1 for x in el["final"]])


def table(a, F, cons, Aq, qs):
    rows = []
    for h in HOUSES + ["Total fragancias", "Total makeup", "Total"]:
        s = (a.casa == h).values if h in HOUSES else ((a.cat == "Fragancias").values if h == "Total fragancias" else (a.cat == "Makeup").values if h == "Total makeup" else np.ones(len(a), bool))
        for q in qs:
            R = Aq[s, q].sum(); fp = F[s, q].sum(); fc = cons[s, q].sum()
            rows.append(dict(casa=h, q=ip.QLIST[q], real=float(R), wape_parl=abs(fp - R) / R, wape_cons=abs(fc - R) / R,
                             spp3_parl=(R - fp) / R, spp3_cons=(R - fc) / R,
                             ean_parl=float(np.abs(F[s, q] - Aq[s, q]).sum() / R), ean_cons=float(np.abs(cons[s, q] - Aq[s, q]).sum() / R)))
    return pd.DataFrame(rows)


def main():
    st, FQ, Aq, a = ipp.load()
    D = json.loads((W / "ideo.json").read_text())
    cons = np.stack(a.cons_q.values)
    cat = a.cat.values
    rf, rm = ipp.fixed_ids(st)
    out = {}
    # ---- A) con trampa: partidos del reporte, voto con oct–jun
    ids = [p["id"] for p in D["partidos"]]; names = [p["nombre"] for p in D["partidos"]]
    idsD = with_da(st, ids)
    FQp = FQ[ids]; FQd = FQ[idsD]
    v = np.array([names.index(x) if x in names else -1 for x in pd.read_parquet(W / "ideo_ean.parquet").loc[a.index, "voto"]])
    fallback = np.where(cat == "Fragancias", names.index("Regla fragancias"), names.index("Regla makeup"))
    v = np.where(v < 0, fallback, v)
    n = np.arange(len(a))
    for lab, M in [("A_parlamento_DAs", FQd), ("A_parlamento_tal_cual", FQp)]:
        out[lab] = table(a, M[v, n], cons, Aq, [0, 1, 2]).to_dict("records")
    rule = np.where((cat == "Fragancias")[:, None], FQ[rf], FQ[rm])
    out["A_reglas_DAs"] = table(a, rule, cons, Aq, [0, 1, 2]).to_dict("records")
    # ---- B) limpia: partidos y voto con Q2+Q3, medida en Q4
    descs = D["temporal_limpio"]["partidos"]
    want = set(descs)
    ids23 = {}
    for i in np.where(((st.fuente != "ninguna") | (st.base == "CV")).values)[0]:
        dsc = ipp.describe(st.loc[i])
        if dsc in want and dsc not in ids23:
            ids23[dsc] = int(i)
    ids23 = [ids23[d] for d in descs]
    FQ23 = FQ[ids23]; FQ23d = FQ[with_da(st, ids23)]
    v23 = vote(FQ23, Aq, [0, 1])
    fb = np.where(cat == "Fragancias", 0, 1)            # las dos primeras son las reglas
    v23 = np.where(v23 < 0, fb, v23)
    out["B_parlamento_DAs"] = table(a, FQ23d[v23, n], cons, Aq, [2]).to_dict("records")
    out["B_parlamento_tal_cual"] = table(a, FQ23[v23, n], cons, Aq, [2]).to_dict("records")
    out["B_reglas_DAs"] = table(a, rule, cons, Aq, [2]).to_dict("records")
    (W / "ideo_vs_cons.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    pd.set_option("display.width", 220)
    for k, rows in out.items():
        d = pd.DataFrame(rows)
        hh = d[d.casa.isin(HOUSES)]
        wins = int((hh.wape_parl < hh.wape_cons).sum())
        w = lambda c: float((hh[c] * hh.real).sum() / hh.real.sum())
        print(f"\n== {k}: gana {wins}/{len(hh)} casa×quarter · WAPE90 pond. {w('wape_parl'):.1%} vs consenso {w('wape_cons'):.1%} · "
              f"error EAN {w('ean_parl'):.1%} vs {w('ean_cons'):.1%}")
        print(d[["casa", "q", "wape_parl", "wape_cons", "spp3_parl", "spp3_cons", "ean_parl", "ean_cons"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
