"""Carga GUMU.xlsx (Gucci Make up) y KYMU.xlsx (Kylie Makeup) -> work/mu.parquet (largo, todas las fotos)."""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLS = ["house", "brand", "pline", "ean", "desc", "fy", "fq", "month", "resp", "isf",
        "cons_ly", "epos", "da", "cons", "act", "cuts"]


def load():
    out = []
    for f, fam in [("GUMU.xlsx", "GUMU"), ("KYMU.xlsx", "KYMU")]:
        for sheet, df in pd.read_excel(ROOT / f, sheet_name=None, header=1).items():
            df.columns = COLS
            df["fam"] = fam
            df["version"] = sheet.split()[-1].replace(".M", "-")  # 'S&OP 2025.M09' -> '2025-09'
            out.append(df)
    d = pd.concat(out, ignore_index=True)
    d["ean"] = d["ean"].astype(str)
    d["date"] = pd.to_datetime(d["month"].str.replace(".M", "-", regex=False) + "-01")
    d["vdate"] = pd.to_datetime(d["version"] + "-01")
    for c in ["isf", "cons_ly", "epos", "da", "cons", "act", "cuts"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    return d


if __name__ == "__main__":
    d = load()
    d.to_parquet(ROOT / "work" / "mu.parquet")
    print(d.shape, d.version.unique())
