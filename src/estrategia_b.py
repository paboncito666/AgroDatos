"""Estrategia B: paralelismo por lotes con procesos.

Cada lote de la línea base se entrega como una tarea independiente a un
proceso. Es una carga de CPU: los procesos, a diferencia de los hilos de
CPython, pueden ejecutar Python en distintos núcleos al mismo tiempo.

El máximo de ocho procesos conserva comparable el experimento con el servidor
descrito en el enunciado. En equipos con menos núcleos se usa el máximo
disponible.
"""
from __future__ import annotations

import multiprocessing as mp
import os
from collections.abc import Iterable

from .linea_base import contar_lote

MAX_PROCESOS = 8


def procesos_disponibles() -> int:
    """Número de procesos usado por las estrategias paralelas."""
    return min(MAX_PROCESOS, os.cpu_count() or 1)


def ejecutar(lotes: Iterable[tuple[int, int]]) -> int:
    """Cuenta primos repartiendo cada lote entre hasta ocho procesos."""
    tareas = list(lotes)
    if not tareas:
        return 0
    with mp.Pool(processes=min(procesos_disponibles(), len(tareas))) as grupo:
        return sum(grupo.map(contar_lote, tareas))
