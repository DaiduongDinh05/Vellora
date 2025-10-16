
import datetime
from uuid import UUID
from pydantic import BaseModel

class CreateRateCustomizationDTO(BaseModel):
    name: str
    description: str | None = None
    year: int

class RateCustomizationResponseDTO(BaseModel):
    id: UUID
    name: str
    year: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True