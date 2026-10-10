"""Ideologías por EAN y propuesta de 10 partidos (2 fijos + 8 nuevos), foto sep-25 contra la verdad de sep-26.

Pasos (correr antes src/ideo_panel.py y src/ideo_engine.py):
 1. Puntuación EAN × estrategia: error del EAN = Σ_q |forecast_q − real_q| / Σ_q real_q en Q2, Q3, Q4 FY26 (tope 200%).
    Los EANs sin real en los 3 quarters (muertos) no entran en la búsqueda; sí votan en la elección.
 2. Mejor estrategia de cada EAN (a posteriori, "con trampa") y qué ideas de esa estrategia importan: una idea importa si
    cambiarla (dejando el resto igual) empeora el error en más de 0,5 puntos.
 3. Perfil ideológico: el 1% de mejores estrategias de cada EAN (≈2.000) frente al banco completo -> posiciones en las brújulas.
 4. Partidos: los 2 fijos (regla fragancias y regla makeup, + DAs de la foto como en la comparación estándar) y 8 nuevos.
    Selección voraz: en cada paso entra la estrategia que más baja el error del parlamento (cada EAN usa su mejor partido),
    con peso 50% por EAN y 50% por volumen. Reglas: todo partido lleva trend (o curva de vida) y ningún partido puede
    ser casi igual a otro (forecast trimestral distinto en menos de un 15% en la mediana de los EANs).
    Después se afina (cada partido = mejor estrategia común para sus votantes) y se simplifica (si una versión más simple
    cuesta menos de 0,2 puntos, se queda la simple).
 5. Elección con el formato fijo de CLAUDE.md, WAPE90 por casa × quarter contra el consenso y pruebas de robustez.
Salida: work/ideo.json, work/ideo_ean.parquet, reportes/IDEOLOGIAS_EAN.xlsx"""
import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_engine as ie  # noqa
import ideo_panel as ip  # noqa

warnings.filterwarnings("ignore")
W = ie.W; ROOT = W.parent
CAPSCORE = 2.0
TOPK = 0.01
MIN_DIST = 0.15
SIMPLE_TOL = 0.002
N_NEW = 8
DIMS = ["base", "estac", "fuente", "tventana", "fuerza", "tope", "dap", "cortes", "daf", "pool"]
FAM = {"LY": "Año pasado", "M3": "Media plana", "M6": "Media plana", "M12": "Media plana", "M3e": "Media estacional",
       "M6e": "Media estacional", "M12e": "Media estacional", "LY+M6e": "Mixta", "CV": "Ciclo de vida"}
MEM = {"LY": "Año pasado", "M3": "3M", "M6": "6M", "M12": "12M", "M3e": "3M", "M6e": "6M", "M12e": "12M", "LY+M6e": "Año pasado + 6M", "CV": "6M"}
QLAB = {"FY26.Q2": "Q2 FY26 · oct–dic 25", "FY26.Q3": "Q3 FY26 · ene–mar 26", "FY26.Q4": "Q4 FY26 · abr–jun 26"}


# ---------------------------------------------------------------- descripción
def pct(x):
    return f"{x * 100:.0f}%"


def describe(r):
    """Fórmula en lenguaje de negocio."""
    b = r["base"]; e = r["estac"]
    eg = {"casa": "su casa", "casa×seg": "su casa × segmento", "línea": "su línea", "categoría": "su categoría"}.get(e, "")
    if b == "LY":
        base = "Mismo mes del año pasado"
    elif b in ("M3", "M6", "M12"):
        base = f"Media de los últimos {b[1:]} meses, plana"
    elif b.endswith("e") and b != "LY+M6e":
        base = f"Media {b[1:-1]}M sin temporada × perfil mensual de {eg}"
    elif b == "LY+M6e":
        base = f"Mitad año pasado, mitad media 6M sin temporada × perfil de {eg}"
    else:
        pool = {"categoría": "su categoría", "casa": "su casa", "casa×seg": "su casa × segmento", "línea": "su línea",
                "categoría×seg": "su categoría × segmento", "franquicia": "su franquicia", "por tipo": "su categoría (fragancias) o su línea (makeup)"}[r["pool"]]
        base = (f"Nivel 6M{' sin temporada' if e != 'sin' else ''} × ciclo de vida: jóvenes, curva de los códigos de {pool} a su edad; "
                f"maduros, trend 12M de su fase" + (" × perfil mensual de su casa" if e != "sin" else ""))
    src = {"EAN": "del propio EAN", "línea": "de su línea", "franquicia": "de su franquicia", "segmento": "de su segmento",
           "casa": "de su casa", "categoría": "de su categoría", "fase": "de su fase (casa × fase)"}
    tr = "" if r["fuente"] == "ninguna" else (f" × (1 + {pct(r['fuerza'])} del trend {int(r['tventana'])}M {src[r['fuente']]}, "
                                               f"tope ±{pct(r['tope'])})")
    adj = []
    if r["cortes"] != "0":
        adj.append("+ mín(10% cortes; 10% envío)" if r["cortes"] == "10%·tope" else f"+ {r['cortes']} cortes")
    if r["dap"] > 0:
        adj.append(f"− {pct(r['dap'])} DAs+ del pasado")
    adj = f" · base {' '.join(adj)}" if adj else " · base sin ajustes"
    daf = " · sin DAs de la foto" if r["daf"] == 0 else f" · + {pct(r['daf'])} DAs de la foto"
    return base + tr + adj + daf


