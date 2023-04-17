import unittest
from src.app.schemas.category import CategoryBase, CategoryCreate, Category
from src.app.models.category import Category

class TestCategorySchemas(unittest.TestCase):
    def test_category_base(self):
        category = CategoryBase(name="Electronics")
        self.assertEqual(category.name, "Electronics")

    def test_category_create(self):
        category_create = CategoryCreate(name="Electronics")
        self.assertEqual(category_create.name, "Electronics")

    def test_category(self):
        category_data = {"id": 1, "name": "Electronics"}
        category = Category(**category_data)
        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "Electronics")



class TestCategoryModel(unittest.TestCase):
    def setUp(self):
        self.category = Category(name="Test Category")

    def test_create_category(self):
        self.assertEqual(self.category.name, "Test Category")