---
description: Genera el spec de un ticket (contexto + plan) y frena para pedir aprobacion antes de tocar codigo.
argument-hint: <ticket-id>
---

Estas armando el spec del ticket `$ARGUMENTS` para el framework pyspec.

1. Corre `pyspec fetch $ARGUMENTS` para traer el ticket (titulo, descripcion, url).
2. Identifica el/los modulo(s) del sistema que toca este ticket.
3. Lee `specs/current/<modulo>.md` para cada modulo relevante. Si no existe
   todavia, generalo primero leyendo el codigo actual (no inventes nada que
   no este en el codigo). Los repos configurados son:
   - backend: $repo_backend
   - frontend: $repo_frontend
   - infra: $repo_infra
4. Lee el codigo de backend/frontend/infra relevante al pedido del ticket.
5. Corre `pyspec new $ARGUMENTS --title "<titulo del ticket>"` para crear
   `specs/active/sc-$ARGUMENTS.spec` desde la plantilla.
6. Completa el spec con:
   - Contexto actual (resumen de lo que dice `current/`)
   - Plan de implementacion paso a paso
   - Archivos a tocar (backend, frontend, infra segun aplique)
   - Justificacion de decisiones tecnicas especificas del ticket

IMPORTANTE: no empieces a implementar. Cuando termines el spec, mostraselo
al usuario y pregunta explicitamente si esta aprobado antes de tocar codigo.
