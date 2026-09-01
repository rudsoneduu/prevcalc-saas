import unittest
from app.engine.task_queue import TaskQueueEngine

class TestPhase2Features(unittest.TestCase):

    def test_job_lifecycle(self):
        job_id = TaskQueueEngine.criar_job("TESTE_JOB")
        self.assertTrue(job_id.startswith("job-"))

        job = TaskQueueEngine.obter_status_job(job_id)
        self.assertEqual(job.status, "PENDING")

        TaskQueueEngine.atualizar_progresso(job_id, 50, "Metade concluído")
        job = TaskQueueEngine.obter_status_job(job_id)
        self.assertEqual(job.progresso_percent, 50)
        self.assertEqual(job.status, "PROCESSING")

        TaskQueueEngine.finalizar_job(job_id, {"sucesso": True}, "Finalizado!")
        job = TaskQueueEngine.obter_status_job(job_id)
        self.assertEqual(job.progresso_percent, 100)
        self.assertEqual(job.status, "COMPLETED")

    def test_cache_fatores(self):
        TaskQueueEngine.salvar_fator_cache("1978-05-Cr$", 2750000000000.0)
        fator = TaskQueueEngine.obter_fator_cache("1978-05-Cr$")
        self.assertEqual(fator, 2750000000000.0)

if __name__ == '__main__':
    unittest.main()
