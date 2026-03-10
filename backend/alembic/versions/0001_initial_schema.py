"""initial schema

Revision ID: 0001
Revises: 
Create Date: 2026-03-10

Creates all tables:
  users, sessions, campuses, divisions, campus_buildings,
  rooms, students, lecturers, tests, student_tests
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── users ──────────────────────────────────────────────────────────────────
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_number', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_system_admin', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_id_number', 'users', ['id_number'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # ── sessions ───────────────────────────────────────────────────────────────
    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_sessions_id', 'sessions', ['id'], unique=False)
    op.create_index('ix_sessions_token', 'sessions', ['token'], unique=True)

    # ── campuses ───────────────────────────────────────────────────────────────
    op.create_table(
        'campuses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('address_details', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_campuses_id', 'campuses', ['id'], unique=False)

    # ── divisions ──────────────────────────────────────────────────────────────
    op.create_table(
        'divisions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campus_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['campus_id'], ['campuses.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_divisions_id', 'divisions', ['id'], unique=False)

    # ── campus_buildings ───────────────────────────────────────────────────────
    op.create_table(
        'campus_buildings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campus_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['campus_id'], ['campuses.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_campus_buildings_id', 'campus_buildings', ['id'], unique=False)

    # ── rooms ──────────────────────────────────────────────────────────────────
    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('building_id', sa.Integer(), nullable=False),
        sa.Column('room_number', sa.String(), nullable=False),
        sa.Column('room_type', sa.String(), nullable=True),
        sa.Column('capacity', sa.Integer(), nullable=True),
        sa.Column('is_available', sa.Boolean(), nullable=True),
        sa.Column('available_from', sa.Time(), nullable=True),
        sa.Column('available_until', sa.Time(), nullable=True),
        sa.ForeignKeyConstraint(['building_id'], ['campus_buildings.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_rooms_id', 'rooms', ['id'], unique=False)

    # ── students ───────────────────────────────────────────────────────────────
    op.create_table(
        'students',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('division_id', sa.Integer(), nullable=True),
        sa.Column('enrollment_year', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['division_id'], ['divisions.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
    )
    op.create_index('ix_students_id', 'students', ['id'], unique=False)

    # ── lecturers ──────────────────────────────────────────────────────────────
    op.create_table(
        'lecturers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('division_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('office_hours', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['division_id'], ['divisions.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
    )
    op.create_index('ix_lecturers_id', 'lecturers', ['id'], unique=False)

    # ── tests ──────────────────────────────────────────────────────────────────
    op.create_table(
        'tests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_name', sa.String(), nullable=False),
        sa.Column('date_time', sa.DateTime(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=True),
        sa.Column('lecturer_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['room_id'], ['rooms.id']),
        sa.ForeignKeyConstraint(['lecturer_id'], ['lecturers.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_tests_id', 'tests', ['id'], unique=False)

    # ── student_tests ──────────────────────────────────────────────────────────
    op.create_table(
        'student_tests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('test_id', sa.Integer(), nullable=False),
        sa.Column('is_registered', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['student_id'], ['students.id']),
        sa.ForeignKeyConstraint(['test_id'], ['tests.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_student_tests_id', 'student_tests', ['id'], unique=False)


def downgrade() -> None:
    op.drop_table('student_tests')
    op.drop_table('tests')
    op.drop_table('lecturers')
    op.drop_table('students')
    op.drop_table('rooms')
    op.drop_table('campus_buildings')
    op.drop_table('divisions')
    op.drop_table('campuses')
    op.drop_table('sessions')
    op.drop_table('users')
