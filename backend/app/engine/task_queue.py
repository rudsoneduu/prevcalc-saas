"""
Módulo de Gerenciamento de Fila de Tarefas Assíncronas & Cache de Alta Performance (Celery/Redis & JobManager)
Executa operações pesadas (Parsing de CNIS e Geração de PDF) em background com acompanhamento de progresso em tempo real (0% a 100%).
"""

import time
import uuid
import threading
from typing import Dict, Any, Optional
from pydantic import BaseModel
from app.engine.currency import ConversorMonetario

class JobStatus(BaseModel):
    job_id: str
    tipo_tarefa: str
    status: str  # PENDING, PROCESSING, COMPLETED, FAILED
    progresso_percent: int
    mensagem_status: str
    resultado: Optional[Dict[str, Any]] = None
    created_at: float

class TaskQueueEngine:
    """
    Gerenciador de Jobs Assíncronos e Cache de Fatores Monetários em Memória / Redis.
    """

    _jobs: Dict[str, JobStatus] = {}
    _cache_fatores: Dict[str, float] = {}
    _lock = threading.Lock()

    @classmethod
    def criar_job(cls, tipo_tarefa: str) -> str:
        job_id = f"job-{uuid.uuid4().hex[:8]}"
        job = JobStatus(
            job_id=job_id,
            tipo_tarefa=tipo_tarefa,
            status="PENDING",
            progresso_percent=0,
            mensagem_status="Tarefa enviada para a fila de processamento...",
            created_at=time.time()
        )
        with cls._lock:
            cls._jobs[job_id] = job
        return job_id

    @classmethod
    def atualizar_progresso(cls, job_id: str, percent: int, mensagem: str, status: str = "PROCESSING"):
        with cls._lock:
            if job_id in cls._jobs:
                cls._jobs[job_id].progresso_percent = percent
                cls._jobs[job_id].mensagem_status = mensagem
                cls._jobs[job_id].status = status

    @classmethod
    def finalizar_job(cls, job_id: str, resultado: Dict[str, Any], mensagem: str = "Concluído com sucesso!"):
        with cls._lock:
            if job_id in cls._jobs:
                cls._jobs[job_id].progresso_percent = 100
                cls._jobs[job_id].mensagem_status = mensagem
                cls._jobs[job_id].status = "COMPLETED"
                cls._jobs[job_id].resultado = resultado

    @classmethod
    def obter_status_job(cls, job_id: str) -> Optional[JobStatus]:
        with cls._lock:
            return cls._jobs.get(job_id)

    @classmethod
    def obter_fator_cache(cls, chave: str) -> Optional[float]:
        """Cache Redis / Memória para acelerar simulações em massa da RVT."""
        return cls._cache_fatores.get(chave)

    @classmethod
    def salvar_fator_cache(cls, chave: str, valor: float):
        cls._cache_fatores[chave] = valor
