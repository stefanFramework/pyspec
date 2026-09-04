---
description: Actualiza current/ con lo que efectivamente se implemento y mueve el spec a archive/.
argument-hint: <ticket-id>
---

Vas a cerrar el ticket `$ARGUMENTS`.

1. Lee `specs/active/sc-$ARGUMENTS.spec` y el codigo final implementado
   (no lo planeado, lo que efectivamente quedo).
2. Actualiza `specs/current/<modulo>.md` de cada modulo tocado reflejando
   los cambios reales, agregando la referencia `[sc-$ARGUMENTS]` a cada
   linea nueva o modificada.
3. Corre `pyspec archive $ARGUMENTS` para mover
   `specs/active/sc-$ARGUMENTS.spec` a `specs/archive/sc-$ARGUMENTS.spec`.
4. Confirma al usuario que modulo(s) quedaron actualizados y que el spec
   se archivo correctamente.
