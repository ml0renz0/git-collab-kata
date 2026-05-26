# 01 — Staging quirúrgico y commits pequeños

## Objetivo

Practicar `git add -p`, `git stash`, `git commit --amend` y `git rebase -i` para separar cambios mezclados y limpiar commits y ordenar la historia Git.

## Demo

- En la presentación resolveremos un flujo completo con `git add -p` y `git stash`.
- Crearemos un cambio útil (`multiply`) y un cambio temporal de debug, luego usaremos stash para apartar lo que no queremos commitear todavía.
- Veremos `git stash push -k -m "debug"`, `git stash list`, `git stash pop` y `git stash drop` para guardar, recuperar o descartar el trabajo temporal según convenga.

## Convención de ramas

Como no se trabaja con forks, cada participante debe usar una rama principal propia y ramas de feature con sufijo de usuario:

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
```

Sustituye `<username>` por tu identificador, por ejemplo `anapascual`.

Como no existe inicialmente, es necesario crear esta rama principal de usuario:

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"

git switch main            # cambiar a la rama principal
git pull --ff-only         # actualizar la rama principal con fast-forward
git switch -c "$MAIN"      # crear y cambiar a la rama del ejercicio
git push -u origin "$MAIN" # subir la rama al repositorio
```

## Ejercicio 1A — Separar cambios mezclados y hacer un fixup sencillo

### Rama esperada

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE="feature/multiply-${USER_ID}"

git switch "$MAIN"        # cambiar a tu rama principal
git pull --ff-only        # actualizar tu rama principal con fast-forward
git switch -c "$FEATURE"  # crear y cambiar a la rama del ejercicio
```

### Escenario

Has editado `app/calculator.py` para añadir una operación nueva, pero también metiste una traza de debug que no debería commitearse.

### Tarea de demo

1. Añade una función `multiply` en `app/calculator.py`.
1. Añade temporalmente un `print` de debug dentro de `multiply` y ejecútalo para probarlo.
1. Usa `git add -p` para añadir solo la implementación de `multiply`, sin la traza de debug.
1. Usa `git stash push -k -m "debug"` para guardar en el stash local el debug de `multiply`.
1. Haz un primer commit incluyendo únicamente la función `multiply`.
1. Comprueba `git stash list`; si no quieres revisar el cambio de debug usa `git stash drop` para descartarlo, o bien usa `git stash pop` si quieres recuperarlo antes.
1. Añade un test `test_multiply` en `tests/test_calculator.py` para la nueva función.
1. Haz un segundo commit incluyendo únicamente el test `test_multiply`.
1. Usa `git rebase -i HEAD~2` y marca el commit del test como `fixup` para dejar un único commit final con función y test.
1. Ejecuta `python scripts/validate.py` en la rama `feature/multiply-<username>`.
1. Sube la rama, abre PR contra tu rama `$MAIN` y combínala.


## Ejercicio 1B — Mezclar cambios de fix en el commit original que los introdujo

### Rama esperada

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
FEATURE="feature/exponentiation-${USER_ID}"

git switch "$MAIN"        # cambiar a tu rama principal
git pull --ff-only        # actualizar tu rama principal con fast-forward
git switch -c "$FEATURE"  # crear y cambiar a la rama del ejercicio
```

### Escenario

Has editado `app/calculator.py` para añadir una operación nueva, pero también metiste un bug y quieres combinar el commit de fix con el commit original para mantener la historia de git limpia.

### Tarea entregable

1. Implementa la función `exponentiation` en `app/calculator.py`, pero invierte por error los parámetros: usa el primero como exponente y el segundo como base.
1. Añade un test `test_exponentiation` en `tests/test_calculator.py`.
1. Usa `git add -p` para incluir la implementación de `exponentiation` en el primer commit.
1. Empuja la rama al remoto con `git push -u origin "$FEATURE"`.
1. Crea un segundo commit con el test `test_exponentiation`, pero equivócate a propósito y pon un `*` en lugar de dos.
1. Arregla el commit previo usando `git commit --amend`.
1. Prueba la función ejecutando: `python -c "from app.calculator import exponentiation ; print(exponentiation(2,3))"` y detecta el problema de parámetros.
1. Arregla el bug de los parámetros y crea un tercer commit de fix.
1. Usa `git rebase -i HEAD~3` para combinar el commit de fix con el commit de la función y dejar una historia limpia. Asegúrate de que el test sigue presente y en un commit aparte.
1. Ejecuta `python scripts/validate.py` en la rama `feature/exponentiation-<username>`.
1. Sube la rama actualizada, abre PR contra tu rama `$MAIN` y combínala.

### Validación local

```bash
pytest -q                              # ejecutar tests en modo silencioso
python scripts/validate.py             # ejecutar validación local del repositorio
```

### Validación en GitHub

Abre PR desde `$FEATURE` contra tu rama `$MAIN`. El workflow debe pasar sin modificar `main`.

## Entregable

- Completa el ejercicio 1A con `multiply`, `test_multiply`, sin la traza de debug y con un único commit final tras el fixup.
- Completa el ejercicio 1B con `exponentiation`, `test_exponentiation`, sin la traza de debug y con dos commits: uno para la función y otro para el test.
- Abre los PR contra tu rama `$MAIN`, no contra `main`.
