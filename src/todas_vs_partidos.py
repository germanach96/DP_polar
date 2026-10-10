"""¿Elegir entre todas las estrategias del banco o entre 6 partidos? Prueba honesta en la foto sep-25.
Cada EAN elige con su error de oct–mar (Q2+Q3) y se mide en abr–jun (Q4). Banco sin bases ni trends de 3 meses y con los DAs
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
    r23 = Aq[:, :2].sum(1); r4 = Aq[:, 2]
    ok = (r23 > 0) & (r4 > 0)
    F = F[:, ok]; A = Aq[ok]; cat = a.cat.values[ok]; n = np.arange(ok.sum())
    e23 = np.abs(F[:, :, :2] - A[None, :, :2]).sum(2) / A[:, :2].sum(1)[None]      # estrategias x EAN
    f4 = F[:, :, 2]
    R4 = A[:, 2].sum()
    ev = lambda x: float(np.abs(x - A[:, 2]).sum() / R4)
    order = np.argsort(e23, 0)
    res = {}
    best = order[0]
    res["La mejor de todas (en oct–mar)"] = dict(abr_jun=ev(f4[best, n]), oct_mar=float((e23[best, n] * A[:, :2].sum(1)).sum() / A[:, :2].sum()))
    for K in [3, 10, 100, 1000]:
        res[f"Media de sus {K} mejores"] = dict(abr_jun=ev(f4[order[:K], n].mean(0)))
    # 6 partidos
    ids = json.loads((W / "ideo_brujulas6.json").read_text())["ids"]
    pos = {i: k for k, i in enumerate(base)}
    p6 = [pos[b6.twin(st, idx, i, daf="1.0")] for i in ids]
    e6 = e23[p6]; o6 = np.argsort(e6, 0)
    res["6 partidos: el mejor para él"] = dict(abr_jun=ev(f4[np.array(p6)[o6[0]], n]), oct_mar=float((e6[o6[0], n] * A[:, :2].sum(1)).sum() / A[:, :2].sum()))
    res["6 partidos: coalición de sus 2 mejores"] = dict(abr_jun=ev(f4[np.array(p6)[o6[:2]], n].mean(0)))
    res["Regla de su categoría"] = dict(abr_jun=ev(np.where(cat == "Fragancias", f4[p6[0]], f4[p6[1]])))
    # ¿acierta? la estrategia elegida, ¿qué puesto ocupa en abr–jun entre todas?
    e4 = np.abs(f4 - A[None, :, 2]) / A[None, :, 2]
    rank = (e4 < e4[best, n][None]).sum(0) / len(base)
    res["_percentil_mediano_en_abr_jun_de_la_mejor_de_oct_mar"] = float(np.median(rank))
    res["_n_estrategias"] = int(len(base)); res["_n_eans"] = int(ok.sum())
    for k, v in res.items():
        print(k, v if not isinstance(v, dict) else {kk: round(x, 3) for kk, x in v.items()})
    (W / "todas_vs_partidos.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
