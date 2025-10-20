from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.modules.trips.models import Trip

class TripRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, trip: Trip) -> Trip:

        self.db.add(trip)
        await self.db.commit()
        result = await self.db.execute(
            select(Trip)
            .options(
                selectinload(Trip.expenses),
                selectinload(Trip.rate_customization),
                selectinload(Trip.rate_category),
            )
            .where(Trip.id == trip.id)
        )
        return result.scalar_one()
    
    async def get(self, trip_id):
        result = await self.db.execute(
            select(Trip)
            .options(
                selectinload(Trip.expenses),
                selectinload(Trip.rate_customization),
                selectinload(Trip.rate_category),
            )
            .where(Trip.id == trip_id)
        )
        return result.scalar_one_or_none()
