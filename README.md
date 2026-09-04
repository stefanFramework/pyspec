# pyspec

Framework de specs multi-repo para trabajar tickets con agentes de codigo
(Claude Code por ahora; otros agentes a futuro).

## Que problema resuelve

Cuando un ticket toca varios repos (backend, frontend, infra), es facil que
un agente de codigo pierda contexto: no sabe como funciona el sistema hoy,
no deja rastro de por que tomo una decision, y es dificil verificar despues
si implemento todo lo que dijo que iba a implementar.

pyspec estandariza eso con tres carpetas versionadas en un repo de specs
propio (separado de backend/frontend/infra):

```
specs/
├── current/   # Estado ACTUAL del sistema, un archivo por modulo. Vivo,
│              # se actualiza siempre, nunca se archiva.
├── active/    # Un .spec por ticket EN CURSO: contexto + plan + archivos
│              # a tocar + justificacion tecnica.
└── archive/   # Specs de tickets ya cerrados. Registro historico de "por
               # que existe esta regla/columna/decision".
```

La regla para decidir donde va cada cosa: si todavia se esta decidiendo o
justificando, vive en `active/` mientras dura el ticket. Si es un hecho
consumado que cualquier ticket futuro necesita conocer, se consolida en
`current/<modulo>.md`, con una referencia `[sc-<id>]` al ticket de origen.

## Que hace pyspec (la herramienta) y que hace el agente

pyspec es deliberadamente una capa fina: fetch de tickets, scaffolding de
archivos y movimiento active → archive. Todo lo que requiere criterio
—leer codigo, redactar el plan, decidir que va en `current/`— lo hace el
agente de codigo (Claude Code), no pyspec.

| pyspec (CLI)              | Agente (Claude Code)                          |
|----------------------------|-----------------------------------------------|
| Config de fuente de datos | Lee `current/` y el codigo relevante          |
| Fetch normalizado del ticket | Redacta el plan y las decisiones tecnicas  |
| Crea `active/sc-<id>.spec` desde plantilla | Completa el contenido del spec |
| Mueve `active/` → `archive/` | Decide cuando el ticket esta listo para cerrar, actualiza `current/` |

## Instalacion

```bash
pip install -e .
```

(Publicacion en PyPI: pendiente.)

## Uso

En la raiz del repo de specs de tu equipo:

```bash
pyspec init
```

Te pregunta:

- **Fuente de datos de tickets**: `trello`, `shortcut` o `manual` (pegar el
  texto del ticket a mano). Para Trello/Shortcut, pyspec no guarda
  credenciales en el config — solo el *nombre* de las variables de entorno
  donde las vas a poner (ej. `TRELLO_API_KEY`, `TRELLO_TOKEN`).
- **Rutas de los repos** del equipo (backend, frontend, infra), relativas
  al repo de specs.
- **Agente de codigo**: por ahora solo `claude-code`.

Esto genera:

- `.pyspec/config.yaml` con la config (no se versiona, ver `.gitignore`).
- `specs/current/`, `specs/active/`, `specs/archive/`.
- `.claude/commands/pyspec-explore.md`, `pyspec-execute.md`,
  `pyspec-verify.md`, `pyspec-archive.md` — comandos de Claude Code
  parametrizados con las rutas de tus repos.

### Workflow de un ticket

1. `/pyspec-explore <id>` — Claude Code lee el ticket, lee `current/` y el
   codigo, y arma `specs/active/sc-<id>.spec`. Se frena y pide aprobacion
   explicita antes de tocar codigo.
2. `/pyspec-execute <id>` — implementa siguiendo el spec aprobado.
3. `/pyspec-verify <id>` — compara el spec contra el diff real antes de
   dar el ticket por cerrado.
4. `/pyspec-archive <id>` — actualiza `specs/current/<modulo>.md` con lo
   que efectivamente quedo implementado (agregando `[sc-<id>]` a cada
   linea nueva o modificada) y mueve el spec a `archive/`.

### Comandos de la CLI

```bash
pyspec init                          # configura este repo de specs
pyspec fetch <ticket-id>             # trae un ticket normalizado y lo imprime
pyspec new <ticket-id> [--modulo x]  # crea specs/active/sc-<id>.spec desde la plantilla
pyspec archive <ticket-id>           # mueve active/sc-<id>.spec a archive/
pyspec status                        # lista tickets activos y modulos documentados
```

## Setup multi-repo

El repo de specs es independiente de backend/frontend/infra — no vive
dentro de ninguno, para no elegir arbitrariamente donde meterlo cuando un
ticket toca varios repos. Para trabajar, todos los repos necesarios deben
estar accesibles en la misma sesion de Claude Code (clonados uno al lado
del otro, o sumando el repo de specs con `/add-dir`).

## Estado del proyecto

Primera implementacion. Soporta Claude Code como unico agente; el diseño
deja lugar para sumar otros (ej. Codex) como un adapter nuevo en
`pyspec/adapters/`, sin tocar la logica de fetch/scaffold/archive.
