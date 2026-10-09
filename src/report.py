"""Genera work/results/backtest.md con rankings y desgloses a partir de work/ev.parquet."""
import sys
import numpy as np
import pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from evaluate import score  # noqa

W = Path(__file__).resolve().parents[1] / "work"
KEY = ["naive", "flat6", "house6", "house12", "brand12", "pline12", "median6", "trim6", "flat3", "flat12",
       "clean40", "clean40_s12", "house12_clean", "lvl6_house", "ets_damped", "epos6", "cutadj4",
       "combo_c12_h12", "combo_3", "combo_h12c_lvl6", "house12_half"]


def agg_level(df, level):
    """Agrega F y A a otro nivel (house/brand + target) antes de medir el error."""
    g = df.groupby(["method", "origin", "lag", "target", level], as_index=False)[["F", "A"]].sum()
    return g


def md(df, r=3):
    return df.round(r).to_markdown()


def main():
    ev = pd.read_parquet(W / "ev.parquet")
    ev = ev[~ev.method.isin(["lvl3_brand"]) | True]
    L = ["# Backtest (generado por src/report.py)\n",
         "Universo base: EANs maduros (>=18 meses de vida al corte), orígenes 2025-07..2026-07 (13 cortes), lags 1-8, ",
         "verdad = última versión. WMAPE = sum|F-A|/sum A a nivel EAN-mes. Bias = sum(F-A)/sum A (+ = sobreforecast).\n"]
    base = ev[ev.mature & (ev.origin >= "2025-07-01") & ~ev.method.str.startswith("consensus")]
    s = score(base).sort_values("wmape")
    s2 = score(base[~base.cut_flag]).rename(columns=lambda c: c + "_nocut")[["wmape_nocut", "bias_nocut"]]
    L += ["## Ranking global (EAN-mes)\n", md(s.join(s2)[["wmape", "bias", "wmape_nocut", "bias_nocut"]])]
    keym = [k for k in KEY if k in s.index]
    L += ["\n## WMAPE por lag\n", md(score(base[base.method.isin(keym)], "lag").wmape.unstack())]
    L += ["\n## Bias por lag\n", md(score(base[base.method.isin(keym)], "lag").bias.unstack())]
    L += ["\n## WMAPE por quarter objetivo\n", md(score(base[base.method.isin(keym)], "fq").wmape.unstack())]
    L += ["\n## Bias por quarter objetivo\n", md(score(base[base.method.isin(keym)], "fq").bias.unstack())]
    for seg in ["house", "abc", "volat", "isf", "resp"]:
        L += [f"\n## WMAPE por {seg}\n", md(score(base[base.method.isin(keym)], seg).wmape.unstack())]
        L += [f"\n## Bias por {seg}\n", md(score(base[base.method.isin(keym)], seg).bias.unstack())]
    # niveles agregados
    for lvl in ["brand", "house"]:
        a = agg_level(base, lvl)
        L += [f"\n## WMAPE agregado a {lvl}-mes\n", md(score(a).sort_values("wmape")[["wmape", "bias"]].head(25))]
    # quarter EAN (suma de 3 meses objetivo en un mismo quarter, lags 1-8 mezclados)
    q = base.groupby(["method", "origin", "ean", "fq"], as_index=False)[["F", "A"]].sum()
    L += ["\n## WMAPE a nivel EAN-quarter (suma de meses del quarter dentro del horizonte)\n",
          md(score(q).sort_values("wmape")[["wmape", "bias"]].head(25))]
    qh = base.groupby(["method", "origin", "house", "fq"], as_index=False)[["F", "A"]].sum()
    L += ["\n## WMAPE a nivel house-quarter\n", md(score(qh).sort_values("wmape")[["wmape", "bias"]].head(25))]
    # consenso vs métodos en los 4 cortes con consenso
    o = pd.to_datetime(["2025-09-01", "2025-12-01", "2026-03-01", "2026-06-01"])
    c = ev[ev.origin.isin(o)]
    sel = ["consensus", "consensus_scopeadj"] + keym
    for nm, cc in [("todos los EANs", c), ("EANs maduros", c[c.mature]), ("no maduros (lanzamientos)", c[~c.mature])]:
        cc = cc[cc.method.isin(sel)]
        sc = score(cc).sort_values("wmape")
        L += [f"\n## Consenso real vs métodos — {nm} (4 versiones)\n", md(sc[["wmape", "bias", "A"]], 3),
              "\nPor versión (WMAPE):\n", md(score(cc, "origin").wmape.unstack())]
    for lvl in ["house"]:
        a = agg_level(c[c.method.isin(sel)], lvl)
        L += [f"\n## Consenso vs métodos agregado a {lvl}-mes (todos los EANs)\n", md(score(a).sort_values("wmape")[["wmape", "bias"]])]
    (W / "results" / "backtest.md").write_text("\n".join(L))
    print("ok")


if __name__ == "__main__":
    main()
