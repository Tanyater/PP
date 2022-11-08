from models import User, Notes, Change
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

engine = create_engine("mysql://root:root@localhost/lab5")

SessionFactory = sessionmaker(bind=engine)
session = Session(engine)

user1 = User(id=1, username='vanya', first_name='Roma', last_name='Lask', email='tracktor@gmail.com', password='1234', notes_count=7)
user2 = User(id=2, username='tanya', first_name='Danya', last_name='Nazarova', email='nazarova@gmail.com', password='4321', notes_count=5)

notes1 = Notes(id=1, title='wow', content='hi', notescol='123', access='yes', user_iduser=1)
notes2 = Notes(id=2, title='leave', content='hello', notescol='412', access='yes', user_iduser=2)

change1 = Change(id=1, username='vanya', time='2022-11-02', notes_idnotes=1, user_iduser=1)
change2 = Change(id=2, username='tanya', time='2022-12-03', notes_idnotes=2, user_iduser=2)

#session.add(user1)
#session.add(user2)
#session.commit()
session.add(notes1)
session.add(notes2)
session.commit()
session.add(change1)
session.add(change2)
session.commit()