import os
from dotenv import load_dotenv

# Load defaults from .env and optional external path
load_dotenv()
_dotenv_file = os.getenv("DOTENV_FILE")
if _dotenv_file and os.path.exists(_dotenv_file):
    load_dotenv(_dotenv_file, override=False)


def _normalized_db_url() -> str:
    # Prefer env var; otherwise default to Neon connection
    url = os.getenv(
        "DATABASE_URL",
        # Default to Neon with psycopg3 driver and required SSL
        "postgresql+psycopg://neondb_owner:npg_0TbRIMg4nqQo@ep-green-truth-adedoaj5-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
    )
    # Normalize to psycopg3 driver if a plain postgresql:// was provided
    if url.startswith("postgresql://") and "+" not in url[len("postgresql"):len("postgresql")+10]:
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = _normalized_db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
