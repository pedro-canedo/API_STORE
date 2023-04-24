import unittest
from unittest.mock import Mock, patch
from src.app.models.order import Order
from src.app.models import User
from src.app.routers import user
import unittest
from datetime import datetime
from src.app.schemas.user import UserBase, UserCreate, User, TokenData, UserAddress
from src.app.schemas.address import Address

class TestUserSchemas(unittest.TestCase):
    def test_user_base(self):
        """
        Testa a criação de um objeto UserBase com base nos dados fornecidos.
        Verifica se os atributos do objeto criado (name e email) correspondem aos valores esperados.
        """
        user_data = {"name": "John Doe", "email": "johndoe@example.com"}
        user = UserBase(**user_data)
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "johndoe@example.com")

    def test_user_create(self):
        """
        Testa a criação de um objeto UserCreate com base nos dados fornecidos.
        Verifica se os atributos do objeto criado (name, email e password) correspondem aos valores esperados.
        """
        user_data = {"name": "John Doe", "email": "johndoe@example.com", "password": "password"}
        user_create = UserCreate(**user_data)
        self.assertEqual(user_create.name, "John Doe")
        self.assertEqual(user_create.email, "johndoe@example.com")
        self.assertEqual(user_create.password, "password")

    def test_user(self):
        """
        Testa a criação de um objeto User com base nos dados fornecidos.
        Verifica se os atributos do objeto criado (id, name e email) correspondem aos valores esperados.
        """
        user_data = {"id": 1, "name": "John Doe", "email": "johndoe@example.com"}
        user = User(**user_data)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "johndoe@example.com")

    def test_token_data(self):
        """
        Testa a criação de um objeto TokenData com base nos dados fornecidos.
        Verifica se os atributos do objeto criado (user_id e expire) correspondem aos valores esperados e se 'expire' é uma instância de datetime.
        """
        token_data = {"user_id": 1, "expire": datetime.now()}
        token = TokenData(**token_data)
        self.assertEqual(token.user_id, 1)
        self.assertIsInstance(token.expire, datetime)

    def test_user_address(self):
        """
        Testa a criação de um objeto UserAddress com base nos dados fornecidos.
        Verifica se os atributos do objeto criado (street, city, state, country e zip_code) correspondem aos valores esperados.
        """
        address_data = {"street": "123 Main St", "city": "Springfield", "state": "IL", "country": "USA", "zip_code": "12345"}
        address = UserAddress(**address_data)
        self.assertEqual(address.street, "123 Main St")
        self.assertEqual(address.city, "Springfield")
        self.assertEqual(address.state, "IL")
        self.assertEqual(address.country, "USA")
        self.assertEqual(address.zip_code, "12345")

    def test_user_address_association(self):
        """
        Testa a associação entre um objeto User e objetos Address.
        Verifica se um objeto User pode ter uma lista de objetos Address associados a ele e se essa lista pode ser atualizada corretamente.
        """
        user_data = {"id": 1, "name": "John Doe", "email": "johndoe@example.com", "addresses": []}
        user = User(**user_data)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertIsInstance(user.addresses, list)
        self.assertEqual(len(user.addresses), 0)

        address_data = {"id": 1, "description": "Home", "postal_code": "12345", "street": "123 Main St", "complement": None, "neighborhood": "Downtown", "city": "Springfield", "state": "IL", "user_id": 1}
        address = Address(**address_data)

        user_data["addresses"].append(address)
        user_with_address = User(**user_data)
        self.assertEqual(user_with_address.id, 1)
        self.assertEqual(user_with_address.name, "John Doe")
        self.assertEqual(user_with_address.email, "johndoe@example.com")
        self.assertIsInstance(user_with_address.addresses, list)
        self.assertEqual(len(user_with_address.addresses), 1)
        self.assertIsInstance(user_with_address.addresses[0], Address)



if __name__ == "__main__":
    unittest.main()
