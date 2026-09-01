import unittest
from app.engine.transition_rules import MotorRegrasTransicao
from app.engine.special_time import EngineTempoEspecial, PeriodoEspecial
from app.engine.bacen_sync import BacenSyncEngine

class TestEnterpriseFeatures(unittest.TestCase):

    def test_comparativo_regras_transicao(self):
        resultado = MotorRegrasTransicao.calcular_todas_regras(
            idade_anos=62,
            sexo="F",
            tempo_contribuicao_anos=30.0,
            tempo_em_13_11_2019=28.5,
            media_pbc=3000.0
        )
        self.assertIsNotNone(resultado.regra_mais_vantajosa)
        self.assertTrue(len(resultado.todas_teses) == 4)

    def test_conversao_tempo_especial_homem(self):
        periodos = [
            PeriodoEspecial(
                descricao_empresa="Metalúrgica S/A",
                agente_nocivo="Ruído 92dB",
                data_inicio="2000-01-01",
                data_fim="2010-01-01",
                tipo_periodo="INSALUBRIDADE_25_ANOS"
            )
        ]
        res = EngineTempoEspecial.converter_periodos_especiais(periodos, sexo="M")
        self.assertGreater(res.tempo_comum_adicional_dias, 0)
        self.assertAlmostEqual(res.tempo_comum_adicional_anos, 4.0, delta=0.5)

    def test_bacen_status_indices(self):
        status = BacenSyncEngine.obter_status_indices()
        self.assertIn("SELIC", status)
        self.assertIn("INPC", status)

if __name__ == '__main__':
    unittest.main()
