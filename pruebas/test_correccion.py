"""
Pruebas de corrección (R2). Ejecutar:  python -m unittest discover -s pruebas
Una estrategia más rápida pero incorrecta NO es una mejora.
"""
import unittest

from src import linea_base


class TestCorreccion(unittest.TestCase):
    def test_linea_base_cuenta_primos_conocidos(self):
        datos = linea_base.preparar(20_000)
        self.assertEqual(linea_base.ejecutar(datos), 2_262)

    def test_linea_base_limites_del_rango(self):
        self.assertEqual(linea_base.ejecutar(linea_base.preparar(2)), 0)
        self.assertEqual(linea_base.ejecutar(linea_base.preparar(3)), 1)
        self.assertEqual(linea_base.ejecutar(linea_base.preparar(4)), 2)

    # TODO (R2): una prueba por estrategia que compare su resultado con la línea base
    # def test_estrategia_b_igual_a_base(self):
    #     d = linea_base.preparar(20000)
    #     self.assertEqual(estrategia_b.ejecutar(d), linea_base.ejecutar(d))


if __name__ == "__main__":
    unittest.main()
