---
description: Implements a ticket following the already-approved spec in specs/active/.
argument-hint: <ticket-id>
---

You're going to implement ticket `$ARGUMENTS` following its spec.

1. Read `specs/active/sc-$ARGUMENTS.spec` in full. If it doesn't exist,
   say so and suggest running `/pyspec:explore $ARGUMENTS` first.
2. Implement the plan step by step, touching the files listed under
   "Files to touch" (backend: $repo_backend, frontend: $repo_frontend,
   infra: $repo_infra).
3. If the scope changes from the original plan during implementation,
   update the spec (`specs/active/sc-$ARGUMENTS.spec`) so it stays the
   source of truth for what was done and why.
4. Don't archive the ticket yourself: that's done by `/pyspec:verify` and
   `/pyspec:archive` once the implementation is confirmed.
