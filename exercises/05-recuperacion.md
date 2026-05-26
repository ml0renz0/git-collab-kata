# 05 — Recuperación de errores

## Objetivo

Practicar `git restore`, `git restore --staged`, `git reset`, `git reflog` y `git revert` para recuperar trabajo local, rescatar commits que parecen perdidos y deshacer cambios en historial compartido sin reescribirlo.

## Demo

- En la presentación romperemos el árbol de trabajo a propósito y lo recuperaremos con `git restore`.
- Añadiremos archivos al stage por error y los sacaremos con `git restore --staged`.
- Crearemos un commit incorrecto y lo desharemos con `git reset --soft`, comparando qué ocurre con el commit, el stage y el árbol de trabajo.
- Perderemos aparentemente un commit con `git reset --hard` y lo recuperaremos desde `git reflog` creando una rama de rescate.
- Cerraremos con `git revert` para deshacer un cambio ya compartido sin mover la historia hacia atrás.

## Convención de ramas

Como en los ejercicios anteriores, cada participante trabaja contra su rama principal de usuario. En este ejercicio hay una restricción adicional: las ramas deben mantener estos nombres base, porque cada una activa una validación distinta.

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE_RECOVERY="feature/recovery-sandbox-${USER_ID}"
RESCUE_REFLOG="rescue/reflog-${USER_ID}"
CHORE_REVERT="chore/revert-demo-${USER_ID}"
```

Sustituye `<username>` por tu identificador, por ejemplo `anapascual`.

El validador acepta `feature/recovery-sandbox`, `rescue/reflog`, `chore/revert-demo` y ramas con esos mismos nombres base más sufijo, como `rescue/reflog-anapascual`. No cambies estas ramas a otros nombres.

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

## Ejercicio 5A — Recuperar el árbol de trabajo y el stage

### Rama esperada

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE_RECOVERY="feature/recovery-sandbox-${USER_ID}"

git switch "$MAIN"                  # cambiar a tu rama principal
git pull --ff-only                  # actualizar tu rama principal con fast-forward
git switch -c "$FEATURE_RECOVERY"   # crear y cambiar a la rama sandbox
```

### Escenario

Estás preparando una nota de recuperación, pero durante una prueba borras un archivo de código y además añades al stage un archivo local de debug que no debería llegar al repositorio.

### Preguntas

- ¿Qué diferencia hay entre restaurar un archivo del árbol de trabajo y sacarlo del stage?
- ¿Qué comando usarías si el archivo modificado todavía no se ha añadido al stage?
- ¿Por qué conviene ejecutar `git status` antes y después de cada recuperación?

### Tarea de demo

1. Borra `app/calculator.py` a propósito.
1. Ejecuta `git status` y confirma que Git detecta el borrado.
1. Recupera el archivo con `git restore app/calculator.py`.
1. Crea `debug.conf` con una línea temporal, por ejemplo `debug=true`.
1. Añade `debug.conf` al stage por error.
1. Ejecuta `git status` para ver que el archivo está staged.
1. Saca `debug.conf` del stage con `git restore --staged debug.conf`.
1. Borra `debug.conf`.
1. Crea `docs/recovery.md` con una nota breve que mencione `restore` y `staged`.
1. Haz un commit solo con `docs/recovery.md`.
1. Ejecuta `python scripts/validate.py` en la rama `feature/recovery-sandbox-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube la rama configurando upstream.
1. Abre PR desde `$FEATURE_RECOVERY` contra `$MAIN` y combínala.

### Resultado esperado observable

- Existe `docs/recovery.md`.
- `docs/recovery.md` menciona `restore` y `staged`.
- Existe `app/calculator.py`.
- No existe `debug.conf`.

---

## Ejercicio 5B — Reflog y revert en recuperación compartida

### Ramas esperadas

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
RESCUE_REFLOG="rescue/reflog-${USER_ID}"
CHORE_REVERT="chore/revert-demo-${USER_ID}"
```

Para la primera parte, trabaja desde tu rama principal y crearás la rama de rescate desde el hash recuperado:

```bash
git switch "$MAIN"
git pull --ff-only
```

