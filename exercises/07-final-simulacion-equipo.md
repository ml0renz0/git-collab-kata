# 07 — Simulación final de equipo

## Objetivo

Simular una semana de trabajo en equipo en 60-90 minutos, usando todo lo practicado: ramas con propósito claro, PRs pequeños, hotfix urgente, rebase de ramas desactualizadas, resolución de conflictos, review, tags de release y recuperación con `revert`.

## Demo

- En la presentación organizaremos cuatro roles sobre una misma rama principal de usuario.
- Crearemos una feature funcional y un hotfix urgente desde la misma base.
- Integraremos primero el hotfix y actualizaremos la feature con rebase.
- Dejaremos un refactor conflictivo y un incidente posterior a release como entregable final.
- Cerraremos conectando el flujo completo con tags de release y `git revert`.

## Convención de ramas

Como en los ejercicios anteriores, cada participante trabaja contra su rama principal de usuario. En este ejercicio es especialmente importante respetar los nombres base de las ramas porque el validador activa comprobaciones distintas para cada rol.

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE_TAX="feature/tax-calculation-${USER_ID}"
REFACTOR_NAMES="refactor/calculator-names-${USER_ID}"
HOTFIX_ZERO="hotfix/division-by-zero-${USER_ID}"
INCIDENT_REVERT="chore/final-incident-${USER_ID}"
```

Sustituye `<username>` por tu identificador, por ejemplo `anapascual`.

El validador acepta `feature/tax-calculation`, `refactor/calculator-names`, `hotfix/division-by-zero`, `chore/final-incident` y ramas con esos mismos nombres base más sufijo, como `feature/tax-calculation-anapascual`. No cambies estas ramas a otros nombres.

Si todavía no existe tu rama principal de usuario, créala desde `main`:

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"

git switch main
git pull --ff-only
git switch -c "$MAIN"
git push -u origin "$MAIN"
```

## Preparación — Roles y ramas desde la misma base

El objetivo es que la feature, el refactor y el hotfix compitan por el mismo módulo. Crea las tres ramas de trabajo desde el mismo `$MAIN` antes de implementar nada.

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE_TAX="feature/tax-calculation-${USER_ID}"
REFACTOR_NAMES="refactor/calculator-names-${USER_ID}"
HOTFIX_ZERO="hotfix/division-by-zero-${USER_ID}"

git switch "$MAIN"
git pull --ff-only
git switch -c "$FEATURE_TAX"
git switch "$MAIN"
git switch -c "$REFACTOR_NAMES"
git switch "$MAIN"
git switch -c "$HOTFIX_ZERO"
```

Roles sugeridos:

- Persona A: feature funcional.
- Persona B: refactor.
- Persona C: hotfix.
- Persona D: reviewer/maintainer.

---

## Ejercicio 7A — Feature, hotfix e integración guiada

### Ramas esperadas

Persona A trabaja en:

```bash
git switch "$FEATURE_TAX"
```

Persona C trabaja en:

```bash
git switch "$HOTFIX_ZERO"
```

Persona D revisa y combina PRs contra:

```bash
git switch "$MAIN"
```

### Escenario

Producto pide calcular impuestos desde la calculadora, pero durante la semana aparece una incidencia urgente: la división por cero debe estar cubierta explícitamente. La feature ya está abierta, el hotfix debe entrar primero y después la feature tendrá que actualizarse antes de combinarse.

### Preguntas

- ¿Por qué el hotfix entra antes que una feature ya abierta?
- ¿Qué hace que la feature de impuestos sea pequeña y revisable?
- ¿Qué comportamiento mínimo debería cubrir `test_calculate_tax`?
- ¿Qué conserva un rebase bien resuelto después de integrar el hotfix?
- ¿Contra qué rama deben abrirse los PRs en esta simulación?

### Tarea de demo

Parte 1: Persona A prepara la feature funcional.

1. En `$FEATURE_TAX`, añade `calculate_tax(amount, rate)` en `app/calculator.py`.
1. Haz que `calculate_tax(100, 0.21)` devuelva `21.0`.
1. Añade un test `test_calculate_tax` en `tests/test_calculator.py`.
1. Haz un commit claro, por ejemplo `feat: add tax calculation`.
1. Sube la rama configurando upstream con `git push -u origin "$FEATURE_TAX"`.
1. Abre PR desde `$FEATURE_TAX` contra `$MAIN`, pero no lo combines todavía.
1. Ejecuta `python scripts/validate.py` en la rama `feature/tax-calculation-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.

