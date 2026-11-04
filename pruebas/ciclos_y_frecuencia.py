"""
ciclos_y_frecuencia.py — Del tiempo medido a la escala física del procesador.

Relaciones (frecuencia f en Hz = ciclos por segundo):
    Periodo de reloj         T = 1 / f                 [s]
    Ciclos transcurridos     N_ciclos ≈ f · t           [ciclos]
    Ciclos por operación     CPO ≈ N_ciclos / N_ops     [ciclos/operación]

ADVERTENCIA: la frecuencia cambia durante la ejecución (escalado dinámico,
turbo, ahorro de energía), así que N_ciclos es una ESTIMACIÓN de orden de
magnitud, no un conteo exacto (el conteo exacto requiere contadores de
hardware, p. ej. `perf stat` en Linux).

Uso:  python ciclos_y_frecuencia.py [n]
"""
import sys
import time

try:
    import psutil
    f_mhz = psutil.cpu_freq().current
except Exception:  # psutil ausente o frecuencia no disponible
    f_mhz = None

n = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
t0 = time.perf_counter()
acumulado = 0
for i in range(n):  # n sumas y n multiplicaciones "de Python"
    acumulado += i * i
t = time.perf_counter() - t0

f_hz = (f_mhz or 2000) * 1e6
origen = "medida con psutil" if f_mhz else "SUPUESTA (2 GHz): psutil no disponible"
ciclos = f_hz * t
print(f"Iteraciones n           : {n:,}")
print(f"Tiempo medido t         : {t:.4f} s")
print(f"Frecuencia f            : {f_hz/1e9:.2f} GHz ({origen})")
print(f"Periodo de reloj T = 1/f: {1/f_hz*1e9:.3f} ns")
print(f"Ciclos estimados f·t    : {ciclos:.3e} ciclos")
print(f"Ciclos por iteración    : {ciclos/n:.0f}  <- una iteración de Python cuesta decenas de ciclos")
print("\nPregunta: si la frecuencia sube al doble y nada más cambia, ¿qué esperaría del tiempo? ¿Por qué")
print("en la práctica la reducción suele ser MENOR? (pista: memoria, caché, E/S no escalan con f)")
