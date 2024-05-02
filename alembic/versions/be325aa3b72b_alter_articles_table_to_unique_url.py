"""alter articles table to unique url

Revision ID: be325aa3b72b
Revises: 6c1de027cd7c
Create Date: 2024-04-15 13:02:16.290701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be325aa3b72b'
down_revision: Union[str, None] = '6c1de027cd7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('uniq_url', 'articles', ['url'])


def downgrade() -> None:
    op.drop_constraint('uniq_url', 'articles')
