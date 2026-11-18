# Entorno experimental — Estrategia A

Registrado el 2026-11-18 antes del experimento. La misma ficha JSON se guarda junto al CSV formal en `resultados/resultados.entorno.json`.

| Característica | Valor |
|---|---|
| Sistema | Windows 10 |
| Procesador | AMD Ryzen 5 PRO 2400G with Radeon Vega Graphics |
| Núcleos físicos / lógicos | 4 / 8 |
| Python | CPython 3.14.8 |
| Alimentación | Corriente conectada (estado AC de Windows: en línea) |
| Perfil de energía | Equilibrado |
| `psutil` | No instalado |
| Frecuencia | No disponible; no se reporta |
| Temperatura | No disponible; plan B: registrar “no medida” |
| Energía RAPL | No disponible; plan B: declarar “energía no medida” |
| Aplicaciones / procesos de fondo | No se registraron; se consideran una fuente de variación no controlada |

Los contadores de sensores del arnés confirman que frecuencia, temperatura, energía RAPL y `psutil` no están disponibles. No se convierte el porcentaje de CPU a potencia ni se estima energía a partir del tiempo.
