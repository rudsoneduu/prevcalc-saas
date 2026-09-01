"""
Módulo de Conversão de Tempo Especial em Comum & Segurado Especial Rural
- Converte tempo trabalhado sob insalubridade/periculosidade até 13/11/2019 (Multiplicador 1.4 M / 1.2 F)
- Cômputo de Tempo Rural pré-11/1991 (Sem recolhimento financeiro obrigatório - Art. 55, §2º Lei 8.213/91)
"""

from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class PeriodoEspecial(BaseModel):
    descricao_empresa: str
    agente_nocivo: str  # ex: Ruído > 85dB, Produtos Químicos, Periculosidade
    data_inicio: str  # YYYY-MM-DD
    data_fim: str     # YYYY-MM-DD
    tipo_periodo: str  # INSALUBRIDADE_25_ANOS, RURAL_PRE_1991

class ResultadoConversaoEspecial(BaseModel):
    tempo_comum_adicional_dias: int
    tempo_comum_adicional_anos: float
    justificativa_legal: str
    periodos_convertidos: List[Dict[str, Any]] = []

class EngineTempoEspecial:
    """
    Calculadora de Conversão de Atividades Nocivas e Período Rural.
    """

    MULTIPLICADOR_HOMEM_25_ANOS = 1.40
    MULTIPLICADOR_MULHER_25_ANOS = 1.20

    @classmethod
    def converter_periodos_especiais(
        cls,
        periodos: List[PeriodoEspecial],
        sexo: str
    ) -> ResultadoConversaoEspecial:
        
        sexo_upper = sexo.upper()
        fator_mult = cls.MULTIPLICADOR_MULHER_25_ANOS if sexo_upper == 'F' else cls.MULTIPLICADOR_HOMEM_25_ANOS
        
        dt_limite_reforma = date(2019, 11, 13)
        total_dias_adicionais = 0
        detalhes = []

        for p in periodos:
            try:
                dt_ini = datetime.strptime(p.data_inicio, "%Y-%m-%d").date()
                dt_fim = datetime.strptime(p.data_fim, "%Y-%m-%d").date()

                if dt_fim > dt_limite_reforma:
                    dt_fim_efetiva = dt_limite_reforma
                else:
                    dt_fim_efetiva = dt_fim

                if dt_ini <= dt_fim_efetiva:
                    dias_brutos = (dt_fim_efetiva - dt_ini).days + 1

                    if p.tipo_periodo == "INSALUBRIDADE_25_ANOS":
                        dias_convertidos = int(dias_brutos * fator_mult)
                        dias_ganho_extra = dias_convertidos - dias_brutos
                        total_dias_adicionais += dias_ganho_extra
                        detalhes.append({
                            "empresa": p.descricao_empresa,
                            "agente": p.agente_nocivo,
                            "dias_brutos": dias_brutos,
                            "fator": fator_mult,
                            "dias_ganho_extra": dias_ganho_extra
                        })
                    elif p.tipo_periodo == "RURAL_PRE_1991":
                        dt_limite_rural = date(1991, 10, 31)
                        if dt_fim <= dt_limite_rural:
                            total_dias_adicionais += dias_brutos
                            detalhes.append({
                                "empresa": p.descricao_empresa,
                                "agente": "Trabalho Rural (Art. 55, §2º)",
                                "dias_brutos": dias_brutos,
                                "fator": 1.0,
                                "dias_ganho_extra": dias_brutos
                            })
            except ValueError:
                continue

        anos_adicionais = round(total_dias_adicionais / 365.25, 2)

        return ResultadoConversaoEspecial(
            tempo_comum_adicional_dias=total_dias_adicionais,
            tempo_comum_adicional_anos=anos_adicionais,
            justificativa_legal=f"Conversão de atividade especial pré-13/11/2019 com fator {fator_mult} ({sexo_upper}). Amparo: Art. 57, §5º da Lei 8.213/91 e Tema 998 STJ.",
            periodos_convertidos=detalhes
        )
