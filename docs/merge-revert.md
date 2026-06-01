# Notas de revert de merge

Use `git merge --no-ff` para que la rama temporal quedara como un merge commit
visible en el historial. Esto hace mas facil revertir toda la prueba como una
unidad, aunque el commit de la rama siga existiendo.

Despues use `git revert -m 1` sobre el merge. El `1` indica el primer padre, es
decir, la linea principal que quiero conservar. Git calcula el cambio que trajo
el otro padre y crea un commit nuevo que lo deshace sin reescribir historia
compartida.
