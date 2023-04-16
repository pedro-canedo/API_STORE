from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.crud.product import create_product, delete_product, get_product, get_productes, update_product
from src.app.auth import get_current_user
from src.app.schemas.product import Product, ProductCreate
from src.app.models import User
from src.app.database.database import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=Product)
def create_product_endpoint(product: ProductCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_product = create_product(db, product)
    return db_product


@router.get("/", response_model=List[Product])
def get_products_endpoint(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_products = get_productes(db)
    return db_products

@router.get("/{product_id}", response_model=Product)
def get_product_endpoint(product_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_product

@router.put("/{product_id}", response_model=Product)
def update_product_endpoint(product_id: int, updated_product: ProductCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    updated_db_product = update_product(db, product_id, updated_product)
    return updated_db_product

@router.delete("/{product_id}")
def delete_product_endpoint(product_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    delete_product(db, product_id)
    return {"message": "Produto excluído com sucesso"}