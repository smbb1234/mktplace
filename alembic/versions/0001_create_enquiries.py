"""create enquiries table

Revision ID: 0001_create_enquiries
Revises: 
Create Date: 2026-05-09 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_enquiries'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'enquiries',
        sa.Column('enquiry_id', sa.String(), primary_key=True),
        sa.Column('session_id', sa.String(), nullable=True),
        sa.Column('vehicle_id', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=False),
        sa.Column('preferred_contact_method', sa.String(), nullable=True),
        sa.Column('preferred_contact_time', sa.String(), nullable=True),
        sa.Column('monthly_budget_gbp', sa.Integer(), nullable=True),
        sa.Column('deposit_gbp', sa.Integer(), nullable=True),
        sa.Column('buying_timeframe', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True, server_default=sa.text("'New'")),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('enquiries')
