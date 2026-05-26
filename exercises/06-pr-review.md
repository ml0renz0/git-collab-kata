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
git commit -m "Address review comments"    # crear commit con mensaje
```

---

## Ejercicio 6C — Limpiar antes del merge

Antes de mergear:

```bash
git fetch origin                       # traer cambios desde el remoto
git log --oneline origin/main..HEAD    # ver commits locales no en main
git rebase -i origin/main              # editar commits antes de rebasar sobre main remoto
git push --force-with-lease            # empujar forzando de forma segura
```

Objetivo:

- Historial revisable.
- Sin commits `wip`.
- Sin commits `Address review comments` si el equipo prefiere squash/fixup.