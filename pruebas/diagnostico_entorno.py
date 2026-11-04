"""
diagnostico_entorno.py — Ficha técnica del computador del experimento (Clase 3).

Antes de diseñar un experimento hay que saber QUÉ se puede medir en el equipo.
Este script genera entorno_equipo.json y entorno_equipo.md con:
  sistema operativo, CPU, núcleos, memoria, versión de Python,
  frecuencia actual/mín./máx., disponibilidad de temperatura y energía.

El .md se copia en docs/entorno.md del repositorio del equipo.

Uso:  python diagnostico_entorno.py
"""
import json
import os
import platform
import sys
from pathlib import Path

try:
    import psutil
except ImportError:
    psutil = None

# Reutiliza los lectores de sensores de la Clase 4 si están presentes
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "02_Clase_4" / "Scripts"))
try:
    import sensores
except ImportError:
    sensores = None

ficha = {
    "sistema_operativo": f"{platform.system()} {platform.release()} ({platform.version()[:60]})",
    "arquitectura": platform.machine(),
    "procesador": platform.processor() or "consultar: lscpu (Linux) / msinfo32 (Windows) / sysctl -a (macOS)",
    "nucleos_logicos": os.cpu_count(),
    "python": sys.version.split()[0],
}
if psutil:
    f = psutil.cpu_freq()
    ficha.update({
        "nucleos_fisicos": psutil.cpu_count(logical=False),
        "memoria_total_gib": round(psutil.virtual_memory().total / 1024**3, 2),
        "frecuencia_actual_mhz": round(f.current, 1) if f else None,
        "frecuencia_min_mhz": round(f.min, 1) if f and f.min else None,
        "frecuencia_max_mhz": round(f.max, 1) if f and f.max else None,
    })
else:
    ficha["nota"] = "psutil no instalado: pip install psutil para más datos (opcional)"
if sensores:
    ficha["sensores"] = sensores.disponibilidad()
    ficha["temperatura_actual_c"] = sensores.temperatura_c()

Path("entorno_equipo.json").write_text(json.dumps(ficha, indent=2, ensure_ascii=False), encoding="utf-8")
lineas = ["# Entorno experimental", "", "| Característica | Valor |", "|---|---|"]
lineas += [f"| {k} | {v} |" for k, v in ficha.items()]
lineas += ["", "> Generado con diagnostico_entorno.py. Los resultados de este equipo solo son",
           "> comparables con otros obtenidos en ESTE mismo entorno."]
Path("entorno_equipo.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
for k, v in ficha.items():
    print(f"{k:<24}: {v}")
print("\nGuardado en entorno_equipo.json y entorno_equipo.md")