Parte 2: Persona C prepara el hotfix urgente.

1. En `$HOTFIX_ZERO`, asegúrate de que existe `divide` en `app/calculator.py`.
1. Haz que `divide(10, 0)` lance `ZeroDivisionError` de forma explícita.
1. Añade o conserva un test cuyo nombre o contenido incluya `zero`.
1. Haz un commit claro, por ejemplo `fix: handle division by zero`.
1. Ejecuta `python scripts/validate.py` en la rama `hotfix/division-by-zero-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube la rama configurando upstream con `git push -u origin "$HOTFIX_ZERO"`.
1. Abre PR desde `$HOTFIX_ZERO` contra `$MAIN`.
1. Persona D revisa que el PR sea pequeño y lo combina primero.
1. Actualiza la rama local `$MAIN` con `git switch "$MAIN"` y `git pull --ff-only`.

Parte 3: Persona A actualiza la feature y Persona D la integra.

1. Vuelve a `$FEATURE_TAX`.
1. Trae cambios remotos con `git fetch origin`.
1. Actualiza la rama con:

```bash
git rebase "origin/$MAIN"
```

1. Si aparecen conflictos, resuélvelos conservando el hotfix y `calculate_tax`.
1. Ejecuta `python scripts/validate.py`.
1. Ejecuta `pytest -q`.
1. Actualiza el remoto con `git push --force-with-lease`.
1. Persona D revisa el PR y lo combina contra `$MAIN`.
1. Actualiza `$MAIN` con `git switch "$MAIN"` y `git pull --ff-only`.

### Resultado esperado observable

- Existe `calculate_tax` en `app/calculator.py`.
- Existe `test_calculate_tax`.
- `calculate_tax(100, 0.21)` devuelve `21.0`.
- `divide(10, 0)` lanza `ZeroDivisionError`.
- Hay un test de regresión que incluye `zero`.
- El hotfix entra antes que la feature.

---

## Ejercicio 7B — Refactor, release e incidente

### Ramas esperadas

Persona B trabaja en:

```bash
git switch "$REFACTOR_NAMES"
```

El incidente posterior a release se trabaja en:

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
INCIDENT_REVERT="chore/final-incident-${USER_ID}"
```

### Escenario

Con el hotfix y la feature ya integrados, queda un refactor que se creó desde la base antigua y tocará el mismo módulo. Después de resolverlo y publicar una release, el equipo simula un incidente posterior y lo deshace con `git revert`, sin reescribir la historia compartida.

### Preguntas

- ¿Cómo demuestras que un refactor no cambió comportamiento?
- ¿Por qué conviene que el refactor entre después del hotfix y de la feature?
- Al resolver conflictos, ¿qué cambios deben conservarse?
- ¿Para qué sirve un tag anotado de release?
- ¿Por qué `revert` es más seguro que `reset --hard` en una rama compartida?
- ¿Qué debe mostrar el historial después de revertir?

### Tarea entregable

Parte 1: Persona B prepara el refactor.

