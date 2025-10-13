import enum
import uuid
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION
from app.core.base import Base


class TripStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"

class TripCategory(str, enum.Enum):
    business = "business"
    personal = "personal"


class Trip(Base):
    __tablename__ = "trips"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    #user_id will be added once implemented
    status: Mapped[TripStatus] = mapped_column(sa.Enum(TripStatus, name="trip_status"), default=TripStatus.active, nullable=False)
    start_address_encrypted: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    end_address_encrypted: Mapped[str | None] = mapped_column(sa.String(128), nullable=True)
    category: Mapped[TripCategory] = mapped_column(sa.Enum(TripCategory, name="trip_category"), default=TripCategory.business, nullable=False)
    purpose: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    reimbursement_rate: Mapped[float | None] = mapped_column(DOUBLE_PRECISION, nullable=True)
    started_at: Mapped[sa.DateTime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    ended_at: Mapped[sa.DateTime | None] = mapped_column(sa.DateTime(timezone=True), nullable=True)
    expenses: Mapped[list["Expense"]] = relationship("Expense", back_populates="trip", cascade="all, delete-orphan")
    #customization will be added once implemented
    #category will be added once implemented


    

     
