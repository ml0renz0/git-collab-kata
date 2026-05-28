# Flujo de review

## Objetivo

Mantener PRs pequeños, con una conversación clara y cambios fáciles de revisar.

## Durante la review

- Separar comentarios funcionales, de naming y de diseño.
- Responder con commits incrementales mientras la conversación está abierta.
- Confirmar que las dudas importantes quedan resueltas antes del merge.

## Criterios de review

- Tratar como feedback funcional cualquier cambio que afecte al comportamiento esperado, la validación o la capacidad de mergear con confianza.
- Tratar como feedback de naming los nombres de secciones, funciones, variables o comandos que dificulten entender la intención.
- Tratar como feedback de diseño las preguntas sobre alcance, responsabilidades o reglas de decisión del equipo.
- Evitar mezclar decisiones de producto con correcciones mecánicas.
- Pedir una segunda mirada cuando una decisión cambie el alcance del PR.

## Antes de pedir merge

- Ejecutar `pytest -q`.
- Ejecutar `python scripts/validate.py`.
- Revisar que el diff del PR atiende los comentarios funcionales y de naming.

## Respuesta de diseño

Bloquean el merge los comentarios que detectan fallos funcionales, validaciones ausentes, riesgos de seguridad o decisiones de alcance sin cerrar. Las preguntas de diseño que solo buscan contexto pueden resolverse en la conversación del PR, siempre que la respuesta quede clara y no cambie el comportamiento esperado.
