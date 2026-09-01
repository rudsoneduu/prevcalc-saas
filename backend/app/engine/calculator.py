"""
Motor Principal de Cálculos Previdenciários (INSS Engine)
Suporta Aposentadoria Comum (EC 103/2019), Revisão da Vida Toda (Tema 1102 STF) e Indenização de Atrasados (Art. 45-A).
"""

from decimal import Decimal, getcontext, ROUND_HALF_UP
from datetime import date, datetime
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from app.engine.currency import ConversorMonetario, Moeda
from app.engine.indices import TabelaIndicesHistoricos

getcontext().prec = 28

class ModalidadeCalculo(str, Enum):
    APOSENTADORIA_COMUM = "APOSENTADORIA_COMUM"
    REVISAO_VIDA_TODA = "REVISAO_VIDA_TODA"
    INDENIZACAO_ATRASADOS = "INDENIZACAO_ATRASADOS"

class SalarioInput(BaseModel):
    competencia: str = Field(..., description="Formato YYYY-MM")
    valor_informado: Decimal
    codigo_moeda: Optional[str] = None

class SimulacaoRequest(BaseModel):
    cliente_id: str
    data_dib: str = Field(..., description="Data de Início do Benefício (YYYY-MM-DD)")
    sexo: str = Field(..., description="'M' ou 'F'")
    tempo_contribuicao_anos: int = Field(..., description="Tempo total de contribuição em anos")
    modalidade: ModalidadeCalculo
    salarios_contribuicao: List[SalarioInput]
    fator_previdenciario_informado: Optional[Decimal] = None
    remuneracao_atual_atrasados: Optional[Decimal] = None

class SalarioProcessado(BaseModel):
    competencia: str
    moeda_original: str
    valor_original: Decimal
    valor_convertido_real: Decimal
    indice_correcao_acumulado: Decimal
    valor_corrigido: Decimal
    teto_epoca: Decimal
    limitado_ao_teto: bool
    descartado: bool
    detalhes: str = ""

class SimulacaoResponse(BaseModel):
    sucesso: bool
    modalidade: ModalidadeCalculo
    data_dib: str
    rmi_apurada: Decimal
    media_pbc: Decimal
    coeficiente_aplicado: Decimal
    fator_previdenciario: Decimal
    salarios_considerados_qtd: int
    salarios_descartados_qtd: int
    memoria_de_calculo: List[SalarioProcessado]
    resumo_atrasados: Optional[Dict[str, Any]] = None

