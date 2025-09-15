from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_alembic(app):
    uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    if uri:
        os.environ.setdefault("SQLALCHEMY_DATABASE_URI", uri)
