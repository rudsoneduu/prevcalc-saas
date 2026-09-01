"""
Motor Comparativo das Regras de Transição da Reforma da Previdência (EC 103/2019)
Itera sobre as 4 regras principais (Pedágio 50%, Pedágio 100%, Pontos, Idade Progressiva),
calcula o tempo e idade FALTANTES para cada regra, estimando a Data Provável da Aposentadoria.
"""

from decimal import Decimal
from datetime import date, datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class TeseResultado(BaseModel):
    codigo_regra: str
    nome_regra: str
    elegivel: bool
    rmi_estimada: float
    coeficiente_aplicado: float
    fator_previdenciario: float
    requisitos_cumpridos: str
    motivo_inelegibilidade: Optional[str] = None
    
    # NOVOS CAMPOS DE PLANEJAMENTO: O QUE FALTA PARA APOSENTAR
    tempo_faltante_anos: float = 0.0
    idade_faltante_anos: float = 0.0
    pontos_faltantes: float = 0.0
    data_provavel_aposentadoria: Optional[str] = None
    orientacao_planejamento: Optional[str] = None

class ComparativoTesesResponse(BaseModel):
    regra_mais_vantajosa: TeseResultado
    todas_teses: List[TeseResultado]
    data_nascimento_segurado: Optional[str] = None
    resumo_planejamento_geral: Optional[str] = None

