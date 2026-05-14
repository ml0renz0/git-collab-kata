# 05 — Recuperación de errores

## Objetivo

Practicar `restore`, `reset`, `reflog` y `revert`.

Estos ejercicios son locales. No necesitan PR.

---

## Ejercicio 5A — Borré un archivo

```bash
rm app/calculator.py
git status
git restore app/calculator.py
```

Comprobar:

```bash
git status
pytest -q
```

---

## Ejercicio 5B — Añadí algo al staging por error

```bash
echo "debug=true" > debug.conf
git add debug.conf
git status
git restore --staged debug.conf
git status
rm debug.conf
```

---

## Ejercicio 5C — Commit equivocado

```bash
echo "bad change" > bad.txt
git add .
git commit -m "Bad commit"
git reset --soft HEAD~1
git status
git reset
rm bad.txt
```

---

## Ejercicio 5D — Recuperar commit perdido

```bash
echo "important" > important.txt
git add .
git commit -m "Important work"
git reset --hard HEAD~1
git reflog
```

Recuperar creando rama de rescate:

```bash
git switch -c rescue/<tu-nombre> <hash-del-commit>
```

---

## Ejercicio 5E — Revert en historial compartido

```bash
git switch main
git pull --ff-only
git switch -c chore/revert-demo
echo "broken" > production.txt
git add .
git commit -m "Add broken production change"
git revert HEAD
```

Debrief:

- `reset` reescribe/mueve historia.
- `revert` crea un commit nuevo que deshace otro.
