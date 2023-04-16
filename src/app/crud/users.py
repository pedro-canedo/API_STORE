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
    stmt = select(User).filter(User.email == email)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def create_access_token(user_id: int):
    access_token_expire_minutes = 30
    expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)
    to_encode = {"user_id": user_id, "exp": expire}
    secret_key = os.environ.get("SECRET_KEY")
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt

def load_access_token(token: str):
    try:
        secret_key = os.environ.get("SECRET_KEY")
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload["user_id"]
        return user_id
    except:
        return None
    
def get_all_users(db: AsyncSession):
    stmt = select(User)
    result = db.execute(stmt)
    return result.scalars().all()

def password_encode(password: str):
    return bcrypt.hash(password)

def password_compare(password: str, hashed_password: str) -> bool:
    return bcrypt.verify(password, hashed_password)


def password_decode(hashed_password: str) -> str:
    key = os.environ.get('SECRET_KEY', b'salt_test')
    f = Fernet(key)
    return f.decrypt(hashed_password.encode('utf-8')).decode('utf-8')

