# app/db/models/report.py
import uuid
from sqlalchemy import String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE")
    )
    pdf_path: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))

    job = relationship("Job", back_populates="report")
