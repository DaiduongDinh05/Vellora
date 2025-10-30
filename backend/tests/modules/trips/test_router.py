import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from fastapi import HTTPException

from app.modules.trips.router import get_trips_service
from app.modules.trips.service import TripsService
from app.modules.trips.schemas import CreateTripDTO, EditTripDTO, EndTripDTO
from app.modules.trips.models import Trip, TripStatus
from app.modules.trips.exceptions import (
    InvalidTripDataError,
    TripNotFoundError,
    TripPersistenceError
)
from app.modules.rate_customizations.exceptions import RateCustomizationNotFoundError
from app.modules.rate_categories.exceptions import InvalidRateCategoryDataError, RateCategoryNotFoundError


class TestStartTripEndpoint:

    @pytest.fixture
    def mock_service(self):
        return AsyncMock(spec=TripsService)

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.active
        trip.start_address_encrypted = "encrypted"
        trip.purpose = "Business"
        trip.reimbursement_rate = 0.65
        trip.rate_customization_id = uuid4()
        trip.rate_category_id = uuid4()
        trip.expenses = []
        return trip

    @pytest.mark.asyncio
    async def test_start_trip_success(self, mock_service, mock_trip):
        from app.modules.trips.router import start_trip
        
        body = CreateTripDTO(
            start_address="123 Main St",
            purpose="Business",
            rate_customization_id=uuid4(),
            rate_category_id=uuid4()
        )
        mock_service.start_trip.return_value = mock_trip

        with patch('app.modules.trips.router.TripResponseDTO.model_validate') as mock_validate:
            mock_validate.return_value = MagicMock()
            result = await start_trip(body, mock_service)

        mock_service.start_trip.assert_called_once_with(body)
        mock_validate.assert_called_once_with(mock_trip)

    @pytest.mark.asyncio
    async def test_start_trip_invalid_data(self, mock_service):
        from app.modules.trips.router import start_trip
        
        body = CreateTripDTO(
            start_address="",
            purpose="Business",
            rate_customization_id=uuid4(),
            rate_category_id=uuid4()
        )
        mock_service.start_trip.side_effect = InvalidTripDataError("Start address is required")

        with pytest.raises(HTTPException) as exc_info:
            await start_trip(body, mock_service)
        
        assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_start_trip_customization_not_found(self, mock_service):
        from app.modules.trips.router import start_trip
        
        body = CreateTripDTO(
            start_address="123 Main St",
            purpose="Business",
            rate_customization_id=uuid4(),
            rate_category_id=uuid4()
        )
        mock_service.start_trip.side_effect = RateCustomizationNotFoundError("Not found")

        with pytest.raises(HTTPException) as exc_info:
            await start_trip(body, mock_service)
        
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_start_trip_category_not_found(self, mock_service):
        from app.modules.trips.router import start_trip
        
        body = CreateTripDTO(
            start_address="123 Main St",
            purpose="Business",
            rate_customization_id=uuid4(),
            rate_category_id=uuid4()
        )
        mock_service.start_trip.side_effect = RateCategoryNotFoundError("Not found")

        with pytest.raises(HTTPException) as exc_info:
            await start_trip(body, mock_service)
        
        assert exc_info.value.status_code == 404


class TestGetTripEndpoint:

    @pytest.fixture
    def mock_service(self):
        return AsyncMock(spec=TripsService)

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.active
        return trip

    @pytest.mark.asyncio
    async def test_get_trip_success(self, mock_service, mock_trip):
        from app.modules.trips.router import get_trip
        
        trip_id = uuid4()
        mock_service.get_trip_by_id.return_value = mock_trip

        with patch('app.modules.trips.router.TripResponseDTO.model_validate') as mock_validate:
            mock_validate.return_value = MagicMock()
            result = await get_trip(trip_id, mock_service)

        mock_service.get_trip_by_id.assert_called_once_with(trip_id)
        mock_validate.assert_called_once_with(mock_trip)

    @pytest.mark.asyncio
    async def test_get_trip_not_found(self, mock_service):
        from app.modules.trips.router import get_trip
        
        trip_id = uuid4()
        mock_service.get_trip_by_id.side_effect = TripNotFoundError("Not found")

        with pytest.raises(HTTPException) as exc_info:
            await get_trip(trip_id, mock_service)
        
        assert exc_info.value.status_code == 404


