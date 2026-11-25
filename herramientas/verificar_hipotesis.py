"""Check whether the experiment has structurally complete, pre-registered hypotheses."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

EMPTY = {"", "-", "—", "_"}
HYPOTHESIS_ID = re.compile(r"H\d+")


def parse_hypotheses(text: str) -> tuple[list[dict[str, str]], list[str]]:
    complete: list[dict[str, str]] = []
    incomplete: list[str] = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or not HYPOTHESIS_ID.fullmatch(cells[0]):
            continue
        if len(cells) != 7:
            incomplete.append(cells[0])
            continue
        if all(value not in EMPTY for value in cells[1:]):
            complete.append(dict(zip(
                ("id", "hipotesis", "vi", "vd", "prediccion", "mecanismo", "refutacion"),
                cells,
            )))
        else:
            incomplete.append(cells[0])
    return complete, incomplete


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hipotesis", type=Path, help="Tabla de hipótesis del equipo en Markdown")
    args = parser.parse_args()
    complete, incomplete = parse_hypotheses(args.hipotesis.read_text(encoding="utf-8"))

    if not complete:
        identifiers = ", ".join(incomplete) if incomplete else "ninguna"
        print(f"NO EVALUABLE: no hay hipótesis completas registradas ({identifiers}).")
        print("Decisión: no confirmar ni refutar; definir una predicción cuantitativa antes de nuevas mediciones.")
        return 2

    print(f"Se encontraron {len(complete)} hipótesis estructuralmente completas.")
    if incomplete:
        print(f"Hipótesis incompletas: {', '.join(incomplete)}.")
    print("La decisión estadística requiere revisar manualmente el diseño, la predicción y sus intervalos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
