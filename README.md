# Git Collaboration Kata

Repositorio para impartir un curso práctico de Git colaborativo avanzado.

La idea es que los ejercicios no publiquen soluciones paso a paso. Los alumnos trabajan en ramas con nombres concretos y la validación comprueba el resultado observable: tests, forma de la rama, historial, ausencia de secretos y algunos criterios específicos del ejercicio.

## Requisitos

- Git 2.40+ recomendado.
- Python 3.11+ o 3.12.
- Cuenta de GitHub si quieres usar pull requests reales con los workflows y el formulario de entrega incluidos.
- GitLab u otra plataforma sirve para practicar Git, pero requiere adaptar CI, PRs/MRs y entrega.

## Instalación local

```bash
git clone https://github.com/ml0renz0/git-collab-kata.git
cd git-collab-kata
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
pytest -q
python scripts/validate.py
```

## Cómo usarlo en clase

1. El instructor crea el repositorio remoto en GitHub.
2. Cada alumno clona el repo.
3. Cada alumno crea su rama principal de trabajo, por ejemplo `main-anapascual`.
4. Cada ejercicio indica una rama esperada, normalmente con sufijo de usuario, por ejemplo `feature/multiply-anapascual`.
5. El alumno hace cambios, commits y abre PR contra su rama `main-<username>`.
6. Los workflows y `scripts/validate.py` validan el resultado observable.
7. Si falla, el alumno debe leer el error y corregir su rama.

Cuando un ejercicio habla de Persona A, Persona B, reviewer o maintainer, no hace falta intervención externa: una sola persona puede simular todos los roles cambiando de rama, abriendo PRs y dejando notas o checklists en la descripción del PR.

Convención recomendada para evitar choques entre participantes:

```bash
USER_ID="<username>"
MAIN="main-${USER_ID}"

git switch main
git pull --ff-only
git switch -c "$MAIN"
git push -u origin "$MAIN"
```

Después, cada feature se crea desde `$MAIN` y se abre contra `$MAIN`, no contra `main`, salvo que el ejercicio indique explícitamente otra cosa.

Método de integración recomendado:

- `Squash and merge`: opción preferida para el kata. Deja un commit por PR en `main-<username>`, así la rama principal personal avanza con unidades de trabajo limpias y fáciles de revisar.
- `Create a merge commit`: conserva todos los commits de la rama y añade un commit de merge. Es útil para enseñar historia real de integración, pero mete más ruido en una rama principal que acumula muchos ejercicios.
- `Rebase and merge`: reaplica los commits de la rama en línea recta, sin commit de merge. Es útil si la rama ya tiene commits muy cuidados, pero exige más higiene en cada rama que se combina.

Usamos `Squash and merge` porque el PR ya conserva el contexto completo: commits intermedios, conversación, checks y revisión. Eso permite practicar commits imperfectos, `fixup`, conflictos o limpieza dentro de la rama sin obligar a que cada paso intermedio quede publicado en la historia final. Los ejercicios que piden merge commits, `bisect`, `revert -m` o `cherry-pick -x` los validan dentro de la rama del ejercicio antes de integrar el PR.

## Workflows incluidos

- `.github/workflows/validate.yml`
  - Ejecuta tests.
  - Ejecuta `scripts/validate.py`.
  - Usa `fetch-depth: 0` para poder validar historial.
  - Se ejecuta en pushes a `main`, `main-**`, `feature/**`, `hotfix/**`, `chore/**`, `rescue/**`, `refactor/**` y `release/**`, y en PRs contra `main`, `main-**` o `release/**`.

- `.github/workflows/pr-hygiene.yml`
  - Valida naming de rama (`feature/`, `hotfix/`, `refactor/`, `chore/`, `rescue/` o `release/`).
  - Rechaza PRs con más de 8 archivos cambiados.
  - Rechaza carpetas o archivos de soluciones (`solutions/`, `answers/`, `docs/solutions.md`, etc.).
  - Se ejecuta en PRs contra `main`, ramas `main-<username>` o `release/**`.

## Ejercicios

Orden sugerido:

1. [Staging quirúrgico y commits pequeños](exercises/01-staging-y-commits.md)
2. [Ramas y sincronización](exercises/02-ramas-y-sincronizacion.md)
3. [Rebase y conflictos](exercises/03-merge-rebase-conflictos.md)
4. [Historial limpio antes de PR](exercises/04-historial-limpio.md)
5. [Recuperación de errores](exercises/05-recuperacion.md)
6. [Pull Requests y review](exercises/06-pr-review.md)
7. [Simulación integradora de equipo](exercises/07-final-simulacion-equipo.md)
8. [Merge y diagnóstico con bisect](exercises/08-diagnostico-bisect.md)
9. [Mantenimiento avanzado y backports](exercises/09-mantenimiento-avanzado.md)

El ejercicio 7 funciona como integración de los flujos colaborativos principales. Los ejercicios 8 y 9 son módulos avanzados posteriores para diagnóstico y mantenimiento de releases.

## CheatSheet

Ver [`docs/cheatsheet.md`](docs/cheatsheet.md).

## Ramas validadas por el kata

`scripts/validate.py` activa validaciones específicas por nombre de rama. Acepta el nombre base o el mismo nombre con sufijo de usuario. Por ejemplo, `feature/multiply` y `feature/multiply-anapascual` activan la misma validación.

