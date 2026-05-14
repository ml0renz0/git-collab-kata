# Git Collaboration Kata

Repositorio para impartir un curso práctico de Git colaborativo avanzado.

La idea es que el repo **no contiene soluciones**. Los alumnos trabajan en ramas con nombres concretos y GitHub Actions valida el resultado observable: tests, forma de la rama, historial, ausencia de secretos y algunos criterios específicos del ejercicio.

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
3. Cada ejercicio indica una rama esperada, por ejemplo `feature/multiply-operation`.
4. El alumno hace cambios, commits y abre PR contra `main`.
5. Los workflows validan el resultado.
6. Si falla, el alumno debe leer el error y corregir su rama.

## Workflows incluidos

- `.github/workflows/validate.yml`
  - Ejecuta tests.
  - Ejecuta `scripts/validate.py`.
  - Usa `fetch-depth: 0` para poder validar historial.

- `.github/workflows/pr-hygiene.yml`
  - Valida naming de rama.
  - Rechaza PRs demasiado grandes para el kata.
  - Rechaza carpetas `solutions/` o `answers/`.

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

| Ejercicio | Rama esperada | Validación específica |
|---|---|---|
| Staging parcial | `feature/multiply-operation` | Existe `multiply`, hay test, no hay `print` de debug |
| Rama básica | `feature/divide-operation` | Existe `divide`, hay test |
| Hotfix | `hotfix/division-by-zero` | `divide` gestiona división por cero, hay test |
| Historial limpio | `feature/clean-history` | Un solo commit sobre `main`, existe `docs/usage.md`, no existe `temp.txt` |
| Squash | `feature/squash-demo` | Un solo commit sobre `main`, existe `docs/squash.md` |
| Fixup/autosquash | `feature/fixup-demo` | Un solo commit sobre `main`, existe `docs/api.md` |
| Simulación final | `feature/tax-calculation` | Existe `calculate_tax`, hay test |

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
