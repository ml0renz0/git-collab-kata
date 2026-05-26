# Chuleta Git para el kata

## Estado e historial

```bash
git status                                    # mostrar estado del repositorio
git log --oneline --graph --decorate --all    # ver historial compacto con decoraciones
git show HEAD                                 # mostrar el último commit
git diff                                      # ver cambios sin stage
git diff --staged                             # ver los cambios staged
```

## Commits pequeños

```bash
git add -p                       # añadir cambios interactivamente por partes
git commit -m "Mensaje claro"    # crear commit con mensaje claro
git commit --amend               # modificar el último commit
```

## Ramas

```bash
git switch main                 # cambiar a la rama principal
git switch -c feature/nombre    # crear y cambiar a rama feature
git branch -vv                  # mostrar ramas y su upstream
```

## Remotos

```bash
git fetch origin                     # traer cambios desde el remoto
git pull --ff-only                   # actualizar con fast-forward
git push -u origin feature/nombre    # empujar rama y configurar upstream
```

## Rebase y merge

```bash
git rebase origin/main    # rebasar sobre main remoto
git rebase --continue     # continuar el rebase
git rebase --abort        # cancelar el rebase en curso

git merge main            # fusionar main en la rama actual
git merge --abort         # cancelar el merge en curso
```

## Recuperación

```bash
git restore archivo             # restaurar el archivo modificado
git restore --staged archivo    # quitar archivo del stage
git reset --soft HEAD~1         # deshacer último commit manteniendo cambios
git reflog                      # ver historial de referencias
git revert <commit>             # revertir commit especificado
```

## Limpieza de historial

```bash
git rebase -i HEAD~3                      # editar los últimos 3 commits
git commit --fixup <commit>               # crear commit fixup para autosquash
git rebase -i --autosquash origin/main    # rebasar aplicando autosquash
git push --force-with-lease               # empujar forzando de forma segura
```

## Stash

```bash
git stash push -u -m "mensaje"    # guardar cambios locales en stash
git stash list                    # listar los stashes
git stash pop                     # recuperar el último stash
```

## Diagnóstico

```bash
git blame archivo     # mostrar autoría de cada línea
git log -S "texto"    # buscar commits que contienen texto
git bisect start      # iniciar búsqueda binaria de commit defectuoso
```