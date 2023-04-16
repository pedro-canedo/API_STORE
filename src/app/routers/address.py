from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.app.crud import address as address_crud
from src.app.schemas.address import Address, AddressCreate, AddressUpdate
from src.app.models import User
from src.app.deps.auth import get_current_admin_user, get_current_user
from src.app.database.database import get_db

router = APIRouter()

@router.get("/", response_model=List[Address])
def get_actual_user_addreess(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return address_crud.get_addresses_by_user_id(db, current_user.id)

@router.get("/{user_id}", response_model=List[Address])
def get_user_address_from_user_id(user_id: int, current_user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    addresses = address_crud.get_addresses_by_user_id(db, user_id)
    if not addresses:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return addresses


@router.post("/", response_model=Address)
def create_user_address(address: AddressCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return address_crud.create_address(db, address, current_user.id)

@router.put("/{address_id}", response_model=Address)
def update_user_address(address_id: int, address: AddressUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_address = address_crud.get_address_by_id(db, address_id)
    if not db_address or db_address.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return address_crud.update_address(db, address, address_id)

@router.delete("/{address_id}")
def delete_user_address(address_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_address = address_crud.get_address_by_id(db, address_id)
    if not db_address or db_address.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    address_crud.delete_address(db, address_id)
    return {"detail": "Endereço deletado com sucesso"}
