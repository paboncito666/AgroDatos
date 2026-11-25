import unittest

from herramientas.verificar_hipotesis import parse_hypotheses


class TestVerificarHipotesis(unittest.TestCase):
    def test_detecta_tabla_sin_hipotesis_completa(self):
        markdown = (
            "| Id | Hipótesis completa | VI | VD | Predicción | Mecanismo | Refutación |\n"
            "|---|---|---|---|---|---|---|\n"
            "| H1 | | | | | | |\n"
            "| H2 | | | | | | |\n"
        )

        complete, incomplete = parse_hypotheses(markdown)

        self.assertEqual(complete, [])
        self.assertEqual(incomplete, ["H1", "H2"])

    def test_acepta_hipotesis_con_campos_completos(self):
        markdown = (
            "| Id | Hipótesis completa | VI | VD | Predicción | Mecanismo | Refutación |\n"
            "|---|---|---|---|---|---|---|\n"
            "| H1 | Si n crece, t aumenta | n | tiempo (s) | aumenta | más operaciones | no aumenta |\n"
        )

        complete, incomplete = parse_hypotheses(markdown)

        self.assertEqual([item["id"] for item in complete], ["H1"])
        self.assertEqual(incomplete, [])


if __name__ == "__main__":
    unittest.main()
