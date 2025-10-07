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
    # Seed Data
    op.execute("""
        INSERT INTO system_role (name, description, code, created_at, updated_at) VALUES
        ('Admin', 'System administrator', 'admin', NOW(), NOW()),
        ('Instructor', 'Main instructor', 'instructor', NOW() - interval '1 day', NOW() - interval '1 day'),
        ('Learner', 'Student learner', 'learner', NOW() - interval '2 days', NOW() - interval '2 days'),
        ('Replacement Instructor', 'Backup instructor', 'replacement_instructor', NOW() - interval '3 days', NOW() - interval '3 days'),
        ('Visiting Instructor', 'Guest instructor', 'visiting_instructor', NOW() - interval '4 days', NOW() - interval '4 days');
    """)

    op.execute("""
        INSERT INTO program (name, description, created_at, updated_at) VALUES
        ('Intro to VR', 'Virtual reality basics', NOW() - interval '6 days', NOW() - interval '5 days'),
        ('Data Science 101', 'Fundamentals of data science', NOW() - interval '5 days', NOW() - interval '4 days');
    """)

    op.execute("""
        INSERT INTO cohort (name, description, program_id, created_at, updated_at) VALUES
        ('Cohort 1', 'First test cohort', 1, NOW() - interval '5 days', NOW() - interval '4 days'),
        ('Cohort 2', 'Second test cohort', 2, NOW() - interval '3 days', NOW() - interval '2 days');
    """)

    op.execute("""
        INSERT INTO cohort_subgroup (name, cohort_id, created_at, updated_at) VALUES
        ('Subgroup A', 1, NOW() - interval '4 days', NOW() - interval '3 days'),
        ('Subgroup B', 1, NOW() - interval '3 days', NOW() - interval '2 days'),
        ('Subgroup C', 2, NOW() - interval '2 days', NOW() - interval '1 day');
    """)

    op.execute('''
        INSERT INTO public."user" (name, email, role_id, status, created_at, updated_at)
        VALUES ('Admin User', 'admin@example.com', 1, 'active', NOW(), NOW());
    ''')

    # Instructors
    op.execute('''
        INSERT INTO public."user" (name, email, role_id, status, created_at, updated_at)
        SELECT 
          'Instructor ' || LPAD(n::text, 3, '0'),
          'instructor' || LPAD(n::text, 3, '0') || '@example.com',
          2,
          'active',
          NOW() - (n || ' days')::interval,
          NOW() - ((n - 1) || ' days')::interval
        FROM generate_series(1,5) AS n;
    ''')

    # Visiting Instructors (role_id = 5)
    op.execute('''
        INSERT INTO public."user" (name, email, role_id, status, created_at, updated_at)
        VALUES 
          ('Visiting Instructor 001', 'visiting001@example.com', 5, 'active', NOW() - INTERVAL '10 minutes', NOW() - INTERVAL '10 minutes'),
          ('Visiting Instructor 002', 'visiting002@example.com', 5, 'active', NOW() - INTERVAL '9 minutes', NOW() - INTERVAL '9 minutes');
    ''')

    # Replacement Instructors (role_id = 4)
    op.execute('''
        INSERT INTO public."user" (name, email, role_id, status, created_at, updated_at)
        VALUES 
          ('Replacement Instructor 001', 'replacement001@example.com', 4, 'active', NOW() - INTERVAL '8 minutes', NOW() - INTERVAL '8 minutes'),
          ('Replacement Instructor 002', 'replacement002@example.com', 4, 'active', NOW() - INTERVAL '7 minutes', NOW() - INTERVAL '7 minutes');
    ''')

    # Learners Cohort 1
    op.execute('''
        INSERT INTO public."user" (name, email, role_id, status, cohort_id, subgroup_id, created_at, updated_at)
        SELECT 
          'Learner ' || LPAD(n::text, 3, '0'),
          'learner' || LPAD(n::text, 3, '0') || '@example.com',
          3,
          'active',
          1,
          CASE WHEN n % 2 = 0 THEN 1 ELSE 2 END,
          NOW() - (n || ' hours')::interval,
          NOW() - ((n + 1) || ' hours')::interval
        FROM generate_series(1,50) AS n;
    ''')

    # Learners Cohort 2
    op.execute('''
        INSERT INTO public."user" (name, email, role_id, status, cohort_id, subgroup_id, created_at, updated_at)
        SELECT 
          'Learner_' || LPAD((n+50)::text, 3, '0'),
          'learner' || (n+50)::text || '@example.com',
          3,
          'active',
          2,
          3,
          NOW() - ((n + 50) || 'hours')::interval,
          NOW() - ((n + 51) || 'hours')::interval
        FROM generate_series(1,50) AS n;
    ''')

    # Periods for Intro to VR
    op.execute("""
        INSERT INTO period (name, description, instructor_id, location_url, capacity, category, created_at, updated_at)
        SELECT 
          'VR Period ' || n,
          'Session ' || n || ' for Intro to VR program.',
          (SELECT id FROM public."user" WHERE role_id = 2 LIMIT 1),
          'http://vr.example.com/session' || n,
          20 + n,
          'virtual_reality',
          NOW() - (n || ' days')::interval,
          NOW() - ((n - 1) || ' days')::interval
        FROM generate_series(1,10) AS n;
    """)

    # Periods for Data Science 101
    op.execute("""
        INSERT INTO period (name, description, instructor_id, location_url, capacity, category, created_at, updated_at)
        SELECT 
          'DS Period ' || n,
          'Session ' || n || ' for Data Science 101 program.',
          (SELECT id FROM public."user" WHERE role_id = 2 OFFSET 1 LIMIT 1),
          'http://ds.example.com/session' || n,
          25 + n,
          'learning_course',
          NOW() - (n || ' days')::interval,
          NOW() - ((n - 1) || ' days')::interval
        FROM generate_series(1,10) AS n;
    """)


def downgrade() -> None:
    # Remove seed data in reverse order
    op.execute("DELETE FROM period;")
    op.execute('DELETE FROM public."user";')
    op.execute("DELETE FROM cohort_subgroup;")
    op.execute("DELETE FROM cohort;")
    op.execute("DELETE FROM program;")
    op.execute("DELETE FROM system_role;")