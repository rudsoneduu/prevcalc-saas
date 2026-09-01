"""
Motor de Recomendação Automática da Melhor Modalidade Previdenciária
Analisa Idade, Sexo, Tempo Total de Contribuição e Histórico de Salários para recomendar a regra mais vantajosa.
"""

from decimal import Decimal
from datetime import date
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class RecomendacaoModalidade(BaseModel):
    codigo_modalidade: str
    titulo_modalidade: str
    justificativa_juridica: str
    elegivel: bool
    score_vantagem: int  # 0 a 100

class MotorRecomendacaoRegras:
    """
    Diagnóstico e parecer prévio automático de elegibilidade.
    """

    @classmethod
    def recomendar_modalidade(
        cls,
        idade_anos: int,
        sexo: str,
        tempo_contribuicao_anos: int,
        salarios_contribuicao: List[Dict[str, Any]],
        data_dib: date
    ) -> RecomendacaoModalidade:
        
        sexo_upper = sexo.upper()
        qtd_pre_1994 = sum(1 for s in salarios_contribuicao if s.get("competencia", "") < "1994-07")
        soma_salarios_pre_1994 = sum(Decimal(str(s.get("valor_informado", 0))) for s in salarios_contribuicao if s.get("competencia", "") < "1994-07")

        # 1. Avaliar Revisão da Vida Toda (Tema 1102 STF)
        # Requisito: Exista quantidade expressiva de salários pré-1994 com valores relevantes
        if qtd_pre_1994 >= 12 and soma_salarios_pre_1994 > Decimal("100000"):
            return RecomendacaoModalidade(
                codigo_modalidade="REVISAO_VIDA_TODA",
                titulo_modalidade="Revisão da Vida Toda (Tema 1102 STF)",
                justificativa_juridica=f"Detectadas {qtd_pre_1994} contribuições de alto valor anteriores a 07/1994 no CNIS. A inclusão do histórico de 1978 a 1994 tende a elevar significativamente a RMI.",
                elegivel=True,
                score_vantagem=95
            )

        # 2. Avaliar Aposentadoria Comum / Geral (EC 103/2019)
        idade_minima = 62 if sexo_upper == 'F' else 65
        tempo_minimo = 15 if sexo_upper == 'F' else 20

        if idade_anos >= idade_minima and tempo_contribuicao_anos >= tempo_minimo:
            return RecomendacaoModalidade(
                codigo_modalidade="APOSENTADORIA_COMUM",
                titulo_modalidade="Aposentadoria Programada Geral (EC 103/2019)",
                justificativa_juridica=f"Segurado cumpre os requisitos definitivos da EC 103/2019: {idade_anos} anos de idade (mínimo {idade_minima}) e {tempo_contribuicao_anos} anos de contribuição (mínimo {tempo_minimo}).",
                elegivel=True,
                score_vantagem=85
            )

        # 3. Default: Aposentadoria Comum com Simulação de Regra de Transição
        return RecomendacaoModalidade(
            codigo_modalidade="APOSENTADORIA_COMUM",
            titulo_modalidade="Aposentadoria Comum (Simulação de Transição)",
            justificativa_juridica=f"Simulação baseada em {tempo_contribuicao_anos} anos de contribuição e {idade_anos} anos de idade na DIB. Análise do Período Básico de Cálculo pós-07/1994.",
            elegivel=True,
            score_vantagem=70
        )
