from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from .enums import RoleCode

class SystemRole(db.Model):
    __tablename__ = "system_role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    code: Mapped[RoleCode] = mapped_column(
        Enum(RoleCode, name="role_code", create_constraint=True), nullable=False
    )
    users = relationship("User", back_populates="role")
