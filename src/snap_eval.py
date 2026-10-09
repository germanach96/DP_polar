"""Evalúa work/snap_fc.parquet: WMAPE/bias por regla, foto y nivel de agregación. -> work/results/snapshots.md"""
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from pathlib import Path

W = Path(__file__).resolve().parents[1] / "work"
AGG = {  # nivel de medición: claves de agregación (además de snap, rule)
    "EAN-mes": ["ean", "target"],
    "EAN-quarter": ["ean", "fq"],
    "pline-quarter": ["pline", "fq"],
    "brand-quarter": ["brand", "fq"],
    "house-quarter": ["house", "fq"],
    "house-8m": ["house"],
    "total-8m": [],
}


def wm(df, keys):
    g = df.groupby(["snap", "rule"] + keys, as_index=False)[["F", "A"]].sum()
    g["ae"] = (g.F - g.A).abs(); g["e"] = g.F - g.A
    s = g.groupby(["rule", "snap"])[["ae", "e", "A"]].sum()
    return (s.ae / s.A).unstack(), (s.e / s.A).unstack()


def summary(fc, title):
    L = [f"\n# {title}\n"]
    tabs = {}
    for lvl, keys in AGG.items():
        w, b = wm(fc, keys)
        tabs[lvl] = (w, b)
    # tabla resumen: WMAPE medio 4 fotos por nivel
    S = pd.DataFrame({lvl: tabs[lvl][0].mean(1) for lvl in AGG})
    B = pd.DataFrame({lvl: tabs[lvl][1].mean(1) for lvl in ["EAN-mes"]}).rename(columns={"EAN-mes": "bias"})
    S = S.join(B)
    # victorias vs naive y consenso por foto (house-quarter y EAN-mes)
    for lvl in ["EAN-mes", "house-quarter"]:
        w = tabs[lvl][0]
        S[f"gana_naive_{lvl}"] = (w.lt(w.loc["naive(LY)"], axis=1)).sum(1)
        S[f"gana_cons_{lvl}"] = (w.lt(w.loc["consenso_foto"], axis=1)).sum(1)
    L.append("## Resumen: WMAPE medio de las 4 fotos por nivel de medición (orden por house-quarter)\n")
    L.append(S.sort_values("house-quarter").round(3).to_markdown())
    for lvl in ["EAN-mes", "house-quarter", "house-8m", "brand-quarter"]:
        w, b = tabs[lvl]
        top = w.mean(1).sort_values().index[:20].tolist() + ["naive(LY)", "consenso_foto", "trend6M@ean", "trend6M@house"]
        top = list(dict.fromkeys(top))
        L.append(f"\n## {lvl}: WMAPE por foto (top 20 + referencias)\n")
        L.append(w.loc[top].round(3).to_markdown())
        L.append(f"\n## {lvl}: bias por foto\n")
        L.append(b.loc[top].round(3).to_markdown())
    return "\n".join(L), S, tabs


def main():
    fc = pd.read_parquet(W / "snap_fc.parquet")
    out = ["# Backtest por foto (generado por src/snap_eval.py)\n",
           "Cada foto usa el histórico reexpresado truncado a su fecha; consenso de fotos < 2026-03 x factor de reexpresión del mes calendario. Horizonte: 8 meses tras el mes en curso. Verdad = última foto.",
           "Universo: sin Local, sin isf>=1. WMAPE = sum|F-A|/sum A tras agregar al nivel indicado. Bias = sum(F-A)/sum A (+ sobreforecast).",
           "Ojo: foto 2026-06 solo tiene 2 meses con verdad (jul, ago 2026).\n"]
    txt, S, _ = summary(fc, "TODOS los EANs del universo (incl. lanzamientos Central)")
    out.append(txt)
    txt2, S2, _ = summary(fc[fc.mature], "Solo EANs maduros (>=18 meses)")
    out.append(txt2)
    (W / "results" / "snapshots.md").write_text("\n".join(out))
    S.to_pickle(W / "snap_summary_all.pkl"); S2.to_pickle(W / "snap_summary_mature.pkl")
    print(S.sort_values("house-quarter").round(3).head(25).to_string())


if __name__ == "__main__":
    main()
