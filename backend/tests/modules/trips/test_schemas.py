import pytest
from uuid import uuid4
from datetime import datetime, timezone
from pydantic import ValidationError

from app.modules.trips.schemas import (
    CreateTripDTO,
    EditTripDTO,
    EndTripDTO,
    TripResponseDTO,
    ExpenseResponseDTO
)
from app.modules.trips.models import TripStatus


class TestCreateTripDTO:

    def test_create_trip_dto_valid(self):
        customization_id = uuid4()
        category_id = uuid4()

        dto = CreateTripDTO(
            start_address="123 Main St",
            purpose="Business meeting",
            vehicle="Toyota Camry",
            rate_customization_id=customization_id,
            rate_category_id=category_id
        )

        assert dto.start_address == "123 Main St"
        assert dto.purpose == "Business meeting"
        assert dto.vehicle == "Toyota Camry"
        assert dto.rate_customization_id == customization_id
        assert dto.rate_category_id == category_id

    def test_create_trip_dto_missing_required_fields(self):
        with pytest.raises(ValidationError):
            CreateTripDTO(start_address="123 Main St")

    def test_create_trip_dto_optional_purpose(self):
        customization_id = uuid4()
        category_id = uuid4()

        dto = CreateTripDTO(
            start_address="123 Main St",
            rate_customization_id=customization_id,
            rate_category_id=category_id
        )

        assert dto.start_address == "123 Main St"
        assert dto.purpose is None
        assert dto.vehicle is None


class TestEndTripDTO:

    def test_end_trip_dto_valid(self):
        dto = EndTripDTO(
            end_address="456 Oak Ave",
            geometry='{"type":"LineString","coordinates":[[-122.4194,37.7749],[-122.4094,37.7849]]}',
            distance_meters=81320.0
        )

        assert dto.end_address == "456 Oak Ave"
        assert dto.geometry == '{"type":"LineString","coordinates":[[-122.4194,37.7749],[-122.4094,37.7849]]}'
        assert dto.distance_meters == 81320.0
        assert dto.miles == 50.53

    def test_end_trip_dto_missing_required_fields(self):
        with pytest.raises(ValidationError):
            EndTripDTO(end_address="456 Oak Ave")
        
        with pytest.raises(ValidationError):
            EndTripDTO(distance_meters=81320.0)
    
    def test_end_trip_dto_negative_distance(self):
        with pytest.raises(ValidationError) as exc_info:
            EndTripDTO(end_address="456 Oak Ave", distance_meters=-100.0)
        assert "Distance must be non-negative" in str(exc_info.value)


class TestEditTripDTO:

    def test_edit_trip_dto_all_fields(self):
        customization_id = uuid4()
        category_id = uuid4()

        dto = EditTripDTO(
            purpose="Updated purpose",
            vehicle="Honda Civic",
            rate_customization_id=customization_id,
            rate_category_id=category_id
        )

        assert dto.purpose == "Updated purpose"
        assert dto.vehicle == "Honda Civic"
        assert dto.rate_customization_id == customization_id
        assert dto.rate_category_id == category_id

    def test_edit_trip_dto_partial_fields(self):
        dto1 = EditTripDTO(purpose="Updated")
        dto2 = EditTripDTO(rate_customization_id=uuid4())
        dto3 = EditTripDTO(rate_category_id=uuid4())
        dto4 = EditTripDTO(vehicle="Ford F150")

        assert dto1.purpose == "Updated"
        assert dto1.vehicle is None
        assert dto4.vehicle == "Ford F150"
        assert dto4.purpose is None
        assert dto1.rate_customization_id is None
        assert dto1.rate_category_id is None

        assert dto2.purpose is None
        assert dto2.rate_customization_id is not None
        
        assert dto3.rate_category_id is not None

    def test_edit_trip_dto_empty(self):
        dto = EditTripDTO()

        assert dto.purpose is None
        assert dto.rate_customization_id is None
        assert dto.rate_category_id is None


class TestExpenseResponseDTO:

    def test_expense_response_dto_valid(self):
        expense_id = uuid4()
        created_at = datetime.now(timezone.utc)

        dto = ExpenseResponseDTO(
            id=str(expense_id),
            type="Parking",
            amount=15.50,
            created_at=created_at
        )

        assert dto.id == str(expense_id)
        assert dto.type == "Parking"
        assert dto.amount == 15.50
        assert dto.created_at == created_at


