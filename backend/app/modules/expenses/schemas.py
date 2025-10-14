import datetime
from uuid import UUID
from pydantic import BaseModel


class CreateExpenseDTO(BaseModel):
    type: str
    amount_cents: float

class ExpenseResponseDTO(BaseModel):
    id: UUID
    trip_id: UUID
    type: str
    amount_cents: float
    created_at: datetime.datetime

    class Config:
        from_attributes=True
