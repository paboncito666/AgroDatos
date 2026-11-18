# Registro de decisiones técnicas (ADR breve)

Cada decisión importante se registra aquí y se enlaza desde el issue o PR correspondiente.

## D-001 — Separar la preparación de la medición de A

- **Fecha:** 2026-11-18 · **Autor:** integrante responsable por confirmar; edición asistida por IA · **Issue/PR:** trabajo en rama `pabon`, PR pendiente de revisión.
- **Contexto:** El comando de línea base iniciaba el cronómetro antes de llamar `preparar(1_000_000)`. Eso mezclaba la generación de lotes con el conteo de primos, pese a que el protocolo compara solo la ejecución.
- **Opciones consideradas:** 1) conservar el tiempo total de preparación y conteo; 2) preparar los lotes antes de iniciar el cronómetro.
- **Decisión:** medir únicamente `ejecutar(lotes)` y descartar la primera medición de 2,52 s como evidencia de tiempo de ejecución.
- **Justificación:** la guía exige separar `preparar(n)` de `ejecutar(datos)` para evitar una fuente de sesgo sistemático; la API de A ya ofrece esa separación.
- **Consecuencias / riesgos:** la nueva evidencia es reproducible como tiempo del núcleo de trabajo, pero no representa el tiempo de extremo a extremo. La ejecución inicial corregida dio 2,43 s y una verificación posterior 2,18 s, ambas para `n = 1 000 000`; son corridas individuales y no se mezclan con las diez repeticiones formales.
