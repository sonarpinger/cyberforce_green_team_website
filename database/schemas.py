from sqlalchemy import and_
from .models import User, ContactForm

def authenticate_user(db, username, hashed_password):
  return db.query(User).filter(and_(User.username == username, User.password == hashed_password)).first()

def create_user(db, username, hashed_password, is_admin=False):
  u = User(username=username, password=hashed_password, is_admin=is_admin)
  db.add(u)
  db.commit()
  return u

def is_admin(db, username):
  return db.query(User).filter(User.username == username).first().is_admin

def create_form(db, name, email, phone, message):
  c = ContactForm(name=name, email=email, phone=phone, message=message)
  db.add(c)
  db.commit()
  return c

def get_forms(db):
  return db.query(ContactForm).all()