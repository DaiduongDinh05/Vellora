from uuid import UUID
from fastapi import APIRouter, Depends
from app.infra.db import AsyncSession
from app.modules.expenses.repository import ExpenseRepo
from app.modules.expenses.service import ExpensesService
from app.container import get_db
from app.modules.expenses.schemas import CreateExpenseDTO, ExpenseResponseDTO
from app.core.error_handler import error_handler
from app.modules.trips.repository import TripRepo


router = APIRouter(prefix="/trips/{trip_id}/expenses")

def get_expenses_service(db: AsyncSession = Depends(get_db)):
    return ExpensesService(ExpenseRepo(db), TripRepo(db))

@router.post("/", response_model= ExpenseResponseDTO)
@error_handler
async def create_expense(trip_id: UUID, body: CreateExpenseDTO, svc = Depends(get_expenses_service)):
    expense = await svc.create_expense(trip_id, body)
    return expense

@router.get("/", response_model=list[ExpenseResponseDTO])
@error_handler
async def get_expenses(trip_id: UUID, svc = Depends(get_expenses_service)):
    expenses = await svc.get_expenses_for_trip(trip_id)
    return expenses

@router.get("/{expense_id}", response_model= ExpenseResponseDTO)
@error_handler
async def get_expense(expense_id: UUID, svc = Depends(get_expenses_service)):
    expense = await svc.get_expense(expense_id)
    return expense