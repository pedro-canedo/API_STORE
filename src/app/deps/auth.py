import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from src.app.models import User
from src.app.database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import os

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

oauth2_scheme = HTTPBearer()


def create_access_token(user_id: int):
    payload = {"sub": user_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token = token.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
def is_admin

