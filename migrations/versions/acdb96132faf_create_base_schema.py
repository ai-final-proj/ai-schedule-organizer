"""create base schema

Revision ID: acdb96132faf
Revises: 
Create Date: 2025-09-09 19:54:29.972750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acdb96132faf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop old tables if they exist
    op.execute("DROP TABLE IF EXISTS schedule_item CASCADE;")
    op.execute("DROP TABLE IF EXISTS period CASCADE;")
    op.execute('DROP TABLE IF EXISTS public."user" CASCADE;')
    op.execute("DROP TABLE IF EXISTS system_role CASCADE;")
    op.execute("DROP TABLE IF EXISTS schedule CASCADE;")
    op.execute("DROP TABLE IF EXISTS program CASCADE;")
    op.execute("DROP TABLE IF EXISTS cohort_subgroup CASCADE;")
    op.execute("DROP TABLE IF EXISTS cohort CASCADE;")

    # Drop enums if they exist
    op.execute("DROP TYPE IF EXISTS role_code CASCADE;")
    op.execute("DROP TYPE IF EXISTS user_status CASCADE;")
    op.execute("DROP TYPE IF EXISTS period_category CASCADE;")

    # Create ENUM types
    op.execute("""
        CREATE TYPE role_code AS ENUM (
            'instructor',
            'learner',
            'admin',
            'replacement_instructor',
            'visiting_instructor'
        );
    """)

    op.execute("""
        CREATE TYPE user_status AS ENUM (
            'active',
            'inactive'
        );
    """)

    op.execute("""
        CREATE TYPE period_category AS ENUM (
            'virtual_reality',
            'face_to_face',
            'assessment',
            'learning_course',
            'other'
        );
    """)

    # Create tables
    op.execute("""
        CREATE TABLE program (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            name VARCHAR(255) NOT NULL,
            description TEXT
        );
    """)

    op.execute("""
        CREATE TABLE cohort (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            name VARCHAR(255) NOT NULL,
            description TEXT,
            program_id INTEGER REFERENCES program(id)
        );
    """)

    op.execute("""
        CREATE TABLE cohort_subgroup (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            name VARCHAR(255) NOT NULL,
            cohort_id INTEGER NOT NULL REFERENCES cohort(id)
        );
    """)

    op.execute("""
        CREATE TABLE schedule (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            name VARCHAR(255) NOT NULL,
            description TEXT,
            program_id INTEGER REFERENCES program(id),
            cohort_id INTEGER REFERENCES cohort(id),
            subgroup_id INTEGER REFERENCES cohort_subgroup(id)
        );
    """)

    op.execute("""
        CREATE TABLE system_role (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            name VARCHAR(255) NOT NULL,
            description TEXT,
            code role_code NOT NULL
        );
    """)

    op.execute('''
        CREATE TABLE public."user" (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            role_id INTEGER NOT NULL REFERENCES system_role(id),
            cohort_id INTEGER REFERENCES cohort(id),
            subgroup_id INTEGER REFERENCES cohort_subgroup(id),
            status user_status NOT NULL
        );
    ''')

    op.execute("""
        CREATE TABLE period (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            name VARCHAR(255) NOT NULL,
            description TEXT,
            instructor_id INTEGER REFERENCES public."user"(id),
            location_url VARCHAR(512),
            capacity INTEGER,
            category period_category NOT NULL
        );
    """)

    op.execute("""
        CREATE TABLE schedule_item (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            schedule_id INTEGER NOT NULL REFERENCES schedule(id),
            program_id INTEGER REFERENCES program(id),
            period_id INTEGER REFERENCES period(id),
            cohort_id INTEGER REFERENCES cohort(id),
            subgroup_id INTEGER REFERENCES cohort_subgroup(id),
            start_date TIMESTAMP NOT NULL,
            end_date TIMESTAMP NOT NULL
        );
    """)


def downgrade() -> None:
    # Drop tables in reverse order
    op.execute("DROP TABLE IF EXISTS schedule_item CASCADE;")
    op.execute("DROP TABLE IF EXISTS period CASCADE;")
    op.execute('DROP TABLE IF EXISTS public."user" CASCADE;')
    op.execute("DROP TABLE IF EXISTS system_role CASCADE;")
    op.execute("DROP TABLE IF EXISTS schedule CASCADE;")
    op.execute("DROP TABLE IF EXISTS program CASCADE;")
    op.execute("DROP TABLE IF EXISTS cohort_subgroup CASCADE;")
    op.execute("DROP TABLE IF EXISTS cohort CASCADE;")

    # Drop ENUM types
    op.execute("DROP TYPE IF EXISTS role_code CASCADE;")
    op.execute("DROP TYPE IF EXISTS user_status CASCADE;")
    op.execute("DROP TYPE IF EXISTS period_category CASCADE;")
