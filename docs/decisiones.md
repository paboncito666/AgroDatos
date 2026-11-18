# Registro de decisiones técnicas (ADR breve)

Cada decisión importante se registra aquí y se enlaza desde el issue o PR correspondiente.

## D-001 — Dos granularidades de procesos para el conteo de primos
- **Fecha:** 2026-11-18 · **Autor(es):** Integrante C · **Issue/PR:** —
- **Contexto:** El conteo de primos es trabajo intensivo de CPU y la línea base solo ocupa un proceso.
- **Opciones consideradas:** 1) hilos; 2) un proceso por lote; 3) un proceso por grupo de lotes.
- **Decisión:** Comparar A (secuencial) con B (una tarea por lote) y C (una tarea por grupo), limitando a ocho procesos.
- **Justificación (incluya evidencia o principio físico):** En CPython los hilos no ejecutan bytecode de CPU en paralelo por el GIL. Los procesos permiten ocupar varios núcleos, pero el envío de tareas, la serialización y la sincronización consumen ciclos y tiempo. B favorece el balance de carga; C reduce esas operaciones de coordinación.
- **Consecuencias / riesgos:** No se debe asumir aceleración ideal de 8x (Ley de Amdahl). El máximo se refiere a procesos y puede no coincidir con núcleos físicos; se debe registrar el entorno y reportar esta limitación.
