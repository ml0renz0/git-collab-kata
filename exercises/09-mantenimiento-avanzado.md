# 09 — Mantenimiento avanzado y backports

## Objetivo

Practicar un flujo de mantenimiento realista con `git worktree`, `git cherry-pick -x` y `git revert -m`. El objetivo es mantener una rama de release sin bloquear el trabajo principal, llevar un hotfix concreto mediante backport y deshacer un merge completo sin reescribir historia compartida.

## Demo

- En la presentación crearemos una rama `release/*` desde la rama principal personal.
- Abriremos esa release en otro directorio con `git worktree`.
- Crearemos un fix en la línea principal y lo llevaremos a la release con `git cherry-pick -x`.
- Cerraremos con un merge intencionado y un `git revert -m 1` para deshacer una rama completa.

## Convención de ramas

Como en los ejercicios anteriores, cada participante trabaja contra su rama principal de usuario. En este ejercicio aparecen ramas de mantenimiento y hotfix:

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
RELEASE="release/v1-${USER_ID}"
SOURCE_FIX="hotfix/factorial-type-guard-${USER_ID}"
BACKPORT_FACTORIAL="hotfix/backport-factorial-${USER_ID}"
REVERT_MERGE="chore/revert-merge-demo-${USER_ID}"
TEMP_DISCOUNT="feature/temporary-discount-${USER_ID}"
```

Sustituye `<username>` por tu identificador, por ejemplo `anapascual`.

El validador acepta `hotfix/backport-factorial`, `chore/revert-merge-demo` y ramas con esos mismos nombres base más sufijo, como `hotfix/backport-factorial-anapascual`. No cambies estas ramas a otros nombres.

A partir de aquí se asume que tu rama principal de usuario ya se creó en el ejercicio 1. Antes de empezar, cámbiate a ella y actualízala:

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"

git switch "$MAIN"
git pull --ff-only
```

Si estás haciendo este ejercicio de forma aislada y `$MAIN` todavía no existe, créala primero desde `main` siguiendo la convención del ejercicio 1 o del README.

## Estado inicial esperado

Antes de empezar este ejercicio, tu rama `$MAIN` debe contener el resultado del ejercicio 8: existe `factorial`, `factorial(0)` devuelve `1`, `factorial(5)` devuelve `120` y `factorial(-1)` lanza `ValueError`.

Si estás practicando este ejercicio de forma aislada, prepara primero esos cambios mínimos en `$MAIN` o completa el ejercicio 8 antes de crear la rama de release.

---

## Parte A — Worktree y backport con cherry-pick

### Ramas esperadas

La rama de release se crea desde tu rama principal:

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
RELEASE="release/v1-${USER_ID}"

git switch "$MAIN"
git pull --ff-only
git switch -c "$RELEASE"
git push -u origin "$RELEASE"
git switch "$MAIN"
```

El fix original se preparará después en:

```bash
SOURCE_FIX="hotfix/factorial-type-guard-${USER_ID}"
```

El backport se prepara en:

```bash
BACKPORT_FACTORIAL="hotfix/backport-factorial-${USER_ID}"
```

### Escenario

La release `v1` ya existe y no debe recibir todas las features nuevas de `$MAIN`. Se detecta un bug pequeño en `factorial`: debe rechazar entradas no enteras. El fix se integra primero en `$MAIN` y luego se lleva a `release/v1-<username>` con `cherry-pick`.

### Práctica guiada

Parte 1: abrir la release en otro directorio.

1. Comprueba que el checkout principal no está usando `$RELEASE`:

```bash
git switch "$MAIN"
```

1. Crea un worktree para trabajar con la release sin abandonar tu checkout principal:

```bash
git worktree add "../git-collab-kata-release-${USER_ID}" "$RELEASE"
```

1. Lista los worktrees activos:

```bash
git worktree list
```

1. En el worktree de release, comprueba que estás en `$RELEASE`.

Parte 2: crear el fix original en la línea principal.

1. Vuelve al checkout principal del repositorio y crea la rama del fix desde `$MAIN`:

```bash
git switch "$MAIN"
git pull --ff-only
git switch -c "$SOURCE_FIX"
```

1. En `$SOURCE_FIX`, modifica `factorial` para que `factorial(2.5)` lance `TypeError`.
1. Conserva los comportamientos de `factorial(0)`, `factorial(5)` y `factorial(-1)`.
1. Añade un test para `factorial(2.5)`.
1. Haz un commit claro, por ejemplo `fix: reject non-integer factorial input`.
1. Guarda el hash del commit con `git log --oneline -1`.
1. Sube `$SOURCE_FIX`, abre PR contra `$MAIN` y combínala.
1. Actualiza tu `$MAIN` con `git switch "$MAIN"` y `git pull --ff-only`.

Parte 3: llevar solo ese fix a la release.

1. En el worktree de release, crea la rama de backport desde `$RELEASE`:

```bash
git switch -c "$BACKPORT_FACTORIAL"
```

1. Aplica solo el commit del fix con `cherry-pick -x`:

```bash
git cherry-pick -x <hash-del-fix>
```

1. Crea `docs/worktree-notes.md` con una nota breve que mencione `git worktree add`, `git worktree list`, `git worktree remove` y `git cherry-pick -x`.
1. Haz un commit para la nota, por ejemplo `docs: describe release worktree backport`.
1. Ejecuta `python scripts/validate.py` en la rama `hotfix/backport-factorial-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube `$BACKPORT_FACTORIAL` y abre PR contra `$RELEASE`.
1. Cuando termines de trabajar con el directorio auxiliar, vuelve al checkout principal y elimina el worktree:

