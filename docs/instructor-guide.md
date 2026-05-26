# Guia para instructor

Esta guia recoge las decisiones operativas recomendadas para impartir el kata sin que la mecanica de GitHub tape el aprendizaje.

## Preparacion del repositorio

1. Crea el repositorio remoto y sube la rama `main` inicial.
1. Activa GitHub Actions.
1. En los ajustes de pull requests, deja `Squash and merge` como metodo preferido de integracion.
1. Si el grupo va justo de tiempo, desactiva temporalmente `Create a merge commit` y `Rebase and merge` para que todos practiquen el mismo flujo.
1. Pide a cada participante que cree su rama principal personal `main-<username>` antes de empezar el ejercicio 1.

## Politica de merge

El flujo preferido para integrar PRs del kata es `Squash and merge`.

- Mantiene `main-<username>` legible: un PR terminado queda representado por un commit claro.
- El PR conserva la historia completa de trabajo: commits intermedios, conversacion, checks y revision.
- No obliga a que cada commit intermedio de cada rama sea perfecto antes de integrarla.
- No destruye la practica interna de cada rama: los ejercicios siguen pudiendo pedir `rebase -i`, `fixup`, merge commits internos, `bisect` o `revert -m`.
- Reduce ruido entre ejercicios: la rama principal personal avanza con unidades de trabajo completas.

Otros metodos:

- `Create a merge commit` conserva todos los commits y anade un merge commit. Sirve para una demo de historia real, pero ensucia rapido `main-<username>`.
- `Rebase and merge` deja una historia lineal con todos los commits de la rama. Es razonable si la rama ya esta muy cuidada, pero exige mas higiene antes de integrar.

Excepciones y matices:

- En los ejercicios 8 y 9, algunas ramas deben contener merge commits internos antes del PR. Eso se valida en la rama del ejercicio; el PR puede integrarse igualmente con `Squash and merge`.
- El backport de `hotfix/backport-factorial-<username>` se abre contra `release/v1-<username>`, no contra `main-<username>`.
- Si quieres que el alumnado inspeccione una historia real con merge commits en la rama principal, habilita `Create a merge commit` solo para una demo controlada.

## Ritmo recomendado

- Ejercicios 1-3: fundamentos colaborativos, ramas, staging, rebase y conflictos.
- Ejercicios 4-6: higiene de historial, recuperacion y review.
- Ejercicio 7: integracion final del flujo de equipo.
- Ejercicios 8-9: modulos avanzados de diagnostico y mantenimiento.

Para una sesion corta, usa el ejercicio 7 como cierre y deja 8-9 como ampliacion.

## Evaluacion

Evalua tres capas:

- Resultado observable: tests, `scripts/validate.py` y archivos esperados.
- Flujo usado: PR contra la rama correcta, rebase donde el ejercicio lo pide, `push --force-with-lease` tras reescritura y `Squash and merge` al integrar.
- Explicacion: el issue final debe mostrar que la persona entiende por que eligio cada comando, no solo que copio una secuencia.

Cuando una validacion falle, pide primero leer el mensaje de error y formular una hipotesis. Esa pequena pausa suele ser donde Git empieza a dejar de parecer magia negra.

## Limpieza posterior

Al terminar:

- Conserva `main-<username>` y los tags de release si vas a revisar entregas.
- Borra ramas de ejercicio ya integradas cuando no hagan falta para correccion.
- Elimina worktrees auxiliares con `git worktree remove`.
- Si se reutiliza el repo para otra cohorte, crea un remoto nuevo o limpia ramas personales y tags de participantes anteriores.
