# Skills y plugins: check obligatorio al empezar
Al arrancar cada sesión, `.claude/hooks/session-start.sh` instala lo que falte y deja en el contexto la tabla «Check de skills y plugins». Se puede repetir con `.claude/hooks/check-tools.sh`.

**Lo primero de cada conversación, antes de hacer nada de lo que pida el usuario:**
1. Mostrar el check: una línea por skill/plugin con «funcionando» o «falta» y el motivo. Para los dos plugins (Ponytail, Impeccable) no basta con «instalado»: confirmar que su skill (`ponytail`, `impeccable`) aparece en la lista de skills disponibles de la sesión. Si está instalado pero no cargado, decirlo: se activa al reiniciar la sesión.
2. Si algo falta o no funciona: **parar**, decir qué falta y qué hace falta para usarlo (comando, permiso, red o clave), y esperar al usuario. No seguir con la tarea.
3. Si todo funciona: seguir y **usar las skills en el trabajo**: cargar con la herramienta Skill las que encajen con la tarea antes de empezar, y decir cuáles se usaron. No aplicar sus ideas de memoria sin cargarlas.

| Skill / plugin | Origen | Instalar | Cuándo usarla |
|---|---|---|---|
| Ponytail (plugin) | github.com/DietrichGebert/ponytail | `/plugin marketplace add DietrichGebert/ponytail` y `/plugin install ponytail@ponytail` | Al escribir o revisar código: la solución más simple que funcione |
| Agent Skills (25) | github.com/addyosmani/agent-skills | `npx skills add addyosmani/agent-skills` | Método: planificar, depurar, tests, revisión, git, documentar |
| OmniRoute (CLI) | github.com/diegosouzapw/OmniRoute | `npm install -g omniroute` | Enrutar modelos de IA; necesita servidor y API keys configurados |
| Graphify | github.com/Graphify-Labs/graphify | `uv tool install graphifyy` y `graphify install` | Preguntas sobre el código y la estructura del proyecto (`/graphify`) |
| Taste Skill (13) | tasteskill.dev | `npx skills add Leonxlnx/taste-skill` | Diseño de páginas, reportes HTML y estilo visual |
| Impeccable (plugin) | impeccable.style | `/plugin marketplace add pbakaus/impeccable` y `/plugin install impeccable@impeccable` | Pulir y auditar diseño frontend (`/impeccable`) |
| Emil Kowalski (14) | emilkowal.ski/skill | `npx skills add emilkowalski/skill` | Animación, interacción y detalles de interfaz |

Además, para cualquier gráfico: skill `dataviz`.

## Skills en cada tarea, no solo al empezar (lección 2026-10-11)
Error cometido: se cargaron skills para el primer HTML y el segundo (explorador) se hizo de memoria, sin cargar ninguna, sin performance, sin auditoría y sin validar colores nuevos; los avisos del hook de Impeccable se ignoraron sin decirlo.

**Cada petición nueva del usuario es una tarea nueva:** volver a mirar esta tabla y cargar con Skill las que encajen, aunque se hayan cargado antes en la conversación. Lo cargado en una tarea anterior no cuenta.

| Tipo de tarea | Cargar antes de empezar (Skill) | Antes de entregar (obligatorio) |
|---|---|---|
| Código Python / scripts | `ponytail` (activo), `code-review-and-quality` | Un `assert` o autocomprobación en cada script nuevo; revisar el diff |
| HTML / página / reporte | `artifact-design`, `impeccable`, una de Taste (`design-taste-frontend` o `high-end-visual-design`) | `impeccable detect --json <archivos>` una vez y triar cada aviso; capturas escritorio + móvil, claro + oscuro |
| Gráficos / colores | `dataviz` | `validate_palette.js` con **todos** los colores nuevos, en claro y en oscuro |
| Animación / interacción | `animate`, `emil-design-eng` | Respeta `prefers-reduced-motion` |
| Página interactiva con datos (filtros, muchas filas) | `performance-optimization` | Medir con Playwright el tiempo de cada filtro/clic y el peso del archivo; redibujar solo lo que cambia |

Reglas:
- **Avisos de hooks** (Impeccable u otros): cada uno se arregla, se ignora con motivo o se pregunta, y se dice en la respuesta. Nunca en silencio.
- **Pasos que una skill exige y se saltan** (p. ej. la entrevista de Impeccable): decirlo en la respuesta y por qué, no omitirlo.
- **Respuesta final:** una línea «Skills usadas: …» y otra «Pasos de skills no hechos: …» (o «ninguno»).

# graphify
- **graphify** (`.claude/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.
