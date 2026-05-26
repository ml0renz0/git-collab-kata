# 05 — Recuperación de errores

## Objetivo

Practicar `restore`, `reset`, `reflog` y `revert`.

Estos ejercicios son locales. No necesitan PR.

---

## Ejercicio 5A — Borré un archivo

```bash
rm app/calculator.py             # eliminar archivo de código
git status                       # mostrar estado del repositorio
git restore app/calculator.py    # restaurar archivo modificado
```

Comprobar:

```bash
git status    # mostrar estado del repositorio
pytest -q     # ejecutar tests en modo silencioso
```

---

## Ejercicio 5B — Añadí algo al staging por error

```bash
echo "debug=true" > debug.conf     # crear archivo de configuración de debug
git add debug.conf                 # añadir archivo de debug al stage
git status                         # mostrar estado del repositorio
git restore --staged debug.conf    # quitar debug.conf del stage
git status                         # mostrar estado del repositorio
rm debug.conf                      # eliminar archivo de configuración de debug
```

---

## Ejercicio 5C — Commit equivocado

```bash
echo "bad change" > bad.txt    # crear un cambio malo de ejemplo
git add .                      # añadir todos los cambios al stage
git commit -m "Bad commit"     # crear commit con mensaje
git reset --soft HEAD~1        # deshacer último commit manteniendo cambios
git status                     # mostrar estado del repositorio
git reset                      # resetear el estado del repositorio
rm bad.txt                     # eliminar archivo malo
```

---

## Ejercicio 5D — Recuperar commit perdido

```bash
echo "important" > important.txt    # crear un cambio importante de ejemplo
git add .                           # añadir todos los cambios al stage
git commit -m "Important work"      # crear commit con mensaje
git reset --hard HEAD~1             # deshacer commits y cambios en el árbol de trabajo
git reflog                          # ver historial de referencias
```

Recuperar creando rama de rescate:

```bash
git switch -c rescue/<tu-nombre> <hash-del-commit>    # crear y cambiar a rama de rescate
```

---

## Ejercicio 5E — Revert en historial compartido

```bash
git switch main                                 # cambiar a la rama principal
git pull --ff-only                              # actualizar con fast-forward
git switch -c chore/revert-demo                 # crear y cambiar a rama de revert
echo "broken" > production.txt                  # crear un cambio roto de ejemplo
git add .                                       # añadir todos los cambios al stage
git commit -m "Add broken production change"    # crear commit con mensaje
git revert HEAD                                 # revertir el último commit
```

Debrief:

- `reset` reescribe/mueve historia.
- `revert` crea un commit nuevo que deshace otro.