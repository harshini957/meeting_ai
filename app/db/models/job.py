# app/db/models/job.py
import uuid
from sqlalchemy import String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    status: Mapped[str] = mapped_column(String, nullable=False)
    error_message: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))

    user = relationship("User", back_populates="jobs")
    recording = relationship("Recording", back_populates="job", uselist=False)
    transcript = relationship("Transcript", back_populates="job", uselist=False)
    llm_output = relationship("LLMOutput", back_populates="job", uselist=False)
    report = relationship("Report", back_populates="job", uselist=False)
