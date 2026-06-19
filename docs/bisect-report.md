# Diagnostico de la regresion de factorial

## Comando de reproduccion

`pytest -q` reproducia el fallo: `factorial(0)` devolvia `0` en lugar de
`1`, mientras que `factorial(5)` y el rechazo de `factorial(-1)` seguian
funcionando.

## Investigacion previa

`git blame app/calculator.py` mostro que las lineas del caso cero procedian
del commit `5e7c878`. `git log -S "factorial" -- app/calculator.py tests` y
`git log -G "factorial\\(" -- app/calculator.py tests` localizaron la
introduccion de la funcion y sus tests, aunque no demostraron por si solos
que el cambio interno del caso cero fuera la causa.

## Commit culpable

`git bisect run pytest -q`, con `6d9512a` como bueno y la punta con fallo
como mala, identifico `5e7c878` (`refactor: simplify factorial loop`) como
el primer commit culpable de que `factorial(0)` devolviera `0`.

## Decision

La rama contiene un merge compartido, asi que se aplica un fix forward en
lugar de reescribir o borrar el commit culpable. El hotfix restaura
`factorial(0)` a `1` y conserva el historial para futuras revisiones.
