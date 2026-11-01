"""Testes AV3: acesso a pedidos, com o esperado vindo do contrato R4."""
import unittest

from miniloja import handlers


class TestAcessoAV3(unittest.TestCase):
    def _criar_pedido(self, usuario_id):
        status, pedido = handlers.post_pedidos(
            usuario_id, {"itens": [{"sku": "CAMISA-M", "preco": 50.0, "qtd": 1}], "uf": "PE"}
        )
        self.assertEqual(status, 201)
        return pedido

    def test_usuario_nao_ve_pedido_de_outro_usuario(self):
        # R4.1: o usuário 202 não pode ver o pedido do usuário 101.
        pedido = self._criar_pedido(101)
        status, corpo = handlers.get_pedido(202, pedido["id"])
        self.assertEqual(status, 404)
        self.assertNotIn("itens", corpo)

    def test_pedido_de_outro_responde_igual_a_pedido_inexistente(self):
        # R4.1: a resposta não pode confirmar que o pedido existe.
        pedido = self._criar_pedido(101)
        self.assertEqual(handlers.get_pedido(202, pedido["id"]), handlers.get_pedido(202, 999999))

    def test_dono_continua_vendo_o_proprio_pedido(self):
        # R4.1: a restrição não pode bloquear o dono.
        pedido = self._criar_pedido(101)
        status, corpo = handlers.get_pedido(101, pedido["id"])
        self.assertEqual(status, 200)
        self.assertEqual(corpo, pedido)


if __name__ == "__main__":
    unittest.main()
