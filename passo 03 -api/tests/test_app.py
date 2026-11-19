
import unittest
from app import app, criar_tabela


class TestAplicacao(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        criar_tabela()

    def setUp(self):
        self.client = app.test_client()

    def test_pagina_inicial(self):
        resposta = self.client.get("/")
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(
            b"Gerenciamento de usu",
            resposta.data
        )


if __name__ == "__main__":
    unittest.main()
