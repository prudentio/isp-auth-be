from typing import List
from app.schemas.response import CamelModel

class UserInfoResponse(CamelModel):
    user_id: int
    region_ids: List[str]