class TestEndTripEndpoint:

    @pytest.fixture
    def mock_service(self):
        return AsyncMock(spec=TripsService)

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.completed
        return trip

    @pytest.mark.asyncio
    async def test_end_trip_success(self, mock_service, mock_trip):
        from app.modules.trips.router import end_trip
        
        trip_id = uuid4()
        body = EndTripDTO(end_address="456 Oak Ave", distance_meters=81320.0)
        mock_service.end_trip.return_value = mock_trip

        with patch('app.modules.trips.router.TripResponseDTO.model_validate') as mock_validate:
            mock_validate.return_value = MagicMock()
            result = await end_trip(trip_id, body, mock_service)

        mock_service.end_trip.assert_called_once_with(trip_id, body)
        mock_validate.assert_called_once_with(mock_trip)

    @pytest.mark.asyncio
    async def test_end_trip_invalid_data(self, mock_service):
        from app.modules.trips.router import end_trip
        
        trip_id = uuid4()
        body = EndTripDTO(end_address="", distance_meters=81320.0)
        mock_service.end_trip.side_effect = InvalidTripDataError("End address is required")

        with pytest.raises(HTTPException) as exc_info:
            await end_trip(trip_id, body, mock_service)
        
        assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_end_trip_not_found(self, mock_service):
        from app.modules.trips.router import end_trip
        
        trip_id = uuid4()
        body = EndTripDTO(end_address="456 Oak Ave", distance_meters=81320.0)
        mock_service.end_trip.side_effect = TripNotFoundError("Not found")

        with pytest.raises(HTTPException) as exc_info:
            await end_trip(trip_id, body, mock_service)
        
        assert exc_info.value.status_code == 404


class TestEditTripEndpoint:

    @pytest.fixture
    def mock_service(self):
        return AsyncMock(spec=TripsService)

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.active
        trip.purpose = "Updated"
        return trip

    @pytest.mark.asyncio
    async def test_edit_trip_success(self, mock_service, mock_trip):
        from app.modules.trips.router import edit_trip
        
        trip_id = uuid4()
        body = EditTripDTO(purpose="Updated")
        mock_service.edit_trip.return_value = mock_trip

        with patch('app.modules.trips.router.TripResponseDTO.model_validate') as mock_validate:
            mock_validate.return_value = MagicMock()
            result = await edit_trip(trip_id, body, mock_service)

        mock_service.edit_trip.assert_called_once_with(trip_id, body)
        mock_validate.assert_called_once_with(mock_trip)

    @pytest.mark.asyncio
    async def test_edit_trip_not_found(self, mock_service):
        from app.modules.trips.router import edit_trip
        
        trip_id = uuid4()
        body = EditTripDTO(purpose="Updated")
        mock_service.edit_trip.side_effect = TripNotFoundError("Not found")

        with pytest.raises(HTTPException) as exc_info:
            await edit_trip(trip_id, body, mock_service)
        
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_edit_trip_invalid_category(self, mock_service):
        from app.modules.trips.router import edit_trip
        
        trip_id = uuid4()
        body = EditTripDTO(rate_category_id=uuid4())
        mock_service.edit_trip.side_effect = InvalidRateCategoryDataError("Category mismatch")

        with pytest.raises(HTTPException) as exc_info:
            await edit_trip(trip_id, body, mock_service)
        
        assert exc_info.value.status_code == 400


class TestCancelTripEndpoint:

    @pytest.fixture
    def mock_service(self):
        return AsyncMock(spec=TripsService)

    @pytest.fixture
    def mock_trip(self):
        trip = MagicMock(spec=Trip)
        trip.id = uuid4()
        trip.status = TripStatus.cancelled
        return trip

    @pytest.mark.asyncio
    async def test_cancel_trip_success(self, mock_service, mock_trip):
        from app.modules.trips.router import cancel_trip
        
        trip_id = uuid4()
        mock_service.cancel_trip.return_value = mock_trip

        with patch('app.modules.trips.router.TripResponseDTO.model_validate') as mock_validate:
            mock_validate.return_value = MagicMock()
            result = await cancel_trip(trip_id, mock_service)

        mock_service.cancel_trip.assert_called_once_with(trip_id)
        mock_validate.assert_called_once_with(mock_trip)

    @pytest.mark.asyncio
    async def test_cancel_trip_not_found(self, mock_service):
        from app.modules.trips.router import cancel_trip
        
        trip_id = uuid4()
        mock_service.cancel_trip.side_effect = TripNotFoundError("Not found")

        with pytest.raises(HTTPException) as exc_info:
            await cancel_trip(trip_id, mock_service)
        
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_cancel_trip_invalid_status(self, mock_service):
        from app.modules.trips.router import cancel_trip
        
        trip_id = uuid4()
        mock_service.cancel_trip.side_effect = InvalidTripDataError("Only active trips can be cancelled")

        with pytest.raises(HTTPException) as exc_info:
            await cancel_trip(trip_id, mock_service)
        
        assert exc_info.value.status_code == 400


class TestGetTripsServiceDependency:

    def test_get_service_returns_service(self):
        from unittest.mock import MagicMock
        
        mock_db = MagicMock()
        
        service = get_trips_service(mock_db)
        
        assert isinstance(service, TripsService)
