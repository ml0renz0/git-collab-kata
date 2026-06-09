# 03 — Rebase y conflictos

## Objetivo

Practicar hotfixes pequeños, actualización de ramas con `fetch` y `rebase`, resolución de conflictos y coordinación entre cambios concurrentes sin perder trabajo de otra persona.

## Demo

- En la presentación resolveremos un hotfix pequeño sobre `divide` usando una rama `hotfix/*`.
- Veremos cómo comprobar que la rama contiene la base correcta antes de empezar.
- Simularemos dos ramas que modifican la misma función `add` desde la misma base.
- Resolveremos el conflicto conservando los cambios funcionales de ambas ramas.
- Compararemos cuándo tiene sentido continuar un rebase, abortarlo o volver a empezar.

## Convención de ramas

Como en los ejercicios anteriores, cada participante trabaja contra su rama principal de usuario. En este ejercicio hay una restricción adicional: el hotfix debe mantener el nombre base `hotfix/division-by-zero`, porque esa rama activa la validación específica del kata.

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
HOTFIX="hotfix/division-by-zero-${USER_ID}"
FEATURE_CAST="feature/add-cast-int-${USER_ID}"
FEATURE_NONE="feature/add-none-validation-${USER_ID}"
```

Sustituye `<username>` por tu identificador, por ejemplo `anapascual`.

El validador acepta `hotfix/division-by-zero` y ramas con ese mismo nombre base más sufijo, como `hotfix/division-by-zero-anapascual`. No cambies el hotfix a `feature/*`.

A partir de aquí se asume que tu rama principal de usuario ya se creó en el ejercicio 1. Antes de empezar, cámbiate a ella y actualízala:

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"

git switch "$MAIN"
git pull --ff-only
```

Si estás haciendo este ejercicio de forma aislada y `$MAIN` todavía no existe, créala primero desde `main` siguiendo la convención del ejercicio 1 o del README.

---

## Parte A — Hotfix con conflicto potencial

### Rama esperada

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
HOTFIX="hotfix/division-by-zero-${USER_ID}"

git switch "$MAIN"        # cambiar a tu rama principal
git pull --ff-only        # actualizar tu rama principal con fast-forward
git switch -c "$HOTFIX"   # crear y cambiar a rama hotfix
```

### Escenario

Después de integrar `divide`, alguien detecta que la división por cero no está tratada de forma explícita. Es un cambio pequeño, urgente y fácil de revisar, así que se prepara como hotfix.

### Preguntas de reflexión

- ¿Qué diferencia práctica hay entre una feature normal y un hotfix?
- ¿Por qué un hotfix debería ser pequeño y fácil de revisar?
- ¿Qué prueba mínima convierte una incidencia en una regresión cubierta?
- ¿Por qué conviene comprobar la base de la rama antes de empezar?

### Práctica guiada

1. Asegúrate de que `divide` existe en `app/calculator.py`. Si no existe, integra primero el resultado de la parte A del ejercicio 02 en tu rama `$MAIN`.
1. Haz que `divide` gestione explícitamente la división por cero lanzando `ZeroDivisionError`.
1. Añade un test cuyo nombre o contenido incluya `zero`.
1. Crea un commit con la implementación y el test.
1. Ejecuta `python scripts/validate.py` en la rama `hotfix/division-by-zero-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube la rama configurando upstream con `git push -u origin "$HOTFIX"`.
1. Abre PR desde `$HOTFIX` contra `$MAIN` y combínala.
1. Actualiza tu rama local `$MAIN` con `git switch "$MAIN"` y `git pull --ff-only`.

---

## Preparación — Dos ramas que tocarán la misma función

Antes de implementar nada para la parte B, crea dos ramas desde el mismo punto de partida. Esto hará que una rama quede desactualizada cuando la otra se integre primero.

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE_CAST="feature/add-cast-int-${USER_ID}"
FEATURE_NONE="feature/add-none-validation-${USER_ID}"

git switch "$MAIN"
git pull --ff-only
git switch -c "$FEATURE_CAST"
git switch "$MAIN"
git switch -c "$FEATURE_NONE"
```

---

## Parte B — Rebase con conflicto manual

### Rama esperada

Persona A trabaja en:

```bash
git switch "$FEATURE_CAST"
```

Persona B trabaja en:

```bash
git switch "$FEATURE_NONE"
```

### Escenario

Dos personas modifican `add` en `app/calculator.py` desde la misma base:

- Persona A cambia `add` para castear los argumentos a `int`.
- Persona B cambia `add` para rechazar explícitamente valores `None`.

La rama de Persona A se integrará primero. Persona B tendrá que actualizar su rama con rebase y resolver el conflicto conservando los dos comportamientos.

Tú haces de Persona A y Persona B: crea las dos ramas, integra primero `$FEATURE_CAST` y después vuelve a `$FEATURE_NONE` para resolver el conflicto.

### Preguntas de reflexión

- ¿Qué significa conservar la intención de dos ramas cuando ambas modifican la misma función?
- ¿Qué revisarías en el diff final después de quitar los marcadores de conflicto?
- ¿Por qué no basta con que el rebase termine sin errores?
- ¿Qué riesgo evita `git push --force-with-lease` después de resolver una rama rebaseada?

### Práctica individual

1. Persona A implementa el casteo a `int` en `add`.
1. Persona A añade un test que demuestre que `add("2", "3")` devuelve `5`.
1. Persona A revisa sus cambios con `git status` y `git diff`.
1. Persona A hace un commit pequeño, sube `$FEATURE_CAST`, abre PR contra `$MAIN` y lo combina.
1. Persona B implementa la validación de `None` en `add` sobre la rama `$FEATURE_NONE`, creada antes de integrar la rama de Persona A.
1. Persona B añade un test que demuestre que `add(None, 3)` falla de forma explícita.
1. Persona B hace un commit pequeño y sube `$FEATURE_NONE` configurando upstream.
1. Persona B trae los cambios remotos con `git fetch origin`.
1. Persona B actualiza su rama con `git rebase "origin/$MAIN"`.
1. Persona B inspecciona el conflicto con `git status` y `git diff`.
1. Persona B resuelve el conflicto en `app/calculator.py` conservando el casteo a `int` y la validación de `None`.
1. Persona B conserva los tests de ambas ramas.
1. Persona B añade los ficheros resueltos al stage y continúa el rebase con `git rebase --continue`.
1. Persona B ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Persona B sube la rama actualizada con `git push --force-with-lease`.
1. Persona B abre PR desde `$FEATURE_NONE` contra `$MAIN` y lo combina.

### Validación local

```bash
python scripts/validate.py             # ejecutar validación local del repositorio
pytest -q                              # ejecutar tests desde el entorno virtual
```

### Validación en GitHub

Abre PR desde cada rama contra tu rama `$MAIN`. El workflow debe pasar sin modificar `main`.

## Entregable

- Completa la parte A con `divide`, gestión explícita de división por cero mediante `ZeroDivisionError` y un test que incluya `zero`.
- Completa la parte B resolviendo el conflicto manual en `add`.
- Conserva los dos comportamientos de `add`: rechazo explícito de `None` y casteo a `int`.
- Conserva los tests de ambas ramas.
- Abre los PR contra tu rama `$MAIN`, no contra `main`.
