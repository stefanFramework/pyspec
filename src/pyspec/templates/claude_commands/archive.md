---
description: Updates current/ with what was actually implemented and moves the spec to archive/.
argument-hint: <ticket-id>
---

You're going to close ticket `$ARGUMENTS`.

1. Read `specs/active/sc-$ARGUMENTS.spec` and the final implemented code
   (not what was planned, what actually ended up there).
2. Update `specs/current/<module>.md` for each touched module to reflect
   the real changes, adding the `[sc-$ARGUMENTS]` reference to every new
   or modified line.
3. Run `pyspec archive $ARGUMENTS` to move
   `specs/active/sc-$ARGUMENTS.spec` to `specs/archive/sc-$ARGUMENTS.spec`.
4. Confirm to the user which module(s) were updated and that the spec was
   successfully archived.
