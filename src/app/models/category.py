from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.app.database.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

    products = relationship("Product", secondary="products_categories", back_populates="categories")
    