Para la segunda parte, vuelve a `$MAIN` y crea la rama de revert:

```bash
git switch "$MAIN"             # cambiar a tu rama principal
git pull --ff-only             # actualizar tu rama principal con fast-forward
git switch -c "$CHORE_REVERT"  # crear y cambiar a la rama de revert
```

### Escenario

Vas a resolver dos accidentes habituales:

- Primero, haces un commit importante y después ejecutas un `reset --hard`; el trabajo parece perdido, pero Git conserva el movimiento en el `reflog`.
- Después, simulas un cambio roto ya publicado y lo deshaces con `revert`, porque en historial compartido no quieres mover la rama hacia atrás.

### Preguntas

- ¿Qué conserva `git reset --soft HEAD~1` que no conserva `git reset --hard HEAD~1`?
- ¿Por qué `git reflog` puede encontrar commits que ya no aparecen en `git log`?
- ¿Qué ventaja tiene crear una rama de rescate en lugar de copiar manualmente el contenido del archivo perdido?
- ¿Por qué `revert` es más apropiado que `reset --hard` cuando otras personas pueden haber basado trabajo en el commit roto?
- ¿Qué debe mostrar el historial después de hacer `git revert HEAD`?

### Tarea entregable

Parte 1: rescate con `reflog`.

1. Desde `$MAIN`, crea `important.txt` con contenido que incluya la palabra `important`.
1. Añade el archivo al stage y crea un commit con mensaje claro, por ejemplo `docs: capture important recovery note`.
1. Ejecuta `git log --oneline -1` y guarda el hash del commit.
1. Ejecuta `git reset --hard HEAD~1` para sacar ese commit de `$MAIN`.
1. Ejecuta `git reflog` y localiza el hash del commit perdido.
1. Recupera el trabajo creando una rama de rescate desde ese hash:

```bash
git switch -c "$RESCUE_REFLOG" <hash-del-commit-perdido>
```

1. Comprueba que `important.txt` existe y contiene la palabra `important`.
1. Ejecuta `python scripts/validate.py` en la rama `rescue/reflog-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube la rama configurando upstream con `git push -u origin "$RESCUE_REFLOG"`.
1. Abre PR desde `$RESCUE_REFLOG` contra `$MAIN` y combínala.

Parte 2: revert en historial compartido.

1. Crea `production.txt` con contenido que incluya la palabra `broken`.
1. Haz un commit con mensaje claro, por ejemplo `chore: add broken production marker`.
1. Ejecuta `git revert HEAD`.
1. Acepta o ajusta el mensaje de revert para que quede claro qué commit se deshace.
1. Comprueba con `git log --oneline "$MAIN"..HEAD` que hay un commit original y un commit de revert.
1. Comprueba que `production.txt` ya no existe.
1. Ejecuta `python scripts/validate.py` en la rama `chore/revert-demo-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube la rama configurando upstream con `git push -u origin "$CHORE_REVERT"`.
1. Abre PR desde `$CHORE_REVERT` contra `$MAIN` y combínala.

### Resultado esperado observable

- En `rescue/reflog-<username>` existe `important.txt`.
- `important.txt` contiene `important`.
- No existe `production.txt`.
- `chore/revert-demo-<username>` tiene al menos dos commits sobre `$MAIN`: el cambio roto y el revert.
- Algún mensaje de commit de la rama contiene `Revert`.

### Validación local

```bash
python scripts/validate.py             # ejecutar validación local del repositorio
pytest -q                              # ejecutar tests desde el entorno virtual
```

### Validación en GitHub

Abre PR desde cada rama contra tu rama `$MAIN`. El workflow debe pasar sin modificar `main`.

## Entregable

- Completa el ejercicio 5A como demo con `docs/recovery.md`, conservando `app/calculator.py` y sin subir `debug.conf`.
- Completa el ejercicio 5B parte 1 creando `rescue/reflog-<username>` desde el commit recuperado con `git reflog`, con `important.txt` presente.
- Completa el ejercicio 5B parte 2 con `chore/revert-demo-<username>`, sin `production.txt` al final y con un commit de revert en el historial.
- Abre los PR contra tu rama `$MAIN`, no contra `main`.
