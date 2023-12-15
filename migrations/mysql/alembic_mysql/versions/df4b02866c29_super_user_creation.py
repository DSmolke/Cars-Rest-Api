"""super user creation

Revision ID: df4b02866c29
Revises: 0a655574bc9f
Create Date: 2023-12-15 07:59:18.561589

"""
from typing import Sequence, Union
from werkzeug.security import generate_password_hash

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'df4b02866c29'
down_revision: Union[str, None] = '0a655574bc9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        f"INSERT INTO users (username, password, email, role, active) VALUES ('SUPER_USER', '{generate_password_hash('SUPER_USER')}', 'SU@GMAIL.COM','ADMIN' ,1)")


def downgrade() -> None:
    op.execute("DELETE FROM users WHERE username = 'SUPER_USER'")
