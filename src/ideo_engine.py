"""Banco de estrategias para la búsqueda de ideologías (foto sep-25, horizonte oct-25..jun-26, real = foto sep-26).

Una estrategia = base × (1 + fuerza × trend de la fuente, tope ±30%) + DAs futuros, con la base calculada sobre el
histórico ajustado (envío + cortes − DAs+ del pasado). Todo con datos anteriores a sep-25 (sep-25 en curso, fuera).

Dimensiones ("ideas") y valores:
  base       LY (mismo mes del año pasado) | M3 / M6 / M12 (media plana) | M3e / M6e / M12e (media sin temporada × perfil
             mensual de un grupo) | LY+M6e (mitad y mitad) | CV (curva de vida: nivel 6M sin temporada × cómo evolucionaron los códigos a su edad)
  estac      perfil estacional de: casa, casa×segmento, línea, categoría (solo bases e y CV; CV también "sin")
  fuente     trend de: ninguno, EAN, línea, franquicia (brand), segmento (casa × tamaño o función), casa, categoría, fase (casa × fase)
  tventana   12M, 6M o 3M (suma ventana / misma ventana del año anterior − 1, EANs Central)
  fuerza     25%, 50%, 75%, 100% del trend
  tope       ±30% (el de las reglas) o ±60% (para ver si el tope esconde diferencias entre fuentes)
  dap        % de los DAs+ del pasado que se restan a la base: 0, 25, 50, 75, 100
  cortes     0 | 10% con tope 10% del envío | 25% | 50% de los cortes del pasado sumados a la base
  daf        % de los DAs de la foto (oct–jun, positivos y negativos) que se suman: 0, 50, 100
Fallbacks (mínimo 5 EANs Central en el grupo): EAN (sin año anterior completo) -> línea -> segmento; franquicia -> casa;
fase -> categoría × fase. Perfil estacional: línea -> casa×segmento -> casa -> categoría (mínimo 5 EANs con 24 meses).
Curva de vida (edad decidida con el usuario): para un EAN de a meses, pares que en su día tuvieron a±2 meses;
multiplicador del mes h = Σ venta de los pares a la edad a+h / Σ su media de las edades a−6..a−1 (sin temporada si se pide).
Mínimo 5 pares; si no, pool más grande (casa×segmento -> casa -> categoría); si la edad a+h aún no se ha visto en nadie,
se mantiene el último multiplicador visto. Ciclo de vida completo: si no hay curva (26+ con edad desconocida, o sin pares),
manda la madurez: trend 12M de los códigos de su misma fase (casa × fase: crecimiento / estable / declive), tope ±30%.
Salida: work/ideo_bank.npz (forecast EAN × quarter de cada estrategia y real) y work/ideo_strats.parquet"""
import itertools
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_panel as ip  # noqa
import methods as mt  # noqa

warnings.filterwarnings("ignore")
W = ip.W; M = ip.M
CAPS = [0.30, 0.60]
MIN_G = 5
BASES_LVL = ["M3", "M6", "M12"]
SEAS = ["casa", "casa×seg", "línea", "categoría"]
SOURCES = ["EAN", "línea", "franquicia", "segmento", "casa", "categoría", "fase"]
TWIN = [12, 6, 3]
STRENGTH = [0.25, 0.5, 0.75, 1.0]
DAP = [0.0, 0.25, 0.5, 0.75, 1.0]
CUTS = ["0", "10%·tope", "25%", "50%"]
DAF = [0.0, 0.5, 1.0]
CURVE_POOLS = ["categoría", "casa", "casa×seg"]


