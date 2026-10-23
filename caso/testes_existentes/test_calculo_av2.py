"""Testes AV2: expectativas calculadas a partir do contrato R1."""
import unittest
from unittest.mock import patch

from miniloja.calculo import calcular_total


class TestCalculoAV2(unittest.TestCase):
    def test_subtotal_soma_preco_vezes_quantidade(self):
        # R1.1: 50*1 + 25*2 = 100; (100 + 12,90) * 1,05 = 118,545.
        # O comportamento float/round atual devolve 118,55.
        itens = [{"preco": 50.0, "qtd": 1}, {"preco": 25.0, "qtd": 2}]
        self.assertEqual(calcular_total(itens, None, "PE"), 118.55)

    def test_promo10_em_sp_aplica_desconto_antes_da_taxa(self):
        # R1.2 e R1.4: (80 - 10%) + 19,90 = 91,90; * 1,07 = 98,333.
        self.assertEqual(calcular_total([{"preco": 80.0, "qtd": 1}], "PROMO10", "SP"), 98.33)

    def test_frete_e_taxa_de_rj_abaixo_do_limite(self):
        # R1.3 e R1.4: (40 + 21,50) * 1,06 = 65,19.
        self.assertEqual(calcular_total([{"preco": 40.0, "qtd": 1}], None, "RJ"), 65.19)

    def test_natal_ativo_aplica_desconto_de_vinte_por_cento(self):
        # R1.2: 300 - 20% = 240; frete grátis (> 200); taxa PE 5% = 252.
        with patch.dict("os.environ", {"MINILOJA_PROMO_NATAL": "1"}):
            total = calcular_total([{"preco": 300.0, "qtd": 1}], "NATAL", "PE")
        self.assertEqual(total, 252.0)


if __name__ == "__main__":
    unittest.main()
