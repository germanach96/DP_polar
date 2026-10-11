"""Reporte HTML interactivo: patrones envío ↔ EPOS. Lee work/epos_patrones.json (correr antes src/epos_patrones.py).
Misma información que src/epos_patrones_report.py (PDF), con filtro por categoría, pestañas por casa y detalle al pasar el ratón.
Salida: reportes/REPORTE_EPOS_PATRONES.html (un solo archivo, sin dependencias salvo las fuentes de Google Fonts)."""
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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #F4F2EC; --paper: #FFFFFF; --ink: #15171C; --ink2: #4A4F59; --muted: #8A8F98; --line: #E2DFD6; --line2: #ECEAE3;
  --frag: #6250D6; --frag-soft: #E7E3FB; --mu: #E3602B; --mu-soft: #FBE3D8; --ship: #5B6573; --ok: #1B7F5B;
  --shadow: 0 1px 0 rgba(21,23,28,.04), 0 8px 24px -12px rgba(21,23,28,.12);
  --ease: cubic-bezier(.23, 1, .32, 1);
  --serif: Fraunces, Georgia, "Times New Roman", serif;
  --sans: Inter, system-ui, -apple-system, "Segoe UI", sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #111215; --paper: #191B20; --ink: #F1EFEA; --ink2: #B9BCC4; --muted: #80858F; --line: #2B2E35; --line2: #23262C;
    --frag: #8F81F0; --frag-soft: #2A2547; --mu: #F28A5C; --mu-soft: #3D271D; --ship: #A3AAB5; --ok: #4CC495;
    --shadow: 0 1px 0 rgba(0,0,0,.3), 0 10px 30px -14px rgba(0,0,0,.6);
  }
}
:root[data-theme="dark"] {
  --bg: #111215; --paper: #191B20; --ink: #F1EFEA; --ink2: #B9BCC4; --muted: #80858F; --line: #2B2E35; --line2: #23262C;
  --frag: #8F81F0; --frag-soft: #2A2547; --mu: #F28A5C; --mu-soft: #3D271D; --ship: #A3AAB5; --ok: #4CC495;
  --shadow: 0 1px 0 rgba(0,0,0,.3), 0 10px 30px -14px rgba(0,0,0,.6);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; scroll-padding-top: 76px; -webkit-text-size-adjust: 100%; }
body { background: var(--bg); color: var(--ink); font-family: var(--sans); font-size: 15px; line-height: 1.55;
  -webkit-font-smoothing: antialiased; font-feature-settings: "tnum" 1, "cv11" 1; }
b, strong { font-weight: 600; color: var(--ink); }
.wrap { max-width: 1180px; margin: 0 auto; padding: 0 28px; }

/* ---------- barra superior ---------- */
.bar { position: sticky; top: 0; z-index: 20; background: color-mix(in srgb, var(--bg) 82%, transparent);
  backdrop-filter: saturate(1.4) blur(14px); -webkit-backdrop-filter: saturate(1.4) blur(14px); border-bottom: 1px solid transparent;
  transition: border-color .2s var(--ease); }
.bar.scrolled { border-bottom-color: var(--line); }
.bar .wrap { display: flex; align-items: center; gap: 20px; height: 60px; }
.brand { font-family: var(--serif); font-weight: 600; font-size: 17px; letter-spacing: -.01em; white-space: nowrap; }
.brand span { color: var(--muted); font-weight: 400; }
.nav { display: flex; gap: 2px; margin-left: 8px; overflow-x: auto; scrollbar-width: none; }
.nav::-webkit-scrollbar { display: none; }
.nav a { font-size: 13px; color: var(--ink2); text-decoration: none; padding: 6px 10px; border-radius: 8px; white-space: nowrap;
  transition: color .15s var(--ease), background-color .15s var(--ease); }
.nav a .n { color: var(--muted); margin-right: 5px; font-variant-numeric: tabular-nums; }
.nav a.on { color: var(--ink); background: var(--paper); box-shadow: var(--shadow); }
@media (hover: hover) { .nav a:hover { color: var(--ink); } }
.bar .sp { flex: 1; }
.theme { border: 0; background: none; color: var(--ink2); width: 34px; height: 34px; border-radius: 9px; cursor: pointer; display: grid; place-items: center; }
@media (hover: hover) { .theme:hover { background: var(--paper); color: var(--ink); } }

/* ---------- control segmentado ---------- */
.seg { position: relative; display: inline-flex; max-width: 100%; overflow-x: auto; scrollbar-width: none; background: var(--line2); border-radius: 10px; padding: 3px; gap: 0; isolation: isolate; }
.seg button { position: relative; z-index: 1; border: 0; background: none; font: inherit; font-size: 13px; font-weight: 500; color: var(--ink2);
  padding: 6px 12px; border-radius: 7px; cursor: pointer; white-space: nowrap; transition: color .15s var(--ease); display: inline-flex; align-items: center; gap: 6px; }
.seg button[aria-pressed="true"] { color: var(--ink); }
.seg button:active { transform: scale(.97); }
.seg::-webkit-scrollbar { display: none; }
.seg .pill { position: absolute; z-index: 0; top: 3px; bottom: 3px; left: 0; border-radius: 7px; background: var(--paper); box-shadow: var(--shadow);
  transition: transform .26s var(--ease), width .26s var(--ease); }
.seg .dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; }
.seg button:disabled { opacity: .35; cursor: default; }

/* ---------- portada ---------- */
.hero { padding: 72px 0 40px; position: relative; }
.kick { font-size: 12px; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; color: var(--frag); }
h1 { font-family: var(--serif); font-weight: 400; font-size: clamp(38px, 6.2vw, 76px); line-height: 1.02; letter-spacing: -.025em; margin: 18px 0 0; max-width: 15ch; text-wrap: balance; }
h1 em { font-style: italic; color: var(--ship); }
.lead { font-size: 18px; color: var(--ink2); max-width: 60ch; margin-top: 22px; text-wrap: pretty; }
.signal { margin-top: 40px; background: var(--paper); border-radius: 20px; box-shadow: var(--shadow); padding: 22px 24px 14px; }
.signal-h { display: flex; flex-wrap: wrap; gap: 10px 22px; align-items: baseline; justify-content: space-between; }
.signal-h .t { font-weight: 600; font-size: 14px; }
.signal-h .s { font-size: 13px; color: var(--muted); }

.tiles { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 22px; }
.tile { background: var(--paper); border-radius: 16px; padding: 20px 22px 18px; box-shadow: var(--shadow); text-decoration: none; color: inherit; display: block;
  position: relative; overflow: hidden; transition: transform .2s var(--ease), box-shadow .2s var(--ease); }
.tile::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: var(--frag); }
.tile:nth-child(even)::before { background: var(--mu); }
@media (hover: hover) { .tile:hover { transform: translateY(-2px); } .tile:hover .go { opacity: 1; transform: none; } }
.tile:active { transform: scale(.985); }
.tv { font-family: var(--serif); font-size: 38px; line-height: 1.05; letter-spacing: -.02em; font-variant-numeric: lining-nums tabular-nums; }
.tk { font-size: 11.5px; font-weight: 600; text-transform: uppercase; letter-spacing: .09em; color: var(--ink2); margin: 8px 0 6px; }
.td { font-size: 13.5px; color: var(--ink2); line-height: 1.5; }
.go { position: absolute; right: 16px; top: 18px; font-size: 12px; color: var(--muted); opacity: 0; transform: translateX(-4px); transition: opacity .2s var(--ease), transform .2s var(--ease); }

/* ---------- secciones ---------- */
section.sec { padding: 72px 0 24px; }
.sec-h { display: grid; grid-template-columns: 84px 1fr; gap: 0 18px; align-items: start; margin-bottom: 28px; }
.num { font-family: var(--serif); font-size: 64px; line-height: .9; color: var(--line); font-variant-numeric: lining-nums; }
.sec-h .kick { color: var(--muted); }
h2 { font-family: var(--serif); font-weight: 400; font-size: clamp(25px, 3.1vw, 36px); line-height: 1.14; letter-spacing: -.015em; margin-top: 8px; max-width: 30ch; text-wrap: balance; }
.grid { display: grid; gap: 18px; }
.g2 { grid-template-columns: 1.25fr 1fr; }
.g2e { grid-template-columns: 1fr 1fr; }
.stack { display: flex; flex-direction: column; gap: 18px; min-width: 0; }
.card { background: var(--paper); border-radius: 18px; box-shadow: var(--shadow); padding: 22px 24px; min-width: 0; }
.card-h { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px 16px; align-items: flex-start; margin-bottom: 6px; }
.ct { font-weight: 600; font-size: 15.5px; letter-spacing: -.005em; }
.cs { font-size: 12.5px; color: var(--muted); margin-top: 2px; }
.kpi { font-family: var(--serif); font-size: 54px; line-height: 1; letter-spacing: -.02em; margin: 6px 0 10px; font-variant-numeric: lining-nums tabular-nums; }
.kl { font-size: 13.5px; color: var(--ink2); line-height: 1.55; }
.kl + .kl { margin-top: 8px; }
.legend { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: 12.5px; color: var(--ink2); margin: 10px 0 4px; }
.legend i { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; vertical-align: -1px; }
.legend i.dash { width: 16px; height: 0; border-radius: 0; border-top: 2px dashed var(--ship); vertical-align: 3px; }
.legend i.ring { background: transparent; border: 2px solid var(--ship); }
.note { margin-top: 18px; padding: 18px 22px; border-radius: 16px; background: var(--paper); box-shadow: var(--shadow); font-size: 14px; color: var(--ink2);
  border-left: 3px solid var(--frag); line-height: 1.6; }
.note.q { border-left-color: var(--mu); }
details.how { margin-top: 12px; }
details.how summary { cursor: pointer; font-size: 13px; color: var(--muted); list-style: none; display: inline-flex; align-items: center; gap: 6px; user-select: none; }
details.how summary::-webkit-details-marker { display: none; }
details.how summary::before { content: "+"; display: inline-grid; place-items: center; width: 18px; height: 18px; border-radius: 50%; border: 1px solid var(--line); font-size: 12px;
  transition: transform .2s var(--ease); }
