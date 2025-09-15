# backend/models/schedule.py
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime
from ..db import db

class Schedule(db.Model):
    __tablename__ = "schedule"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    program_id: Mapped[int | None] = mapped_column(db.ForeignKey("program.id"))
    cohort_id: Mapped[int | None] = mapped_column(db.ForeignKey("cohort.id"))
    subgroup_id: Mapped[int | None] = mapped_column(db.ForeignKey("cohort_subgroup.id"))

    program = relationship("Program", back_populates="schedules")
    cohort = relationship("Cohort", back_populates="schedules")
    subgroup = relationship("CohortSubgroup", back_populates="schedules")
    items = relationship("ScheduleItem", back_populates="schedule", cascade="all, delete-orphan")

class ScheduleItem(db.Model):
    __tablename__ = "schedule_item"
    id: Mapped[int] = mapped_column(primary_key=True)
    schedule_id: Mapped[int] = mapped_column(db.ForeignKey("schedule.id"), nullable=False)
    program_id: Mapped[int | None] = mapped_column(db.ForeignKey("program.id"))
    period_id: Mapped[int | None] = mapped_column(db.ForeignKey("period.id"))
    cohort_id: Mapped[int | None] = mapped_column(db.ForeignKey("cohort.id"))
    subgroup_id: Mapped[int | None] = mapped_column(db.ForeignKey("cohort_subgroup.id"))

    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    end_date:   Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)

    schedule = relationship("Schedule", back_populates="items")
    program = relationship("Program")
    period = relationship("Period", back_populates="schedule_items")
    cohort = relationship("Cohort")
    subgroup = relationship("CohortSubgroup")
