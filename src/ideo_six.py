"""Parlamento de 6 partidos y voto con influencia de los códigos similares (foto sep-25; verdad sep-26).

Partidos: Regla fragancias y Regla makeup (fijas) + Ciclo de vida (obligatorio: edad) + 3 elegidos por los datos, uno por forma de base.
Vetado: todo lo que use solo los últimos 3 meses (bases M3 / M3e y trend de 3M).

Pregunta nueva: ¿qué hicieron otros EANs como yo y les sirvió?
  Similares = mismos casa × segmento × tramo de edad (mínimo 5; si no, casa × tramo; si no, categoría × tramo), sin el propio EAN.
  Puntuación de cada partido para un EAN = α · su propio error + (1 − α) · error medio de sus similares con ese partido
  (error = Σ |forecast − real| / Σ real en los quarters de elección, tope 200%; sin ventas en esos quarters, su propio error no informa).
  α = 1: solo su pasado (como hasta ahora). α = 0: hace lo que les funcionó a sus similares.
Prueba limpia: partidos y voto con oct–mar (Q2+Q3), medida en abr–jun (Q4). También se comparan otras definiciones de similares.
Salida: work/ideo_six.json"""
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
FORMS6 = ["LY", "M6", "M12", "M6e", "M12e", "LY+M6e"]
ALPHAS = [1.0, 0.75, 0.5, 0.25, 0.0]
TRAMOS = ["6–11", "12–17", "18–25", "26+"]


def scores(FQ, Aq, qs, ids=None):
    """Error por EAN (tope 200%) en los quarters qs; si el real es 0, NaN (no informa)."""
    F = FQ if ids is None else FQ[ids]
    r = Aq[:, qs].sum(1)
    e = np.abs(F[:, :, qs] - Aq[None, :, qs]).sum(2)
    return np.where(r[None] > 0, np.minimum(e / np.where(r > 0, r, 1)[None], ipp.CAPSCORE), np.nan)


def select6(Sc, w, st, fixed, cand, dfix, verbose=True):
    """2 reglas + ciclo de vida (mejor variante) + 3 formas elegidas como en select_forms, sin 3M."""
    cx = ipp.complexity(st)
    form = st.base.values
    ok = cand & (st.tventana.values != 3)
    for d in dfix:
        ok &= d >= ipp.MIN_DIST
    rows = {f: np.where((form == f) & ok)[0] for f in FORMS6 + ["CV"]}

    def best_in(f, others):
        r = rows[f]
        tot = (np.minimum(Sc[others].min(0)[None], Sc[r]) * w[None]).sum(1)
        near = np.where(tot <= tot.min() + ipp.SIMPLE_TOL)[0]
        return int(r[near[np.lexsort((tot[near], cx[r][near]))[0]]])

    P = {f: best_in(f, list(fixed)) for f in FORMS6 + ["CV"]}

    def lloyd(P):
        for _ in range(12):
            ch = False
            for f in list(P):
                s_ = best_in(f, list(fixed) + [P[g] for g in P if g != f])
                if s_ != P[f]:
                    P[f] = s_; ch = True
            if not ch:
                return P
        return P

    P = lloyd(P)
    while len(P) > 4:
        cost = {f: ipp.objective(Sc, w, list(fixed) + [P[g] for g in P if g != f]) for f in P if f != "CV"}
        f = min(cost, key=cost.get)
        if verbose:
            print(f"  fuera {f}: {ipp.describe(st.loc[P[f]])}")
        del P[f]
        P = lloyd(P)
    ids = list(fixed) + [P["CV"]] + [P[f] for f in P if f != "CV"]
    if verbose:
        for i in ids:
            print("   ", ipp.describe(st.loc[i]))
    return ids


def peer_groups(a):
    """Índices de similares por EAN para varias definiciones (jerarquía con mínimo 5)."""
    keys = {"casa×seg×edad": [("casa", "seg", "tramo"), ("casa", "tramo"), ("cat", "tramo")],
            "casa×edad": [("casa", "tramo"), ("cat", "tramo")],
            "casa×seg (sin edad)": [("casa", "seg"), ("casa",)],
            "línea": [("casa", "linea"), ("casa", "seg"), ("casa",)]}
    out = {}
    for name, levels in keys.items():
        grp = []
        for i in range(len(a)):
            for lev in levels:
                k = tuple(a.iloc[i][c] for c in lev)
                m = np.ones(len(a), bool)
                for c, v in zip(lev, k):
                    m &= a[c].values == v
                m[i] = False
                if m.sum() >= 5:
                    grp.append(np.where(m)[0]); break
            else:
                grp.append(np.where(a.cat.values == a.cat.values[i])[0])
        out[name] = grp
    return out


def choose(S_own, groups, alpha):
    """S_own: partidos x EAN (NaN = sin info). Devuelve partido elegido por EAN."""
    Pn, n = S_own.shape
    peer = np.stack([np.nanmean(S_own[:, g], 1) for g in groups], 1)      # partidos x EAN
    own = np.where(np.isfinite(S_own), S_own, peer)                       # sin ventas -> manda lo de sus similares
    sc = alpha * own + (1 - alpha) * peer
    return np.nanargmin(np.where(np.isfinite(sc), sc, np.inf), 0)


