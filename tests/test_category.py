import unittest
from src.app.schemas.category import CategoryBase, CategoryCreate, Category
from src.app.models.category import Category

class TestCategorySchemas(unittest.TestCase):
    def test_category_base(self):
        """
        Testa a criação de um objeto CategoryBase com base nos dados fornecidos.
        Verifica se o atributo 'name' do objeto criado corresponde ao valor esperado.
        """
        category = CategoryBase(name="Electronics")
        self.assertEqual(category.name, "Electronics")

    def test_category_create(self):
        """
        Testa a criação de um objeto CategoryCreate com base nos dados fornecidos.
        Verifica se o atributo 'name' do objeto criado corresponde ao valor esperado.
        """
        category_create = CategoryCreate(name="Electronics")
        self.assertEqual(category_create.name, "Electronics")

    def test_category(self):
        """
        Testa a criação de um objeto Category com base nos dados fornecidos.
        Verifica se os atributos 'id' e 'name' do objeto criado correspondem aos valores esperados.
        """
        category_data = {"id": 1, "name": "Electronics"}
        category = Category(**category_data)
        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "Electronics")



class TestCategoryModel(unittest.TestCase):
    def setUp(self):
        self.category = Category(name="Test Category")

    def test_create_category(self):
        """
        Testa a criação de um objeto Category (modelo) com base nos dados fornecidos.
        Verifica se o atributo 'name' do objeto criado corresponde ao valor esperado.
        """
        self.assertEqual(self.category.name, "Test Category")