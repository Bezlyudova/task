"""data3

Revision ID: c6420967ca4d
Revises: 26235ae49f5a
Create Date: 2024-06-08 17:44:31.002124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6420967ca4d'
down_revision: Union[str, None] = '26235ae49f5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('priority', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'priority')
    # ### end Alembic commands ###