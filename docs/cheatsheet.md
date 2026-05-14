# Chuleta Git para el kata

## Estado e historial

```bash
git status
git log --oneline --graph --decorate --all
git show HEAD
git diff
git diff --staged
```

## Commits pequeños

```bash
git add -p
git commit -m "Mensaje claro"
git commit --amend
```

## Ramas

```bash
git switch main
git switch -c feature/nombre
git branch -vv
```

## Remotos

```bash
git fetch origin
git pull --ff-only
git push -u origin feature/nombre
```

## Rebase y merge

```bash
git rebase origin/main
git rebase --continue
git rebase --abort

git merge main
git merge --abort
```

## Recuperación

```bash
git restore archivo
git restore --staged archivo
git reset --soft HEAD~1
git reflog
git revert <commit>
```

## Limpieza de historial

```bash
git rebase -i HEAD~3
git commit --fixup <commit>
git rebase -i --autosquash origin/main
git push --force-with-lease
```

## Stash

```bash
git stash push -u -m "mensaje"
git stash list
git stash pop
```

## Diagnóstico

```bash
git blame archivo
git log -S "texto"
git bisect start
```
