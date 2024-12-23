"""upgrade date column

Revision ID: 1343561f3332
Revises: 919128a8becc
Create Date: 2024-12-11 17:17:40.724126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1343561f3332'
down_revision: Union[str, None] = '919128a8becc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('invoice_day', sa.Date(), nullable=False))
    op.alter_column('users', 'need_pay_date',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Date(),
               existing_nullable=False)
    op.alter_column('users', 'activated_date',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Date(),
               existing_nullable=False)
    op.drop_column('users', 'pay_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('pay_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.alter_column('users', 'activated_date',
               existing_type=sa.Date(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.alter_column('users', 'need_pay_date',
               existing_type=sa.Date(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.drop_column('users', 'invoice_day')
    # ### end Alembic commands ###