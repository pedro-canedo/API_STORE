from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
import os
from src.app.models import User
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer
from cryptography.fernet import Fernet
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from passlib.hash import bcrypt

def get_user_by_email(email: str, db: AsyncSession):
    """
    Busca um usuário pelo email no banco de dados.
    
    Args:
        email (str): Email do usuário a ser buscado.
        db (AsyncSession): Sessão de banco de dados.

    Returns:
        User: Usuário encontrado ou None se nenhum usuário for encontrado.
    """
    ...
    stmt = select(User).filter(User.email == email)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def create_access_token(user_id: int):
    """
    Cria um token de acesso para um usuário.

    Args:
        user_id (int): ID do usuário para o qual o token será criado.

    Returns:
        str: Token de acesso gerado.
    """
    access_token_expire_minutes = 30
    expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)
    to_encode = {"user_id": user_id, "exp": expire}
    secret_key = os.environ.get("SECRET_KEY")
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt

def load_access_token(token: str):
    """
    Decodifica um token de acesso e retorna o ID do usuário.

    Args:
        token (str): Token de acesso a ser decodificado.

    Returns:
        int: ID do usuário associado ao token ou None se o token não puder ser decodificado.
    """
    try:
        secret_key = os.environ.get("SECRET_KEY")
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload["user_id"]
        return user_id
    except:
        return None
    
def get_all_users(db: AsyncSession):
    """
    Retorna uma lista de todos os usuários no banco de dados.

    Args:
        db (AsyncSession): Sessão de banco de dados.

    Returns:
        List[User]: Lista de usuários encontrados.
    """
    stmt = select(User)
    result = db.execute(stmt)
    return result.scalars().all()

def password_encode(password: str):
    """
    Codifica uma senha de usuário.

    Args:
        password (str): Senha de usuário a ser codificada.

    Returns:
        str: Senha codificada.
    """
    return bcrypt.hash(password)

def password_compare(password: str, hashed_password: str) -> bool:
    """
    Compara uma senha de usuário com sua versão codificada.

    Args:
        password (str): Senha em texto plano.
        hashed_password (str): Senha codificada.

    Returns:
        bool: True se a senha corresponder à sua versão codificada, False caso contrário.
    """
    return bcrypt.verify(password, hashed_password)


def password_decode(hashed_password: str) -> str:
    """
    Decodifica uma senha previamente codificada.

    Args:
        hashed_password (str): Senha codificada a ser decodificada.

    Returns:
        str: Senha decodificada em texto plano.
    """
    key = os.environ.get('SECRET_KEY', b'salt_test')
    f = Fernet(key)
    return f.decrypt(hashed_password.encode('utf-8')).decode('utf-8')

