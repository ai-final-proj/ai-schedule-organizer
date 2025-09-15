"""seed base data

Revision ID: b096446ff2bc
Revises: acdb96132faf
Create Date: 2025-09-09 19:54:52.919196
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b096446ff2bc"
down_revision: Union[str, None] = "acdb96132faf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Roles ---
    op.execute(
        sa.text(
            """
            INSERT INTO system_role (name, description, code) VALUES
              ('Admin', 'System administrator', 'admin'),
              ('Instructor', 'Main instructor', 'instructor'),
              ('Learner', 'Student learner', 'learner'),
              ('Replacement Instructor', 'Backup instructor', 'replacement_instructor'),
              ('Visiting Instructor', 'Guest instructor', 'visiting_instructor');
            """
        )
    )



    # --- Programs ---
    op.execute(
        sa.text(
            """
            INSERT INTO program (name, description) VALUES
              ('Intro to VR', 'Virtual reality basics'),
              ('Data Science 101', 'Fundamentals of data science');
            """
        )
    )






def downgrade() -> None:
    # Reverse order to satisfy FKs. This clears seeded data.
    op.execute(sa.text("DELETE FROM schedule_item"))
    op.execute(sa.text("DELETE FROM period"))
    op.execute(sa.text('DELETE FROM "user"'))           # seeded users
    op.execute(sa.text("DELETE FROM schedule"))
    op.execute(sa.text("DELETE FROM program"))          # seeded programs
    op.execute(sa.text("DELETE FROM cohort_subgroup"))  # seeded subgroups
    op.execute(sa.text("DELETE FROM cohort"))           # seeded cohorts
    op.execute(sa.text("DELETE FROM system_role"))      # seeded roles
