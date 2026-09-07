---
description: Generates a ticket's spec (context + plan) and stops to ask for approval before touching code.
argument-hint: <ticket-id> (optional if the data source is manual)
---

You're writing a spec for the pyspec framework. The argument passed to
this command, if any, is the ticket id: `$ARGUMENTS`.

Configured ticket data source: `$data_source`.

1. Determine the ticket id, title, and description:
   - If `$ARGUMENTS` is not empty, that's the ticket id.
     - If the data source is `trello` or `shortcut`: run `pyspec fetch $ARGUMENTS`
       to fetch the title/description/url automatically.
     - If the data source is `manual`: don't run `pyspec fetch` — it expects an
       interactive terminal (it prompts for title/description line by line) and
       will hang when run from here. Instead, ask the user directly in this
       conversation for the ticket's title and description.
   - If `$ARGUMENTS` is empty (only makes sense with a `manual` data source):
     ask the user directly in this conversation for the ticket's title and
     description, then generate the ticket id yourself as a 2-3 word
     kebab-case slug summarizing the task (e.g. `metcon-diff-change`). Use
     that slug as the ticket id for every step below.
2. Identify the module(s) of the system this ticket touches.
3. Read `specs/current/<module>.md` for each relevant module. If it doesn't
   exist yet, generate it first by reading the current code (don't invent
   anything that isn't in the code). The configured repos are:
   - backend: $repo_backend
   - frontend: $repo_frontend
   - infra: $repo_infra
4. Read the backend/frontend/infra code relevant to the ticket's request.
5. Run `pyspec new <ticket-id> --title "<ticket title>"` (using the ticket
   id from step 1) to create `specs/active/sc-<ticket-id>.spec` from the
   template.
6. Fill in the spec with:
   - Current context (summary of what `current/` says)
   - Step-by-step implementation plan
   - Files to touch (backend, frontend, infra as applicable)
   - Justification for ticket-specific technical decisions

IMPORTANT: do not start implementing. Once the spec is done, show it to
the user and explicitly ask whether it's approved before touching code.
If you generated the ticket id yourself in step 1, make sure to clearly
state it, since the user will need it for `/pyspec:execute`,
`/pyspec:verify`, and `/pyspec:archive` on this same ticket.
