import uuid
import sqlalchemy as sa
from app.core.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION


class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = (
        sa.UniqueConstraint("trip_id", "type", name="uq_expenses_trip_id_type"),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid = True), primary_key=True, index=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    trip_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), sa.ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[str] = mapped_column(sa.String(50), nullable = False)
    amount: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False)
    created_at: Mapped[sa.DateTime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)

    trip: Mapped["Trip"] = relationship("Trip", back_populates="expenses")
    user: Mapped["User"] = relationship("User", back_populates="expenses")