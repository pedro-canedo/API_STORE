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
    """Cria um token de acesso JWT com o ID do usuário como payload.

    Args:
        user_id (int): ID do usuário.

    Returns:
        str: Token de acesso JWT.
    """
    payload = {"sub": user_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Obtém o usuário atual com base no token de acesso fornecido.

    Args:
        db (AsyncSession, optional): Sessão de banco de dados. Padrão: Depends(get_db).
        token (str, optional): Token de acesso JWT. Padrão: Depends(oauth2_scheme).

    Raises:
        HTTPException: Exceção HTTP com status code 401 ou 404.

    Returns:
        User: Usuário atual.
    """
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
    
def is_admin(user: User) -> bool:
    """Verifica se o usuário é um administrador.

    Args:
        user (User): Usuário a ser verificado.

    Returns:
        bool: Verdadeiro se o usuário é um administrador, Falso caso contrário.
    """
    return user.is_admin

def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtém o usuário atual se ele for um administrador.

    Args:
        current_user (User, optional): Usuário atual. Padrão: Depends(get_current_user).

    Raises:
        HTTPException: Exceção HTTP com status code 403 se o usuário atual não for um administrador.

    Returns:
        User: Usuário atual se ele for um administrador.
    """
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Acesso não permitido")
    return current_user
