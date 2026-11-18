from dataclasses import replace
import io
import contextlib
import unittest
from unittest.mock import patch

from energia import calcular, carregar_cenario, ler_decimal, menu_energia


class EnergiaTests(unittest.TestCase):
    def setUp(self):
        self.cenario = carregar_cenario()

    def test_balanco_padrao(self):
        r = calcular(self.cenario)
        self.assertAlmostEqual(r.consumo_original, 9)
        self.assertAlmostEqual(r.consumo_led, 5.4)
        self.assertAlmostEqual(r.geracao_potencial, 14.96475)
        self.assertAlmostEqual(r.solar_usada, 2.16)
        self.assertAlmostEqual(r.rede_com_solar, 3.24)
        self.assertAlmostEqual(r.retorno_led, 40 / 3.6)
        self.assertAlmostEqual(r.retorno_solar_incremental, 3000 / 2.16)

    def test_sem_coincidencia(self):
        r = calcular(replace(self.cenario, coincidencia=0))
        self.assertEqual(r.solar_usada, 0)
        self.assertEqual(r.rede_com_solar, r.consumo_led)
        self.assertIsNone(r.retorno_solar_incremental)

    def test_geracao_limita_autoconsumo(self):
        r = calcular(replace(self.cenario, solar_kwp=0.001, coincidencia=1))
        self.assertEqual(r.geracao_potencial, r.solar_usada)
        self.assertAlmostEqual(r.solar_usada + r.rede_com_solar, r.consumo_led)

    def test_sem_tarifa_ou_uso(self):
        r = calcular(replace(self.cenario, tarifa=0, horas_dia=0))
        self.assertEqual(r.gasto_solar, 0)
        self.assertIsNone(r.retorno_led)
        self.assertIsNone(r.retorno_solar_incremental)

    def test_entrada_decimal_invalida_e_virgula(self):
        with patch("builtins.input", side_effect=["NaN", "25", "5,5"]):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(ler_decimal("Horas", 5, 0, 24), 5.5)
            self.assertEqual(output.getvalue().count("Informe um número"), 2)

    def test_menu_exemplo(self):
        with patch("builtins.input", side_effect=["1"]):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                menu_energia()
        self.assertIn("3,24 kWh", output.getvalue())
        self.assertIn("115,74 anos", output.getvalue())


if __name__ == "__main__":
    unittest.main()