| Rama base | Enunciado | Validación específica |
|---|---|---|
| `feature/multiply` | 01 — Parte A | `multiply`, `test_multiply`, sin `print(` de debug y un commit sobre la base |
| `feature/exponentiation` | 01 — Parte B | `exponentiation`, `test_exponentiation`, sin `print(` de debug y dos commits separados: implementación y test |
| `feature/divide-operation` | 02 — Parte A | `divide`, `test_divide` y resultado esperado para `divide(10, 2)` |
| `feature/modulus-operation` | 02 — Parte B | `divide`, `modulus`, sus tests, resultados esperados y sin merge commits sobre la base |
| `hotfix/division-by-zero` | 03 — Parte A | `divide(10, 0)` lanza explícitamente `ZeroDivisionError` y los tests cubren el caso `zero` |
| `feature/add-cast-int` | 03 — Parte B, Persona A | `add("2", "3")` devuelve `5` y hay test que cubre ese casteo |
| `feature/add-none-validation` | 03 — Parte B, Persona B | `add` conserva el casteo, rechaza `None`, hay test y no hay merge commits sobre la base |
| `feature/clean-history` | 04 — Parte A | existe `docs/usage.md`, no existe `temp.txt` y queda un commit sobre la base |
| `feature/squash-demo` | 04 — Parte B, squash | existe `docs/squash.md` y queda un commit sobre la base |
| `feature/fixup-demo` | 04 — Parte B, fixup/autosquash | existe `docs/api.md` y queda un commit sobre la base |
| `feature/recovery-sandbox` | 05 — Parte A | existen `app/calculator.py` y `docs/recovery.md`; la nota menciona `restore`, `staged` y `clean`; no existe `debug.conf` |
| `rescue/reflog` | 05 — Parte B, reflog | existe `important.txt` y contiene `important` |
| `chore/revert-demo` | 05 — Parte B, revert | no existe `production.txt`, hay al menos dos commits sobre la base y algún mensaje contiene `Revert` |
| `feature/pr-template` | 06 — Parte A | existe `docs/pr-template.md` con los cuatro apartados de PR, un commit sobre la base y máximo 3 archivos cambiados |
| `feature/review-cleanup` | 06 — Parte B | existe `docs/review-workflow.md`, cubre feedback funcional/naming/diseño, menciona pruebas y `range-diff`, no conserva `## Notes`, queda un commit y máximo 3 archivos |
| `feature/tax-calculation` | 07 — Parte A, feature | `calculate_tax`, `test_calculate_tax`, resultado esperado, preserva el hotfix de `subtract` si ya está en la base y no añade merge commits |
| `hotfix/subtract-none-validation` | 07 — Parte A, hotfix | `subtract(None, 3)` lanza `ValueError` y hay test de regresión |
| `refactor/calculator-names` | 07 — Parte B, refactor | `add` y `subtract` usan `left`/`right`, conserva comportamientos acumulados, tests relevantes y no añade merge commits |
| `chore/final-incident` | 07 — Parte B, incidente | existe el tag anotado `v1.0.0-<username>`, no existe `release-blocker.txt`, hay al menos dos commits y algún mensaje contiene `Revert` |
| `hotfix/factorial-regression` | 08 | `factorial` funciona para `0`, `5` y `-1`, hay informe con diagnóstico, al menos cinco commits sobre la base y al menos un merge commit |
| `hotfix/backport-factorial` | 09 — Parte A | `factorial(2.5)` lanza `TypeError`, existen notas de worktree y algún commit contiene la traza de `cherry-pick -x` |
| `chore/revert-merge-demo` | 09 — Parte B | no existe `experimental_discount`, la rama contiene merge commit, revert posterior y `docs/merge-revert.md` explica `merge --no-ff`, `revert -m 1` y el primer padre |

Cada fila acepta el sufijo `-<username>`, por ejemplo `feature/multiply-anapascual`. La rama `hotfix/backport-factorial-<username>` se valida contra `release/v1-<username>`; el resto usa la rama base del PR, `main-<username>` o `main` según el contexto.

Cuando `scripts/validate.py` se ejecuta en una rama `main-<username>` con la forma final de release, también valida el estado acumulado de la calculadora y comprueba que exista el tag anotado `v1.0.0-<username>`. Si detecta que el incidente final ya forma parte de la entrega, también exige `v1.0.1-<username>`.

## Entrega final

- Cada enunciado distingue qué parte se trabaja como demo, práctica guiada, práctica individual o entregable final.
- Cada alumno crea un único issue de entrega al final usando el formulario de GitHub `Entrega Kata Git Colab`.
- En ese issue se indica la rama principal personal, por ejemplo `main-anapascual`.
- Los PRs se trazan filtrando por rama destino, por ejemplo `is:pr base:main-anapascual`.
- El formulario incluye 18 preguntas integradoras orientadas a buenas prácticas de Git, más que a recordar datos concretos de cada ejercicio.
- Las secciones `Preguntas de reflexión` dentro de los ejercicios son para discusión y preparación; no son el cuestionario final de entrega.
- Los issues de GitHub son visibles para las personas con acceso al repositorio. Si las respuestas deben ser privadas o evaluables, recoge el cuestionario por un canal privado y usa el issue solo para identificar la rama de entrega.

## Filosofía

Este repo está diseñado para provocar situaciones reales:

- ramas desactualizadas;
- conflictos;
- commits mal hechos;
- historial sucio;
- recuperación con `reflog`;
- limpieza de archivos sin seguimiento con `clean`;
- PRs pequeños;
- reviews;
- squash/fixup;
- comparación de ramas reescritas con `range-diff`;
- hotfixes;
- tags/releases;
- merge commits;
- diagnóstico con `blame`, `log -S`, `log -G` y `bisect`;
- backports con `cherry-pick`;
- trabajo paralelo con `worktree`.

La teoría debe aparecer solo cuando el ejercicio lo pide.
