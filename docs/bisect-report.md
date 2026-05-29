# Informe bisect factorial

## Comando de reproducción

Ejecuté `pytest -q` en la rama `hotfix/factorial-regression-codexfodex`.
La regresión aparece en `factorial(0)`: el test esperaba `1`, pero la función
devolvía `0`.

Para diagnosticarlo usé:

```bash
git bisect start
git bisect bad
git bisect good 0e2eddbab462121bdf9d1215a6968152f564021a
git bisect run pytest -q
git bisect reset
```

## Commit culpable

`git bisect` identificó como primer commit malo:

```text
d24789f966fe2f351c89fe8003b4f0d6d1410257 refactor: simplify factorial loop
```

El cambio parecía pequeño, pero añadió un caso especial incorrecto para
`factorial(0)`.

## Decisión

Como el commit roto ya forma parte de una rama compartida, decidí hacer fix
forward en vez de reescribir la historia. El arreglo elimina el caso especial
incorrecto y deja que el acumulador inicial `1` cubra `factorial(0)`, mientras
los tests mantienen cubiertos `factorial(0)`, `factorial(5)` y `factorial(-1)`.

## Preguntas

- Marcar un commit como `good` significa que en ese punto el fallo no se
  reproduce; marcarlo como `bad` significa que el fallo sí aparece. Git usa esas
  dos señales para partir el historial y buscar el primer commit malo.
- El commit normal de `factorial` tiene un solo padre y añade código/tests. El
  merge commit de documentación tiene dos padres y registra que una rama auxiliar
  se integró, aunque su contenido sea solo documentación.
- `git merge --no-ff "$DOCS_FACTORIAL"` fuerza un commit de merge aunque Git
  pudiera avanzar por fast-forward, así queda visible que hubo una rama de trabajo
  separada.
- `git bisect run` evita ir commit por commit a mano: ejecuta el comando de test,
  interpreta el código de salida y avanza solo.
- `git bisect reset` es necesario para volver a la rama normal; si no, me quedo
  en un commit intermedio con el repositorio en modo bisect.
- Si el commit roto ya está compartido, fix forward conserva la historia que otras
  personas ya pueden tener y añade un arreglo auditable.
- Un informe mínimo debe incluir cómo reproducir el fallo, qué commit lo introdujo,
  qué evidencia dio `git bisect`, qué decisión se tomó y cómo se comprobó el fix.
