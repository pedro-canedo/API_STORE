from datetime import datetime
import unittest
from src.app.schemas.order import OrderBase, OrderCreate, OrderItemCreate, OrderItem


class TestOrderItemSchemas(unittest.TestCase):
    def test_order_item_create(self):
        order_item_data = {"product_id": 1, "price": 10.0, "quantity": 2}
        order_item = OrderItemCreate(**order_item_data)
        self.assertEqual(order_item.product_id, 1)
        self.assertEqual(order_item.price, 10.0)
        self.assertEqual(order_item.quantity, 2)

    def test_order_item(self):
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
        order_item = OrderItemBase(product_id=1, quantity=5)
        self.assertEqual(order_item.product_id, 1)
        self.assertEqual(order_item.quantity, 5)
        self.assertIsNone(order_item.price)
        
    def test_create_order_item_create(self):
        order_item_create = OrderItemCreate(product_id=1, quantity=5, price=10.0)
        self.assertEqual(order_item_create.product_id, 1)
        self.assertEqual(order_item_create.quantity, 5)
        self.assertEqual(order_item_create.price, 10.0)
        
    def test_create_order_item(self):
        order_item = OrderItem(id=1, product_id=1, quantity=5, price=10.0)
        self.assertEqual(order_item.id, 1)
        self.assertEqual(order_item.product_id, 1)
        self.assertEqual(order_item.quantity, 5)
        self.assertEqual(order_item.price, 10.0)