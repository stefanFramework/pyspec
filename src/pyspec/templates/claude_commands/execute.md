---
description: Implementa un ticket siguiendo el spec ya aprobado en specs/active/.
argument-hint: <ticket-id>
---

Vas a implementar el ticket `$ARGUMENTS` siguiendo su spec.

1. Lee `specs/active/sc-$ARGUMENTS.spec` completo. Si no existe, avisa y
   sugiere correr `/pyspec-explore $ARGUMENTS` primero.
2. Implementa el plan paso a paso, tocando los archivos listados en
   "Archivos a tocar" (backend: $repo_backend, frontend: $repo_frontend,
   infra: $repo_infra).
3. Si durante la implementacion el alcance cambia respecto del plan
   original, actualiza el spec (`specs/active/sc-$ARGUMENTS.spec`) para que
   siga siendo la fuente de verdad de lo que se hizo y por que.
4. No archives el ticket vos mismo: eso lo hace `/pyspec-verify` y
   `/pyspec-archive` una vez confirmada la implementacion.
