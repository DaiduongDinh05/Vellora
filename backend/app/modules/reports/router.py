from datetime import datetime, timezone
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
    try:
        return await service.generate_report(user.id, dto)
    except ValueError as e:
        raise HTTPException(status_code=429, detail=str(e))


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
    
    if report.expires_at and report.expires_at < datetime.now(timezone.utc):
        report.status = ReportStatus.expired
        await service.session.commit()
        raise HTTPException(status_code=410, detail="Report expired please regenerate")

    if report.status != ReportStatus.completed:
        raise HTTPException(status_code=400, detail="Report not generated yet")

    storage = S3ReportStorage()

    if not storage.exists(report.file_name):
        report.status = ReportStatus.expired
        await service.session.commit()
        raise HTTPException(status_code=410, detail="Report no longer available and must be regenerated")

    signed_url = storage.get_signed_url(report.file_name)

    return {"download_url": signed_url}

@router.get("/history", response_model=list[ReportResponse])
async def list_reports(user = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    repo = ReportRepository()
    reports = await repo.list_for_user(db, user.id)
    reports.sort(key=lambda r: r.requested_at, reverse=True)
    now = datetime.now(timezone.utc)
    changed = False
    for report in reports:
        if (report.status == ReportStatus.completed and report.expires_at and report.expires_at < now):
            report.status = ReportStatus.expired
            changed = True

    if changed:
        await db.commit()

    return [
        ReportResponse.model_validate(r, from_attributes=True)
        for r in reports
    ]

@router.post("/{report_id}/retry", response_model=ReportResponse)
async def retry_report(report_id: UUID, service: ReportsService = Depends(get_reports_service),user=Depends(get_current_user)):
    try:
        report = await service.retry_report(report_id, user.id)
        return ReportResponse.model_validate(report, from_attributes=True)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except PermissionError:
        raise HTTPException(status_code=403, detail="Not allowed")

@router.post("/{report_id}/regenerate")
async def regenerate_report(report_id: UUID,service: ReportsService = Depends(get_reports_service),user=Depends(get_current_user)):
    try:
        result = await service.regenerate_report(report_id, user.id)
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except PermissionError:
        raise HTTPException(status_code=403, detail="Not allowed")
