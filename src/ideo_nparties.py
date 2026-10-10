"""¿Cuántos partidos? Prueba limpia en el tiempo para parlamentos de 2 a 10 partidos (2 reglas fijas + k nuevos, uno por forma de base).

Para cada k: los partidos se eligen SOLO con oct–mar (Q2+Q3), cada EAN vota con el formato fijo usando Q2+Q3, y se mide abr–jun (Q4),
que nadie vio. Métricas en Q4: error EAN a EAN, WAPE90 por casa (ponderado) y % de EANs que eligieron el partido que de verdad fue
el mejor en Q4; con el partido tal cual y con + 100% DAs de la foto. Referencias: reglas y consenso.
También con trampa (partidos y voto con Q2–Q4, medido en Q2–Q4) para ver la diferencia entre lo que se ve dentro y fuera.
Salida: work/ideo_nparties.json"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_parties as ipp  # noqa
import ideo_vs_cons as ivc  # noqa

W = ipp.W
HOUSES = ivc.HOUSES


def metrics(a, F, Aq, cons, q):
    R = Aq[:, q]
    ean = float(np.abs(F[:, q] - R).sum() / R.sum())
    rows = []
    for h in HOUSES:
        s = (a.casa == h).values
        rows.append((R[s].sum(), abs(F[s, q].sum() - R[s].sum()) / R[s].sum(), abs(cons[s, q].sum() - R[s].sum()) / R[s].sum()))
    rr = np.array(rows)
    return ean, float((rr[:, 0] * rr[:, 1]).sum() / rr[:, 0].sum()), int((rr[:, 1] < rr[:, 2]).sum())


def main():
    st, FQ, Aq, a = ipp.load()
    cons = np.stack(a.cons_q.values)
    cat = a.cat.values
    rf, rm = ipp.fixed_ids(st)
    cand = ((st.fuente != "ninguna") | (st.base == "CV")).values
    cache = pd.read_pickle(W / "ideo_stage1.pkl"); dfix = cache[4]
    n = np.arange(len(a))
    out = {"limpia": [], "trampa": []}
    rule = np.where((cat == "Fragancias")[:, None], FQ[rf], FQ[rm])
    out["ref"] = dict(reglas_DAs=metrics(a, rule, Aq, cons, 2), consenso=metrics(a, cons, Aq, cons, 2))
    for tag, qs_sel, qs_eval in [("limpia", [0, 1], [2]), ("trampa", [0, 1, 2], [0, 1, 2])]:
        r = Aq[:, qs_sel].sum(1); c = np.where(r > 0)[0]
        Sc = np.empty((len(st), len(c)), np.float32)
        for i in range(0, len(st), 20000):
            Sc[i:i + 20000] = np.minimum(np.abs(FQ[i:i + 20000][:, c][:, :, qs_sel] - Aq[None, c][:, :, qs_sel]).sum(2) / r[c][None], ipp.CAPSCORE)
        w = 0.5 / len(c) + 0.5 * r[c] / r[c].sum()
        for k in range(0, 9):
            ids, _ = ipp.select_forms(Sc, w, st, [rf, rm], cand, dfix, n_new=k, verbose=False) if k > 0 else ([rf, rm], [])
            P = FQ[ids]; Pd = FQ[ivc.with_da(st, ids)]
            v = ivc.vote(P, Aq, qs_sel)
            v = np.where(v < 0, np.where(cat == "Fragancias", 0, 1), v)
            Fp = P[v, n]; Fd = Pd[v, n]
            res = dict(k=k + 2, partidos=[ipp.describe(st.loc[i]) for i in ids[2:]], obj=ipp.objective(Sc, w, ids))
            for q in qs_eval:
                best = np.abs(P[:, :, q] - Aq[None, :, q]).argmin(0)
                e1 = metrics(a, Fp, Aq, cons, q); e2 = metrics(a, Fd, Aq, cons, q)
                res[str(q)] = dict(ean=e1[0], w90=e1[1], gana=e1[2], ean_da=e2[0], w90_da=e2[1], gana_da=e2[2], acierto=float((v == best).mean()))
            out[tag].append(res)
            q = qs_eval[-1]
            print(f"{tag} {k + 2:>2} partidos · Q{q + 2}: error EAN {res[str(q)]['ean']:.1%} / +DAs {res[str(q)]['ean_da']:.1%} · "
                  f"WAPE90 {res[str(q)]['w90']:.1%} / +DAs {res[str(q)]['w90_da']:.1%} · acierta su mejor {res[str(q)]['acierto']:.0%}")
        del Sc
    print("ref Q4 (error EAN, WAPE90, casas):", out["ref"])
    (W / "ideo_nparties.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=float))


if __name__ == "__main__":
    main()
