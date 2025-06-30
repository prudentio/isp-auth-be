from typing import Annotated
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.exceptions import CustomHTTPException
from app.infrastructure.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/access-token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise jwt.InvalidTokenError
        return user_id
    except jwt.InvalidTokenError:
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Unauthorized. Invalid token."
        )