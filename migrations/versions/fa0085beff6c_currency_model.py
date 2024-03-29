"""Currency model

Revision ID: fa0085beff6c
Revises: 
Create Date: 2024-02-23 03:39:26.752469

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'fa0085beff6c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currencies',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=False), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('name'),
    sa.UniqueConstraint('code')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('currencies')
    # ### end Alembic commands ###
