import os
from dotenv import load_dotenv

load_dotenv()
# Optionally load an explicit .env path if provided by the runtime
_dotenv_file = os.getenv("DOTENV_FILE")
if _dotenv_file and os.path.exists(_dotenv_file):
    load_dotenv(_dotenv_file, override=False)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    # Use DATABASE_URL if provided; otherwise default to a local SQLite file for dev
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///ai_schedule.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