class MotorRegrasTransicao:
    """
    Motor especializado na simulação de regras da EC 103/2019 e planejamento de DIB futura.
    """

    @classmethod
    def calcular_todas_regras(
        cls,
        idade_anos: int,
        sexo: str,
        tempo_contribuicao_anos: float,
        tempo_em_13_11_2019: float,
        media_pbc: float,
        fator_prev: float = 1.0,
        ano_dib: int = 2026,
        dt_nascimento_iso: str = "1993-06-21"
    ) -> ComparativoTesesResponse:
        
        sexo_upper = sexo.upper()
        teses: List[TeseResultado] = []
        ano_atual = ano_dib

        try:
            dt_nasc = datetime.strptime(dt_nascimento_iso, "%Y-%m-%d").date()
        except Exception:
            dt_nasc = date(1993, 6, 21)

        # 1. REGRA DO PEDÁGIO 50% (Art. 17 da EC 103/2019)
        tempo_min_2019 = 28.0 if sexo_upper == 'F' else 33.0
        tempo_alvo_50 = 30.0 if sexo_upper == 'F' else 35.0

        if tempo_em_13_11_2019 >= tempo_min_2019:
            faltava_em_2019 = max(0.0, tempo_alvo_50 - tempo_em_13_11_2019)
            pedagio_50 = faltava_em_2019 * 0.50
            tempo_necessario_50 = tempo_alvo_50 + pedagio_50
            tempo_faltante = max(0.0, tempo_necessario_50 - tempo_contribuicao_anos)

            elegivel = tempo_faltante <= 0
            rmi_50 = max(1518.00, media_pbc * fator_prev) if elegivel else 0.0

            dt_aposentadoria = date(ano_atual + int(tempo_faltante), dt_nasc.month, dt_nasc.day).strftime("%d/%m/%Y")

            teses.append(TeseResultado(
                codigo_regra="PEDAGIO_50",
                nome_regra="Regra de Transição: Pedágio 50% (Art. 17)",
                elegivel=elegivel,
                rmi_estimada=round(rmi_50, 2),
                coeficiente_aplicado=1.0,
                fator_previdenciario=fator_prev,
                requisitos_cumpridos=f"Tempo de contribuição com pedágio: {tempo_necessario_50:.1f}a.",
                tempo_faltante_anos=round(tempo_faltante, 1),
                motivo_inelegibilidade=None if elegivel else f"Faltam {tempo_faltante:.1f} anos de contribuição com o pedágio de 50%.",
                data_provavel_aposentadoria=dt_aposentadoria,
                orientacao_planejamento=f"Contribuir continuamente por mais {tempo_faltante:.1f} anos."
            ))
        else:
            teses.append(TeseResultado(
                codigo_regra="PEDAGIO_50",
                nome_regra="Regra de Transição: Pedágio 50% (Art. 17)",
                elegivel=False,
                rmi_estimada=0.0,
                coeficiente_aplicado=0.0,
                fator_previdenciario=fator_prev,
                requisitos_cumpridos="Incompleto",
                motivo_inelegibilidade=f"Não possuía {tempo_min_2019:.0f} anos de contribuição em 13/11/2019 (possui {tempo_em_13_11_2019:.1f}a). Regra não aplicável.",
                tempo_faltante_anos=99.0
            ))

        # 2. REGRA DO PEDÁGIO 100% (Art. 20 da EC 103/2019)
        idade_min_100 = 57 if sexo_upper == 'F' else 60
        tempo_alvo_100 = 30.0 if sexo_upper == 'F' else 35.0
        faltava_100 = max(0.0, tempo_alvo_100 - tempo_em_13_11_2019)
        tempo_necessario_100 = tempo_alvo_100 + faltava_100

        tempo_faltante_100 = max(0.0, tempo_necessario_100 - tempo_contribuicao_anos)
        idade_faltante_100 = max(0, idade_min_100 - idade_anos)

        elegivel_100 = idade_faltante_100 <= 0 and tempo_faltante_100 <= 0
        rmi_100 = max(1518.00, media_pbc * 1.00) if elegivel_100 else 0.0

        anos_espera_100 = max(tempo_faltante_100, idade_faltante_100)
        dt_apos_100 = date(ano_atual + int(anos_espera_100), dt_nasc.month, dt_nasc.day).strftime("%d/%m/%Y")

        teses.append(TeseResultado(
            codigo_regra="PEDAGIO_100",
            nome_regra="Regra de Transição: Pedágio 100% (Art. 20)",
            elegivel=elegivel_100,
            rmi_estimada=round(rmi_100, 2),
            coeficiente_aplicado=1.00,
            fator_previdenciario=1.0,
            requisitos_cumpridos=f"Exige {idade_min_100} anos de idade e {tempo_necessario_100:.1f}a de contribuição. Benefício integral 100%.",
            tempo_faltante_anos=round(tempo_faltante_100, 1),
            idade_faltante_anos=float(idade_faltante_100),
            motivo_inelegibilidade=None if elegivel_100 else f"Faltam {idade_faltante_100} anos de idade e {tempo_faltante_100:.1f} anos de contribuição.",
            data_provavel_aposentadoria=dt_apos_100,
            orientacao_planejamento=f"Regra vantajosa (100% sem fator). Previsão de atendimento dos requisitos em {dt_apos_100}."
        ))

        # 3. REGRA DOS PONTOS (Art. 15 da EC 103/2019)
        pontos_alvo = 93 if sexo_upper == 'F' else 103
        tempo_min_pontos = 30.0 if sexo_upper == 'F' else 35.0
        pontos_atuais = idade_anos + tempo_contribuicao_anos

        pontos_faltantes = max(0.0, pontos_alvo - pontos_atuais)
        tempo_faltante_pts = max(0.0, tempo_min_pontos - tempo_contribuicao_anos)

        # A cada ano de contribuição a pessoa soma +2 pontos (+1 ano idade +1 ano tempo)
        anos_para_pontos = round(pontos_faltantes / 2.0, 1) if pontos_faltantes > 0 else 0.0
        anos_totais_espera_pts = max(tempo_faltante_pts, anos_para_pontos)

        elegivel_pts = pontos_faltantes <= 0 and tempo_faltante_pts <= 0
        coef_pontos = 0.60 + max(0.0, tempo_contribuicao_anos - (15.0 if sexo_upper == 'F' else 20.0)) * 0.02
        rmi_pts = max(1518.00, media_pbc * coef_pontos) if elegivel_pts else 0.0

        dt_apos_pts = date(ano_atual + int(anos_totais_espera_pts), dt_nasc.month, dt_nasc.day).strftime("%d/%m/%Y")

        teses.append(TeseResultado(
            codigo_regra="PONTOS",
            nome_regra="Regra de Transição: Sistema de Pontos (Art. 15)",
            elegivel=elegivel_pts,
            rmi_estimada=round(rmi_pts, 2),
            coeficiente_aplicado=round(coef_pontos, 2),
            fator_previdenciario=1.0,
            requisitos_cumpridos=f"Exige {pontos_alvo} pontos e {tempo_min_pontos:.0f}a de contribuição.",
            tempo_faltante_anos=round(tempo_faltante_pts, 1),
            pontos_faltantes=round(pontos_faltantes, 1),
            motivo_inelegibilidade=None if elegivel_pts else f"Possui {pontos_atuais:.1f} pts (faltam {pontos_faltantes:.1f} pontos e {tempo_faltante_pts:.1f}a de tempo).",
            data_provavel_aposentadoria=dt_apos_pts,
            orientacao_planejamento=f"Completará os pontos necessários aproximadamente em {dt_apos_pts} mantendo contribuições ativas."
        ))

        # 4. REGRA GERAL DA APOSENTADORIA POR IDADE (EC 103/2019)
        idade_min_geral = 62 if sexo_upper == 'F' else 65
        tempo_min_geral = 15.0 if sexo_upper == 'F' else 20.0

        idade_faltante_geral = max(0, idade_min_geral - idade_anos)
        tempo_faltante_geral = max(0.0, tempo_min_geral - tempo_contribuicao_anos)

        elegivel_geral = idade_faltante_geral <= 0 and tempo_faltante_geral <= 0
        coef_geral = 0.60 + max(0.0, tempo_contribuicao_anos - (15.0 if sexo_upper == 'F' else 20.0)) * 0.02
        rmi_geral = max(1518.00, media_pbc * coef_geral) if elegivel_geral else 0.0

        anos_espera_geral = max(idade_faltante_geral, tempo_faltante_geral)
        ano_apos_geral = dt_nasc.year + idade_min_geral
        dt_apos_geral = date(ano_apos_geral, dt_nasc.month, dt_nasc.day).strftime("%d/%m/%Y")

        teses.append(TeseResultado(
            codigo_regra="REGRA_GERAL_IDADE",
            nome_regra="Regra Geral: Aposentadoria por Idade (Art. 26)",
            elegivel=elegivel_geral,
            rmi_estimada=round(rmi_geral, 2),
            coeficiente_aplicado=round(coef_geral, 2),
            fator_previdenciario=1.0,
            requisitos_cumpridos=f"Exige {idade_min_geral} anos de idade e {tempo_min_geral:.0f}a de contribuição.",
            tempo_faltante_anos=round(tempo_faltante_geral, 1),
            idade_faltante_anos=float(idade_faltante_geral),
            motivo_inelegibilidade=None if elegivel_geral else f"Faltam {idade_faltante_geral} anos de idade (atingirá {idade_min_geral} anos em {dt_apos_geral}) e {tempo_faltante_geral:.1f}a de contribuição.",
            data_provavel_aposentadoria=dt_apos_geral,
            orientacao_planejamento=f"Previsão de Aposentadoria por Idade Urbana em {dt_apos_geral} com o cumprimento das 240 contribuições (20 anos)."
        ))

        # Selecionar regra mais vantajosa
        teses_elegiveis = [t for t in teses if t.elegivel]
        if teses_elegiveis:
            regra_mais_vantajosa = max(teses_elegiveis, key=lambda x: x.rmi_estimada)
        else:
            regra_mais_vantajosa = teses[-1]  # Default para Regra Geral por Idade

        resumo_geral = f"Para se aposentar pela Regra Geral por Idade ({idade_min_geral} anos), faltam {idade_faltante_geral} anos de idade e {tempo_faltante_geral:.1f} anos de contribuição. Data provável da aposentadoria: {dt_apos_geral}."

        return ComparativoTesesResponse(
            regra_mais_vantajosa=regra_mais_vantajosa,
            todas_teses=teses,
            data_nascimento_segurado=dt_nasc.strftime("%d/%m/%Y"),
            resumo_planejamento_geral=resumo_geral
        )
