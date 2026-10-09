"""Carga DATA.xlsx (una pestaña por versión/snapshot) a un parquet largo y tidy."""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLS = ["house", "brand", "pline", "ean", "desc", "fy", "fq", "month", "resp", "isf",
        "cons_ly", "epos", "da", "cons", "act", "cuts"]
VERSION_DATE = {  # mes de la foto (S&OP del mes)
    "S&OP 2025.M09": "2025-09", "S&OP 2025.M12": "2025-12", "S&OP 2026.M03": "2026-03",
    "S&OP 2026.M06": "2026-06", "Month-2026.M09.W38": "2026-09",
}


def load(path=ROOT / "DATA.xlsx"):
    out = []
    for sheet, df in pd.read_excel(path, sheet_name=None, header=1).items():
        df.columns = COLS
        df["version"] = VERSION_DATE[sheet]
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
    d.to_parquet(ROOT / "work" / "data.parquet")
    print(d.shape)
