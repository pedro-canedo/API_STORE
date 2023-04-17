from typing import List
from sqlalchemy.orm import Session
from src.app.models import Address
from src.app.schemas.address import AddressCreate, AddressUpdate

def get_addresses_by_user_id(db: Session, user_id: int) -> List[Address]:
    """
    Retorna uma lista de endereços correspondentes a um determinado ID de usuário.

    Args:
    - db (Session): sessão do banco de dados.
    - user_id (int): ID do usuário cujos endereços serão retornados.

    Returns:
    - List[Address]: lista de endereços correspondentes ao ID do usuário.

    Raises:
    - None.
    """
    return db.query(Address).filter(Address.user_id == user_id).all()

def get_address_by_id(db: Session, address_id: int) -> Address:
    """
    Retorna um único endereço com base em seu ID.

    Args:
    - db (Session): sessão do banco de dados.
    - address_id (int): ID do endereço a ser retornado.

    Returns:
    - Address: endereço correspondente ao ID fornecido.

    Raises:
    - None.
    """
    return db.query(Address).filter(Address.id == address_id).first()

def create_address(db: Session, address: AddressCreate, user_id: int) -> Address:
    """
    Cria um novo endereço no banco de dados.

    Args:
    - db (Session): sessão do banco de dados.
    - address (AddressCreate): dados do endereço a serem criados.
    - user_id (int): ID do usuário proprietário do endereço.

    Returns:
    - Address: endereço criado.

    Raises:
    - None.
    """
    new_address = Address(**address.dict(), user_id=user_id)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

def update_address(db: Session, address: AddressUpdate, address_id: int) -> Address:
    """
    Atualiza um endereço existente no banco de dados.

    Args:
    - db (Session): sessão do banco de dados.
    - address (AddressUpdate): dados do endereço a serem atualizados.
    - address_id (int): ID do endereço a ser atualizado.

    Returns:
    - Address: endereço atualizado.

    Raises:
    - None.
    """
    db_address = get_address_by_id(db, address_id)
    if not db_address:
        return None

    for key, value in address.dict().items():
        if value is not None:
            setattr(db_address, key, value)

    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    return db_address

def delete_address(db: Session, address_id: int) -> bool:
    """
    Exclui um endereço existente no banco de dados.

    Args:
    - db (Session): sessão do banco de dados.
    - address_id (int): ID do endereço a ser excluído.

    Returns:
    - bool: True se o endereço foi excluído com sucesso, False se o endereço não existe.

    Raises:
    - None.
    """
    db_address = get_address_by_id(db, address_id)
    if not db_address:
        return False

    db.delete(db_address)
    db.commit()

    return True