details.how[open] summary::before { transform: rotate(45deg); }
details.how .body { font-size: 13.5px; color: var(--ink2); padding: 10px 0 0 24px; max-width: 75ch; }
.chart { position: relative; width: 100%; }
.chart svg { display: block; width: 100%; height: auto; overflow: visible; }
.ax { font-family: var(--sans); font-size: 11px; fill: var(--muted); }
.axl { font-family: var(--sans); font-size: 11.5px; fill: var(--ink2); font-weight: 500; }
.lb { font-family: var(--sans); font-size: 12.5px; fill: var(--ink); font-weight: 600; }
.vl { font-family: var(--sans); font-size: 11.5px; fill: var(--ink2); font-weight: 600; font-variant-numeric: tabular-nums; }
.halo { paint-order: stroke; stroke: var(--paper); stroke-width: 4px; stroke-linejoin: round; }
.gl { stroke: var(--line2); stroke-width: 1; }
.gl0 { stroke: var(--line); stroke-width: 1.2; }
.hit { fill: transparent; cursor: crosshair; }
.col .xh { stroke: var(--ink2); stroke-width: 1; stroke-dasharray: 2 3; opacity: 0; transition: opacity .12s; }
.col:hover .xh { opacity: .6; }
[data-tip] { cursor: pointer; }
.mk { transition: opacity .2s var(--ease), r .15s var(--ease); }
.dim .mk { opacity: .12; }
.pt { transition: opacity .2s var(--ease); }
@media (hover: hover) { .pt:hover { stroke: var(--ink); stroke-width: 1.5; } }

/* tabla */
.tb { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 12px; }
.tb th { font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); text-align: left; font-weight: 600; padding: 6px 8px; border-bottom: 1px solid var(--line); }
.tb td { padding: 8px; border-bottom: 1px solid var(--line2); font-variant-numeric: tabular-nums; vertical-align: middle; }
.tb tr:last-child td { border-bottom: 0; }
.meter { display: flex; align-items: center; gap: 8px; }
.meter .m { flex: 1; height: 6px; border-radius: 3px; background: var(--line2); overflow: hidden; min-width: 40px; }
.meter .m span { display: block; height: 100%; border-radius: 3px; }
.sw { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 7px; }

/* reglas */
.rules { display: flex; flex-direction: column; gap: 10px; }
.rule { background: var(--paper); border-radius: 16px; box-shadow: var(--shadow); overflow: hidden; }
.rule button { all: unset; box-sizing: border-box; width: 100%; display: grid; grid-template-columns: 40px 1fr 20px; gap: 14px; align-items: center; padding: 16px 20px; cursor: pointer; }
.rule button:focus-visible { outline: 2px solid var(--frag); outline-offset: -2px; border-radius: 16px; }
.rn { width: 36px; height: 36px; border-radius: 50%; background: var(--frag); color: #fff; display: grid; place-items: center; font-family: var(--serif); font-size: 18px; }
.rule:nth-child(even) .rn { background: var(--mu); }
.rt { font-weight: 600; font-size: 16px; }
.rs { font-size: 13.5px; color: var(--ink2); margin-top: 2px; }
.chev { color: var(--muted); transition: transform .25s var(--ease); }
.rule.open .chev { transform: rotate(180deg); }
.rd { display: grid; grid-template-rows: 0fr; transition: grid-template-rows .3s var(--ease); }
.rule.open .rd { grid-template-rows: 1fr; }
.rd > div { overflow: hidden; }
.rd .in { padding: 0 20px 18px 74px; font-size: 13.5px; color: var(--ink2); }
.rd .ev { margin-top: 8px; font-size: 12.5px; color: var(--muted); }
.rd .ev a { color: var(--ink2); }

.foot { margin: 80px 0 0; padding: 28px 0 60px; border-top: 1px solid var(--line); display: grid; grid-template-columns: repeat(4, 1fr); gap: 22px; font-size: 13px; color: var(--ink2); }
.foot b { display: block; margin-bottom: 4px; }
.foot code { font-size: 12px; background: var(--line2); padding: 1px 5px; border-radius: 4px; }
.empty { padding: 40px 0; text-align: center; color: var(--muted); font-size: 14px; }

/* tooltip */
#tip { position: fixed; z-index: 50; pointer-events: none; background: var(--ink); color: var(--bg); font-size: 12.5px; line-height: 1.45; padding: 9px 12px; border-radius: 10px;
  max-width: 260px; opacity: 0; transform: translateY(4px) scale(.98); transform-origin: top left; transition: opacity .12s var(--ease), transform .12s var(--ease); box-shadow: 0 10px 30px -10px rgba(0,0,0,.4); }
#tip.on { opacity: 1; transform: none; }
#tip b { color: var(--bg); }
#tip .r { display: flex; justify-content: space-between; gap: 14px; }
#tip .r span:last-child { font-weight: 600; font-variant-numeric: tabular-nums; }
#tip .h { font-weight: 600; margin-bottom: 3px; }
#tip .sw { margin-right: 6px; }

/* aparición */
.reveal { opacity: 0; transform: translateY(14px); transition: opacity .7s var(--ease), transform .7s var(--ease); }
.reveal.in { opacity: 1; transform: none; }
.draw { stroke-dasharray: 1; stroke-dashoffset: 1; }
.in .draw { stroke-dashoffset: 0; transition: stroke-dashoffset 1.4s var(--ease) .15s; }
.drawn .draw { stroke-dashoffset: 0; transition: none; }
.grow { transform-box: fill-box; transform-origin: 50% 100%; transform: scaleY(0); }
.growx { transform-box: fill-box; transform-origin: 0 50%; transform: scaleX(0); }
.in .grow, .in .growx { transform: none; transition: transform .8s var(--ease); }
.drawn .grow, .drawn .growx { transition: none; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .reveal, .reveal.in { opacity: 1; transform: none; transition: none; }
  .draw, .in .draw { stroke-dashoffset: 0; transition: none; }
  .grow, .growx { transform: none !important; transition: none !important; }
  .seg .pill, .tile, .rd, .chev { transition: none; }
}

@media (max-width: 1280px) { .nav { display: none; } }
@media (max-width: 900px) {
  .g2, .g2e { grid-template-columns: 1fr; }
  .tiles { grid-template-columns: 1fr 1fr; }
  .foot { grid-template-columns: 1fr 1fr; }
  .nav { display: none; }
}
@media (max-width: 560px) {
  .wrap { padding: 0 16px; }
  body { font-size: 14.5px; }
  .tiles { grid-template-columns: 1fr; }
  .sec-h { grid-template-columns: 1fr; }
  .num { font-size: 44px; margin-bottom: 4px; }
  .card { padding: 18px 16px; border-radius: 16px; }
  .signal { padding: 16px 14px 10px; }
  .foot { grid-template-columns: 1fr; }
  .rd .in { padding-left: 20px; }
  .bar .brand span { display: none; }
  .bar .wrap { gap: 10px; }
  .theme { display: none; }
  .seg button { padding: 6px 9px; }
  .hero { padding-top: 44px; }
}
</style>
</head>
<body>
<div id="tip" role="status" aria-live="polite"></div>

<header class="bar" id="bar">
  <div class="wrap">
    <div class="brand">EPOS <span>· patrones sep-26</span></div>
    <nav class="nav" id="nav">
      <a href="#ruido"><span class="n">1</span>Ruido</a>
      <a href="#tendencia"><span class="n">2</span>Tendencia</a>
      <a href="#lanzamientos"><span class="n">3</span>Lanzamientos</a>
      <a href="#ciclo"><span class="n">4</span>Ciclo de vida</a>
      <a href="#carga"><span class="n">5</span>Carga y bajas</a>
      <a href="#forecast"><span class="n">6</span>Forecast</a>
    </nav>
    <div class="sp"></div>
    <div class="seg" id="catSeg" role="group" aria-label="Categoría">
      <button data-v="all" aria-pressed="true">Todas</button>
      <button data-v="Fragancias" aria-pressed="false"><i class="dot" style="background:var(--frag)"></i>Fragancias</button>
      <button data-v="Makeup" aria-pressed="false"><i class="dot" style="background:var(--mu)"></i>Makeup</button>
    </div>
    <button class="theme" id="theme" aria-label="Cambiar tema" title="Cambiar tema">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
    </button>
  </div>
</header>

