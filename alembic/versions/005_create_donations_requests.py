"""create donations and blood requests tables

Revision ID: 005
Revises: 004
Create Date: 2026-02-06 18:28:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '005'
down_revision: Union[str, None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE urgencylevel AS ENUM ('low', 'medium', 'high', 'critical')")
    
    op.create_table(
        'donations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('donor_profile_id', sa.Integer(), nullable=False),
        sa.Column('donation_date', sa.Date(), nullable=False),
        sa.Column('blood_type', sa.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', name='bloodtype'), nullable=False),
        sa.Column('units', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['donor_profile_id'], ['donor_profiles.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'blood_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('patient_name', sa.String(), nullable=False),
        sa.Column('blood_type', sa.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', name='bloodtype'), nullable=False),
        sa.Column('units_needed', sa.Integer(), nullable=False),
        sa.Column('urgency', sa.Enum('low', 'medium', 'high', 'critical', name='urgencylevel'), nullable=False),
        sa.Column('hospital', sa.String(), nullable=False),
        sa.Column('contact_number', sa.String(), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('blood_requests')
    op.drop_table('donations')
    op.execute('DROP TYPE urgencylevel')
