# Chuleta Git para el kata

## Variables del kata

```bash
USER_ID="<username>"          # identificador personal, por ejemplo anapascual
MAIN="main-${USER_ID}"        # rama principal personal del participante
```

Crear la rama principal personal:

```bash
git switch main               # cambiar a la rama base del repositorio
git pull --ff-only            # actualizar main sin crear merge commits
git switch -c "$MAIN"         # crear la rama principal personal
git push -u origin "$MAIN"    # subirla y configurar upstream
```

## Estado e historial

```bash
git status                                    # mostrar estado del repositorio
git log --oneline --graph --decorate --all    # ver historial compacto con decoraciones
git log --oneline "$MAIN"..HEAD               # ver commits de la rama actual sobre tu main
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
git switch "$MAIN"                         # cambiar a tu rama principal
git pull --ff-only                         # actualizar tu rama principal
git switch -c feature/nombre-"$USER_ID"    # crear y cambiar a rama feature
git branch -vv                             # mostrar ramas y su upstream
```

## Remotos

```bash
git fetch origin                       # traer cambios desde el remoto sin modificar tu rama
git pull --ff-only                     # actualizar con fast-forward
git push -u origin "$FEATURE"          # empujar rama y configurar upstream
git push --force-with-lease            # actualizar remoto tras rebase de forma segura
```

## Rebase y merge

```bash
git rebase "origin/$MAIN"    # rebasar sobre tu main remoto
git rebase "$MAIN"           # rebasar sobre tu main local
git rebase --continue        # continuar el rebase
git rebase --abort           # cancelar el rebase en curso

git merge "$MAIN"            # fusionar tu main en la rama actual
git merge --abort            # cancelar el merge en curso
```

## Recuperación

```bash
git restore archivo             # restaurar el archivo modificado
git restore --staged archivo    # quitar archivo del stage
git reset --soft HEAD~1         # deshacer último commit manteniendo cambios
git reset --hard HEAD~1         # mover HEAD atrás descartando cambios del árbol de trabajo
git reflog                      # ver historial de referencias
git switch -c rescue/nombre <hash> # crear una rama desde un commit recuperado
git revert <commit>             # revertir commit especificado
```

## Limpieza de historial

```bash
git rebase -i HEAD~3                   # editar los últimos 3 commits
git rebase -i "$MAIN"                  # limpiar commits de la rama actual sobre tu main
git commit --fixup <commit>            # crear commit fixup para autosquash
git rebase -i --autosquash "$MAIN"     # rebasar aplicando autosquash
git push --force-with-lease            # empujar forzando de forma segura
```

## Stash

```bash
git stash push -u -m "mensaje"    # guardar cambios locales en stash
git stash apply                   # aplicar el último stash sin eliminarlo del stash
git stash list                    # listar los stashes
git stash pop                     # recuperar el último stash
git stash drop                    # eliminar el último stash
```

## Validación y PRs

```bash
pytest -q                    # ejecutar tests
python scripts/validate.py    # ejecutar validación del kata
git push -u origin "$FEATURE" # subir una rama nueva
```

Cada PR se abre desde la rama del ejercicio contra `$MAIN`, no contra `main`.
Al final del kata, el formulario de entrega se crea como issue e indica la rama `$MAIN`.
Los PRs se pueden trazar filtrando por rama destino, por ejemplo `is:pr base:main-anapascual`.

## Diagnóstico

```bash
git blame archivo     # mostrar autoría de cada línea
git log -S "texto"    # buscar commits que contienen texto
git bisect start      # iniciar búsqueda binaria de commit defectuoso
```