<main class="wrap">
  <section class="hero">
    <div class="kick">EPOS · patrones · foto sep-26 · 5 casas</div>
    <h1>El consumidor compra a ritmo constante. <em>El ruido lo meten los pedidos.</em></h1>
    <p class="lead">Seis patrones entre el envío (sell-in) y el EPOS (sell-out) de Burberry, Gucci, Marc Jacobs, Gucci Make up y Kylie Makeup, de jul-24 a ago-26.
      Todo en relativo: cada EAN se compara consigo mismo, porque no todos los clientes reportan EPOS.</p>
    <div class="signal reveal">
      <div class="signal-h">
        <div><div class="t" id="sigT"></div><div class="s">Crecimiento de cada mes frente al mismo mes del año anterior · EANs maduros</div></div>
        <div class="legend" style="margin:0"><span><i class="dash"></i>Envío</span><span><i id="sigDot" style="background:var(--frag)"></i>EPOS</span></div>
      </div>
      <div class="chart" id="cHero"></div>
    </div>
    <div class="tiles" id="tiles"></div>
  </section>

  <section class="sec" id="ruido">
    <div class="sec-h reveal"><div class="num">01</div><div><div class="kick">Ruido</div>
      <h2 id="h-ruido"></h2></div></div>
    <div class="grid g2">
      <div class="card reveal">
        <div class="card-h"><div><div class="ct">Crecimiento mensual frente al año anterior</div><div class="cs" id="noiseSub"></div></div>
          <div class="seg" id="houseSeg1" role="group" aria-label="Casa"></div></div>
        <div class="legend"><span><i class="dash"></i>Envío</span><span><i id="noiseDot"></i>EPOS</span></div>
        <div class="chart" id="cNoise"></div>
      </div>
      <div class="stack">
        <div class="card reveal">
          <div class="ct">EANs cuyo envío es más inestable que su EPOS</div>
          <div class="kpi" id="kNoise"></div>
          <div class="kl" id="kNoiseL"></div>
        </div>
        <div class="card reveal">
          <div class="ct">Distancia entre el mejor y el peor mes</div>
          <div class="cs">jul-25 → jul-26 · por casa</div>
          <div class="legend"><span><i style="background:var(--ship)"></i>Envío</span><span><i style="background:var(--frag)"></i><i style="background:var(--mu);margin-left:-4px"></i>EPOS</span></div>
          <div class="chart" id="cRange"></div>
        </div>
      </div>
    </div>
    <div class="note reveal" id="n-ruido"></div>
  </section>

  <section class="sec" id="tendencia">
    <div class="sec-h reveal"><div class="num">02</div><div><div class="kick">Tendencia</div>
      <h2 id="h-trend"></h2></div></div>
    <div class="grid g2">
      <div class="card reveal">
        <div class="ct">Cada punto es un EAN: crecimiento FY26 del EPOS frente al del envío</div>
        <div class="cs" id="scSub"></div>
        <div class="legend"><span><i style="background:var(--frag)"></i>Fragancias</span><span><i style="background:var(--mu)"></i>Makeup</span><span style="color:var(--muted)">zona sombreada = misma dirección</span></div>
        <div class="chart" id="cScatter"></div>
        <details class="how"><summary>Cómo se calcula</summary><div class="body">Crecimiento = suma FY26 / suma FY25 − 1, por EAN, de envío y de EPOS. EANs maduros (lanzados antes de ene-24) con envío y EPOS en los dos años.
          Los valores se recortan a −80% y +150% para que el gráfico se lea; el tamaño del punto es el envío FY25.</div></details>
      </div>
      <div class="stack">
        <div class="card reveal">
          <div class="ct">Envío y EPOS van en la misma dirección</div>
          <div class="kpi" id="kSame"></div>
          <div class="kl" id="kSameL"></div>
          <table class="tb" id="tbHouse"></table>
        </div>
        <div class="card reveal">
          <div class="ct">¿La tendencia de jul–dic sigue en ene–jun?</div>
          <div class="cs">% de EANs que mantienen el signo de su crecimiento</div>
          <div class="legend"><span><i style="background:var(--ink2)"></i>EPOS (color de la categoría)</span><span><i style="background:var(--ship);opacity:.55"></i>Envío</span></div>
          <div class="chart" id="cPersist"></div>
          <div class="kl" id="kPersistL"></div>
        </div>
      </div>
    </div>
  </section>

  <section class="sec" id="lanzamientos">
    <div class="sec-h reveal"><div class="num">03</div><div><div class="kick">Lanzamientos</div>
      <h2 id="h-launch"></h2></div></div>
    <div class="grid g2">
      <div class="card reveal">
        <div class="card-h"><div><div class="ct">Los 13 primeros meses de un lanzamiento</div><div class="cs" id="launchSub"></div></div>
          <div class="seg" id="launchSeg" role="group" aria-label="Categoría del lanzamiento">
            <button data-v="Fragancias" aria-pressed="true"><i class="dot" style="background:var(--frag)"></i>Fragancias</button>
            <button data-v="Makeup" aria-pressed="false"><i class="dot" style="background:var(--mu)"></i>Makeup</button></div></div>
        <div class="legend"><span><i style="background:var(--ship)"></i>Envío</span><span><i id="launchDot"></i>EPOS</span><span style="color:var(--muted)">cada mes en % de lo que el consumidor compra en sus 13 primeros meses</span></div>
        <div class="chart" id="cLaunch"></div>
      </div>
      <div class="stack">
        <div class="card reveal">
          <div class="ct">Envío por cada unidad vendida</div>
          <div class="cs">Envío ÷ EPOS. La referencia es la de los veteranos (incluye los clientes que no reportan)</div>
          <div class="chart" id="cRatio"></div>
          <div class="kl" id="kRatioL"></div>
        </div>
        <div class="note q reveal" style="margin-top:0"><b>Pregunta abierta.</b> ¿Los envíos de lanzamiento incluyen probadores o material de exposición? Si es así, parte del «doble» no es stock vendible.</div>
      </div>
    </div>
    <div class="note reveal" id="n-launch"></div>
  </section>

  <section class="sec" id="ciclo">
    <div class="sec-h reveal"><div class="num">04</div><div><div class="kick">Ciclo de vida</div>
      <h2 id="h-vet"></h2></div></div>
    <div class="grid g2">
      <div class="card reveal">
        <div class="ct">EPOS FY26 frente a FY25: veteranos activos frente al total de la casa</div>
        <div class="cs">Veteranos = con envío desde jul-23 y todavía activos</div>
        <div class="legend"><span><i style="background:var(--frag)"></i><i style="background:var(--mu);margin-left:-4px"></i>Veteranos</span><span><i style="background:var(--ship);opacity:.45"></i>Total de la casa (con lanzamientos)</span></div>
        <div class="chart" id="cVet"></div>
      </div>
      <div class="stack" id="cohortStack"></div>
    </div>
    <div class="note reveal" id="n-vet"></div>
  </section>

  <section class="sec" id="carga">
    <div class="sec-h reveal"><div class="num">05</div><div><div class="kick">Carga del canal y bajas</div>
      <h2 id="h-load"></h2></div></div>
    <div class="grid g2e">
      <div class="card reveal">
        <div class="ct">Envío de los 3 meses siguientes: EANs cargados frente a normales</div>
        <div class="cs">Exceso de crecimiento del envío sobre el del EPOS · cortes sep-25 → abr-26</div>
        <div class="legend"><span><i style="background:var(--frag)"></i><i style="background:var(--mu);margin-left:-4px"></i>Cargados</span><span><i class="ring"></i>Normales</span><span style="color:var(--muted)">derecha: meses en que cargados &lt; normales</span></div>
        <div class="chart" id="cDumb"></div>
        <div class="kl" id="kDumbL"></div>
        <details class="how"><summary>Qué es «cargado»</summary><div class="body">Un EAN está cargado cuando su relación envío/EPOS de los últimos 12 meses está más de un 15% por encima de la suya de FY25: ha enviado más de lo que el consumidor ha comprado.
          Se compara cada EAN consigo mismo, nunca en unidades.</div></details>
      </div>
      <div class="card reveal">
        <div class="card-h"><div><div class="ct">La casa a lo largo del año</div><div class="cs">Envío por unidad de EPOS en 12 meses y crecimiento del envío de los 3 meses siguientes</div></div>
          <div class="seg" id="houseSeg2" role="group" aria-label="Casa"></div></div>
        <div class="legend"><span><i id="loadDot"></i>Envío ÷ EPOS, 12 meses (eje izquierdo)</span><span><i style="background:var(--ship);opacity:.5;border-radius:2px"></i>Envío 3 meses siguientes vs año anterior (eje derecho)</span></div>
        <div class="chart" id="cLoad"></div>
        <div class="kl" id="kLoadL"></div>
      </div>
    </div>
    <div class="grid g2e" style="margin-top:18px">
      <div class="card reveal">
        <div class="ct">Bajas: el consumidor sigue comprando después del último envío</div>
        <div class="cs" id="exitSub"></div>
        <div class="chart" id="cExit"></div>
      </div>
      <div class="stack">
        <div class="card reveal"><div class="kl" id="kExitL"></div></div>
        <div class="note reveal" style="margin-top:0"><b>Gucci Make up, a nivel casa:</b> acumuló carga 9 meses sin dejar de enviar por encima del EPOS y corrigió de golpe en may–jul-26.
          <b>La carga avisa, pero no dice cuándo llega la corrección.</b> El WOS (semanas de stock) lo diría.</div>
      </div>
    </div>
  </section>

  <section class="sec" id="forecast">
    <div class="sec-h reveal"><div class="num">06</div><div><div class="kick">Qué significa para el forecast</div>
      <h2>El EPOS no sirve como número, pero sí como brújula: marca la dirección, la edad del producto y si el canal está lleno</h2></div></div>
    <div class="grid g2">
      <div class="rules reveal" id="rules"></div>
      <div class="stack">
        <div class="card reveal"><div class="ct">Por qué solo en relativo</div>
          <div class="kl" style="margin-top:8px">No todos los clientes reportan EPOS (suman ~80% del envío). Por eso todo el reporte compara cada EAN o casa consigo mismo: frente al año anterior o frente a su propia relación envío/EPOS. El nivel absoluto no se usa nunca.</div></div>
        <div class="card reveal"><div class="ct">Qué falta para cerrar el círculo</div>
          <div class="kl" style="margin-top:8px"><b>WOS</b> (semanas de stock) por EAN y cliente: stock = WOS × venta semanal. Convierte «cargado» en un dato y diría cuándo llega la corrección.</div>
          <div class="kl"><b>Probadores y material de exposición:</b> saber si están en el envío de lanzamiento.</div>
          <div class="kl"><b>Más historia de EPOS:</b> hoy hay 2 años (jul-24 → jul-26); cada mes nuevo refuerza o desmiente estos patrones.</div></div>
        <div class="note reveal" style="margin-top:0"><b>Siguiente paso:</b> probar los puntos 1–3 como partido «Consumidor (EPOS)» en el parlamento, con cortes oct-25 → mar-26 y lo real hasta ago-26.</div>
      </div>
    </div>
  </section>

  <footer class="foot">
    <div><b>Envío</b>Sell-in de la foto sep-26 (actuals), jul-23 → ago-26.</div>
    <div><b>EPOS</b>Venta al consumidor de los clientes que reportan (~80% del envío), jul-24 → jul-26.</div>
    <div><b>Cómo se compara</b>Siempre en relativo: crecimiento frente al año anterior o relación envío/EPOS frente a la propia historia del EAN.</div>
    <div><b>Datos y cálculo</b>DATA.xlsx, GUMU.xlsx, KYMU.xlsx (foto sep-26). <code>src/epos_patrones.py</code> · página: <code>src/epos_patrones_html.py</code></div>
  </footer>
