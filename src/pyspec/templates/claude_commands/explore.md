---
description: Generates a ticket's spec (context + plan) and stops to ask for approval before touching code.
argument-hint: <ticket-id>
---

You're writing the spec for ticket `$ARGUMENTS` for the pyspec framework.

Configured ticket data source: `$data_source`.

1. Get the ticket's title and description. `$ARGUMENTS` here is just the
   ticket id (it's reused as-is in `specs/active/sc-$ARGUMENTS.spec` later).
   - If the data source is `manual`: don't run `pyspec fetch` — it expects an
     interactive terminal (it prompts for title/description line by line) and
     will hang when run from here. Instead, ask the user directly in this
     conversation for the ticket's title and description before continuing.
   - If the data source is `trello` or `shortcut`: run `pyspec fetch $ARGUMENTS`
     to fetch the ticket (title, description, url) automatically.
2. Identify the module(s) of the system this ticket touches.
3. Read `specs/current/<module>.md` for each relevant module. If it doesn't
   exist yet, generate it first by reading the current code (don't invent
   anything that isn't in the code). The configured repos are:
   - backend: $repo_backend
   - frontend: $repo_frontend
   - infra: $repo_infra
4. Read the backend/frontend/infra code relevant to the ticket's request.
5. Run `pyspec new $ARGUMENTS --title "<ticket title>"` to create
   `specs/active/sc-$ARGUMENTS.spec` from the template.
6. Fill in the spec with:
   - Current context (summary of what `current/` says)
   - Step-by-step implementation plan
   - Files to touch (backend, frontend, infra as applicable)
   - Justification for ticket-specific technical decisions

IMPORTANT: do not start implementing. Once the spec is done, show it to
the user and explicitly ask whether it's approved before touching code.
