from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateVehicleDTO(BaseModel):
    name: str
    license_plate: str
    model: str
    year: int | None
    color: str | None


class EditVehicleDTO(BaseModel):
    name: str | None
    license_plate: str | None
    model: str | None
    year: int | None
    color: str | None
    is_active: bool | None
    


class VehicleResponse(BaseModel):
    id: UUID
    name: str
    license_plate: str
    model: str
    year: Optional[int]
    color: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class VehicleListResponse(BaseModel):
    vehicles: list[VehicleResponse]
    total: int