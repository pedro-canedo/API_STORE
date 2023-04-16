from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.crud.category import create_category, get_category, get_categories, update_category, delete_category
from typing import List
from src.app.schemas.category import Category, CategoryCreate
from src.app.models import User
from src.app.deps.auth import get_current_user
from src.app.database.database import get_db

router = APIRouter()

@router.post("/", response_model=Category)
def create_category_endpoint(category: CategoryCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_category = create_category(db, category)
    return db_category

@router.get("/", response_model=List[Category])
def get_categories_endpoint(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_categories = get_categories(db)
    return db_categories

@router.get("/{category_id}", response_model=Category)
def get_category_endpoint(category_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_category = get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return db_category

@router.put("/{category_id}", response_model=Category)
def update_category_endpoint(category_id: int, updated_category: CategoryCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_category = get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    updated_db_category = update_category(db, category_id, updated_category)
    return updated_db_category

@router.delete("/{category_id}")
def delete_category_endpoint(category_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_category = get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    delete_category(db, category_id)
    return {"message": "Categoria excluída com sucesso"}