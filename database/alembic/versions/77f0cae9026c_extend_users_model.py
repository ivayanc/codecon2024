"""Extend users model

Revision ID: 77f0cae9026c
Revises: ec65d5341c21
Create Date: 2024-04-13 13:26:54.456467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77f0cae9026c'
down_revision: Union[str, None] = 'ec65d5341c21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('birthday_date', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('region', sa.String(), nullable=True))
    op.add_column('users', sa.Column('city', sa.String(), nullable=True))
    op.add_column('users', sa.Column('street', sa.String(), nullable=True))
    op.add_column('users', sa.Column('house_number', sa.String(), nullable=True))
    op.add_column('users', sa.Column('flat_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'flat_number')
    op.drop_column('users', 'house_number')
    op.drop_column('users', 'street')
    op.drop_column('users', 'city')
    op.drop_column('users', 'region')
    op.drop_column('users', 'birthday_date')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    # ### end Alembic commands ###