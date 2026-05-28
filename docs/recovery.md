# Recovery notes

Hoy he probado una recuperacion basica de Git: si borro un archivo por error,
`git restore` me permite devolverlo desde el ultimo commit confirmado.

Tambien he visto que un archivo puede estar en el area staged sin que yo quiera
commitearlo. En ese caso `git restore --staged` lo saca del stage, pero no lo
borra del arbol de trabajo; luego ya puedo decidir si lo elimino o lo arreglo.
