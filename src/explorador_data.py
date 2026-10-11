"""Datos del explorador del parlamento (src/explorador_html.py): la misma regla del parlamento, un año más tarde.

- Voto con FY26: fotos sep-25, dic-25 y mar-26 → 6 urnas (quarters de FY26 cerrados antes de sep-26), mismo formato fijo (fy25_eleccion.choose).
  Las fotos sep-25 y mar-26 se usan tal cual (DAs y bandera); makeup no tiene foto dic-25: ahí su urna va sin DAs futuros.
- Proyección: foto sep-26 tal cual → oct-26..jun-27 de los 6 partidos (DAs futuros según la bandera), el elegido y la coalición.
  Sin FY26 (nuevos): lo que votaron sus parecidos.
- Brújulas con FY26: misma lógica que fy25_brujulas, foto sep-25 → real oct-25..jun-26; ya hay DAs, así que el eje de DAs (restar 0% o 50%) sí se mide.
- Por EAN: atributos, historia mensual de envíos (jul-22..ago-26; sep-26 no está cerrado) y EPOS (desde jul-24 hasta el último mes con datos).
Salida: work/explorador.json"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import fy25_eleccion as fe  # noqa
import ideo_engine as ie  # noqa
import ideo_panel as ip  # noqa
import ideo_parties as ipp  # noqa
import mu_backtest as mb  # noqa
import six_multi as sm  # noqa

W = ip.W
FOTO, VOTO, KNOWN = "2026-09", ["2025-09", "2025-12", "2026-03"], "2026-08-01"
N = sm.NAMES_UNO


def brujulas(sp_snap="2025-09"):
    """Posición de cada EAN en las 3 brújulas con lo que vio en FY26 (foto sep-25 → real oct-25..jun-26)."""
    P = ip.build(sp_snap, save=False); ctx = ie.Ctx(P); a = P["attr"]
    v = np.where(ctx.vote)[0]
    A = P["A"][v]; Aq = np.stack([A[:, ix].sum(1) for ix in P["qidx"]], 1); real = Aq.sum(1)
    flag = a.isf.values[v].astype(int).clip(0, 2)
    DAfq = np.stack([(np.array([sm.FLAGW[f] for f in flag])[:, None] * P["DAf"][v])[:, ix].sum(1) for ix in P["qidx"]], 1)
    qmat = np.zeros((9, 3))
    for q, ix in enumerate(P["qidx"]):
        qmat[ix, q] = 1
    seas = {s: ctx.season(s) for s in ie.SEAS}
    CV = {(p, s): ctx.curve(p, s) for p in ie.CURVE_POOLS for s in [None, "casa"]}
    trends = [t for t in ie.TRENDS if t[1] != 3]                     # vetado: 3 meses
    G = {(s, w): ctx.trend(s, w) for s, w, _, _ in trends[1:]}
    MULT = np.stack([np.ones(len(a))] + [1 + f * np.clip(G[(s, w)], -c, c) for s, w, f, c in trends[1:]], 0)[:, v]
    rows, scores = [], []
    for dap in [0.0, 0.5]:
        for cut in ie.CUTS:
            X = ie.adjusted(ctx, dap, cut)
            cores = [("LY", None, None)] + [(b, None, None) for b in ["M6", "M12"]] + [(b + "e", s, None) for b in ["M6", "M12"] for s in ie.SEAS]
            cores += [("LY+M6e", s, None) for s in ie.SEAS] + [("CV", s, p) for p in ie.CURVE_POOLS for s in [None, "casa"]]
            for b, s, pool in cores:
                B = ie.base_matrix(ctx, X, b, seas[s] if s else None, CV[(pool, s)] if b == "CV" else None)[v]
                tl = trends if b != "CV" else trends[:1]
                Fq = np.clip(B[None] * MULT[:len(tl), :, None], 0, None) @ qmat + DAfq[None]
                scores.append(np.minimum(np.abs(Fq - Aq[None]).sum(2) / np.where(real > 0, real, 1)[None], ipp.CAPSCORE))
                rows += [dict(base=b, estac=s or "sin", fuente=src, fuerza=f, cortes=cut, dap=dap) for src, w, f, c in tl]
    Sc = np.concatenate(scores); st = pd.DataFrame(rows)
    b = st.base.values; f_ = st.fuente.values; fz = st.fuerza.values; es = st.estac.values
    axes = {"c1x": (np.isin(b, ["M6", "M12"]), np.isin(b, ["M6e", "M12e"]) & (es == "casa")),
            "c1y": (np.isin(b, ["M6"]) | (np.isin(b, ["M6e"]) & (es == "casa")), np.isin(b, ["M12"]) | (np.isin(b, ["M12e"]) & (es == "casa"))),
            "c2x": (np.isin(f_, ["EAN", "línea"]), np.isin(f_, ["casa", "categoría"])),
            "c2y": (((f_ == "ninguna") & (b != "CV")) | ((f_ != "ninguna") & (fz <= 0.25)), (f_ != "ninguna") & (fz >= 0.75)),
            "c3x": (st.dap.values == 0.0, st.dap.values == 0.5),
            "c3y": (st.cortes.values == "0", st.cortes.values == "50%")}
    ok = real > 0
    pos = pd.DataFrame(index=a.index[v][ok])
    for k, (L, R) in axes.items():
        pos[k] = np.tanh((Sc[L][:, ok].min(0) - Sc[R][:, ok].min(0)) / 0.05)
    stats = {k: dict(der=float((pos[k] > 0.3).mean()), izq=float((pos[k] < -0.3).mean()), centro=float((pos[k].abs() <= 0.3).mean())) for k in axes}
    print("brújulas FY26:", len(pos), "EANs ·", len(st), "estrategias")
    return pos, stats


def main():
    sp = sm.specs()
    Btr = pd.concat([fe.ballots(f, sp, hasta=KNOWN) for f in VOTO], ignore_index=True)
    Bte = fe.ballots(FOTO, sp)
    B, voto, Bv, partido = fe.choose(Btr, Bte)
    E = B.drop_duplicates("ean").set_index("ean")
    Wq = np.stack([sm.wq(Btr["F:" + n].values, Btr.real.values) for n in N], 1)
    err = pd.DataFrame(np.minimum(Wq, 2), columns=N); err["ean"] = Btr.ean.values
    e_ean = err.groupby("ean")[N].mean()                                  # error medio FY26 por partido (tope 200%)
    # foto sep-26: forecast mensual de los 6 partidos con DAs futuros según la bandera
    P = ip.build(FOTO, save=False); a = P["attr"]; m = P["m"]
    F0 = sm.forecasts(P, sp)
    wf = np.array([sm.FLAGW[f] for f in a.isf.values.astype(int).clip(0, 2)])[:, None]
    F = np.clip(F0 + wf[None] * P["DAf"][None], 0, None)
    H = P["H"][:, :m]                                                     # jul-22..ago-26
    months = [t.strftime("%Y-%m") for t in ip.M[:m]]; fmonths = [t.strftime("%Y-%m") for t in P["months"]]
    # EPOS (sell-out) desde jul-24
    ep0 = list(ip.M).index(pd.Timestamp("2024-07-01"))
    Ef = pd.read_pickle(W / "epos.pkl")
    Ef.columns = pd.DatetimeIndex(Ef.columns)
    Em = mb.load()[2]
    EP = pd.concat([Ef, Em]); EP.index = EP.index.astype(str)
    EP = EP[~EP.index.duplicated()].reindex(index=a.index, columns=ip.M[ep0:m])
    EP = EP.loc[:, :EP.columns[EP.fillna(0).sum().values > 0][-1]]      # el EPOS llega un mes más tarde: hasta el último mes con datos
    pos, stats = brujulas()
    Bj = json.loads((W / "ideo_brujulas6.json").read_text())
    fixed = {k: {n: [round(p * .86, 3) for p in Bj["posiciones"][k][n]] for n in N} for k in ["c1", "c2", "c3"]}
    for k, xy in {"c1": (0.0, -0.6), "c2": (0.35, 0.6), "c3": (-1.0, -1.0)}.items():   # mismos ajustes que ideologia_report
        fixed[k]["Ciclo de vida"] = [round(xy[0] * .86, 3), round(xy[1] * .86, 3)]
    parl = set(E.index)
    keep = a.central.values | a.index.isin(parl)                          # Central (cuentan para los trends de grupo) + parlamento
    r = lambda x: None if not np.isfinite(x) else round(float(x), 1)
    rows = []
    for i in np.where(keep)[0]:
        e = a.index[i]; x = a.iloc[i]
        row = dict(id=e, d=x.desc, c=x["cat"], h=x.casa, b=x.brand, l=x.linea, s=x.seg, t=x.tramo, f=x.fase, age=int(x.edad), isf=int(x.isf),
                   cen=bool(x.central), hist=[r(v) for v in H[i]], epos=[r(v) for v in EP.iloc[i].values])
        if e in parl:
            row.update(p=1, v=partido.get(e, "Empate"), vp=E.loc[e, "partido"], c1=E.loc[e, "coal1"], c2=E.loc[e, "coal2"],
                       hi=int(E.loc[e, "historia"] == fe.HIST[0]), lv=E.loc[e, "nivel"],
                       fc=[[r(v) for v in F[k][i]] for k in range(len(N))],
                       err=[r(v * 100) for v in e_ean.loc[e].values] if e in e_ean.index else None,
                       pos=[round(float(pos.loc[e, k]), 3) for k in ["c1x", "c1y", "c2x", "c2y", "c3x", "c3y"]] if e in pos.index else None)
        rows.append(row)
    out = dict(foto=FOTO, months=months, fmonths=fmonths, epos_from=ip.M[ep0].strftime("%Y-%m"), epos_to=EP.columns[-1].strftime("%Y-%m"), parties=N, markers=fixed, stats=stats,
               n_parl=len(parl), n_votantes=int(len(voto)), eans=rows)
    (W / "explorador.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":"), default=float))
    seats = pd.Series({e: partido.get(e, "Empate") for e in parl}).value_counts()
    print(f"{len(rows)} EANs ({len(parl)} en el parlamento, {len(voto)} votan con FY26)"); print(seats.to_string())
    print("con brújula:", int(sum(1 for x in rows if x.get("pos"))), "· con EPOS:", int(sum(1 for x in rows if any(v for v in x["epos"] if v))))


if __name__ == "__main__":
    main()