</main>

<script>
const D = __DATA__;
const HOUSES = ["BURBERRY", "Gucci", "Marc Jacobs", "Gucci Make up", "Kylie Makeup"];
const CAT = {"BURBERRY": "Fragancias", "Gucci": "Fragancias", "Marc Jacobs": "Fragancias", "Gucci Make up": "Makeup", "Kylie Makeup": "Makeup"};
const nm = h => h === "BURBERRY" ? "Burberry" : h;
const MESES = {Jan: "ene", Feb: "feb", Mar: "mar", Apr: "abr", May: "may", Jun: "jun", Jul: "jul", Aug: "ago", Sep: "sep", Oct: "oct", Nov: "nov", Dec: "dic"};
const mes = m => { const [a, b] = m.split("-"); return MESES[a] + "-" + b; };
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const col = c => c === "Fragancias" ? "var(--frag)" : "var(--mu)";
const colH = h => col(CAT[h]);
const pc = (x, s = true) => { const r = Math.round(x * 100); if (r === 0) return "0%"; return (r < 0 ? "−" : (s ? "+" : "")) + Math.abs(r) + "%"; };
const pp = x => Math.round(x * 100) + "%";
const dec = (x, d) => x.toFixed(d).replace(".", ",");
const lerp = (v, a, b, A, B) => A + (v - a) / (b - a) * (B - A);
const esc = s => String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
const tipRow = (k, v, c) => `<div class='r'><span>${c ? `<i class='sw' style='background:${c}'></i>` : ""}${k}</span><span>${v}</span></div>`;
const units = x => Math.round(x).toLocaleString("es-ES");

let state = { cat: "all", h1: "BURBERRY", h2: "Gucci Make up", launch: "Fragancias" };
const housesIn = () => HOUSES.filter(h => state.cat === "all" || CAT[h] === state.cat);
const catsIn = () => state.cat === "all" ? ["Fragancias", "Makeup"] : [state.cat];
const $ = id => document.getElementById(id);

/* ---------- ejes y piezas comunes ---------- */
function yAxis(x0, x1, y0, y1, lo, hi, ticks, fmt, side = "left") {
  return ticks.map(t => {
    const y = lerp(t, lo, hi, y1, y0);
    const zero = Math.abs(t) < 1e-9;
    const tx = side === "left" ? `<text x="${x0 - 8}" y="${y + 4}" text-anchor="end" class="ax">${fmt(t)}</text>` : `<text x="${x1 + 8}" y="${y + 4}" class="ax">${fmt(t)}</text>`;
    return (side === "left" ? `<line x1="${x0}" x2="${x1}" y1="${y}" y2="${y}" class="${zero ? "gl0" : "gl"}"/>` : "") + tx;
  }).join("");
}
const W = el => Math.max(280, el.clientWidth);
const poly = (pts, color, w, extra = "") => `<polyline points="${pts.map(p => p.join(",")).join(" ")}" fill="none" stroke="${color}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round" ${extra}/>`;

/* ---------- línea envío vs EPOS (portada y sección 1) ---------- */
function noiseChart(el, h, opt = {}) {
  const d = D.noise.houses[h], months = D.noise.months, w = W(el), H = opt.H || Math.round(Math.min(340, Math.max(220, w * .42)));
  const x0 = 46, x1 = w - (opt.labels ? 70 : 12), y0 = 12, y1 = H - 28, lo = -.8, hi = .8, n = months.length;
  const X = i => lerp(i, 0, n - 1, x0, x1), cl = v => Math.max(lo, Math.min(hi, v)), Y = v => lerp(cl(v), lo, hi, y1, y0);
  const c = colH(h);
  let s = `<svg viewBox="0 0 ${w} ${H}" role="img" aria-label="Envío y EPOS de ${nm(h)}, crecimiento mensual">`;
  s += yAxis(x0, x1, y0, y1, lo, hi, [-.8, -.4, 0, .4, .8], t => pc(t));
  months.forEach((m, i) => { if (i % (w < 520 ? 3 : 2) === 0 || i === n - 1) s += `<text x="${X(i)}" y="${H - 8}" text-anchor="middle" class="ax">${mes(m)}</text>`; });
  // banda entre las dos líneas
  const band = d.ship.map((v, i) => [X(i), Y(v)]).concat(d.epos.map((v, i) => [X(i), Y(v)]).reverse());
  s += `<polygon points="${band.map(p => p.join(",")).join(" ")}" fill="${c}" opacity=".07"/>`;
  s += poly(d.ship.map((v, i) => [X(i), Y(v)]), "var(--ship)", 1.8, `stroke-dasharray="5 4"`);
  s += poly(d.epos.map((v, i) => [X(i), Y(v)]), c, 2.6, `class="draw" pathLength="1"`);
  d.epos.forEach((v, i) => { s += `<circle cx="${X(i)}" cy="${Y(v)}" r="3" fill="${c}" stroke="var(--paper)" stroke-width="1.5"/>`; });
  if (opt.labels) {
    let ys = Y(d.ship[n - 1]), ye = Y(d.epos[n - 1]);
    if (Math.abs(ys - ye) < 16) { const m = (ys + ye) / 2, up = d.ship[n - 1] >= d.epos[n - 1]; ys = m + (up ? -8 : 8); ye = m + (up ? 8 : -8); }
    s += `<text x="${x1 + 8}" y="${ys + 4}" class="lb" style="fill:var(--ship)">Envío</text>`;
    s += `<text x="${x1 + 8}" y="${ye + 4}" class="lb" style="fill:${c}">EPOS</text>`;
  }
  const bw = (x1 - x0) / (n - 1);
  months.forEach((m, i) => {
    const tip = `<div class='h'>${nm(h)} · ${mes(m)}</div>` + tipRow("Envío", pc(d.ship[i]), css("--ship")) + tipRow("EPOS", pc(d.epos[i]), c.startsWith("var") ? css(c.slice(4, -1)) : c);
    s += `<g class="col" data-tip="${esc(tip)}"><line class="xh" x1="${X(i)}" x2="${X(i)}" y1="${y0}" y2="${y1}"/><rect class="hit" x="${X(i) - bw / 2}" y="${y0}" width="${bw}" height="${y1 - y0}"/></g>`;
  });
  el.innerHTML = s + "</svg>";
}

function rangeChart(el) {
  const hs = housesIn(), w = W(el), rowH = 46, H = hs.length * rowH + 30, x0 = Math.min(118, w * .3), x1 = w - 46, hi = 1.2;
  let s = `<svg viewBox="0 0 ${w} ${H}">`;
  [0, .4, .8, 1.2].forEach(t => { const x = lerp(t, 0, hi, x0, x1); s += `<line x1="${x}" x2="${x}" y1="4" y2="${H - 22}" class="gl"/><text x="${x}" y="${H - 6}" text-anchor="middle" class="ax">${Math.round(t * 100)} pts</text>`; });
  hs.forEach((h, i) => {
    const r = D.noise.rango[h], y = 10 + i * rowH, c = colH(h);
    const tip = `<div class='h'>${nm(h)}</div>` + tipRow("Rango envío", Math.round(r.ship * 100) + " pts") + tipRow("Rango EPOS", Math.round(r.epos * 100) + " pts") + tipRow("EANs maduros", D.noise.houses[h].n);
    s += `<g data-tip="${esc(tip)}"><rect x="0" y="${y - 4}" width="${w}" height="${rowH - 6}" fill="transparent"/>`;
    s += `<text x="${x0 - 10}" y="${y + 14}" text-anchor="end" class="lb">${nm(h)}</text>`;
    s += `<rect class="growx" x="${x0}" y="${y}" width="${lerp(r.ship, 0, hi, 0, x1 - x0)}" height="10" rx="3" fill="var(--ship)"/>`;
    s += `<text x="${x0 + lerp(r.ship, 0, hi, 0, x1 - x0) + 6}" y="${y + 9}" class="vl">${Math.round(r.ship * 100)}</text>`;
    s += `<rect class="growx" x="${x0}" y="${y + 13}" width="${lerp(r.epos, 0, hi, 0, x1 - x0)}" height="10" rx="3" fill="${c}"/>`;
    s += `<text x="${x0 + lerp(r.epos, 0, hi, 0, x1 - x0) + 6}" y="${y + 22}" class="vl">${Math.round(r.epos * 100)}</text></g>`;
  });
  el.innerHTML = s + "</svg>";
}

