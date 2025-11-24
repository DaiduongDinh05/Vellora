from uuid import UUID
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter

from app.container import get_db
from app.modules.reports.repository import ReportRepository
from app.modules.reports.service import ReportsService
from app.modules.reports.schemas import GenerateReportDTO, ReportResponse, ReportStatusResponse
from app.core.dependencies import get_current_user
from app.modules.reports.models import ReportStatus
from app.modules.reports.storage import S3ReportStorage


router = APIRouter(prefix="/reports", tags=["Reports"])

def get_reports_service(db: AsyncSession = Depends(get_db)):
    return ReportsService(db, ReportRepository())

@router.post("", response_model=ReportResponse)
async def create_report(dto: GenerateReportDTO, user=Depends(get_current_user), service: ReportsService = Depends(get_reports_service)):
    return await service.generate_report(user.id, dto)


#for frontend u might need to poll like every 3 secs or smthn so that the status get updated
@router.get("/{report_id}/status", response_model=ReportStatusResponse)
async def check_report_status(report_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = ReportRepository()
    report = await repo.get_by_id(db, report_id)

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return ReportStatusResponse(
        id=report.id,
        status=report.status,
        file_url=report.file_url
    )

@router.get("/{report_id}/download")
async def download_report(report_id: UUID, service: ReportsService = Depends(get_reports_service)):
    report = await service.repo.get_by_id(service.session, report_id)

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.status != ReportStatus.completed:
        raise HTTPException(status_code=400, detail="Report not generated yet")

    storage = S3ReportStorage()
    signed_url = storage.get_signed_url(report.file_name)

    return {"download_url": signed_url}

# @router.post("/{report_id}/generate", response_model=ReportResponse)
# async def generate_now(report_id: UUID,service: ReportsService = Depends(get_reports_service)):
#     report = await service.generate_now(report_id)
#     return ReportResponse.model_validate(report, from_attributes=True)