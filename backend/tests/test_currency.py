import unittest
from datetime import date
from decimal import Decimal
from app.engine.currency import ConversorMonetario, Moeda, DIVISOR_CUMULATIVO_1978_PARA_REAL

class TestConversorMonetario(unittest.TestCase):

    def test_identificacao_moedas_historicas(self):
        self.assertEqual(ConversorMonetario.identificar_moeda_por_data(date(1980, 5, 15)), Moeda.CRUZEIRO_1978)
        self.assertEqual(ConversorMonetario.identificar_moeda_por_data(date(1987, 10, 1)), Moeda.CRUZADO)
        self.assertEqual(ConversorMonetario.identificar_moeda_por_data(date(1989, 6, 20)), Moeda.CRUZADO_NOVO)
        self.assertEqual(ConversorMonetario.identificar_moeda_por_data(date(1991, 1, 1)), Moeda.CRUZEIRO_1990)
        self.assertEqual(ConversorMonetario.identificar_moeda_por_data(date(1993, 9, 10)), Moeda.CRUZEIRO_REAL)
        self.assertEqual(ConversorMonetario.identificar_moeda_por_data(date(1994, 7, 1)), Moeda.REAL)
        self.assertEqual(ConversorMonetario.identificar_moeda_por_data(date(2026, 9, 1)), Moeda.REAL)

    def test_fator_acumulado_1978(self):
        fator_1978 = ConversorMonetario.obter_fator_conversao_acumulado(date(1980, 1, 1))
        self.assertEqual(fator_1978, DIVISOR_CUMULATIVO_1978_PARA_REAL)

    def test_conversao_cruzeiro_1985_para_real(self):
        # Cr$ 1.500.000,00 em 05/1985
        # 1.500.000 / 2.750.000.000.000 = 0.000000545454... -> R$ 0.00 (devido ao valor extremamente irrisório sem correção monetária prévia)
        # Cr$ 2.750.000.000.000 em 1985 -> R$ 1,00 exato
        valor_cr = Decimal('2750000000000')
        valor_real = ConversorMonetario.converter_para_real(valor_cr, date(1985, 5, 1))
        self.assertEqual(valor_real, Decimal('1.00'))

    def test_conversao_cruzeiro_real_1994_para_real(self):
        # CR$ 825.000,00 em 06/1994 -> 825.000 / 2.750 = R$ 300,00
        valor_cr_real = Decimal('825000')
        valor_real = ConversorMonetario.converter_para_real(valor_cr_real, date(1994, 6, 1))
        self.assertEqual(valor_real, Decimal('300.00'))

    def test_conversao_real_manter_valor(self):
        valor = Decimal('5500.50')
        valor_convertido = ConversorMonetario.converter_para_real(valor, date(2024, 1, 1))
        self.assertEqual(valor_convertido, Decimal('5500.50'))

if __name__ == '__main__':
    unittest.main()
