import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import datetime, timezone, timedelta

from app.modules.trips.service import TripsService
from app.modules.trips.repository import TripRepo
from app.modules.rate_categories.repository import RateCategoryRepo
from app.modules.rate_customizations.repository import RateCustomizationRepo
from app.modules.expenses.repository import ExpenseRepo
from app.modules.expenses.service import ExpensesService
from app.modules.trips.schemas import CreateTripDTO, EditTripDTO, EndTripDTO, ManualCreateTripDTO
from app.modules.trips.models import Trip, TripStatus
from app.modules.rate_categories.models import RateCategory
from app.modules.rate_customizations.models import RateCustomization
from app.modules.trips.exceptions import (
    InvalidTripDataError,
    TripNotFoundError,
    TripPersistenceError
)
from app.modules.rate_customizations.exceptions import RateCustomizationNotFoundError
from app.modules.rate_categories.exceptions import InvalidRateCategoryDataError, RateCategoryNotFoundError


class TestTripsServiceStartTrip:

    @pytest.fixture
    def trip_repo(self):
        return AsyncMock(spec=TripRepo)

    @pytest.fixture
    def category_repo(self):
        return AsyncMock(spec=RateCategoryRepo)

    @pytest.fixture
    def customization_repo(self):
        return AsyncMock(spec=RateCustomizationRepo)

    @pytest.fixture
    def expense_repo(self):
        return AsyncMock(spec=ExpenseRepo)

    @pytest.fixture
    def service(self, trip_repo, category_repo, customization_repo, expense_repo):
        return TripsService(trip_repo, category_repo, customization_repo, expense_repo)

    @pytest.fixture
    def mock_customization(self):
        customization = MagicMock(spec=RateCustomization)
        customization.id = uuid4()
        return customization

    @pytest.fixture
    def mock_category(self):
        category = MagicMock(spec=RateCategory)
        category.id = uuid4()
        category.cost_per_mile = 0.65
        category.rate_customization_id = uuid4()
        return category

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.active
        trip.geometry_encrypted = "gAAAAABhZ6_mock_geometry_encrypted"
        return trip

    @pytest.mark.asyncio
    async def test_start_trip_success(
        self, service, trip_repo, category_repo, customization_repo, 
        mock_customization, mock_category, mock_trip
    ):
        mock_category.rate_customization_id = mock_customization.id
        dto = CreateTripDTO(
            start_address="123 Main St",
            purpose="Business meeting",
            vehicle="Toyota Camry",
            rate_customization_id=mock_customization.id,
            rate_category_id=mock_category.id
        )
        customization_repo.get.return_value = mock_customization
        category_repo.get.return_value = mock_category
        trip_repo.save.return_value = mock_trip

        with patch('app.modules.trips.service.encrypt_address', return_value="encrypted") as mock_encrypt:
            with patch('app.modules.trips.service.Trip', return_value=mock_trip):
                result = await service.start_trip(dto)

        assert result == mock_trip
        mock_encrypt.assert_called_once_with("123 Main St")
        trip_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_trip_empty_address(self, service):
        dto = CreateTripDTO(
            start_address="   ",
            purpose="Business",
            vehicle="Honda Civic",
            rate_customization_id=uuid4(),
            rate_category_id=uuid4()
        )

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.start_trip(dto)
        assert "Start address is required" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_start_trip_customization_not_found(
        self, service, customization_repo
    ):
        dto = CreateTripDTO(
            start_address="123 Main St",
            purpose="Business",
            vehicle="Nissan Altima",
            rate_customization_id=uuid4(),
            rate_category_id=uuid4()
        )
        customization_repo.get.return_value = None

        with pytest.raises(RateCustomizationNotFoundError):
            await service.start_trip(dto)

    @pytest.mark.asyncio
    async def test_start_trip_category_not_found(
        self, service, customization_repo, category_repo, mock_customization
    ):
        dto = CreateTripDTO(
            start_address="123 Main St",
            purpose="Business",
            vehicle="Chevy Malibu",
            rate_customization_id=mock_customization.id,
            rate_category_id=uuid4()
        )
        customization_repo.get.return_value = mock_customization
        category_repo.get.return_value = None

        with pytest.raises(RateCategoryNotFoundError):
            await service.start_trip(dto)

    @pytest.mark.asyncio
    async def test_start_trip_category_mismatch(
        self, service, customization_repo, category_repo, 
        mock_customization, mock_category
    ):
        different_customization_id = uuid4()
        mock_category.rate_customization_id = different_customization_id
        dto = CreateTripDTO(
            start_address="123 Main St",
            purpose="Business",
            vehicle="BMW X3",
            rate_customization_id=mock_customization.id,
            rate_category_id=mock_category.id
        )
        customization_repo.get.return_value = mock_customization
        category_repo.get.return_value = mock_category

        with pytest.raises(InvalidRateCategoryDataError) as exc_info:
            await service.start_trip(dto)
        assert "does not belong to this customization" in str(exc_info.value)


