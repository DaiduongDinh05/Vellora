from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import sqlalchemy as sa
from app.modules.reports.models import Report
from sqlalchemy.orm import selectinload

#im not committing inside the repo so the service layer can control the transaction.
# which should prevent partial writes and should keep things flexible for background jobs, retries and rollback

class ReportRepository:

    @staticmethod
    async def create(session: AsyncSession, report: Report) -> Report:
        session.add(report)
        await session.flush()
        return report

    @staticmethod
    async def get_by_id(session: AsyncSession, report_id: UUID) -> Report | None:
        result = await session.execute(
            sa.select(Report).where(Report.id == report_id)
            .options(selectinload(Report.user))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_for_user(session: AsyncSession, user_id: UUID) -> list[Report]:
        result = await session.execute(
            sa.select(Report).where(Report.user_id == user_id)
        )
        return result.scalars().all()
