"""
prototipo_estrategias.py — Plantilla de prototipo con tres estrategias (Clase 3).

Ilustra la ESTRUCTURA que debe tener el primer script de cada equipo:
  1. Generación de datos de prueba reproducible (semilla fija)
  2. Tres estrategias con la MISMA interfaz y el MISMO resultado
  3. Verificación de corrección antes de medir
  4. Una medición preliminar (no es el experimento formal: eso es la Clase 4)

Problema de ejemplo (neutro, no pertenece a ningún equipo): construir el texto
de un reporte con n líneas. Las estrategias difieren en cuántas veces se
COPIAN bytes en memoria, que es trabajo físico real del procesador y la RAM.

Uso:  python prototipo_estrategias.py [n_lineas]
"""
import io
import random
import sys
import time

SEMILLA = 7


def generar_datos(n: int) -> list[tuple[str, float]]:
    rng = random.Random(SEMILLA)
    return [(f"producto_{rng.randint(1, 999):03d}", round(rng.uniform(1, 500), 2)) for _ in range(n)]


def estrategia_concatenacion(filas):   # crea un texto nuevo en cada +=  (puede copiar todo lo previo)
    texto = ""
    for nombre, precio in filas:
        texto = texto + f"{nombre};{precio:.2f}\n"
    return texto


def estrategia_join(filas):            # acumula piezas y copia una sola vez al final
    return "".join(f"{nombre};{precio:.2f}\n" for nombre, precio in filas)


def estrategia_buffer(filas):          # búfer en memoria que crece por bloques
    b = io.StringIO()
    for nombre, precio in filas:
        b.write(f"{nombre};{precio:.2f}\n")
    return b.getvalue()


ESTRATEGIAS = [estrategia_concatenacion, estrategia_join, estrategia_buffer]

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    filas = generar_datos(n)
    salidas = {f.__name__: f(filas) for f in ESTRATEGIAS}
    assert len(set(salidas.values())) == 1, "¡Las estrategias producen textos distintos!"
    print(f"Corrección verificada: 3 estrategias, mismo texto de {len(salidas['estrategia_join']):,} caracteres\n")
    for f in ESTRATEGIAS:
        t0 = time.perf_counter()
        f(filas)
        print(f"{f.__name__:<28} {time.perf_counter() - t0:8.4f} s   (UNA corrida: preliminar, no concluyente)")
    print("\nNota: CPython a veces optimiza 'texto = texto + ...' cuando nadie más referencia el texto;")
    print("por eso la diferencia puede ser menor de la esperada. ¡Las hipótesis se verifican, no se suponen!")
    print("Hipótesis para la Clase 4: ¿cómo cambia cada tiempo si n crece 10 veces?")
