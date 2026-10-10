"""Infografía (2 páginas A4 horizontal) del parlamento de 6 partidos con la lógica de DAs reconstruida.
Lee lo mismo que src/six_report.py. Salida: reportes/INFOGRAFIA_6_PARTIDOS.pdf"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_brujulas6 as b6  # noqa
import ideo_report as ir  # noqa
import ideo_viz as iv  # noqa
import six_report as sr  # noqa
import votes_report as vr  # noqa

ROOT = sr.ROOT; W = sr.W
OUT = ROOT / "reportes" / "INFOGRAFIA_6_PARTIDOS.pdf"
INK, INK2, MUTED = iv.INK, iv.INK2, iv.MUTED
pc, n0 = iv.pc, iv.n0
LEMA = {"Regla fragancias": "El año pasado, corregido por el trend de su tamaño",
        "Regla makeup": "El nivel de medio año, con la mitad del trend de su función",
        "Ciclo de vida": "¿Cómo les fue a los otros códigos a mi edad?",
        "Media 6M prudente": "Medio año plano con la caída de la categoría",
        "Media 6M estacional": "Medio año con la temporada de mi casa y el trend de mi fase",
        "Media 12M estacional": "Un año de nivel con la temporada de mi línea y mi propio trend"}


def voters(E, n):
    g = E[E.voto == n]
    cat = g.cat.value_counts(normalize=True); tr = g.tramo.value_counts(); fa = g.fase.value_counts()
    txt = f"{pc(cat.get('Makeup', 0))} makeup · {pc(cat.get('Fragancias', 0))} fragancias. Más votado por: {tr.index[0]} meses ({tr.iloc[0]}) y fase {fa.index[0].lower()} ({fa.iloc[0]})"
    if (g.isf == 2).sum() >= 8:
        txt += f"; {int((g.isf == 2).sum())} con bandera 2"
    return txt + "."


def card(P, D, Bj, B, E, n):
    k = Bj["nombres"].index(n); i = Bj["ideas"][k]
    T = D["por"]["Total"]["Total"]
    tr = "jóvenes: curva de su edad · maduros: trend de su fase" if n == "Ciclo de vida" else f"{i['fuente']} · {i['trend']}"
    base = i["familia"] if i["familia"] == i["memoria"] else f"{i['familia']} · {i['memoria']}"
    rows = [("Base", base), ("Temporada", i["estac"]), ("Trend", tr), ("DAs base", f"resta {i['dap']} de los planificados"), ("Cortes", f"+{i['cortes']}")]
    rr = "".join(f"<div class='ir'><span>{a}</span><b>{b}</b></div>" for a, b in rows)
    smax = max(T["seats"][x] for x in P.names); vmax = max(T["vol"][x] for x in P.names)
    err = float(np.abs(B["F:" + n] - B.real).sum() / B.real.sum())
    return (f"<div class='pc' style='--c:{P.col[n]}'><div class='ph'><div class='pn'>{P.num[n]}</div><div><div class='pt'>{n}</div>"
            f"<div class='pb'>{'Fijo · ' if n.startswith('Regla') else ''}{P.bloc[n]}</div></div></div><div class='pl'>«{LEMA[n]}»</div>{rr}"
            f"<div class='pm'><div><span>EANs</span><b>{T['seats'][n]}</b><i style='width:{T['seats'][n] / smax * 100:.0f}%'></i></div>"
            f"<div><span>Volumen</span><b>{pc(T['vol'][n])}</b><i style='width:{T['vol'][n] / vmax * 100:.0f}%'></i></div>"
            f"<div><span>Error EAN solo</span><b>{pc(err)}</b></div></div><div class='pv'>{voters(E, n)}</div></div>")


def main():
    D = json.loads((W / "six_multi.json").read_text()); Bj = json.loads((W / "ideo_brujulas6.json").read_text())
    C = json.loads((W / "da_conversion.json").read_text())
    B = pd.read_parquet(W / "six_multi.parquet"); E = pd.read_parquet(W / "six_multi_ean.parquet").set_index("ean")
    POS = pd.read_parquet(W / "ideo_brujulas6_ean.parquet")
    P = b6.P6(); T = D["por"]["Total"]["Total"]; per = D["persistencia"]
    conv = {r["cat"]: r["conversion"] for r in C["total"]}
    fs = sr.flag_share()
    cards = "".join(card(P, D, Bj, B, E, n) for n in P.names)
    rules = (f"<div class='rules'><div class='rl'><b>Trend</b>Con los actuals tal cual: los DAs no lo tocan.</div>"
             f"<div class='rl'><b>Base</b>DAs de cada mes leídos de la última foto en la que aún era futuro (o9 los borra). Cuánto restar: cada partido. "
             f"Se ejecutó el {pc(conv['Fragancias'])} en fragancias y el {pc(conv['Makeup'])} en makeup.</div>"
             f"<div class='rl'><b>DAs futuros</b>Insight: se suman según la bandera de la foto. Sin bandera 100%, bandera 1 50%, bandera 2 0% "
             f"(ahí el consenso ya es {pc(fs[2]['da_cons'])} DAs).</div></div>")
    p1 = (f"<section class='page ip'><div class='blob'></div><div class='hd'><div><div class='kick'>Sistema de elecciones · fotos sep-25, dic-25 y mar-26 → real sep-26</div>"
          f"<h1>Los 6 partidos</h1><div class='sub'>Dos reglas fijas, el ciclo de vida para la edad y tres partidos de nivel reciente. Ninguno usa solo los últimos 3 meses. "
          f"Cada EAN vota en 6 urnas (foto × quarter) por el partido que mejor le acertó; el más votado se queda con el {pc(max(T['seats'][x] for x in P.names) / T['eans'])} de los EANs.</div>{rules}</div>"
          f"<div class='mh'>{iv.hemicycle(P, T['seats'], w=300)}{iv.volbar(P, T['vol'], h=3.6, minlab=0.12)}"
          f"<div class='mhl'>{T['eans']} EANs · barra = volumen real de los EANs que gana cada partido</div></div></div><div class='cards c3'>{cards}</div></section>")
    # página 2: brújulas + horizonte
    pts = POS.join(E[["voto"]])
    def mk(kx, ky):
        out = []
        for e, r in pts.iterrows():
            if r.voto not in P.col or r.voto == "Empate":
                continue
            rng = np.random.default_rng(abs(hash(e)) % 2**32)
            out.append(dict(x=float(np.clip(r[kx] + rng.normal(0, .02), -1.08, 1.08)), y=float(np.clip(r[ky] + rng.normal(0, .02), -1.08, 1.08)), party=r.voto, vol=float(r.real)))
        return out
    specs = [("c1", "1 · ¿De dónde parto?", ("Plana", "Con temporada"), ("Reciente (6M)", "Lejana (12M / año pasado)"),
              ("Planos de memoria larga", "Estacionales de memoria larga", "Planos de lo reciente", "Estacionales de lo reciente")),
             ("c2", "2 · ¿A quién sigo?", ("Individual: EAN, línea", "Colectivo: casa, categoría"), ("Trend suave", "Trend completo"),
              ("Individualistas creyentes", "Colectivistas creyentes", "Individualistas escépticos", "Colectivistas escépticos")),
             ("c3", "3 · ¿Cómo limpio la base?", ("Deja los DAs planificados", "Los resta"), ("No suma cortes", "Suma cortes"),
              ("Suma cortes, deja DAs", "Suma cortes y resta DAs", "Base tal cual", "Solo resta DAs"))]
    comps = "".join(iv.compass(P, mk(k + "x", k + "y"), xl, yl, t, q, w=330, h=360, xlim=(-1.14, 1.14), ylim=(-1.14, 1.14), small=True,
                               fixed={nm: (Bj["posiciones"][k][nm][0] * .86, Bj["posiciones"][k][nm][1] * .86) for nm in P.names}) for k, t, xl, yl, q in specs)
    hb = sr.bars([(f"{lg} meses · {nm}", per[f][c]["ean"], col) for f, lg in [("2025-09", "7–9"), ("2025-12", "4–6"), ("2026-03", "1–3")]
                  for c, nm, col in [("cons", "consenso", iv.CONS), ("parl", "parlamento", INK)]], w=330, lab_w=130, maxv=1.0)
    leg = "".join(f"<span>{P.dot(n, num=True)}{n}</span>" for n in P.names)
    p2 = (f"<section class='page ip'><div class='blob'></div><div class='kick'>Brújulas · cada punto es un EAN de la foto sep-25, del color del partido al que vota</div>"
          f"<h2>Dónde está cada partido y qué ha demostrado</h2><div class='lg'>{leg}<span class='lm'>círculo con borde = partido por su fórmula · "
          f"posición del EAN = cuántos puntos de error gana con cada lado (centro: le da igual)</span></div>"
          f"<div class='g3c'>{comps}</div>"
          f"<div class='bot'><div class='box'><div class='ct'>El horizonte manda</div><div class='cs'>Error EAN a EAN en abr–jun; cada EAN eligió su partido con oct–mar</div>"
          f"<div class='lg2'><span><i style='background:{iv.CONS}'></i>Consenso</span><span><i style='background:{INK}'></i>Parlamento</span></div>{hb}</div>"
          f"<div class='box'><div class='ct'>Qué proponemos</div><ul class='ul'>"
          f"<li><b>Lejos (7–9 meses):</b> el partido de cada EAN. Falla un {pc(per['2025-09']['parl']['ean'])} contra {pc(per['2025-09']['cons']['ean'])} del consenso.</li>"
          f"<li><b>Cerca (1–6 meses):</b> el consenso, que tiene pedidos e información que el histórico no tiene.</li>"
          f"<li><b>Códigos nuevos:</b> ciclo de vida, y sin DAs futuros si tienen bandera 2.</li>"
          f"<li><b>Guardar los DAs de cada foto</b>: sin ellos no se puede limpiar la base.</li></ul></div></div></section>")
    css = vr.CSS + iv.CSS_EXTRA + ir.EXTRA + __import__("ideo_infografia").CSS + f"""
