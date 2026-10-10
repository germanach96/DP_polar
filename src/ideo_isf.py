"""DAs futuros según la Ignore System Forecast Flag de la foto (sí/no), parlamento de 6 (src/ideo_brujulas6.py).

Con la flag prendida el consenso es casi todo DAs (flag 2: 100%; flag 1: 65%; sin flag: 11%), así que parlamento + DAs duplica.
Variantes para los DAs futuros de la foto:
  V0  todos: partido + 100% DAs                                  (lo de ahora)
  V1  flag 1 o 2: solo partido, sin DAs · sin flag: + DAs        (la flag dice "los DAs ya son el forecast")
  V2  flag 2: sin DAs · flag 1 y sin flag: + DAs
  V3  flag 1 o 2: el mayor entre partido y DAs (por quarter) · sin flag: + DAs
  V4  flag 1 o 2: solo los DAs (≈ consenso manual) · sin flag: partido + DAs
  V5  flag 2: sin DAs · flag 1: + 50% DAs · sin flag: + DAs
El voto (oct–mar) se hace con las mismas reglas de DAs que la variante; se mide abr–jun. Salida: work/ideo_isf.json"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_parties as ipp  # noqa
import ideo_panel as ip  # noqa
import ideo_six as s6  # noqa
import ideo_vs_cons as ivc  # noqa

W = ipp.W
KEY = ["base", "estac", "fuente", "tventana", "fuerza", "tope", "dap", "cortes", "daf", "pool"]


def twin(st, i, daf):
    idx = {tuple(r): k for k, r in zip(st.id.values, st[KEY].astype(str).itertuples(index=False))}
    r = st.loc[i, KEY].astype(str).to_dict(); r["daf"] = daf
    return idx[tuple(r[k] for k in KEY)]


def main():
    st, FQ, Aq, a = ipp.load()
    cons = np.stack(a.cons_q.values); cat = a.cat.values; n = np.arange(len(a))
    Pn = pd.read_pickle(W / "ideo_panel.pkl"); vi = Pn["attr"].index.get_indexer(a.index)
    DAq = np.stack([Pn["DAf"][vi][:, ix].clip(0).sum(1) for ix in ip.QIDX], 1)          # DAs+ futuros por quarter
    ids = json.loads((W / "ideo_brujulas6.json").read_text())["ids"]
    Pda = FQ[ids]                                                   # con 100% DAs
    P0 = FQ[[twin(st, i, "0.0") for i in ids]]                      # mismo partido sin DAs futuros
    flag = a.isf.values
    f12 = (flag >= 1)[None, :, None]; f2 = (flag == 2)[None, :, None]
    var = {"V0 todos + DAs": Pda,
           "V1 flag 1-2 sin DAs": np.where(f12, P0, Pda),
           "V2 solo flag 2 sin DAs": np.where(f2, P0, Pda),
           "V3 flag 1-2 máx(partido, DAs)": np.where(f12, np.maximum(P0, DAq[None]), Pda),
           "V4 flag 1-2 solo DAs": np.where(f12, np.broadcast_to(DAq[None], P0.shape), Pda),
           "V5 flag 2 sin DAs, flag 1 con 50%": np.where(f2, P0, np.where(f12, FQ[[twin(st, i, "0.5") for i in ids]], Pda))}
    rows = []
    for k, P in var.items():
        v = ivc.vote(P, Aq, [0, 1]); v = np.where(v < 0, np.where(cat == "Fragancias", 0, 1), v)
        F = P[v, n]
        r = dict(variante=k, **s6.evaluate(a, F, Aq, cons, 2))
        for t in s6.TRAMOS:
            r["ean_" + t] = s6.evaluate(a, F, Aq, cons, 2, a.tramo.values == t)["ean"]
        for f in [0, 1, 2]:
            m = flag == f
            r[f"ean_flag{f}"] = s6.evaluate(a, F, Aq, cons, 2, m)["ean"]
            r[f"sesgo_flag{f}"] = float(F[m, 2].sum() / Aq[m, 2].sum() - 1)
        rows.append(r)
    ref = dict(variante="Consenso", **s6.evaluate(a, cons, Aq, cons, 2))
    for t in s6.TRAMOS:
        ref["ean_" + t] = s6.evaluate(a, cons, Aq, cons, 2, a.tramo.values == t)["ean"]
    for f in [0, 1, 2]:
        m = flag == f
        ref[f"ean_flag{f}"] = s6.evaluate(a, cons, Aq, cons, 2, m)["ean"]; ref[f"sesgo_flag{f}"] = float(cons[m, 2].sum() / Aq[m, 2].sum() - 1)
    rows.append(ref)
    df = pd.DataFrame(rows)
    pd.set_option("display.width", 250)
    print(df.round(3).to_string(index=False))
    (W / "ideo_isf.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False, default=float))


if __name__ == "__main__":
    main()
