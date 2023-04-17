import unittest
from src.app.schemas.address import Address, AddressCreate, AddressUpdate


class TestAddressSchemas(unittest.TestCase):
    def test_address_create(self):
        address_data = {
            "description": "Casa",
            "postal_code": "12345678",
            "street": "Rua dos Bobos",
            "complement": "Apto 123",
            "neighborhood": "Bairro Feliz",
            "city": "São Paulo",
            "state": "SP",
        }
        address = AddressCreate(**address_data)
        self.assertEqual(address.description, "Casa")
        self.assertEqual(address.postal_code, "12345678")
        self.assertEqual(address.street, "Rua dos Bobos")
        self.assertEqual(address.complement, "Apto 123")
        self.assertEqual(address.neighborhood, "Bairro Feliz")
        self.assertEqual(address.city, "São Paulo")
        self.assertEqual(address.state, "SP")

    def test_address(self):
        address_data = {
            "id": 1,
            "description": "Casa",
            "postal_code": "12345678",
            "street": "Rua dos Bobos",
            "complement": "Apto 123",
            "neighborhood": "Bairro Feliz",
            "city": "São Paulo",
            "state": "SP",
            "user_id": 1,
        }
        address = Address(**address_data)
        self.assertEqual(address.id, 1)
        self.assertEqual(address.description, "Casa")
        self.assertEqual(address.postal_code, "12345678")
        self.assertEqual(address.street, "Rua dos Bobos")
        self.assertEqual(address.complement, "Apto 123")
        self.assertEqual(address.neighborhood, "Bairro Feliz")
        self.assertEqual(address.city, "São Paulo")
        self.assertEqual(address.state, "SP")
        self.assertEqual(address.user_id, 1)

    def test_address_update(self):
        address_data = {
            "description": "Casa",
            "postal_code": "12345678",
            "street": "Rua dos Bobos",
            "complement": "Apto 123",
            "neighborhood": "Bairro Feliz",
            "city": "São Paulo",
            "state": "SP",
        }
        address_update = AddressUpdate(**address_data)
        self.assertEqual(address_update.description, "Casa")
        self.assertEqual(address_update.postal_code, "12345678")
        self.assertEqual(address_update.street, "Rua dos Bobos")
        self.assertEqual(address_update.complement, "Apto 123")
        self.assertEqual(address_update.neighborhood, "Bairro Feliz")
        self.assertEqual(address_update.city, "São Paulo")
        self.assertEqual(address_update.state, "SP")
