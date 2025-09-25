import os
from dotenv import load_dotenv

load_dotenv()
# Optionally load an explicit .env path if provided by the runtime
_dotenv_file = os.getenv("DOTENV_FILE")
if _dotenv_file and os.path.exists(_dotenv_file):
    load_dotenv(_dotenv_file, override=False)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    # PostgreSQL database connection - DATABASE_URL is required
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Validate DATABASE_URL at module import time
if not Config.SQLALCHEMY_DATABASE_URI:
    raise ValueError("DATABASE_URL environment variable is required for PostgreSQL connection")
