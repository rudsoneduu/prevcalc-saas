import unittest
from decimal import Decimal
from app.engine.calculator import MotorCalculoINSS, SimulacaoRequest, SalarioInput, ModalidadeCalculo
from app.engine.pdf_report import GeradorRelatorioPDF
from app.engine.cnis_parser import CNISParserEngine

class TestPDFModules(unittest.TestCase):

    def test_geracao_relatorio_pdf(self):
        req = SimulacaoRequest(
            cliente_id="test-pdf-123",
            data_dib="2026-09-01",
            sexo="M",
            tempo_contribuicao_anos=35,
            modalidade=ModalidadeCalculo.APOSENTADORIA_COMUM,
            salarios_contribuicao=[
                SalarioInput(competencia="1994-07", valor_informado=Decimal("500.00"), codigo_moeda="R$"),
                SalarioInput(competencia="2024-01", valor_informado=Decimal("5500.00"), codigo_moeda="R$")
            ]
        )
        simulacao = MotorCalculoINSS.executar_simulacao(req)
        pdf_bytes = GeradorRelatorioPDF.gerar_relatorio_pdf_bytes(simulacao, cliente_nome="João Teste")
        
        self.assertIsNotNone(pdf_bytes)
        self.assertTrue(len(pdf_bytes) > 500)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

if __name__ == '__main__':
    unittest.main()
