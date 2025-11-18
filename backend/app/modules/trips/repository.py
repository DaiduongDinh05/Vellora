from uuid import UUID
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
    
    async def get(self, trip_id: UUID, user_id: UUID = None):
        query = select(Trip).options(
            selectinload(Trip.expenses),
            selectinload(Trip.rate_customization),
            selectinload(Trip.rate_category),
        ).where(Trip.id == trip_id)
        
        if user_id is not None:
            query = query.where(Trip.user_id == user_id)
            
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_trips(self, user_id: UUID):
        result = await self.db.execute(
            select(Trip)
            .options(
                selectinload(Trip.expenses),
                selectinload(Trip.rate_customization),
                selectinload(Trip.rate_category),
            )
            .where(Trip.user_id == user_id)
            .order_by(Trip.started_at.desc())
        )
        return result.scalars().all()
    
    async def get_active_trip(self, user_id: UUID):
        result = await self.db.execute(
            select(Trip)
            .options(
                selectinload(Trip.expenses),
                selectinload(Trip.rate_customization),
                selectinload(Trip.rate_category),
            )
            .where(Trip.user_id == user_id, Trip.status == "active")
        )
        return result.scalar_one_or_none()
