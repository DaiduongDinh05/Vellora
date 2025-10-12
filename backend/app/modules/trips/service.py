from app.modules.trips.repository import TripRepo
from app.modules.trips.schemas import CreateTripDTO, EditTripDTO, EndTripDTO
from app.modules.trips.crypto import encrypt_address
from app.modules.trips.models import Trip
from app.modules.trips.exceptions import InvalidTripDataError, TripPersistenceError


class TripsService:
    def __init__(self, repo: TripRepo):
        self.repo = repo

    async def startTrip(self, data: CreateTripDTO):

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
    
    async def endTrip(self, data: EndTripDTO):
        pass

    async def editTrip(self, data: EditTripDTO):
        pass

    async def cancelTrip(self, trip_id: int):
        pass

    async def getTripById(self, trip_id: int):
        pass

    async def getActiveTrip(self, user_id: int):
        raise NotImplementedError("Users Not implemented yet")

    async def getTripsByUserId(self, user_id: int):
        raise NotImplementedError("Users Not implemented yet")
    


    