/* ---------- dispersión ---------- */
function scatter(el) {
  const pts = D.trend.points.filter(p => state.cat === "all" || p.cat === state.cat);
  const w = W(el), H = Math.round(Math.min(480, Math.max(300, w * .78))), x0 = 48, x1 = w - 12, y0 = 10, y1 = H - 40, lo = -.8, hi = 1.5;
  const X = v => lerp(v, lo, hi, x0, x1), Y = v => lerp(v, lo, hi, y1, y0);
  let s = `<svg viewBox="0 0 ${w} ${H}" role="img" aria-label="Dispersión de crecimiento EPOS frente a envío por EAN">`;
  s += `<rect x="${X(0)}" y="${y0}" width="${x1 - X(0)}" height="${Y(0) - y0}" fill="var(--line2)" opacity=".7"/>`;
  s += `<rect x="${x0}" y="${Y(0)}" width="${X(0) - x0}" height="${y1 - Y(0)}" fill="var(--line2)" opacity=".7"/>`;
  const ticks = [-.5, 0, .5, 1, 1.5];
  s += yAxis(x0, x1, y0, y1, lo, hi, ticks, t => pc(t));
  ticks.forEach(t => { s += `<line x1="${X(t)}" x2="${X(t)}" y1="${y0}" y2="${y1}" class="${t === 0 ? "gl0" : "gl"}"/><text x="${X(t)}" y="${y1 + 16}" text-anchor="middle" class="ax">${pc(t)}</text>`; });
  s += `<line x1="${X(lo)}" y1="${Y(lo)}" x2="${X(hi)}" y2="${Y(hi)}" stroke="var(--muted)" stroke-dasharray="3 4"/>`;
  s += `<text x="${X(1.12)}" y="${Y(1.2) - 4}" class="ax halo" text-anchor="middle">envío = EPOS</text>`;
  if (w >= 460) {
    s += `<text x="${X(1.45)}" y="${Y(-.7)}" class="ax" text-anchor="end">EPOS crece, envío cae</text>`;
    s += `<text x="${X(-.75)}" y="${Y(1.38)}" class="ax">envío crece, EPOS cae</text>`;
  }
  [...pts].sort((a, b) => b.w - a.w).forEach(p => {
    const r = Math.max(3, Math.min(10, Math.sqrt(p.w) / 10));
    const same = Math.sign(p.x) === Math.sign(p.y);
    const tip = `<div class='h'>${p.cat} · EAN maduro</div>` + tipRow("EPOS FY26 vs FY25", pc(p.x)) + tipRow("Envío FY26 vs FY25", pc(p.y)) + tipRow("Envío FY25", units(p.w) + " uds") + `<div style='opacity:.7;margin-top:3px'>${same ? "Misma dirección" : "Dirección contraria"}</div>`;
    s += `<circle class="pt" cx="${X(p.x)}" cy="${Y(p.y)}" r="${r}" fill="${col(p.cat)}" fill-opacity=".55" stroke="var(--paper)" stroke-width=".8" data-tip="${esc(tip)}"/>`;
  });
  s += `<text x="${(x0 + x1) / 2}" y="${H - 4}" text-anchor="middle" class="axl">EPOS FY26 vs FY25 →</text>`;
  s += `<text x="12" y="${(y0 + y1) / 2}" text-anchor="middle" class="axl" transform="rotate(-90 12 ${(y0 + y1) / 2})">Envío FY26 vs FY25 →</text>`;
  el.innerHTML = s + "</svg>";
  $("scSub").textContent = `${pts.length} EANs maduros · tamaño = envío FY25 · pasa el ratón por un punto`;
}

function persistChart(el) {
  const P = D.trend.persist, rows = state.cat === "all" ? ["Total", "Fragancias", "Makeup"] : [state.cat];
  const w = W(el), rowH = 52, H = rows.length * rowH + 26, x0 = 96, x1 = w - 44;
  let s = `<svg viewBox="0 0 ${w} ${H}">`;
  [0, .25, .5, .75, 1].forEach(t => { const x = lerp(t, 0, 1, x0, x1); s += `<line x1="${x}" x2="${x}" y1="2" y2="${H - 20}" class="gl"/><text x="${x}" y="${H - 5}" text-anchor="middle" class="ax">${pp(t)}</text>`; });
  rows.forEach((r, i) => {
    const p = P[r], y = 8 + i * rowH, c = r === "Total" ? "var(--ink2)" : col(r);
    const tip = `<div class='h'>${r} · ${p.n} EANs</div>` + tipRow("Mantienen signo (EPOS)", pp(p.keep_epos)) + tipRow("Mantienen signo (envío)", pp(p.keep_ship)) + tipRow("Correlación EPOS", dec(p.corr_epos, 2)) + tipRow("Correlación envío", dec(p.corr_ship, 2));
    s += `<g data-tip="${esc(tip)}"><rect x="0" y="${y - 4}" width="${w}" height="${rowH - 8}" fill="transparent"/><text x="${x0 - 10}" y="${y + 17}" text-anchor="end" class="lb">${r}</text>`;
    s += `<rect class="growx" x="${x0}" y="${y}" width="${lerp(p.keep_epos, 0, 1, 0, x1 - x0)}" height="14" rx="4" fill="${c}"/><text x="${x0 + lerp(p.keep_epos, 0, 1, 0, x1 - x0) + 6}" y="${y + 11}" class="vl">${pp(p.keep_epos)}</text>`;
    s += `<rect class="growx" x="${x0}" y="${y + 18}" width="${lerp(p.keep_ship, 0, 1, 0, x1 - x0)}" height="14" rx="4" fill="var(--ship)" opacity=".55"/><text x="${x0 + lerp(p.keep_ship, 0, 1, 0, x1 - x0) + 6}" y="${y + 29}" class="vl">${pp(p.keep_ship)}</text></g>`;
  });
  el.innerHTML = s + "</svg>";
}

/* ---------- lanzamientos ---------- */
function launchChart(el) {
  const c = state.launch, x = D.launch[c], w = W(el), H = Math.round(Math.min(330, Math.max(230, w * .44))), x0 = 44, x1 = w - 8, y0 = 14, y1 = H - 40, hi = .7, n = x.ship.length, bw = (x1 - x0) / n;
  let s = `<svg viewBox="0 0 ${w} ${H}" role="img" aria-label="Envío y EPOS en los 13 primeros meses de un lanzamiento">`;
  s += yAxis(x0, x1, y0, y1, 0, hi, [0, .2, .4, .6], t => pp(t));
  for (let i = 0; i < n; i++) {
    const cx = x0 + bw * i;
    const tip = `<div class='h'>${c} · mes ${i}</div>` + tipRow("Envío", dec(x.ship[i] * 100, 1) + "%", css("--ship")) + tipRow("EPOS", dec(x.epos[i] * 100, 1) + "%", css(c === "Fragancias" ? "--frag" : "--mu")) + `<div style='opacity:.7;margin-top:3px'>% de lo que el consumidor compra en 13 meses</div>`;
    s += `<g data-tip="${esc(tip)}"><rect x="${cx}" y="${y0}" width="${bw}" height="${y1 - y0}" class="hit"/>`;
    [[x.ship[i], "var(--ship)"], [x.epos[i], col(c)]].forEach(([v, cc], k) => {
      const h = lerp(Math.min(v, hi), 0, hi, 0, y1 - y0);
      s += `<rect class="grow" style="transition-delay:${i * 25}ms" x="${cx + bw * .14 + k * bw * .37}" y="${y1 - h}" width="${bw * .34}" height="${Math.max(h, .5)}" rx="3" fill="${cc}"/>`;
    });
    s += `<text x="${cx + bw / 2}" y="${y1 + 15}" text-anchor="middle" class="ax">${i}</text></g>`;
    if (x.ship[i] > .3) s += `<text x="${cx + bw * .31}" y="${lerp(Math.min(x.ship[i], hi), 0, hi, y1, y0) - 6}" text-anchor="middle" class="vl">${pp(x.ship[i])}</text>`;
  }
  s += `<text x="${(x0 + x1) / 2}" y="${H - 4}" text-anchor="middle" class="axl">meses desde el lanzamiento</text>`;
  el.innerHTML = s + "</svg>";
  $("launchSub").textContent = `${x.n} lanzamientos de ${c.toLowerCase()} jul-24 → jul-25 · pasa el ratón por cada mes`;
  $("launchDot").style.background = col(c);
}

function ratioChart(el) {
  const c = state.launch, x = D.launch[c], w = W(el), hi = 2.8, x0 = Math.min(150, w * .38), x1 = w - 50;
  const rows = [["Año 1 (meses 0–11)", x.y1, col(c), 1], ["Año 2 (meses 12–19)", x.y2, col(c), .55], ["Veteranos", x.vet_ratio, "var(--ship)", 1]];
  const H = rows.length * 38 + 10, xv = lerp(x.vet_ratio, 0, hi, x0, x1);
  let s = `<svg viewBox="0 0 ${w} ${H}">`;
  rows.forEach(([lab, v, cc, op], i) => {
    const y = 8 + i * 38;
    s += `<text x="${x0 - 10}" y="${y + 14}" text-anchor="end" class="lb">${lab}</text>`;
    s += `<rect class="growx" x="${x0}" y="${y}" width="${lerp(v, 0, hi, 0, x1 - x0)}" height="20" rx="4" fill="${cc}" fill-opacity="${op}"/>`;
    s += `<text x="${x0 + lerp(v, 0, hi, 0, x1 - x0) + 7}" y="${y + 14}" class="vl" style="fill:var(--ink)">${dec(v, 2)}×</text>`;
  });
  s += `<line x1="${xv}" x2="${xv}" y1="2" y2="${H - 4}" stroke="var(--ink2)" stroke-dasharray="2 3"/>`;
  el.innerHTML = s + "</svg>";
  const e2 = x.epos_y2_vs_y1;
  $("kRatioL").innerHTML = `En el año 2 el EPOS ${Math.abs(e2) < .05 ? "se mantiene" : "cae un " + pc(e2).replace("−", "")} frente a los meses 4–11, pero el envío baja a <b>${dec(x.y2, 2)}×</b> del EPOS, por debajo de los veteranos (${dec(x.vet_ratio, 2)}×): señal de que el cliente vende el stock del lanzamiento. (${x.n_y2} lanzados jul–dic-24)`;
}

