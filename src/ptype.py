"""Clasificación de tipo de producto a partir de la descripción (tamaño y formato)."""
import re
import numpy as np
import pandas as pd

ANC = re.compile(r"\b(DEO|DEOSTK|B/L|BL|S/G|SG|SOAP|OIL|PRFOIL|BMIST)\b")


def size_ml(desc):
    d = desc.upper()
    m = re.findall(r"(\d+(?:\.\d+)?)\s*ML", d)
    if not m:
        m = re.findall(r"EDP\s?(\d{2,3})\b", d)
    if not m:
        return np.nan
    return float(m[0])


def classify(desc, house):
    d = desc.upper()
    if house == "Kylie Makeup":
        return "accesorio_maquillaje"
    if ANC.search(d):
        return "ancilar(deo/BL/SG)"
    s = size_ml(d)
    if "REFILL" in d and (np.isnan(s) or s >= 150):
        return "refill/jumbo(>=150)"
    if np.isnan(s):
        return "sin_tamaño"
    if s <= 15:
        return "mini(<=15ml/penspray)"
    if s <= 40:
        return "pequeño(20-40)"
    if s <= 60:
        return "medio(45-60)"
    if s < 150:
        return "grande(75-125)"
    return "refill/jumbo(>=150)"


def add_types(attr):
    attr = attr.copy()
    attr["ptype"] = [classify(str(d), h) for d, h in zip(attr.desc, attr.house)]
    attr["house_ptype"] = attr.house + "|" + attr.ptype
    return attr


if __name__ == "__main__":
    from pathlib import Path
    W = Path(__file__).resolve().parents[1] / "work"
    a = add_types(pd.read_pickle(W / "attr.pkl"))
    H = pd.read_pickle(W / "hist.pkl")
    a["vol"] = H.sum(axis=1)
    print(a.groupby("ptype").agg(n=("house", "size"), vol=("vol", "sum")))
