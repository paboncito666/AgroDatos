"""Estrategia C: paralelismo por grupos de lotes (granularidad gruesa).

Frente a la estrategia B, esta alternativa entrega aproximadamente una tarea
por proceso. Reduce serialización y coordinación en la cola de trabajo, pero
puede repartir peor la carga cuando un grupo tarda más que los demás.
"""
from __future__ import annotations

import math
import multiprocessing as mp
from collections.abc import Iterable

from .estrategia_b import procesos_disponibles
from .linea_base import contar_lote


def contar_grupo(grupo: list[tuple[int, int]]) -> int:
    """Función de nivel de módulo para que Windows pueda crear procesos hijos."""
    return sum(contar_lote(lote) for lote in grupo)


def agrupar_lotes(lotes: list[tuple[int, int]], procesos: int) -> list[list[tuple[int, int]]]:
    """Forma grupos contiguos de tamaño similar, sin modificar la entrada."""
    tamano = math.ceil(len(lotes) / procesos)
    return [lotes[i:i + tamano] for i in range(0, len(lotes), tamano)]


def ejecutar(lotes: Iterable[tuple[int, int]]) -> int:
    """Cuenta primos con menos tareas interproceso y la misma respuesta exacta."""
    tareas = list(lotes)
    if not tareas:
        return 0
    procesos = min(procesos_disponibles(), len(tareas))
    grupos = agrupar_lotes(tareas, procesos)
    with mp.Pool(processes=len(grupos)) as grupo:
        return sum(grupo.map(contar_grupo, grupos))
