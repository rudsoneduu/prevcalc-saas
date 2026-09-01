"""
Aplicação Web FastAPI - Servidor da Engine de Cálculos Previdenciários
Plataforma Enterprise Completa (Fases 1, 2 e 3): Planejamento de Aposentadoria Faltante, e-PPP, Gov.br OAuth2, Criptografia LGPD e Celery/Redis
"""

import threading
import time
from fastapi import FastAPI, HTTPException, UploadFile, File, Response, Body, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import List, Dict, Any

from app.engine.currency import ConversorMonetario, TABELA_TRANSICOES
from app.engine.calculator import MotorCalculoINSS, SimulacaoRequest, SimulacaoResponse
from app.engine.cnis_parser import CNISParserEngine
from app.engine.pdf_report import GeradorRelatorioPDF
from app.engine.rule_recommender import MotorRecomendacaoRegras
from app.engine.transition_rules import MotorRegrasTransicao, ComparativoTesesResponse
from app.engine.special_time import EngineTempoEspecial, PeriodoEspecial
from app.engine.bacen_sync import BacenSyncEngine
from app.engine.task_queue import TaskQueueEngine, JobStatus
from app.engine.ppp_parser import PPPParserEngine, ResultadoPPP
from app.engine.govbr_integration import GovBrIntegrationEngine
from app.engine.lgpd_security import LGPDSecurityEngine, LGPDComplianceStatus

app = FastAPI(
    title="INSS Web Engine Enterprise API - Planejamento Faltante",
    description="API Enterprise com Planejamento de Requisitos Faltantes para Aposentadoria, Extrator e-PPP, Gov.br OAuth2 e LGPD",
    version="5.5.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "online", "engine_version": "5.5.0", "precisao_num": "Decimal(28)", "planning_engine": "Active"}

@app.post("/api/v1/calculos/teses-comparativas", response_model=ComparativoTesesResponse)
def simular_teses_comparativas(payload: Dict[str, Any] = Body(...)):
    try:
        resultado = MotorRegrasTransicao.calcular_todas_regras(
            idade_anos=payload.get("idade_anos", 33),
            sexo=payload.get("sexo", "M"),
            tempo_contribuicao_anos=payload.get("tempo_contribuicao_anos", 11.0),
            tempo_em_13_11_2019=payload.get("tempo_em_13_11_2019", 5.0),
            media_pbc=payload.get("media_pbc", 4500.00),
            fator_prev=payload.get("fator_prev", 1.0),
            dt_nascimento_iso=payload.get("dt_nascimento_iso", "1993-06-21")
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao simular teses comparativas: {str(e)}")

# DEMAIS ENDPOINTS DA APLICAÇÃO
@app.post("/api/v1/ppp/parse-pdf", response_model=ResultadoPPP)
async def parse_ppp_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")
    try:
        conteudo_bytes = await file.read()
        return PPPParserEngine.processar_ppp_pdf(conteudo_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar e-PPP: {str(e)}")

@app.post("/api/v1/govbr/oauth-start")
def iniciar_oauth_govbr(redirect_uri: str = "http://localhost:3000/auth/govbr/callback"):
    return GovBrIntegrationEngine.iniciar_fluxo_oauth(redirect_uri)

@app.post("/api/v1/govbr/cnis-direct")
def extrair_cnis_direto_govbr(token: str = Body(..., embed=True)):
    return GovBrIntegrationEngine.extrair_cnis_direto_api(token)

@app.get("/api/v1/security/lgpd-status", response_model=LGPDComplianceStatus)
def obter_status_lgpd():
    return LGPDComplianceStatus()

@app.get("/api/v1/jobs/{job_id}/status", response_model=JobStatus)
def consultar_status_job(job_id: str):
    job = TaskQueueEngine.obter_status_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID não encontrado.")
    return job

@app.get("/api/v1/indices/bacen-status")
def obter_status_bacen():
    return BacenSyncEngine.obter_status_indices()

@app.get("/api/v1/moedas/tabela")
def obter_tabela_moedas():
    resultado = []
    for t in TABELA_TRANSICOES:
        resultado.append({
            "moeda_origem": t.moeda_origem.value,
            "moeda_destino": t.moeda_destino.value,
            "data_inicio": t.data_inicio.isoformat(),
            "data_fim": t.data_fim.isoformat(),
            "divisor": str(t.divisor),
            "norma_legal": t.norma_legal
        })
    return {"tabela_transicoes": resultado}

@app.post("/api/v1/calculos/simulacao", response_model=SimulacaoResponse)
def calcular_simulacao(request: SimulacaoRequest):
    try:
        resultado = MotorCalculoINSS.executar_simulacao(request)
        return resultado
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no motor de cálculo: {str(e)}")

@app.post("/api/v1/calculos/tempo-especial")
def converter_tempo_especial(payload: Dict[str, Any] = Body(...)):
    try:
        periodos_raw = payload.get("periodos", [])
        periodos = [PeriodoEspecial(**p) for p in periodos_raw]
        sexo = payload.get("sexo", "F")
        return EngineTempoEspecial.converter_periodos_especiais(periodos, sexo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao converter tempo especial: {str(e)}")

@app.post("/api/v1/cnis/parse-pdf")
async def parse_cnis_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")

    try:
        conteudo_bytes = await file.read()
        resultado_cnis = CNISParserEngine.processar_cnis_pdf(conteudo_bytes, data_dib_ref=date(2026, 9, 1))

        salarios_dict = [s.model_dump() for s in resultado_cnis.salarios]
        recomendacao = MotorRecomendacaoRegras.recomendar_modalidade(
            idade_anos=resultado_cnis.dados_pessoais.idade_anos,
            sexo=resultado_cnis.dados_pessoais.sexo_estimado,
            tempo_contribuicao_anos=resultado_cnis.tempo_total_anos,
            salarios_contribuicao=salarios_dict,
            data_dib=date(2026, 9, 1)
        )

        return {
            "sucesso": True,
            "nome_arquivo": file.filename,
            "dados_pessoais": resultado_cnis.dados_pessoais.model_dump(),
            "tempo_total_anos": resultado_cnis.tempo_total_anos,
            "vinculos": [v.model_dump() for v in resultado_cnis.vinculos],
            "salarios": salarios_dict,
            "itens_complementacao": [i.model_dump() for i in resultado_cnis.itens_complementacao],
            "total_complementar_darf": resultado_cnis.total_complementar_darf,
            "recomendacao_modalidade": recomendacao.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento do CNIS: {str(e)}")

@app.post("/api/v1/calculos/relatorio-pdf")
def gerar_relatorio_pdf(payload: Dict[str, Any] = Body(...)):
    try:
        req = SimulacaoRequest(**payload.get("simulacao", payload))
        simulacao = MotorCalculoINSS.executar_simulacao(req)

        cliente_nome = payload.get("cliente_nome", "RUDSON EDUARDO DE OLIVEIRA AMARO")
        cpf = payload.get("cpf", "041.929.711-19")
        nit = payload.get("nit", "114.45167.11-0")
        data_nascimento = payload.get("data_nascimento", "21/06/1993")
        idade_formatada = payload.get("idade_formatada", "33 Anos e 2 Meses")

        pdf_bytes = GeradorRelatorioPDF.gerar_relatorio_pdf_bytes(
            simulacao=simulacao,
            cliente_nome=cliente_nome,
            cpf=cpf,
            nit=nit,
            data_nascimento=data_nascimento,
            idade_formatada=idade_formatada
        )
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=parecer_previdenciario_{cliente_nome.replace(' ', '_')}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar parecer PDF: {str(e)}")
