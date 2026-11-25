# Informe de análisis — Estrategia A

**Equipo:** 3 · **Fecha de medición:** 2026-11-18 · **Análisis:** 2026-11-25 · **Rama:** `pabon`

## Resumen

Se analizó el CSV formal de la línea base secuencial para tres límites de entrada y diez repeticiones por tamaño. El tiempo medio fue 0,3651 s para n=300 000, 2,0786 s para n=1 000 000 y 5,0236 s para n=2 000 000. El primer caso tuvo CV de 11,77 % y conserva todas sus repeticiones. No hay estrategias paralelas en este conjunto, por lo que estos resultados no miden aceleración multinúcleo ni energía.

## 1. Introducción

AgroDatos requiere contar primos y la implementación A usa un solo proceso. En esta fase se caracteriza el costo temporal al aumentar n en la misma máquina; no se compara el efecto de variar procesos.

## 2. Hipótesis

La tabla de hipótesis del equipo estaba vacía antes de este análisis. No se formulan hipótesis retrospectivas con estos datos; el contraste formal queda pendiente de una predicción registrada antes de una nueva medición. Véase [`hipotesis.md`](hipotesis.md).

## 3. Método

- Estrategia: A, conteo secuencial por lotes de 50 000 números; únicamente A está implementada.
- VI: límite exclusivo n = 300 000, 1 000 000 y 2 000 000. VD principal: tiempo de pared de `ejecutar(lotes)`, medido con `time.perf_counter()`.
- Diez repeticiones temporizadas por combinación, una corrida de calentamiento y orden pseudoaleatorio con semilla 42. La preparación ocurre antes del cronómetro.
- El CSV tiene una corrida de memoria separada por tamaño. Se excluye de estadísticas de tiempo porque `tracemalloc` altera el tiempo.
- Entorno e instrumentación: [`entorno.md`](entorno.md); protocolo detallado: [`protocolo.md`](protocolo.md).

## 4. Resultados

Resumen calculado desde las treinta corridas temporizadas. El intervalo de confianza del 95 % para la media usa t de Student con 9 grados de libertad (t=2,262).

| Estrategia | n | Repeticiones | Media [s] | Desv. estándar [s] | CV [%] | IC95 % media [s] |
|---|---:|---:|---:|---:|---:|---:|
| A_linea_base | 300 000 | 10 | 0,365137 | 0,042983 | 11,77 | [0,334391; 0,395883] |
| A_linea_base | 1 000 000 | 10 | 2,078560 | 0,170129 | 8,18 | [1,956866; 2,200254] |
| A_linea_base | 2 000 000 | 10 | 5,023589 | 0,158914 | 3,16 | [4,909917; 5,137261] |

El resumen CSV generado es [`../resultados/resumen_estadistico.csv`](../resultados/resumen_estadistico.csv). Las tres mediciones separadas de pico de memoria con `tracemalloc` fueron 0,003 MiB. No hubo medición de RSS, temperatura, frecuencia ni energía.

La revisión exploratoria de Tukey señaló 0,449336 s (repetición 7) para n=300 000 y 5,468558 s (repetición 3) para n=2 000 000. No hay causas confirmadas en la bitácora; se conservan todas las observaciones. Para n=300 000, una sensibilidad hipotética sin la repetición 7 daría media 0,355781 s y CV 9,30 %, frente a 0,365137 s y 11,77 % usando todos los datos. El resumen oficial utiliza siempre las diez corridas. Detalles: [`analisis_atipicos.md`](analisis_atipicos.md).

Los gráficos se incorporarán en su etapa correspondiente de este análisis.

## 5. Discusión

El contraste de hipótesis, la explicación física y las amenazas a la validez se desarrollarán tras completar los pasos 3–6.

## 6. Propuesta de mejora para la empresa

Pendiente del contraste entre A y al menos dos estrategias alternativas. No se recomienda desplegar paralelismo a partir de este conjunto de referencia solamente.

## 7. Conclusiones

La línea base responde correctamente y su duración crece con n; CV supera el umbral orientativo de 10 % en n=300 000. Los resultados son preliminares y específicos de esta máquina y versión de Python.

## 8. Referencias

- CSV y condiciones medidos: [`../resultados/resultados.csv`](../resultados/resultados.csv), [`../resultados/resultados.entorno.json`](../resultados/resultados.entorno.json).
- Protocolo del equipo: [`protocolo.md`](protocolo.md).

## Anexo: uso de IA

La asistencia se registra en [`uso_ia.md`](uso_ia.md); los cálculos estadísticos son reproducibles mediante el analizador local y los tests.
