"""Posición de cada EAN en las brújulas políticas (correr después de src/ideo_parties.py).

Cada eje enfrenta dos ideas con la misma flexibilidad a cada lado (mismas opciones en todo lo demás). Para cada EAN se toma
su mejor estrategia de cada lado (mínimo error del banco con esa idea) y la posición es tanh(ventaja / 5 puntos): ventaja = error del lado izquierdo − error del lado derecho.
  0     -> le da igual (los dos lados le dan el mismo error)
  ±0,76 -> un lado le ahorra 5 puntos de error
  ±0,96 -> un lado le ahorra 10 puntos o más
Ejes:
  estacional   media plana 3/6/12M                             vs media 3/6/12M sin temporada × perfil de su casa
  corto        media de 12M (plana o estacional)               vs media de 3M (plana o estacional)
  individual   trend colectivo (casa o categoría)              vs individual (propio EAN o su línea)
  fe           trend suave (25% o sin trend)                   vs trend completo (75–100%)
  tventana     trend de 12M                                    vs trend de 3M
  dap          no limpia DAs del pasado (0%)                   vs limpia el 100%
  daf          no suma DAs de la foto (0%)                     vs suma el 100%
  cortes       no suma cortes                                  vs suma el 50%
  ciclo        nivel 6M sin trend o con trend de su fase       vs nivel 6M × ciclo de vida (curva por edad)
Salida: work/ideo_compass.parquet"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_parties as ipp  # noqa

SCALE = 0.05


def main():
    st, FQ, Aq, a = ipp.load()
    real = Aq.sum(1); cols = np.where(real > 0)[0]
    Sc = np.empty((len(st), len(cols)), np.float32)
    for i in range(0, len(st), 20000):
        Sc[i:i + 20000] = np.minimum(np.abs(FQ[i:i + 20000][:, cols] - Aq[None, cols]).sum(2) / real[cols][None], ipp.CAPSCORE)
    del FQ
    b = st.base.values; f = st.fuente.values; fz = st.fuerza.values
    es = st.estac.values
    axes = {
        "estacional": (np.isin(b, ["M3", "M6", "M12"]), np.isin(b, ["M3e", "M6e", "M12e"]) & (es == "casa")),
        "corto": (np.isin(b, ["M12", "M12e"]), np.isin(b, ["M3", "M3e"])),
        "individual": (np.isin(f, ["casa", "categoría"]), np.isin(f, ["EAN", "línea"])),
        "fe": (((f == "ninguna") & (b != "CV")) | ((f != "ninguna") & (fz <= 0.25)), (f != "ninguna") & (fz >= 0.75)),
        "tventana": (st.tventana.values == 12, st.tventana.values == 3),
        "dap": (st.dap.values == 0, st.dap.values == 1),
        "daf": (st.daf.values == 0, st.daf.values == 1),
        "cortes": (st.cortes.values == "0", st.cortes.values == "50%"),
        "ciclo": (np.isin(b, ["M6", "M6e"]) & ((f == "ninguna") | (f == "fase")), b == "CV"),
    }
    out = pd.DataFrame(index=a.index[cols])
    for k, (L, R) in axes.items():
        eL = Sc[L].min(0); eR = Sc[R].min(0)
        out["adv_" + k] = eL - eR
        out[k] = np.tanh((eL - eR) / SCALE)
    out.to_parquet(ipp.W / "ideo_compass.parquet")
    print(out.describe().round(2).to_string())


if __name__ == "__main__":
    main()
