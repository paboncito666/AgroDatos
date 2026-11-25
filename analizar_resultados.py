"""Resume y grafica las corridas registradas por el experimento.

Uso:
    python analizar_resultados.py resultados/resultados.csv

No usa las corridas de memoria para calcular tiempos: ``tracemalloc`` añade
sobrecosto y esas filas se registran por separado a propósito.
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path


# Valores bilaterales de Student para IC del 95 %, grados de libertad 1..30.
T_95 = (12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262,
        2.228, 2.201, 2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101,
        2.093, 2.086, 2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052,
        2.048, 2.045, 2.042)


def leer_tiempos(ruta: Path) -> dict[tuple[str, int], list[float]]:
    """Lee únicamente repeticiones temporizadas (no las mediciones de memoria)."""
    grupos: dict[tuple[str, int], list[float]] = defaultdict(list)
    with ruta.open(newline="", encoding="utf-8") as archivo:
        for fila in csv.DictReader(archivo):
            if fila.get("medicion_memoria") == "si" or int(fila["repeticion"]) <= 0:
                continue
            grupos[(fila["estrategia"], int(fila["n"]))].append(float(fila["tiempo_s"]))
    if not grupos:
        raise ValueError("No hay corridas temporizadas en el CSV.")
    return grupos


def resumir(valores: list[float]) -> tuple[float, float, float, float]:
    """Devuelve media, desviación muestral, CV e IC95 (semiancho), en segundos."""
    media = statistics.fmean(valores)
    desviacion = statistics.stdev(valores) if len(valores) > 1 else 0.0
    cv = desviacion / media * 100 if media else 0.0
    if len(valores) < 2:
        return media, desviacion, cv, 0.0
    t = T_95[min(len(valores) - 2, len(T_95) - 1)]
    return media, desviacion, cv, t * desviacion / math.sqrt(len(valores))


def escribir_resumen(grupos: dict[tuple[str, int], list[float]], salida: Path) -> None:
    """Escribe una tabla Markdown que puede incorporarse directamente al informe."""
    lineas = [
        "# Resumen estadístico de tiempos",
        "",
        "Solo incluye corridas temporizadas; las de memoria se excluyen porque trazan asignaciones.",
        "El intervalo es media ± IC95 %, con t de Student y desviación muestral.",
        "",
        "| Estrategia | n | repeticiones | media (s) | desv. (s) | CV (%) | IC95 ± (s) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for (estrategia, n), valores in sorted(grupos.items(), key=lambda item: (item[0][1], item[0][0])):
        media, desv, cv, ic = resumir(valores)
        lineas.append(
            f"| {estrategia} | {n:,} | {len(valores)} | {media:.6f} | {desv:.6f} | {cv:.2f} | {ic:.6f} |"
        )
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def graficar(grupos: dict[tuple[str, int], list[float]], carpeta: Path) -> list[Path]:
    """Genera las figuras solicitadas, si matplotlib está instalado."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib no está instalado: se creó el resumen, pero no las gráficas.")
        return []

    carpeta.mkdir(parents=True, exist_ok=True)
    estrategias = sorted({estrategia for estrategia, _ in grupos})
    tamanos = sorted({n for _, n in grupos})
    figura, eje = plt.subplots(figsize=(8, 5))
    for estrategia in estrategias:
        puntos = [(n, *resumir(grupos[(estrategia, n)])[::3]) for n in tamanos if (estrategia, n) in grupos]
        eje.errorbar([p[0] for p in puntos], [p[1] for p in puntos], yerr=[p[2] for p in puntos],
                     marker="o", capsize=4, label=estrategia)
    eje.set(xscale="log", yscale="log", xlabel="Tamaño de entrada, n", ylabel="Tiempo de ejecución (s)",
            title="Tiempo de ejecución frente al tamaño de entrada")
    eje.grid(True, which="both", alpha=.25)
    eje.legend()
    figura.tight_layout()
    tiempo_n = carpeta / "tiempo_vs_n.png"
    figura.savefig(tiempo_n, dpi=160)
    plt.close(figura)

    mayor_n = max(tamanos)
    disponibles = [e for e in estrategias if (e, mayor_n) in grupos]
    medias = [resumir(grupos[(e, mayor_n)])[0] for e in disponibles]
    errores = [resumir(grupos[(e, mayor_n)])[3] for e in disponibles]
    figura, eje = plt.subplots(figsize=(8, 5))
    eje.bar(disponibles, medias, yerr=errores, capsize=5)
    eje.set(xlabel="Estrategia", ylabel="Tiempo de ejecución (s)",
            title=f"Comparación de estrategias para n = {mayor_n:,}")
    eje.grid(axis="y", alpha=.25)
    figura.tight_layout()
    comparacion = carpeta / "comparacion_n_mayor.png"
    figura.savefig(comparacion, dpi=160)
    plt.close(figura)
    return [tiempo_n, comparacion]


def main() -> None:
    parser = argparse.ArgumentParser(description="Analiza el CSV del experimento multinúcleo.")
    parser.add_argument("csv", type=Path, help="CSV creado por experimentos.ejecutar_experimento")
    parser.add_argument("--salida", type=Path, default=None, help="Markdown de resumen")
    parser.add_argument("--graficos", type=Path, default=None, help="Carpeta para PNG")
    args = parser.parse_args()
    grupos = leer_tiempos(args.csv)
    salida = args.salida or args.csv.with_name("estadisticas.md")
    carpeta = args.graficos or args.csv.parent / "graficos"
    escribir_resumen(grupos, salida)
    figuras = graficar(grupos, carpeta)
    print(f"Resumen: {salida}")
    for figura in figuras:
        print(f"Gráfica: {figura}")


if __name__ == "__main__":
    main()
