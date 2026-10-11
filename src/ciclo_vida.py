"""¿Cómo seccionar el ciclo de vida? Prueba de con quién se compara un código joven para su curva de vida.

Curva de vida: para un EAN de a meses (6–17), los "parecidos" que en su día tuvieron a ± 2 meses (mínimo 5); multiplicador del mes h =
Σ venta de los parecidos a la edad a+h / Σ su media de las edades a−6..a−1. Forecast = nivel 6M del EAN × curva + DAs futuros
según la bandera (como el partido); base restando 0% o 100% de los DAs planificados.
Agrupaciones de parecidos (si no hay 5, sube al siguiente nivel):
  categoría (tipo: fragancias / makeup) · categoría × tamaño/función (sin casa) · casa · casa × tamaño/función (la actual)
  · franquicia (brand) · línea; cada una sin y con temporada de su casa. Referencia: nivel 6M plano (sin curva).
Fotos: sep-25, dic-25 y mar-26; quarters completos; EANs Central de 6–17 meses con lanzamiento visto.
Error = Σ_q |forecast − real| / Σ real (por quarter), y sesgo = Σ forecast / Σ real − 1.
Salida: work/ciclo_vida.json"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_engine as ie  # noqa
import ideo_panel as ip  # noqa

W = ie.W
SNAPS = ["2025-09", "2025-12", "2026-03"]
POOLS = ["categoría", "categoría×seg", "casa", "casa×seg", "franquicia", "línea"]
LEVEL_NAME = {"cat": "categoría", "catseg": "categoría×seg", "casa": "casa", "seg": "casa×seg", "franq": "franquicia", "linea": "línea"}


def main():
    rows = []
    for snap in SNAPS:
        P = ip.build(snap, save=False); ctx = ie.Ctx(P); a = P["attr"]
        young = a.votante.values & a.tramo.isin(["6–11", "12–17"]).values & (a.launch.values >= 1)
        qs = [(q, ix) for q, ix in zip(P["qlist"], P["qidx"]) if len(ix) == 3 and P["valid"][ix].all()]
        A = P["A"]
        wf = np.array([{0: 1.0, 1: 0.5, 2: 0.0}[int(f)] for f in a.isf.values.clip(0, 2)])[:, None]
        DAf = wf * P["DAf"]                                           # DAs futuros según la bandera, como el partido
        variants = {}
        curves = {}
        for pool in POOLS:
            for seas in [None, "casa"]:
                curves[(pool, seas)] = (ctx.curve(pool, seas), ctx.curve_level.copy())
        for dap in [0.0, 1.0]:
            X = ie.adjusted(ctx, dap, "0"); tag = f" · resta {int(dap * 100)}% DAs base"
            variants["Sin curva (nivel 6M plano)" + tag] = (np.clip(ie.base_matrix(ctx, X, "M6") + DAf, 0, None), None)
            for (pool, seas), (CV, lev) in curves.items():
                S = ctx.season(seas) if seas else None
                variants[f"{pool}{' + temporada' if seas else ''}{tag}"] = (np.clip(ie.base_matrix(ctx, X, "CV", S, CV) + DAf, 0, None), lev)
        for name, (F, lev) in variants.items():
            for i in np.where(young)[0]:
                for q, ix in qs:
                    rows.append(dict(foto=snap, q=q, ean=a.index[i], cat=a.cat.values[i], casa=a.casa.values[i], tramo=a.tramo.values[i],
                                     variante=name, f=float(F[i, ix].sum()), real=float(A[i, ix].sum()),
                                     nivel=(LEVEL_NAME.get(lev[i], "sin pares") if lev is not None else "—")))
        print(f"{snap}: {young.sum()} EANs jóvenes · quarters {[q for q, _ in qs]}")
    d = pd.DataFrame(rows)
    d["err"] = (d.f - d.real).abs()
    def summ(g):
        return pd.Series(dict(error=g.err.sum() / g.real.sum(), sesgo=g.f.sum() / g.real.sum() - 1, n=g.ean.nunique()))
    out = {}
    for by, nm in [(["variante"], "total"), (["variante", "cat"], "categoría"), (["variante", "tramo"], "tramo"), (["variante", "foto"], "foto")]:
        t = d.groupby(by).apply(summ).reset_index()
        out[nm] = t.to_dict("records")
        piv = t.pivot_table(index="variante", columns=by[1:] if len(by) > 1 else None, values="error") if len(by) > 1 else t.set_index("variante")[["error", "sesgo", "n"]]
        print(f"\n— {nm}"); print((piv * (100 if len(by) > 1 else 1)).round(1 if len(by) > 1 else 3).to_string())
    # de qué nivel salen los parecidos (cobertura) para cada agrupación sin temporada
    cov = d[d.variante.isin([p_ + " · resta 0% DAs base" for p_ in POOLS])].drop_duplicates(["foto", "ean", "variante"]).groupby(["variante", "nivel"]).size().unstack(fill_value=0)
    print("\n— nivel de los parecidos usado (EANs)"); print(cov.to_string())
    out["cobertura"] = cov.reset_index().to_dict("records")
    (W / "ciclo_vida.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=float))
    d.to_parquet(W / "ciclo_vida.parquet")


if __name__ == "__main__":
    main()
