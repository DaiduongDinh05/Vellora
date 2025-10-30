import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import datetime, timezone

from app.modules.trips.service import TripsService
from app.modules.trips.repository import TripRepo
from app.modules.rate_categories.repository import RateCategoryRepo
from app.modules.rate_customizations.repository import RateCustomizationRepo
from app.modules.trips.schemas import CreateTripDTO, EditTripDTO, EndTripDTO
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
    def service(self, trip_repo, category_repo, customization_repo):
        return TripsService(trip_repo, category_repo, customization_repo)

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
            rate_customization_id=mock_customization.id,
            rate_category_id=mock_category.id
        )
        customization_repo.get.return_value = mock_customization
        category_repo.get.return_value = mock_category

        with pytest.raises(InvalidRateCategoryDataError) as exc_info:
            await service.start_trip(dto)
        assert "does not belong to this customization" in str(exc_info.value)


class TestTripsServiceGetTripById:

    @pytest.fixture
    def trip_repo(self):
        return AsyncMock(spec=TripRepo)

    @pytest.fixture
    def service(self, trip_repo):
        return TripsService(trip_repo, AsyncMock(), AsyncMock())

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.active
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
        return TripsService(trip_repo, AsyncMock(), AsyncMock())

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.active
        trip.reimbursement_rate = 0.65
        return trip

    @pytest.mark.asyncio
    async def test_end_trip_success(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        dto = EndTripDTO(end_address="456 Oak Ave", distance_meters=81320.0)
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
        dto = EndTripDTO(end_address="   ", distance_meters=81320.0)
        trip_repo.get.return_value = mock_trip

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.end_trip(trip_id, dto)
        assert "End address is required" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_end_trip_already_completed(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        dto = EndTripDTO(end_address="456 Oak Ave", distance_meters=81320.0)
        mock_trip.status = TripStatus.completed
        trip_repo.get.return_value = mock_trip

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.end_trip(trip_id, dto)
        assert "already ended" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_end_trip_cancelled(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        dto = EndTripDTO(end_address="456 Oak Ave", distance_meters=81320.0)
        mock_trip.status = TripStatus.cancelled
        trip_repo.get.return_value = mock_trip

        with pytest.raises(InvalidTripDataError) as exc_info:
            await service.end_trip(trip_id, dto)
        assert "Cannot end a cancelled trip" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_end_trip_negative_miles(self, service, trip_repo, mock_trip):
        trip_id = uuid4()
        # Negative distance should be caught by Pydantic validator
        with pytest.raises(ValueError) as exc_info:
            dto = EndTripDTO(end_address="456 Oak Ave", distance_meters=-10.5)
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
    def service(self, trip_repo, category_repo, customization_repo):
        return TripsService(trip_repo, category_repo, customization_repo)

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.active
        trip.rate_customization_id = uuid4()
        trip.rate_category_id = uuid4()
        trip.reimbursement_rate = 0.65
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
        return TripsService(trip_repo, AsyncMock(), AsyncMock())

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.active
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
