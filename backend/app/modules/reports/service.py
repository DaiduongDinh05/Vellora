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

        await self.session.commit()

        return report