import os
from dotenv import load_dotenv
from sqlalchemy.engine import make_url

# Load defaults from .env and optional external path
load_dotenv()
_dotenv_file = os.getenv("DOTENV_FILE")
if _dotenv_file and os.path.exists(_dotenv_file):
    load_dotenv(_dotenv_file, override=False)


NEON_DEFAULT = (
    "postgresql+psycopg://neondb_owner:npg_0TbRIMg4nqQo@"
    "ep-green-truth-adedoaj5-pooler.c-2.us-east-1.aws.neon.tech/neondb?"
    "sslmode=require&channel_binding=require"
)


def _normalized_db_url() -> str:
    # Prefer env var; otherwise default to Neon connection
    env_url = os.getenv("DATABASE_URL")
    url = env_url or NEON_DEFAULT

    # Normalize to psycopg3 driver if a plain postgresql:// was provided
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

    # Validate URL; if invalid and came from env, fall back to Neon
    try:
        make_url(url)
    except Exception as e:
        if env_url:
            # Env provided but invalid; warn and fallback
            print(f"[warn] Invalid DATABASE_URL provided; falling back to Neon. Reason: {e}", flush=True)
            return NEON_DEFAULT
    return url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = _normalized_db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
