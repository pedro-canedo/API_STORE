from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum
from src.app.schemas.product import Product
from src.app.schemas.user import UserAddress
from src.app.schemas.address import Address

class OrderItemBase(BaseModel):
    product_id: int
    price: float = Field(default=None, extra={"readOnly": True})
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int = Field(default=None, extra={"readOnly": True})
    address_id: int
    status: str
    order_date: datetime
    items: List[OrderItem] = []

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    items: List[OrderItem]

    class Config:
        orm_mode = True


class OrderProductDetail(BaseModel):
    id: int
    product_id: int
    price: float
    quantity: int
    product: Product

class OrderDetail(BaseModel):
    id: int
    user_id: int
    address_id: int
    status: str
    order_date: datetime
    products: List[OrderProductDetail]
    total_value: float
    user_address: List[Address]

class OrderItemCreateInput(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    price: float

class OrderCreateInput(BaseModel):
    address_id: int
    order_date: datetime
    items: List[OrderItemCreateInput]

class OrderStatus(str, Enum):
    PENDING = "Pendente"
    PAID = "Pago"
    SHIPPED = "Enviado"
    DELIVERED = "Entregue"
    CANCELED = "Cancelado"

class OrderCreateInput(BaseModel):
    address_id: int
    order_date: datetime
    items: List[OrderItemCreateInput]
