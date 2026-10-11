"""Reporte HTML interactivo: patrones envío ↔ EPOS. Lee work/epos_patrones.json (correr antes src/epos_patrones.py).
Misma información que src/epos_patrones_report.py (PDF), con filtro por categoría, detalle al pasar el ratón,
tabla de datos bajo cada gráfico y modo oscuro.
Diseño revisado con las skills dataviz (paleta validada, sin doble eje, pequeños múltiplos), design-taste-frontend
y emil-design-eng (movimiento y estados).
Salida: reportes/REPORTE_EPOS_PATRONES.html (un solo archivo; las fuentes se cargan de Google Fonts)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reportes" / "REPORTE_EPOS_PATRONES.html"

HTML = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Patrones EPOS</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* Paleta validada con dataviz/scripts/validate_palette.js:
   claro  #6250D6 / #E3602B -> pasa las 5 comprobaciones; oscuro #8F81F0 / #DD6A36 -> pasa.
   Envío = gris neutro a propósito (serie de comparación, con línea discontinua como segunda codificación). */
:root {
  --bg: #F5F6F7; --paper: #FFFFFF; --ink: #14161A; --ink2: #4B515B; --muted: #7E848E; --line: #DFE2E6; --line2: #EDEFF2;
  --frag: #6250D6; --frag-soft: #EEEBFC; --mu: #E3602B; --mu-soft: #FCEDE6; --ship: #5B6573; --ok: #1B7F5B;
  --shadow: 0 1px 0 rgba(20,22,26,.04), 0 10px 28px -16px rgba(40,48,64,.18);
  --ease: cubic-bezier(.23, 1, .32, 1);
  --display: Geist, Inter, system-ui, sans-serif;
  --sans: Inter, system-ui, -apple-system, "Segoe UI", sans-serif;
  --r: 16px; --rc: 10px;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #111317; --paper: #1A1D22; --ink: #EEF0F3; --ink2: #B6BBC4; --muted: #828894; --line: #2C3038; --line2: #23262D;
    --frag: #8F81F0; --frag-soft: #272347; --mu: #DD6A36; --mu-soft: #3A251C; --ship: #A3AAB5; --ok: #4CC495;
    --shadow: 0 1px 0 rgba(0,0,0,.3), 0 12px 30px -16px rgba(0,0,0,.7);
  }
}
:root[data-theme="dark"] {
  --bg: #111317; --paper: #1A1D22; --ink: #EEF0F3; --ink2: #B6BBC4; --muted: #828894; --line: #2C3038; --line2: #23262D;
  --frag: #8F81F0; --frag-soft: #272347; --mu: #DD6A36; --mu-soft: #3A251C; --ship: #A3AAB5; --ok: #4CC495;
  --shadow: 0 1px 0 rgba(0,0,0,.3), 0 12px 30px -16px rgba(0,0,0,.7);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; scroll-padding-top: 76px; -webkit-text-size-adjust: 100%; }
body { background: var(--bg); color: var(--ink); font-family: var(--sans); font-size: 15px; line-height: 1.55; -webkit-font-smoothing: antialiased; }
b, strong { font-weight: 600; color: var(--ink); }
.wrap { max-width: 1180px; margin: 0 auto; padding: 0 28px; }
#top { position: absolute; top: 0; height: 8px; width: 1px; }

/* barra superior: una línea, 60px */
.bar { position: sticky; top: 0; z-index: 20; background: color-mix(in srgb, var(--bg) 84%, transparent);
  backdrop-filter: saturate(1.4) blur(14px); -webkit-backdrop-filter: saturate(1.4) blur(14px); border-bottom: 1px solid transparent; transition: border-color .2s var(--ease); }
.bar.scrolled { border-bottom-color: var(--line); }
.bar .wrap { display: flex; align-items: center; gap: 18px; height: 60px; }
.brand { font-family: var(--display); font-weight: 600; font-size: 16px; letter-spacing: -.01em; white-space: nowrap; }
.brand span { color: var(--muted); font-weight: 500; }
.nav { display: flex; gap: 2px; }
.nav a { font-size: 13px; color: var(--ink2); text-decoration: none; padding: 6px 10px; border-radius: 8px; white-space: nowrap; transition: color .15s var(--ease), background-color .15s var(--ease); }
.nav a.on { color: var(--ink); background: var(--paper); box-shadow: var(--shadow); }
@media (hover: hover) and (pointer: fine) { .nav a:hover { color: var(--ink); } }
.bar .sp { flex: 1; }
.iconbtn { border: 0; background: none; color: var(--ink2); width: 34px; height: 34px; border-radius: 9px; cursor: pointer; display: grid; place-items: center; transition: transform .16s var(--ease); }
.iconbtn:active { transform: scale(.94); }
@media (hover: hover) and (pointer: fine) { .iconbtn:hover { background: var(--paper); color: var(--ink); } }

/* control segmentado: el único filtro de la página, arriba */
.seg { position: relative; display: inline-flex; background: var(--line2); border-radius: var(--rc); padding: 3px; isolation: isolate; max-width: 100%; }
.seg button { position: relative; z-index: 1; border: 0; background: none; font: inherit; font-size: 13px; font-weight: 500; color: var(--ink2);
  padding: 6px 12px; border-radius: 7px; cursor: pointer; white-space: nowrap; display: inline-flex; align-items: center; gap: 7px;
  transition: color .15s var(--ease), transform .16s var(--ease); }
.seg button[aria-pressed="true"] { color: var(--ink); }
.seg button:active { transform: scale(.97); }
.seg button:focus-visible, .iconbtn:focus-visible, .rule button:focus-visible, [data-tip]:focus-visible { outline: 2px solid var(--frag); outline-offset: 2px; }
.seg .pill { position: absolute; z-index: 0; top: 3px; bottom: 3px; left: 0; border-radius: 7px; background: var(--paper); box-shadow: var(--shadow);
  transition: transform .24s var(--ease), width .24s var(--ease); }
.key { display: inline-block; width: 10px; height: 10px; border-radius: 3px; flex: none; }

/* portada */
.hero { padding: 64px 0 28px; }
.eyebrow { font-size: 12px; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
h1 { font-family: var(--display); font-weight: 600; font-size: clamp(32px, 4.4vw, 54px); line-height: 1.08; letter-spacing: -.035em; margin-top: 14px; max-width: 30ch; text-wrap: balance; }
h1 span { color: var(--muted); }
.lead { font-size: 17px; color: var(--ink2); max-width: 56ch; margin-top: 16px; }
.signal { margin-top: 32px; background: var(--paper); border-radius: var(--r); box-shadow: var(--shadow); padding: 22px 24px 16px; }
.signal-h { display: flex; flex-wrap: wrap; gap: 8px 22px; align-items: baseline; justify-content: space-between; }

/* cifras clave: rejilla asimétrica */
.bento { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 14px; }
.tile { background: var(--paper); border-radius: var(--r); padding: 20px 22px; box-shadow: var(--shadow); text-decoration: none; color: inherit; display: flex; flex-direction: column;
  transition: transform .2s var(--ease); }
.tile.wide { grid-column: span 2; }
.tile.t-frag { background: var(--frag-soft); box-shadow: none; }
.tile.t-mu { background: var(--mu-soft); box-shadow: none; }
@media (hover: hover) and (pointer: fine) { .tile:hover { transform: translateY(-2px); } }
.tile:active { transform: scale(.985); }
.tv { font-family: var(--sans); font-weight: 600; font-size: 34px; line-height: 1.05; letter-spacing: -.03em; }
.tile.wide .tv { font-size: 46px; }
.tk { font-size: 13.5px; font-weight: 600; margin: 10px 0 4px; }
.td { font-size: 13.5px; color: var(--ink2); line-height: 1.5; max-width: 46ch; }

/* secciones */
section.sec { padding: 80px 0 8px; }
h2 { font-family: var(--display); font-weight: 600; font-size: clamp(24px, 2.7vw, 32px); line-height: 1.16; letter-spacing: -.025em; max-width: 32ch; text-wrap: balance; margin-bottom: 26px; }
.grid { display: grid; gap: 16px; }
.g2 { grid-template-columns: 1.3fr 1fr; }
.g2e { grid-template-columns: 1fr 1fr; }
.g3 { grid-template-columns: repeat(3, 1fr); }
.stack { display: flex; flex-direction: column; gap: 16px; min-width: 0; }
.card { background: var(--paper); border-radius: var(--r); box-shadow: var(--shadow); padding: 22px 24px; min-width: 0; }
.ct { font-weight: 600; font-size: 15.5px; letter-spacing: -.005em; }
.cs { font-size: 12.5px; color: var(--muted); margin-top: 2px; }
.fig { font-family: var(--sans); font-weight: 600; font-size: 56px; line-height: 1; letter-spacing: -.035em; margin: 10px 0 12px; }
.kl { font-size: 13.5px; color: var(--ink2); line-height: 1.55; }
.kl + .kl { margin-top: 8px; }
.legend { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: 12.5px; color: var(--ink2); margin: 10px 0 2px; align-items: center; }
.legend span { display: inline-flex; align-items: center; gap: 6px; }
.lk { display: inline-block; width: 16px; height: 0; border-top: 2px solid; }
.lk.d { border-top-style: dashed; }
.ring { width: 10px; height: 10px; border-radius: 50%; border: 2px solid var(--ship); display: inline-block; }
.note { margin-top: 16px; padding: 18px 22px; border-radius: var(--r); background: var(--paper); box-shadow: var(--shadow); font-size: 14px; color: var(--ink2); line-height: 1.6; max-width: 100%; }
.note .tag { display: inline-block; font-size: 12px; font-weight: 600; color: var(--ink); background: var(--line2); padding: 2px 8px; border-radius: 6px; margin-right: 6px; }
details.data { margin-top: 12px; border-top: 1px solid var(--line2); padding-top: 10px; }
details.data summary { cursor: pointer; font-size: 13px; color: var(--muted); list-style: none; display: inline-flex; align-items: center; gap: 6px; user-select: none; }
details.data summary::-webkit-details-marker { display: none; }
details.data summary::before { content: ""; width: 7px; height: 7px; border-right: 1.5px solid currentColor; border-bottom: 1.5px solid currentColor; transform: rotate(-45deg); transition: transform .2s var(--ease); }
details.data[open] summary::before { transform: rotate(45deg); }
details.data .body { font-size: 13px; color: var(--ink2); padding-top: 8px; overflow-x: auto; }
.chart { position: relative; width: 100%; }
.chart svg { display: block; width: 100%; height: auto; overflow: visible; }
.ax { font-family: var(--sans); font-size: 11px; fill: var(--muted); font-variant-numeric: tabular-nums; }
.axl { font-family: var(--sans); font-size: 11.5px; fill: var(--ink2); font-weight: 500; }
.lb { font-family: var(--sans); font-size: 12.5px; fill: var(--ink); font-weight: 600; }
.vl { font-family: var(--sans); font-size: 11.5px; fill: var(--ink2); font-weight: 600; font-variant-numeric: tabular-nums; }
.halo { paint-order: stroke; stroke: var(--paper); stroke-width: 4px; stroke-linejoin: round; }
.gl { stroke: var(--line2); stroke-width: 1; }
.gl0 { stroke: var(--line); stroke-width: 1.2; }
.hit { fill: transparent; }
.col .xh { stroke: var(--ink2); stroke-width: 1; opacity: 0; transition: opacity .12s; }
@media (hover: hover) and (pointer: fine) { .col:hover .xh { opacity: .5; } }
.col:focus-visible .xh { opacity: .5; }
[data-tip] { cursor: default; outline: none; }
.mini { min-width: 0; }
.mini-h { display: flex; justify-content: space-between; align-items: baseline; gap: 8px; }
.mini-h .n { font-weight: 600; font-size: 14px; display: inline-flex; align-items: center; gap: 7px; }
.mini-h .m { font-size: 12px; color: var(--muted); font-variant-numeric: tabular-nums; white-space: nowrap; }

/* tablas */
.tb { width: 100%; border-collapse: collapse; font-size: 13px; }
.tb th { font-size: 11px; text-transform: uppercase; letter-spacing: .05em; color: var(--muted); text-align: left; font-weight: 600; padding: 6px 8px; border-bottom: 1px solid var(--line); white-space: nowrap; }
.tb td { padding: 7px 8px; font-variant-numeric: tabular-nums; white-space: nowrap; }
.tb tbody tr + tr td { border-top: 1px solid var(--line2); }
.tb td.num, .tb th.num { text-align: right; }
.meter { display: inline-flex; align-items: center; gap: 8px; }
.meter i { display: inline-block; height: 6px; border-radius: 3px; }

/* recomendaciones */
.rules { display: flex; flex-direction: column; gap: 10px; }
.rule { background: var(--paper); border-radius: var(--r); box-shadow: var(--shadow); overflow: hidden; }
.rule button { all: unset; box-sizing: border-box; width: 100%; display: grid; grid-template-columns: 34px 1fr 18px; gap: 14px; align-items: center; padding: 16px 20px; cursor: pointer; border-radius: var(--r); }
.rn { width: 32px; height: 32px; border-radius: 50%; background: var(--line2); color: var(--ink); display: grid; place-items: center; font-weight: 600; font-size: 14px; }
.rt { font-weight: 600; font-size: 15.5px; }
.rs { font-size: 13.5px; color: var(--ink2); margin-top: 2px; }
.chev { color: var(--muted); transition: transform .22s var(--ease); }
.rule.open .chev { transform: rotate(180deg); }
.rd { display: grid; grid-template-rows: 0fr; transition: grid-template-rows .24s var(--ease); }
.rule.open .rd { grid-template-rows: 1fr; }
.rd > div { overflow: hidden; }
.rd .in { padding: 0 20px 18px 68px; font-size: 13.5px; color: var(--ink2); }
.rd .in a { color: var(--ink2); }

.foot { margin: 80px 0 0; padding: 28px 0 60px; border-top: 1px solid var(--line); display: grid; grid-template-columns: repeat(4, 1fr); gap: 22px; font-size: 13px; color: var(--ink2); }
.foot b { display: block; margin-bottom: 4px; }
.foot code { font-size: 12px; background: var(--line2); padding: 1px 5px; border-radius: 4px; }

/* detalle al pasar el ratón: el valor manda, la serie acompaña */
#tip { position: fixed; z-index: 50; pointer-events: none; background: var(--ink); color: var(--bg); font-size: 12.5px; line-height: 1.45; padding: 9px 12px; border-radius: 10px;
  min-width: 170px; max-width: 270px; opacity: 0; transform: scale(.97); transition: opacity .125s var(--ease), transform .125s var(--ease); box-shadow: 0 12px 30px -10px rgba(0,0,0,.45); }
#tip.on { opacity: 1; transform: none; }
#tip.instant { transition: none; }
#tip .h { opacity: .7; margin-bottom: 4px; font-size: 12px; }
#tip .r { display: flex; justify-content: space-between; align-items: center; gap: 16px; }
#tip .r .k { display: inline-flex; align-items: center; gap: 7px; opacity: .78; }
#tip .r .k i { display: inline-block; width: 12px; height: 0; border-top: 2px solid; }
#tip .r .v { font-weight: 600; font-variant-numeric: tabular-nums; }
#tip .f { opacity: .6; margin-top: 4px; font-size: 11.5px; }

/* aparición al entrar en pantalla (una vez por sección; explica la lectura del gráfico) */
.reveal { opacity: 0; transform: translateY(12px); transition: opacity .6s var(--ease), transform .6s var(--ease); }
.reveal.in { opacity: 1; transform: none; }
.draw { stroke-dasharray: 1; stroke-dashoffset: 1; }
.in .draw { stroke-dashoffset: 0; transition: stroke-dashoffset 1.2s var(--ease) .1s; }
.grow { transform-box: fill-box; transform-origin: 50% 100%; transform: scaleY(.0001); }
.growx { transform-box: fill-box; transform-origin: 0 50%; transform: scaleX(.0001); }
.in .grow, .in .growx { transform: none; transition: transform .7s var(--ease); }
.drawn .draw, .drawn .grow, .drawn .growx { transition: none; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .reveal { transform: none; transition: opacity .3s ease; }
  .draw, .in .draw { stroke-dashoffset: 0; transition: none; }
  .grow, .growx { transform: none !important; transition: none !important; }
  .seg .pill, .tile, .rd, .chev, #tip { transition-property: opacity; }
}

@media (max-width: 1200px) { .nav { display: none; } }
@media (max-width: 900px) {
  .g2, .g2e { grid-template-columns: 1fr; }
  .g3 { grid-template-columns: 1fr 1fr; }
  .bento { grid-template-columns: 1fr 1fr; }
  .foot { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 600px) {
  .wrap { padding: 0 16px; }
  body { font-size: 14.5px; }
  .g3, .bento { grid-template-columns: 1fr; }
  .tile.wide { grid-column: auto; }
  .card { padding: 18px 16px; }
  .signal { padding: 16px 14px 10px; }
  .foot { grid-template-columns: 1fr; }
  .rd .in { padding-left: 20px; }
  .brand { display: none; }
  .tb th, .tb td { white-space: normal; padding: 6px 5px; }
  .bar .wrap { gap: 8px; }
  .seg button { padding: 6px 9px; }
  .hero { padding-top: 40px; }
  .fig { font-size: 48px; }
}
</style>
</head>
<body>
<div id="top"></div>
<div id="tip" role="tooltip"></div>

<header class="bar" id="bar">
  <div class="wrap">
    <div class="brand">Patrones EPOS <span>· foto sep-26</span></div>
    <nav class="nav" id="nav" aria-label="Secciones">
      <a href="#ruido">Ruido</a><a href="#tendencia">Tendencia</a><a href="#lanzamientos">Lanzamientos</a>
      <a href="#ciclo">Ciclo de vida</a><a href="#carga">Carga y bajas</a><a href="#forecast">Forecast</a>
    </nav>
    <div class="sp"></div>
    <div class="seg" id="catSeg" role="group" aria-label="Filtrar por categoría">
      <button data-v="all" aria-pressed="true">Todas</button>
      <button data-v="Fragancias" aria-pressed="false"><i class="key" style="background:var(--frag)"></i>Fragancias</button>
      <button data-v="Makeup" aria-pressed="false"><i class="key" style="background:var(--mu)"></i>Makeup</button>
    </div>
    <button class="iconbtn" id="theme" aria-label="Cambiar entre modo claro y oscuro" title="Modo claro u oscuro">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
    </button>
  </div>
</header>

<main class="wrap">
  <section class="hero">
    <div class="eyebrow">Envío y EPOS en 5 casas</div>
    <h1>El consumidor compra a ritmo constante. <span>El ruido lo meten los pedidos.</span></h1>
    <p class="lead">Seis patrones entre envío (sell-in) y EPOS (sell-out), jul-24 a ago-26. Cada EAN se compara consigo mismo.</p>
    <div class="signal reveal">
      <div class="signal-h">
        <div><div class="ct" id="sigT"></div><div class="cs">Crecimiento de cada mes frente al mismo mes del año anterior, EANs maduros</div></div>
        <div class="legend" style="margin:0"><span><i class="lk d" style="border-color:var(--ship)"></i>Envío</span><span><i class="lk" style="border-color:var(--frag)"></i>EPOS</span></div>
      </div>
      <div class="chart" id="cHero"></div>
    </div>
    <div class="bento" id="tiles"></div>
  </section>

  <section class="sec" id="ruido">
    <h2 class="reveal" id="h-ruido"></h2>
    <div class="card reveal">
      <div class="ct">Crecimiento mensual frente al año anterior, casa a casa</div>
      <div class="cs">jul-25 a jul-26. Misma escala en todas las casas. Pasa el ratón por un mes para ver las cifras.</div>
      <div class="legend"><span><i class="lk d" style="border-color:var(--ship)"></i>Envío</span><span><i class="lk" style="border-color:var(--frag)"></i>EPOS fragancias</span><span><i class="lk" style="border-color:var(--mu)"></i>EPOS makeup</span></div>
      <div class="grid g3" id="cNoise" style="margin-top:8px"></div>
      <details class="data"><summary>Ver datos</summary><div class="body" id="tNoise"></div></details>
    </div>
    <div class="grid g2" style="margin-top:16px">
      <div class="card reveal">
        <div class="ct">Distancia entre el mejor y el peor mes</div>
        <div class="cs">Puntos de crecimiento, jul-25 a jul-26</div>
        <div class="legend"><span><i class="key" style="background:var(--ship)"></i>Envío</span><span><i class="key" style="background:var(--frag)"></i><i class="key" style="background:var(--mu);margin-left:-4px"></i>EPOS</span></div>
        <div class="chart" id="cRange"></div>
      </div>
      <div class="card reveal">
        <div class="ct">EANs cuyo envío es más inestable que su EPOS</div>
        <div class="fig" id="kNoise"></div>
        <div class="kl" id="kNoiseL"></div>
        <div class="kl" id="n-ruido" style="margin-top:14px"></div>
      </div>
    </div>
  </section>

  <section class="sec" id="tendencia">
    <h2 class="reveal" id="h-trend"></h2>
    <div class="grid g2">
      <div class="card reveal">
        <div class="ct">Cada punto es un EAN: crecimiento FY26 del EPOS frente al del envío</div>
        <div class="cs" id="scSub"></div>
        <div class="legend"><span><i class="key" style="background:var(--frag);border-radius:50%"></i>Fragancias</span><span><i class="key" style="background:var(--mu);border-radius:50%"></i>Makeup</span><span style="color:var(--muted)">Zona sombreada: misma dirección</span></div>
        <div class="chart" id="cScatter"></div>
        <details class="data"><summary>Cómo se calcula</summary><div class="body">Crecimiento = suma FY26 / suma FY25 - 1, por EAN, de envío y de EPOS. EANs maduros (lanzados antes de ene-24) con envío y EPOS en los dos años.
          Los valores se recortan a -80% y +150% para que el gráfico se lea; el tamaño del punto es el envío FY25. El resumen por casa está en la tabla de la derecha.</div></details>
      </div>
      <div class="stack">
        <div class="card reveal">
          <div class="ct">Envío y EPOS van en la misma dirección</div>
          <div class="fig" id="kSame"></div>
          <div class="kl" id="kSameL"></div>
          <div style="overflow-x:auto;margin-top:12px"><table class="tb" id="tbHouse"></table></div>
        </div>
        <div class="card reveal">
          <div class="ct">¿La tendencia de jul-dic sigue en ene-jun?</div>
          <div class="cs">% de EANs que mantienen el signo de su crecimiento</div>
          <div class="legend"><span><i class="key" style="background:var(--ink2)"></i>EPOS (color de la categoría)</span><span><i class="key" style="background:var(--ship);opacity:.5"></i>Envío</span></div>
          <div class="chart" id="cPersist"></div>
          <div class="kl" id="kPersistL"></div>
        </div>
      </div>
    </div>
  </section>

  <section class="sec" id="lanzamientos">
    <h2 class="reveal" id="h-launch"></h2>
    <div class="grid g2e" id="launchGrid"></div>
    <div class="grid g2" style="margin-top:16px">
      <div class="note reveal" id="n-launch" style="margin-top:0"></div>
      <div class="note reveal" style="margin-top:0"><span class="tag">Pregunta abierta</span>¿Los envíos de lanzamiento incluyen probadores o material de exposición? Si es así, parte del «doble» no es stock vendible.</div>
    </div>
  </section>

  <section class="sec" id="ciclo">
    <h2 class="reveal" id="h-vet"></h2>
    <div class="grid g2">
      <div class="card reveal">
        <div class="ct">EPOS FY26 frente a FY25: veteranos activos frente al total de la casa</div>
        <div class="cs">Veteranos: con envío desde jul-23 y todavía activos</div>
        <div class="legend"><span><i class="key" style="background:var(--frag)"></i><i class="key" style="background:var(--mu);margin-left:-4px"></i>Veteranos</span><span><i class="key" style="background:var(--ship);opacity:.45"></i>Total de la casa (con lanzamientos)</span></div>
        <div class="chart" id="cVet"></div>
        <details class="data"><summary>Ver datos</summary><div class="body" id="tVet"></div></details>
      </div>
      <div class="stack" id="cohortStack"></div>
    </div>
    <div class="note reveal" id="n-vet"></div>
  </section>

  <section class="sec" id="carga">
    <h2 class="reveal" id="h-load"></h2>
    <div class="grid g2e">
      <div class="card reveal">
        <div class="ct">Envío de los 3 meses siguientes: EANs cargados frente a normales</div>
        <div class="cs">Exceso de crecimiento del envío sobre el del EPOS, cortes sep-25 a abr-26</div>
        <div class="legend"><span><i class="key" style="background:var(--frag);border-radius:50%"></i><i class="key" style="background:var(--mu);border-radius:50%;margin-left:-4px"></i>Cargados</span><span><i class="ring"></i>Normales</span><span style="color:var(--muted)">Derecha: meses en que cargados &lt; normales</span></div>
        <div class="chart" id="cDumb"></div>
        <div class="kl" id="kDumbL" style="margin-top:6px"></div>
        <details class="data"><summary>Qué es «cargado»</summary><div class="body">Un EAN está cargado cuando su relación envío/EPOS de los últimos 12 meses está más de un 15% por encima de la suya de FY25: ha enviado más de lo que el consumidor ha comprado.
          Se compara cada EAN consigo mismo, nunca en unidades.</div></details>
      </div>
      <div class="card reveal">
        <div class="ct">Bajas: el consumidor sigue comprando después del último envío</div>
        <div class="cs" id="exitSub"></div>
        <div class="legend" id="exitLeg"></div>
        <div class="chart" id="cExit"></div>
        <div class="kl" id="kExitL" style="margin-top:6px"></div>
        <details class="data"><summary>Ver datos</summary><div class="body" id="tExit"></div></details>
      </div>
    </div>
    <div class="card reveal" style="margin-top:16px">
      <div class="ct">La casa mes a mes: carga acumulada y lo que pasa después</div>
      <div class="cs">Arriba, envío por unidad de EPOS en 12 meses. Abajo, crecimiento del envío de los 3 meses siguientes frente al año anterior. El nivel del ratio depende de qué clientes reportan: importa si sube o baja.</div>
      <div class="grid g3" id="cLoad" style="margin-top:12px"></div>
      <details class="data"><summary>Ver datos</summary><div class="body" id="tLoad"></div></details>
    </div>
    <div class="note reveal"><span class="tag">Gucci Make up</span>A nivel casa acumuló carga 9 meses sin dejar de enviar por encima del EPOS y corrigió de golpe en may-jul-26.
      <b>La carga avisa, pero no dice cuándo llega la corrección.</b> El WOS (semanas de stock) lo diría.</div>
  </section>

  <section class="sec" id="forecast">
    <h2 class="reveal">El EPOS no sirve como número, pero sí como brújula: marca la dirección, la edad del producto y si el canal está lleno</h2>
    <div class="grid g2">
      <div class="rules reveal" id="rules"></div>
      <div class="stack">
        <div class="card reveal"><div class="ct">Por qué solo en relativo</div>
          <div class="kl" style="margin-top:8px">No todos los clientes reportan EPOS (suman ~80% del envío). Por eso todo el reporte compara cada EAN o casa consigo mismo: frente al año anterior o frente a su propia relación envío/EPOS. El nivel absoluto no se usa nunca.</div></div>
        <div class="card reveal"><div class="ct">Qué falta para cerrar el círculo</div>
          <div class="kl" style="margin-top:8px"><b>WOS</b> (semanas de stock) por EAN y cliente: stock = WOS × venta semanal. Convierte «cargado» en un dato y diría cuándo llega la corrección.</div>
          <div class="kl"><b>Probadores y material de exposición:</b> saber si están en el envío de lanzamiento.</div>
          <div class="kl"><b>Más historia de EPOS:</b> hoy hay 2 años (jul-24 a jul-26); cada mes nuevo refuerza o desmiente estos patrones.</div></div>
        <div class="note reveal" style="margin-top:0"><span class="tag">Siguiente paso</span>Probar los puntos 1 a 3 como partido «Consumidor (EPOS)» en el parlamento, con cortes oct-25 a mar-26 y lo real hasta ago-26.</div>
      </div>
    </div>
  </section>

  <footer class="foot">
    <div><b>Envío</b>Sell-in de la foto sep-26 (actuals), jul-23 a ago-26.</div>
    <div><b>EPOS</b>Venta al consumidor de los clientes que reportan (~80% del envío), jul-24 a jul-26.</div>
    <div><b>Cómo se compara</b>Siempre en relativo: crecimiento frente al año anterior o relación envío/EPOS frente a la propia historia del EAN.</div>
    <div><b>Datos y cálculo</b>DATA.xlsx, GUMU.xlsx y KYMU.xlsx (foto sep-26). <code>src/epos_patrones.py</code> y <code>src/epos_patrones_html.py</code></div>
  </footer>
</main>

<script>
const D = __DATA__;
const HOUSES = ["BURBERRY", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"];
const CAT = {"BURBERRY": "Fragancias", "Gucci": "Fragancias", "Marc Jacobs": "Fragancias", "Gucci Make up": "Makeup", "Kylie Makeup": "Makeup"};
const nm = h => h === "BURBERRY" ? "Burberry" : h;
const MESES = {Jan: "ene", Feb: "feb", Mar: "mar", Apr: "abr", May: "may", Jun: "jun", Jul: "jul", Aug: "ago", Sep: "sep", Oct: "oct", Nov: "nov", Dec: "dic"};
const mes = m => { const [a, b] = m.split("-"); return MESES[a] + "-" + b; };
const cssv = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const col = c => c === "Fragancias" ? "var(--frag)" : "var(--mu)";
const colRaw = c => cssv(c === "Fragancias" ? "--frag" : "--mu");
const colH = h => col(CAT[h]);
const pc = (x, s = true) => { const r = Math.round(x * 100); if (r === 0) return "0%"; return (r < 0 ? "−" : (s ? "+" : "")) + Math.abs(r) + "%"; };
const pp = x => Math.round(x * 100) + "%";
const dec = (x, d) => x.toFixed(d).replace(".", ",");
const lerp = (v, a, b, A, B) => A + (v - a) / (b - a) * (B - A);
const esc = s => String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
const units = x => Math.round(x).toLocaleString("es-ES");
const $ = id => document.getElementById(id);

/* detalle: valor fuerte, serie con clave de línea */
const T = {
  h: t => `<div class='h'>${t}</div>`,
  r: (k, v, c) => `<div class='r'><span class='k'>${c ? `<i style='border-color:${c}'></i>` : ""}${k}</span><span class='v'>${v}</span></div>`,
  f: t => `<div class='f'>${t}</div>`,
};

let state = { cat: "all" };
const housesIn = () => HOUSES.filter(h => state.cat === "all" || CAT[h] === state.cat);
const catsIn = () => state.cat === "all" ? ["Fragancias", "Makeup"] : [state.cat];
const W = el => Math.max(240, el.clientWidth);
const poly = (pts, color, w, extra = "") => `<polyline points="${pts.map(p => p.join(",")).join(" ")}" fill="none" stroke="${color}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round" ${extra}/>`;
const dot = (x, y, c) => `<circle cx="${x}" cy="${y}" r="4" fill="${c}" stroke="var(--paper)" stroke-width="2"/>`;
function yAxis(x0, x1, y0, y1, lo, hi, ticks, fmt) {
  return ticks.map(t => { const y = lerp(t, lo, hi, y1, y0), z = Math.abs(t) < 1e-9;
    return `<line x1="${x0}" x2="${x1}" y1="${y}" y2="${y}" class="${z ? "gl0" : "gl"}"/><text x="${x0 - 8}" y="${y + 4}" text-anchor="end" class="ax">${fmt(t)}</text>`; }).join("");
}
function table(head, rows, numFrom = 1) {
  return `<table class="tb"><thead><tr>${head.map((h, i) => `<th class="${i >= numFrom ? "num" : ""}">${h}</th>`).join("")}</tr></thead><tbody>` +
    rows.map(r => `<tr>${r.map((c, i) => `<td class="${i >= numFrom ? "num" : ""}">${c}</td>`).join("")}</tr>`).join("") + "</tbody></table>";
}
/* columnas de mes con crosshair: el lector apunta a una fecha, no a una línea */
function cols(X, n, y0, y1, bw, tipFn) {
  let s = "";
  for (let i = 0; i < n; i++) s += `<g class="col" tabindex="0" data-tip="${esc(tipFn(i))}"><line class="xh" x1="${X(i)}" x2="${X(i)}" y1="${y0}" y2="${y1}"/><rect class="hit" x="${X(i) - bw / 2}" y="${y0}" width="${bw}" height="${y1 - y0}"/></g>`;
  return s;
}

/* ---------- ruido ---------- */
function noiseSVG(h, w, H, opt = {}) {
  const d = D.noise.houses[h], months = D.noise.months, n = months.length;
  const x0 = 40, x1 = w - (opt.labels ? 64 : 8), y0 = 10, y1 = H - 24, lo = -.8, hi = .8;
  const X = i => lerp(i, 0, n - 1, x0, x1), Y = v => lerp(Math.max(lo, Math.min(hi, v)), lo, hi, y1, y0), c = colH(h);
  let s = `<svg viewBox="0 0 ${w} ${H}" role="img" aria-label="Envío y EPOS de ${nm(h)}, crecimiento mensual">`;
  s += yAxis(x0, x1, y0, y1, lo, hi, opt.small ? [-.8, 0, .8] : [-.8, -.4, 0, .4, .8], t => pc(t));
  const step = w < 360 ? 6 : (w < 560 ? 3 : 2);
  months.forEach((m, i) => { if (i % step === 0) s += `<text x="${X(i)}" y="${H - 6}" text-anchor="middle" class="ax">${mes(m)}</text>`; });
  const band = d.ship.map((v, i) => [X(i), Y(v)]).concat(d.epos.map((v, i) => [X(i), Y(v)]).reverse());
  s += `<polygon points="${band.map(p => p.join(",")).join(" ")}" fill="${c}" opacity=".07"/>`;
  s += poly(d.ship.map((v, i) => [X(i), Y(v)]), "var(--ship)", 1.6, `stroke-dasharray="5 4"`);
  s += poly(d.epos.map((v, i) => [X(i), Y(v)]), c, 2, `class="draw" pathLength="1"`);
  if (!opt.small) d.epos.forEach((v, i) => { s += dot(X(i), Y(v), c); });
  if (opt.labels) {
    let ys = Y(d.ship[n - 1]), ye = Y(d.epos[n - 1]);
    if (Math.abs(ys - ye) < 16) { const m = (ys + ye) / 2, up = d.ship[n - 1] >= d.epos[n - 1]; ys = m + (up ? -8 : 8); ye = m + (up ? 8 : -8); }
    s += `<text x="${x1 + 10}" y="${ys + 4}" class="lb">Envío</text><text x="${x1 + 10}" y="${ye + 4}" class="lb">EPOS</text>`;
  }
  s += cols(X, n, y0, y1, (x1 - x0) / (n - 1), i => T.h(`${nm(h)}, ${mes(months[i])}`) + T.r("EPOS", pc(d.epos[i]), colRaw(CAT[h])) + T.r("Envío", pc(d.ship[i]), cssv("--ship")));
  return s + "</svg>";
}
function drawHero() {
  const el = $("cHero"), w = W(el);
  $("sigT").textContent = "Burberry: el EPOS se mueve en una franja estrecha; el envío salta";
  el.innerHTML = noiseSVG("BURBERRY", w, Math.round(Math.min(280, Math.max(200, w * .27))), { labels: true });
}
function drawNoise() {
  const box = $("cNoise"), hs = housesIn();
  box.innerHTML = hs.map(h => `<div class="mini"><div class="mini-h"><span class="n"><i class="key" style="background:${colH(h)}"></i>${nm(h)}</span>
    <span class="m">rango ${Math.round(D.noise.rango[h].ship * 100)} vs ${Math.round(D.noise.rango[h].epos * 100)} pts</span></div><div class="chart"></div></div>`).join("");
  box.querySelectorAll(".chart").forEach((el, i) => { const w = W(el); el.innerHTML = noiseSVG(hs[i], w, Math.round(Math.max(150, w * .52)), { small: true }); });
  const months = D.noise.months;
  $("tNoise").innerHTML = table(["Mes", ...hs.flatMap(h => [nm(h) + " envío", nm(h) + " EPOS"])], months.map((m, i) => [mes(m), ...hs.flatMap(h => [pc(D.noise.houses[h].ship[i]), pc(D.noise.houses[h].epos[i])])]));
}
function rangeChart(el) {
  const hs = housesIn(), w = W(el), rowH = 46, H = hs.length * rowH + 28, x0 = Math.min(116, w * .3), x1 = w - 40, hi = 1.2;
  let s = `<svg viewBox="0 0 ${w} ${H}">`;
  [0, .4, .8, 1.2].forEach(t => { const x = lerp(t, 0, hi, x0, x1); s += `<line x1="${x}" x2="${x}" y1="2" y2="${H - 22}" class="gl"/><text x="${x}" y="${H - 6}" text-anchor="middle" class="ax">${Math.round(t * 100)}</text>`; });
  hs.forEach((h, i) => {
    const r = D.noise.rango[h], y = 8 + i * rowH, c = colH(h), L = v => lerp(v, 0, hi, 0, x1 - x0);
    const tip = T.h(nm(h)) + T.r("Rango envío", Math.round(r.ship * 100) + " pts", cssv("--ship")) + T.r("Rango EPOS", Math.round(r.epos * 100) + " pts", colRaw(CAT[h])) + T.f(`${D.noise.houses[h].n} EANs maduros`);
    s += `<g tabindex="0" data-tip="${esc(tip)}"><rect class="hit" x="0" y="${y - 4}" width="${w}" height="${rowH - 6}"/>`;
    s += `<text x="${x0 - 10}" y="${y + 15}" text-anchor="end" class="lb">${nm(h)}</text>`;
    s += `<rect class="growx" x="${x0}" y="${y}" width="${L(r.ship)}" height="11" rx="4" fill="var(--ship)"/><text x="${x0 + L(r.ship) + 6}" y="${y + 10}" class="vl">${Math.round(r.ship * 100)}</text>`;
    s += `<rect class="growx" x="${x0}" y="${y + 13}" width="${L(r.epos)}" height="11" rx="4" fill="${c}"/><text x="${x0 + L(r.epos) + 6}" y="${y + 23}" class="vl">${Math.round(r.epos * 100)}</text></g>`;
  });
  el.innerHTML = s + "</svg>";
}

/* ---------- tendencia ---------- */
let scatterPts = [];
function scatter(el) {
  const pts = D.trend.points.filter(p => state.cat === "all" || p.cat === state.cat);
  const w = W(el), H = Math.round(Math.min(470, Math.max(300, w * .78))), x0 = 62, x1 = w - 10, y0 = 10, y1 = H - 40, lo = -.8, hi = 1.5;
  const X = v => lerp(v, lo, hi, x0, x1), Y = v => lerp(v, lo, hi, y1, y0);
  let s = `<svg viewBox="0 0 ${w} ${H}" role="img" aria-label="Crecimiento de EPOS frente a envío por EAN">`;
  s += `<rect x="${X(0)}" y="${y0}" width="${x1 - X(0)}" height="${Y(0) - y0}" fill="var(--line2)" opacity=".75"/><rect x="${x0}" y="${Y(0)}" width="${X(0) - x0}" height="${y1 - Y(0)}" fill="var(--line2)" opacity=".75"/>`;
  const ticks = [-.5, 0, .5, 1, 1.5];
  s += yAxis(x0, x1, y0, y1, lo, hi, ticks, t => pc(t));
  ticks.forEach(t => { s += `<line x1="${X(t)}" x2="${X(t)}" y1="${y0}" y2="${y1}" class="${t === 0 ? "gl0" : "gl"}"/><text x="${X(t)}" y="${y1 + 16}" text-anchor="middle" class="ax">${pc(t)}</text>`; });
  s += `<line x1="${X(lo)}" y1="${Y(lo)}" x2="${X(hi)}" y2="${Y(hi)}" stroke="var(--muted)" stroke-width="1" opacity=".6"/>`;
  s += `<text x="${X(1.12)}" y="${Y(1.2) - 6}" class="ax halo" text-anchor="middle">envío = EPOS</text>`;
  if (w >= 460) s += `<text x="${X(1.45)}" y="${Y(-.7)}" class="ax" text-anchor="end">EPOS crece, envío cae</text><text x="${X(-.75)}" y="${Y(1.38)}" class="ax">envío crece, EPOS cae</text>`;
  scatterPts = [...pts].sort((a, b) => b.w - a.w).map(p => ({ ...p, cx: X(p.x), cy: Y(p.y), r: Math.max(3, Math.min(10, Math.sqrt(p.w) / 10)) }));
  scatterPts.forEach((p, i) => { s += `<circle data-i="${i}" cx="${p.cx}" cy="${p.cy}" r="${p.r}" fill="${col(p.cat)}" fill-opacity=".55" stroke="var(--paper)" stroke-width="1"/>`; });
  s += `<circle id="scHi" r="0" fill="none" stroke="var(--ink)" stroke-width="1.5" pointer-events="none"/>`;
  s += `<text x="${(x0 + x1) / 2}" y="${H - 4}" text-anchor="middle" class="axl">EPOS FY26 vs FY25 →</text>`;
  s += `<text x="10" y="${(y0 + y1) / 2}" text-anchor="middle" class="axl" transform="rotate(-90 10 ${(y0 + y1) / 2})">Envío FY26 vs FY25 →</text>`;
  el.innerHTML = s + "</svg>";
  $("scSub").textContent = `${pts.length} EANs maduros. Tamaño = envío FY25. Acerca el ratón a un punto.`;
  const svg = el.querySelector("svg"), hi_ = $("scHi");
  svg.onpointermove = e => {
    const r = svg.getBoundingClientRect(), k = w / r.width, mx = (e.clientX - r.left) * k, my = (e.clientY - r.top) * k;
    let best = null, bd = 24 * k;
    scatterPts.forEach(p => { const d = Math.hypot(p.cx - mx, p.cy - my) - p.r; if (d < bd) { bd = d; best = p; } });
    if (!best) { hi_.setAttribute("r", 0); hideTip(); return; }
    hi_.setAttribute("cx", best.cx); hi_.setAttribute("cy", best.cy); hi_.setAttribute("r", best.r + 2);
    const same = Math.sign(best.x) === Math.sign(best.y);
    showTip(T.h(`${best.cat}, EAN maduro`) + T.r("EPOS FY26 vs FY25", pc(best.x)) + T.r("Envío FY26 vs FY25", pc(best.y)) + T.r("Envío FY25", units(best.w) + " uds") + T.f(same ? "Misma dirección" : "Dirección contraria"), e.clientX, e.clientY);
  };
  svg.onpointerleave = () => { hi_.setAttribute("r", 0); hideTip(); };
}
function houseTable() {
  const hs = housesIn(), B = D.trend.by_house;
  $("tbHouse").innerHTML = `<thead><tr><th>Casa</th><th class="num">EANs</th><th>Misma dirección</th><th class="num">Correlación</th></tr></thead><tbody>` +
    hs.map(h => `<tr><td><span class="meter"><i class="key" style="background:${colH(h)}"></i>${nm(h)}</span></td><td class="num">${B[h].n}</td>
    <td><span class="meter"><i style="width:${Math.round(B[h].same * 70)}px;background:${colH(h)}"></i>${pp(B[h].same)}</span></td><td class="num">${dec(B[h].corr, 2)}</td></tr>`).join("") + "</tbody>";
}
function persistChart(el) {
  const P = D.trend.persist, rows = state.cat === "all" ? ["Total", "Fragancias", "Makeup"] : [state.cat];
  const w = W(el), rowH = 50, H = rows.length * rowH + 24, x0 = 92, x1 = w - 42, L = v => lerp(v, 0, 1, 0, x1 - x0);
  let s = `<svg viewBox="0 0 ${w} ${H}">`;
  [0, .25, .5, .75, 1].forEach(t => { const x = lerp(t, 0, 1, x0, x1); s += `<line x1="${x}" x2="${x}" y1="2" y2="${H - 20}" class="gl"/><text x="${x}" y="${H - 5}" text-anchor="middle" class="ax">${pp(t)}</text>`; });
  rows.forEach((r, i) => {
    const p = P[r], y = 6 + i * rowH, c = r === "Total" ? "var(--ink2)" : col(r);
    const tip = T.h(`${r}, ${p.n} EANs`) + T.r("Mantienen signo, EPOS", pp(p.keep_epos)) + T.r("Mantienen signo, envío", pp(p.keep_ship)) + T.r("Correlación EPOS", dec(p.corr_epos, 2)) + T.r("Correlación envío", dec(p.corr_ship, 2));
    s += `<g tabindex="0" data-tip="${esc(tip)}"><rect class="hit" x="0" y="${y - 4}" width="${w}" height="${rowH - 6}"/><text x="${x0 - 10}" y="${y + 17}" text-anchor="end" class="lb">${r}</text>`;
    s += `<rect class="growx" x="${x0}" y="${y}" width="${L(p.keep_epos)}" height="14" rx="4" fill="${c}"/><text x="${x0 + L(p.keep_epos) + 6}" y="${y + 11}" class="vl">${pp(p.keep_epos)}</text>`;
    s += `<rect class="growx" x="${x0}" y="${y + 17}" width="${L(p.keep_ship)}" height="14" rx="4" fill="var(--ship)" opacity=".5"/><text x="${x0 + L(p.keep_ship) + 6}" y="${y + 28}" class="vl">${pp(p.keep_ship)}</text></g>`;
  });
  el.innerHTML = s + "</svg>";
}

/* ---------- lanzamientos: una ficha por categoría ---------- */
function launchSVG(c, w) {
  const x = D.launch[c], H = Math.round(Math.min(280, Math.max(210, w * .5))), x0 = 40, x1 = w - 6, y0 = 16, y1 = H - 38, hi = .7, n = x.ship.length, bw = (x1 - x0) / n;
  let s = `<svg viewBox="0 0 ${w} ${H}" role="img" aria-label="Envío y EPOS en los 13 primeros meses, ${c}">`;
  s += yAxis(x0, x1, y0, y1, 0, hi, [0, .2, .4, .6], t => pp(t));
  for (let i = 0; i < n; i++) {
    const cx = x0 + bw * i;
    const tip = T.h(`${c}, mes ${i} desde el lanzamiento`) + T.r("Envío", dec(x.ship[i] * 100, 1) + "%", cssv("--ship")) + T.r("EPOS", dec(x.epos[i] * 100, 1) + "%", colRaw(c)) + T.f("% de lo que el consumidor compra en 13 meses");
    s += `<g tabindex="0" data-tip="${esc(tip)}"><rect class="hit" x="${cx}" y="${y0}" width="${bw}" height="${y1 - y0 + 18}"/>`;
    [[x.ship[i], "var(--ship)"], [x.epos[i], col(c)]].forEach(([v, cc], k) => {
      const h = lerp(Math.min(v, hi), 0, hi, 0, y1 - y0);
      s += `<rect class="grow" style="transition-delay:${i * 30}ms" x="${cx + bw * .14 + k * bw * .37}" y="${y1 - h}" width="${bw * .34}" height="${Math.max(h, .5)}" rx="3" fill="${cc}"/>`;
    });
    s += `<text x="${cx + bw / 2}" y="${y1 + 15}" text-anchor="middle" class="ax">${i}</text></g>`;
    if (x.ship[i] > .3) s += `<text x="${cx + bw * .31}" y="${lerp(Math.min(x.ship[i], hi), 0, hi, y1, y0) - 6}" text-anchor="middle" class="vl">${pp(x.ship[i])}</text>`;
  }
  s += `<text x="${(x0 + x1) / 2}" y="${H - 3}" text-anchor="middle" class="axl">meses desde el lanzamiento</text>`;
  return s + "</svg>";
}
function ratioSVG(c, w) {
  const x = D.launch[c], hi = 2.8, x0 = Math.min(150, w * .4), x1 = w - 48, L = v => lerp(v, 0, hi, 0, x1 - x0);
  const rows = [["Año 1 (meses 0-11)", x.y1, col(c), 1], ["Año 2 (meses 12-19)", x.y2, col(c), .5], ["Veteranos", x.vet_ratio, "var(--ship)", 1]];
  const H = rows.length * 34 + 6, xv = x0 + L(x.vet_ratio);
  let s = `<svg viewBox="0 0 ${w} ${H}" role="img" aria-label="Envío por unidad vendida, ${c}">`;
  rows.forEach(([lab, v, cc, op], i) => {
    const y = 6 + i * 34;
    s += `<text x="${x0 - 10}" y="${y + 13}" text-anchor="end" class="lb">${lab}</text><rect class="growx" x="${x0}" y="${y}" width="${L(v)}" height="18" rx="4" fill="${cc}" fill-opacity="${op}"/>`;
    s += `<text x="${x0 + L(v) + 7}" y="${y + 13}" class="vl" style="fill:var(--ink)">${dec(v, 2)}×</text>`;
  });
  s += `<line x1="${xv}" x2="${xv}" y1="0" y2="${H}" stroke="var(--ink2)" stroke-width="1" opacity=".5"/>`;
  return s + "</svg>";
}
function drawLaunch() {
  const g = $("launchGrid"), cs = catsIn();
  g.style.gridTemplateColumns = cs.length === 1 ? "1fr" : "";
  g.innerHTML = cs.map(c => { const x = D.launch[c], e2 = x.epos_y2_vs_y1;
    return `<div class="card reveal in drawn"><div class="ct"><span class="meter"><i class="key" style="background:${col(c)}"></i>${c}</span></div>
      <div class="cs">${x.n} lanzamientos jul-24 a jul-25. Cada mes en % de lo que el consumidor compra en sus 13 primeros meses.</div>
      <div class="legend"><span><i class="key" style="background:var(--ship)"></i>Envío</span><span><i class="key" style="background:${col(c)}"></i>EPOS</span></div>
      <div class="chart" data-k="l" data-c="${c}"></div>
      <div class="ct" style="font-size:14px;margin-top:14px">Envío por cada unidad vendida</div><div class="cs">Envío ÷ EPOS. Referencia: los veteranos (incluye clientes que no reportan).</div>
      <div class="chart" data-k="r" data-c="${c}" style="margin-top:8px"></div>
      <div class="kl" style="margin-top:8px">En el año 2 el EPOS ${Math.abs(e2) < .05 ? "se mantiene" : "cae un " + pp(-e2)} frente a los meses 4-11, pero el envío baja a <b>${dec(x.y2, 2)}×</b> del EPOS, por debajo de los veteranos (${dec(x.vet_ratio, 2)}×): el cliente vende el stock del lanzamiento. (${x.n_y2} lanzados jul-dic-24)</div>
      <details class="data"><summary>Ver datos</summary><div class="body">${table(["Mes", "Envío", "EPOS"], x.ship.map((v, i) => [i, dec(v * 100, 1) + "%", dec(x.epos[i] * 100, 1) + "%"]))}</div></details></div>`; }).join("");
  g.querySelectorAll(".chart").forEach(el => { const w = W(el); el.innerHTML = el.dataset.k === "l" ? launchSVG(el.dataset.c, w) : ratioSVG(el.dataset.c, w); });
}

/* ---------- ciclo de vida ---------- */
function vetChart(el) {
  const hs = housesIn(), V = D.veterans.houses, w = W(el), H = Math.round(Math.min(340, Math.max(250, w * .55))), x0 = 44, x1 = w - 6, y0 = 18, y1 = H - 50, lo = -.3, hi = .2, bw = (x1 - x0) / hs.length, yz = lerp(0, lo, hi, y1, y0);
  let s = `<svg viewBox="0 0 ${w} ${H}" role="img" aria-label="EPOS de veteranos frente al total de la casa">`;
  s += yAxis(x0, x1, y0, y1, lo, hi, [-.3, -.2, -.1, 0, .1, .2], t => pc(t));
  hs.forEach((h, i) => {
    const v = V[h], cx = x0 + bw * i;
    const tip = T.h(nm(h)) + T.r("Veteranos", pc(v.epos_yoy), colRaw(CAT[h])) + T.r("Total de la casa", pc(v.casa_epos_yoy), cssv("--ship")) + T.r("Veteranos que caen", pp(v.pct_caen)) + T.f(`${v.n} EANs veteranos`);
    s += `<g tabindex="0" data-tip="${esc(tip)}"><rect class="hit" x="${cx}" y="${y0}" width="${bw}" height="${H - y0}"/>`;
    [[v.epos_yoy, colH(h), 1], [v.casa_epos_yoy, "var(--ship)", .45]].forEach(([val, c, op], k) => {
      const y = lerp(val, lo, hi, y1, y0), top = Math.min(y, yz), hg = Math.max(Math.abs(y - yz), 1), bx = cx + bw * .17 + k * bw * .34, bww = bw * .3;
      s += `<rect class="grow" style="transform-origin:50% ${val >= 0 ? "100%" : "0%"}" x="${bx}" y="${top}" width="${bww}" height="${hg}" rx="4" fill="${c}" fill-opacity="${op}"/>`;
      s += `<text x="${bx + bww / 2}" y="${val >= 0 ? y - 6 : y + 14}" text-anchor="middle" class="vl">${pc(val)}</text>`;
    });
    s += `<text x="${cx + bw / 2}" y="${H - 26}" text-anchor="middle" class="lb">${nm(h)}</text><text x="${cx + bw / 2}" y="${H - 10}" text-anchor="middle" class="ax">${pp(v.pct_caen)} caen</text></g>`;
  });
  el.innerHTML = s + "</svg>";
  $("tVet").innerHTML = table(["Casa", "Veteranos", "Total casa", "Caen", "EANs"], hs.map(h => [nm(h), pc(V[h].epos_yoy), pc(V[h].casa_epos_yoy), pp(V[h].pct_caen), V[h].n]));
}
function cohorts() {
  const keys = ["Antes de FY24", "Lanzados FY24", "Lanzados FY25", "Lanzados FY26"];
  // rampa ordinal de un solo tono por categoría (generaciones = categorías ordenadas)
  const shades = { Fragancias: ["#3E2FA3", "#6250D6", "#9A8CE6", "#CFC8F5"], Makeup: ["#A9401A", "#E3602B", "#F29B77", "#F9CFBE"] };
  const box = $("cohortStack");
  box.innerHTML = catsIn().map(c => `<div class="card reveal in drawn"><div class="ct"><span class="meter"><i class="key" style="background:${col(c)}"></i>${c}: peso de cada generación en el envío</span></div>
    <div class="cs">Reparto del envío de cada año fiscal según cuándo se lanzó el EAN</div><div class="chart" data-c="${c}" style="margin-top:8px"></div>
    <div class="legend">${keys.map((k, i) => `<span><i class="key" style="background:${shades[c][i]}"></i>${k}</span>`).join("")}</div></div>`).join("");
  box.querySelectorAll(".chart").forEach(el => {
    const c = el.dataset.c, co = D.veterans.cohorts[c], w = W(el), x0 = 42, x1 = w - 2, H = 3 * 34 + 2;
    let s = `<svg viewBox="0 0 ${w} ${H}">`;
    ["FY24", "FY25", "FY26"].forEach((fy, j) => {
      const y = 2 + j * 34; let acc = x0;
      s += `<text x="${x0 - 8}" y="${y + 17}" text-anchor="end" class="lb">${fy}</text>`;
      keys.forEach((k, i) => {
        const v = (co[k] || [0, 0, 0])[j], ww = (x1 - x0) * v;
        if (ww > .5) {
          s += `<rect tabindex="0" data-tip="${esc(T.h(`${c}, ${fy}`) + T.r(k, pp(v), shades[c][i]))}" x="${acc + 1}" y="${y}" width="${Math.max(ww - 2, 0)}" height="24" rx="4" fill="${shades[c][i]}"/>`;
          if (v >= .07) s += `<text x="${acc + ww / 2}" y="${y + 16}" text-anchor="middle" class="vl" style="fill:${i < 2 ? "#fff" : "#14161A"};pointer-events:none">${pp(v)}</text>`;
        }
        acc += ww;
      });
    });
    el.innerHTML = s + "</svg>";
  });
}

/* ---------- carga y bajas ---------- */
function dumbbell(el) {
  const order = ["BURBERRY", "Gucci Make up", "Marc Jacobs", "Gucci", "Kylie Makeup"].filter(h => housesIn().includes(h));
  const by = D.load.ean_house, w = W(el), rowH = 42, H = order.length * rowH + 32, x0 = Math.min(116, w * .3), x1 = w - 88, lo = -.3, hi = .25, X = v => lerp(v, lo, hi, x0, x1);
  let s = `<svg viewBox="0 0 ${w} ${H}">`;
  [-.2, -.1, 0, .1, .2].forEach(t => { s += `<line x1="${X(t)}" x2="${X(t)}" y1="4" y2="${H - 22}" class="${t === 0 ? "gl0" : "gl"}"/><text x="${X(t)}" y="${H - 6}" text-anchor="middle" class="ax">${pc(t)}</text>`; });
  order.forEach((h, i) => {
    const b = by[h], y = 22 + i * rowH, xc = X(b.cargado), xn = X(b.normal), good = b.cargado < b.normal && b.meses >= 6;
    const tip = T.h(nm(h)) + T.r("Cargados", pc(b.cargado), colRaw(CAT[h])) + T.r("Normales", pc(b.normal), cssv("--ship")) + T.r("Descargados", pc(b.descargado)) + T.f(`Cargados por debajo de normales en ${b.meses} de ${b.de} meses`);
    s += `<g tabindex="0" data-tip="${esc(tip)}"><rect class="hit" x="0" y="${y - 18}" width="${w}" height="${rowH - 4}"/>`;
    s += `<text x="${x0 - 12}" y="${y + 4}" text-anchor="end" class="lb">${nm(h)}</text>`;
    s += `<line x1="${xc}" x2="${xn}" y1="${y}" y2="${y}" stroke="var(--line)" stroke-width="6" stroke-linecap="round"/>`;
    s += `<circle cx="${xn}" cy="${y}" r="6" fill="var(--paper)" stroke="var(--ship)" stroke-width="2"/><circle cx="${xc}" cy="${y}" r="7" fill="${colH(h)}" stroke="var(--paper)" stroke-width="2"/>`;
    s += `<text x="${x1 + 12}" y="${y + 4}" class="vl" style="fill:${good ? "var(--ok)" : "var(--muted)"}">${b.meses} de ${b.de} meses</text></g>`;
  });
  el.innerHTML = s + "</svg>";
  const c = D.load.ean_cat;
  $("kDumbL").innerHTML = catsIn().map(k => `<b>${k}:</b> cargados ${pc(c[k].cargado)} frente a normales ${pc(c[k].normal)} (${c[k].meses} de ${c[k].de} meses).`).join(" ") +
    (housesIn().includes("Kylie Makeup") ? " En Kylie los «cargados» siguen creciendo: puede que gane tiendas o clientes sin EPOS; con el EPOS solo no se puede distinguir." : "");
}
function exitChart(el) {
  const ex = D.load.exits, cs = catsIn(), w = W(el), H = Math.round(Math.min(290, Math.max(220, w * .5))), x0 = 44, x1 = w - 92, y0 = 14, y1 = H - 40;
  const X = k => lerp(k, -6, 6, x0, x1), Y = v => lerp(Math.min(v, 1.1), 0, 1.1, y1, y0);
  let s = `<svg viewBox="0 0 ${w} ${H}" role="img" aria-label="EPOS antes y después del último envío">`;
  s += `<rect x="${X(0)}" y="${y0}" width="${x1 - X(0)}" height="${y1 - y0}" fill="var(--line2)" opacity=".6"/>`;
  s += yAxis(x0, x1, y0, y1, 0, 1.1, [0, .25, .5, .75, 1], t => pp(t));
  s += `<line x1="${X(0)}" x2="${X(0)}" y1="${y0}" y2="${y1}" stroke="var(--ink2)" stroke-width="1" opacity=".6"/><text x="${X(0) + 6}" y="${y0 + 12}" class="ax">último envío</text>`;
  for (let k = -6; k <= 6; k += 2) s += `<text x="${X(k)}" y="${y1 + 16}" text-anchor="middle" class="ax">${k > 0 ? "+" + k : k === 0 ? "0" : "−" + (-k)}</text>`;
  s += `<text x="${(x0 + x1) / 2}" y="${H - 3}" text-anchor="middle" class="axl">meses frente al último envío relevante</text>`;
  cs.forEach(c => {
    const cv = ex[c].curve;
    s += poly(cv.map((v, i) => [X(i - 6), Y(v)]), col(c), 2, `class="draw" pathLength="1"`);
    cv.forEach((v, i) => { s += dot(X(i - 6), Y(v), col(c)); });
    s += `<text x="${x1 + 10}" y="${Y(cv[12]) + (c === "Fragancias" ? -2 : 10)}" class="vl">${c} ${pp(cv[12])}</text>`;
  });
  s += cols(i => X(i - 6), 13, y0, y1, (x1 - x0) / 12, i => { const k = i - 6;
    return T.h(k === 0 ? "Mes del último envío" : (k > 0 ? `${k} meses después` : `${-k} meses antes`)) + cs.map(c => T.r(c, pp(ex[c].curve[i]), colRaw(c))).join("") + T.f("EPOS frente a su nivel de 6 a 12 meses antes"); });
  el.innerHTML = s + "</svg>";
  $("exitLeg").innerHTML = cs.map(c => `<span><i class="lk" style="border-color:${col(c)}"></i>${c}</span>`).join("");
  $("exitSub").textContent = "Mediana del EPOS de los EANs que dejaron de enviarse (" + cs.map(c => `${ex[c].n} de ${c.toLowerCase()}`).join(" y ") + "). 100% = su EPOS de 6 a 12 meses antes.";
  $("kExitL").innerHTML = (cs.includes("Fragancias") ? `<b>Fragancias:</b> el EPOS sigue 6 meses después del último envío (aún al ${pp(ex.Fragancias.curve[12])}). ` : "") +
    (cs.includes("Makeup") ? `<b>Makeup:</b> se agota en 3 o 4 meses (${pp(ex.Makeup.curve[10])} a los 4 meses). ` : "") + "Antes del corte el EPOS ya cae: es la señal de declive.";
  $("tExit").innerHTML = table(["Mes", ...cs], ex[cs[0]].curve.map((_, i) => [i - 6 > 0 ? "+" + (i - 6) : String(i - 6).replace("-", "−"), ...cs.map(c => pp(ex[c].curve[i]))]));
}
function loadMultiples() {
  const box = $("cLoad"), hs = housesIn(), months = D.load.months, n = months.length;
  const all = hs.flatMap(h => D.load.r12[h]), rlo = Math.floor((Math.min(...all) - .02) * 10) / 10, rhi = Math.ceil((Math.max(...all) + .02) * 10) / 10;
  box.innerHTML = hs.map(h => `<div class="mini"><div class="mini-h"><span class="n"><i class="key" style="background:${colH(h)}"></i>${nm(h)}</span><span class="m"></span></div><div class="chart"></div></div>`).join("");
  box.querySelectorAll(".chart").forEach((el, j) => {
    const h = hs[j], r = D.load.r12[h], nx = D.load.next[h], w = W(el), x0 = 40, x1 = w - 6, bw = (x1 - x0) / n, X = i => x0 + bw * (i + .5);
    const a0 = 8, a1 = 78, b0 = 112, b1 = 172, H = 194;
    const Y1 = v => lerp(v, rlo, rhi, a1, a0), lo2 = -.5, hi2 = .5, Y2 = v => lerp(Math.max(lo2, Math.min(hi2, v)), lo2, hi2, b1, b0);
    let s = `<svg viewBox="0 0 ${w} ${H}" role="img" aria-label="Carga de ${nm(h)}">`;
    [rlo, (rlo + rhi) / 2, rhi].forEach(t => { s += `<line x1="${x0}" x2="${x1}" y1="${Y1(t)}" y2="${Y1(t)}" class="gl"/><text x="${x0 - 6}" y="${Y1(t) + 4}" text-anchor="end" class="ax">${dec(t, 2)}×</text>`; });
    [-.5, 0, .5].forEach(t => { s += `<line x1="${x0}" x2="${x1}" y1="${Y2(t)}" y2="${Y2(t)}" class="${t === 0 ? "gl0" : "gl"}"/><text x="${x0 - 6}" y="${Y2(t) + 4}" text-anchor="end" class="ax">${pc(t)}</text>`; });
    nx.forEach((v, i) => { if (v != null) { const y = Y2(v), z = Y2(0); s += `<rect class="grow" style="transform-origin:50% ${v >= 0 ? "100%" : "0%"}" x="${X(i) - bw * .32}" y="${Math.min(y, z)}" width="${bw * .64}" height="${Math.max(Math.abs(y - z), 1)}" rx="2" fill="var(--ship)" opacity=".5"/>`; } });
    s += poly(r.map((v, i) => [X(i), Y1(v)]), colH(h), 2, `class="draw" pathLength="1"`);
    [0, n - 1].forEach(i => { s += `<text x="${X(i)}" y="${H - 2}" text-anchor="${i ? "end" : "start"}" class="ax">${mes(months[i])}</text>`; });
    s += cols(X, n, a0, b1, bw, i => T.h(`${nm(h)}, ${mes(months[i])}`) + T.r("Envío ÷ EPOS, 12 meses", dec(r[i], 2) + "×", colRaw(CAT[h])) + T.r("Envío 3 meses siguientes", nx[i] == null ? "sin dato aún" : pc(nx[i]), cssv("--ship")));
    el.innerHTML = s + "</svg>";
    const iMax = r.indexOf(Math.max(...r));
    el.parentElement.querySelector(".m").textContent = `máximo ${mes(months[iMax])}, ${dec(r[iMax], 2)}×`;
  });
  $("tLoad").innerHTML = table(["Mes", ...hs.flatMap(h => [nm(h) + " ratio", nm(h) + " 3M sig."])], months.map((m, i) => [mes(m), ...hs.flatMap(h => [dec(D.load.r12[h][i], 2) + "×", D.load.next[h][i] == null ? "-" : pc(D.load.next[h][i])])]));
}

/* ---------- textos calculados con los datos ---------- */
function texts() {
  const n = D.noise, t = D.trend, la = D.launch, v = D.veterans, lo = D.load, P = t.persist;
  const fall = HOUSES.map(h => v.houses[h].epos_yoy).filter(x => x < -.05);
  const a = Math.round(-Math.max(...fall) * 100), b = Math.round(-Math.min(...fall) * 100), vr = `−${a} a −${b}%`, vrTxt = `entre un ${a} y un ${b}%`;
  const newF = 1 - v.cohorts.Fragancias["Antes de FY24"][2], newM = 1 - v.cohorts.Makeup["Antes de FY24"][2];
  $("h-ruido").textContent = `Los pedidos van a saltos: el crecimiento mensual del envío oscila unas ${Math.round(n.ratio_ruido)} veces más que el del EPOS`;
  $("h-trend").textContent = `A 12 meses, envío y EPOS van en la misma dirección en ${Math.round(t.same * 10)} de cada 10 EANs. La tendencia del EPOS se mantiene; la del envío, no`;
  $("h-launch").textContent = "El primer año se envía el doble de lo que se vende; el segundo, menos de lo normal mientras el cliente vende ese stock";
  $("h-vet").textContent = `Los códigos veteranos pierden ${vrTxt} de venta al consumidor cada año. La casa crece por los lanzamientos`;
  $("h-load").textContent = `Si un EAN acumula 12 meses enviando más de lo que vende, los 3 meses siguientes envía menos: en fragancias pasa los ${lo.ean_cat.Fragancias.meses} meses medidos`;
  $("kNoise").textContent = pp(n.pct_env_mas_ruidoso);
  $("kNoiseL").innerHTML = `Mediana: el crecimiento mensual del envío se mueve <b>${dec(n.ratio_ruido, 1)} veces</b> más que el del EPOS (desviación típica del crecimiento de cada mes, EAN a EAN).`;
  const bb = n.houses.BURBERRY, mn = x => Math.min(...x), mx = x => Math.max(...x);
  $("n-ruido").innerHTML = `Ejemplo: en Burberry el EPOS de cada mes está entre ${pc(mx(bb.epos))} y ${pc(mn(bb.epos))} frente al año anterior; el envío salta de ${pc(mn(bb.ship))} a ${pc(mx(bb.ship))}.
    <b>Un mes de envíos no dice nada de la demanda; un trimestre de EPOS, sí.</b> Por eso el trend del envío a 3 o 6 meses falla y la forma mensual del envío cambia de un año a otro.`;
  $("kSame").textContent = pp(t.same);
  $("kSameL").innerHTML = `de los EANs crecen o caen a la vez en FY26 (correlación ${dec(t.corr, 2)}). Como el EPOS no cubre a todos los clientes, se compara cada EAN consigo mismo, nunca en unidades.`;
  $("kPersistL").innerHTML = `Total: <b>${pp(P.Total.keep_epos)}</b> frente a ${pp(P.Total.keep_ship)}. Correlación de un semestre al siguiente: EPOS ${dec(P.Total.corr_epos, 2)} frente a envío ${dec(P.Total.corr_ship, 2)}.
    En makeup el EPOS de jul-dic anticipa el envío de ene-jun mejor que el propio envío (${dec(P.Makeup.epos_to_ship, 2)} frente a ${dec(P.Makeup.corr_ship, 2)}).`;
  $("n-launch").innerHTML = `<span class="tag">Consecuencia para la regla</span>En fragancias el mes del lanzamiento se envía el ${pp(la.Fragancias.m0_ship)} de lo que el consumidor comprará en 13 meses.
    Para un EAN de 12 a 23 meses, el «mismo mes del año pasado» es llenado de canal y la base sale inflada; es donde más falla la regla de fragancias (EANs de 6 a 17 meses).
    Para esos EANs la base debería ser el EPOS × la relación de los veteranos (o algo menos), no el envío del año anterior.`;
  $("n-vet").innerHTML = `<span class="tag">Consecuencia para el trend</span>El trend de la casa mezcla dos poblaciones. A un EAN veterano de Gucci no le aplica el ${pc(v.houses.Gucci.casa_epos_yoy)} de la casa sino un ${pc(v.houses.Gucci.epos_yoy)}; a uno de Kylie, un ${pc(v.houses["Kylie Makeup"].epos_yoy)} y no el ${pc(v.houses["Kylie Makeup"].casa_epos_yoy)}.
    En FY26 los lanzamientos desde FY24 ya son el ${pp(newF)} del envío en fragancias y el ${pp(newM)} en makeup. El trend de un EAN debería salir de su generación (los de su edad en su casa) y medirse en EPOS.`;
  const tiles = [
    [`${Math.round(n.ratio_ruido)}×`, "más ruido en el envío", `El crecimiento mensual del envío oscila unas ${Math.round(n.ratio_ruido)} veces más que el del EPOS, en el ${pp(n.pct_env_mas_ruidoso)} de los EANs.`, "#ruido", "wide t-frag"],
    [pp(t.same), "misma dirección a 12 meses", `Envío y EPOS crecen o caen juntos en ${Math.round(t.same * 10)} de cada 10 EANs.`, "#tendencia", ""],
    [`${pp(P.Total.keep_epos)} / ${pp(P.Total.keep_ship)}`, "la tendencia persiste", "EPOS frente a envío: EANs que mantienen su dirección de un semestre a otro.", "#tendencia", ""],
    [`${dec(la.Fragancias.y1, 1)}× → ${dec(la.Fragancias.y2, 2)}×`, "lanzamientos de fragancias", `Envío por unidad vendida en el año 1 y en el año 2 (veteranos ${dec(la.Fragancias.vet_ratio, 2)}×).`, "#lanzamientos", ""],
    [vr, "veteranos, cada año", "Venta al consumidor de los códigos con historia. Marc Jacobs, 0%.", "#ciclo", ""],
    [`${lo.ean_cat.Fragancias.meses} de ${lo.ean_cat.Fragancias.de}`, "meses en que la carga se corrige", "Fragancias: si en 12 meses se envía de más frente al EPOS, los 3 meses siguientes se envía menos.", "#carga", "wide t-mu"],
  ];
  $("tiles").innerHTML = tiles.map(([v_, k, d, href, cls]) => `<a class="tile reveal ${cls}" href="${href}"><div class="tv">${v_}</div><div class="tk">${k}</div><div class="td">${d}</div></a>`).join("");
  const rules = [
    ["La tendencia, del EPOS", "Trend del EAN = crecimiento de 12 meses de su EPOS, comparándolo consigo mismo.", `El EPOS mantiene su dirección de un semestre a otro en el ${pp(P.Total.keep_epos)} de los EANs; el envío, en el ${pp(P.Total.keep_ship)}.`, "#tendencia"],
    ["Seguir a mi generación", "Veteranos: el crecimiento del EPOS de los veteranos de su casa, nunca el trend total de la casa.", `Los veteranos pierden ${vrTxt} al año (Marc Jacobs, 0%); el total de la casa incluye los lanzamientos y engaña.`, "#ciclo"],
    ["Lanzamientos: año 2 ≠ año 1", `Del mes 12 al 23, base = EPOS × ${dec(Math.min(la.Fragancias.y2, la.Makeup.y2), 2)} a ${dec(Math.max(la.Fragancias.y2, la.Makeup.y2), 2)}, no el envío del año pasado.`, `El envío del año 1 fue llenado de canal: ${dec(la.Fragancias.y1, 1)}× (fragancias) y ${dec(la.Makeup.y1, 1)}× (makeup) lo que se vendió.`, "#lanzamientos"],
    ["Semáforo de carga", "Si envío/EPOS de 12 meses supera en un 15% su propio FY25, recortar los meses siguientes.", "Funciona en fragancias y Gucci Make up; en Kylie no, hasta tener el WOS.", "#carga"],
    ["Bajas", "Al planificar la salida de un código, contar con que el cliente sigue vendiendo después del último envío.", "Unos 6 meses en fragancias y 3 o 4 en makeup.", "#carga"],
  ];
  $("rules").innerHTML = rules.map(([t_, s_, ev, href], i) => `<div class="rule${i === 0 ? " open" : ""}"><button aria-expanded="${i === 0}"><span class="rn">${i + 1}</span><span><span class="rt">${t_}</span><div class="rs">${s_}</div></span>
    <svg class="chev" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg></button>
    <div class="rd"><div><div class="in"><b>Evidencia:</b> ${ev} <a href="${href}">Ver el gráfico</a></div></div></div></div>`).join("");
  document.querySelectorAll(".rule button").forEach(btn => btn.addEventListener("click", () => {
    const r = btn.parentElement, o = !r.classList.contains("open"); r.classList.toggle("open", o); btn.setAttribute("aria-expanded", o);
  }));
}

/* ---------- filtro ---------- */
function bindSeg(el, onPick) {
  el.insertAdjacentHTML("afterbegin", `<span class="pill"></span>`);
  const place = () => { const on = el.querySelector('button[aria-pressed="true"]'), p = el.querySelector(".pill"); if (on) { p.style.width = on.offsetWidth + "px"; p.style.transform = `translateX(${on.offsetLeft}px)`; } };
  el.querySelectorAll("button").forEach(b => b.addEventListener("click", () => { el.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b)); place(); onPick(b.dataset.v); }));
  el._place = place; requestAnimationFrame(place);
}
function drawAll() {
  drawHero(); drawNoise(); rangeChart($("cRange")); scatter($("cScatter")); houseTable(); persistChart($("cPersist"));
  drawLaunch(); vetChart($("cVet")); cohorts(); dumbbell($("cDumb")); exitChart($("cExit")); loadMultiples();
}

/* ---------- detalle al pasar el ratón o con el teclado ---------- */
const tip = $("tip");
let tipOn = null, lastHide = 0;
function placeTip(x, y) {
  const r = tip.getBoundingClientRect(), pad = 14;
  let tx = x + pad, ty = y + pad;
  if (tx + r.width > innerWidth - 8) tx = x - r.width - pad;
  if (ty + r.height > innerHeight - 8) ty = y - r.height - pad;
  tip.style.left = Math.max(8, tx) + "px"; tip.style.top = Math.max(8, ty) + "px";
}
function showTip(html, x, y) {
  // si ya había uno abierto (o se cerró hace nada), el siguiente aparece sin animación
  tip.classList.toggle("instant", tip.classList.contains("on") || performance.now() - lastHide < 250);
  if (tip.innerHTML !== html) tip.innerHTML = html;
  tip.classList.add("on"); placeTip(x, y);
}
function hideTip() { if (tip.classList.contains("on")) lastHide = performance.now(); tip.classList.remove("on"); tipOn = null; }
document.addEventListener("pointerover", e => { const t = e.target.closest("[data-tip]"); if (t) { tipOn = t; showTip(t.getAttribute("data-tip"), e.clientX, e.clientY); } });
document.addEventListener("pointermove", e => { if (tipOn) placeTip(e.clientX, e.clientY); });
document.addEventListener("pointerout", e => { const t = e.target.closest("[data-tip]"); if (t && t === tipOn && !t.contains(e.relatedTarget)) hideTip(); });
document.addEventListener("focusin", e => { const t = e.target.closest && e.target.closest("[data-tip]"); if (t) { const r = t.getBoundingClientRect(); tipOn = t; showTip(t.getAttribute("data-tip"), r.left + r.width / 2, r.top + 8); } });
document.addEventListener("focusout", e => { if (e.target === tipOn) hideTip(); });
addEventListener("wheel", hideTip, { passive: true });
addEventListener("touchmove", hideTip, { passive: true });

/* ---------- arranque ---------- */
try { const th = localStorage.getItem("epos-theme"); if (th) document.documentElement.dataset.theme = th; } catch (e) {}
texts();
bindSeg($("catSeg"), v => { state.cat = v; drawAll(); markDrawn(); });
drawAll();

// la animación de entrada se ve una vez; al filtrar, los gráficos cambian sin repetirla
function markDrawn() { document.querySelectorAll(".reveal.in").forEach(el => el.classList.add("drawn")); }
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); setTimeout(() => e.target.classList.add("drawn"), 1500); }
}), { threshold: .1, rootMargin: "0px 0px -6% 0px" });
document.querySelectorAll(".reveal:not(.in)").forEach(el => io.observe(el));

// barra y sección activa con IntersectionObserver (sin escuchar el scroll)
new IntersectionObserver(([e]) => $("bar").classList.toggle("scrolled", !e.isIntersecting)).observe($("top"));
const links = [...document.querySelectorAll("#nav a")];
const so = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) links.forEach(a => a.classList.toggle("on", a.getAttribute("href") === "#" + e.target.id)); }), { rootMargin: "-40% 0px -55% 0px" });
document.querySelectorAll("section.sec").forEach(s => so.observe(s));

let rz; addEventListener("resize", () => { clearTimeout(rz); rz = setTimeout(() => { drawAll(); markDrawn(); $("catSeg")._place(); }, 120); });
$("theme").addEventListener("click", () => {
  const root = document.documentElement, dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = dark ? "light" : "dark";
  try { localStorage.setItem("epos-theme", root.dataset.theme); } catch (e) {}
  drawAll(); markDrawn();
});
document.fonts && document.fonts.ready.then(() => $("catSeg")._place());
</script>
</body>
</html>
"""


def main():
    D = json.loads((ROOT / "work" / "epos_patrones.json").read_text())
    html = HTML.replace("__DATA__", json.dumps(D, separators=(",", ":")))
    assert "—" not in html and "–" not in html, "sin guiones largos (design-taste-frontend 9.G)"
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
