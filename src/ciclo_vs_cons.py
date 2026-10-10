"""Comparación histórica (pedida por el usuario 2026-10-10): Ciclo de vida contra el consenso de o9 en la foto sep-25 → real sep-26.
El consenso NO se usa para decidir; esto es solo para saber dónde queda la propuesta frente a lo que hoy calcula o9.
Opciones: consenso tal cual · Ciclo de vida con DAs futuros según la bandera · Ciclo de vida + 100% DAs · regla + 100% DAs.
Métricas por quarter (Q2 = 1–3 meses, Q3 = 4–6, Q4 = 7–9): error EAN a EAN (Σ|f−r| / Σr) y WAPE90 de la casa (Σ_casa |Σf − Σr| / Σr), sesgo,
casas en las que el Ciclo de vida gana al consenso, y error EAN a EAN por tramo de edad y por bandera (9 meses juntos).
Salida: work/ciclo_vs_cons.json"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_panel as ip  # noqa
import six_multi as sm  # noqa

W = ip.W
N = sm.NAMES_UNO


def main():
    P = ip.build(ip.SNAP, save=False); a = P["attr"]; v = a.votante.values; av = a[v]
    F0 = sm.forecasts(P, sm.specs())[:, v]
    flag = av.isf.values.astype(int).clip(0, 2)
    wf = np.array([sm.FLAGW[f] for f in flag])[:, None]; DA = P["DAf"][v]
    fr = (av.cat.values == "Fragancias")[:, None]
    ciclo = F0[N.index("Ciclo de vida")]
    opts = {"Consenso o9": P["cons"][v],
            "Ciclo de vida (DAs según bandera)": np.clip(ciclo + wf * DA, 0, None),
            "Ciclo de vida + 100% DAs": np.clip(ciclo + DA, 0, None),
            "Regla + 100% DAs": np.clip(np.where(fr, F0[N.index("Regla fragancias")], F0[N.index("Regla makeup")]) + DA, 0, None)}
    A = P["A"][v]
    out = dict(horizonte={}, tramo={}, bandera={})
    for q, ix, lg in zip(P["qlist"], P["qidx"], ["1–3", "4–6", "7–9"]):
        r = A[:, ix].sum(1); gc = None; res = {}
        for nm, F in opts.items():
            f = F[:, ix].sum(1)
            g = pd.DataFrame(dict(c=av.casa.values, f=f, r=r)).groupby("c").sum()
            res[nm] = dict(ean=float(np.abs(f - r).sum() / r.sum()), wape90=float((g.f - g.r).abs().sum() / g.r.sum()), sesgo=float(f.sum() / r.sum() - 1))
            if nm == "Consenso o9":
                gc = g
            else:
                res[nm]["casas_gana_al_consenso"] = int(((g.f - g.r).abs() < (gc.f - gc.r).abs()).sum())
        out["horizonte"][lg] = res
    for col, key in [("tramo", "tramo"), ("isf", "bandera")]:
        for k, idx in pd.Series(np.arange(v.sum())).groupby(av[col].values):
            i = idx.values; r = A[i].sum(1)
            if r.sum() > 0:
                out[key][str(int(k)) if col == "isf" else k] = dict(n=int(len(i)), **{nm: float(np.abs(F[i].sum(1) - r).sum() / r.sum()) for nm, F in opts.items()})
    (W / "ciclo_vs_cons.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    for lg, res in out["horizonte"].items():
        print(lg, " · ".join(f"{nm}: EAN {x['ean']:.0%} casa {x['wape90']:.1%} sesgo {x['sesgo']:+.0%}" + (f" gana {x['casas_gana_al_consenso']}/5" if "casas_gana_al_consenso" in x else "") for nm, x in res.items()))
    for key in ["tramo", "bandera"]:
        print(key, {k: {nm: round(x[nm] * 100) for nm in opts} for k, x in out[key].items()})


if __name__ == "__main__":
    main()
