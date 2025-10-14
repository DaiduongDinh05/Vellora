from uuid import UUID
from app.modules.expenses.repository import ExpenseRepo
from app.modules.expenses.schemas import CreateExpenseDTO
from app.modules.expenses.exceptions import ExpenseNotFoundError, ExpensePersistenceError, InvalidExpenseDataError
from app.modules.trips.repository import TripRepo
from app.modules.expenses.models import Expense
from app.modules.trips.exceptions import TripNotFoundError


class ExpensesService:
    def __init__(self, expense_repo: ExpenseRepo, trip_repo: TripRepo):
        self.expense_repo = expense_repo
        self.trip_repo = trip_repo

    async def create_expense(self, trip_id: UUID, data: CreateExpenseDTO):

        trip = await self.trip_repo.get_trip(trip_id)
        if not trip:
            raise TripNotFoundError("Trip not found")

        if not data.type.strip():
            raise InvalidExpenseDataError("Type is required")
        
        if data.amount_cents <= 0:
            raise InvalidExpenseDataError("Amount must be positive")
        try:
            expense = Expense(
                trip_id = trip_id,
                type = data.type,
                amount_cents = data.amount_cents
            )
        except Exception as e:
            raise ExpensePersistenceError("Unexpected error occurred while saving expense") from e

        return await self.expense_repo.save(expense)

    async def get_expense(self, expense_id: UUID):
        expense = await self.expense_repo.get_expense(expense_id)

        if not expense:
            raise ExpenseNotFoundError("Expense not found")
        
        return expense