"""Create dependency-free SVG plots with 95% confidence intervals."""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from xml.sax.saxutils import escape

if __package__:
    from .analizar_resultados import load_and_summarize
else:
    from analizar_resultados import load_and_summarize

BLUE = "#1769aa"
GRID = "#d8dee8"
TEXT = "#202b3c"
WIDTH = 960
HEIGHT = 600


def _text(x: float, y: float, value: str, *, size: int = 14, anchor: str = "middle") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial,sans-serif" '
        f'font-size="{size}" fill="{TEXT}" text-anchor="{anchor}">{escape(value)}</text>'
    )


def _document(title: str, description: str, elements: list[str]) -> str:
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        f"<title>{escape(title)}</title>",
        f"<desc>{escape(description)}</desc>",
        '<rect width="100%" height="100%" fill="white"/>',
        *elements,
        "</svg>",
        "",
    ])


def plot_time_vs_n(summaries: list[dict[str, float | int | str]], output: Path) -> None:
    points = [row for row in summaries if row["estrategia"] == "A_linea_base"]
    if not points or any(float(row["ic95_inferior_s"]) <= 0 for row in points):
        raise ValueError("Se requieren medias y límites IC95 % positivos para la gráfica log-log.")

    left, right, top, bottom = 105, 900, 90, 490
    log_x_min = math.log10(min(int(row["n"]) for row in points))
    log_x_max = math.log10(max(int(row["n"]) for row in points))
    log_y_min = math.log10(min(float(row["ic95_inferior_s"]) for row in points) * 0.9)
    log_y_max = math.log10(max(float(row["ic95_superior_s"]) for row in points) * 1.1)

    def x_pos(n: int) -> float:
        return left + (math.log10(n) - log_x_min) / (log_x_max - log_x_min) * (right - left)

    def y_pos(seconds: float) -> float:
        return bottom - (math.log10(seconds) - log_y_min) / (log_y_max - log_y_min) * (bottom - top)

    elements = [
        _text(WIDTH / 2, 38, "Estrategia A: tiempo de ejecución vs. n (escala log-log)", size=21),
        _text(WIDTH / 2, 65, "Barras: IC 95 % de la media (t de Student)", size=14),
    ]

    y_ticks = [10 ** (math.floor(log_y_min * 2) / 2 + i * 0.5) for i in range(20)]
    for value in y_ticks:
        if not (10**log_y_min <= value <= 10**log_y_max):
            continue
        y = y_pos(value)
        elements.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{GRID}"/>')
        elements.append(_text(left - 12, y + 5, f"{value:g}", anchor="end"))

    for row in points:
        x = x_pos(int(row["n"]))
        elements.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" stroke="{GRID}"/>')
        elements.append(_text(x, bottom + 25, f"{int(row['n']):,}"))

    elements.extend([
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="{TEXT}"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="{TEXT}"/>',
        _text((left + right) / 2, HEIGHT - 25, "n (límite exclusivo, números)", size=15),
        f'<text x="25" y="{(top + bottom) / 2}" transform="rotate(-90 25 {(top + bottom) / 2})" '
        f'font-family="Arial,sans-serif" font-size="15" fill="{TEXT}" text-anchor="middle">Tiempo de pared (s)</text>',
    ])

    coords = [(x_pos(int(row["n"])), y_pos(float(row["media_s"]))) for row in points]
    path = " ".join(
        ("M" if index == 0 else "L") + f" {x:.1f} {y:.1f}"
        for index, (x, y) in enumerate(coords)
    )
    elements.append(f'<path d="{path}" fill="none" stroke="{BLUE}" stroke-width="3"/>')

    for row, (x, y) in zip(points, coords):
        low = y_pos(float(row["ic95_inferior_s"]))
        high = y_pos(float(row["ic95_superior_s"]))
        elements.extend([
            f'<line x1="{x:.1f}" y1="{high:.1f}" x2="{x:.1f}" y2="{low:.1f}" stroke="{BLUE}" stroke-width="2"/>',
            f'<line x1="{x-8:.1f}" y1="{high:.1f}" x2="{x+8:.1f}" y2="{high:.1f}" stroke="{BLUE}" stroke-width="2"/>',
            f'<line x1="{x-8:.1f}" y1="{low:.1f}" x2="{x+8:.1f}" y2="{low:.1f}" stroke="{BLUE}" stroke-width="2"/>',
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{BLUE}"/>',
        ])

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        _document(
            "Estrategia A: tiempo de ejecución vs. n",
            "Gráfica log-log de las medias de tiempo con intervalos de confianza del 95 por ciento.",
            elements,
        ),
        encoding="utf-8",
    )


