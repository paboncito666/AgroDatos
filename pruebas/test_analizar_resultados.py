import unittest

from herramientas.analizar_resultados import summarize_rows


class TestAnalizarResultados(unittest.TestCase):
    def test_excluye_memoria_y_calcula_intervalo_t(self):
        rows = [
            {"estrategia": "A", "n": "10", "repeticion": "1", "tiempo_s": "1", "medicion_memoria": "no"},
            {"estrategia": "A", "n": "10", "repeticion": "2", "tiempo_s": "3", "medicion_memoria": "no"},
            {"estrategia": "A", "n": "10", "repeticion": "0", "tiempo_s": "100", "medicion_memoria": "si"},
        ]

        result = summarize_rows(rows)[0]

        self.assertEqual(result["repeticiones"], 2)
        self.assertEqual(result["media_s"], 2)
        self.assertEqual(result["desviacion_estandar_s"], 2**0.5)
        self.assertAlmostEqual(result["ic95_inferior_s"], 2 - 12.706, places=3)
        self.assertAlmostEqual(result["ic95_superior_s"], 2 + 12.706, places=3)

    def test_rechaza_repeticiones_duplicadas(self):
        rows = [
            {"estrategia": "A", "n": "10", "repeticion": "1", "tiempo_s": "1", "medicion_memoria": "no"},
            {"estrategia": "A", "n": "10", "repeticion": "1", "tiempo_s": "2", "medicion_memoria": "no"},
        ]

        with self.assertRaisesRegex(ValueError, "duplicada"):
            summarize_rows(rows)


if __name__ == "__main__":
    unittest.main()
