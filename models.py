from ast import For
from tokenize import Floatnumber
from xmlrpc.client import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

engine = create_engine(
      "mysql://root:root@localhost/lab5", echo=False)
SessionFactory = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	username = Column(String(45), unique=True)
	first_name = Column(String(45))
	last_name = Column(String(45))
	email = Column(String(45), unique=True)
	password = Column(String(100))
	phone = Column(String(45))


class Wallet(Base):
	__tablename__ = "wallet"

	id = Column(Integer, primary_key=True)
	money = Column(Float)
	name = Column(String(45), default='Wallet')
	currency = Column(Enum('EUR', 'USD', 'UAH'), default='UAH')
	status = Column(Enum('active', 'blocked'), default='active')
	user_id = Column(Integer, ForeignKey("user.id"))


class Transfer(Base):
	__tablename__ = "transfer"

	id = Column(Integer, primary_key=True)
	money = Column(Float)
	currency = Column(Enum('EUR', 'USD', 'UAH'), default='UAH')
	complete = Column(Boolean, default=False)
	from_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
	from_wallet_id = Column(Integer, ForeignKey("wallet.id"), nullable=False)
	to_wallet_id = Column(Integer, ForeignKey("wallet.id"), nullable=False)
