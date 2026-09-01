import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")

    def test_tabela_moedas(self):
        response = self.client.get("/api/v1/moedas/tabela")
        self.assertEqual(response.status_code, 200)
        tabela = response.json()["tabela_transicoes"]
        self.assertEqual(len(tabela), 5)
        self.assertEqual(tabela[0]["moeda_origem"], "Cr$")

    def test_simulacao_endpoint(self):
        payload = {
            "cliente_id": "client-api-test",
            "data_dib": "2026-09-01",
            "sexo": "M",
            "tempo_contribuicao_anos": 35,
            "modalidade": "APOSENTADORIA_COMUM",
            "salarios_contribuicao": [
                {"competencia": "1994-07", "valor_informado": 500.00, "codigo_moeda": "R$"},
                {"competencia": "2024-01", "valor_informado": 3000.00, "codigo_moeda": "R$"}
            ]
        }
        response = self.client.post("/api/v1/calculos/simulacao", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["sucesso"])
        self.assertEqual(data["modalidade"], "APOSENTADORIA_COMUM")
        self.assertGreater(float(data["rmi_apurada"]), 0)

if __name__ == '__main__':
    unittest.main()
