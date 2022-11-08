from ast import For
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
	__tablename__ = "user"
	id = Column(Integer, primary_key=True)
	username = Column(String(45), unique=True)
	first_name = Column(String(45))
	last_name = Column(String(45))
	email = Column(String(45), unique=True)
	password = Column(String(45))
	notes_count = Column(Integer)


class Notes(Base):
	__tablename__ = "notes"
	id = Column(Integer, primary_key=True)
	title = Column(String(45))
	content = Column(String(45))
	notescol = Column(String(45))
	access = Column(String(45))
	user_iduser = Column(Integer, ForeignKey("user.id"), nullable=False)


class Change(Base):
	__tablename__ = "change"
	id = Column(Integer, primary_key=True)
	username = Column(String(45))
	time = Column(Date)
	notes_idnotes = Column(Integer, ForeignKey("notes.id"), nullable=False)
	user_iduser = Column(Integer, ForeignKey("user.id"), nullable=False)