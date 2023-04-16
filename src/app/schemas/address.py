from pydantic import BaseModel
from typing import Optional

class AddressBase(BaseModel):
    description: str
    postal_code: str
    street: str
    complement: Optional[str]
    neighborhood: str
    city: str
    state: str

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
        
class AddressUpdate(AddressBase):
    pass

class AddressFromCEP(AddressBase):
    pass