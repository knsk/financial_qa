"""create articles table

Revision ID: cbb69db2fc2e
Revises: 
Create Date: 2024-04-10 19:08:49.061052

"""
from datetime import datetime
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql.functions import current_timestamp
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = 'cbb69db2fc2e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'articles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.Unicode(255), nullable=False),
        sa.Column('url', sa.Unicode(255), nullable=False),
        sa.Column('text', sa.Text, default=None),
        sa.Column('published_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=current_timestamp()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=current_timestamp(), onupdate=datetime.now),
    )


def downgrade() -> None:
    op.drop_table('articles')

