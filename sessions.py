from models import User, Wallet, Transfer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

#session = Session()
engine = create_engine(
      "mysql://root:root@localhost/lab5")
SessionFactory = sessionmaker(bind=engine)
session = Session(engine)

user1 = User(id=1,username='sgt_pepper',first_name='Oleh',last_name='Chovhaniuk',email='olehchovhaniuk@gmail.com',password='password12345',phone='+380943461234')
user2 = User(id=2,username='galaher',first_name='Ihor',last_name='Chernel',email='ihorko@gmail.com',password='qwerty12345',phone='+380946851234')

wallet1 = Wallet(id=1, money=346.,name='wallet1',currency='USD',status='active',user_id=user2.id)
wallet2 = Wallet(id=2, money=1056.,name='wallet2',currency='UAH',status='active',user_id=user1.id)

transfer1 = Transfer(id=1,money=34.,currency='EUR',complete=False,from_user_id=user1.id,from_wallet_id=wallet1.id,to_wallet_id=wallet2.id)
transfer2 = Transfer(id=2,money=433.,currency='UAH',complete=True,from_user_id=user2.id,from_wallet_id=wallet2.id,to_wallet_id=wallet1.id)

session.add(user1)
session.add(user2)
session.commit()
session.add(wallet1)
session.add(wallet2)
session.commit()
session.add(transfer1)
session.add(transfer2)
session.commit()