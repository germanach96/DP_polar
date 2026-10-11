"""¿Qué decidiríamos en sep-25, solo con el pasado? (pedido del usuario 2026-10-10: en sep-25 no existe la foto sep-26)

1. Ensayo con el pasado (todo cerrado antes de sep-25): fotos simuladas sep-24, dic-24 y mar-25 (solo histórico; FY23 del LY).
   - Elegir con las urnas de Q2 y Q3 de FY25 (sep-24 Q2–Q3, dic-24 Q3) y medir en Q4 FY25 desde las 3 fotos (7–9, 4–6 y 1–3 meses).
   - Se comparan las formas de usar los 6 partidos: regla de su categoría, un partido, coalición de 2, media de los 6 y cada partido solo.
   - La decisión = la opción con menor error EAN a EAN en el ensayo (y se mira el WAPE90 de la casa).
2. Aplicación en sep-25: cada EAN elige con las 6 urnas del pasado (sep-24 Q2–Q4, dic-24 Q3–Q4, mar-25 Q4) y se pronostica desde la foto sep-25.
3. Solo para confirmar (no estaba disponible al decidir): real de la foto sep-26, Q2–Q4 FY26.
Salida: work/decision_sep25.json"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import fy25_eleccion as fe  # noqa
import six_multi as sm  # noqa

W = fe.W; N = fe.N
PAST = fe.PAST; KNOWN = fe.KNOWN
OPTS = {"regla": "Regla de su categoría", "un_partido": "Un partido (su voto)", "coalicion": "Coalición de sus 2 mejores", "media6": "Media de los 6"}
COLS = list(OPTS) + ["F:" + n for n in N]


def scores(B):
    ean = lambda x, c: float(np.abs(x[c] - x.real).sum() / x.real.sum())
    def w90(x, c):
        g = x.groupby("casa").agg(r=("real", "sum"), f=(c, "sum"))
        return dict(wape90=float((g.f - g.r).abs().sum() / g.r.sum()), sesgo=float(g.f.sum() / g.r.sum() - 1))
    out = {}
    for lg in ["7–9", "4–6", "1–3", "total"]:
        x = B if lg == "total" else B[B.lag == lg]
        if len(x):
            out[lg] = {c: dict(ean=ean(x, c), **w90(x, c)) for c in COLS}
    return out


def show(title, R):
    print(f"\n{title}")
    print(pd.DataFrame({lg: {OPTS.get(c, c.replace("F:", "Solo ")): f"{R[lg][c]['ean']:.1%}" for c in COLS} for lg in R}).to_string())
    print("WAPE90 casa (sesgo):", {OPTS[c]: f"{R['total'][c]['wape90']:.1%} ({R['total'][c]['sesgo']:+.0%})" for c in OPTS})


def main():
    sp = sm.specs()
    past = pd.concat([fe.ballots(s, sp, hasta=KNOWN) for s in PAST], ignore_index=True)
    # 1. ensayo con el pasado
    tr = past[past.q.isin(["FY25.Q2", "FY25.Q3"])]; te = past[past.q == "FY25.Q4"]
    Bt, *_ = fe.choose(tr, te)
    R1 = scores(Bt); show("1. Ensayo con el pasado: elegir con Q2–Q3 FY25, medir en Q4 FY25", R1)
    cand = list(OPTS)
    decision = min(cand, key=lambda c: R1["total"][c]["ean"])
    best_solo = min(["F:" + n for n in N], key=lambda c: R1["total"][c]["ean"])
    print(f"\nDecisión con el pasado: {OPTS[decision]} (mejor partido solo: {best_solo[2:]})")
    # 2. aplicación en sep-25 con las 6 urnas del pasado; 3. confirmación con sep-26
    B25 = fe.ballots(fe.ip.SNAP, sp)
    B, voto, Bv, partido = fe.choose(past, B25)
    R2 = scores(B); show("3. Confirmación (real sep-26, no disponible al decidir): foto sep-25 → Q2–Q4 FY26", R2)
    v26, _ = sm.elect(B25)
    j = pd.DataFrame(dict(v=voto)).join(v26.rename("v26"), how="inner")
    out = dict(ensayo=R1, decision=decision, decision_nombre=OPTS[decision], mejor_solo=best_solo[2:], aplicacion=R2, opciones=OPTS,
               urnas_pasado=sorted({f"{f}|{q}" for f, q in zip(past.foto, past.q)}), n_votantes=int(len(voto)),
               sin_historia=int((B.drop_duplicates("ean").historia != fe.HIST[0]).sum()), n_prueba=int(B.ean.nunique()),
               persistencia=dict(igual=float((j.v == j.v26).mean()), n=int(len(j))),
               escanos={p: int((partido == p).sum()) for p in N + ["Empate"]})
    (W / "decision_sep25.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print("persistencia:", out["persistencia"], "· escaños:", out["escanos"])


if __name__ == "__main__":
    main()
