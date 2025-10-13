import datetime
from app.modules.trips.models import Trip, TripCategory, TripStatus
from app.modules.trips.utils.crypto import decrypt_address
from pydantic import BaseModel

class CreateTripDTO(BaseModel):
    start_address: str
    category: TripCategory = TripCategory.business
    purpose: str | None = None
    reimbursement_rate: float | None = None

class EndTripDTO(BaseModel):
    end_address: str

class EditTripDTO(BaseModel):
    # category, customization, and reimbursment will be added once implemented
    purpose: str | None = None

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
    def model_validate(cls, trip: Trip):

        data = {
            #convert uuid to str
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

        # Create and return a new instance of TripResponseDTO
        return cls(**data)

    class Config:
        from_attributes = True