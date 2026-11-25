# Paso 5 — Contraste de hipótesis

## Revisión de registro

Se ejecutó `python herramientas\verificar_hipotesis.py docs\hipotesis.md`. El verificador devuelve **NO EVALUABLE** (código 2): H1, H2 y H3 están vacías. La plantilla no contiene una predicción cuantitativa registrada antes de observar los resultados. El script de clase `verificar_hipotesis.py` no se encontró en los archivos accesibles; el verificador local comprueba y reporta explícitamente este estado, pero no se presenta como el original del curso.

## Árbol de decisión aplicado

1. **¿Existe una hipótesis completa y previa a la medición?** No: las tres filas H1–H3 siguen vacías. Se detiene el contraste formal; los resultados no pueden confirmar ni refutar una predicción retrospectiva.
2. **¿La variable independiente del experimento coincide con la hipótesis a evaluar?** El CSV solo mide estrategia A y varía `n`. No varía el número de procesos `k` ni compara A/B/C.
3. **¿Qué conclusión permite la evidencia?** Solo una descripción exploratoria: el tiempo de A crece entre los tres tamaños medidos. No se puede evaluar la expectativa gerencial de dividir el tiempo por ocho al usar ocho núcleos, ni concluir sobre paralelismo o eficiencia.

El árbol visual de decisión de la clase no estaba disponible como archivo legible en el repositorio/material accesible. Se deja explícito el recorrido aplicable y la rama terminal “sin hipótesis previa/no evaluable”, en lugar de atribuir al material una regla no verificada.

## Acción para una próxima medición

Antes de ejecutar estrategias nuevas, registrar H1–H3 con variable independiente, magnitud/unidad, predicción cuantitativa, mecanismo y criterio de refutación; después ejecutar al menos A y las estrategias alternativas con los mismos valores de `n`, equipo y protocolo. La hipótesis de “tiempo dividido por 8” solo se podrá contrastar con mediciones comparables que varíen `k`; el número de núcleos lógicos no equivale por sí solo a escalamiento lineal.
