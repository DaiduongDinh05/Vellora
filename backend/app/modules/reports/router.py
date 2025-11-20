from uuid import UUID
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter

from app.container import get_db
from app.modules.reports.repository import ReportRepository
from app.modules.reports.service import ReportsService
from app.modules.reports.schemas import GenerateReportDTO, ReportResponse
from app.core.dependencies import get_current_user


router = APIRouter(prefix="/reports", tags=["Reports"])

def get_reports_service(db: AsyncSession = Depends(get_db)):
    return ReportsService(db, ReportRepository())

@router.post("", response_model=ReportResponse)
async def create_report(dto: GenerateReportDTO, user=Depends(get_current_user), service: ReportsService = Depends(get_reports_service)):
    return await service.generate_report(user.id, dto)

@router.post("/{report_id}/generate", response_model=ReportResponse)
async def generate_now(report_id: UUID,service: ReportsService = Depends(get_reports_service)):
    report = await service.generate_now(report_id)
    return ReportResponse.model_validate(report, from_attributes=True)