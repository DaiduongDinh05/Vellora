import datetime
from typing import List
from uuid import UUID
from app.modules.trips.models import Trip, TripStatus
from app.modules.trips.utils.crypto import decrypt_address, decrypt_geometry
from app.modules.trips.utils.distance import meters_to_miles
from app.modules.expenses.schemas import CreateExpenseDTO
from pydantic import BaseModel, Field, field_validator, ValidationError

class CreateTripDTO(BaseModel):
    start_address: str
    purpose: str | None = None
    vehicle: str | None = None
    rate_customization_id: UUID
    rate_category_id: UUID
    
    @field_validator('rate_customization_id', 'rate_category_id')
    @classmethod
    def validate_uuids(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if len(v) > 36:
                v = v[:36]
        return v

class EndTripDTO(BaseModel):
    end_address: str
    geometry: dict
    distance_meters: float
    
    @field_validator('distance_meters')
    @classmethod
    def validate_distance(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Distance must be non-negative")
        return v
    
    @property
    def miles(self) -> float:
        return meters_to_miles(self.distance_meters)

class EditTripDTO(BaseModel):
    purpose: str | None = None
    vehicle: str | None = None
    miles: float | None = None
    rate_customization_id: UUID | None = None
    rate_category_id: UUID | None = None
    
    @field_validator('miles')
    @classmethod
    def validate_miles(cls, v: float | None) -> float | None:
        if v is not None and v < 0:
            raise ValueError("Miles must be non-negative")
        return v

class ManualCreateTripDTO(BaseModel):
    start_address: str
    end_address: str
    purpose: str | None = None
    vehicle: str | None = None
    miles: float
    geometry: dict | None = None
    started_at: datetime.datetime
    ended_at: datetime.datetime
    rate_customization_id: UUID
    rate_category_id: UUID
    expenses: List[CreateExpenseDTO] | None = None 

class ExpenseResponseDTO(BaseModel):
    id: str
    type: str
    amount: float
    created_at: datetime.datetime

class TripResponseDTO(BaseModel):
    id: str
    status: TripStatus
    start_address: str
    end_address: str | None = None
    geometry: dict | None = None
    purpose: str | None = None
    vehicle: str | None = None
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
            "vehicle": trip.vehicle,
            "miles": trip.miles,
            "reimbursement_rate": trip.reimbursement_rate,
            "geometry": decrypt_geometry(trip.geometry_encrypted) if trip.geometry_encrypted else None,
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
                    amount=e.amount,
                    created_at=e.created_at,
                )
                for e in getattr(trip, "expenses", [])
            ],
        }

        # Create and return a new instance of TripResponseDTO
        return cls(**data)

    class Config:
        from_attributes = True

class MonthlyTripStatsResponseDTO(BaseModel):
    month: int
    year: int
    total_drives: int
    total_miles: float
    total_reimbursement: float