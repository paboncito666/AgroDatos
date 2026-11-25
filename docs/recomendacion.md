# Paso 7 — Recomendación para AgroDatos

## Decisión actual

Mantener la estrategia A como referencia validada y no activar “todos los núcleos” en producción basándose solo en la expectativa de dividir el tiempo por ocho. El experimento midió A a 300 000, 1 000 000 y 2 000 000; no contiene una alternativa paralela ni una variación del número de procesos. No hay evidencia para cuantificar aceleración o ahorro energético.

Como referencia en el equipo ensayado, A promedió 2,0786 s para n=1 000 000 (IC95 % de la media [1,9569; 2,2003]) y 5,0236 s para n=2 000 000 ([4,9099; 5,1373]). Son medias de diez corridas, no garantías de latencia por solicitud. Para n=300 000 el CV fue 11,77 %, por encima del criterio orientativo de 10 %; repetir ese caso antes de usarlo para planificar capacidad.

## Piloto propuesto

1. Implementar y probar una estrategia alternativa (por ejemplo, repartir lotes con procesos) contra A, con igual salida, datos, equipo y sección cronometrada.
2. Ensayar `k = 1, 2, 4` procesos en este computador de 4 núcleos físicos/8 lógicos; no asumir que 8 lógicos equivalen a 8 núcleos físicos.
3. Medir al menos n=1 000 000 y 2 000 000 con diez repeticiones por combinación, calentamiento y orden aleatorio/bloqueado. Mantener preparación fuera del cronómetro y memoria en corridas separadas.
4. **Criterio propuesto, no resultado medido:** considerar la alternativa solo si reduce el tiempo medio al menos 20 % en el tamaño operacional y el IC95 % de la reducción pareada entre A y alternativa queda por encima de cero. Esto requiere que la media no supere aproximadamente 1,663 s para n=1 000 000 o 4,019 s para n=2 000 000 en este mismo entorno.
5. Si energía o temperatura importan a la decisión, instrumentarlas directamente (RAPL o vatímetro; sensores disponibles) antes de afirmar ahorro o riesgo térmico. Registrar cualquier indisponibilidad como “no medido”.

## Condiciones de validez y riesgos

Las referencias temporales solo aplican al AMD Ryzen 5 PRO 2400G, CPython 3.14.8, Windows 10, perfil Equilibrado, corriente conectada y al algoritmo actual en el intervalo medido. Otras máquinas, versiones, granularidad o distribuciones de datos requieren una nueva línea base.

El paralelismo añade creación/gestión de procesos, coordinación y transferencia de argumentos/resultados; en entradas pequeñas esos costos pueden superar el trabajo ahorrado. Si se activan más núcleos físicos, la potencia y el calor pueden variar, y la frecuencia puede cambiar por límites térmicos/eléctricos. Nada de ello se cuantificó en estas mediciones. Validar corrección, medir el mismo trabajo y documentar la carga del equipo antes de despliegue.
