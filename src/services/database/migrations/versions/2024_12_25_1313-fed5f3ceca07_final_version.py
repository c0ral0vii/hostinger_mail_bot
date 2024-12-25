"""final version

Revision ID: fed5f3ceca07
Revises: 6bc15acf2576
Create Date: 2024-12-25 13:13:58.022126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fed5f3ceca07'
down_revision: Union[str, None] = '6bc15acf2576'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
