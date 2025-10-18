from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.rate_customizations.models import RateCustomization

class RateCustomizationRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, rate_customization: RateCustomization) -> RateCustomization:
        self.db.add(rate_customization)
        await self.db.commit()
        await self.db.refresh(rate_customization)

        return rate_customization
    
    async def get(self, customization_id: UUID) -> RateCustomization:
        return await self.db.scalar(select(RateCustomization).where(RateCustomization.id == customization_id))
    
    async def delete(self, customization : RateCustomization) -> None:
        await self.db.delete(customization)
        await self.db.commit()