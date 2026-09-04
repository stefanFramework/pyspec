---
description: Compara el spec activo contra el diff real antes de dar el ticket por cerrado.
argument-hint: <ticket-id>
---

Vas a verificar el ticket `$ARGUMENTS` antes de archivarlo.

1. Lee `specs/active/sc-$ARGUMENTS.spec` completo, en particular el "Plan"
   y "Archivos a tocar".
2. Revisa el diff real (`git diff` / archivos modificados) en los repos
   tocados (backend: $repo_backend, frontend: $repo_frontend,
   infra: $repo_infra).
3. Compara plan vs diff real y reporta:
   - Que del plan se implemento tal cual.
   - Que quedo a mitad de camino o no se hizo.
   - Que se hizo pero no estaba en el plan original (y si el spec se
     actualizo para reflejarlo).
4. No modifiques codigo en este paso, solo reporta. Si encontras algo
   pendiente, decilo explicitamente antes de sugerir `/pyspec-archive`.
