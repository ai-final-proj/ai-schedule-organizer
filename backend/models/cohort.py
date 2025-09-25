from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Cohort(db.Model):
    __tablename__ = "cohort"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now(), onupdate=db.func.now())
    name: Mapped[str]
    description: Mapped[str | None]
    program_id: Mapped[int | None] = mapped_column(db.ForeignKey("program.id"))

    program = relationship("Program", back_populates="cohorts")
    subgroups = relationship("CohortSubgroup", back_populates="cohort", cascade="all, delete-orphan")
    users = relationship("User", back_populates="cohort")
    schedules = relationship("Schedule", back_populates="cohort")

class CohortSubgroup(db.Model):
    __tablename__ = "cohort_subgroup"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now(), onupdate=db.func.now())
    name: Mapped[str]
    cohort_id: Mapped[int] = mapped_column(db.ForeignKey("cohort.id"), nullable=False)

    cohort = relationship("Cohort", back_populates="subgroups")
    users = relationship("User", back_populates="subgroup")
    schedules = relationship("Schedule", back_populates="subgroup")
