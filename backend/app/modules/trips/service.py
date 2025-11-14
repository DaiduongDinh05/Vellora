from datetime import datetime, timezone
from uuid import UUID
from app.modules.trips.repository import TripRepo
from app.modules.trips.schemas import CreateTripDTO, EditTripDTO, EndTripDTO, ManualCreateTripDTO
from app.modules.trips.utils.crypto import encrypt_address, encrypt_geometry
from app.modules.trips.models import Trip, TripStatus
from app.modules.trips.exceptions import InvalidTripDataError, TripNotFoundError, TripPersistenceError, TripAlreadyActiveError
from app.modules.rate_categories.repository import RateCategoryRepo
from app.modules.rate_customizations.repository import RateCustomizationRepo
from app.modules.rate_customizations.exceptions import RateCustomizationNotFoundError
from app.modules.rate_categories.exceptions import InvalidRateCategoryDataError, RateCategoryNotFoundError
from app.modules.expenses.models import Expense
from app.modules.expenses.repository import ExpenseRepo


class TripsService:
    def __init__(self, repo: TripRepo, category_repo: RateCategoryRepo, customization_repo: RateCustomizationRepo, expense_service=None):
        self.repo = repo
        self.category_repo = category_repo
        self.customization_repo = customization_repo
        self.expense_service = expense_service

    async def start_trip(self, user_id: UUID, data: CreateTripDTO):

        if not data.start_address.strip():
            raise InvalidTripDataError("Start address is required")
        
        # Check if user already has an active trip
        active_trip = await self.repo.get_active_trip(user_id)
        if active_trip:
            raise TripAlreadyActiveError("You already have an active trip")
        
        customization = await self.customization_repo.get(data.rate_customization_id, user_id)
        if not customization:
            raise RateCustomizationNotFoundError("Rate customization not found or not owned by user")
        
        category = await self.category_repo.get(data.rate_category_id)
        if not category:
            raise RateCategoryNotFoundError("Rate category not found")

        if category.rate_customization_id != customization.id:
            raise InvalidRateCategoryDataError("Category does not belong to this customization")
        
        reimbursement_rate = category.cost_per_mile

        try:
            encrypted_address = encrypt_address(data.start_address)

            trip = Trip(
                user_id=user_id,
                start_address_encrypted = encrypted_address,
                purpose = data.purpose,
                vehicle = data.vehicle,
                reimbursement_rate=reimbursement_rate,
                rate_customization_id=data.rate_customization_id,
                rate_category_id=data.rate_category_id,
            )
                    
            return await self.repo.save(trip)

        except Exception as e:
            raise TripPersistenceError(f"Unexpected error occurred while saving trip: {e}") from e
    
    async def manual_create_trip(self, user_id: UUID, data: ManualCreateTripDTO):
        if not data.start_address.strip():
            raise InvalidTripDataError("Start address is required")
        
        if not data.end_address.strip():
            raise InvalidTripDataError("End address is required")
        
        if data.miles <= 0:
            raise InvalidTripDataError("Miles must be greater than 0")
        
        if data.ended_at <= data.started_at:
            raise InvalidTripDataError("End time must be after start time")
        
        customization = await self.customization_repo.get(data.rate_customization_id)
        if not customization:
            raise RateCustomizationNotFoundError("Rate customization not found")
        
        category = await self.category_repo.get(data.rate_category_id)
        if not category:
            raise RateCategoryNotFoundError("Rate category not found")

        if category.rate_customization_id != customization.id:
            raise InvalidRateCategoryDataError("Category does not belong to this customization")
        
        try:
            encrypted_start_address = encrypt_address(data.start_address)
            encrypted_end_address = encrypt_address(data.end_address)
            encrypted_geometry = encrypt_geometry(data.geometry) if data.geometry else None
            
            reimbursement_rate = category.cost_per_mile
            mileage_total = data.miles * reimbursement_rate

            trip = Trip(
                user_id=user_id,
                status=TripStatus.completed,
                start_address_encrypted=encrypted_start_address,
                end_address_encrypted=encrypted_end_address,
                purpose=data.purpose,
                vehicle=data.vehicle,
                miles=data.miles,
                geometry_encrypted=encrypted_geometry,
                reimbursement_rate=reimbursement_rate,
                mileage_reimbursement_total=mileage_total,
                expense_reimbursement_total=0.0, 
                started_at=data.started_at,
                ended_at=data.ended_at,
                rate_customization_id=data.rate_customization_id,
                rate_category_id=data.rate_category_id,
            )
            
            saved_trip = await self.repo.save(trip)
            
            if data.expenses and self.expense_service:
                for expense_data in data.expenses:
                    await self.expense_service.create_expense(user_id, saved_trip.id, expense_data)
                    
            return saved_trip

        except Exception as e:
            raise TripPersistenceError(f"Unexpected error occurred while saving manual trip: {e}") from e
    
    async def get_trip_by_id(self, user_id: UUID, trip_id: UUID):
        trip = await self.repo.get(trip_id, user_id)

        if trip:
            return trip
        
        raise TripNotFoundError("Trip doesn't exist or not owned by user")
    
    async def end_trip(self, user_id: UUID, trip_id: UUID, data: EndTripDTO):
        if not data.end_address.strip():
            raise InvalidTripDataError("End address is required")
        
        #check if trip exists first
        trip = await self.get_trip_by_id(user_id, trip_id)
      
        if trip.status == TripStatus.completed:
            raise InvalidTripDataError("Trip already ended")
        
        if trip.status == TripStatus.cancelled:
            raise InvalidTripDataError("Cannot end a cancelled trip")
        
        #idk if i wanna add this. just to make sure start and end addrr arent the same
        # if data.end_address.strip().lower() == trip.start_address_encrypted:
        #     raise InvalidTripDataError("Start and end addresses cannot be the same")

        miles = data.miles
        if miles < 0:
            raise InvalidTripDataError("Miles must be non-negative")
                
        try: 

            trip.miles = miles
            trip.geometry_encrypted = encrypt_geometry(data.geometry)
            trip.mileage_reimbursement_total = miles * (trip.reimbursement_rate or 0.0)
            trip.status = TripStatus.completed
            trip.end_address_encrypted = encrypt_address(data.end_address)
            trip.ended_at = datetime.now(timezone.utc)

            return await self.repo.save(trip)
               
        except Exception as e:
            await self.repo.db.rollback()
            raise TripPersistenceError(f"Unexpected error occurred while ending trip: {e}") from e

        
    async def edit_trip(self, user_id: UUID, trip_id: UUID, data: EditTripDTO):
        #check if trip exists first
        trip = await self.get_trip_by_id(user_id, trip_id)
        
        try:

            if data.purpose is not None:
                trip.purpose = data.purpose

            if data.vehicle is not None:
                trip.vehicle = data.vehicle

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

    async def cancel_trip(self, user_id: UUID, trip_id: UUID):

        trip = await self.get_trip_by_id(user_id, trip_id)

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
    


    