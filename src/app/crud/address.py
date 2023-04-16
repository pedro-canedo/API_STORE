from typing import List
from sqlalchemy.orm import Session
from src.app.models import Address
from src.app.schemas.address import AddressCreate, AddressUpdate

def get_addresses_by_user_id(db: Session, user_id: int) -> List[Address]:
    return db.query(Address).filter(Address.user_id == user_id).all()

def get_address_by_id(db: Session, address_id: int) -> Address:
    return db.query(Address).filter(Address.id == address_id).first()

def create_address(db: Session, address: AddressCreate, user_id: int) -> Address:
    new_address = Address(**address.dict(), user_id=user_id)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

def update_address(db: Session, address: AddressUpdate, address_id: int) -> Address:
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
    db_address = get_address_by_id(db, address_id)
    if not db_address:
        return False

    db.delete(db_address)
    db.commit()

    return True