1. En `$REFACTOR_NAMES`, renombra los parámetros de `add` y `subtract` a `left` y `right`.
1. Conserva el comportamiento existente de `add` y `subtract`.
1. Si tu `$MAIN` ya incluye comportamientos extra en `add`, como casteo a `int` o validación de `None`, consérvalos.
1. Revisa el diff para confirmar que no has mezclado cambios funcionales.
1. Haz un commit claro, por ejemplo `refactor: rename calculator operands`.
1. Sube la rama configurando upstream con `git push -u origin "$REFACTOR_NAMES"`.
1. Abre PR desde `$REFACTOR_NAMES` contra `$MAIN`, pero no lo combines todavía.
1. Ejecuta `python scripts/validate.py` en la rama `refactor/calculator-names-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.

Parte 2: Persona B actualiza el refactor y Persona D lo integra.

1. Vuelve a `$REFACTOR_NAMES`.
1. Trae cambios remotos con `git fetch origin`.
1. Actualiza la rama con:

```bash
git rebase "origin/$MAIN"
```

1. Si aparecen conflictos, resuélvelos conservando:
   - `calculate_tax`;
   - el hotfix de división por cero;
   - los nombres `left` y `right` en `add` y `subtract`;
   - los tests de todas las ramas.
1. Ejecuta `python scripts/validate.py`.
1. Ejecuta `pytest -q`.
1. Actualiza el remoto con `git push --force-with-lease`.
1. Persona D revisa el PR y lo combina contra `$MAIN`.
1. Actualiza `$MAIN` con `git switch "$MAIN"` y `git pull --ff-only`.

Parte 3: crear release.

1. Comprueba que estás en `$MAIN`.
1. Ejecuta los checks finales:

```bash
python scripts/validate.py
pytest -q
```

1. Crea una etiqueta anotada:

```bash
git tag -a "v1.0.0-${USER_ID}" -m "Release v1.0.0 ${USER_ID}"
```

1. Sube la etiqueta:

```bash
git push origin "v1.0.0-${USER_ID}"
```

Parte 4: resolver incidente posterior a release.

1. Desde `$MAIN`, crea la rama del incidente:

```bash
git switch "$MAIN"
git pull --ff-only
git switch -c "$INCIDENT_REVERT"
```

1. Crea `release-blocker.txt` con contenido que incluya la palabra `broken`.
1. Haz un commit con mensaje claro, por ejemplo `chore: add broken release marker`.
1. Ejecuta:

```bash
git revert HEAD
```

1. Comprueba que `release-blocker.txt` ya no existe.
1. Comprueba con `git log --oneline "$MAIN"..HEAD` que hay un commit original y un commit de revert.
1. Ejecuta `python scripts/validate.py` en la rama `chore/final-incident-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube la rama configurando upstream con `git push -u origin "$INCIDENT_REVERT"`.
1. Abre PR desde `$INCIDENT_REVERT` contra `$MAIN` y combínala.
1. Actualiza `$MAIN` con `git switch "$MAIN"` y `git pull --ff-only`.
1. Crea y sube el tag de hotfix:

```bash
git tag -a "v1.0.1-${USER_ID}" -m "Release hotfix v1.0.1 ${USER_ID}"
git push origin "v1.0.1-${USER_ID}"
```

### Resultado esperado observable

- `add` y `subtract` siguen existiendo.
- Sus dos primeros parámetros se llaman `left` y `right`.
- `add(2, 3)` devuelve `5`.
- `subtract(5, 3)` devuelve `2`.
- `$MAIN` contiene el hotfix, la feature y el refactor.
- La release queda marcada con un tag anotado `v1.0.0-<username>`.
- `release-blocker.txt` no existe al final.
- La rama `chore/final-incident-<username>` tiene al menos dos commits sobre `$MAIN`: el commit roto y el revert.
- Algún mensaje de commit contiene `Revert`.
- La release corregida queda marcada con `v1.0.1-<username>`.

### Validación local

```bash
python scripts/validate.py             # ejecutar validación local del repositorio
pytest -q                              # ejecutar tests desde el entorno virtual
```

### Validación en GitHub

Abre PR desde cada rama contra tu rama `$MAIN`. El workflow debe pasar sin modificar `main`.

## Entregable

- Completa el ejercicio 7A como demo con `feature/tax-calculation-<username>`, `hotfix/division-by-zero-<username>` y la feature actualizada con rebase tras integrar el hotfix.
- Completa el ejercicio 7B con `refactor/calculator-names-<username>` renombrando parámetros a `left` y `right` sin cambiar comportamiento.
- Integra primero el hotfix, después la feature actualizada con rebase y finalmente el refactor actualizado con rebase.
- Crea el tag anotado `v1.0.0-<username>` desde `$MAIN`.
- Completa el incidente en `chore/final-incident-<username>` con `git revert`, sin `release-blocker.txt` al final, y crea el tag anotado `v1.0.1-<username>`.
- Abre todos los PR contra tu rama `$MAIN`, no contra `main`.
