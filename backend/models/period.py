from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from .enums import PeriodCategory

class Period(db.Model):
    __tablename__ = "period"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    instructor_id: Mapped[int | None] = mapped_column(db.ForeignKey("user.id"))
    location_url: Mapped[str | None]
    capacity: Mapped[int | None]
    category: Mapped[PeriodCategory] = mapped_column(
        Enum(PeriodCategory, name="period_category", create_constraint=True), nullable=False
    )

    instructor = relationship("User", back_populates="periods_as_instructor")
    schedule_items = relationship("ScheduleItem", back_populates="period")
