from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from .enums import UserStatus

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    role_id: Mapped[int] = mapped_column(db.ForeignKey("system_role.id"), nullable=False)
    cohort_id: Mapped[int | None] = mapped_column(db.ForeignKey("cohort.id"))
    subgroup_id: Mapped[int | None] = mapped_column(db.ForeignKey("cohort_subgroup.id"))
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status", create_constraint=True), nullable=False
    )

    role = relationship("SystemRole", back_populates="users")
    cohort = relationship("Cohort", back_populates="users")
    subgroup = relationship("CohortSubgroup", back_populates="users")
    periods_as_instructor = relationship("Period", back_populates="instructor")