class Ctx:
    def __init__(self, P):
        self.P = P; a = P["attr"]; self.a = a; self.m = m = P["m"]
        H = P["H"].copy(); H[:, m:] = np.nan
        self.Hm = H; self.H0 = np.nan_to_num(H)
        self.central = a.central.values
        self.keys = dict(casa=(a.cat + "|" + a.casa).values, seg=(a.casa + "|" + a.seg).values, linea=(a.casa + "|" + a.linea).values,
                         franq=(a.casa + "|" + a.brand).values, cat=a.cat.values, fase=(a.casa + "|" + a.fase).values,
                         catfase=(a.cat + "|" + a.fase).values)
        self.vote = a.votante.values
        self.month_of = np.array([t.month for t in M])

    # ---------- trends ----------
    def group_g(self, keys, w, min_n=MIN_G):
        g = mt._group_g(self.Hm, self.m, w, keys, self.central)
        n = pd.Series(self.central.astype(int)).groupby(keys).transform("sum").values
        return np.where((n >= min_n) & np.isfinite(g), g, np.nan)

    def trend(self, src, w):
        k = self.keys
        g_seg = np.nan_to_num(self.group_g(k["seg"], w, 0))      # como las reglas: sin mínimo de EANs
        if src == "segmento":
            return g_seg
        if src == "casa":
            return np.nan_to_num(self.group_g(k["casa"], w, 0))
        if src == "categoría":
            return np.nan_to_num(self.group_g(k["cat"], w, 0))
        if src == "línea":
            return np.where(np.isfinite(gl := self.group_g(k["linea"], w)), gl, g_seg)
        if src == "franquicia":
            gc = np.nan_to_num(self.group_g(k["casa"], w, 0))
            return np.where(np.isfinite(gf := self.group_g(k["franq"], w)), gf, gc)
        if src == "fase":
            gcf = np.nan_to_num(self.group_g(k["catfase"], w))
            return np.where(np.isfinite(gf := self.group_g(k["fase"], w)), gf, gcf)
        if src == "EAN":
            m = self.m
            rec = self.Hm[:, m - w:m]; ly = self.Hm[:, m - w - 12:m - 12]
            ok = np.isfinite(ly).all(1) & (np.nansum(ly, 1) > 0)
            ge = np.nansum(rec, 1) / np.where(ok, np.nansum(ly, 1), 1) - 1
            gl = self.trend("línea", w)
            return np.where(ok, ge, gl)
        raise ValueError(src)

    # ---------- estacionalidad ----------
    def season(self, how):
        """Índice por EAN y mes calendario (n x 13, columna = mes 1..12): perfil de los últimos 24 meses de los EANs del grupo
        con los 24 meses de historia (like-for-like), media 1."""
        m = self.m
        lfl = np.isfinite(self.Hm[:, m - 24]) & self.central
        X = self.H0[:, m - 24:m] * lfl[:, None]
        mo = self.month_of[m - 24:m]
        order = {"línea": ["linea", "seg", "casa", "cat"], "casa×seg": ["seg", "casa", "cat"], "casa": ["casa", "cat"], "categoría": ["cat"]}[how]
        out = np.full((len(X), 13), np.nan)
        for lev in order[::-1]:   # de grueso a fino: lo fino sobrescribe si tiene suficientes EANs
            keys = self.keys[lev]
            df = pd.DataFrame(X); df["k"] = keys
            G = df.groupby("k").sum()
            n = pd.Series(lfl.astype(int)).groupby(keys).sum()
            prof = np.zeros((len(G), 13))
            for mm in range(1, 13):
                prof[:, mm] = G.values[:, mo == mm].sum(1)
            tot = prof[:, 1:].sum(1, keepdims=True)
            prof = np.where(tot > 0, prof / np.where(tot > 0, tot, 1) * 12, np.nan)
            prof[:, 1:] = np.clip(prof[:, 1:], 0.2, 5)
            prof[:, 1:] = prof[:, 1:] / prof[:, 1:].mean(1, keepdims=True)
            good = (n.reindex(G.index).values >= MIN_G) & np.isfinite(prof[:, 1:]).all(1)
            P = pd.DataFrame(np.where(good[:, None], prof, np.nan), index=G.index).reindex(keys).values
            out = np.where(np.isfinite(P[:, 1:2]), P, out)
        out[:, 1:] = np.where(np.isfinite(out[:, 1:]), out[:, 1:], 1.0)
        return out

    # ---------- curva de vida ----------
    def curve(self, pool, how_seas):
        """Multiplicador n x 9 (meses m+1..m+9) sobre el nivel 6M sin temporada."""
        m = self.m; a = self.a
        L = a.launch.values; age = a.edad.values
        S = self.season(how_seas) if how_seas else None
        Y = self.H0.copy()
        if S is not None:
            idx = S[:, self.month_of[:m]]           # n x m
            Y[:, :m] = Y[:, :m] / idx
        peers = np.where(L >= 1)[0]               # lanzamiento visto en los datos
        pools = {"casa×seg": ["seg", "casa", "cat"], "casa": ["casa", "cat"], "categoría": ["cat"]}[pool]
        out = np.full((len(Y), 9), np.nan)
        cache = {}
        for i in np.where(self.vote)[0]:
            ai = age[i]
            if L[i] < 1 or ai < 6:
                continue
            for lev in pools:
                key = (lev, self.keys[lev][i], ai)
                if key in cache:
                    res = cache[key]
                else:
                    pp = peers[self.keys[lev][peers] == self.keys[lev][i]]
                    res = []
                    for h in range(1, 10):
                        num = den = 0.0; who = set()
                        for p in pp:
                            for a2 in range(max(6, ai - 2), ai + 3):
                                t = L[p] + a2 + h
                                if t > m - 1:
                                    continue
                                lvl = Y[p, L[p] + a2 - 6:L[p] + a2].mean()
                                num += Y[p, t]; den += lvl; who.add(p)
                        res.append(num / den if (len(who) >= MIN_G and den > 0) else np.nan)
                    cache[key] = res
                if np.isfinite(res[0]):
                    r = np.array(res, float)
                    for h in range(1, 9):
                        if not np.isfinite(r[h]):
                            r[h] = r[h - 1]
                    out[i] = np.clip(r, 0.2, 5)
                    break
        # madurez: sin curva (26+ / edad desconocida o sin pares) -> trend 12M de los códigos en su misma fase (casa × fase, tope ±30%)
        gf = np.clip(self.trend("fase", 12), -0.3, 0.3)
        nocurve = ~np.isfinite(out[:, 0])
        out[nocurve] = (1 + gf[nocurve])[:, None]
        return out


