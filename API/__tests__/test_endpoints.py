# python API/__tests__/test_endpoints.py
import unittest
import requests
import uuid
import time
import os
from dotenv import load_dotenv

load_dotenv()

class TestApiRoutes(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:1234/api"
    VIDEO_PATH = 'video_teste.mp4'
    API_KEY = os.environ.get("API_KEYS", "").split(",")[0].strip()  # pega a primeira chave do .env

    # header reutilizável em todas as requisições autenticadas
    @property
    def auth_headers(self):
        return {"X-API-Key": self.API_KEY}

    def test_health_endpoint(self):
        """Teste para garantir que o servidor está online (rota pública, sem auth)"""
        response = requests.get(f"{self.BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "healthy")

    # ─── Testes de autenticação ────────────────────────────────────────────────

    def test_auth_missing_key(self):
        """Teste de segurança: requisição sem API Key deve retornar 401"""
        response = requests.get(f"{self.BASE_URL}/status/{uuid.uuid4()}")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Missing API Key", response.json().get("error"))

    def test_auth_invalid_key(self):
        """Teste de segurança: API Key inválida deve retornar 403"""
        response = requests.get(
            f"{self.BASE_URL}/status/{uuid.uuid4()}",
            headers={"X-API-Key": "chave-invalida"}
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn("Invalid", response.json().get("error"))

    # ─── Testes de fluxo ──────────────────────────────────────────────────────

    def test_full_detection_flow(self):
        """Teste de fluxo completo: Upload -> Status -> Results"""
        print("\nTesting Full Flow (Upload -> Processing -> Completed)...")

        # 1. Enviar vídeo
        with open(self.VIDEO_PATH, 'rb') as video:
            post_res = requests.post(
                f"{self.BASE_URL}/detect",
                files={'video': video},
                headers=self.auth_headers
            )

        self.assertEqual(post_res.status_code, 202)
        job_id = post_res.json().get("job_id")
        self.assertIsNotNone(job_id)

        # 2. Polling de Status (espera até completar ou timeout)
        max_retries = 10
        completed = False
        for _ in range(max_retries):
            status_res = requests.get(
                f"{self.BASE_URL}/status/{job_id}",
                headers=self.auth_headers
            )
            state = status_res.json().get("status")

            if state == "completed":
                completed = True
                break
            elif state == "error":
                self.fail(f"Job fell into error state: {status_res.json().get('error')}")

            time.sleep(1) # Aguarda o processamento

        self.assertTrue(completed, "Job timed out before completion")

        # 3. Verificar resultados finais
        result_res = requests.get(
            f"{self.BASE_URL}/results/{job_id}",
            headers=self.auth_headers
        )
        self.assertEqual(result_res.status_code, 200)

        data = result_res.json().get("results")
        self.assertIn("confidence", data)
        self.assertIn("verdict", data)
        print(f"[SUCCESS] Verdict: {data['verdict']} ({data['confidence']})")

    def test_status_invalid_id(self):
        """Teste de segurança: ID inexistente"""
        random_id = str(uuid.uuid4())
        response = requests.get(
            f"{self.BASE_URL}/status/{random_id}",
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_results_while_processing(self):
        """Teste: Tentar pegar resultado antes da hora"""
        with open(self.VIDEO_PATH, 'rb') as video:
            post_res = requests.post(
                f"{self.BASE_URL}/detect",
                files={'video': video},
                headers=self.auth_headers
            )

        job_id = post_res.json().get("job_id")

        # Imediatamente tenta pegar o resultado
        response = requests.get(
            f"{self.BASE_URL}/results/{job_id}",
            headers=self.auth_headers
        )

        # Deve retornar 202 (Accepted) mas com erro informando que ainda processa
        self.assertEqual(response.status_code, 202)
        self.assertIn("still in progress", response.json().get("error"))

if __name__ == "__main__":
    unittest.main()
