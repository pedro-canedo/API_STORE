from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models import Category
from src.app.schemas.category import CategoryCreate

def create_category(db: AsyncSession, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    return db_category

def get_category(db: AsyncSession, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: AsyncSession):
    return db.query(Category).all()

def update_category(db: AsyncSession, category_id: int, updated_category: CategoryCreate):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    db_category.name = updated_category.name
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: AsyncSession, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    db.delete(db_category)
    db.commit()