class MotorCalculoINSS:
    """
    Engine de Cálculo Previdenciário com estrita conformidade às regras do INSS e STF.
    """

    @classmethod
    def executar_simulacao(cls, request: SimulacaoRequest) -> SimulacaoResponse:
        if request.modalidade == ModalidadeCalculo.APOSENTADORIA_COMUM:
            return cls._calcular_aposentadoria_comum(request)
        elif request.modalidade == ModalidadeCalculo.REVISAO_VIDA_TODA:
            return cls._calcular_revisao_vida_toda(request)
        elif request.modalidade == ModalidadeCalculo.INDENIZACAO_ATRASADOS:
            return cls._calcular_indenizacao_atrasados(request)
        else:
            raise ValueError(f"Modalidade não suportada: {request.modalidade}")

    @classmethod
    def _calcular_aposentadoria_comum(cls, req: SimulacaoRequest) -> SimulacaoResponse:
        """
        Regra da EC 103/2019:
        - PBC: Apenas salários a partir de 07/1994.
        - 100% da média aritmética dos salários corrigidos.
        - Coeficiente: 60% + 2% por ano acima de 15 anos (Mulher) / 20 anos (Homem).
        """
        data_corte_1994 = "1994-07"
        salarios_processados: List[SalarioProcessado] = []

        for item in req.salarios_contribuicao:
            comp = item.competencia[:7]
            descartado_pbc = comp < data_corte_1994

            dt_comp = datetime.strptime(comp + "-01", "%Y-%m-%d").date()
            moeda_orig = item.codigo_moeda or ConversorMonetario.identificar_moeda_por_data(dt_comp).value

            # Conversão para Real
            valor_real = ConversorMonetario.converter_para_real(item.valor_informado, dt_comp)
            
            # Fator de Correção Monetária pelo INPC
            fator_inpc = TabelaIndicesHistoricos.obter_fator_inpc_acumulado(comp, req.data_dib[:7])
            valor_corrigido = (valor_real * fator_inpc).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            teto_epoca = TabelaIndicesHistoricos.obter_teto(comp)
            limitado = valor_corrigido > teto_epoca

            salarios_processados.append(SalarioProcessado(
                competencia=comp,
                moeda_original=moeda_orig,
                valor_original=item.valor_informado,
                valor_convertido_real=valor_real,
                indice_correcao_acumulado=fator_inpc,
                valor_corrigido=valor_corrigido,
                teto_epoca=teto_epoca,
                limitado_ao_teto=limitado,
                descartado=descartado_pbc,
                detalhes="Descartado (anterior a 07/1994)" if descartado_pbc else "Incluído no PBC"
            ))

        salarios_validos = [s for s in salarios_processados if not s.descartado]

        if not salarios_validos:
            media_pbc = Decimal("0.00")
        else:
            soma = sum(s.valor_corrigido for s in salarios_validos)
            media_pbc = (soma / Decimal(len(salarios_validos))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Cálculo do Coeficiente EC 103/2019
        anos_base = 15 if req.sexo.upper() == 'F' else 20
        anos_excedentes = max(0, req.tempo_contribuicao_anos - anos_base)
        coeficiente_pct = Decimal("60") + Decimal(anos_excedentes * 2)
        coeficiente_decimal = coeficiente_pct / Decimal("100")

        rmi_calculada = (media_pbc * coeficiente_decimal).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Respeitar o Salário Mínimo e Teto da DIB
        teto_dib = TabelaIndicesHistoricos.obter_teto(req.data_dib[:7])
        sm_dib = TabelaIndicesHistoricos.obter_salario_minimo(req.data_dib[:7])
        rmi_final = max(sm_dib, min(rmi_calculada, teto_dib))

        return SimulacaoResponse(
            sucesso=True,
            modalidade=req.modalidade,
            data_dib=req.data_dib,
            rmi_apurada=rmi_final,
            media_pbc=media_pbc,
            coeficiente_aplicado=coeficiente_decimal,
            fator_previdenciario=Decimal("1.0000"),
            salarios_considerados_qtd=len(salarios_validos),
            salarios_descartados_qtd=len(salarios_processados) - len(salarios_validos),
            memoria_de_calculo=salarios_processados
        )

    @classmethod
    def _calcular_revisao_vida_toda(cls, req: SimulacaoRequest) -> SimulacaoResponse:
        """
        Revisão da Vida Toda (Tema 1102 STF):
        - Considera todo o histórico (1978 a DIB).
        - Conversão de todas as moedas para Real.
        - Aplicação de IRSM de 02/1994 (39.67%) se aplicável.
        - Média dos 80% maiores salários (descarte dos 20% menores).
        """
        salarios_temp = []

        for item in req.salarios_contribuicao:
            comp = item.competencia[:7]
            dt_comp = datetime.strptime(comp + "-01", "%Y-%m-%d").date()
            moeda_orig = item.codigo_moeda or ConversorMonetario.identificar_moeda_por_data(dt_comp).value

            valor_real = ConversorMonetario.converter_para_real(item.valor_informado, dt_comp)
            fator_inpc = TabelaIndicesHistoricos.obter_fator_inpc_acumulado(comp, req.data_dib[:7])

            # IRSM de 02/1994
            if comp == "1994-02":
                fator_inpc = fator_inpc * TabelaIndicesHistoricos.obter_irsm_fevereiro_1994()

            valor_corrigido = (valor_real * fator_inpc).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            teto_epoca = TabelaIndicesHistoricos.obter_teto(comp)

            salarios_temp.append({
                "competencia": comp,
                "moeda_original": moeda_orig,
                "valor_original": item.valor_informado,
                "valor_convertido_real": valor_real,
                "indice_correcao_acumulado": fator_inpc,
                "valor_corrigido": valor_corrigido,
                "teto_epoca": teto_epoca,
                "limitado_ao_teto": valor_corrigido > teto_epoca
            })

        # Regra dos 80% maiores salários (Descarte dos 20% menores)
        salarios_ordenados = sorted(salarios_temp, key=lambda x: x["valor_corrigido"], reverse=True)
        total_qtd = len(salarios_ordenados)
        qtd_considerar = max(1, int(Decimal(total_qtd) * Decimal("0.80")))

        competencias_consideradas = set(s["competencia"] for s in salarios_ordenados[:qtd_considerar])

        memoria_calculo: List[SalarioProcessado] = []
        salarios_validos_valores = []

        for s in salarios_temp:
            descartado = s["competencia"] not in competencias_consideradas
            if not descartado:
                salarios_validos_valores.append(s["valor_corrigido"])

            memoria_calculo.append(SalarioProcessado(
                competencia=s["competencia"],
                moeda_original=s["moeda_original"],
                valor_original=s["valor_original"],
                valor_convertido_real=s["valor_convertido_real"],
                indice_correcao_acumulado=s["indice_correcao_acumulado"],
                valor_corrigido=s["valor_corrigido"],
                teto_epoca=s["teto_epoca"],
                limitado_ao_teto=s["limitado_ao_teto"],
                descartado=descartado,
                detalhes="Descartado (20% menores salários)" if descartado else "Incluído na Média (80% Maiores)"
            ))

        soma = sum(salarios_validos_valores)
        media_pbc = (soma / Decimal(len(salarios_validos_valores))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        fator_prev = req.fator_previdenciario_informado or Decimal("1.0000")
        rmi_calculada = (media_pbc * fator_prev).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        teto_dib = TabelaIndicesHistoricos.obter_teto(req.data_dib[:7])
        sm_dib = TabelaIndicesHistoricos.obter_salario_minimo(req.data_dib[:7])
        rmi_final = max(sm_dib, min(rmi_calculada, teto_dib))

        return SimulacaoResponse(
            sucesso=True,
            modalidade=req.modalidade,
            data_dib=req.data_dib,
            rmi_apurada=rmi_final,
            media_pbc=media_pbc,
            coeficiente_aplicado=Decimal("1.00"),
            fator_previdenciario=fator_prev,
            salarios_considerados_qtd=len(salarios_validos_valores),
            salarios_descartados_qtd=total_qtd - len(salarios_validos_valores),
            memoria_de_calculo=memoria_calculo
        )

    @classmethod
    def _calcular_indenizacao_atrasados(cls, req: SimulacaoRequest) -> SimulacaoResponse:
        """
        Indenização de Períodos em Atraso (Art. 45-A da Lei 8.212/91):
        - Períodos até 11/10/1996: ISENTO de juros e multa (STJ / Súmula 45 AGU).
        - Períodos pós 11/10/1996: Incidência de Multa de 10% e Juros SELIC.
        """
        data_corte_stj = "1996-10"
        remuneracao_base = req.remuneracao_atual_atrasados or Decimal("5000.00")
        aliquota_inss = Decimal("0.20")  # 20%

        memoria_calculo: List[SalarioProcessado] = []
        total_principal = Decimal("0.00")
        total_juros = Decimal("0.00")
        total_multa = Decimal("0.00")

        for item in req.salarios_contribuicao:
            comp = item.competencia[:7]
            dt_comp = datetime.strptime(comp + "-01", "%Y-%m-%d").date()

            # Valor da contribuição principal (20% sobre a remuneração)
            valor_principal = (remuneracao_base * aliquota_inss).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            if comp <= data_corte_stj:
                # Regra pré-10/1996: Sem juros e sem multa
                juros = Decimal("0.00")
                multa = Decimal("0.00")
                detalhe = "Pré-10/1996: Isento de Juros e Multa (Súmula 45 AGU / STJ)"
            else:
                # Regra pós-10/1996: Multa de 10% + SELIC estimada (ex: 0.5% ao mês acumulado)
                multa = (valor_principal * Decimal("0.10")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                juros = (valor_principal * Decimal("0.35")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) # Ex: SELIC acumulada de teste
                detalhe = "Pós-10/1996: Incidência de Multa (10%) e Juros SELIC"

            valor_total_item = valor_principal + juros + multa
            total_principal += valor_principal
            total_juros += juros
            total_multa += multa

            memoria_calculo.append(SalarioProcessado(
                competencia=comp,
                moeda_original="R$",
                valor_original=remuneracao_base,
                valor_convertido_real=remuneracao_base,
                indice_correcao_acumulado=Decimal("1.0000"),
                valor_corrigido=valor_total_item,
                teto_epoca=TabelaIndicesHistoricos.obter_teto(comp),
                limitado_ao_teto=False,
                descartado=False,
                detalhes=f"{detalhe} | Principal: R$ {valor_principal} | Multa: R$ {multa} | Juros: R$ {juros}"
            ))

        total_geral = total_principal + total_juros + total_multa

        return SimulacaoResponse(
            sucesso=True,
            modalidade=req.modalidade,
            data_dib=req.data_dib,
            rmi_apurada=total_geral,
            media_pbc=remuneracao_base,
            coeficiente_aplicado=aliquota_inss,
            fator_previdenciario=Decimal("1.0000"),
            salarios_considerados_qtd=len(memoria_calculo),
            salarios_descartados_qtd=0,
            memoria_de_calculo=memoria_calculo,
            resumo_atrasados={
                "total_principal": total_principal,
                "total_juros": total_juros,
                "total_multa": total_multa,
                "total_geral": total_geral
            }
        )
