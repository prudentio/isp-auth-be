from pydantic import BaseModel
from enum import IntEnum

class RegionLevel(IntEnum):
    rt = 1
    rw = 2
    kelurahan = 3
    kecamatan = 4
    kabupaten = 5

class GetRegionByLevelResponse(BaseModel):
    id: str
    name: str
    parent_id: str