# 03 — Merge, rebase y conflictos

## Objetivo

Provocar conflictos controlados y resolverlos.

---

## Ejercicio 3A — Hotfix con conflicto potencial

### Rama esperada

```bash
git switch main
git pull --ff-only
git switch -c hotfix/division-by-zero
```

### Tarea

1. Asegúrate de que existe `divide`.
2. Haz que `divide` gestione explícitamente división por cero.
3. Añade un test cuyo nombre o contenido incluya `zero`.
4. Abre PR contra `main`.

### Validación

```bash
pytest -q
python scripts/validate.py
```

---

## Ejercicio 3B — Conflicto manual

### Parejas

- Persona A modifica `add` para castear inputs a `int`.
- Persona B modifica `add` para validar `None`.

### Tarea

Ambas personas abren PR. Uno entrará primero. El segundo deberá resolver conflicto.

### Comandos esperados

```bash
git fetch origin
git rebase origin/main
git status
git diff
git add app/calculator.py
git rebase --continue
```

### Reto

Abortar y volver a empezar:

```bash
git rebase --abort
```
