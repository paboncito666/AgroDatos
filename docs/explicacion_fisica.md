# Paso 6 — Interpretación con física y computación

## Trabajo y ciclos de CPU

La estrategia A recorre todos los enteros del intervalo `[2,n)` y aplica pruebas de divisibilidad. Para cada candidato impar, `es_primo(k)` inspecciona divisores impares hasta `isqrt(k)` o hasta encontrar un divisor. Así, al aumentar `n` no solo se visitan más candidatos: también crece el límite de búsqueda para los primos y para los compuestos sin factores pequeños.

Entre n=300 000 y n=2 000 000, n aumenta por un factor 6,67 y el tiempo medio por un factor 13,76. El exponente empírico de los extremos es `ln(13,76)/ln(6,67) ≈ 1,38` en este intervalo. No es una ley asintótica ni debe extrapolarse: solo describe tres tamaños en este equipo.

El tiempo medio por candidato pasó de aproximadamente 1,22 µs a 2,51 µs entre esos extremos. Es consistente con más trabajo de divisibilidad por candidato, aunque el código no cuenta operaciones y la frecuencia del CPU no se midió. Para una frecuencia estable, los ciclos se aproximarían por `N_ciclos ≈ f × t`; aquí `f` cambia dinámicamente y no se registró, por lo que no se calculan ciclos.

## CPU y paralelismo

`cpu_proceso_s / tiempo_s × 100` promedió aproximadamente 99,3 % para n=300 000 y 1 000 000, y 99,6 % para n=2 000 000. Esto indica que el único proceso estuvo ocupado cerca de un núcleo durante casi todo el tiempo medido; no es el porcentaje de uso total de la máquina ni una medida de potencia. Un resultado ligeramente superior a 100 % puede ocurrir por diferencias de resolución entre los relojes.

El equipo tiene 4 núcleos físicos y 8 lógicos, pero A es secuencial. Los datos no comparan k=1,2,4,8: no permiten calcular aceleración `S=t_A/t_k`, eficiencia `η=S/k` ni verificar la expectativa de dividir el tiempo por ocho.

## Memoria, transferencia, energía y calor

Las corridas separadas registraron 0,003 MiB de pico `tracemalloc` para cada n. Esta lectura solo cuenta asignaciones Python nuevas durante `ejecutar`; la lista de lotes se creó antes de iniciar `tracemalloc`. Además, el instrumento no mide RSS, memoria nativa ni procesos hijos. Por eso no prueba que la memoria total de la estrategia sea constante ni permite comparar memoria completa del proceso.

El programa no lee archivos durante la sección cronometrada. No se midieron ancho de banda de memoria ni bytes transferidos; atribuir la duración a un cuello de botella de DRAM no está respaldado. El uso alto de CPU frente al tiempo de pared sí es consistente con trabajo predominantemente computacional en esta implementación.

Frecuencia, temperatura y RAPL no estaban disponibles. No se midió potencia `P`, energía `E=∫P dt` ni calor disipado; no se puede afirmar ahorro energético, calentamiento observado ni estrangulamiento térmico. Al paralelizar, más núcleos activos pueden elevar potencia y temperatura, y modificar la frecuencia por límites térmicos/eléctricos; son riesgos que deben medirse en una comparación posterior, no explicaciones probadas de estas corridas.

## Alcance

La interpretación se limita al Ryzen 5 PRO 2400G, CPython 3.14.8, Windows 10, perfil Equilibrado, corriente conectada y los tres tamaños ensayados. Aplicaciones/procesos de fondo, frecuencia y temperatura no quedaron controlados o medidos; el CV de 11,77 % en el tamaño menor y los candidatos Tukey descritos en [`analisis_atipicos.md`](analisis_atipicos.md) se mantienen como limitaciones explícitas.
