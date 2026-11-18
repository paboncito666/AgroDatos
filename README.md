# Equipo 3 — Procesamiento multinúcleo

> Proyecto: *Laboratorio colaborativo de rendimiento y eficiencia computacional desde la física aplicada*
> Física Aplicada al Desarrollo de Software · SENA · ADSO · 7.º trimestre

## 1. Problema y pregunta

AgroDatos S.A. analiza números primos por lotes, pero la implementación inicial utiliza un único proceso. El equipo compara cómo cambia el tiempo de pared al variar el límite `n`, manteniendo el mismo algoritmo secuencial, equipo y versión de Python.

## 2. Alcance de esta entrega: estrategia A

La estrategia A es la referencia secuencial implementada en [`src/linea_base.py`](src/linea_base.py):

- `preparar(n)` genera lotes de 50 000 números que cubren `[2, n)`.
- `ejecutar(lotes)` cuenta los primos de forma secuencial y devuelve el total.
- La preparación ocurre fuera del cronómetro; solo se mide `ejecutar(lotes)`.
- Las estrategias B y C no forman parte de esta entrega.

## 3. Evidencia y resultados

**Ejecución inicial requerida** (`python -m src.linea_base`, 18-11-2026): con `n = 1 000 000` se obtuvieron **78 498 primos** en **2,43 s**. La verificación final volvió a obtener 78 498 en **2,18 s**. Son corridas individuales, no estimaciones estadísticas; no se mezclan con las diez repeticiones formales.

El experimento formal de A utiliza tres tamaños y diez repeticiones por tamaño. Sus filas, incluidas las corridas de memoria separadas, se guardan en [`resultados/resultados.csv`](resultados/resultados.csv), y las condiciones automáticas en [`resultados/resultados.entorno.json`](resultados/resultados.entorno.json). Los IC95 % son t de Student con 9 grados de libertad.

| n (límite exclusivo) | repeticiones de tiempo | media [s] | desviación estándar [s] | CV [%] | IC95 % de la media [s] |
|---:|---:|---:|---:|---:|---:|
| 300 000 | 10 | 0,3651 | 0,0430 | 11,77 | [0,3344; 0,3959] |
| 1 000 000 | 10 | 2,0786 | 0,1701 | 8,18 | [1,9569; 2,2003] |
| 2 000 000 | 10 | 5,0236 | 0,1589 | 3,16 | [4,9099; 5,1373] |

El CV de `n = 300 000` supera el umbral orientativo de 10 %; se conserva y reporta la dispersión, sin excluir corridas. La corrida de memoria con `tracemalloc` registró un pico de 0,003 MiB por tamaño; no es una medición de RSS ni incluye procesos hijos. Aumentar `n` de 300 000 a 2 000 000 multiplicó el tiempo medio aproximadamente 13,8 veces en este equipo. No se afirma aceleración ni ahorro de energía con solo la estrategia A.

## 4. Entorno y límites de medición

Medición del 18-11-2026: Windows 10, AMD Ryzen 5 PRO 2400G, 4 núcleos físicos y 8 lógicos, CPython 3.14.8, perfil de energía Equilibrado y corriente conectada. `psutil` no está instalado; frecuencia, temperatura y energía RAPL no están disponibles en este entorno. Por ello no se reportan esas magnitudes ni se infiere potencia a partir del uso de CPU. Detalles y plan B: [`docs/entorno.md`](docs/entorno.md).

## 5. Reproducción

Desde la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# Opcional: pip install -r requirements.txt (psutil y matplotlib)
python -m src.linea_base
python -m unittest discover -s pruebas
python -m experimentos.ejecutar_experimento --rapido
python -m experimentos.ejecutar_experimento
```

La medición formal utiliza `[300000, 1000000, 2000000]`, diez repeticiones, un calentamiento y orden aleatorio con semilla 42. La preparación de los lotes queda fuera del cronómetro. Las lecturas de memoria se registran aparte porque `tracemalloc` altera los tiempos. El procedimiento completo está en [`docs/protocolo.md`](docs/protocolo.md).

## 6. Verificación y flujo de trabajo

Las pruebas validan resultados conocidos de la estrategia A, incluidos los límites del intervalo. El trabajo de esta entrega se realiza en la rama `pabon`, a partir de `origin/pabon`; las pruebas y resultados se registran antes de crear el commit. La guía del curso requiere integrar cambios mediante un pull request con revisión sustantiva de otro integrante; este commit local, por sí solo, no sustituye esa revisión.

Comandos de validación:

```powershell
python -m unittest discover -s pruebas
python -m experimentos.ejecutar_experimento --rapido
```

## 7. Equipo y roles

| Rol | Integrante | Responsabilidad |
|---|---|---|
| R1 — Coordinación y protocolo | _(nombre)_ | Mantiene el protocolo, las variables controladas y la planeación. |
| R2 — Estrategia base | _(nombre)_ | Documenta A y verifica la corrección de las estrategias. |
| R3 — Estrategias alternativas | _(nombre)_ | Diseña B y C y explica sus efectos físicos. |
| R4 — Medición y análisis | _(nombre)_ | Automatiza mediciones, registra CSV y analiza resultados. |

Todos participan en la comprensión de la física y el código; los nombres quedan por completar por el equipo.

## 8. Documentación del proyecto

- [Hipótesis](docs/hipotesis.md) · [Variables experimentales](docs/variables.md) · [Protocolo](docs/protocolo.md) · [Entorno](docs/entorno.md)
- [Decisiones técnicas](docs/decisiones.md) · [Uso de IA](docs/uso_ia.md) · [Informe](docs/informe.md)

Las estrategias B y C, su comparación y las conclusiones de rendimiento del equipo siguen pendientes.
