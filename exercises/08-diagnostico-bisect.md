# 08 — Merge y diagnóstico con bisect

## Objetivo

Practicar `git merge --no-ff`, `git blame`, `git log -S`, `git log -G`, `git bisect`, `git bisect run`, lectura de historial y decisión de recuperación cuando una regresión ya existe en una rama compartida. El objetivo no es solo arreglar el bug, sino entender cómo queda una historia con merge, acotar la investigación, localizar qué commit introdujo el fallo y dejar una explicación mínima que otra persona pueda revisar.

## Demo

- En la presentación construiremos una pequeña historia con una operación `factorial`.
- Crearemos una rama auxiliar de documentación y la fusionaremos con `git merge --no-ff` para observar un merge commit real.
- Dejaremos varios commits intermedios: uno correcto, un merge commit, cambios de ruido y un commit que introduce una regresión.
- Antes de lanzar `bisect`, acotaremos la investigación con `git blame`, `git log -S` y `git log -G`.
- Usaremos `git bisect start`, `git bisect good`, `git bisect bad`, `git bisect run` y `git bisect reset`.
- Cerraremos con un hotfix pequeño y un informe de diagnóstico en `docs/bisect-report.md`.

## Convención de ramas

Como en los ejercicios anteriores, cada participante trabaja contra su rama principal de usuario. En este ejercicio la rama debe mantener el nombre base `hotfix/factorial-regression`, porque activa la validación específica del kata.

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
HOTFIX_FACTORIAL="hotfix/factorial-regression-${USER_ID}"
DOCS_FACTORIAL="chore/factorial-notes-${USER_ID}"
```

Sustituye `<username>` por tu identificador, por ejemplo `anapascual`.

El validador acepta `hotfix/factorial-regression` y ramas con ese mismo nombre base más sufijo, como `hotfix/factorial-regression-anapascual`. No cambies esta rama a `feature/*`.

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

## Parte A — Preparar una regresión diagnosticable

### Rama esperada

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"
HOTFIX_FACTORIAL="hotfix/factorial-regression-${USER_ID}"
DOCS_FACTORIAL="chore/factorial-notes-${USER_ID}"

git switch "$MAIN"
git pull --ff-only
git switch -c "$HOTFIX_FACTORIAL"
```

### Escenario

El equipo añadió `factorial`, integró una rama auxiliar de documentación mediante merge y después alguien detecta que `factorial(0)` ya no devuelve `1`. Antes de arreglarlo, vas a localizar el commit que introdujo la regresión.

### Práctica guiada

Parte 1: crear una historia con un bug escondido.

1. Añade `factorial(n)` en `app/calculator.py`.
1. Haz que `factorial(0)` devuelva `1`, `factorial(5)` devuelva `120` y `factorial(-1)` lance `ValueError`.
1. Añade tests para `factorial(0)`, `factorial(5)` y `factorial(-1)`.
1. Haz un commit claro, por ejemplo `feat: add factorial operation`.
1. Crea una rama auxiliar de documentación desde la rama actual:

```bash
git switch -c "$DOCS_FACTORIAL"
```

1. Añade una nota breve en `docs/factorial.md` y haz un commit, por ejemplo `docs: explain factorial operation`.
1. Vuelve a la rama del hotfix:

```bash
git switch "$HOTFIX_FACTORIAL"
```

1. Fusiona la rama auxiliar creando un merge commit explícito:

```bash
git merge --no-ff "$DOCS_FACTORIAL"
```

1. Observa la historia con `git log --oneline --graph --decorate "$MAIN"..HEAD`.
1. Introduce una regresión a propósito: cambia `factorial(0)` para que falle o devuelva `0`.
1. Haz un commit con apariencia inocente, por ejemplo `refactor: simplify factorial loop`.
1. Añade otro cambio de ruido pequeño en `docs/factorial.md` y haz un commit más.
1. Comprueba que ahora `pytest -q` falla por la regresión de `factorial(0)`.

Parte 2: investigar el historial antes de hacer `bisect`.

1. Mira qué commits tocaron las líneas actuales de `factorial`:

```bash
git blame app/calculator.py
```

1. Busca commits que añadieron o quitaron apariciones de la cadena `factorial`:

```bash
git log -S "factorial" -- app/calculator.py tests
```

1. Busca commits cuyas líneas modificadas coincidan con una llamada o definición de `factorial`:

```bash
git log -G "factorial\\(" -- app/calculator.py tests
```

1. Anota qué aporta cada comando y qué duda deja abierta antes de usar `bisect`.

Parte 3: diagnosticar con `bisect`.

1. Marca el estado actual como malo:

```bash
git bisect start
git bisect bad
```

1. Localiza un commit bueno anterior, por ejemplo el commit `feat: add factorial operation`.
1. Marca ese commit como bueno:

```bash
git bisect good <hash-del-commit-bueno>
```

1. En cada paso, ejecuta el test de regresión y marca el commit como `good` o `bad`.
1. Como alternativa, automatiza la búsqueda con:

```bash
git bisect run pytest -q
```

1. Apunta el hash y el mensaje del commit que Git identifica como culpable.
1. Vuelve al estado normal:

```bash
git bisect reset
```

---

## Parte B — Hotfix e informe de diagnóstico

### Rama esperada

```bash
git switch "$HOTFIX_FACTORIAL"
```

### Escenario

Ya sabes qué commit introdujo la regresión. Como la rama representa trabajo compartido, no vas a borrar el commit roto: harás un fix forward y dejarás documentado el diagnóstico.

### Preguntas de reflexión

- ¿Qué significa marcar un commit como `good` o `bad` durante un bisect?
- ¿Qué diferencia ves entre el commit normal de `factorial` y el merge commit de documentación?
- ¿Por qué `git merge --no-ff "$DOCS_FACTORIAL"` crea un commit de merge aunque Git pudiera avanzar por fast-forward?
- ¿Qué te aportan `git blame`, `git log -S` y `git log -G` antes de empezar un `bisect`?
- ¿Qué ventaja aporta `git bisect run` frente a ejecutar manualmente los tests?
- ¿Por qué debes ejecutar `git bisect reset` al terminar?
- Si el commit roto ya está compartido, ¿por qué conviene hacer un fix forward en vez de reescribir la historia?
- ¿Qué información mínima debe tener un informe de diagnóstico para que otra persona confíe en el arreglo?

### Práctica individual

1. Arregla `factorial` para que:
   - `factorial(0)` devuelva `1`;
   - `factorial(5)` devuelva `120`;
   - `factorial(-1)` lance `ValueError`.
1. Asegúrate de que los tests cubren esos tres comportamientos.
1. Crea `docs/bisect-report.md` con estos apartados:

```markdown
## Comando de reproducción

## Investigación previa

## Commit culpable

## Decisión
```

1. En el informe, menciona `git blame`, `git log -S`, `git log -G`, `git bisect`, el caso `factorial(0)`, el hash o mensaje del commit culpable y la decisión de hacer fix forward.
1. Haz un commit claro, por ejemplo `fix: restore factorial zero case`.
1. Ejecuta `python scripts/validate.py` en la rama `hotfix/factorial-regression-<username>`.
1. Ejecuta `pytest -q` desde el entorno virtual del proyecto.
1. Sube la rama configurando upstream con `git push -u origin "$HOTFIX_FACTORIAL"`.
1. Abre PR desde `$HOTFIX_FACTORIAL` contra `$MAIN` y combínala.

### Resultado esperado observable

- Existe `factorial` en `app/calculator.py`.
- `factorial(0)` devuelve `1`.
- `factorial(5)` devuelve `120`.
- `factorial(-1)` lanza `ValueError`.
- Los tests cubren los casos `0`, `5` y `-1`.
- Existe `docs/bisect-report.md`.
- El informe menciona `git blame`, `git log -S`, `git log -G`, `git bisect`, `factorial(0)`, el commit culpable y la decisión de fix forward.
- La rama conserva una historia con varios commits y al menos un merge commit para que `bisect` y `merge` tengan sentido.

### Validación local

```bash
python scripts/validate.py             # ejecutar validación local del repositorio
pytest -q                              # ejecutar tests desde el entorno virtual
```

### Validación en GitHub

Abre PR desde `$HOTFIX_FACTORIAL` contra tu rama `$MAIN`. El workflow debe pasar sin modificar `main`.

## Entregable

- Completa la historia de `hotfix/factorial-regression-<username>` con un merge commit, una regresión diagnosticable y un fix posterior.
- Usa `git merge --no-ff` para fusionar la rama auxiliar `chore/factorial-notes-<username>`.
- Usa `git blame`, `git log -S` y `git log -G` para acotar la investigación antes del bisect.
- Usa `git bisect` o `git bisect run` para localizar el commit culpable.
- Deja `docs/bisect-report.md` con el diagnóstico y la decisión de fix forward.
- Abre el PR contra tu rama `$MAIN`, no contra `main`.
