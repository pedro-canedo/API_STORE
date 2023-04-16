from datetime import datetime
from src.app.schemas import order as order_schema
from fastapi import HTTPException
from src.app.crud import product as product_crud
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas.order import OrderCreate
from sqlalchemy.orm import joinedload, subqueryload
from sqlalchemy import select
from src.app.models import Order, OrderItem

def create_order(db: AsyncSession, order: order_schema.OrderCreateInput, current_user_id: int):
    # Calcular o preço dos itens
    items = []
    for item_input in order.items:
        product = product_crud.get_product(db, item_input.product_id)
        if product is None:
            raise HTTPException(status_code=404, detail=f"Produto com ID {item_input.product_id} não encontrado")
        price = product.price * item_input.quantity
        item = OrderItem(product_id=item_input.product_id, price=price, quantity=item_input.quantity)
        items.append(item)

    db_order = Order(
        user_id=current_user_id,
        address_id=order.address_id,
        status="Pendente",
        order_date=order.order_date,
        items=items
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: AsyncSession, order_id: int, new_status: str):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail=f"Pedido com ID {order_id} não encontrado")
    db_order.status = new_status
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders_by_user_id(db: AsyncSession, user_id: int):
    stmt = (
        select(Order)
        .filter(Order.user_id == user_id)
        .options(subqueryload(Order.items).subqueryload(OrderItem.product))
    )
    result = db.execute(stmt)
    return result.scalars().all()


def get_orders_by_date_range(db: AsyncSession, user_id: int, start_date: datetime, end_date: datetime):
    stmt = (
        select(Order)
        .filter(Order.user_id == user_id)
        .filter(Order.order_date.between(start_date, end_date))
        .options(joinedload(Order.items).joinedload(OrderItem.product))
    )
    result = db.execute(stmt)
    return result.scalars().all()

def get_order(db: AsyncSession, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def update_order(db: AsyncSession, order_id: int, updated_order: OrderCreate):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    db_order.status = updated_order.status
    db_order.order_date = updated_order.order_date
    db_order.address_id = updated_order.address_id
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: AsyncSession, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    db.delete(db_order)
    db.commit()
