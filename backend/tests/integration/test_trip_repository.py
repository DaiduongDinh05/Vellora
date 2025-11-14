
import pytest
from uuid import uuid4
from app.modules.expenses.models import Expense
from app.modules.rate_categories.models import RateCategory
from app.modules.rate_customizations.models import RateCustomization
from app.modules.trips.models import Trip, TripStatus
from app.modules.trips.repository import TripRepo


@pytest.mark.integration
@pytest.mark.asyncio
class TestTripRepoIntegration:

    async def test_save_trip_with_relationships(self, test_db_session):

        customization = RateCustomization(
            id=uuid4(),
            name="Standard Rate",
            description="Standard mileage rate",
            year=2024
        )
        test_db_session.add(customization)
        await test_db_session.commit()
        
        category = RateCategory(
            id=uuid4(),
            name="Mileage",
            cost_per_mile=0.67,
            rate_customization_id=customization.id
        )
        test_db_session.add(category)
        await test_db_session.commit()
        
        trip = Trip(
            id=uuid4(),
            status=TripStatus.active,
            start_address_encrypted="encrypted_start_address",
            purpose="Business meeting",
            vehicle="Company Car",
            geometry_encrypted="gAAAAABhZ6_encrypted_geometry_data_here",
            rate_customization_id=customization.id,
            rate_category_id=category.id,
            reimbursement_rate=0.67
        )
        
        repo = TripRepo(test_db_session)
        
        result = await repo.save(trip)
        
        assert result.id == trip.id
        assert result.status == TripStatus.active
        assert result.start_address_encrypted == "encrypted_start_address"
        assert result.purpose == "Business meeting"
        
        assert result.rate_customization is not None
        assert result.rate_customization.name == "Standard Rate"
        assert result.rate_category is not None
        assert result.rate_category.name == "Mileage"
        assert len(result.expenses) == 0 

    async def test_get_trip_by_id(self, test_db_session):

        customization = RateCustomization(
            id=uuid4(),
            name="International Rate",
            description="International travel rate",
            year=2024
        )
        test_db_session.add(customization)
        await test_db_session.commit()
        
        category = RateCategory(
            id=uuid4(),
            name="Per Diem",
            cost_per_mile=1.25,
            rate_customization_id=customization.id
        )
        test_db_session.add(category)
        await test_db_session.commit()
        
        trip = Trip(
            id=uuid4(),
            status=TripStatus.completed,
            start_address_encrypted="encrypted_start",
            end_address_encrypted="encrypted_end",
            purpose="Client visit",
            vehicle="Rental Car",
            miles=50.5,
            geometry_encrypted="gAAAAABhZ7_client_visit_geometry_encrypted",
            reimbursement_rate=0.67,
            mileage_reimbursement_total=33.84,
            rate_customization_id=customization.id,
            rate_category_id=category.id
        )
        test_db_session.add(trip)
        await test_db_session.commit()
        
        repo = TripRepo(test_db_session)
        
        result = await repo.get(trip.id)
        
        assert result is not None
        assert result.id == trip.id
        assert result.status == TripStatus.completed
        assert result.miles == 50.5
        assert result.mileage_reimbursement_total == 33.84
        
        assert result.rate_customization.name == "International Rate"
        assert result.rate_category.name == "Per Diem"

    async def test_get_trip_not_found(self, test_db_session):

        repo = TripRepo(test_db_session)
        non_existent_id = uuid4()
        
        result = await repo.get(non_existent_id)
        
        assert result is None

    async def test_save_and_retrieve_trip_with_expenses(self, test_db_session):
        customization = RateCustomization(id=uuid4(), name="Default", year=2024)
        test_db_session.add(customization)
        await test_db_session.commit()
        
        category = RateCategory(
            id=uuid4(), 
            name="Travel", 
            cost_per_mile=0.67,
            rate_customization_id=customization.id
        )
        test_db_session.add(category)
        await test_db_session.commit()
        
        trip = Trip(
            id=uuid4(),
            status=TripStatus.active,
            start_address_encrypted="encrypted_start",
            vehicle="Personal Vehicle",
            geometry_encrypted="gAAAAABhZ8_travel_geometry_encrypted",
            rate_customization_id=customization.id,
            rate_category_id=category.id,
            reimbursement_rate=0.67
        )
        test_db_session.add(trip)
        await test_db_session.commit()
        
        expense = Expense(
            id=uuid4(),
            trip_id=trip.id,
            type="Hotel",
            amount=150.00
        )
        test_db_session.add(expense)
        await test_db_session.commit()
        
        repo = TripRepo(test_db_session)
        
        result = await repo.get(trip.id)
        
        assert result is not None
        assert len(result.expenses) == 1
        assert result.expenses[0].type == "Hotel"
        assert result.expenses[0].amount == 150.00

    async def test_save_updates_existing_trip(self, test_db_session):
        customization = RateCustomization(id=uuid4(), name="Standard", year=2024)
        test_db_session.add(customization)
        await test_db_session.commit()
        
        category = RateCategory(
            id=uuid4(), 
            name="Mileage", 
            cost_per_mile=0.67,
            rate_customization_id=customization.id
        )
        test_db_session.add(category)
        await test_db_session.commit()
        
        trip = Trip(
            id=uuid4(),
            status=TripStatus.active,
            start_address_encrypted="encrypted_start",
            vehicle="Work Truck",
            geometry_encrypted="gAAAAABhZ9_mileage_geometry_encrypted",
            rate_customization_id=customization.id,
            rate_category_id=category.id,
            reimbursement_rate=0.67
        )
        test_db_session.add(trip)
        await test_db_session.commit()
        
        repo = TripRepo(test_db_session)
        
        trip.purpose = "Updated purpose"
        trip.status = TripStatus.completed
        trip.miles = 100.0
        trip.mileage_reimbursement_total = 67.0
        
        updated_trip = await repo.save(trip)
        
        assert updated_trip.purpose == "Updated purpose"
        assert updated_trip.status == TripStatus.completed
        assert updated_trip.miles == 100.0
        assert updated_trip.mileage_reimbursement_total == 67.0
        
        retrieved = await repo.get(trip.id)
        assert retrieved.purpose == "Updated purpose"
        assert retrieved.status == TripStatus.completed
