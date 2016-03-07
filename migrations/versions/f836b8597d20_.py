"""Real Name을 위한 초석입니다! 단계 1. 새로이 이름이 들어갈 자리를 만듭니다.

Revision ID: f836b8597d20
Revises: 03755072666d
Create Date: 2016-03-02 12:23:51.327823

"""

# revision identifiers, used by Alembic.
revision = 'f836b8597d20'
down_revision = '03755072666d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('realname', sa.String(length=50), nullable=False, server_default=''))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('realname')
    ### end Alembic commands ###
