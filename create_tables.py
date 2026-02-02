# create_tables.py
from app.db.session import engine
from app.db.base import Base

# Import ALL models so SQLAlchemy sees them
from app.db.models.user import User
from app.db.models.job import Job
from app.db.models.recording import Recording
from app.db.models.transcripts import Transcript
from app.db.models.llm_output import LLMOutput
from app.db.models.report import Report

Base.metadata.create_all(bind=engine)
