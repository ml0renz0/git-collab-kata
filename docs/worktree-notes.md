# Notas de worktree y backport

Para la release use `git worktree add` porque me deja tener una carpeta separada
con `release/v1-codexfodex` sin abandonar el checkout principal. Despues conviene
mirar `git worktree list` para no perder de vista que carpetas estan vivas.

El arreglo de `factorial` no lo mezcle entero desde `main-codexfodex`; solo traje
el commit concreto con `git cherry-pick -x`, asi queda escrito de donde salio el
backport. Al terminar, `git worktree remove` sirve para limpiar la carpeta
auxiliar y no dejar estados duplicados por ahi.
