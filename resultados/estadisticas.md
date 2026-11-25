# Resumen estadístico de tiempos

Solo incluye corridas temporizadas; las de memoria se excluyen porque trazan asignaciones.
El intervalo es media ± IC95 %, con t de Student y desviación muestral.

| Estrategia | n | repeticiones | media (s) | desv. (s) | CV (%) | IC95 ± (s) |
|---|---:|---:|---:|---:|---:|---:|
| A_linea_base | 300,000 | 10 | 0.578846 | 0.162023 | 27.99 | 0.115896 |
| B_procesos_por_lote | 300,000 | 10 | 0.834020 | 0.222097 | 26.63 | 0.158868 |
| C_procesos_por_grupo | 300,000 | 10 | 0.813534 | 0.215701 | 26.51 | 0.154293 |
| A_linea_base | 1,000,000 | 10 | 2.654428 | 0.585717 | 22.07 | 0.418968 |
| B_procesos_por_lote | 1,000,000 | 10 | 1.765442 | 0.318801 | 18.06 | 0.228041 |
| C_procesos_por_grupo | 1,000,000 | 10 | 1.784433 | 0.551490 | 30.91 | 0.394485 |
| A_linea_base | 2,000,000 | 10 | 5.906906 | 1.271235 | 21.52 | 0.909324 |
| B_procesos_por_lote | 2,000,000 | 10 | 3.182685 | 0.466422 | 14.65 | 0.333635 |
| C_procesos_por_grupo | 2,000,000 | 10 | 3.114083 | 0.596927 | 19.17 | 0.426986 |
