# 06 — Pull Requests y review

## Objetivo

Practicar PRs pequeños, descripciones revisables, feedback cruzado, commits incrementales durante la review, comparación de ramas reescritas con `git range-diff` y limpieza final del historial antes del merge.

## Demo

- En la presentación prepararemos un PR pequeño con una descripción clara y verificable.
- Revisaremos cómo separar lo que cambia, por qué cambia, cómo se ha probado y qué riesgos quedan.
- Simularemos comentarios de review: un cambio funcional, un cambio de naming y una pregunta de diseño.
- Veremos cómo responder con commits incrementales mientras dura la review.
- Cerraremos limpiando la rama con `rebase -i` y usando `git range-diff` antes del `push --force-with-lease`.

## Convención de ramas

Como en los ejercicios anteriores, cada participante trabaja contra su rama principal de usuario. En este ejercicio las ramas deben mantener estos nombres base, porque cada una activa una validación distinta.

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE_PR="feature/pr-template-${USER_ID}"
FEATURE_REVIEW="feature/review-cleanup-${USER_ID}"
```

Sustituye `<username>` por tu identificador, por ejemplo `anapascual`.

El validador acepta `feature/pr-template`, `feature/review-cleanup` y ramas con esos mismos nombres base más sufijo, como `feature/review-cleanup-anapascual`. No cambies estas ramas a otros nombres.

Si todavía no existe tu rama principal de usuario, créala desde `main`:

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"

git switch main
git pull --ff-only
git switch -c "$MAIN"
git push -u origin "$MAIN"
```

---

## Parte A — PR pequeño con descripción revisable

### Rama esperada

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE_PR="feature/pr-template-${USER_ID}"

git switch "$MAIN"        # cambiar a tu rama principal
git pull --ff-only        # actualizar tu rama principal con fast-forward
git switch -c "$FEATURE_PR"  # crear y cambiar a la rama del PR pequeño
```

### Escenario

El equipo quiere que todos los PRs tengan una descripción mínima común. Vas a preparar un cambio de documentación pequeño que sirva como referencia para futuras reviews.

### Preguntas de reflexión

- ¿Qué hace que un PR sea pequeño y revisable?
- ¿Qué información necesita una persona reviewer para entender el cambio sin reconstruirlo desde los commits?
- ¿Por qué conviene incluir cómo se ha probado aunque el cambio sea solo de documentación?
- ¿Contra qué rama debe abrirse el PR en este kata?

### Práctica guiada

1. Crea `docs/pr-template.md`.
1. Añade estos apartados, con una nota breve debajo de cada uno:

```markdown
## Qué cambia

## Por qué

## Cómo se ha probado

## Riesgos
```

1. Revisa que el PR cambia como máximo 3 archivos con `git diff --name-only "$MAIN"..HEAD`.
1. Haz un commit claro, por ejemplo `docs: add pr template guide`.
1. Ejecuta `python scripts/validate.py` en la rama `feature/pr-template-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube la rama configurando upstream con `git push -u origin "$FEATURE_PR"`.
1. Abre PR desde `$FEATURE_PR` contra `$MAIN`, no contra `main`.
1. Usa en la descripción del PR los mismos cuatro apartados de `docs/pr-template.md`.
1. Pide review y combina el PR cuando el workflow esté en verde.
1. Actualiza tu rama local `$MAIN` con `git switch "$MAIN"` y `git pull --ff-only`.

### Resultado esperado observable

- Existe `docs/pr-template.md`.
- El archivo contiene los apartados `Qué cambia`, `Por qué`, `Cómo se ha probado` y `Riesgos`.
- La rama tiene un solo commit sobre `$MAIN`.
- El PR cambia como máximo 3 archivos.

---

## Parte B — Review cruzada y limpieza antes del merge

### Rama esperada

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE_REVIEW="feature/review-cleanup-${USER_ID}"

