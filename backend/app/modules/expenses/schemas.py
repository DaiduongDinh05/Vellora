import datetime
from uuid import UUID
from pydantic import BaseModel


class CreateExpenseDTO(BaseModel):
    type: str
    amount: float

class EditExpenseDTO(BaseModel):
    type: str | None = None 
    amount: float | None = None 

class ExpenseResponseDTO(BaseModel):
    id: UUID
    trip_id: UUID
    type: str
    amount: float
    created_at: datetime.datetime

    class Config:
        from_attributes=True
