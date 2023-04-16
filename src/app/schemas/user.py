
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from .address import Address

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    addresses: Optional[List[Address]]

    class Config:
        orm_mode = True
        
class TokenData(BaseModel):
    user_id: int
    expire: datetime