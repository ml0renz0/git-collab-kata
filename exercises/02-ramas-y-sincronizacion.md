# 02 — Ramas y sincronización

## Objetivo

Practicar creación de ramas, configuración de upstream, `fetch`, `pull --ff-only` y actualización de una rama de feature desactualizada resolviendo conflictos.

## Demo

- En la presentación veremos cómo una rama local queda conectada a una rama remota con `git push -u`.
- Compararemos `git pull --ff-only` con un `pull` que crea merge commits.
- Simularemos dos ramas creadas desde la misma base: una se integra primero y la otra queda desactualizada.
- Resolveremos conflictos en `app/calculator.py` y `tests/test_calculator.py` conservando los cambios de ambas ramas.

## Convención de ramas

Como no se trabaja con forks, cada participante usa una rama principal propia y ramas de feature con sufijo de usuario:

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE_DIVIDE="feature/divide-operation-${USER_ID}"
FEATURE_MODULUS="feature/modulus-operation-${USER_ID}"
```

Sustituye `<username>` por tu identificador, por ejemplo `anapascual`.

Si todavía no existe tu rama principal de usuario, créala desde `main`:

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"

git switch main
git pull --ff-only
git switch -c "$MAIN"
git push -u origin "$MAIN"
```

## Preparación — Dos ramas desde la misma base

Antes de implementar nada, crea las dos ramas desde el mismo punto de partida. Esto hará que la rama de `modulus` quede desactualizada cuando integres `divide`.

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE_DIVIDE="feature/divide-operation-${USER_ID}"
FEATURE_MODULUS="feature/modulus-operation-${USER_ID}"

git switch "$MAIN"
git pull --ff-only
git switch -c "$FEATURE_DIVIDE"
git switch "$MAIN"
git switch -c "$FEATURE_MODULUS"
```

---

## Ejercicio 2A — Feature branch con upstream

### Rama esperada

```bash
git switch "$FEATURE_DIVIDE"
```

### Escenario

Quieres añadir una nueva operación `divide` en una rama aislada y dejarla preparada para abrir PR contra tu rama `$MAIN`.

### Tarea de demo

1. Añade una función `divide` en `app/calculator.py`.
1. Añade un test `test_divide` en `tests/test_calculator.py`.
1. Haz un commit pequeño con la función y el test.
1. Sube la rama configurando upstream con `git push -u origin "$FEATURE_DIVIDE"`.
1. Comprueba la relación entre rama local y rama remota con `git branch -vv`.
1. Ejecuta `python scripts/validate.py` en la rama `feature/divide-operation-<username>`.
1. Abre PR desde `$FEATURE_DIVIDE` contra `$MAIN` y combínala.
1. Actualiza tu rama local `$MAIN` con `git switch "$MAIN"` y `git pull --ff-only`.

---

## Ejercicio 2B — Rama desactualizada con conflicto

### Rama esperada

```bash
git switch "$FEATURE_MODULUS"
```

### Escenario

La rama `$FEATURE_MODULUS` se creó antes de integrar `divide`, así que no contiene los cambios de 2A. Ahora vas a añadir otra operación en los mismos ficheros para forzar un conflicto al actualizar la rama.

### Tarea entregable

1. Añade una función `modulus` en `app/calculator.py` que devuelva el resto de la división entera con `%`.
1. Añade un test `test_modulus` en `tests/test_calculator.py`.
1. Haz un commit pequeño con la función y el test.
1. Sube la rama configurando upstream con un único comando.
1. Trae los cambios remotos.
1. Actualiza tu rama con $MAIN.
1. Resuelve los conflictos en `app/calculator.py` y `tests/test_calculator.py`, conservando `divide`, `modulus`, `test_divide` y `test_modulus`.
1. Añade los ficheros `app/calculator.py` y `tests/test_calculator.py` al stage y continúa.
1. Ejecuta `python scripts/validate.py` en la rama `feature/modulus-operation-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube la rama actualizada.
1. Abre PR desde `$FEATURE_MODULUS` contra `$MAIN` y combínala.

### Validación local

```bash
python scripts/validate.py             # ejecutar validación local del repositorio
pytest -q                              # ejecutar tests desde el entorno virtual
```

### Validación en GitHub

Abre PR desde cada feature contra tu rama `$MAIN`. El workflow debe pasar sin modificar `main`.

## Entregable

- Completa el ejercicio 2A con `divide`, `test_divide` y upstream configurado para `feature/divide-operation-<username>`.
- Completa el ejercicio 2B con `modulus`, `test_modulus` y upstream configurado para `feature/modulus-operation-<username>`.
- Resuelve el conflicto de 2B conservando los cambios de ambas ramas.
- Abre los PR contra tu rama `$MAIN`, no contra `main`.
