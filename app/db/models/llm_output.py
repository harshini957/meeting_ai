# app/db/models/llm_output.py
import uuid
from sqlalchemy import Text, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class LLMOutput(Base):
    __tablename__ = "llm_outputs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE")
    )
    provider: Mapped[str] = mapped_column(String, default="gemini")
    structured_output: Mapped[dict] = mapped_column(JSONB, nullable=False)
    raw_output: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))

    job = relationship("Job", back_populates="llm_output")