class TestTripsServiceManualCreateTrip:

    @pytest.fixture
    def trip_repo(self):
        return AsyncMock(spec=TripRepo)

    @pytest.fixture
    def category_repo(self):
        return AsyncMock(spec=RateCategoryRepo)

    @pytest.fixture
    def customization_repo(self):
        return AsyncMock(spec=RateCustomizationRepo)

    @pytest.fixture
    def expense_repo(self):
        return AsyncMock(spec=ExpenseRepo)

    @pytest.fixture
    def service(self, trip_repo, category_repo, customization_repo, expense_repo):
        return TripsService(trip_repo, category_repo, customization_repo, expense_repo)

    @pytest.fixture
    def mock_customization(self):
        customization = MagicMock(spec=RateCustomization)
        customization.id = uuid4()
        return customization

    @pytest.fixture
    def mock_category(self):
        category = MagicMock(spec=RateCategory)
        category.id = uuid4()
        category.cost_per_mile = 0.65
        category.rate_customization_id = uuid4()
        return category

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.completed
        return trip

    @pytest.mark.asyncio
    async def test_manual_create_trip_success(
        self, service, trip_repo, category_repo, customization_repo, 
        mock_customization, mock_category, mock_trip
    ):
        started_time = datetime.now(timezone.utc)
        ended_time = started_time + timedelta(hours=2)
        
        mock_category.rate_customization_id = mock_customization.id
        dto = ManualCreateTripDTO(
            start_address="123 Main St",
            end_address="456 Oak Ave",
            purpose="Business meeting",
            vehicle="Honda Civic",
            miles=25.5,
            geometry='{"type":"LineString"}',
            started_at=started_time,
            ended_at=ended_time,
            rate_customization_id=mock_customization.id,
            rate_category_id=mock_category.id
        )
        
        customization_repo.get.return_value = mock_customization
        category_repo.get.return_value = mock_category
        trip_repo.save.return_value = mock_trip

        with patch('app.modules.trips.service.encrypt_address', return_value="encrypted") as mock_encrypt_addr:
            with patch('app.modules.trips.service.encrypt_geometry', return_value="encrypted_geom") as mock_encrypt_geom:
                with patch('app.modules.trips.service.Trip', return_value=mock_trip):
                    result = await service.manual_create_trip(dto)

        assert result == mock_trip
        assert mock_encrypt_addr.call_count == 2  # start and end address
        mock_encrypt_geom.assert_called_once()
        trip_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_manual_create_trip_empty_start_address(self, service):
        started_time = datetime.now(timezone.utc)
        ended_time = started_time + timedelta(hours=1)
        
        dto = ManualCreateTripDTO(
            start_address="   ",
            end_address="456 Oak Ave",
            miles=10.0,
            started_at=started_time,
            ended_at=ended_time,
            rate_customization_id=uuid4(),
            rate_category_id=uuid4()
        )

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.manual_create_trip(dto)
        assert "Start address is required" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_manual_create_trip_empty_end_address(self, service):
        started_time = datetime.now(timezone.utc)
        ended_time = started_time + timedelta(hours=1)
        
        dto = ManualCreateTripDTO(
            start_address="123 Main St",
            end_address="   ",
            miles=10.0,
            started_at=started_time,
            ended_at=ended_time,
            rate_customization_id=uuid4(),
            rate_category_id=uuid4()
        )

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.manual_create_trip(dto)
        assert "End address is required" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_manual_create_trip_customization_not_found(self, service, customization_repo):
        started_time = datetime.now(timezone.utc)
        ended_time = started_time + timedelta(hours=1)
        
        dto = ManualCreateTripDTO(
            start_address="123 Main St",
            end_address="456 Oak Ave",
            miles=10.0,
            started_at=started_time,
            ended_at=ended_time,
            rate_customization_id=uuid4(),
            rate_category_id=uuid4()
        )
        customization_repo.get.return_value = None

        with pytest.raises(RateCustomizationNotFoundError):
            await service.manual_create_trip(dto)

    @pytest.mark.asyncio
    async def test_manual_create_trip_category_not_found(
        self, service, customization_repo, category_repo, mock_customization
    ):
        started_time = datetime.now(timezone.utc)
        ended_time = started_time + timedelta(hours=1)
        
        dto = ManualCreateTripDTO(
            start_address="123 Main St",
            end_address="456 Oak Ave",
            miles=10.0,
            started_at=started_time,
            ended_at=ended_time,
            rate_customization_id=mock_customization.id,
            rate_category_id=uuid4()
        )
        customization_repo.get.return_value = mock_customization
        category_repo.get.return_value = None

        with pytest.raises(RateCategoryNotFoundError):
            await service.manual_create_trip(dto)

    @pytest.mark.asyncio
    async def test_manual_create_trip_category_mismatch(
        self, service, customization_repo, category_repo, 
        mock_customization, mock_category
    ):
        started_time = datetime.now(timezone.utc)
        ended_time = started_time + timedelta(hours=1)
        
        different_customization_id = uuid4()
        mock_category.rate_customization_id = different_customization_id
        dto = ManualCreateTripDTO(
            start_address="123 Main St",
            end_address="456 Oak Ave",
            miles=10.0,
            started_at=started_time,
            ended_at=ended_time,
            rate_customization_id=mock_customization.id,
            rate_category_id=mock_category.id
        )
        customization_repo.get.return_value = mock_customization
        category_repo.get.return_value = mock_category

        with pytest.raises(InvalidRateCategoryDataError) as exc_info:
            await service.manual_create_trip(dto)
        assert "does not belong to this customization" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_manual_create_trip_negative_miles(self, service):
        started_time = datetime.now(timezone.utc)
        ended_time = started_time + timedelta(hours=1)
        
        dto = ManualCreateTripDTO(
            start_address="123 Main St",
            end_address="456 Oak Ave",
            miles=-5.0,
            started_at=started_time,
            ended_at=ended_time,
            rate_customization_id=uuid4(),
            rate_category_id=uuid4()
        )

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.manual_create_trip(dto)
        assert "Miles must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_manual_create_trip_zero_miles(self, service):
        started_time = datetime.now(timezone.utc)
        ended_time = started_time + timedelta(hours=1)
        
        dto = ManualCreateTripDTO(
            start_address="123 Main St",
            end_address="456 Oak Ave",
            miles=0.0,
            started_at=started_time,
            ended_at=ended_time,
            rate_customization_id=uuid4(),
            rate_category_id=uuid4()
        )

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.manual_create_trip(dto)
        assert "Miles must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_manual_create_trip_invalid_time_order(self, service):
        started_time = datetime.now(timezone.utc)
        ended_time = started_time - timedelta(hours=1) 
        
        dto = ManualCreateTripDTO(
            start_address="123 Main St",
            end_address="456 Oak Ave",
            miles=10.0,
            started_at=started_time,
            ended_at=ended_time,
            rate_customization_id=uuid4(),
            rate_category_id=uuid4()
        )

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.manual_create_trip(dto)
        assert "End time must be after start time" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_manual_create_trip_same_start_end_time(self, service):
        start_end_time = datetime.now(timezone.utc)
        
        dto = ManualCreateTripDTO(
            start_address="123 Main St",
            end_address="456 Oak Ave",
            miles=10.0,
            started_at=start_end_time,
            ended_at=start_end_time,
            rate_customization_id=uuid4(),
            rate_category_id=uuid4()
        )

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.manual_create_trip(dto)
        assert "End time must be after start time" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_manual_create_trip_with_expenses(
        self, service, trip_repo, category_repo, customization_repo, expense_repo,
        mock_customization, mock_category, mock_trip
    ):
        started_time = datetime.now(timezone.utc)
        ended_time = started_time + timedelta(hours=2)
        
        mock_category.rate_customization_id = mock_customization.id
        expense_data = [
            {"type": "Parking", "amount": 15.50},
            {"type": "Toll", "amount": 5.75}
        ]
        
        dto = ManualCreateTripDTO(
            start_address="123 Main St",
            end_address="456 Oak Ave",
            purpose="Business meeting",
            vehicle="Honda Civic",
            miles=25.5,
            geometry='{"type":"LineString"}',
            started_at=started_time,
            ended_at=ended_time,
            rate_customization_id=mock_customization.id,
            rate_category_id=mock_category.id,
            expenses=expense_data
        )
        
        customization_repo.get.return_value = mock_customization
        category_repo.get.return_value = mock_category
        trip_repo.save.return_value = mock_trip

        service.expense_service.create_expense = AsyncMock()

        with patch('app.modules.trips.service.encrypt_address', return_value="encrypted"):
            with patch('app.modules.trips.service.encrypt_geometry', return_value="encrypted_geom"):
                with patch('app.modules.trips.service.Trip', return_value=mock_trip):
                    result = await service.manual_create_trip(dto)

        assert result == mock_trip
        assert service.expense_service.create_expense.call_count == 2  


