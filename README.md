# pyspec

A specs framework for working tickets with coding agents (Claude Code for
now; other agents later). Works both for multi-repo setups (backend,
frontend, infra in separate repos) and for a single repo.

## What problem it solves

When a ticket touches code the agent has no memory of — whether because
it lives in another repo, or simply because time passed since that part of
the system was last touched — it's easy for a coding agent to lose
context: it doesn't know how the system works today, it leaves no trace of
why it made a decision, and it's hard to verify afterwards whether it
actually implemented what it said it would. This shows up more the more
repos a ticket touches, but it happens in a single repo too.

pyspec standardizes this with three versioned folders (in a dedicated
specs repo if you work multi-repo, or inside the project's own repo if
it's just one):

```
specs/
├── current/   # ACTUAL state of the system, one file per module. Alive,
│              # always kept up to date, never archived.
├── active/    # One .spec per ticket IN PROGRESS: context + plan + files
│              # to touch + technical justification.
└── archive/   # Specs of closed tickets. Historical record of "why does
               # this rule/column/decision exist".
```

The rule for deciding where something goes: if it's still being decided
or justified, it lives in `active/` for the duration of the ticket. Once
it's a settled fact that any future ticket needs to know, it gets
consolidated into `current/<module>.md`, with a `[sc-<id>]` reference back
to the originating ticket.

## What pyspec (the tool) does vs. what the agent does

pyspec is deliberately a thin layer: fetching tickets, scaffolding files,
and moving active → archive. Everything that requires judgment — reading
code, writing the plan, deciding what goes into `current/` — is done by
the coding agent (Claude Code), not pyspec.

| pyspec (CLI)                 | Agent (Claude Code)                                   |
|-------------------------------|-------------------------------------------------------|
| Data source config            | Reads `current/` and the relevant code                |
| Normalized ticket fetch        | Writes the plan and the technical decisions           |
| Creates `active/sc-<id>.spec` from a template | Fills in the spec's content            |
| Moves `active/` → `archive/`  | Decides when a ticket is ready to close, updates `current/` |

## Install

```bash
pip install -e .
```

(PyPI publishing: pending.)

## Usage

From the root of your team's specs repo (multi-repo) or the root of the
project (single repo):

```bash
pyspec init
```

It asks you for:

- **Ticket data source**: `trello`, `shortcut` or `manual` (paste the
  ticket text by hand). For Trello/Shortcut, pyspec never stores
  credentials in the config — only the *name* of the environment
  variables you'll set them in (e.g. `TRELLO_API_KEY`, `TRELLO_TOKEN`).
- **Repo paths** for the team (backend, frontend, infra), relative to the
  specs repo. These are optional: for a single-repo setup, leave them
  empty or fill in just one (e.g. `backend: .`) — they're only used to
  parametrize the Claude Code commands, they don't change the rest of
  pyspec's behavior.
- **Coding agent**: only `claude-code` for now.

This generates:

- `.pyspec/config.yaml` with the config (not versioned, see `.gitignore`).
- `specs/current/`, `specs/active/`, `specs/archive/`.
- `.claude/commands/pyspec/explore.md`, `execute.md`, `verify.md`,
  `archive.md` — Claude Code commands parametrized with your repo
  paths, exposed as `/pyspec:explore`, `/pyspec:execute`,
  `/pyspec:verify`, `/pyspec:archive` (directory-based namespacing).

### Ticket workflow

1. `/pyspec:explore <id>` — Claude Code reads the ticket, reads
   `current/` and the code, and writes `specs/active/sc-<id>.spec`. It
   stops and explicitly asks for approval before touching any code.
2. `/pyspec:execute <id>` — implements the approved spec.
3. `/pyspec:verify <id>` — compares the spec against the actual diff
   before the ticket is considered done.
4. `/pyspec:archive <id>` — updates `specs/current/<module>.md` with what
   was actually implemented (adding `[sc-<id>]` to every new or modified
   line) and moves the spec to `archive/`.

### CLI commands

```bash
pyspec init                          # configure this specs repo
pyspec upgrade                       # re-generate the Claude Code commands after a pyspec update
pyspec fetch <ticket-id>             # fetch a normalized ticket and print it
pyspec new <ticket-id> [--modulo x]  # create specs/active/sc-<id>.spec from the template
pyspec archive <ticket-id>           # move active/sc-<id>.spec to archive/
pyspec status                        # list active tickets and documented modules
```

## Multi-repo setup

The specs repo is independent from backend/frontend/infra — it doesn't
live inside any of them, so you don't have to arbitrarily pick one when a
ticket touches several repos. To work, all the repos a ticket needs must
be accessible in the same Claude Code session (cloned side by side, or
adding the specs repo with `/add-dir`).

## Project status

First implementation. Supports Claude Code as the only agent; the design
leaves room to add others (e.g. Codex) as a new adapter under
`pyspec/adapters/`, without touching the fetch/scaffold/archive logic.
