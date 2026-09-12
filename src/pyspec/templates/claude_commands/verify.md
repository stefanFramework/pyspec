---
description: Compares the active spec against the actual diff before considering the ticket closed, and writes a demo script.
argument-hint: <ticket-id>
---

You're going to verify ticket `$ARGUMENTS` before archiving it.

1. Read `specs/active/sc-$ARGUMENTS.spec` in full, in particular the
   "Plan", "Acceptance criteria", and "Files to touch" sections.
2. Review the actual diff (`git diff` / modified files) in the touched
   repos (backend: $repo_backend, frontend: $repo_frontend,
   infra: $repo_infra).
3. Compare the plan against the actual diff and report:
   - What from the plan was implemented as-is.
   - What was left half-done or not done at all.
   - What was done but wasn't in the original plan (and whether the spec
     was updated to reflect it).
4. Don't modify code in this step, only report. If you find something
   pending, say so explicitly before suggesting `/pyspec:archive`.
5. Close with a **"Cómo probarla"** section, in Spanish, regardless of
   whether the ticket is fully done. Write it as a shooting script for
   someone recording a short screen video: the screens to visit, in
   order, and what should become visible on each one. Leave out anything
   that won't show up on camera:
   - No setup commands (how to run the repos) — say only which branch to
     be on, and which other repo has to be running too if the change
     spans more than one.
   - No test commands — that's what the quality gates already covered.
   - No verification the camera can't see (DB queries, network tab,
     `docker exec`, reading the DOM). If the only proof something worked
     is a database row, say plainly that this part isn't demonstrable
     instead of dressing up a query as a demo step.
   - Name concrete data to reach the state (a record, a role, an id) only
     from data that already exists locally — verify that first.
   If nothing in the ticket has a visible surface yet, say so and explain
   why instead of inventing a recipe that won't work.

Keep the rest of your report high-level and in plain language: what
changed from a user's point of view, not a diff. Skip file names,
function/variable names, and internal data structures unless asked.
