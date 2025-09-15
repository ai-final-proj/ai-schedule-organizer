from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Cohort(db.Model):
    __tablename__ = "cohort"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]

    subgroups = relationship("CohortSubgroup", back_populates="cohort", cascade="all, delete-orphan")
    users = relationship("User", back_populates="cohort")
    schedules = relationship("Schedule", back_populates="cohort")

class CohortSubgroup(db.Model):
    __tablename__ = "cohort_subgroup"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    cohort_id: Mapped[int] = mapped_column(db.ForeignKey("cohort.id"), nullable=False)

    cohort = relationship("Cohort", back_populates="subgroups")
    users = relationship("User", back_populates="subgroup")
    schedules = relationship("Schedule", back_populates="subgroup")
