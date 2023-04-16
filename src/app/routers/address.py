from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.app.crud import address as address_crud
from src.app.schemas.address import Address, AddressCreate, AddressUpdate
from src.app.models import User
from src.app.auth import get_current_user
from src.app.database.database import get_db

router = APIRouter()

@router.get("/", response_model=List[Address])
def get_user_addresses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return address_crud.get_addresses(db, current_user.id)

@router.get("/{address_id}", response_model=Address)
def get_user_address(address_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    address = address_crud.get_address_by_id(db, address_id)
    if not address or address.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return address

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
