# Ticket $ticket_id: $title

## Source
$url

## Current context (from current/$modulo.md)
<summary of how the part of the system this ticket touches works today>

## Plan
1. ...

## Acceptance criteria
<what "done" means, observable from outside>

## Tests to write (specification)
<tests that must exist and fail first, one per real behavior/business-logic
branch. Only tests that add value: no asserting a field merely exists on a
model, no pure type/constant checks, no asserting static copy that doesn't
depend on any branch, no near-duplicates of an existing test.>

## Files to touch
- backend/...
- frontend/...
- infra/... (if applicable)

## Technical decisions and justification
<why this approach was chosen, alternatives discarded if any>