/* ---------- veteranos ---------- */
function vetChart(el) {
  const hs = housesIn(), V = D.veterans.houses, w = W(el), H = Math.round(Math.min(360, Math.max(260, w * .55))), x0 = 46, x1 = w - 8, y0 = 18, y1 = H - 52, lo = -.3, hi = .2, bw = (x1 - x0) / hs.length, yz = lerp(0, lo, hi, y1, y0);
  let s = `<svg viewBox="0 0 ${w} ${H}" role="img" aria-label="EPOS de veteranos frente al total de la casa">`;
  s += yAxis(x0, x1, y0, y1, lo, hi, [-.3, -.2, -.1, 0, .1, .2], t => pc(t));
  hs.forEach((h, i) => {
    const v = V[h], cx = x0 + bw * i;
    const tip = `<div class='h'>${nm(h)}</div>` + tipRow("Veteranos", pc(v.epos_yoy)) + tipRow("Total de la casa", pc(v.casa_epos_yoy)) + tipRow("Veteranos que caen", pp(v.pct_caen)) + tipRow("EANs veteranos", v.n);
    s += `<g data-tip="${esc(tip)}"><rect class="hit" x="${cx}" y="${y0}" width="${bw}" height="${y1 - y0 + 40}"/>`;
    [[v.epos_yoy, colH(h), 1], [v.casa_epos_yoy, "var(--ship)", .45]].forEach(([val, c, op], k) => {
      const y = lerp(val, lo, hi, y1, y0), top = Math.min(y, yz), hgt = Math.max(Math.abs(y - yz), 1), bx = cx + bw * .17 + k * bw * .34, bww = bw * .3;
      s += `<rect class="grow" style="transform-origin:50% ${val >= 0 ? "100%" : "0%"}" x="${bx}" y="${top}" width="${bww}" height="${hgt}" rx="4" fill="${c}" fill-opacity="${op}"/>`;
      s += `<text x="${bx + bww / 2}" y="${val >= 0 ? y - 6 : y + 14}" text-anchor="middle" class="vl">${pc(val)}</text>`;
    });
    s += `<text x="${cx + bw / 2}" y="${H - 28}" text-anchor="middle" class="lb">${nm(h)}</text>`;
    s += `<text x="${cx + bw / 2}" y="${H - 12}" text-anchor="middle" class="ax">${pp(v.pct_caen)} caen</text></g>`;
  });
  el.innerHTML = s + "</svg>";
}

function cohorts() {
  const keys = ["Antes de FY24", "Lanzados FY24", "Lanzados FY25", "Lanzados FY26"];
  const shades = { Fragancias: ["#3E2FA3", "#6250D6", "#9A8CE6", "#CFC8F5"], Makeup: ["#B4441B", "#E3602B", "#F29B77", "#F9CFBE"] };
  const box = $("cohortStack");
  box.innerHTML = catsIn().map(c => `<div class="card reveal in"><div class="ct" style="color:${col(c)}">${c}: peso de cada generación en el envío</div>
    <div class="cs">Reparto del envío de cada año fiscal según el año de lanzamiento del EAN</div><div class="chart" data-c="${c}"></div>
    <div class="legend">${keys.map((k, i) => `<span><i style="background:${shades[c][i]};border-radius:3px"></i>${k}</span>`).join("")}</div></div>`).join("");
  box.querySelectorAll(".chart").forEach(el => {
    const c = el.dataset.c, co = D.veterans.cohorts[c], w = W(el), x0 = 44, x1 = w - 4, H = 3 * 36 + 4;
    let s = `<svg viewBox="0 0 ${w} ${H}">`;
    ["FY24", "FY25", "FY26"].forEach((fy, j) => {
      const y = 4 + j * 36; let acc = x0;
      s += `<text x="${x0 - 8}" y="${y + 18}" text-anchor="end" class="lb">${fy}</text>`;
      keys.forEach((k, i) => {
        const v = (co[k] || [0, 0, 0])[j], ww = (x1 - x0) * v;
        if (ww > .5) {
          const tip = `<div class='h'>${c} · ${fy}</div>` + tipRow(k, pp(v));
          s += `<rect class="growx" x="${acc + 1}" y="${y}" width="${Math.max(ww - 2, 0)}" height="26" rx="4" fill="${shades[c][i]}" data-tip="${esc(tip)}"/>`;
          if (v >= .07) s += `<text x="${acc + ww / 2}" y="${y + 17}" text-anchor="middle" class="vl" style="fill:${i < 2 ? "#fff" : "#15171C"};pointer-events:none">${pp(v)}</text>`;
        }
        acc += ww;
      });
    });
    el.innerHTML = s + "</svg>";
  });
}

/* ---------- carga ---------- */
function dumbbell(el) {
  const order = ["BURBERRY", "Gucci Make up", "Marc Jacobs", "Gucci", "Kylie Makeup"].filter(h => housesIn().includes(h));
  const by = D.load.ean_house, w = W(el), rowH = 44, H = order.length * rowH + 34, x0 = Math.min(118, w * .3), x1 = w - 92, lo = -.3, hi = .25;
  let s = `<svg viewBox="0 0 ${w} ${H}">`;
  [-.2, -.1, 0, .1, .2].forEach(t => { const x = lerp(t, lo, hi, x0, x1); s += `<line x1="${x}" x2="${x}" y1="6" y2="${H - 24}" class="${t === 0 ? "gl0" : "gl"}"/><text x="${x}" y="${H - 8}" text-anchor="middle" class="ax">${pc(t)}</text>`; });
  order.forEach((h, i) => {
    const b = by[h], y = 24 + i * rowH, xc = lerp(b.cargado, lo, hi, x0, x1), xn = lerp(b.normal, lo, hi, x0, x1), good = b.cargado < b.normal && b.meses >= 6;
    const tip = `<div class='h'>${nm(h)}</div>` + tipRow("Cargados", pc(b.cargado)) + tipRow("Normales", pc(b.normal)) + tipRow("Descargados", pc(b.descargado)) + tipRow("Meses cargados < normales", `${b.meses} de ${b.de}`);
    s += `<g data-tip="${esc(tip)}"><rect x="0" y="${y - 18}" width="${w}" height="${rowH - 6}" fill="transparent"/>`;
    s += `<text x="${x0 - 12}" y="${y + 4}" text-anchor="end" class="lb">${nm(h)}</text>`;
    s += `<line x1="${xc}" x2="${xn}" y1="${y}" y2="${y}" stroke="var(--line)" stroke-width="6" stroke-linecap="round"/>`;
    s += `<circle cx="${xn}" cy="${y}" r="6" fill="var(--paper)" stroke="var(--ship)" stroke-width="2"/>`;
    s += `<circle cx="${xc}" cy="${y}" r="7" fill="${colH(h)}" stroke="var(--paper)" stroke-width="2"/>`;
    s += `<text x="${x1 + 12}" y="${y + 4}" class="vl" style="fill:${good ? "var(--ok)" : "var(--muted)"};font-weight:700">${b.meses} de ${b.de} meses</text></g>`;
  });
  el.innerHTML = s + "</svg>";
  const c = D.load.ean_cat;
  $("kDumbL").innerHTML = catsIn().map(k => `<b style="color:${col(k)}">${k}:</b> cargados ${pc(c[k].cargado)} frente a normales ${pc(c[k].normal)} (${c[k].meses} de ${c[k].de} meses).`).join(" ") +
    (housesIn().includes("Kylie Makeup") ? " En Kylie los «cargados» siguen creciendo: puede que gane tiendas o clientes sin EPOS; con el EPOS solo no se puede distinguir." : "");
}

function loadChart(el) {
  const h = state.h2, r = D.load.r12[h], nx = D.load.next[h], months = D.load.months, n = months.length;
  const w = W(el), H = Math.round(Math.min(320, Math.max(230, w * .5))), x0 = 46, x1 = w - 46, y0 = 14, y1 = H - 30, bw = (x1 - x0) / n;
  const rv = r.filter(v => v != null), rlo = Math.floor((Math.min(...rv) - .05) * 10) / 10, rhi = Math.ceil((Math.max(...rv) + .05) * 10) / 10;
  const lo2 = -.5, hi2 = .5, X = i => x0 + bw * (i + .5), Y2 = v => lerp(Math.max(lo2, Math.min(hi2, v)), lo2, hi2, y1, y0), Y1 = v => lerp(v, rlo, rhi, y1, y0);
  let s = `<svg viewBox="0 0 ${w} ${H}" role="img" aria-label="Carga de ${nm(h)} a lo largo del año">`;
  [-.5, -.25, 0, .25, .5].forEach(t => { const y = Y2(t); s += `<line x1="${x0}" x2="${x1}" y1="${y}" y2="${y}" class="${t === 0 ? "gl0" : "gl"}"/><text x="${x1 + 8}" y="${y + 4}" class="ax">${pc(t)}</text>`; });
  const tk = []; for (let t = rlo; t <= rhi + 1e-9; t += (rhi - rlo) > .5 ? .2 : .1) tk.push(+t.toFixed(2));
  tk.forEach(t => { s += `<text x="${x0 - 8}" y="${Y1(t) + 4}" text-anchor="end" class="ax" style="fill:${colH(h)}">${dec(t, 1)}×</text>`; });
  months.forEach((m, i) => {
    const v = nx[i];
    if (v != null) { const y = Y2(v), z = Y2(0); s += `<rect class="grow" style="transform-origin:50% ${v >= 0 ? "100%" : "0%"}" x="${X(i) - bw * .3}" y="${Math.min(y, z)}" width="${bw * .6}" height="${Math.max(Math.abs(y - z), 1)}" rx="3" fill="var(--ship)" opacity=".42"/>`; }
    if (i % (w < 520 ? 3 : 2) === 0) s += `<text x="${X(i)}" y="${H - 8}" text-anchor="middle" class="ax">${mes(m)}</text>`;
  });
  s += poly(r.map((v, i) => [X(i), Y1(v)]), colH(h), 2.6, `class="draw" pathLength="1"`);
  r.forEach((v, i) => { s += `<circle cx="${X(i)}" cy="${Y1(v)}" r="3" fill="${colH(h)}" stroke="var(--paper)" stroke-width="1.5"/>`; });
  months.forEach((m, i) => {
    const tip = `<div class='h'>${nm(h)} · ${mes(m)}</div>` + tipRow("Envío ÷ EPOS, 12 meses", dec(r[i], 2) + "×") + tipRow("Envío 3 meses siguientes", nx[i] == null ? "sin dato aún" : pc(nx[i]));
    s += `<g class="col" data-tip="${esc(tip)}"><line class="xh" x1="${X(i)}" x2="${X(i)}" y1="${y0}" y2="${y1}"/><rect class="hit" x="${X(i) - bw / 2}" y="${y0}" width="${bw}" height="${y1 - y0}"/></g>`;
  });
  el.innerHTML = s + "</svg>";
  $("loadDot").style.background = colH(h);
  const iMax = r.indexOf(Math.max(...r));
  $("kLoadL").innerHTML = `${nm(h)}: el envío por unidad de EPOS llega a su máximo en <b>${mes(months[iMax])}</b> (${dec(r[iMax], 2)}×). Las barras muestran cómo creció el envío de los 3 meses siguientes frente al año anterior. El nivel del ratio depende de qué clientes reportan; lo que importa es si sube o baja.`;
}