def ideas(r):
    """Etiquetas cortas de la ideología."""
    return dict(familia=FAM[r["base"]], memoria=MEM[r["base"]],
                estac=("propia (año pasado)" if r["base"] == "LY" else ("propia + " + r["estac"]) if r["base"] == "LY+M6e"
                       else ("ninguna" if r["estac"] == "sin" else r["estac"])),
                fuente=("edad y fase (ciclo de vida)" if r["base"] == "CV" else r["fuente"]),
                trend=("—" if r["fuente"] == "ninguna" else f"{pct(r['fuerza'])} · {int(r['tventana'])}M · ±{pct(r['tope'])}"),
                dap=pct(r["dap"]), cortes=("10% con tope" if r["cortes"] == "10%·tope" else r["cortes"]), daf=pct(r["daf"]))


def complexity(st):
    c = np.zeros(len(st))
    c += st.dap.map({0.0: 0, 0.5: 1, 1.0: 1}).fillna(2).values
    c += st.cortes.map({"0": 0, "25%": 1}).fillna(2).values
    c += st.daf.map({0.0: 0, 1.0: 0}).fillna(1).values
    c += st.fuerza.map({0.0: 0, 1.0: 0, 0.5: 1}).fillna(2).values
    c += st.tventana.map({0: 0, 12: 0, 6: 1}).fillna(2).values
    c += st.tope.map({0.0: 0, 0.3: 0}).fillna(1).values
    c += st.estac.map({"sin": 0, "casa": 0, "categoría": 1, "casa×seg": 1}).fillna(2).values
    c += st.fuente.map({"ninguna": 0, "segmento": 0, "casa": 0, "EAN": 0, "línea": 1, "categoría": 1, "franquicia": 1}).fillna(1).values
    return c


# ---------------------------------------------------------------- carga
def load():
    st = pd.read_parquet(W / "ideo_strats.parquet")
    FQ = np.load(W / "ideo_fq.npy")
    B = np.load(W / "ideo_bank.npz"); Aq = B["Aq"]
    P = pd.read_pickle(W / "ideo_panel.pkl"); a = P["attr"].loc[B["voters"]].copy()
    vi = P["attr"].index.get_indexer(B["voters"])
    a["cons_q"] = list(np.stack([P["cons"][vi][:, ix].sum(1) for ix in ip.QIDX], 1))
    a["daf_q"] = list(np.stack([P["DAf"][vi][:, ix].sum(1) for ix in ip.QIDX], 1))
    return st, FQ, Aq, a


def find(st, **kw):
    q = st
    for k, v in kw.items():
        q = q[q[k] == v]
    assert len(q) == 1, (kw, len(q))
    return int(q.id.values[0])


def fixed_ids(st):
    rf = find(st, base="LY", estac="sin", fuente="segmento", tventana=12, fuerza=1.0, tope=0.3, dap=0.5, cortes="25%", daf=1.0)
    rm = find(st, base="M6", estac="sin", fuente="segmento", tventana=12, fuerza=0.5, tope=0.3, dap=0.25, cortes="10%·tope", daf=1.0)
    return rf, rm


# ---------------------------------------------------------------- distancia entre partidos
def dist_to(FQ, p, cols, chunk=20000):
    """Mediana sobre EANs de Σ_q|F_s − F_p| / Σ_q (F_s + F_p)/2, para todas las estrategias s."""
    out = np.empty(len(FQ), np.float32)
    fp = FQ[p][cols]
    for i in range(0, len(FQ), chunk):
        f = FQ[i:i + chunk][:, cols]
        num = np.abs(f - fp[None]).sum(2); den = ((f + fp[None]) / 2).sum(2)
        x = np.where(den > 0, num / np.where(den > 0, den, 1), 0)
        out[i:i + chunk] = np.median(x, 1)
    return out


