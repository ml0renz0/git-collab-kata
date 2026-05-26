# 07 — Simulación final de equipo

## Objetivo

Simular una semana de trabajo en 60-90 minutos.

---

## Roles

- Persona A: feature funcional.
- Persona B: refactor.
- Persona C: hotfix.
- Persona D: reviewer/maintainer.

---

## Parte 1 — Feature funcional

### Rama esperada

```bash
git switch main                          # cambiar a la rama principal
git pull --ff-only                       # actualizar con fast-forward
git switch -c feature/tax-calculation    # crear y cambiar a rama feature tax-calculation
```

### Tarea

1. Añadir `calculate_tax` en `app/calculator.py`.
2. Añadir tests.
3. Abrir PR.

### Validación

```bash
pytest -q                     # ejecutar tests en modo silencioso
python scripts/validate.py    # ejecutar validación local del repositorio
```

---

## Parte 2 — Refactor conflictivo

### Rama sugerida

```bash
git switch main                            # cambiar a la rama principal
git pull --ff-only                         # actualizar con fast-forward
git switch -c refactor/calculator-names    # crear y cambiar a rama refactor
```

### Tarea

Refactorizar nombres o estructura de `app/calculator.py` sin cambiar comportamiento.

---

## Parte 3 — Hotfix urgente

### Rama sugerida

```bash
git switch main                          # cambiar a la rama principal
git pull --ff-only                       # actualizar con fast-forward
git switch -c hotfix/division-by-zero    # crear y cambiar a rama hotfix
```

### Tarea

Corregir división por cero y abrir PR pequeño.

---

## Parte 4 — Integración

El maintainer decide el orden:

1. Entra hotfix.
2. Feature se actualiza con rebase.
3. Refactor entra después.
4. Se resuelven conflictos.
5. Se crea tag.

```bash
git tag -a v1.0.0 -m "Release v1.0.0"    # crear etiqueta anotada para release
git push origin v1.0.0                   # empujar etiqueta/release al remoto
```

---

## Parte 5 — Incidente

Se descubre que un commit rompió algo.

Tarea:

```bash
git revert <commit>                             # revertir commit especificado
git tag -a v1.0.1 -m "Release hotfix v1.0.1"    # crear etiqueta anotada para hotfix
git push origin v1.0.1                          # empujar etiqueta/release al remoto
```