def evaluate(a, F, Aq, cons, q, sel=None):
    s = np.ones(len(a), bool) if sel is None else sel
    R = Aq[s, q]
    out = dict(ean=float(np.abs(F[s, q] - R).sum() / R.sum()) if R.sum() > 0 else np.nan)
    if sel is None:
        rr = []
        for h in HOUSES:
            m = (a.casa == h).values
            Rh = Aq[m, q].sum(); rr.append((Rh, abs(F[m, q].sum() - Rh) / Rh, abs(cons[m, q].sum() - Rh) / Rh))
        rr = np.array(rr)
        out["w90"] = float((rr[:, 0] * rr[:, 1]).sum() / rr[:, 0].sum()); out["gana_casas"] = int((rr[:, 1] < rr[:, 2]).sum())
    return out


def main():
    st, FQ, Aq, a = ipp.load()
    cons = np.stack(a.cons_q.values); cat = a.cat.values; n = np.arange(len(a))
    rf, rm = ipp.fixed_ids(st)
    cand = ((st.fuente != "ninguna") | (st.base == "CV")).values & ~st.base.isin(["M3", "M3e"]).values
    dfix = pd.read_pickle(W / "ideo_stage1.pkl")[4]
    res = {}
    for tag, qs in [("limpia", [0, 1]), ("final", [0, 1, 2])]:
        r = Aq[:, qs].sum(1); c = np.where(r > 0)[0]
        Sc = np.empty((len(st), len(c)), np.float32)
        for i in range(0, len(st), 20000):
            Sc[i:i + 20000] = np.minimum(np.abs(FQ[i:i + 20000][:, c][:, :, qs] - Aq[None, c][:, :, qs]).sum(2) / r[c][None], ipp.CAPSCORE)
        w = 0.5 / len(c) + 0.5 * r[c] / r[c].sum()
        print(f"Partidos ({tag}, quarters {qs}):")
        ids = select6(Sc, w, st, [rf, rm], cand, dfix)
        res[tag] = dict(ids=ids, partidos=[ipp.describe(st.loc[i]) for i in ids], obj=ipp.objective(Sc, w, ids))
        del Sc
    # ---- voto con influencia de los similares: prueba limpia
    ids = res["limpia"]["ids"]; P = FQ[ids]
    S_own = scores(P, Aq, [0, 1])
    groups = peer_groups(a)
    best4 = np.abs(P[:, :, 2] - Aq[None, :, 2]).argmin(0)
    tab = []
    vfmt = ivc.vote(P, Aq, [0, 1]); vfmt = np.where(vfmt < 0, np.where(cat == "Fragancias", 0, 1), vfmt)
    base = dict(similares="—", alpha="formato fijo", acierto=float((vfmt == best4).mean()), **evaluate(a, P[vfmt, n], Aq, cons, 2))
    for t in TRAMOS:
        base["ean_" + t] = evaluate(a, P[vfmt, n], Aq, cons, 2, a.tramo.values == t)["ean"]
    tab.append(base)
    for gname, g in groups.items():
        for al in ALPHAS:
            v = choose(S_own, g, al)
            row = dict(similares=gname, alpha=al, acierto=float((v == best4).mean()), **evaluate(a, P[v, n], Aq, cons, 2))
            for t in TRAMOS:
                row["ean_" + t] = evaluate(a, P[v, n], Aq, cons, 2, a.tramo.values == t)["ean"]
            tab.append(row)
    # mejor α por tramo (con casa × segmento × edad): ¿cuánto conviene escuchar a los similares según la edad?
    g = groups["casa×seg×edad"]
    vt = np.zeros(len(a), int); best_alpha = {}
    for t in TRAMOS:
        m = a.tramo.values == t
        errs = {al: evaluate(a, P[choose(S_own, g, al), n], Aq, cons, 2, m)["ean"] for al in ALPHAS}
        best_alpha[t] = errs
    rule = np.where((cat == "Fragancias")[:, None], FQ[rf], FQ[rm])
    refs = dict(reglas_DAs=evaluate(a, rule, Aq, cons, 2), consenso=evaluate(a, cons, Aq, cons, 2))
    for t in TRAMOS:
        refs["reglas_DAs"]["ean_" + t] = evaluate(a, rule, Aq, cons, 2, a.tramo.values == t)["ean"]
        refs["consenso"]["ean_" + t] = evaluate(a, cons, Aq, cons, 2, a.tramo.values == t)["ean"]
    out = dict(partidos=res, tabla=tab, alpha_por_tramo=best_alpha, refs=refs,
               n_tramo={t: int((a.tramo == t).sum()) for t in TRAMOS},
               sin_ventas_octmar=int((Aq[:, :2].sum(1) == 0).sum()))
    (W / "ideo_six.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=float))
    pd.set_option("display.width", 250)
    print(pd.DataFrame(tab).round(3).to_string(index=False))
    print(pd.DataFrame(best_alpha).round(3).to_string())
    print(refs)


if __name__ == "__main__":
    main()
