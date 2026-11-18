"""
Línea base — Equipo 3: Procesamiento multinúcleo.

Situación inicial: el módulo de análisis de la empresa cuenta números primos
en lotes de rangos numéricos usando UN SOLO proceso (un núcleo), aunque el
computador tiene varios núcleos disponibles.

preparar(n) -> lista de lotes (inicio, fin) que cubren [2, n)
ejecutar(lotes) -> cantidad total de primos

Importante en Windows/macOS: todo código que cree procesos debe ejecutarse
dentro de  if __name__ == "__main__":
"""
import math
import time

TAMANO_LOTE = 50_000


def es_primo(k: int) -> bool:
    if k < 2:
        return False
    if k % 2 == 0:
        return k == 2
    for d in range(3, math.isqrt(k) + 1, 2):
        if k % d == 0:
            return False
    return True


def contar_lote(lote: tuple[int, int]) -> int:
    inicio, fin = lote
    return sum(1 for k in range(inicio, fin) if es_primo(k))


def preparar(n: int):
    return [(i, min(i + TAMANO_LOTE, n)) for i in range(2, n, TAMANO_LOTE)]


def ejecutar(lotes) -> int:
    return sum(contar_lote(l) for l in lotes)   # un núcleo trabaja; los demás esperan


if __name__ == "__main__":
    lotes = preparar(1_000_000)
    t0 = time.perf_counter()
    print("Primos menores que 1 000 000:", ejecutar(lotes))   # 78 498
    print(f"Tiempo: {time.perf_counter() - t0:.2f} s")
