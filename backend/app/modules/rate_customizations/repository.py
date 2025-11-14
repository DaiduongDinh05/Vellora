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
    
    async def get(self, customization_id: UUID, user_id: UUID = None) -> RateCustomization:
        query = select(RateCustomization).where(RateCustomization.id == customization_id)
        if user_id is not None:
            query = query.where(RateCustomization.user_id == user_id)
        return await self.db.scalar(query)
    
    async def delete(self, customization : RateCustomization) -> None:
        await self.db.delete(customization)
        await self.db.commit()

    async def get_by_user_and_name(self, user_id: UUID, name: str) -> RateCustomization | None:
        query = select(RateCustomization).where(
            RateCustomization.user_id == user_id,
            RateCustomization.name == name
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_customizations(self, user_id: UUID):
        result = await self.db.execute(
            select(RateCustomization)
            .where(RateCustomization.user_id == user_id)
            .order_by(RateCustomization.created_at.desc())
        )
        return result.scalars().all()