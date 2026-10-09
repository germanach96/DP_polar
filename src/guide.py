"""Aplica la GUÍA a la última foto (2026-09): por house x tipo de producto
   techo = LY ; suelo = LY x (1 + trend12M tipo, tope ±30%) ; número = punto medio (LY x (1 + 0.5 x trend))
y lo compara con el consenso actual. -> work/results/guia_actual.md"""
import sys
import warnings
import numpy as np
import pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import methods as mt  # noqa
from ptype import add_types  # noqa
from evaluate import fq  # noqa
warnings.filterwarnings("ignore")
W = Path(__file__).resolve().parents[1] / "work"
DAMP = 0.5


def main():
    H = pd.read_pickle(W / "hist.pkl"); a = add_types(pd.read_pickle(W / "attr.pkl"))
    keep = (a.resp != "Local") & (a.isf.fillna(0) == 0)
    H = H[keep.reindex(H.index).values]; a = a.reindex(H.index)
    months = pd.date_range("2023-07-01", "2027-06-01", freq="MS")
    Hm = H.reindex(columns=months).values
    m = months.get_loc(pd.Timestamp("2026-09-01"))
    base = np.clip(mt._ly(Hm, m), 0, None)
    g = mt._group_g(Hm, m, 12, a.house_ptype.values); g = np.clip(np.nan_to_num(g), -0.3, 0.3)
    gh = mt._group_g(Hm, m, 12, a.house.values)
    full = base * (1 + g)[:, None]; mid = base * (1 + DAMP * g)[:, None]
    fut = pd.read_pickle(W / "fut_latest.pkl").reindex(index=H.index, columns=months[m + 1:m + 9]).fillna(0).values
    tg = months[m + 1:m + 9]
    rows = []
    for i, e in enumerate(H.index):
        for k in range(8):
            rows.append((e, a.house[e], a.ptype[e], a.brand[e], tg[k], base[i, k], full[i, k], mid[i, k], fut[i, k], g[i]))
    D = pd.DataFrame(rows, columns=["ean", "house", "ptype", "brand", "target", "LY", "suelo", "numero", "consenso", "g12_tipo"])
    D["fq"] = fq(D.target).values
    L = ["# Guía aplicada a la foto 2026-09 (oct-26 .. may-27), universo sin Local ni manuales\n",
         "techo = LY; suelo = LY x (1 + trend 12M house x tipo, tope ±30%); número = LY x (1 + 50% del trend). Banda histórica del número: house-8m P10 -13% / P90 +9%; house-quarter P10 -15% / P90 +16%.\n"]
    gt = D.groupby(["house", "ptype"]).agg(g12_tipo=("g12_tipo", "first"), LY=("LY", "sum"), numero=("numero", "sum"), consenso=("consenso", "sum"))
    gt["cons_vs_numero"] = gt.consenso / gt.numero - 1
    L += ["## Trend 12M por house x tipo (a ago-26) y totales 8 meses\n", gt.round(3).to_markdown()]
    for keys in [["house"], ["house", "fq"]]:
        t = D.groupby(keys)[["LY", "suelo", "numero", "consenso"]].sum()
        t["P10"] = t.numero * 0.87 if keys == ["house"] else t.numero * 0.85
        t["P90"] = t.numero * 1.09 if keys == ["house"] else t.numero * 1.16
        t["cons_vs_numero"] = t.consenso / t.numero - 1
        t["cons_vs_LY"] = t.consenso / t.LY - 1
        L += [f"\n## Por {' x '.join(keys)}\n", t.round(3).to_markdown()]
    gh_s = pd.Series(gh, index=H.index).groupby(a.house).first().round(3).to_dict()
    L += [f"Trend 12M house: {gh_s}"]
    (W / "results" / "guia_actual.md").write_text("\n".join(L))
    print("\n".join(L[2:]))


if __name__ == "__main__":
    main()
