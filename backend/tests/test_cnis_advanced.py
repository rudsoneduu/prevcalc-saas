import unittest
from datetime import date
from app.engine.cnis_parser import CNISParserEngine
from app.engine.rule_recommender import MotorRecomendacaoRegras

class TestCNISAdvanced(unittest.TestCase):

    def test_recomendacao_revisao_vida_toda(self):
        salarios_pre_1994 = [
            {"competencia": f"1985-0{i}", "valor_informado": 50000.0} for i in range(1, 9)
        ] + [
            {"competencia": f"1986-0{i}", "valor_informado": 50000.0} for i in range(1, 9)
        ]
        rec = MotorRecomendacaoRegras.recomendar_modalidade(
            idade_anos=65,
            sexo="M",
            tempo_contribuicao_anos=35,
            salarios_contribuicao=salarios_pre_1994,
            data_dib=date(2026, 9, 1)
        )
        self.assertEqual(rec.codigo_modalidade, "REVISAO_VIDA_TODA")
        self.assertTrue(rec.elegivel)

    def test_recomendacao_aposentadoria_comum(self):
        salarios_recentes = [
            {"competencia": f"2020-0{i}", "valor_informado": 3000.0} for i in range(1, 5)
        ]
        rec = MotorRecomendacaoRegras.recomendar_modalidade(
            idade_anos=66,
            sexo="M",
            tempo_contribuicao_anos=35,
            salarios_contribuicao=salarios_recentes,
            data_dib=date(2026, 9, 1)
        )
        self.assertEqual(rec.codigo_modalidade, "APOSENTADORIA_COMUM")

if __name__ == '__main__':
    unittest.main()
