"""alembic

Revision ID: b595f4a104da
Revises: 
Create Date: 2022-11-03 18:36:47.659743

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Date
# revision identifiers, used by Alembic.
revision = 'b595f4a104da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        Column('id', Integer, primary_key=True),
        Column('username', String(45), unique=True),
        Column('first_name', String(45)),
        Column('last_name', String(45)),
        Column('email', String(45), unique=True),
        Column('password', String(45)),
        Column('notes_count', Integer)
    )
    op.create_table(
        'notes',
        Column('id', Integer, primary_key=True),
        Column('title', String(45)),
        Column('content', String(45)),
        Column('notescol', String(45)),
        Column('access', String(45)),
        Column('user_iduser', Integer, ForeignKey("user.id"), nullable=False)
    )
    op.create_table(
        'change',
        Column('id', Integer, primary_key=True),
        Column('username', String(45)),
        Column('time', Date),
        Column('notes_idnotes', Integer, ForeignKey("notes.id"), nullable=False),
        Column('user_iduser', Integer, ForeignKey("user.id"), nullable=False)
    )


def downgrade() -> None:
    pass
