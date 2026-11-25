# Plantilla de hipótesis

Una hipótesis verificable **predice un resultado medible** y **puede resultar falsa**.

## Estructura
> **Si** _(cambio en la variable independiente)_, **entonces** _(variable dependiente, con unidad)_
> **aumentará / disminuirá** aproximadamente _(magnitud o factor)_, **porque** _(mecanismo físico/computacional)_,
> **manteniendo constantes** _(variables controladas)_.

## Ejemplo (problema neutro de la demostración, NO de un equipo)
> **Si** se reemplaza la lista intermedia por un generador al sumar n cuadrados, **entonces** el pico de memoria
> (MiB) **disminuirá** en más de un 90 % para n = 10⁶ y el tiempo (s) variará menos de un 20 %, **porque** el
> generador no almacena los n valores (memoria constante) pero realiza el mismo número de operaciones,
> **manteniendo** el mismo equipo, versión de Python y n.

## Hipótesis del equipo
| Id | Hipótesis completa | VI | VD (unidad) | Predicción cuantitativa | Mecanismo físico | ¿Cómo la refutaríamos? |
|---|---|---|---|---|---|---|
| H1 | | | | | | |
| H2 | Si se usa B (procesos por lote) en vez de A, el tiempo t (s) disminuirá para n = 1 000 000, porque procesos separados pueden ejecutar instrucciones Python en varios núcleos; el costo de crear procesos, serializar lotes y sincronizar resultados impide esperar una reducción exacta proporcional a ocho. | Estrategia | Tiempo t (s) | t_B < t_A en la media de 10 repeticiones | Trabajo de CPU repartido entre núcleos; sobrecosto de coordinación | Si el IC95 de B no queda por debajo del de A o su media es mayor. |
| H3 | Si se usa C (procesos por grupo) en vez de B, el tiempo t (s) puede disminuir para n grande al enviar menos tareas entre procesos, pero puede aumentar para n pequeño o con grupos desequilibrados. | Estrategia y granularidad | Tiempo t (s) | Diferencia medible frente a B para n = 2 000 000; el signo se determina con IC95 | Menos mensajes y serialización versus menor balance de carga entre núcleos | Si las medias tienen IC95 solapados o la tendencia contradice la predicción por tamaño. |

## Lista de verificación
- [ ] Tiene dirección (aumenta/disminuye) y una magnitud aproximada.
- [ ] La VD es medible con las herramientas disponibles en el laboratorio.
- [ ] Indica qué resultado la **refutaría**.
- [ ] Explica el mecanismo con al menos una magnitud física y su unidad SI.
- [ ] No afirma ahorro de energía si no se va a medir energía.
