from models import *

user1 = User(id=1,
             firstname='test',
             lastname='test',
             email='test@localhost',
             password='test',
             role='customuser'
             )
film1 = Films(id=1,
              name='test',
              genre='test',
              duration=120.5,
              rating=4.5,
              release_date='2005-11-11'
              )
schelude1 = Schelude(id=1,
                     num_of_movies=1
                     )
session1 = Sessions(id=1,
                   sch_id=1,
                   showtime=260,
                   num_of_sessions=2
                   )
visiting1 = Visiting(id=1,
                     sch_id=1,
                     num_of_people=50
                     )
hasfilms1 = ScheludeHasFilms(schelude_id=1,
                            films_id=1)
hasusers1 = ScheludeHasUsers(schelude_id=1,
                            user_id=1)

session.add(user1)
session.add(film1)
session.add(schelude1)
session.commit()

session.add(session1)
session.add(visiting1)
session.add(hasfilms1)
session.add(hasusers1)
session.commit()