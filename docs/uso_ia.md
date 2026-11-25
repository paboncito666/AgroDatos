# Bitácora de uso de inteligencia artificial

La IA es una herramienta de apoyo permitida. Cada uso relevante se registra. **Usted es responsable de
verificar todo lo que la IA produce y de poder explicarlo sin ella.**

| # | Fecha | Integrante | Herramienta | Propósito (investigar, depurar, alternativas...) | Consulta (resumen) | ¿Qué se usó de la respuesta? | ¿Cómo se verificó? | Errores o suposiciones detectadas en la respuesta |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-11-18 | Integrante responsable por confirmar | Copilot SDK | Revisar, probar y documentar la estrategia A | Ejecutar la línea base y seguir el protocolo de medición del equipo | Separar preparación y cronómetro; agregar pruebas de resultados conocidos; registrar entorno y analizar diez corridas | Pruebas unitarias, comando de A, prueba de humo, CSV formal con 30 tiempos y 3 mediciones de memoria | La primera ejecución cronometró también la preparación y se descartó; frecuencia, temperatura y energía no estaban disponibles, así que no se reportaron |
| 2 | 2026-11-25 | Integrante responsable por confirmar | Copilot SDK | Auditar el CSV y analizar resultados de clase 5 | Revisar filas, resumir incertidumbre, atípicos, gráficos, hipótesis, física y recomendación | Añadir auditoría, resumen reproducible, gráficos SVG, sensibilidad sin eliminar datos, estado no evaluable de hipótesis vacías y criterio cuantificado para un piloto | Conteos del CSV, pruebas unitarias, regeneración del resumen y gráficos; estadísticas y umbrales de recomendación cotejados con los datos originales | Los scripts originales de clase 5 y la tabla visual del árbol no estaban disponibles; no se atribuyeron causas no registradas, no se inventaron hipótesis ni resultados de estrategias ausentes |

## Reflexión individual (Clase 5, una por integrante)
- **Nombre:**
- ¿En qué le ayudó la IA y en qué lo confundió?
- Un error o afirmación sin evidencia que detectó en la IA y cómo lo comprobó:
- ¿Qué parte del proyecto puede explicar completamente sin ayuda?
