from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.infrastructure.config import settings
from jose import jwt, JWTError
from app.exceptions import CustomHTTPException

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/api/auth/access-token", "/docs", "/openapi.json", "/api/export-excel"]:
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise CustomHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Authorization header missing or invalid"
            )
        
        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
            request.state.user_id = payload.get("id")
        except JWTError:
            raise CustomHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Invalid Token"
            )
        
        return await call_next(request)