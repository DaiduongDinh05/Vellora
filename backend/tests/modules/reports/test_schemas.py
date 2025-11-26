import pytest
from datetime import date, datetime
from uuid import uuid4
from pydantic import ValidationError

from app.modules.reports.schemas import GenerateReportDTO, ReportResponse, ReportStatusResponse
from app.modules.reports.models import ReportStatus


class TestGenerateReportDTO:

    def test_valid_date_range(self):
        dto = GenerateReportDTO(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31)
        )
        assert dto.start_date == date(2024, 1, 1)
        assert dto.end_date == date(2024, 1, 31)

    def test_same_start_end_date(self):
        dto = GenerateReportDTO(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 1)
        )
        assert dto.start_date == dto.end_date

    def test_end_date_before_start_date_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            GenerateReportDTO(
                start_date=date(2024, 1, 31),
                end_date=date(2024, 1, 1)
            )
        assert "end_date cannot be earlier than start_date" in str(exc_info.value)


class TestReportResponse:

    def test_valid_response_creation(self):
        response = ReportResponse(
            id=uuid4(),
            user_id=uuid4(),
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            status="pending",
            file_name=None,
            file_url=None,
            requested_at=datetime.now(),
            completed_at=None,
            expires_at=None
        )
        assert response.status == "pending"
        assert response.file_name is None


class TestReportStatusResponse:

    def test_valid_status_response(self):
        response = ReportStatusResponse(
            id=uuid4(),
            status=ReportStatus.pending,
            file_url=None
        )
        assert response.status == ReportStatus.pending
        assert response.file_url is None