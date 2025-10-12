from app.modules.trips.schemas import CreateTripDTO
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.trips.models import Trip

class TripRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_trip(self, trip: Trip) -> Trip:

        self.db.add(trip)
        await self.db.commit()
        await self.db.refresh(trip)

        return trip

    