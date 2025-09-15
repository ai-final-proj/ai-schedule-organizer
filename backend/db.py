from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import os

db = SQLAlchemy()

def init_alembic(app):
    os.environ.setdefault("SQLALCHEMY_DATABASE_URI", app.config["SQLALCHEMY_DATABASE_URI"])