function exitChart(el) {
  const ex = D.load.exits, w = W(el), H = Math.round(Math.min(300, Math.max(220, w * .48))), x0 = 46, x1 = w - 14, y0 = 14, y1 = H - 40;
  const X = k => lerp(k, -6, 6, x0, x1), Y = v => lerp(Math.min(v, 1.1), 0, 1.1, y1, y0);
  let s = `<svg viewBox="0 0 ${w} ${H}">`;
  s += yAxis(x0, x1, y0, y1, 0, 1.1, [0, .25, .5, .75, 1], t => pp(t));
  s += `<rect x="${X(0)}" y="${y0}" width="${x1 - X(0)}" height="${y1 - y0}" fill="var(--line2)" opacity=".5"/>`;
  s += `<line x1="${X(0)}" x2="${X(0)}" y1="${y0}" y2="${y1}" stroke="var(--ink2)" stroke-dasharray="3 3"/><text x="${X(0) + 6}" y="${y0 + 12}" class="ax">último envío</text>`;
  for (let k = -6; k <= 6; k += 2) s += `<text x="${X(k)}" y="${y1 + 16}" text-anchor="middle" class="ax">${k > 0 ? "+" + k : k === 0 ? "0" : "−" + (-k)}</text>`;
  s += `<text x="${(x0 + x1) / 2}" y="${H - 4}" text-anchor="middle" class="axl">meses frente al último envío relevante</text>`;
  catsIn().forEach(c => {
    const cv = ex[c].curve;
    s += poly(cv.map((v, i) => [X(i - 6), Y(v)]), col(c), 2.6, `class="draw" pathLength="1"`);
    cv.forEach((v, i) => { s += `<circle cx="${X(i - 6)}" cy="${Y(v)}" r="3" fill="${col(c)}" stroke="var(--paper)" stroke-width="1.5"/>`; });
    s += `<text x="${X(6)}" y="${Y(cv[12]) + (c === "Fragancias" ? -12 : 18)}" text-anchor="end" class="vl halo" style="fill:${col(c)}">${c} ${pp(cv[12])}</text>`;
  });
  const bw = (x1 - x0) / 12;
  for (let i = 0; i <= 12; i++) {
    const k = i - 6;
    const tip = `<div class='h'>${k === 0 ? "Mes del último envío" : (k > 0 ? k + " meses después" : -k + " meses antes")}</div>` + catsIn().map(c => tipRow(c, pp(ex[c].curve[i]), css(c === "Fragancias" ? "--frag" : "--mu"))).join("") + `<div style='opacity:.7;margin-top:3px'>EPOS frente a su nivel de 6–12 meses antes</div>`;
    s += `<g class="col" data-tip="${esc(tip)}"><line class="xh" x1="${X(k)}" x2="${X(k)}" y1="${y0}" y2="${y1}"/><rect class="hit" x="${X(k) - bw / 2}" y="${y0}" width="${bw}" height="${y1 - y0}"/></g>`;
  }
  el.innerHTML = s + "</svg>";
  $("exitSub").textContent = "Mediana del EPOS de los EANs que dejaron de enviarse (" + catsIn().map(c => `${ex[c].n} de ${c.toLowerCase()}`).join(", ") + ") · 100% = su EPOS de 6–12 meses antes";
  $("kExitL").innerHTML = (catsIn().includes("Fragancias") ? `<b style="color:var(--frag)">Fragancias:</b> el EPOS sigue 6 meses después del último envío (aún al ${pp(ex.Fragancias.curve[12])}). ` : "") +
    (catsIn().includes("Makeup") ? `<b style="color:var(--mu)">Makeup:</b> se agota en 3–4 meses (${pp(ex.Makeup.curve[10])} a los 4 meses). ` : "") +
    `<br><br>Antes del corte el EPOS ya cae: es la señal de declive. Al planificar la salida de un código, cuenta con esa cola de venta en el cliente.`;
}

/* ---------- textos que dependen de los datos ---------- */
function texts() {
  const n = D.noise, t = D.trend, la = D.launch, v = D.veterans, lo = D.load;
  const vetFall = HOUSES.map(h => v.houses[h].epos_yoy).filter(x => x < -.05);
  const lo_ = Math.round(-Math.max(...vetFall) * 100), hi_ = Math.round(-Math.min(...vetFall) * 100), vr = `−${lo_} a −${hi_}%`, vrTxt = `entre un ${lo_} y un ${hi_}%`;
  const newF = 1 - v.cohorts.Fragancias["Antes de FY24"][2], newM = 1 - v.cohorts.Makeup["Antes de FY24"][2];
  $("h-ruido").textContent = `Los pedidos van a saltos: el crecimiento mensual del envío oscila unas ${Math.round(n.ratio_ruido)} veces más que el del EPOS`;
  $("h-trend").textContent = `A 12 meses, envío y EPOS van en la misma dirección en ${Math.round(t.same * 10)} de cada 10 EANs. La tendencia del EPOS se mantiene de un semestre a otro; la del envío, no`;
  $("h-launch").textContent = `El primer año se envía el doble de lo que se vende; el segundo, menos de lo normal mientras el cliente vende ese stock`;
  $("h-vet").textContent = `Los códigos veteranos pierden ${vrTxt} de venta al consumidor cada año. La casa crece por los lanzamientos`;
  $("h-load").textContent = `Si un EAN acumula 12 meses enviando más de lo que vende, los 3 meses siguientes envía menos: en fragancias pasa los ${lo.ean_cat.Fragancias.meses} meses medidos`;
  $("kNoise").textContent = pp(n.pct_env_mas_ruidoso);
  $("kNoiseL").innerHTML = `Mediana: el crecimiento mensual del envío se mueve <b>${dec(n.ratio_ruido, 1)} veces</b> más que el del EPOS (desviación típica del crecimiento de cada mes, EAN a EAN).`;
  const b = n.houses.BURBERRY, mn = a => Math.min(...a), mx = a => Math.max(...a);
  $("n-ruido").innerHTML = `Ejemplo: en Burberry el EPOS de cada mes está entre ${pc(mx(b.epos))} y ${pc(mn(b.epos))} frente al año anterior; el envío salta de ${pc(mn(b.ship))} a ${pc(mx(b.ship))}.
    <b>Un mes de envíos no dice nada de la demanda; un trimestre de EPOS, sí.</b> Por eso el trend del envío a 3–6 meses falla y la forma mensual del envío cambia de un año a otro.`;
  $("kSame").textContent = pp(t.same);
  $("kSameL").innerHTML = `de los EANs crecen o caen a la vez en FY26. Correlación ${dec(t.corr, 2)}. Como el EPOS no cubre a todos los clientes, se compara cada EAN consigo mismo, nunca en unidades.`;
  const P = t.persist;
  $("kPersistL").innerHTML = `Total: <b>${pp(P.Total.keep_epos)}</b> frente a ${pp(P.Total.keep_ship)}. Correlación de un semestre al siguiente: EPOS ${dec(P.Total.corr_epos, 2)} frente a envío ${dec(P.Total.corr_ship, 2)}.
    En makeup el EPOS de jul–dic anticipa el envío de ene–jun mejor que el propio envío (${dec(P.Makeup.epos_to_ship, 2)} frente a ${dec(P.Makeup.corr_ship, 2)}).`;
  $("n-launch").innerHTML = `En fragancias el mes del lanzamiento se envía el ${pp(la.Fragancias.m0_ship)} de lo que el consumidor comprará en 13 meses.
    <b>Consecuencia para la regla:</b> para un EAN de 12–23 meses, el «mismo mes del año pasado» es llenado de canal y la base sale inflada. Es donde más falla la regla de fragancias (EANs de 6–17 meses).
    Para esos EANs la base debería ser el EPOS × la relación de los veteranos (o algo menos), no el envío del año anterior.`;
  $("n-vet").innerHTML = `<b>Consecuencia para el trend:</b> el trend de la casa mezcla dos poblaciones. A un EAN veterano de Gucci no le aplica el ${pc(v.houses.Gucci.casa_epos_yoy)} de la casa sino un ${pc(v.houses.Gucci.epos_yoy)}; a uno de Kylie, un ${pc(v.houses["Kylie Makeup"].epos_yoy)} y no el ${pc(v.houses["Kylie Makeup"].casa_epos_yoy)}.
    En FY26 los lanzamientos desde FY24 ya son el ${pp(newF)} del envío en fragancias y el ${pp(newM)} en makeup. El trend de un EAN debería salir de su generación (los de su edad en su casa) y medirse en EPOS.`;
  const tiles = [
    [`${Math.round(n.ratio_ruido)}×`, "más ruido en el envío", `El crecimiento mensual del envío oscila ~${Math.round(n.ratio_ruido)} veces más que el del EPOS (${pp(n.pct_env_mas_ruidoso)} de los EANs).`, "#ruido"],
    [pp(t.same), "misma dirección a 12 meses", `Envío y EPOS crecen o caen juntos en ${Math.round(t.same * 10)} de cada 10 EANs en el año.`, "#tendencia"],
    [`${pp(P.Total.keep_epos)} <span style="color:var(--muted)">vs</span> ${pp(P.Total.keep_ship)}`, "la tendencia persiste", "El EPOS mantiene su dirección de un semestre a otro; el envío, mucho menos.", "#tendencia"],
    [`${dec(la.Fragancias.y1, 1)}× → ${dec(la.Fragancias.y2, 2)}×`, "lanzamientos de fragancias", `Envío por unidad vendida en el año 1 y en el año 2 (veteranos ${dec(la.Fragancias.vet_ratio, 2)}×).`, "#lanzamientos"],
    [vr, "veteranos, cada año", "Venta al consumidor de los códigos con historia; la casa crece por los lanzamientos (Marc Jacobs, 0%).", "#ciclo"],
    [`${lo.ean_cat.Fragancias.meses} de ${lo.ean_cat.Fragancias.de}`, "meses: la carga se corrige", "Fragancias: si en 12 meses se envía de más frente al EPOS, los 3 meses siguientes se envía menos.", "#carga"],
  ];
  $("tiles").innerHTML = tiles.map(([a, k, d, href]) => `<a class="tile reveal" href="${href}"><span class="go">ver →</span><div class="tv">${a}</div><div class="tk">${k}</div><div class="td">${d}</div></a>`).join("");
  const rules = [
    ["La tendencia, del EPOS", "Trend del EAN = crecimiento de 12 meses de su EPOS, comparándolo consigo mismo.", `El EPOS mantiene su dirección de un semestre a otro en el ${pp(P.Total.keep_epos)} de los EANs; el envío, en el ${pp(P.Total.keep_ship)}.`, "#tendencia"],
    ["Seguir a mi generación", "Veteranos: el crecimiento del EPOS de los veteranos de su casa, nunca el trend total de la casa.", `Los veteranos pierden ${vrTxt} al año (Marc Jacobs, 0%); el total de la casa incluye los lanzamientos y engaña.`, "#ciclo"],
    ["Lanzamientos: año 2 ≠ año 1", `Del mes 12 al 23, base = EPOS × ${dec(Math.min(la.Fragancias.y2, la.Makeup.y2), 2)}–${dec(Math.max(la.Fragancias.y2, la.Makeup.y2), 2)}, no el envío del año pasado.`, `El envío del año 1 fue llenado de canal: ${dec(la.Fragancias.y1, 1)}× (fragancias) y ${dec(la.Makeup.y1, 1)}× (makeup) lo que se vendió.`, "#lanzamientos"],
    ["Semáforo de carga", "Si envío/EPOS de 12 meses supera en un 15% su propio FY25, recortar los meses siguientes.", "Funciona en fragancias y Gucci Make up; en Kylie no, hasta tener el WOS.", "#carga"],
    ["Bajas", "Al planificar la salida de un código, contar con que el cliente sigue vendiendo después del último envío.", "Unos 6 meses en fragancias y 3–4 en makeup.", "#carga"],
  ];
  $("rules").innerHTML = rules.map(([t_, s_, ev, href], i) => `<div class="rule${i === 0 ? " open" : ""}"><button aria-expanded="${i === 0}"><span class="rn">${i + 1}</span><span><span class="rt">${t_}</span><div class="rs">${s_}</div></span>
    <svg class="chev" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg></button>
    <div class="rd"><div><div class="in"><b>Evidencia:</b> ${ev}<div class="ev"><a href="${href}">Ver el gráfico ↑</a></div></div></div></div></div>`).join("");
  document.querySelectorAll(".rule button").forEach(b => b.addEventListener("click", () => {
    const r = b.parentElement, o = !r.classList.contains("open"); r.classList.toggle("open", o); b.setAttribute("aria-expanded", o);
  }));
}

