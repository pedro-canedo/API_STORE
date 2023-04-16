from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.category import Category
from src.app.models import Product
from src.app.schemas.product import ProductCreate



def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(name=product.name, description=product.description, price=product.price)

    categories = db.query(Category).filter(Category.id.in_(product.categories)).all()

    db_product.categories.extend(categories)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: AsyncSession, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_productes(db: AsyncSession):
    return db.query(Product).all()

def update_product(db: AsyncSession, product_id: int, updated_product: ProductCreate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db_product.name = updated_product.name
    db_product.description = updated_product.description
    db_product.price = updated_product.price
    db_product.categories = db.query(Category).filter(Category.id.in_(updated_product.category_ids)).all()
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: AsyncSession, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db.delete(db_product)
    db.commit()