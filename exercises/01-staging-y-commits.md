# 01 — Staging quirúrgico y commits pequeños

## Objetivo

Practicar `git add -p`, commits pequeños y `commit --amend`.

---

## Ejercicio 1A — Separar cambios mezclados

### Rama esperada

```bash
git switch main
git pull --ff-only
git switch -c feature/multiply-operation
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
git diff
git add -p
git diff --staged
git commit --amend
```

### Validación local

```bash
pytest -q
python scripts/validate.py
```

### Validación en GitHub

Abre PR contra `main`. El workflow debe pasar.
