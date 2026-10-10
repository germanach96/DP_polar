"""Parlamento de 6 con juego fijo de partidos (la primera selección limpia sin 3M) y la curva de vida corregida (solo <18 meses).
Evalúa abr–jun con voto por su pasado y con influencia de similares (alpha). Salida: work/ideo_six_fijo.json"""
import sys, json, numpy as np, pandas as pd
from pathlib import Path; sys.path.insert(0, str(Path(__file__).parent))
import ideo_parties as ipp, ideo_vs_cons as ivc, ideo_six as s6
st, FQ, Aq, a = ipp.load(); cons = np.stack(a.cons_q.values); cat = a.cat.values; n = np.arange(len(a))
rf, rm = ipp.fixed_ids(st)
def fid(**kw): return ipp.find(st, **kw)
old = [rf, rm,
 fid(base='CV', estac='sin', fuente='ninguna', tventana=0, fuerza=0.0, tope=0.0, dap=1.0, cortes='0', daf=0.0, pool='casa×seg'),
 fid(base='M6', estac='sin', fuente='categoría', tventana=6, fuerza=1.0, tope=0.6, dap=0.0, cortes='0', daf=0.0),
 fid(base='M6e', estac='casa', fuente='fase', tventana=12, fuerza=1.0, tope=0.6, dap=0.0, cortes='25%', daf=0.0),
 fid(base='M12e', estac='línea', fuente='EAN', tventana=12, fuerza=0.5, tope=0.3, dap=0.0, cortes='25%', daf=0.0)]
P = FQ[old]
v = ivc.vote(P, Aq, [0, 1]); v = np.where(v < 0, np.where(cat == 'Fragancias', 0, 1), v)
r = s6.evaluate(a, P[v, n], Aq, cons, 2)
print('mismos 6 partidos, curva corregida:', {k: round(x, 3) for k, x in r.items()})
for t in s6.TRAMOS:
    m = a.tramo.values == t
    print(t, round(s6.evaluate(a, P[v, n], Aq, cons, 2, m)['ean'], 3), 'ciclo solo:', round(float(np.abs(P[2][m, 2] - Aq[m, 2]).sum() / Aq[m, 2].sum()), 3),
          'sesgo ciclo', round(float(P[2][m, 2].sum() / Aq[m, 2].sum() - 1), 2), 'votan ciclo', int((v[m] == 2).sum()))
S_own = s6.scores(P, Aq, [0, 1]); groups = s6.peer_groups(a)
best4 = np.abs(P[:, :, 2] - Aq[None, :, 2]).argmin(0)
rows = []
for g, gr in groups.items():
    for al in s6.ALPHAS:
        vv = s6.choose(S_own, gr, al)
        row = dict(sim=g, alpha=al, acierto=round(float((vv == best4).mean()), 3), **{k: round(x, 3) for k, x in s6.evaluate(a, P[vv, n], Aq, cons, 2).items()})
        for t in s6.TRAMOS:
            row[t] = round(s6.evaluate(a, P[vv, n], Aq, cons, 2, a.tramo.values == t)['ean'], 3)
        rows.append(row)
row = dict(sim='formato fijo', alpha=1, acierto=round(float((v == best4).mean()), 3), **{k: round(x, 3) for k, x in r.items()})
for t in s6.TRAMOS: row[t] = round(s6.evaluate(a, P[v, n], Aq, cons, 2, a.tramo.values == t)['ean'], 3)
rows.insert(0, row)
# sin ventas en oct-mar: ¿qué pasa con ellos?
nos = Aq[:, :2].sum(1) == 0
print('sin ventas oct–mar', nos.sum(), 'real Q4', Aq[nos, 2].sum(), 'tramos', pd.Series(a.tramo.values[nos]).value_counts().to_dict())
pd.set_option('display.width', 220); print(pd.DataFrame(rows).to_string(index=False))
json.dump(dict(ids=[int(i) for i in old], partidos=[ipp.describe(st.loc[i]) for i in old], tabla=rows), open(str(ipp.W / 'ideo_six_fijo.json'), 'w'), ensure_ascii=False, indent=1)
