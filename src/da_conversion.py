"""¿Se ejecutaron los DAs planificados? Conversión de cada DA de una foto en envío real (verdad = foto sep-26).

Para cada foto V (fragancias: sep-25, dic-25, mar-26, jun-26; makeup: sep-25, mar-26) y cada mes futuro t ≤ ago-26:
  DA planificado d = DA de la foto V para el mes t (solo positivos; los negativos aparte)
  base             = consenso de la foto V en t − DA de la foto V en t (lo que el consenso tenía sin el DA)
  real             = envío del mes t en la foto sep-26
Conversión (uplift real / DA): Σ (real − base × (1 + r0)) / Σ d en los EAN-mes con DA, donde r0 es el desvío medio de la base en
los EAN-mes SIN DA de la misma foto y casa (corrige que la base ya venga alta o baja ese periodo).
  100% = el DA se convirtió entero en envío extra; 0% = no hubo nada extra.
Con flag 2 la base es ~0 (el consenso es el DA): ahí la conversión es real / DA.
También: ¿el DA seguía vivo en la foto siguiente? (% del volumen planificado que la siguiente foto aún tiene en ese mes).
Salida: work/da_conversion.json"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import house_compare as hc  # noqa
import ideo_panel as ip  # noqa

W = hc.W; M = hc.M; LAST = hc.LAST


def rows_for(d, H, cat, casa_of, vers):
    out = []
    for i, v in enumerate(vers[:-1]):
        V = pd.Timestamp(v + "-01")
        x = d[(d.version == v) & (d.date > V) & (d.date <= LAST)]
        nxt = d[d.version == vers[i + 1]].pivot_table(index=["ean", "date"], values="da", aggfunc="sum").da
        g = x.groupby(["ean", "date"]).agg(da=("da", "sum"), cons=("cons", "sum"), isf=("isf", "max")).reset_index()
        g["ean"] = g.ean.astype(str)
        g = g[g.ean.isin(H.index)]
        g["real"] = [H.at[e, t] if np.isfinite(H.at[e, t]) else 0.0 for e, t in zip(g.ean, g.date)]
        g["base"] = g.cons - g.da
        g["foto"] = v; g["lag"] = [(t.year - V.year) * 12 + t.month - V.month for t in g.date]
        g["cat"] = cat; g["casa"] = g.ean.map(casa_of)
        key = pd.MultiIndex.from_arrays([g.ean.astype(type(nxt.index.levels[0][0])) if len(nxt) else g.ean, g.date])
        g["da_sig"] = nxt.reindex(key).fillna(0).values if vers[i + 1] != vers[-1] or True else 0
        g["sig_cerrado"] = g.date < pd.Timestamp(vers[i + 1] + "-01")
        out.append(g)
    return pd.concat(out, ignore_index=True)


def conversion(g):
    """Uplift real / DA corrigiendo el sesgo de la base con los EAN-mes sin DA de la misma foto y casa."""
    res = []
    for (f, c), x in g.groupby(["foto", "casa"]):
        nod = x[(x.da == 0) & (x.base > 0)]
        r0 = (nod.real.sum() - nod.base.sum()) / nod.base.sum() if nod.base.sum() > 0 else 0.0
        y = x[x.da > 0].copy()
        y["extra"] = y.real - y.base * (1 + r0)
        res.append(y)
    return pd.concat(res) if res else g.iloc[:0]


def summary(y, by):
    t = y.groupby(by).agg(n=("da", "size"), da=("da", "sum"), extra=("extra", "sum"), real=("real", "sum"), base=("base", "sum"))
    t["conversion"] = t.extra / t.da
    t["real_sobre_consenso"] = t.real / (t.base + t.da)
    return t


def main():
    d = pd.read_parquet(W / "data.parquet"); d["ean"] = d.ean.astype(str)
    Hf = pd.read_pickle(W / "hist.pkl").reindex(columns=M); Hf.index = Hf.index.astype(str)
    a = pd.read_pickle(W / "attr.pkl"); a.index = a.index.astype(str)
    frag = rows_for(d[d.house.isin(ip.FRAG)], Hf, "Fragancias", a.house.map(ip.FRAG).to_dict(), ip.VERS_F)
    import mu_backtest as mb
    dm, Hm, *_ = mb.load(); dm = dm.copy(); dm["ean"] = dm.ean.astype(str); Hm.index = Hm.index.astype(str)
    casa_m = dm.groupby("ean").fam.first().map(ip.MU).to_dict()
    mu = rows_for(dm[dm.fam.isin(ip.MU)], Hm, "Makeup", casa_m, ip.VERS_M)
    g = pd.concat([frag, mu], ignore_index=True)
    g["flag"] = g.isf.fillna(0).astype(int).clip(0, 2)
    y = conversion(g)
    y["lag_g"] = pd.cut(y.lag, [0, 3, 6, 9], labels=["1–3 meses", "4–6 meses", "7–9 meses"])
    y["tam"] = pd.cut(y.da / (y.base.clip(lower=1)), [-1, 0.25, 1, 1e9], labels=["DA < 25% de la base", "25–100%", "DA > base"])
    out = {}
    for name, by in [("total", ["cat"]), ("flag", ["cat", "flag"]), ("casa", ["casa"]), ("lag", ["cat", "lag_g"]), ("foto", ["cat", "foto"]), ("tam", ["cat", "tam"])]:
        t = summary(y, by)
        out[name] = t.reset_index().astype({c: str for c in by}).to_dict("records")
        print(f"\n— {name}"); print(t[["n", "da", "extra", "conversion", "real_sobre_consenso"]].round(2).to_string())
    # ¿seguía el DA en la foto siguiente? (solo meses aún abiertos en la siguiente foto: era el plan vigente)
    z = g[(g.da > 0) & ~g.sig_cerrado]
    viv = z.groupby(["cat", "foto"]).apply(lambda q: pd.Series(dict(da=q.da.sum(), sigue=np.minimum(q.da_sig.clip(lower=0), q.da).sum() / q.da.sum())))
    print("\n— % del DA planificado que sigue en la foto siguiente (mes aún abierto)"); print(viv.round(2).to_string())
    out["sigue"] = viv.reset_index().to_dict("records")
    # negativos
    neg = g[g.da < 0]
    out["negativos"] = dict(n=int(len(neg)), da=float(neg.da.sum()))
    (W / "da_conversion.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=float))


if __name__ == "__main__":
    main()
