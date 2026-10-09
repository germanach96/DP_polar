"""¿Incluir lanzamientos en el trend del grupo (house x tamaño)? Local dinámico = <6 meses de envíos en la foto.
Evaluación siempre sobre el mismo universo: EANs Central en la foto (>=6 meses de envíos) sin forecast manual (isf de la foto)."""
import sys, warnings
import numpy as np, pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import methods as mt  # noqa
import tracking as tk  # noqa
from ptype import add_types  # noqa
warnings.filterwarnings("ignore")
W = Path(__file__).resolve().parents[1] / "work"


def main():
    d = pd.read_parquet(W / "data.parquet")
    H = pd.read_pickle(W / "hist.pkl").reindex(columns=tk.MONTHS)
    a = add_types(pd.read_pickle(W / "attr.pkl")).reindex(H.index)
    M = tk.MONTHS
    rows = []
    for s in tk.SNAPS:
        V = pd.Timestamp(s + "-01"); m = M.get_loc(V)
        x = d[d.version == s]
        isf = x.groupby("ean").isf.max().reindex(H.index).fillna(0)
        Hm = H.values.copy(); Hm[:, m:] = np.nan
        nmonths = (np.nan_to_num(Hm) > 0).sum(1)              # meses con envío hasta la foto
        first = np.argmax(np.isfinite(Hm), 1).astype(float); first[~np.isfinite(Hm).any(1)] = np.nan
        age = m - first                                       # meses de vida en la foto
        central = age >= 6
        alive24 = np.isfinite(Hm[:, m - 24])
        keys = a.house_ptype.values
        variants = {
            "solo_LFL(>=24m)": alive24 & (isf.values == 0),
            "central(>=6m)_sin_manuales": central & (isf.values == 0),
            "central(>=6m)_con_manuales": central,
            "todo(incl.<6m)_con_manuales": np.isfinite(Hm).any(1),
        }
        fi = [j for j in range(m + 1, m + 9) if M[j] <= tk.LAST_TRUTH]
        A = np.nan_to_num(H.values[:, fi])
        ev = central & (isf.values == 0)
        for nm, mask in variants.items():
            g = np.clip(np.nan_to_num(mt._group_g(Hm, m, 12, keys, mask)), -.3, .3)
            for pct in (0.5, 1.0):
                F = np.stack([np.nan_to_num(Hm[:, j - 12]) * (1 + pct * g) for j in fi], 1)
                for seg, sel in [("maduros(>=18m)", ev & (age >= 18)), ("jóvenes(6-17m)", ev & (age >= 6) & (age < 18)), ("todo_central", ev)]:
                    f, aa = F[sel], A[sel]
                    rows.append(dict(snap=s, trend=nm, pct=pct, seg=seg, wmape=np.abs(f - aa).sum() / aa.sum(),
                                     bias=f.sum() / aa.sum() - 1, vol=aa.sum()))
            wgt = np.nan_to_num(Hm[:, m - 12:m]).sum(1) * ev
            rows.append(dict(snap=s, trend=nm, pct=-1, seg="trend_medio", wmape=np.nan, bias=np.average(g, weights=wgt + 1e-9), vol=np.nan))
    R = pd.DataFrame(rows)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
    tm = R[R.seg == "trend_medio"].pivot_table(index="trend", columns="snap", values="bias")
    print("trend medio aplicado (ponderado por volumen):"); print(tm.round(3))
    R = R[R.seg != "trend_medio"]
    w = R.groupby(["seg", "pct", "trend"]).agg(wmape=("wmape", "mean"), bias_medio=("bias", "mean"), bias_abs=("bias", lambda x: x.abs().mean()))
    print(w.round(3))
    print(R.pivot_table(index=["seg", "pct", "trend"], columns="snap", values="bias").round(3))
    share = R[(R.trend == "solo_LFL(>=24m)") & (R.pct == 0.5)].pivot_table(index="seg", columns="snap", values="vol")
    print("volumen real evaluado:"); print(share.round(0))
    (W / "results" / "launch_trend.md").write_text("# Lanzamientos en el trend (src/launch_trend.py)\n\n" + tm.round(3).to_markdown() + "\n\n" + w.round(3).to_markdown())


if __name__ == "__main__":
    main()
