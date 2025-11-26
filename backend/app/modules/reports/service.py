from datetime import datetime, timedelta, timezone
import os
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fpdf import FPDF
from app.modules.reports.schemas import GenerateReportDTO
from app.modules.reports.models import Report, ReportStatus
from app.modules.reports.repository import ReportRepository
from app.modules.reports.data_builder import ReportDataBuilder
from app.modules.reports.storage import S3ReportStorage
from app.modules.reports.renderer_fpdf import ReportPDFRenderer
from app.modules.reports.queue import ReportQueue



class ReportsService:


    def __init__(self, session: AsyncSession, repo: type[ReportRepository]):
        self.session = session
        self.repo = repo
        self.data_builder = ReportDataBuilder(session)
        self.renderer = ReportPDFRenderer()
        self.storage = S3ReportStorage()

    async def generate_report(self, user_id: UUID, dto: GenerateReportDTO) -> Report:
        report = Report(
            user_id=user_id,
            start_date=dto.start_date,
            end_date=dto.end_date,
            status=ReportStatus.pending,
        )

        created_report = await self.repo.create(self.session, report)
        await self.session.commit()
         
        queue = ReportQueue()
        queue.send(str(created_report.id))

        return created_report

    async def generate_now(self, report_id: UUID) -> Report:
        report = await self.repo.get_by_id(self.session, report_id)
        if not report:
            raise ValueError("Report not found")

        data = await self.data_builder.build(report)

        pdf_bytes = self.renderer.render(data)

        key = self.storage.save(report.id, pdf_bytes)

        report.file_name = key
        report.file_url = key
        report.status = ReportStatus.completed
        now = datetime.now(timezone.utc)
        report.completed_at = now
        report.expires_at = now + timedelta(days=90)

        await self.session.commit()
        await self.session.refresh(report)

        return report
    
    async def retry_report(self, report_id: UUID, user_id: UUID) -> Report:
        report = await self.repo.get_by_id(self.session, report_id)

        if not report:
            raise ValueError("Report not found")

        if report.user_id != user_id:
            raise PermissionError("Not allowed")

        if report.status not in {ReportStatus.failed, ReportStatus.expired}:
            raise ValueError("Only failed or expired reports can be retried")

        #reset state
        report.status = ReportStatus.pending
        report.file_url = None
        report.file_name = None
        report.expires_at = None
        report.completed_at = None

        await self.repo.update(self.session, report)
        await self.session.commit()

        #requeue
        queue = ReportQueue()
        queue.send(str(report.id))

        return report
    
    async def regenerate_report(self, report_id: UUID, user_id: UUID):
        report = await self.repo.get_by_id(self.session, report_id)

        if not report:
            raise ValueError("Report not found")

        if report.user_id != user_id:
            raise PermissionError("Not allowed")

        if report.status not in {ReportStatus.completed, ReportStatus.expired}:
            raise ValueError("Only completed or expired reports can be regenerated")

        #if file still exists in storage then try to sign it
        if report.file_name:
            if self.storage.exists(report.file_name):
                url = self.storage.get_signed_url(report.file_name)
                return {
                    "status": "available",
                    "download_url": url
                }

        #i file missing then regenerate
        report.status = ReportStatus.pending
        report.file_url = None
        report.file_name = None
        report.expires_at = None
        report.completed_at = None

        await self.repo.update(self.session, report)
        await self.session.commit()

        queue = ReportQueue()
        queue.send(str(report.id))

        return {"status": "regenerating"}