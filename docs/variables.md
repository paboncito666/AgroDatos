# Variables experimentales — Estrategia A

| Tipo | Variable | Símbolo | Unidad | Valores / rango | Instrumento o forma de obtención | Justificación |
|---|---|---|---|---|---|---|
| Independiente | Tamaño del límite exclusivo | n | enteros | 300 000; 1 000 000; 2 000 000 | Parámetro de `preparar(n)` | Cambia la cantidad de candidatos evaluados |
| Dependiente | Tiempo de ejecución | t | s | 10 repeticiones por n | `time.perf_counter()` alrededor de `ejecutar(lotes)` | Magnitud primaria de rendimiento |
| Dependiente | Tiempo de CPU del proceso | t_CPU | s | 10 repeticiones por n | `time.process_time()` | Diagnóstico de trabajo CPU frente a espera |
| Dependiente | Uso de CPU del proceso | U | % | `100 × t_CPU / t` | Derivado por el arnés | No equivale a potencia eléctrica |
| Dependiente | Pico de memoria Python | M | MiB | Una corrida separada por n | `tracemalloc` | Separa memoria del tiempo por el sobrecosto del instrumento |
| Dependiente (opcional) | Frecuencia | f | MHz | No disponible | Sensor del sistema | No medida en este entorno |
| Dependiente (opcional) | Temperatura | θ | °C | No disponible | Sensor del sistema | No medida en este entorno |
| Dependiente (opcional) | Energía | E | J | No disponible | RAPL / vatímetro | Energía no medida |
| Controlada | Equipo y procesador | — | — | Ryzen 5 PRO 2400G; 4 físicos / 8 lógicos | Diagnóstico del entorno | Se compara en un mismo equipo |
| Controlada | Python | — | — | CPython 3.14.8 | `platform` | Evita diferencias de versión |
| Controlada | Alimentación y perfil | — | — | Corriente; Equilibrado | Estado AC de Windows y `powercfg` | Reduce cambios de frecuencia por perfil o batería |
| Controlada | Regla de entrada y tamaño de lote | — | — | Enteros consecutivos `[2,n)`; lotes de 50 000 | `preparar(n)` determinista | Mantiene igual método de generación y granularidad para cada n |

## Mapa de dependencias

`n → cantidad de candidatos → evaluaciones de primalidad → tiempo t y tiempo de CPU t_CPU`

La estrategia A usa un solo proceso; no se evalúa aceleración paralela en esta entrega.

## Variables no controladas y mitigación

| Variable no controlada | Efecto posible | Mitigación |
|---|---|---|
| Frecuencia dinámica / temperatura | Cambios en el tiempo por candidato | Perfil Equilibrado fijo; temperatura y frecuencia no disponibles; diez repeticiones |
| Procesos del sistema operativo | Interrupciones y variación de tiempo | Orden aleatorio, una corrida de calentamiento y diez repeticiones |
| Temperatura entre corridas | Deriva térmica | Registrar como limitación; no inventar valores sin sensor |
