"""Panel único fragancias + makeup para la búsqueda de ideologías (foto sep-25 contra la verdad de la foto sep-26).

Por EAN (todos los EANs de la foto sep-25; los votantes se filtran después):
  H    histórico de la última foto (sep-26), NaN antes del primer envío; solo se usan columnas < sep-25
  C    cortes de la última foto
  DAp  DAs+ planificados de los meses pasados (src: da_plan): el de la última foto en la que el mes aún no estaba cerrado;
       antes de la primera foto (sep-25), el que guarda esa foto como pasado      -> para limpiar la base
  DAf  DAs de la foto sep-25 en oct-25..jun-26 (positivos y negativos) -> se suman al forecast
  cons consenso de la foto sep-25 tal cual en oct-25..jun-26
  A    real oct-25..jun-26 (foto sep-26)
Atributos: categoría, casa, franquicia (brand), línea, segmento (tamaño en fragancias, función en makeup), isf, edad, fase.

Edad (decidido con el usuario): meses desde el lanzamiento hasta sep-25. Lanzamiento = primer mes de dos meses seguidos con envío.
Si ese mes es jul-22 (inicio de los datos, extendidos con el LY) la edad real es desconocida: tramo 26+.
Tramos: 6–11, 12–17, 18–25, 26+ meses.
Fase (madurez): crecimiento / estable / declive según el trend 6M propio frente al año anterior, relativo al de su casa (±15%):
  el mercado cayó un 36–51% en mar–ago 25, así que en absoluto casi todo saldría "declive". Solo con 18+ meses;
con menos de 18 meses la fase es la de su tramo de edad (lanzamiento o consolidación).
build(snap) sirve para cualquier foto (2025-09, 2025-12, 2026-03, 2026-06; makeup solo 2025-09 y 2026-03).
Salida: work/ideo_panel.pkl (sep-25) o work/ideo_panel_<foto>.pkl"""
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import house_compare as hc  # noqa
import da_test as dt  # noqa
import mu_backtest as mb  # noqa
from ptype import add_types  # noqa
from wape90 import cons_da, fq  # noqa

warnings.filterwarnings("ignore")
W = hc.W
# Histórico extendido un año hacia atrás (jul-22..jun-23) con "Consensus - Final LY M" de la foto sep-26: el LY de cada mes coincide
# al 100% con el histórico del año anterior (comprobado en fragancias y makeup). Permite una foto simulada en sep-24 (voto con FY25).
M = pd.date_range("2022-07-01", "2027-06-01", freq="MS")
EXT = M[:12]
SNAP = "2025-09"
VOTE_SNAP = "2024-09"                                 # foto simulada: solo histórico (no hay DAs, consenso ni bandera de esa fecha)
V = pd.Timestamp(SNAP + "-01"); m = M.get_loc(V); MONTHS = list(M[m + 1:m + 10])
QS = [fq(t) for t in MONTHS]
QLIST = list(dict.fromkeys(QS))                      # FY26.Q2, FY26.Q3, FY26.Q4
QIDX = [[i for i, q in enumerate(QS) if q == x] for x in QLIST]
FRAG = {"BURBERRY": "Burberry", "Gucci": "Gucci", "CP-Marc Jacobs": "Marc Jacobs"}
MU = {"GUMU": "Gucci Make up", "KYMU": "Kylie Makeup"}
SIZE = {"mini(<=15ml/penspray)": "Mini ≤15", "pequeño(20-40)": "Pequeño 20–40", "medio(45-60)": "Medio 45–60", "grande(75-125)": "Grande 75–125",
        "refill/jumbo(>=150)": "Jumbo/refill ≥150", "ancilar(deo/BL/SG)": "Ancilares", "sin_tamaño": "Sin tamaño"}
AGEB = ["6–11", "12–17", "18–25", "26+"]
PHASE_CUT = 0.15


def mu_function(brand):
    """Función de makeup a partir del brand (Gucci Lips / Lips -> Lips); el resto se queda con su nombre."""
    b = str(brand)
    for k in ["Lips", "Face", "Eyes"]:
        if k in b:
            return k
    return b.split(" (")[0]


def launch_idx(H):
    """Primer mes de dos meses seguidos con envío (>0). -1 si nunca."""
    X = np.nan_to_num(H) > 0
    two = X[:, :-1] & X[:, 1:]
    out = np.where(two.any(1), two.argmax(1), -1)
    return out


