import datetime
from app.modules.trips.models import Trip, TripCategory, TripStatus
from app.modules.trips.crypto import decrypt_address
from pydantic import BaseModel, field_validator

class CreateTripDTO(BaseModel):
    start_address: str
    category: TripCategory = TripCategory.business
    purpose: str | None = None
    reimbursement_rate: float | None = None

class EndTripDTO(BaseModel):
    end_address: str
    #might add end time here

class EditTripDTO(BaseModel):
    pass

class TripResponseDTO(BaseModel):
    id: str
    status: TripStatus
    start_address: str
    end_address: str | None = None
    category: TripCategory
    purpose: str | None = None
    reimbursement_rate: float | None = None
    started_at: datetime.datetime
    ended_at: datetime.datetime | None = None

    @classmethod
    def model_validate(cls, trip: Trip, **kwargs):

        data = {
            "id": str(trip.id),
            "status": trip.status,
            "start_address": decrypt_address(trip.start_address_encrypted),
            "end_address": decrypt_address(trip.end_address_encrypted) if trip.end_address_encrypted else None,
            "category": trip.category,
            "purpose": trip.purpose,
            "reimbursement_rate": trip.reimbursement_rate,
            "started_at": trip.started_at,
            "ended_at": trip.ended_at
        }
        return cls(**data)

    class Config:
        from_attributes = True