# Git Collaboration Kata

Repositorio para impartir un curso práctico de Git colaborativo avanzado.

La idea es que los ejercicios no publiquen soluciones paso a paso. Los alumnos trabajan en ramas con nombres concretos y la validación comprueba el resultado observable: tests, forma de la rama, historial, ausencia de secretos y algunos criterios específicos del ejercicio.

## Requisitos

- Git 2.40+ recomendado.
- Python 3.11+ o 3.12.
- Cuenta en GitHub, GitLab o equivalente si quieres usar pull requests reales.
- Para GitHub Actions, sube este repo a GitHub y activa Actions.

## Instalación local

```bash
git clone <url-del-repo>
cd git-collab-kata
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
pytest -q
python scripts/validate.py
```

## Cómo usarlo en clase

1. El instructor crea el repositorio remoto.
2. Cada alumno clona el repo.
3. Cada alumno crea su rama principal de trabajo, por ejemplo `main-anapascual`.
4. Cada ejercicio indica una rama esperada, normalmente con sufijo de usuario, por ejemplo `feature/multiply-anapascual`.
5. El alumno hace cambios, commits y abre PR contra su rama `main-<username>`.
6. Los workflows y `scripts/validate.py` validan el resultado observable.
7. Si falla, el alumno debe leer el error y corregir su rama.

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

## Workflows incluidos

- `.github/workflows/validate.yml`
  - Ejecuta tests.
  - Ejecuta `scripts/validate.py`.
  - Usa `fetch-depth: 0` para poder validar historial.
  - Se ejecuta en pushes a `main`, `main-**`, `feature/**`, `hotfix/**`, `chore/**`, `rescue/**` y `refactor/**`, y en PRs contra `main` o `main-**`.

- `.github/workflows/pr-hygiene.yml`
  - Valida naming de rama (`feature/`, `hotfix/`, `refactor/`, `chore/` o `rescue/`).
  - Rechaza PRs demasiado grandes para el kata.
  - Rechaza carpetas `solutions/` o `answers/`.
  - Se ejecuta en PRs contra `main` o ramas `main-<username>`.

## Ejercicios

Orden sugerido:

1. [`exercises/01-staging-y-commits.md`](exercises/01-staging-y-commits.md)
2. [`exercises/02-ramas-y-sincronizacion.md`](exercises/02-ramas-y-sincronizacion.md)
3. [`exercises/03-merge-rebase-conflictos.md`](exercises/03-merge-rebase-conflictos.md)
4. [`exercises/04-historial-limpio.md`](exercises/04-historial-limpio.md)
5. [`exercises/05-recuperacion.md`](exercises/05-recuperacion.md)
6. [`exercises/06-pr-review.md`](exercises/06-pr-review.md)
7. [`exercises/07-final-simulacion-equipo.md`](exercises/07-final-simulacion-equipo.md)

## Chuleta rápida

Ver [`docs/cheatsheet.md`](docs/cheatsheet.md).

## Convención de ramas del kata

`scripts/validate.py` acepta el nombre base o el mismo nombre con sufijo de usuario. Por ejemplo, `feature/multiply` y `feature/multiply-anapascual` activan la misma validación.

| Ejercicio | Rama esperada | Validación específica |
|---|---|---|
| 1A Staging parcial | `feature/multiply-<username>` | Existe `multiply`, hay `test_multiply`, no hay `print` de debug |
| 1B Fix mezclado con commit original | `feature/exponentiation-<username>` | Existe `exponentiation`, hay `test_exponentiation`, no hay `print` de debug |
| 2A Rama básica con upstream | `feature/divide-operation-<username>` | Existe `divide`, hay `test_divide` |
| 2B Rama desactualizada con conflicto | `feature/modulus-operation-<username>` | Existen `divide` y `modulus`, hay `test_divide` y `test_modulus` |
| 3A Hotfix | `hotfix/division-by-zero-<username>` | `divide` lanza `ZeroDivisionError`, hay test con referencia a `zero` |
| 3B Conflicto Persona A | `feature/add-cast-int-<username>` | `add("2", "3")` devuelve `5`, hay test |
| 3B Conflicto Persona B | `feature/add-none-validation-<username>` | `add` rechaza `None`, conserva casteo a `int`, hay test |
| 4A Historial limpio demo | `feature/clean-history-<username>` | Un solo commit sobre `main-<username>`, existe `docs/usage.md`, no existe `temp.txt` |
| 4B Squash entregable | `feature/squash-demo-<username>` | Un solo commit sobre `main-<username>`, existe `docs/squash.md` |
| 4B Fixup/autosquash entregable | `feature/fixup-demo-<username>` | Un solo commit sobre `main-<username>`, existe `docs/api.md` |
| 5A Recuperación sandbox | `feature/recovery-sandbox-<username>` | Existe `docs/recovery.md`, conserva `app/calculator.py`, no existe `debug.conf` |
| 5B Reflog entregable | `rescue/reflog-<username>` | Existe `important.txt` con contenido recuperado |
| 5B Revert entregable | `chore/revert-demo-<username>` | No existe `production.txt`, hay commit de revert |
| Simulación final | `feature/tax-calculation` | Existe `calculate_tax`, hay test |

## Entrega final

- Para cada ejercicio, la kata tiene una parte de demo para la presentación y una parte de entrega para completar después.
- Cada alumno crea un único issue de entrega al final usando el formulario de GitHub `Entrega Kata Git Colab`.
- En ese issue se indica la rama principal personal, por ejemplo `main-anapascual`.
- Los PRs se trazan filtrando por rama destino, por ejemplo `is:pr base:main-anapascual`.
- El formulario incluye preguntas tipo test basadas en cada ejercicio y un campo para el aprendizaje clave.
- Los issues de GitHub son visibles para las personas con acceso al repositorio. Si las respuestas deben ser privadas o evaluables, recoge el cuestionario por un canal privado y usa el issue solo para identificar la rama de entrega.

## Filosofía

Este repo está diseñado para provocar situaciones reales:

- ramas desactualizadas;
- conflictos;
- commits mal hechos;
- historial sucio;
- recuperación con `reflog`;
- PRs pequeños;
- reviews;
- squash/fixup;
- hotfixes;
- tags/releases.

La teoría debe aparecer solo cuando el ejercicio lo pide.