# ---------------------------------------------------------------- selección
def _pair(FQ, i, j, cols):
    a = FQ[i][cols]; b = FQ[j][cols]
    num = np.abs(a - b).sum(1); den = ((a + b) / 2).sum(1)
    return np.where(den > 0, num / np.where(den > 0, den, 1), 0)


def objective(Sc, w, ids):
    return float((Sc[ids].min(0) * w).sum())


def select(Sc, w, st, FQ, cols, fixed, cand, n_new=N_NEW, verbose=True, refine=True, dcache=None):
    dcache = {} if dcache is None else dcache

    def D(p):
        if p not in dcache:
            dcache[p] = dist_to(FQ, p, cols)
        return dcache[p]

    chosen = list(fixed)
    cb = Sc[chosen].min(0)
    steps = []
    for k in range(n_new):
        gain = (np.maximum(cb[None] - Sc, 0) * w[None]).sum(1)
        gain[~cand] = -1
        for p in chosen:
            gain[D(p) < MIN_DIST] = -1
        s = int(gain.argmax()); chosen.append(s); cb = np.minimum(cb, Sc[s])
        steps.append(dict(id=s, gain=float(gain[s]), obj=float((cb * w).sum())))
        if verbose:
            print(f"  +{k + 1}: obj {steps[-1]['obj']:.4f}  {describe(st.loc[s])}")
    if not refine:
        return chosen, steps
    # afinado: cada partido nuevo = mejor estrategia común para sus votantes (respetando la distancia con los demás)
    cx = complexity(st)
    for it in range(8):
        changed = False
        for j in range(len(fixed), len(chosen)):
            others = [p for i, p in enumerate(chosen) if i != j]
            vote = Sc[chosen].argmin(0)
            mine = vote == j
            ok = cand.copy()
            for p in others:
                ok &= D(p) >= MIN_DIST
            # costo de cada candidato reemplazando al partido j
            rest = Sc[others].min(0)
            tot = (np.minimum(rest[None], Sc) * w[None]).sum(1)
            tot[~ok] = np.inf
            s = int(tot.argmin())
            # simplificación: la más simple dentro de la tolerancia
            near = np.where(tot <= tot[s] + SIMPLE_TOL)[0]
            s2 = int(near[np.lexsort((tot[near], cx[near]))[0]])
            cur = tot[chosen[j]] if np.isfinite(tot[chosen[j]]) else np.inf
            if s2 != chosen[j] and (tot[s2] < cur - 1e-6 or (tot[s2] <= cur + SIMPLE_TOL and cx[s2] < cx[chosen[j]])):
                if verbose:
                    print(f"  afinado {j}: {describe(st.loc[chosen[j]])}\n        -> {describe(st.loc[s2])} ({cur:.4f} -> {tot[s2]:.4f}, votantes {mine.sum()})")
                chosen[j] = s2; changed = True
        if not changed:
            break
    return chosen, steps


FORMS = ["LY", "M3", "M6", "M12", "M3e", "M6e", "M12e", "LY+M6e", "CV"]


def select_forms(Sc, w, st, fixed, cand, dfix, n_new=N_NEW, verbose=True):
    """Un partido por forma de base. Dentro de cada forma, la configuración (estacionalidad, trend, DAs, cortes) que más baja
    el error del parlamento, con los demás partidos fijos (afinado por turnos hasta que nada cambia). Luego se quita, de una en
    una, la forma que menos aporta hasta quedar n_new. Ninguna puede ser casi igual a una regla fija (distancia < 15%)."""
    cx = complexity(st)
    form = st.base.values
    okfix = np.ones(len(st), bool)
    for d in dfix:
        okfix &= d >= MIN_DIST
    rows = {f: np.where((form == f) & cand & okfix)[0] for f in FORMS}

    def best_in(f, others):
        r = rows[f]
        rest = Sc[others].min(0)
        tot = (np.minimum(rest[None], Sc[r]) * w[None]).sum(1)
        mn = tot.min()
        near = np.where(tot <= mn + SIMPLE_TOL)[0]
        k = near[np.lexsort((tot[near], cx[r][near]))[0]]
        return int(r[k]), float(tot[k])

    def lloyd(P):
        for it in range(12):
            changed = False
            for f in list(P):
                others = list(fixed) + [P[g] for g in P if g != f]
                s_, _ = best_in(f, others)
                if s_ != P[f]:
                    P[f] = s_; changed = True
            if not changed:
                break
        return P

    P = {}
    for f in FORMS:                                # arranque: cada forma por su cuenta junto a las reglas
        if len(rows[f]):
            P[f] = best_in(f, list(fixed))[0]
    P = lloyd(P)
    drops = []
    while len(P) > n_new:
        cost = {f: objective(Sc, w, list(fixed) + [P[g] for g in P if g != f]) for f in P}
        f = min(cost, key=cost.get)
        drops.append(dict(forma=f, id=P[f], obj_sin=cost[f], obj_con=objective(Sc, w, list(fixed) + list(P.values()))))
        if verbose:
            print(f"  fuera {f}: {describe(st.loc[P[f]])} (sin ella {cost[f]:.4f})")
        del P[f]
        P = lloyd(P)
    chosen = list(fixed) + list(P.values())
    if verbose:
        for f, s_ in P.items():
            print(f"  {f}: {describe(st.loc[s_])}")
        print(f"  objetivo {objective(Sc, w, chosen):.4f}")
    return chosen, drops


