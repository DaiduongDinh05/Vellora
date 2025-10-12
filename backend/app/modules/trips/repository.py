from app.modules.trips.schemas import CreateTripDTO
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.trips.models import Trip

class TripRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_trip(self, trip: Trip) -> Trip:

        self.db.add(trip)
        await self.db.commit()
        await self.db.refresh(trip)

        return trip
    
    async def get_trip(self, trip_id):
        return await self.db.scalar(select(Trip).where(Trip.id == trip_id))

    async def update_trip(self, trip: Trip) -> Trip:
        
        self.db.add(trip)       
        await self.db.commit()
        await self.db.refresh(trip)

        return trip