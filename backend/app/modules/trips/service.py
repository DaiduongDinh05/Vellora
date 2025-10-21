from datetime import datetime, timezone
from uuid import UUID
from app.modules.trips.repository import TripRepo
from app.modules.trips.schemas import CreateTripDTO, EditTripDTO, EndTripDTO
from app.modules.trips.utils.crypto import encrypt_address
from app.modules.trips.models import Trip, TripStatus
from app.modules.trips.exceptions import InvalidTripDataError, TripNotFoundError, TripPersistenceError
from app.modules.rate_categories.repository import RateCategoryRepo
from app.modules.rate_customizations.repository import RateCustomizationRepo
from app.modules.rate_customizations.exceptions import RateCustomizationNotFoundError
from app.modules.rate_categories.exceptions import InvalidRateCategoryDataError, RateCategoryNotFoundError


class TripsService:
    def __init__(self, repo: TripRepo, category_repo: RateCategoryRepo, customization_repo: RateCustomizationRepo):
        self.repo = repo
        self.category_repo = category_repo
        self.customization_repo = customization_repo

    async def start_trip(self, data: CreateTripDTO):

        if not data.start_address.strip():
            raise InvalidTripDataError("Start address is required")
        
        customization = await self.customization_repo.get(data.rate_customization_id)
        if not customization:
            raise RateCustomizationNotFoundError("Rate customization not found")
        
        category = await self.category_repo.get(data.rate_category_id)
        if not category:
            raise RateCategoryNotFoundError("Rate category not found")

        if category.rate_customization_id != customization.id:
            raise InvalidRateCategoryDataError("Category does not belong to this customization")
        
        reimbursement_rate = category.cost_per_mile
        
        #for when users is implemented
        # if user has active trip
        #     raise TripAlreadyActiveError("You already have an active trip")

        try:
            encrypted_address = encrypt_address(data.start_address)

            trip = Trip(
                start_address_encrypted = encrypted_address,
                purpose = data.purpose,
                reimbursement_rate=reimbursement_rate,
                rate_customization_id=data.rate_customization_id,
                rate_category_id=data.rate_category_id,
            )
                    
            return await self.repo.save(trip)

        except Exception as e:
            raise TripPersistenceError(f"Unexpected error occurred while saving trip: {e}") from e
    
    async def get_trip_by_id(self, trip_id: UUID):
        trip = await self.repo.get(trip_id)

        if trip:
            return trip
        
        raise TripNotFoundError("Trip doesn't exist")
    
    async def end_trip(self, trip_id: UUID ,data: EndTripDTO):
        if not data.end_address.strip():
            raise InvalidTripDataError("End address is required")
        
        #check if trip exists first
        trip = await self.get_trip_by_id(trip_id)
      
        if trip.status == TripStatus.completed:
            raise InvalidTripDataError("Trip already ended")
        
        if trip.status == TripStatus.cancelled:
            raise InvalidTripDataError("Cannot end a cancelled trip")
        
        #idk if i wanna add this. just to make sure start and end addrr arent the same
        # if data.end_address.strip().lower() == trip.start_address_encrypted:
        #     raise InvalidTripDataError("Start and end addresses cannot be the same")

        if data.miles is None:
            raise InvalidTripDataError("Miles are required to complete the trip")
        if data.miles < 0:
            raise InvalidTripDataError("Miles must be non-negative")
                
        try: 

            trip.miles = data.miles
            trip.mileage_reimbursement_total = data.miles * (trip.reimbursement_rate or 0.0)
            trip.status = TripStatus.completed
            trip.end_address_encrypted = encrypt_address(data.end_address)
            trip.ended_at = datetime.now(timezone.utc)

            return await self.repo.save(trip)
               
        except Exception as e:
            await self.repo.db.rollback()
            raise TripPersistenceError(f"Unexpected error occurred while ending trip: {e}") from e

        
    async def edit_trip(self, trip_id: UUID, data: EditTripDTO):
        #check if trip exists first
        trip = await self.get_trip_by_id(trip_id)
        
        try:

            if data.purpose is not None:
                trip.purpose = data.purpose

            if data.rate_customization_id is not None:
                customization = await self.customization_repo.get(data.rate_customization_id)
                if not customization:
                    raise RateCustomizationNotFoundError("Rate customization not found")
                trip.rate_customization_id = data.rate_customization_id

            if data.rate_category_id is not None:
                category = await self.category_repo.get(data.rate_category_id)
                if not category:
                    raise RateCategoryNotFoundError("Rate category not found")

                if data.rate_customization_id is not None:
                    customization_id = data.rate_customization_id
                else:
                    customization_id = trip.rate_customization_id

                if category.rate_customization_id != customization_id:
                    raise InvalidRateCategoryDataError("Category does not belong to this customization")

                trip.rate_category_id = data.rate_category_id
                trip.reimbursement_rate = category.cost_per_mile

            return await self.repo.save(trip)
        
        except Exception as e:
            await self.repo.db.rollback()
            raise TripPersistenceError(f"Unexpected error occurred while editing trip: {e}") from e

    async def cancel_trip(self, trip_id: UUID):

        trip = await self.get_trip_by_id(trip_id)

        if trip.status != TripStatus.active:
            raise InvalidTripDataError("Only active trips can be cancelled")

        try:
            trip.status = TripStatus.cancelled
            trip.ended_at = datetime.now(timezone.utc)
            return await self.repo.save(trip)

        except Exception as e:
            await self.repo.db.rollback()
            raise TripPersistenceError(f"Unexpected error occurred while cancelling trip {e}") from e


    async def get_active_trip(self, user_id: UUID):
        raise NotImplementedError("Users Not implemented yet")

    async def get_trips_by_userId(self, user_id: UUID):
        raise NotImplementedError("Users Not implemented yet")
    


    