.cards.c3 {{ grid-template-columns: repeat(3, 1fr); gap: 3mm; margin-top: 3mm; }}
.c3 .pt {{ font-size: 11pt; }} .c3 .pl {{ font-size: 8.4pt; min-height: 0; }} .c3 .ir {{ font-size: 7pt; grid-template-columns: 15mm 1fr; }}
.c3 .pv {{ font-size: 6.8pt; }} .c3 .pm b {{ font-size: 12pt; }}
.rules {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.4mm; margin-top: 2.4mm; }}
.rl {{ background: #fff; border: 1px solid #E6EAEE; border-left: 3px solid {INK}; border-radius: 9px; padding: 1.6mm 2.4mm; font-size: 6.9pt; line-height: 1.38; color: {INK2}; }}
.rl b {{ display: block; color: {INK}; font-size: 8pt; margin-bottom: .4mm; }}
.bot {{ position: relative; display: grid; grid-template-columns: 1.1fr 1fr; gap: 3.4mm; margin-top: 3mm; }}
.ip .g3c {{ gap: 3mm; }}
"""
    html = f"<!doctype html><html><head><meta charset='utf-8'><title>Los 6 partidos</title><style>{css}</style></head><body>{p1}{p2}</body></html>"
    hp = W / "infografia_6_partidos.html"; hp.write_text(html, encoding="utf-8")
    subprocess.run([vr.CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={OUT}", f"file://{hp}"], check=True, capture_output=True)
    print(OUT)


if __name__ == "__main__":
    main()
