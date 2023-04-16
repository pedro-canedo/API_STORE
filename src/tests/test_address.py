import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAddress(unittest.TestCase):

    def test_create_address(self):
        response = client.post("/addresses", json={
            "user_id": 1,
            "description": "Home",
            "postal_code": "12345-678",
            "street": "Rua Teste",
            "complement": "Apto 123",
            "neighborhood": "Bairro Teste",
            "city": "Cidade Teste",
            "state": "SP"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "Home")
        self.assertEqual(response.json()["postal_code"], "12345-678")

    def test_read_address(self):
        response = client.get("/addresses/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "Home")
        self.assertEqual(response.json()["postal_code"], "12345-678")
