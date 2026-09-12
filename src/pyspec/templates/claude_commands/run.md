---
description: Runs the full pyspec pipeline (explore, execute, verify, archive) for one or more tickets. Stops to ask for plan approval on each ticket unless --skip-permissions is passed.
argument-hint: <ticket-id> [<ticket-id> ...] [--skip-permissions] [--auto-pr]
---

Full pipeline for one or more tickets. Arguments: `$ARGUMENTS`.

## Parsing the arguments

Split `$ARGUMENTS` on whitespace/commas. `--skip-permissions` and
`--auto-pr` are flags and can appear anywhere; every other token is a
ticket id, in the order given. With a `manual` data source and no id at
all, that's only valid for a single-ticket run — a queue of more than one
ticket needs an explicit id per ticket so each one is distinguishable.

Configured ticket data source: `$data_source`.

## Queue

- **One id:** run the steps below once, for it.
- **Several ids:** process them one after another, in the given order.
  State the queue up front, before touching anything, so the user sees
  the order before any work starts.
- **A blocked ticket doesn't stop the queue.** If one can't be finished
  (contradictory acceptance criteria, a decision only a human can make, a
  gate that fails for reasons outside its scope), report it, leave its
  spec in `active/` unarchived, and move on to the next id. List it as
  not done in the final summary.
- Report on each ticket as it finishes — don't save every report for the
  end.

## Per ticket

1. **Explore.** Read `.claude/commands/pyspec/explore.md` and carry out
   its steps for this ticket id (use this ticket's id wherever that file
   refers to `$ARGUMENTS`).
2. **Approval gate:**
   - **Without `--skip-permissions`:** stop here. Show the plan and wait
     for the user's explicit approval before continuing to step 3 for
     this ticket. Don't move on to the next ticket in the queue either
     until you get an answer for this one.
   - **With `--skip-permissions`:** don't stop — the spec just written is
     the contract from here on. Continue straight to step 3. Only stop
     mid-flight if the ticket is genuinely blocked (see Queue rules
     above).
3. **Execute.** Read `.claude/commands/pyspec/execute.md` and carry out
   its steps for this ticket id, passing along `--auto-pr` if it was
   given.
4. **Verify.** Read `.claude/commands/pyspec/verify.md` and carry out its
   steps for this ticket id.
5. **Archive.** If verify found nothing pending, read
   `.claude/commands/pyspec/archive.md` and carry out its steps for this
   ticket id. If verify found something pending, say so and leave it in
   `active/` instead — never archive an incomplete ticket just because
   `--skip-permissions` is set.

## Final report

With more than one id, close with a queue summary: one line per ticket
(id, what happened, done or blocked and why), plus every "Cómo probarla"
produced in step 4.
