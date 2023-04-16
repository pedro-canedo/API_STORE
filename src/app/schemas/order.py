from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

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

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    items: List[OrderItem]

    class Config:
        orm_mode = True
class OrderItemCreateInput(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    price: float

class OrderCreateInput(BaseModel):
    address_id: int
    order_date: datetime
    items: List[OrderItemCreateInput]
    
class OrderCreate(OrderBase):
    items: List[OrderItemCreate]
    
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