# ---------------------------------------------------------------- elección (formato fijo)
def election(FQp, Aq, names):
    """FQp: partidos x EAN x 3. Devuelve votos por quarter, voto final y WAPE por quarter."""
    P_, n, Q = FQp.shape
    err = np.abs(FQp - Aq[None])
    wq = np.where(Aq[None] > 0, err / np.where(Aq[None] > 0, Aq[None], 1), err)       # WAPE del EAN en el quarter
    best = wq.min(0, keepdims=True)
    tie = np.isclose(wq, best, rtol=1e-9, atol=1e-9)
    ntie = tie.sum(0)
    votes = np.where((ntie <= 3)[None], tie, False).astype(int)                         # P x n x Q
    qwin = np.where(ntie == 1, np.array(names, dtype=object)[wq.argmin(0)], "Empate")   # n x Q (para las tarjetas por quarter)
    tv = votes.sum(2)                                                                    # P x n
    top = tv.max(0, keepdims=True)
    cand = tv == top
    sw = np.where(cand, wq.sum(2), np.inf)
    bm = sw.min(0, keepdims=True)
    win = cand & np.isclose(sw, bm, rtol=1e-9, atol=1e-9)
    final = np.where(win.sum(0) == 1, np.array(names, dtype=object)[sw.argmin(0)], "Empate")
    desemp = (cand.sum(0) > 1) & (final != "Empate")
    return dict(votes=votes, qwin=qwin, final=final, desempate=desemp, wq=wq, void=(ntie > 3))


def tally(final, real, names):
    vol = real.sum() or 1
    t = dict(eans=int(len(final)), real=float(real.sum()), seats={}, vol={})
    for p in names + ["Empate"]:
        mk = final == p
        t["seats"][p] = int(mk.sum()); t["vol"][p] = float(real[mk].sum() / vol)
    t["win_eans"] = max(names, key=lambda p: t["seats"][p]); t["win_vol"] = max(names, key=lambda p: t["vol"][p])
    return t


# ---------------------------------------------------------------- perfiles (brújulas)
def axis_scores(st):
    b = st.base.values
    seas = np.isin(b, ["LY", "LY+M6e", "M3e", "M6e", "M12e"]) | ((b == "CV") & (st.estac.values != "sin"))
    short = pd.Series(b).map({"M3": 1, "M3e": 1, "M6": .5, "M6e": .5, "CV": .5, "LY+M6e": .25, "M12": 0, "M12e": 0, "LY": 0}).values
    indiv = pd.Series(st.fuente.values).map({"EAN": 1, "línea": .8, "fase": .6, "franquicia": .5, "segmento": .4, "casa": .2,
                                            "categoría": 0}).values           # NaN si no lleva trend
    faith = np.where(st.fuente.values == "ninguna", 0, st.fuerza.values * st.tope.values / 0.6)   # caída máxima asumida (0..1)
    twin = pd.Series(st.tventana.values).map({3: 1, 6: .5, 12: 0}).values
    dap = st.dap.values
    cuts = pd.Series(st.cortes.values).map({"0": 0, "10%·tope": .2, "25%": .5, "50%": 1}).values
    daf = st.daf.values
    curve = (b == "CV").astype(float)
    return dict(estacional=seas.astype(float), corto=short, individual=indiv, fe=faith, tventana=twin, dap=dap, cortes=cuts, daf=daf, curva=curve)


def profiles(Sc, st, K):
    top = np.argpartition(Sc, K, axis=0)[:K]          # K x n
    ax = axis_scores(st); out = {}
    for k, v in ax.items():
        mb = np.nanmean(v)
        mt = np.array([np.nanmean(v[top[:, j]]) for j in range(Sc.shape[1])])
        lift = mt - mb
        out[k] = np.where(lift >= 0, lift / max(1 - mb, 1e-9), lift / max(mb, 1e-9))
        out[k + "_raw"] = mt
    return out, top


