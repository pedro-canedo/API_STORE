from datetime import datetime
from src.app.schemas import order as order_schema
from fastapi import HTTPException
from src.app.crud import product as product_crud
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas.order import OrderCreate
from sqlalchemy import func
from src.app.models import Order, Product, User, Address
from sqlalchemy import and_
from sqlalchemy.orm import joinedload, subqueryload
from sqlalchemy import select
from src.app.models.order import Order, OrderItem

def create_order(db: AsyncSession, order: order_schema.OrderCreateInput, current_user_id: int):
    """
    Cria um novo pedido no banco de dados.
    :param db: Sessão do banco de dados.
    :param order: Objeto contendo as informações do novo pedido.
    :param current_user_id: ID do usuário que está fazendo o pedido.
    :return: Retorna o objeto do pedido criado.
    :raises HTTPException: Se um produto com o ID especificado não for encontrado.
    """
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
    """
    Atualiza o status de um pedido no banco de dados.
    :param db: Sessão do banco de dados.
    :param order_id: ID do pedido a ser atualizado.
    :param new_status: Novo status do pedido.
    :return: Retorna o objeto do pedido atualizado.
    :raises HTTPException: Se o pedido com o ID especificado não for encontrado.
    """
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail=f"Pedido com ID {order_id} não encontrado")
    db_order.status = new_status
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders_by_user_id(db: AsyncSession, user_id: int):
    """
    Retorna uma lista de pedidos pertencentes ao usuário especificado.
    :param db: Sessão do banco de dados.
    :param user_id: ID do usuário.
    :return: Retorna uma lista de objetos de pedidos.
    """
    stmt = (
        select(Order)
        .filter(Order.user_id == user_id)
        .options(subqueryload(Order.items).subqueryload(OrderItem.product))
    )
    result = db.execute(stmt)
    return result.scalars().all()


def get_orders_by_date_range(db: AsyncSession, start_date: datetime, end_date: datetime):
    """
    Retorna uma lista de pedidos que foram feitos dentro do intervalo de datas especificado.
    :param db: Sessão do banco de dados.
    :param start_date: Data de início do intervalo de datas.
    :param end_date: Data final do intervalo de datas.
    :return: Retorna uma lista de objetos de pedidos.
    """
    stmt = (
        select(Order)
        .filter(
            Order.order_date.between(
                func.date(start_date) + func.current_time(),
                func.date(end_date) + func.current_time()
            )
        )
    )
    result = db.execute(stmt)
    return result.scalars().all()


def get_order(db: AsyncSession, order_id: int):
    """
    Retorna um objeto de pedido com base no ID especificado.
    :param db: Sessão do banco de dados.
    :param order_id: ID do pedido a ser retornado.
    :return: Retorna o objeto do pedido com o ID especificado, se encontrado.
    """
    return db.query(Order).filter(Order.id == order_id).first()

def update_order(db: AsyncSession, order_id: int, updated_order: OrderCreate):
    """
    Atualiza um pedido no banco de dados com base no ID especificado.
    :param db: Sessão do banco de dados.
    :param order_id: ID do pedido a ser atualizado.
    :param updated_order: Objeto contendo as informações atualizadas do pedido.
    :return: Retorna o objeto do pedido atualizado.
    """
    db_order = db.query(Order).filter(Order.id == order_id).first()
    db_order.status = updated_order.status
    db_order.order_date = updated_order.order_date
    db_order.address_id = updated_order.address_id
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: AsyncSession, order_id: int):
    """
    Exclui um pedido do banco de dados com base no ID especificado.
    :param db: Sessão do banco de dados.
    :param order_id: ID do pedido a ser excluído.
    :return: Retorna True se o pedido foi excluído com sucesso e False caso contrário.
    """
    db_order = db.query(Order).filter(Order.id == order_id).first()
    db.delete(db_order)
    db.commit()
    

def get_order_details(db: AsyncSession, order_id: int, user_id: int):
    db_order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not db_order:
        return None
    stmt = (
        select(Order, Product, User, OrderItem.price, OrderItem.quantity)
        .select_from(Order)
        .join(OrderItem, OrderItem.order_id == Order.id)
        .join(Product, Product.id == OrderItem.product_id)
        .join(User, User.id == Order.user_id)
        # .join(Address, Address.user_id == Order.user_id)
        .where(and_(Order.id == order_id, Order.user_id == user_id))
    )
    result = db.execute(stmt)

    if result:
        order_details = []
        total_value = 0
        user_address = None

        for order, product, user, price, quantity in result.all():
            order_details.append(
                order_schema.OrderProductDetail(
                    id=order.id,
                    product_id=product.id,
                    product=product,
                    price=price * quantity,
                    quantity=quantity
                )
            )

            if not user_address:
                user_address = user.addresses

        order_detail = order_schema.OrderDetail(
            **{k: v for k, v in order.__dict__.items() if k != '_sa_instance_state'},
            products=order_details,
            total_value=total_value,
            user_address=user_address
        )


        return order_detail
    else:
        return None

