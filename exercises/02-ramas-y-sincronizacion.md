# 02 — Ramas y sincronización

## Objetivo

Practicar creación de ramas, configuración de upstream, `fetch`, `pull --ff-only` y actualización de una rama de feature desactualizada resolviendo conflictos.

## Demo

- En la presentación veremos cómo una rama local queda conectada a una rama remota con `git push -u`.
- Compararemos `git pull --ff-only` con un `pull` que crea merge commits.
- Simularemos dos ramas creadas desde la misma base: una se integra primero y la otra queda desactualizada.
- Resolveremos conflictos en `app/calculator.py` y `tests/test_calculator.py` conservando los cambios de ambas ramas. Para que el conflicto sea reproducible, las dos ramas modificarán la misma zona del módulo y la misma línea de import de tests.

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

## Parte A — Feature branch con upstream

### Rama esperada

```bash
git switch "$FEATURE_DIVIDE"
```

### Escenario

Quieres añadir una nueva operación `divide` en una rama aislada y dejarla preparada para abrir PR contra tu rama `$MAIN`.

### Preguntas de reflexión

- ¿Qué aporta una rama de feature frente a trabajar directamente sobre la rama principal?
- ¿Qué significa que una rama local tenga upstream configurado?
- ¿Por qué conviene abrir el PR contra la rama base correcta?
- ¿Qué información te da `git branch -vv` durante el trabajo colaborativo?

### Práctica guiada

1. Añade una función `divide` en `app/calculator.py` justo después de `subtract`.
1. En `tests/test_calculator.py`, modifica la línea de import para importar también `divide`.
1. Añade un test `test_divide` justo después de `test_subtract`.
1. Haz un commit pequeño con la función y el test.
1. Sube la rama configurando upstream con `git push -u origin "$FEATURE_DIVIDE"`.
1. Comprueba la relación entre rama local y rama remota con `git branch -vv`.
1. Ejecuta `python scripts/validate.py` en la rama `feature/divide-operation-<username>`.
1. Abre PR desde `$FEATURE_DIVIDE` contra `$MAIN` y combínala.
1. Actualiza tu rama local `$MAIN` con `git switch "$MAIN"` y `git pull --ff-only`.

---

## Parte B — Rama desactualizada con conflicto

### Rama esperada

```bash
git switch "$FEATURE_MODULUS"
```

### Escenario

La rama `$FEATURE_MODULUS` se creó antes de integrar `divide`, así que no contiene los cambios de la parte A. Ahora vas a añadir otra operación en la misma zona de los mismos ficheros para provocar un conflicto al rebasear la rama.

### Preguntas de reflexión

- ¿Qué diferencia hay entre traer cambios con `fetch` y modificar tu rama con `pull`, `merge` o `rebase`?
- ¿Cuándo preferirías rebasear una rama corta propia y cuándo preservarías un merge commit?
- Al resolver un conflicto, ¿cómo compruebas que no perdiste intención de ninguna rama?
- Si actualizas una rama publicada con rebase, ¿por qué debes empujar con cuidado?

### Práctica individual

1. Añade una función `modulus` en `app/calculator.py` justo después de `subtract`, en el mismo lugar donde la otra rama añadió `divide`.
1. En `tests/test_calculator.py`, modifica la línea de import para importar también `modulus`, partiendo de la versión antigua que todavía no conoce `divide`.
1. Añade un test `test_modulus` justo después de `test_subtract`, en el mismo lugar donde la otra rama añadió `test_divide`.
1. Haz un commit pequeño con la función y el test.
1. Sube la rama configurando upstream con `git push -u origin "$FEATURE_MODULUS"`.
1. Trae los cambios remotos con `git fetch origin`.
1. Actualiza tu rama con `$MAIN`.
1. Resuelve los conflictos en `app/calculator.py` y `tests/test_calculator.py`, conservando `divide`, `modulus`, `test_divide`, `test_modulus` y una sola línea de import válida.
1. Si tu versión de Git resolviera alguno de los ficheros automáticamente, revisa igualmente el diff para confirmar que no se perdió ningún cambio de la otra rama.
1. Añade los ficheros resueltos al stage y continúa el rebase.
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

- Completa la parte A con `divide`, `test_divide` y upstream configurado para `feature/divide-operation-<username>`.
- Completa la parte B con `modulus`, `test_modulus` y upstream configurado para `feature/modulus-operation-<username>`.
- Resuelve el conflicto de la parte B conservando los cambios de ambas ramas.
- Abre los PR contra tu rama `$MAIN`, no contra `main`.
