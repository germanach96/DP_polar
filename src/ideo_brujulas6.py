"""Los 6 partidos y las brújulas de las 3 preguntas, con la lógica de DAs decidida (foto sep-25 → real sep-26).

DAs futuros de la foto: según la Ignore System Forecast Flag del EAN en la foto (sin flag 100%, flag 1 50%, flag 2 0%).
DAs de los meses de la base: los planificados (src/ideo_panel.da_plan); cuánto restar es ideología de cada partido.
  1 ¿De dónde parto?      x: plana ↔ con temporada · y: memoria reciente (6M) ↔ lejana (12M / año pasado)
  2 ¿A quién sigo?        x: individual (EAN, línea) ↔ colectivo (casa, categoría) · y: trend suave ↔ completo
  3 ¿Cómo limpio la base? x: deja los DAs planificados ↔ los resta · y: no suma cortes ↔ suma cortes
Partidos: los 6 de src/ideo_six_fijo.py; para los 4 nuevos se vuelve a elegir con datos (oct–mar) cuánto restan de DAs y suman de cortes.
EANs: posición por la ventaja de cada lado (tanh(ventaja / 5 puntos)) con estrategias sin 3M y DAs futuros según su flag.
Salida: work/ideo_brujulas6.json (ids y posiciones de los partidos, estadísticas) y work/ideo_brujulas6_ean.parquet"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_parties as ipp  # noqa
import ideo_viz as iv  # noqa

W = ipp.W
NAMES = ["Regla fragancias", "Regla makeup", "Ciclo de vida", "Media 6M prudente", "Media 6M estacional", "Media 12M estacional"]
KEY = ["base", "estac", "fuente", "tventana", "fuerza", "tope", "dap", "cortes", "daf", "pool"]
FLAG_DAF = {0: "1.0", 1: "0.5", 2: "0.0"}
IDENT = {"EAN": -1.0, "línea": -0.65, "franquicia": -0.35, "segmento": -0.05, "fase": 0.2, "edad": 0.35, "casa": 0.65, "categoría": 1.0}
CUTX = {"0": -1.0, "10%·tope": -0.6, "25%": 0.0, "50%": 1.0}
MEMY = {"M6": -0.6, "M6e": -0.6, "CV": -0.6, "M12": 0.4, "M12e": 0.4, "LY+M6e": 0.2, "LY": 1.0}
COL6 = {"Regla fragancias": "#6250d6", "Media 12M estacional": "#eda100", "Media 6M estacional": "#00a3c4", "Regla makeup": "#eb6834",
        "Media 6M prudente": "#2a78d6", "Ciclo de vida": "#e87ba4", "Empate": iv.EMPATE}
ORDER6 = ["Regla fragancias", "Media 12M estacional", "Media 6M estacional", "Regla makeup", "Media 6M prudente", "Ciclo de vida"]
BLOC6 = {"Regla fragancias": "Año pasado", "Media 12M estacional": "Estacional", "Media 6M estacional": "Estacional", "Regla makeup": "Nivel plano",
         "Media 6M prudente": "Nivel plano", "Ciclo de vida": "Ciclo de vida"}


class P6:
    """Orden, colores y números de los 6 partidos (paleta validada para daltonismo entre vecinos)."""

    def __init__(self):
        self.names = ORDER6; self.order = ORDER6 + ["Empate"]; self.col = COL6
        self.num = {n: i + 1 for i, n in enumerate(ORDER6)}; self.bloc = BLOC6

    def short(self, n):
        return n

    def dot(self, n, size=3, num=False):
        if num and n != "Empate":
            return f"<i class='nb' style='background:{self.col[n]}'>{self.num[n]}</i>"
        return f"<i class='dt' style='background:{self.col[n]};width:{size}mm;height:{size}mm'></i>"


def index(st):
    return {tuple(r): k for k, r in zip(st.id.values, st[KEY].astype(str).itertuples(index=False))}


def twin(st, idx, i, **ch):
    r = st.loc[i, KEY].astype(str).to_dict(); r.update({k: str(v) for k, v in ch.items()})
    return idx[tuple(r[k] for k in KEY)]


def flagged(FQ, st, idx, i, flag):
    """Forecast por quarter (EAN x 3) de la estrategia i con los DAs futuros según la flag de cada EAN."""
    tw = {f: twin(st, idx, i, daf=FLAG_DAF[f]) for f in (0, 1, 2)}
    out = np.empty(FQ.shape[1:], np.float32)
    for f, j in tw.items():
        m = flag == f
        out[m] = FQ[j][m]
    return out


def position(r):
    b = r["base"]
    seas = 1.0 if b == "LY" else (0.8 if (b.endswith("e") or b == "LY+M6e") else -0.8)
    fuente = "edad" if b == "CV" else r["fuente"]
    fe = 0.6 if b == "CV" else (2 * min(r["fuerza"] * r["tope"] / 0.6, 1) - 1)
    return dict(c1=(seas, MEMY[b]), c2=(IDENT[fuente], fe), c3=(2 * float(r["dap"]) - 1, CUTX[r["cortes"]]))


def main():
    st, FQ, Aq, a = ipp.load()
    idx = index(st); flag = a.isf.values.astype(int).clip(0, 2)
    old = json.loads((W / "ideo_six_fijo.json").read_text())["ids"]
    ids = list(old)
    r23 = Aq[:, :2].sum(1); c = np.where(r23 > 0)[0]
    w = 0.5 / len(c) + 0.5 * r23[c] / r23[c].sum()
    sc = lambda F: np.minimum(np.abs(F[c][:, :2] - Aq[c][:, :2]).sum(1) / r23[c], ipp.CAPSCORE)
    cur = np.stack([sc(flagged(FQ, st, idx, i, flag)) for i in ids])
    cx = ipp.complexity(st)
    V = {j: [twin(st, idx, old[j], dap=d, cortes=k) for d in ["0.0", "0.25", "0.5", "0.75", "1.0"] for k in ["0", "10%·tope", "25%", "50%"]] for j in range(2, 6)}
    S = {j: np.stack([sc(flagged(FQ, st, idx, i, flag)) for i in V[j]]) for j in V}
    for _ in range(10):
        ch = False
        for j in V:
            rest = np.delete(cur, j, 0).min(0)
            tot = (np.minimum(rest[None], S[j]) * w[None]).sum(1)
            near = np.where(tot <= tot.min() + ipp.SIMPLE_TOL)[0]
            k = near[np.lexsort((tot[near], cx[np.array(V[j])][near]))[0]]
            if V[j][k] != ids[j]:
                ids[j] = V[j][k]; cur[j] = S[j][k]; ch = True
        if not ch:
            break
    for nm, i in zip(NAMES, ids):
        print(f"  {nm}: {ipp.describe(st.loc[i])}".replace(" · + 100% DAs de la foto", "").replace(" · sin DAs de la foto", "") + " · DAs foto según flag")
    # posiciones de los EANs: estrategias sin 3M, DAs futuros según la flag de cada EAN
    real = Aq.sum(1); cols = np.where(real > 0)[0]
    base_rows = np.where((st.daf.values == 1.0) & ~st.base.isin(["M3", "M3e"]).values & (st.tventana.values != 3))[0]
    sub = st.iloc[base_rows]
    Sc = np.empty((len(base_rows), len(cols)), np.float32)
    for f in (0, 1, 2):
        mcol = flag[cols] == f
        if not mcol.any():
            continue
        rows_f = np.array([twin(st, idx, i, daf=FLAG_DAF[f]) for i in base_rows]) if f else base_rows
        cc = cols[mcol]
        for k in range(0, len(rows_f), 20000):
            rr = rows_f[k:k + 20000]
            Sc[k:k + 20000][:, mcol] = np.minimum(np.abs(FQ[rr][:, cc] - Aq[None, cc]).sum(2) / real[cc][None], ipp.CAPSCORE)
    b = sub.base.values; f_ = sub.fuente.values; fz = sub.fuerza.values; es = sub.estac.values
    axes = {"c1x": (np.isin(b, ["M6", "M12"]), np.isin(b, ["M6e", "M12e"]) & (es == "casa")),
            "c1y": (np.isin(b, ["M6"]) | (np.isin(b, ["M6e"]) & (es == "casa")), np.isin(b, ["M12"]) | (np.isin(b, ["M12e"]) & (es == "casa"))),
            "c2x": (np.isin(f_, ["EAN", "línea"]), np.isin(f_, ["casa", "categoría"])),
            "c2y": (((f_ == "ninguna") & (b != "CV")) | ((f_ != "ninguna") & (fz <= 0.25)), (f_ != "ninguna") & (fz >= 0.75)),
            "c3x": (sub.dap.values == 0, sub.dap.values == 1),
            "c3y": (sub.cortes.values == "0", sub.cortes.values == "50%")}
    pos = pd.DataFrame(index=a.index[cols])
    for k_, (L, R) in axes.items():
        pos[k_] = np.tanh((Sc[L].min(0) - Sc[R].min(0)) / 0.05)
    pos = pos.join(a[["real", "cat", "tramo", "isf"]])
    pos.to_parquet(W / "ideo_brujulas6_ean.parquet")
    share = lambda col, side, g=pos: float(((g[col] > 0.3) if side > 0 else (g[col] < -0.3)).mean())
    fr, mu = pos[pos.cat == "Fragancias"], pos[pos.cat == "Makeup"]
    stats = {k_: dict(der=share(k_, 1), izq=share(k_, -1), centro=float((pos[k_].abs() <= 0.3).mean()),
                      der_fr=share(k_, 1, fr), izq_fr=share(k_, -1, fr), der_mu=share(k_, 1, mu), izq_mu=share(k_, -1, mu)) for k_ in axes}
    out = dict(ids=[int(i) for i in ids], nombres=NAMES, partidos=[ipp.describe(st.loc[i]) for i in ids],
               ideas=[ipp.ideas(st.loc[i]) for i in ids], stats=stats,
               posiciones={k: {nm: position(st.loc[i])[k] for nm, i in zip(NAMES, ids)} for k in ["c1", "c2", "c3"]})
    (W / "ideo_brujulas6.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=float))
    print({k: {kk: round(v, 2) for kk, v in s.items()} for k, s in stats.items()})


if __name__ == "__main__":
    main()
