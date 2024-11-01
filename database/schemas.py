from sqlalchemy import and_
from .models import User, ContactForm

def get_hash_for_user(db, username):
  try:
    return db.query(User).filter(User.username == username).first().password
  except AttributeError:
    return None

def create_user(db, username, hashed_password, is_admin=False):
  u = User(username=username, password=hashed_password, is_admin=is_admin)
  db.add(u)
  db.commit()
  return u

def is_admin(db, username):
  try:
    return db.query(User).filter(User.username == username).first().is_admin
  except AttributeError:
    return False

def create_form(db, name, email, phone, message):
  c = ContactForm(name=name, email=email, phone=phone, message=message)
  db.add(c)
  db.commit()
  return c

def get_forms(db):
  return db.query(ContactForm).all()

def get_users(db):
  # dont return hashed passwords, filter out on backend
  return db.query(User).all()

def delete_user(db, username):
  db.query(User).filter(User.username == username).delete()
  db.commit()
  return

def delete_all_forms(db):
  db.query(ContactForm).delete()
  db.commit()
  return

def toggle_user_flag(db, username):
  try:
    u = db.query(User).filter(User.username == username).first()
    u.is_flagged = not u.is_flagged
    db.commit()
    return u.is_flagged
  except AttributeError:
    return False