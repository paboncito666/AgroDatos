# Protocolo experimental reproducible — Estrategia A

**Responsable:** R1 (por asignar) · **Revisión:** pendiente del equipo · **Versión:** 1 · **Fecha:** 2026-11-18

## 1. Objetivo

Medir el tiempo de pared de la línea base secuencial para contar primos menores que `n`, en tres tamaños de entrada. `preparar(n)` genera los lotes antes del cronómetro; se mide exclusivamente `ejecutar(lotes)`. Esta entrega caracteriza A y no compara todavía las estrategias B o C.

## 2. Condiciones de ejecución

- Mismo equipo y CPython 3.14.8 en todas las corridas; perfil de energía Equilibrado y corriente conectada.
- Entrada determinista: números del intervalo `[2, n)` agrupados en lotes de 50 000; no se leen archivos.
- Frecuencia, temperatura y energía no disponibles en este equipo. Los procesos de fondo del sistema no se controlaron ni se registraron; sus efectos se mitigan con diez repeticiones y orden aleatorio.
- Las ejecuciones temporizadas no usan `tracemalloc`. Las mediciones de memoria se guardan por separado y no se usan para inferir tiempos.

## 3. Procedimiento ejecutado

| Paso | Acción | Comando / método | Evidencia |
|---|---|---|---|
| 1 | Verificar casos conocidos y límites | `python -m unittest discover -s pruebas` | Pruebas de A |
| 2 | Evidencia inicial de A | `python -m src.linea_base` | 78 498 primos para `n = 1 000 000`; 2,43 s, una corrida |
| 3 | Verificación final de A | `python -m src.linea_base` | 78 498 primos; 2,18 s, una corrida no incluida en el análisis formal |
| 4 | Prueba de humo | `python -m experimentos.ejecutar_experimento --rapido` | CSV temporal de humo |
| 5 | Experimento formal | `python -m experimentos.ejecutar_experimento` | `resultados/resultados.csv` y `resultados/resultados.entorno.json` |

El cronómetro del comando de A empieza después de preparar los lotes. La ejecución inicial anterior a este ajuste no se incluye: también cronometraba `preparar(n)`.

## 4. Parámetros

- Tamaños: `n = 300 000`, `1 000 000`, `2 000 000`. Cubren cargas diferentes, mantienen un intervalo y una granularidad fija, y son suficientemente mayores que la resolución del reloj.
- Repeticiones: 10 mediciones temporizadas por tamaño (30 en total).
- Calentamiento: una ejecución no registrada con el primer tamaño, según el script.
- Orden: aleatorio con semilla 42; al haber solo A, aleatoriza la secuencia de tamaños y repeticiones, no la estrategia.
- Memoria: corrida independiente identificada por `medicion_memoria=si` para cada combinación de estrategia y tamaño.

## 5. Calidad y análisis

Reportar media, desviación estándar, coeficiente de variación (CV) e intervalo de confianza del 95 % por tamaño. Si CV > 10 %, informar la dispersión y no descartar repeticiones sin causa documentada. Reportar cualquier atípico con y sin él si se justifica excluirlo. Las corridas no permiten comparar A con estrategias aún no implementadas ni concluir sobre energía.

| n | Media [s] | Desviación estándar [s] | CV [%] | IC95 % de la media [s] |
|---:|---:|---:|---:|---:|
| 300 000 | 0,365137 | 0,042983 | 11,77 | [0,334391; 0,395883] |
| 1 000 000 | 2,078560 | 0,170129 | 8,18 | [1,956866; 2,200254] |
| 2 000 000 | 5,023589 | 0,158914 | 3,16 | [4,909917; 5,137261] |

El IC95 % usa el valor crítico t = 2,262 para 9 grados de libertad. El CV supera 10 % para `n = 300 000`; no se excluyeron corridas. Los valores completos están en `resultados/resultados.csv`.

La revisión de observaciones altas y la comparación de sensibilidad sin excluir datos se documentan en [`analisis_atipicos.md`](analisis_atipicos.md). La bitácora no asocia una causa conocida a ninguna corrida formal individual.

## 6. Incidentes

| Fecha | Incidente | Corridas afectadas | Decisión |
|---|---|---|---|
| 2026-11-18 | El primer cronómetro de `src.linea_base` incluía la preparación de lotes. | Primera ejecución preliminar, 2,52 s. | Descartada; se movió `preparar(n)` antes del cronómetro y se repitió. |
