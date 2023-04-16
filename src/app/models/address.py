from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.app.database.database import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    description = Column(String(255), nullable=False)
    postal_code = Column(String(10), nullable=False)
    street = Column(String(255), nullable=False)
    complement = Column(String(255))
    neighborhood = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(2), nullable=False)

    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="address")