class TestTripsServiceGetTripById:

    @pytest.fixture
    def trip_repo(self):
        return AsyncMock(spec=TripRepo)

    @pytest.fixture
    def service(self, trip_repo):
        return TripsService(trip_repo, AsyncMock(), AsyncMock(), AsyncMock())

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.active
        trip.geometry_encrypted = "gAAAAABhZ7_get_trip_geometry_encrypted"
        return trip

    @pytest.mark.asyncio
    async def test_get_trip_by_id_success(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        trip_repo.get.return_value = mock_trip

        result = await service.get_trip_by_id(trip_id)

        assert result == mock_trip
        trip_repo.get.assert_called_once_with(trip_id)

    @pytest.mark.asyncio
    async def test_get_trip_by_id_not_found(self, service, trip_repo):
        trip_id = uuid4()
        trip_repo.get.return_value = None

        with pytest.raises(TripNotFoundError) as exc_info:
            await service.get_trip_by_id(trip_id)
        assert "doesn't exist" in str(exc_info.value)


class TestTripsServiceEndTrip:

    @pytest.fixture
    def trip_repo(self):
        repo = AsyncMock(spec=TripRepo)
        repo.db = MagicMock()
        repo.db.rollback = AsyncMock()
        return repo

    @pytest.fixture
    def service(self, trip_repo):
        return TripsService(trip_repo, AsyncMock(), AsyncMock(), AsyncMock())

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.active
        trip.reimbursement_rate = 0.65
        trip.geometry_encrypted = "gAAAAABhZ8_end_trip_geometry_encrypted"
        return trip

    @pytest.mark.asyncio
    async def test_end_trip_success(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        dto = EndTripDTO(end_address="456 Oak Ave", geometry='{"type":"LineString","coordinates":[[-122.4194,37.7749],[-122.4094,37.7849]]}', distance_meters=81320.0)
        trip_repo.get.return_value = mock_trip
        trip_repo.save.return_value = mock_trip

        with patch('app.modules.trips.service.encrypt_address', return_value="encrypted"):
            result = await service.end_trip(trip_id, dto)

        assert result == mock_trip
        assert mock_trip.miles == 50.53
        assert mock_trip.status == TripStatus.completed
        assert mock_trip.mileage_reimbursement_total == 50.53 * 0.65
        trip_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_end_trip_empty_address(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        dto = EndTripDTO(end_address="   ", geometry='{"type":"Point","coordinates":[-122.4194,37.7749]}', distance_meters=81320.0)
        trip_repo.get.return_value = mock_trip

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.end_trip(trip_id, dto)
        assert "End address is required" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_end_trip_already_completed(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        dto = EndTripDTO(end_address="456 Oak Ave", geometry='{"type":"Polygon","coordinates":[[[-122.4,37.8],[-122.4,37.7],[-122.3,37.7],[-122.3,37.8],[-122.4,37.8]]]}', distance_meters=81320.0)
        mock_trip.status = TripStatus.completed
        trip_repo.get.return_value = mock_trip

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.end_trip(trip_id, dto)
        assert "already ended" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_end_trip_cancelled(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        dto = EndTripDTO(end_address="456 Oak Ave", geometry='{"type":"MultiPoint","coordinates":[[-122.4194,37.7749],[-122.4094,37.7849]]}', distance_meters=81320.0)
        mock_trip.status = TripStatus.cancelled
        trip_repo.get.return_value = mock_trip

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.end_trip(trip_id, dto)
        assert "Cannot end a cancelled trip" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_end_trip_negative_miles(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        with pytest.raises(ValueError) as exc_info:
            dto = EndTripDTO(end_address="456 Oak Ave", geometry='{"type":"Point","coordinates":[-122.4194,37.7749]}', distance_meters=-10.5)
        assert "Distance must be non-negative" in str(exc_info.value)


class TestTripsServiceEditTrip:

    @pytest.fixture
    def trip_repo(self):
        repo = AsyncMock(spec=TripRepo)
        repo.db = MagicMock()
        repo.db.rollback = AsyncMock()
        return repo

    @pytest.fixture
    def category_repo(self):
        return AsyncMock(spec=RateCategoryRepo)

    @pytest.fixture
    def customization_repo(self):
        return AsyncMock(spec=RateCustomizationRepo)

    @pytest.fixture
    def expense_repo(self):
        return AsyncMock(spec=ExpenseRepo)

    @pytest.fixture
    def service(self, trip_repo, category_repo, customization_repo, expense_repo):
        return TripsService(trip_repo, category_repo, customization_repo, expense_repo)

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.active
        trip.rate_customization_id = uuid4()
        trip.rate_category_id = uuid4()
        trip.reimbursement_rate = 0.65
        trip.geometry_encrypted = "gAAAAABhZ9_edit_trip_geometry_encrypted"
        return trip

    @pytest.mark.asyncio
    async def test_edit_trip_purpose_only(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        dto = EditTripDTO(purpose="Updated purpose")
        trip_repo.get.return_value = mock_trip
        trip_repo.save.return_value = mock_trip

        result = await service.edit_trip(trip_id, dto)

        assert result == mock_trip
        assert mock_trip.purpose == "Updated purpose"
        trip_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_edit_trip_vehicle_only(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        dto = EditTripDTO(vehicle="Tesla Model 3")
        trip_repo.get.return_value = mock_trip
        trip_repo.save.return_value = mock_trip

        result = await service.edit_trip(trip_id, dto)

        assert result == mock_trip
        assert mock_trip.vehicle == "Tesla Model 3"
        trip_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_edit_trip_customization_only(
        self, service, trip_repo, customization_repo, mock_trip
    ):
        trip_id = uuid4()
        new_customization_id = uuid4()
        dto = EditTripDTO(rate_customization_id=new_customization_id)
        mock_customization = MagicMock(spec=RateCustomization)
        mock_customization.id = new_customization_id
        trip_repo.get.return_value = mock_trip
        customization_repo.get.return_value = mock_customization
        trip_repo.save.return_value = mock_trip

        result = await service.edit_trip(trip_id, dto)

        assert result == mock_trip
        assert mock_trip.rate_customization_id == new_customization_id
        trip_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_edit_trip_category_only(
        self, service, trip_repo, category_repo, mock_trip
    ):
        trip_id = uuid4()
        new_category_id = uuid4()
        dto = EditTripDTO(rate_category_id=new_category_id)
        mock_category = MagicMock(spec=RateCategory)
        mock_category.id = new_category_id
        mock_category.cost_per_mile = 0.85
        mock_category.rate_customization_id = mock_trip.rate_customization_id
        trip_repo.get.return_value = mock_trip
        category_repo.get.return_value = mock_category
        trip_repo.save.return_value = mock_trip

        result = await service.edit_trip(trip_id, dto)

        assert result == mock_trip
        assert mock_trip.rate_category_id == new_category_id
        assert mock_trip.reimbursement_rate == 0.85
        trip_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_edit_trip_customization_and_category(
        self, service, trip_repo, category_repo, customization_repo, mock_trip
    ):
        trip_id = uuid4()
        new_customization_id = uuid4()
        new_category_id = uuid4()
        dto = EditTripDTO(
            rate_customization_id=new_customization_id,
            rate_category_id=new_category_id
        )
        mock_customization = MagicMock(spec=RateCustomization)
        mock_customization.id = new_customization_id
        mock_category = MagicMock(spec=RateCategory)
        mock_category.id = new_category_id
        mock_category.cost_per_mile = 0.95
        mock_category.rate_customization_id = new_customization_id
        trip_repo.get.return_value = mock_trip
        customization_repo.get.return_value = mock_customization
        category_repo.get.return_value = mock_category
        trip_repo.save.return_value = mock_trip

        result = await service.edit_trip(trip_id, dto)

        assert result == mock_trip
        assert mock_trip.rate_customization_id == new_customization_id
        assert mock_trip.rate_category_id == new_category_id
        assert mock_trip.reimbursement_rate == 0.95

    @pytest.mark.asyncio
    async def test_edit_trip_category_mismatch(
        self, service, trip_repo, category_repo, mock_trip
    ):
        trip_id = uuid4()
        new_category_id = uuid4()
        dto = EditTripDTO(rate_category_id=new_category_id)
        mock_category = MagicMock(spec=RateCategory)
        mock_category.id = new_category_id
        mock_category.rate_customization_id = uuid4()
        trip_repo.get.return_value = mock_trip
        category_repo.get.return_value = mock_category

        with pytest.raises(TripPersistenceError) as exc_info:
            await service.edit_trip(trip_id, dto)
        assert "does not belong to this customization" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_edit_trip_customization_not_found(
        self, service, trip_repo, customization_repo, mock_trip
    ):
        trip_id = uuid4()
        dto = EditTripDTO(rate_customization_id=uuid4())
        trip_repo.get.return_value = mock_trip
        customization_repo.get.return_value = None

        with pytest.raises(TripPersistenceError):
            await service.edit_trip(trip_id, dto)

    @pytest.mark.asyncio
    async def test_edit_trip_category_not_found(
        self, service, trip_repo, category_repo, mock_trip
    ):
        trip_id = uuid4()
        dto = EditTripDTO(rate_category_id=uuid4())
        trip_repo.get.return_value = mock_trip
        category_repo.get.return_value = None

        with pytest.raises(TripPersistenceError):
            await service.edit_trip(trip_id, dto)


class TestTripsServiceCancelTrip:

    @pytest.fixture
    def trip_repo(self):
        return AsyncMock(spec=TripRepo)

    @pytest.fixture
    def service(self, trip_repo):
        return TripsService(trip_repo, AsyncMock(), AsyncMock(), AsyncMock())

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.active
        trip.geometry_encrypted = "gAAAAABhZ10_cancel_trip_geometry_encrypted"
        return trip

    @pytest.mark.asyncio
    async def test_cancel_trip_success(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        trip_repo.get.return_value = mock_trip
        trip_repo.save.return_value = mock_trip

        result = await service.cancel_trip(trip_id)

        assert result == mock_trip
        assert mock_trip.status == TripStatus.cancelled
        assert mock_trip.ended_at is not None
        trip_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_cancel_trip_already_completed(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        mock_trip.status = TripStatus.completed
        trip_repo.get.return_value = mock_trip

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.cancel_trip(trip_id)
        assert "Only active trips can be cancelled" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_cancel_trip_already_cancelled(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        mock_trip.status = TripStatus.cancelled
        trip_repo.get.return_value = mock_trip

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.cancel_trip(trip_id)
        assert "Only active trips can be cancelled" in str(exc_info.value)
