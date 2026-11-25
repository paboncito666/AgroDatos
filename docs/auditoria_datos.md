# Paso 1 — Inspección de `resultados.csv`

Auditoría del archivo formal de estrategia A, producido el 2026-11-18 y analizado el 2026-11-25. Se verificaron encabezados, conteos, etiquetas de repetición y celdas vacías; no se modificaron los datos.

## Columnas y unidades

Las unidades no forman parte de los nombres CSV; se interpretan con el arnés de medición:

| Columna | Unidad / significado |
|---|---|
| `marca_tiempo` | Fecha y hora local ISO |
| `equipo` | Identificador del equipo |
| `estrategia` | Identificador de la estrategia |
| `n` | Límite entero exclusivo del intervalo `[2, n)` |
| `repeticion` | Índice; `0` identifica la corrida de memoria |
| `tiempo_s` | Tiempo de pared, segundos |
| `cpu_proceso_s` | Tiempo de CPU del proceso, segundos |
| `uso_cpu_pct` | `100 × cpu_proceso_s / tiempo_s`, porcentaje del proceso |
| `pico_mem_mib` | Pico de memoria Python de `tracemalloc`, MiB |
| `rss_mib` | Memoria residente del proceso, MiB |
| `frecuencia_mhz` | Frecuencia de CPU, MHz |
| `temperatura_c` | Temperatura, °C |
| `energia_j` | Energía, J |
| `potencia_w` | Potencia media derivada de RAPL, W |
| `medicion_memoria` | `si` para corrida de memoria; `no` para corrida temporizada |
| `observacion` | Nota de la corrida; “corrida de memoria” en las lecturas separadas |

## Conteo e integridad

- 16 columnas y 33 filas de datos (sin contar el encabezado).
- 30 corridas temporizadas de `A_linea_base`: 10 por cada `n` (300 000, 1 000 000 y 2 000 000). Cada conjunto contiene exactamente las etiquetas de repetición 1–10.
- 3 corridas de memoria, una por cada tamaño y con etiqueta de repetición 0.
- No faltan filas ni valores en las columnas de identificación, tiempo, CPU, porcentaje de CPU o clasificación de corrida.
- Los campos vacíos son esperados según la instrumentación: `pico_mem_mib` está vacío en las 30 corridas de tiempo porque `tracemalloc` se ejecuta aparte; la memoria RSS está vacía en todas porque `psutil` no está instalado; frecuencia, temperatura, energía y potencia están vacías en las 33 filas porque los sensores/RAPL no estaban disponibles; `observacion` está vacía en las corridas de tiempo.
- Las tres corridas etiquetadas como memoria tardan más porque `tracemalloc` añade sobrecosto. Sus tiempos no se incluyen en el resumen de rendimiento.

No se encontraron archivos de `analizar_resultados.py` o `verificar_hipotesis.py` entre los materiales y rutas locales disponibles durante esta inspección. Se documenta y ejecuta una implementación reproducible del análisis en los siguientes pasos; no se atribuirá a los scripts originales de clase.

## Evidencia

La fuente de datos permanece intacta: [`resultados/resultados.csv`](../resultados/resultados.csv). Condiciones de ejecución: [`resultados/resultados.entorno.json`](../resultados/resultados.entorno.json).
