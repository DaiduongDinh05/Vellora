from uuid import UUID
from fastapi import APIRouter, Depends, Response, status
from app.infra.db import AsyncSession
from app.modules.expenses.repository import ExpenseRepo
from app.modules.expenses.service import ExpensesService
from app.container import get_db
from app.modules.expenses.schemas import CreateExpenseDTO, EditExpenseDTO, ExpenseResponseDTO
from app.core.error_handler import error_handler
from app.core.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.trips.repository import TripRepo


router = APIRouter(prefix="/trips/{trip_id}/expenses", tags=["Expenses"])

def get_expenses_service(db: AsyncSession = Depends(get_db)):
    return ExpensesService(ExpenseRepo(db), TripRepo(db))

@router.post("/", response_model= ExpenseResponseDTO)
@error_handler
async def create_expense(
    trip_id: UUID, 
    body: CreateExpenseDTO, 
    svc = Depends(get_expenses_service),
    current_user: User = Depends(get_current_user)
):
    expense = await svc.create_expense(current_user.id, trip_id, body)
    return expense

@router.get("/", response_model=list[ExpenseResponseDTO])
@error_handler
async def get_expenses(
    trip_id: UUID, 
    svc = Depends(get_expenses_service),
    current_user: User = Depends(get_current_user)
):
    expenses = await svc.get_expenses_for_trip(current_user.id, trip_id)
    return expenses

@router.get("/{expense_id}", response_model= ExpenseResponseDTO)
@error_handler
async def get_expense(
    expense_id: UUID, 
    svc = Depends(get_expenses_service),
    current_user: User = Depends(get_current_user)
):
    expense = await svc.get_expense(current_user.id, expense_id)
    return expense

@router.patch("/{expense_id}", response_model=ExpenseResponseDTO)
@error_handler
async def edit_expense(
    expense_id: UUID, 
    body: EditExpenseDTO, 
    svc = Depends(get_expenses_service),
    current_user: User = Depends(get_current_user)
):
    expense = await svc.edit_expense(current_user.id, expense_id, body)
    return expense

@router.delete("/{expense_id}")
@error_handler
async def delete_expense(
    expense_id: UUID, 
    svc = Depends(get_expenses_service),
    current_user: User = Depends(get_current_user)
):
    await svc.delete_expense(current_user.id, expense_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)