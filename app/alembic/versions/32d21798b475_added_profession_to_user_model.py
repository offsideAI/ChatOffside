"""Added Profession to User model

Revision ID: 32d21798b475
Revises: d4ad2f800764
Create Date: 2023-04-07 02:12:26.903299

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '32d21798b475'
down_revision = 'd4ad2f800764'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profession', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'profession')
    # ### end Alembic commands ###
