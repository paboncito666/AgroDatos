# Paso 3 — Revisión de variabilidad y atípicos

Se revisaron las corridas temporizadas del CSV sin cambiar ni excluir filas. El CV se calcula como desviación estándar muestral/media. Se usó la regla exploratoria de Tukey (1,5 × RIC, cuartiles inclusivos); un punto fuera de la cerca es una señal para investigar, no evidencia de error.

| n | CV con todos los datos | Revisión de Tukey | Corrida señalada |
|---:|---:|---|---|
| 300 000 | 11,77 % | Una observación sobre la cerca superior (0,435263 s) | repetición 7: 0,449336 s |
| 1 000 000 | 8,18 % | Sin observaciones fuera de las cercas | — |
| 2 000 000 | 3,16 % | Una observación sobre la cerca superior (5,068999 s) | repetición 3: 5,468558 s |

Solo `n=300 000` incumple el umbral orientativo CV ≤ 10 %. El protocolo deja constancia de procesos del sistema no controlados y de frecuencia/temperatura no disponibles, factores que podrían producir variación temporal. Sin embargo, no hay una incidencia individual registrada para la repetición 7. Esa observación usó 0,453125 s de CPU para 0,449336 s de pared (100,8 % por resolución y diferencias de reloj); esto no identifica la causa. Para la repetición 3 de `n=2 000 000` se registraron 5,453125 s de CPU y 5,468558 s de pared (99,7 %), también sin incidente asociado. Variación de frecuencia/térmica o interferencia del sistema son posibilidades, no causas comprobadas.

## Sensibilidad, no exclusión

Para estimar cuánto influye la observación señalada en el caso que supera el CV, se recalculó `n=300 000` retirando únicamente la repetición 7 **de forma hipotética**:

| Cálculo para n=300 000 | Repeticiones | Media [s] | Desv. estándar [s] | CV [%] | IC95 % media [s] |
|---|---:|---:|---:|---:|---:|
| Todas las observaciones (resultado oficial) | 10 | 0,365137 | 0,042983 | 11,77 | [0,334391; 0,395883] |
| Sensibilidad sin repetición 7 (no sustituye resultado oficial) | 9 | 0,355781 | 0,033073 | 9,30 | [0,330359; 0,381203] |

El segundo cálculo usa t=2,306 con 8 grados de libertad. Como no se documentó una causa para descartar la repetición 7, el resultado principal permanece con las diez corridas. La sensibilidad solo muestra que esa observación eleva el CV; no prueba que sea inválida. El candidato alto de 5,468558 s para `n=2 000 000` tampoco se elimina; ese grupo tiene CV bajo (3,16 %).

## Decisión

Conservar todas las filas originales y sus estadísticas completas. En futuras sesiones, registrar hora, procesos concurrentes, alimentación, perfil de energía y cualquier incidente durante cada corrida. Frecuencia y temperatura requieren sensores que no estuvieron disponibles en este equipo.
