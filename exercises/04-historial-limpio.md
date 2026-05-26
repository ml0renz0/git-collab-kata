# 04 — Historial limpio antes de PR

## Objetivo

Practicar `git rebase -i`, squash, fixup, autosquash y actualización segura del remoto cuando una rama ya publicada necesita reescribir su historial antes de abrir o actualizar un PR.

## Demo

- En la presentación ensuciaremos una rama con commits `wip`, archivos temporales y cambios útiles mezclados.
- Veremos cómo leer el historial con `git log --oneline --graph --decorate`.
- Usaremos `git rebase -i` para borrar commits que no deben llegar al PR y combinar commits que sí pertenecen a la misma unidad de cambio.
- Compararemos `squash` y `fixup`: cuándo queremos conservar parte del mensaje y cuándo queremos descartarlo.
- Cerraremos con `git commit --fixup` y `git rebase -i --autosquash` para automatizar una limpieza habitual en ramas largas.

## Convención de ramas

Como en los ejercicios anteriores, cada participante trabaja contra su rama principal de usuario. En este ejercicio es especialmente importante respetar los nombres base de las ramas, porque el validador comprueba tanto archivos como forma del historial.

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE_CLEAN="feature/clean-history-${USER_ID}"
FEATURE_SQUASH="feature/squash-demo-${USER_ID}"
FEATURE_FIXUP="feature/fixup-demo-${USER_ID}"
```

Sustituye `<username>` por tu identificador, por ejemplo `anapascual`.

El validador acepta `feature/clean-history`, `feature/squash-demo`, `feature/fixup-demo` y ramas con esos mismos nombres base más sufijo, como `feature/clean-history-anapascual`. No cambies estas ramas a otros nombres.

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

## Ejercicio 4A — Limpiar commits basura

### Rama esperada

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE_CLEAN="feature/clean-history-${USER_ID}"

git switch "$MAIN"              # cambiar a tu rama principal
git pull --ff-only              # actualizar tu rama principal con fast-forward
git switch -c "$FEATURE_CLEAN"  # crear y cambiar a la rama del ejercicio
```

### Escenario

Has preparado documentación de uso para el proyecto, pero en la rama hay ruido: un archivo temporal, mensajes malos y commits que solo existen para deshacer errores previos.

### Preguntas

- ¿Qué commits cuentan una intención útil y cuáles solo son ruido?
- ¿Qué diferencia hay entre borrar un archivo en un commit nuevo y eliminar del historial el commit que lo introdujo?
- ¿Por qué conviene revisar el PR antes de pedir review aunque el código ya funcione?

### Tarea de demo

1. Crea un archivo temporal `temp.txt` y commitéalo con un mensaje malo, por ejemplo `wip`.
1. Crea `docs/usage.md` con documentación útil y commitéalo con un mensaje malo, por ejemplo `stuff`.
1. Borra `temp.txt` y commitéalo.
1. Revisa la rama con `git log --oneline --graph --decorate "$MAIN"..HEAD`.
1. Limpia la rama con `git rebase -i "$MAIN"` para que al final quede un solo commit útil sobre `$MAIN`.
1. Usa un mensaje final claro, por ejemplo `docs: add usage guide`.
1. Ejecuta `python scripts/validate.py` en la rama `feature/clean-history-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube la rama configurando upstream con `git push -u origin "$FEATURE_CLEAN"`.
1. Abre PR desde `$FEATURE_CLEAN` contra `$MAIN` y comprueba que el PR muestra un único commit útil.

### Resultado esperado observable

- Existe `docs/usage.md`.
- No existe `temp.txt`.
- La rama tiene un solo commit sobre `$MAIN`.
- No hay mensajes `wip`, `stuff`, `tmp`, `temp`.

---

## Ejercicio 4B — Squash y fixup antes de PR

### Ramas esperadas

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE_SQUASH="feature/squash-demo-${USER_ID}"
FEATURE_FIXUP="feature/fixup-demo-${USER_ID}"
```

Para la primera parte:

