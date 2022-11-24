from ast import For
from tokenize import Floatnumber
from xmlrpc.client import Boolean
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

#session = Session()
engine = create_engine(
      "mysql://root:root@localhost/lab5", echo=False)
SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()

session = SessionFactory()

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(45), nullable=False)
    lastname = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    role = Column(Enum('admin', 'customuser'), default='customuser')


class Films(Base):
    __tablename__ = 'Films'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False, unique=True)
    genre = Column(String(45), nullable=False)
    duration = Column(Float, nullable=False)
    rating = Column(Float, nullable=False, default=3.0)
    release_date = Column(Date, nullable=False)


class Schelude(Base):
    __tablename__ = 'Schelude'

    id = Column(Integer, primary_key=True, autoincrement=True)
    num_of_movies = Column(Integer, nullable=False, default=0)


class Sessions(Base):
    __tablename__ = 'Sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sch_id = Column(Integer, ForeignKey("Schelude.id"), primary_key=True)
    showtime = Column(Float, nullable=False, default=0.0)
    num_of_sessions = Column(Integer, nullable=False, default=0)


class Visiting(Base):
    __tablename__ = 'Visiting'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sch_id = Column(Integer, ForeignKey("Schelude.id"), primary_key=True)
    num_of_people = Column(Integer, nullable=False, default=0)


class ScheludeHasFilms(Base):
    __tablename__ = 'schelude_has_films'
    schelude_id = Column(Integer, ForeignKey("Schelude.id"), primary_key=True)
    films_id = Column(Integer, ForeignKey("Films.id"), primary_key=True)


class ScheludeHasUsers(Base):
    __tablename__ = 'schelude_has_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    schelude_id = Column(Integer, ForeignKey("Schelude.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"), primary_key=True)

Base.metadata.create_all(engine)