import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestCategory(unittest.TestCase):

    def test_create_category(self):
        response = client.post("/categories", json={
            "name": "Test Category"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Category")

    def test_read_category(self):
        response = client.get("/categories/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Category")
