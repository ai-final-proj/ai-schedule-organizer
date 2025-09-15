from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Program(db.Model):
    __tablename__ = "program"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]

    schedules = relationship("Schedule", back_populates="program")
