---
description: Compares the active spec against the actual diff before considering the ticket closed.
argument-hint: <ticket-id>
---

You're going to verify ticket `$ARGUMENTS` before archiving it.

1. Read `specs/active/sc-$ARGUMENTS.spec` in full, in particular the
   "Plan" and "Files to touch" sections.
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
