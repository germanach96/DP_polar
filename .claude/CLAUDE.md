# Skills y plugins: check obligatorio al empezar
Al arrancar cada sesión, `.claude/hooks/session-start.sh` instala lo que falte y deja en el contexto la tabla «Check de skills y plugins» más la **revisión de funcionamiento**: `.claude/hooks/skills-health.py` abre cada SKILL.md (repo y plugins) y prueba de verdad Impeccable (`detect`) y Graphify (`query`). Se puede repetir con `.claude/hooks/check-tools.sh`.

**Revisión en cada mensaje:** el hook de cada mensaje vuelve a correr `skills-health.py --short` (menos de 1 s) y deja la línea «Revisión de skills: …» en el contexto. Si dice FALLA, parar y decir al usuario qué falta, aunque la tarea no parezca necesitar esa skill.

**Lo primero de cada conversación, antes de hacer nada de lo que pida el usuario:**
1. Mostrar el check: una línea por skill/plugin con «funcionando» o «falta» y el motivo. Para los dos plugins (Ponytail, Impeccable) no basta con «instalado»: confirmar que su skill (`ponytail`, `impeccable`) aparece en la lista de skills disponibles de la sesión. Si está instalado pero no cargado, decirlo: se activa al reiniciar la sesión.
2. Si algo falta o no funciona (en el check, en la línea «Revisión de skills» o al cargar una skill con Skill y que dé error): **parar**, decir qué falta y qué hace falta para usarlo (comando, permiso, red o clave), y esperar al usuario. No seguir con la tarea.
3. Si todo funciona: seguir y **usar las skills en el trabajo**: cargar con la herramienta Skill las que encajen con la tarea antes de empezar, y decir cuáles se usaron. No aplicar sus ideas de memoria sin cargarlas.

| Skill / plugin | Origen | Instalar | Cuándo usarla |
|---|---|---|---|
| Ponytail (plugin) | github.com/DietrichGebert/ponytail | `/plugin marketplace add DietrichGebert/ponytail` y `/plugin install ponytail@ponytail` | **Solo en código puro** (Python, scripts, hooks, bugs): la solución más simple que funcione. Apagado en todo lo demás (ver «Ponytail: solo código puro») |
| Agent Skills (25) | github.com/addyosmani/agent-skills | `npx skills add addyosmani/agent-skills` | Método: planificar, depurar, tests, revisión, git, documentar |
| OmniRoute (CLI) | github.com/diegosouzapw/OmniRoute | `npm install -g omniroute` | **No operativo** (acordado 2026-10-11): sin servidor ni API keys; el check lo marca sin bloquear |
| Graphify | github.com/Graphify-Labs/graphify | `uv tool install graphifyy` y `graphify install` | Grafo versionado en `graphify-out/` (código + documentos; `.graphifyignore` deja fuera skills, `work/` y `reportes/`). Se actualiza solo al arrancar. Para preguntas sobre el código o dónde está algo: `graphify query "…"` primero. Si cambian los .md, `/graphify . --update` |
| Taste Skill (13) | tasteskill.dev | `npx skills add Leonxlnx/taste-skill` | Diseño de páginas, reportes HTML y estilo visual |
| Impeccable (plugin) | impeccable.style | `/plugin marketplace add pbakaus/impeccable` y `/plugin install impeccable@impeccable` | Diseñar, auditar y pulir (`/impeccable`). Contexto en `PRODUCT.md` (para quién y para qué) y `DESIGN.md` + `.impeccable/design.json` (sistema visual «El Parlamento») |
| Emil Kowalski (14) | emilkowal.ski/skill | `npx skills add emilkowalski/skill` | Animación, interacción y detalles de interfaz |

Además, para cualquier gráfico: skill `dataviz`.

## Ponytail: solo código puro (decidido por el usuario 2026-10-11)
Ponytail empuja a «lo mínimo que funcione» y recorta pulido; en decisiones de diseño eso choca con Impeccable, Taste, Emil y `DESIGN.md`. Por eso:
- **Encendido** solo cuando la tarea es código puro: el mensaje habla de código (Python, script, `.py`, función, bug, test, hook, pandas…) y de nada visual.
- **Apagado** en todo lo demás: diseño (HTML, CSS, SVG, PDF, reporte, página, gráfico, colores, hemiciclo, explorador, animación, interfaz…), preguntas de negocio, análisis y método. Si el mensaje mezcla código y diseño, **gana el diseño**: un script que genera un reporte se trata como diseño.
- Lo decide `.claude/hooks/ponytail-switch.py` en cada mensaje (por palabras clave) y deja en el contexto «PONYTAIL ACTIVO» o «PONYTAIL APAGADO». Apagado borra el flag del plugin, así sus subagentes y su barra de estado tampoco lo aplican.
- Con «PONYTAIL APAGADO», las reglas de Ponytail que se inyectan al arrancar la sesión **no se aplican**: no se recortan pasos de las skills, ni pulido, ni detalle por «lo mínimo». El cierre de Ponytail («qué me salté») tampoco hace falta; basta la línea de las 7.
- El usuario puede forzarlo con los comandos del plugin (`/ponytail full`, `stop ponytail`); el hook no los pisa en ese mensaje.
- En la línea final: «Ponytail (usado: código puro)» o «Ponytail (apagado: tarea de diseño / no es código)».

