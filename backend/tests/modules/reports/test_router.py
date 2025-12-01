import pytest
from datetime import date, datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.modules.reports.router import router
from app.modules.reports.service import ReportsService
from app.modules.reports.models import Report, ReportStatus
from app.modules.reports.schemas import GenerateReportDTO
from app.modules.reports.exceptions import (
    ReportNotFoundError, ReportPermissionError, ReportRateLimitError
)


@pytest.fixture
def mock_service():
    return AsyncMock(spec=ReportsService)


@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id = uuid4()
    return user


@pytest.fixture
def sample_report():
    report = MagicMock(spec=Report)
    report.id = uuid4()
    report.user_id = uuid4()
    report.start_date = date(2024, 1, 1)
    report.end_date = date(2024, 1, 31)
    report.status = ReportStatus.pending
    report.file_name = None
    report.file_url = None
    report.requested_at = datetime.now(timezone.utc)
    report.completed_at = None
    report.expires_at = None
    return report


class TestCreateReport:

    @pytest.mark.asyncio
    async def test_create_report_success(self, mock_service, mock_user, sample_report):
        from app.modules.reports.router import create_report
        
        generate_dto = GenerateReportDTO(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31)
        )
        mock_service.generate_report.return_value = sample_report

        result = await create_report(generate_dto, mock_user, mock_service)

        mock_service.generate_report.assert_called_once_with(mock_user.id, generate_dto)
        assert result.id == sample_report.id
        assert result.status == sample_report.status

    @pytest.mark.asyncio
    async def test_create_report_rate_limit_error(self, mock_service, mock_user):
        from app.modules.reports.router import create_report
        from fastapi import HTTPException
        
        generate_dto = GenerateReportDTO(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31)
        )
        mock_service.generate_report.side_effect = ReportRateLimitError("Rate limited")

        with pytest.raises(HTTPException) as exc_info:
            await create_report(generate_dto, mock_user, mock_service)
        
        assert exc_info.value.status_code == 429
        assert "Rate limited" in str(exc_info.value.detail)


class TestCheckReportStatus:

    @pytest.mark.asyncio
    async def test_check_status_success(self, mock_service, sample_report):
        from app.modules.reports.router import check_report_status
        
        report_id = uuid4()
        mock_service.get_report_status.return_value = sample_report

        result = await check_report_status(report_id, mock_service)

        mock_service.get_report_status.assert_called_once_with(report_id)
        assert result.id == sample_report.id
        assert result.status == sample_report.status

    @pytest.mark.asyncio
    async def test_check_status_not_found(self, mock_service):
        from app.modules.reports.router import check_report_status
        from fastapi import HTTPException
        
        report_id = uuid4()
        mock_service.get_report_status.side_effect = ReportNotFoundError("Not found")

        with pytest.raises(HTTPException) as exc_info:
            await check_report_status(report_id, mock_service)
        
        assert exc_info.value.status_code == 404
        assert "Not found" in str(exc_info.value.detail)


class TestDownloadReport:

    @pytest.mark.asyncio
    async def test_download_success(self, mock_service, mock_user):
        from app.modules.reports.router import download_report
        
        report_id = uuid4()
        mock_service.get_download_url.return_value = "http://example.com/report.pdf"

        result = await download_report(report_id, mock_user, mock_service)

        mock_service.get_download_url.assert_called_once_with(report_id, mock_user.id)
        assert result["download_url"] == "http://example.com/report.pdf"

    @pytest.mark.asyncio
    async def test_download_permission_denied(self, mock_service, mock_user):
        from app.modules.reports.router import download_report
        from fastapi import HTTPException
        
        report_id = uuid4()
        mock_service.get_download_url.side_effect = ReportPermissionError("Permission denied")

        with pytest.raises(HTTPException) as exc_info:
            await download_report(report_id, mock_user, mock_service)
        
        assert exc_info.value.status_code == 403
        assert "Permission denied" in str(exc_info.value.detail)


class TestListReports:

    @pytest.mark.asyncio
    async def test_list_reports_success(self, mock_service, mock_user, sample_report):
        from app.modules.reports.router import list_reports
        
        reports = [sample_report]
        mock_service.list_user_reports.return_value = reports

        result = await list_reports(mock_user, mock_service)

        mock_service.list_user_reports.assert_called_once_with(mock_user.id)
        assert len(result) == 1
        assert result[0].id == sample_report.id

    @pytest.mark.asyncio
    async def test_list_reports_empty(self, mock_service, mock_user):
        from app.modules.reports.router import list_reports
        
        mock_service.list_user_reports.return_value = []

        result = await list_reports(mock_user, mock_service)

        assert result == []


class TestRetryReport:

    @pytest.mark.asyncio
    async def test_retry_success(self, mock_service, mock_user, sample_report):
        from app.modules.reports.router import retry_report
        
        report_id = uuid4()
        mock_service.retry_report.return_value = sample_report

        result = await retry_report(report_id, mock_service, mock_user)

        mock_service.retry_report.assert_called_once_with(report_id, mock_user.id)
        assert result.id == sample_report.id

    @pytest.mark.asyncio
    async def test_retry_permission_denied(self, mock_service, mock_user):
        from app.modules.reports.router import retry_report
        from fastapi import HTTPException
        
        report_id = uuid4()
        mock_service.retry_report.side_effect = ReportPermissionError("Permission denied")

        with pytest.raises(HTTPException) as exc_info:
            await retry_report(report_id, mock_service, mock_user)
        
        assert exc_info.value.status_code == 403
        assert "Permission denied" in str(exc_info.value.detail)


class TestRegenerateReport:

    @pytest.mark.asyncio
    async def test_regenerate_success(self, mock_service, mock_user):
        from app.modules.reports.router import regenerate_report
        
        report_id = uuid4()
        mock_service.regenerate_report.return_value = {"status": "regenerating"}

        result = await regenerate_report(report_id, mock_service, mock_user)

        mock_service.regenerate_report.assert_called_once_with(report_id, mock_user.id)
        assert result["status"] == "regenerating"