import unittest
import requests
import uuid

class TestApiRoutes(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/api"

    # def test_health_endpoint(self):
    #     """Teste para garantir que o servidor está online e saudável"""
    #     print("\nTesting GET /health...")
    #     response = requests.get(f"{self.BASE_URL}/health")
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json().get("status"), "healthy")

    def test_status_endpoint_valid_id(self):
        """Teste para verificar o status de um job que (supostamente) existe"""
        # Primeiro, criamos um job para ter um ID real
        print("Testing GET /status/<job_id>...")
        with open('video_teste.mp4', 'rb') as f:
            post_res = requests.post(f"{self.BASE_URL}/detect", files={'video': f})
            job_id = post_res.json().get("job_id")

        # Agora testamos a rota de status com esse ID
        response = requests.get(f"{self.BASE_URL}/status/{job_id}")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())
        self.assertEqual(response.json().get("job_id"), job_id)

    def test_status_endpoint_invalid_id(self):
        """Teste de segurança: verificar comportamento com ID inexistente"""
        print("Testing GET /status/ com ID inválido...")
        random_id = str(uuid.uuid4())
        response = requests.get(f"{self.BASE_URL}/status/{random_id}")
        
        # O sistema deve retornar 404 Not Found conforme planejado no Swagger
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json())

if __name__ == "__main__":
    unittest.main()