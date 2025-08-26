from pydantic import Field
from app.schemas.response import CamelModel

class LoginRequest(CamelModel):
    username:str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class LoginResponseData(CamelModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int