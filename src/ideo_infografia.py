"""Infografía (2 páginas A4 horizontal): los 10 partidos elegidos, sus ideas y votantes, brújulas políticas y cómo se agruparon.
Lee los mismos datos que src/ideo_report.py. Salida: reportes/INFOGRAFIA_IDEOLOGIAS.pdf"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ideo_report as ir  # noqa
import ideo_viz as iv  # noqa
import votes_report as vr  # noqa

OUT = ir.ROOT / "reportes" / "INFOGRAFIA_IDEOLOGIAS.pdf"
INK, INK2, MUTED = iv.INK, iv.INK2, iv.MUTED
pc = iv.pc
# lema por forma de base (la regla está en la fórmula; el lema la cuenta en una frase)
LEMA = {"fix_rf": "El año pasado, corregido por el trend de su segmento",
        "fix_rm": "El nivel de medio año, con la mitad del trend",
        "LY": "Lo que vendí el año pasado, con el trend de mi franquicia",
        "LY+M6e": "Mitad memoria del año pasado, mitad presente",
        "M12e": "Un año de nivel con la temporada de mi casa",
        "M6e": "Medio año con temporada y mi propio trend",
        "M3e": "Lo último que vendí, con temporada y el trend de mi fase",
        "M6": "Medio año plano y mi propio trend, sin promociones",
        "M12": "Un año plano y mi propio trend",
        "M3": "Los prudentes: el último trimestre con la caída de la categoría",
        "CV": "¿Cómo les fue a los otros códigos a mi edad?"}


def key(p):
    return "fix_rf" if p["nombre"] == "Regla fragancias" else "fix_rm" if p["nombre"] == "Regla makeup" else p["base"]


def voters(E, n):
    g = E[E.voto == n]
    cat = g.cat.value_counts(normalize=True)
    tr = g.tramo.value_counts(); fa = g.fase.value_counts()
    top_t = tr.index[0]; top_f = fa.index[0]
    dead = int((g.real == 0).sum())
    txt = f"{pc(cat.get('Makeup', 0))} makeup · {pc(cat.get('Fragancias', 0))} fragancias. Más votado por: {top_t} meses ({tr.iloc[0]}) y fase {top_f.lower()} ({fa.iloc[0]})"
    if dead >= 10:
        txt += f". Incluye {dead} EANs sin venta oct–jun"
    if (g.isf == 2).sum() >= 10:
        txt += f"; {int((g.isf == 2).sum())} con bandera 2"
    return txt + "."


def ideas_rows(p):
    i = p["ideas"]
    tr = "sin trend" if i["trend"] == "—" else f"{i['fuente']} · {i['trend']}"
    if p["base"] == "CV":
        tr = "jóvenes: curva de su edad · maduros: trend de su fase"
    rows = [("Base", i["familia"] if i["familia"] == i["memoria"] else f"{i['familia']} · {i['memoria']}"), ("Temporada", i["estac"]), ("Trend", tr),
            ("DAs", f"pasado −{i['dap']} · foto +{i['daf']}"), ("Cortes", f"+{i['cortes']}")]
    return "".join(f"<div class='ir'><span>{a}</span><b>{b}</b></div>" for a, b in rows)


def party_card(P, D, E, p):
    n = p["nombre"]; T = D["eleccion"]["total"]
    w = pd.DataFrame(D["w90"]); w90 = float((w[n] * w.real).sum() / w.real.sum())
    seats, vol = T["seats"][n], T["vol"][n]
    smax = max(T["seats"][x] for x in P.names); vmax = max(T["vol"][x] for x in P.names)
    col = P.col[n]
    return (f"<div class='pc' style='--c:{col}'><div class='ph'><div class='pn'>{P.num[n]}</div><div><div class='pt'>{n}</div>"
            f"<div class='pb'>{'Fijo · ' if p['fijo'] else ''}{P.bloc[n]}</div></div></div>"
            f"<div class='pl'>«{LEMA[key(p)]}»</div>{ideas_rows(p)}"
            f"<div class='pm'><div><span>EANs</span><b>{seats}</b><i style='width:{seats / smax * 100:.0f}%'></i></div>"
            f"<div><span>Volumen</span><b>{pc(vol)}</b><i style='width:{vol / vmax * 100:.0f}%'></i></div>"
            f"<div><span>WAPE90 solo</span><b>{pc(w90)}</b></div></div>"
            f"<div class='pv'>{voters(E, n)}</div></div>")


def page1(P, D, E):
    T = D["eleccion"]["total"]
    cards = "".join(party_card(P, D, E, p) for p in P.list)
    tl = D["temporal_limpio"]["Total"]
    head = (f"<div class='hd'><div><div class='kick'>Sistema de elecciones · foto sep-25 → real sep-26 · {iv.n0(D['n_estrategias'])} estrategias por EAN</div>"
            f"<h1>Los 10 partidos</h1><div class='sub'>Las 2 reglas actuales + 8 partidos nuevos, uno por forma de base. "
            f"Cada uno resume las estrategias que mejor le habrían ido a un grupo de EANs. Ninguno tiene mayoría: el que más EANs gana se queda con el "
            f"{pc(max(T['seats'][x] for x in P.names) / T['eans'])}.</div></div>"
            f"<div class='mh'>{iv.hemicycle(P, T['seats'], w=300)}{iv.volbar(P, T['vol'], h=3.6, minlab=0.11)}"
            f"<div class='mhl'>{T['eans']} EANs · barra = volumen · elegir partido con oct–mar y aplicarlo en abr–jun: error EAN {pc(tl['ean_elegido'])} "
            f"(reglas {pc(tl['ean_regla'])}, consenso {pc(tl['ean_cons'])})</div></div></div>")
    return f"<section class='page ip'><div class='blob'></div>{head}<div class='cards'>{cards}</div></section>"


def flow(P, D):
    ap = D["aportes"]
    steps = [(iv.n0(D["n_estrategias"]), "estrategias por EAN", "base · temporada · trend (de quién, ventana, fuerza, tope) · DAs pasado · cortes · DAs foto"),
             (str(D["n_con_real"]), "EANs con su mejor estrategia", "con trampa: comparadas con el real oct-25 → jun-26 de la foto sep-26"),
             ("9 → 8", "formas de base", "un partido por forma; el dato elige lo demás. Sale la que menos aporta (media 12M plana)"),
             (f"{pc(D['obj_reglas'])} → {pc(D['obj_final'])}", "error del parlamento", f"2 reglas → 10 partidos; techo con 203.160 estrategias: {pc(D['oraculo'])}")]
    st = "".join(f"<div class='fs'><div class='fn'>{a}</div><div class='ft'>{b}</div><div class='fx'>{c}</div></div>" for a, b, c in steps)
    bars = ""
    mx = max(ap[i - 1]["obj"] - ap[i]["obj"] for i in range(1, len(ap)))
    for i in range(1, len(ap)):
        n = ap[i]["partido"]; d = ap[i - 1]["obj"] - ap[i]["obj"]
        bars += (f"<div class='cb'><span>{P.dot(n, num=True)}{P.short(n)}</span><i style='width:{d / mx * 100:.0f}%;background:{P.col[n]}'></i>"
                 f"<b>−{f'{d * 100:.1f}'.replace('.', ',')}</b></div>")
    R = D["robustez"]
    rob = (f"<div class='rb'><b>¿Y con EANs nuevos?</b> Elegidos con la mitad de los EANs y medidos en la otra (10 veces): "
           f"{pc(np.mean([r['solo_reglas'] for r in R]))} → {pc(np.mean([r['fuera'] for r in R]))}. Las formas de base se repiten; el detalle de cada partido, no.</div>")
    nxt = ("<div class='rb nx'><b>Para confirmar</b><br/>· Los 8 partidos nuevos (las formas son estables; el detalle se puede simplificar).<br/>"
           "· Repetir la elección con las fotos dic-25, mar-26 y jun-26.<br/>· En el total de la casa la regla sigue siendo más segura.</div>")
    return (f"<div class='flow'><div class='ct'>Cómo se agruparon</div>{st}<div class='ct' style='margin-top:2.6mm'>Lo que aporta cada partido "
            f"<small>(puntos de error que quita, en orden)</small></div>{bars}{rob}{nxt}</div>")


def page2(P, D, E, C):
    specs = [ir.SPECS1[0], ir.SPECS1[1], ir.SPECS2[0], ir.SPECS2[1]]
    cs = ir.compasses(P, E, C, specs, small=True, w=330, h=232)
    caps = ["Fragancias se inclina por la temporada de su casa; makeup se reparte.",
            "Casi todos en el centro: en sep-25 su trend y el de su casa caen igual.",
            "Casi la mitad acierta más con el trend completo; pocos lo suavizan.",
            "Los DAs de la foto separan a makeup: muchos aciertan más sin ellos."]
    grid = "".join(f"<div class='cw'>{c}<div class='cc'>{t}</div></div>" for c, t in zip(cs, caps))
    leg = "".join(f"<span>{P.dot(n, num=True)}{P.short(n)}</span>" for n in P.names)
    return (f"<section class='page ip'><div class='blob'></div><div class='kick'>Brújulas políticas · cada punto es un EAN, del color del partido al que vota</div>"
            f"<h2>Dónde está cada EAN y cada partido</h2><div class='lg'>{leg}<span class='lm'>número = mediana de los votantes del partido · "
            f"posición = cuántos puntos de error gana el EAN con cada lado (centro: le da igual)</span></div>"
            f"<div class='p2'><div class='g22'>{grid}</div>{flow(P, D)}</div></section>")


CSS = f"""
.ip .kick {{ color: {INK2}; }}
.ip h1 {{ font-size: 28pt; margin-top: .6mm; }}
.hd {{ position: relative; display: grid; grid-template-columns: 1fr 78mm; gap: 6mm; align-items: start; }}
.sub {{ font-size: 8.6pt; line-height: 1.5; color: {INK2}; margin-top: 1.6mm; max-width: 170mm; }}
.mh {{ background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; padding: 2mm 3mm 2.2mm; }}
.mh svg {{ display: block; width: 62%; margin: 0 auto 1mm; }}
.mhl {{ font-size: 6.4pt; color: {MUTED}; margin-top: 1mm; line-height: 1.35; }}
.cards {{ position: relative; display: grid; grid-template-columns: repeat(5, 1fr); gap: 2.6mm; margin-top: 3mm; }}
.pc {{ background: #fff; border: 1px solid #E6EAEE; border-top: 3.4px solid var(--c); border-radius: 11px; padding: 2.2mm 2.6mm 2mm; display: flex; flex-direction: column; }}
.ph {{ display: grid; grid-template-columns: 7.4mm 1fr; gap: 1.8mm; align-items: center; }}
.pn {{ width: 7.4mm; height: 7.4mm; border-radius: 50%; background: var(--c); color: #fff; font-family: InterDisplay, Inter; font-weight: 700;
  font-size: 11pt; display: flex; align-items: center; justify-content: center; }}
.pt {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 9.6pt; line-height: 1.1; }}
.pb {{ font-size: 6pt; color: {MUTED}; margin-top: .3mm; }}
.pl {{ font-size: 7.4pt; font-style: italic; color: {INK}; margin: 1.6mm 0 1.4mm; line-height: 1.32; min-height: 7mm; }}
.ir {{ display: grid; grid-template-columns: 12.5mm 1fr; gap: 1mm; font-size: 6.2pt; line-height: 1.3; padding: .5mm 0; border-top: 1px solid #F1F3F5; }}
.ir span {{ color: {MUTED}; }} .ir b {{ font-weight: 600; color: {INK}; }}
.pm {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.4mm; margin-top: 1.6mm; }}
.pm div {{ position: relative; background: #F6F7F9; border-radius: 6px; padding: .8mm 1.4mm 1.2mm; overflow: hidden; }}
.pm span {{ display: block; font-size: 5.4pt; color: {MUTED}; }}
.pm b {{ font-family: InterDisplay, Inter; font-size: 10.5pt; }}
.pm i {{ position: absolute; left: 0; bottom: 0; height: 1mm; background: var(--c); }}
.pv {{ font-size: 6.2pt; line-height: 1.38; color: {INK2}; margin-top: 1.4mm; }}
.lg {{ position: relative; display: flex; flex-wrap: wrap; gap: 1mm 3.4mm; font-size: 7pt; color: {INK2}; margin: .6mm 0 2mm; }}
.lg .lm {{ color: {MUTED}; flex-basis: 100%; font-size: 6.6pt; }}
.lg i.nb {{ display: inline-flex; align-items: center; justify-content: center; width: 3.4mm; height: 3.4mm; border-radius: 50%; color: #fff; font-style: normal;
  font-size: 5.4pt; font-weight: 700; margin-right: 1.2mm; vertical-align: -.5mm; }}
.p2 {{ position: relative; display: grid; grid-template-columns: 1fr 82mm; gap: 4mm; }}
.g22 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2.6mm; }}
.cw .cmpw {{ padding: 1.6mm 2mm .4mm; }}
.cw .cmpt {{ font-size: 9pt; }}
.cc {{ font-size: 6.6pt; color: {INK2}; margin: .8mm 1mm 0; }}
.flow {{ background: #fff; border: 1px solid #E6EAEE; border-radius: 12px; padding: 3mm 3.4mm; }}
.flow .ct {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 11pt; margin-bottom: 1.6mm; }}
.flow .ct small {{ font-family: Inter; font-weight: 400; font-size: 6.6pt; color: {MUTED}; }}
.fs {{ position: relative; border-left: 2.4px solid {INK}; padding: .4mm 0 1.6mm 3mm; }}
.fn {{ font-family: InterDisplay, Inter; font-weight: 700; font-size: 13pt; line-height: 1.1; }}
.ft {{ font-size: 7.6pt; font-weight: 700; }}
.fx {{ font-size: 6.6pt; color: {INK2}; line-height: 1.35; }}
.cb {{ display: grid; grid-template-columns: 30mm 1fr 9mm; align-items: center; gap: 1.6mm; font-size: 6.8pt; margin: .9mm 0; }}
.cb i {{ display: block; height: 2.6mm; border-radius: 2px; }}
.cb b {{ text-align: right; font-size: 7pt; }}
.cb i.nb {{ display: inline-flex; align-items: center; justify-content: center; width: 3.2mm; height: 3.2mm; border-radius: 50%; color: #fff; font-style: normal;
  font-size: 5pt; font-weight: 700; margin-right: 1mm; vertical-align: -.4mm; }}
.rb.nx {{ background: #fff; border: 1px solid #E6EAEE; }}
.rb {{ font-size: 6.8pt; line-height: 1.4; color: {INK2}; margin-top: 2.4mm; background: #F6F7F9; border-radius: 8px; padding: 1.8mm 2.4mm; }}
"""


def main():
    D, E, C, X, Pn = ir.load()
    P = iv.Parties(D)
    css = vr.CSS + iv.CSS_EXTRA + ir.EXTRA + CSS
    html = f"<!doctype html><html><head><meta charset='utf-8'><title>Los 10 partidos</title><style>{css}</style></head><body>{page1(P, D, E)}{page2(P, D, E, C)}</body></html>"
    hp = ir.W / "infografia_ideologias.html"
    hp.write_text(html, encoding="utf-8")
    subprocess.run([vr.CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={OUT}", f"file://{hp}"], check=True, capture_output=True)
    print(OUT)


if __name__ == "__main__":
    main()