def importance(Sc, st, best, best_sc):
    """Cuánto empeora (en puntos de error) la mejor alternativa al cambiar UNA idea de la mejor estrategia del EAN, dejando el resto igual.
    Grupos de ideas: base (forma + estacionalidad + pool), trend (fuente, ventana, fuerza, tope -> se compara con 'sin trend'),
    DAs del pasado, cortes, DAs de la foto. Si empeora menos de 0,5 puntos, esa idea no importa para el EAN."""
    keycols = ["base", "estac", "fuente", "tventana", "fuerza", "tope", "dap", "cortes", "daf", "pool"]
    codes = np.stack([pd.factorize(st[c].astype(str))[0] for c in keycols], 1)
    ci = {c: i for i, c in enumerate(keycols)}
    look = {tuple(r): i for i, r in enumerate(map(tuple, codes))}
    none_tr = tuple(codes[np.where(st.fuente.values == "ninguna")[0][0], [ci["fuente"], ci["tventana"], ci["fuerza"], ci["tope"]]])
    imp = {g: np.full(len(best), np.nan) for g in ["base", "fuente", "dap", "cortes", "daf"]}
    for j, b in enumerate(best):
        r = codes[b]
        for g in ["dap", "cortes", "daf"]:
            alts = []
            for v in np.unique(codes[:, ci[g]]):
                if v != r[ci[g]]:
                    x = r.copy(); x[ci[g]] = v; alts.append(look.get(tuple(x)))
            alts = [x for x in alts if x is not None]
            imp[g][j] = Sc[alts, j].min() - best_sc[j] if alts else np.nan
        if st.fuente.values[b] != "ninguna":
            x = r.copy(); x[[ci["fuente"], ci["tventana"], ci["fuerza"], ci["tope"]]] = none_tr
            k = look.get(tuple(x))
            imp["fuente"][j] = Sc[k, j] - best_sc[j] if k is not None else np.nan
        else:
            imp["fuente"][j] = 0.0 if st.base.values[b] != "CV" else np.nan
        same = (codes[:, [ci[c] for c in ["fuente", "tventana", "fuerza", "tope", "dap", "cortes", "daf"]]] == r[[ci[c] for c in ["fuente", "tventana", "fuerza", "tope", "dap", "cortes", "daf"]]]).all(1)
        same &= codes[:, ci["base"]] != r[ci["base"]]
        alts = np.where(same)[0]
        imp["base"][j] = Sc[alts, j].min() - best_sc[j] if len(alts) else np.nan
    return imp


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    st, FQ, Aq, a = load()
    rf, rm = fixed_ids(st)
    real = Aq.sum(1); alive = real > 0
    cols = np.where(alive)[0]
    E = np.abs(FQ - Aq[None]).sum(2)                                   # S x n
    Sc = np.minimum(E[:, cols] / real[cols][None], CAPSCORE).astype(np.float32)
    aa = a.iloc[cols]
    n = len(cols)
    w = 0.5 / n + 0.5 * aa.real.values / aa.real.sum()
    cand = ((st.fuente != "ninguna") | (st.base == "CV")).values
    print(f"carga {time.time() - t0:.0f}s · {len(st)} estrategias · {n} EANs con real")

    # ---- 2-3. mejor estrategia por EAN, importancia de cada idea y perfiles (caché: es lo más lento)
    cache = W / "ideo_stage1.pkl"
    cx = complexity(st)
    K = int(len(st) * TOPK)
    if cache.exists():
        best, best_sc, imp, prof, dfix = pd.read_pickle(cache)
    else:
        best = np.empty(n, int); best_sc = np.empty(n)
        for j in range(n):
            col = Sc[:, j]; mn = col.min()
            near = np.where(col <= mn + 1e-6)[0]
            best[j] = near[np.argmin(cx[near])]; best_sc[j] = mn
        imp = importance(Sc, st, best, best_sc)
        print(f"mejores por EAN {time.time() - t0:.0f}s")
        prof, _ = profiles(Sc, st, K)
        print(f"perfiles {time.time() - t0:.0f}s")
        dfix = [dist_to(FQ, p, cols) for p in (rf, rm)]
        print(f"distancias a las reglas {time.time() - t0:.0f}s")
        pd.to_pickle((best, best_sc, imp, prof, dfix), cache)
    ID = pd.DataFrame([ideas(r) for r in st[["base", "estac", "fuente", "tventana", "fuerza", "tope", "dap", "cortes", "daf"]].to_dict("records")])

    # ---- 4. partidos: uno por forma de base
    print("Selección (todos los EANs):")
    chosen, drops = select_forms(Sc, w, st, [rf, rm], cand, dfix)
    obj_rules = objective(Sc, w, [rf, rm]); obj_final = objective(Sc, w, chosen)
    # selección libre (sin una forma por partido), solo para medir cuánto cuesta la estructura
    free, _ = select(Sc, w, st, FQ, cols, [rf, rm], cand, verbose=False, refine=False, dcache={rf: dfix[0], rm: dfix[1]})
    obj_free = objective(Sc, w, free)
    print(f"objetivo: reglas {obj_rules:.4f} · 10 partidos {obj_final:.4f} · libre {obj_free:.4f} · oráculo {float((Sc.min(0) * w).sum()):.4f}")
    # orden por aporte (voraz sobre la lista final)
    order = [rf, rm]; contrib = [dict(id=-1, obj=obj_rules)]
    rest = chosen[2:]
    while rest:
        g = [objective(Sc, w, order + [p]) for p in rest]
        p = rest[int(np.argmin(g))]; order.append(p); rest.remove(p); contrib.append(dict(id=p, obj=min(g)))
    chosen = order
    # distancias entre partidos (comprobación de que no son casi iguales)
    dmat = np.array([[float(np.median(_pair(FQ, i, j, cols))) for j in chosen] for i in chosen])
    # ---- robustez: elige con una mitad de EANs, mide en la otra
    rng = np.random.default_rng(7); rob = []
    for rep in range(10):
        perm = rng.permutation(n); A_, B_ = perm[: n // 2], perm[n // 2:]
        dA = [d for d in dfix]   # la distancia a las reglas se mide con todos los EANs
        chA, _ = select_forms(Sc[:, A_], w[A_], st, [rf, rm], cand, dA, verbose=False)
        chB, _ = select_forms(Sc[:, B_], w[B_], st, [rf, rm], cand, dA, verbose=False)
        ob = lambda ch, S_: float((Sc[ch][:, S_].min(0) * w[S_]).sum() / w[S_].sum())
        rob.append(dict(rep=rep, dentro=ob(chA, A_), fuera=ob(chA, B_), techo_fuera=ob(chB, B_), solo_reglas=ob([rf, rm], B_),
                        final_fuera=ob(chosen, B_), formas_A=sorted(st.base[i] for i in chA[2:]),
                        iguales=int(len(set(chA[2:]) & set(chosen[2:]))), formas_iguales=int(len(set(st.base[chA[2:]]) & set(st.base[chosen[2:]])))))
        print(f"  robustez {rep}: dentro {rob[-1]['dentro']:.3f} fuera {rob[-1]['fuera']:.3f} techo {rob[-1]['techo_fuera']:.3f} "
              f"reglas {rob[-1]['solo_reglas']:.3f} · formas {rob[-1]['formas_A']} · mismos partidos {rob[-1]['iguales']}")
    print(f"partidos {time.time() - t0:.0f}s")
    # ---- prueba limpia en el tiempo: partidos elegidos SOLO con Q2+Q3, cada EAN elige con Q2+Q3, se mide en Q4
    r23 = Aq[:, :2].sum(1); c23 = np.where(r23 > 0)[0]
    E23 = np.abs(FQ[:, c23, :2] - Aq[None, c23, :2]).sum(2)
    Sc23 = np.minimum(E23 / r23[c23][None], CAPSCORE).astype(np.float32); del E23
    w23 = 0.5 / len(c23) + 0.5 * r23[c23] / r23[c23].sum()
    ch23, _ = select_forms(Sc23, w23, st, [rf, rm], cand, dfix, verbose=False)
    del Sc23
    print("partidos con Q2+Q3:", [describe(st.loc[i]) for i in ch23[2:]])

    # ---- 5. elección con los 10 partidos (todos los votantes, también los muertos)
    names = name_parties(st, chosen)
    FQp = FQ[chosen]
    el = election(FQp, Aq, names)
    a["voto"] = el["final"]; a["desempate"] = el["desempate"]
    for qi, q in enumerate(ip.QLIST):
        a["ganador_" + q] = el["qwin"][:, qi]
    for i, p in enumerate(names):
        a["votos:" + p] = el["votes"][i].sum(1)
        a["F:" + p] = FQp[i].sum(1)
        a["err:" + p] = np.abs(FQp[i] - Aq).sum(1)
    a["cons"] = [x.sum() for x in a.cons_q]
    a["err:Consenso"] = [np.abs(c - q).sum() for c, q in zip(a.cons_q, Aq)]
    # mejores por EAN a posteriori (solo EANs con real)
    a["mejor"] = None; a["mejor_err"] = np.nan
    a.loc[aa.index, "mejor"] = [describe(st.loc[b]) for b in best]
    a.loc[aa.index, "mejor_err"] = best_sc
    for k in ["familia", "memoria", "estac", "fuente", "trend", "dap", "cortes", "daf"]:
        a.loc[aa.index, "mejor_" + k] = ID.loc[best, k].values
    for g in imp:
        a.loc[aa.index, "importa_" + g] = imp[g]
    for k, v in prof.items():
        a.loc[aa.index, "pos_" + k] = v
    a.drop(columns=["cons_q", "daf_q"]).to_parquet(W / "ideo_ean.parquet")

    # ---- resúmenes
    out = dict(n_estrategias=int(len(st)), n_votantes=int(len(a)), n_con_real=int(n), n_muertos=int((~alive).sum()), topk=K,
               obj_reglas=obj_rules, obj_final=obj_final, obj_libre=obj_free, oraculo=float((Sc.min(0) * w).sum()),
               libre=[describe(st.loc[i]) for i in free[2:]], descartes=[dict(d, formula=describe(st.loc[d["id"]])) for d in drops],
               distancias=dmat.tolist(),
               partidos=[], aportes=[], robustez=rob, pop={}, imp={}, dims_cat={}, prof={})
    for i, (p, s) in enumerate(zip(names, chosen)):
        r = st.loc[s]
        out["partidos"].append(dict(nombre=p, id=int(s), fijo=i < 2, formula=describe(r), ideas=ideas(r), **{k: (str(r[k]) if k in ("cortes", "estac", "base", "fuente", "pool") else float(r[k])) for k in DIMS}))
    for c in contrib:
        out["aportes"].append(dict(partido=(names[chosen.index(c["id"])] if c["id"] >= 0 else "Reglas fijas"), obj=c["obj"]))
    # popularidad de ideas en la mejor estrategia (solo donde la idea importa) por categoría
    for cat in ["Fragancias", "Makeup"]:
        s = (aa.cat == cat).values; vv = aa.real.values[s]
        out["pop"][cat] = {}
        for k, g in [("familia", "base"), ("memoria", "base"), ("estac", "base"), ("fuente", "fuente"), ("dap", "dap"), ("cortes", "cortes"), ("daf", "daf")]:
            lab = ID.loc[best[s], k].values; im = imp[g][s] >= 0.005
            lab = np.where(im, lab, "No importa")
            ser = pd.Series(vv).groupby(lab).sum() / vv.sum(); cnt = pd.Series(lab).value_counts()
            out["pop"][cat][k] = {str(x): dict(eans=int(cnt[x]), vol=float(ser[x])) for x in cnt.index}
        out["imp"][cat] = {g: dict(mediana=float(np.nanmedian(imp[g][s])), importa=float(np.nanmean(imp[g][s] >= 0.005))) for g in imp}
    out["prof"] = {k: {cat: float(np.nanmean(v[(aa.cat == cat).values])) for cat in ["Fragancias", "Makeup"]} for k, v in prof.items() if not k.endswith("_raw")}
    # elección
    out["eleccion"] = elect_summary(a, names, el, Aq)
    out["w90"] = wape90(a, names, FQp, Aq)
    out["temporal"] = temporal(a, names, FQp, Aq)
    out["temporal_limpio"] = temporal(a, name_parties(st, ch23), FQ[ch23], Aq)
    out["temporal_limpio"]["partidos"] = [describe(st.loc[i]) for i in ch23]
    out["names"] = names
    out["tiempo"] = time.time() - t0
    (W / "ideo.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=float))
    excel(a, names)
    print(f"listo {time.time() - t0:.0f}s")
    return out


def name_parties(st, chosen):
    names = ["Regla fragancias", "Regla makeup"]
    used = set(names)
    for s in chosen[2:]:
        r = st.loc[s]
        b = r["base"]
        if b == "CV":
            nm = "Ciclo de vida"
        elif b == "LY":
            nm = "Año pasado"
        elif b == "LY+M6e":
            nm = "Mixta"
        elif b.endswith("e"):
            nm = f"Media {b[1:-1]}M estacional"
        else:
            nm = f"Media {b[1:]}M"
        tr = {"EAN": "propio", "línea": "línea", "franquicia": "franquicia", "segmento": "segmento", "casa": "casa", "categoría": "categoría",
              "fase": "fase", "ninguna": ""}[r["fuente"]]
        full = nm + (f" · {tr}" if tr else "")
        if full in used:
            full += f" · DAs {pct(r['daf'])}"
        used.add(full); names.append(full)
    return names


def elect_summary(a, names, el, Aq):
    real = a.real.values
    out = dict(total=tally(a.voto.values, real, names), por={}, por_q={}, desempates=int(a.desempate.sum()),
               quarters_nulos=int(el["void"].sum()))
    groups = [("cat", "Categoría"), ("casa", "Casa"), ("seg", "Tamaño"), ("tramo", "Edad"), ("fase", "Fase"), ("isf", "Bandera")]
    for col, nm in groups:
        g = a if col != "seg" else a[a.cat == "Fragancias"]
        out["por"][nm] = {str(k): tally(x.voto.values, x.real.values, names) for k, x in g.groupby(col)}
    for qi, q in enumerate(ip.QLIST):
        out["por_q"][q] = tally(el["qwin"][:, qi], Aq[:, qi], names)
    return out


def wape90(a, names, FQp, Aq):
    rows = []
    cons = np.stack(a.cons_q.values)
    for h in ["Burberry", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"]:
        s = (a.casa == h).values
        for qi, q in enumerate(ip.QLIST):
            R = Aq[s, qi].sum()
            r = dict(casa=h, q=q, real=float(R), Consenso=float(abs(cons[s, qi].sum() - R) / R), spp3_Consenso=float((R - cons[s, qi].sum()) / R))
            for i, p in enumerate(names):
                F = FQp[i][s, qi].sum()
                r[p] = float(abs(F - R) / R); r["spp3_" + p] = float((R - F) / R)
            rows.append(r)
    return rows


def temporal(a, names, FQp, Aq):
    """Prueba de persistencia: cada EAN elige su partido con Q2+Q3 (menor error) y se aplica en Q4."""
    err = np.abs(FQp - Aq[None])
    pick = err[:, :, :2].sum(2).argmin(0)
    f4 = FQp[pick, np.arange(len(pick)), 2]
    cons = np.stack(a.cons_q.values)[:, 2]
    A4 = Aq[:, 2]
    cat = a.cat.values
    res = {"w90": []}
    for h in ["Burberry", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"]:
        s = (a.casa == h).values; R = A4[s].sum()
        rule = FQp[0][s, 2] if h in ("Burberry", "Gucci", "Marc Jacobs") else FQp[1][s, 2]
        res["w90"].append(dict(casa=h, real=float(R), elegido=float(abs(f4[s].sum() - R) / R), regla=float(abs(rule.sum() - R) / R),
                               consenso=float(abs(cons[s].sum() - R) / R), spp3_elegido=float((R - f4[s].sum()) / R)))
    for c in ["Fragancias", "Makeup", "Total"]:
        s = np.ones(len(a), bool) if c == "Total" else cat == c
        rule = FQp[0][:, 2] if c == "Fragancias" else FQp[1][:, 2]
        if c == "Total":
            rule = np.where(cat == "Fragancias", FQp[0][:, 2], FQp[1][:, 2])
        best4 = err[:, s, 2].argmin(0)
        res[c] = dict(ean_elegido=float(np.abs(f4[s] - A4[s]).sum() / A4[s].sum()), ean_regla=float(np.abs(rule[s] - A4[s]).sum() / A4[s].sum()),
                      ean_cons=float(np.abs(cons[s] - A4[s]).sum() / A4[s].sum()),
                      acierto=float((pick[s] == best4).mean()), azar=1 / len(names),
                      **{"ean_" + p: float(np.abs(FQp[i][s, 2] - A4[s]).sum() / A4[s].sum()) for i, p in enumerate(names)})
    return res


def excel(a, names):
    cols = ["desc", "cat", "casa", "linea", "seg", "edad", "tramo", "fase", "isf", "real", "voto", "mejor", "mejor_err",
            "mejor_familia", "mejor_memoria", "mejor_estac", "mejor_fuente", "mejor_trend", "mejor_dap", "mejor_cortes", "mejor_daf"]
    x = a[cols].copy()
    for p in names + ["Consenso"]:
        x["error " + p] = np.where(a.real > 0, a["err:" + p] / a.real.where(a.real > 0, 1), np.nan)
    x = x.rename(columns=dict(desc="Descripción", cat="Categoría", casa="Casa", linea="Línea", seg="Segmento", edad="Edad (meses)", tramo="Tramo",
                              fase="Fase", isf="Bandera", real="Real oct–jun", voto="Vota a", mejor="Mejor estrategia a posteriori",
                              mejor_err="Error mejor", mejor_familia="Base", mejor_memoria="Memoria", mejor_estac="Estacionalidad",
                              mejor_fuente="Trend de", mejor_trend="Trend (fuerza·ventana·tope)", mejor_dap="DAs pasado restados",
                              mejor_cortes="Cortes sumados", mejor_daf="DAs foto sumados"))
    x.index.name = "EAN"
    out = ROOT / "reportes" / "IDEOLOGIAS_EAN.xlsx"
    with pd.ExcelWriter(out) as xw:
        x.sort_values(["Categoría", "Casa", "Real oct–jun"], ascending=[True, True, False]).to_excel(xw, sheet_name="EANs")


if __name__ == "__main__":
    main()
