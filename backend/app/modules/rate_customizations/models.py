from app.core.base import Base
import uuid
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
class RateCustomization(Base):
    __tablename__ = "rate_customizations"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4) 
    #userid will be added once implemented
    name: Mapped[str] = mapped_column(sa.String(60), nullable=False)
    description: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    year: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    created_at: Mapped[sa.DateTime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    trips: Mapped[list["Trip"]] = relationship("Trip", back_populates="rate_customization")
    #once userid is implemnted i will add a unique constraint so users cant have the same name for multiple customziations.
    # __table_args__ = (
    #     sa.UniqueConstraint("user_id", "name", name="uq_rate_customizations_user_name"),
    # )