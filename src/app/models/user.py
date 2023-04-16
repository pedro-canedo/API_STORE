from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from src.app.database.database import  Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    addresses = relationship("Address", back_populates="user")
    orders = relationship("Order", back_populates="user")
