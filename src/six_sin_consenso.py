"""Prueba honesta sin consenso (el consenso es la salida de o9 que se quiere sustituir): formas de usar los 6 partidos.
El EAN elige con oct–mar (Q2+Q3) y se mide abr–jun (Q4) en las fotos sep-25 (7–9 meses), dic-25 (4–6) y mar-26 (1–3).
Opciones: regla de su categoría, voto del EAN, voto del grupo (casa × tamaño/función × edad), media de los 6, media de sus 2 mejores (coalición)."""
import sys, numpy as np, pandas as pd
from pathlib import Path; sys.path.insert(0, str(Path(__file__).parent))
import six_multi as sm
B = pd.read_parquet(str(Path(__file__).resolve().parents[1] / 'work' / 'six_multi.parquet'))
N = sm.NAMES; F = lambda x: np.stack([x['F:' + n].values for n in N], 1)
tr = B[B.q.isin(['FY26.Q2', 'FY26.Q3'])].copy()
# error por EAN y partido en oct–mar (para top-2 y grupos)
Wq = np.stack([sm.wq(tr['F:' + n].values, tr.real.values) for n in N], 1)
err = pd.DataFrame(np.minimum(Wq, 2), columns=N); err['ean'] = tr.ean.values
for c in ['casa', 'seg', 'tramo', 'cat']: err[c] = tr[c].values
e_ean = err.groupby('ean')[N].mean()
voto, _ = sm.elect(tr)
grp = err.groupby(['casa', 'seg', 'tramo'])[N].mean(); grp_pick = grp.idxmin(1)
cat_pick = err.groupby('cat')[N].mean().idxmin(1)
rows = []
for f, lg in [('2025-09', '7–9'), ('2025-12', '4–6'), ('2026-03', '1–3')]:
    x = B[(B.foto == f) & (B.q == 'FY26.Q4')].copy(); R = x.real.sum(); FF = F(x); n = np.arange(len(x))
    res = {}
    ev = lambda f_: float(np.abs(f_ - x.real.values).sum() / R)
    res['Regla de su categoría'] = ev(np.where(x.cat == 'Fragancias', x['F:Regla fragancias'], x['F:Regla makeup']))
    p, _ = sm.apply_vote(x, voto); res['Parlamento (voto del EAN)'] = ev(p)
    g = [grp_pick.get((c, s, t), cat_pick[k]) for c, s, t, k in zip(x.casa, x.seg, x.tramo, x.cat)]
    res['Voto del grupo (casa×tamaño/función×edad)'] = ev(FF[n, [N.index(z) for z in g]])
    res['Media de los 6 partidos'] = ev(FF.mean(1))
    top = e_ean.reindex(x.ean).values
    o = np.argsort(np.where(np.isfinite(top), top, 1.0), 1)[:, :2]
    res['Media de sus 2 mejores'] = ev(np.take_along_axis(FF, o, 1).mean(1))
    for k_, nm in enumerate(N): res['Solo ' + nm] = ev(FF[:, k_])
    rows.append(pd.Series(res, name=f'{lg} meses (foto {f})'))
T = pd.DataFrame(rows).T
pd.set_option('display.width', 200); print((T * 100).round(0).to_string())
# WAPE90 por casa (ponderado) para las opciones principales
print()
for f, lg in [('2025-09', '7–9'), ('2025-12', '4–6'), ('2026-03', '1–3')]:
    x = B[(B.foto == f) & (B.q == 'FY26.Q4')].copy(); FF = F(x); n = np.arange(len(x))
    p, _ = sm.apply_vote(x, voto)
    top = e_ean.reindex(x.ean).values; o = np.argsort(np.where(np.isfinite(top), top, 1.0), 1)[:, :2]
    opts = {'regla': np.where(x.cat == 'Fragancias', x['F:Regla fragancias'], x['F:Regla makeup']), 'parlamento': p,
            'coalición 2': np.take_along_axis(FF, o, 1).mean(1), 'media 6': FF.mean(1)}
    out = []
    for k, v in opts.items():
        x['_f'] = v; g = x.groupby('casa').agg(r=('real', 'sum'), f=('_f', 'sum'))
        out.append(f"{k} {((g.f - g.r).abs().sum() / g.r.sum()):.1%} (sesgo {g.f.sum() / g.r.sum() - 1:+.0%})")
    print(f"{lg} meses: " + " · ".join(out))