/* ---------- controles ---------- */
function seg(el, items, value, onPick) {
  el.innerHTML = `<span class="pill"></span>` + items.map(([v, lab, c]) => `<button data-v="${esc(v)}" aria-pressed="${v === value}">${c ? `<i class="dot" style="background:${c}"></i>` : ""}${lab}</button>`).join("");
  bindSeg(el, onPick);
}
function bindSeg(el, onPick) {
  if (!el.querySelector(".pill")) el.insertAdjacentHTML("afterbegin", `<span class="pill"></span>`);
  const place = () => {
    const on = el.querySelector('button[aria-pressed="true"]'), pill = el.querySelector(".pill");
    if (on) { pill.style.width = on.offsetWidth + "px"; pill.style.transform = `translateX(${on.offsetLeft}px)`; }
  };
  el.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
    if (b.disabled) return;
    el.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b)); place(); onPick(b.dataset.v);
  }));
  el._place = place; requestAnimationFrame(place);
}
function houseSegs() {
  const hs = housesIn();
  if (!hs.includes(state.h1)) state.h1 = hs[0];
  if (!hs.includes(state.h2)) state.h2 = hs.includes("Gucci Make up") ? "Gucci Make up" : hs[0];
  const items = hs.map(h => [h, nm(h), colH(h)]);
  seg($("houseSeg1"), items, state.h1, v => { state.h1 = v; drawNoise(); });
  seg($("houseSeg2"), items, state.h2, v => { state.h2 = v; loadChart($("cLoad")); });
}
function drawNoise() {
  noiseChart($("cNoise"), state.h1);
  $("noiseDot").style.background = colH(state.h1);
  $("noiseSub").textContent = `${nm(state.h1)} · ${D.noise.houses[state.h1].n} EANs maduros · pasa el ratón por cada mes`;
}
function drawHero() {
  const h = "BURBERRY";
  $("sigT").textContent = `${nm(h)}, jul-25 → jul-26: el EPOS se mueve en una franja estrecha; el envío, no`;
  noiseChart($("cHero"), h, { labels: true, H: Math.round(Math.min(300, Math.max(210, W($("cHero")) * .3))) });
}
function table() {
  const hs = housesIn(), T = D.trend.by_house;
  $("tbHouse").innerHTML = `<tr><th>Casa</th><th>EANs</th><th>Misma dirección</th><th>Correlación</th></tr>` + hs.map(h => `<tr><td><i class="sw" style="background:${colH(h)}"></i>${nm(h)}</td><td>${T[h].n}</td>
    <td><div class="meter"><div class="m"><span style="width:${T[h].same * 100}%;background:${colH(h)}"></span></div>${pp(T[h].same)}</div></td><td>${dec(T[h].corr, 2)}</td></tr>`).join("");
}
function launchSeg() {
  const el = $("launchSeg");
  if (state.cat !== "all") state.launch = state.cat;
  el.querySelectorAll("button").forEach(b => { b.setAttribute("aria-pressed", b.dataset.v === state.launch); b.disabled = state.cat !== "all" && b.dataset.v !== state.cat; });
  el._place && el._place();
}

function drawAll() {
  drawHero(); drawNoise(); rangeChart($("cRange")); scatter($("cScatter")); table(); persistChart($("cPersist"));
  launchSeg(); launchChart($("cLaunch")); ratioChart($("cRatio")); vetChart($("cVet")); cohorts();
  dumbbell($("cDumb")); loadChart($("cLoad")); exitChart($("cExit"));
}

/* ---------- tooltip ---------- */
const tip = $("tip");
let tipOn = null;
function moveTip(x, y) {
  const r = tip.getBoundingClientRect(), pad = 14;
  let tx = x + pad, ty = y + pad;
  if (tx + r.width > innerWidth - 8) tx = x - r.width - pad;
  if (ty + r.height > innerHeight - 8) ty = y - r.height - pad;
  tip.style.left = Math.max(8, tx) + "px"; tip.style.top = Math.max(8, ty) + "px";
}
document.addEventListener("pointerover", e => {
  const t = e.target.closest("[data-tip]");
  if (!t) return;
  tipOn = t; tip.innerHTML = t.getAttribute("data-tip"); tip.classList.add("on"); moveTip(e.clientX, e.clientY);
  const pt = t.classList.contains("pt") ? t : null;
  if (pt) pt.setAttribute("r", +pt.getAttribute("r") + 2);
});
document.addEventListener("pointermove", e => { if (tipOn) moveTip(e.clientX, e.clientY); });
document.addEventListener("pointerout", e => {
  const t = e.target.closest("[data-tip]");
  if (t && t === tipOn && !t.contains(e.relatedTarget)) {
    tip.classList.remove("on"); tipOn = null;
    if (t.classList.contains("pt")) t.setAttribute("r", +t.getAttribute("r") - 2);
  }
});
addEventListener("scroll", () => { if (tipOn) { tip.classList.remove("on"); tipOn = null; } }, { passive: true });

/* ---------- arranque ---------- */
texts();
bindSeg($("catSeg"), v => { state.cat = v; houseSegs(); drawAll(); markDrawn(); });
bindSeg($("launchSeg"), v => { state.launch = v; launchChart($("cLaunch")); ratioChart($("cRatio")); markDrawn(); });
houseSegs();
drawAll();

// Tras la primera aparición, los redibujados (filtros, pestañas) no repiten la animación de entrada.
function markDrawn() { document.querySelectorAll(".reveal.in").forEach(el => setTimeout(() => el.classList.add("drawn"), 0)); }
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); setTimeout(() => e.target.classList.add("drawn"), 1700); }
}), { threshold: .12, rootMargin: "0px 0px -6% 0px" });
document.querySelectorAll(".reveal").forEach(el => io.observe(el));

const secs = [...document.querySelectorAll("section.sec")], links = [...document.querySelectorAll("#nav a")];
addEventListener("scroll", () => {
  $("bar").classList.toggle("scrolled", scrollY > 8);
  let cur = null; secs.forEach(s => { if (s.getBoundingClientRect().top < 140) cur = s.id; });
  links.forEach(a => a.classList.toggle("on", a.getAttribute("href") === "#" + cur));
}, { passive: true });

let rz; addEventListener("resize", () => { clearTimeout(rz); rz = setTimeout(() => { drawAll(); markDrawn(); document.querySelectorAll(".seg").forEach(s => s._place && s._place()); }, 120); });

$("theme").addEventListener("click", () => {
  const dark = document.documentElement.dataset.theme ? document.documentElement.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  document.documentElement.dataset.theme = dark ? "light" : "dark";
  try { localStorage.setItem("epos-theme", document.documentElement.dataset.theme); } catch (e) {}
  drawAll(); markDrawn();
});
try { const t = localStorage.getItem("epos-theme"); if (t) { document.documentElement.dataset.theme = t; drawAll(); } } catch (e) {}
document.fonts && document.fonts.ready.then(() => document.querySelectorAll(".seg").forEach(s => s._place && s._place()));
</script>
</body>
</html>
"""


def main():
    D = json.loads((ROOT / "work" / "epos_patrones.json").read_text())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(HTML.replace("__DATA__", json.dumps(D, separators=(",", ":"))), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
