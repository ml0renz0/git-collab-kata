# 03 — Merge, rebase y conflictos

## Objetivo

Provocar conflictos controlados y resolverlos.

---

## Ejercicio 3A — Hotfix con conflicto potencial

### Rama esperada

```bash
git switch main                          # cambiar a la rama principal
git pull --ff-only                       # actualizar con fast-forward
git switch -c hotfix/division-by-zero    # crear y cambiar a rama hotfix
```

### Tarea

1. Asegúrate de que existe `divide`.
2. Haz que `divide` gestione explícitamente división por cero.
3. Añade un test cuyo nombre o contenido incluya `zero`.
4. Abre PR contra `main`.

### Validación

```bash
pytest -q                     # ejecutar tests en modo silencioso
python scripts/validate.py    # ejecutar validación local del repositorio
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
git fetch origin             # traer cambios desde el remoto
git rebase origin/main       # rebasar sobre main remoto
git status                   # mostrar estado del repositorio
git diff                     # ver cambios sin stage
git add app/calculator.py    # añadir archivo al stage
git rebase --continue        # continuar el rebase
```

### Reto

Abortar y volver a empezar:

```bash
git rebase --abort    # cancelar el rebase en curso
```