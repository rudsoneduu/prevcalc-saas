import unittest
from app.engine.ppp_parser import PPPParserEngine
from app.engine.govbr_integration import GovBrIntegrationEngine
from app.engine.lgpd_security import LGPDSecurityEngine

class TestPhase3Features(unittest.TestCase):

    def test_ppp_parser(self):
        res = PPPParserEngine.processar_ppp_pdf(b"%PDF-1.4 Mock PPP")
        self.assertTrue(res.sucesso)
        self.assertTrue(len(res.agentes_nocivos) > 0)
        self.assertTrue(res.elegivel_conversao_1_4)

    def test_govbr_oauth(self):
        flow = GovBrIntegrationEngine.iniciar_fluxo_oauth("http://localhost:3000/auth/callback")
        self.assertIn("auth_url", flow)
        self.assertIn("sso.acesso.gov.br", flow["auth_url"])

        session = GovBrIntegrationEngine.trocar_codigo_por_token("auth_code_123")
        self.assertEqual(session.nivel_govbr, "OURO")
        self.assertEqual(session.cpf_autenticado, "805.104.261-15")

    def test_lgpd_criptografia_pii(self):
        cpf_puro = "805.104.261-15"
        cpf_encriptado = LGPDSecurityEngine.encriptar_pii(cpf_puro)
        self.assertTrue(cpf_encriptado.startswith("ENC_"))

        cpf_decriptado = LGPDSecurityEngine.decriptar_pii(cpf_encriptado)
        self.assertEqual(cpf_decriptado, cpf_puro)

if __name__ == '__main__':
    unittest.main()
