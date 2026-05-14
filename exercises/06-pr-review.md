# 06 — Pull Requests y review

## Objetivo

Practicar PRs pequeños, feedback y limpieza posterior.

---

## Ejercicio 6A — PR pequeño

### Tarea

1. Crea una rama `feature/<algo-pequeno>`.
2. Cambia máximo 3 archivos.
3. Abre PR contra `main`.
4. Usa esta plantilla en la descripción:

```markdown
## Qué cambia

## Por qué

## Cómo se ha probado

## Riesgos
```

---

## Ejercicio 6B — Review cruzada

### Roles

- Autor.
- Reviewer.
- Maintainer.

### Reviewer debe pedir

1. Un cambio funcional.
2. Un cambio de naming.
3. Una pregunta de diseño.

### Autor debe responder

Con commits incrementales, por ejemplo:

```bash
git commit -m "Address review comments"
```

---

## Ejercicio 6C — Limpiar antes del merge

Antes de mergear:

```bash
git fetch origin
git log --oneline origin/main..HEAD
git rebase -i origin/main
git push --force-with-lease
```

Objetivo:

- Historial revisable.
- Sin commits `wip`.
- Sin commits `Address review comments` si el equipo prefiere squash/fixup.
