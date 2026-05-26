# 04 — Historial limpio antes de PR

## Objetivo

Practicar `rebase -i`, squash, fixup y autosquash.

---

## Ejercicio 4A — Limpiar commits basura

### Rama esperada

```bash
git switch main                        # cambiar a la rama principal
git pull --ff-only                     # actualizar con fast-forward
git switch -c feature/clean-history    # crear y cambiar a rama feature clean-history
```

### Tarea

1. Crea un archivo temporal `temp.txt` y commitéalo con mensaje malo, por ejemplo `wip`.
2. Crea `docs/usage.md` con documentación útil y commitéalo con mensaje malo, por ejemplo `stuff`.
3. Borra `temp.txt` y commitéalo.
4. Limpia la rama con `git rebase -i` para que al final quede **un solo commit útil** sobre `main`.

### Resultado esperado observable

- Existe `docs/usage.md`.
- No existe `temp.txt`.
- La rama tiene un solo commit sobre `main`.
- No hay mensajes `wip`, `stuff`, `tmp`, `temp`.

### Validación

```bash
python scripts/validate.py    # ejecutar validación local del repositorio
```

---

## Ejercicio 4B — Squash

### Rama esperada

```bash
git switch main                      # cambiar a la rama principal
git pull --ff-only                   # actualizar con fast-forward
git switch -c feature/squash-demo    # crear y cambiar a rama feature squash
```

### Tarea

1. Crea `docs/squash.md` en tres commits pequeños.
2. Usa `git rebase -i` para dejar un solo commit final.

### Validación

```bash
python scripts/validate.py    # ejecutar validación local del repositorio
```

---

## Ejercicio 4C — Fixup/autosquash

### Rama esperada

```bash
git switch main                     # cambiar a la rama principal
git pull --ff-only                  # actualizar con fast-forward
git switch -c feature/fixup-demo    # crear y cambiar a rama feature fixup
```

### Tarea

1. Crea `docs/api.md` con un commit principal.
2. Haz uno o varios commits `--fixup` contra ese commit.
3. Ejecuta autosquash.

```bash
git commit --fixup <hash>                 # crear commit fixup para autosquash
git rebase -i --autosquash origin/main    # rebasar aplicando autosquash
```

### Validación

```bash
python scripts/validate.py    # ejecutar validación local del repositorio
```