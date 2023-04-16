from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models import Order, OrderItem
from src.app.schemas.order import OrderCreate
from sqlalchemy import select

def create_order(db: AsyncSession, order: OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.flush()

    for item in order.items:
        db_item = OrderItem(order_id=db_order.id, **item.dict())
        db.add(db_item)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders_by_user_id(db: AsyncSession, user_id: int):
    stmt = select(Order).filter(Order.user_id == user_id)
    result = db.execute(stmt)
    return result.scalars().all()

def get_orders_by_date_range(db: AsyncSession, user_id: int, start_date: datetime, end_date: datetime):
    stmt = (
        select(Order)
        .filter(Order.user_id == user_id)
        .filter(Order.order_date.between(start_date, end_date))
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
