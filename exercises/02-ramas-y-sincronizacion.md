# 02 — Ramas y sincronización

## Objetivo

Practicar creación de ramas, upstream, `fetch`, `pull --ff-only` y actualización desde `main`.

---

## Ejercicio 2A — Feature branch básica

### Rama esperada

```bash
git switch main
git pull --ff-only
git switch -c feature/divide-operation
```

### Tarea

1. Añade una función `divide` en `app/calculator.py`.
2. Añade un test para `divide`.
3. Sube la rama configurando upstream.

```bash
git push -u origin feature/divide-operation
```

### Comprobaciones

```bash
git branch -vv
pytest -q
python scripts/validate.py
```

---

## Ejercicio 2B — Rama desactualizada

### Escenario

Mientras trabajas, `main` avanza.

### Tarea para el instructor

Mergea un cambio pequeño en `main`, por ejemplo documentación en `README.md`.

### Tarea para el alumno

Actualizar su rama sin crear un merge commit innecesario:

```bash
git fetch origin
git rebase origin/main
```

### Comprobación

```bash
git log --oneline --graph --decorate --all
```
