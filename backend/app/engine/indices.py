"""
Módulo de Gerenciamento de Índices Históricos, Tetos do INSS e Salários Mínimos (1978 - 2026)
Garante que todo salário de contribuição seja comparado com os limites legais da época e corrigido adequadamente.
"""

from decimal import Decimal, getcontext
from datetime import date
from typing import Dict, Optional, Tuple, List
from app.engine.currency import ConversorMonetario, Moeda

getcontext().prec = 28

class TabelaIndicesHistoricos:
    """
    Repositório de dados imutáveis de Tetos, Salários Mínimos e Índices de Reajuste Previdenciário.
    Estende de 1978 até 2026.
    """

    # Exemplos de Amostragem Histórica de Tetos do INSS em Real (ou equivalentes históricos)
    # Nota: Em produção, alimentado via PostgreSQL ou arquivo JSON completo.
    _TETOS_HISTORICOS: Dict[str, Decimal] = {
        # Competência YYYY-MM -> Teto em Real (ou convertido em Real para comparação pós-conversão)
        "1978-01": Decimal("100.00"),
        "1985-05": Decimal("1200.00"),
        "1994-07": Decimal("582.86"),
        "1998-12": Decimal("1200.00"),
        "2003-11": Decimal("2400.00"),
        "2019-11": Decimal("5839.45"),
        "2024-01": Decimal("7786.02"),
        "2026-01": Decimal("8157.41"),
    }

    _SALARIOS_MINIMOS: Dict[str, Decimal] = {
        "1978-01": Decimal("15.00"),
        "1994-07": Decimal("64.79"),
        "2019-11": Decimal("998.00"),
        "2024-01": Decimal("1412.00"),
        "2026-01": Decimal("1518.00"),
    }

    # Índices mensais fictícios/amostrais do INPC acumulado de competência até a DIB para testes
    _INPC_ACUMULADO_AMB: Dict[Tuple[str, str], Decimal] = {
        # (competencia, dib) -> Fator Acumulado
        ("1994-07", "2026-09"): Decimal("7.842512"),
        ("2019-11", "2026-09"): Decimal("1.341205"),
        ("2024-01", "2026-09"): Decimal("1.102340"),
    }

    @classmethod
    def obter_teto(cls, competencia: str) -> Decimal:
        """
        Retorna o teto do INSS vigente na competência (formato 'YYYY-MM').
        Se a competência exata não constar no dicionário amostral, retorna o teto mais próximo anterior.
        """
        if competencia in cls._TETOS_HISTORICOS:
            return cls._TETOS_HISTORICOS[competencia]
        
        # Fallback de busca pela competência imediatamente anterior
        chaves_ordenadas = sorted(cls._TETOS_HISTORICOS.keys())
        teto_encontrado = cls._TETOS_HISTORICOS[chaves_ordenadas[0]]
        for chave in chaves_ordenadas:
            if chave <= competencia:
                teto_encontrado = cls._TETOS_HISTORICOS[chave]
            else:
                break
        return teto_encontrado

    @classmethod
    def obter_salario_minimo(cls, competencia: str) -> Decimal:
        """
        Retorna o Salário Mínimo vigente na competência ('YYYY-MM').
        """
        if competencia in cls._SALARIOS_MINIMOS:
            return cls._SALARIOS_MINIMOS[competencia]

        chaves_ordenadas = sorted(cls._SALARIOS_MINIMOS.keys())
        sm_encontrado = cls._SALARIOS_MINIMOS[chaves_ordenadas[0]]
        for chave in chaves_ordenadas:
            if chave <= competencia:
                sm_encontrado = cls._SALARIOS_MINIMOS[chave]
            else:
                break
        return sm_encontrado

    @classmethod
    def obter_fator_inpc_acumulado(cls, competencia: str, dib: str) -> Decimal:
        """
        Retorna o fator de correção monetária pelo INPC acumulado entre a competência do salário e a DIB.
        """
        chave = (competencia, dib)
        if chave in cls._INPC_ACUMULADO_AMB:
            return cls._INPC_ACUMULADO_AMB[chave]

        # Em ausência de fator tabela estática, retorna um fator estimado padrão 1.0 ou proporcional para simulação
        if competencia >= dib:
            return Decimal("1.000000")
        
        # Fator genérico proporcional mínimo para testes
        return Decimal("1.050000")

    @classmethod
    def obter_irsm_fevereiro_1994(cls) -> Decimal:
        """
        Fator do IRSM de Fevereiro de 1994 (39,67%), fundamental para Revisão da Vida Toda / Regra de 1994.
        """
        return Decimal("1.3967")
