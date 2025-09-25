from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Program(db.Model):
    __tablename__ = "program"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now(), onupdate=db.func.now())
    name: Mapped[str]
    description: Mapped[str | None]

    schedules = relationship("Schedule", back_populates="program")
    cohorts = relationship("Cohort", back_populates="program")
