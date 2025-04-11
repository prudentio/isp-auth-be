from typing import Generic,TypeVar
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar("T")

class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

class SuccessResponse(CamelModel, Generic[T]):
    status_code: int
    data: T

class ErrorResponse(CamelModel):
    status_code: int
    message: str