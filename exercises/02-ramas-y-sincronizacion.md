# 02 — Ramas y sincronización

## Objetivo

Practicar creación de ramas, upstream, `fetch`, `pull --ff-only` y actualización desde `main`.

---

## Ejercicio 2A — Feature branch básica

### Rama esperada

```bash
git switch main                           # cambiar a la rama principal
git pull --ff-only                        # actualizar con fast-forward
git switch -c feature/divide-operation    # crear y cambiar a rama feature divide
```

### Tarea

1. Añade una función `divide` en `app/calculator.py`.
2. Añade un test para `divide`.
3. Sube la rama configurando upstream.

```bash
git push -u origin feature/divide-operation    # empujar rama y configurar upstream
```

### Comprobaciones

```bash
git branch -vv                # mostrar ramas y su upstream
pytest -q                     # ejecutar tests en modo silencioso
python scripts/validate.py    # ejecutar validación local del repositorio
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
git fetch origin          # traer cambios desde el remoto
git rebase origin/main    # rebasar sobre main remoto
```

### Comprobación

```bash
git log --oneline --graph --decorate --all    # ver historial compacto con decoraciones
```