## Skills en cada tarea, no solo al empezar (lección 2026-10-11)
Error cometido: se cargaron skills para el primer HTML y el segundo (explorador) se hizo de memoria, sin cargar ninguna, sin performance, sin auditoría y sin validar colores nuevos; los avisos del hook de Impeccable se ignoraron sin decirlo.

**Cada petición nueva del usuario es una tarea nueva:** volver a mirar esta tabla y cargar con Skill las que encajen, aunque se hayan cargado antes en la conversación. Lo cargado en una tarea anterior no cuenta.

| Tipo de tarea | Cargar antes de empezar (Skill) | Antes de entregar (obligatorio) |
|---|---|---|
| Código Python / scripts (código puro) | `ponytail` (encendido por el hook), `code-review-and-quality` | Un `assert` o autocomprobación en cada script nuevo; revisar el diff |
| HTML / página / reporte | `artifact-design`, `impeccable` (lee `PRODUCT.md`/`DESIGN.md`), una de Taste (`design-taste-frontend` o `high-end-visual-design`) y una de Emil (`emil-design-eng`) | `impeccable detect --json <archivos>` una vez y triar cada aviso; capturas escritorio + móvil, claro + oscuro; seguir `DESIGN.md` |
| Gráficos / colores | `dataviz` | `validate_palette.js` con **todos** los colores nuevos, en claro y en oscuro |
| Animación / interacción | `animate`, `emil-design-eng` | Respeta `prefers-reduced-motion`; respuesta táctil (`DESIGN.md`) |
| Pregunta sobre el código o la estructura | `graphify` | Responder desde `graphify query`, citando archivo y línea |
| Página interactiva con datos (filtros, muchas filas) | `performance-optimization` | Medir con Playwright el tiempo de cada filtro/clic y el peso del archivo; redibujar solo lo que cambia |

Reglas:
- **Avisos de hooks** (Impeccable u otros): cada uno se arregla, se ignora con motivo o se pregunta, y se dice en la respuesta. Nunca en silencio.
- **Pasos que una skill exige y se saltan** (p. ej. la entrevista de Impeccable): decirlo en la respuesta y por qué, no omitirlo.
- **Respuesta final (obligatoria, la comprueba un hook):** termina con
  `Skills y plugins: Ponytail (…) · Agent Skills (…) · OmniRoute (…) · Graphify (…) · Taste (…) · Impeccable (…) · Emil (…)`
  con «usado: qué skill» o «no aplica: motivo» en cada una, y di qué pasos de skills no se hicieron.

## Hooks que lo hacen cumplir (`.claude/settings.json`)
- `UserPromptSubmit` → `.claude/hooks/skills-reminder.sh`: en cada mensaje revisa que todas las skills funcionan (`skills-health.py --short`), enciende o apaga Ponytail (`ponytail-switch.py`, autocomprobación con `--selftest`) y recuerda que es tarea nueva y qué cargar.
- `Stop` → `.claude/hooks/skills-stop-check.py`: no deja cerrar el turno si falta la línea con las 7, si se escribió HTML/CSS/SVG sin `impeccable` + una de Taste + una de Emil o sin pasar `impeccable detect`, o Python sin `code-review-and-quality` (o `ponytail:ponytail-review`). Detecta archivos escritos con Write/Edit o desde Bash (`>`/`tee`). Solo mira lo cargado en el turno actual. Bloquea una vez por turno (no hace bucle) y si falla deja pasar.
- `SessionStart` → `.claude/hooks/session-start.sh`: instala lo que falte, actualiza el grafo de Graphify (código, sin IA) y muestra el check con la revisión de funcionamiento completa.
- Todas las skills siguen activas (decisión del usuario 2026-10-11: no desactivar ninguna). OmniRoute no se puede usar por ahora; Ponytail solo en código puro; las otras 5 se usan según la tabla y se da cuenta de las 7 en cada respuesta.

# graphify
- **graphify** (`.claude/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.
