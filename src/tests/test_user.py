import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestUser(unittest.TestCase):

    def test_create_user(self):
        response = client.post("/users", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "test123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test User")
        self.assertEqual(response.json()["email"], "test@example.com")

    def test_read_user(self):
        response = client.get("/users/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test User")
        self.assertEqual(response.json()["email"], "test@example.com")
