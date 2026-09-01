"""
Módulo de Conversão Monetária Histórica (1978 - 2026)
Diretriz de Precisão: Utilização exclusiva de decimal.Decimal com precisão de 28 casas decimais.
"""

from decimal import Decimal, getcontext, ROUND_HALF_UP
from datetime import date
from enum import Enum
from typing import NamedTuple, Optional

# Define a precisão global do contexto Decimal para evitar perdas de ponto flutuante (IEEE 754)
getcontext().prec = 28

class Moeda(Enum):
    CRUZEIRO_1978 = "Cr$"
    CRUZADO = "Cz$"
    CRUZADO_NOVO = "NCz$"
    CRUZEIRO_1990 = "Cr$"
    CRUZEIRO_REAL = "CR$"
    REAL = "R$"

class TransicaoMonetaria(NamedTuple):
    moeda_origem: Moeda
    moeda_destino: Moeda
    data_inicio: date
    data_fim: date
    divisor: Decimal
    norma_legal: str

# Tabela cronológica oficial de transição de moedas do Brasil (1978 - 2026)
TABELA_TRANSICOES = [
    TransicaoMonetaria(
        moeda_origem=Moeda.CRUZEIRO_1978,
        moeda_destino=Moeda.CRUZADO,
        data_inicio=date(1978, 1, 1),
        data_fim=date(1986, 2, 27),
        divisor=Decimal('1000'),
        norma_legal="Decreto-Lei nº 2.283/1986"
    ),
    TransicaoMonetaria(
        moeda_origem=Moeda.CRUZADO,
        moeda_destino=Moeda.CRUZADO_NOVO,
        data_inicio=date(1986, 2, 28),
        data_fim=date(1989, 1, 15),
        divisor=Decimal('1000'),
        norma_legal="Lei nº 7.730/1989"
    ),
    TransicaoMonetaria(
        moeda_origem=Moeda.CRUZADO_NOVO,
        moeda_destino=Moeda.CRUZEIRO_1990,
        data_inicio=date(1989, 1, 16),
        data_fim=date(1990, 3, 15),
        divisor=Decimal('1'),  # Paridade 1:1 na mudança de nomenclatura
        norma_legal="Lei nº 8.024/1990"
    ),
    TransicaoMonetaria(
        moeda_origem=Moeda.CRUZEIRO_1990,
        moeda_destino=Moeda.CRUZEIRO_REAL,
        data_inicio=date(1990, 3, 16),
        data_fim=date(1993, 7, 31),
        divisor=Decimal('1000'),
        norma_legal="Lei nº 8.697/1993"
    ),
    TransicaoMonetaria(
        moeda_origem=Moeda.CRUZEIRO_REAL,
        moeda_destino=Moeda.REAL,
        data_inicio=date(1993, 8, 1),
        data_fim=date(1994, 6, 30),
        divisor=Decimal('2750'),  # Valor fixo da URV em 30/06/1994
        norma_legal="Lei nº 8.880/1994"
    )
]

# Divisor cumulativo direto de Cruzeiros de 1978 para Real (R$): 1.000 * 1.000 * 1 * 1.000 * 2.750
DIVISOR_CUMULATIVO_1978_PARA_REAL = Decimal('2750000000000')

class ConversorMonetario:
    """
    Engine de conversão de valores monetários históricos para a moeda corrente (Real - R$).
    Garante matemática de precisão fixa e auditoria das etapas de conversão.
    """

    @staticmethod
    def identificar_moeda_por_data(data_competencia: date) -> Moeda:
        """
        Retorna a moeda legal vigente em determinada competência (ano/mês).
        """
        if data_competencia < date(1986, 2, 28):
            return Moeda.CRUZEIRO_1978
        elif data_competencia <= date(1989, 1, 15):
            return Moeda.CRUZADO
        elif data_competencia <= date(1990, 3, 15):
            return Moeda.CRUZADO_NOVO
        elif data_competencia <= date(1993, 7, 31):
            return Moeda.CRUZEIRO_1990
        elif data_competencia <= date(1994, 6, 30):
            return Moeda.CRUZEIRO_REAL
        else:
            return Moeda.REAL

    @classmethod
    def converter_para_real(
        cls, 
        valor_original: Decimal | float | str | int, 
        data_competencia: date, 
        moeda_declarada: Optional[Moeda] = None,
        casas_decimais: int = 2
    ) -> Decimal:
        """
        Converte um valor na moeda original da competência para Real (R$),
        aplicando a cadeia exata de divisores históricos.
        """
        if not isinstance(valor_original, Decimal):
            valor = Decimal(str(valor_original))
        else:
            valor = valor_original

        if data_competencia >= date(1994, 7, 1):
            return valor.quantize(Decimal(10) ** -casas_decimais, rounding=ROUND_HALF_UP)

        moeda_vigente = moeda_declarada or cls.identificar_moeda_por_data(data_competencia)

        # Aplica sequencialmente os divisores a partir da moeda identificada até o Real
        valor_atual = valor
        iniciou_conversao = False

        for transicao in TABELA_TRANSICOES:
            if transicao.moeda_origem == moeda_vigente:
                iniciou_conversao = True

            if iniciou_conversao:
                valor_atual = valor_atual / transicao.divisor

        return valor_atual.quantize(Decimal(10) ** -casas_decimais, rounding=ROUND_HALF_UP)

    @classmethod
    def obter_fator_conversao_acumulado(cls, data_competencia: date) -> Decimal:
        """
        Retorna o fator divisor acumulado exato da competência informada para o Real.
        """
        if data_competencia >= date(1994, 7, 1):
            return Decimal('1')

        moeda_vigente = cls.identificar_moeda_por_data(data_competencia)
        fator = Decimal('1')
        iniciou = False

        for transicao in TABELA_TRANSICOES:
            if transicao.moeda_origem == moeda_vigente:
                iniciou = True
            if iniciou:
                fator = fator * transicao.divisor

        return fator
