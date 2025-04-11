from argon2 import PasswordHasher, exceptions
from datetime import datetime, timedelta
from jose import jwt
from app.infrastructure.config import settings

ph = PasswordHasher()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except exceptions.VerifyMismatchError:
        return False

def create_access_token(data: dict, expires_at: int | None = None):
    to_encode = data.copy()

    if not expires_at:
       expires = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
       expires_at = int(expires.timestamp())

    to_encode.update({"exp": expires_at})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt