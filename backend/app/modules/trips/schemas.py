import datetime
from typing import List
from uuid import UUID
from app.modules.trips.models import Trip, TripStatus
from app.modules.trips.utils.crypto import decrypt_address
from pydantic import BaseModel, Field

class CreateTripDTO(BaseModel):
    start_address: str
    purpose: str | None = None
    rate_customization_id: UUID
    rate_category_id: UUID

class EndTripDTO(BaseModel):
    end_address: str
    miles: float

class EditTripDTO(BaseModel):
    purpose: str | None = None
    rate_customization_id: UUID | None = None
    rate_category_id: UUID | None = None

class ExpenseResponseDTO(BaseModel):
    id: str
    type: str
    amount_cents: float
    created_at: datetime.datetime

class TripResponseDTO(BaseModel):
    id: str
    status: TripStatus
    start_address: str
    end_address: str | None = None
    purpose: str | None = None
    miles: float | None = None
    reimbursement_rate: float | None = None
    mileage_reimbursement_total: float | None = None
    expense_reimbursement_total: float | None = None
    total_reimbursement: float | None = None
    started_at: datetime.datetime
    ended_at: datetime.datetime | None = None
    updated_at: datetime.datetime
    rate_customization_id: UUID
    rate_category_id: UUID
    expenses: List[ExpenseResponseDTO] = []

    @classmethod
    def model_validate(cls, trip: Trip):

        data = {
            #convert uuid to str
            "id": str(trip.id),
            "status": trip.status,
            "start_address": decrypt_address(trip.start_address_encrypted),
            "end_address": decrypt_address(trip.end_address_encrypted) if trip.end_address_encrypted else None,
            "purpose": trip.purpose,
            "miles": trip.miles,
            "reimbursement_rate": trip.reimbursement_rate,
            "mileage_reimbursement_total": trip.mileage_reimbursement_total,
            "expense_reimbursement_total": trip.expense_reimbursement_total,
            "total_reimbursement": (trip.mileage_reimbursement_total or 0) + (trip.expense_reimbursement_total or 0),
            "started_at": trip.started_at,
            "ended_at": trip.ended_at,
            "updated_at": trip.updated_at,
            "rate_customization_id": trip.rate_customization_id,
            "rate_category_id": trip.rate_category_id,
            "expenses": [
                ExpenseResponseDTO(
                    id=str(e.id),
                    type=e.type,
                    amount_cents=e.amount_cents,
                    created_at=e.created_at,
                )
                for e in getattr(trip, "expenses", [])
            ],
        }

        # Create and return a new instance of TripResponseDTO
        return cls(**data)

    class Config:
        from_attributes = True