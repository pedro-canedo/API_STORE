import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestProduct(unittest.TestCase):

    def test_create_product(self):
        response = client.post("/products", json={
            "name": "Test Product",
            "description": "This is a test product",
            "price": 10.99,
            "category_ids": [1]
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Product")
        self.assertEqual(response.json()["price"], 10.99)

    def test_read_product(self):
        response = client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Product")
        self.assertEqual(response.json()["price"], 10.99)
