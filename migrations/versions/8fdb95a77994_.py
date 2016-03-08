"""Real Name을 위한 초석입니다! 단계 3. 나머지 Column들을 삭제합니다.

Revision ID: 8fdb95a77994
Revises: 57a8604ea770
Create Date: 2016-03-02 13:41:20.351077

"""

# revision identifiers, used by Alembic.
revision = '8fdb95a77994'
down_revision = '57a8604ea770'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_name_en')
        batch_op.drop_column('middle_name_en')
        batch_op.drop_column('first_name_kr')
        batch_op.drop_column('first_name_en')
        batch_op.drop_column('last_name_kr')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_name_kr', mysql.VARCHAR(length=50), nullable=False, server_default=""))
        batch_op.add_column(sa.Column('first_name_en', mysql.VARCHAR(length=50), nullable=False, server_default=""))
        batch_op.add_column(sa.Column('first_name_kr', mysql.VARCHAR(length=50), nullable=False, server_default=""))
        batch_op.add_column(sa.Column('middle_name_en', mysql.VARCHAR(length=50), nullable=True))
        batch_op.add_column(sa.Column('last_name_en', mysql.VARCHAR(length=50), nullable=False, server_default=""))
    ### end Alembic commands ###
