import unittest
from decimal import Decimal
from app.engine.calculator import MotorCalculoINSS, SimulacaoRequest, SalarioInput, ModalidadeCalculo

class TestMotorCalculoINSS(unittest.TestCase):

    def setUp(self):
        self.salarios_amostra = [
            SalarioInput(competencia="1985-05", valor_informado=Decimal("2750000000000"), codigo_moeda="Cr$"),
            SalarioInput(competencia="1994-06", valor_informado=Decimal("825000"), codigo_moeda="CR$"),
            SalarioInput(competencia="1994-07", valor_informado=Decimal("500.00"), codigo_moeda="R$"),
            SalarioInput(competencia="2019-11", valor_informado=Decimal("2000.00"), codigo_moeda="R$"),
            SalarioInput(competencia="2024-01", valor_informado=Decimal("3000.00"), codigo_moeda="R$"),
        ]

    def test_aposentadoria_comum_descarta_pre_1994(self):
        req = SimulacaoRequest(
            cliente_id="test-123",
            data_dib="2026-09-01",
            sexo="M",
            tempo_contribuicao_anos=35,
            modalidade=ModalidadeCalculo.APOSENTADORIA_COMUM,
            salarios_contribuicao=self.salarios_amostra
        )
        res = MotorCalculoINSS.executar_simulacao(req)
        self.assertTrue(res.sucesso)
        self.assertEqual(res.salarios_considerados_qtd, 3)  # Apenas pós-07/1994
        self.assertEqual(res.salarios_descartados_qtd, 2)    # 1985-05 e 1994-06 descartados

    def test_revisao_vida_toda_inclui_historico_completo(self):
        req = SimulacaoRequest(
            cliente_id="test-456",
            data_dib="2026-09-01",
            sexo="F",
            tempo_contribuicao_anos=30,
            modalidade=ModalidadeCalculo.REVISAO_VIDA_TODA,
            salarios_contribuicao=self.salarios_amostra
        )
        res = MotorCalculoINSS.executar_simulacao(req)
        self.assertTrue(res.sucesso)
        # Total 5 salários: 80% maiores = 4 salários considerados, 1 descartado (o menor)
        self.assertEqual(res.salarios_considerados_qtd, 4)
        self.assertEqual(res.salarios_descartados_qtd, 1)

    def test_indenizacao_atrasados_regra_stj_1996(self):
        salarios_atraso = [
            SalarioInput(competencia="1995-05", valor_informado=Decimal("1000.00")), # Pré-10/1996
            SalarioInput(competencia="2000-05", valor_informado=Decimal("1000.00")), # Pós-10/1996
        ]
        req = SimulacaoRequest(
            cliente_id="test-789",
            data_dib="2026-09-01",
            sexo="M",
            tempo_contribuicao_anos=20,
            modalidade=ModalidadeCalculo.INDENIZACAO_ATRASADOS,
            salarios_contribuicao=salarios_atraso,
            remuneracao_atual_atrasados=Decimal("5000.00")
        )
        res = MotorCalculoINSS.executar_simulacao(req)
        self.assertTrue(res.sucesso)
        
        # Mês 1995-05: Principal = 1000.00 (20% de 5000), Juros = 0, Multa = 0
        # Mês 2000-05: Principal = 1000.00, Multa = 100.00, Juros = 350.00
        resumo = res.resumo_atrasados
        self.assertIsNotNone(resumo)
        self.assertEqual(resumo["total_principal"], Decimal("2000.00"))
        self.assertEqual(resumo["total_multa"], Decimal("100.00"))
        self.assertEqual(resumo["total_juros"], Decimal("350.00"))

if __name__ == '__main__':
    unittest.main()
