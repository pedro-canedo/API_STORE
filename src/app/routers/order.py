from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.crud import order as order_crud
from src.app.schemas import order as order_schema
from src.app.models import User
from src.app.deps.auth import get_current_active_user, get_current_user
from src.app.database.database import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=order_schema.Order)
def create_order(order: order_schema.OrderCreateInput, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return order_crud.create_order(db, order, current_user_id=current_user.id)



@router.get("/", response_model=List[order_schema.Order])
def list_orders(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return order_crud.get_orders_by_user_id(db, current_user.id)


@router.put("/orders/{order_id}/status", response_model=order_schema.Order, tags=["orders"])
async def update_order_status(
    order_id: int,
    status: order_schema.OrderStatus,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await order_crud.update_order_status(db, order_id, status.value)


@router.get("/date-range", response_model=List[order_schema.Order])
def list_orders_by_date_range(start_date: datetime, end_date: datetime, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = order_crud.get_orders_by_date_range(db, current_user.id, start_date, end_date) 
    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail="Não foram encontrados pedidos para este período de data")

@router.get("/{order_id}", response_model=order_schema.Order)
def get_order_endpoint(order_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_order = order_crud.get_order(db, order_id)
    if not db_order or db_order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return db_order

@router.put("/{order_id}", response_model=order_schema.Order)
def update_order_endpoint(order_id: int, updated_order: order_schema.OrderCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_order = order_crud.get_order(db, order_id)
    if not db_order or db_order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    updated_db_order = order_crud.update_order(db, order_id, updated_order)
    return updated_db_order

@router.delete("/{order_id}")
def delete_order_endpoint(order_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_order = order_crud.get_order(db, order_id)
    if not db_order or db_order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    order_crud.delete_order(db, order_id)
    return {"message": "Pedido excluído com sucesso"}