def adjusted(ctx, dap, cut):
    P = ctx.P; m = ctx.m; H = ctx.Hm
    C = P["C"]; D = P["DAp"]
    if cut == "0":
        ca = 0
    elif cut == "10%·tope":
        ca = np.minimum(0.10 * C, 0.10 * np.nan_to_num(H))
    else:
        ca = float(cut.rstrip("%")) / 100 * C
    X = np.clip(np.nan_to_num(H) + ca - dap * D, 0, None)
    X[:, m:] = 0
    # LY usa también los cortes de antes del lanzamiento (como la regla de fragancias); las medias, solo meses con historia
    return X, np.where(np.isfinite(H), X, np.nan)


def base_matrix(ctx, XX, base, S=None, CV=None):
    m = ctx.m; fut = range(m + 1, m + 10)
    X0, X = XX
    if base == "LY":
        return np.stack([X0[:, j - 12] for j in fut], 1)
    if base == "LY+M6e":
        return 0.5 * base_matrix(ctx, XX, "LY") + 0.5 * base_matrix(ctx, XX, "M6e", S)
    w = 6 if base == "CV" else int(base[1:].rstrip("e"))
    win = X[:, m - w:m]
    if base.endswith("e") or base == "CV":
        idx = S[:, ctx.month_of[m - win.shape[1]:m]] if S is not None else 1.0
        lvl = np.nan_to_num(np.nanmean(win / idx, 1))
        tgt = S[:, ctx.month_of[m + 1:m + 10]] if S is not None else np.ones((len(X), 9))
        mult = CV if CV is not None else 1.0
        return lvl[:, None] * tgt * mult
    lvl = np.nan_to_num(np.nanmean(win, 1))
    return np.repeat(lvl[:, None], 9, 1)


TRENDS = [("ninguna", 0, 0.0, 0.0)] + [(s, w, f, c) for c in CAPS for s in SOURCES for w in TWIN for f in STRENGTH]


