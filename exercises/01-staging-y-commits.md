# 01 — Staging quirúrgico y commits pequeños

## Objetivo

Practicar primero `git add -p` y `git stash` para separar cambios mezclados. Después, usar `git commit --amend` y `git rebase -i` para corregir commits pequeños sin perder la intención de la historia Git.

## Demo

- En la presentación resolveremos un flujo completo con `git add -p` y `git stash`.
- Crearemos un cambio útil (`multiply`) y un cambio temporal de debug, luego usaremos stash para apartar lo que no queremos commitear todavía.
- Veremos `git stash push -k -m "debug"`, `git stash list`, `git stash pop` y `git stash drop` para guardar, recuperar o descartar el trabajo temporal según convenga.
- Separaremos la práctica en dos momentos: primero dejar limpio el árbol de trabajo y después limpiar la historia de la rama.

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
git switch -c "$MAIN"      # crear y cambiar a tu rama principal personal
git push -u origin "$MAIN" # subir la rama al repositorio
```

## Parte A — Separar cambios mezclados y hacer un fixup sencillo

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

### Preguntas de reflexión

- ¿Cómo decides qué parte de un cambio pertenece al commit y qué parte es solo apoyo temporal?
- ¿Qué revisarías antes de crear el commit para asegurarte de que no entra una traza local?
- ¿Qué ventaja tiene apartar cambios con `stash` frente a borrarlos directamente?
- ¿Por qué conviene que el commit final cuente una intención completa?

### Práctica guiada

Parte 1: aislar el cambio útil.

1. Añade una función `multiply` en `app/calculator.py`.
1. Añade temporalmente un `print` de debug dentro de `multiply` y ejecútalo para probarlo.
1. Usa `git add -p` para añadir solo la implementación de `multiply`, sin la traza de debug.
1. Usa `git stash push -k -m "debug"` para guardar en el stash local el debug de `multiply`.
1. Haz un primer commit incluyendo únicamente la función `multiply`.
1. Comprueba `git stash list`; si no quieres revisar el cambio de debug usa `git stash drop` para descartarlo, o bien usa `git stash pop` si quieres recuperarlo antes.
1. Comprueba con `git status` que entiendes qué queda en el árbol de trabajo antes de seguir.

Parte 2: añadir el test y compactar la intención.

1. Añade un test `test_multiply` en `tests/test_calculator.py` para la nueva función.
1. Haz un segundo commit incluyendo únicamente el test `test_multiply`.
1. Revisa la historia con `git log --oneline "$MAIN"..HEAD` y confirma que hay dos commits relacionados con la misma intención.
1. Usa `git rebase -i HEAD~2` y marca el commit del test como `fixup` para dejar un único commit final con función y test.
1. Comprueba de nuevo la historia: debe quedar un solo commit final sobre `$MAIN`.
1. Ejecuta `python scripts/validate.py` en la rama `feature/multiply-<username>`.
1. Sube la rama, abre PR contra tu rama `$MAIN` y combínala.


## Parte B — Mezclar cambios de fix en el commit original que los introdujo

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

### Preguntas de reflexión

- ¿Cuándo tiene sentido usar `commit --amend` y cuándo necesitas un `rebase -i`?
- Si una rama ya está publicada, ¿qué riesgo aparece al reescribir su historia?
- ¿Por qué `push --force-with-lease` es más prudente que `push -f`?
- ¿Qué diferencia hay entre una historia honesta para depurar y una historia limpia para revisar?

### Práctica individual

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
1. Como ya habías subido la rama antes del rebase, actualiza el remoto adecuadamente.
1. Abre PR contra tu rama `$MAIN` y combínala.

### Validación local

```bash
pytest -q                              # ejecutar tests en modo silencioso
python scripts/validate.py             # ejecutar validación local del repositorio
```

### Validación en GitHub

Abre PR desde `$FEATURE` contra tu rama `$MAIN`. El workflow debe pasar sin modificar `main`.

## Entregable

- Completa la parte A con `multiply`, `test_multiply`, sin la traza de debug y con un único commit final tras el fixup.
- Completa la parte B con `exponentiation`, `test_exponentiation` y dos commits finales: uno para la función corregida y otro para el test.
- Abre los PR contra tu rama `$MAIN`, no contra `main`.
