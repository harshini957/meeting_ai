# app/db/models/recording.py
import uuid
from sqlalchemy import String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Recording(Base):
    __tablename__ = "recordings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE")
    )
    audio_path: Mapped[str] = mapped_column(String, nullable=False)
    duration_seconds: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))

    job = relationship("Job", back_populates="recording")
