from datetime import datetime
import unittest
from src.app.schemas.order import OrderBase, OrderCreate, OrderItemCreate, OrderItem


class TestOrderItemSchemas(unittest.TestCase):
    def test_order_item_create(self):
        """
        Este teste verifica se um objeto OrderItemCreate é criado corretamente com os dados fornecidos. Ele compara os atributos do objeto criado com os valores esperados (product_id, price e quantity).
        """
        order_item_data = {"product_id": 1, "price": 10.0, "quantity": 2}
        order_item = OrderItemCreate(**order_item_data)
        self.assertEqual(order_item.product_id, 1)
        self.assertEqual(order_item.price, 10.0)
        self.assertEqual(order_item.quantity, 2)

    def test_order_item(self):
        """
        Este teste verifica se um objeto OrderItem é criado corretamente com os dados fornecidos. Ele compara os atributos do objeto criado com os valores esperados (id, product_id, price e quantity).
        """
        order_item_data = {"id": 1, "product_id": 1, "price": 10.0, "quantity": 2}
        order_item = OrderItem(**order_item_data)
        self.assertEqual(order_item.id, 1)
        self.assertEqual(order_item.product_id, 1)
        self.assertEqual(order_item.price, 10.0)
        self.assertEqual(order_item.quantity, 2)


from src.app.schemas import OrderItemBase

class TestOrderItemBase(unittest.TestCase):
    def setUp(self):
        self.item_data = {"product_id": 1, "price": 10.0, "quantity": 5}
    
    def test_create_order_item_base(self):
        """
        Este teste verifica se um objeto OrderItemBase é criado corretamente com os dados fornecidos. Ele compara os atributos do objeto criado com os valores esperados (product_id e quantity) e verifica se o atributo "price" é None.
        """
        order_item = OrderItemBase(product_id=1, quantity=5)
        self.assertEqual(order_item.product_id, 1)
        self.assertEqual(order_item.quantity, 5)
        self.assertIsNone(order_item.price)
        
    def test_create_order_item_create(self):
        """
        Este teste é semelhante ao test_order_item_create na classe TestOrderItemSchemas. Ele verifica se um objeto OrderItemCreate é criado corretamente com os dados fornecidos e compara os atributos do objeto criado com os valores esperados (product_id, price e quantity).
        """
        order_item_create = OrderItemCreate(product_id=1, quantity=5, price=10.0)
        self.assertEqual(order_item_create.product_id, 1)
        self.assertEqual(order_item_create.quantity, 5)
        self.assertEqual(order_item_create.price, 10.0)
        
    def test_create_order_item(self):
        """
        Este teste é semelhante ao test_order_item na classe TestOrderItemSchemas. Ele verifica se um objeto OrderItem é criado corretamente com os dados fornecidos e compara os atributos do objeto criado com os valores esperados (id, product_id, price e quantity).
        """
        order_item = OrderItem(id=1, product_id=1, quantity=5, price=10.0)
        self.assertEqual(order_item.id, 1)
        self.assertEqual(order_item.product_id, 1)
        self.assertEqual(order_item.quantity, 5)
        self.assertEqual(order_item.price, 10.0)