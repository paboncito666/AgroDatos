import tempfile
import unittest
from pathlib import Path

from herramientas.graficar_resultados import plot_largest_n, plot_time_vs_n
from herramientas.analizar_resultados import load_and_summarize


class TestGraficarResultados(unittest.TestCase):
    def test_crea_graficos_con_unidades_e_intervalos(self):
        lines = ["estrategia,n,repeticion,tiempo_s,medicion_memoria"]
        for n, base in ((300000, 1.0), (1000000, 3.0)):
            for repetition in range(1, 11):
                lines.append(f"A_linea_base,{n},{repetition},{base + repetition / 100:.2f},no")
        lines.append("A_linea_base,1000000,0,20,si")
        csv_text = "\n".join(lines) + "\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "data.csv"
            source.write_text(csv_text, encoding="utf-8")
            summaries = load_and_summarize(source)

            log_plot = root / "time.svg"
            comparison = root / "largest.svg"
            plot_time_vs_n(summaries, log_plot)
            plot_largest_n(summaries, comparison)

            log_content = log_plot.read_text(encoding="utf-8")
            comparison_content = comparison.read_text(encoding="utf-8")
            self.assertIn("log-log", log_content)
            self.assertIn("IC 95 %", log_content)
            self.assertIn("Tiempo de pared (s)", log_content)
            self.assertIn("no hay comparación", comparison_content)
            self.assertIn("IC 95 %", comparison_content)


if __name__ == "__main__":
    unittest.main()
