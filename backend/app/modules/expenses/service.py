from uuid import UUID
from app.modules.expenses.repository import ExpenseRepo
from app.modules.expenses.schemas import CreateExpenseDTO, EditExpenseDTO
from app.modules.expenses.exceptions import ExpenseNotFoundError, ExpensePersistenceError, InvalidExpenseDataError
from app.modules.expenses.exceptions import DuplicateExpenseError
from app.modules.trips.repository import TripRepo
from app.modules.expenses.models import Expense
from app.modules.trips.exceptions import TripNotFoundError
from sqlalchemy.exc import IntegrityError


class ExpensesService:
    def __init__(self, expense_repo: ExpenseRepo, trip_repo: TripRepo):
        self.expense_repo = expense_repo
        self.trip_repo = trip_repo

    async def _update_trip_total(self, trip_id: UUID):
        total = await self.expense_repo.sum_by_trip(trip_id)
        trip = await self.trip_repo.get(trip_id)
        if not trip:
            raise TripNotFoundError("Trip not found")

        trip.expense_reimbursement_total = total
        await self.trip_repo.save(trip)

    async def create_expense(self, trip_id: UUID, data: CreateExpenseDTO):

        trip = await self.trip_repo.get(trip_id)
        if not trip:
            raise TripNotFoundError("Trip not found")

        if not data.type.strip():
            raise InvalidExpenseDataError("Type is required")
        
        if data.amount <= 0:
            raise InvalidExpenseDataError("Amount must be positive")
        
        cleaned_type = data.type.strip().capitalize()

        existing = await self.expense_repo.get_by_trip_and_type(trip_id, cleaned_type)
        if existing:
            raise DuplicateExpenseError("An expense with this type already exists for the trip")

        try:
            expense = Expense(
                trip_id = trip_id,
                type = cleaned_type,
                amount = data.amount
            )

            saved_expense = await self.expense_repo.save(expense)
            await self._update_trip_total(trip_id)
            return saved_expense
        except IntegrityError as e:
            raise DuplicateExpenseError("An expense with this type already exists for the trip") from e
        except Exception as e:
            raise ExpensePersistenceError("Unexpected error occurred while saving expense") from e

    
    async def get_expenses_for_trip(self, trip_id: UUID):
        
        trip = await self.trip_repo.get(trip_id)
        if not trip:
            raise TripNotFoundError("Trip not found")

        return await self.expense_repo.get_expenses_by_trip_id(trip_id)

    async def get_expense(self, expense_id: UUID):
        expense = await self.expense_repo.get_expense(expense_id)

        if not expense:
            raise ExpenseNotFoundError("Expense not found")
        
        return expense
    
    async def edit_expense(self, expense_id: UUID, data: EditExpenseDTO):
        expense = await self.get_expense(expense_id)

        if data.type is not None:
            if not data.type.strip():
                raise InvalidExpenseDataError("Type cannot be empty")
            cleaned = data.type.strip().capitalize()

            if cleaned != expense.type:
                existing = await self.expense_repo.get_by_trip_and_type(expense.trip_id, cleaned)
                if existing:
                    raise DuplicateExpenseError("An expense with this type already exists for the trip")
            expense.type = cleaned

        if data.amount is not None:
            if data.amount <= 0:
                raise InvalidExpenseDataError("Amount must be positive")
            expense.amount = data.amount
        
        saved_expense = await self.expense_repo.save(expense)
        await self._update_trip_total(expense.trip_id)
        return saved_expense
        
    async def delete_expense(self, expense_id: UUID):
        expense = await self.get_expense(expense_id)
        trip_id = expense.trip_id
        await self.expense_repo.delete_expense(expense)
        await self._update_trip_total(trip_id)