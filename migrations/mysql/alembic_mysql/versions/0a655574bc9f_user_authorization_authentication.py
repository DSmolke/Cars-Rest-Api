"""User, authorization, authentication

Revision ID: 0a655574bc9f
Revises: 
Create Date: 2023-12-02 17:04:58.801710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a655574bc9f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
    'users',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('username', sa.String(255)),
    sa.Column('password', sa.String(255)),
    sa.Column('email', sa.String(255)),
    sa.Column('role', sa.String(10)),
    sa.Column('active', sa.Boolean, default=False)
    )


def downgrade() -> None:
    op.drop_table('users')