```bash
git switch "$MAIN"               # cambiar a tu rama principal
git pull --ff-only               # actualizar tu rama principal con fast-forward
git switch -c "$FEATURE_SQUASH"  # crear y cambiar a la rama de squash
```

Para la segunda parte, vuelve a `$MAIN` y crea la rama de fixup:

```bash
git switch "$MAIN"              # cambiar a tu rama principal
git pull --ff-only              # actualizar tu rama principal con fast-forward
git switch -c "$FEATURE_FIXUP"  # crear y cambiar a la rama de fixup
```

### Escenario

Vas a preparar dos PRs de documentación. En el primero, escribes una guía por partes y luego haces squash para que la historia cuente una sola intención. En el segundo, partes de un commit principal y añades correcciones pequeñas con `fixup` para practicar autosquash.

### Preguntas

- ¿Cuándo usarías `squash` y cuándo `fixup`?
- ¿Qué hace `git rebase -i --autosquash "$MAIN"` con los commits `fixup! ...`?
- Si ya habías subido una rama antes de reescribirla, ¿por qué `git push --force-with-lease` es más seguro que `git push -f`?
- ¿Contra qué rama debe abrirse el PR en este kata?

### Tarea entregable

Parte 1: squash manual.

1. En `$FEATURE_SQUASH`, crea `docs/squash.md` con una primera sección breve y haz un commit.
1. Añade una segunda sección al mismo archivo y haz otro commit.
1. Añade una tercera sección al mismo archivo y haz un tercer commit.
1. Revisa los tres commits con `git log --oneline "$MAIN"..HEAD`.
1. Usa `git rebase -i "$MAIN"` para dejar un solo commit final.
1. Usa un mensaje final claro, por ejemplo `docs: explain squash workflow`.
1. Ejecuta `python scripts/validate.py` en la rama `feature/squash-demo-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube la rama configurando upstream con `git push -u origin "$FEATURE_SQUASH"`.
1. Abre PR desde `$FEATURE_SQUASH` contra `$MAIN`.

Parte 2: fixup/autosquash.

1. En `$FEATURE_FIXUP`, crea `docs/api.md` con un commit principal y mensaje claro, por ejemplo `docs: add api notes`.
1. Guarda el hash de ese commit con `git log --oneline -1`.
1. Añade una aclaración a `docs/api.md`.
1. Crea un commit `fixup` contra el commit principal.
1. Añade otro pequeño ajuste a `docs/api.md`.
1. Crea otro commit `fixup` contra el mismo commit principal.
1. Ejecuta `git rebase -i --autosquash "$MAIN"` y comprueba que Git reordena los commits `fixup`.
1. Deja la rama con un solo commit final sobre `$MAIN`.
1. Ejecuta `python scripts/validate.py` en la rama `feature/fixup-demo-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube la rama configurando upstream. Si ya la habías subido antes del autosquash, usa `git push --force-with-lease`.
1. Abre PR desde `$FEATURE_FIXUP` contra `$MAIN`.

Comandos útiles:

```bash
git commit --fixup <hash-del-commit-principal>
git rebase -i --autosquash "$MAIN"
git push --force-with-lease
```

### Validación local

```bash
python scripts/validate.py             # ejecutar validación local del repositorio
pytest -q                              # ejecutar tests desde el entorno virtual
```

### Validación en GitHub

Abre PR desde cada feature contra tu rama `$MAIN`. El workflow debe pasar sin modificar `main`.

## Entregable

- Completa el ejercicio 4A como demo con `docs/usage.md`, sin `temp.txt`, sin mensajes temporales y con un solo commit sobre `$MAIN`.
- Completa el ejercicio 4B parte 1 con `docs/squash.md` y un solo commit final sobre `$MAIN`.
- Completa el ejercicio 4B parte 2 con `docs/api.md`, usando commits `fixup` y `git rebase -i --autosquash`, y deja un solo commit final sobre `$MAIN`.
- Si reescribes una rama que ya habías subido, actualiza el remoto con `git push --force-with-lease`.
- Abre los PR contra tu rama `$MAIN`, no contra `main`.