def strategies():
    rows = []
    cores = [("LY", None)] + [(b, None) for b in BASES_LVL] + [(b + "e", s) for b in BASES_LVL for s in SEAS] + [("LY+M6e", s) for s in SEAS]
    for dap, cut, daf in itertools.product(DAP, CUTS, DAF):
        for b, s in cores:
            for src, w, f, cap in TRENDS:
                rows.append(dict(base=b, estac=s or "sin", fuente=src, tventana=w, fuerza=f, tope=cap, dap=dap, cortes=cut, daf=daf, pool="—"))
        for pool in CURVE_POOLS:
            for s in [None, "casa"]:
                rows.append(dict(base="CV", estac=s or "sin", fuente="ninguna", tventana=0, fuerza=0.0, tope=0.0, dap=dap, cortes=cut, daf=daf, pool=pool))
    st = pd.DataFrame(rows)
    st["id"] = np.arange(len(st))
    return st


def run():
    t0 = time.time()
    P = pd.read_pickle(W / "ideo_panel.pkl"); ctx = Ctx(P)
    st = strategies()
    v = np.where(ctx.vote)[0]; nv = len(v)
    A = P["A"][v]; Aq = np.stack([A[:, ix].sum(1) for ix in ip.QIDX], 1).astype(np.float32)
    DAf = P["DAf"][v].astype(np.float32)
    houses = sorted(set(P["attr"].casa.values[v]))
    S = {s: ctx.season(s) for s in SEAS}
    G = {(s, w): ctx.trend(s, w) for s in SOURCES for w in TWIN}
    CVm = {(p, s): ctx.curve(p, s) for p in CURVE_POOLS for s in [None, "casa"]}
    print(f"preparación {time.time() - t0:.0f}s")
    FQ = np.zeros((len(st), nv, 3), np.float32)      # forecast por quarter
    key = {tuple(r): i for i, r in zip(st.id, st[["base", "estac", "fuente", "tventana", "fuerza", "tope", "dap", "cortes", "daf", "pool"]].itertuples(index=False))}
    qmat = np.zeros((9, 3), np.float32)
    for q, ix in enumerate(ip.QIDX):
        qmat[ix, q] = 1
    trends = TRENDS
    MULT = np.stack([np.ones(len(ctx.a))] + [1 + f * np.clip(G[(s, w)], -c, c) for s, w, f, c in trends[1:]], 0)[:, v].astype(np.float32)
    for dap, cut in itertools.product(DAP, CUTS):
        X = adjusted(ctx, dap, cut)
        cores = [("LY", None, None, "—")] + [(b, None, None, "—") for b in BASES_LVL] + [(b + "e", s, None, "—") for b in BASES_LVL for s in SEAS]
        cores += [("LY+M6e", s, None, "—") for s in SEAS]
        cores += [("CV", s, p, p) for p in CURVE_POOLS for s in [None, "casa"]]
        for b, s, pool, plab in cores:
            Sm = S[s] if s else None
            B = base_matrix(ctx, X, b, Sm, CVm[(pool, s)] if b == "CV" else None)[v].astype(np.float32)
            mults = MULT if b != "CV" else MULT[:1]
            tl = trends if b != "CV" else trends[:1]
            F0 = B[None] * mults[:, :, None]                     # T x n x 9
            for daf in DAF:
                F = np.clip(F0 + daf * DAf[None], 0, None)
                Fq = F @ qmat                                     # T x n x 3
                for k, (src, w, f, c) in enumerate(tl):
                    FQ[key[(b, s or "sin", src, w, f, c, dap, cut, daf, plab)]] = Fq[k]
        print(f"dap={dap} cortes={cut} {time.time() - t0:.0f}s")
    np.save(W / "ideo_fq.npy", FQ)
    np.savez(W / "ideo_bank.npz", Aq=Aq, voters=np.array(P["attr"].index[v], dtype=str), houses=np.array(houses, dtype=str))
    st.to_parquet(W / "ideo_strats.parquet")
    pd.to_pickle(dict(G={f"{s}|{w}": G[(s, w)] for s, w in G}, S=S, CV={f"{p}|{s}": CVm[(p, s)] for p, s in CVm}), W / "ideo_aux.pkl")
    print(f"{len(st)} estrategias x {nv} EANs listo en {time.time() - t0:.0f}s")


if __name__ == "__main__":
    run()
