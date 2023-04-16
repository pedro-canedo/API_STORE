from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.crud.cep import get_address_by_postal_code
from src.app.schemas.address import AddressFromCEP
from src.app.models import User
from src.app.auth import get_current_user
from src.app.database.database import get_db

router = APIRouter()

@router.get("/cep/{postal_code}", response_model=AddressFromCEP)
def get_address(postal_code: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    address_data = get_address_by_postal_code(postal_code)
    if not address_data:
        raise HTTPException(status_code=404, detail="CEP não encontrado")
    mapped_data = {
        "description": "",
        "postal_code": address_data["cep"],
        "street": address_data["logradouro"],
        "neighborhood": address_data["bairro"],
        "city": address_data["localidade"],
        "state": address_data["uf"]
    }
    return AddressFromCEP(**mapped_data)