```bash
git worktree remove "../git-collab-kata-release-${USER_ID}"
```

### Resultado esperado observable

- `factorial(2.5)` lanza `TypeError`.
- Se conservan los comportamientos de `factorial(0)`, `factorial(5)` y `factorial(-1)`.
- La rama de backport contiene un commit creado con `git cherry-pick -x`.
- Existe `docs/worktree-notes.md`.
- La nota menciona `git worktree add`, `git worktree list`, `git worktree remove` y `git cherry-pick -x`.

---

## Parte B — Revertir un merge commit

### Rama esperada

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
REVERT_MERGE="chore/revert-merge-demo-${USER_ID}"
TEMP_DISCOUNT="feature/temporary-discount-${USER_ID}"

git switch "$MAIN"
git pull --ff-only
git switch -c "$REVERT_MERGE"
```

### Escenario

Una rama completa de prueba se fusionó con merge commit, pero después el equipo decide que no debe entrar. Como ese merge ya está compartido, se deshace con `git revert -m 1`, conservando la historia.

### Preguntas de reflexión

- ¿Qué ventaja tiene `git worktree` frente a hacer `switch` continuamente entre `$MAIN` y `$RELEASE`?
- ¿Por qué `git cherry-pick -x` es útil en un backport?
- ¿Qué riesgo tendría mezclar toda la rama `$MAIN` dentro de una release antigua?
- ¿Qué representa el `-m 1` en `git revert -m 1 <merge-commit>`?
- ¿Por qué revertir un merge commit no es lo mismo que borrar la rama original?

### Práctica individual

Parte 1: crear y fusionar una rama temporal.

1. Desde `$REVERT_MERGE`, crea una rama temporal:

```bash
git switch -c "$TEMP_DISCOUNT"
```

1. Añade una función experimental `experimental_discount(amount, rate)` en `app/calculator.py`.
1. Añade un test mínimo para esa función.
1. Haz un commit claro, por ejemplo `feat: try temporary discount helper`.
1. Vuelve a `$REVERT_MERGE`:

```bash
git switch "$REVERT_MERGE"
```

1. Fusiona la rama temporal creando un merge commit:

```bash
git merge --no-ff "$TEMP_DISCOUNT"
```

1. Localiza el hash del merge commit con `git log --oneline --graph --decorate "$MAIN"..HEAD`.

Parte 2: revertir el merge completo.

1. Revierte el merge conservando como línea principal el primer padre:

```bash
git revert -m 1 <hash-del-merge-commit>
```

1. Comprueba que `experimental_discount` ya no existe.
1. Crea `docs/merge-revert.md` con una nota breve que mencione `git merge --no-ff`, `git revert -m 1` y `primer padre`.
1. Haz un commit para la nota, por ejemplo `docs: explain merge revert`.
1. Ejecuta `python scripts/validate.py` en la rama `chore/revert-merge-demo-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube `$REVERT_MERGE`, abre PR contra `$MAIN` y combínala.

### Resultado esperado observable

- La rama `chore/revert-merge-demo-<username>` contiene al menos un merge commit.
- Algún commit posterior revierte ese merge.
- `experimental_discount` no existe al final.
- Existe `docs/merge-revert.md`.
- La nota menciona `git merge --no-ff`, `git revert -m 1` y `primer padre`.

### Validación local

```bash
python scripts/validate.py             # ejecutar validación local del repositorio
pytest -q                              # ejecutar tests desde el entorno virtual
```

### Validación en GitHub

Abre el PR de backport contra `$RELEASE` y el PR de revert contra `$MAIN`. Los workflows deben pasar sin modificar `main`.

## Entregable

- Completa `hotfix/backport-factorial-<username>` usando un worktree de release y `git cherry-pick -x`.
- Completa `chore/revert-merge-demo-<username>` usando `git merge --no-ff` y `git revert -m 1`.
- Deja `docs/worktree-notes.md` y `docs/merge-revert.md` con las decisiones tomadas.
