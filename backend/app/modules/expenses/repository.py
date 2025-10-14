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