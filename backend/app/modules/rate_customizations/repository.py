from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.rate_customizations.models import RateCustomization

class RateCustomizationRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_customization(self, rate_customization: RateCustomization) -> RateCustomization:
        self.db.add(rate_customization)
        await self.db.commit()
        await self.db.refresh(rate_customization)

        return rate_customization