from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models import *



def create_entry(model_class, commit=True, **kwargs):
    session = SessionFactory()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return session.query(model_class).filter_by(**kwargs).one()


def get_entry_by_id(model_class, id, **kwargs):
	session = SessionFactory()
	return session.query(model_class).filter_by(id=id, **kwargs).one()


def update_entry(entry, *, commit=True, **kwargs):
	session = SessionFactory()
	for key, value in kwargs.items():
		setattr(entry, key, value)
	if commit:
		session.commit()
	return entry


def delete_entry(model_class, id, *, commit=True, **kwargs):
    session = SessionFactory()
    session.query(model_class).filter_by(id=id, **kwargs).delete()
    if commit:
        session.commit()



def create_entry_wallet(model_class, commit=True, **kwargs):
    session = SessionFactory()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return []


def create_entry_transfer(model_class, commit=True, **kwargs):
    session = SessionFactory()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return []


def get_entry_by_user_id(model_class, from_user_id, **kwargs):
    session = SessionFactory()
    return session.query(model_class).filter_by(from_user_id=from_user_id, **kwargs).all()


def get_entry_by_status(model_class, status, **kwargs):
    session = SessionFactory()
    return session.query(model_class).filter_by(status=status, **kwargs).all()


def get_entry_scalar(model_class, id):
	session = SessionFactory()
	return session.query(model_class).filter_by(id=id).scalar()

#def get_entry_by_currency(model_class, currency, **kwargs):
#    session = SessionFactory()
#    return session.query(model_class).filter_by(currency=currency, **kwargs).all()