"""Descriptivos: YoY por house x quarter (envíos, EPOS, cortes), peso de lanzamientos, estacionalidad."""
import numpy as np
import pandas as pd
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from evaluate import fq  # noqa

W = Path(__file__).resolve().parents[1] / "work"


def main():
    H = pd.read_pickle(W / "hist.pkl"); C = pd.read_pickle(W / "cuts.pkl"); E = pd.read_pickle(W / "epos.pkl")
    attr = pd.read_pickle(W / "attr.pkl")
    out = []
    def agg(M, name):
        df = M.T.copy(); df.index = pd.DatetimeIndex(df.index)
        df = df.groupby(attr.house.reindex(df.columns).values, axis=1).sum() if False else df.T.groupby(attr.house.reindex(M.index).values).sum().T
        df.index = pd.DatetimeIndex(df.index)
        q = df.groupby(fq(df.index).values).sum()
        q["TOTAL"] = q.sum(1)
        return q
    Hq = agg(H.fillna(0), "ship"); Cq = agg(C, "cuts"); Eq = agg(E.reindex(columns=H.columns).fillna(0), "epos")
    yoy = Hq / Hq.shift(4) - 1
    eyoy = Eq / Eq.shift(4).replace(0, np.nan) - 1
    lines = ["# Descriptivos (generado por src/descriptive.py)\n"]
    lines += ["## Envíos por quarter fiscal (unidades)\n", Hq.round(0).to_markdown(), "\n## YoY envíos\n", yoy.round(3).to_markdown(),
              "\n## Supply cuts por quarter (bruto, puede estar x4)\n", Cq.round(0).to_markdown(),
              "\n## Cuts/4 como % de envíos\n", (Cq / 4 / Hq).round(3).to_markdown(),
              "\n## EPOS por quarter\n", Eq.round(0).to_markdown(), "\n## YoY EPOS\n", eyoy.round(3).to_markdown()]
    # lanzamientos: peso de EANs con < 12 meses de vida
    fs = attr.first_sale
    rows = []
    for fy, (a, b) in {"FY24": ("2023-07", "2024-06"), "FY25": ("2024-07", "2025-06"), "FY26": ("2025-07", "2026-06")}.items():
        cols = pd.date_range(a + "-01", b + "-01", freq="MS")
        new = fs >= pd.Timestamp(a + "-01") - pd.DateOffset(months=0)
        tot = H[cols].sum().sum()
        rows.append(dict(fy=fy, total=tot, launches_in_fy=H.loc[new, cols].sum().sum(), share=H.loc[new, cols].sum().sum() / tot,
                         n_launch=int(new.sum())))
    lines += ["\n## Peso de lanzamientos del propio FY (primera venta dentro del FY)\n", pd.DataFrame(rows).round(3).to_markdown(index=False)]
    lines += ["\nNota FY24: la serie empieza en 2023.M07, así que 'lanzamiento' en FY24 no es distinguible del histórico."]
    # like-for-like YoY (EANs vendiendo ambos años) por house
    rows = []
    for fy, (a, b) in {"FY25": ("2024-07", "2025-06"), "FY26": ("2025-07", "2026-06")}.items():
        cur = pd.date_range(a + "-01", b + "-01", freq="MS"); ly = cur - pd.DateOffset(years=1)
        sc = H[cur].sum(1); sl = H[ly].sum(1)
        for h in sorted(attr.house.unique()):
            sel = (attr.house == h)
            lfl = sel & (sl > 0) & (sc > 0)
            rows.append(dict(fy=fy, house=h, total_yoy=sc[sel].sum() / sl[sel].sum() - 1, lfl_yoy=sc[lfl].sum() / sl[lfl].sum() - 1,
                             new_share=sc[sel & (sl == 0)].sum() / sc[sel].sum(), lost_share_ly=sl[sel & (sc == 0)].sum() / sl[sel].sum()))
    lines += ["\n## YoY total vs like-for-like (EANs con venta en ambos años)\n", pd.DataFrame(rows).round(3).to_markdown(index=False)]
    # estacionalidad por house: peso de cada mes calendario en el FY
    df = H.fillna(0).T; df.index = pd.DatetimeIndex(df.index)
    g = df.T.groupby(attr.house.reindex(H.index).values).sum().T
    g["FY"] = [f"FY{(d.year + (d.month >= 7)) % 100}" for d in g.index]
    sh = []
    for fy, x in g.groupby("FY"):
        x = x.drop(columns="FY")
        if len(x) == 12:
            s = x / x.sum(); s.index = s.index.strftime("%m"); s.columns = [f"{c}|{fy}" for c in s.columns]; sh.append(s)
    lines += ["\n## Estacionalidad: % del FY por mes calendario\n", pd.concat(sh, axis=1).round(3).to_markdown()]
    (W / "results" / "descriptive.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
