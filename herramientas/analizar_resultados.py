"""Summarize timed experiment runs with a 95% Student-t confidence interval."""
from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Iterable

T_975 = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
    16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
    21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060,
    26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042,
}

REQUIRED_FIELDS = {"estrategia", "n", "repeticion", "tiempo_s", "medicion_memoria"}


def summarize_rows(rows: Iterable[dict[str, str]]) -> list[dict[str, float | int | str]]:
    groups: dict[tuple[str, int], list[float]] = defaultdict(list)
    seen_repetitions: set[tuple[str, int, int]] = set()

    for row_number, row in enumerate(rows, start=2):
        if row.get("medicion_memoria") == "si":
            continue
        if row.get("medicion_memoria") != "no":
            raise ValueError(f"Fila {row_number}: medicion_memoria debe ser 'si' o 'no'.")

        try:
            strategy = row["estrategia"]
            n = int(row["n"])
            repetition = int(row["repeticion"])
            seconds = float(row["tiempo_s"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Fila {row_number}: faltan datos válidos para resumir.") from exc

        if not strategy or n <= 0 or repetition <= 0 or not math.isfinite(seconds) or seconds <= 0:
            raise ValueError(f"Fila {row_number}: estrategia, n, repetición o tiempo inválido.")
        key = (strategy, n, repetition)
        if key in seen_repetitions:
            raise ValueError(f"Fila {row_number}: repetición duplicada {key}.")
        seen_repetitions.add(key)
        groups[(strategy, n)].append(seconds)

    summaries = []
    for (strategy, n), samples in sorted(groups.items(), key=lambda item: (item[0][0], item[0][1])):
        count = len(samples)
        if count < 2:
            raise ValueError(f"{strategy}, n={n}: se requieren al menos dos corridas temporizadas.")

        mean = statistics.mean(samples)
        deviation = statistics.stdev(samples)
        critical = T_975.get(count - 1, 1.96)
        margin = critical * deviation / math.sqrt(count)
        summaries.append({
            "estrategia": strategy,
            "n": n,
            "repeticiones": count,
            "media_s": mean,
            "desviacion_estandar_s": deviation,
            "cv_pct": 100 * deviation / mean if mean else 0.0,
            "ic95_inferior_s": mean - margin,
            "ic95_superior_s": mean + margin,
            "min_s": min(samples),
            "max_s": max(samples),
        })
    return summaries


def load_and_summarize(csv_path: Path) -> list[dict[str, float | int | str]]:
    with csv_path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        missing_fields = REQUIRED_FIELDS.difference(reader.fieldnames or [])
        if missing_fields:
            raise ValueError(f"Faltan columnas requeridas: {', '.join(sorted(missing_fields))}.")
        return summarize_rows(reader)


def write_summary_csv(
    path: Path,
    summaries: list[dict[str, float | int | str]],
) -> None:
    fields = [
        "estrategia", "n", "repeticiones", "media_s", "desviacion_estandar_s",
        "cv_pct", "ic95_inferior_s", "ic95_superior_s", "min_s", "max_s",
    ]
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summaries)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="CSV generado por experimentos/ejecutar_experimento.py")
    parser.add_argument("--salida-csv", type=Path, help="Guardar además el resumen en CSV")
    args = parser.parse_args()

    summaries = load_and_summarize(args.csv)
    print("Estrategia | n | repeticiones | media [s] | DE [s] | CV [%] | IC95 % media [s]")
    for item in summaries:
        print(
            f"{item['estrategia']} | {item['n']} | {item['repeticiones']} | "
            f"{item['media_s']:.6f} | {item['desviacion_estandar_s']:.6f} | "
            f"{item['cv_pct']:.2f} | "
            f"[{item['ic95_inferior_s']:.6f}, {item['ic95_superior_s']:.6f}]"
        )
    if args.salida_csv:
        args.salida_csv.parent.mkdir(parents=True, exist_ok=True)
        write_summary_csv(args.salida_csv, summaries)
        print(f"Resumen guardado en {args.salida_csv}")


if __name__ == "__main__":
    main()
