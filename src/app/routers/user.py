import jwt
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.crud.users import get_all_users, get_user_by_email, password_compare, password_encode
from src.app.deps.auth import create_access_token, get_current_admin_user, get_current_user
from src.app.schemas import user as user_schema
from src.app.models import User
import os
from src.app.database.database import get_db


router = APIRouter()



@router.post("/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = get_user_by_email(user.email, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    hashed_password = password_encode(user.password)
    db_user = User(name=user.name, email=user.email,
                   password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/all-users", response_model=List[user_schema.User])
def list_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado")
    users = get_all_users(db)
    return users


@router.post("/login")
def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    db_user = get_user_by_email(email, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário ainda não possui cadastro")
    if not password_compare(password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")
    access_token = create_access_token(db_user.id)
    return {"access_token": access_token}


@router.post("/validate-token")
def validate_token(current_user: User = Depends(get_current_user)):
    return {"message": "Token válido"}