VERS_F = ["2025-09", "2025-12", "2026-03", "2026-06", "2026-09"]
VERS_M = ["2025-09", "2026-03", "2026-09"]


def extend(H, v, eans):
    """H (EAN x meses desde jul-23) -> EAN x M, con jul-22..jun-23 tomado del LY de jul-23..jun-24 (foto v = sep-26). NaN antes de la primera venta."""
    ly = v.pivot_table(index="ean", columns="date", values="cons_ly", aggfunc="sum").reindex(index=eans, columns=EXT + pd.DateOffset(years=1))
    ly.columns = EXT
    X = H.reindex(index=eans, columns=M)
    X[EXT] = ly.values
    last = M <= hc.LAST
    f = X.fillna(0).where(pd.DataFrame(np.broadcast_to(last, X.shape), index=X.index, columns=M))
    started = f.fillna(0).cumsum(axis=1) > 0
    return f.where(started)


def da_plan(d, eans, V, vers):
    """DA planificado de cada mes (EAN x M) visto desde la foto V: el de la última foto W <= V en la que el mes todavía no estaba
    cerrado (W <= mes). Meses anteriores a la primera foto: el que registra la primera foto (o9 los guarda como pasado).
    Devuelve (DA, fuente) con fuente = foto usada por mes (str) para auditar."""
    vs = [v for v in vers if pd.Timestamp(v + "-01") <= V]
    if not vs:                                       # antes de la primera foto con DAs (foto simulada sep-24): sin DAs
        return pd.DataFrame(0.0, index=eans, columns=M), pd.Series("", index=M)
    piv = {v: d[d.version == v].pivot_table(index="ean", columns="date", values="da", aggfunc="sum").reindex(index=eans, columns=M).fillna(0)
           for v in vs}
    out = pd.DataFrame(0.0, index=eans, columns=M); src = pd.Series("", index=M)
    for t in M:
        if t > V:
            continue
        cand = [v for v in vs if pd.Timestamp(v + "-01") <= t]
        w = cand[-1] if cand else vs[0]
        out[t] = piv[w][t].values; src[t] = w
    return out, src


