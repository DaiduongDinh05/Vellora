from datetime import datetime, timezone
from uuid import UUID
from app.modules.trips.repository import TripRepo
from app.modules.trips.schemas import CreateTripDTO, EditTripDTO, EndTripDTO
from app.modules.trips.crypto import encrypt_address
from app.modules.trips.models import Trip, TripStatus
from app.modules.trips.exceptions import InvalidTripDataError, TripNotFoundError, TripPersistenceError


class TripsService:
    def __init__(self, repo: TripRepo):
        self.repo = repo

    async def start_trip(self, data: CreateTripDTO):

        if not data.start_address.strip():
            raise InvalidTripDataError("Start address is required")
        
        if data.reimbursement_rate is not None and data.reimbursement_rate < 0:
            raise InvalidTripDataError("Reimbursement rate cannot be negative")
        
        #for when users is implemented
        # if user has active trip
        #     raise TripAlreadyActiveError("You already have an active trip")
        try:
            encrypted_address = encrypt_address(data.start_address)

            trip = Trip(
                start_address_encrypted = encrypted_address,
                category = data.category,
                purpose = data.purpose,
                reimbursement_rate = data.reimbursement_rate
            )
                    
            return await self.repo.create_trip(trip)

        except Exception as e:
            raise TripPersistenceError("Unexpected error occurred while saving trip") from e
    
    async def end_trip(self, trip_id: UUID ,data: EndTripDTO):
        if not data.end_address.strip():
            raise InvalidTripDataError("End address is required")
        
        #check if trip exists first
        trip = await self.repo.get_trip(trip_id)

        if not trip:
            raise TripNotFoundError("Trip doesn't exist")
      
        if trip.status == TripStatus.completed:
            raise InvalidTripDataError("Trip already ended")
        
        try: 
            trip.status = TripStatus.completed
            trip.end_address_encrypted = encrypt_address(data.end_address)
            trip.ended_at = datetime.now(timezone.utc)

            return await self.repo.update_trip(trip)
               
        except Exception as e:
            await self.repo.db.rollback()
            raise TripPersistenceError("Unexpected error occurred while saving trip") from e

        
    async def edit_trip(self, data: EditTripDTO):
        pass

    async def cancel_trip(self, trip_id: int):
        pass

    async def get_trip_by_id(self, trip_id: int):
        pass

    async def get_active_trip(self, user_id: int):
        raise NotImplementedError("Users Not implemented yet")

    async def get_trips_by_userId(self, user_id: int):
        raise NotImplementedError("Users Not implemented yet")
    


    