def plot_largest_n(summaries: list[dict[str, float | int | str]], output: Path) -> None:
    largest_n = max(int(row["n"]) for row in summaries)
    rows = [row for row in summaries if int(row["n"]) == largest_n]
    if not rows:
        raise ValueError("No hay corridas resumidas para el tamaño máximo.")

    left, right, top, bottom = 130, 890, 100, 490
    ymax = max(float(row["ic95_superior_s"]) for row in rows) * 1.2

    def y_pos(seconds: float) -> float:
        return bottom - seconds / ymax * (bottom - top)

    elements = [
        _text(WIDTH / 2, 38, f"Estrategias para n={largest_n:,}", size=21),
        _text(WIDTH / 2, 66, "Media de tiempo y IC 95 %", size=14),
    ]
    for tick in range(5):
        value = ymax * tick / 4
        y = y_pos(value)
        elements.extend([
            f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{GRID}"/>',
            _text(left - 12, y + 5, f"{value:.2f}", anchor="end"),
        ])
    elements.extend([
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="{TEXT}"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="{TEXT}"/>',
        _text((left + right) / 2, HEIGHT - 25, "Estrategia", size=15),
        f'<text x="30" y="{(top + bottom) / 2}" transform="rotate(-90 30 {(top + bottom) / 2})" '
        f'font-family="Arial,sans-serif" font-size="15" fill="{TEXT}" text-anchor="middle">Tiempo de pared (s)</text>',
    ])

    slot = (right - left) / len(rows)
    bar_width = min(100, slot * 0.45)
    for index, row in enumerate(rows):
        x = left + slot * (index + 0.5)
        mean = float(row["media_s"])
        low = float(row["ic95_inferior_s"])
        high = float(row["ic95_superior_s"])
        elements.extend([
            f'<rect x="{x-bar_width/2:.1f}" y="{y_pos(mean):.1f}" width="{bar_width:.1f}" '
            f'height="{bottom-y_pos(mean):.1f}" fill="{BLUE}" opacity="0.82"/>',
            f'<line x1="{x:.1f}" y1="{y_pos(high):.1f}" x2="{x:.1f}" y2="{y_pos(low):.1f}" stroke="{TEXT}" stroke-width="2"/>',
            f'<line x1="{x-10:.1f}" y1="{y_pos(high):.1f}" x2="{x+10:.1f}" y2="{y_pos(high):.1f}" stroke="{TEXT}" stroke-width="2"/>',
            f'<line x1="{x-10:.1f}" y1="{y_pos(low):.1f}" x2="{x+10:.1f}" y2="{y_pos(low):.1f}" stroke="{TEXT}" stroke-width="2"/>',
            _text(x, bottom + 25, str(row["estrategia"])),
            _text(x, y_pos(high) - 12, f"{mean:.3f} s"),
        ])

    note = "Solo está implementada A; no hay comparación con estrategias alternativas."
    elements.append(_text(WIDTH / 2, HEIGHT - 58, note, size=14))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        _document(
            f"Estrategias para n={largest_n}",
            note + " La barra muestra la media y las barras de error el intervalo de confianza del 95 por ciento.",
            elements,
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="CSV generado por el experimento")
    parser.add_argument("--directorio", type=Path, default=Path("resultados/graficos"))
    args = parser.parse_args()
    summaries = load_and_summarize(args.csv)
    plot_time_vs_n(summaries, args.directorio / "tiempo_vs_n.svg")
    plot_largest_n(summaries, args.directorio / "estrategias_n_maximo.svg")
    print(f"Gráficos SVG guardados en {args.directorio}")


if __name__ == "__main__":
    main()