class TestTripResponseDTO:

    def test_trip_response_dto_valid(self):
        trip_id = uuid4()
        customization_id = uuid4()
        category_id = uuid4()
        started_at = datetime.now(timezone.utc)
        updated_at = datetime.now(timezone.utc)

        dto = TripResponseDTO(
            id=str(trip_id),
            status=TripStatus.active,
            start_address="123 Main St",
            purpose="Business",
            reimbursement_rate=0.65,
            started_at=started_at,
            updated_at=updated_at,
            rate_customization_id=customization_id,
            rate_category_id=category_id
        )

        assert dto.id == str(trip_id)
        assert dto.status == TripStatus.active
        assert dto.start_address == "123 Main St"
        assert dto.purpose == "Business"
        assert dto.reimbursement_rate == 0.65

    def test_trip_response_dto_from_orm(self):
        from unittest.mock import MagicMock, patch
        from app.modules.trips.models import Trip
        
        mock_trip = MagicMock(spec=Trip)
        mock_trip.id = uuid4()
        mock_trip.status = TripStatus.active
        mock_trip.start_address_encrypted = "encrypted_start"
        mock_trip.end_address_encrypted = None
        mock_trip.purpose = "Business"
        mock_trip.vehicle = "Honda Civic"
        mock_trip.miles = None
        mock_trip.reimbursement_rate = 0.65
        mock_trip.mileage_reimbursement_total = None
        mock_trip.expense_reimbursement_total = None
        mock_trip.started_at = datetime.now(timezone.utc)
        mock_trip.ended_at = None
        mock_trip.updated_at = datetime.now(timezone.utc)
        mock_trip.rate_customization_id = uuid4()
        mock_trip.rate_category_id = uuid4()
        mock_trip.geometry_encrypted = None
        mock_trip.expenses = []

        with patch('app.modules.trips.schemas.decrypt_address', return_value="123 Main St"):
            dto = TripResponseDTO.model_validate(mock_trip)

        assert str(mock_trip.id) == dto.id
        assert dto.status == TripStatus.active
        assert dto.start_address == "123 Main St"
        assert dto.total_reimbursement == 0

    def test_trip_response_dto_with_expenses(self):
        from unittest.mock import MagicMock, patch
        from app.modules.trips.models import Trip
        from app.modules.expenses.models import Expense
        
        mock_expense1 = MagicMock(spec=Expense)
        mock_expense1.id = uuid4()
        mock_expense1.type = "Parking"
        mock_expense1.amount = 15.50
        mock_expense1.created_at = datetime.now(timezone.utc)

        mock_expense2 = MagicMock(spec=Expense)
        mock_expense2.id = uuid4()
        mock_expense2.type = "Tolls"
        mock_expense2.amount = 5.00
        mock_expense2.created_at = datetime.now(timezone.utc)

        mock_trip = MagicMock(spec=Trip)
        mock_trip.id = uuid4()
        mock_trip.status = TripStatus.completed
        mock_trip.start_address_encrypted = "encrypted_start"
        mock_trip.end_address_encrypted = "encrypted_end"
        mock_trip.purpose = "Business"
        mock_trip.vehicle = "Toyota Prius"
        mock_trip.miles = 50.0
        mock_trip.reimbursement_rate = 0.65
        mock_trip.mileage_reimbursement_total = 32.50
        mock_trip.expense_reimbursement_total = 20.50
        mock_trip.started_at = datetime.now(timezone.utc)
        mock_trip.ended_at = datetime.now(timezone.utc)
        mock_trip.updated_at = datetime.now(timezone.utc)
        mock_trip.rate_customization_id = uuid4()
        mock_trip.rate_category_id = uuid4()
        mock_trip.geometry_encrypted = None
        mock_trip.expenses = [mock_expense1, mock_expense2]

        with patch('app.modules.trips.schemas.decrypt_address', side_effect=["123 Main St", "456 Oak Ave"]):
            dto = TripResponseDTO.model_validate(mock_trip)

        assert dto.status == TripStatus.completed
        assert dto.miles == 50.0
        assert dto.total_reimbursement == 53.0
        assert len(dto.expenses) == 2
        assert dto.expenses[0].type == "Parking"
        assert dto.expenses[1].type == "Tolls"

    def test_trip_response_dto_missing_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            TripResponseDTO(
                id=str(uuid4()),
                status=TripStatus.active
            )
        
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("start_address",) for error in errors)
