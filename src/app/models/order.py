from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, Table, CheckConstraint
from sqlalchemy.orm import relationship
from src.app.database.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    address_id = Column(Integer, ForeignKey("addresses.id", ondelete="CASCADE"))
    status = Column(String(50), nullable=False)
    order_date = Column(DateTime, nullable=False)

    __table_args__ = (
        CheckConstraint(status.in_(["Pendente", "Pago", "Enviado", "Entregue", "Cancelado"])),
    )
    
    user = relationship("User", back_populates="orders")
    address = relationship("Address", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")



class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")