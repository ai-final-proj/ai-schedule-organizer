import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    # Use DATABASE_URL if provided; otherwise default to a local SQLite file for dev
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///ai_schedule.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
