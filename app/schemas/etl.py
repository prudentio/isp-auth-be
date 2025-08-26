from dataclasses import dataclass
from enum import Enum
from datetime import  date, datetime
from typing import List
from uuid import UUID

class TypeAggregateEnum(Enum):
    SURVEYOR = "surveyor"
    REGION = "region"

@dataclass
class AggregatedData:
    date: date
    region_id: str
    surveyor_id: str
    surveyor_name: str
    total_data: int

@dataclass
class ExtractedData:
    date: datetime
    tag_id: List[UUID]
    surveyor_id: UUID
    family_cards: List[str]
