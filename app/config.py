# app/config.py
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:harshini@127.0.0.1:5433/ai_llm_db"
)
