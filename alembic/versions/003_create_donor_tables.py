"""create donor tables

Revision ID: 003
Revises: 002
Create Date: 2026-02-06 18:28:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE bloodtype AS ENUM ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE availabilitystatus AS ENUM ('available', 'unavailable', 'recently_donated');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE registrationstatus AS ENUM ('pending', 'approved', 'rejected');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    
    op.create_table(
        'donor_registrations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('contact_number', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('blood_type', sa.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', name='bloodtype'), nullable=False),
        sa.Column('municipality', sa.String(), nullable=False),
        sa.Column('availability', sa.Enum('available', 'unavailable', 'recently_donated', name='availabilitystatus'), nullable=False),
        sa.Column('status', sa.Enum('pending', 'approved', 'rejected', name='registrationstatus'), nullable=False),
        sa.Column('review_reason', sa.Text(), nullable=True),
        sa.Column('reviewed_by', sa.Integer(), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['reviewed_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_donor_registrations_contact_number'), 'donor_registrations', ['contact_number'], unique=False)
    
    op.create_table(
        'donor_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('registration_id', sa.Integer(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('blood_type', sa.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', name='bloodtype'), nullable=False),
        sa.Column('municipality', sa.String(), nullable=False),
        sa.Column('availability', sa.Enum('available', 'unavailable', 'recently_donated', name='availabilitystatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['registration_id'], ['donor_registrations.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_donor_profiles_user_id'), 'donor_profiles', ['user_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_donor_profiles_user_id'), table_name='donor_profiles')
    op.drop_table('donor_profiles')
    op.drop_index(op.f('ix_donor_registrations_contact_number'), table_name='donor_registrations')
    op.drop_table('donor_registrations')
    op.execute('DROP TYPE bloodtype')
    op.execute('DROP TYPE availabilitystatus')
    op.execute('DROP TYPE registrationstatus')
