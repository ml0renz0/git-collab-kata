# 01 — Staging quirúrgico y commits pequeños

## Objetivo

Practicar `git add -p`, commits pequeños y `commit --amend`.

---

## Ejercicio 1A — Separar cambios mezclados

### Rama esperada

```bash
git switch main                             # cambiar a la rama principal
git pull --ff-only                          # actualizar rama principal con fast-forward
git switch -c feature/multiply-operation    # crear y cambiar a nueva rama
```

### Escenario

Has tocado `app/calculator.py` para añadir una operación nueva, pero también metiste una traza de debug que no debería commitearse.

### Tarea

1. Añade una función `multiply` en `app/calculator.py`.
2. Añade temporalmente un `print` de debug dentro de `add`.
3. Usa `git add -p` para commitear solo la función nueva.
4. Descarta el debug antes de subir.
5. Añade un test para `multiply`.
6. Si el test se te olvidó en el primer commit, usa `git commit --amend`.

### Comandos obligatorios

```bash
git diff                               # ver cambios sin stage
git add -p                             # añadir cambios interactivos por partes
git diff --staged                      # ver los cambios que ya están staged
git commit --amend                     # modificar el último commit
```

### Validación local

```bash
pytest -q                              # ejecutar tests en modo silencioso
python scripts/validate.py             # ejecutar validación local del repositorio
```

### Validación en GitHub

Abre PR contra `main`. El workflow debe pasar.