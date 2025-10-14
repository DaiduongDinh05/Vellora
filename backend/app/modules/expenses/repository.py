from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.expenses.models import Expense

class ExpenseRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, expense: Expense) -> Expense:
        self.db.add(expense)
        await self.db.commit()
        await self.db.refresh(expense)
        
        return expense
    
    async def get_expense(self, expense_id: UUID) -> Expense:
        return await self.db.scalar(select(Expense).where(Expense.id == expense_id))
    
    async def get_expenses_by_trip_id(self, trip_id: UUID):
        query = select(Expense).where(Expense.trip_id == trip_id)
        result = await self.db.execute(query)
        return result.scalars().all()