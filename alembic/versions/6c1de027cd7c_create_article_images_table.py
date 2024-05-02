"""create article_images table

Revision ID: 6c1de027cd7c
Revises: cbb69db2fc2e
Create Date: 2024-04-10 19:24:18.093310

"""
from datetime import datetime
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql.functions import current_timestamp
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6c1de027cd7c'
down_revision: Union[str, None] = 'cbb69db2fc2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'article_images',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('article_id', sa.Integer, sa.ForeignKey("articles.id", ondelete="CASCADE")),
        sa.Column('url', sa.Unicode(255), nullable=False),
        sa.Column('image', sa.LargeBinary, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=current_timestamp()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=current_timestamp(), onupdate=datetime.now),
    )


def downgrade() -> None:
    op.drop_table('article_images')