git switch "$MAIN"            # cambiar a tu rama principal
git pull --ff-only            # actualizar tu rama principal con fast-forward
git switch -c "$FEATURE_REVIEW"  # crear y cambiar a la rama de review
```

### Escenario

Vas a abrir un PR de documentación para explicar cómo quiere trabajar el equipo durante una review. Otra persona revisará el PR y pedirá tres cosas: un cambio funcional, un cambio de naming y una pregunta de diseño.

Durante la review se aceptan commits incrementales. Antes de mergear, limpiarás el historial para que la rama final cuente una sola intención.

Simula la review tú mismo: abre el PR, anota los tres comentarios como checklist en la descripción o en comentarios del PR, y respóndelos como si vinieran de otra persona.

### Preguntas de reflexión

- ¿Qué diferencia hay entre un comentario bloqueante y una pregunta de diseño?
- ¿Por qué es útil responder una pregunta de diseño en la conversación del PR aunque también cambies el código o la documentación?
- ¿Qué ventaja tiene hacer commits incrementales durante la review?
- ¿Por qué conviene limpiar commits como `Address review comments` antes del merge?
- ¿Qué te permite comprobar `git range-diff` antes de sobrescribir una rama remota con historial reescrito?
- ¿Por qué `git push --force-with-lease` es más seguro que `git push -f` después de reescribir la rama?

### Práctica individual

Parte 1: abrir el PR y recibir feedback.

1. Crea `docs/review-workflow.md` con una primera versión breve.
1. Incluye un apartado temporal llamado `## Notes`.
1. Haz un commit claro, por ejemplo `docs: draft review workflow`.
1. Sube la rama configurando upstream con `git push -u origin "$FEATURE_REVIEW"`.
1. Abre PR desde `$FEATURE_REVIEW` contra `$MAIN`.
1. Deja tres comentarios de review simulando al reviewer. Escríbelos tú mismo como checklist de review en el PR:
   - un cambio funcional: añadir que antes de pedir merge se ejecutan `pytest -q` y `python scripts/validate.py`;
   - un cambio de naming: renombrar `## Notes` a `## Criterios de review`;
   - una pregunta de diseño: decidir qué comentarios deben bloquear el merge.

Parte 2: responder a la review con commits incrementales.

1. Responde la pregunta de diseño en la conversación del PR.
1. Actualiza `docs/review-workflow.md` para incluir el cambio funcional.
1. Renombra el apartado `## Notes` a `## Criterios de review`.
1. Añade una sección breve `## Respuesta de diseño` que explique qué comentarios bloquean el merge y cuáles solo piden aclaración.
1. Añade una nota breve indicando que, tras reescribir la rama, se revisa el cambio con `git range-diff` antes de empujar.
1. Haz un commit incremental, por ejemplo `Address review comments`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Revisa el diff del PR y confirma que los comentarios de review quedan atendidos.

Parte 3: limpiar antes del merge.

1. Trae los cambios remotos con `git fetch origin`.
1. Revisa el historial del PR:

```bash
git log --oneline "origin/$MAIN"..HEAD
```

1. Limpia la rama con rebase interactivo:

```bash
git rebase -i "origin/$MAIN"
```

1. Combina el commit `Address review comments` con el commit original usando `fixup` o `squash`.
1. Deja un solo commit final con un mensaje claro, por ejemplo `docs: document review workflow`.
1. Comprueba que el historial ya no contiene `Address review comments`.
1. Compara la versión publicada de la rama con la versión reescrita:

```bash
git range-diff "origin/$MAIN" "origin/$FEATURE_REVIEW" HEAD
```

1. Comprueba que `range-diff` muestra la misma intención final aunque los commits se hayan combinado.
1. Ejecuta de nuevo `python scripts/validate.py`.
1. Ejecuta de nuevo `pytest -q`.
1. Actualiza el remoto con `git push --force-with-lease`.
1. Pide aprobación final y combina el PR.

### Resultado esperado observable

- Existe `docs/review-workflow.md`.
- El archivo menciona el cambio funcional, el cambio de naming y la pregunta de diseño.
- El archivo menciona `pytest -q` y `python scripts/validate.py`.
- El archivo menciona `git range-diff`.
- El apartado `## Notes` ya no existe.
- La rama tiene un solo commit sobre `$MAIN`.
- El historial final no contiene un commit `Address review comments`.
- El PR cambia como máximo 3 archivos.

### Validación local

```bash
python scripts/validate.py             # ejecutar validación local del repositorio
pytest -q                              # ejecutar tests desde el entorno virtual
```

### Validación en GitHub

Abre PR desde cada feature contra tu rama `$MAIN`. El workflow debe pasar sin modificar `main`.

## Entregable

- Completa la parte A como práctica guiada con `docs/pr-template.md`, los cuatro apartados de descripción y un solo commit sobre `$MAIN`.
- Completa la parte B con `docs/review-workflow.md`, respondiendo a feedback funcional, naming y diseño.
- Limpia `feature/review-cleanup-<username>` para que quede un solo commit final, sin `Address review comments`, y revisado con `git range-diff` antes del `push --force-with-lease`.
- Mantén los PRs pequeños: como máximo 3 archivos modificados por rama.
- Abre los PR contra tu rama `$MAIN`, no contra `main`.
