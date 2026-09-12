---
description: Implements a ticket following the already-approved spec in specs/active/. Optionally opens a PR with --auto-pr.
argument-hint: <ticket-id> [--auto-pr]
---

You're going to implement a ticket following its spec. Arguments: `$ARGUMENTS`.

Parse `$ARGUMENTS`: `--auto-pr` is a flag and can appear anywhere; every
other token is the ticket id.

1. Read `specs/active/sc-<ticket-id>.spec` in full. If it doesn't exist,
   say so and suggest running `/pyspec:explore <ticket-id>` first.
2. Implement the plan **test-first**, one test at a time, following the
   "Tests to write" section of the spec: write the test, watch it fail
   for the right reason, write the minimum code to make it pass,
   refactor with tests green, repeat. Only for the tests actually listed
   in the spec — don't invent more as you go. If you find you genuinely
   need one the spec didn't anticipate, add it to the spec first so the
   spec stays the source of truth for what was done and why.
3. Touch the files listed under "Files to touch" (backend: $repo_backend,
   frontend: $repo_frontend, infra: $repo_infra). If the scope changes
   from the original plan during implementation, update the spec to
   reflect what actually happened.
4. Run each touched repo's configured quality gates before considering
   the ticket done:
   - backend — test: `$repo_backend_test`, lint: `$repo_backend_lint`
   - frontend — test: `$repo_frontend_test`, lint: `$repo_frontend_lint`
   - infra — test: `$repo_infra_test`, lint: `$repo_infra_lint`
   Skip a gate that isn't configured for that repo. If a gate fails for a
   reason outside this ticket's scope (pre-existing breakage), say so
   explicitly instead of silently working around it.
5. Don't archive the ticket yourself: that's done by `/pyspec:verify` and
   `/pyspec:archive` once the implementation is confirmed.

## `--auto-pr`

If `--auto-pr` was passed and every gate in step 4 is green: for each
touched repo, create a branch off its configured base branch
($repo_backend_base_branch / $repo_frontend_base_branch /
$repo_infra_base_branch — ask the user if a touched repo has none
configured), commit, push the ticket branch, and open a PR. Follow that
repo's own commit/PR conventions (read its `CLAUDE.md` if it has one) for
title, body, and attribution — pyspec doesn't impose a house style here.
Never push directly to a base branch.

Without `--auto-pr`, don't touch git beyond what's needed to run the
tests — no branch, no commit, no push.

## Reporting

Keep your report high-level and in plain language: what changed from a
user's point of view, what decisions you made that they should know
about, and whether the gates passed. Skip file names, function/variable
names, and internal data structures unless asked.
