"""seed_default_irs_rates

Revision ID: 6e54ed232b7d
Revises: 1eb993c8e081
Create Date: 2025-11-10 14:02:56.683318

"""
from typing import Sequence, Union
import uuid
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '6e54ed232b7d'
down_revision: Union[str, Sequence[str], None] = '1eb993c8e081'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed default IRS rate customization and categories."""
    
    rate_customizations = sa.table(
        'rate_customizations',
        sa.column('id', UUID),
        sa.column('name', sa.String),
        sa.column('description', sa.Text),
        sa.column('year', sa.Integer),
        sa.column('created_at', sa.DateTime)
    )
    
    rate_categories = sa.table(
        'rate_categories',
        sa.column('id', UUID),
        sa.column('name', sa.String),
        sa.column('cost_per_mile', sa.DOUBLE_PRECISION),
        sa.column('rate_customization_id', UUID),
        sa.column('created_at', sa.DateTime)
    )
    
    
    irs_customization_id = uuid.uuid4()
    current_time = datetime.utcnow()
    
    op.bulk_insert(rate_customizations, [
        {
            'id': irs_customization_id,
            'name': 'IRS Standard Rates',
            'description': 'Official IRS standard mileage rates for business use',
            'year': 2025, 
            'created_at': current_time
        }
    ])
    
    
    op.bulk_insert(rate_categories, [
        {
            'id': uuid.uuid4(),
            'name': 'Business use',
            'cost_per_mile': 0.70,
            'rate_customization_id': irs_customization_id,
            'created_at': current_time
        },
        {
            'id': uuid.uuid4(),
            'name': 'Medical or military moving',
            'cost_per_mile': 0.21,
            'rate_customization_id': irs_customization_id,
            'created_at': current_time
        },
        {
            'id': uuid.uuid4(),
            'name': 'Charity use',
            'cost_per_mile': 0.14,
            'rate_customization_id': irs_customization_id,
            'created_at': current_time
        }
    ])


def downgrade() -> None:
    """Remove seeded IRS rate data."""
    
    op.execute(
        "DELETE FROM rate_customizations WHERE name = 'IRS Standard Rates'"
    )
