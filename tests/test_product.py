import unittest
from src.app.schemas.product import Product, ProductCreate


class TestProductSchema(unittest.TestCase):
    def test_product_schema(self):
        """
        Testa a criação de um objeto Product com base nos dados fornecidos.
        Verifica se os atributos do objeto criado (id, name, description, price e category_ids)
        correspondem aos valores esperados.
        """
        product_dict = {
            "id": 1,
            "name": "Product Name",
            "description": "Product Description",
            "price": 99.99,
            "category_ids": [1, 2, 3]
        }
        product = Product(**product_dict)
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, "Product Name")
        self.assertEqual(product.description, "Product Description")
        self.assertEqual(product.price, 99.99)
        self.assertEqual(product.category_ids, [1, 2, 3])

    def test_product_create_schema(self):
        """
        Testa a criação de um objeto ProductCreate com base nos dados fornecidos.
        Verifica se os atributos do objeto criado (name, description, price e category_ids)
        correspondem aos valores esperados.
        """
        product_create_dict = {
            "name": "Product Name",
            "description": "Product Description",
            "price": 99.99,
            "category_ids": [1, 2, 3]
        }
        product_create = ProductCreate(**product_create_dict)
        self.assertEqual(product_create.name, "Product Name")
        self.assertEqual(product_create.description, "Product Description")
        self.assertEqual(product_create.price, 99.99)
        self.assertEqual(product_create.category_ids, [1, 2, 3])
