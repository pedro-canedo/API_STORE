import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestOrder(unittest.TestCase):

    def test_create_order(self):
        response = client.post("/orders", json={
            "user_id": 1,
            "address_id": 1,
            "status": "Pendente",
            "order_date": "2023-05-01T10:30:00",
            "items": [
                {
                    "product_id": 1,
                    "price": 10.99,
                    "quantity": 2
                }
            ]
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "Pendente")
        self.assertEqual(response.json()["order_date"], "2023-05-01T10:30:00")

    def test_read_order(self):
        response = client.get("/orders/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "Pendente")
        self.assertEqual(response.json()["order_date"], "2023-05-01T10:30:00")