def build(snap=SNAP, save=True):
    V = pd.Timestamp(snap + "-01"); m = M.get_loc(V); MONTHS = list(M[m + 1:m + 10])
    QS = [fq(t) for t in MONTHS]
    QLIST = list(dict.fromkeys(QS)); QIDX = [[i for i, q in enumerate(QS) if q == x] for x in QLIST]
    SNAP_ = snap
    # fragancias
    d = pd.read_parquet(W / "data.parquet")
    Hf = pd.read_pickle(W / "hist.pkl")
    Hf = extend(Hf, d[d.version == "2026-09"], Hf.index)
    Cf = pd.read_pickle(W / "cuts.pkl").reindex(index=Hf.index, columns=M).fillna(0)
    a = add_types(pd.read_pickle(W / "attr.pkl")).reindex(Hf.index)
    x = d[d.version == SNAP_]
    keep = a.house.isin(FRAG).values             # todos: los que no están en la foto también cuentan para trends de grupo
    Hf, Cf, a = Hf[keep], Cf[keep], a[keep]
    DAf_all = da_plan(d, Hf.index, V, VERS_F)[0]
    Cn, Da = cons_da(x, V, Hf.index, MONTHS)
    isf = x.groupby("ean").isf.max().reindex(Hf.index).fillna(0).values
    fr = pd.DataFrame(dict(cat="Fragancias", casa=a.house.map(FRAG).values, brand=a.brand.astype(str).values,
                           linea=a.pline.astype(str).values, seg=a.ptype.map(SIZE).fillna("Sin tamaño").values,
                           desc=a.desc.astype(str).values, isf=isf, foto=Hf.index.isin(set(x.ean))), index=Hf.index)
    parts = [(fr, Hf.values, Cf.values, np.clip(np.nan_to_num(DAf_all.values), 0, None), Da, Cn)]
    # makeup
    dm, Hdf, Edf, Cdf, attr, fac = mb.load()
    xm = dm[dm.version == SNAP_]
    keep = attr.fam.isin(MU).values
    Hm, Cm, at = Hdf[keep], Cdf[keep].reindex(columns=M).fillna(0), attr[keep]
    Hm = extend(Hm, dm[dm.version == "2026-09"], Hm.index)
    DAm = np.clip(np.nan_to_num(da_plan(dm, Hm.index, V, VERS_M)[0].values), 0, None)
    Cnm, Dam = cons_da(xm, V, Hm.index, MONTHS)
    isfm = xm.groupby("ean").isf.max().reindex(Hm.index).fillna(0).values
    desc = dm.groupby("ean").desc.last().reindex(Hm.index).astype(str).values
    mu = pd.DataFrame(dict(cat="Makeup", casa=at.fam.map(MU).values, brand=at.brand.astype(str).values,
                           linea=at.pline.astype(str).values, seg=[mu_function(b) for b in at.brand], desc=desc, isf=isfm,
                           foto=Hm.index.isin(set(xm.ean))), index=Hm.index)
    parts.append((mu, Hm.values, Cm.values, DAm, Dam, Cnm))
    attr = pd.concat([p[0] for p in parts])
    attr.index = attr.index.astype(str)
    H = np.vstack([p[1] for p in parts]).astype(float)
    C = np.vstack([p[2] for p in parts]).astype(float)
    DAp = np.vstack([p[3] for p in parts]).astype(float)
    DAp[:, m:] = 0                                   # solo DAs del pasado para limpiar la base
    DAf = np.vstack([p[4] for p in parts]).astype(float)
    cons = np.vstack([p[5] for p in parts]).astype(float)
    A = np.nan_to_num(H[:, m + 1:m + 10])
    Hm_ = H.copy(); Hm_[:, m:] = np.nan             # lo que se sabía en sep-25 (sep-25 en curso, fuera)
    central, alive = hc.central_mask(Hm_, m)
    L = launch_idx(Hm_)
    age = np.where(L >= 0, m - L, -1)
    censored = L == 0
    ageb = np.where(age < 12, AGEB[0], np.where(age < 18, AGEB[1], np.where((age < 26) & ~censored, AGEB[2], AGEB[3])))
    # fase: trend 6M propio (suma 6M / mismos 6M del año anterior) frente al de su casa (EANs Central), solo 18+ meses
    H0 = np.nan_to_num(Hm_)
    rec = H0[:, m - 6:m].sum(1); ly = H0[:, m - 18:m - 12].sum(1)
    cs = pd.DataFrame(dict(r=rec * central, l=ly * central, k=attr.casa.values)).groupby("k").sum()
    gc = (cs.r / cs.l).reindex(attr.casa.values).values
    g6 = np.where(ly > 0, rec / np.where(ly > 0, ly, 1) / gc - 1, np.nan)
    phase = np.where(age < 12, "Lanzamiento", np.where(age < 18, "Consolidación",
                     np.where(~np.isfinite(g6), "Estable", np.where(g6 > PHASE_CUT, "Crecimiento", np.where(g6 < -PHASE_CUT, "Declive", "Estable")))))
    attr["edad"] = age; attr["tramo"] = ageb; attr["fase"] = phase; attr["g6"] = g6
    attr["central"] = central; attr["launch"] = L
    act = (A.sum(1) > 0) | (H0[:, m - 6:m].sum(1) > 0)
    if snap not in VERS_F:                           # foto simulada: votan todos los Central con actividad
        attr["foto"] = True
    attr["votante"] = attr.foto & central & act
    attr["real"] = A.sum(1)
    for k, ix in zip(QLIST, QIDX):
        attr["real_" + k] = A[:, ix].sum(1)
    valid = np.array([t <= hc.LAST for t in MONTHS])
    P = dict(attr=attr, H=H, C=C, DAp=DAp, DAf=DAf, cons=cons, A=A, m=m, snap=snap, months=MONTHS, qlist=QLIST, qidx=QIDX, valid=valid)
    if save:
        pd.to_pickle(P, W / ("ideo_panel.pkl" if snap == SNAP else f"ideo_panel_{snap}.pkl"))
    return P


if __name__ == "__main__":
    P = build(); a = P["attr"]
    v = a[a.votante]
    print("EANs:", len(a), "| en la foto:", int(a.foto.sum()), "| votantes (Central con actividad):", len(v))
    print(pd.crosstab(v.casa, v.tramo, margins=True))
    print(pd.crosstab(v.cat, v.fase, margins=True))
    print(v.groupby("cat").real.sum())
