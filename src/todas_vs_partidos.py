"""¿Elegir entre todas las estrategias del banco o entre 6 partidos? Prueba honesta en la foto sep-25.
Validación cruzada con los 3 quarters de la foto: cada EAN elige con 2 quarters y se mide en el tercero, rotando
(Q2+Q3 -> Q4, Q2+Q4 -> Q3, Q3+Q4 -> Q2). Solo Q2+Q3 -> Q4 respeta el orden del tiempo; las otras dos miden si lo elegido se repite. Banco sin bases ni trends de 3 meses y con los DAs
futuros según la bandera de cada EAN (100% / 50% / 0%). Opciones:
  - la mejor estrategia del banco para ese EAN (~44.000 opciones)
  - la media de sus K mejores estrategias del banco (K = 3, 10, 100, 1.000)
  - los 6 partidos: el mejor para él, y la coalición de sus 2 mejores
  - la regla de su categoría (referencia)
Salida: work/todas_vs_partidos.json"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_brujulas6 as b6  # noqa
import ideo_parties as ipp  # noqa

W = ipp.W


def main():
    st, FQ, Aq, a = ipp.load()
    idx = b6.index(st); flag = a.isf.values.astype(int).clip(0, 2)
    base = np.where((st.daf.values == 1.0) & ~st.base.isin(["M3", "M3e"]).values & (st.tventana.values != 3))[0]
    # forecast por EAN con los DAs futuros de su bandera
    F = np.empty((len(base),) + FQ.shape[1:], np.float32)
    for f in (0, 1, 2):
        m = flag == f
        rows = base if f == 0 else np.array([b6.twin(st, idx, i, daf=b6.FLAG_DAF[f]) for i in base])
        F[:, m] = FQ[rows][:, m]
    ids = json.loads((W / "ideo_brujulas6.json").read_text())["ids"]
    pos = {i: k for k, i in enumerate(base)}
    p6 = np.array([pos[b6.twin(st, idx, i, daf="1.0")] for i in ids])
    QN = ["oct–dic", "ene–mar", "abr–jun"]
    res = {}
    for test in (2, 1, 0):
        tr = [q for q in (0, 1, 2) if q != test]
        rtr = Aq[:, tr].sum(1); rte = Aq[:, test]
        ok = (rtr > 0) & (rte > 0)
        Fo = F[:, ok]; A = Aq[ok]; cat = a.cat.values[ok]; n = np.arange(ok.sum())
        etr = np.abs(Fo[:, :, tr] - A[None, :, tr]).sum(2) / A[:, tr].sum(1)[None]
        fte = Fo[:, :, test]; R = A[:, test].sum()
        ev = lambda x: float(np.abs(x - A[:, test]).sum() / R)
        order = np.argsort(etr, 0)
        e6 = etr[p6]; o6 = np.argsort(e6, 0)
        r = {"La mejor de todas": ev(fte[order[0], n]),
             "Media de sus 10 mejores de todas": ev(fte[order[:10], n].mean(0)),
             "La mejor de los 6 partidos": ev(fte[p6[o6[0]], n]),
             "Coalición de sus 2 mejores partidos": ev(fte[p6[o6[:2]], n].mean(0)),
             "Regla de su categoría": ev(np.where(cat == "Fragancias", fte[p6[0]], fte[p6[1]])),
             "_dentro_todas": float((etr[order[0], n] * A[:, tr].sum(1)).sum() / A[:, tr].sum()),
             "_dentro_6": float((e6[o6[0], n] * A[:, tr].sum(1)).sum() / A[:, tr].sum()),
             "_eans": int(ok.sum())}
        res[f"elige {' + '.join(QN[q] for q in tr)} -> prueba {QN[test]}"] = r
    keys = [k for k in next(iter(res.values())) if not k.startswith("_eans")]
    res["media de las 3 pruebas"] = {k: float(np.mean([v[k] for v in res.values()])) for k in keys}
    res["_n_estrategias"] = int(len(base))
    for k, v in res.items():
        print(k, v if not isinstance(v, dict) else {kk: round(x, 3) for kk, x in v.items()})
    (W / "todas_vs_partidos.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
