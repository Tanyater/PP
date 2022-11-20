"""create tables
Revision ID: 67c53ff764b2
Revises:
Create Date: 2022-10-25 19:38:29.439691
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy import Enum
from sqlalchemy import Boolean
# revision identifiers, used by Alembic.
revision = '67c53ff764b2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        Column('id', Integer, primary_key = True),
        Column('username', String(45), unique = True),
        Column('first_name', String(45)),
        Column('last_name', String(45)),
        Column('email', String(45), unique = True),
        Column('password', String(100)),
        Column('phone', String(45)),
    )

    op.create_table(
        'wallet',
        Column('id', Integer, primary_key = True),
        Column('money', Float),
        Column('name', String(45), default = 'Wallet'),
        Column('currency', Enum('EUR','USD','UAH'), default = 'UAH'),
        Column('status', Enum('active', 'blocked'), default = 'active'),
        Column('user_id', Integer, ForeignKey("user.id"))
    )

    op.create_table(
        'transfer',
        Column('id',Integer,primary_key = True),
        Column('money', Float),
        Column('currency',Enum('EUR','USD','UAH'), default = 'UAH'),
        Column('complete', Boolean, default = False),
        Column('from_user_id',Integer,ForeignKey("user.id"), nullable = False),
        Column('from_wallet_id', Integer, ForeignKey("wallet.id"), nullable = False),
        Column('to_wallet_id', Integer, ForeignKey("wallet.id"), nullable = False)
    )

def downgrade() -> None:
    pass